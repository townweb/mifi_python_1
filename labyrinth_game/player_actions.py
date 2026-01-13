"""Действия игрока: перемещение, инвентарь, взаимодействия."""

from labyrinth_game.constants import (
    ITEM_SWORD,
    ITEM_TORCH,
    ITEM_TREASURE_CHEST,
    ITEM_TREASURE_KEY,
    MSG_CANT_GO,
    MSG_CHEST_TOO_HEAVY,
    MSG_INVENTORY_EMPTY,
    MSG_INVENTORY_PREFIX,
    MSG_ITEM_TAKEN_PREFIX,
    MSG_NO_ITEM_HERE,
    MSG_NO_SUCH_ITEM,
    MSG_SWORD_USED,
    MSG_TORCH_USED,
    MSG_TREASURE_CHEST_FORBIDDEN,
    MSG_TREASURE_GATE_LOCKED,
    MSG_TREASURE_GATE_OPEN,
    ROOM_TREASURE,
    ROOMS,
    STEP_INCREMENT,
)
from labyrinth_game.utils import attempt_open_treasure, describe_current_room, random_event


def move_player(game_state: dict, direction: str) -> None:
    """Перемещает игрока по направлению."""
    current_room = game_state["current_room"]
    exits = ROOMS[current_room]["exits"]

    if direction not in exits:
        print(MSG_CANT_GO)
        return

    next_room = exits[direction]

    if next_room == ROOM_TREASURE:
        if "rusty_key" not in game_state["player_inventory"]:
            print(MSG_TREASURE_GATE_LOCKED)
            return
        print(MSG_TREASURE_GATE_OPEN)

    game_state["current_room"] = next_room
    game_state["steps_taken"] += STEP_INCREMENT

    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state: dict, item: str) -> None:
    """Поднимает предмет из комнаты в инвентарь."""
    room = game_state["current_room"]
    room_items = ROOMS[room]["items"]

    if item == ITEM_TREASURE_CHEST:
        print(MSG_TREASURE_CHEST_FORBIDDEN)
        return

    if item not in room_items:
        print(MSG_NO_ITEM_HERE)
        return

    room_items.remove(item)
    game_state["player_inventory"].append(item)
    print(f"{MSG_ITEM_TAKEN_PREFIX} {item}")


def use_item(game_state: dict, item: str) -> None:
    """Использует предмет из инвентаря."""
    inventory = game_state["player_inventory"]

    if item not in inventory:
        print(MSG_NO_SUCH_ITEM)
        return

    if item == ITEM_TORCH:
        print(MSG_TORCH_USED)
        return

    if item == ITEM_SWORD:
        print(MSG_SWORD_USED)
        return

    if item == ITEM_TREASURE_KEY:
        if game_state["current_room"] == ROOM_TREASURE:
            attempt_open_treasure(game_state)
        else:
            print("Сундука рядом нет.")
        return

    print("Вы не знаете, как использовать этот предмет.")


def show_inventory(game_state: dict) -> None:
    """Печатает инвентарь."""
    inventory = game_state["player_inventory"]
    if not inventory:
        print(MSG_INVENTORY_EMPTY)
        return
    print(f"{MSG_INVENTORY_PREFIX} {', '.join(inventory)}")
