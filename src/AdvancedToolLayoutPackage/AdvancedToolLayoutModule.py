import Config
from Constants import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *




class SettingsButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        IconPixmap = QPixmap(SettingsButtonPreference.ICON_PATH)
        self.setFixedSize(IconPixmap.size())
        # self.setMaximumWidth(SettingsButtonPreference.MAX_WIDTH)
        self.setFont(QFont(Config.FONT_NAME, Config.DEFAULT_BUTTON_FONT_SIZE))

        self.setIcon(QIcon(IconPixmap))
        self.setIconSize(QSize(50, 50))

        self.setToolTip(SettingsButtonPreference.TOOLTIP_TEXT)
        # self.setText(SettingsButtonPreference.BUTTON_TEXT)
        
        self.clicked.connect(self.OpenSettingsFrame)
    
    def OpenSettingsFrame(self):
        """
        Открывает окно с настройками
        """
        pass

class StatusFrame(QFrame):
    """
    Фрейм, на котором находится TextLabel, выводящий текущий статус и сообщение
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.MainHBoxLayout = QHBoxLayout()
        self.MainHBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.MainHBoxLayout)

        self.TextLabel = QLabel(self)
        self.TextLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.TextLabel.setFixedHeight(Config.DEFAULT_BUTTON_FONT_SIZE * 4)
        self.TextLabel.setFont(QFont(Config.FONT_NAME, Config.DEFAULT_STATUS_FRAME_FONT_SIZE))

        self.MainHBoxLayout.addWidget(self.TextLabel)
        self.SetStatus()
        pass

    def SetStatus(self, StatusStyleSheet: StatusFramePreference=StatusFramePreference.OK_STYLESHEET, Text: str='Message generated automatically'):
        """
        Меняет текст и статус в StatusFrame
        """
        self.TextLabel.setStyleSheet(StatusStyleSheet)
        self.TextLabel.setText(Text)
        pass

class AdvancedToolLayout(QHBoxLayout):
    """
    Лэй для SettingsButton и StatusFrame
    """
    def __init__(self, parent):
        super().__init__()
        self.setSpacing(10)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.SettingsButton = SettingsButton(parent)
        self.addWidget(self.SettingsButton)

        self.StatusFrame = StatusFrame(parent)
        self.addWidget(self.StatusFrame)