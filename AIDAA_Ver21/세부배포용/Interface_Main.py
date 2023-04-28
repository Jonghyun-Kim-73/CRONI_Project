import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Function_Mem_ShMem import ShMem, InterfaceMem
from Interface_ABCWidget import *
from Interface_QSS import *
from datetime import datetime

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

class Main(QWidget):
    def __init__(self, ShMem):
        super(Main, self).__init__()
        self.inmem:InterfaceMem = InterfaceMem(ShMem, self)
        self.setGeometry(0, 0, 1920, 1200)
        self.setFixedSize(1920, 1200)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 상단바 제거
        self.setObjectName('Main')
        self.setStyleSheet(qss)
        self.m_flag = False
        # Frame ------------------------------------------------------
        self.top = MainTop(self)
        self.tab = MainTab(self)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)  # margin 제거
        lay.addWidget(self.top)
        lay.addWidget(self.tab)
        lay.setSpacing(0)   # margin 제거
        # End frame --------------------------------------------------

    # window drag
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton) and self.top.underMouse():
        # if (event.button() == Qt.LeftButton):  # 화면 움직이기 위함
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag and self.top.underMouse():
        # if Qt.LeftButton and self.m_flag:  # 화면 움직이기 위함
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 윈도우 position 변경
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def close(self) -> bool:
        QApplication.closeAllWindows()
        return super().close()        
# ----------------------------------------------------------------------------------------------------------------------
# MainTop
# ----------------------------------------------------------------------------------------------------------------------
class MainTop(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedHeight(50)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(10, 7, 8, 7)
        title_left = QHBoxLayout()
        title_left.setContentsMargins(0, 0, 5, 0)
        title_left.addWidget(MainTopTime(self))
        title_left.addWidget(MainTopSystemName(self))
        title_left.setSpacing(10)
        lay.addLayout(title_left)
        lay.setSpacing(10)
        # 현재 click된 btn & btn hover color 변경 위함
        self.btnGroup = QButtonGroup()

        btn1 = MainTopCallMain(self)
        btn2 = MainTopCallIFAP(self)
        btn3 = MainTopCallAIDAA(self)
        btn4 = MainTopCallEGIS(self)

        self.btnGroup.addButton(btn1, 0)
        self.btnGroup.addButton(btn2, 1)
        self.btnGroup.addButton(btn3, 2)
        self.btnGroup.addButton(btn4, 3)
        btn1.setChecked(True)

        lay.addWidget(btn1)
        lay.addWidget(btn2)
        lay.addWidget(btn3)
        lay.addWidget(btn4)
        lay.addWidget(MainTopClose(self))
class MainTopTime(ABCLabel):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedSize(465, 36)
        self.startTimer(600)
        self.time_freeze = datetime.now() # 현재 시간 Pick 하고 Freeze
        
    def timerEvent(self, a0: 'QTimerEvent') -> None:
        """ 타이머 디스플레이 업데이트 """
        current_time = self.time_freeze # + self.inmem.get_td() # 현재시간 + time_delta()
        real_time = current_time.strftime('%Y.%m.%d')
        real_time2 = current_time.strftime("%H:%M:%S")
        self.setText(real_time + " / " + real_time2)
        return super().timerEvent(a0)
class MainTopSystemName(ABCLabel):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedSize(465, 36)
        self.setContentsMargins(0, 0, 0, 0)
        self.setText('Main')
class MainTopCallMain(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Main')
        self.setFixedSize(218, 36)
        self.clicked.connect(self.dis_update)
        self.setCheckable(True)
        self.setChecked(False)
    def dis_update(self):
        self.setChecked(True)
        self.inmem.widget_ids['MainTopSystemName'].setText('Main')
        self.inmem.widget_ids['MainTab'].change_system_page('Main')
class MainTopCallIFAP(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Pre-abnormal')
        self.setFixedSize(218, 36)
        self.clicked.connect(self.dis_update)
        self.setCheckable(True)
        self.setChecked(False)

    def dis_update(self):
        self.setChecked(True)
        self.inmem.widget_ids['MainTopSystemName'].setText('IFAP')
        self.inmem.widget_ids['MainTab'].change_system_page('IFAP')
class MainTopCallEGIS(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Emergency')
        self.setFixedSize(218, 36)
        self.clicked.connect(self.dis_update)
        self.setCheckable(True)
        self.setChecked(False)

    def dis_update(self):
        self.setChecked(True)
        self.inmem.widget_ids['MainTopSystemName'].setText('EGIS')
        self.inmem.widget_ids['MainTab'].change_system_page('EGIS')
class MainTopCallAIDAA(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Abnormal')
        self.setFixedSize(218, 36)
        self.clicked.connect(self.dis_update)
        self.setCheckable(True)
        self.setChecked(False)

    def dis_update(self):
        self.setChecked(True)
        self.inmem.widget_ids['MainTopSystemName'].setText('AIDAA')
        self.inmem.widget_ids['MainTab'].change_system_page('AIDAA')
class MainTopClose(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        icon = os.path.join(ROOT_PATH, 'close.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(35, 35))  # 아이콘 크기
        self.setFixedSize(QSize(35, 35))
        self.setContentsMargins(0, 0, 0, 0)
        self.clicked.connect(self.close_main)

    def close_main(self):
        self.inmem.widget_ids['Main'].close()
# ----------------------------------------------------------------------------------------------------------------------
# MainTab
# ----------------------------------------------------------------------------------------------------------------------
class MainTab(ABCStackWidget):
    def __init__(self, parent):
        super(MainTab, self).__init__(parent)
        [self.addWidget(_) for _ in [MainTabMain(self), MainTabIFAP(self), MainTabEGIS(self)]]

    def change_system_page(self, system_name: str):
        """요청한 index 페이지로 전환

        Args:
            system_name (str): Main, IFAP, ...
        """
        self.setCurrentIndex({'Main': 0, 'IFAP': 1, 'EGIS': 2}[system_name])
class MainTabIFAP(ABCWidget):
    def __init__(self, parent):
        super(MainTabIFAP, self).__init__(parent)
class MainTabEGIS(ABCWidget):
    def __init__(self, parent):
        super(MainTabEGIS, self).__init__(parent)
class MainTabMain(ABCWidget):
    def __init__(self, parent):
        super(MainTabMain, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(10, 15, 10, 10)
        lay.addWidget(MainAlarm(self))
        lay.addWidget(MainTabRight(self))
        lay.setSpacing(10)
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
        self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallIFAP'].dis_update)

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
        
        self.startTimer(600)

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        self.w_contents.setText(f'IFAP information -> Val {self.inmem.ShMem.get_IFAP_para_val("V0")}')
        return super().timerEvent(a0)

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
        self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallAIDAA'].dis_update)

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
        self.gotobtn.clicked.connect(self.inmem.widget_ids['MainTopCallEGIS'].dis_update)

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
class MainAlarm(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(AlarmScrollArea(self, 'Main'))  # Alarm Table Height 구분 위함
#         lay.addWidget(AlarmSortSystemBtns(self))
        lay.setSpacing(10)
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
class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
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

    def dis_update(self):
        pass
# ----------------------------------------------------------------------------------------------------------------------
