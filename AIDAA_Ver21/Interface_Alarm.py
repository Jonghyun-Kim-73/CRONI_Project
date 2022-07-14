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
        lay.addWidget(AlarmFix(self))
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
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        lay = QHBoxLayout(self)
        # lay.addWidget(AlarmFixUrgentAct(self))
        lay.addWidget(AlarmFixPreTrip(self))
        lay.addWidget(AlarmFixTrip(self))

# class AlarmFixUrgentAct(ABCLabel, QLabel):
    # def __init__(self, parent):
        # super(AlarmFixUrgentAct, self).__init__(parent)
        # self.setStyleSheet('background-color: rgb(238, 238, 238); border: 1px solid rgb(128, 128, 128);')
        # self.widget_timer(iter_=500, funs=[self.dis_update])
        # self.setText('긴급조치')
        # self.blick = False

    # def dis_update(self):
        # if self.inmem.ShMem.get_para_val('iFixUgentAct') == 1 and self.blick == False:
            # self.setStyleSheet('background-color: rgb(255, 255, 0); border: 1px solid rgb(128, 128, 128);')
            # self.blick = True
        # else:
            # self.setStyleSheet('background-color: rgb(238, 238, 238); border: 1px solid rgb(128, 128, 128);')
            # self.blick = False

class AlarmFixPreTrip(ABCPushButton, QLabel):
    def __init__(self, parent):
        super(AlarmFixPreTrip, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238); border: 1px solid rgb(128, 128, 128);')
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.setText('Prediction')
        self.clicked.connect(self.change_main_display)
        self.blick = False

    def dis_update(self):
        """
        Prediction Blink 시 AIDAA도 blick.
        """
        if self.inmem.ShMem.get_para_val('iFixPreTrip') == 1 and self.blick == False:
            self.setStyleSheet('background-color: rgb(255, 255, 0); border: 1px solid rgb(128, 128, 128);')
            if self.inmem.get_current_system_name() == 'Main':
                self.inmem.widget_ids['MainTopCallAIDAA'].setStyleSheet('background-color: rgb(255, 255, 0);')
            else:
                self.inmem.widget_ids['MainTopCallAIDAA'].setStyleSheet('background-color: rgb(238, 238, 238);')
            self.blick = True
        else:
            self.setStyleSheet('background-color: rgb(238, 238, 238); border: 1px solid rgb(128, 128, 128);')
            self.inmem.widget_ids['MainTopCallAIDAA'].setStyleSheet('background-color: rgb(238, 238, 238);')
            self.blick = False

    def change_main_display(self):
        self.inmem.change_current_system_name('PreTrip')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()

class AlarmFixTrip(ABCLabel, QLabel):
    def __init__(self, parent):
        super(AlarmFixTrip, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238); border: 1px solid rgb(128, 128, 128);')
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.setText('Trip')
        self.blick = False

    def dis_update(self):
        if self.inmem.ShMem.get_para_val('iFixTrip') == 1 and self.blick == False:
            self.setStyleSheet('background-color: rgb(255, 255, 0); border: 1px solid rgb(128, 128, 128);')
            if self.inmem.get_current_system_name() == 'Main':
                self.inmem.widget_ids['MainTopCallEGIS'].setStyleSheet('background-color: rgb(255, 255, 0);')
            else:
                self.inmem.widget_ids['MainTopCallEGIS'].setStyleSheet('background-color: rgb(238, 238, 238);')
            self.blick = True
        else:
            self.setStyleSheet('background-color: rgb(238, 238, 238); border: 1px solid rgb(128, 128, 128);')
            self.inmem.widget_ids['MainTopCallEGIS'].setStyleSheet('background-color: rgb(238, 238, 238);')
            self.blick = False

class AlarmTable(ABCTableWidget, QTableWidget):
    def __init__(self, parent):
        super(AlarmTable, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')

        self.column_labels = ['DESCRIPTION', 'VALUE', 'SETPOINT', 'UNIT', 'DATE', 'TIME']
        self.setColumnCount(len(self.column_labels))
        self.setHorizontalHeaderLabels([l for l in self.column_labels])

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