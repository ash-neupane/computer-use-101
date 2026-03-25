"""Configuration loading. Merges default.json with optional overrides."""

import json
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
DEFAULT_PATH = CONFIG_DIR / "default.json"


def deep_merge(base, overrides):
    merged = base.copy()
    for key, val in overrides.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(val, dict):
            merged[key] = deep_merge(merged[key], val)
        else:
            merged[key] = val
    return merged


def load_config(overrides_path=None):
    with open(DEFAULT_PATH) as f:
        config = json.load(f)
    if overrides_path:
        with open(overrides_path) as f:
            overrides = json.load(f)
        config = deep_merge(config, overrides)
    return config
