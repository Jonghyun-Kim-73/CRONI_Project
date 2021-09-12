import multiprocessing
import sys
import time

class TEST_All_Function_module(multiprocessing.Process):
    def __init__(self, shmem, Max_len):
        multiprocessing.Process.__init__(self)
        self.daemon = True
        self.shmem = shmem
        self.local_mem = self.shmem.get_shmem_db()

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