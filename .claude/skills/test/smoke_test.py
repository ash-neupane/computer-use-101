import numpy as np

from envs.minesweeper.env import MinesweeperEnv

EPISODES = 100


def main():
    env = MinesweeperEnv(rows=5, cols=5, mines=3)
    rewards, lengths = [], []

    for ep in range(EPISODES):
        _obs, _info = env.reset(seed=ep)
        total_reward, steps, terminated = 0.0, 0, False
        while not terminated:
            action = env.action_space.sample()
            _obs, reward, terminated, _truncated, _info = env.step(action)
            total_reward += reward
            steps += 1
        rewards.append(total_reward)
        lengths.append(steps)

    env.close()

    mean_reward = np.mean(rewards)
    mean_length = np.mean(lengths)
    print(f"Episodes:    {EPISODES}")
    print(f"Mean reward: {mean_reward:.4f} ± {np.std(rewards):.4f}")
    print(f"Mean length: {mean_length:.1f} ± {np.std(lengths):.1f}")

    assert mean_reward < 0, f"Expected negative mean reward for random agent, got {mean_reward}"
    assert mean_length < 25, f"Expected mean length < total cells, got {mean_length}"
    print("PASSED")


if __name__ == "__main__":
    main()
