from tkinter import N
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
import Interface_QSS as qss
from AIDAA_Ver21.Interface_Enum import Alarm_Table


class MainAlarm(ABCWidget):
    def __init__(self, parent):
        super(MainAlarm, self).__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(qss.Alarm_Table)
        # lay.addWidget(AlarmFix(self))
        lay.addWidget(AlarmScrollArea(self, Alarm_Table.Main))  # Alarm Table Height 구분 위함
        lay.addWidget(AlarmSortSystemBtns(self))
        lay.setSpacing(10)

class AIDAAAlarm(ABCWidget):
    def __init__(self, parent):
        super(AIDAAAlarm, self).__init__(parent)
        self.setStyleSheet(qss.Main_Tab)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(AlarmFix(self))
        lay.addWidget(AlarmScrollArea(self, Alarm_Table.AIDAA))
        lay.addWidget(AlarmSortAIDAABtns(self))
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

# ----------------------------------------------------------------------------------------------------------------------
class AlarmFix(ABCWidget):
    def __init__(self, parent):
        super(AlarmFix, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 5)

        # lay.addWidget(AlarmFixUrgentAct(self))
        lay.addWidget(AlarmFixPreTrip(self))
        lay.addWidget(AlarmFixTrip(self))
        lay.setSpacing(10)

        self.widget_timer(iter_=500, funs=[self.dis_update])

        self.blick = False

    def dis_update(self):
        # self.inmem.widget_ids['AlarmFixPreTrip'].dis_update() # 실행 후 확인
        # self.inmem.widget_ids['AlarmFixTrip'].dis_update()
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
            self.inmem.widget_ids['MainTabRightPreAbnormalW'].diable_widget(False)
            self.inmem.widget_ids['MainTabRightAbnormalW'].diable_widget(True)
            self.inmem.widget_ids['MainTabRightEmergencyW'].diable_widget(True)
        elif (self.inmem.ShMem.get_para_val('iFixPreAb') == 1 or self.inmem.ShMem.get_para_val('iFixPreAb') == 0) and \
            self.inmem.ShMem.get_para_val('iFixPreTrip') == 1 and \
            self.inmem.ShMem.get_para_val('iFixTrip') == 0:
            self.inmem.widget_ids['MainTabRightPreAbnormalW'].diable_widget(False)
            self.inmem.widget_ids['MainTabRightAbnormalW'].diable_widget(False)
            self.inmem.widget_ids['MainTabRightEmergencyW'].diable_widget(True)
        elif (self.inmem.ShMem.get_para_val('iFixPreAb') == 1 or self.inmem.ShMem.get_para_val('iFixPreAb') == 0) and \
            (self.inmem.ShMem.get_para_val('iFixPreTrip') == 1 or self.inmem.ShMem.get_para_val('iFixPreTrip') == 0) and \
            self.inmem.ShMem.get_para_val('iFixTrip') == 0:
            self.inmem.widget_ids['MainTabRightPreAbnormalW'].diable_widget(False)
            self.inmem.widget_ids['MainTabRightAbnormalW'].diable_widget(False)
            self.inmem.widget_ids['MainTabRightEmergencyW'].diable_widget(False)
        else:
            self.inmem.widget_ids['MainTabRightPreAbnormalW'].diable_widget(True)
            self.inmem.widget_ids['MainTabRightAbnormalW'].diable_widget(True)
            self.inmem.widget_ids['MainTabRightEmergencyW'].diable_widget(True)


class AlarmFixPreTrip(ABCPushButton):
    def __init__(self, parent):
        super(AlarmFixPreTrip, self).__init__(parent)
        self.setObjectName("Left")
        self.setFixedSize(465, 40)
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
        self.setFixedSize(465, 40)
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

class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

# Scroll Bar 적용
class AlarmScrollArea(ABCScrollArea):
    def __init__(self, parent, table):
        super(AlarmScrollArea, self).__init__(parent)
        self.margins = QMargins(0, 40, 0, 0)    # header height
        self.setViewportMargins(self.margins)
        self.setFixedWidth(940)

        self.headings_widget = QWidget(self)
        self.headings_layout = QHBoxLayout()
        self.headings_widget.setLayout(self.headings_layout)
        self.headings_layout.setContentsMargins(0, 0, 10, 0)

        # header item
        self.heading_label = [0, 0, 0, 0, 0, 0]
        self.heading_label[0] = QLabel("DESCRIPTION")
        self.heading_label[1] = QLabel("VALUE")
        self.heading_label[2] = QLabel("SETPOINT")
        self.heading_label[3] = QLabel("UNIT")
        self.heading_label[4] = QLabel("DATE")
        self.heading_label[5] = QLabel("TIME")

        # size
        self.heading_label[0].setFixedWidth(442)
        self.heading_label[1].setFixedWidth(93)
        self.heading_label[2].setFixedWidth(142)
        self.heading_label[3].setFixedWidth(77)
        self.heading_label[4].setFixedWidth(78)
        self.heading_label[5].setFixedWidth(108)

        for label in range(6):
            self.headings_layout.addWidget(self.heading_label[label])
            self.heading_label[label].setObjectName("Alarm_Header_M")
            self.heading_label[label].setAlignment(Qt.AlignCenter)

        self.heading_label[0].setAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.heading_label[0].setContentsMargins(5, 0, 0, 0)
        self.heading_label[0].setObjectName("Alarm_Header_F")
        self.heading_label[5].setObjectName("Alarm_Header_L")
        # self.headings_layout.addStretch(1)
        self.headings_layout.setSpacing(0)

        self.scrollwidget = QWidget()
        self.scrollwidget.setObjectName("scroll")
        self.grid = QGridLayout(self.scrollwidget)
        self.grid.addWidget(AlarmTable(self, table))
        self.grid.setContentsMargins(0, 0, 10, 0)
        self.setWidget(self.scrollwidget)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, event):
        rect = self.viewport().geometry()
        self.headings_widget.setGeometry(0, 0, rect.width() - 1, self.margins.top())
        QScrollArea.resizeEvent(self, event)

class AlarmTable(ABCTableWidget):
    def __init__(self, parent, table):
        super(AlarmTable, self).__init__(parent)

        if table == Alarm_Table.Main:
            # self.setFixedWidth(910)
            self.hcell = 40
        else:
            # self.setFixedSize(1240, 1190)
            self.hcell = 40

        self.setShowGrid(False)  # Grid 지우기
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.horizontalHeader().setVisible(False)  # Table Header 숨기기
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Scroll Bar 설정
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setRowCount(50)
        self.column_labels = [(' DESCRIPTION:', 410), ('VALUE', 93), ('SETPOINT', 141), ('UNIT', 77), ('DATE', 77), ('TIME', 109)]
        self.setColumnCount(len(self.column_labels))
        self.col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            self.col_names.append(l)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setContentsMargins(0, 0, 0, 0)

        self.setSelectionBehavior(QTableView.SelectRows)  # 테이블 row click

        # 테이블 정렬
        delegate = AlignDelegate(self)
        for row in range(1, self.rowCount()):
            self.setItemDelegateForColumn(row, delegate)

        # 테이블 헤더
        self.setHorizontalHeaderLabels(self.col_names)
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정
        self.horizontalHeader().setFixedHeight(40)
        # scroll 설정
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        # get scroll position
        # self.scrollBar = self.verticalScrollBar()
        # self.scrollBar.valueChanged.connect(lambda value: self.scrolled(self.scrollBar, value))

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, self.hcell)

        self.setContentsMargins(0, 0, 0, 0)
        self.widget_timer(500, [self.dis_update])
        self.dis_alarm_list = []

    def paintEvent(self, e: QPaintEvent) -> None:
        super(AlarmTable, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        self.draw_row_line(qp)
        qp.restore()

    def draw_row_line(self, qp):
        for i in range(len(self.dis_alarm_list) + 1):
            if i % 5 == 0:
                qp.setPen(QPen(QColor(128, 128, 128), 3))
                qp.drawLine(0, i * self.hcell, self.width(), i * self.hcell)

    def dis_update(self):
        new_alarm_list = self.update_dis_alarm_list()
        self.setRowCount(len(self.dis_alarm_list))

        self.setFixedSize(909, self.hcell * self.rowCount())

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, self.hcell)

        # 테이블 정렬
        delegate = AlignDelegate(self)
        for row in range(1, self.rowCount()):
            self.setItemDelegateForColumn(row, delegate)

        for alarm_name in new_alarm_list:
            self.insertRow(0)
            self.setItem(0, 0, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_des(alarm_name)}'))
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
        self.setFixedWidth(945)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(AlarmSystem_IFAP_SortPress(self))
        lay.addWidget(AlarmSystem_AIDAA_SortPress(self))
        lay.addWidget(AlarmSystem_EGIS_SortPress(self))
        lay.setSpacing(10)

class AlarmSystem_IFAP_SortPress(ABCPushButton):
    def __init__(self, parent):
        super(AlarmSystem_IFAP_SortPress, self).__init__(parent)
        self.setFixedSize(306, 40)
        self.setObjectName("Bottom")
        self.setText('Alarm_Pre-abnormal')

class AlarmSystem_AIDAA_SortPress(ABCPushButton):
    def __init__(self, parent):
        super(AlarmSystem_AIDAA_SortPress, self).__init__(parent)
        self.setFixedSize(307, 40)
        self.setObjectName("Bottom")
        self.setText('Alarm_Abnormal')

class AlarmSystem_EGIS_SortPress(ABCPushButton):
    def __init__(self, parent):
        super(AlarmSystem_EGIS_SortPress, self).__init__(parent)
        self.setFixedSize(307, 40)
        self.setObjectName("Bottom")
        self.setText('Alarm_Emergency')

# ----------------------------------------------------------------------------------------------------------------------
# AIDAA 에서 Sort 버튼
class AlarmSortAIDAABtns(ABCWidget):
    def __init__(self, parent):
        super(AlarmSortAIDAABtns, self).__init__(parent)
        lay = QHBoxLayout(self)
        self.setFixedWidth(940)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(AlarmAIDAA_Suppress_SortPress(self))
        lay.addWidget(AlarmSystem_Sortsystem_SortPress(self))
        lay.setSpacing(10)

class AlarmAIDAA_Suppress_SortPress(ABCPushButton):
    def __init__(self, parent):
        super(AlarmAIDAA_Suppress_SortPress, self).__init__(parent)
        self.setFixedSize(465, 40)
        self.setObjectName("Bottom")
        self.setText('Sort Press')

class AlarmSystem_Sortsystem_SortPress(ABCPushButton):
    def __init__(self, parent):
        super(AlarmSystem_Sortsystem_SortPress, self).__init__(parent)
        self.setFixedSize(465, 40)
        self.setObjectName("Bottom")
        self.setText('Sort System')