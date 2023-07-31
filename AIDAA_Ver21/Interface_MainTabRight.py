import typing
from PyQt5.QtCore import QObject, QTimerEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
import socket
import random

class MainTabRight(ABCWidget):
    def __init__(self, parent):
        super(MainTabRight, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.vl = QVBoxLayout(self)
        self.vl.setContentsMargins(0, 0, 0, 0)
        self.PreAbnormalW = MainTabRightPreAbnormalW(self)
        self.AbnormalW = MainTabRightAbnormalW(self)
        self.EmergencyW = MainTabRightEmergencyW(self)
        self.vl.addWidget(self.PreAbnormalW)
        self.vl.addWidget(self.AbnormalW)
        self.vl.addWidget(self.EmergencyW)
        self.vl.setSpacing(15)
        self.vl.addStretch(1)
        self.inmem.widget_ids['MainTabRightPreAbnormalW'].diable_widget(True)
        self.inmem.widget_ids['MainTabRightAbnormalW'].diable_widget(True)
        self.inmem.widget_ids['MainTabRightEmergencyW'].diable_widget(True)
class MainTabRightPreAbnormalW(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(945, 365)
        self.w_title_layout = QWidget(self)
        self.w_title_layout.setFixedSize(945, 70)

        self.w_title = MainTabRightPreAbnormalWTitle(self, 'Pre-abnormal')

        self.gotobtn = MainTabRightPreAbnormalWBTN(self, 'Go to IFAP')
        self.gotobtn.setFixedSize(254, 51)
        # self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallIFAP'].dis_update)

        self.w_contents = MainTabRightPreAbnormalWContent(self, 'IFAP information')
        self.w_contents.setContentsMargins(10, 0, 0, 0)

        self.hl = QHBoxLayout()

        self.hl.addWidget(self.w_title)
        self.hl.addStretch(1)
        self.hl.addWidget(self.gotobtn)
        self.hl.setContentsMargins(8, 0, 8, 0)
        self.w_title_layout.setLayout(self.hl)

        self.vl = QVBoxLayout(self)
        self.vl.setContentsMargins(0, 0, 0, 0)
        self.vl.addWidget(self.w_title_layout)
        self.vl.addWidget(self.w_contents)
        
        self.IFAP_msg = ''
        self.UDP_thread = MainTabRightPreAbnormalWThread(self)
        self.UDP_thread.start()
        self.startTimer(600)
        
    def diable_widget(self, bool_):
        self.w_title.setDisabled(bool_)
        self.w_contents.setDisabled(bool_)
        self.gotobtn.setDisabled(bool_)
        
    def timerEvent(self, a0: QTimerEvent) -> None:
        self.w_contents.setText(f'Counter Test : {self.IFAP_msg}')
        return super().timerEvent(a0)
class MainTabRightPreAbnormalWTitle(ABCLabel):
    def __init__(self, parent, text, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
class MainTabRightPreAbnormalWBTN(ABCPushButton):
    def __init__(self, parent, text, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
class MainTabRightPreAbnormalWContent(ABCLabel):
    def __init__(self, parent, text, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
class MainTabRightPreAbnormalWThread(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver.bind(('127.0.0.1', 7003))
        self.receiver.settimeout(1.0)
        self.counter = 0
    def run(self) -> None:
        while True:
            try:
                message, _ = self.receiver.recvfrom(1000)
            except:
                pass
            self.counter += 1
            self.parent.IFAP_msg = f'Counter {self.counter}'
class MainTabRightAbnormalW(ABCWidget):
    def __init__(self, parent):
        super(MainTabRightAbnormalW, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(945, 365)
        self.w_title_layout = QWidget(self)
        self.w_title_layout.setFixedSize(945, 70)

        self.w_title = MainTabRightAbnormalWTitle(self, 'Abnormal')

        self.gotobtn = MainTabRightAbnormalWBTN(self, 'AIDAA')
        self.gotobtn.setFixedSize(254, 51)
        # self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallAIDAA'].dis_update)

        self.w_contents = MainTabRightAbnormalWContent(self, '진단 결과: 증기발생기 수위 채널 고장 (고) \n'
                                                             '진단 결과: -')
        self.w_contents.setContentsMargins(10, 0, 0, 0)

        self.hl = QHBoxLayout()

        self.hl.addWidget(self.w_title)
        self.hl.addStretch(1)
        self.hl.addWidget(self.gotobtn)
        self.hl.setContentsMargins(8, 0, 8, 0)
        self.w_title_layout.setLayout(self.hl)

        self.vl = QVBoxLayout(self)
        self.vl.setContentsMargins(0, 0, 0, 0)
        self.vl.addWidget(self.w_title_layout)
        self.vl.addWidget(self.w_contents)
        self.startTimer(1000)

    def diable_widget(self, bool_):
        self.w_title.setDisabled(bool_)
        self.w_contents.setDisabled(bool_)
        self.gotobtn.setDisabled(bool_)

    def timerEvent(self, a0: QTimerEvent) -> None:
        if len(self.inmem.ShMem.get_on_alarms()) >= 2:
            if self.inmem.dis_AI['Train'] == 0 and self.inmem.ShMem.get_para_val('iFixTrain') == 0 or self.inmem.ShMem.get_para_val('iFixTrain') == 1:  # Train 상태
                self.inmem.get_diagnosis_result()
                self.w_contents.setText(f"진단 결과: {self.inmem.dis_AI['AI'][0][0]} \n"
                                        f"진단 정확도: {self.inmem.dis_AI['AI'][0][-1]}")
            elif self.inmem.dis_AI['Train'] == 1 and self.inmem.ShMem.get_para_val('iFixTrain') == 0 or self.inmem.ShMem.get_para_val('iFixTrain') == 2:# Untrain 상태
                self.w_contents.setText(f"진단 결과: 화학 및 체적 제어계통 \n"
                                        f"진단 정확도: {round(random.uniform(98, 100),2)}%")
        else:
            self.w_contents.setText(f"AIDAA 비활성 상태입니다.")
        return super().timerEvent(a0)
class MainTabRightAbnormalWTitle(ABCLabel):
    def __init__(self, parent, text, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
class MainTabRightAbnormalWBTN(ABCPushButton):
    def __init__(self, parent, text, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
        self.startTimer(1000)
    def timerEvent(self, a0: QTimerEvent) -> None:
        if len(self.inmem.ShMem.get_on_alarms()) >= 2:
            if int(self.inmem.ShMem.get_para_val('KCNTOMS') / 5) % 2 == 1:
                self.setStyleSheet('background-color: rgb(0, 176, 218);') # 파란색
            else:
                self.setStyleSheet('background-color: rgb(231, 231, 234);')  # 회색
        else:
            self.setStyleSheet('background-color: rgb(231, 231, 234);') # 회색

class MainTabRightAbnormalWContent(ABCLabel):
    def __init__(self, parent, text, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
class MainTabRightEmergencyW(ABCWidget):
    def __init__(self, parent):
        super(MainTabRightEmergencyW, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(945, 365)
        self.w_title_layout = QWidget(self)
        self.w_title_layout.setFixedSize(945, 70)

        self.w_title = MainTabRightEmergencyWTitle(self, 'Emergency')

        self.gotobtn = MainTabRightEmergencyWBTN(self, 'EGIS')
        self.gotobtn.setFixedSize(254, 51)
        # self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallEGIS'].dis_update)

        self.w_contents = MainTabRightAbnormalWContent(self, 'EGIS information')
        self.w_contents.setContentsMargins(10, 0, 0, 0)

        self.hl = QHBoxLayout()

        self.hl.addWidget(self.w_title)
        self.hl.addStretch(1)
        self.hl.addWidget(self.gotobtn)
        self.hl.setContentsMargins(8, 0, 8, 0)
        self.w_title_layout.setLayout(self.hl)

        self.vl = QVBoxLayout(self)
        self.vl.setContentsMargins(0, 0, 0, 0)
        self.vl.addWidget(self.w_title_layout)
        self.vl.addWidget(self.w_contents)

    def diable_widget(self, bool_):
        self.w_title.setDisabled(bool_)
        self.w_contents.setDisabled(bool_)
        self.gotobtn.setDisabled(bool_)
class MainTabRightEmergencyWTitle(ABCLabel):
    def __init__(self, parent, text, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
class MainTabRightEmergencyWBTN(ABCPushButton):
    def __init__(self, parent, text, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
class MainTabRightEmergencyWContent(ABCLabel):
    def __init__(self, parent, text, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)