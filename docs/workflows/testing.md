# Testing Protocol

## E2E Testing — New Blank Slate

Every env must pass this protocol from a clean state before merging.

### 1. Fresh install

```bash
pip install -e ".[dev]"
playwright install chromium
```

### 2. Unit tests

```bash
pytest tests/ -v
```

All tests must pass. No skips unless documented.

### 3. Lint

```bash
ruff check .
```

Zero violations.

### 4. Random agent smoke test

Run 100 episodes with a random agent. Print mean reward and episode length.

```python
from envs.minesweeper.env import MinesweeperEnv
import numpy as np

env = MinesweeperEnv()
rewards, lengths = [], []
for ep in range(100):
    obs, info = env.reset(seed=ep)
    total_reward, steps, terminated = 0.0, 0, False
    while not terminated:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        steps += 1
    rewards.append(total_reward)
    lengths.append(steps)
env.close()
print(f"Mean reward: {np.mean(rewards):.4f} ± {np.std(rewards):.4f}")
print(f"Mean length: {np.mean(lengths):.1f} ± {np.std(lengths):.1f}")
```

Sanity check: mean reward should be negative (random play hits mines), mean length should be < total cells.

### 5. Manual play

Open `envs/minesweeper/game.html` in a browser and play a full game. Verify:
- Cells reveal on click
- Flood-fill works on zero-neighbor cells
- Mine click ends the game
- Numbers and colors are correct
