from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_QSS import *
from AIDAA_Ver21.Interface_Alarm_Pop import Popup

class MainAlarm(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(AlarmScrollArea(self, 'Main'))  # Alarm Table Height 구분 위함
#         lay.addWidget(AlarmSortSystemBtns(self))
        lay.setSpacing(10)
class AIDAAAlarm(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(AlarmFix(self))
        lay.addWidget(AlarmScrollArea(self, 'AIDAA'))
        lay.addWidget(AlarmSortAIDAABtns(self))
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
# ----------------------------------------------------------------------------------------------------------------------
class AlarmFix(ABCWidget):
    def __init__(self, parent):
        super(AlarmFix, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 5)

        lay.addWidget(AlarmFixPreTrip(self, 465))
        lay.addWidget(AlarmFixTrip(self, 465))
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
            if self.inmem.widget_ids['MainTopSystemName'].text() != 'IFAP':
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
    def __init__(self, parent, width):
        super(AlarmFixPreTrip, self).__init__(parent)
        self.setFixedSize(width, 40)
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
            if self.inmem.widget_ids['MainTopSystemName'].text() != 'AIDAA':
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
        self.inmem.widget_ids['MainTopSystemName'].setText('AIDAA')
        self.inmem.widget_ids['MainTab'].change_system_page('PreTrip')
class AlarmFixTrip(ABCLabel):
    def __init__(self, parent, width):
        super(AlarmFixTrip, self).__init__(parent)
        self.setFixedSize(width, 40)
        self.setText('Trip')
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.blick = False

    def dis_update(self):
        if self.inmem.ShMem.get_para_val('iFixTrip') == 1 and self.blick == False:
            self.setStyleSheet('background-color: rgb(0, 176, 218);')
            if self.inmem.widget_ids['MainTopSystemName'].text() != 'EGIS':
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
    def __init__(self, parent, type_, widget_name=''):
        super().__init__(parent, widget_name)
        self.margins = QMargins(0, 40, 0, 0)    # header height
        self.setViewportMargins(self.margins)
        self.setFixedWidth(940)

        self.headings_widget = QWidget(self)
        self.headings_layout = QHBoxLayout()
        self.headings_widget.setLayout(self.headings_layout)
        self.headings_layout.setContentsMargins(0, 0, 10, 0)

        # header item
        self.heading_label = [
            AlarmHeadingLabel(self, "DESCRIPTION", 442, 'F'),
            AlarmHeadingLabel(self, "VALUE", 93, 'M'),
            AlarmHeadingLabel(self, "SETPOINT", 142, 'M'),
            AlarmHeadingLabel(self, "UNIT", 77, 'M'),
            AlarmHeadingLabel(self, "DATE", 78, 'M'),
            AlarmHeadingLabel(self, "TIME", 108, 'L')
        ]
        [self.headings_layout.addWidget(w) for w in self.heading_label]

        self.heading_label[0].setAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.heading_label[0].setContentsMargins(5, 0, 0, 0)

        # self.headings_layout.addStretch(1)
        self.headings_layout.setSpacing(0)
        
        self.setWidget(AlarmTableWidget(self, type_))
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, event):
        rect = self.viewport().geometry()
        self.headings_widget.setGeometry(0, 0, rect.width() - 1, self.margins.top())
        QScrollArea.resizeEvent(self, event)
class AlarmTable(ABCTableWidget):
    def __init__(self, parent, type_, widget_name=''):
        super().__init__(parent, widget_name)
        self.rowset = 0
        if type_ == 'Main':
            self.setRowCount(26)
            self.setFixedSize(909, 1035)
        else:
            self.setRowCount(25)
            self.setFixedSize(909, 980)

        self.hcell = 44
        
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
        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, self.hcell)

        self.setContentsMargins(0, 0, 0, 0)
        self.widget_timer(500, [self.dis_update])
        self.dis_alarm_list = []

        self.doubleClicked.connect(self.call_double_click) # 더블 클릭시 PDF 활성화 기능 추가

    def paintEvent(self, e: QPaintEvent) -> None:
        super(AlarmTable, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        self.draw_row_line(qp)
        qp.restore()

    def draw_row_line(self, qp):
        self.rowset = len(self.dis_alarm_list) + 1

        for i in range(self.rowset):
            if i % 5 == 0:
                qp.setPen(QPen(rgb_to_qCOLOR(DarkGray), 3))
                qp.drawLine(0, i * self.hcell, self.width(), i * self.hcell)

    def call_double_click(self, index):
        selected_row = self.selectedIndexes()[0].row()
        for alarm_name in self.inmem.ShMem.get_alarmdb().keys():
            if f"{' ' + self.inmem.ShMem.get_alarmdb()[alarm_name]['Des']}" == self.item(selected_row, 0).text():
                print(alarm_name)
                self.popup = Popup(file_path=f'D:/CRONI_Interface/AIDAA_Ver21/Alarm_procedures/{alarm_name}.pdf', alarm_des=alarm_name)
                self.popup.show()

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
            '''
            1. 분할 경보
                1.1. 단순 분할 경보
                1.2. 다중 변수 분할 경보
                1.3. 계산식 포함 분할 경보
            2. 다중 변수
                2.1. 단순 다중 변수
                2.2. 계산식 포함 다중 변수
            3. 계산식 포함
            4. 기타
            '''
            # 1.1 단순 분할 경보
            if alarm_name[:-2] == 'KLAMPO321' or alarm_name[:-2] == 'KLAMPO325' or alarm_name[:-2] == 'KLAMPO328' or alarm_name[:-2] == 'KLAMPO329' or alarm_name[:-2] == 'KLAMPO332' or alarm_name[:-2] == 'KLAMPO265' or alarm_name[:-2] == 'KLAMPO314' or alarm_name[:-2] == 'KLAMPO338':
                self.insertRow(0)
                self.setItem(0, 0, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_des(alarm_name)}'))  # Description
                self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)))}'))  # Value
                if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == float:
                    self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name))}'))  # Setpoint
                else: # Setpoint가 변수 이름일 경우
                    self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)))}'))  # Setpoint
                self.setItem(0, 3, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_unit(alarm_name)}'))  # Unit
                self.setItem(0, 4, QTableWidgetItem('0'))  # Date
                self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))  # Time

            # 1.2 다중 변수 분할 경보
            elif alarm_name[:-2] == 'KLAMPO316' or alarm_name[:-2] == 'KLAMPO326':
                if alarm_name[:-2] == 'KLAMPO316':
                    for i in range(2):
                        self.insertRow(0)
                        self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[i]))}'))  # Value
                        if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == float:
                            self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i])}'))  # Setpoint
                        else:  # Setpoint가 변수 이름일 경우
                            self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]))}'))  # Setpoint
                        self.setItem(0, 3, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_unit(alarm_name)[i]}'))  # Unit
                        if i == 1:
                            self.setSpan(0, 0, 2, 1)
                            self.setItem(0, 0, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_des(alarm_name)}'))  # Description
                            self.setSpan(0, 4, 2, 1)
                            self.setItem(0, 4, QTableWidgetItem('0'))  # Date
                            self.setSpan(0, 5, 2, 1)
                            self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))  # Time
                elif alarm_name[:-2] == 'KLAMPO326':
                    for i in range(2):
                        self.insertRow(0)
                        if i == 0:
                            print(abs(self.inmem.ShMem.get_para_list(self.inmem.ShMem.get_alarm_val(alarm_name)[i])[-2] - (self.inmem.ShMem.get_para_list(self.inmem.ShMem.get_alarm_val(alarm_name)[i])[-1] * 5.0)))
                            self.setItem(0, 1, QTableWidgetItem(f'{" " + str(abs(self.inmem.ShMem.get_para_list(self.inmem.ShMem.get_alarm_val(alarm_name)[i])[-2] - (self.inmem.ShMem.get_para_list(self.inmem.ShMem.get_alarm_val(alarm_name)[i])[-1] * 5.0)))}'))  # Value
                        else:
                            self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[i]))}'))  # Value
                        if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == float:
                            self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i])}'))  # Setpoint
                        else:  # Setpoint가 변수 이름일 경우
                            self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]))}'))  # Setpoint
                        self.setItem(0, 3, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_unit(alarm_name)[i]}'))  # Unit
                        if i == 1:
                            self.setSpan(0, 0, 2, 1)
                            self.setItem(0, 0, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_des(alarm_name)}'))  # Description
                            self.setSpan(0, 4, 2, 1)
                            self.setItem(0, 4, QTableWidgetItem('0'))  # Date
                            self.setSpan(0, 5, 2, 1)
                            self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))  # Time

            # 1.3 계산식 포함 분할 경보
            elif alarm_name[:-2] == 'KLAMPO254' or alarm_name[:-2] == 'KLAMPO315' or alarm_name[:-2] == 'KLAMPO319' or alarm_name[:-2] == 'KLAMPO320' or alarm_name[:-2] == 'KLAMPO327':
                # 공통 정보 먼저 표기
                self.insertRow(0)
                self.setItem(0, 0, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_des(alarm_name)}'))  # Description
                self.setItem(0, 3, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_unit(alarm_name)}'))  # Unit
                self.setItem(0, 4, QTableWidgetItem('0'))  # Date
                self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))  # Time
                if alarm_name[:-2] == 'KLAMPO254':
                    if self.inmem.ShMem.get_para_val('UMAXDT') == 0 or self.inmem.ShMem.get_para_val('CDT100') == 0:
                        RDTEMP = 0
                    else:
                        RDTEMP = (self.inmem.ShMem.get_para_val('UMAXDT') / self.inmem.ShMem.get_para_val('CDT100')) * 100.0
                    if RDTEMP >= 100.0: RDTEMP = 100.
                    if RDTEMP <= 0.0: RDTEMP = 0.
                    if True:
                        CRIL = {1: 1.818, 2: 1.824, 3: 1.818, 4: 208.0,
                                5: 93.0, 6: -22.0, 7: 12.0}
                        # Control A
                        KRIL1 = 228
                        # Control B
                        KRIL2 = int(CRIL[1] * RDTEMP + CRIL[4])
                        if KRIL2 >= 228: KRIL2 = 228
                        # Control C
                        KRIL3 = int(CRIL[2] * RDTEMP + CRIL[5])
                        if KRIL3 >= 228: KRIL3 = 228
                        # Control D
                        if RDTEMP >= CRIL[7]:
                            KRIL4 = int(CRIL[3] * RDTEMP + CRIL[6])
                            if KRIL4 >= 160: KRIL4 = 160
                            if KRIL4 <= 0: KRIL4 = 0
                        else:
                            KRIL4 = 0

                    setpoint_dic = {'1': KRIL1, '2': KRIL2, '3': KRIL3, '4': KRIL4}

                    self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)))}'))  # Value
                    self.setItem(0, 2, QTableWidgetItem(f'{" " + str(setpoint_dic[alarm_name[-1]])}'))  # Setpoint
                elif alarm_name[:-2] == 'KLAMPO315':
                    RUAVMX = max(self.inmem.ShMem.get_para_val('UAVLEG1'), self.inmem.ShMem.get_para_val('UAVLEG2'), self.inmem.ShMem.get_para_val('UAVLEG3'))
                    RAVGT = {'1': abs(self.inmem.ShMem.get_para_val('UAVLEG1') - RUAVMX), '2': abs(self.inmem.ShMem.get_para_val('UAVLEG2') - RUAVMX), '3': abs(self.inmem.ShMem.get_para_val('UAVLEG3') - RUAVMX)}
                    self.setItem(0, 1, QTableWidgetItem(f'{" " + str(RAVGT[alarm_name[-1]])}'))  # Value
                    if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == float:
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name))}'))  # Setpoint
                    else:  # Setpoint가 변수 이름일 경우
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)))}'))  # Setpoint
                elif alarm_name[:-2] == 'KLAMPO319':
                    self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name))*0.01)}'))  # Value
                    if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == float:
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name))}'))  # Setpoint
                    else:  # Setpoint가 변수 이름일 경우
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)))}'))  # Setpoint
                elif alarm_name[:-2] == 'KLAMPO320':
                    self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[0])-self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[1]))}'))  # Value
                    if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == float:
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name))}'))  # Setpoint
                    else:  # Setpoint가 변수 이름일 경우
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name))*0.1)}'))  # Setpoint
                elif alarm_name[:-2] == 'KLAMPO327':
                    self.setItem(0, 1, QTableWidgetItem(f'{" " + str(abs(self.inmem.ShMem.get_para_list(self.inmem.ShMem.get_alarm_val(alarm_name))[-2] - self.inmem.ShMem.get_para_list(self.inmem.ShMem.get_alarm_val(alarm_name))[-1] * 5.0))}'))  # Value
                    if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == float:
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name))}'))  # Setpoint
                    else:  # Setpoint가 변수 이름일 경우
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)))}'))  # Setpoint

            #  2.1 단순 다중 변수
            elif alarm_name == 'KLAMPO269' or alarm_name == 'KLAMPO301' or alarm_name == 'KLAMPO312' or alarm_name == 'KLAMPO337' or alarm_name == 'KLAMPO339' or alarm_name == 'KLAMPO340':
                for i in range(2):
                    self.insertRow(0)
                    self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[i]))}'))  # Value
                    if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == float:
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i])}'))  # Setpoint
                    else:  # Setpoint가 변수 이름일 경우
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]))}'))  # Setpoint
                    self.setItem(0, 3, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_unit(alarm_name)[i]}'))  # Unit
                    if i == 1:
                        self.setSpan(0, 0, 2, 1)
                        self.setItem(0, 0, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_des(alarm_name)}'))  # Description
                        self.setSpan(0, 4, 2, 1)
                        self.setItem(0, 4, QTableWidgetItem('0'))  # Date
                        self.setSpan(0, 5, 2, 1)
                        self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))  # Time

            # 2.2 계산식 포함 다중 변수
            elif alarm_name == 'KLAMPO256' or alarm_name == 'KLAMPO310' or alarm_name == 'KLAMPO311' or alarm_name == 'KLAMPO313':
                if alarm_name == 'KLAMPO256':
                    for i in range(2):
                        self.insertRow(0)
                        self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[i]))}'))  # Value
                        if i == 1:
                            if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == float:
                                self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i])}'))  # Setpoint
                            else:  # Setpoint가 변수 이름일 경우
                                self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i])-0.75)}'))  # Setpoint
                        else:
                            if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == float:
                                self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i])}'))  # Setpoint
                            else:  # Setpoint가 변수 이름일 경우
                                self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]))}'))  # Setpoint
                        self.setItem(0, 3, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_unit(alarm_name)[i]}'))  # Unit
                        if i == 1:
                            self.setSpan(0, 0, 2, 1)
                            self.setItem(0, 0, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_des(alarm_name)}'))  # Description
                            self.setSpan(0, 4, 2, 1)
                            self.setItem(0, 4, QTableWidgetItem('0'))  # Date
                            self.setSpan(0, 5, 2, 1)
                            self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))  # Time
                elif alarm_name == 'KLAMPO310':
                    for i in range(2):
                        self.insertRow(0)
                        if i == 0:
                            self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[i])/100)}'))  # Value
                        else:
                            self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[i]))}'))  # Value
                        if i == 0:
                            if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == float:
                                self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i])}'))  # Setpoint
                            else:  # Setpoint가 변수 이름일 경우
                                self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i])+self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i+1]))}'))  # Setpoint
                        else:
                            if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == float:
                                self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i])}'))  # Setpoint
                            else:  # Setpoint가 변수 이름일 경우
                                self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i+1]))}'))  # Setpoint
                        self.setItem(0, 3, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_unit(alarm_name)[i]}'))  # Unit
                        if i == 1:
                            self.setSpan(0, 0, 2, 1)
                            self.setItem(0, 0, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_des(alarm_name)}'))  # Description
                            self.setSpan(0, 4, 2, 1)
                            self.setItem(0, 4, QTableWidgetItem('0'))  # Date
                            self.setSpan(0, 5, 2, 1)
                            self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))  # Time
                elif alarm_name == 'KLAMPO311':
                    for i in range(2):
                        self.insertRow(0)
                        if i == 0:
                            self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[i])/100)}'))  # Value
                        else:
                            self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[i]))}'))  # Value
                        if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == float:
                            self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i])}'))  # Setpoint
                        else:  # Setpoint가 변수 이름일 경우
                            self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]))}'))  # Setpoint
                        self.setItem(0, 3, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_unit(alarm_name)[i]}'))  # Unit
                        if i == 1:
                            self.setSpan(0, 0, 2, 1)
                            self.setItem(0, 0, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_des(alarm_name)}'))  # Description
                            self.setSpan(0, 4, 2, 1)
                            self.setItem(0, 4, QTableWidgetItem('0'))  # Date
                            self.setSpan(0, 5, 2, 1)
                            self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))  # Time
                elif alarm_name == 'KLAMPO313':
                    for i in range(2):
                        self.insertRow(0)
                        if i == 0:
                            self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[i])-self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[i+1]))}'))  # Value
                        else:
                            self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[i+1])-self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[i+2]))}'))  # Value
                        if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]) == float:
                            self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i])}'))  # Setpoint
                        else:  # Setpoint가 변수 이름일 경우
                            self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)[i]))}'))  # Setpoint
                        self.setItem(0, 3, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_unit(alarm_name)[i]}'))  # Unit
                        if i == 1:
                            self.setSpan(0, 0, 2, 1)
                            self.setItem(0, 0, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_des(alarm_name)}'))  # Description
                            self.setSpan(0, 4, 2, 1)
                            self.setItem(0, 4, QTableWidgetItem('0'))  # Date
                            self.setSpan(0, 5, 2, 1)
                            self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))  # Time

            # 3. 계산식 포함
            elif alarm_name == 'KLAMPO255' or alarm_name == 'KLAMPO258' or alarm_name == 'KLAMPO302' or alarm_name == 'KLAMPO303' or alarm_name == 'KLAMPO304' or alarm_name == 'KLAMPO318' or alarm_name == 'KLAMPO334':
                # 공통 정보 먼저 표기
                self.insertRow(0)
                self.setItem(0, 0, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_des(alarm_name)}'))  # Description
                self.setItem(0, 3, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_unit(alarm_name)}'))  # Unit
                self.setItem(0, 4, QTableWidgetItem('0'))  # Date
                self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))  # Time
                if alarm_name == 'KLAMPO258':
                    self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)))}'))  # Value
                    if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == float:
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name))}'))  # Setpoint
                    else:  # Setpoint가 변수 이름일 경우
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name))-1.5)}'))  # Setpoint
                else:
                    if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == float:
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name))}'))  # Setpoint
                    else:  # Setpoint가 변수 이름일 경우
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)))}'))  # Setpoint
                    if alarm_name == 'KLAMPO255':
                        IROD = 0
                        for _ in range(1, 53):
                            if self.inmem.ShMem.get_para_val([f'KZROD{_}']) < 0.0:
                                IROD += 1
                        self.setItem(0, 1, QTableWidgetItem(f'{" " + str(IROD)}'))  # Value
                    elif alarm_name == 'KLAMPO302' or alarm_name == 'KLAMPO303' or alarm_name == 'KLAMPO304':
                        self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[0])*self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)[1]))}'))  # Value
                    elif alarm_name == 'KLAMPO318':
                        self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)) - 0.98E5)}'))  # Value
                    elif alarm_name == "KLAMPO334":
                        self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)) * 0.047)}'))  # Value

            # 4. 기타
            else:
                if alarm_name == 'KLAMPO325': pass
                else:
                    self.insertRow(0)
                    self.setItem(0, 0, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_des(alarm_name)}'))  # Description
                    self.setItem(0, 1, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_val(alarm_name)))}'))  # Value
                    if type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == int or type(self.inmem.ShMem.get_alarm_setpoint(alarm_name)) == float:
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_alarm_setpoint(alarm_name))}'))  # Setpoint
                    else:  # Setpoint가 변수 이름일 경우
                        self.setItem(0, 2, QTableWidgetItem(f'{" " + str(self.inmem.ShMem.get_para_val(self.inmem.ShMem.get_alarm_setpoint(alarm_name)))}'))  # Setpoint
                    self.setItem(0, 3, QTableWidgetItem(f'{" " + self.inmem.ShMem.get_alarm_unit(alarm_name)}'))  # Unit
                    self.setItem(0, 4, QTableWidgetItem('0'))  # Date
                    self.setItem(0, 5, QTableWidgetItem(f'{self.inmem.get_time()}'))  # Time
    def update_dis_alarm_list(self):
        new_alarm_list = []
        for alarm_name in self.inmem.ShMem.get_on_alarms():
            if not alarm_name in self.dis_alarm_list:
                self.dis_alarm_list.append(alarm_name)
                new_alarm_list.append(alarm_name)
        return new_alarm_list
# ----------------------------------------------------------------------------------------------------------------------
class AlarmTableWidget(ABCWidget):
    def __init__(self, parent, type_, widget_name=''):
        super().__init__(parent, widget_name)
        
        self.alarmtable = AlarmTable(self, type_)
        self.setFixedWidth(self.alarmtable.width())
        
        vl = QVBoxLayout(self)
        vl.addWidget(self.alarmtable)
        vl.addStretch(1)
        vl.setContentsMargins(0, 0, 10, 0)
class AlarmHeadingLabel(ABCLabel):
    def __init__(self, parent, text, fix_width, pos, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedWidth(fix_width)
        self.setText(text)
        self.setProperty('Pos', pos)
        self.style().polish(self)
# ----------------------------------------------------------------------------------------------------------------------
# Main 에서 Sort 버튼
'''class AlarmSortSystemBtns(ABCWidget):
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
        self.setText('Alarm_Pre-abnormal')
class AlarmSystem_AIDAA_SortPress(ABCPushButton):
    def __init__(self, parent):
        super(AlarmSystem_AIDAA_SortPress, self).__init__(parent)
        self.setFixedSize(307, 40)
        self.setText('Alarm_Abnormal')
class AlarmSystem_EGIS_SortPress(ABCPushButton):
    def __init__(self, parent):
        super(AlarmSystem_EGIS_SortPress, self).__init__(parent)
        self.setFixedSize(307, 40)
        self.setText('Alarm_Emergency')'''
# ----------------------------------------------------------------------------------------------------------------------
# AIDAA 에서 Sort 버튼
class AlarmSortAIDAABtns(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        lay = QHBoxLayout(self)
        self.setFixedWidth(940)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(AlarmAIDAA_Suppress_SortPress(self))
        lay.addWidget(AlarmSystem_Sortsystem_SortPress(self))
        lay.setSpacing(10)
class AlarmAIDAA_Suppress_SortPress(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedSize(465, 40)
        self.setText('Sort Press')
class AlarmSystem_Sortsystem_SortPress(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedSize(465, 40)
        self.setText('Sort System')