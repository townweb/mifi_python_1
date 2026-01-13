"""Вспомогательные функции (описание, помощь, загадки, победа, ловушки)."""

import math

from labyrinth_game.constants import (
    COMMANDS,
    EVENT_PROBABILITY,
    EVENT_TYPE_MODULO,
    HELP_CMD_WIDTH,
    ITEM_COIN,
    ITEM_SWORD,
    ITEM_TORCH,
    ITEM_TREASURE_CHEST,
    ITEM_TREASURE_KEY,
    MSG_CHEST_LOCKED_ASK,
    MSG_CHEST_OPEN_KEY,
    MSG_CHEST_RETREAT,
    MSG_CODE_PROMPT,
    MSG_EXITS,
    MSG_FOUND_COIN,
    MSG_HEAR_RUSTLE,
    MSG_ITEMS,
    MSG_NO_PUZZLES,
    MSG_PUZZLE_PRESENT,
    MSG_SWORD_SCARES,
    MSG_TRAP_DANGER,
    MSG_TRAP_TRIGGERED,
    MSG_VICTORY,
    MSG_WRONG_ANSWER,
    ROOM_TREASURE,
    ROOMS,
)


def _normalize_text(text: str) -> str:
    """Нормализация ввода: trim, lower, схлопывание пробелов."""
    raw = text.strip().lower()
    parts = raw.split()
    return " ".join(parts)


def describe_current_room(game_state: dict) -> None:
    """Печатает описание текущей комнаты стабильным форматом."""
    room = game_state["current_room"]
    data = ROOMS[room]

    print(data["description"])

    if data["items"]:
        print(f"{MSG_ITEMS} {', '.join(data['items'])}")

    print(f"{MSG_EXITS} {', '.join(data['exits'].keys())}")

    if data["puzzle"] is not None:
        print(MSG_PUZZLE_PRESENT)
    else:
        print(MSG_NO_PUZZLES)


def show_help() -> None:
    """Печатает справку по командам."""
    for cmd, desc in COMMANDS.items():
        print(f"  {cmd:<{HELP_CMD_WIDTH}} - {desc}")


def pseudo_random(seed: int, modulo: int) -> int:
    """Псевдослучайное число в диапазоне [0, modulo)."""
    x = math.sin(seed * 12.9898)
    x = x * 43758.5453
    frac = x - math.floor(x)
    scaled = frac * modulo
    return int(math.floor(scaled))


def trigger_trap(game_state: dict) -> None:
    """Срабатывание ловушки — завершает игру."""
    print(MSG_TRAP_TRIGGERED)
    game_state["game_over"] = True


def random_event(game_state: dict) -> None:
    """Случайные события: вызывать после успешного перемещения."""
    steps_taken = game_state["steps_taken"]
    if pseudo_random(steps_taken, EVENT_PROBABILITY) != 0:
        return

    event_type = pseudo_random(steps_taken + 1, EVENT_TYPE_MODULO)

    if event_type == 0:
        room = game_state["current_room"]
        if ITEM_COIN not in ROOMS[room]["items"]:
            ROOMS[room]["items"].append(ITEM_COIN)
        print(MSG_FOUND_COIN)
        return

    if event_type == 1:
        print(MSG_HEAR_RUSTLE)
        if ITEM_SWORD in game_state["player_inventory"]:
            print(MSG_SWORD_SCARES)
        return

    if event_type == 2:
        room = game_state["current_room"]
        if room == "trap_room" and ITEM_TORCH not in game_state["player_inventory"]:
            print(MSG_TRAP_DANGER)
            trigger_trap(game_state)


def solve_puzzle(game_state: dict) -> None:
    """Пытается решить загадку в текущей комнате."""
    room = game_state["current_room"]
    puzzle = ROOMS[room]["puzzle"]

    if puzzle is None:
        print(MSG_NO_PUZZLES)
        return

    question, answers = puzzle
    print(question)
    user_answer = _normalize_text(input("Ваш ответ: "))

    accepted = _accepted_answers(answers)
    if user_answer in accepted:
        ROOMS[room]["puzzle"] = None
        _grant_puzzle_reward(game_state, room)
        return

    print(MSG_WRONG_ANSWER)
    if room == "trap_room":
        trigger_trap(game_state)


def _accepted_answers(answers) -> list:
    if isinstance(answers, str):
        return [_normalize_text(answers)]
    return [_normalize_text(a) for a in answers]


def _grant_puzzle_reward(game_state: dict, room: str) -> None:
    """Выдаёт награду за решённую загадку (зависит от комнаты)."""
    inventory = game_state["player_inventory"]

    if room == "hall":
        if ITEM_SWORD not in inventory:
            inventory.append(ITEM_SWORD)
        return

    if room == "library":
        if ITEM_TREASURE_KEY not in inventory:
            inventory.append(ITEM_TREASURE_KEY)
        return

    if room == ROOM_TREASURE:
        game_state["treasure_code_solved"] = True


def attempt_open_treasure(game_state: dict) -> None:
    """Открывает сундук ключом или кодом/загадкой."""
    if game_state["current_room"] != ROOM_TREASURE:
        return

    if ITEM_TREASURE_CHEST not in ROOMS[ROOM_TREASURE]["items"]:
        return

    if ITEM_TREASURE_KEY in game_state["player_inventory"]:
        print(MSG_CHEST_OPEN_KEY)
        ROOMS[ROOM_TREASURE]["items"].remove(ITEM_TREASURE_CHEST)
        print(MSG_VICTORY)
        game_state["game_over"] = True
        return

    if game_state.get("treasure_code_solved", False):
        ROOMS[ROOM_TREASURE]["items"].remove(ITEM_TREASURE_CHEST)
        print(MSG_VICTORY)
        game_state["game_over"] = True
        return

    choice = _normalize_text(input(f"{MSG_CHEST_LOCKED_ASK} "))
    if choice != "да":
        print(MSG_CHEST_RETREAT)
        return

    code = _normalize_text(input(MSG_CODE_PROMPT))
    puzzle = ROOMS[ROOM_TREASURE]["puzzle"]
    if puzzle is None:
        print("Код неверный.")
        return

    _, answers = puzzle
    accepted = _accepted_answers(answers)

    if code in accepted:
        ROOMS[ROOM_TREASURE]["items"].remove(ITEM_TREASURE_CHEST)
        print(MSG_VICTORY)
        game_state["game_over"] = True
    else:
        print("Код неверный.")
