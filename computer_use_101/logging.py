"""Weights & Biases logging for RL training runs."""

import wandb


class RunLogger:
    def __init__(self, run: wandb.sdk.wandb_run.Run):
        self._run = run

    def log_episode(self, episode, reward, length, epsilon, loss=None):
        payload = {
            "episode": episode,
            "episode_reward": reward,
            "episode_length": length,
            "epsilon": epsilon,
        }
        if loss is not None:
            payload["loss"] = loss
        self._run.log(payload, step=episode)

    def log_summary(self, episode, avg_reward, avg_length, win_rate, epsilon):
        self._run.log(
            {
                "avg_reward": avg_reward,
                "avg_length": avg_length,
                "win_rate": win_rate,
                "epsilon": epsilon,
            },
            step=episode,
        )

    def finish(self):
        self._run.finish()
