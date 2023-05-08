from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.pyplot import cla
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *

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

    def diable_widget(self, bool_):
        self.w_title.setDisabled(bool_)
        self.w_contents.setDisabled(bool_)
        self.gotobtn.setDisabled(bool_)
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

    def diable_widget(self, bool_):
        self.w_title.setDisabled(bool_)
        self.w_contents.setDisabled(bool_)
        self.gotobtn.setDisabled(bool_)
class MainTabRightAbnormalWTitle(ABCLabel):
    def __init__(self, parent, text, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
class MainTabRightAbnormalWBTN(ABCPushButton):
    def __init__(self, parent, text, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
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