from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_MainTabMain import *
from AIDAA_Ver21.Interface_MainTabAIDAA import *
from AIDAA_Ver21.Interface_Procedure import *


class Main(QWidget):
    def __init__(self, ShMem):
        super(Main, self).__init__()
        self.inmem:InterfaceMem = InterfaceMem(ShMem, self)
        self.setGeometry(200, 200, 1900, 1000)

        lay = QVBoxLayout(self)
        lay.addWidget(MainTop(self))
        lay.addWidget(MainTab(self))

# ----------------------------------------------------------------------------------------------------------------------
# MainTop
# ----------------------------------------------------------------------------------------------------------------------


class MainTop(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTop, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(149, 185, 211);')

        lay = QHBoxLayout(self)
        lay.addWidget(MainTopTime(self))
        lay.addWidget(MainTopSystemName(self))
        lay.addWidget(MainTopCallMain(self))
        lay.addWidget(MainTopCallIFAP(self))
        lay.addWidget(MainTopCallAIDAA(self))
        lay.addWidget(MainTopCallEGIS(self))
        lay.addWidget(MainTopClose(self))


class MainTopTime(ABCLabel, QLabel):
    def __init__(self, parent):
        super(MainTopTime, self).__init__(parent)
        # timer section
        timer = QTimer(self)
        timer.setInterval(200)
        timer.timeout.connect(lambda: self.setText(self.inmem.get_time()))
        timer.start()


class MainTopSystemName(ABCLabel, QLabel):
    def __init__(self, parent):
        super(MainTopSystemName, self).__init__(parent)
        # timer section
        timer = QTimer(self)
        timer.setInterval(200)
        timer.timeout.connect(self.dis_update)
        timer.start()

    def dis_update(self):
        if self.inmem.get_current_system_name() == 'Procedure':
            self.setText('AIDAA')
        else:
            self.setText(self.inmem.get_current_system_name())


class MainTopCallMain(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(MainTopCallMain, self).__init__(parent)
        self.setText('Main')
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.inmem.change_current_system_name('Main')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()


class MainTopCallIFAP(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(MainTopCallIFAP, self).__init__(parent)
        self.setText('IFAP')
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.inmem.change_current_system_name('IFAP')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()


class MainTopCallAIDAA(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(MainTopCallAIDAA, self).__init__(parent)
        self.setText('AIDAA')
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.inmem.change_current_system_name('AIDAA')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()


class MainTopCallEGIS(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(MainTopCallEGIS, self).__init__(parent)
        self.setText('EGIS')
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.inmem.change_current_system_name('EGIS')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()


class MainTopClose(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(MainTopClose, self).__init__(parent)
        self.setText('X')
        self.clicked.connect(self.close_main)

    def close_main(self):
        self.inmem.widget_ids['Main'].close()

# ----------------------------------------------------------------------------------------------------------------------
# MainTab
# ----------------------------------------------------------------------------------------------------------------------


class MainTab(ABCStackWidget, QStackedWidget):
    def __init__(self, parent):
        super(MainTab, self).__init__(parent)
        [self.addWidget(_) for _ in [MainTabMain(self), MainTabIFAP(self), MainTabAIDAA(self), MainTabEGIS(self), Procedure(self)]]

    def change_system_page(self, system_name):
        self.setCurrentIndex({'Main': 0, 'IFAP': 1, 'AIDAA': 2, 'EGIS': 3, 'Procedure': 4}[system_name])


class MainTabIFAP(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabIFAP, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(213, 242, 211);')


class MainTabEGIS(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabEGIS, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(244, 242, 211);')