from AIDAA_Ver2.Procedure.ab_procedure import ab_pro
import numpy as np

class symp_check:
    def __init__(self, shmem):
        self.shmem = shmem
        print('IF-THEN Rule Test')
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
        '''
        경보 및 증상 0~7
        '''
        # 경보 및 증상 0: 모든 원자로냉각재계통 누설 시 공통적 증상 -> 경보 및 증상 1~3 전체 만족 시
        if ab_pro[procedure_name]['경보 및 증상'][1]['AutoClick'] == True and ab_pro[procedure_name]['경보 및 증상'][2]['AutoClick'] == True and ab_pro[procedure_name]['경보 및 증상'][3]['AutoClick'] == True:
            ab_pro[procedure_name]['경보 및 증상'][0]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][0]['AutoClick'] = True  # IF-THEN dummy 확인용

        # 경보 및 증상 1: PZR 수위 또는 압력 감소
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5: #deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_decrease('ZINST63') or self.sym_decrease('ZINST63'):
                ab_pro[procedure_name]['경보 및 증상'][1]['AutoClick'] = True
            else: ab_pro[procedure_name]['경보 및 증상'][1]['AutoClick'] = False # IF-THEN dummy 확인용

        # 경보 및 증상 2: VCT 수위 감소 또는 보충횟수 증가
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5: #deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_decrease('ZVCT'):
                ab_pro[procedure_name]['경보 및 증상'][2]['AutoClick'] = True
            else: ab_pro[procedure_name]['경보 및 증상'][2]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 3: 발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5: #deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_increase('WCHGNO'):
                ab_pro[procedure_name]['경보 및 증상'][3]['AutoClick'] = True
            else: ab_pro[procedure_name]['경보 및 증상'][3]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 4: 복수기 공기추출계통 방사선감시기(CG-RE004/RE013)의 고방사선경보
        if self.db_val('DSECON') > 3.9E-3:
            ab_pro[procedure_name]['경보 및 증상'][4]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][4]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 5: 증기발생기 취출수계통 및 시료채취계통 방사선감지기(BM-RE410,RC-RE019/029 /039)의 고방사선경보
        if self.db_val('DSECON') > 3.9E-3:
            ab_pro[procedure_name]['경보 및 증상'][5]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][5]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 6: 증기발생기의 급수 및 증기유량 편차 및 경보 발생
        RSTFWD = {1: self.db_val('WSTM1') * 0.1, 2: self.db_val('WSTM2') * 0.1, 3: self.db_val('WSTM3') * 0.1}
        if (abs(self.db_val('WSTM1') - self.db_val('WFWLN1')) > RSTFWD[1]) or (abs(self.db_val('WSTM2') - self.db_val('WFWLN2')) > RSTFWD[2]) or (abs(self.db_val('WSTM3') - self.db_val('WFWLN3')) > RSTFWD[3]):
            ab_pro[procedure_name]['경보 및 증상'][6]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][6]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 7: 주증기관 방사선감지기(AB-RE801A/801B/801C)의 고방사선경보
        if self.db_val('DSECON') > 3.9E-3:
            ab_pro[procedure_name]['경보 및 증상'][7]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][7]['AutoClick'] = False  # IF-THEN dummy 확인용

        '''
        자동 동작 사항 0~3
        '''
        # 자동 동작 사항 0: 가압기 수위가 17％ 이하로 감소할 경우 유출수 밸브가(BG-HV001/002/003, BG-LV459/460 ) 자동으로 차단된다.
        if self.db_val('ZINST63') < 17 and self.db_val('BHV1') == 0 and self.db_val('BHV2') == 0 and self.db_val('BHV3') == 0 and self.db_val('BLV459') == 0:
            ab_pro[procedure_name]['자동 동작 사항'][0]['AutoClick'] = True
        else: ab_pro[procedure_name]['자동 동작 사항'][0]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 자동 동작 사항 1: 증기발생기 전열관 누설 시 증기발생기 취출수계통 고방사선경보가 발생하면 증기발생기 취출수 차단밸브(BM-HV103/203/303)와 시료채취 차단밸브(BM-HV107/207/307)가 닫히고 동시에 취출수 방사선감시기 시료채취 차단밸브(BM-RV410)가 자동으로 닫힌다.
        if (self.db_val('DSECON') > 3.9E-3) and (self.db_val('ZINST116') == 0):
            ab_pro[procedure_name]['자동 동작 사항'][1]['AutoClick'] = True
        else: ab_pro[procedure_name]['자동 동작 사항'][1]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 자동 동작 사항 2: RCS 압력이 136.78㎏/㎠ 이하가 되면 원자로 트립(Rx Trip)이 발생한다.
        if self.db_val('KLAMPO9') == 1:
            ab_pro[procedure_name]['자동 동작 사항'][2]['AutoClick'] = True
        else: ab_pro[procedure_name]['자동 동작 사항'][2]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 자동 동작 사항 3: RCS 압력이 126.57㎏/㎠ 이하가 되면 안전주입(SI)이 발생한다.
        if self.db_val('KLAMPO6') == 1:
            ab_pro[procedure_name]['자동 동작 사항'][3]['AutoClick'] = True
        else: ab_pro[procedure_name]['자동 동작 사항'][3]['AutoClick'] = False  # IF-THEN dummy 확인용



