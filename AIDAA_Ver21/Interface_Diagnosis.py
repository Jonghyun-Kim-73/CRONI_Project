from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Simulator_CNS import *
from AIDAA_Ver21.Interface_Search import *
from AIDAA_Ver21.Interface_Procedure import *
from AIDAA_Ver21.Interface_Main import *

# ----------------------------------------------------------------------------------------------------------------------

class Diagnosis(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Diagnosis, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        self.setGeometry(200, 200, 1900, 1000)

        lay = QVBoxLayout(self)
        lay.addWidget(DiagnosisTop(self))
        lay.addWidget(ProcedureDiagonsisTable(self))
        lay.addWidget(SystemDiagnosisTable(self))
        lay.addWidget(ProcedureCheckTable(self))


class DiagnosisTop(ABCWidget, QWidget):
    def __init__(self, parent):
        super(DiagnosisTop, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(DiagnosisTopCallProcedureSearch(self))
        lay.addWidget(DiagnosisTopCallSystemSearch(self))

class DiagnosisTopCallProcedureSearch(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(DiagnosisTopCallProcedureSearch, self).__init__(parent)
        self.setText('비정상 절차서 검색')
        self.clicked.connect(self.dis_update)
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")


    def dis_update(self):
        print('비정상 절차서 검색 창으로 이동')
        ProcedureSearch(self).show()

class DiagnosisTopCallSystemSearch(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(DiagnosisTopCallSystemSearch, self).__init__(parent)
        self.setText('시스템 검색')
        self.clicked.connect(self.dis_update)
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")

    def dis_update(self):
        print('시스템 검색 창으로 이동')
        SystemSearch(self).show()
# ----------------------------------------------------------------------------------------------------------------------

class ProcedureDiagonsisTable(ABCTableWidget, QTableWidget):
    def __init__(self, parent):
        super(ProcedureDiagonsisTable, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.column_labels = ['비정상 절차서 명', '긴급', '방사선', '진입조건', 'AI 정확도']
        self.setColumnCount(len(self.column_labels))
        self.setHorizontalHeaderLabels([l for l in self.column_labels])
        self.setRowCount(5)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setStyleSheet("""QTableWidget{background: #e9e9e9;selection-color: white;border: 1px solid lightgrey;
                            selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);
                            color: #202020;
                            outline: 0;}
                            QTableWidget::item::hover{
                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);}
                            QTableWidget::item::focus
                            {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);border: 0px;}""")

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

        # [self.urgent_chbox[i].setStyleSheet("QCheckBo" "x::indicator" "{""background-color : black;""}") for i in range(5)]
        # [self.radiation_chbox[i].setStyleSheet("QCheckBo" "x::indicator" "{""background-color : black;""}") for i in range(5)]

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
        [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI[i][0])) for i in range(5)]
        [self.urgent_chbox[i].setChecked(self.inmem.dis_AI[i][1]) for i in range(5)]
        [self.radiation_chbox[i].setChecked(self.inmem.dis_AI[i][2]) for i in range(5)]
        [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI[i][3])) for i in range(5)]
        [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI[i][4])) for i in range(5)]
        # [self.setItem(i, 1, QTableWidgetItem(self.inmem.dis_AI[i][1])) for i in range(5)]
        # self.radiation_chbox1.setChecked(True)

    def dis_procedure(self):
        self.inmem.change_current_system_name('Procedure')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()
# ----------------------------------------------------------------------------------------------------------------------


class SystemDiagnosisTable(ABCTableWidget, QTableWidget):
    def __init__(self, parent):
        super(SystemDiagnosisTable, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.column_labels = ['System', '관련 경보', 'AI 정확도']
        self.setColumnCount(len(self.column_labels))
        self.setHorizontalHeaderLabels([l for l in self.column_labels])

        self.setRowCount(5)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setStyleSheet("""QTableWidget{background: #e9e9e9;selection-color: white;border: 1px solid lightgrey;
                            selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);
                            color: #202020;
                            outline: 0;}
                            QTableWidget::item::hover{
                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);}
                            QTableWidget::item::focus
                            {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);border: 0px;}""")

        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        # print('시스템 진단 AI 업데이트 예정')
        [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI_system[i][0])) for i in range(1)]
        [self.setItem(i, 1, QTableWidgetItem(self.inmem.dis_AI_system[i][1])) for i in range(1)]
        [self.setItem(i, 2, QTableWidgetItem(self.inmem.dis_AI_system[i][2])) for i in range(1)]
        pass

# ----------------------------------------------------------------------------------------------------------------------

class ProcedureCheckTable(ABCTableWidget, QTableWidget):
    def __init__(self, parent):
        super(ProcedureCheckTable, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.column_labels = ['비정상 절차서:', 'Value', 'Set-point', 'Unit']
        self.setColumnCount(len(self.column_labels))
        self.setHorizontalHeaderLabels([l for l in self.column_labels])

        self.setRowCount(10)


# ----------------------------------------------------------------------------------------------------------------------


class DiagnosisTab(ABCStackWidget, QStackedWidget):
    def __init__(self, parent):
        super(DiagnosisTab, self).__init__(parent)
        [self.addWidget(_) for _ in [Procedure(self)]]

    def change_system_page(self, system_name):
        self.setCurrentIndex({'Main': 0, 'IFAP': 1, 'AIDAA': 2, 'EGIS': 3}[system_name])