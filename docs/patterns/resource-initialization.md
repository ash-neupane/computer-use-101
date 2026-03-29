# Resource Initialization Pattern

External resources (database clients, W&B runs, API clients, browser instances) must be initialized in the **entrypoint script** and passed into all classes and functions that need them.

## Why

- Makes dependencies explicit — you can see every resource a function needs from its signature.
- Prevents hidden global state and import-time side effects.
- Makes testing trivial — pass a mock instead of the real client.
- Guarantees cleanup — the entrypoint owns the lifecycle with `try/finally`.

## Structure

```
scripts/run.py          ← entrypoint: loads .env, inits wandb/db/browser, calls train()
scripts/train_dqn.py    ← pure logic: receives a RunLogger, never touches wandb directly
computer_use_101/logging.py  ← thin wrapper: RunLogger holds a wandb.Run, exposes log methods
```

## Example

```python
# scripts/run.py — the ONLY place that creates external resources
from dotenv import load_dotenv
import wandb
from computer_use_101.logging import RunLogger
from scripts.train_dqn import train

def main():
    load_dotenv(".env")
    run = wandb.init(project="computer-use-101", config={...})
    logger = RunLogger(run)
    try:
        train(args, logger)
    finally:
        logger.finish()
```

```python
# scripts/train_dqn.py — receives resources, never creates them
def train(args, logger: RunLogger):
    # logger is ready to use, no init needed
    logger.log_episode(ep, reward, length, epsilon)
```

```python
# computer_use_101/logging.py — wrapper, no init logic
class RunLogger:
    def __init__(self, run: wandb.sdk.wandb_run.Run):
        self._run = run

    def log_episode(self, episode, reward, length, epsilon, loss=None):
        self._run.log({...}, step=episode)
```

## Rules

1. **Entrypoint owns the lifecycle.** `load_dotenv()`, `wandb.init()`, `playwright.start()`, DB connections — all live in `run.py` or equivalent.
2. **Library code receives, never creates.** Functions and classes take initialized clients as arguments.
3. **Cleanup in `finally`.** The entrypoint is responsible for closing resources.
4. **No import-time side effects.** Importing a module must never trigger network calls, file reads, or resource allocation.
