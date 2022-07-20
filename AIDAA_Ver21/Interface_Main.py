import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_MainTabMain import *
from AIDAA_Ver21.Interface_MainTabAIDAA import *
from AIDAA_Ver21.Interface_AIDAA_Procedure import *
from AIDAA_Ver21.Interface_AIDAA_Action_ import *
from AIDAA_Ver21.Interface_AIDAA_Pretrip import *

import Interface_QSS as qss
from datetime import datetime

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

class Main(QWidget):
    def __init__(self, ShMem):
        super(Main, self).__init__()
        self.inmem:InterfaceMem = InterfaceMem(ShMem, self)
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 상단바 제거
        QFontDatabase.addApplicationFont("Arial.ttf")
        QFontDatabase.addApplicationFont("맑은 고딕.ttf")

        self.top = MainTop(self)
        self.tab = MainTab(self)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)  # margin 제거
        lay.addWidget(self.top)
        lay.addWidget(self.tab)
        lay.setSpacing(0)   # margin 제거
        
        self.m_flag = False

    # window drag
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton) and self.top.underMouse():
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag and self.top.underMouse():
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 윈도우 position 변경
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

# ----------------------------------------------------------------------------------------------------------------------
# MainTop
# ----------------------------------------------------------------------------------------------------------------------


class MainTop(ABCWidget):
    def __init__(self, parent):
        super(MainTop, self).__init__(parent)
        self.setStyleSheet(qss.Top_Bar)
        self.setObjectName("BG")
        self.setFixedHeight(45)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(5, 5, 5, 5)
        lay.addWidget(MainTopTime(self))
        lay.addWidget(MainTopSystemName(self))
        lay.setSpacing(5)
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
        self.setFixedSize(315, 35)
        # timer section
        timer = QTimer(self)
        timer.setInterval(200)
        timer.timeout.connect(self.dis_update)
        timer.start()

    def dis_update(self):
        """ 타이머 디스플레이 업데이트 """
        current_time = datetime.now() + self.inmem.get_td() # 현재시간 + time_delta()
        real_time = current_time.strftime('%Y.%m.%d')
        real_time2 = current_time.strftime("%H:%M:%S")
        self.setText(real_time + " / " + real_time2)

class MainTopSystemName(ABCLabel):
    def __init__(self, parent):
        super(MainTopSystemName, self).__init__(parent)
        self.setObjectName("Title")
        self.setFixedSize(634, 35)
        # timer section
        timer = QTimer(self)
        timer.setInterval(200)
        timer.timeout.connect(self.dis_update)
        timer.start()

    def dis_update(self):
        if self.inmem.get_current_system_name() == 'Procedure':
            self.setText('AIDAA')
        elif self.inmem.get_current_system_name() == 'Action':
            self.setText('AIDAA')
        elif self.inmem.get_current_system_name() == 'PreTrip':
            self.setText('AIDAA')
        else:
            self.setText(self.inmem.get_current_system_name())


class MainTopCallMain(ABCPushButton):
    def __init__(self, parent):
        super(MainTopCallMain, self).__init__(parent)
        self.setText('Main')
        self.setObjectName("Tab")
        self.setFixedSize(224, 35)
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.inmem.change_current_system_name('Main')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()


class MainTopCallIFAP(ABCPushButton):
    def __init__(self, parent):
        super(MainTopCallIFAP, self).__init__(parent)
        self.setText('Pre-abnormal')
        self.setObjectName("Tab")
        self.setFixedSize(224, 35)
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.inmem.change_current_system_name('IFAP')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()


class MainTopCallAIDAA(ABCPushButton):
    def __init__(self, parent):
        super(MainTopCallAIDAA, self).__init__(parent)
        self.setText('Abnormal')
        self.setObjectName("Tab")
        self.setFixedSize(224, 35)
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.inmem.change_current_system_name('AIDAA')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()


class MainTopCallEGIS(ABCPushButton):
    def __init__(self, parent):
        super(MainTopCallEGIS, self).__init__(parent)
        self.setText('Emergency')
        self.setObjectName("Tab")
        self.setFixedSize(224, 35)
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


class MainTab(ABCStackWidget):
    def __init__(self, parent):
        super(MainTab, self).__init__(parent)
        [self.addWidget(_) for _ in [MainTabMain(self), MainTabIFAP(self), MainTabAIDAA(self), MainTabEGIS(self),
                                     Procedure(self), Action(self), PreTrip(self)]]

    def change_system_page(self, system_name: str):
        """요청한 index 페이지로 전환

        Args:
            system_name (str): Main, IFAP, ...
        """
        self.setCurrentIndex({'Main': 0, 'IFAP': 1, 'AIDAA': 2, 'EGIS': 3, 'Procedure': 4, 'Action': 5, 'PreTrip': 6}[system_name])

class MainTabIFAP(ABCWidget):
    def __init__(self, parent):
        super(MainTabIFAP, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(213, 242, 211);')

class MainTabEGIS(ABCWidget):
    def __init__(self, parent):
        super(MainTabEGIS, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(244, 242, 211);')