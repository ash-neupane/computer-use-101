import io
from pathlib import Path

import gymnasium
import numpy as np
from gymnasium import spaces
from PIL import Image
from playwright.sync_api import sync_playwright


class MinesweeperEnv(gymnasium.Env):
    metadata = {"render_modes": ["rgb_array"]}

    def __init__(self, rows=5, cols=5, mines=3, render_mode="rgb_array"):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.render_mode = render_mode

        self.action_space = spaces.Discrete(rows * cols)

        self._viewport_w = cols * 62 + 20
        self._viewport_h = rows * 62 + 20
        self.observation_space = spaces.Box(0, 255, shape=(self._viewport_h, self._viewport_w, 3), dtype=np.uint8)

        self._browser = None
        self._page = None
        self._prev_progress = 0.0
        self._html_path = Path(__file__).parent / "game.html"

    def _ensure_browser(self):
        if self._browser is not None:
            return
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=True)

    def _screenshot(self):
        png = self._page.screenshot()
        img = Image.open(io.BytesIO(png)).convert("RGB")
        return np.array(img)

    def _get_game_state(self):
        return self._page.evaluate("() => window.gameState")

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._ensure_browser()

        game_seed = seed if seed is not None else self.np_random.integers(0, 2**31)
        url = f"file://{self._html_path}?rows={self.rows}&cols={self.cols}&mines={self.mines}&seed={game_seed}"

        if self._page is None:
            self._page = self._browser.new_page()
            self._page.set_viewport_size({"width": self._viewport_w, "height": self._viewport_h})

        self._page.goto(url)
        self._page.wait_for_function("() => window.gameState !== undefined")
        self._page.wait_for_load_state("networkidle")
        self._prev_progress = 0.0

        obs = self._screenshot()
        info = self._get_game_state()
        return obs, info

    def step(self, action):
        row, col = divmod(int(action), self.cols)

        state_before = self._get_game_state()
        if state_before["status"] != "playing":
            return self._screenshot(), 0.0, True, False, state_before

        already_revealed = state_before["revealed"][row][col]

        self._page.evaluate(f"() => window.clickCell({row}, {col})")

        state = self._get_game_state()
        progress = state["revealedCount"] / state["totalSafe"]

        if state["status"] == "lost":
            reward = -1.0
            terminated = True
        elif state["status"] == "won":
            reward = progress - self._prev_progress
            terminated = True
        elif already_revealed:
            reward = 0.0
            terminated = False
        else:
            reward = progress - self._prev_progress
            terminated = False

        self._prev_progress = progress
        obs = self._screenshot()
        return obs, reward, terminated, False, state

    def render(self):
        if self._page is None:
            return None
        return self._screenshot()

    def close(self):
        if self._page:
            self._page.close()
            self._page = None
        if self._browser:
            self._browser.close()
            self._browser = None
        if hasattr(self, "_playwright") and self._playwright:
            self._playwright.stop()
            self._playwright = None
