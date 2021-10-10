import Config
from Constants import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import CustomButtonModule
from . import HidenTagFrameModule


class PreviewScreenShotButton(CustomButtonModule.CustomButton):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent, PreviewScreenShotButtonPreference.BUTTON_TEXT)

class PreviewVideoButton(CustomButtonModule.CustomButton):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent, PreviewVideoButtonPreference.BUTTON_TEXT)



class ProfileHidenLayout(QVBoxLayout):
    def __init__(self, Window: QMainWindow=None):
        super().__init__()
        self.Window = Window
        self.setSpacing(10)
        # self.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.PreviewScreenShotButton = PreviewScreenShotButton()
        self.PreviewVideoButton = PreviewVideoButton()
        self.HidenTagFrame = HidenTagFrameModule.TagFrame(Window)

        self.PreviewScreenShotButton.clicked.connect(self.HidenTagFrame.UpdatePreviewImageLabel)

        self.addWidget(self.HidenTagFrame)
        self.addWidget(self.PreviewScreenShotButton)
        self.addWidget(self.PreviewVideoButton)
