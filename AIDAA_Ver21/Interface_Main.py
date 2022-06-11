import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_MainTabMain import *
from AIDAA_Ver21.Interface_MainTabAIDAA import *
import Interface_QSS as qss
from datetime import datetime

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

class Main(QWidget):
    def __init__(self, ShMem):
        super(Main, self).__init__()
        self.inmem:InterfaceMem = InterfaceMem(ShMem, self)
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 상단바 제거
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)  # margin 제거
        lay.addWidget(MainTop(self))
        lay.addWidget(MainTab(self))

# ----------------------------------------------------------------------------------------------------------------------
# MainTop
# ----------------------------------------------------------------------------------------------------------------------


class MainTop(ABCWidget):
    def __init__(self, parent):
        super(MainTop, self).__init__(parent)
        self.setStyleSheet(qss.Top_Bar)
        self.setObjectName("BG")
        self.setFixedHeight(45)
        QFontDatabase.addApplicationFont("Arial.ttf")
        lay = QHBoxLayout(self)
        lay.setContentsMargins(5, 0, 0, 0)
        lay.addWidget(MainTopTime(self))
        lay.addWidget(MainTopSystemName(self))

        # 현재 click된 btn & btn hover color 변경 위함
        self.btnGroup = QButtonGroup()
        self.btnGroup.setExclusive(False)
        self.btnGroup.buttonClicked[int].connect(self.btnClicked)

        btn1 = MainTopCallMain(self)
        btn2 = MainTopCallIFAP(self)
        btn3 = MainTopCallAIDAA(self)
        btn4 = MainTopCallEGIS(self)

        self.btnGroup.addButton(btn1, 0)
        self.btnGroup.addButton(btn2, 1)
        self.btnGroup.addButton(btn3, 2)
        self.btnGroup.addButton(btn4, 3)

        lay.addWidget(btn1)
        lay.addWidget(btn2)
        lay.addWidget(btn3)
        lay.addWidget(btn4)
        lay.addWidget(MainTopClose(self))

    def btnClicked(self, id):
        for button in self.btnGroup.buttons():
            if button is self.btnGroup.button(id):
                button.setStyleSheet("QPushButton {background: rgb(0, 176, 218);} QPushButton:hover {background: rgb(0, 176, 218)}")
            else:
                button.setStyleSheet("QPushButton {background: rgb(231, 231, 234);} QPushButton:hover {background: rgb(0, 176, 218)}")


class MainTopTime(ABCLabel):
    def __init__(self, parent):
        super(MainTopTime, self).__init__(parent)
        self.setObjectName("Title")
        self.setFixedSize(314, 35)
        # timer section
        timer = QTimer(self)
        timer.setInterval(200)
        #timer.timeout.connect(lambda: self.setText(self.inmem.get_time()))
        timer.timeout.connect(self.dis_update)
        timer.start()

    def dis_update(self):
        """ 타이머 디스플레이 업데이트 """
        real_time = datetime.now().strftime('%Y.%m.%d')
        real_time2 = datetime.now().strftime('%H:%M:%S')
        self.setText(real_time + " / " + real_time2)


class MainTopSystemName(ABCLabel):
    def __init__(self, parent):
        super(MainTopSystemName, self).__init__(parent)
        self.setObjectName("Title")
        self.setFixedSize(633, 35)
        # timer section
        timer = QTimer(self)
        timer.setInterval(200)
        timer.timeout.connect(self.dis_update)
        timer.start()

    def dis_update(self):
        self.setText(self.inmem.get_current_system_name())


class MainTopCallMain(ABCPushButton):
    def __init__(self, parent):
        super(MainTopCallMain, self).__init__(parent)
        self.setText('Main')
        self.setObjectName("Tab")
        self.setFixedSize(223, 35)
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.inmem.change_current_system_name('Main')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()


class MainTopCallIFAP(ABCPushButton):
    def __init__(self, parent):
        super(MainTopCallIFAP, self).__init__(parent)
        self.setText('IFAP')
        self.setObjectName("Tab")
        self.setFixedSize(223, 35)
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.inmem.change_current_system_name('IFAP')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()


class MainTopCallAIDAA(ABCPushButton):
    def __init__(self, parent):
        super(MainTopCallAIDAA, self).__init__(parent)
        self.setText('AIDAA')
        self.setObjectName("Tab")
        self.setFixedSize(223, 35)
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.inmem.change_current_system_name('AIDAA')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()


class MainTopCallEGIS(ABCPushButton):
    def __init__(self, parent):
        super(MainTopCallEGIS, self).__init__(parent)
        self.setText('EGIS')
        self.setObjectName("Tab")
        self.setFixedSize(223, 35)
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.inmem.change_current_system_name('EGIS')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()


class MainTopClose(ABCPushButton):
    def __init__(self, parent):
        super(MainTopClose, self).__init__(parent)
        icon = os.path.join(ROOT_PATH, '../AIDAA_Ver21/Img/close.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(35, 35))  # 아이콘 크기
        self.setFixedSize(QSize(35, 35))
        self.clicked.connect(self.close_main)

    def close_main(self):
        self.inmem.widget_ids['Main'].close()

# ----------------------------------------------------------------------------------------------------------------------
# MainTab
# ----------------------------------------------------------------------------------------------------------------------


class MainTab(ABCStackWidget, QStackedWidget):
    def __init__(self, parent):
        super(MainTab, self).__init__(parent)
        [self.addWidget(_) for _ in [MainTabMain(self), MainTabIFAP(self), MainTabAIDAA(self), MainTabEGIS(self)]]

    def change_system_page(self, system_name):
        self.setCurrentIndex({'Main': 0, 'IFAP': 1, 'AIDAA': 2, 'EGIS': 3}[system_name])


class MainTabIFAP(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabIFAP, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(213, 242, 211);')


class MainTabEGIS(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabEGIS, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(244, 242, 211);')