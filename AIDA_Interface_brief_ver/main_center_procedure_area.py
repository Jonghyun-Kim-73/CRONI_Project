import os
import sys
import pandas as pd
from datetime import datetime
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainCenterProcedureArea(QWidget):
    """ 가운데 절차서 진단 디스플레이 위젯 """

    def __init__(self, parent=None):
        super(MainCenterProcedureArea, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubW')
        # self.setMaximumWidth(int(self.parentWidget().width() / 5) * 2)  # 1/3 부분을 차지

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # 2. 증상 및 XAI Area
        self.Symptomxai_area = SymptomXAIArea(self)

        # 3. 절차서 x 일때 조치 Area
        self.non_procedure_area = NonProcedureArea(self)

        # 1. 절차서 Table
        procedure_label = QLabel('절차서 Area')
        procedure_label.setMinimumHeight(30)
        procedure_area = ProcedureArea(self, self.Symptomxai_area, self.non_procedure_area)

        # 4. 기능 복구 조치 Btn
        non_procedure_btn = QPushButton('기능 복구 조치 Btn')
        non_procedure_btn.setObjectName('Btn')
        non_procedure_btn.clicked.connect(self.open_area)

        # --------------------------------------------------------------------------------------------------------------
        layout.addWidget(procedure_label)
        layout.addWidget(procedure_area)
        layout.addWidget(self.Symptomxai_area)
        layout.addWidget(self.non_procedure_area)
        layout.addWidget(non_procedure_btn)

        self.setLayout(layout)

    def open_area(self):
        if self.non_procedure_area.cond_visible:
            self.non_procedure_area.open_area(cond=False)
        else:
            self.non_procedure_area.open_area(cond=True)
        self.Symptomxai_area.open_area(cond=False)


# ----------------------------------------------------------------------------------------------------------------------


class ProcedureArea(QWidget):
    def __init__(self, parent, symxai, nonpro):
        super(ProcedureArea, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubArea')

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.procedure_table = ProcedureTable(self, symxai, nonpro)

        # --------------------------------------------------------------------------------------------------------------

        layout.addWidget(self.procedure_table)
        self.setLayout(layout)


class ProcedureTable(QTableWidget):
    def __init__(self, parent, symxai, nonpro):
        super(ProcedureTable, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('ProcedureTable')

        # SymXai과 Nonpro 위젯 메모리 주소 받기
        self.symxai, self.nonpro = symxai, nonpro

        # 테이블 프레임 모양 정의
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기

        # 테이블 셋업
        col_info = [('비정상 절차서 명', 230), ('AI확신도', 100), ('진입 조건 확인', 100), ('긴급', 0)]

        self.setColumnCount(len(col_info))

        col_names = []
        for i, (l, w) in enumerate(col_info):
            self.setColumnWidth(i, w)
            col_names.append(l)

        self.max_cell = 3

        for i in range(0, self.max_cell):
            self.add_empty_procedure(i)

        cell_height = self.rowHeight(0)
        total_height = self.horizontalHeader().height() + cell_height * self.max_cell + 4  # TODO 4 매번 계산.

        # self.parent().setMaximumHeight(total_height)
        # self.setMaximumHeight(total_height)

        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(cell_height / 3)

        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().setStretchLastSection(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def add_empty_procedure(self, i):
        self.insertRow(i)
        [self.setCellWidget(i, _, ProcedureEmptyCell(self)) for _ in range(0, 4)]

    def add_procedure(self, row, name, ai_prob, if_prob, em):
        """
        테이블에 진단 결과 정보 저장하기

        :param name:
        :param ai_prob:
        :param if_prob:
        :param em:
        :return:
        """
        item1 = ProcedureNameCell(self, name, self.symxai, self.nonpro)
        item2 = ProcedureAIProbCell(self, name, ai_prob, self.symxai, self.nonpro)
        item3 = ProcedureInfoCell(self, if_prob, self.symxai, self.nonpro)
        item4 = ProcedureInfoCell(self, em, self.symxai, self.nonpro)
        self.setCellWidget(row, 0, item1)
        self.setCellWidget(row, 1, item2)
        self.setCellWidget(row, 2, item3)
        self.setCellWidget(row, 3, item4)

    def update_procedure(self):
        self.add_procedure(0, '비정상00', 50, '12/12', 'Y')
        self.add_procedure(1, '비정상02', 30, '2/4', 'N')
        self.add_procedure(2, '비정상03', 20, '0/5', 'N')

    def contextMenuEvent(self, event) -> None:
        """ ProcedureTable 에 기능 올리기  """
        menu = QMenu(self)
        add_procedure = menu.addAction("Add procedure")
        update_procedure = menu.addAction("Update procedure")
        get_net = menu.addAction("Get_pronet")

        add_procedure.triggered.connect(lambda a: self.add_procedure(0, '비정상00', 95, '10/12', 'Y'))
        update_procedure.triggered.connect(lambda a: self.add_procedure(0, '비정상01', 80, '10/12', 'Y'))
        get_net.triggered.connect(self.update_procedure)
        menu.exec_(event.globalPos())


class ProcedureEmptyCell(QLabel):
    """ 공백 Cell """
    def __init__(self, parent):
        super(ProcedureEmptyCell, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True) # 상위 스타일 상속
        self.setObjectName('ProcedureItemEmpty')
        self.isempty = True


class ProcedureBaseCell(QLabel):
    """ 셀 Label 공통 """
    def __init__(self, parent, symxai, nonpro):
        super(ProcedureBaseCell, self).__init__(parent=parent)
        # SymXai과 Nonpro 위젯 메모리 주소 받기
        self.symxai, self.nonpro = symxai, nonpro

        self.procedure_name = ''

    def mousePressEvent(self, e) -> None:
        if self.nonpro.cond_visible:
            self.nonpro.open_area(cond=False)
        else:
            self.symxai.open_area(cond=True, abnomal_name=self.procedure_name)


class ProcedureBaseWidget(QWidget):
    """ 셀 Widget 공통 """
    def __init__(self, parent, symxai, nonpro):
        super(ProcedureBaseWidget, self).__init__(parent=parent)
        # SymXai과 Nonpro 위젯 메모리 주소 받기
        self.symxai, self.nonpro = symxai, nonpro

        self.procedure_name = ''

    def mousePressEvent(self, e) -> None:
        if self.nonpro.cond_visible:
            self.nonpro.open_area(cond=False)
        else:
            self.symxai.open_area(cond=True, abnomal_name=self.procedure_name)


class ProcedureNameCell(ProcedureBaseCell):
    """ 절차서 명 Cell """
    def __init__(self, parent, name, symxai, nonpro):
        super(ProcedureNameCell, self).__init__(parent, symxai, nonpro)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('ProcedureItemInfo')
        self.isempty = False

        self.procedure_name = name

        self.setText(name)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 가운데 정렬


class ProcedureAIProbCell(ProcedureBaseWidget):
    """ AI 확신도 """
    def __init__(self, parent, name, aiprob, symxai, nonpro):
        super(ProcedureAIProbCell, self).__init__(parent, symxai, nonpro)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속

        self.isempty = False

        self.procedure_name = name

        layer = QHBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)
        layer.setSpacing(5)

        prg_bar = QProgressBar()
        prg_bar.setObjectName('ProcedureItemProgress')
        prg_bar.setValue(aiprob)
        prg_bar.setTextVisible(False)

        prg_label = QLabel()
        prg_label.setObjectName('ProcedureItemProgressLabel')
        prg_label.setFixedWidth(30)
        prg_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)  # 텍스트 가운데 정렬
        prg_label.setText(f'{aiprob}%')

        layer.addWidget(prg_bar)
        layer.addWidget(prg_label)

        self.setLayout(layer)


class ProcedureInfoCell(ProcedureBaseCell):
    """ 절차서 Info Cell """
    def __init__(self, parent, name, symxai, nonpro):
        super(ProcedureInfoCell, self).__init__(parent, symxai, nonpro)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('ProcedureItemInfo')
        self.isempty = False

        self.procedure_name = name

        self.setText(name)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 가운데 정렬

# ----------------------------------------------------------------------------------------------------------------------


class SymptomXAIArea(QWidget):
    def __init__(self, parent):
        super(SymptomXAIArea, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubArea')

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        self.Vlayout = QVBoxLayout(self)
        self.Vlayout.setContentsMargins(0, 0, 0, 0)
        self.Vlayout.setSpacing(0)

        self.Abnormal_procedure_name = QLabel('')
        self.Abnormal_procedure_name.setFixedHeight(30)

        self.Hlayout = QHBoxLayout()
        self.Hlayout.setContentsMargins(0, 0, 0, 0)
        self.Hlayout.setSpacing(0)

        self.Symptom_area = SymptomArea(self)
        self.XAI_area = QLabel('Xai')
        # --------------------------------------------------------------------------------------------------------------
        self.Hlayout.addWidget(self.Symptom_area)
        self.Hlayout.addWidget(self.XAI_area)

        self.Vlayout.addWidget(self.Abnormal_procedure_name)
        self.Vlayout.addLayout(self.Hlayout)

        self.setLayout(self.Vlayout)

        self.fold_time = 200
        self.ani_symptomxai_area = QPropertyAnimation(self, b'minimumHeight')
        self.ani_symptomxai_area.setDuration(self.fold_time)

        self._visible(False)
        self.cond_visible = False
        self.abnomal_name = ''

    def _visible(self, trig):
        self.Symptom_area.setVisible(trig)
        self.XAI_area.setVisible(trig)
        self.Abnormal_procedure_name.setVisible(trig)

        if trig:
            self.Vlayout.setContentsMargins(5, 5, 5, 5)
        else:
            self.Vlayout.setContentsMargins(0, 0, 0, 0)
        self.cond_visible = trig

    def open_area(self, cond, abnomal_name=''):
        if cond == True and abnomal_name == self.abnomal_name:
            cond = False

        if cond:
            self._visible(True)
            self.Abnormal_procedure_name.setText(f'{abnomal_name}')
            self.abnomal_name = abnomal_name

            # self.ani_symptomxai_area.setStartValue(self.height())
            self.ani_symptomxai_area.setStartValue(self.height())
            self.ani_symptomxai_area.setEndValue(458)
            self.ani_symptomxai_area.start()
        else:
            self._visible(False)
            self.abnomal_name = ''
            self.ani_symptomxai_area.setStartValue(self.height())
            self.ani_symptomxai_area.setEndValue(0)
            self.ani_symptomxai_area.start()


class SymptomArea(QWidget):
    def __init__(self, parent):
        super(SymptomArea, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubArea')

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layer = QVBoxLayout(self)
        layer.setContentsMargins(2, 2, 2, 2)
        layer.setSpacing(5)

        label1 = QLabel('Symptom Check')
        label1.setFixedHeight(30)

        label2 = QLabel('Symptom Check2')
        label1.setFixedHeight(30)

        # --------------------------------------------------------------------------------------------------------------
        layer.addWidget(label1)
        layer.addWidget(label2)

        # layer.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.Expanding))

        self.setLayout(layer)


# ----------------------------------------------------------------------------------------------------------------------


class NonProcedureArea(QWidget):
    def __init__(self, parent):
        super(NonProcedureArea, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubArea')
        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        self.Vlayout = QVBoxLayout(self)
        self.Vlayout.setContentsMargins(5, 5, 5, 5)
        self.Vlayout.setSpacing(0)

        self.non_procedure_label = QLabel('기능 복구 조치 Area')
        self.non_procedure_label.setMinimumHeight(30)
        # --------------------------------------------------------------------------------------------------------------
        self.Vlayout.addWidget(self.non_procedure_label)
        self.setLayout(self.Vlayout)

        self.fold_time = 200
        self.ani_non_procedure_area = QPropertyAnimation(self, b'minimumHeight')
        self.ani_non_procedure_area.setDuration(self.fold_time)

        self._visible(False)
        self.cond_visible = False


    def _visible(self, trig):
        self.non_procedure_label.setVisible(trig)
        if trig:
            self.Vlayout.setContentsMargins(5, 5, 5, 5)
        else:
            self.Vlayout.setContentsMargins(0, 0, 0, 0)
        self.cond_visible = trig

    def open_area(self, cond):
        if cond:
            self._visible(True)
            self.ani_non_procedure_area.setStartValue(self.height())
            self.ani_non_procedure_area.setEndValue(458)
            self.ani_non_procedure_area.start()
        else:
            self._visible(False)
            self.ani_non_procedure_area.setStartValue(self.height())
            self.ani_non_procedure_area.setEndValue(0)
            self.ani_non_procedure_area.start()