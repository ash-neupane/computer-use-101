from dataclasses import dataclass


@dataclass
class RewardConfig:
    bomb: float = -100.0
    reveal_one: float = 1.0
    reveal_flood: float = 20.0
    win: float = 500.0
    already_revealed: float = 0.0


def compute_reward(config, status, cells_revealed, won):
    if status == "lost":
        return config.bomb

    reward = 0.0
    if cells_revealed == 0:
        return config.already_revealed
    elif cells_revealed == 1:
        reward = config.reveal_one
    else:
        reward = config.reveal_flood

    if won:
        reward += config.win

    return reward
