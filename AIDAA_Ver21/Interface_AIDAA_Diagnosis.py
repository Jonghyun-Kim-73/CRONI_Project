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
        self.setContentsMargins(0, 0, 0, 0)
        #self.setFixedWidth(950)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 10)
        lay.addWidget(DiagnosisTop(self))
        lay.addWidget(ProcedureDiagonsisTable(self))
        lay.addWidget(SystemDiagnosisTable(self))
        lay.addWidget(ProcedureCheckTable(self))
        lay.setSpacing(15)

class DiagnosisTop(ABCWidget):
    def __init__(self, parent):
        super(DiagnosisTop, self).__init__(parent)
        #self.setContentsMargins(0, 0, 0, 0)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(DiagnosisTopCallProcedureSearch(self))
        lay.addWidget(DiagnosisTopCallSystemSearch(self))
        lay.setSpacing(10)

class DiagnosisTopCallProcedureSearch(ABCPushButton):
    def __init__(self, parent):
        super(DiagnosisTopCallProcedureSearch, self).__init__(parent)
        self.setObjectName("Button")
        icon = os.path.join(ROOT_PATH, 'Img', 'search.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(30, 30))
        self.setFixedSize(635, 55)
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
        self.setIconSize(QSize(30, 30))
        self.setFixedSize(635, 55)
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
        self.setFixedHeight(252)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.column_labels = [(' 비정상 절차서 명', 760), ('긴급', 100), ('방사선', 100), ('진입조건', 150), ('AI 정확도', 170)]
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(3)

        self.col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            self.col_names.append(l)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setContentsMargins(0, 0, 0, 0)

        self.setSelectionBehavior(QTableView.SelectRows)    # 테이블 row click
        self.horizontalHeader().setFixedHeight(55)

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
            self.setRowHeight(i, 65)

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
        # urgent checkbox 삽입 (행길이 3; checkbox 3개)
        self.urgent_chbox1 = QCheckBox()
        self.urgent_chbox2 = QCheckBox()
        self.urgent_chbox3 = QCheckBox()
        self.urgent_chbox = {0: self.urgent_chbox1, 1: self.urgent_chbox2, 2: self.urgent_chbox3}
        # radiation checkbox 삽입 (행길이 3; checkbox 3개)
        self.radiation_chbox1 = QCheckBox()
        self.radiation_chbox2 = QCheckBox()
        self.radiation_chbox3 = QCheckBox()
        self.radiation_chbox = {0: self.radiation_chbox1, 1: self.radiation_chbox2, 2: self.radiation_chbox3}

        # urgent checkbox 가운데 정렬
        if self.inmem.dis_AI['Train'] != 2:
            for i in range(3):
                uregent_cellwidget = QWidget()
                urgent_layCB = QHBoxLayout(uregent_cellwidget)
                urgent_layCB.addWidget(self.urgent_chbox[i])
                urgent_layCB.setAlignment(Qt.AlignCenter)
                urgent_layCB.setContentsMargins(0, 0, 0, 0)
                uregent_cellwidget.setLayout(urgent_layCB)
                self.setCellWidget(i, 1, uregent_cellwidget)
            for i in range(1, 3):
                radiation_cellwidget = QWidget()
                radiation_layCB = QHBoxLayout(radiation_cellwidget)
            for i in range(3):
                radiation_cellwidget = QWidget()
                radiation_layCB = QHBoxLayout(radiation_cellwidget)
                radiation_layCB.addWidget(self.radiation_chbox[i])
                radiation_layCB.setAlignment(Qt.AlignCenter)
                radiation_layCB.setContentsMargins(0, 0, 0, 0)
                radiation_cellwidget.setLayout(radiation_layCB)
                self.setCellWidget(i, 2, radiation_cellwidget)
        else:
            for i in range(1, 3):
                uregent_cellwidget = QWidget()
                urgent_layCB = QHBoxLayout(uregent_cellwidget)
                urgent_layCB.addWidget(self.urgent_chbox[i])
                urgent_layCB.setAlignment(Qt.AlignCenter)
                urgent_layCB.setContentsMargins(0, 0, 0, 0)
                uregent_cellwidget.setLayout(urgent_layCB)
                self.setCellWidget(i, 1, uregent_cellwidget)
                radiation_cellwidget = QWidget()
                radiation_layCB = QHBoxLayout(radiation_cellwidget)
                radiation_layCB.addWidget(self.radiation_chbox[i])
                radiation_layCB.setContentsMargins(0, 0, 0, 0)
                radiation_cellwidget.setLayout(radiation_layCB)
                self.setCellWidget(i, 2, radiation_cellwidget)


    def dis_update(self):
        if self.currentRow() != -1 and self.inmem.dis_AI['Train'] == 0:
            self.inmem.current_table['Procedure'] = self.currentRow()
            self.inmem.current_table['selected_procedure'] = self.item(self.currentRow(), 0).text()
        self.inmem.Train_Shortcut_key() # 학습여부 단축키 상시 확인

        if self.inmem.dis_AI['Train'] == 0: # 학습된 시나리오의 경우
            try:
                if self.item(0, 0).text() == self.inmem.dis_AI['AI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['AI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['AI'][2][0]:
                    # 비정상 절차서 명이 변경될 경우에만, 표 내용 업데이트
                    [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(3)]
                    [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(3)]
                else:
                    self.setStyleSheet("""QTableWidget{background: #e9e9e9;selection-color: white;border: 1px solid lightgrey;
                                                selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);
                                                color: #202020;
                                                outline: 0;}
                                                QTableWidget::item::hover{
                                                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);}
                                                QTableWidget::item::focus
                                                {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);border: 0px;}""")
                    [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(3)]
                    [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(3)]
                    [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(3)]
                    [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(3)]
                    [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(3)]
                    [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(3)]
                    [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(3)]
            except:
                self.setStyleSheet("""QTableWidget{background: #e9e9e9;selection-color: white;border: 1px solid lightgrey;
                                            selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);
                                            color: #202020;
                                            outline: 0;}
                                            QTableWidget::item::hover{
                                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);}
                                            QTableWidget::item::focus
                                            {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);border: 0px;}""")
                self.make_centerCB()
                [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(3)]
                [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(3)]
                [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(3)]
                [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(3)]
                [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(3)]
                [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(3)]

        elif self.inmem.dis_AI['Train'] == 1: # 학습되지 않은 시나리오의 경우
            self.clear()
            self.col_names = []
            for i, (l, w) in enumerate(self.column_labels):
                self.setColumnWidth(i, w)
                self.col_names.append(l)
            self.setHorizontalHeaderLabels(self.col_names)
            self.setStyleSheet('background-color: rgb(0, 0, 0);') # 블러 표시

        # --------------------------------------------------------------------------------------------------------------
        # 인공지능 모듈 적용 시 구동 코드
        # AI Diagnosis Calculation -------------------------------------------------------------------------------------
        # self.inmem.get_diagnosis_result()
        # if self.inmem.ShMem.get_para_val('iFixTrain') == 1:
        #     self.inmem.dis_AI['Train'] = 0
        # elif self.inmem.ShMem.get_para_val('iFixTrain') == 2:
        #     self.inmem.dis_AI['Train'] = 1
        # else:
        #     if np.shape(self.inmem.get_train_check_val()) == (1, 10, 46):
        #         self.inmem.get_train_check_result()
        # --------------------------------------------------------------------------------------------------------------
        # if self.inmem.ShMem.get_para_val('iFixTrain') == 2 or self.inmem.dis_AI['Train'] == 1: # 훈련되지 않은 시나리오
        #     try:
        #         if self.item(0, 0).text() == self.inmem.dis_AI['AI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['AI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['AI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['AI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['AI'][4][0]:
        #             [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(1,5)]
        #             [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(1,5)]
        #         else:
        #             self.clear()
        #             self.setHorizontalHeaderLabels(self.col_names)
        #             self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        #             self.make_centerCB()
        #             [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
        #             [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(1,5)]
        #             [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(1,5)]
        #             [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(1,5)]
        #             [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(1,5)]
        #             [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
        #     except:
        #         [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
        #         [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(1,5)]
        #         [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(1,5)]
        #         [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(1, 5)]
        #         [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(1, 5)]
        #         [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
        #
        # elif self.inmem.ShMem.get_para_val('iFixTrain') == 1 or self.inmem.dis_AI['Train'] == 0 : # 훈련된 시나리오
        #     try:
        #         if self.item(0, 0).text() == self.inmem.dis_AI['AI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['AI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['AI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['AI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['AI'][4][0]:
        #             [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
        #             [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
        #         else:
        #             self.make_centerCB()
        #             [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
        #             [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
        #             [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
        #             [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
        #             [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
        #             [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
        #     except:
        #         [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
        #         [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
        #         [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
        #         [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
        #         [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
        #         [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
        #
        # else:
        #     try:
        #         if self.item(0, 0).text() == self.inmem.dis_AI['AI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['AI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['AI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['AI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['AI'][4][0]:
        #             [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
        #             [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
        #         else:
        #             self.make_centerCB()
        #             [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
        #             [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
        #             [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
        #             [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
        #             [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
        #             [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
        #     except:
        #         [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
        #         [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
        #         [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
        #         [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
        #         [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
        #         [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]


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
        self.setFixedHeight(252)    # 변경하려면 row height 변경 필요
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.column_labels = [(' System', 960), ('관련 경보', 150), ('AI 정확도', 170)]
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(3)
        col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            col_names.append(l)

        # self.setFocusPolicy(Qt.NoFocus)
        self.setContentsMargins(0, 0, 0, 0)

        self.setSelectionBehavior(QTableView.SelectRows)  # 테이블 row click
        self.horizontalHeader().setFixedHeight(55)

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
            self.setRowHeight(i, 65)
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
        if self.currentRow() != -1 and self.inmem.dis_AI['Train'] == 1:
            self.inmem.current_table['System'] = self.currentRow()
            self.inmem.current_table['selected_system'] = self.item(self.currentRow(), 0).text()

        if self.inmem.dis_AI['Train'] == 0: # 학습된 시나리오의 경우
            self.clear()
            col_names = []
            for i, (l, w) in enumerate(self.column_labels):
                self.setColumnWidth(i, w)
                col_names.append(l)
            self.setHorizontalHeaderLabels(col_names)
            self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
            self.setStyleSheet('background-color: rgb(0, 0, 0);') # 블러 표시

        elif self.inmem.dis_AI['Train'] == 1: # 학습되지 않은 시나리오의 경우
            try:
                if self.item(0, 0).text() == self.inmem.dis_AI['System'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['System'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['System'][2][0] :
                    [self.setItem(i, 1, QTableWidgetItem(self.inmem.dis_AI['System'][i][1])) for i in range(3)]
                    [self.setItem(i, 2, QTableWidgetItem(self.inmem.dis_AI['System'][i][2])) for i in range(3)]
                else:
                    self.setStyleSheet("""QTableWidget{background: #e9e9e9;selection-color: white;border: 1px solid lightgrey;
                                                selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);
                                                color: #202020;
                                                outline: 0;}
                                                QTableWidget::item::hover{
                                                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);}
                                                QTableWidget::item::focus
                                                {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);border: 0px;}""")
                    [self.setItem(i, 0, QTableWidgetItem(" " + self.inmem.dis_AI['System'][i][0])) for i in range(3)]
                    [self.setItem(i, 1, QTableWidgetItem(self.inmem.dis_AI['System'][i][1])) for i in range(3)]
                    [self.setItem(i, 2, QTableWidgetItem(self.inmem.dis_AI['System'][i][2])) for i in range(3)]
                    [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(3)]
            except:
                self.setStyleSheet("""QTableWidget{background: #e9e9e9;selection-color: white;border: 1px solid lightgrey;
                                            selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);
                                            color: #202020;
                                            outline: 0;}
                                            QTableWidget::item::hover{
                                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);}
                                            QTableWidget::item::focus
                                            {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);border: 0px;}""")
                [self.setItem(i, 0, QTableWidgetItem(" " + self.inmem.dis_AI['System'][i][0])) for i in range(3)]
                [self.setItem(i, 1, QTableWidgetItem(self.inmem.dis_AI['System'][i][1])) for i in range(3)]
                [self.setItem(i, 2, QTableWidgetItem(self.inmem.dis_AI['System'][i][2])) for i in range(3)]
                [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(3)]

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
        self.setObjectName("Tab3")
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setShowGrid(False)  # Grid 지우기
        self.setFixedHeight(721)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setSelectionMode(QAbstractItemView.NoSelection)

        self.column_labels = [(' 비정상 절차서:', 880), ('Value', 100), ('Set-point', 200), ('Unit', 100)]
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(10)
        col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            col_names.append(l)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setContentsMargins(0, 0, 0, 0)
        self.symptom_count = 0
        self.setSelectionBehavior(QTableView.SelectRows)  # 테이블 row click
        self.horizontalHeader().setFixedHeight(55)
        # self.setItemDelegate(MyStyledItem(margin=3, radius=5, border_width=3, border_color=QColor(178,178,178)))
        # 테이블 헤더
        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정
        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 65)

        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        # iFixTrain 대응을 위한 code
        if self.inmem.dis_AI['Train'] == 0: # 학습된 시나리오
            self.inmem.current_table['current_window'] = 0
            self.inmem.current_table['System'] = -1
        elif self.inmem.dis_AI['Train'] == 1: # 학습되지 않은 시나리오 시나리오
            self.inmem.current_table['current_window'] = 1
            self.inmem.current_table['Procedure'] = -1

        if self.inmem.current_table['current_window'] == 0: # 학습된 시나리오
            if self.inmem.current_table['Procedure'] != -1:
                self.setColumnCount(len(self.column_labels))
                for i in range(0, self.rowCount()):
                    self.setRowHeight(i, 65)
                self.column_labels = [
                    ' 비정상 절차서: %s' % f'{self.inmem.dis_AI["AI"][self.inmem.current_table["Procedure"]][0]}', 'Value',
                    'Set-point', 'Unit']
                self.setHorizontalHeaderLabels([l for l in self.column_labels])
                self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
                if self.inmem.dis_AI['AI'][self.inmem.current_table["Procedure"]][0] == '학습여부를 아직 확인할 수 없습니다.' or self.inmem.dis_AI['AI'][self.inmem.current_table["Procedure"]][0] == '해당 시나리오는 학습되지 않은 시나리오입니다.':
                    print('해당 사항은 선택할 수 없습니다.')
                    [self.setItem(i, 0, QTableWidgetItem('해당 사항은 선택할 수 없습니다.')) for i in range(self.rowCount())]
                else:
                    symptom = self.inmem.ShMem.get_pro_symptom(self.inmem.dis_AI["AI"][self.inmem.current_table["Procedure"]][0])
                    if self.inmem.current_table['procedure_name'] != self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]:
                        self.symptom_count = self.inmem.ShMem.get_pro_symptom_count(
                            self.inmem.dis_AI["AI"][self.inmem.current_table["Procedure"]][0])
                        self.setRowCount(self.symptom_count)
                        [self.setItem(i, 0, QTableWidgetItem(" " + symptom[i]['Des'])) for i in range(self.symptom_count)]
                        [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(self.symptom_count)]
                        [self.item(i, 0).setSelected(False) for i in range(self.symptom_count)] # 아이쳄 1,2,3 추가시 수정필요
                        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음':
                            for i in range(0, self.symptom_count):
                                if symptom[i]['ManClick']:
                                    self.item(i, 0).setSelected(True)  # 아이쳄 1,2,3 추가시 수정필요
                    self.inmem.current_table['procedure_name'] = self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]
            else:
                self.clear()
                self.column_labels = ['비정상 절차서:', 'Value', 'Set-point', 'Unit']
                self.setColumnCount(len(self.column_labels))
                self.setHorizontalHeaderLabels([l for l in self.column_labels])
                self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)

                    # for i in range(self.symptom_count):
                    #     if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    #             self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                    #         if self.inmem.get_ab_procedure_Manual_Check(i):
                    #             # self.setStyleSheet("""QTableWidget::item {
                    #             #                     font: 30px;
                    #             #                     border-bottom: 1px solid rgb(128, 128, 128);
                    #             #                     background:yellow;
                    #             # }""")
                    #             print(i)


        elif self.inmem.current_table['current_window'] == 1: # 학습되지 않은 시나리오
            if self.inmem.current_table['System'] != -1:
                for i in range(0, self.rowCount()):
                    self.setRowHeight(i, 65)
                self.column_labels = [' System: %s' % f'{self.inmem.dis_AI["System"][self.inmem.current_table["System"]][0]}', 'Value', 'Set-point', 'Unit']
                self.setColumnCount(len(self.column_labels))
                self.setHorizontalHeaderLabels([l for l in self.column_labels])
                self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
                system_alarm = int(self.inmem.dis_AI['System'][self.inmem.current_table["System"]][1])
                self.setRowCount(system_alarm)
                [self.setItem(i, 0, QTableWidgetItem('추후 업데이트 예정')) for i in range(system_alarm)]
                [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(system_alarm)]

            else:
                self.clear()
                self.column_labels = [' System:', 'Value', 'Set-point', 'Unit']
                self.setColumnCount(len(self.column_labels))
                self.setHorizontalHeaderLabels([l for l in self.column_labels])
                self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)


# ----------------------------------------------------------------------------------------------------------------------