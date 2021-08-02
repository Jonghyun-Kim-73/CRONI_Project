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
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
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
        get_info = abnomal_name.split('_')  # 경보 비정상 나누는 기준

        if cond == True and abnomal_name == self.abnomal_name:
            cond = False

        if cond:
            self._visible(True, get_info)
            self.Abnormal_procedure_name.setText(f'{abnomal_name}')
            self.abnomal_name = abnomal_name
            self.row = row
            if get_info[0] == '경보':
                self.Symptom_area.abnormal_name = get_info[1]
                # 경보_Intermediate range high flux rod stop 중 뒤에 부분을 넘겨줌.
            else:
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
            if get_info[0] == '경보':
                self.Symptom_area.abnormal_name = get_info[1]
                # 경보_Intermediate range high flux rod stop 중 뒤에 부분을 넘겨줌.
            else:
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
        with open('../../AIDA_Interface_brief_ver/Procedure/procedure.json', 'rb') as f:
            json_data = json.load(f)
        # self.abnormal_name는
        # 경보 -> Intermediate range high flux rod stop
        # 비정상 -> Ab15_08: 증기발생기 수위 채널 고장 '고' 를 가지고 있다.
        if self.abnormal_name == '':
            pass
        else:
            # 1. json 절차서 db 에서 self.abnormal_name 과 유사한 절차서 명이 있는지 탐색한다.
            get_procedure_name_in_json = ''  # json 파일에서 절차서 명 가져오기
            for json_in_procedure_name in json_data.keys():  # 순회하면서 self.abnormal_name 과 비교
                if self.abnormal_name in json_in_procedure_name:
                    get_procedure_name_in_json = json_in_procedure_name  # 최종 선택
            # 2. 만약 유사한 절차서 명이 있다면 json 절차서 db 에서 해당 절차서의 전체 길이를 확인한다.
            if get_procedure_name_in_json != '':
                # TODO 만약에 Json 파일에 절차서 명과 이미 등록된 절차서 명이 다르면 오류 발생함.
                try:
                    for i in range(len(json_data[get_procedure_name_in_json])):
                        if i < len(self.sym_dict):
                            self.sym_dict[i].update_text(json_data[get_procedure_name_in_json][f"{i}"]["절차"])
                except Exception as e:
                    print('절차서 명 에러 부분 TODO 확인...', e)
            # ----------------------------------------------------------------------------------------------------------
            # 경보
            if get_procedure_name_in_json == 'L1 경보(11) Intermediate range high flux rod stop': pass
            if get_procedure_name_in_json == 'L2 경보(11) Power range overpower rod stop':
                if local_mem['KBCDO7']['List'][-1] <= local_mem['KBCDO7']['List'][-2]:
                    self.sym_dict[0].update_condition(True)
                if local_mem['KLAMPO9']['Val'][-1] == 1:
                    self.sym_dict[1].update_condition(True)
                if local_mem['ZINST1']['Val'][-1] >= 103:
                    self.sym_dict[2].update_condition(True)

            if get_procedure_name_in_json == 'L4 경보(11) Control bank lo-lo limit': pass
            if get_procedure_name_in_json == 'L5 경보(11) Two or more rod at bottom': pass
            if get_procedure_name_in_json == 'L7 경보(03) CCWS outlet temp hi (49.0 deg C)': pass
            if get_procedure_name_in_json == 'L8 경보(01) Instrument air press lo (6.3 kg/cm2)': pass
            if get_procedure_name_in_json == 'L9 경보(06) RWST level lo-lo (5%)': pass
            if get_procedure_name_in_json == 'L11 경보(06) L/D HX outlet temp hi(58 deg C)': pass
            if get_procedure_name_in_json == 'L12 경보(06) RHX L/D outlet temp hi(202 deg C)': pass
            if get_procedure_name_in_json == 'L13 경보(06) VCT level lo(20 %) or VCT level hi(80 %)': pass
            if get_procedure_name_in_json == 'L14 경보(06) VCT press lo(0.7 kg/cm2) or VCT press hi (4.5 kg/cm2)': pass
            if get_procedure_name_in_json == 'L15 경보(06) RCP seal inj wtr flow lo(1.4 m3/hr)': pass
            if get_procedure_name_in_json == 'L19 경보(05) PRZ press lo SI': pass
            if get_procedure_name_in_json == 'L23 경보(05) CTMT phase B iso actuated': pass
            if get_procedure_name_in_json == 'L46 경보(02) CTMT sump level hi or CTMT sump level hi-hi': pass
            if get_procedure_name_in_json == 'L48 경보(26) CTMT air temp hi(48.89 deg C)': pass
            if get_procedure_name_in_json == 'L47 경보(26) CTMT moisture hi(70% of R.H.)': pass
            # -----------------------------------------------------------------------------------------------------------
            # Right 경보
            if get_procedure_name_in_json == 'R1 경보(01) Rad hi alarm': pass
            if get_procedure_name_in_json == 'R2 경보(03) CTMT press hi 1 alert': pass
            if get_procedure_name_in_json == 'R3 경보(03) CTMT press hi 2 alert': pass
            if get_procedure_name_in_json == 'R5 경보(01) Accum. Tk press lo (43.4 kg/cm2) or Accum. Tk press hi (43.4 kg/cm2)': pass
            if get_procedure_name_in_json == 'R7 경보(09) PRZ press hi alert(162.4 kg/cm2)': pass

            if get_procedure_name_in_json == 'R8 경보(09) PRZ press lo alert(153.6 kg/cm2)':
                if abs(['KBCDO23']['List'][-1] - local_mem['KBCDO23']['List'][-2]) > 1:
                    self.sym_dict[0].update_condition(True)
                if local_mem['WFWLN1']['Val'] >= 350 or local_mem['WFWLN2']['Val'] >= 350 or local_mem['WFWLN3']['Val'] >= 350: #저출력 70%(가정) 급수 유량 normal: 약 315
                    self.sym_dict[1].update_condition(True)
                if local_mem['ZINST101']['Val'] >= 65:      #저출력 70%(가정) main steam flow normal: 59.4
                    self.sym_dict[2].update_condition(True)
                if local_mem['BPORV']['Val'] > 0:
                    self.sym_dict[3].update_condition(True)
                if local_mem['BPRZSP']['Val'] > 0:          #비정상적인 개방?
                    self.sym_dict[4].update_condition(True)
                if local_mem['BPRZSP']['Val'] == 0 and local_mem['QPRZB']['Val'] > 0:
                    self.sym_dict[5].update_condition(True)
                if local_mem['BPORV']['Val'] == 0:
                    self.sym_dict[6].update_condition(True)
                if local_mem['BPRZSP']['Val'] == 0 and local_mem['QPRZB']['Val'] > 0:
                    self.sym_dict[7].update_condition(True)

            if get_procedure_name_in_json == 'R9 경보(09) PRZ PORV opening(164.2 kg/cm2)':
                if local_mem['ZINST65']['Val'] >= 164.15:
                    self.sym_dict[0].update_condition(True)
                if local_mem['KBCDO22']['List'][-1] <= local_mem['KBCDO22']['List'][-2]:
                    self.sym_dict[1].update_condition(True)
                if local_mem['BPORV']['Val'] > 0 and local_mem['ZINST65']['List'][-1] < local_mem['ZINST65']['List'][
                    -2]:
                    self.sym_dict[2].update_condition(True)
                if local_mem['ZPRTL']['List'][-1] > local_mem['ZPRTL']['List'][-2] and local_mem['ZINST48']['List'][
                    -1] > local_mem['ZINST48']['List'][-2] and local_mem['UPRT']['List'][-1] > \
                        local_mem['UPRT']['List'][-2]:
                    self.sym_dict[3].update_condition(True)

            if get_procedure_name_in_json == 'R10 경보(10) PRZ cont level hi heater on(over 5%)':
                if local_mem['KBCDO22']['List'][-1] <= local_mem['KBCDO22']['List'][-2]:
                    self.sym_dict[0].update_condition(True)
                if local_mem['ZINST63']['Val'] >= local_mem['ZINST57']['Val'] + 5:  #ZINST57: PRZ LEVEL SETPOINT
                    self.sym_dict[1].update_condition(True)                         #OVER 5%
                if local_mem['QPRZB']['Val'] > 0:
                    self.sym_dict[2].update_condition(True)
            if get_procedure_name_in_json == 'R11 경보(09) PRZ cont level lo heater off(17%)': pass
            if get_procedure_name_in_json == 'R12 경보(09) PRZ press lo back-up heater on(153.6 kg/cm2)':
                if abs(['KBCDO23']['List'][-1] - local_mem['KBCDO23']['List'][-2]) > 1:
                    self.sym_dict[0].update_condition(True)
                if local_mem['BPRZSP']['Val'] > 0 and local_mem['QPRZP']['Val'] == 0:
                    self.sym_dict[1].update_condition(True)
                # if local_mem['WFWLN1']['Val'] > 0:
                #     self.sym_dict[2].update_condition(True) 과도한 급수공급 증기사용
                if local_mem['BHV40']['Val'] > 0:
                    self.sym_dict[3].update_condition(True)
                if local_mem['QPRZB']['Val'] > 0:
                    self.sym_dict[4].update_condition(True)

            if get_procedure_name_in_json == 'R13 경보(08) Tref/Auct. Tavg Deviation(1.67 deg C)':
                if local_mem['UAVLEGS']['List'][-1] > local_mem['UAVLEGS']['List'][-2]:
                    self.sym_dict[4].update_condition(True)
                if local_mem['KBCDO22']['List'][-1] > local_mem['KBCDO22']['List'][-2]:
                    self.sym_dict[4].update_condition(True)
                if local_mem['UAVLEGM']['List'][-1] < local_mem['UAVLEGM']['List'][-2]:
                    self.sym_dict[4].update_condition(True)
                if local_mem['KLAMPO28']['Val'] == 1 and local_mem['KBCDO7']['List'][-1] > local_mem['KBCDO7']['List'][-2]:
                    self.sym_dict[4].update_condition(True)
                if local_mem['ZINST65']['List'][-1] > local_mem['ZINST65']['List'][-2] and local_mem['ZINST63']['List'][-1] > local_mem['ZINST63']['List'][-2]:
                    self.sym_dict[4].update_condition(True)

            if get_procedure_name_in_json == 'R14 경보(08) RCS 1,2,3 Tavg hi(312.78 deg C)':
                if local_mem['KBCDO22']['List'][-1] < local_mem['KBCDO22']['List'][-2]:
                    self.sym_dict[0].update_condition(True)
                if local_mem['KBCDO7']['List'][-1] > local_mem['KBCDO7']['List'][-2] or local_mem['KBCDO16']['List'][-1] < local_mem['KBCDO16']['List'][-2]:
                    self.sym_dict[1].update_condition(True)
                if local_mem['KBCDO7']['List'][-1] < local_mem['KBCDO7']['List'][-2]:
                    self.sym_dict[2].update_condition(True)

            if get_procedure_name_in_json == 'R15 경보(08) RCS 1,2,3 Tavg/auct Tavg hi/lo(1.1 deg C)': pass
            if get_procedure_name_in_json == 'R16 경보(08) RCS 1,2,3 lo flow alert(92%)': pass
            if get_procedure_name_in_json == 'R18 경보(09) PRT press hi( 0.6kg/cm2)':
                if local_mem['BPORV']['Val'] > 0:
                    self.sym_dict[0].update_condition(True)
                if local_mem['BPSV10']['Val'] > 0:
                    self.sym_dict[0].update_condition(True)
                if local_mem['ZPRTL']['List'][-1] > local_mem['ZPRTL']['List'][-2]:
                    self.sym_dict[0].update_condition(True)

            if get_procedure_name_in_json == 'R19 경보(12) SG 1,2,3 level lo(25% of span)':
                if local_mem['BFV478'] == 0:
                    self.sym_dict[2].update_condition(True)
            if get_procedure_name_in_json == 'R20 경보(12) SG 1,2,3 stm/FW flow deviation(10% of loop flow)': pass
            if get_procedure_name_in_json == 'R22 경보(14) Condensate stor Tk level lo or Condensate stor Tk level lo-lo or Condensate stor Tk level hi': pass
            if get_procedure_name_in_json == 'R25 경보(03) MSIV tripped': pass
            if get_procedure_name_in_json == 'R27 경보(12) MSL press rate hi steam iso': pass
            if get_procedure_name_in_json == 'R28 경보(12) MSL 1,2,3 press low(41.1 kg/cm*2 = 0.403E7 pas)': pass
            if get_procedure_name_in_json == 'R29 경보(03) AFW(MD) actuated': pass
            if get_procedure_name_in_json == 'R33 경보(15) FW temp hi(231.1 deg C)': pass
            if get_procedure_name_in_json == 'R34 경보(16) Condensate pump flow lo(1400 gpm=88.324 kg/s)': pass
            if get_procedure_name_in_json == 'R35 경보(16) Condenser abs press hi(633. mmmHg)': pass
            if get_procedure_name_in_json == 'R37 경보(15) TBN trip P-4': pass
            if get_procedure_name_in_json == 'R38 경보(15) SG 1,2,3 wtr level hi-hi TBN trip': pass
            if get_procedure_name_in_json == 'R39 경보(15) Condenser vacuum lo TBN trip': pass
            if get_procedure_name_in_json == 'R40 경보(15) TBN overspeed hi TBN trip': pass

            # ----------------------------------------------------------------------------------------------------------
            # 비정상
            if get_procedure_name_in_json == 'Ab63_04: 제어봉 낙하':
                if local_mem['KLAMPO15']['Val'] == 1:
                    self.sym_dict[0].update_condition(True)
                if local_mem['KBCDO23']['List'][-1] < local_mem['KBCDO23']['List'][-2]:
                    self.sym_dict[1].update_condition(True)
                if local_mem['UAVLEGM']['List'][-1] < local_mem['UAVLEGM']['List'][-2]:
                    self.sym_dict[2].update_condition(True)
                if local_mem['KLAMPO313']['Val'] == 1:
                    self.sym_dict[3].update_condition(True)
                if local_mem['KLAMPO255']['Val'] == 1:
                    self.sym_dict[4].update_condition(True)
                if local_mem['KBCDO23']['List'][-1] < local_mem['KBCDO23']['List'][-2]:
                    self.sym_dict[5].update_condition(True)
                if local_mem['KBCDO22']['List'][-1] < local_mem['KBCDO22']['List'][-2]:
                    self.sym_dict[6].update_condition(True)

            if get_procedure_name_in_json == 'Ab63_02: 제어봉의 계속적인 삽입':
                if local_mem['KBCDO7']['List'][-1] < local_mem['KBCDO7']['List'][-2]:  # KBCDO7 : D bank (Mal_type : 4)
                    self.sym_dict[0].update_condition(True)
                if local_mem['ZINST124']['List'][-1] < local_mem['ZINST124']['List'][-2]:
                    self.sym_dict[1].update_condition(True)
                if local_mem['KLAMPO313']['Val'] == 1:
                    self.sym_dict[2].update_condition(True)
                if local_mem['KLAMPO254']['Val'] == 1:
                    self.sym_dict[3].update_condition(True)
                if local_mem['QPRZB']['Val'] > 0:
                    self.sym_dict[4].update_condition(True)
                if local_mem['WCHGNO']['Val'] > 0:
                    self.sym_dict[5].update_condition(True)

            if get_procedure_name_in_json == 'Ab19_02: 가압기 안전밸브 고장':
                # print(local_mem['WNETCH']['List'])
                # print(local_mem['ZVCT']['List'])
                # print(local_mem['ZINST63']['List'])

                if local_mem['KLAMPO312']['Val'] == 1:
                    self.sym_dict[0].update_condition(True)
                if local_mem['KLAMPO308']['Val'] == 1:
                    self.sym_dict[1].update_condition(True)
                if local_mem['KLAMPO317']['Val'] == 1:
                    self.sym_dict[2].update_condition(True)
                if local_mem['ZINST63']['List'][-1] != local_mem['ZINST63']['List'][-2]:
                    self.sym_dict[3].update_condition(True)
                if local_mem['WNETCH']['List'][-1] > local_mem['WNETCH']['List'][-2]:
                    self.sym_dict[4].update_condition(True)
                if local_mem['ZVCT']['List'][-1] < local_mem['ZVCT']['List'][-2]:
                    self.sym_dict[5].update_condition(True)
                if local_mem['QPRZB']['Val'] > 0:
                    self.sym_dict[6].update_condition(True)
                if local_mem['BHV6']['Val'] == 0:
                    self.sym_dict[7].update_condition(True)
                if local_mem['KLAMPO9']['Val'] == 1:
                    self.sym_dict[8].update_condition(True)

            if get_procedure_name_in_json == 'Ab59_02: 충전수 유량조절밸즈 후단누설':
                if local_mem['KLAMPO266']['Val'] == 1 or local_mem['KLAMPO274']['Val'] == 1:
                    self.sym_dict[0].update_condition(True)
                if local_mem['KLAMPO271']['Val'] == 1 or local_mem['KLAMPO263']['Val'] == 1:
                    self.sym_dict[1].update_condition(True)
                if local_mem['KLAMPO261']['Val'] == 1:
                    self.sym_dict[2].update_condition(True)
                if local_mem['WNETCH']['List'][-1] > local_mem['WNETCH']['List'][-2]:
                    self.sym_dict[3].update_condition(True)
                if local_mem['ZINST63']['List'][-1] < local_mem['ZINST63']['List'][-2]:
                    self.sym_dict[4].update_condition(True)
                if local_mem['ZVCT']['List'][-1] < local_mem['ZVCT']['List'][-2]:
                    self.sym_dict[5].update_condition(True)
                if local_mem['ZINST63']['List'][-1] <= 17:
                    self.sym_dict[6].update_condition(True)
                    # 위의 절차 만족시 아래 절차 시작
                    if local_mem['QPRZH']['Val'] < 1e-10 and local_mem['QPRZB']['Val'] == 0:
                        self.sym_dict[7].update_condition(True)
                    if local_mem['BHV1']['Val'] == 0 or local_mem['BHV2']['Val'] == 0 or local_mem['BHV3']['Val'] == 0:
                        self.sym_dict[8].update_condition(True)
                    if local_mem['BLV459']['Val'] == 0:
                        self.sym_dict[9].update_condition(True)
                    if local_mem['BFV122']['Val'] == 1:
                        self.sym_dict[10].update_condition(True)
                    if local_mem['BPV145']['Val'] == 0:
                        self.sym_dict[11].update_condition(True)

            if get_procedure_name_in_json == 'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설':
                if local_mem['ZINST58']['List'][-1] < local_mem['ZINST58']['List'][-2] or local_mem['ZINST63']['List'][
                    -1] < local_mem['ZINST63']['List'][-2]:
                    self.sym_dict[0].update_condition(True)
                if local_mem['ZVCT']['List'][-1] < local_mem['ZVCT']['List'][-2]:
                    self.sym_dict[1].update_condition(True)
                if local_mem['WCHGNO']['List'][-1] > local_mem['WCHGNO']['List'][-2]:
                    self.sym_dict[2].update_condition(True)

            if get_procedure_name_in_json == 'Ab23_06: 증기발생기 전열관 누설':
                if local_mem['ZINST58']['List'][-1] < local_mem['ZINST58']['List'][-2] or local_mem['ZINST63']['List'][
                    -1] < local_mem['ZINST63']['List'][-2]:
                    self.sym_dict[0].update_condition(True)
                if local_mem['ZVCT']['List'][-1] < local_mem['ZVCT']['List'][-2]:
                    self.sym_dict[1].update_condition(True)
                if local_mem['WCHGNO']['List'][-1] > local_mem['WCHGNO']['List'][-2]:
                    self.sym_dict[2].update_condition(True)
                if local_mem['KLAMPO320']['Val'] == 1:
                    self.sym_dict[3].update_condition(True)
                if local_mem['ZINST63']['Val'] <= 17:
                    if local_mem['BHV1']['Val'] == 0 and local_mem['BHV2']['Val'] == 0 and local_mem['BHV3'][
                        'Val'] == 0 and local_mem['BLV459']['Val'] == 0:
                        self.sym_dict[4].update_condition(True)
                if local_mem['WCHGNO']['List'][-1] > local_mem['WCHGNO']['List'][-2]:
                    self.sym_dict[5].update_condition(True)
                if local_mem['BHV108']['Val'] == 0 and local_mem['BHV208']['Val'] == 0 and local_mem['BHV308'][
                    'Val'] == 0 and local_mem['BLV459']['Val'] == 0:
                    self.sym_dict[6].update_condition(True)
                if local_mem['ZINST58']['Val'] <= 136.78:
                    if local_mem['KLAMPO9']['Val'] == 1:
                        self.sym_dict[7].update_condition(True)
                if local_mem['ZINST58']['Val'] <= 126.57:
                    if local_mem['BHV22']['Val'] > 0:
                        self.sym_dict[8].update_condition(True)

            if get_procedure_name_in_json == 'Ab20_04: 가압기 수위 채널 고장 (저)':
                if local_mem['KLAMPO260']['Val'] == 1:
                    self.sym_dict[0].update_condition(True)
                if local_mem['KLAMPO274']['Val'] == 1 or local_mem['KLAMPO266']['Val'] == 1:
                    if local_mem['WNETCH']['List'][-1] > local_mem['WNETCH']['List'][-2]:
                        self.sym_dict[1].update_condition(True)
                if local_mem['ZPRZNO']['List'][-1] > local_mem['ZPRZNO']['List'][-2]:
                    self.sym_dict[2].update_condition(True)
                if local_mem['KLAMPO310']['Val'] == 1:
                    self.sym_dict[3].update_condition(True)
                if local_mem['KLAMPO280']['Val'] == 1 and local_mem['KLAMPO9']['Val'] == 1:
                    self.sym_dict[4].update_condition(True)
                if local_mem['KLAMPO311']['Val'] == 1:
                    self.sym_dict[5].update_condition(True)
                if local_mem['KLAMPO260']['Val'] == 1:
                    self.sym_dict[6].update_condition(True)
                if local_mem['KLAMPO274']['Val'] == 1:
                    self.sym_dict[7].update_condition(True)
                if local_mem['QPRZH']['Val'] < 1e-10 and local_mem['QPRZB']['Val'] == 0:
                    self.sym_dict[8].update_condition(True)
                if local_mem['BHV1']['Val'] == 0 and local_mem['BHV2']['Val'] == 0 and local_mem['BHV3']['Val'] == 0:
                    self.sym_dict[9].update_condition(True)
                if local_mem['BLV459']['Val'] == 0:
                    self.sym_dict[10].update_condition(True)
                if local_mem['ZINST63']['List'][-1] > local_mem['ZINST63']['List'][-2]:
                    if local_mem['KLAMPO9']['Val'] == 1:
                        self.sym_dict[11].update_condition(True)

            if get_procedure_name_in_json == 'Ab21_11: 가압기 살수밸브 고장 (열림)':
                if local_mem['KBHON']['Val'] == 1 and local_mem['KLAMPO118']['Val'] == 1:
                    self.sym_dict[0].update_condition(True)
                if local_mem['KLAMPO308']['Val'] == 1:
                    self.sym_dict[1].update_condition(True)
                if local_mem['BPORV']['Val'] == 0:
                    self.sym_dict[2].update_condition(True)
                if local_mem['KLAMPO216']['Val'] == 1:
                    self.sym_dict[3].update_condition(True)
                if local_mem['ZINST63']['List'][-1] > local_mem['ZINST63']['List'][-2]:
                    self.sym_dict[4].update_condition(True)
                if local_mem['KLAMPO308']['Val'] == 1 and local_mem['KLAMPO9']['Val'] == 1:
                    self.sym_dict[5].update_condition(True)
                if local_mem['KLAMPO269']['Val'] == 1:
                    self.sym_dict[6].update_condition(True)
                if local_mem['QPRZH']['Val'] > 1E-10 and local_mem['KLAMPO118']['Val'] == 1:
                    self.sym_dict[7].update_condition(True)
                if local_mem['BHV6']['Val'] == 0:
                    self.sym_dict[8].update_condition(True)
                if local_mem['KLAMPO9']['Val'] == 1:
                    self.sym_dict[9].update_condition(True)
                if local_mem['BHV22']['Val'] == 1:
                    self.sym_dict[10].update_condition(True)

            if get_procedure_name_in_json == 'Ab60_02: 재생열교환기 전단부위 파열':
                if local_mem['KLAMPO260']['Val'] == 1:
                    self.sym_dict[0].update_condition(True)
                if local_mem['ZVCT']['List'][-1] < local_mem['ZVCT']['List'][-2]:
                    self.sym_dict[1].update_condition(True)
                if local_mem['ZVCT']['Val'] <= 30:
                    if local_mem['KLAMPO86']['Val'] == 1:
                        self.sym_dict[2].update_condition(True)
                if local_mem['ZVCT']['Val'] <= 20:
                    if local_mem['KLAMPO263']['Val'] == 1:
                        self.sym_dict[3].update_condition(True)
                if local_mem['ZVCT']['Val'] <= 5:
                    if local_mem['BLV616']['Val'] == 0 and local_mem['BLV615']['Val'] == 1:
                        self.sym_dict[4].update_condition(True)
                if local_mem['KLAMPO312']['Val'] == 1:
                    self.sym_dict[5].update_condition(True)
                if local_mem['QPRZB']['Val'] == 0 and local_mem['QPRZH']['Val'] < 1E-10:
                    self.sym_dict[6].update_condition(True)
                if local_mem['BLV459']['Val'] == 0 and local_mem['BHV1']['Val'] == 0 and local_mem['BHV2'][
                    'Val'] == 0 and local_mem['BHV3']['Val'] == 0:
                    self.sym_dict[7].update_condition(True)
                if local_mem['URHXUT']['List'][-1] < local_mem['URHXUT']['List'][-2]:
                    self.sym_dict[8].update_condition(True)
                if local_mem['UCHGUT']['List'][-1] < local_mem['UCHGUT']['List'][-2]:
                    self.sym_dict[9].update_condition(True)
                if local_mem['ZSUMP']['List'][-1] > local_mem['ZSUMP']['List'][-2]:
                    self.sym_dict[10].update_condition(True)
                if local_mem['ZINST22']['List'][-1] > local_mem['ZINST22']['List'][-2]:
                    self.sym_dict[11].update_condition(True)
                if local_mem['ZINST23']['List'][-1] > local_mem['ZINST23']['List'][-2]:
                    self.sym_dict[12].update_condition(True)
                if local_mem['ZINST36']['List'][-1] < local_mem['ZINST36']['List'][-2] and local_mem['BPV145']['List'][
                    -1] < local_mem['BPV145']['List'][-2]:
                    self.sym_dict[13].update_condition(True)
                if local_mem['UNRHXUT']['List'][-1] < local_mem['UNRHXUT']['List'][-2]:
                    self.sym_dict[14].update_condition(True)
                if local_mem['BFV122']['List'][-1] > local_mem['BFV122']['List'][-2]:
                    self.sym_dict[15].update_condition(True)

            if get_procedure_name_in_json == "Ab23_01: RCS에서 1차기기 냉각수 계통(CCW)으로 누설":

                if local_mem['ZINST63']['List'][-1] != local_mem['ZINST63']['List'][-2] \
                        or local_mem['ZINST58']['List'][-1] != local_mem['ZINST58']['List'][-2]:
                    self.sym_dict[0].update_condition(True)
                if local_mem['ZVCT']['List'][-1] < local_mem['ZVCT']['List'][-2]:
                    self.sym_dict[1].update_condition(True)
                if local_mem['WNETCH']['List'][-1] > local_mem['WCHGNO']['List'][-2]:
                    self.sym_dict[2].update_condition(True)
                if local_mem['ZINST22']['List'][-1] > local_mem['ZINST22']['List'][-2]:
                    self.sym_dict[3].update_condition(True)
                if local_mem['UCTMT']['List'][-1] > local_mem['UCTMT']['List'][-2]:
                    self.sym_dict[4].update_condition(True)
                if local_mem['BHV1']['Val'] and local_mem['BHV2']['Val'] and local_mem['BHV3']['Val'] and \
                        local_mem['BHV459']['Val'] == 0:
                    self.sym_dict[5].update_condition(True)
                if local_mem['KLAMPO9']['Val'] == 1:
                    self.sym_dict[6].update_condition(True)
                if local_mem['BHV22']['Val'] > 0:
                    self.sym_dict[7].update_condition(True)

            if get_procedure_name_in_json == 'Ab21_01: 가압기 압력 채널 고장 (고)':

                if local_mem['ZINST58']['Val'] >= 157:
                    self.sym_dict[0].update_condition(True)
                if local_mem['BPRZSP']['Val'] > 0:
                    self.sym_dict[1].update_condition(True)
                if local_mem['QPRZB']['Val'] == 0:
                    self.sym_dict[2].update_condition(True)
                if local_mem['QPRZH']['Val'] < 0.5:
                    self.sym_dict[3].update_condition(True)
                if local_mem['ZINST58']['Val'] >= 157:
                    if local_mem['KLAMPO308']['Val'] == 1:
                        self.sym_dict[4].update_condition(True)
                if local_mem['BHV6']['Val'] == 0:
                    self.sym_dict[5].update_condition(True)
                if local_mem['KLAMPO308']['Val'] == 1:
                    if local_mem['KLAMPO9']['Val'] == 1:
                        self.sym_dict[6].update_condition(True)
                if local_mem['KLAMPO269']['Val'] == 1:
                    self.sym_dict[7].update_condition(True)
                if local_mem['QPRZH']['Val'] == 0:
                    if local_mem['QPRZB']['Val'] == 0:
                        self.sym_dict[8].update_condition(True)
                if local_mem['BPRZSP']['Val'] > 0:
                    self.sym_dict[9].update_condition(True)
                if local_mem['KLAMPO9']['Val'] == 1:
                    self.sym_dict[10].update_condition(True)

            if get_procedure_name_in_json == 'Ab21_02: 가압기 압력 채널 고장 (저)':
                # BPORV , KLAMPO309 KLAMPO307 문제있음
                if local_mem['ZINST58']['Val'] >= 155:
                    self.sym_dict[0].update_condition(True)
                    if local_mem['QPRZH']['Val'] < 0.5 and local_mem['QPRZB']['Val'] == 0:
                        self.sym_dict[1].update_condition(True)
                if local_mem['KLAMPO307']['Val'] == 1:
                    if local_mem['ZINST58'] >= 155:
                        self.sym_dict[2].update_condition(True)
                if local_mem['BPORV']['Val'] == 1 and local_mem['KLAMPO309']['Val'] == 1:
                    self.sym_dict[3].update_condition(True)
                if local_mem['BPORV']['Val'] == 0 and local_mem['ZINST58']['List'][-1] < local_mem['ZINST58']['List'][
                    -2]:
                    self.sym_dict[4].update_condition(True)
                if local_mem['QPRZH']['Val'] == 0 and local_mem['QPRZB']['Val'] == 0:
                    self.sym_dict[5].update_condition(True)
                if local_mem['BPRZSP']['Val'] != 0:
                    self.sym_dict[6].update_condition(True)

            if get_procedure_name_in_json == 'Ab15_07: 증기발생기 수위 채널 고장 (저)':
                if local_mem['KLAMPO319']['Val'] == 1:
                    self.sym_dict[0].update_condition(True)
                if (local_mem['BFV478']['Val'] > 1 and local_mem['WFWLN1']['Val'] > local_mem['WFWLN2']['Val']) \
                        or (local_mem['BFV488']['Val'] > 1 and local_mem['WFWLN2']['Val'] > local_mem['WFWLN3']['Val']) \
                        or (local_mem['BFV498']['Val'] > 1 and local_mem['WFWLN3']['Val'] > local_mem['WFWLN1']['Val']):
                    self.sym_dict[1].update_condition(True)
                if local_mem['KLAMPO320']['Val'] == 1:
                    self.sym_dict[2].update_condition(True)
                if (local_mem['ZSGN1']['List'][-1] > local_mem['ZSGN1']['List'][-9]) \
                        or (local_mem['ZSGN2']['List'][-1] > local_mem['ZSGN2']['List'][-9]) or \
                        (local_mem['ZSGN3']['List'][-1] > local_mem['ZSGN3']['List'][-9]):
                    self.sym_dict[3].update_condition(True)
                if local_mem['KLAMPO338']['Val'] == 1 and local_mem['KLAMPO214']['Val'] == 1:
                    self.sym_dict[4].update_condition(True)
                if (local_mem['ZINST87']['Val'] < local_mem['ZINST86']['Val'] and local_mem['WFWLN1']['Val'] >
                    local_mem['WFWLN2']['Val']) \
                        or (local_mem['ZINST86']['Val'] < local_mem['ZINST87']['Val'] and local_mem['WFWLN2']['Val'] >
                            local_mem['WFWLN1']['Val']) \
                        or (local_mem['ZINST85']['Val'] < local_mem['ZINST86']['Val'] and local_mem['WFWLN3']['Val'] >
                            local_mem['WFWLN2']['Val']):
                    self.sym_dict[5].update_condition(True)

            if get_procedure_name_in_json == 'Ab15_08: 증기발생기 수위 채널 고장 (고)':
                if (local_mem['BFV478']['Val'] < 0.5 and local_mem['WFWLN1']['Val'] > local_mem['WFWLN2']['Val']) \
                        or (
                        local_mem['BFV488']['Val'] < 0.5 and local_mem['WFWLN2']['Val'] > local_mem['WFWLN3']['Val']) \
                        or (
                        local_mem['BFV498']['Val'] < 0.5 and local_mem['WFWLN3']['Val'] > local_mem['WFWLN1']['Val']):
                    self.sym_dict[0].update_condition(True)
                if local_mem['KLAMPO320']['Val'] == 1:
                    self.sym_dict[1].update_condition(True)
                if (local_mem['ZSGN1']['Val'] == 0) \
                        or (local_mem['ZSGN2']['Val'] == 0) or \
                        (local_mem['ZSGN3']['Val'] == 0):
                    self.sym_dict[2].update_condition(True)
                if (local_mem['ZINST87']['Val'] < local_mem['ZINST86']['Val'] and local_mem['WFWLN1']['Val'] >
                    local_mem['WFWLN2']['Val']) \
                        or (local_mem['ZINST86']['Val'] < local_mem['ZINST87']['Val'] and local_mem['WFWLN2']['Val'] >
                            local_mem['WFWLN1']['Val']) \
                        or (local_mem['ZINST85']['Val'] < local_mem['ZINST86']['Val'] and local_mem['WFWLN3']['Val'] >
                            local_mem['WFWLN2']['Val']):
                    self.sym_dict[3].update_condition(True)

            if get_procedure_name_in_json == 'Ab21_12: 가압기 PORV (열림)':
                if local_mem['BPORV']['Val'] != 0:
                    self.sym_dict[0].update_condition(True)
                if local_mem['KLAMPO312']['Val'] != 0:
                    self.sym_dict[1].update_condition(True)
                if local_mem['BHV6']['Val'] == 0:
                    self.sym_dict[2].update_condition(True)
                if local_mem['CPPRZL']['Val'] > local_mem['PPRZN']['Val']:
                    self.sym_dict[3].update_condition(True)
                if local_mem['UPRT']['Val'] > 45:
                    self.sym_dict[4].update_condition(True)
                if local_mem['QPRZB']['Val'] != 0 and local_mem['QPRZH']['Val'] == 1:
                    self.sym_dict[5].update_condition(True)
                if local_mem['BHV6']['Val'] == 0:
                    self.sym_dict[6].update_condition(True)
            # --------------------------------------------------------------------------------------------------------------

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
        self.setObjectName('ProcedureTable')  # ProcedureTable 와 동일

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
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
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
