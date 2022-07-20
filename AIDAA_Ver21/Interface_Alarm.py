from tkinter import N
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *


class MainAlarm(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainAlarm, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(167, 242, 211);')

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        # lay.addWidget(AlarmFix(self))
        lay.addWidget(AlarmTable(self))
        lay.addWidget(AlarmSortSystemBtns(self))

class AIDAAAlarm(ABCWidget, QWidget):
    def __init__(self, parent):
        super(AIDAAAlarm, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(167, 242, 211);')

        lay = QVBoxLayout(self)
        lay.addWidget(AlarmFix(self))
        lay.addWidget(AlarmTable(self))
        lay.addWidget(AlarmSortAIDAABtns(self))

# ----------------------------------------------------------------------------------------------------------------------
class AlarmFix(ABCWidget, QWidget):
    def __init__(self, parent):
        super(AlarmFix, self).__init__(parent)
        lay = QHBoxLayout(self)
        # lay.addWidget(AlarmFixUrgentAct(self))
        lay.addWidget(AlarmFixPreTrip(self))
        lay.addWidget(AlarmFixTrip(self))
        lay.setSpacing(5)

        self.widget_timer(iter_=500, funs=[self.dis_update])

        self.blick = False

    def dis_update(self):
        self.dis_update_pre_abnormal()
        self.dis_ws_enable()

    def dis_update_pre_abnormal(self):
        if self.inmem.ShMem.get_para_val('iFixPreAb') == 1 and self.blick == False:
            self.setStyleSheet('background-color: rgb(0, 176, 218);')
            if self.inmem.get_current_system_name() != 'IFAP':
                self.inmem.widget_ids['MainTopCallIFAP'].setStyleSheet('background-color: rgb(0, 176, 218);')
                self.inmem.widget_ids['MainTabRightPreAbnormalW'].gotobtn.setStyleSheet('background-color: rgb(0, 176, 218);')
            else:
                self.inmem.widget_ids['MainTopCallAIDAA'].setStyleSheet('background-color: rgb(255, 255, 255);')
                self.inmem.widget_ids['MainTabRightPreAbnormalW'].gotobtn.setStyleSheet('background-color: rgb(255, 255, 255);')
            self.blick = True
        elif self.inmem.ShMem.get_para_val('iFixPreAb') == 1:  # 1값이 아닐때 영향받음
            self.setStyleSheet('background-color: rgb(0, 176, 86);')
            self.inmem.widget_ids['MainTopCallIFAP'].setStyleSheet('background-color: rgb(255, 255, 255);')
            self.inmem.widget_ids['MainTabRightPreAbnormalW'].gotobtn.setStyleSheet('background-color: rgb(255, 255, 255);')
            self.blick = False

    def dis_ws_enable(self):
        if self.inmem.ShMem.get_para_val('iFixPreAb') == 1 and \
            self.inmem.ShMem.get_para_val('iFixPreTrip') == 0 and \
            self.inmem.ShMem.get_para_val('iFixTrip') == 0:
            self.inmem.widget_ids['MainTabRightPreAbnormalW'].setDisabled(False)
            self.inmem.widget_ids['MainTabRightAbnormalW'].setDisabled(True)
            self.inmem.widget_ids['MainTabRightEmergencyW'].setDisabled(True)
        elif (self.inmem.ShMem.get_para_val('iFixPreAb') == 1 or self.inmem.ShMem.get_para_val('iFixPreAb') == 0) and \
            self.inmem.ShMem.get_para_val('iFixPreTrip') == 1 and \
            self.inmem.ShMem.get_para_val('iFixTrip') == 0:
            self.inmem.widget_ids['MainTabRightPreAbnormalW'].setDisabled(False)
            self.inmem.widget_ids['MainTabRightAbnormalW'].setDisabled(False)
            self.inmem.widget_ids['MainTabRightEmergencyW'].setDisabled(True)
        elif (self.inmem.ShMem.get_para_val('iFixPreAb') == 1 or self.inmem.ShMem.get_para_val('iFixPreAb') == 0) and \
            (self.inmem.ShMem.get_para_val('iFixPreTrip') == 1 or self.inmem.ShMem.get_para_val('iFixPreTrip') == 0) and \
            self.inmem.ShMem.get_para_val('iFixTrip') == 0:
            self.inmem.widget_ids['MainTabRightPreAbnormalW'].setDisabled(False)
            self.inmem.widget_ids['MainTabRightAbnormalW'].setDisabled(False)
            self.inmem.widget_ids['MainTabRightEmergencyW'].setDisabled(False)
        else:
            self.inmem.widget_ids['MainTabRightPreAbnormalW'].setDisabled(True)
            self.inmem.widget_ids['MainTabRightAbnormalW'].setDisabled(True)
            self.inmem.widget_ids['MainTabRightEmergencyW'].setDisabled(True)


class AlarmFixPreTrip(ABCPushButton, QLabel):
    def __init__(self, parent):
        super(AlarmFixPreTrip, self).__init__(parent)
        self.setObjectName("Left")
        self.setFixedSize(474, 35)
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.setText('PreTrip')
        self.clicked.connect(self.change_main_display)
        self.blick = False
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        """
        Prediction Blink 시 AIDAA도 blick.
        """
        if self.inmem.ShMem.get_para_val('iFixPreTrip') == 1 and self.blick == False:
            self.setStyleSheet('background-color: rgb(0, 176, 218);')
            if self.inmem.get_current_system_name() != 'AIDAA':
                self.inmem.widget_ids['MainTopCallAIDAA'].setStyleSheet('background-color: rgb(0, 176, 218);')
                self.inmem.widget_ids['MainTabRightAbnormalW'].gotobtn.setStyleSheet('background-color: rgb(0, 176, 218);')
            else:
                self.inmem.widget_ids['MainTopCallAIDAA'].setStyleSheet('background-color: rgb(255, 255, 255);')
                self.inmem.widget_ids['MainTabRightAbnormalW'].gotobtn.setStyleSheet('background-color: rgb(255, 255, 255);')
            self.blick = True
        elif self.inmem.ShMem.get_para_val('iFixPreTrip') == 1:  # 1값이 아닐때 영향받음
            self.setStyleSheet('background-color: rgb(0, 176, 86);')
            self.inmem.widget_ids['MainTopCallAIDAA'].setStyleSheet('background-color: rgb(255, 255, 255);')
            self.inmem.widget_ids['MainTabRightAbnormalW'].gotobtn.setStyleSheet('background-color: rgb(255, 255, 255);')
            self.blick = False

    def change_main_display(self):
        self.inmem.change_current_system_name('PreTrip')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()

class AlarmFixTrip(ABCLabel):
    def __init__(self, parent):
        super(AlarmFixTrip, self).__init__(parent)
        self.setObjectName("Left")
        self.setFixedSize(475, 35)
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.setText('Trip')
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.blick = False

    def dis_update(self):
        if self.inmem.ShMem.get_para_val('iFixTrip') == 1 and self.blick == False:
            self.setStyleSheet('background-color: rgb(0, 176, 218);')
            if self.inmem.get_current_system_name() != 'EGIS':
                self.inmem.widget_ids['MainTopCallEGIS'].setStyleSheet('background-color: rgb(0, 176, 218);')
                self.inmem.widget_ids['MainTabRightEmergencyW'].gotobtn.setStyleSheet('background-color: rgb(0, 176, 218);')
            else:
                self.inmem.widget_ids['MainTopCallEGIS'].setStyleSheet('background-color: rgb(255, 255, 255);')
                self.inmem.widget_ids['MainTabRightEmergencyW'].gotobtn.setStyleSheet('background-color: rgb(255, 255, 255);')
            self.blick = True
        elif self.inmem.ShMem.get_para_val('iFixTrip') == 1:
            self.setStyleSheet('background-color: rgb(0, 176, 86);')
            self.inmem.widget_ids['MainTopCallEGIS'].setStyleSheet('background-color: rgb(255, 255, 255);')
            self.inmem.widget_ids['MainTabRightEmergencyW'].gotobtn.setStyleSheet('background-color: rgb(255, 255, 255);')
            self.blick = False

class AlarmTable(ABCTableWidget):
    def __init__(self, parent):
        super(AlarmTable, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        self.column_labels = ['DESCRIPTION', 'VALUE', 'SETPOINT', 'UNIT', 'DATE', 'TIME']
        self.setColumnCount(len(self.column_labels))
        self.setFixedWidth(900) # 임시
        self.setHorizontalHeaderLabels([l for l in self.column_labels])
        self.setContentsMargins(0, 0, 0, 0)
        self.widget_timer(500, [self.dis_update])
        self.dis_alarm_list = []

    def dis_update(self):
        new_alarm_list = self.update_dis_alarm_list()

        for alarm_name in new_alarm_list:
            self.insertRow(0)
            self.setItem(0, 0, QTableWidgetItem(f'{self.inmem.ShMem.get_alarm_des(alarm_name)}'))
            self.setItem(0, 1, QTableWidgetItem('0'))
            self.setItem(0, 2, QTableWidgetItem('0'))
            self.setItem(0, 3, QTableWidgetItem('0'))
            self.setItem(0, 4, QTableWidgetItem('0'))
            self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))

    def update_dis_alarm_list(self):
        new_alarm_list = []
        for alarm_name in self.inmem.ShMem.get_on_alarms():
            if not alarm_name in self.dis_alarm_list:
                self.dis_alarm_list.append(alarm_name)
                new_alarm_list.append(alarm_name)
        return new_alarm_list
# ----------------------------------------------------------------------------------------------------------------------
# Main 에서 Sort 버튼
class AlarmSortSystemBtns(ABCWidget):
    def __init__(self, parent):
        super(AlarmSortSystemBtns, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(AlarmSystem_IFAP_SortPress(self))
        lay.addWidget(AlarmSystem_AIDAA_SortPress(self))
        lay.addWidget(AlarmSystem_EGIS_SortPress(self))
        lay.setSpacing(5)

class AlarmSystem_IFAP_SortPress(ABCPushButton):
    def __init__(self, parent):
        super(AlarmSystem_IFAP_SortPress, self).__init__(parent)
        self.setObjectName("Bottom")
        self.setText('Alarm_Pre-abnormal')

class AlarmSystem_AIDAA_SortPress(ABCPushButton):
    def __init__(self, parent):
        super(AlarmSystem_AIDAA_SortPress, self).__init__(parent)
        self.setObjectName("Bottom")
        self.setText('Alarm_Abnormal')

class AlarmSystem_EGIS_SortPress(ABCPushButton):
    def __init__(self, parent):
        super(AlarmSystem_EGIS_SortPress, self).__init__(parent)
        self.setObjectName("Bottom")
        self.setText('Alarm_Emergency')

    def dis_update(self):
        new_alarm_list = self.update_dis_alarm_list()

        for alarm_name in new_alarm_list:
            self.insertRow(0)
            self.setItem(0, 0, QTableWidgetItem(f'{self.inmem.ShMem.get_alarm_des(alarm_name)}'))
            self.setItem(0, 1, QTableWidgetItem('0'))
            self.setItem(0, 2, QTableWidgetItem('0'))
            self.setItem(0, 3, QTableWidgetItem('0'))
            self.setItem(0, 4, QTableWidgetItem('0'))
            self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))

    def update_dis_alarm_list(self):
        new_alarm_list = []
        for alarm_name in self.inmem.ShMem.get_on_alarms():
            if not alarm_name in self.dis_alarm_list:
                self.dis_alarm_list.append(alarm_name)
                new_alarm_list.append(alarm_name)
        return new_alarm_list
# ----------------------------------------------------------------------------------------------------------------------
# Main 에서 Sort 버튼
class AlarmSortSystemBtns(ABCWidget, QWidget):
    def __init__(self, parent):
        super(AlarmSortSystemBtns, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        lay = QHBoxLayout(self)
        lay.addWidget(AlarmSystem_IFAP_SortPress(self))
        lay.addWidget(AlarmSystem_AIDAA_SortPress(self))
        lay.addWidget(AlarmSystem_EGIS_SortPress(self))

class AlarmSystem_IFAP_SortPress(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(AlarmSystem_IFAP_SortPress, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        self.setText('Alarm_IFAP')

class AlarmSystem_AIDAA_SortPress(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(AlarmSystem_AIDAA_SortPress, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        self.setText('Alarm_AIDAA')

class AlarmSystem_EGIS_SortPress(ABCPushButton, QPushButton):    
    def __init__(self, parent):
        super(AlarmSystem_EGIS_SortPress, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        self.setText('Alarm_EGIS')

# ----------------------------------------------------------------------------------------------------------------------
# AIDAA 에서 Sort 버튼
class AlarmSortAIDAABtns(ABCWidget, QWidget):
    def __init__(self, parent):
        super(AlarmSortAIDAABtns, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        lay = QHBoxLayout(self)
        lay.addWidget(AlarmAIDAA_Suppress_SortPress(self))
        lay.addWidget(AlarmSystem_Sortsystem_SortPress(self))

class AlarmAIDAA_Suppress_SortPress(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(AlarmAIDAA_Suppress_SortPress, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        self.setText('Sort Press')

class AlarmSystem_Sortsystem_SortPress(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(AlarmSystem_Sortsystem_SortPress, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        self.setText('Sort System')