import multiprocessing
import numpy as np
import copy
import sys
#
from AIDA_Interface_brief_ver.ENVCNS import ENVCNS
# AI Module
# from diagnosis_AI import IC_Diagnosis_Pack

import time
import pickle
import pandas as pd


class All_Function_module(multiprocessing.Process):
    def __init__(self, shmem, Max_len):
        multiprocessing.Process.__init__(self)
        self.daemon = True
        self.shmem = shmem

        # 1 CNS 환경 생성 ----------------------------------------------------
        # CNS 정보 읽기
        self.cns_ip, self.cns_port = self.shmem.get_cns_info()
        self.remote_ip, self.remote_port = self.shmem.get_remote_info()
        self.cns_env = ENVCNS(Name='EnvCNS', IP=self.cns_ip, PORT=int(self.cns_port),
                              RIP=self.remote_ip, RPORT=int(self.remote_port),
                              Max_len=Max_len)

        #------------------------------ 추가 부분
        self.lgb_model = pickle.load(open('model/Lightgbm_max_depth_feature_137_200825.h5', 'rb'))
        self.lgb_para = pd.read_csv('./DB/Final_parameter_200825.csv')['0'].tolist()
        with open('./DB/min_max_scaler.pkl', 'rb') as f:
            self.minmax_scaler = pickle.load(f)

    def pr_(self, s):
        head_ = 'AllFuncM'
        return print(f'[{head_:10}][{s}]')

    def _update_cnsenv_to_sharedmem(self):
        # st = time.time()
        self.shmem.change_shmem_db(self.cns_env.mem)
        # print(time.time()-st)

    def check_init(self):
        if self.shmem.get_logic('Init_Call'):
            self.pr_('Initial Start...')
            self.cns_env.reset(file_name='cns_log', initial_nub=self.shmem.get_logic('Init_nub'))
            self._update_cnsenv_to_sharedmem()
            self.shmem.change_logic_val('Init_Call', False)
            self.pr_('Initial End!')

            # 버그 수정 2번째 초기조건에서 0으로 초기화 되지 않는 현상 수정
            if self.cns_env.CMem.CTIME != 0:
                self.cns_env.CMem.update()

    def check_mal(self):
        sw, info_mal = self.shmem.get_shmem_malinfo()
        if sw:
            self.pr_('Mal Start...')
            self.shmem.change_logic_val('Mal_Call', False)
            for _ in info_mal:
                if not info_mal[_]['Mal_done']:     # mal history 중 입력이 안된 것을 찾아서 수행.
                    self.cns_env._send_malfunction_signal(info_mal[_]['Mal_nub'],
                                                          info_mal[_]['Mal_opt'],
                                                          info_mal[_]['Mal_time']
                                                          )
                    self.shmem.change_mal_list(_)
            self.pr_('Mal End!')
            # -- file name 최초 malcase로 전달받음
            self.cns_env.file_name = f'{info_mal[1]["Mal_nub"]}_{info_mal[1]["Mal_opt"]}_{info_mal[1]["Mal_time"]}'
            self.cns_env.init_line()

    def check_speed(self):
        if self.shmem.get_logic('Speed_Call'):
            self.cns_env.want_tick = self.shmem.get_logic('Speed')
            self.shmem.change_logic_val('Speed_Call', False)

    def run(self):
        # ==============================================================================================================
        # - 공유 메모리에서 logic 부분을 취득 후 사용되는 AI 네트워크 정보 취득
        local_logic = self.shmem.get_logic_info()

        # if local_logic['Run_ai']:                                     ** old
            # AI Module 초기화                                           ** old
            # self.IC_Pack = IC_Diagnosis_Pack()   # min_max 용


        while True:
            local_logic = self.shmem.get_logic_info()
            if local_logic['Close']: sys.exit()
            if local_logic['Run']:
                if local_logic['Run_ai']:
                    """
                    TODO AI 방법론 추가
                    """
                    # Make action from AI ------------------------------------------------------------------------------
                    # - 동작이 허가된 AI 모듈이 cns_env 에서 상태를 취득하여 액션을 계산함.
                    # TODO 향후 cns_env에서 노멀라이제이션까지 모두 처리 할 것.

                    # ** old -------------------------------------------------------------
                    # if local_logic['Run_ProDiag']:
                    #     ab_dig_result = self.IC_Pack.get_Dig_result(self.cns_env.mem)
                    #     self.shmem.change_logic_val('Ab_Dig_Result', ab_dig_result)
                    # if local_logic['Run_XAI']:
                    #     shap_result = self.IC_Pack.get_XAI_result(self.cns_env.mem)
                    #     self.shmem.change_logic_val('Ab_Xai_Result', shap_result)

                    # 진단 모듈 -----------------------------------------------------------------------------------------
                    procedure_des = {
                        0: 'Normal: 정상',
                        1: 'Ab21_01: 가압기 압력 채널 고장 (고)',
                        2: 'Ab21_02: 가압기 압력 채널 고장 (저)',
                        3: 'Ab20_04: 가압기 수위 채널 고장 (저)',
                        4: 'Ab15_07: 증기발생기 수위 채널 고장 (저)',
                        5: 'Ab15_08: 증기발생기 수위 채널 고장 (고)',
                        6: 'Ab63_04: 제어봉 낙하',
                        7: 'Ab63_02: 제어봉의 계속적인 삽입',
                        8: 'Ab21_12: 가압기 PORV (열림)',
                        9: 'Ab19_02: 가압기 안전밸브 고장',
                        10: 'Ab21_11: 가압기 살수밸브 고장 (열림)',
                        11: 'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설',
                        12: 'Ab60_02: 재생열교환기 전단부위 파열',
                        13: 'Ab59_02: 충전수 유량조절밸즈 후단누설',
                        14: 'Ab23_01: RCS에서 1차기기 냉각수 계통(CCW)으로 누설',
                        15: 'Ab23_06: 증기발생기 전열관 누설'
                    }
                    rank_result = {}
                    lgb_data = self.minmax_scaler.transform([[self.cns_env.mem[i]['Val'] for i in self.lgb_para]])
                    lgb_result = list(self.lgb_model.predict(lgb_data)[0])

                    for i in range(5):
                        index_ = lgb_result.index(max(lgb_result))
                        rank_result[i] = {'index': procedure_des[lgb_result.index(max(lgb_result))],
                                          'value': max(lgb_result)}
                        del lgb_result[index_]

                    self.shmem.change_logic_val('Ab_Dig_Result', rank_result)
                    # 진단 모듈 End -------------------------------------------------------------------------------------

                    # end AI
                # One Step CNS -------------------------------------------------------------------------------------
                Action_dict = {}  # 향후 액션 추가
                self.cns_env.step(0) # 1초 돌 때 (5tick)

                # Update All mem -----------------------------------------------------------------------------------
                self._update_cnsenv_to_sharedmem()

                # 자동 멈춤 조건
                if self.cns_env.mem['KCNTOMS']['Val'] > 7500:
                    self.shmem.change_logic_val('Run', False)

            else:
                self.check_init()
                self.check_mal()
                self.check_speed()
