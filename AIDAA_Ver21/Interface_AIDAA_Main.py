import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_MainTabAIDAA import *
from AIDAA_Ver21.Interface_AIDAA_Procedure import *
from AIDAA_Ver21.Interface_AIDAA_Action import *
from AIDAA_Ver21.Interface_AIDAA_Pretrip import *

from Interface_QSS import qss
from datetime import datetime

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

class AIDAAMain(QWidget):
    def __init__(self, ShMem):
        super(AIDAAMain, self).__init__()
        self.inmem:InterfaceMem = InterfaceMem(ShMem, self)
        self.setGeometry(0, 0, 1920, 1200)
        self.setFixedSize(1920, 1200)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 상단바 제거
        self.setObjectName('AIDAAMain')
        self.setStyleSheet(qss)
        self.m_flag = False
        # Frame ------------------------------------------------------
        self.top = AIDAAMainTop(self)
        self.tab = AIDAAMainTab(self)
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
class AIDAAMainTop(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedHeight(50)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(10, 7, 8, 7)
        title_left = QHBoxLayout()
        title_left.setContentsMargins(0, 0, 5, 0)
        title_left.addWidget(AIDAAMainTopTime(self))
        title_left.addWidget(AIDAAMainTopSystemName(self))
        title_left.setSpacing(10)
        lay.addLayout(title_left)
        lay.setSpacing(10)
        # 현재 click된 btn & btn hover color 변경 위함
        self.btnGroup = QButtonGroup()

        btn1 = AIDAAMainTopCallMain(self)

        self.btnGroup.addButton(btn1, 0)
        btn1.setChecked(True)
        lay.addStretch(1)
        lay.addWidget(btn1)
        lay.addWidget(AIDAAMainTopClose(self))
class AIDAAMainTopTime(ABCLabel):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedSize(465, 36)
        self.startTimer(600)
        self.time_freeze = datetime.now() # 현재 시간 Pick 하고 Freeze
        self.simtime = ''
        
    def timerEvent(self, a0: 'QTimerEvent') -> None:
        """ 타이머 디스플레이 업데이트 """
        current_time = self.time_freeze + self.inmem.get_td() # 현재시간 + time_delta()
        real_time = current_time.strftime('%Y.%m.%d')
        self.simtime = current_time.strftime("%H:%M:%S")
        self.setText(real_time + " / " + self.simtime)
        return super().timerEvent(a0)
class AIDAAMainTopSystemName(ABCLabel):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedSize(465, 36)
        self.setContentsMargins(0, 0, 0, 0)
        self.setText('Main')
class AIDAAMainTopCallMain(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Main')
        # self.setFixedSize(218, 36)
        self.setFixedSize(800, 36)
        self.clicked.connect(self.dis_update)
        self.setCheckable(True)
        self.setChecked(False)
    def dis_update(self):
        self.setChecked(True)
        self.inmem.widget_ids['AIDAAMainTopSystemName'].setText('Main')
        self.inmem.widget_ids['AIDAAMainTab'].change_system_page('AIDAA')
class AIDAAMainTopClose(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        icon = os.path.join(ROOT_PATH, '../AIDAA_Ver21/Img/close.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(35, 35))  # 아이콘 크기
        self.setFixedSize(QSize(35, 35))
        self.setContentsMargins(0, 0, 0, 0)
        self.clicked.connect(self.close_main)

    def close_main(self):
        self.inmem.widget_ids['AIDAAMain'].close()
# ----------------------------------------------------------------------------------------------------------------------
# MainTab
# ----------------------------------------------------------------------------------------------------------------------
class AIDAAMainTab(ABCStackWidget):
    def __init__(self, parent):
        super(AIDAAMainTab, self).__init__(parent)
        [self.addWidget(_) for _ in [MainTabAIDAA(self), Procedure(self), Action(self), PreTrip(self)]]

    def change_system_page(self, system_name: str):
        """요청한 index 페이지로 전환

        Args:
            system_name (str): Main, IFAP, ...
        """
        self.setCurrentIndex({'AIDAA': 0, 'Procedure': 1, 'Action': 2, 'PreTrip': 3}[system_name])
        if system_name == 'AIDAA':
            self.inmem.widget_ids['AIDAAMainTopSystemName'].setText('Main')
        elif system_name == 'Procedure':
            self.inmem.widget_ids['AIDAAMainTopSystemName'].setText('Procedure')
        elif system_name == 'Action':
            self.inmem.widget_ids['AIDAAMainTopSystemName'].setText('System')
        elif system_name == 'PreTrip':
            self.inmem.widget_ids['AIDAAMainTopSystemName'].setText('Prediction')