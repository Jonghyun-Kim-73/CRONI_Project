from AIDAA_Ver21.DB_AlarmDB import AlarmDB
from collections import deque
from datetime import timedelta
from AIDAA_Ver21.ab_procedure import ab_pro
from collections import deque


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

    def show_ai_diagnosis_result(self, ranked_list):
        return ranked_list

    # Procedure
    def get_pro_procedure(self, procedure_name):
        return {'경보 및 증상': ab_pro[procedure_name]['경보 및 증상'], '자동 동작 사항': ab_pro[procedure_name]['자동 동작 사항'], '긴급 조치 사항': ab_pro[procedure_name]['긴급 조치 사항'], '후속 조치 사항': ab_pro[procedure_name]['후속 조치 사항']}

    def get_pro_procedure_count(self, procedure_name):
        return {'경보 및 증상': len(ab_pro[procedure_name]['경보 및 증상'].keys()), '자동 동작 사항': len(ab_pro[procedure_name]['자동 동작 사항'].keys()), '긴급 조치 사항': len(ab_pro[procedure_name]['긴급 조치 사항'].keys()), '후속 조치 사항': len(ab_pro[procedure_name]['후속 조치 사항'].keys())}
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
        self.dis_AI = {'AI': [['Ab63_02: 제어봉의 계속적인 삽입', False, False, '05/07', '79.52%'], ['Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설', True, True, '05/09', '9.34%'], ['Ab59_02: 충전수 유량조절밸즈 후단누설', True, True, '05/14', '5.52%'], ['Ab63_04: 제어봉 낙하', False, False, '05/14', '1.55%'], ['Ab60_02: 재생열교환기 전단부위 파열', True, True, '05/15', '0.76%']]}
        self.dis_AI_system = [['CVCS', '03/09', '72%']]
        self.current_table = {'Procedure':0, 'System': 0, 'current_window': -1, 'procedure_name':""}
        self.current_procedure = {'num':0, 'des':{0:'내용 없음', 1:'목적', 2:'경보 및 증상', 3: '자동 동작 사항', 4: '긴급 조치 사항', 5: '후속 조치 사항'}}
        self.current_procedure_log = 0


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

    def update_ai_diagnosis_result(self, ranked_list):
        self.dis_AI = ranked_list

