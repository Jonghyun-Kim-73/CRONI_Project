from AIDAA_Ver2.Procedure.ab_procedure import ab_pro
from AIDAA_Ver2.DB.db import db_make
from AIDAA_Ver2.TOOL.TOOL_Alarm import init_alarm_db, update_alarm

from collections import deque


class SHMem:
    def __init__(self, cnsinfo, remoteinfo, max_len_deque, test=False, db_path='./DB/db.txt', db_add_path='./DB/db_add.txt'):
        self.cnsip, self.cnsport = cnsinfo
        self.remoteip, self.remoteport = remoteinfo
        self.max_len_deque = max_len_deque
        self.test = test
        # 0] 기능 동작 로직
        self.AI = True          # AI 모듈들 동작 허용
        self.XAI = True         # XAI 모듈 동작
        self.ProDiag = True     # 절차서 진단용 AI 모듈 동작

        # 1] CNS 변수용 shmem
        self.mem = db_make().make_mem_structure(self.max_len_deque, db_path, db_add_path)

        print('Main 메모리 생성 완료')
        # 2] Trig 변수용 shmem
        self.logic = {'Run': False,
                      'Run_ai': self.AI,
                      'Run_XAI': self.XAI, 'Run_ProDiag': self.ProDiag,

                      'Initial_condition': False,
                      'Init_Call': False, 'Init_nub': 1,

                      'Mal_Call': False, 'Mal_list': {},

                      'Speed_Call': False, 'Speed': 1,
                      'Auto_Call': False, 'Auto_re_man': False,

                      'Rod_Control_Call': True,

                      'Operation_Strategy': 'N',  # Normal, Abnormal, Em
                      'Operation_Strategy_list': deque(maxlen=2),

                      'Ab_Dig_Result': {},
                      'Ab_Xai_Result': {},
                      'AB_prog': [],

                      'Ab_Procedure': ab_pro,

                      'Close': False,
                      }
        print('Trig 메모리 생성 완료')
        # 3] 변수 그래픽 표기용
        self.save_mem = {
            'KCNTOMS': [], 'PPRZ': [],
        }
        # 4] 알람 감시용
        self.alarm_dict = init_alarm_db()

    def get_test(self):
        return self.test

    def get_max_len(self):
        return self.max_len_deque

    def call_init(self, init_nub):
        self.logic = {'Run': False,
                      'Run_ai': self.AI,
                      'Run_XAI': self.XAI, 'Run_ProDiag': self.ProDiag,

                      'Initial_condition': True,
                      'Init_Call': True, 'Init_nub': init_nub,

                      'Mal_Call': False, 'Mal_list': {},

                      'Speed_Call': False, 'Speed': 1,
                      'Auto_Call': False, 'Auto_re_man': False,

                      'Rod_Control_Call': True,

                      'Operation_Strategy': 'N',  # Normal, Abnormal, Em
                      'Operation_Strategy_list': deque(maxlen=2),

                      'Ab_Dig_Result': {},
                      'Ab_Xai_Result': {},
                      'AB_prog': [],

                      'Ab_Procedure': ab_pro,

                      'Close': False,
                      }

        for key in self.save_mem:
            self.save_mem[key].clear()

    def call_subpression(self):
        self.alarm_dict = init_alarm_db()

    def append_strategy_list(self, st):
        self.logic['Operation_Strategy_list'].append(st)

    def change_mal_val(self, mal_index, mal_dict):
        self.logic['Mal_list'][mal_index] = mal_dict
        self.logic['Mal_Call'] = True

    def change_logic_val(self, key, val):
        self.logic[key] = val

    def change_mal_list(self, nub):
        self.logic['Mal_list'][nub]['Mal_done'] = True

    def change_shmem_db(self, mem):
        saved_mem_key = self.save_mem.keys()
        # 기존 CNS 데이터 업데이트
        for key_val in mem.keys():
            self.mem[key_val] = mem[key_val]
            if key_val in saved_mem_key:
                self.save_mem[key_val].append(mem[key_val]['Val'])
        # 현재 기준으로 발생한 알람 업데이트
        self.alarm_dict = update_alarm(mem, self.alarm_dict)

    def change_alarm_val(self, val_name, val):
        self.alarm_dict[val_name]['Val'] = val

    def change_shmem_val(self, val_name, val):
        self.mem[val_name]['Val'] = val

    def change_pro_mam_click(self, procedure_name, type_, step_nub, clicked):
        self.logic['Ab_Procedure'][procedure_name][type_][step_nub]['ManClick'] = clicked

    def change_pro_auto_click(self, procedure_name, step_nub, clicked):
        self.logic['Ab_Procedure'][procedure_name][step_nub]['AutoClick'] = clicked

    def send_close(self):
        self.logic['Close'] = True

    def get_speed(self, speed):
        self.logic['Speed_Call'] = True
        self.logic['Speed'] = speed
        return str(speed)

    def get_logic(self, key):
        return self.logic[key]

    def get_logic_info(self):
        return self.logic

    def get_cnsip(self):
        return self.cnsip

    def get_cnsport(self):
        return int(self.cnsport)

    def get_remoteip(self):
        return self.remoteip

    def get_remoteport(self):
        return int(self.remoteport)

    def get_shmem_val(self, val_name):
        return self.mem[val_name]['Val']

    def get_shmem_vallist(self, val_name):
        return self.mem[val_name]['List']

    def get_shmem_malinfo(self):
        return self.logic['Mal_Call'], self.logic['Mal_list']

    def get_shmem_db(self):
        return self.mem

    def get_shmem_save_db(self):
        return self.save_mem

    def get_procedure_info(self, procedure_name):
        """ 비정상 및 경보 관련 절차서 DB 에서 선택된 절차서 확인 """
        if procedure_name in self.logic['Ab_Procedure'].keys():
            return self.logic['Ab_Procedure'][procedure_name]
        else:
            return None
    # Urgent action or not
    def get_pro_urgent_act(self, procedure_name):
        return self.logic['Ab_Procedure'][procedure_name]['긴급조치']

    # Symptom count
    def get_pro_symptom_count(self, procedure_name):
        return len(self.logic['Ab_Procedure'][procedure_name]['경보 및 증상'].keys())

    def get_pro_symptom_satify(self, procedure_name):
        return 5

    # Symptom des name
    def get_pro_symptom_des(self, procedure_name, idx):
        return self.logic['Ab_Procedure'][procedure_name]['경보 및 증상'][idx]['Des']

    # Symptom color
    def get_pro_symptom_color(self, procedure_name, idx):
        return self.logic['Ab_Procedure'][procedure_name]['경보 및 증상'][idx]['AutoClick']

    def get_pro_symptom_color2(self, procedure_name, name, idx):
        return self.logic['Ab_Procedure'][procedure_name][name][idx]['AutoClick']

    # get manual click
    def get_pro_manclick(self, procedure_name, name, idx):
        return self.logic['Ab_Procedure'][procedure_name][name][idx]['ManClick']

    # Symptom cnt
    def get_pro_symptom_num(self, procedure_name, name):
        return len(self.logic['Ab_Procedure'][procedure_name][name].keys())

    # Symptom all des name
    def get_pro_symptom_all_des(self, procedure_name, name, idx):
        return self.logic['Ab_Procedure'][procedure_name][name][idx]['Des']

    # Symptom main_4_left name
    def get_pro_symptom_left(self, procedure_name):
        return self.logic['Ab_Procedure'][procedure_name].keys()

    def get_pro_symptom_Nub(self, procedure_name, name, idx):
        return self.logic['Ab_Procedure'][procedure_name][name][idx]['Nub']

    def get_alarm_des(self, alarm_name):
        return self.alarm_dict[alarm_name]['Des']

    def get_occur_alarm_nub(self):
        result = 0
        for key in self.alarm_dict.keys():
            if self.alarm_dict[key]['Val'] == 1:
                result += self.alarm_dict[key]['Val']
        return result

    def get_occur_alarm_info(self):
        """
        현재 발생한 알람 dict 로 제공함.
        :return: {'KLAMPOxx': 'lo/lo...', 'KLAMPOxx': 'hi/hi...'}
        """
        result = {}
        for key in self.alarm_dict.keys():
            if self.alarm_dict[key]['Val'] == 1:
                result[key] = self.alarm_dict[key]['Des']
        return result

    def check_para(self, para_name):
        if para_name in self.mem.keys():
            return True
        else:
            return False

    def add_dumy_val(self):
        """ 절차서 If-then 부분 테스트를 위한 List 채우기 """
        # 1. Basic version
        # [self.mem[key]['List'].append(self.mem[key]['Val']) for key in self.mem.keys()]

        # 2. Time 변수만 제어
        for key in self.mem.keys():
            # 2.1 특정 변수 수정
            self.mem[key]['Val'] = self.mem[key]['Val'] + 1 if key == 'KCNTOMS' else self.mem[key]['Val']
            self.mem[key]['Val'] = self.mem[key]['Val'] + 0.01 if key == 'UAVLEG2' else self.mem[key]['Val']

            # 2.2 Close
            self.mem[key]['List'].append(self.mem[key]['Val'])

        print(f"[TOOL_Shmem.py]_{self.mem['KCNTOMS']['Val']}")