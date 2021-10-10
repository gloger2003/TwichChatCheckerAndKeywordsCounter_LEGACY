import Config
from Constants import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import CustomButtonModule
from . import TagFrameModule

class CheckerButton(CustomButtonModule.CustomButton):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent, CheckerButtonPreference.START_BUTTON_TEXT)

class NewBrowserButton(CustomButtonModule.CustomButton):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent, NewBrowserButtonPreference.CREATE_BUTTON_TEXT)

class ProfileLayout(QVBoxLayout):
    def __init__(self, Window: QMainWindow=None):
        super().__init__()
        self.setSpacing(10)
        self.Window = Window

        self.CheckerButton = CheckerButton()
        self.NewBrowserButton = NewBrowserButton()
        self.TagFrame = TagFrameModule.TagFrame(Window)

        self.addWidget(self.TagFrame)
        self.addWidget(self.NewBrowserButton)
        self.addWidget(self.CheckerButton)