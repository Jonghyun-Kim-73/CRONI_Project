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
        self.setFixedHeight(900)
        self.vl = QVBoxLayout(self)
        self.vl.addWidget(MainTabRightPreAbnormalW(self))
        self.vl.addWidget(MainTabRightAbnormalW(self))
        self.vl.addWidget(MainTabRightEmergencyW(self))
        self.vl.addStretch(1)
        self.inmem.widget_ids['MainTabRightPreAbnormalW'].diable_widget(True)
        self.inmem.widget_ids['MainTabRightAbnormalW'].diable_widget(True)
        self.inmem.widget_ids['MainTabRightEmergencyW'].diable_widget(True)

class MainTabRightPreAbnormalW(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabRightPreAbnormalW, self).__init__(parent)
        self.setStyleSheet('border-radius: 5px; border:1px;')

        self.w_title = QLabel('Pre-abnormal')
        self.w_title.setObjectName('RightTabTitle')

        self.w_contents = QLabel('...')
        self.w_contents.setObjectName('RightTabTitle')

        self.hl = QHBoxLayout()
        self.gotobtn = QPushButton('Go to Pre-abnormal page')
        self.gotobtn.setObjectName("Right")
        self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallIFAP'].dis_update)
        self.hl.addStretch(1)
        self.hl.addWidget(self.gotobtn)

        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.w_title)
        self.vl.addWidget(self.w_contents)
        self.vl.addLayout(self.hl)

    def diable_widget(self, bool_):
        self.w_title.setDisabled(bool_)
        self.w_contents.setDisabled(bool_)
        self.gotobtn.setDisabled(bool_)

    
class MainTabRightAbnormalW(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabRightAbnormalW, self).__init__(parent)
        self.setStyleSheet('border-radius: 5px; border:1px;')

        self.w_title = QLabel('Abnormal')
        self.w_title.setObjectName('RightTabTitle')

        self.w_contents = QLabel('...')
        self.w_contents.setObjectName('RightTabTitle')

        self.hl = QHBoxLayout()
        self.gotobtn = QPushButton('Go to Abnormal page')
        self.gotobtn.setObjectName("Right")
        self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallAIDAA'].dis_update)
        self.hl.addStretch(1)
        self.hl.addWidget(self.gotobtn)

        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.w_title)
        self.vl.addWidget(self.w_contents)
        self.vl.addLayout(self.hl)

    def diable_widget(self, bool_):
        self.w_title.setDisabled(bool_)
        self.w_contents.setDisabled(bool_)
        self.gotobtn.setDisabled(bool_)

class MainTabRightEmergencyW(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabRightEmergencyW, self).__init__(parent)
        self.setStyleSheet('border-radius: 5px; border:1px;')

        self.w_title = QLabel('Emergency')
        self.w_title.setObjectName('RightTabTitle')

        self.w_contents = QLabel('...')
        self.w_contents.setObjectName('RightTabTitle')

        self.hl = QHBoxLayout()
        self.gotobtn = QPushButton('Go to Pre-abnormal page')
        self.gotobtn.setObjectName("Right")
        self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallEGIS'].dis_update)
        self.hl.addStretch(1)
        self.hl.addWidget(self.gotobtn)

        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.w_title)
        self.vl.addWidget(self.w_contents)
        self.vl.addLayout(self.hl)

    def diable_widget(self, bool_):
        self.w_title.setDisabled(bool_)
        self.w_contents.setDisabled(bool_)
        self.gotobtn.setDisabled(bool_)

