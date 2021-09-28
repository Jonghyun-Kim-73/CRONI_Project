import multiprocessing
import sys
import time

#----------------------- 추가 부분
import pickle
import pandas as pd
import numpy as np


class TEST_All_Function_module(multiprocessing.Process):
    def __init__(self, shmem, Max_len):
        multiprocessing.Process.__init__(self)
        self.daemon = True
        self.shmem = shmem
        self.local_mem = self.shmem.get_shmem_db()
        #------------------------------ 추가 부분
        self.lgb_model = pickle.load(open('model/Lightgbm_max_depth_feature_137_200825.h5', 'rb'))
        self.lgb_para = pd.read_csv('./DB/Final_parameter_200825.csv')['0'].tolist()

    def pr_(self, s):
        head_ = 'AllFuncM'
        return print(f'[{head_:10}][{s}]')

    def _update_cnsenv_to_sharedmem(self):
        self.shmem.change_shmem_db(self.local_mem)

    def _update_shardmem_to_localmem(self):
        self.local_mem = self.shmem.get_shmem_db()

    def check_init(self):
        if self.shmem.get_logic('Init_Call'):
            self.pr_('Initial Start...')

            self.local_mem['KCNTOMS']['Val'] = 0

            self._update_cnsenv_to_sharedmem()
            self.shmem.change_logic_val('Init_Call', False)
            self.pr_('Initial End!')

    def check_mal(self):
        sw, info_mal = self.shmem.get_shmem_malinfo()
        if sw:
            self.pr_('Mal Start...')
            self.shmem.change_logic_val('Mal_Call', False)
            for _ in info_mal:
                if not info_mal[_]['Mal_done']:     # mal history 중 입력이 안된 것을 찾아서 수행.
                    # 동작하지 않음.
                    self.shmem.change_mal_list(_)

            self.pr_('Mal End!')
            # -- file name 최초 malcase로 전달받음

    def check_speed(self):
        if self.shmem.get_logic('Speed_Call'):
            # 동작하지 않음
            self.shmem.change_logic_val('Speed_Call', False)

    def run(self):
        # ==============================================================================================================
        # - 공유 메모리에서 logic 부분을 취득 후 사용되는 AI 네트워크 정보 취득
        local_logic = self.shmem.get_logic_info()

        while True:
            local_logic = self.shmem.get_logic_info()
            if local_logic['Close']: sys.exit()
            if local_logic['Run']:
                if local_logic['Run_ai']:
                    """
                    TODO AI 방법론 추가
                    """
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
                    lgb_data = [self.local_mem[i]['Val'] for i in self.lgb_para]
                    lgb_result = list(self.lgb_model.predict([lgb_data])[0])
                    for i in range(5):
                        index_ = lgb_result.index(max(lgb_result))
                        rank_result[i] = {'index': procedure_des[lgb_result.index(max(lgb_result))], 'value': max(lgb_result)}
                        del lgb_result[index_]

                    self.shmem.change_logic_val('Ab_Dig_Result', rank_result)
                    # 진단 모듈 End -------------------------------------------------------------------------------------

                # One Step CNS -------------------------------------------------------------------------------------
                Action_dict = {}  # 향후 액션 추가

                self.local_mem['KCNTOMS']['Val'] += 5
                time.sleep(1)

                print(self.local_mem['KCNTOMS']['Val'])

                # Update All mem -----------------------------------------------------------------------------------
                self._update_cnsenv_to_sharedmem()

            else:
                self.check_init()
                self.check_mal()
                self.check_speed()

                self._update_shardmem_to_localmem()