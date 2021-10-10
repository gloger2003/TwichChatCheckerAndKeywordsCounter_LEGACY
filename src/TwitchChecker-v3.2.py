import os
import re
import cv2
import shutil
from threading import Thread
from datetime import datetime
import time

import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import selenium
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions

import Config
from Constants import *

from ProfileLayoutPackage.ProfileLayoutModule import ProfileLayout
from AdvancedToolLayoutPackage.AdvancedToolLayoutModule import AdvancedToolLayout
from AdvancedToolLayoutPackage.BrowserLinkLayoutModule import BrowserLinkLayout
from ProfileHidenLayoutPackage.ProfileHidenLayoutModule import ProfileHidenLayout

def GetTimeStamp():
    return int(datetime.now().timestamp() * 1000)

class Message(object):
    def __init__(self, User: str='', Text: str='', Tick: int=0):
        super().__init__()
        self.User = User
        self.Text = Text
        self.Id = hash(User) + hash(Text)
        self.Tick = Tick

    def __eq__(self, cls):
        return self.Id == cls.Id

    def __ne__(self, cls):
        return self.Id != cls.Id


class Window(QMainWindow):
    CheckChatSignal = pyqtSignal(list)
    SetStatusSignal = pyqtSignal(list)

    def __init__(self):
        super().__init__(parent=None)
        self.RUN_CHECKER = False
        self.CLOSED = False
        self.START_TIMESTAMP = 0
        self.STOP_TIMESTAMP = 0

        self.CheckChatThreadObject        = CheckChatThread(self)
        self.BrowserLoadUrlThreadObject   = BrowserLoadUrlThread(self) 
        self.CreateNewVideoThreadObject   = CreateVideoThread(self, [])
        self.CreateNewBrowserThreadObject = CreateNewBrowserThread(self)

        self.LoadGui()
        self.SetStatusSignal.connect(self.setStatus)
        pass

    def setStatus(self, StatusData: list=[]):
        self.AdvancedToolLayout.StatusFrame.SetStatus(StatusData[0], StatusData[1])

    def closeEvent(self, a0: QCloseEvent):
        self.RUN_CHECKER = False
        self.CLOSED = True
        try:
            Thread(target=self.Driver.quit, args=[]).start()
        except:
            pass
        return super().closeEvent(a0)

    def LoadGui(self):
        """
        Создаёт GUI приложения
        """
        self.CentralWidget = QFrame(self)
        self.setCentralWidget(self.CentralWidget)

        self.MainVBoxLayout = QVBoxLayout()
        self.MainVBoxLayout.setContentsMargins(10, 10, 10, 10)
        self.MainVBoxLayout.setSpacing(10)
        # self.MainVBoxLayout.setAlignment(Qt.AlignmentFlag.AlignBaseline)
        self.CentralWidget.setLayout(self.MainVBoxLayout)

        self.MainHBoxLayout = QHBoxLayout()
        self.MainVBoxLayout.addLayout(self.MainHBoxLayout)

        self.ProfileLayout      = ProfileLayout(self)
        self.BrowserLinkLayout  = BrowserLinkLayout(self)
        self.ProfileHidenLayout = ProfileHidenLayout(self)
        self.AdvancedToolLayout = AdvancedToolLayout(self)

        self.ProfileLayout.CheckerButton.clicked.connect(self.RunChecker)
        self.ProfileLayout.NewBrowserButton.clicked.connect(self.CreateNewBrowserThreadObject.start)
        self.BrowserLinkLayout.JumpButton.clicked.connect(self.BrowserLoadUrlThreadObject.start)
        
        self.MainVBoxLayout.addLayout(self.BrowserLinkLayout)
        self.MainHBoxLayout.addLayout(self.ProfileLayout)
        self.MainHBoxLayout.addLayout(self.ProfileHidenLayout)
        self.MainVBoxLayout.addLayout(self.AdvancedToolLayout)

        self.setFocus()
        pass

    def Center(self):
        """
        Центрирует окно программы
        """
        FrameGeometry = self.frameGeometry()
        Screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        CenterPoint = QApplication.desktop().screenGeometry(Screen).center()
        FrameGeometry.moveCenter(CenterPoint)
        self.move(FrameGeometry.topLeft())

    def RunChecker(self):
        """
        Запускает или останавливает проверку чата, в зависимости от {RUN_CHECKER}
        """
        if self.RUN_CHECKER:
            self.RUN_CHECKER = False
            self.ProfileLayout.CheckerButton.setText(CheckerButtonPreference.START_BUTTON_TEXT)
            self.ProfileLayout.CheckerButton.setStyleSheet(CheckerButtonPreference.START_STYLESHEET)
            self.STOP_TIMESTAMP = GetTimeStamp()
        else:
            self.RUN_CHECKER = True
            self.ProfileLayout.CheckerButton.setText(CheckerButtonPreference.STOP_BUTTON_TEXT)
            self.ProfileLayout.CheckerButton.setStyleSheet(CheckerButtonPreference.STOP_STYLESHEET)
            
            self.CheckChatThreadObject.start()
        self.setFocus()

    def Recount(self, Messages: list=[Message]):
        """
        Считает кол-во повторений того или иного тэга в списке {Messages} сообщений {Message}
        """
        for Tag, Data in Config.TAGS_DICT.items():
            # Кол-во повторений
            Count = 0
            for message in Messages:
                for assoc in Data['associations'] + [Tag]:
                    if message.Text.find(assoc.lower()) != -1:
                        Count += 1
                        break

            # Записываем кол-во повторений тэга в профиль
            self.ProfileLayout.TagFrame.UpdateValue(Tag, Count)
            self.ProfileHidenLayout.HidenTagFrame.HidenTagFrame.UpdateValue(Tag, Count)

        # Записываем общее кол-во сообщений
        self.ProfileLayout.TagFrame.UpdateValue('Messages', len(Messages) - 1)
        try:
            Config.TAGS_DICT['Messages']
            self.ProfileHidenLayout.HidenTagFrame.HidenTagFrame.UpdateValue('Messages', len(Messages) - 1)
        except:
            pass
        pass




class CreateNewBrowserThread(QThread):
    """
    Создаёт новое окно браузера, если старое было закрыто
    """
    def __init__(self, Window: Window):
        self.Window = Window
        super().__init__()
    
    def run(self):
        try:
            self.Window.Driver.quit()
        except:
            pass

        self.Window.CustomChromeOptions = ChromeOptions()
        self.Window.CustomChromeOptions.add_argument('--log-level-0')
        
        if Config.PROXY:
            self.Window.CustomChromeOptions.add_argument(f'--proxy-server={Config.PROXY}')

        if Config.USER_AGENT:
            self.Window.CustomChromeOptions.add_argument(f'User-agent={Config.USER_AGENT}')

        if Config.BROWSER_HEADLESS_MODE: 
            self.Window.CustomChromeOptions.add_argument('--headless')

        if Config.BROWSER_MAXIMIZED_WINDOW:
            self.Window.CustomChromeOptions.add_argument('--start-maximized')
        
        self.Window.Driver = Chrome(chrome_options=self.Window.CustomChromeOptions, executable_path=Config.CHROMEDRIVER_PATH)
        self.deleteLater()

class BrowserLoadUrlThread(QThread):
    """
    закружает указанную страницу
    """
    def __init__(self, Window: Window):
        self.Window = Window
        super().__init__()

    def LoadLink(self):
        Link = self.Window.BrowserLinkLayout.LinkLineEdit.text()
        self.Window.Driver.get(Link)
        pass
    
    def run(self):
        try:
            self.LoadLink()
        except:
            self.Window.CreateNewBrowserThreadObject = CreateNewBrowserThread(self.Window)
            self.Window.CreateNewBrowserThreadObject.finished.connect(self.LoadLink)
            self.Window.CreateNewBrowserThreadObject.start()
            pass
        self.Window.setFocus()

class CheckChatThread(QThread):
    def __init__(self, Window: Window):
        self.Window = Window
        super().__init__()

    def run(self):
        Messages = [Message()]

        ChatClassName = 'chat-line__message'
        TextClassName = 'text-fragment'
        UserClassName = 'chat-author__display-name'

        ChatClassName = 'tw-flex-grow-1'

        self.Window.START_TIMESTAMP = GetTimeStamp()
        
        while self.Window.RUN_CHECKER:
            try:
                # Получаем список сообщений чата или None
                GettedMessageList = self.Window.Driver.find_elements_by_tag_name('li')
                for GettedMessage in GettedMessageList:
                    try:
                        NewMessage = Message\
                        (
                            Text = GettedMessage.find_element_by_class_name(TextClassName).text.lower(),
                            User = GettedMessage.find_element_by_class_name(UserClassName).text,
                            Tick = GetTimeStamp() - self.Window.START_TIMESTAMP
                        )

                        # Модификатор совпадения нового сообщения из списка GettedMessageList, со старым из списка Messages
                        MessageIsFinded = False
                        for LastMessage in Messages[-len(GettedMessageList):]:
                            if NewMessage == LastMessage:
                                MessageIsFinded = True
                                break
                        if not MessageIsFinded:
                            Messages.append(NewMessage)
                    except (TypeError, IndexError, AttributeError, selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.StaleElementReferenceException) as e:
                        ChatClassName = 'tw-flex-grow-1' if ChatClassName == 'chat-line__message' else 'tw-flex-grow-1'
                        print(e)
                            
            except (IndexError, AttributeError, selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.StaleElementReferenceException) as e: 
                ChatClassName = 'tw-flex-grow-1' if ChatClassName == 'chat-line__message' else 'tw-flex-grow-1'
                print(e)
        
            # Пересчитываем для профиля
            self.Window.Recount(Messages)
            self.Window.SetStatusSignal.emit([StatusFramePreference.WARNING_STYLESHEET, f'Получено {len(Messages) - 1} сообщений из чата, прошло {(GetTimeStamp() - self.Window.START_TIMESTAMP) // 1000} сек.'])
        
        print('STOPPED!')

        self.Window.CreateNewVideoThreadObject = CreateVideoThread(self.Window, Messages)
        # self.Window.CreateNewVideoThreadObject.Messages = Messages
        self.Window.CreateNewVideoThreadObject.start()
        # self.deleteLater()

class CreateVideoThread(QThread):
    def __init__(self, Window: Window, Messages: list):
        self.Window = Window
        self.Messages = Messages
        super().__init__()

    def run(self):
        try:
            shutil.rmtree(Config.SCREENSHOTS_PATH)
        except:
            pass
        try:
            os.mkdir(Config.SCREENSHOTS_PATH)
        except Exception as E:
            pass

        HidenTagFrame = self.Window.ProfileHidenLayout.HidenTagFrame.HidenTagFrame
        for Tag, Item in HidenTagFrame.ITEM_DICT.items():
            Item.setText('0')

        width, height = Config.SCREENSHOT_RESOLUTION
        video = cv2.VideoWriter(Config.VIDEO_NAME, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), Config.FPS, (width, height))
        
        AllTicksCount = self.Window.STOP_TIMESTAMP - self.Window.START_TIMESTAMP
        AllScrenShotsCount = AllTicksCount // int(1 / Config.FPS * 1000)
        ScreenShotNumber = 0
        self.Messages.pop(0)
        for Tick in range(AllTicksCount):
            if self.Window.CLOSED or self.Window.RUN_CHECKER: 
                cv2.destroyAllWindows()
                video.release()
                Info = 'Рендер был экстренно остановлен, видео сохранено не полностью!'
                self.Window.SetStatusSignal.emit([StatusFramePreference.ERROR_STYLESHEET, Info])
                self.terminate()
                return
            for message in self.Messages:
                if message.Tick == Tick:
                    for Tag, Data in Config.TAGS_DICT.items():
                        # Кол-во повторений
                        Count = int(HidenTagFrame.ITEM_DICT[Tag].text())
                        AssociationsIsFinded = False
                        if Tag == 'Messages':
                            HidenTagFrame.UpdateValue(Tag, Count + 1)
                            continue
                        else:
                            for assoc in Data['associations'] + [Tag]:
                                if message.Text.find(assoc.lower()) != -1:
                                    AssociationsIsFinded = True
                                    break

                            if AssociationsIsFinded:
                                HidenTagFrame.UpdateValue(Tag, Count + 1)

            if Tick % int(1 / Config.FPS * 1000) == 0:
                HidenTagFrame.SaveScreenShot()

                ScreenShotPath = f'{Config.SCREENSHOTS_PATH}/{VideoPreference.SCREENSHOT_NAME}'
                ScreenShotNumber += 1

                video.write(cv2.imread(ScreenShotPath, cv2.IMREAD_COLOR))
                
                Info = f'Запись кадров: {ScreenShotNumber}/{AllScrenShotsCount}'

                self.Window.SetStatusSignal.emit([StatusFramePreference.WARNING_STYLESHEET, Info])
                
                self.Window.ProfileHidenLayout.HidenTagFrame.UpdatePreviewImageLabelFromBufferSignal.emit()

        Info = f'Рендер завершён. Всего кадров записано: {ScreenShotNumber}. Длительность: {AllTicksCount // 1000} cек. Путь к видео: {Config.VIDEO_NAME}.'
        self.Window.SetStatusSignal.emit([StatusFramePreference.OK_STYLESHEET, Info])
        
        cv2.destroyAllWindows()
        video.release()
        self.deleteLater()



if __name__ == '__main__':
    App = QApplication([])
    App.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    QFontDatabase.addApplicationFont(Config.FONT_PATH)
    App.setFont(QFont(Config.FONT_NAME, Config.DEFAULT_FONT_SIZE))
    
    AppWindow = Window()
    AppWindow.setWindowTitle(GeneralPreference.WINDOW_TITLE_TEXT)
    AppWindow.setWindowIcon(QIcon(GeneralPreference.WINDOW_ICON_PATH))
    AppWindow.setStyleSheet(GeneralPreference.TOOLTIP_STYLESHEET)
    AppWindow.setWindowTitle(GeneralPreference.WINDOW_TITLE_TEXT)
    AppWindow.show()
    AppWindow.resize(*Config.DEFAULT_WINDOW_RESOLUTION)
    AppWindow.Center()
    AppWindow.setMinimumSize(AppWindow.size())
    AppWindow.setMaximumHeight(AppWindow.height())

    App.exec()