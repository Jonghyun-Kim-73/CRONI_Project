from AIDAA_Ver21.DB_AlarmDB import AlarmDB
from collections import deque
from datetime import timedelta
from AIDAA_Ver21.ab_procedure import ab_pro
from collections import deque
import numpy as np
import pandas as pd
import pickle
from keras.models import load_model


class ShMem:
    def __init__(self):
        self.mem = self.make_cns_mem(max_len=10)
        self.AlarmDB: AlarmDB = AlarmDB(self)
        self.add_val_to_list()

    def make_cns_mem(self, max_len, db_path='./db.txt', db_add_path='./db_add.txt'):
        # 초기 shared_mem의 구조를 선언한다.
        idx = 0
        shared_mem = {}
        for file_name in [db_path, db_add_path]:
            with open(file_name, 'r') as f:
                while True:
                    temp_ = f.readline().split('\t')
                    if temp_[0] == '':  # if empty space -> break
                        break
                    if temp_[0] == '#':  # Pass this value. We don't require this value.
                        pass  # These values are normally static values in SMABRES Code.
                    else:
                        sig = 0 if temp_[1] == 'INTEGER' else 1
                        shared_mem[temp_[0]] = {'Sig': sig, 'Val': 0, 'Num': idx, 'List': deque(maxlen=max_len)}
                        idx += 1

        # 다음과정을 통하여 shared_mem 은 PID : { type. val, num }를 가진다.
        return shared_mem

    def update_alarmdb(self):
        self.AlarmDB.update_alarmdb_from_ShMem()

    def add_val_to_list(self):
        [self.mem[para]['List'].append(self.mem[para]['Val']) for para in self.mem.keys()]

    def change_para_val(self, para, val):
        self.mem[para]['Val'] = val

    def get_para_val(self, para):
        return self.mem[para]['Val']

    def get_para_list(self, para):
        return self.mem[para]['List']

    def get_mem(self):
        return self.mem

    def get_alarmdb(self):
        return self.AlarmDB.alarmdb
    
    def get_on_alarms(self):
        return self.AlarmDB.get_on_alarms()

    def get_on_alarms_des(self):
        return self.AlarmDB.get_on_alarms_des()

    def get_alarm_des(self, para):
        return self.AlarmDB.get_alarm_des(para)

    def check_para_name(self, para):
        return True if para in self.mem.keys() else False

    def check_para_type(self, para):
        return self.mem[para]['Sig']

# ----------------------------------------------------------------------------------------------------------------------
    # Urgent action or not
    def get_pro_urgent_act(self, procedure_name):
        return ab_pro[procedure_name]['긴급조치']

    # radiation or not
    def get_pro_radiation(self, procedure_name):
        return ab_pro[procedure_name]['방사선']
    
    def get_pro_symptom(self, procedure_name):
        return ab_pro[procedure_name]['경보 및 증상']

    # Symptom count
    def get_pro_symptom_count(self, procedure_name):
        return len(ab_pro[procedure_name]['경보 및 증상'].keys())

    def get_pro_symptom_satify(self, procedure_name):
        return 5

    # Procedure
    def get_pro_procedure(self, procedure_name):
        return {'경보 및 증상': ab_pro[procedure_name]['경보 및 증상'], '자동 동작 사항': ab_pro[procedure_name]['자동 동작 사항'], '긴급 조치 사항': ab_pro[procedure_name]['긴급 조치 사항'], '후속 조치 사항': ab_pro[procedure_name]['후속 조치 사항']}

    def get_pro_procedure_count(self, procedure_name):
        return {'경보 및 증상': len(ab_pro[procedure_name]['경보 및 증상'].keys()), '자동 동작 사항': len(ab_pro[procedure_name]['자동 동작 사항'].keys()), '긴급 조치 사항': len(ab_pro[procedure_name]['긴급 조치 사항'].keys()), '후속 조치 사항': len(ab_pro[procedure_name]['후속 조치 사항'].keys())}
        return {'목적': 0, '경보 및 증상': len(ab_pro[procedure_name]['경보 및 증상'].keys()),
                '자동 동작 사항': len(ab_pro[procedure_name]['자동 동작 사항'].keys()),
                '긴급 조치 사항': len(ab_pro[procedure_name]['긴급 조치 사항'].keys()),
                '후속 조치 사항': len(ab_pro[procedure_name]['후속 조치 사항'].keys())}


# ----------------------------------------------------------------------------------------------------------------------


class InterfaceMem:
    def __init__(self, Shmem, top_widget):
        self.ShMem: ShMem = Shmem
        self.widget_ids = {}
        # Top_widget 정보 등록
        self.add_widget_id(top_widget)
        # Current system
        self.system_switch = {'Main': 1, 'IFAP': 0, 'AIDAA': 0, 'EGIS': 0, 'Procedure': 0, 'Action': 0, 'PreTrip': 0}
        self.system_state_switch = {'Normal': 1, 'Pre-abnormal': 0, 'Abnormal': 0, 'Emergency': 0}

        self.diagnosis_convert_text = {0: 'Normal: 정상', 1: 'Ab21_01: 가압기 압력 채널 고장 (고)', 2: 'Ab21_02: 가압기 압력 채널 고장 (저)',
                                  3: 'Ab20_04: 가압기 수위 채널 고장 (저)', 4: 'Ab15_07: 증기발생기 수위 채널 고장 (저)',
                                  5: 'Ab15_08: 증기발생기 수위 채널 고장 (고)',
                                  6: 'Ab63_04: 제어봉 낙하', 7: 'Ab63_02: 제어봉의 계속적인 삽입', 8: 'Ab21_12: 가압기 PORV (열림)',
                                  9: 'Ab19_02: 가압기 안전밸브 고장', 10: 'Ab21_11: 가압기 살수밸브 고장 (열림)',
                                  11: 'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설',
                                  12: 'Ab60_02: 재생열교환기 전단부위 파열', 13: 'Ab59_02: 충전수 유량조절밸즈 후단누설',
                                  14: 'Ab23_01: RCS에서 1차기기 냉각수 계통(CCW)으로 누설', 15: 'Ab23_06: 증기발생기 전열관 누설',
                                  16: '해당 시나리오는 학습되지 않은 시나리오입니다.', 17: '학습여부를 아직 확인할 수 없습니다.'}
        self.current_procedure = {self.diagnosis_convert_text[i]: {'num': 0, 'des': {0: '내용 없음', 1: '목적', 2: '경보 및 증상',
                                                                                     3: '자동 동작 사항', 4: '긴급 조치 사항',
                                                                                     5: '후속 조치 사항'}} for i in range(18)}
        self.current_procedure_log = [0, 0]  # [절차서 화면 전환 용도, 선택 절차서 전환 용도]
        self.current_table = {'Procedure':0, 'System': 0, 'current_window': -1, 'procedure_name':""}

        self.procedure_progress_state = {
            self.diagnosis_convert_text[i]: {'목적': 0, '경보 및 증상': 0, '자동 동작 사항': 0, '긴급 조치 사항': 0, '후속 조치 사항': 0} for i
            in range(18)}
        self.pro_procedure_count = [self.ShMem.get_pro_procedure_count(self.diagnosis_convert_text[i]) for i in
                                    range(16)]
        self.procedure_click_state = {self.diagnosis_convert_text[i]: {'목적': [0 for k in range(20)],
                                                                       '경보 및 증상': [0 for k in range(
                                                                           self.pro_procedure_count[i]['경보 및 증상'])],
                                                                       '자동 동작 사항': [0 for k in range(
                                                                           self.pro_procedure_count[i]['자동 동작 사항'])],
                                                                       '긴급 조치 사항': [0 for k in range(
                                                                           self.pro_procedure_count[i]['긴급 조치 사항'])],
                                                                       '후속 조치 사항': [0 for k in range(
                                                                           self.pro_procedure_count[i]['후속 조치 사항'])]}
                                      for i in range(16)}
        self.access_procedure = []

        # AI Part ---------------------------------------------------------------------------------------------------
        self.diagnosis_para = pd.read_csv('./AI/Final_parameter_200825.csv')['0'].tolist()
        self.train_check_para = pd.read_csv('./AI/Final_parameter.csv')['0'].tolist()
        self.diagnosis_model = pickle.load(open('./AI/Ab_Diagnosis_model.h5', 'rb'))
        self.train_check_model = load_model('./AI/Train_Untrain_epoch27_[0.00225299]_acc_[0.9724685967462512].h5', compile=False)
        print('인공지능 모델 로드 완료')

        self.dis_AI = {'AI': '', 'Train':''}
        self.dis_AI_system = [['CVCS', '03/09', '72%']]


    # 인공지능 전처리 용 ------------------------------------------------------------------------------------------------------
    def get_diagnosis_val(self):
        return [self.ShMem.get_para_val(i) for i in self.diagnosis_para]

    def get_diagnosis_result(self):  # 상위 5개의 진단 결과만 출력
        self.dis_AI['AI'] = [self.make_raw(max_v, max_i) for (max_v, max_i) in self.GetTop(self.diagnosis_model.predict([self.get_diagnosis_val()])[0], 5)]

    def get_train_check_val(self):
        return np.array([np.array([self.ShMem.get_para_list(i) for i in self.train_check_para]).reshape(-1,46)])

    def get_train_check_result(self): # 데이터 shape: (1,10,46) 강제
        if np.mean(np.power(self.flatten(self.get_train_check_val())-self.flatten(self.train_check_model.predict(self.get_train_check_val())), 2), axis=1)[0] <= 0.00225299:
            self.dis_AI['Train'] = 0 # 훈련된 시나리오
        else:
            self.dis_AI['Train'] = 1 # 훈련되지 않은 시나리오

    def flatten(self, X):
        '''
        Flatten a 3D array.
        Input
        X            A 3D array for lstm, where the array is sample x timesteps x features.
        Output
        flattened_X  A 2D array, sample x features.
        '''
        flattened_X = np.empty((X.shape[0], X.shape[2]))  # sample x features array.
        for i in range(X.shape[0]):
            flattened_X[i] = X[i, (X.shape[1] - 1), :]
        return (flattened_X)

    def make_raw(self, max_v, max_i):
        diagnosis_convert_text = {0: 'Normal: 정상', 1: 'Ab21_01: 가압기 압력 채널 고장 (고)', 2: 'Ab21_02: 가압기 압력 채널 고장 (저)',
                                  3: 'Ab20_04: 가압기 수위 채널 고장 (저)', 4: 'Ab15_07: 증기발생기 수위 채널 고장 (저)',
                                  5: 'Ab15_08: 증기발생기 수위 채널 고장 (고)',
                                  6: 'Ab63_04: 제어봉 낙하', 7: 'Ab63_02: 제어봉의 계속적인 삽입', 8: 'Ab21_12: 가압기 PORV (열림)',
                                  9: 'Ab19_02: 가압기 안전밸브 고장', 10: 'Ab21_11: 가압기 살수밸브 고장 (열림)',
                                  11: 'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설',
                                  12: 'Ab60_02: 재생열교환기 전단부위 파열', 13: 'Ab59_02: 충전수 유량조절밸즈 후단누설',
                                  14: 'Ab23_01: RCS에서 1차기기 냉각수 계통(CCW)으로 누설', 15: 'Ab23_06: 증기발생기 전열관 누설',
                                  16: '해당 시나리오는 학습되지 않은 시나리오입니다.', 17: '학습여부를 아직 확인할 수 없습니다.'}

        procedure_name = diagnosis_convert_text[max_i]
        try:
            urgent_action = self.ShMem.get_pro_urgent_act(procedure_name)  # True / False
            radiation = self.ShMem.get_pro_radiation(procedure_name)  # True / False
            total_symptomc = self.ShMem.get_pro_symptom_count(procedure_name)
            total_symptoms = self.ShMem.get_pro_symptom_satify(procedure_name)
        except:
            urgent_action = False
            radiation = False
            total_symptomc = 0
            total_symptoms = 0
        return [procedure_name, urgent_action, radiation, f'{total_symptoms:02}/{total_symptomc:02}', f'{max_v * 100:2.2f}%']

    def GetTop(self, raw_list, get_top):
        """ 리스트에서 최대값 랭크와 인덱스 제공 """
        if self.dis_AI['Train'] == 0:
            result = []
            index_ = [i for i in range(len(raw_list))]
            raw_list_ = [i for i in raw_list]
            for i in range(get_top):
                max_idx = np.array(raw_list_).argmax()
                maxv_ = raw_list_[max_idx]
                maxv_id = index_[max_idx]
                index_.pop(max_idx)
                raw_list_.pop(max_idx)
                result.append((maxv_, maxv_id))
        elif self.dis_AI['Train'] == 1:
            result = []
            index_ = [i for i in range(len(raw_list))]
            raw_list_ = [i for i in raw_list]
            result.append((0, 16))
            for i in range(get_top):
                max_idx = np.array(raw_list_).argmax()
                maxv_ = raw_list_[max_idx]
                maxv_id = index_[max_idx]
                index_.pop(max_idx)
                raw_list_.pop(max_idx)
                result.append((maxv_, maxv_id))
        else:
            result = []
            index_ = [i for i in range(len(raw_list))]
            raw_list_ = [i for i in raw_list]
            result.append((0, 17))
            for i in range(get_top):
                max_idx = np.array(raw_list_).argmax()
                maxv_ = raw_list_[max_idx]
                maxv_id = index_[max_idx]
                index_.pop(max_idx)
                raw_list_.pop(max_idx)
                result.append((maxv_, maxv_id))

        return result

    # Widget 링크 용 ----------------------------------------------------------------------------------------------------
    def add_widget_id(self, widget, widget_name=''):
        """새롭게 생성된 위젯의 정보를 self.widget_ids:dict 에 저장하는 함수

        Args:
            widget (_type_): Qwidget, QPushButton를 기반한 ABC 클래스
            widget_name (str, optional): 클래스의 이름이 중복적으로 사용되는 경우 수동 할당을 위해서 존재. Defaults to '' 는 class 명을 따라감.
        """
        self.widget_ids[type(widget).__name__ if widget_name == '' else widget_name] = widget

    def show_widget_ids(self):
        return self.widget_ids

    def change_current_system_name(self, system_name:str):
        """ 버튼 클릭시 화면 전환

        Args:
            system_name (str): Main, IFAP 등 self.system_switch에 작성된 값중 하나여야 함.
        """
        for name in self.system_switch.keys():
            self.system_switch[name] = 1 if system_name == name else 0
        self.widget_ids['MainTab'].change_system_page(system_name)

    def get_time(self):
        return str(timedelta(seconds=self.ShMem.get_para_val('KCNTOMS')/5))

    def get_current_system_name(self):
        return list(self.system_switch.keys())[list(self.system_switch.values()).index(1)]
