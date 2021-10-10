import Config
from Constants import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class CustomButton(QPushButton):
    def __init__(self, parent: QWidget=None, DefaultText: str='Кнопка'):
        super().__init__(parent)
        self.setText(DefaultText)
        self.setFont(QFont(Config.FONT_NAME, Config.DEFAULT_BUTTON_FONT_SIZE))