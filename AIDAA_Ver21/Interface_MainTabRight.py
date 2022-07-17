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
        self.hl = QHBoxLayout()
        self.vl.setContentsMargins(0, 0, 0, 0)
        self.hl.setContentsMargins(0, 0, 0, 0)
        # 현재 click된 btn & btn hover color 변경 위함
        self.btnGroup = QButtonGroup()
        self.btnGroup.setExclusive(False)
        self.btnGroup.buttonClicked[int].connect(self.btnClicked)

        btn1 = MainTabRightTopNormalBtn(self)
        btn2 = MainTabRightTopPreabnormalBtn(self)
        btn3 = MainTabRightTopAbnormalBtn(self)
        btn4 = MainTabRightTopEmergencyBtn(self)

        self.btnGroup.addButton(btn1, 0)
        self.btnGroup.addButton(btn2, 1)
        self.btnGroup.addButton(btn3, 2)
        self.btnGroup.addButton(btn4, 3)

        self.hl.addWidget(btn1)
        self.hl.addWidget(btn2)
        self.hl.addWidget(btn3)
        self.hl.addWidget(btn4)

        self.hl.setSpacing(5)
        self.hl.addStretch(1)
        self.vl.addLayout(self.hl)
        self.vl.addWidget(MainTabRightBottomWid(self))
        self.vl.setSpacing(5)
        self.inmem.widget_ids['MainTabRightTopNormalBtn'].dis_update()

    def btnClicked(self, id):
        for button in self.btnGroup.buttons():
            if button is self.btnGroup.button(id):
                button.setStyleSheet("QPushButton {background: rgb(255, 255, 255);} QPushButton:hover {background: rgb(0, 178, 218)}")
            else:
                button.setStyleSheet("QPushButton {background: rgb(128, 128, 128);} QPushButton:hover {background: rgb(0, 178, 218)}")


# ------------------------------------------------------------------------------------------
class MainTabRightTopNormalBtn(ABCPushButton):
    def __init__(self, parent):
        super(MainTabRightTopNormalBtn, self).__init__(parent)
        self.setObjectName("Right")
        self.setFixedSize(224, 35)
        self.setText('Normal')
        self.clicked.connect(self.dis_update)
        
    def dis_update(self):
        self.inmem.widget_ids['MainTabRightBottomWid'].change_condition_page(self.text())
        self.inmem.widget_ids['MainTabRightTopNormalBtn'].dis_on()
        self.inmem.widget_ids['MainTabRightTopPreabnormalBtn'].dis_off()
        self.inmem.widget_ids['MainTabRightTopAbnormalBtn'].dis_off()
        self.inmem.widget_ids['MainTabRightTopEmergencyBtn'].dis_off()
    
    def dis_on(self):
        self.setStyleSheet("QPushButton {background: rgb(255, 255, 255);} QPushButton:hover {background: rgb(0, 178, 218)}")
        
    def dis_off(self):
        self.setStyleSheet("QPushButton {background: rgb(128, 128, 128);} QPushButton:hover {background: rgb(0, 178, 218)}")
    
class MainTabRightTopPreabnormalBtn(ABCPushButton):
    def __init__(self, parent):
        super(MainTabRightTopPreabnormalBtn, self).__init__(parent)
        self.setObjectName("Right")
        self.setFixedSize(224, 35)
        self.setText('Pre-abnormal')
        self.clicked.connect(self.dis_update)
    
    def dis_update(self):
        self.inmem.widget_ids['MainTabRightBottomWid'].change_condition_page(self.text())
        self.inmem.widget_ids['MainTabRightTopNormalBtn'].dis_off()
        self.inmem.widget_ids['MainTabRightTopPreabnormalBtn'].dis_on()
        self.inmem.widget_ids['MainTabRightTopAbnormalBtn'].dis_off()
        self.inmem.widget_ids['MainTabRightTopEmergencyBtn'].dis_off()

    def dis_on(self):
        self.setStyleSheet("QPushButton {background: rgb(255, 255, 255);} QPushButton:hover {background: rgb(0, 178, 218)}")

    def dis_off(self):
        self.setStyleSheet("QPushButton {background: rgb(128, 128, 128);} QPushButton:hover {background: rgb(0, 178, 218)}")
    
class MainTabRightTopAbnormalBtn(ABCPushButton):
    def __init__(self, parent):
        super(MainTabRightTopAbnormalBtn, self).__init__(parent)
        self.setObjectName("Right")
        self.setFixedSize(224, 35)
        self.setText('Abnormal')
        self.clicked.connect(self.dis_update)
    
    def dis_update(self):
        self.inmem.widget_ids['MainTabRightBottomWid'].change_condition_page(self.text())
        self.inmem.widget_ids['MainTabRightTopNormalBtn'].dis_off()
        self.inmem.widget_ids['MainTabRightTopPreabnormalBtn'].dis_off()
        self.inmem.widget_ids['MainTabRightTopAbnormalBtn'].dis_on()
        self.inmem.widget_ids['MainTabRightTopEmergencyBtn'].dis_off()

    def dis_on(self):
        self.setStyleSheet("QPushButton {background: rgb(255, 255, 255);} QPushButton:hover {background: rgb(0, 178, 218)}")

    def dis_off(self):
        self.setStyleSheet("QPushButton {background: rgb(128, 128, 128);} QPushButton:hover {background: rgb(0, 178, 218)}")
        
class MainTabRightTopEmergencyBtn(ABCPushButton):
    def __init__(self, parent):
        super(MainTabRightTopEmergencyBtn, self).__init__(parent)
        self.setObjectName("Right")
        self.setFixedSize(224, 35)
        self.setText('Emergency')
        self.clicked.connect(self.dis_update)
    
    def dis_update(self):
        self.inmem.widget_ids['MainTabRightBottomWid'].change_condition_page(self.text())
        self.inmem.widget_ids['MainTabRightTopNormalBtn'].dis_off()
        self.inmem.widget_ids['MainTabRightTopPreabnormalBtn'].dis_off()
        self.inmem.widget_ids['MainTabRightTopAbnormalBtn'].dis_off()
        self.inmem.widget_ids['MainTabRightTopEmergencyBtn'].dis_on()

    def dis_on(self):
        self.setStyleSheet("QPushButton {background: rgb(255, 255, 255);} QPushButton:hover {background: rgb(0, 178, 218)}")

    def dis_off(self):
        self.setStyleSheet("QPushButton {background: rgb(128, 128, 128);} QPushButton:hover {background: rgb(0, 178, 218)}")
            
# ------------------------------------------------------------------------------------------
class MainTabRightBottomWid(ABCStackWidget):
    def __init__(self, parent):
        super(MainTabRightBottomWid, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(231,231,234);')   # 수정 예정
        [self.addWidget(_) for _ in [MainTabRightBottomNormalW(self),
                                     MainTabRightBottomPreabnormalW(self),
                                     MainTabRightBottomAbnormalW(self),
                                     MainTabRightBottomEmergencyW(self)]]

    def change_condition_page(self, condition_name: str):
        """요청한 index 페이지로 전환

        Args:
            condition_name (str): Normal, PreAbnormal, ...
        """
        self.setCurrentIndex({'Normal': 0, 'Pre-abnormal': 1, 'Abnormal': 2, 'Emergency': 3}[condition_name])

class MainTabRightBottomNormalW(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabRightBottomNormalW, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(231,231,234);')

class MainTabRightBottomPreabnormalW(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabRightBottomPreabnormalW, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(231,231,234);')
        
class MainTabRightBottomAbnormalW(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabRightBottomAbnormalW, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(231,231,234);')

class MainTabRightBottomEmergencyW(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabRightBottomEmergencyW, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(231,231,234);')