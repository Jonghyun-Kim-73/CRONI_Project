import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_MainTabMain import *
from AIDAA_Ver21.Interface_MainTabAIDAA import *
from AIDAA_Ver21.Interface_AIDAA_Procedure import *
from AIDAA_Ver21.Interface_AIDAA_Action import *
from AIDAA_Ver21.Interface_AIDAA_Pretrip import *
from AIDAA_Ver21.Interface_EGIS_Main import *

from Interface_QSS import qss
from datetime import datetime

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

class Main(QWidget):
    def __init__(self, ShMem):
        super(Main, self).__init__()
        self.inmem:InterfaceMem = InterfaceMem(ShMem, self)
        self.setGeometry(0, 0, 1920, 1200)
        self.setFixedSize(1920, 1200)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 상단바 제거
        self.setObjectName('Main')
        self.setStyleSheet(qss)
        self.m_flag = False
        # Frame ------------------------------------------------------
        self.top = MainTop(self)
        self.tab = MainTab(self)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)  # margin 제거
        lay.addWidget(self.top)
        lay.addWidget(self.tab)
        lay.setSpacing(0)   # margin 제거
        # End frame --------------------------------------------------

    # window drag
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton) and self.top.underMouse():
        # if (event.button() == Qt.LeftButton):  # 화면 움직이기 위함
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag and self.top.underMouse():
        # if Qt.LeftButton and self.m_flag:  # 화면 움직이기 위함
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 윈도우 position 변경
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def close(self) -> bool:
        QApplication.closeAllWindows()
        return super().close()        
# ----------------------------------------------------------------------------------------------------------------------
# MainTop
# ----------------------------------------------------------------------------------------------------------------------
class MainTop(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedHeight(50)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(10, 7, 8, 7)
        title_left = QHBoxLayout()
        title_left.setContentsMargins(0, 0, 5, 0)
        title_left.addWidget(MainTopTime(self))
        title_left.addWidget(MainTopSystemName(self))
        title_left.setSpacing(10)
        lay.addLayout(title_left)
        lay.setSpacing(10)
        # 현재 click된 btn & btn hover color 변경 위함
        self.btnGroup = QButtonGroup()

        btn1 = MainTopCallMain(self)
        btn2 = MainTopCallIFAP(self)
        btn3 = MainTopCallAIDAA(self)
        btn4 = MainTopCallEGIS(self)

        self.btnGroup.addButton(btn1, 0)
        self.btnGroup.addButton(btn2, 1)
        self.btnGroup.addButton(btn3, 2)
        self.btnGroup.addButton(btn4, 3)
        btn1.setChecked(True)

        lay.addWidget(btn1)
        lay.addWidget(btn2)
        lay.addWidget(btn3)
        lay.addWidget(btn4)
        lay.addWidget(MainTopClose(self))
class MainTopTime(ABCLabel):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedSize(465, 36)
        self.startTimer(200)
        self.time_freeze = datetime.now() # 현재 시간 Pick 하고 Freeze
        
    def timerEvent(self, a0: 'QTimerEvent') -> None:
        """ 타이머 디스플레이 업데이트 """
        current_time = self.time_freeze + self.inmem.get_td() # 현재시간 + time_delta()
        real_time = current_time.strftime('%Y.%m.%d')
        real_time2 = current_time.strftime("%H:%M:%S")
        self.setText(real_time + " / " + real_time2)
        return super().timerEvent(a0)
class MainTopSystemName(ABCLabel):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedSize(465, 36)
        self.setContentsMargins(0, 0, 0, 0)
        self.setText('Main')
class MainTopCallMain(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Main')
        self.setFixedSize(218, 36)
        self.clicked.connect(self.dis_update)
        self.setCheckable(True)
        self.setChecked(False)

    def dis_update(self):
        self.setChecked(True)
        self.inmem.widget_ids['MainTopSystemName'].setText('Main')
        self.inmem.widget_ids['MainTab'].change_system_page('Main')
class MainTopCallIFAP(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Pre-abnormal')
        self.setFixedSize(218, 36)
        self.clicked.connect(self.dis_update)
        self.setCheckable(True)
        self.setChecked(False)

    def dis_update(self):
        self.setChecked(True)
        self.inmem.widget_ids['MainTopSystemName'].setText('IFAP')
        self.inmem.widget_ids['MainTab'].change_system_page('IFAP')
class MainTopCallAIDAA(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Abnormal')
        self.setFixedSize(218, 36)
        self.clicked.connect(self.dis_update)
        self.setCheckable(True)
        self.setChecked(False)

    def dis_update(self):
        self.setChecked(True)
        self.inmem.widget_ids['MainTopSystemName'].setText('AIDAA')
        self.inmem.widget_ids['MainTab'].change_system_page('AIDAA')
class MainTopCallEGIS(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Emergency')
        self.setFixedSize(218, 36)
        self.clicked.connect(self.dis_update)
        self.setCheckable(True)
        self.setChecked(False)

    def dis_update(self):
        self.setChecked(True)
        self.inmem.widget_ids['MainTopSystemName'].setText('EGIS')
        self.inmem.widget_ids['MainTab'].change_system_page('EGIS')
class MainTopClose(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        icon = os.path.join(ROOT_PATH, '../AIDAA_Ver21/Img/close.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(35, 35))  # 아이콘 크기
        self.setFixedSize(QSize(35, 35))
        self.setContentsMargins(0, 0, 0, 0)
        self.clicked.connect(self.close_main)

    def close_main(self):
        self.inmem.widget_ids['Main'].close()
# ----------------------------------------------------------------------------------------------------------------------
# MainTab
# ----------------------------------------------------------------------------------------------------------------------
class MainTab(ABCStackWidget):
    def __init__(self, parent):
        super(MainTab, self).__init__(parent)
        [self.addWidget(_) for _ in [MainTabMain(self), MainTabIFAP(self), MainTabAIDAA(self), MainTabEGIS(self), Procedure(self), 
                                     Action(self), PreTrip(self)]]

    def change_system_page(self, system_name: str):
        """요청한 index 페이지로 전환

        Args:
            system_name (str): Main, IFAP, ...
        """
        self.setCurrentIndex({'Main': 0, 'IFAP': 1, 'AIDAA': 2, 'EGIS': 3, 'Procedure': 4, 'Action': 5, 'PreTrip': 6}[system_name])

class MainTabIFAP(ABCWidget):
    def __init__(self, parent):
        super(MainTabIFAP, self).__init__(parent)
class MainTabEGIS(ABCWidget):
    def __init__(self, parent):
        super(MainTabEGIS, self).__init__(parent)
        self.EGISapp = EGISmain(self)
        self.EGISapp.show()