from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Simulator_CNS import *
from AIDAA_Ver21.Interface_Search import *
from AIDAA_Ver21.Interface_Procedure import *
from AIDAA_Ver21.Interface_Main import *
from AIDAA_Ver21.symptom_check import *
import Interface_QSS as qss
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------------------------------------------------

class Diagnosis(ABCWidget):
    def __init__(self, parent):
        super(Diagnosis, self).__init__(parent)
        self.setStyleSheet(qss.AIDAA_Diagnosis)
        self.setObjectName("BG")
        self.setContentsMargins(0, 0, 8, 0)
        self.setFixedWidth(950)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(DiagnosisTop(self))
        lay.addWidget(ProcedureDiagonsisTable(self))
        lay.addWidget(SystemDiagnosisTable(self))
        lay.addWidget(ProcedureCheckTable(self))


class DiagnosisTop(ABCWidget):
    def __init__(self, parent):
        super(DiagnosisTop, self).__init__(parent)
        self.setContentsMargins(0, 0, 30, 0)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 5)
        lay.addWidget(DiagnosisTopCallProcedureSearch(self))
        lay.addWidget(DiagnosisTopCallSystemSearch(self))
        lay.setSpacing(8)

class DiagnosisTopCallProcedureSearch(ABCPushButton):
    def __init__(self, parent):
        super(DiagnosisTopCallProcedureSearch, self).__init__(parent)
        self.setObjectName("Button")
        icon = os.path.join(ROOT_PATH, 'Img', 'search.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(25, 25))
        self.setFixedSize(451, 35)
        self.setText('비정상 절차서 검색')
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        print('비정상 절차서 검색 창으로 이동')
        ProcedureSearch(self).show()

class DiagnosisTopCallSystemSearch(ABCPushButton):
    def __init__(self, parent):
        super(DiagnosisTopCallSystemSearch, self).__init__(parent)
        self.setObjectName("Button")
        icon = os.path.join(ROOT_PATH, 'Img', 'search.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(25, 25))
        self.setFixedSize(451, 35)
        self.setText('시스템 검색')
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        print('시스템 검색 창으로 이동')
        SystemSearch(self).show()
# ----------------------------------------------------------------------------------------------------------------------

class ProcedureDiagonsisTable(ABCTableWidget):
    def __init__(self, parent):
        super(ProcedureDiagonsisTable, self).__init__(parent)
        self.setObjectName("Table")
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setShowGrid(False)  # Grid 지우기
        self.setFixedWidth(950)
        self.setFixedHeight(211)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기

        column_labels = [('비정상 절차서 명', 555), ('긴급', 95), ('방사선', 95), ('진입조건', 107), ('AI 정확도', 95)]
        self.setColumnCount(len(column_labels))
        self.setRowCount(5)
        # self.setHorizontalHeaderLabels([l for l in self.column_labels])
        col_names = []
        for i, (l, w) in enumerate(column_labels):
            self.setColumnWidth(i, w)
            col_names.append(l)


        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        # self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setContentsMargins(0, 0, 0, 0)

        self.setSelectionBehavior(QTableView.SelectRows)    # 테이블 row click
        self.horizontalHeader().setFixedHeight(35)

        # 테이블 헤더
        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().setStyleSheet(
            "::section {background: rgb(128, 128, 128);font-size:14pt;border:0px solid;}")
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 35)

        self.doubleClicked.connect(self.dis_procedure)
        self.make_centerCB()

        self.widget_timer(iter_=500, funs=[self.dis_update])

    def make_centerCB(self):
        # urgent checkbox 삽입 (행길이 5; checkbox 5개)
        self.urgent_chbox1 = QCheckBox()
        self.urgent_chbox2 = QCheckBox()
        self.urgent_chbox3 = QCheckBox()
        self.urgent_chbox4 = QCheckBox()
        self.urgent_chbox5 = QCheckBox()
        self.urgent_chbox = {0: self.urgent_chbox1, 1: self.urgent_chbox2, 2: self.urgent_chbox3, 3: self.urgent_chbox4,
                             4: self.urgent_chbox5}
        # radiation checkbox 삽입 (행길이 5; checkbox 5개)
        self.radiation_chbox1 = QCheckBox()
        self.radiation_chbox2 = QCheckBox()
        self.radiation_chbox3 = QCheckBox()
        self.radiation_chbox4 = QCheckBox()
        self.radiation_chbox5 = QCheckBox()
        self.radiation_chbox = {0: self.radiation_chbox1, 1: self.radiation_chbox2, 2: self.radiation_chbox3,
                                3: self.radiation_chbox4, 4: self.radiation_chbox5}

        # urgent checkbox 가운데 정렬
        for i in range(5):
            uregent_cellwidget = QWidget()
            urgent_layCB = QHBoxLayout(uregent_cellwidget)
            urgent_layCB.addWidget(self.urgent_chbox[i])
            urgent_layCB.setAlignment(Qt.AlignCenter)
            urgent_layCB.setContentsMargins(0, 0, 0, 0)
            uregent_cellwidget.setLayout(urgent_layCB)
            self.setCellWidget(i, 1, uregent_cellwidget)
        for i in range(5):
            radiation_cellwidget = QWidget()
            radiation_layCB = QHBoxLayout(radiation_cellwidget)
            radiation_layCB.addWidget(self.radiation_chbox[i])
            radiation_layCB.setAlignment(Qt.AlignCenter)
            radiation_layCB.setContentsMargins(0, 0, 0, 0)
            radiation_cellwidget.setLayout(radiation_layCB)
            self.setCellWidget(i, 2, radiation_cellwidget)

    def dis_update(self):
        # print('절차서 진단 AI 업데이트 예정')
        [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
        [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
        [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
        [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
        [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
        self.inmem.current_table['Procedure'] = self.currentRow()

    def dis_procedure(self):
        self.inmem.change_current_system_name('Procedure')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()
# ----------------------------------------------------------------------------------------------------------------------


class SystemDiagnosisTable(ABCTableWidget, QTableWidget):
    def __init__(self, parent):
        super(SystemDiagnosisTable, self).__init__(parent)
        self.setObjectName("Table")
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setShowGrid(False)  # Grid 지우기
        self.setFixedWidth(950)
        self.setFixedHeight(211)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기

        self.column_labels = [('System', 739), ('관련 경보', 98), ('AI 정확도', 95)]
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(5)
        # self.setHorizontalHeaderLabels([l for l in self.column_labels])
        col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            col_names.append(l)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        # self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setContentsMargins(0, 0, 0, 0)

        self.setSelectionBehavior(QTableView.SelectRows)  # 테이블 row click
        self.horizontalHeader().setFixedHeight(35)

        # 테이블 헤더
        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().setStyleSheet(
            "::section {background: rgb(128, 128, 128);font-size:14pt;border:0px solid;}")
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 35)

        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.doubleClicked.connect(self.dis_system)

    def dis_update(self):
        # print('시스템 진단 AI 업데이트 예정')
        [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI_system[i][0])) for i in range(1)]
        [self.setItem(i, 1, QTableWidgetItem(self.inmem.dis_AI_system[i][1])) for i in range(1)]
        [self.setItem(i, 2, QTableWidgetItem(self.inmem.dis_AI_system[i][2])) for i in range(1)]

    def dis_system(self):
        self.inmem.change_current_system_name('Action')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()

# ----------------------------------------------------------------------------------------------------------------------

class ProcedureCheckTable(ABCTableWidget, QTableWidget):
    def __init__(self, parent):
        super(ProcedureCheckTable, self).__init__(parent)
        self.setObjectName("Table")
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setShowGrid(False)  # Grid 지우기
        self.setFixedWidth(950)
        # self.setFixedHeight(211)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기

        self.column_labels = [('비정상 절차서:', 665), ('Value', 95), ('Set-point', 92), ('Unit', 95)]
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(10)
        # self.setHorizontalHeaderLabels([l for l in self.column_labels])
        col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            col_names.append(l)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        # self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setContentsMargins(0, 0, 0, 0)

        self.setSelectionBehavior(QTableView.SelectRows)  # 테이블 row click
        self.horizontalHeader().setFixedHeight(35)

        # 테이블 헤더
        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().setStyleSheet(
            "::section {background: rgb(128, 128, 128);font-size:14pt;border:0px solid;}")
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 35)

        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.current_table['Procedure'] != -1:
            self.inmem.current_procedure[0]=self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]
            self.column_labels = [f'비정상 절차서: {self.inmem.current_procedure[0]}', 'Value', 'Set-point', 'Unit']
            self.setColumnCount(len(self.column_labels))
            self.setHorizontalHeaderLabels([l for l in self.column_labels])

            symptom_count = self.inmem.ShMem.get_pro_symptom_count(self.inmem.current_procedure[0])
            self.setRowCount(symptom_count)
            symptom = self.inmem.ShMem.get_pro_symptom(self.inmem.current_procedure[0])
            [self.setItem(i, 0, QTableWidgetItem(symptom[i]['Des'])) for i in range(symptom_count)]

            [self.item(i,0).setBackground(QColor(150,100,100)) for i in range(symptom_count)]


# ----------------------------------------------------------------------------------------------------------------------