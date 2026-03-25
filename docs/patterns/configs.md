# Configuration Pattern

All configuration lives in `config/default.json`. CLI overrides are handled in the entrypoint via `click`.

## Why

- Single source of truth for defaults — no magic numbers scattered across modules.
- Easy to diff between experiments — just compare JSON files.
- Library code stays pure — it receives values, never reads config files.

## Structure

```
config/default.json     ← all defaults: device, logging, wandb, experiment, reward
scripts/run.py          ← entrypoint: loads config, applies CLI overrides, passes values in
computer_use_101/config.py  ← load_config() with deep merge for overrides
```

## config/default.json layout

```json
{
    "device": "cpu",
    "logging": { "level": "info", "log_every": 50 },
    "wandb": { "entity": "...", "project": "..." },
    "experiment": { "rows": 5, "episodes": 2000, "lr": 1e-3, ... },
    "reward": { "bomb": -10.0, "win": 50.0, ... }
}
```

## Overrides

Pass a JSON file to override any subset of keys:

```bash
python -m scripts.run --config config/big_grid.json --episodes 5000
```

The override file only needs the keys you want to change — `deep_merge` handles the rest.

## Rules

1. **No hardcoded config in library code.** Functions receive values as arguments.
2. **CLI with click only.** Never `argparse`.
3. **Override files are partial.** They merge on top of `default.json`, not replace it.
4. **New experiments = new override file.** Don't edit `default.json` for a one-off run.
