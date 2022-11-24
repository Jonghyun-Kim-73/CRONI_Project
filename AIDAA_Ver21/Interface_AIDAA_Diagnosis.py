from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_AIDAA_Procedure_Search import ProcedureSearch, SystemSearch, XAISearch

import numpy as np
import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------------------------------------------------
class Diagnosis(ABCWidget):
    def __init__(self, parent):
        super(Diagnosis, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        #self.setFixedWidth(950)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(DiagnosisTop(self))
        lay.addWidget(DiagnosisProcedureTableScrollArea(self))
        lay.addWidget(DiagnosisSystemScrollArea(self))
        lay.addWidget(ProcedureCheckTableScrollArea(self))
        lay.setSpacing(15)
        self.ProSearchWidget = ProcedureSearch(self)
        self.SysSearchWidget = SystemSearch(self)
        self.XAISearchWidget = XAISearch(self)
        
    def show_ProSearchWidget(self):
        self.ProSearchWidget.show()
    
    def show_SysSearchWidget(self):
        self.SysSearchWidget.show()
        
    def show_XAISearchWidget(self, name):
        # name = sys_name or pro_name
        self.XAISearchWidget.show(name)
class DiagnosisTop(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(DiagnosisTopCallProcedureSearch(self))
        lay.addWidget(DiagnosisTopCallSystemSearch(self))
        lay.setSpacing(10)
class DiagnosisTopCallProcedureSearch(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        icon = os.path.join(ROOT_PATH, 'Img', 'search.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(23, 23))
        self.setFixedSize(467, 40)
        self.setText('비정상 절차서 검색')

        self.clicked.connect(self.inmem.widget_ids['Diagnosis'].show_ProSearchWidget)
class DiagnosisTopCallSystemSearch(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        icon = os.path.join(ROOT_PATH, 'Img', 'search.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(23, 23))
        self.setFixedSize(467, 40)
        self.setText('시스템 검색')
        
        self.clicked.connect(self.inmem.widget_ids['Diagnosis'].show_SysSearchWidget)
# ----------------------------------------------------------------------------------------------------------------------
class DiagnosisProcedureTableScrollArea(ABCScrollArea):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.margins = QMargins(0, 40, 0, 0)  # header height
        self.setViewportMargins(self.margins)
        self.setFixedSize(946, 162)  # 초기 테이블 크기
        
        self.headings_widget = QWidget(self)
        self.headings_layout = QHBoxLayout()
        self.headings_widget.setLayout(self.headings_layout)
        self.headings_layout.setContentsMargins(0, 0, 0, 0)
        
        # header item
        self.heading_label = [
            DiagnosisProcedureHeadingLabel(self, " 비정상 절차서 명", 556, 'F', Qt.AlignmentFlag.AlignLeft),
            DiagnosisProcedureHeadingLabel(self, " 긴급", 80, 'M', Qt.AlignmentFlag.AlignCenter),
            DiagnosisProcedureHeadingLabel(self, " 방사선", 90, 'M', Qt.AlignmentFlag.AlignCenter),
            DiagnosisProcedureHeadingLabel(self, " 진입조건", 120, 'M', Qt.AlignmentFlag.AlignCenter),
            DiagnosisProcedureHeadingLabel(self, " AI", 100, 'L', Qt.AlignmentFlag.AlignCenter),
        ]
        for label in self.heading_label:
            self.headings_layout.addWidget(label)

        # self.headings_layout.addStretch(1)
        self.headings_layout.setSpacing(0)
        
        self.setWidget(DiagnosisProcedureTableWidget(self))
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
    def resizeEvent(self, event):
        rect = self.viewport().geometry()
        self.headings_widget.setGeometry(0, 0, rect.width() - 1, self.margins.top())
        QScrollArea.resizeEvent(self, event)
class DiagnosisProcedureTable(ABCTableWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFixedWidth(945)
        # self.setFixedSize(945, 120) # 초기 테이블 크기
        
        self.setShowGrid(False)  # Grid 지우기
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.horizontalHeader().setVisible(False)  # Col header 숨기기
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionBehavior(QTableView.SelectRows)    # 테이블 row click
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        
        self.column_labels = [(' 비정상 절차서 명', 556), ('긴급', 80), ('방사선', 90), ('진입조건', 120), ('AI', 100)]
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(3)
        self.col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            self.col_names.append(l)
        
        self.setContentsMargins(0, 0, 0, 0)

        # 테이블 헤더
        self.setHorizontalHeaderLabels(self.col_names)
        self.horizontalHeader().setFixedHeight(40)
        self.horizontalHeader().sectionPressed.disconnect()
        # self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정

        [self.setRowHeight(i, 40) for i in range(self.rowCount())] # 테이블 행 높이 조절

        for i in range(3):
            pro_name, logic_condition, ai_probability = self.inmem.dis_AI['AI'][i]
            self.setCellWidget(i, 0, DiagnosisProcedureItem(self, f' {pro_name}', pro_name))
            self.setCellWidget(i, 1, DiagnosisProcedureCheckBox(self, pro_name, 'Rad'))
            self.setCellWidget(i, 2, DiagnosisProcedureCheckBox(self, pro_name, 'Urgent'))
            self.setCellWidget(i, 3, DiagnosisProcedureItem(self, logic_condition, pro_name))
            self.setCellWidget(i, 4, DiagnosisProcedureItem(self, ai_probability, pro_name))

        self.startTimer(600)
        
    def contextMenuEvent(self, a0: QContextMenuEvent) -> None:
        if self.inmem.ShMem.get_para_val('iFixTrain') == 0:
            menu = QMenu()
            xai = menu.addAction('XAI')
            act = menu.exec(a0.globalPos())
            if act == xai:
                pro_name = self.cellWidget(self.selectedIndexes()[0].row(), 0).pro_name
                self.inmem.widget_ids['Diagnosis'].show_XAISearchWidget(pro_name)
        return super().contextMenuEvent(a0)

    def timerEvent(self, event: QTimerEvent) -> None:
        block = 'Off' if self.inmem.ShMem.get_para_val('iFixTrain') == 0 else 'On'
        self.setProperty('Block', block)
        for i in range(3):
            pro_name, logic_condition, ai_probability = self.inmem.dis_AI['AI'][i]
            self.cellWidget(i, 0).update_item(f' {pro_name[:20]}...', pro_name, block) # 15자 까지만 보이기
            self.cellWidget(i, 1).update_item(pro_name, block)
            self.cellWidget(i, 2).update_item(pro_name, block)
            self.cellWidget(i, 3).update_item(logic_condition, pro_name, block)
            self.cellWidget(i, 4).update_item(ai_probability, pro_name, block)

        # def XAISearchShow(self):
    #     XAISearch(self).show()

    #     # --------------------------------------------------------------------------------------------------------------
    #     # 인공지능 모듈 적용 시 구동 코드
    #     # AI Diagnosis Calculation -------------------------------------------------------------------------------------
    #     # self.inmem.get_diagnosis_result()
    #     # if self.inmem.ShMem.get_para_val('iFixTrain') == 1:
    #     #     self.inmem.dis_AI['Train'] = 0
    #     # elif self.inmem.ShMem.get_para_val('iFixTrain') == 2:
    #     #     self.inmem.dis_AI['Train'] = 1
    #     # else:
    #     #     if np.shape(self.inmem.get_train_check_val()) == (1, 10, 46):
    #     #         self.inmem.get_train_check_result()
    #     # --------------------------------------------------------------------------------------------------------------
    #     # if self.inmem.ShMem.get_para_val('iFixTrain') == 2 or self.inmem.dis_AI['Train'] == 1: # 훈련되지 않은 시나리오
    #     #     try:
    #     #         if self.item(0, 0).text() == self.inmem.dis_AI['AI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['AI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['AI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['AI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['AI'][4][0]:
    #     #             [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(1,5)]
    #     #             [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(1,5)]
    #     #         else:
    #     #             self.clear()
    #     #             self.setHorizontalHeaderLabels(self.col_names)
    #     #             self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
    #     #             self.make_centerCB()
    #     #             [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
    #     #             [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(1,5)]
    #     #             [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(1,5)]
    #     #             [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(1,5)]
    #     #             [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(1,5)]
    #     #             [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
    #     #     except:
    #     #         [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
    #     #         [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(1,5)]
    #     #         [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(1,5)]
    #     #         [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(1, 5)]
    #     #         [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(1, 5)]
    #     #         [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
    #     #
    #     # elif self.inmem.ShMem.get_para_val('iFixTrain') == 1 or self.inmem.dis_AI['Train'] == 0 : # 훈련된 시나리오
    #     #     try:
    #     #         if self.item(0, 0).text() == self.inmem.dis_AI['AI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['AI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['AI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['AI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['AI'][4][0]:
    #     #             [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
    #     #             [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
    #     #         else:
    #     #             self.make_centerCB()
    #     #             [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
    #     #             [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
    #     #             [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
    #     #             [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
    #     #             [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
    #     #             [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
    #     #     except:
    #     #         [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
    #     #         [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
    #     #         [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
    #     #         [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
    #     #         [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
    #     #         [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
    #     #
    #     # else:
    #     #     try:
    #     #         if self.item(0, 0).text() == self.inmem.dis_AI['AI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['AI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['AI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['AI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['AI'][4][0]:
    #     #             [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
    #     #             [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
    #     #         else:
    #     #             self.make_centerCB()
    #     #             [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
    #     #             [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
    #     #             [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
    #     #             [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
    #     #             [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
    #     #             [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]
    #     #     except:
    #     #         [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['AI'][i][0])) for i in range(5)]
    #     #         [self.urgent_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][1]) for i in range(5)]
    #     #         [self.radiation_chbox[i].setChecked(self.inmem.dis_AI['AI'][i][2]) for i in range(5)]
    #     #         [self.setItem(i, 3, QTableWidgetItem(self.inmem.dis_AI['AI'][i][3])) for i in range(5)]
    #     #         [self.setItem(i, 4, QTableWidgetItem(self.inmem.dis_AI['AI'][i][4])) for i in range(5)]
    #     #         [self.item(i, 0).setToolTip(self.item(i, 0).text()) for i in range(5)]

        self.style().polish(self)
        return super().timerEvent(event)
# ----------------------------------------------------------------------------------------------------------------------
class DiagnosisProcedureItem(ABCLabel):
    def __init__(self, parent, text, pro_name, widget_name=''):
        super().__init__(parent, widget_name)
        self.block = 'Off'
        self.update_item(text, pro_name, 'Off')
    
    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        if self.block == 'Off':
            self.inmem.widget_ids['Procedure'].set_procedure_name(self.pro_name)
            self.inmem.widget_ids['MainTab'].change_system_page('Procedure')
        return super().mouseDoubleClickEvent(a0)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.inmem.widget_ids['ProcedureCheckTable'].update_table_items('Pro_name', self.pro_name)
        return super().mousePressEvent(ev)

    def update_item(self, text, pro_name, block):
        self.setProperty('Block', block)
        self.block = block
        self.pro_name = pro_name
        self.setText(text if block == 'Off' else '')
        self.setToolTip(self.pro_name)
class DiagnosisProcedureCheckBox(ABCCheckBox):
    def __init__(self, parent, pro_name, type_, widget_name=''):
        super().__init__(parent, widget_name)
        self.type_ = type_
        self.block = 'Off'
        self.update_item(pro_name, 'Off')

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        if self.block == 'Off':
            self.inmem.widget_ids['Procedure'].set_procedure_name(self.pro_name)
            self.inmem.widget_ids['MainTab'].change_system_page('Procedure')
        return super().mouseDoubleClickEvent(a0)
    
    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.inmem.widget_ids['ProcedureCheckTable'].update_table_items('Pro_name', self.pro_name)
        return super().mousePressEvent(ev)

    def update_item(self, pro_name, block):
        self.setProperty('Block', block)
        self.block = block
        self.pro_name = pro_name
        self.toggle = self.inmem.ShMem.get_pro_radiation(pro_name) if self.type_ == 'Rad' else self.inmem.ShMem.get_pro_urgent_act(pro_name)
        self.setCheckState(Qt.Checked if self.toggle else Qt.Unchecked)
        self.style().polish(self) # 반영이 안되서 직접 수행
class DiagnosisProcedureTableWidget(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        
        self.diagnosisproceduretable = DiagnosisProcedureTable(self)
        self.setFixedWidth(self.diagnosisproceduretable.width())
        
        vl = QVBoxLayout(self)
        vl.addWidget(self.diagnosisproceduretable)
        vl.addStretch(1)
        vl.setContentsMargins(0, 0, 0, 0)
class DiagnosisProcedureHeadingLabel(ABCLabel):
    def __init__(self, parent, text, fix_width, pos, alignment, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedWidth(fix_width)
        self.setText(text)
        self.setProperty('Pos', pos)
        self.setAlignment(Qt.AlignVCenter | alignment)
        self.style().polish(self)
# ----------------------------------------------------------------------------------------------------------------------
class DiagnosisSystemScrollArea(ABCScrollArea):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.margins = QMargins(0, 40, 0, 0)  # header height
        self.setViewportMargins(self.margins)
        self.setFixedSize(946, 162)

        self.headings_widget = QWidget(self)
        self.headings_layout = QHBoxLayout()
        self.headings_widget.setLayout(self.headings_layout)
        self.headings_layout.setContentsMargins(0, 0, 0, 0)

        # header item
        self.heading_label = [
            DiagnosisProcedureHeadingLabel(self, " System:", 696, 'F', Qt.AlignmentFlag.AlignLeft),
            DiagnosisProcedureHeadingLabel(self, "관련 경보", 130, 'M', Qt.AlignmentFlag.AlignCenter),
            DiagnosisProcedureHeadingLabel(self, "AI 정확도", 120, 'L', Qt.AlignmentFlag.AlignCenter),
        ]

        for label in self.heading_label:
            self.headings_layout.addWidget(label)

        # self.headings_layout.addStretch(1)
        self.headings_layout.setSpacing(0)

        self.setWidget(DiagnosisSystemTableWidget(self))
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, event):
        rect = self.viewport().geometry()
        self.headings_widget.setGeometry(0, 0, rect.width() - 1, self.margins.top())
        QScrollArea.resizeEvent(self, event)
class DiagnosisSystemTable(ABCTableWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedWidth(945)
        # self.setFixedSize(945, 120) # 초기 테이블 크기
        
        self.setShowGrid(False)  # Grid 지우기
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.horizontalHeader().setVisible(False)  # Col header 숨기기
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionBehavior(QTableView.SelectRows)    # 테이블 row click
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.column_labels = [(' System', 696), ('관련 경보', 120), ('AI 정확도', 120)]
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(3)
        self.col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            self.col_names.append(l)

        self.setContentsMargins(0, 0, 0, 0)

        # 테이블 헤더
        self.setHorizontalHeaderLabels(self.col_names)
        self.horizontalHeader().setFixedHeight(40)
        self.horizontalHeader().sectionPressed.disconnect()
        # self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정
        
        [self.setRowHeight(i, 40) for i in range(self.rowCount())] # 테이블 행 높이 조절

        for i in range(3):
            sys_name, logic_condition, ai_probability = self.inmem.dis_AI['System'][i]
            self.setCellWidget(i, 0, DiagnosisSystemItem(self, f' {sys_name}', sys_name))
            self.setCellWidget(i, 1, DiagnosisSystemItem(self, logic_condition, sys_name))
            self.setCellWidget(i, 2, DiagnosisSystemItem(self, ai_probability, sys_name))

        self.startTimer(600)
        
    def contextMenuEvent(self, a0: QContextMenuEvent) -> None:
        if self.inmem.ShMem.get_para_val('iFixTrain') == 1:
            menu = QMenu()
            xai = menu.addAction('XAI')
            act = menu.exec(a0.globalPos())
            if act == xai:
                sys_name = self.cellWidget(self.selectedIndexes()[0].row(), 0).sys_name
                self.inmem.widget_ids['Diagnosis'].show_XAISearchWidget(sys_name)
        return super().contextMenuEvent(a0)

    def timerEvent(self, event: QTimerEvent) -> None:
        block = 'Off' if self.inmem.ShMem.get_para_val('iFixTrain') == 1 else 'On'
        self.setProperty('Block', block)
        for i in range(3):
            sys_name, logic_condition, ai_probability = self.inmem.dis_AI['System'][i]
            self.cellWidget(i, 0).update_item(f' {sys_name}', sys_name, block)
            self.cellWidget(i, 1).update_item(logic_condition, sys_name, block)
            self.cellWidget(i, 2).update_item(ai_probability, sys_name, block)
        self.style().polish(self)
        return super().timerEvent(event)
# ----------------------------------------------------------------------------------------------------------------------
class DiagnosisSystemItem(ABCLabel):
    def __init__(self, parent, text, sys_name, widget_name=''):
        super().__init__(parent, widget_name)
        self.block = 'Off'
        self.update_item(text, sys_name, 'Off')
    
    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        if self.block == 'Off':
            # self.inmem.widget_ids['Procedure'].set_procedure_name(self.sys_name)
            self.inmem.widget_ids['MainTab'].change_system_page('Action')
        return super().mouseDoubleClickEvent(a0)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if self.block == 'Off':
            self.inmem.widget_ids['ProcedureCheckTable'].update_table_items('Sys_name', self.sys_name)
        return super().mousePressEvent(ev)

    def update_item(self, text, sys_name, block):
        self.setProperty('Block', block)
        self.block = block
        self.sys_name = sys_name
        self.setText(text if block == 'Off' else '')
class DiagnosisSystemTableWidget(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        
        self.diagnosissystemtable = DiagnosisSystemTable(self)
        self.setFixedWidth(self.diagnosissystemtable.width())
        
        vl = QVBoxLayout(self)
        vl.addWidget(self.diagnosissystemtable)
        vl.addStretch(1)
        vl.setContentsMargins(0, 0, 0, 0)
# ----------------------------------------------------------------------------------------------------------------------
class ProcedureCheckTableScrollArea(ABCScrollArea):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.margins = QMargins(0, 40, 0, 0)  # header height
        self.setViewportMargins(self.margins)
        self.setFixedWidth(946)

        self.headings_widget = QWidget(self)
        self.headings_layout = QHBoxLayout()
        self.headings_widget.setLayout(self.headings_layout)
        self.headings_layout.setContentsMargins(0, 0, 10, 0)

        # header item
        self.heading_label = [
            DiagnosisProcedureHeadingLabel(self, " 비정상절차서:", 604, 'F', Qt.AlignmentFlag.AlignLeft),
            DiagnosisProcedureHeadingLabel(self, "VALUE", 93, 'M', Qt.AlignmentFlag.AlignCenter),
            DiagnosisProcedureHeadingLabel(self, "SETPOINT", 142, 'M', Qt.AlignmentFlag.AlignCenter),
            DiagnosisProcedureHeadingLabel(self, "UNIT", 77, 'L', Qt.AlignmentFlag.AlignCenter)
        ]

        for label in self.heading_label:
            self.headings_layout.addWidget(label)

        # self.headings_layout.addStretch(1)
        self.headings_layout.setSpacing(0)

        self.setWidget(ProcedureCheckTableWidget(self))
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, event):
        rect = self.viewport().geometry()
        self.headings_widget.setGeometry(0, 0, rect.width() - 1, self.margins.top())
        QScrollArea.resizeEvent(self, event)
class ProcedureCheckTable(ABCTableWidget):
    def __init__(self, parent):
        super(ProcedureCheckTable, self).__init__(parent)
        self.setFixedSize(915, 675)  # 초기 테이블 크기

        self.setShowGrid(False)  # Grid 지우기
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.horizontalHeader().setVisible(False)  # Col header 숨기기
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionBehavior(QTableView.SelectRows)    # 테이블 row click
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.column_labels = [(' 비정상 절차서:', 604), ('Value', 93), ('Set-point', 142), ('Unit', 77)]
        self.setColumnCount(len(self.column_labels))
        col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            col_names.append(l)

        self.setContentsMargins(0, 0, 0, 0)
        self.symptom_count = 0

        # 테이블 헤더
        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().setFixedHeight(40)
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정

    def update_table_items(self, type_, name):
        [self.removeRow(0) for _ in range(self.rowCount())]

        if type_ == 'Pro_name':
            out_name = f'{name[:15]}...'if len(name) >= 15 else name
            self.inmem.widget_ids['ProcedureCheckTableScrollArea'].heading_label[0].setText(f" 비정상절차서: {out_name}")
            self.inmem.widget_ids['ProcedureCheckTableScrollArea'].heading_label[0].setToolTip(f" 비정상절차서: {name}")
            symptom = self.inmem.ShMem.get_pro_symptom(name)
            symptom_count = self.inmem.ShMem.get_pro_symptom_count(name)
            self.setRowCount(symptom_count)
            
            [self.setCellWidget(i, 0, ProcedureCheckTableItem(self, f' {symptom[i]["Des"]}')) for i in range(symptom_count)]
            [self.setCellWidget(i, 1, ProcedureCheckTableItem(self, f' Test...')) for i in range(symptom_count)]
            [self.setCellWidget(i, 2, ProcedureCheckTableItem(self, f' Test...')) for i in range(symptom_count)]
            [self.setCellWidget(i, 3, ProcedureCheckTableItem(self, f' Test...')) for i in range(symptom_count)]
            
        if type_ == 'Sys_name':
            self.inmem.widget_ids['ProcedureCheckTableScrollArea'].heading_label[0].setText(f" 시스템 명: {name[:15]}")

            symptom_count = 10
            self.setRowCount(symptom_count)
            [self.setCellWidget(i, 0, ProcedureCheckTableItem(self, f' ...')) for i in range(symptom_count)]
            [self.setCellWidget(i, 1, ProcedureCheckTableItem(self, f' ...')) for i in range(symptom_count)]
            [self.setCellWidget(i, 2, ProcedureCheckTableItem(self, f' ...')) for i in range(symptom_count)]
            [self.setCellWidget(i, 3, ProcedureCheckTableItem(self, f' ...')) for i in range(symptom_count)]

        [self.setRowHeight(i, 40) for i in range(self.rowCount())] # 테이블 행 높이 조절
        self.setFixedSize(915, 40 * self.rowCount() if 675 < 40 * self.rowCount() else 675) # Scroll 위함
# ----------------------------------------------------------------------------------------------------------------------
class ProcedureCheckTableItem(ABCLabel):
    def __init__(self, parent, text, widget_name=''):
        super().__init__(parent, widget_name)
        self.setToolTip(text)
        if len(text) >= 20:
            self.setText(text[:20] + '...')
        else:
            self.setText(text)
class ProcedureCheckTableWidget(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        
        self.procedurechecktable = ProcedureCheckTable(self)
        self.setFixedWidth(self.procedurechecktable.width())
        
        vl = QVBoxLayout(self)
        vl.addWidget(self.procedurechecktable)
        vl.addStretch(1)
        vl.setContentsMargins(0, 0, 0, 0)
