import multiprocessing
import sys
import time
#
from AIDAA_Ver2.Env.ENVCNS import ENVCNS
from AIDAA_Ver2.TOOL.TOOL_etc import p_
from AIDAA_Ver2.TOOL.TOOL_Shmem import SHMem


class All_Function_module(multiprocessing.Process):
    def __init__(self, shmem, max_len_deque, test_mode):
        multiprocessing.Process.__init__(self)
        self.daemon = True

        self.shmem:SHMem = shmem

        self.test_mode = test_mode
        self.local_mem = self.shmem.get_shmem_db()      # Test Mode 용 메모리 복사

        # 1 CNS 환경 생성 ----------------------------------------------------
        # CNS 정보 읽기
        self.cns_ip, self.cns_port = self.shmem.get_cns_info()
        self.remote_ip, self.remote_port = self.shmem.get_remote_info()
        self.cns_env = ENVCNS(Name='EnvCNS', IP=self.cns_ip, PORT=int(self.cns_port),
                              RIP=self.remote_ip, RPORT=int(self.remote_port),
                              Max_len=max_len_deque)

    def _update_cnsenv_to_sharedmem(self):
        if self.test_mode:
            self.shmem.change_shmem_db(self.local_mem)
        else:
            self.shmem.change_shmem_db(self.cns_env.mem)

    def _update_shardmem_to_localmem(self):
        self.local_mem = self.shmem.get_shmem_db()

    def check_init(self):
        if self.shmem.get_logic('Init_Call'):
            p_(__file__, 'Initial Start...')
            if not self.test_mode:
                self.cns_env.reset(file_name='cns_log', initial_nub=self.shmem.get_logic('Init_nub'))
            self._update_cnsenv_to_sharedmem()
            self.shmem.change_logic_val('Init_Call', False)
            p_(__file__, 'Initial End!')

            # 버그 수정 2번째 초기조건에서 0으로 초기화 되지 않는 현상 수정
            if self.cns_env.CMem.CTIME != 0:
                self.cns_env.CMem.update()

    def check_mal(self):
        sw, info_mal = self.shmem.get_shmem_malinfo()
        if sw:
            p_(__file__, 'Mal Start...')
            self.shmem.change_logic_val('Mal_Call', False)

            if self.test_mode:
                # 동작하지 않음
                p_(__file__, 'Mal End!')
                pass
            else:
                for _ in info_mal:
                    if not info_mal[_]['Mal_done']:     # mal history 중 입력이 안된 것을 찾아서 수행.
                        self.cns_env._send_malfunction_signal(info_mal[_]['Mal_nub'],
                                                              info_mal[_]['Mal_opt'],
                                                              info_mal[_]['Mal_time']
                                                              )
                        # -1번 시나리오만 들어감.
                        # self.cns_env.mem['cINIT']['Val'] = initial_nub
                        self.cns_env.mem['cMAL']['Val'] = 1 if sw else 0
                        self.cns_env.mem['cMALA']['Val'] = 0

                        self.cns_env.mem['cMALC']['Val'] = info_mal[_]['Mal_nub']
                        self.cns_env.mem['cMALO']['Val'] = info_mal[_]['Mal_opt']
                        self.cns_env.mem['cMALT']['Val'] = info_mal[_]['Mal_time']

                        self.shmem.change_mal_list(_)

                p_(__file__, 'Mal End!')
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

                    # end AI
                # One Step CNS -------------------------------------------------------------------------------------
                Action_dict = {'AB': True}  # 향후 액션 추가
                if self.test_mode:
                    self.local_mem['KCNTOMS']['Val'] += 5
                    time.sleep(0.1)
                    print(self.local_mem['KCNTOMS']['Val'])
                else:
                    self.cns_env.step(Action_dict)  # 1초 돌 때 (5tick)

                # Update All mem -----------------------------------------------------------------------------------
                self._update_cnsenv_to_sharedmem()

                #자동 멈춤 조건
                if self.cns_env.mem['KCNTOMS']['Val'] > 5 * 60 * 25 or self.cns_env.mem['KLAMPO9']['Val'] == 1:
                    self.shmem.change_logic_val('Run', False)

            else:
                self.check_init()
                self.check_mal()
                self.check_speed()

                if self.test_mode:
                    self._update_shardmem_to_localmem()
