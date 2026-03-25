"""Pixel-based DQN for Minesweeper. Validates that RL can learn from raw screenshots."""

import json
import random
from collections import deque
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from computer_use_101.logging import RunLogger
from computer_use_101.minesweeper.env import MinesweeperEnv
from computer_use_101.minesweeper.reward import RewardConfig


class ConvDQN(nn.Module):
    def __init__(self, h, w, n_actions):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=5, stride=2),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=5, stride=2),
            nn.ReLU(),
            nn.Conv2d(32, 32, kernel_size=3, stride=2),
            nn.ReLU(),
        )
        dummy = torch.zeros(1, 3, h, w)
        conv_out = self.conv(dummy).view(1, -1).size(1)
        self.head = nn.Sequential(
            nn.Linear(conv_out, 128),
            nn.ReLU(),
            nn.Linear(128, n_actions),
        )

    def forward(self, x):
        x = self.conv(x)
        return self.head(x.view(x.size(0), -1))


class ReplayBuffer:
    def __init__(self, capacity):
        self.buf = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buf.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buf, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            torch.stack(states),
            torch.tensor(actions, dtype=torch.long),
            torch.tensor(rewards, dtype=torch.float32),
            torch.stack(next_states),
            torch.tensor(dones, dtype=torch.float32),
        )

    def __len__(self):
        return len(self.buf)


def obs_to_tensor(obs):
    return torch.from_numpy(obs).permute(2, 0, 1).float() / 255.0


def train(args, logger: RunLogger):
    device = args.device
    reward_cfg = args.reward

    reward_config = RewardConfig(
        bomb=reward_cfg["bomb"],
        reveal_one=reward_cfg["reveal_one"],
        reveal_flood=reward_cfg["reveal_flood"],
        win=reward_cfg["win"],
        already_revealed=reward_cfg["already_revealed"],
    )
    env = MinesweeperEnv(rows=args.rows, cols=args.cols, mines=args.mines, reward_config=reward_config)
    n_actions = env.action_space.n
    h, w = env.observation_space.shape[:2]

    policy_net = ConvDQN(h, w, n_actions).to(device)
    target_net = ConvDQN(h, w, n_actions).to(device)
    target_net.load_state_dict(policy_net.state_dict())

    optimizer = optim.Adam(policy_net.parameters(), lr=args.lr)
    replay = ReplayBuffer(args.buffer_size)

    epsilon = args.eps_start
    eps_decay = (args.eps_start - args.eps_end) / args.eps_decay_steps

    episode_rewards = []
    episode_lengths = []
    best_avg = float("-inf")
    log_path = Path(args.log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    for ep in range(args.episodes):
        obs, _ = env.reset(seed=ep)
        state = obs_to_tensor(obs).to(device)
        total_reward = 0.0
        steps = 0

        while True:
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                with torch.no_grad():
                    action = policy_net(state.unsqueeze(0)).argmax(1).item()

            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            next_state = obs_to_tensor(obs).to(device)

            replay.push(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            steps += 1

            if len(replay) >= args.batch_size:
                s, a, r, ns, d = replay.sample(args.batch_size)
                s, a, r, ns, d = s.to(device), a.to(device), r.to(device), ns.to(device), d.to(device)

                q_values = policy_net(s).gather(1, a.unsqueeze(1)).squeeze(1)
                with torch.no_grad():
                    next_q = target_net(ns).max(1).values
                    target_q = r + args.gamma * next_q * (1 - d)

                loss = nn.functional.smooth_l1_loss(q_values, target_q)
                optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(policy_net.parameters(), 1.0)
                optimizer.step()

            if done:
                break

        epsilon = max(args.eps_end, epsilon - eps_decay)
        episode_rewards.append(total_reward)
        episode_lengths.append(steps)
        logger.log_episode(ep, total_reward, steps, epsilon)

        if (ep + 1) % args.target_update == 0:
            target_net.load_state_dict(policy_net.state_dict())

        if (ep + 1) % args.log_every == 0:
            recent = episode_rewards[-args.log_every :]
            avg_r = np.mean(recent)
            avg_len = np.mean(episode_lengths[-args.log_every :])
            win_rate = sum(1 for r in recent if r > 0) / len(recent)
            logger.log_summary(ep, avg_r, avg_len, win_rate, epsilon)
            print(
                f"ep {ep + 1:>5} | avg_r {avg_r:>7.1f} | avg_len {avg_len:>5.1f} | "
                f"win% {win_rate:>5.1%} | eps {epsilon:.3f}"
            )
            if avg_r > best_avg:
                best_avg = avg_r
                torch.save(policy_net.state_dict(), log_path / "best_model.pt")

    env.close()

    metrics = {
        "episode_rewards": episode_rewards,
        "episode_lengths": episode_lengths,
    }
    with open(log_path / "metrics.json", "w") as f:
        json.dump(metrics, f)

    torch.save(policy_net.state_dict(), log_path / "final_model.pt")
    print(f"\nDone. Metrics saved to {log_path / 'metrics.json'}")
