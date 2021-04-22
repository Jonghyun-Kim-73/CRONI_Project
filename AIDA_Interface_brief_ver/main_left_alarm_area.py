import os
import sys
import pandas as pd
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainLeftAlarmArea(QWidget):
    """ 왼쪽 알람 디스플레이 위젯 """
    def __init__(self, parent=None, mem=None):
        super(MainLeftAlarmArea, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubW')
        self.setFixedWidth(int(self.parentWidget().width()/7) * 4)                          # 1/3 부분을 차지

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. 알람 Table
        alarm_label = QLabel('경보 Area')
        alarm_label.setMinimumHeight(30)
        self.alarm_table_wid = ArarmArea(self, self.mem)
        # 2. 알람 Table btn
        alarm_tabel_btn = AlarmSuppressionButton(self)  # 'Suppression Btn')
        # 3. 예지 Area
        prog_label = QLabel('예지 Area')
        prog_label.setMinimumHeight(30)
        prog_area = ProgArea(self)

        # --------------------------------------------------------------------------------------------------------------
        layout.addWidget(alarm_label)
        layout.addWidget(self.alarm_table_wid)
        layout.addSpacing(5)
        layout.addWidget(alarm_tabel_btn)
        layout.addSpacing(10)
        layout.addWidget(prog_label)
        layout.addWidget(prog_area)

        self.setLayout(layout)

    def test1(self):
        print('Alarm Update')

# ----------------------------------------------------------------------------------------------------------------------


class ArarmArea(QWidget):
    def __init__(self, parent, mem=None):
        super(ArarmArea, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubArea')

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.alarm_table = AlarmTable(self, self.mem)
        # --------------------------------------------------------------------------------------------------------------

        layout.addWidget(self.alarm_table)
        self.setLayout(layout)


class AlarmTable(QTableWidget):
    """ 알람 테이블 위젯 """
    def __init__(self, parent, mem):
        super(AlarmTable, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('AlarmTable')

        # 테이블 프레임 모양 정의
        self.verticalHeader().setVisible(False)     # Row 넘버 숨기기

        # 테이블 셋업
        col_info = [('긴급여부', 60), ('경보명', 400), ('현재값', 100), ('설정치', 100), ('발생시간', 0)]

        self.setColumnCount(len(col_info))

        col_names = []
        for i, (l, w) in enumerate(col_info):
            self.setColumnWidth(i, w)
            col_names.append(l)

        self.max_cell = 13

        for i in range(0, self.max_cell):
            self.add_empty_alarm(i)

        cell_height = self.rowHeight(0)
        total_height = self.horizontalHeader().height() + cell_height * self.max_cell + 4        # TODO 4 매번 계산.

        self.parent().setMaximumHeight(total_height)
        self.setMaximumHeight(total_height)

        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(cell_height/3)

        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().setStretchLastSection(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.emergec_alarm_dict = {

        }

        self.call_refresh = False

        if self.mem != None:
            # timer section
            timer = QTimer(self)
            timer.setInterval(1000)
            timer.timeout.connect(self._update)
            timer.start()

    def _update(self):
        if not self.call_refresh:
            self._update_mem_to_alarm_panel()

    def _update_mem_to_alarm_panel(self):
        self.local_mem = self.mem.get_shmem_db()

        """
        알람 섹션
        
        현재 파라 메터가 알람관련 변수라면 입력된 값을 Overwrite
        # -----------  Left panel : KLARML(3,II) -----------------------------------------------------------------------
        #
        #           ---------------------------------------------------
        #           | II = 1 |   9    |   17   |   25   |   33   |  41 |
        #           ---------------------------------------------------
        #           |   2    |   10   |   18   |   26   |   34   |  42|
        #           ---------------------------------------------------
        #           |   3    |   11   |   19   |   27   |   35   |  43 |
        #           ---------------------------------------------------
        #           |   4    |   12   |   20   |   28   |   36   |  44 |
        #           ---------------------------------------------------
        #           |   5    |   13   |   21   |   29   |   37   |  45 |
        #           ---------------------------------------------------
        #           |   6    |   14   |   22   |   30   |   38   |  46 |
        #           ---------------------------------------------------
        #           |   7    |   15   |   23   |   31   |   39   |  47 |
        #           ---------------------------------------------------
        #           |   8    |   16   |   24   |   32   |   40   |  48 |
        #           ---------------------------------------------------
        #
        # ==============================================================================================================
        # -----------  Right panel : KLARMR(3,IJ)
        #
        #       -----------------------------------------------------------------
        #       | IJ=1  |   7   |  13   |  18   |  21   |  26   |  32   |  38   |
        #       -----------------------------------------------------------------
        #       |   2   |   8   |  14   |  19   |  22   |  27   |  33   |  39   |
        #       -----------------------------------------------------------------
        #       |   3   |   9   |  15   |  20   |       |  28   |  34   |  40   |
        #       -----------------------------------------------------------------
        #       |   4   |   10  |  16   |       |  23   |  29   |  35   |  41   |
        #       -----------------------------------------------------------------
        #       |   5   |   11  |       |       |  24   |  30   |  36   |       |
        #       -----------------------------------------------------------------
        #       |   6   |   12  |  17   |       |  25   |  31   |  37   |  42   |
        #       -----------------------------------------------------------------
        #
        # ==============================================================================================================
        
        - CNS와 연결된 경우 동작함.
        - check_alarm_cond 에 CNS 파라메터가 저장되고 저장되지 않은 경우 알람이 추가되는 구조
        - urgent 의 경우 현재 원자로 Trip 부분
        - 알람 1줄에는 CNS 변수의 정보가 저장되어 이 기준을 가지고 관련 절차서를 반환함.
        
        - TODO suppression 버튼을 누르게되면 조건 재확인하여 알람 최신화가 되는 기능 추가해야함.
            - 1) 알람 최신화시 조건이 만족되면 emergec_alarm_dict 에서도 지워야함.
            - 2) 항시 조건이 만족한지 확인하는 모듈도 만들어야함.
            - 3) 최종적으로 해당하는 알람 라인을 지워야함.
        """

        self.alarm_info_db = {
            # 'KLAMPO251': {'Urgent': False, 'CurPara': '', 'Criteria': '', 'Descrip': '...'}
            'KLAMPO251': {'U': False, 'CurP': 'XPIRM',   'CriP': 'CIRFH',   'D': 'Intermediate range high flux rod stop(20% of FP)'},
            'KLAMPO252': {'U': False, 'CurP': 'QPROREL', 'CriP': 'CPRFH',   'D': 'Power range overpower rod stop(103% of FP)'},
            'KLAMPO253': {'U': False, 'CurP': 'KZBANK4', 'CriP': '',        'D': 'Control bank D full rod withdrawl(220 steps)'},
            'KLAMPO254': {'U': False, 'CurP': '',        'CriP': '',        'D': 'Control bank lo-lo limit'},
            'KLAMPO255': {'U': False, 'CurP': '',        'CriP': '',        'D': 'Two or more rod at bottom(ref:A-II-8 p.113 & KAERI87-39)'},

            'KLAMPO256': {'U': False, 'CurP': 'CAXOFF',  'CriP': '',        'D': 'Axial power distribution limit'},
            'KLAMPO257': {'U': False, 'CurP': 'UCCWIN',  'CriP': 'CUCCWH',  'D': 'CCWS outlet temp hi (49.0 deg C)'},
            'KLAMPO258': {'U': False, 'CurP': 'PINSTA',  'CriP': 'CINSTP',  'D': 'Instrument air press lo (6.3 kg/cm2)'},
            'KLAMPO259': {'U': False, 'CurP': 'ZRWST',   'CriP': 'CZRWSLL', 'D': 'RWST level lo-lo (5%)'},
            'KLAMPO260': {'U': False, 'CurP': '',        'CriP': '',        'D': 'L/D HX outlet flow lo (15 m3/hr)'},

            'KLAMPO261': {'U': False, 'CurP': 'UNRHXUT', 'CriP': 'CULDHX',  'D': 'L/D HX outlet temp hi(58 deg C)'},
            'KLAMPO262': {'U': False, 'CurP': 'URHXUT',  'CriP': 'CURHX',   'D': 'RHX L/D outlet temp hi(202 deg C)'},
            'KLAMPO263': {'U': False, 'CurP': 'ZVCT',    'CriP': 'CZVCT2',  'D': 'VCT level lo(20 %)'},
            'KLAMPO264': {'U': False, 'CurP': 'PVCT',    'CriP': 'CPVCTL',  'D': 'VCT press lo(0.7 kg/cm2)'},
            'KLAMPO265': {'U': False, 'CurP': '',        'CriP': 'CWRCPS',  'D': 'RCP seal inj wtr flow lo(1.4 m3/hr)'},

            'KLAMPO266': {'U': False, 'CurP': '',        'CriP': '',  'D': 'Charging flow cont flow lo(5 m3/hr)'},
            'KLAMPO267': {'U': False, 'CurP': '',        'CriP': '',        'D': 'Not used'},
            'KLAMPO268': {'U': False, 'CurP': 'WNETLD',  'CriP': 'CWLHXH',  'D': 'L/D HX outlet flow hi (30  m3/hr)'},
            'KLAMPO269': {'U': False, 'CurP': '',        'CriP': '',        'D': 'PRZ press lo SI'},
            'KLAMPO270': {'U': False, 'CurP': 'KCTMTSP', 'CriP': '',        'D': 'CTMT spray actuated'},

            'KLAMPO271': {'U': False, 'CurP': 'ZVCT',    'CriP': 'CZVCT6',  'D': 'VCT level hi(80 %)'},
            'KLAMPO272': {'U': False, 'CurP': 'PVCT',    'CriP': 'CPVCTH',  'D': 'VCT press hi (4.5 kg/cm2)'},
            'KLAMPO273': {'U': False, 'CurP': 'KCISOB',  'CriP': '',        'D': 'CTMT phase B iso actuated'},
            'KLAMPO274': {'U': False, 'CurP': 'WCHGNO',  'CriP': 'CWCHGH',  'D': 'Charging flow cont flow hi(27 m3/hr)'},
            'KLAMPO295': {'U': False, 'CurP': 'ZSUMP',   'CriP': '',        'D': 'CTMT sump level hi'},

            'KLAMPO296': {'U': False, 'CurP': 'ZSUMP',   'CriP': '',        'D': 'CTMT sump level hi-hi'},
            'KLAMPO297': {'U': False, 'CurP': 'UCTMT',   'CriP': 'CUCTMT',  'D': 'CTMT air temp hi(48.89 deg C)'},
            'KLAMPO298': {'U': False, 'CurP': 'HUCTMT',  'CriP': 'CHCTMT',  'D': 'CTMT moisture hi(70% of R.H.)'},

            'KLAMPO301': {'U': False, 'CurP': '',        'CriP': '',        'D': 'Rad hi alarm'},
            'KLAMPO302': {'U': False, 'CurP': '',        'CriP': '',        'D': 'CTMT press hi 1 alert'},
            'KLAMPO303': {'U': False, 'CurP': '',        'CriP': '',        'D': 'CTMT press hi 2 alert'},
            'KLAMPO304': {'U': False, 'CurP': '',        'CriP': '',        'D': 'CTMT press hi 3 alert'},
            'KLAMPO305': {'U': False, 'CurP': 'PACCTK',  'CriP': 'CPACCL',  'D': 'Accum. Tk press lo (43.4 kg/cm2)'},

            'KLAMPO306': {'U': False, 'CurP': 'PACCTK',  'CriP': 'CPACCH',  'D': 'Accum. Tk press hi (43.4 kg/cm2)'},
            'KLAMPO307': {'U': False, 'CurP': 'PPRZ',    'CriP': 'CPPRZH',  'D': 'PRZ press hi alert(162.4 kg/cm2)'},
            'KLAMPO308': {'U': False, 'CurP': 'PPRZ',    'CriP': 'CPPRZL',  'D': 'PRZ press lo alert(153.6 kg/cm2)'},
            'KLAMPO309': {'U': False, 'CurP': 'BPORV',   'CriP': '',        'D': 'PRZ PORV opening(164.2 kg/cm2)'},
            'KLAMPO310': {'U': False, 'CurP': '',        'CriP': '',        'D': 'PRZ cont level hi heater on(over 5%)'},

            'KLAMPO311': {'U': False, 'CurP': '',        'CriP': '',        'D': 'PRZ cont level lo heater off(17%)'},
            'KLAMPO312': {'U': False, 'CurP': '',        'CriP': '',        'D': 'PRZ press lo back-up heater on(153.6 kg/cm2)'},
            'KLAMPO313': {'U': False, 'CurP': '',        'CriP': '',        'D': 'Tref/Auct. Tavg Deviation(1.67 deg C)'},
            'KLAMPO314': {'U': False, 'CurP': 'UAVLEGM', 'CriP': 'CUTAVG',  'D': 'RCS 1,2,3 Tavg hi(312.78 deg C)'},
            'KLAMPO315': {'U': False, 'CurP': '',        'CriP': '',        'D': 'RCS 1,2,3 Tavg/auct Tavg hi/lo(1.1 deg C)'},

            'KLAMPO316': {'U': False, 'CurP': '',        'CriP': '',        'D': 'RCS 1,2,3 lo flow alert(92%)'},
            'KLAMPO317': {'U': False, 'CurP': 'UPRT',    'CriP': 'CUPRT',   'D': 'PRT temp hi(45deg C )'},
            'KLAMPO318': {'U': False, 'CurP': '',        'CriP': 'CPPRT',   'D': 'PRT  press hi( 0.6kg/cm2)'},
            'KLAMPO319': {'U': False, 'CurP': '',        'CriP': 'CZSGW',   'D': 'SG 1,2,3 level lo(25% of span)'},
            'KLAMPO320': {'U': False, 'CurP': '',        'CriP': '',        'D': 'SG 1,2,3 stm/FW flow deviation(10% of loop flow)'},

            'KLAMPO321': {'U': False, 'CurP': '',        'CriP': '',        'D': 'RCP 1,2,3 trip'},
            'KLAMPO322': {'U': False, 'CurP': 'ZCNDTK',  'CriP': '',        'D': 'Condensate stor Tk level lo'},
            'KLAMPO323': {'U': False, 'CurP': '',        'CriP': '',        'D': 'Condensate stor Tk level lo-lo'},
            'KLAMPO324': {'U': False, 'CurP': 'ZCNDTK',  'CriP': 'CZCTKH',  'D': 'Condensate stor Tk level hi'},
            'KLAMPO325': {'U': False, 'CurP': '',        'CriP': '',        'D': 'MSIV tripped'},

            'KLAMPO326': {'U': False, 'CurP': '',        'CriP': '',        'D': 'MSL press rate hi steam iso'},
            'KLAMPO327': {'U': False, 'CurP': '',        'CriP': 'CMSLH',   'D': 'MSL 1,2,3 press rate hi(-7.03 kg/cm*2/sec = 6.89E5 Pa/sec)'},
            'KLAMPO328': {'U': False, 'CurP': '',        'CriP': 'CPSTML',  'D': 'MSL 1,2,3 press low(41.1 kg/cm*2 = 0.403E7 pas)'},
            'KLAMPO329': {'U': False, 'CurP': '',        'CriP': '',        'D': 'AFW(MD) actuated'},
            'KLAMPO330': {'U': False, 'CurP': 'ZCOND',   'CriP': 'CZCNDL',  'D': 'Condenser level lo(27")'},

            'KLAMPO331': {'U': False, 'CurP': 'PFWPOUT', 'CriP': 'CPFWOH',  'D': 'FW pump discharge header press hi'},
            'KLAMPO332': {'U': False, 'CurP': '',        'CriP': '',        'D': 'FW pump trip'},
            'KLAMPO333': {'U': False, 'CurP': 'UFDW',    'CriP': 'CUFWH',   'D': 'FW temp hi(231.1 deg C)'},
            'KLAMPO334': {'U': False, 'CurP': 'WCDPO',   'CriP': 'CWCDPO',  'D': 'Condensate pump flow lo(1400 gpm=88.324 kg/s)'},
            'KLAMPO335': {'U': False, 'CurP': 'PVAC',    'CriP': 'CPVACH',  'D': 'Condenser abs press hi(633. mmmHg)'},

            'KLAMPO336': {'U': False, 'CurP': 'ZCOND',   'CriP': 'CZCNDH',  'D': 'Condenser level hi (45" )'},
            'KLAMPO337': {'U': False, 'CurP': '',        'CriP': '',        'D': 'TBN trip P-4'},
            'KLAMPO338': {'U': False, 'CurP': '',        'CriP': '',        'D': 'SG 1,2,3 wtr level hi-hi TBN trip'},
            'KLAMPO339': {'U': False, 'CurP': '',        'CriP': '',        'D': 'Condenser vacuum lo TBN trip'},
            'KLAMPO340': {'U': False, 'CurP': '',        'CriP': '',        'D': 'TBN overspeed hi TBN trip'},

            'KLAMPO341': {'U': False, 'CurP': 'KGENB',   'CriP': '',        'D': 'Gen. brk open'},
            # End
        }
        for para_key in self.alarm_info_db.keys():
            self._check_alarm(para_key)

        # 발생한 알람 현재 값 받아서 업데이트
        # 전체 row 를 순회하면서 해당 cell의 3번째 정보창이 비어있지 않으면, 해당셀에 저장된 para 값을 받아서 업데이트
        for i in range(0, self.rowCount()):
            if not self.cellWidget(i, 2).isempty:
                curp, crip = self._check_curp_crip(self.cellWidget(i, 2).alarm_name)
                self.cellWidget(i, 2).dis_update(curp)

    def _check_alarm_cond(self, para):
        """ 발생한 알람 dict 에서 이전에 발생여부 확인후 참/거짓 반환  """
        if self.local_mem[para]['Val'] == 1:
            if not para in self.emergec_alarm_dict.keys():
                return True
            else:
                return False
        else:
            return False

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

    def _check_alarm(self, para):
        """ para 를 self.alarm_info_db에서 탐색후 해당 정보를 할당 """
        if self._check_alarm_cond(para):
            self.emergec_alarm_dict[para] = self.alarm_info_db[para]['D']
            curp, crip = self._check_curp_crip(para)
            urgent = self.alarm_info_db[para]['U']
            self._add_alarm(para, None, curp, crip, urgent)

    def contextMenuEvent(self, event) -> None:
        """ AlarmTable 기능 테스트 """
        menu = QMenu(self)
        test_action1 = menu.addAction("Add Urgent alarm")
        test_action2 = menu.addAction("Add Normal alarm")

        test_action1.triggered.connect(lambda a, alarm_id=0, urgent=True: self.add_alarm(alarm_id, urgent))
        test_action2.triggered.connect(lambda a, alarm_id=1, urgent=False: self.add_alarm(alarm_id, urgent))
        menu.exec_(event.globalPos())

    def add_empty_alarm(self, i):
        self.insertRow(i)
        [self.setCellWidget(i, _, AlarmEmptyCell(self)) for _ in range(0, 5)]

    def add_alarm(self, alarm_id: int, urgent: bool):
        """ Alarm 1개 추가 기능 """
        # db load
        db = pd.read_csv('./DB/alarm_info.csv')
        alarm_info = db.loc[alarm_id, "alarm_name"]
        criteria = db.loc[alarm_id, "criteria"]
        criteria_id = db.loc[alarm_id, "criteria_id"]
        self._add_alarm(criteria_id, alarm_info, 0, criteria, urgent)

    def _add_alarm(self, alarm_name, alarm_info, current, criteria, urgent):
        """ 알람 저장 """
        if alarm_info is None:
            # CNS에 연되면 아래 코드 동작
            alarm_info = self.emergec_alarm_dict[alarm_name]

        item_1 = AlarmItemInfo(self, alarm_name=alarm_name, alarm_info='R' if urgent else 'N')
        item_2 = AlarmItemInfo(self, alarm_name=alarm_name, alarm_info=str(alarm_info))
        item_3 = AlarmItemInfo(self, alarm_name=alarm_name, alarm_info=str(current))
        item_4 = AlarmItemInfo(self, alarm_name=alarm_name, alarm_info=str(criteria))
        item_5 = AlarmItemTimer(self, alarm_name=alarm_name)                          # item 인스턴스 생성

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
        self.scrollToTop()
        pass

    def refresh(self):
        """ suppression btn 용 """
        # TODO 아직 시간이나 주요 기능 없음
        print('Refresh!')
        self.call_refresh = True

        self.emergec_alarm_dict.clear()

        for i in range(self.rowCount()):
            self.removeRow(0)

        for i in range(0, self.max_cell):
            self.add_empty_alarm(i)

        self.call_refresh = False


class AlarmSuppressionButton(QPushButton):
    """알람 Suppression 버튼"""
    def __init__(self, parent):
        super(AlarmSuppressionButton, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('Btn')

        self.setText('Suppression Btn')

        self.clicked.connect(self._run)

    def _run(self):
        # TODO Suppresion 버튼 기능 추가.
        self.parent().alarm_table_wid.alarm_table.refresh()


class AlarmEmptyCell(QLabel):
    """ 공백 Cell """
    def __init__(self, parent):
        super(AlarmEmptyCell, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True) # 상위 스타일 상속
        self.setObjectName('AlarmItemEmpty')
        self.isempty = True


class AlarmItemInfo(QLabel):
    """ 긴급 여부 판단 아이템 """
    def __init__(self, parent, alarm_name, alarm_info):
        super(AlarmItemInfo, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('AlarmItemInfo')

        self.alarm_name = alarm_name
        self.isempty = False
        self.dis_update(alarm_info)

    def dis_update(self, alarm_info):
        """ 알람 정보 디스플레이 업데이트 """
        self.setText(str(alarm_info))
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 정렬

    def mousePressEvent(self, e) -> None:
        print(self.alarm_name)

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


# ----------------------------------------------------------------------------------------------------------------------

class ProgArea(QWidget):
    def __init__(self, parent):
        super(ProgArea, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubArea')

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

        label1 = QLabel('Trip 예정 시간')

        label2 = QLabel('Trip 예상 기여 변수')

        # --------------------------------------------------------------------------------------------------------------
        layout.addWidget(label1)
        layout.addSpacing(50)
        layout.addWidget(label2)
        layout.addSpacing(120)

        self.setLayout(layout)



