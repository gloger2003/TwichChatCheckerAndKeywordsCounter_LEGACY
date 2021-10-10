TAGS_DICT = {
    'Messages': {
        'row': 2,
        'col': 1,
        'associations': [
            'Lol', 'LLLOOOOOLLLL', 'LOOOOOOL'
        ]
    },
    'Lol': {
        'row': 0,
        'col': 0,
        'associations': [
            'Lol', 'LLLOOOOOLLLL', 'LOOOOOOL', 'kek', 
        ]
    },
    'Wtf': {
        'row': 0,
        'col': 1,
        'associations': [
            'what the fuck', '  WHAT?!', 'wwwwtttffff', 'wtf'
        ]
    },
    'Pog': {
        'row': 0,
        'col': 2,
        'associations': [
            'pog', 'chump', 'chp', 'Champ', 'Pag'
        ]
    },
    'XD': {
        'row': 1,
        'col': 0,
        'associations': [
            'ah', 'eh', 'xd', 'oh'
        ]
    },
    'Insta': {
        'row': 1,
        'col': 1,
        'associations': [
            'instagramm', 'insta',
        ]
    },
    'Ez': {
        'row': 1,
        'col': 2,
        'associations': [
            'ez', 'yeah', 'yea'
        ]
    },
}

PRESSET_DIR = './Presets'

DEFAULT_URL = 'https://www.twitch.tv/shroud/clip/BoringFriendlyCakeAMPTropPunch-2QlYA8L3W3INyxDR'
# DEFAULT_URL = 'https://www.twitch.tv/sneakylol/clip/MoralConcernedDonkeyRitzMitz-QBUpcsJFVB2DFpfM'
# DEFAULT_URL = 'https://clips.twitch.tv/SpunkyAmazonianWeaselRuleFive-WKcbQ25JvC2ETowA'
# DEFAULT_URL = 'https://www.twitch.tv/ESL_CSGO/clip/SpunkyAmazonianWeaselRuleFive-WKcbQ25JvC2ETowA'
USER_AGENT = None
PROXY = None
BROWSER_HEADLESS_MODE    = False
BROWSER_MAXIMIZED_WINDOW = False

FONT_PATH = f'{PRESSET_DIR}/font.ttf'
FONT_NAME = 'axiforma'

DEFAULT_WINDOW_RESOLUTION    = (1480, 720)
SCREENSHOT_RESOLUTION        = (1280, 720)
PREVIEW_LABEL_MAX_RESOLUTION = (1000, 500)
PREVIEW_LABEL_MIN_RESOLUTION = (500, 500)

DEFAULT_FONT_SIZE = 20
DEFAULT_BUTTON_FONT_SIZE = 20
DEFAULT_STATUS_FRAME_FONT_SIZE = 15
DEFAULT_HIDEN_TAG_COUNT_FONT_SIZE = 60
DEFAULT_HIDEN_TAG_NAME_FONT_SIZE = 30
DEFAULT_TOOLTIP_FONT_SIZE = 15
DEFAULT_LINK_LINE_EDIT_FONT_SIZE = 10

DEFAUT_HIDEN_ITEM_SIZE = 200

PREVIEW_IMAGE_PATH = f'{PRESSET_DIR}/Preview.png'

FPS = 30
VIDEO_NAME = 'NewVideo.avi'

READY = True
PRESETS_PATH = f'{PRESSET_DIR}/settings.json'
DEV_MODE = True

CHROMEDRIVER_PATH = f'{PRESSET_DIR}/chromedriver.exe'
SCREENSHOTS_PATH = './Screenshots'


def ReadFile(SourceData: dict={}):
    """
    Открывает файл с настройками и импортирует все данные из него в виде json-словаря
    
    * ``SourceData`` - Исходный json-словарь с константами из модуля Config 
    """
    FileData = SourceData
    try:
        with open(PRESETS_PATH, 'r', encoding='utf-8') as f:
            FileData = json.load(f, parse_int=int, parse_float=float)
            FileData['READY']
    except (FileNotFoundError, KeyError):
        if not DEV_MODE:
            with open(PRESETS_PATH, 'w', encoding='utf-8') as f:
                json.dump(SourceData, f, indent=1, ensure_ascii=False)
    return FileData


# ==========================================================
# Обновляет содержимое модуля Config при его импорте
# ==========================================================
from pprint import pprint
import json

SourceData = {}
for var in dir():
    if not var.startswith("__") and var.isupper():
        SourceData[var] = locals()[var]

FileData = ReadFile(SourceData)
globals().update(FileData)
# ==========================================================