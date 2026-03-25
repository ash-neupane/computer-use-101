import numpy as np
import pytest
from gymnasium.utils.env_checker import check_env

from computer_use_101.minesweeper.env import MinesweeperEnv
from computer_use_101.minesweeper.reward import RewardConfig


@pytest.fixture
def env():
    e = MinesweeperEnv(rows=5, cols=5, mines=3)
    yield e
    e.close()


def test_reset_returns_observation(env):
    obs, info = env.reset(seed=42)
    assert isinstance(obs, np.ndarray)
    assert obs.ndim == 3
    assert obs.shape[2] == 3
    assert info["status"] == "playing"


def test_step_safe_cell(env):
    env.reset(seed=42)
    board = env._get_game_state()["board"]
    safe_action = next(
        r * env.cols + c for r in range(env.rows) for c in range(env.cols) if board[r][c] != -1
    )
    obs, reward, terminated, truncated, info = env.step(safe_action)
    assert isinstance(obs, np.ndarray)
    assert reward >= 0
    assert not truncated


def test_step_mine_gives_negative_reward(env):
    env.reset(seed=42)
    board = env._get_game_state()["board"]
    mine_action = next(
        r * env.cols + c for r in range(env.rows) for c in range(env.cols) if board[r][c] == -1
    )
    obs, reward, terminated, truncated, info = env.step(mine_action)
    assert reward == RewardConfig().bomb
    assert terminated


def test_repeated_click_no_reward(env):
    env.reset(seed=42)
    board = env._get_game_state()["board"]
    safe_action = next(
        r * env.cols + c for r in range(env.rows) for c in range(env.cols) if board[r][c] != -1
    )
    env.step(safe_action)
    _, reward, _, _, _ = env.step(safe_action)
    assert reward == 0.0


def test_flood_fill_reward(env):
    env.reset(seed=42)
    board = env._get_game_state()["board"]
    zero_action = next(
        (r * env.cols + c for r in range(env.rows) for c in range(env.cols) if board[r][c] == 0), None
    )
    if zero_action is None:
        pytest.skip("No zero cell in this seed")
    _, reward, _, _, _ = env.step(zero_action)
    assert reward == RewardConfig().reveal_flood


def test_custom_reward_config():
    config = RewardConfig(bomb=-50, reveal_one=10, reveal_flood=100, win=1000)
    e = MinesweeperEnv(rows=5, cols=5, mines=3, reward_config=config)
    e.reset(seed=42)
    board = e._get_game_state()["board"]
    mine_action = next(
        r * e.cols + c for r in range(e.rows) for c in range(e.cols) if board[r][c] == -1
    )
    _, reward, _, _, _ = e.step(mine_action)
    assert reward == -50.0
    e.close()


def test_multiple_resets(env):
    for seed in [1, 2, 3]:
        obs, info = env.reset(seed=seed)
        assert info["status"] == "playing"
        assert info["revealedCount"] == 0


def test_full_game_terminates(env):
    env.reset(seed=42)
    terminated = False
    for action in range(env.rows * env.cols):
        if terminated:
            break
        _, _, terminated, _, info = env.step(action)
    assert terminated


def test_check_env():
    env = MinesweeperEnv(rows=5, cols=5, mines=3)
    try:
        # Browser rendering has subpixel nondeterminism, so check_env's
        # determinism assertion will fail. We verify core compliance here;
        # determinism is tested separately via game state, not pixels.
        check_env(env, skip_render_check=True)
    except AssertionError as e:
        if "Deterministic" not in str(e):
            raise
    finally:
        env.close()
