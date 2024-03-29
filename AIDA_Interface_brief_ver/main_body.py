import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))    # 콘솔용 절대 경로

from multiprocessing.managers import BaseManager
from multiprocessing import Process
from collections import deque

from AIDA_Interface_brief_ver.db import db_make
from AIDA_Interface_brief_ver.TOOL.TOOL_etc import p_

from AIDA_Interface_brief_ver.CNS_Platform_controller import InterfaceFun
from AIDA_Interface_brief_ver.CNS_All_module import All_Function_module
from AIDA_Interface_brief_ver.TEST_ALL_module import TEST_All_Function_module

from AIDA_Interface_brief_ver.Procedure.ab_procedure import ab_pro

import socket
ip_reg = {
    # 자기 본래 아이피 : {'내부망 아이피' ...}
    '203.237.121.221': {'comip': '192.168.142.1', 'comport':7101, 'cnsip':'192.168.142.133', 'cnsport':7101},   # 상원
    '192.168.100.55': {'comip': '192.168.32.1', 'comport':7101, 'cnsip':'192.168.32.135', 'cnsport':7101},     # 혜선
    '192.168.0.29': {'comip': '192.168.0.29', 'comport': 7105, 'cnsip':'192.168.0.101', 'cnsport': 7105},       # 대일
    '192.168.0.10': {'comip': '192.168.0.29', 'comport': 7105, 'cnsip':'192.168.0.101', 'cnsport': 7105},       # 대일
    '192.168.72.1': {'comip': '192.168.0.192', 'comport':7101, 'cnsip':'192.168.0.107', 'cnsport':7101},        # 윤히
    '192.168.32.1': {'comip': '192.168.37.1', 'comport':7101, 'cnsip':'192.168.37.129', 'cnsport':7101},        # 상현
    '169.254.32.88': {'comip': '192.168.37.1', 'comport':7101, 'cnsip':'192.168.37.129', 'cnsport':7101},       # 지훈
}


class Body:
    def __init__(self):
        # from AUTO_UI_TO_PY import AutoUiToPy
        # AutoUiToPy._ui_to_py()
        get_com_ip = socket.gethostbyname(socket.getfqdn())
        # 초기 입력 인자 전달 --------------------------------------------------------------------------------------------
        parser = argparse.ArgumentParser(description='CNS 플랫폼_Ver0')
        parser.add_argument('--test', type=bool, default=False, required=False, help='인터페이스 테스트 모드 [default=False]')
        parser.add_argument('--comip', type=str, default=ip_reg[get_com_ip]['comip'], required=False, help="현재 컴퓨터의 ip [default='']")
        parser.add_argument('--comport', type=int, default=ip_reg[get_com_ip]['comport'], required=False, help="현재 컴퓨터의 port [default=7001]")
        parser.add_argument('--cnsip', type=str, default=ip_reg[get_com_ip]['cnsip'], required=False, help="CNS 컴퓨터의 ip [default='']")
        parser.add_argument('--cnsport', type=int, default=ip_reg[get_com_ip]['cnsport'], required=False, help="CNS 컴퓨터의 port [default=7001]")
        self.args = parser.parse_args()
        print('=' * 25 + '초기입력 파라메터' + '=' * 25)

    def start(self):
        # 공유 메모리 선언 -----------------------------------------------------------------------------------------------
        BaseManager.register('SHMem', SHMem)
        manager = BaseManager()
        manager.start()
        max_len_deque = 20
        shmem = manager.SHMem(cnsinfo=(self.args.cnsip, self.args.cnsport),
                              remoteinfo=(self.args.comip, self.args.comport),
                              max_len_deque=max_len_deque,
                              )
        # Build Process ------------------------------------------------------------------------------------------------
        p_list = []

        # Build AI-CNS
        if not self.args.test:
            p_ai = All_Function_module(shmem, max_len_deque)
            p_list.append(p_ai)
        else:
            p_ai = TEST_All_Function_module(shmem, max_len_deque)
            p_list.append(p_ai)

            p_(__file__, 'Test Mode')
            pass

        # Build Interface
        p = InterfaceFun(shmem)
        p_list.append(p)

        # --------------------------------------------------------------------------------------------------------------
        [p_.start() for p_ in p_list]
        [p_.join() for p_ in p_list]  # finished at the same time
        # End ----------------------------------------------------------------------------------------------------------


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


if __name__ == '__main__':
    main_process = Body()
    main_process.start()
