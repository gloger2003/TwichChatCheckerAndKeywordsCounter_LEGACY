import Config

class GeneralPreference:
    WINDOW_TITLE_TEXT = 'Twitch Checker 3.2 Core Remake Edition'
    WINDOW_ICON_PATH  = f'{Config.PRESSET_DIR}/icon.ico'

    TOOLTIP_STYLESHEET = 'QToolTip { border: 1px; border-radius: 15px; font-size:' + f'{Config.DEFAULT_TOOLTIP_FONT_SIZE}px;' + '}'
    pass

class VideoPreference:
    SCREENSHOT_NAME  = 'tmp.png'
    SCREENSHOT_PATH  = './Screenshot/'
    SCREENSHOT_TIME_DELAY = 1 // 30

class CheckerButtonPreference:
    START_BUTTON_TEXT = 'Запустить счётчик'
    STOP_BUTTON_TEXT  = 'Остановить счётчик'
    START_STYLESHEET = ''
    STOP_STYLESHEET  = 'color: rgb(250, 150, 100);'

class SettingsButtonPreference:
    ICON_PATH = f'{Config.PRESSET_DIR}/settings_icon.png'
    BUTTON_TEXT = 'Настройки'
    TOOLTIP_TEXT = 'Открыть настройки программы'
    MAX_WIDTH = 200

class StatusFramePreference:
    MAIN_STYLESHEET     = str(f'border-radius: {Config.DEFAULT_BUTTON_FONT_SIZE // 2}px;')
    OK_STYLESHEET       = 'color: rgb(150, 250, 100);' + MAIN_STYLESHEET
    WARNING_STYLESHEET  = 'color: rgb(250, 250, 100);' + MAIN_STYLESHEET
    ERROR_STYLESHEET    = 'color: rgb(250, 150, 100);' + MAIN_STYLESHEET

class NewBrowserButtonPreference:
    CREATE_BUTTON_TEXT = 'Новое окно Google Chrome'

class PreviewScreenShotButtonPreference:
    BUTTON_TEXT = 'Обновить Preview'

class PreviewVideoButtonPreference:
    BUTTON_TEXT = 'Создать Preview-видео'

class PreviewImageLabelPreference:
    PREVIEW_STYLESHEET = f'border-radius: 5px; border: 1px solid rgb(100, 100, 250); background-color: rgb(0, 255, 0);'

class HidenTagFramePreference:
    STYLESHEET = 'background-color: rgba(0, 255, 0, 255);'

class TagFramePreference:
    STYLESHEET = 'background-color: rgb(30, 30, 30); border-radius: 5px; border: 1px solid rgb(100, 100, 250);'
    FORM_STYLESHEET = 'border: 0px;'

class JumpButtonPreference:
    BUTTON_TEXT = 'Перейти'
    LOADING_BUTTON_TEXT = 'Загружаю'

class CreateNewBrowserThreadPreference:
    CREATE_WINDOW = 0
    CREATE_WINDOW_AND_OPEN_LINK = 1
    CREATE_WINDOW_AND_OPEN_LINK_AND_RUN_CHECK_CHAT = 2