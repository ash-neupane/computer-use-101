from envs.minesweeper.reward import RewardConfig, compute_reward


def test_bomb_reward():
    config = RewardConfig()
    assert compute_reward(config, "lost", 0, False) == -100.0


def test_reveal_one():
    config = RewardConfig()
    assert compute_reward(config, "playing", 1, False) == 1.0


def test_reveal_flood():
    config = RewardConfig()
    assert compute_reward(config, "playing", 5, False) == 20.0


def test_win_bonus():
    config = RewardConfig()
    assert compute_reward(config, "playing", 1, True) == 501.0


def test_win_bonus_flood():
    config = RewardConfig()
    assert compute_reward(config, "playing", 3, True) == 520.0


def test_already_revealed():
    config = RewardConfig()
    assert compute_reward(config, "playing", 0, False) == 0.0


def test_custom_config():
    config = RewardConfig(bomb=-50, reveal_one=10, reveal_flood=100, win=1000)
    assert compute_reward(config, "lost", 0, False) == -50.0
    assert compute_reward(config, "playing", 1, False) == 10.0
    assert compute_reward(config, "playing", 4, False) == 100.0
    assert compute_reward(config, "playing", 1, True) == 1010.0
