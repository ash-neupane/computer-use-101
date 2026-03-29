"""Entrypoint for training runs. Initializes all external resources and passes them in."""

from pathlib import Path
from types import SimpleNamespace

import click
import torch
import wandb
from dotenv import load_dotenv

from computer_use_101.config import load_config
from computer_use_101.logging import RunLogger
from scripts.train_dqn import train

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


@click.command()
@click.option("--config", "config_path", default=None, type=click.Path(exists=True), help="Override config JSON path")
@click.option("--episodes", default=None, type=int, help="Override number of episodes")
def main(config_path, episodes):
    """Train DQN on Minesweeper pixels."""
    load_dotenv(ENV_PATH)
    cfg = load_config(config_path)

    if episodes is not None:
        cfg["experiment"]["episodes"] = episodes

    device = torch.device(cfg["device"])
    exp = cfg["experiment"]
    wb = cfg["wandb"]

    run_config = {**exp, "device": str(device), "algo": "dqn", "obs": "pixels"}
    run = wandb.init(
        entity=wb["entity"],
        project=wb["project"],
        config=run_config,
        name=f"dqn_{exp['rows']}x{exp['cols']}_{exp['mines']}m",
        tags=["dqn", "pixels", "baseline"],
    )
    logger = RunLogger(run)

    args = SimpleNamespace(
        rows=exp["rows"],
        cols=exp["cols"],
        mines=exp["mines"],
        episodes=exp["episodes"],
        batch_size=exp["batch_size"],
        buffer_size=exp["buffer_size"],
        lr=exp["lr"],
        gamma=exp["gamma"],
        eps_start=exp["eps_start"],
        eps_end=exp["eps_end"],
        eps_decay_steps=exp["eps_decay_steps"],
        target_update=exp["target_update"],
        log_every=cfg["logging"]["log_every"],
        log_dir=exp["log_dir"],
        device=device,
        reward=cfg["reward"],
    )

    try:
        train(args, logger)
    finally:
        logger.finish()


if __name__ == "__main__":
    main()
