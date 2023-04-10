from turtle import st
from AIDAA_Ver21.DB_AlarmDB import AlarmDB
from datetime import timedelta
from AIDAA_Ver21.ab_procedure import ab_pro
from AIDAA_Ver21.CVCS.Core_mimic import *
from collections import deque
import numpy as np
import pandas as pd
import pickle
# from keras.models import load_model


class ShMem:
    def __init__(self):
        self.mem = self.make_cns_mem(max_len=10)
        self.AlarmDB: AlarmDB = AlarmDB(self)
        self.add_val_to_list()
        # Interface_AIDAA_Action.py -------------------------------------------------------------------------------------
        self.CVCS = CVCS()
    
    # - CVCS part -------------------------------------------------------------------------------------------------------
    def update_CVCS(self):                    self.CVCS.step()
    def get_CVCS_para_val(self, para):        return self.CVCS.mem[para]['V'] if para in self.CVCS.mem.keys() else None
    # - Normal part -----------------------------------------------------------------------------------------------------
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

    def update_alarmdb(self):        self.AlarmDB.update_alarmdb_from_ShMem()
    def add_val_to_list(self):       [self.mem[para]['List'].append(self.mem[para]['Val']) for para in self.mem.keys()]
    
    def change_para_val(self, para, val):       self.mem[para]['Val'] = val
    def change_cvcs_para_val(self, para, val):       self.CVCS.mem[para]['V'] = val

    def get_para_val(self, para):         return self.mem[para]['Val']
    def get_para_list(self, para):        return self.mem[para]['List']
    def get_mem(self):                    return self.mem
    def get_alarmdb(self):                return self.AlarmDB.alarmdb
    def get_alarms(self):                 return self.AlarmDB.get_alarms()
    def get_on_alarms(self):              return self.AlarmDB.get_on_alarms()
    def get_on_alarms_val(self):          return self.AlarmDB.get_on_alarms_val()
    def get_alarm_val(self, para):        return self.AlarmDB.get_alarm_val(para)
    def get_on_alarms_des(self):          return self.AlarmDB.get_on_alarms_des()
    def get_alarm_des(self, para):        return self.AlarmDB.get_alarm_des(para)
    def get_on_alarms_unit(self):         return self.AlarmDB.get_on_alarms_unit()
    def get_alarm_unit(self, para):       return self.AlarmDB.get_alarms_unit(para)
    def get_on_alarms_setpoint(self):     return self.AlarmDB.get_on_alarms_setpoint()
    def get_alarm_setpoint(self, para):   return self.AlarmDB.get_alarms_setpoint(para)

    def check_para_name(self, para):      return True if para in self.mem.keys() else False
    def check_para_type(self, para):      return self.mem[para]['Sig']
    def check_cvcs_para_name(self, para): return True if para in self.CVCS.mem.keys() else False
    def check_cvcs_para_type(self, para): return 0 if isinstance(self.CVCS.mem[para], int) else 1

    # ----------------------------------------------------------------------------------------------------------------------
    def get_pro_all_ab_procedure_names(self):
        out = []
        for name_ in ab_pro.keys():
            if 'Ab' in name_:
                out.append(name_)
        return out

    # Urgent action or not
    def get_pro_urgent_act(self, procedure_name):
        return ab_pro[procedure_name]['긴급조치']

    # radiation or not
    def get_pro_radiation(self, procedure_name):
        return ab_pro[procedure_name]['방사선']

    def get_pro_symptom(self, procedure_name):
        return ab_pro[procedure_name]['경보 및 증상']

    # Symptom count
    def get_pro_count(self, procedure_name, title):
        return len(ab_pro[procedure_name][title].keys())

    def get_pro_purpose_count(self, procedure_name):
        return self.get_pro_count(procedure_name, '목적')

    def get_pro_symptom_count(self, procedure_name):
        return self.get_pro_count(procedure_name, '경보 및 증상')

    def get_pro_automatic_count(self, procedure_name):
        return self.get_pro_count(procedure_name, '자동 동작 사항')

    def get_pro_urgent_count(self, procedure_name):
        return self.get_pro_count(procedure_name, '긴급 조치 사항')

    def get_pro_follow_count(self, procedure_name):
        return self.get_pro_count(procedure_name, '후속 조치 사항')

    def get_pro_symptom_satify(self, procedure_name):
        return 5

    # Procedure
    def get_pro_procedure(self, procedure_name):
        return {'경보 및 증상': ab_pro[procedure_name]['경보 및 증상'], '자동 동작 사항': ab_pro[procedure_name]['자동 동작 사항'],
                '긴급 조치 사항': ab_pro[procedure_name]['긴급 조치 사항'], '후속 조치 사항': ab_pro[procedure_name]['후속 조치 사항']}

    def get_pro_procedure_count(self, procedure_name):
        return {'목적': 0, '경보 및 증상': len(ab_pro[procedure_name]['경보 및 증상'].keys()),
                '자동 동작 사항': len(ab_pro[procedure_name]['자동 동작 사항'].keys()),
                '긴급 조치 사항': len(ab_pro[procedure_name]['긴급 조치 사항'].keys()),
                '후속 조치 사항': len(ab_pro[procedure_name]['후속 조치 사항'].keys())}

    def get_pro_procedure_content(self, procedure_name, state, content, type_) -> str:
        """_summary_

        Args:
            procedure_name (_type_): 'Ab21_02: 가압기 압력 채널 고장 (저)'
            state (_type_): '경보 및 증상'
            content (_type_): 0
            type (_type_): 'Des'

        Returns:
            _type_: _description_
        """
        return ab_pro[procedure_name][state][content][type_]

    def get_pro_procedure_contents(self, pro_name, title):
        return ab_pro[pro_name][title]
    def get_system_alarm_num(self):
        system_alarm = {'화학 및 체적 제어계통': [], '원자로 냉각재 계통': [], '주급수 계통': [],
                        '보조 급수 계통': [], '제어봉 제어 계통': [], '잔열 제거 계통': [], '주증기 계통': [],
                        '복수 계통': [], '터빈 계통': [], '전기 계통': []}
        alarm_list = [alarm_name for alarm_name in self.get_on_alarms()]
        alarmdb = self.get_alarmdb()
        for alarm_name in alarm_list:
            for system_name in system_alarm:
                if system_name == alarmdb[alarm_name]['System']:
                    system_alarm[system_name].append(alarm_name)
        return system_alarm
# ----------------------------------------------------------------------------------------------------------------------


class InterfaceMem:
    def __init__(self, Shmem, top_widget):
        self.ShMem: ShMem = Shmem
        self.widget_ids = {}
        # Top_widget 정보 등록
        self.add_widget_id(top_widget)
                
        self.diagnosis_convert_text = {0: 'Normal: 정상', 1: 'Ab21_01: 가압기 압력 채널 고장 (고)', 2: 'Ab21_02: 가압기 압력 채널 고장 (저)',
                                       3: 'Ab20_04: 가압기 수위 채널 고장 (저)', 4: 'Ab15_07: 증기발생기 수위 채널 고장 (저)',
                                       5: 'Ab15_08: 증기발생기 수위 채널 고장 (고)',
                                       6: 'Ab63_04: 제어봉 낙하', 7: 'Ab63_02: 제어봉의 계속적인 삽입', 8: 'Ab21_12: 가압기 PORV (열림)',
                                       9: 'Ab19_02: 가압기 안전밸브 고장', 10: 'Ab21_11: 가압기 살수밸브 고장 (열림)',
                                       11: 'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설',
                                       12: 'Ab60_02: 재생열교환기 전단부위 파열', 13: 'Ab59_02: 충전수 유량조절밸브 후단누설',
                                       14: 'Ab23_01: RCS에서 1차기기 냉각수 계통(CCW)으로 누설', 15: 'Ab23_06: 증기발생기 전열관 누설',
                                       16: '해당 시나리오는 학습되지 않은 시나리오입니다.', 17: '학습여부를 아직 확인할 수 없습니다.'}
        self.abnormal_procedure_list = set([key if 'Ab' in key else '' for key in  ab_pro.keys()])  # ab_pro에서 'Ab' 가진 key 만 추출 ['Ab63_04: 제어봉 낙하', 'Ab... ']
        self.abnormal_procedure_list.remove('')
        self.abnormal_system_list = ['화학 및 체적 제어계통', '원자로 냉각재 계통', '주급수 계통', '보조 급수 계통', '제어봉 제어 계통', '잔열 제거 계통', '주증기 계통']
        self.dis_AI = {'AI': [['Ab63_02: 제어봉의 계속적인 삽입', '05/07', '79.52%'], ['Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설', '05/09', '9.34%'], ['Ab59_02: 충전수 유량조절밸브 후단누설', '05/14', '5.52%'], ['Ab63_04: 제어봉 낙하', '05/14', '1.55%'], ['Ab60_02: 재생열교환기 전단부위 파열', '05/15', '0.76%']],
                      'Train': 0,
                       'XAI': [['PRZ Level', '82%'], ['PRZ Pressure', '5%'], ['Loop1 Flow', '1%'], ['Loop2 Flow', '0.5%'], ['Loop3 Flow', '0.3%']],
                       'System': [['화학 및 체적 제어계통', '5', '72%'], ['원자로 냉각재 계통', '3', '16%'], ['주급수 계통', '1', '6%'], ['제어봉 제어 계통', '1', '3%'], ['잔열 제거 계통', '1', '3%']]}# 정지냉각계통
        # Interface_AIDAA_Procedure.py -------------------------------------------------------------------------------------
        looptitle = ['목적', '경보 및 증상', '자동 동작 사항', '긴급 조치 사항', '후속 조치 사항']
        self.ProcedureHis = {pro_name: {
            'SequenceTitleClickHis': {'목적': True, '경보 및 증상': False, '자동 동작 사항': False, '긴급 조치 사항': False,
                                      '후속 조치 사항': False},
            'SequenceTitleClick': '목적',
            'SequenceTitleCondHis': {title: 0 for title in looptitle},
            'ContentsClickHis': {title: [0 for i in range(self.ShMem.get_pro_count(pro_name, title))] for title in
                                 looptitle},
            'Contents': {title: self.ShMem.get_pro_procedure_contents(pro_name, title) for title in looptitle},
        } for pro_name in self.ShMem.get_pro_all_ab_procedure_names()}

        # ------------------------------------------------------------------------------------------------------------------------------------------
        self.current_table = {'Procedure': -1, 'System': -1, 'current_window': -1, 'procedure_name': "",
                              'selected_procedure':"", 'selected_system':""}
        self.pro_procedure_count = [self.ShMem.get_pro_procedure_count(self.diagnosis_convert_text[i]) for i in
                                    range(16)]
        self.access_procedure = []

        # self.current_search = {'Procedure':{'number':'', 'name':''}, # 검색창에 작성한 내용 저장
        #                        'System':'', # 검색창에 작성한 내용 저장
        #                        'reset_number':-1, 'reset_name':-1,# reset: 0 / search: 1
        #                        'system_reset':-1, # reset: 0 / search: 1
        #                        'current_procedure': -1,
        #                        'active_window': 0} # seach 비활성: 0, search 활성: 1

        # AI Part ---------------------------------------------------------------------------------------------------
        # self.diagnosis_para = pd.read_csv('./AI/Final_parameter_200825.csv')['0'].tolist()
        # self.train_check_para = pd.read_csv('./AI/Final_parameter.csv')['0'].tolist()
        # self.diagnosis_model = pickle.load(open('./AI/Ab_Diagnosis_model.h5', 'rb'))
        # self.train_check_model = load_model('./AI/Train_Untrain_epoch27_[0.00225299]_acc_[0.9724685967462512].h5',
        #                                     compile=False)
        # print('인공지능 모델 로드 완료')

    # 인공지능 전처리 용 ------------------------------------------------------------------------------------------------------
    def get_diagnosis_val(self):
        return [self.ShMem.get_para_val(i) for i in self.diagnosis_para]

    def get_diagnosis_result(self):  # 상위 5개의 진단 결과만 출력
        self.dis_AI['AI'] = [self.make_raw(max_v, max_i) for (max_v, max_i) in
                             self.GetTop(self.diagnosis_model.predict([self.get_diagnosis_val()])[0], 3)]

    def get_train_check_val(self):
        return np.array([np.array([self.ShMem.get_para_list(i) for i in self.train_check_para]).reshape(-1, 46)])

    def get_train_check_result(self):  # 데이터 shape: (1,10,46) 강제
        if np.mean(np.power(self.flatten(self.get_train_check_val()) - self.flatten(
                self.train_check_model.predict(self.get_train_check_val())), 2), axis=1)[0] <= 0.00225299:
            self.dis_AI['Train'] = 0  # 훈련된 시나리오
        else:
            self.dis_AI['Train'] = 1  # 훈련되지 않은 시나리오

    # 단축키 설정 --------------------------------------------------------------------------------------------------------
    # def Train_Shortcut_key(self):
    #     if self.ShMem.get_para_val('iFixTrain') == 0:
    #         self.dis_AI['Train'] = 0
    #     elif self.ShMem.get_para_val('iFixTrain') == 1:
    #         self.dis_AI['Train'] = 1

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
                                  12: 'Ab60_02: 재생열교환기 전단부위 파열', 13: 'Ab59_02: 충전수 유량조절밸브 후단누설',
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
        return [procedure_name, urgent_action, radiation, f'{total_symptoms:02}/{total_symptomc:02}',
                f'{max_v * 100:2.2f}%']

    def GetTop(self, raw_list, get_top):
        """ 리스트에서 최대값 랭크와 인덱스 제공 """
        if self.dis_AI['Train'] == 0 or self.ShMem.get_para_val('iFixTrain') == 1:
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
        elif self.dis_AI['Train'] == 1 or self.ShMem.get_para_val('iFixTrain') == 2:
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
            # result.append((0, 17))
            for i in range(get_top):
                max_idx = np.array(raw_list_).argmax()
                maxv_ = raw_list_[max_idx]
                maxv_id = index_[max_idx]
                index_.pop(max_idx)
                raw_list_.pop(max_idx)
                result.append((maxv_, maxv_id))

        return result
    # Procedure_Search.py ----------------------------------------------------------------------------------------------
    def is_name_in_db(self, target_list, target_name):
        if target_name == '':
            return target_list, False
        else:
            bool_list, set_list = [], []
            for name in target_list:
                if target_name in name:
                    bool_list.append(True)
                    set_list.append(name)
                else:
                    bool_list.append(False)
            if any(bool_list):
                return set_list, True
            else:
                return target_list, False
        
    def is_procedure_name_in_db(self, procedure_name:str) -> tuple[list, bool]:
        """ abnormal_procedure_list 에 procedure_name이 있으면 true

        Args:
            procedure_name (str): 절차서명

        Returns:
            tuple[str, bool]: [절차서 명, [1 존재, 0 없음]]
        """
        return self.is_name_in_db(list(self.abnormal_procedure_list), procedure_name)
            
    def is_system_name_in_db(self, system_name:str) -> tuple[list, bool]:
        """ abnormal_system_list 에 system_name이 있으면 true

        Args:
            system_name (str): 시스템 명

        Returns:
            tuple[str, bool]: [시스템 명, [1 존재, 0 없음]]
        """
        return self.is_name_in_db(self.abnormal_system_list, system_name)
    
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

    def get_time(self):
        return str(timedelta(seconds=self.ShMem.get_para_val('KCNTOMS') / 5))

    def get_td(self):
        return timedelta(seconds=self.ShMem.get_para_val('KCNTOMS') / 5)

    def get_ab_procedure_num(self, content):
        return self.ShMem.get_pro_procedure(
            self.dis_AI['AI'][self.current_table['Procedure']][0])[
            self.current_procedure[self.dis_AI['AI'][self.current_table['Procedure']][0]]['des'][
                self.current_procedure[self.dis_AI['AI'][self.current_table['Procedure']][0]]['num']]][content]['Nub']

    def get_ab_procedure_des(self, content):
        return self.ShMem.get_pro_procedure(
            self.dis_AI['AI'][self.current_table['Procedure']][0])[
            self.current_procedure[self.dis_AI['AI'][self.current_table['Procedure']][0]]['des'][
                self.current_procedure[self.dis_AI['AI'][self.current_table['Procedure']][0]]['num']]][
            content]['Des']
