from os import name
import time
from threading import Thread

import Config
from Constants import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class HidenTagFrame(QFrame):
    PAINTER_ACCESS = True
    SaveScreenShotSignal = pyqtSignal(int)
    def __init__(self, parent: QFrame):
        super().__init__(parent)

        self.setFixedSize(*Config.SCREENSHOT_RESOLUTION)
        self.setStyleSheet(HidenTagFramePreference.STYLESHEET)
        self.hide()

        self.ITEM_DICT = {}

        self.MainGridLayout = QGridLayout()
        self.setLayout(self.MainGridLayout)

        self.UpdateMainForm()
        self.SaveScreenShotSignal.connect(self.SaveScreenShot)
        pass

    def SavePreviewImage(self):
        if self.PAINTER_ACCESS:
            return self.grab().save(Config.PREVIEW_IMAGE_PATH, 'png', quality=100)
        return False

    def SavePreviewImageToBuffer(self):
        return self.grab()

    def SaveScreenShot(self, Name: str=VideoPreference.SCREENSHOT_NAME):
        return self.grab().save(f'{Config.SCREENSHOTS_PATH}/{Name}' , 'png', quality=100)

    def UpdateValue(self, Tag: str, Value: int):
        self.ITEM_DICT[Tag].setText(str(Value))
        pass

    def UpdateMainForm(self):
        for Tag, Data in Config.TAGS_DICT.items():
            ItemFrame = QFrame(self)
            ItemFrame.setMinimumWidth(Config.DEFAUT_HIDEN_ITEM_SIZE)

            ItemLayout = QVBoxLayout()
            ItemLayout.setSpacing(20)
            ItemLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ItemFrame.setLayout(ItemLayout)

            TagCountLabel = QLabel(self)
            TagCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            TagCountLabel.setFont(QFont(Config.FONT_NAME, Config.DEFAULT_HIDEN_TAG_COUNT_FONT_SIZE))
            TagCountLabel.setText('0')
            self.ITEM_DICT[Tag] = TagCountLabel

            TagNameLabel = QLabel(self)
            TagNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            TagNameLabel.setFont(QFont(Config.FONT_NAME, Config.DEFAULT_HIDEN_TAG_NAME_FONT_SIZE))
            TagNameLabel.setText(Tag)

            ItemLayout.addWidget(TagCountLabel)
            ItemLayout.addWidget(TagNameLabel)

            self.MainGridLayout.addWidget(ItemFrame, Data['row'], Data['col'])
        pass
    



class TagFrame(QFrame):
    UpdatePreviewImageLabelFromBufferSignal = pyqtSignal()
    def __init__(self, Window: QMainWindow):
        super().__init__()

        self.MainVBoxLayout = QVBoxLayout()
        self.MainVBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.MainVBoxLayout.setSpacing(0)
        self.setLayout(self.MainVBoxLayout)

        self.PreviewImageLabel = QLabel(self)
        self.PreviewImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PreviewImageLabel.setStyleSheet(PreviewImageLabelPreference.PREVIEW_STYLESHEET)
        self.PreviewImageLabel.setMinimumSize(*Config.PREVIEW_LABEL_MIN_RESOLUTION)
        self.PreviewImageLabel.setMaximumSize(*Config.PREVIEW_LABEL_MAX_RESOLUTION)
        self.PreviewImageLabel.setScaledContents(True)
        
        self.HidenTagFrame = HidenTagFrame(self)
        self.MainVBoxLayout.addWidget(self.PreviewImageLabel)
        
        self.UpdatePreviewImageLabelFromBufferSignal.connect(self.UpdatePreviewImageLabelFromBuffer)
        # self.UpdatePreviewImageLabel()
        self.UpdatePreviewImageLabelFromBufferSignal.emit()
        
    def UpdatePreviewImageLabel(self):
        if self.HidenTagFrame.SavePreviewImage():
            self.PreviewImageLabel.setPixmap(QPixmap(Config.PREVIEW_IMAGE_PATH))

    def UpdatePreviewImageLabelFromBuffer(self):
        self.PreviewImageLabel.setPixmap(self.HidenTagFrame.SavePreviewImageToBuffer())