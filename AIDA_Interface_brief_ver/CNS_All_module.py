import multiprocessing
import numpy as np
import copy
#
from AIDA_Interface_brief_ver.ENVCNS import ENVCNS

import time


class All_Function_module(multiprocessing.Process):
    def __init__(self, shmem):
        multiprocessing.Process.__init__(self)
        self.daemon = True
        self.shmem = shmem

        # 1 CNS 환경 생성 ----------------------------------------------------
        # CNS 정보 읽기
        self.cns_ip, self.cns_port = self.shmem.get_cns_info()
        self.cns_env = ENVCNS(Name='EnvCNS', IP=self.cns_ip, PORT=int(self.cns_port))

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
            self.shmem.change_logic_val('UpdateUI', True)
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
        if local_logic['Run_ai']:
            pass

        while True:
            local_logic = self.shmem.get_logic_info()
            if local_logic['Run']:
                if local_logic['Run_ai']:
                    """
                    TODO AI 방법론 추가
                    """
                    # Make action from AI ------------------------------------------------------------------------------
                    # - 동작이 허가된 AI 모듈이 cns_env 에서 상태를 취득하여 액션을 계산함.
                    # TODO 향후 cns_env에서 노멀라이제이션까지 모두 처리 할 것.

                    pass

                # One Step CNS -------------------------------------------------------------------------------------
                Action_dict = {}  # 향후 액션 추가
                self.cns_env.step(0)

                # Update All mem -----------------------------------------------------------------------------------
                self._update_cnsenv_to_sharedmem()
                self.shmem.change_logic_val('UpdateUI', True)

                # 자동 멈춤 조건
                # if self.cns_env.mem['KCNTOMS']['Val'] > 3000:
                #     self.shmem.change_logic_val('Run', False)

            else:
                self.check_init()
                self.check_mal()
                self.check_speed()
