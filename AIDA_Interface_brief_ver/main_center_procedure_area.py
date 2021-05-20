import os
import sys
import pandas as pd
from datetime import datetime
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from collections import deque
import json

# from AIDA_Interface_brief_ver.main_center_precedure_area_symptom import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainCenterProcedureArea(QWidget):
    """ 가운데 절차서 진단 디스플레이 위젯 """

    def __init__(self, parent=None, mem=None):
        super(MainCenterProcedureArea, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubW')
        # self.setMaximumWidth(int(self.parentWidget().width() / 5) * 2)  # 1/3 부분을 차지

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # 2. 증상 및 XAI Area
        self.Symptomxai_area = SymptomXAIArea(self, self.mem)

        # 3. 절차서 x 일때 조치 Area
        self.non_procedure_area = NonProcedureArea(self)

        # 1. 절차서 Table
        procedure_label = QLabel('절차서 Area')
        procedure_label.setMinimumHeight(30)
        procedure_area = ProcedureArea(self, self.Symptomxai_area, self.non_procedure_area, self.mem)

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
    def __init__(self, parent, symxai, nonpro, mem):
        super(ProcedureArea, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubArea')

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.procedure_table = ProcedureTable(self, symxai, nonpro, self.mem)

        # --------------------------------------------------------------------------------------------------------------

        layout.addWidget(self.procedure_table)
        self.setLayout(layout)


class ProcedureTable(QTableWidget):
    def __init__(self, parent, symxai, nonpro, mem):
        super(ProcedureTable, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('ProcedureTable')

        # SymXai과 Nonpro 위젯 메모리 주소 받기
        self.symxai, self.nonpro = symxai, nonpro

        # 테이블 프레임 모양 정의
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기

        # 테이블 셋업
        col_info = [('비정상 절차서 명', 500), ('AI확신도', 100), ('진입 조건 확인', 100), ('긴급', 0)]

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

        if self.mem != None:
            timer1 = QTimer(self)
            timer1.setInterval(1000)
            timer1.timeout.connect(self._update_procedure)
            timer1.start()

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
        item1 = ProcedureNameCell(self, name, row, self.symxai, self.nonpro)
        item2 = ProcedureAIProbCell(self, name, ai_prob, row, self.symxai, self.nonpro)
        item3 = ProcedureInfoCell(self, if_prob, row, self.symxai, self.nonpro)
        item4 = ProcedureInfoCell(self, em, row, self.symxai, self.nonpro)
        self.setCellWidget(row, 0, item1)
        self.setCellWidget(row, 1, item2)
        self.setCellWidget(row, 2, item3)
        self.setCellWidget(row, 3, item4)

    def update_procedure(self):
        self.add_procedure(0, '비정상_00', 50, '12/12', 'Y')
        self.add_procedure(1, '비정상_02', 30, '2/4', 'N')
        self.add_procedure(2, '비정상_03', 20, '0/5', 'N')

    def _update_procedure(self):
        ab_dig_result = self.mem.get_logic('Ab_Dig_Result')
        if not ab_dig_result == {}:
            self.add_procedure(0, ab_dig_result[0]['N'], ab_dig_result[0]['P'], '12/12', 'Y')
            self.add_procedure(1, ab_dig_result[1]['N'], ab_dig_result[1]['P'], '2/4', 'Y')
            self.add_procedure(2, ab_dig_result[2]['N'], ab_dig_result[2]['P'], '0/5', 'Y')

    def contextMenuEvent(self, event) -> None:
        """ ProcedureTable 에 기능 올리기  """
        menu = QMenu(self)
        add_procedure = menu.addAction("Add procedure")
        update_procedure = menu.addAction("Update procedure")
        get_net = menu.addAction("Get_pronet")

        add_procedure.triggered.connect(lambda a: self.add_procedure(0, '비정상_00', 95, '10/12', 'Y'))
        update_procedure.triggered.connect(lambda a: self.add_procedure(0, '비정상_01', 80, '10/12', 'Y'))
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
    def __init__(self, parent, row, symxai, nonpro):
        super(ProcedureBaseCell, self).__init__(parent=parent)
        # SymXai과 Nonpro 위젯 메모리 주소 받기
        self.symxai, self.nonpro = symxai, nonpro

        self.procedure_name = ''
        self.row = row

    def mousePressEvent(self, e) -> None:
        if self.nonpro.cond_visible:
            self.nonpro.open_area(cond=False)
        else:
            self.symxai.open_area(cond=True, abnomal_name=self.procedure_name, row=self.row)


class ProcedureBaseWidget(QWidget):
    """ 셀 Widget 공통 """
    def __init__(self, parent, row, symxai, nonpro):
        super(ProcedureBaseWidget, self).__init__(parent=parent)
        # SymXai과 Nonpro 위젯 메모리 주소 받기
        self.symxai, self.nonpro = symxai, nonpro

        self.procedure_name = ''
        self.row = row

    def mousePressEvent(self, e) -> None:
        if self.nonpro.cond_visible:
            self.nonpro.open_area(cond=False)
        else:
            self.symxai.open_area(cond=True, abnomal_name=self.procedure_name, row=self.row)


class ProcedureNameCell(ProcedureBaseCell):
    """ 절차서 명 Cell """
    def __init__(self, parent, name, row, symxai, nonpro):
        super(ProcedureNameCell, self).__init__(parent, row, symxai, nonpro)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('ProcedureItemInfo')
        self.isempty = False

        self.procedure_name = name
        self.row = row

        self.setText(name)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 가운데 정렬


class ProcedureAIProbCell(ProcedureBaseWidget):
    """ AI 확신도 """
    def __init__(self, parent, name, aiprob, row, symxai, nonpro):
        super(ProcedureAIProbCell, self).__init__(parent, row, symxai, nonpro)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속

        self.isempty = False

        self.procedure_name = name
        self.row = row

        layer = QHBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)
        layer.setSpacing(5)

        prg_bar = QProgressBar()
        prg_bar.setObjectName('ProcedureItemProgress')
        prg_bar.setValue(aiprob)
        prg_bar.setTextVisible(False)

        prg_label = QLabel()
        prg_label.setObjectName('ProcedureItemProgressLabel')
        prg_label.setFixedWidth(45)
        prg_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)  # 텍스트 가운데 정렬
        prg_label.setText(f'{aiprob}%')

        layer.addWidget(prg_bar)
        layer.addWidget(prg_label)

        self.setLayout(layer)


class ProcedureInfoCell(ProcedureBaseCell):
    """ 절차서 Info Cell """
    def __init__(self, parent, name, row, symxai, nonpro):
        super(ProcedureInfoCell, self).__init__(parent, row, symxai, nonpro)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('ProcedureItemInfo')
        self.isempty = False

        self.procedure_name = name
        self.row = row

        self.setText(name)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 가운데 정렬


# ----------------------------------------------------------------------------------------------------------------------


class SymptomXAIArea(QWidget):
    def __init__(self, parent, mem):
        super(SymptomXAIArea, self).__init__(parent=parent)
        self.mem = mem
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
        self.Hlayout.setSpacing(2)

        self.Symptom_area = SymptomArea(self, self.mem)
        self.XAI_area = XAIArea(self, self.mem)
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
        self.row = 0

    def _visible(self, trig, get_info=['경보', '비정상']):
        self.Symptom_area.setVisible(trig)
        if get_info[0] == '경보':
            self.XAI_area.setVisible(False)
        else:
            self.XAI_area.setVisible(trig)
        self.Abnormal_procedure_name.setVisible(trig)

        if trig:
            self.Vlayout.setContentsMargins(5, 5, 5, 5)
        else:
            self.Vlayout.setContentsMargins(0, 0, 0, 0)
        self.cond_visible = trig

    def open_area(self, cond, abnomal_name='', row=0):
        get_info = abnomal_name.split('_')      # 경보 비정상 나누는 기준

        if cond == True and abnomal_name == self.abnomal_name:
            cond = False

        if cond:
            self._visible(True, get_info)
            self.Abnormal_procedure_name.setText(f'{abnomal_name}')
            self.abnomal_name = abnomal_name
            self.row = row
            self.Symptom_area.abnormal_name = self.abnomal_name
            self.Symptom_area.selected_row = self.row
            self.XAI_area.xai_table.selected_procedure_nub = self.row

            # self.ani_symptomxai_area.setStartValue(self.height())
            self.ani_symptomxai_area.setStartValue(self.height())
            self.ani_symptomxai_area.setEndValue(558)
            self.ani_symptomxai_area.start()
        else:
            self._visible(False, get_info)
            self.abnomal_name = ''
            self.row = row
            self.Symptom_area.abnormal_name = self.abnomal_name
            self.Symptom_area.selected_row = self.row
            self.XAI_area.xai_table.selected_procedure_nub = self.row

            self.ani_symptomxai_area.setStartValue(self.height())
            self.ani_symptomxai_area.setEndValue(0)
            self.ani_symptomxai_area.start()


class SymptomArea(QWidget):
    def __init__(self, parent, mem):
        super(SymptomArea, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubArea')
        self.mem = mem
        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layer = QVBoxLayout(self)
        layer.setContentsMargins(2, 2, 2, 2)
        layer.setSpacing(5)

        label0 = QLabel('Symptom Check')
        label0.setFixedHeight(30)

        self.label1 = QLabel('경보 및 증상 Check')
        self.label1.setFixedHeight(30)

        label2 = QLabel('자동동작사항 Check')
        label2.setFixedHeight(30)

        # --------------------------------------------------------------------------------------------------------------
        layer.addWidget(label0)
        self.sym_layer = QVBoxLayout()
        self.sym_dict = {
            i: SymptomWidget(self, txt='', cond=False) for i in range(10)
        }
        [self.sym_layer.addWidget(self.sym_dict[i]) for i in self.sym_dict.keys()]

        layer.addLayout(self.sym_layer)
        layer.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.Expanding))

        self.setLayout(layer)

        self.abnormal_name = ''
        self.selected_row = 0

        # TODO CNS 업데이트 모듈 만들어야함.

        timer1 = QTimer(self)
        timer1.setInterval(1000)
        timer1.timeout.connect(self._update)
        timer1.start()

    def _update(self):
        # self.sym_layer.removeWidget()
        local_mem = self.mem.get_shmem_db()
        self._clear_txt_cond()

        # json파일 로드
        with open('./Procedure/procedure.json', 'rb') as f:
            json_data = json.load(f)

        if self.abnormal_name == 'Normal: 정상':
            # 절차 입력
            self.sym_dict[0].update_text('압력 만족')
            self.sym_dict[1].update_text('압력 만족')
            self.sym_dict[2].update_text('압력 만족')
            self.sym_dict[3].update_text('압력 만족')
            self.sym_dict[4].update_text('압력 만족')
            self.sym_dict[5].update_text('압력 만족')

            # 절차 만족 로직
            if local_mem['PPRZ']['Val'] > 15311339.0:
                self.sym_dict[0].update_condition(True)

        if self.abnormal_name == 'Ab63_02: 제어봉의 계속적인 삽입':
            self.sym_dict[0].update_text('제어봉 위치 지시계와 스텝계수기상의 계속적인 제어봉 삽입')
            self.sym_dict[1].update_text('원자로 출력 감소')
            self.sym_dict[2].update_text('“T REF/AUCT T AVG HIGH” 경보 발생')
            self.sym_dict[3].update_text('"ROD BANKS LOW/LO-LO LIMIT” 경보 발생')
            self.sym_dict[4].update_text('가압기 보조전열기 켜짐')
            self.sym_dict[5].update_text('가압기 보조전열기 켜짐')


            # print(local_mem['KBCDO7']['List'])
            # print(local_mem['KBCDO7']['Val'])

            # 초당으로 비교하면 깜빡거림 발생=>9초 전이랑 비교
            if local_mem['KBCDO7']['List'][-1] < local_mem['KBCDO7']['List'][-9]:  #KBCDO7 : D bank (Mal_type : 4)
               self.sym_dict[0].update_condition(True)
            if local_mem['ZINST124']['List'][-1] < local_mem['ZINST124']['List'][-9]:
                self.sym_dict[1].update_condition(True)
            if local_mem['KLAMPO313']['Val'] == 1:
                self.sym_dict[2].update_condition(True)
            if local_mem['KLAMPO254']['Val'] == 1:
                self.sym_dict[3].update_condition(True)
            if local_mem['QPRZB']['Val'] > 0:
                self.sym_dict[4].update_condition(True)
            if local_mem['WCHGNO']['Val'] > 0:
                self.sym_dict[5].update_condition(True)

        if self.abnormal_name == 'Ab19_02: 가압기 안전밸브 고장':
            #json파일 이용 절차 입력
            self.sym_dict[0].update_text(json_data[self.abnormal_name]["0"]["절차"])
            self.sym_dict[1].update_text(json_data[self.abnormal_name]["1"]["절차"])
            self.sym_dict[2].update_text(json_data[self.abnormal_name]["2"]["절차"])
            self.sym_dict[3].update_text(json_data[self.abnormal_name]["3"]["절차"])
            self.sym_dict[4].update_text(json_data[self.abnormal_name]["4"]["절차"])
            self.sym_dict[5].update_text(json_data[self.abnormal_name]["5"]["절차"])
            self.sym_dict[6].update_text(json_data[self.abnormal_name]["6"]["절차"])
            self.sym_dict[7].update_text(json_data[self.abnormal_name]["7"]["절차"])
            self.sym_dict[8].update_text(json_data[self.abnormal_name]["8"]["절차"])
            print(local_mem['WNETCH']['List'])
            print(local_mem['ZVCT']['List'])
            print(local_mem['ZINST63']['List'])

            if local_mem['KLAMPO312']['Val'] == 1:
                self.sym_dict[0].update_condition(True)
            if local_mem['KLAMPO308']['Val'] == 1:
                self.sym_dict[1].update_condition(True)
            if local_mem['KLAMPO317']['Val'] == 1:
                self.sym_dict[2].update_condition(True)
            if local_mem['ZINST63']['List'][-1] != local_mem['ZINST63']['List'][-5]:
                self.sym_dict[3].update_condition(True)
            if local_mem['WNETCH']['List'][-1] > local_mem['WCHGNO']['List'][-9]:
                self.sym_dict[4].update_condition(True)
            if local_mem['ZVCT']['List'][-1] < local_mem['ZVCT']['List'][-9]:
                self.sym_dict[5].update_condition(True)
            if local_mem['QPRZB']['Val'] > 0:
                self.sym_dict[6].update_condition(True)
            if local_mem['BHV6']['Val'] == 0:
                self.sym_dict[7].update_condition(True)
            if local_mem['KLAMPO9']['Val'] == 1:
                self.sym_dict[8].update_condition(True)
    def _clear_txt_cond(self):
        for key in self.sym_dict.keys():
            self.sym_dict[key].update_condition(False)
            self.sym_dict[key].update_text('')


class SymptomWidget(QWidget):
    def __init__(self, parent, txt, cond=False):
        super(SymptomWidget, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SymptomW')

        self.curent_cond = cond

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layer = QHBoxLayout(self)

        layer.setContentsMargins(2, 2, 2, 2)
        layer.setSpacing(5)

        self.txt_label = QLabel(txt)
        self.txt_dis = SymptomDisLabel(self, cond)

        # --------------------------------------------------------------------------------------------------------------
        layer.addWidget(self.txt_dis)
        layer.addWidget(self.txt_label)
        self.setLayout(layer)

    def update_condition(self, cond: bool):
        self.curent_cond = self.txt_dis.update_condition(cond)

    def update_text(self, txt: str):
        self.txt_label.setText(txt)


class SymptomDisLabel(QLabel):
    def __init__(self, parent, cond=False):
        super(SymptomDisLabel, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SymptomDisLabel')

        self.setFixedWidth(15)
        self.setFixedHeight(15)

        self.curent_cond = cond
        self.update_condition(self.curent_cond)

    def update_condition(self, condition: bool):
        cond = 'True' if condition else 'False'
        self.curent_cond = condition
        self.setProperty("Condition", cond)
        self.style().polish(self)
        return self.curent_cond

    # def mousePressEvent(self, e) -> None:
    #     self.update_condition(True)


class XAIArea(QWidget):
    def __init__(self, parent, mem):
        super(XAIArea, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubArea')

        self.setMaximumWidth(450)

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layer = QVBoxLayout(self)
        layer.setContentsMargins(0, 0, 0, 0)
        layer.setSpacing(0)

        self.xai_table = XAITable(self, self.mem)

        # --------------------------------------------------------------------------------------------------------------
        layer.addWidget(self.xai_table)
        self.setLayout(layer)


class XAITable(QTableWidget):
    def __init__(self, parent, mem):
        super(XAITable, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('ProcedureTable')             # ProcedureTable 와 동일

        # self.setMaximumWidth(self.parent().width())

        # 테이블 프레임 모양 정의
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기

        # 테이블 셋업
        col_info = [('변수 명', 350), ('가중치', 0)]

        self.setColumnCount(len(col_info))

        col_names = []
        for i, (l, w) in enumerate(col_info):
            self.setColumnWidth(i, w)
            col_names.append(l)

        self.max_cell = 5

        for i in range(0, self.max_cell):
            self.add_empty_procedure(i)

        # shap val 아이템 저장
        self.shap_val_dict = {i: self.add_value(i, '', 0) for i in range(self.max_cell)}

        cell_height = self.rowHeight(0)
        total_height = self.horizontalHeader().height() + cell_height * self.max_cell + 4  # TODO 4 매번 계산.

        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(cell_height / 3)

        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().setStretchLastSection(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.selected_procedure_nub = 0

        if self.mem != None:
            timer1 = QTimer(self)
            timer1.setInterval(1000)
            timer1.timeout.connect(self._update_XAI)
            timer1.start()

    def add_empty_procedure(self, i):
        self.insertRow(i)
        [self.setCellWidget(i, _, ProcedureEmptyCell(self)) for _ in range(0, 2)]

    def add_value(self, row, name, weight):
        """
        테이블에 진단 결과 정보 저장하기

        :param name:
        :param ai_prob:
        :param if_prob:
        :param em:
        :return:
        """
        XaiInfo = XAITableInfoCell(self, name)
        XaiProb = XAITableProbCell(self, name, weight)
        self.setCellWidget(row, 0, XaiInfo)
        self.setCellWidget(row, 1, XaiProb)
        return {'info': XaiInfo, 'prob': XaiProb}

    def contextMenuEvent(self, event) -> None:
        """ XAITable 에 기능 올리기  """
        menu = QMenu(self)
        add_value = menu.addAction("Add procedure")
        add_value.triggered.connect(self._update_XAI)
        menu.exec_(event.globalPos())

    def _update_XAI(self):
        shap_result = self.mem.get_logic('Ab_Xai_Result')
        if not shap_result == {}:
            selected_procedure = self.selected_procedure_nub
            for i in range(self.max_cell):
                shap_val = shap_result[selected_procedure][f'SHAP_VAL{i}']
                shap_val_name = shap_result[selected_procedure][f'SHAP_NAME{i}']
                shap_val_desc = shap_result[selected_procedure][f'SHAP_DESC{i}']
                self.shap_val_dict[i]['info'].update_(shap_val_desc)
                self.shap_val_dict[i]['prob'].update_(shap_val_name, shap_val)

    def _test(self):
        self.add_value(0, 'PZR압력', 95)
        self.add_value(1, 'PZR수위', 50)
        self.add_value(2, 'RCSAvgTemp', 20)
        self.add_value(3, 'RCSLoop1Temp', 10)
        self.add_value(4, 'RCSLoop2Temp', 5)


class XAITableEmptyCell(QLabel):
    """ 공백 Cell """
    def __init__(self, parent):
        super(XAITableEmptyCell, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True) # 상위 스타일 상속
        self.setObjectName('ProcedureItemEmpty')
        self.isempty = True


class XAITableProbCell(QWidget):
    """ 변수 가중치 """
    def __init__(self, parent, para_name, weight):
        super(XAITableProbCell, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속

        self.isempty = False
        self.para_name = para_name

        layer = QHBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)
        layer.setSpacing(0)

        self.prg_bar = QProgressBar()
        self.prg_bar.setMaximumWidth(30)
        self.prg_bar.setObjectName('ProcedureItemProgress')
        self.prg_bar.setValue(weight)
        self.prg_bar.setTextVisible(False)

        self.prg_label = QLabel()
        self.prg_label.setObjectName('ProcedureItemProgressLabel')
        self.prg_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)  # 텍스트 가운데 정렬
        self.prg_label.setText(f'{weight}%')

        layer.addWidget(self.prg_bar)
        layer.addWidget(self.prg_label)

        self.setLayout(layer)

    def update_(self, name, weight):
        self.para_name = name
        self.prg_bar.setValue(int(weight))
        self.prg_label.setText(f'{weight}%')


class XAITableInfoCell(QLabel):
    """ 절차서 Info Cell """
    def __init__(self, parent, para_name):
        super(XAITableInfoCell, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('ProcedureItemInfo')
        self.isempty = False

        self.para_name = para_name
        self.setText(para_name)

        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 가운데 정렬

    def update_(self, name):
        self.para_name = name
        self.setText(name)


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
            self.ani_non_procedure_area.setEndValue(558)
            self.ani_non_procedure_area.start()
        else:
            self._visible(False)
            self.ani_non_procedure_area.setStartValue(self.height())
            self.ani_non_procedure_area.setEndValue(0)
            self.ani_non_procedure_area.start()