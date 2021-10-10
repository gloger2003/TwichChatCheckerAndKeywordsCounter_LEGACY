import Config
from Constants import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class TagFrame(QFrame):
    def __init__(self, parent: QMainWindow=None):
        super().__init__(parent=parent)
        self.setStyleSheet(TagFramePreference.STYLESHEET)

        self.FORM_DICT = {}
        
        self.MainFormLayout = QFormLayout()
        self.MainFormLayout.setContentsMargins(0, 0, 0, 0)
        self.MainFormLayout.setSpacing(10)
        self.setLayout(self.MainFormLayout)

        self.UpdateMainForm()

    def AddForm(self, Tag: str):
        Form = QLabel()
        Form.setAlignment(Qt.AlignmentFlag.AlignRight)
        Form.setStyleSheet(TagFramePreference.FORM_STYLESHEET)
        Form.setText('0')
        self.FORM_DICT[Tag] = Form

        TagLabel = QLabel(Tag)
        TagLabel.setStyleSheet(TagFramePreference.FORM_STYLESHEET)
        self.MainFormLayout.addRow(TagLabel, Form)

    def UpdateMainForm(self):
        for RowIndex in range(self.MainFormLayout.rowCount()):
            self.MainFormLayout.removeRow(RowIndex)

        for Tag in Config.TAGS_DICT:
            self.AddForm(Tag)

    def UpdateValue(self, Tag: str, Value: int):
        self.FORM_DICT[Tag].setText(str(Value))
        pass