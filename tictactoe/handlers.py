"""TicTacToe Handlers."""

from copy import deepcopy

from autokitteh import (
    check_and_set_value,
    Event,
    get_value,
    get_webhook_url,
    http_outcome,
    set_value,
)
import shortuuid


_BASE_URL = get_webhook_url("webhook")


def on_webhook(event: Event) -> None:
    data = event.data

    if data.method != "GET":
        print("not get")
        return

    suffix = data.url.path_suffix
    if suffix.startswith("/"):
        suffix = suffix[1:]
    print(f"path: {suffix}")
    match suffix.split("/"):
        case [""]:
            _help()
            return
        case ["new"]:
            _new()
            return
        case ["game", game_id]:
            _render(game_id, None)
            return
        case ["game", game_id, who]:
            _render(game_id, who)
            return
        case ["game", game_id, who, turn, xy]:
            _move(game_id, who, turn, xy)
            return
        case _:
            http_outcome(404, "Not Found")
            return


def _help() -> None:
    http_outcome(
        200,
        f"""<html>
    <body>
        <h1>TicTacToe</h1>
        <ul>
            <li><a href="/{_BASE_URL}/new">/new</a> - Start a new game</li>
            <li>/game/&lt;game_id&gt; - Observe an existing game</li>
            <li>/game/&lt;game_id&gt;/&lt;who&gt; - Join an existing game as 'X' or 'O'</li>
        </ul>
    </body>
</html>""",  # noqa: E501
    )


def _redirect(game_id: str, who: str) -> None:
    http_outcome(
        302,
        headers={"Location": f"/{_BASE_URL}/game/{game_id}/{who}"},
    )


def _new() -> None:
    game_id = shortuuid.uuid()

    print(f"new game: {game_id}")

    set_value(
        game_id,
        {
            "board": [[None] * 3 for _ in range(3)],
            "turn": 0,
        },
    )

    _redirect(game_id, "X")


def _move(game_id: str, who: str, turn: str, xy: str) -> None:
    if who not in ("X", "O"):
        http_outcome(400, "who must be 'X' or 'O'")
        return

    if xy not in ("00", "01", "02", "10", "11", "12", "20", "21", "22"):
        http_outcome(400, "xy must be in 'xy' format where x and y are 0, 1, or 2")
        return

    game = get_value(game_id)
    if game is None:
        http_outcome(404, "Game not found")
        return

    if str(game["turn"]) != turn:
        http_outcome(400, "invalid turn")
        return

    expected_who = "X" if int(turn) % 2 == 0 else "O"

    if who != expected_who:
        http_outcome(400, f"it's {expected_who}'s turn")
        return

    row, col = int(xy[0]), int(xy[1])
    if game["board"][row][col] is not None:
        http_outcome(400, "cell already occupied")
        return

    new_game = deepcopy(game)
    new_game["board"][row][col] = who
    new_game["turn"] += 1

    if not check_and_set_value(game_id, game, new_game):
        http_outcome(409, "conflict, please try again")
        return

    _redirect(game_id, who)


def _render(game_id: str, who: str | None) -> None:
    if who not in ("X", "O", None):
        http_outcome(400, "who must be 'X' or 'O' or none")
        return

    game = get_value(game_id)
    if game is None:
        http_outcome(404, "Game not found")
        return

    turn = game["turn"]

    who_next = None if _is_game_over(game["board"]) else ("X" if turn % 2 == 0 else "O")
    you = f"playing as {who}" if who else "observing the game"

    def cell(row: int, col: int) -> str:
        on_click, clickable = "", ""
        if who == who_next and game["board"][row][col] is None:
            on_click = f" onclick=\"location.href='/{_BASE_URL}/game/{game_id}/{who}/{turn}/{row}{col}'\""  # noqa: E501
            clickable = "clickable-cell"

        val = game["board"][row][col] or "&nbsp;"

        return f"<td class='cell {clickable}' {on_click}>{val}</td>"

    def row(row: int) -> str:
        return f"<tr>{cell(row, 0)}{cell(row, 1)}{cell(row, 2)}</tr>"

    auto_refresh = who_next and who != who_next

    http_outcome(
        200,
        f"""
<html>
    <head>
        <title>TicTacToe Game {game_id}</title>

        <style>
            body {{ text-align: center }}

            table {{
                border-collapse: separate;
                border-spacing: 0;
                margin: 20px auto;
            }}

            .cell {{
                width: 60px;
                height: 60px;
                border: 2px solid #333;
                text-align: center;
                font-size: 24px;
                transition: background-color 0.2s ease;
            }}

            .clickable-cell {{
                cursor: pointer;
            }}

            .clickable-cell:hover {{
                background-color: #e6f3ff;
            }}
        </style>
    </head>
    <body>
        <h1>TicTacToe Game {game_id}</h1>
        <p>{turn} moves made.</p>
        <p>You are {you}.</p>
        <p>{f"Next turn is for {who_next}." if who_next else "<b>Game over!</b>"}</p>
        <table border="1">
            {row(0)}
            {row(1)}
            {row(2)}
        </table>

        <script>
            const autoReload = {"true" if auto_refresh else "false"};

            function reload() {{
                window.location.reload();
            }}

            if (autoReload) {{
                setInterval(reload, 5000);
            }}
        </script>
    </body>
</html>
""",
    )


def _is_game_over(board: list[list[str | None]]) -> bool:
    if all(cell is not None for row in board for cell in row):
        # No more moves possible.
        return True

    wins = (
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),
        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),
        ((0, 0), (1, 1), (2, 2)),
        ((0, 2), (1, 1), (2, 0)),
    )

    for pattern in wins:
        vals = {board[x][y] for x, y in pattern}
        if len(vals) == 1 and vals.pop() is not None:
            return True

    return False
