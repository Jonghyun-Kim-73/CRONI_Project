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
        self.PreAbnormalW.setObjectName("BG")
        self.AbnormalW.setObjectName("BG")
        self.EmergencyW.setObjectName("BG")

        self.vl.addWidget(self.PreAbnormalW)
        self.vl.addWidget(self.AbnormalW)
        self.vl.addWidget(self.EmergencyW)
        self.vl.setSpacing(15)
        self.vl.addStretch(1)
        self.inmem.widget_ids['MainTabRightPreAbnormalW'].diable_widget(True)
        self.inmem.widget_ids['MainTabRightAbnormalW'].diable_widget(True)
        self.inmem.widget_ids['MainTabRightEmergencyW'].diable_widget(True)

class MainTabRightPreAbnormalW(ABCWidget):
    def __init__(self, parent):
        super(MainTabRightPreAbnormalW, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(945, 365)
        self.w_title_layout = QWidget(self)
        self.w_title_layout.setObjectName('RightTabTitleBG1')
        self.w_title_layout.setFixedSize(945, 70)

        self.w_title = QLabel('Pre-abnormal')
        self.w_title.setObjectName('RightTabTitle1')

        self.gotobtn = QPushButton('IFAP')
        self.gotobtn.setObjectName("RightTabBtn1")
        self.gotobtn.setFixedSize(254, 51)
        self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallIFAP'].dis_update)

        self.w_contents = QLabel('...')
        self.w_contents.setObjectName('RightTabContent')
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

    
class MainTabRightAbnormalW(ABCWidget):
    def __init__(self, parent):
        super(MainTabRightAbnormalW, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(945, 365)

        self.w_title_layout = QWidget(self)
        self.w_title_layout.setObjectName('RightTabTitleBG2')
        self.w_title_layout.setFixedSize(945, 70)

        self.w_title = QLabel('Abnormal')
        self.w_title.setObjectName('RightTabTitle1')

        self.gotobtn = QPushButton('AIDAA')
        self.gotobtn.setObjectName("RightTabBtn1")
        self.gotobtn.setFixedSize(254, 51)
        self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallAIDAA'].dis_update)

        self.w_contents = QLabel('...')
        self.w_contents.setObjectName('RightTabContent')
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

class MainTabRightEmergencyW(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabRightEmergencyW, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(945, 365)

        self.w_title_layout = QWidget(self)
        self.w_title_layout.setObjectName('RightTabTitleBG3')
        self.w_title_layout.setFixedSize(945, 70)

        self.w_title = QLabel('Emergency')
        self.w_title.setObjectName('RightTabTitle1')

        self.gotobtn = QPushButton('EGIS')
        self.gotobtn.setObjectName("RightTabBtn1")
        self.gotobtn.setFixedSize(254, 51)
        self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallEGIS'].dis_update)

        self.w_contents = QLabel('...')
        self.w_contents.setObjectName('RightTabContent')
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

