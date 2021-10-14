from AIDAA_Ver2.Procedure.ab_procedure import ab_pro
from AIDAA_Ver2.DB.db import db_make

from collections import deque


class SHMem:
    def __init__(self, cnsinfo, remoteinfo, max_len_deque):
        self.cnsip, self.cnsport = cnsinfo
        self.remoteip, self.remoteport = remoteinfo
        # 0] 기능 동작 로직
        self.AI = True          # AI 모듈들 동작 허용
        self.XAI = True         # XAI 모듈 동작
        self.ProDiag = True     # 절차서 진단용 AI 모듈 동작

        # 1] CNS 변수용 shmem
        self.mem = db_make().make_mem_structure(max_len_deque)

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

        for key_val in mem.keys():
            self.mem[key_val] = mem[key_val]
            if key_val in saved_mem_key:
                self.save_mem[key_val].append(mem[key_val]['Val'])

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

    def get_cns_info(self):
        return self.cnsip, self.cnsport

    def get_remote_info(self):
        return self.remoteip, self.remoteport

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

    def check_para(self, para_name):
        if para_name in self.mem.keys():
            return True
        else:
            return False