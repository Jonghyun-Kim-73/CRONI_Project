from AIDAA_Ver2.Procedure.ab_procedure import ab_pro
import numpy as np

class symp_check:
    def __init__(self, shmem):
        self.shmem = shmem
        self.abnormal_procedure_23_06()

    def db_val(self, val):
        return self.shmem.get_shmem_val(val)

    def db_list(self, val, num):
        return self.shmem.get_shmem_vallist(val)[num]

    def sym_increase(self, val):
        return self.db_list(val, 0) < self.db_list(val, 1) < self.db_list(val, 2) < self.db_list(val, 3) < self.db_list(val, 4)

    def sym_decrease(self, val):
        return self.db_list(val, 0) > self.db_list(val, 1) > self.db_list(val, 2) > self.db_list(val, 3) > self.db_list(val, 4)

    def abnormal_procedure_23_06(self):
        procedure_name = 'Ab23_06: 증기발생기 전열관 누설'
        # 경보 및 증상 1
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5: #deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_decrease('ZINST63') or self.sym_decrease('ZINST63'):
                ab_pro[procedure_name]['경보 및 증상'][0]['AutoClick'] = True
            else: ab_pro[procedure_name]['경보 및 증상'][0]['AutoClick'] = False # IF-THEN dummy 확인용

        # 경보 및 증상 2


