from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.pyplot import cla
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *


class MainTabRight(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabRight, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(230, 184, 175);')

        self.vl = QVBoxLayout(self)
        self.vl.addWidget(MainTabRightPreAbnormalW(self))
        self.vl.addWidget(MainTabRightAbnormalW(self))
        self.vl.addWidget(MainTabRightEmergencyW(self))       

class MainTabRightPreAbnormalW(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabRightPreAbnormalW, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(230, 184, 165);')

        self.w_title = QLabel('Pre-abnormal')
        self.w_title.setStyleSheet('background-color: rgb(230, 154, 165);')

        self.w_contents = QLabel('...')
        self.w_title.setStyleSheet('background-color: rgb(230, 114, 165);')

        self.hl = QHBoxLayout()
        self.gotobtn = QPushButton('Go to Pre-abnormal page')
        self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallIFAP'].dis_update)
        self.hl.addStretch(1)
        self.hl.addWidget(self.gotobtn)

        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.w_title)
        self.vl.addWidget(self.w_contents)
        self.vl.addLayout(self.hl)

        self.setDisabled(True)

class MainTabRightAbnormalW(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabRightAbnormalW, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(230, 184, 165);')

        self.w_title = QLabel('Abnormal')
        self.w_title.setStyleSheet('background-color: rgb(230, 154, 165);')

        self.w_contents = QLabel('...')
        self.w_title.setStyleSheet('background-color: rgb(230, 114, 165);')

        self.hl = QHBoxLayout()
        self.gotobtn = QPushButton('Go to Abnormal page')
        self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallAIDAA'].dis_update)
        self.hl.addStretch(1)
        self.hl.addWidget(self.gotobtn)

        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.w_title)
        self.vl.addWidget(self.w_contents)
        self.vl.addLayout(self.hl)

        self.setDisabled(True)

class MainTabRightEmergencyW(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabRightEmergencyW, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(230, 184, 165);')

        self.w_title = QLabel('Emergency')
        self.w_title.setStyleSheet('background-color: rgb(230, 154, 165);')

        self.w_contents = QLabel('...')
        self.w_contents.setStyleSheet('background-color: rgb(230, 114, 165);')

        self.hl = QHBoxLayout()
        self.gotobtn = QPushButton('Go to Pre-abnormal page')
        self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallEGIS'].dis_update)
        self.hl.addStretch(1)
        self.hl.addWidget(self.gotobtn)

        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.w_title)
        self.vl.addWidget(self.w_contents)
        self.vl.addLayout(self.hl)

        self.setDisabled(True)