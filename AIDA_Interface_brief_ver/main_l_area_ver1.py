import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDA_Interface_brief_ver.TOOL.TOOL_etc import ToolEtc as T

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainLeftArea(QWidget):
    """ 왼쪽 알람 디스플레이 위젯 """
    def __init__(self, parent, h, w, mem=None):
        super(MainLeftArea, self).__init__(parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainLeftArea')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setFixedHeight(h)
        self.setFixedWidth(w)
        # 레이어 셋업 ---------------------------------------------------------------------------------------------------
        sp_h, s, side_s = 30, 5, 5
        scroll_w = 20
        # 1. 알람 Table
        self.AlarmTable = AlarmTable(self, x=side_s, y=side_s, w=w-side_s*2 - scroll_w, h=h-(side_s*2+s+sp_h), mem=self.mem)
        self.AlarmTableScrollBar = self.AlarmTable.verticalScrollBar()
        self.AlarmTableScrollBar.setParent(self)
        self.AlarmTableScrollBar.setGeometry(side_s + self.AlarmTable.width() + s,
                                             side_s + self.AlarmTable.horizontalHeader().height(),
                                             scroll_w,
                                             h-(side_s*2+s+sp_h) - self.AlarmTable.horizontalHeader().height())

        # 2. Subpress Btn
        self.SubPressBtm = SupPresBtn(self, x=side_s, y=h-sp_h-side_s, w=w-side_s*2 - scroll_w, h=sp_h, mem=self.mem)


class AlarmTable(QTableWidget):
    def __init__(self, parent, x=0, y=0, w=0, h=0, mem=None):
        super(AlarmTable, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainLeftAlarmTable')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        print(self.geometry())
        T.set_round_frame(self)
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        # 1. Column 셋업
        self.col_info = [('경보명', 260), ('현재값', 50), ('설정치', 50), ('Unit', 10), ('발생시간', 100), ('경보절차서', 0)]
        self.setColumnCount(len(self.col_info))
        [self.setColumnWidth(i, w) for i, (l, w) in enumerate(self.col_info)]
        self.setHorizontalHeaderLabels([l for (l, w) in self.col_info])
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setFixedHeight(30)
        # 2. Row 셋업
        self.max_line = 23
        [self._add_empty_line(i) for i in range(self.max_line)]
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalScrollBar().setSingleStep(self.rowHeight(0))       # Click 시 이동하는 거리
        self.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical{
                border: none;
                background: rgb(127, 127, 127);                 /* 활성화 x */
                margin: 20 0 20 0;
            }
            QScrollBar::handle:vertical{
                background: rgb(38, 55, 96);                    /* 활성화 o */
            }
            QScrollBar::sub-line:vertical{
                background: rgb(38, 55, 96);                    /* 활성화 o */
                height: 20;
                border-image: url(./interface_image/U_arrow.svg);
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:vertical{
                background: rgb(38, 55, 96);                    /* 활성화 o */
                height: 20;
                border-image: url(./interface_image/D_arrow.svg);
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            """)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)                  # Grid 지우기
        # Alarm info ---------------------------------------------------------------------------------------------------
        self.alarm_info_db = {
            # 'KLAMPO251': {'Urgent': False, 'CurPara': '', 'Criteria': '', 'Descrip': '...'} __ old
            # 'KLAMPO251': {'Descrip': '...', 'Unit': '', 'Criteria': ''}
            'KLAMPO251': {'D': 'Intermediate range high flux rod stop',         'U': '',      'C': ''},
            'KLAMPO252': {'D': 'Power range overpower rod stop',                'U': '',      'C': ''},
            'KLAMPO253': {'D': 'Control bank D full rod withdrawl',             'U': 'Step',  'C': '220'},   # No
            'KLAMPO254': {'D': 'Control bank lo-lo limit',                      'U': '',      'C': ''},
            'KLAMPO255': {'D': 'Two or more rod at bottom',                     'U': '',      'C': ''},

            'KLAMPO256': {'D': 'Axial power distribution limit',                'U': '',      'C': ''},  # No
            'KLAMPO257': {'D': 'CCWS outlet temp hi',                           'U': 'Deg C', 'C': '49.0'},
            'KLAMPO258': {'D': 'Instrument air press lo',                       'U': 'Kg/cm2','C': '6.3'},
            'KLAMPO259': {'D': 'RWST level lo-lo',                              'U': '%',     'C': '5'},
            'KLAMPO260': {'D': 'L/D HX outlet flow lo',                         'U': 'm3/hr', 'C': '15'},  # No

            'KLAMPO261': {'D': 'L/D HX outlet temp hi',                         'U': 'Deg C', 'C': '58'},
            'KLAMPO262': {'D': 'RHX L/D outlet temp hi',                        'U': 'Deg C', 'C': '202'},
            'KLAMPO263': {'D': 'VCT level lo',                                  'U': '%',     'C': '20'},
            'KLAMPO264': {'D': 'VCT press lo',                                  'U': 'kg/cm2','C': '0.7'},
            'KLAMPO265': {'D': 'RCP seal inj wtr flow lo',                      'U': 'm3/hr', 'C': '1.4'},

            'KLAMPO266': {'D': 'Charging flow cont flow lo',                    'U': 'm3/hr', 'C': '5'},  # No
            'KLAMPO267': {'D': 'Not used',                                      'U': '',      'C': ''},  # No
            'KLAMPO268': {'D': 'L/D HX outlet flow hi',                         'U': 'm3/hr', 'C': '30'},  # No
            'KLAMPO269': {'D': 'PRZ press lo SI',                               'U': '',      'C': ''},
            'KLAMPO270': {'D': 'CTMT spray actuated',                           'U': '',      'C': ''},  # No

            'KLAMPO271': {'D': 'VCT level hi',                                  'U': '%',     'C': '80'},
            'KLAMPO272': {'D': 'VCT press hi',                                  'U': 'kg/cm2','C': '4.5'},
            'KLAMPO273': {'D': 'CTMT phase B iso actuated',                     'U': '',      'C': ''},
            'KLAMPO274': {'D': 'Charging flow cont flow hi',                    'U': 'm3/hr', 'C': '27'},  # No
            'KLAMPO295': {'D': 'CTMT sump level hi',                            'U': '',      'C': ''},  # No

            'KLAMPO296': {'D': 'CTMT sump level hi-hi',                         'U': '',      'C': ''},
            'KLAMPO297': {'D': 'CTMT air temp hi',                              'U': 'Deg C', 'C': '48.89'},
            'KLAMPO298': {'D': 'CTMT moisture hi',                              'U': '% of R.H.', 'C': '70'},

            'KLAMPO301': {'D': 'Rad hi alarm',                                  'U': '',      'C': ''},
            'KLAMPO302': {'D': 'CTMT press hi 1 alert',                         'U': '',      'C': ''},
            'KLAMPO303': {'D': 'CTMT press hi 2 alert',                         'U': '',      'C': ''},
            'KLAMPO304': {'D': 'CTMT press hi 3 alert',                         'U': '',      'C': ''},
            'KLAMPO305': {'D': 'Accum. Tk press lo',                            'U': 'kg/cm2','C': '43.4'},

            'KLAMPO306': {'D': 'Accum. Tk press hi',                            'U': 'kg/cm2','C': '43.4'},
            'KLAMPO307': {'D': 'PRZ press hi alert',                            'U': 'kg/cm2','C': '162.4'},
            'KLAMPO308': {'D': 'PRZ press lo alert',                            'U': 'kg/cm2','C': '153.6'},
            'KLAMPO309': {'D': 'PRZ PORV opening',                              'U': 'kg/cm2','C': '164.2'},
            'KLAMPO310': {'D': 'PRZ cont level hi heater on',                   'U': '%',     'C': '5'},

            'KLAMPO311': {'D': 'PRZ cont level lo heater off',                  'U': '%',     'C': '17'},
            'KLAMPO312': {'D': 'PRZ press lo back-up heater on',                'U': 'kg/cm2','C': '153.6'},
            'KLAMPO313': {'D': 'Tref/Auct. Tavg Deviation',                     'U': 'Deg C', 'C': '1.67'},
            'KLAMPO314': {'D': 'RCS 1,2,3 Tavg hi',                             'U': 'Deg C', 'C': '312.78'},
            'KLAMPO315': {'D': 'RCS 1,2,3 Tavg/auct Tavg hi/lo',                'U': 'Deg C', 'C': '1.1'},

            'KLAMPO316': {'D': 'RCS 1,2,3 lo flow alert',                       'U': '%',     'C': '92'},
            'KLAMPO317': {'D': 'PRT temp hi',                                   'U': 'Deg C', 'C': '45'},
            'KLAMPO318': {'D': 'PRT press hi',                                  'U': 'kg/cm2','C': '0.6'},
            'KLAMPO319': {'D': 'SG 1,2,3 level lo',                             'U': '%',     'C': '25'},
            'KLAMPO320': {'D': 'SG 1,2,3 stm/FW flow deviation',                'U': '%',     'C': '10'},

            'KLAMPO321': {'D': 'RCP 1,2,3 trip',                                'U': '',      'C': ''},  # No
            'KLAMPO322': {'D': 'Condensate stor Tk level lo',                   'U': '',      'C': ''},
            'KLAMPO323': {'D': 'Condensate stor Tk level lo-lo',                'U': '',      'C': ''},
            'KLAMPO324': {'D': 'Condensate stor Tk level hi',                   'U': '',      'C': ''},
            'KLAMPO325': {'D': 'MSIV tripped',                                  'U': '',      'C': ''},

            'KLAMPO326': {'D': 'MSL press rate hi steam iso',                   'U': '',      'C': ''},
            'KLAMPO327': {'D': 'MSL 1,2,3 press rate hi',                       'U': 'Pa/sec','C': '689e5'},
            'KLAMPO328': {'D': 'MSL 1,2,3 press low',                           'U': 'kg/cm2','C': '41.1'},
            'KLAMPO329': {'D': 'AFW(MD) actuated'},
            'KLAMPO330': {'D': 'Condenser level lo',                            'U': '"',     'C': '27'},  # No

            'KLAMPO331': {'D': 'FW pump discharge header press hi',             'U': '',      'C': ''},  # No
            'KLAMPO332': {'D': 'FW pump trip',                                  'U': '',      'C': ''},  # No
            'KLAMPO333': {'D': 'FW temp hi',                                    'U': 'Deg C', 'C': '231.1'},
            'KLAMPO334': {'D': 'Condensate pump flow lo',                       'U': 'kg/s',  'C': '88.324'},
            'KLAMPO335': {'D': 'Condenser abs press hi',                        'U': 'mmmHg', 'C': '633'},

            'KLAMPO336': {'D': 'Condenser level hi',                            'U': '"',     'C': '45'},
            'KLAMPO337': {'D': 'TBN trip P-4',                                  'U': '',      'C': ''},
            'KLAMPO338': {'D': 'SG 1,2,3 wtr level hi-hi TBN trip',             'U': '',      'C': ''},
            'KLAMPO339': {'D': 'Condenser vacuum lo TBN trip',                  'U': '',      'C': ''},
            'KLAMPO340': {'D': 'TBN overspeed hi TBN trip',                     'U': '',      'C': ''},

            'KLAMPO341': {'D': 'Gen. brk open',                                 'U': '',      'C': ''},  # No
            # End
        }

    def paintEvent(self, e: QPaintEvent) -> None:
        """ tabelview의 위에 라인 그리기 """
        super(AlarmTable, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        for i in range(self.max_line):
            if i % 5 == 3:
                pen.setColor(QColor(38, 55, 96))            # 가로선 -> 버튼 color
                pen.setWidth(3)
            else:
                pen.setColor(QColor(127, 127, 127))         # 가로선 -> 활성화 x color
                pen.setWidth(1)

            qp.setPen(pen)
            qp.drawLine(0, i*30, self.viewport().width(), i*30)
        qp.restore()

    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        """ AlarmTable 기능 테스트 """
        menu = QMenu()
        add_empty_alarm = menu.addAction('Add Empty Alarm')
        add_alarm = menu.addAction('Add Test Alarm')

        add_empty_alarm.triggered.connect(lambda a: self._add_empty_line(self.columnCount()))
        add_alarm.triggered.connect(lambda a, id='KLAMPO251', current=10: self._add_alarm(id, current))
        menu.exec_(e.globalPos())

    def _add_empty_line(self, i):
        self.insertRow(i)
        [self.setCellWidget(i, _, AlarmEmptyCell(i, self)) for _ in range(len(self.col_info))]
        self.scrollToBottom()

    def _add_alarm(self, alarm_id, current):
        alarm_info = self.alarm_info_db[alarm_id]['D']
        alarm_unit = self.alarm_info_db[alarm_id]['U']
        alarm_criteria = self.alarm_info_db[alarm_id]['C']

        # item 인스턴스 생성
        item_1 = AlarmItemInfo(self, alarm_id, alarm_info)
        item_2 = AlarmItemInfo(self, alarm_id, alarm_unit)
        item_3 = AlarmItemInfo(self, alarm_id, str(current))
        item_4 = AlarmItemInfo(self, alarm_id, alarm_criteria)
        item_5 = AlarmItemTimer(self, alarm_id)

        # 비어 있지 않은 셀 탐색 후 아래에서 위로 데이터 쌓기
        add_row_pos = 0
        for _ in range(0, self.rowCount()):
            if self.cellWidget(_, 0).isempty:
                add_row_pos += 1

        self.insertRow(add_row_pos)  # 마지막 Row 에 섹션 추가

        self.setCellWidget(add_row_pos, 0, item_1)
        self.setCellWidget(add_row_pos, 1, item_2)
        self.setCellWidget(add_row_pos, 2, item_3)
        self.setCellWidget(add_row_pos, 3, item_4)
        self.setCellWidget(add_row_pos, 4, item_5)

        if self.cellWidget(0, 0).isempty:
            # 비어있는 경우 맨 윗줄 지우기
            self.removeRow(0)
        else:
            pass
        self.scrollToBottom()

    def refresh(self):
        """ cell 내용 지우기 및 초기화 """
        pass

class AlarmEmptyCell(QLabel):
    """ 공백 Cell """
    def __init__(self, i, parent):
        super(AlarmEmptyCell, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('AlarmItemEmpty')
        self.isempty = True
        self.setText(str(i))


class AlarmItemInfo(QLabel):
    """ 긴급 여부 판단 아이템 """
    def __init__(self, parent, alarm_id, alarm_info):
        super(AlarmItemInfo, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('AlarmItemInfo')

        self.alarm_id = alarm_id
        self.isempty = False
        self.dis_update(alarm_info)

    def dis_update(self, alarm_info):
        """ 알람 정보 디스플레이 업데이트 """
        self.setText(str(alarm_info))
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 정렬


class AlarmItemTimer(QLabel):
    """ 발생 시간 타이머 아이템 """
    def __init__(self, parent, alarm_id):
        super(AlarmItemTimer, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('AlarmItemInfo')

        self.alarm_id = alarm_id
        self.isempty = False
        self.dis_update()

    def dis_update(self, load_realtime=True):
        """ 타이머 디스플레이 업데이트 """
        if load_realtime:
            real_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            # TODO 나중에 CNS 변수 사용시 real_time 부분 수정할 것.
            real_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.setText(real_time)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 정렬


class SupPresBtn(QPushButton):
    def __init__(self, parent, x=0, y=0, w=0, h=0, mem=None):
        super(SupPresBtn, self).__init__(parent=parent)
        self.mem = mem
        self._AlarmTable:QTableWidget = self.parent().AlarmTable
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainLeftSupPresBtn')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        T.set_round_frame(self)
        # 레이어 셋업 ---------------------------------------------------------------------------------------------------
        self.setText('Suppression Button')

    def mousePressEvent(self, *args, **kwargs):
        """ Btn 클릭 시 -> AlarmTable clear"""
        self._AlarmTable.refresh()
        super(SupPresBtn, self).mousePressEvent(*args, **kwargs)