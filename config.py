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

PERSON_RECT_X = 850
PERSON_RECT_Y = 205
PERSON_RECT_WIDTH = 260
PERSON_RECT_HEIGHT = 520
PERSON_COLOR = (0, 0, 0)

GAME_TITLE = "RADIK, PLEASE!"
ICON_PATH = "assets/images/icon.png"
BACKGROUND_PATH = "assets/images/bg.png"
TABLE_PATH = "assets/images/table.png"
MUSIC_PATH = "assets/sounds/bg.mp3"
DEFAULT_MUSIC_VOLUME = 0.4
DEFAULT_SOUND_VOLUME = 0.7
DEFAULT_MUSIC_ENABLED = True
DEFAULT_SOUND_ENABLED = True
MIN_VOLUME = 0.0
MAX_VOLUME = 1.0
VOLUME_ROUND_DIGITS = 2
VOLUME_PERCENT = 100

DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800
WINDOW_MODE_TYPE_INDEX = 0
WINDOW_MODE_TEXT_INDEX = 1
WINDOW_MODE_WIDTH_INDEX = 2
WINDOW_MODE_HEIGHT_INDEX = 3
WINDOW_MODE_WINDOWED = "windowed"
WINDOW_MODE_FULLSCREEN = "fullscreen"
WINDOW_MODE_BORDERED_FULLSCREEN = "bordered_fullscreen"
WINDOW_MODES = (
    (WINDOW_MODE_WINDOWED, "900x600", 900, 600),
    (WINDOW_MODE_WINDOWED, "1200x800", 1200, 800),
    (WINDOW_MODE_WINDOWED, "1536x1024", 1536, 1024),
    (WINDOW_MODE_FULLSCREEN, "Полный экран", 0, 0),
    (WINDOW_MODE_BORDERED_FULLSCREEN, "Полный экран с рамками", 0, 0),
)
DEFAULT_WINDOW_MODE_NUMBER = 1

SCREEN_MENU = "menu"
SCREEN_SETTINGS = "settings"
SCREEN_GAME = "game"

BUTTON_START = "start"
BUTTON_CONTINUE = "continue"
BUTTON_SETTINGS = "settings"
BUTTON_EXIT = "exit"
BUTTON_MUSIC = "music"
BUTTON_SOUND = "sound"
BUTTON_WINDOW_SIZE = "window_size"
BUTTON_BACK = "back"
SLIDER_MUSIC_VOLUME = "music_volume"
SLIDER_SOUND_VOLUME = "sound_volume"

SAVE_FILE = "save.json"
SETTINGS_FILE = "settings.json"
SETTINGS_ENCODING = "utf-8"
SETTING_MUSIC_ENABLED = "music_enabled"
SETTING_SOUND_ENABLED = "sound_enabled"
SETTING_MUSIC_VOLUME = "music_volume"
SETTING_SOUND_VOLUME = "sound_volume"
SETTING_WINDOW_MODE_NUMBER = "window_mode_number"

MENU_TITLE_TEXT = "RADIK, PLEASE!"
MENU_START_TEXT = "Начать игру"
MENU_CONTINUE_TEXT = "Продолжить"
MENU_SETTINGS_TEXT = "Настройки"
MENU_EXIT_TEXT = "Выход"
MENU_BACK_TEXT = "Назад"

SETTINGS_TITLE_TEXT = "Настройки"
SETTING_ON_TEXT = "вкл"
SETTING_OFF_TEXT = "выкл"
MUSIC_SETTING_TEXT = "Музыка: {state}"
SOUND_SETTING_TEXT = "Звук: {state}"
MUSIC_VOLUME_TEXT = "Громкость музыки: {volume}%"
SOUND_VOLUME_TEXT = "Громкость звука: {volume}%"
WINDOW_SIZE_TEXT = "Окно: {mode}"

MENU_BUTTON_WIDTH = 520
MENU_BUTTON_HEIGHT = 60
MENU_FIRST_BUTTON_Y = 240
MENU_BUTTON_GAP = 80
SETTINGS_FIRST_BUTTON_Y = 180
SETTINGS_BUTTON_GAP = 70
SLIDER_TRACK_WIDTH = 360
SLIDER_TRACK_HEIGHT = 8
SLIDER_TRACK_OFFSET_Y = 42
SLIDER_LABEL_OFFSET_Y = 24
SLIDER_KNOB_WIDTH = 18
SLIDER_KNOB_HEIGHT = 28

TITLE_Y = 120
TITLE_FONT_SIZE = 64
BUTTON_FONT_SIZE = 38
GAME_FONT_SIZE = 40

BACKGROUND_X = 0
BACKGROUND_Y = 0
MIN_SCALED_SIZE = 1
TABLE_X = -25
TABLE_Y = 400
TABLE_WIDTH = 1600
TABLE_HEIGHT = 915

MENU_BACKGROUND_COLOR = (0, 0, 0)
MENU_TEXT_COLOR = (235, 235, 235)
BUTTON_COLOR = (45, 45, 45)
BUTTON_HOVER_COLOR = (70, 70, 70)
BUTTON_DISABLED_COLOR = (35, 35, 35)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_DISABLED_TEXT_COLOR = (120, 120, 120)
SLIDER_TRACK_COLOR = (70, 70, 70)
SLIDER_FILL_COLOR = (180, 180, 180)
SLIDER_KNOB_COLOR = (255, 255, 255)
