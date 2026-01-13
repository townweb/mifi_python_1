"""Константы и данные игры (без логики)."""

# Общие настройки
GAME_TITLE = "Лабиринт сокровищ"
WELCOME_TEXT = "Добро пожаловать в Лабиринт сокровищ!"
COMMAND_PROMPT = "> "
HELP_CMD_WIDTH = 16
STEP_INCREMENT = 1

# Случайные события
EVENT_PROBABILITY = 10
EVENT_TYPE_MODULO = 3

# Комнаты
ROOM_ENTRANCE = "entrance"
ROOM_HALL = "hall"
ROOM_TRAP = "trap_room"
ROOM_LIBRARY = "library"
ROOM_ARMORY = "armory"
ROOM_TREASURE = "treasure_room"

# Предметы
ITEM_TORCH = "torch"
ITEM_RUSTY_KEY = "rusty_key"
ITEM_SWORD = "sword"
ITEM_TREASURE_KEY = "treasure_key"
ITEM_TREASURE_CHEST = "treasure_chest"
ITEM_COIN = "coin"

# Стабильные фразы для тестов
MSG_EXITS = "Выходы:"
MSG_ITEMS = "Заметные предметы:"
MSG_PUZZLE_PRESENT = "Кажется, здесь \nесть загадка (используйте команду solve)."
MSG_NO_PUZZLES = "Загадок здесь нет."
MSG_PUZZLE_SOLVED = "Правильно! Загадка решена."
MSG_WRONG_ANSWER = "Неверно. Попробуйте \nснова."
MSG_CANT_GO = "Нельзя пойти в \nэтом направлении."
MSG_NO_ITEM_HERE = "Такого \nпредмета здесь нет."
MSG_QUIT = "\nВыход из игры."
MSG_TRAP_TRIGGERED = "Ловушка активирована! Пол стал дрожать..."
MSG_VICTORY = "В сундуке сокровище! Вы победили!"
MSG_CHEST_OPEN_KEY = "Вы применяете ключ, и замок щёлкает. Сундук открыт!"
MSG_CHEST_LOCKED_ASK = "Сундук заперт. ... Ввести код? (да/нет)"
MSG_CHEST_RETREAT = "Вы отступаете от сундука."
MSG_TREASURE_GATE_LOCKED = "Дверь заперта. Нужен ключ, чтобы пройти дальше."
MSG_TREASURE_GATE_OPEN = "Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ."
MSG_TREASURE_CHEST_FORBIDDEN = "Нельзя унести сундук с собой."
MSG_UNKNOWN_COMMAND = "Неизвестная команда. Введите help для списка команд."

# Прочие сообщения (не обязательно для тестов, но делаем стабильными)
MSG_INVENTORY_EMPTY = "Инвентарь пуст."
MSG_INVENTORY_PREFIX = "Инвентарь:"
MSG_ITEM_TAKEN_PREFIX = "Вы подняли:"
MSG_NO_SUCH_ITEM = "У вас нет такого предмета."
MSG_TORCH_USED = "Вы зажигаете факел. Вокруг становится светлее."
MSG_SWORD_USED = "Вы крепче сжимаете меч. Чувствуете уверенность."
MSG_CHEST_TOO_HEAVY = "Вы не можете поднять сундук, он слишком тяжелый."
MSG_CHEST_NO_HERE = "Сундука здесь нет."
MSG_CHEST_NO_USE = "Похоже, здесь это не поможет."
MSG_CODE_PROMPT = "Код: "

# Сообщения случайных событий
MSG_FOUND_COIN = "Вы замечаете блеск на полу: монетка появляется в комнате."
MSG_HEAR_RUSTLE = "Вы слышите шорох в темноте..."
MSG_SWORD_SCARES = "Вы взмахиваете мечом — существо отступает."
MSG_TRAP_DANGER = "Вам кажется, что плиты под ногами готовы сработать..."

# Загадки
PUZZLE_HALL_QUESTION = 'На пьедестале надпись: "Назовите число, которое идет после девяти."'
PUZZLE_HALL_ANSWERS = ["10", "десять"]

PUZZLE_LIBRARY_QUESTION = 'На полке записка: "Что тяжелее: килограмм железа или килограмм перьев?"'
PUZZLE_LIBRARY_ANSWERS = ["одинаково", "равны", "одинаковые", "равно"]

PUZZLE_TRAP_QUESTION = 'На стене царапина: "Скажи слово, которое означает «свет»."'
PUZZLE_TRAP_ANSWERS = ["свет"]

PUZZLE_TREASURE_QUESTION = 'На замке цифры и строка: "Код — сумма двух и двух, повторённая дважды."'
PUZZLE_TREASURE_ANSWERS = ["44", "сорок четыре"]

# Команды
COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "help": "показать помощь",
    "quit": "выйти из игры",
}

# Данные комнат
ROOMS = {
    ROOM_ENTRANCE: {
        "description": "Вы стоите у входа в лабиринт. Воздух холодный, стены сырые.",
        "exits": {"north": ROOM_HALL, "east": ROOM_TRAP},
        "items": [ITEM_TORCH],
        "puzzle": None,
    },
    ROOM_HALL: {
        "description": "Большой зал с эхом. В центре — пьедестал с надписью.",
        "exits": {"south": ROOM_ENTRANCE, "west": ROOM_LIBRARY, "east": ROOM_ARMORY, "north": ROOM_TREASURE},
        "items": [],
        "puzzle": (PUZZLE_HALL_QUESTION, PUZZLE_HALL_ANSWERS),
    },
    ROOM_TRAP: {
        "description": "Комната с подозрительными плитами. Кажется, что пол здесь опасен.",
        "exits": {"west": ROOM_ENTRANCE},
        "items": [ITEM_RUSTY_KEY],
        "puzzle": (PUZZLE_TRAP_QUESTION, PUZZLE_TRAP_ANSWERS),
    },
    ROOM_LIBRARY: {
        "description": "Пыльная библиотека. Старые свитки и книги смотрят на вас молча.",
        "exits": {"east": ROOM_HALL, "north": ROOM_ARMORY},
        "items": [],
        "puzzle": (PUZZLE_LIBRARY_QUESTION, PUZZLE_LIBRARY_ANSWERS),
    },
    ROOM_ARMORY: {
        "description": "Оружейная. На стойках — пустые крепления и следы былой славы.",
        "exits": {"west": ROOM_HALL, "south": ROOM_LIBRARY},
        "items": [],
        "puzzle": None,
    },
    ROOM_TREASURE: {
        "description": "Комната сокровищ. В центре стоит массивный сундук.",
        "exits": {"south": ROOM_HALL},
        "items": [ITEM_TREASURE_CHEST],
        "puzzle": (PUZZLE_TREASURE_QUESTION, PUZZLE_TREASURE_ANSWERS),
    },
}
