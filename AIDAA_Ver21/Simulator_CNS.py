from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
import pandas as pd
import numpy as np
import pickle


class CNS(QWidget):
    def __init__(self, ShMem):
        super(CNS, self).__init__()
        self.ShMem: ShMem = ShMem
        self.inmem: InterfaceMem = InterfaceMem(ShMem, self)
        self.setGeometry(50, 50, 300, 100)

        lay = QVBoxLayout(self)
        one_step_btn = QPushButton('OneStep', self)
        one_step_btn.clicked.connect(self.one_step)
        one_step_btn.clicked.connect(self.ex)

        lay2 = QHBoxLayout()
        change_val_btn = QPushButton('ChangeVal', self)
        change_val_btn.clicked.connect(self.change_val)
        self.paraname = QLineEdit('para_name')
        self.paraval = QLineEdit('para_val')
        lay2.addWidget(change_val_btn)
        lay2.addWidget(self.paraname)
        lay2.addWidget(self.paraval)

        self.mes = QLabel('')

        lay.addWidget(one_step_btn)
        lay.addLayout(lay2)
        lay.addWidget(self.mes)

# ----------------------------------------------------------------------------------------------------------------------
        # 컨트롤러 실행과 함께 AI 실행 준비
        self.AIProcedurePara = pd.read_csv('./AI/Final_parameter_200825.csv')['0'].tolist()
        self.AIProcedureModel = pickle.load(open('./AI/Ab_Diagnosis_model.h5', 'rb'))

    def one_step(self):
        self.ShMem.change_para_val('KCNTOMS', self.ShMem.get_para_val('KCNTOMS') + 5)
        self.ShMem.add_val_to_list()
        self.ShMem.update_alarmdb()
        self.mes.setText(f'OneStep 진행함. [KCNTOMS: {self.ShMem.get_para_val("KCNTOMS")}]')

    def change_val(self):
        if self.ShMem.check_para_name(self.paraname.text()):
            self.mes.setText(f'{self.paraname.text()} 변수 있음.')
            if self.paraval.text().isdigit():
                self.mes.setText(f'{self.paraname.text()} 변수는 {self.paraval.text()} 로 변경됨.')
                o = int(self.paraval.text()) if self.ShMem.check_para_type(self.paraname.text()) == 0 else float(self.paraval.text())
                self.ShMem.change_para_val(self.paraname.text(), o)
            else:
                self.mes.setText(f'{self.paraval.text()} 은 숫자가 아님.')
        else:
            self.mes.setText(f'{self.paraname.text()} 변수 없음.')

        self.paraname.setText('para_name')
        self.paraval.setText('para_val')

# ----------------------------------------------------------------------------------------------------------------------

    def ex(self):
        AIProcedureValue = [self.ShMem.get_para_val(i) for i in self.AIProcedurePara]
        ai_result = self.AIProcedureModel.predict([AIProcedureValue])
        dis_data = [self.make_raw(max_v, max_i) for (max_v, max_i) in self.GetTop(ai_result[0], 5)]
        self.inmem.dis_AI['AI'] = dis_data

    def make_raw(self, max_v, max_i):
        diagnosis_convert_text = {0: 'Normal: 정상', 1: 'Ab21_01: 가압기 압력 채널 고장 (고)', 2: 'Ab21_02: 가압기 압력 채널 고장 (저)',
                                  3: 'Ab20_04: 가압기 수위 채널 고장 (저)', 4: 'Ab15_07: 증기발생기 수위 채널 고장 (저)',
                                  5: 'Ab15_08: 증기발생기 수위 채널 고장 (고)',
                                  6: 'Ab63_04: 제어봉 낙하', 7: 'Ab63_02: 제어봉의 계속적인 삽입', 8: 'Ab21_12: 가압기 PORV (열림)',
                                  9: 'Ab19_02: 가압기 안전밸브 고장', 10: 'Ab21_11: 가압기 살수밸브 고장 (열림)',
                                  11: 'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설',
                                  12: 'Ab60_02: 재생열교환기 전단부위 파열', 13: 'Ab59_02: 충전수 유량조절밸즈 후단누설',
                                  14: 'Ab23_01: RCS에서 1차기기 냉각수 계통(CCW)으로 누설', 15: 'Ab23_06: 증기발생기 전열관 누설'}

        procedure_name = diagnosis_convert_text[max_i]
        urgent_action = self.ShMem.get_pro_urgent_act(procedure_name)  # True / False
        radiation = self.ShMem.get_pro_radiation(procedure_name)  # True / False
        total_symptomc = self.ShMem.get_pro_symptom_count(procedure_name)
        total_symptoms = self.ShMem.get_pro_symptom_satify(procedure_name)
        return [procedure_name, urgent_action, radiation, f'{total_symptoms:02}/{total_symptomc:02}', f'{max_v * 100:2.2f}%']

    def GetTop(self, raw_list, get_top):
        """ 리스트에서 최대값 랭크와 인덱스 제공 """
        result = []
        index_ = [i for i in range(len(raw_list))]
        raw_list_ = [i for i in raw_list]
        for i in range(get_top):
            max_idx = np.array(raw_list_).argmax()

            # maxv_ = np.array(raw_list).max()
            maxv_ = raw_list_[max_idx]
            maxv_id = index_[max_idx]

            index_.pop(max_idx)
            raw_list_.pop(max_idx)

            result.append((maxv_, maxv_id))
        return result




