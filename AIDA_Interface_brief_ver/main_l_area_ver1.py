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
        # 1. 알람 Table
        self.AlarmTable = AlarmTable(self, x=side_s, y=side_s, w=w-side_s*2, h=h-(side_s*2+s+sp_h), mem=self.mem)
        self.AlarmTableScrollBar = self.AlarmTable.verticalScrollBar()
        print(self.AlarmTableScrollBar)
        self.AlarmTableScrollBar.setParent(self)
        self.AlarmTableScrollBar.setGeometry(0, 0, 10, 100)
        # 2. Subpress Btn
        self.SubPressBtm = SupPresBtn(self, x=side_s, y=h-sp_h-side_s, w=w-side_s*2, h=sp_h, mem=self.mem)


class AlarmTable(QTableWidget):
    def __init__(self, parent, x=0, y=0, w=0, h=0, mem=None):
        super(AlarmTable, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainLeftAlarmTable')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        self._set_frame()
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        # 1. Column 셋업
        self.col_info = [('경보명', 260), ('현재값', 50), ('설정치', 50), ('Unit', 10), ('발생시간', 100), ('경보절차서', 0)]
        self.setColumnCount(len(self.col_info))
        [self.setColumnWidth(i, w) for i, (l, w) in enumerate(self.col_info)]
        self.setHorizontalHeaderLabels([l for (l, w) in self.col_info])
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setFixedHeight(30)
        # 2. Row 셋업
        [self._add_empty_line(i) for i in range(23)]
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)                  # Grid 지우기
        self.setItemDelegate(AlarmLineDelegate(self))
        # Alarm info ---------------------------------------------------------------------------------------------------
        self.alarm_info_db = {
            # 'KLAMPO251': {'Urgent': False, 'CurPara': '', 'Criteria': '', 'Descrip': '...'} __ old
            # 'KLAMPO251': {'Descrip': '...', 'Unit': '', 'Criteria': ''}
            'KLAMPO251': {'D': 'Intermediate range high flux rod stop',         'U': '',      'L': ''},
            'KLAMPO252': {'D': 'Power range overpower rod stop',                'U': '',      'L': ''},
            'KLAMPO253': {'D': 'Control bank D full rod withdrawl',             'U': 'Step',  'L': '220'},   # No
            'KLAMPO254': {'D': 'Control bank lo-lo limit',                      'U': '',      'L': ''},
            'KLAMPO255': {'D': 'Two or more rod at bottom',                     'U': '',      'L': ''},

            'KLAMPO256': {'D': 'Axial power distribution limit',                'U': '',      'L': ''},  # No
            'KLAMPO257': {'D': 'CCWS outlet temp hi',                           'U': 'Deg C', 'L': '49.0'},
            'KLAMPO258': {'D': 'Instrument air press lo',                       'U': 'Kg/cm2','L': '6.3'},
            'KLAMPO259': {'D': 'RWST level lo-lo',                              'U': '%',     'L': '5'},
            'KLAMPO260': {'D': 'L/D HX outlet flow lo',                         'U': 'm3/hr', 'L': '15'},  # No

            'KLAMPO261': {'D': 'L/D HX outlet temp hi',                         'U': 'Deg C', 'L': '58'},
            'KLAMPO262': {'D': 'RHX L/D outlet temp hi',                        'U': 'Deg C', 'L': '202'},
            'KLAMPO263': {'D': 'VCT level lo',                                  'U': '%',     'L': '20'},
            'KLAMPO264': {'D': 'VCT press lo',                                  'U': 'kg/cm2','L': '0.7'},
            'KLAMPO265': {'D': 'RCP seal inj wtr flow lo',                      'U': 'm3/hr', 'L': '1.4'},

            'KLAMPO266': {'D': 'Charging flow cont flow lo',                    'U': 'm3/hr', 'L': '5'},  # No
            'KLAMPO267': {'D': 'Not used',                                      'U': '',      'L': ''},  # No
            'KLAMPO268': {'D': 'L/D HX outlet flow hi',                         'U': 'm3/hr', 'L': '30'},  # No
            'KLAMPO269': {'D': 'PRZ press lo SI',                               'U': '',      'L': ''},
            'KLAMPO270': {'D': 'CTMT spray actuated',                           'U': '',      'L': ''},  # No

            'KLAMPO271': {'D': 'VCT level hi',                                  'U': '%',     'L': '80'},
            'KLAMPO272': {'D': 'VCT press hi',                                  'U': 'kg/cm2','L': '4.5'},
            'KLAMPO273': {'D': 'CTMT phase B iso actuated',                     'U': '',      'L': ''},
            'KLAMPO274': {'D': 'Charging flow cont flow hi',                    'U': 'm3/hr', 'L': '27'},  # No
            'KLAMPO295': {'D': 'CTMT sump level hi',                            'U': '',      'L': ''},  # No

            'KLAMPO296': {'D': 'CTMT sump level hi-hi',                         'U': '',      'L': ''},
            'KLAMPO297': {'D': 'CTMT air temp hi',                              'U': 'Deg C', 'L': '48.89'},
            'KLAMPO298': {'D': 'CTMT moisture hi',                              'U': '% of R.H.', 'L': '70'},

            'KLAMPO301': {'D': 'Rad hi alarm',                                  'U': '',      'L': ''},
            'KLAMPO302': {'D': 'CTMT press hi 1 alert',                         'U': '',      'L': ''},
            'KLAMPO303': {'D': 'CTMT press hi 2 alert',                         'U': '',      'L': ''},
            'KLAMPO304': {'D': 'CTMT press hi 3 alert',                         'U': '',      'L': ''},
            'KLAMPO305': {'D': 'Accum. Tk press lo',                            'U': 'kg/cm2','L': '43.4'},

            'KLAMPO306': {'D': 'Accum. Tk press hi',                            'U': 'kg/cm2','L': '43.4'},
            'KLAMPO307': {'D': 'PRZ press hi alert',                            'U': 'kg/cm2','L': '162.4'},
            'KLAMPO308': {'D': 'PRZ press lo alert',                            'U': 'kg/cm2','L': '153.6'},
            'KLAMPO309': {'D': 'PRZ PORV opening',                              'U': 'kg/cm2','L': '164.2'},
            'KLAMPO310': {'D': 'PRZ cont level hi heater on',                   'U': '%',     'L': '5'},

            'KLAMPO311': {'D': 'PRZ cont level lo heater off',                  'U': '%',     'L': '17'},
            'KLAMPO312': {'D': 'PRZ press lo back-up heater on',                'U': 'kg/cm2','L': '153.6'},
            'KLAMPO313': {'D': 'Tref/Auct. Tavg Deviation',                     'U': 'Deg C', 'L': '1.67'},
            'KLAMPO314': {'D': 'RCS 1,2,3 Tavg hi',                             'U': 'Deg C', 'L': '312.78'},
            'KLAMPO315': {'D': 'RCS 1,2,3 Tavg/auct Tavg hi/lo',                'U': 'Deg C', 'L': '1.1'},

            'KLAMPO316': {'D': 'RCS 1,2,3 lo flow alert',                       'U': '%',     'L': '92'},
            'KLAMPO317': {'D': 'PRT temp hi',                                   'U': 'Deg C', 'L': '45'},
            'KLAMPO318': {'D': 'PRT press hi',                                  'U': 'kg/cm2','L': '0.6'},
            'KLAMPO319': {'D': 'SG 1,2,3 level lo',                             'U': '%',     'L': '25'},
            'KLAMPO320': {'D': 'SG 1,2,3 stm/FW flow deviation',                'U': '%',     'L': '10'},

            'KLAMPO321': {'D': 'RCP 1,2,3 trip',                                'U': '',      'L': ''},  # No
            'KLAMPO322': {'D': 'Condensate stor Tk level lo',                   'U': '',      'L': ''},
            'KLAMPO323': {'D': 'Condensate stor Tk level lo-lo',                'U': '',      'L': ''},
            'KLAMPO324': {'D': 'Condensate stor Tk level hi',                   'U': '',      'L': ''},
            'KLAMPO325': {'D': 'MSIV tripped',                                  'U': '',      'L': ''},

            'KLAMPO326': {'D': 'MSL press rate hi steam iso',                   'U': '',      'L': ''},
            'KLAMPO327': {'D': 'MSL 1,2,3 press rate hi',                       'U': 'Pa/sec','L': '689e5'},
            'KLAMPO328': {'D': 'MSL 1,2,3 press low',                           'U': 'kg/cm2','L': '41.1'},
            'KLAMPO329': {'D': 'AFW(MD) actuated'},
            'KLAMPO330': {'D': 'Condenser level lo',                            'U': '"',     'L': '27'},  # No

            'KLAMPO331': {'D': 'FW pump discharge header press hi',             'U': '',      'L': ''},  # No
            'KLAMPO332': {'D': 'FW pump trip',                                  'U': '',      'L': ''},  # No
            'KLAMPO333': {'D': 'FW temp hi',                                    'U': 'Deg C', 'L': '231.1'},
            'KLAMPO334': {'D': 'Condensate pump flow lo',                       'U': 'kg/s',  'L': '88.324'},
            'KLAMPO335': {'D': 'Condenser abs press hi',                        'U': 'mmmHg', 'L': '633'},

            'KLAMPO336': {'D': 'Condenser level hi',                            'U': '"',     'L': '45'},
            'KLAMPO337': {'D': 'TBN trip P-4',                                  'U': '',      'L': ''},
            'KLAMPO338': {'D': 'SG 1,2,3 wtr level hi-hi TBN trip',             'U': '',      'L': ''},
            'KLAMPO339': {'D': 'Condenser vacuum lo TBN trip',                  'U': '',      'L': ''},
            'KLAMPO340': {'D': 'TBN overspeed hi TBN trip',                     'U': '',      'L': ''},

            'KLAMPO341': {'D': 'Gen. brk open',                                 'U': '',      'L': ''},  # No
            # End
        }

    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        """ AlarmTable 기능 테스트 """
        menu = QMenu()
        add_empty_alarm = menu.addAction('Add Empty Alarm')
        add_alarm = menu.addAction('Add Test Alarm')

        add_empty_alarm.triggered.connect(lambda a: self._add_empty_line(self.columnCount()))
        # add_empty_alarm.triggered.connect(lambda a, id='KLAMPO251', current=10, criteria='100':
        #                                   self._add_alarm(id, current, criteria))
        menu.exec_(e.globalPos())

    def _set_frame(self):
        """ 라운드 테두리 """
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def _add_empty_line(self, i):
        self.insertRow(i)
        [self.setCellWidget(i, _, AlarmEmptyCell(i, self)) for _ in range(len(self.col_info))]
        self.scrollToBottom()

    def _add_alarm(self, alarm_id, current):
        alarm_info = self.alarm_info_db[alarm_id]['D']
        alarm_unit = self.alarm_info_db[alarm_id]['U']
        alarm_criteria = self.alarm_info_db[alarm_id]['C']


class AlarmLineDelegate(QItemDelegate):
    """ 5개 셀씩 라인 및 셀 내부 라인 """
    def __init__(self, parent):
        super(AlarmLineDelegate, self).__init__(parent)
        self._parent_table_widget: QTableWidget = parent

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
        painter.save()
        pen = QPen()
        self._parent_table_widget.rowCount()
        # 세로선 --------------------------------------------------------------------------------------------------------
        # pen.setColor(QColor(127, 127, 127))  # 세로선 -> 활성화 x color
        # pen.setWidth(1)
        # painter.setPen(pen)
        # if index.column() != 0:
        #     painter.drawLine(option.rect.topLeft(), option.rect.bottomLeft())

        # 가로선 --------------------------------------------------------------------------------------------------------
        if self._parent_table_widget.rowCount() % 5 == 0:
            if index.row() % 5 == 4:                        # 5번째 줄 마지막 row인 경우
                pen.setColor(QColor(38, 55, 96))            # 가로선 -> 버튼 color
                pen.setWidth(10)
            else:
                pen.setColor(QColor(127, 127, 127))         # 가로선 -> 활성화 x color
                pen.setWidth(1)
        else:
            if index.row() % 5 == (self._parent_table_widget.rowCount() % 5) - 1:  # 5번째 줄 마지막 row인 경우
                pen.setColor(QColor(38, 55, 96))            # 가로선 -> 버튼 color
                pen.setWidth(10)
            else:
                pen.setColor(QColor(127, 127, 127))         # 가로선 -> 활성화 x color
                pen.setWidth(1)
        painter.setPen(pen)
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
        painter.restore()


class AlarmEmptyCell(QLabel):
    """ 공백 Cell """
    def __init__(self, i, parent):
        super(AlarmEmptyCell, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('AlarmItemEmpty')
        self.isempty = True
        self.setText(str(i))


class AlarmItemTimer(QLabel):
    """ 발생 시간 타이머 아이템 """
    def __init__(self, parent, alarm_name):
        super(AlarmItemTimer, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('AlarmItemInfo')

        self.alarm_name = alarm_name
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
        self._set_frame()
        # 레이어 셋업 ---------------------------------------------------------------------------------------------------
        self.setText('Suppression Button')

    def _set_frame(self):
        """ 라운드 테두리 """
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def mousePressEvent(self, *args, **kwargs):
        """ Btn 클릭 시 -> AlarmTable clear"""
        self._AlarmTable.clear()
        super(SupPresBtn, self).mousePressEvent(*args, **kwargs)