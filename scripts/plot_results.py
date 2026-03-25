"""Plot DQN training curve with random baseline comparison."""

import argparse
import json
from pathlib import Path

import numpy as np


def smooth(values, window=50):
    if len(values) < window:
        return values
    return np.convolve(values, np.ones(window) / window, mode="valid").tolist()


def plot(metrics_path, output_path=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed. Install with: pip install matplotlib")
        print("Falling back to text summary.\n")
        return text_summary(metrics_path)

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


def text_summary(metrics_path):
    with open(metrics_path) as f:
        data = json.load(f)

    rewards = data["episode_rewards"]
    n = len(rewards)
    early = rewards[: min(50, n)]
    late = rewards[max(0, n - 50) :]

    print(f"Episodes: {n}")
    print(f"Early avg reward (first 50):  {np.mean(early):.1f}")
    print(f"Late avg reward (last 50):    {np.mean(late):.1f}")
    print(f"Improvement:                  {np.mean(late) - np.mean(early):+.1f}")
    print(f"Best episode:                 {max(rewards):.1f}")
    print(f"Late win rate:                {sum(1 for r in late if r > 0) / len(late):.1%}")


def main():
    parser = argparse.ArgumentParser(description="Plot DQN training results")
    parser.add_argument("metrics", type=str, default="runs/dqn/metrics.json", nargs="?")
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()
    plot(args.metrics, args.output)


if __name__ == "__main__":
    main()
