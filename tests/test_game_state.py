import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path

GAME_HTML = Path(__file__).parent.parent / "computer_use_101" / "minesweeper" / "game.html"


@pytest.fixture(scope="module")
def browser():
    pw = sync_playwright().start()
    b = pw.chromium.launch(headless=True)
    yield b
    b.close()
    pw.stop()


@pytest.fixture
def page(browser):
    p = browser.new_page()
    p.goto(f"file://{GAME_HTML}?rows=5&cols=5&mines=3&seed=42")
    p.wait_for_function("() => window.gameState !== undefined")
    yield p
    p.close()


def test_initial_state(page):
    state = page.evaluate("() => window.gameState")
    assert state["status"] == "playing"
    assert state["revealedCount"] == 0
    assert state["totalSafe"] == 22
    assert len(state["board"]) == 5
    assert len(state["board"][0]) == 5


def test_mine_count(page):
    board = page.evaluate("() => window.gameState.board")
    mine_count = sum(cell == -1 for row in board for cell in row)
    assert mine_count == 3


def test_click_safe_cell(page):
    board = page.evaluate("() => window.gameState.board")
    safe_r, safe_c = next(
        (r, c) for r in range(5) for c in range(5) if board[r][c] != -1
    )
    page.evaluate(f"() => window.clickCell({safe_r}, {safe_c})")
    state = page.evaluate("() => window.gameState")
    assert state["revealedCount"] >= 1
    assert state["status"] in ("playing", "won")


def test_click_mine_loses(page):
    board = page.evaluate("() => window.gameState.board")
    mine_r, mine_c = next(
        (r, c) for r in range(5) for c in range(5) if board[r][c] == -1
    )
    page.evaluate(f"() => window.clickCell({mine_r}, {mine_c})")
    state = page.evaluate("() => window.gameState")
    assert state["status"] == "lost"


def test_reset_game(page):
    page.evaluate("() => window.clickCell(0, 0)")
    page.evaluate("() => window.resetGame(99)")
    state = page.evaluate("() => window.gameState")
    assert state["status"] == "playing"
    assert state["revealedCount"] == 0


def test_flood_fill(page):
    board = page.evaluate("() => window.gameState.board")
    zero_cell = next(
        ((r, c) for r in range(5) for c in range(5) if board[r][c] == 0), None
    )
    if zero_cell is None:
        pytest.skip("No zero cell in this seed")
    r, c = zero_cell
    page.evaluate(f"() => window.clickCell({r}, {c})")
    state = page.evaluate("() => window.gameState")
    assert state["revealedCount"] > 1


def test_deterministic_seed(browser):
    results = []
    for _ in range(2):
        p = browser.new_page()
        p.goto(f"file://{GAME_HTML}?rows=5&cols=5&mines=3&seed=123")
        p.wait_for_function("() => window.gameState !== undefined")
        results.append(p.evaluate("() => window.gameState.board"))
        p.close()
    assert results[0] == results[1]
