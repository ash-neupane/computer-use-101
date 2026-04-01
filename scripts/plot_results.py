"""Plot DQN training curve with random baseline comparison."""

import json
from pathlib import Path

import click
import matplotlib.pyplot as plt
import numpy as np


def smooth(values, window=50):
    if len(values) < window:
        return values
    return np.convolve(values, np.ones(window) / window, mode="valid").tolist()


def plot(metrics_path, output_path=None):
    with open(metrics_path) as f:
        data = json.load(f)

    rewards = data["episode_rewards"]
    lengths = data["episode_lengths"]
    smoothed_r = smooth(rewards)
    smoothed_l = smooth(lengths)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.plot(rewards, alpha=0.2, color="steelblue", label="per-episode")
    ax1.plot(range(49, 49 + len(smoothed_r)), smoothed_r, color="steelblue", linewidth=2, label="smoothed (50)")
    ax1.axhline(y=np.mean(rewards[:50]), color="red", linestyle="--", alpha=0.7, label="random baseline (first 50 eps)")
    ax1.set_ylabel("Episode Reward")
    ax1.legend()
    ax1.set_title("DQN on Minesweeper Pixels")

    ax2.plot(lengths, alpha=0.2, color="darkorange")
    ax2.plot(range(49, 49 + len(smoothed_l)), smoothed_l, color="darkorange", linewidth=2)
    ax2.set_ylabel("Episode Length")
    ax2.set_xlabel("Episode")

    plt.tight_layout()
    out = Path(output_path) if output_path else Path(metrics_path).parent / "training_curve.png"
    plt.savefig(out, dpi=150)
    print(f"Saved plot to {out}")
    plt.close()


@click.command()
@click.argument("metrics", default="runs/dqn/metrics.json", type=click.Path(exists=True))
@click.option("--output", default=None, type=click.Path(), help="Output path for the plot image")
def main(metrics, output):
    """Plot DQN training results."""
    plot(metrics, output)


if __name__ == "__main__":
    main()
