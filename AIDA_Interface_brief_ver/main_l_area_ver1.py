import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDA_Interface_brief_ver.TOOL.TOOL_etc import ToolEtc as T
from AIDA_Interface_brief_ver.Procedure.alarm_procedure import alarm_pd

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainLeftArea(QWidget):
    """ 왼쪽 알람 디스플레이 위젯 """
    def __init__(self, parent, h, w, mem=None):
        super(MainLeftArea, self).__init__(parent)
        self.mem = mem
        self.Mainwindow = parent

        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainLeftArea')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setFixedHeight(h)
        self.setFixedWidth(w)
        # 레이어 셋업 ---------------------------------------------------------------------------------------------------
        sp_h, s, side_s = 30, 5, 5
        scroll_w = 20
        # 1. 알람 Table
        self.AlarmTable = AlarmTable(self, x=side_s, y=side_s, w=w-side_s*2 - scroll_w, h=h-(side_s*2+s+sp_h))
        self.AlarmTableScrollBar = self.AlarmTable.verticalScrollBar()
        self.AlarmTableScrollBar.setParent(self)
        self.AlarmTableScrollBar.setGeometry(side_s + self.AlarmTable.width() + s,
                                             side_s + self.AlarmTable.horizontalHeader().height(),
                                             scroll_w,
                                             h-(side_s*2+s+sp_h) - self.AlarmTable.horizontalHeader().height())

        # 2. Subpress Btn
        self.SubPressBtm = SupPresBtn(self, x=side_s, y=h-sp_h-side_s, w=w-side_s*2 - scroll_w, h=sp_h)

    def paintEvent(self, e: QPaintEvent) -> None:
        qp = QPainter(self)
        qp.save()
        pen = QPen()
        pen.setColor(QColor(127, 127, 127))  # 가로선 -> 활성화 x color
        pen.setWidth(2)
        qp.setPen(pen)
        qp.drawRoundedRect(self.AlarmTable.geometry(), 10, 10)
        qp.restore()


class AlarmTable(QTableWidget):
    def __init__(self, parent, x=0, y=0, w=0, h=0):
        super(AlarmTable, self).__init__(parent=parent)
        self.mem = parent.mem
        self.local_mem = self.mem.get_shmem_db()
        self.Mainwindow = parent.Mainwindow
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setObjectName('MainLeftAlarmTable')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        T.set_round_frame(self)
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        # 1. Column 셋업
        self.col_info = [('경보명', 240), ('현재값', 50), ('설정치', 50), ('Unit', 10), ('발생시간', 0)]
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
            'Empty':     {'D': '',                                              'CurP':'',         'CriP': '',        'U': '',      'C': ''},    # Empty Cell
            'KLAMPO251': {'D': 'Intermediate range high flux rod stop',         'CurP': 'XPIRM',   'CriP': 'CIRFH',   'U': '',      'C': ''},
            'KLAMPO252': {'D': 'Power range overpower rod stop',                'CurP': 'QPROREL', 'CriP': 'CPRFH',   'U': '',      'C': ''},
            'KLAMPO253': {'D': 'Control bank D full rod withdrawl',             'CurP': 'KZBANK4', 'CriP': '',        'U': 'Step',  'C': '220'},   # No
            'KLAMPO254': {'D': 'Control bank lo-lo limit',                      'CurP': '',        'CriP': '',        'U': '',      'C': ''},
            'KLAMPO255': {'D': 'Two or more rod at bottom',                     'CurP': '',        'CriP': '',        'U': '',      'C': ''},

            'KLAMPO256': {'D': 'Axial power distribution limit',                'CurP': 'CAXOFF',  'CriP': '',        'U': '',      'C': ''},  # No
            'KLAMPO257': {'D': 'CCWS outlet temp hi',                           'CurP': 'UCCWIN',  'CriP': 'CUCCWH',  'U': 'Deg C', 'C': '49.0'},
            'KLAMPO258': {'D': 'Instrument air press lo',                       'CurP': 'PINSTA',  'CriP': 'CINSTP',  'U': 'Kg/cm2','C': '6.3'},
            'KLAMPO259': {'D': 'RWST level lo-lo',                              'CurP': 'ZRWST',   'CriP': 'CZRWSLL', 'U': '%',     'C': '5'},
            'KLAMPO260': {'D': 'L/D HX outlet flow lo',                         'CurP': '',        'CriP': '',        'U': 'm3/hr', 'C': '15'},  # No

            'KLAMPO261': {'D': 'L/D HX outlet temp hi',                         'CurP': 'UNRHXUT', 'CriP': 'CULDHX',  'U': 'Deg C', 'C': '58'},
            'KLAMPO262': {'D': 'RHX L/D outlet temp hi',                        'CurP': 'URHXUT',  'CriP': 'CURHX',   'U': 'Deg C', 'C': '202'},
            'KLAMPO263': {'D': 'VCT level lo',                                  'CurP': 'ZVCT',    'CriP': 'CZVCT2',  'U': '%',     'C': '20'},
            'KLAMPO264': {'D': 'VCT press lo',                                  'CurP': 'PVCT',    'CriP': 'CPVCTL',  'U': 'kg/cm2','C': '0.7'},
            'KLAMPO265': {'D': 'RCP seal inj wtr flow lo',                      'CurP': '',        'CriP': 'CWRCPS',  'U': 'm3/hr', 'C': '1.4'},

            'KLAMPO266': {'D': 'Charging flow cont flow lo',                    'CurP': '',        'CriP': '',        'U': 'm3/hr', 'C': '5'},  # No
            'KLAMPO267': {'D': 'Not used',                                      'CurP': '',        'CriP': '',        'U': '',      'C': ''},  # No
            'KLAMPO268': {'D': 'L/D HX outlet flow hi',                         'CurP': 'WNETLD',  'CriP': 'CWLHXH',  'U': 'm3/hr', 'C': '30'},  # No
            'KLAMPO269': {'D': 'PRZ press lo SI',                               'CurP': '',        'CriP': '',        'U': '',      'C': ''},
            'KLAMPO270': {'D': 'CTMT spray actuated',                           'CurP': 'KCTMTSP', 'CriP': '',        'U': '',      'C': ''},  # No

            'KLAMPO271': {'D': 'VCT level hi',                                  'CurP': 'ZVCT',    'CriP': 'CZVCT6',  'U': '%',     'C': '80'},
            'KLAMPO272': {'D': 'VCT press hi',                                  'CurP': 'PVCT',    'CriP': 'CPVCTH',  'U': 'kg/cm2','C': '4.5'},
            'KLAMPO273': {'D': 'CTMT phase B iso actuated',                     'CurP': 'KCISOB',  'CriP': '',        'U': '',      'C': ''},
            'KLAMPO274': {'D': 'Charging flow cont flow hi',                    'CurP': 'WCHGNO',  'CriP': 'CWCHGH',  'U': 'm3/hr', 'C': '27'},  # No
            'KLAMPO295': {'D': 'CTMT sump level hi',                            'CurP': 'ZSUMP',   'CriP': '',        'U': '',      'C': ''},  # No

            'KLAMPO296': {'D': 'CTMT sump level hi-hi',                         'CurP': 'ZSUMP',   'CriP': '',        'U': '',      'C': ''},
            'KLAMPO297': {'D': 'CTMT air temp hi',                              'CurP': 'UCTMT',   'CriP': 'CUCTMT',  'U': 'Deg C', 'C': '48.89'},
            'KLAMPO298': {'D': 'CTMT moisture hi',                              'CurP': 'HUCTMT',  'CriP': 'CHCTMT',  'U': '% of R.H.', 'C': '70'},

            'KLAMPO301': {'D': 'Rad hi alarm',                                  'CurP': '',        'CriP': '',        'U': '',      'C': ''},
            'KLAMPO302': {'D': 'CTMT press hi 1 alert',                         'CurP': '',        'CriP': '',        'U': '',      'C': ''},
            'KLAMPO303': {'D': 'CTMT press hi 2 alert',                         'CurP': '',        'CriP': '',        'U': '',      'C': ''},
            'KLAMPO304': {'D': 'CTMT press hi 3 alert',                         'CurP': '',        'CriP': '',        'U': '',      'C': ''},
            'KLAMPO305': {'D': 'Accum. Tk press lo',                            'CurP': 'PACCTK',  'CriP': 'CPACCL',  'U': 'kg/cm2','C': '43.4'},

            'KLAMPO306': {'D': 'Accum. Tk press hi',                            'CurP': 'PACCTK',  'CriP': 'CPACCH',  'U': 'kg/cm2','C': '43.4'},
            'KLAMPO307': {'D': 'PRZ press hi alert',                            'CurP': 'PPRZ',    'CriP': 'CPPRZH',  'U': 'kg/cm2','C': '162.4'},
            'KLAMPO308': {'D': 'PRZ press lo alert',                            'CurP': 'PPRZ',    'CriP': 'CPPRZL',  'U': 'kg/cm2','C': '153.6'},
            'KLAMPO309': {'D': 'PRZ PORV opening',                              'CurP': 'BPORV',   'CriP': '',        'U': 'kg/cm2','C': '164.2'},
            'KLAMPO310': {'D': 'PRZ cont level hi heater on',                   'CurP': '',        'CriP': '',        'U': '%',     'C': '5'},

            'KLAMPO311': {'D': 'PRZ cont level lo heater off',                  'CurP': '',        'CriP': '',        'U': '%',     'C': '17'},
            'KLAMPO312': {'D': 'PRZ press lo back-up heater on',                'CurP': 'PPRZ',    'CriP': 'CPPRZL',  'U': 'kg/cm2','C': '153.6'},
            'KLAMPO313': {'D': 'Tref/Auct. Tavg Deviation',                     'CurP': '',        'CriP': '',        'U': 'Deg C', 'C': '1.67'},
            'KLAMPO314': {'D': 'RCS 1,2,3 Tavg hi',                             'CurP': 'UAVLEGM', 'CriP': 'CUTAVG',  'U': 'Deg C', 'C': '312.78'},
            'KLAMPO315': {'D': 'RCS 1,2,3 Tavg/auct Tavg hi/lo',                'CurP': '',        'CriP': '',        'U': 'Deg C', 'C': '1.1'},

            'KLAMPO316': {'D': 'RCS 1,2,3 lo flow alert',                       'CurP': '',        'CriP': '',        'U': '%',     'C': '92'},
            'KLAMPO317': {'D': 'PRT temp hi',                                   'CurP': 'UPRT',    'CriP': 'CUPRT',   'U': 'Deg C', 'C': '45'},
            'KLAMPO318': {'D': 'PRT press hi',                                  'CurP': '',        'CriP': 'CPPRT',   'U': 'kg/cm2','C': '0.6'},
            'KLAMPO319': {'D': 'SG 1,2,3 level lo',                             'CurP': '',        'CriP': 'CZSGW',   'U': '%',     'C': '25'},
            'KLAMPO320': {'D': 'SG 1,2,3 stm/FW flow deviation',                'CurP': '',        'CriP': '',        'U': '%',     'C': '10'},

            'KLAMPO321': {'D': 'RCP 1,2,3 trip',                                'CurP': '',        'CriP': '',        'U': '',      'C': ''},  # No
            'KLAMPO322': {'D': 'Condensate stor Tk level lo',                   'CurP': 'ZCNDTK',  'CriP': '',        'U': '',      'C': ''},
            'KLAMPO323': {'D': 'Condensate stor Tk level lo-lo',                'CurP': '',        'CriP': '',        'U': '',      'C': ''},
            'KLAMPO324': {'D': 'Condensate stor Tk level hi',                   'CurP': 'ZCNDTK',  'CriP': 'CZCTKH',  'U': '',      'C': ''},
            'KLAMPO325': {'D': 'MSIV tripped',                                  'CurP': '',        'CriP': '',        'U': '',      'C': ''},

            'KLAMPO326': {'D': 'MSL press rate hi steam iso',                   'CurP': '',        'CriP': '',        'U': '',      'C': ''},
            'KLAMPO327': {'D': 'MSL 1,2,3 press rate hi',                       'CurP': '',        'CriP': 'CMSLH',   'U': 'Pa/sec','C': '689e5'},
            'KLAMPO328': {'D': 'MSL 1,2,3 press low',                           'CurP': '',        'CriP': 'CPSTML',  'U': 'kg/cm2','C': '41.1'},
            'KLAMPO329': {'D': 'AFW(MD) actuated',                              'CurP': '',        'CriP': '',        'U': '',      'C': '0'},
            'KLAMPO330': {'D': 'Condenser level lo',                            'CurP': 'ZCOND',   'CriP': 'CZCNDL',  'U': '"',     'C': '27'},  # No

            'KLAMPO331': {'D': 'FW pump discharge header press hi',             'CurP': 'PFWPOUT', 'CriP': 'CPFWOH',  'U': '',      'C': ''},  # No
            'KLAMPO332': {'D': 'FW pump trip',                                  'CurP': '',        'CriP': '',        'U': '',      'C': ''},  # No
            'KLAMPO333': {'D': 'FW temp hi',                                    'CurP': 'UFDW',    'CriP': 'CUFWH',   'U': 'Deg C', 'C': '231.1'},
            'KLAMPO334': {'D': 'Condensate pump flow lo',                       'CurP': 'WCDPO',   'CriP': 'CWCDPO',  'U': 'kg/s',  'C': '88.324'},
            'KLAMPO335': {'D': 'Condenser abs press hi',                        'CurP': 'PVAC',    'CriP': 'CPVACH',  'U': 'mmmHg', 'C': '633'},

            'KLAMPO336': {'D': 'Condenser level hi',                            'CurP': 'ZCOND',   'CriP': 'CZCNDH',  'U': '"',     'C': '45'},
            'KLAMPO337': {'D': 'TBN trip P-4',                                  'CurP': '',        'CriP': '',        'U': '',      'C': ''},
            'KLAMPO338': {'D': 'SG 1,2,3 wtr level hi-hi TBN trip',             'CurP': '',        'CriP': '',        'U': '',      'C': ''},
            'KLAMPO339': {'D': 'Condenser vacuum lo TBN trip',                  'CurP': '',        'CriP': '',        'U': '',      'C': ''},
            'KLAMPO340': {'D': 'TBN overspeed hi TBN trip',                     'CurP': '',        'CriP': '',        'U': '',      'C': ''},

            'KLAMPO341': {'D': 'Gen. brk open',                                 'CurP': 'KGENB',   'CriP': '',        'U': '',      'C': ''},  # No
            # End
        }
        self.alarm_his = []
        # Alarm display update -----------------------------------------------------------------------------------------
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self._update_alarm_display)
        timer.start()

    # ==================================================================================================================
    # 함수 Overwrite

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
        self.local_mem = self.mem.get_shmem_db()

        menu = QMenu()
        add_empty_alarm = menu.addAction('Add Empty Alarm')
        add_alarm = menu.addAction('Add Test Alarm 1')
        add_alarms = menu.addAction('Add Test Alarms')

        def alarms_(ids):
            for i in range(len(ids)):
                self._add_alarm(ids[i], 10)

        add_empty_alarm.triggered.connect(lambda a: self._add_empty_line(self.columnCount()))
        add_alarm.triggered.connect(lambda a, id='KLAMPO251', current=10: self._add_alarm(id, current))
        add_alarms.triggered.connect(lambda a, ids=['KLAMPO263', 'KLAMPO308', 'KLAMPO312']: alarms_(ids))
        menu.exec_(e.globalPos())

    # ==================================================================================================================
    # Private functions

    def _add_empty_line(self, i):
        self.insertRow(i)
        [self.setCellWidget(i, _, AlarmItemInfo(self, 'Empty', '')) for _ in range(len(self.col_info))]
        self.scrollToBottom()

    def _add_alarm(self, alarm_id, current):
        """ 새로운 알람 추가 """
        alarm_info = self.alarm_info_db[alarm_id]['D']
        alarm_unit = self.alarm_info_db[alarm_id]['U']
        alarm_criteria = self.alarm_info_db[alarm_id]['C']

        # item 인스턴스 생성
        item_1 = AlarmItemInfo(self, alarm_id, alarm_info)
        item_2 = AlarmItemInfo(self, alarm_id, str(current))
        item_3 = AlarmItemInfo(self, alarm_id, alarm_criteria)
        item_4 = AlarmItemInfo(self, alarm_id, alarm_unit)
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

    def _update_alarm_display(self):
        self.local_mem = self.mem.get_shmem_db()

        # 1. 발생한 알람 현재 값 받아서 업데이트
        # 전체 row 를 순회하면서 해당 cell의 3번째 정보창이 비어있지 않으면, 해당셀에 저장된 para 값을 받아서 업데이트
        for i in range(0, self.rowCount()):
            if not self.cellWidget(i, 1).isempty:
                curp, crip = self._check_curp_crip(self.cellWidget(i, 1).alarm_id)
                self.cellWidget(i, 1).dis_update(curp)

        # 2. 새롭게 발생한 알람 찾기
        alarm_list = list(self.alarm_info_db.keys())
        del alarm_list[alarm_list.index('Empty')]

        for alarm_name in alarm_list:                       # 사전에 선정된 알람 DB의 알람 id 를 순회함.
            if self.local_mem[alarm_name]['Val'] == 1:      # 만약 해당 알람 id 값이 1 이면 알람 추가를 시도함.
                if not alarm_name in self.alarm_his:        # 이전에 추가된 알람이 아닌 경우에만 추가함.
                    self._add_alarm(alarm_name, 0)
                    self.alarm_his.append(alarm_name)

    def _check_curp_crip(self, para):
        # 현재 값이나 기준치가 모호한 경우 공백으로 처리
        curp = '' if self.alarm_info_db[para]['CurP'] == '' else self.local_mem[self.alarm_info_db[para]['CurP']]['Val']
        crip = '' if self.alarm_info_db[para]['CriP'] == '' else self.local_mem[self.alarm_info_db[para]['CriP']]['Val']

        # 추가적으로 변수에따라 입력되는 값.
        if True:
            if para == 'KLAMPO253': crip = '200'
            if para == 'KLAMPO256':
                curp = f"{round(self.local_mem['CAXOFF']['Val'], 2)}"
                crip = '0.3 ~ 0.12'
            if para == 'KLAMPO258': crip = crip - 1.5
            if para == 'KLAMPO270': crip = '1'
            if para == 'KLAMPO273': crip = '1'
        if True:
            if para == 'KLAMPO295': crip = '2.492'
            if para == 'KLAMPO296': crip = '2.9238'
            if para == 'KLAMPO302':
                curp = str(self.local_mem['PCTMT']['Val'] * self.mem['PAKGCM']['Val'])
                crip = '0.3515'
            if para == 'KLAMPO303':
                curp = str(self.local_mem['PCTMT']['Val'] * self.mem['PAKGCM']['Val'])
                crip = '1.02'
            if para == 'KLAMPO304':
                curp = str(self.local_mem['PCTMT']['Val'] * self.mem['PAKGCM']['Val'])
                crip = '1.62'
        if True:
            if para == 'KLAMPO308':
                curp = f"{self.local_mem['PPRZ']['Val'] / 1e+5 : 3.2f}"
                crip = f"{self.local_mem['CPPRZL']['Val'] / 1e+5 : 3.2f}"
            if para == 'KLAMPO309': crip = '0.01'
            if para == 'KLAMPO318':
                curp = str(self.local_mem['PPRT']['Val'] - 0.98E5)
            if para == 'KLAMPO319':
                curp = f"{self.local_mem['ZINST78']['Val']:3.2f}"
                crip = f"{self.local_mem['CZSGW']['Val'] * 100:3.2f}"
            if para == 'KLAMPO322': crip = '8.55'
            if para == 'KLAMPO323': crip = '7.57'
            if para == 'KLAMPO332':
                curp = str(
                    self.local_mem['KFWP1']['Val'] + self.local_mem['KFWP2']['Val'] + self.local_mem['KFWP3']['Val'])
                crip = '0'
            if para == 'KLAMPO334': curp = str(self.local_mem['WCDPO']['Val'] * 0.047)
            if para == 'KLAMPO335':
                curp = f'{curp:3.3f}'
                crip = f'{crip:3.3f}'
            if para == 'KLAMPO338':
                crip = '0.78'
            if para == 'KLAMPO341': crip = '0'
        return curp, crip

    # ==================================================================================================================
    # Public functions

    def refresh(self):
        """ 정상화된 알람 제거 """
        self.local_mem = self.mem.get_shmem_db()

        removed_index = []

        for i in range(0, self.rowCount()):
            if not self.cellWidget(i, 1).isempty:
                para = self.cellWidget(i, 1).alarm_id
                if self.local_mem[para]['Val'] == 0:
                    # 알람 발생 불만족 조건도달하여 해당 알람 라인 삭제
                    removed_index.append(i)
                """ 기능 테스트 용 """
                # if para == 'KLAMPO253' or para == 'KLAMPO251':
                #     removed_index.append(i)
        # Removed_index 에 로깅된 cell 라인 제거
        for i, pos in enumerate(removed_index):
            self.removeRow(pos - i)
        # 현재 남은 라인이 최대 라인의 수보다 적은지 파악
        if self.max_line < self.rowCount():
            [self._add_empty_line(0) for _ in range(self.max_line - self.rowCount())]   # 최대 라인만큼 채우기
        else:
            # 제거된 라인수 만큼 cell 추가
            [self._add_empty_line(0) for _ in range(len(removed_index))]
        pass


class AlarmItemInfo(QLabel):
    """ AlarmTable 의 Item """
    def __init__(self, parent, alarm_id, alarm_info):
        super(AlarmItemInfo, self).__init__(parent=parent)
        self.Mainwindow = parent.Mainwindow
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setObjectName('AlarmItemInfo')

        self.alarm_id = alarm_id
        self.isempty = True if alarm_id == 'Empty' else False
        self.dis_update(alarm_info)

    # ==================================================================================================================
    # Public functions

    def dis_update(self, alarm_info):
        """ 알람 정보 디스플레이 업데이트 """
        self.setText(str(alarm_info))
        self.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)  # 텍스트 정렬

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        print(f'{self.alarm_id}_Cell Clicked')

        get_alarm_procedure = alarm_pd[self.alarm_id]

        if get_alarm_procedure is not None:
            if ev.button() == Qt.RightButton:
                self.Mainwindow.update_selected_procedure(get_alarm_procedure, change_panel=True)
            elif ev.button() == Qt.LeftButton:
                self.Mainwindow.update_selected_procedure(get_alarm_procedure, change_panel=False)

        super(AlarmItemInfo, self).mousePressEvent(ev)


class AlarmItemTimer(QLabel):
    """ 발생 시간 타이머 아이템 """
    def __init__(self, parent, alarm_id):
        super(AlarmItemTimer, self).__init__(parent=parent)
        self.Mainwindow = parent.Mainwindow
        # --------------------------------------------------------------------------------------------------------------
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

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        print(f'{self.alarm_id}_Cell Clicked')

        get_alarm_procedure = alarm_pd[self.alarm_id]

        if get_alarm_procedure is not None:
            if ev.button() == Qt.RightButton:
                self.Mainwindow.update_selected_procedure(get_alarm_procedure, change_panel=True)
            elif ev.button() == Qt.LeftButton:
                self.Mainwindow.update_selected_procedure(get_alarm_procedure, change_panel=False)

        super(AlarmItemTimer, self).mousePressEvent(ev)


class SupPresBtn(QPushButton):
    def __init__(self, parent, x=0, y=0, w=0, h=0):
        super(SupPresBtn, self).__init__(parent=parent)
        self.mem = parent.mem
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