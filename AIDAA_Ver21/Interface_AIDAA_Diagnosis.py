from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Function_Simulator_CNS import *
from AIDAA_Ver21.Interface_AIDAA_Procedure_Search import *
from AIDAA_Ver21.Interface_AIDAA_Procedure import *
from AIDAA_Ver21.Interface_Main import *
from AIDAA_Ver21.Function_AIDAA_Procedure_symptom_check import *
import numpy as np
import Interface_QSS as qss
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------------------------------------------------

class Diagnosis(ABCWidget):
    def __init__(self, parent):
        super(Diagnosis, self).__init__(parent)
        self.setStyleSheet(qss.AIDAA_Diagnosis)
        self.setObjectName("BG")
        self.setContentsMargins(0, 0, 5, 0)
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
        lay.setContentsMargins(0, 0, 0, 0)
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
        # self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")

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
        # self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")

    def dis_update(self):
        print('시스템 검색 창으로 이동')
        SystemSearch(self).show()
# ----------------------------------------------------------------------------------------------------------------------

class MyDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, *args):
        QStyledItemDelegate.__init__(self, parent, *args)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.backgroundBrush = QBrush(QColor(0, 176, 218))

class MyStyledItem(QStyledItemDelegate):
    def __init__(self, margin, radius, border_color, border_width, parent=None):
        """
        margin: distance between border and top of cell
        radius: radius of rounded corner
        border_color: color of border
        border_width: width of border
        """
        super().__init__(parent)
        self.margin = margin
        self.radius = radius
        self.border_color = border_color
        self.border_width = border_width

    def sizeHint(self, option, index):
        # increase original sizeHint to accommodate space needed for border
        size = super().sizeHint(option, index)
        size = size.grownBy(QMargins(0, self.margin, 0, self.margin))
        return size

    def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(painter.Antialiasing)

        painter.setClipping(True)
        painter.setClipRect(option.rect)

        # border enable
        option.rect.adjust(0, self.margin, 0, -self.margin)
        super().paint(painter, option, index)

        pen = painter.pen()
        pen.setColor(self.border_color)
        pen.setWidth(self.border_width)
        painter.setPen(pen)
        # 라인 그리기
        if index.column() == 0:
            rect = option.rect.adjusted(0, 0, self.radius + self.border_width, 0)
            painter.drawRoundedRect(rect, self.radius, self.radius)
        elif index.column() == index.model().columnCount(index.parent()) - 1:
            rect = option.rect.adjusted(-self.radius - self.border_width, 0, -self.border_width, 0)
            painter.drawRoundedRect(rect, self.radius, self.radius)
        else:
            rect = option.rect.adjusted(0, 0, self.border_width, 0)
            painter.drawRect(rect)

        # draw lines between columns
        # if index.column() > 0:
        #     painter.drawLine(rect.top(), rect.bottom())
        #     pen.setWidth(20)
        #     painter.setPen(pen)
        #     painter.drawLine(option.rect.topLeft(), option.rect.bottomLeft())
        painter.restore()

class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

class ProcedureDiagonsisTable(ABCTableWidget):
    def __init__(self, parent):
        super(ProcedureDiagonsisTable, self).__init__(parent)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setShowGrid(False)  # Grid 지우기
        self.setFixedHeight(212)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        column_labels = [(' 비정상 절차서 명', 510), ('긴급', 105), ('방사선', 105), ('진입조건', 103), ('AI 정확도', 120)]
        self.setColumnCount(len(column_labels))
        self.setRowCount(5)

        self.col_names = []
        for i, (l, w) in enumerate(column_labels):
            self.setColumnWidth(i, w)
            self.col_names.append(l)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setContentsMargins(0, 0, 0, 0)

        self.setSelectionBehavior(QTableView.SelectRows)    # 테이블 row click
        self.horizontalHeader().setFixedHeight(35)

        # 테이블 정렬
        delegate = AlignDelegate(self)
        self.setItemDelegateForColumn(3, delegate)
        self.setItemDelegateForColumn(4, delegate)

        # 테이블 헤더
        self.setHorizontalHeaderLabels(self.col_names)
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 35)

        self.doubleClicked.connect(self.dis_procedure)
        self.make_centerCB()    # 체크박스
        self.clicked.connect(self.control_table)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)  # 우클릭 컨텍스트 메뉴 구성
        xai_menu = QAction("XAI", self)
        xai_menu.triggered.connect(self.XAISearchShow)
        self.addAction(xai_menu)

        self.widget_timer(iter_=500, funs=[self.dis_update])

    def XAISearchShow(self):
        XAISearch(self).show()

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
        if self.inmem.dis_AI['Train'] == 1 or self.inmem.ShMem.get_para_val('iFixTrain') == 2:
            for i in range(1,5):
                uregent_cellwidget = QWidget()
                urgent_layCB = QHBoxLayout(uregent_cellwidget)
                urgent_layCB.addWidget(self.urgent_chbox[i])
                urgent_layCB.setAlignment(Qt.AlignCenter)
                urgent_layCB.setContentsMargins(0, 0, 0, 0)
                uregent_cellwidget.setLayout(urgent_layCB)
                self.setCellWidget(i, 1, uregent_cellwidget)
            for i in range(1,5):
                radiation_cellwidget = QWidget()
                radiation_layCB = QHBoxLayout(radiation_cellwidget)
                radiation_layCB.addWidget(self.radiation_chbox[i])
                radiation_layCB.setAlignment(Qt.AlignCenter)
                radiation_layCB.setContentsMargins(0, 0, 0, 0)
                radiation_cellwidget.setLayout(radiation_layCB)
                self.setCellWidget(i, 2, radiation_cellwidget)

        # if self.inmem.dis_AI['Train'] == 0 or self.inmem.dis_AI['Train'] == '' or self.inmem.ShMem.get_para_val('iFixTrain') == 1: # 훈련된 시나리오
        else:
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
        if self.currentRow() != -1:
            self.inmem.current_table['Procedure'] = self.currentRow()

        # AI Diagnosis Calculation -------------------------------------------------------------------------------------
        self.inmem.get_diagnosis_result()
        if np.shape(self.inmem.get_train_check_val()) == (1,10,46):
            self.inmem.get_train_check_result()
        # --------------------------------------------------------------------------------------------------------------
        if self.inmem.ShMem.get_para_val('iFixTrain') == 2 or self.inmem.dis_AI['Train'] == 1: # 훈련되지 않은 시나리오
            try:
                if self.item(0, 0).text() == self.inmem.dis_AI['AI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['AI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['AI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['AI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['AI'][4][0]:
                    [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(1,5)]
                    [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(1,5)]
                else:
                    self.clear()
                    self.setHorizontalHeaderLabels(self.col_names)
                    self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
                    self.make_centerCB()
                    [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
                    [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(1,5)]
                    [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(1,5)]
                    [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(1,5)]
                    [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(1,5)]
                    [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
            except:
                [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
                [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(1,5)]
                [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(1,5)]
                [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(1, 5)]
                [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(1, 5)]
                [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]

        elif self.inmem.ShMem.get_para_val('iFixTrain') == 1 or self.inmem.dis_AI['Train'] == 0 : # 훈련된 시나리오
            try:
                if self.item(0, 0).text() == self.inmem.dis_AI['AI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['AI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['AI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['AI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['AI'][4][0]:
                    [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
                    [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
                else:
                    self.make_centerCB()
                    [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
                    [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
                    [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
                    [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
                    [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
                    [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
            except:
                [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
                [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
                [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
                [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
                [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
                [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]

        else:
            try:
                if self.item(0, 0).text() == self.inmem.dis_AI['AI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['AI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['AI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['AI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['AI'][4][0]:
                    [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
                    [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
                else:
                    self.make_centerCB()
                    [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
                    [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
                    [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
                    [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
                    [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
                    [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
            except:
                [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
                [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
                [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
                [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
                [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
                [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]

            # try:
            #     if self.item(0, 0).text() == self.inmem.dis_AI['AI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['AI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['AI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['AI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['AI'][4][0]:
            #         [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(1,5)]
            #         [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(1,5)]
            #     else:
            #         self.make_centerCB()
            #         [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
            #         [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(1,5)]
            #         [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(1,5)]
            #         [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(1,5)]
            #         [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(1,5)]
            # except:
            #     [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
            #     [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(1,5)]
            #     [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(1,5)]
            #     [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(1, 5)]
            #     [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(1, 5)]
        if self.inmem.current_table['current_window'] == 1:
            self.clearselect()


    def control_table(self):
        self.inmem.current_table['current_window'] = 0

    def clearselect(self):
        self.clearSelection()
        self.repaint()

    def dis_procedure(self):
        self.inmem.change_current_system_name('Procedure')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()
# ----------------------------------------------------------------------------------------------------------------------


class SystemDiagnosisTable(ABCTableWidget):
    def __init__(self, parent):
        super(SystemDiagnosisTable, self).__init__(parent)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setShowGrid(False)  # Grid 지우기
        self.setFixedHeight(212)    # 변경하려면 row height 변경 필요
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.column_labels = [(' System', 705), ('관련 경보', 118), ('AI 정확도', 120)]
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(5)
        col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            col_names.append(l)

        # self.setFocusPolicy(Qt.NoFocus)
        self.setContentsMargins(0, 0, 0, 0)

        self.setSelectionBehavior(QTableView.SelectRows)  # 테이블 row click
        self.horizontalHeader().setFixedHeight(35)

        # 테이블 정렬
        delegate = AlignDelegate(self)
        self.setItemDelegateForColumn(1, delegate)
        self.setItemDelegateForColumn(2, delegate)

        # 테이블 헤더
        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 35)

        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.doubleClicked.connect(self.dis_system)
        self.clicked.connect(self.control_table)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)  # 우클릭 컨텍스트 메뉴 구성
        xai_menu = QAction("XAI", self)
        xai_menu.triggered.connect(self.XAISearchShow)
        self.addAction(xai_menu)

        self.widget_timer(iter_=500, funs=[self.dis_update])

    def XAISearchShow(self):
        XAISearch(self).show()

    def dis_update(self):
        # print('시스템 진단 AI 업데이트 예정')
        if self.currentRow() != -1:
            self.inmem.current_table['System'] = self.currentRow()
        try:
            if self.item(0, 0).text() == self.inmem.dis_AI_system[0][0] and self.item(1, 0).text() == self.inmem.dis_AI_system[1][0] and self.item(2, 0).text() == self.inmem.dis_AI_system[2][0] and self.item(3, 0).text() == self.inmem.dis_AI_system[3][0] and self.item(4, 0).text() == self.inmem.dis_AI_system[4][0]:
                [self.setItem(i, 1, QTableWidgetItem(self.inmem.dis_AI_system[i][1])) for i in range(5)]
                [self.setItem(i, 2, QTableWidgetItem(self.inmem.dis_AI_system[i][2])) for i in range(5)]
            else:
                [self.setItem(i, 0, QTableWidgetItem(" " + self.inmem.dis_AI_system[i][0])) for i in range(5)]
                [self.setItem(i, 1, QTableWidgetItem(self.inmem.dis_AI_system[i][1])) for i in range(5)]
                [self.setItem(i, 2, QTableWidgetItem(self.inmem.dis_AI_system[i][2])) for i in range(5)]
                [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
        except:
            [self.setItem(i, 0, QTableWidgetItem(" " + self.inmem.dis_AI_system[i][0])) for i in range(5)]
            [self.setItem(i, 1, QTableWidgetItem(self.inmem.dis_AI_system[i][1])) for i in range(5)]
            [self.setItem(i, 2, QTableWidgetItem(self.inmem.dis_AI_system[i][2])) for i in range(5)]
            [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]

        if self.inmem.current_table['current_window'] == 0:
            self.clearselect()


    def control_table(self):
        self.inmem.current_table['current_window'] = 1

    def clearselect(self):
        self.clearSelection()
        self.repaint()

    def dis_system(self):
        self.inmem.change_current_system_name('Action')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()

# ----------------------------------------------------------------------------------------------------------------------

class ProcedureCheckTable(ABCTableWidget):
    def __init__(self, parent):
        super(ProcedureCheckTable, self).__init__(parent)
        # self.setObjectName("tab3")
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setShowGrid(False)  # Grid 지우기
        # self.setFixedHeight(211)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기


        self.column_labels = [(' 비정상 절차서:', 615), ('Value', 105), ('Set-point', 122), ('Unit', 101)]
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(10)
        col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            col_names.append(l)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setContentsMargins(0, 0, 0, 0)

        self.setSelectionBehavior(QTableView.SelectRows)  # 테이블 row click
        self.horizontalHeader().setFixedHeight(35)
        # self.setItemDelegate(MyStyledItem(margin=3, radius=5, border_width=3, border_color=QColor(178,178,178)))
        # 테이블 헤더
        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정
        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 35)

        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.current_table['current_window'] == 0:
            if self.inmem.current_table['Procedure'] != -1:
                self.setColumnCount(len(self.column_labels))
                self.column_labels = [
                    ' 비정상 절차서: %s' % f'{self.inmem.dis_AI["AI"][self.inmem.current_table["Procedure"]][0]}', 'Value',
                    'Set-point', 'Unit']
                self.setHorizontalHeaderLabels([l for l in self.column_labels])
                if self.inmem.dis_AI['AI'][self.inmem.current_table["Procedure"]][0] == '학습여부를 아직 확인할 수 없습니다.' or self.inmem.dis_AI['AI'][self.inmem.current_table["Procedure"]][0] == '해당 시나리오는 학습되지 않은 시나리오입니다.':
                    print('해당 사항은 선택할 수 없습니다.')
                    [self.setItem(i, 0, QTableWidgetItem('해당 사항은 선택할 수 없습니다.')) for i in range(10)]
                else:
                    symptom = self.inmem.ShMem.get_pro_symptom(self.inmem.dis_AI["AI"][self.inmem.current_table["Procedure"]][0])
                    if self.inmem.current_table['procedure_name'] != self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]:
                        symptom_count = self.inmem.ShMem.get_pro_symptom_count(
                            self.inmem.dis_AI["AI"][self.inmem.current_table["Procedure"]][0])
                        self.setRowCount(symptom_count)
                        [self.setItem(i, 0, QTableWidgetItem(" " + symptom[i]['Des'])) for i in range(symptom_count)]
                        [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(symptom_count)]
                    self.inmem.current_table['procedure_name'] = self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]


        elif self.inmem.current_table['current_window'] == 1:
            if self.inmem.current_table['System'] != -1:
                self.column_labels = [' System: %s' % f'{self.inmem.dis_AI_system[self.inmem.current_table["System"]][0]}', 'Value', 'Set-point', 'Unit']
                self.setColumnCount(len(self.column_labels))
                self.setHorizontalHeaderLabels([l for l in self.column_labels])
                system_alarm = int(self.inmem.dis_AI_system[self.inmem.current_table["System"]][1])
                self.setRowCount(system_alarm)
                [self.setItem(i, 0, QTableWidgetItem('추후 업데이트 예정')) for i in range(system_alarm)]
                [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(system_alarm)]



# ----------------------------------------------------------------------------------------------------------------------