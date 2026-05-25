DEFAULT_MIN_AGE = 16
DEFAULT_MAX_AGE = 30
DEFAULT_REWARD = 10
DEFAULT_FINE = 5
DEFAULT_DISMISSAL_BALANCE = -50
DEFAULT_MONEY = 0
DEFAULT_AGE = 0

INVALID_PERSON_CHANCE = 0.45
MIN_TOO_YOUNG_AGE = 10

MIN_PASS_DAYS = 1
MAX_PASS_DAYS = 120
MAX_EXPIRED_DAYS = 60

MIN_GROUP_NUMBER = 100000
MAX_GROUP_NUMBER = 999999
GROUP_SEPARATOR = "-"
GROUP_SPLIT_MAX_COUNT = 1
GROUP_PATTERN = r"^[А-Я]{2}-\d{6}$"
VALID_GROUP_PREFIXES = ("ИС", "ПИ", "БИ", "ЭК", "МТ")
BAD_GROUP_PREFIX = "ЮР"
BAD_GROUP_VARIANTS = ("123456", "АА123456", "A1-000001", "ГРУППА")
AGE_MISTAKE_VARIANTS = (-2, -1, 1, 2)

DECISION_ALLOW = "allow"
DECISION_DENY = "deny"
ALLOW_DECISIONS = ("allow", "accept", "pass", "пропустить", "допустить")
DENY_DECISIONS = ("deny", "reject", "kick", "вышвырнуть", "отказать", "не пропустить")

PERSON_NAMES = (
    "Артур",
    "Саша",
    "Данил",
    "Алина",
    "Мария",
    "Илья",
    "Кирилл",
    "Вика",
    "Егор",
)

NO_DOCUMENT = "no_document"
EXPIRED_DOCUMENT = "expired_document"
TOO_YOUNG = "too_young"
BAD_GROUP_FORMAT = "bad_group_format"
BAD_GROUP_PREFIX_ERROR = "bad_group_prefix"
WRONG_NAME = "wrong_name"
WRONG_AGE = "wrong_age"
WRONG_GROUP = "wrong_group"

DATE_FORMAT = "%d.%m.%Y"
NO_DATE_TEXT = "нет данных"

PERSON_NAME_TEXT = "Имя"
PERSON_AGE_TEXT = "Возраст"
PERSON_GROUP_TEXT = "Группа"
DOCUMENT_VALID_UNTIL_TEXT = "Действителен до"
NO_DOCUMENT_TEXT = "Пропуска нет"

INSTRUCTION_HAS_DOCUMENT = "Пропускать только людей с пропуском."
INSTRUCTION_NOT_EXPIRED = "Срок действия пропуска не должен быть истекшим."
INSTRUCTION_MIN_AGE = "Возраст посетителя должен быть от {min_age} лет."
INSTRUCTION_GROUP = "Группа должна иметь формат АА-000000 и начинаться с: {prefixes}."
INSTRUCTION_DATA_MATCH = "Данные в пропуске должны совпадать с данными посетителя."

ERROR_NO_DOCUMENT = "Нет пропуска"
ERROR_EXPIRED_DOCUMENT = "Срок действия пропуска истёк"
ERROR_TOO_YOUNG = "Посетитель младше допустимого возраста"
ERROR_WRONG_NAME = "Имя в пропуске не совпадает"
ERROR_WRONG_AGE = "Возраст в пропуске не совпадает"
ERROR_BAD_GROUP_FORMAT = "Неверный формат группы"
ERROR_BAD_GROUP_PREFIX = "Группа не относится к институту"
ERROR_WRONG_GROUP = "Группа в пропуске не совпадает"

MESSAGE_NO_CURRENT_PERSON = "Нельзя принять решение: нет текущего посетителя"
MESSAGE_GAME_ALREADY_OVER = "Игра окончена"
MESSAGE_DISMISSED = "Долг слишком большой: игрока уволили"
MESSAGE_UNKNOWN_DECISION = "Неизвестное решение игрока: {decision}"
