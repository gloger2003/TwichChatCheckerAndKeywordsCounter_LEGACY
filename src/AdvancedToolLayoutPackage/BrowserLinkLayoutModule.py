import Config
from Constants import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import CustomButtonModule


class JumpButton(CustomButtonModule.CustomButton):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent, JumpButtonPreference.BUTTON_TEXT)

class LinkLineEdit(QLineEdit):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        self.setText(Config.DEFAULT_URL)
        self.setFixedHeight(50)
        self.setFont(QFont(Config.FONT_NAME, Config.DEFAULT_LINK_LINE_EDIT_FONT_SIZE))



class BrowserLinkLayout(QHBoxLayout):
    def __init__(self, Window: QMainWindow):
        super().__init__()
        self.setSpacing(10)
        self.setContentsMargins(0, 0, 0, 0)

        self.JumpButton = JumpButton(Window)
        self.addWidget(self.JumpButton)

        self.LinkLineEdit = LinkLineEdit(Window)
        self.addWidget(self.LinkLineEdit)
