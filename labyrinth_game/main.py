"""Точка входа: инициализация и игровой цикл."""

from labyrinth_game.constants import COMMAND_PROMPT, MSG_QUIT, MSG_UNKNOWN_COMMAND, WELCOME_TEXT
from labyrinth_game.player_actions import move_player, show_inventory, take_item, use_item
from labyrinth_game.utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle


def process_command(game_state: dict, command_line: str) -> None:
    """Разбирает команду и вызывает соответствующее действие."""
    raw = command_line.strip()
    if not raw:
        return

    parts = raw.split()
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    directions = {"north", "south", "east", "west"}

    if cmd in directions:
        move_player(game_state, cmd)
        return

    if cmd == "go":
        if not arg:
            print(MSG_UNKNOWN_COMMAND)
            return
        move_player(game_state, arg.lower())
        return

    if cmd == "look":
        describe_current_room(game_state)
        return

    if cmd == "take":
        if not arg:
            print(MSG_UNKNOWN_COMMAND)
            return
        take_item(game_state, arg)
        return

    if cmd == "use":
        if not arg:
            print(MSG_UNKNOWN_COMMAND)
            return
        use_item(game_state, arg)
        return

    if cmd == "inventory":
        show_inventory(game_state)
        return

    if cmd == "solve":
        solve_puzzle(game_state)
        if game_state["current_room"] == "treasure_room":
            attempt_open_treasure(game_state)
        return

    if cmd == "help":
        show_help()
        return

    if cmd == "quit":
        print(MSG_QUIT)
        game_state["game_over"] = True
        return

    print(MSG_UNKNOWN_COMMAND)


def main() -> None:
    """Запуск игры."""
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    print(WELCOME_TEXT)
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command_line = input(COMMAND_PROMPT)
        process_command(game_state, command_line)


if __name__ == "__main__":
    main()
