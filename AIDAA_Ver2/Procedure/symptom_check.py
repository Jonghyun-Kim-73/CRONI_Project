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

    def abnormal_procedure_59_02(self):
        procedure_name = 'Ab59_02: 충전수 유량조절밸즈 후단누설'
        '''
        경보 및 증상 0~13
        '''
        # 경보 및 증상 1: CHG FLOW CONT FLOW HI/LO(JP005)
        if self.db_val('WCHGNO') < self.db_val('CWCHGL'):
            ab_pro[procedure_name]['경보 및 증상'][0]['AutoClick'] = True
        else:
            ab_pro[procedure_name]['경보 및 증상'][0]['AutoClick'] = False

        # 경보 및 증상 2: PRZR CONT LEVEL LOW DEVIATION(JP006)
        ab_pro[procedure_name]['경보 및 증상'][1]['AutoClick'] = False # 관련 경보 확인 불가(추후조치)

        # 경보 및 증상 3: VOL CONT TK LEVEL HIGH/LOW(JP005)
        if self.db_val('ZVCT') > self.db_val('CZVCT6'):
            ab_pro[procedure_name]['경보 및 증상'][2]['AutoClick'] = True
        else:
            ab_pro[procedure_name]['경보 및 증상'][2]['AutoClick'] = False

        # 경보 및 증상 4: REGEN HX LETDN LINE TEMP HIGH(JP005)
        if self.db_val('URHXUT') > self.db_val('CURHX'):
            ab_pro[procedure_name]['경보 및 증상'][3]['AutoClick'] = True
        else:
            ab_pro[procedure_name]['경보 및 증상'][3]['AutoClick'] = False

        # 경보 및 증상 5: RCP SEAL INJ WTR FLOW LOW(JP005)
        if (self.db_val('WRCPSI1') < self.db_val('CWRCPS')) or (self.db_val('WRCPSI2') < self.db_val('CWRCPS')) or (self.db_val('WRCPSI3') < self.db_val('CWRCPS')):
            ab_pro[procedure_name]['경보 및 증상'][4]['AutoClick'] = True
        else:
            ab_pro[procedure_name]['경보 및 증상'][4]['AutoClick'] = False

        # 경보 및 증상 6: 1E RAD WARN ＆ HIGH ALARM(JP004)
        ab_pro[procedure_name]['경보 및 증상'][5]['AutoClick'] = False # 관련 경보 확인 불가(추후조치)

        # 경보 및 증상 7: 충전유량 지시계 지시치 증가(BG-FI122A JP001)
        if self.sym_increase('WCHGNO'): # CNS상 추전유량 지시치가 증가하는것으로 확인, 그러나 데이터에서는 감소하는 경향을 확인(추후조치)
            ab_pro[procedure_name]['경보 및 증상'][6]['AutoClick'] = True
        else:
            ab_pro[procedure_name]['경보 및 증상'][6]['AutoClick'] = False

        # 경보 및 증상 8: 가압기 수위 지시계 지시치 감소(BB-LI459A/460/461/460B  JP001/005)
        if self.sym_decrease('ZINST63'):
            ab_pro[procedure_name]['경보 및 증상'][7]['AutoClick'] = True
        else:
            ab_pro[procedure_name]['경보 및 증상'][7]['AutoClick'] = False

        # 경보 및 증상 9: 체적제어탱크 수위 지시계 지시치 감소(BG-LI115/112A  JP001/005)
        if self.sym_decrease('ZVCT'):
            ab_pro[procedure_name]['경보 및 증상'][8]['AutoClick'] = True
        else:
            ab_pro[procedure_name]['경보 및 증상'][8]['AutoClick'] = False

        # 경보 및 증상 10: 재생 열교환기 후단 유출수 온도 지시계 지시치 증가(BG-TI140  JP001)
        # (재생 열교환기 전단 충전수 관로 누설시)
        if self.sym_increase('URHXUT'): # jupyter에서는 UCHGUT(충전수 출구 온도)로 되어있는데 URHXUT(RHX 출구 온도)가 맞는듯 함(추후조치)
            ab_pro[procedure_name]['경보 및 증상'][9]['AutoClick'] = True
        else:
            ab_pro[procedure_name]['경보 및 증상'][9]['AutoClick'] = False

        # 경보 및 증상 11: 재생 열교환기 후단 충전수 온도 지시계 지시치 감소(BG-TI123  JP001)
        # (재생 열교환기 후단 충전수 관로 누설시)
        if self.sym_decrease('UCHGUT'):
            ab_pro[procedure_name]['경보 및 증상'][10]['AutoClick'] = True
        else:
            ab_pro[procedure_name]['경보 및 증상'][10]['AutoClick'] = False

        # 경보 및 증상 12: RCP 밀봉수 주입유량 지시계 지시치 감소(BG-FR154A/155A/156A  JP005)
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5: #deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_decrease('WRCPSI1') or self.sym_decrease('WRCPSI2') or self.sym_decrease('WRCPSI3'):
                ab_pro[procedure_name]['경보 및 증상'][11]['AutoClick'] = True
            else: ab_pro[procedure_name]['경보 및 증상'][11]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 13: 격납건물 외부에서 누설 시 보조건물 배수조 수위 증가
        if self.sym_increase('ZSUMP'):
            ab_pro[procedure_name]['경보 및 증상'][12]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][12]['AutoClick'] = False

        # 경보 및 증상 14: 격납건물 내부에서 누설 시 격납건물 배수조 수위 및 온도/습도 증가
        if self.sym_increase('ZSUMP') and self.sym_increase('UCTMT') and self.sym_increase('HUCTMT'):
            ab_pro[procedure_name]['경보 및 증상'][13]['AutoClick'] = True
        else:
            ab_pro[procedure_name]['경보 및 증상'][13]['AutoClick'] = False

        '''
        자동 동작 사항 0~7
        '''
        # 자동 동작 사항 1: 가압기 수위지시계 및 기록계(BB-LI459A/460, BB-LR459) 지시치 17%이하로 감소되면 다음과 같은 자동 동작이 발생한다.
        if ab_pro[procedure_name]['자동 동작 사항'][1]['AutoClick'] == True and ab_pro[procedure_name]['자동 동작 사항'][2]['AutoClick'] == True \
                and ab_pro[procedure_name]['자동 동작 사항'][3]['AutoClick'] == True and ab_pro[procedure_name]['자동 동작 사항'][4]['AutoClick'] == True \
                and ab_pro[procedure_name]['자동 동작 사항'][5]['AutoClick'] == True and ab_pro[procedure_name]['자동 동작 사항'][6]['AutoClick'] == True \
                and ab_pro[procedure_name]['자동 동작 사항'][7]['AutoClick'] == True:
            ab_pro[procedure_name]['자동 동작 사항'][0]['AutoClick'] = True
        else: ab_pro[procedure_name]['자동 동작 사항'][0]['AutoClick'] = False

        # 자동 동작 사항 2: 모든 가압기 전열기 꺼짐(OFF)
        if self.db_val('QPRZ') == 0: # QPRZ는 모든 전열기 파워를 나타내는 변수임.
            ab_pro[procedure_name]['자동 동작 사항'][1]['AutoClick'] = True
        else: ab_pro[procedure_name]['자동 동작 사항'][1]['AutoClick'] = False

        # 자동 동작 사항 3: 유출수 오리피스차단밸브(BG-HV1/2/3) 자동 닫힘
        if self.db_val('BHV1') == 0 and self.db_val('BHV2') == 0 and self.db_val('BHV3') == 0:
            ab_pro[procedure_name]['자동 동작 사항'][2]['AutoClick'] = True
        else: ab_pro[procedure_name]['자동 동작 사항'][2]['AutoClick'] = False

        # 자동 동작 사항 4: 유출수 차단밸브(BG-LV459/460) 자동 닫힘
        if self.db_val('BLV459') == 0:
            ab_pro[procedure_name]['자동 동작 사항'][3]['AutoClick'] = True
        else: ab_pro[procedure_name]['자동 동작 사항'][3]['AutoClick'] = False

        # 자동 동작 사항 5: 충전수 유량 조절밸브(BG-FV122) 완전 열림
        if self.db_val('BFV122') == 1:
            ab_pro[procedure_name]['자동 동작 사항'][4]['AutoClick'] = True
        else: ab_pro[procedure_name]['자동 동작 사항'][4]['AutoClick'] = False

        # 자동 동작 사항 6: 유출수 열교환기 출구온도 증가에 따라 기기냉각수 조절밸브(EG-TV144) 서서히 열림
        ab_pro[procedure_name]['자동 동작 사항'][5]['AutoClick'] = False # 해당 변수 확인 불가(추후조치)

        # 자동 동작 사항 7: 저압 유출수 압력조절밸브(BG-PV145) 자동 닫힘
        if self.db_val('BPV145') <= 0.0005: # 완전히 닫히지 않아서 조건문으로 설정(추후조치)
            ab_pro[procedure_name]['자동 동작 사항'][6]['AutoClick'] = True
        else:
            ab_pro[procedure_name]['자동 동작 사항'][6]['AutoClick'] = False

        # 자동 동작 사항 8: 원자로보충수계통의 빈번한 자동 동작
        ab_pro[procedure_name]['자동 동작 사항'][7]['AutoClick'] = False # (추후조치)

    def abnormal_procedure_60_02(self):
        procedure_name = 'Ab60_02: 재생열교환기 전단부위 파열'
        '''
        경보 및 증상 0~14
        '''
        # 경보 및 증상 0: 유출수 유량지시계(BG-FI150) 지시치 감소 및 유출수 열교환기 출구유량 ‘저’ 경보(15㎥/hr) 발생
        if self.db_val('WNETLD') < self.db_val('CWLHXL'):
            ab_pro[procedure_name]['경보 및 증상'][0]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][0]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 1: VCT 수위지시계(BG-LI112A/LI115) 지시치 감소 및 다음 증상 발생 -> 경보 및 증상 2~4 전체 만족 시
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5: #deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_decrease('ZVCT') and ab_pro[procedure_name]['자동 동작 사항'][2]['AutoClick'] == True and ab_pro[procedure_name]['자동 동작 사항'][3]['AutoClick'] == True and ab_pro[procedure_name]['자동 동작 사항'][4]['AutoClick'] == True:
                ab_pro[procedure_name]['경보 및 증상'][1]['AutoClick'] = True
            else: ab_pro[procedure_name]['경보 및 증상'][1]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 2: VCT 수위 30% 이하시 원자로보충수계통 ‘자동’ 위치에서 자동 보충
        if self.db_val('ZVCT') < self.db_val('CZVCT3') and self.db_val('KLAMPO86') == 1:
            ab_pro[procedure_name]['경보 및 증상'][2]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][2]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 3: VCT 수위 20% 이하시 VCT 수위 ‘저’ 경보
        if self.db_val('ZVCT') < self.db_val('CZVCT2') and self.db_val('KLAMPO263') == 1:
            ab_pro[procedure_name]['경보 및 증상'][3]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][3]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 4: VCT 수위 5% 이하시 충전펌프 흡입원이 VCT에서 RWST로 전환 BG-LV115B/LV115D Open, BG-LV115C/LV115E Close
        if self.db_val('ZVCT') < self.db_val('CZVCT1') and self.db_val('BLV616') != 1 and self.db_val('BLV615') != 0:
            ab_pro[procedure_name]['경보 및 증상'][4]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][4]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 5: 가압기 수위 ‘저’ 편차 경보(기준수위 - 5%) 발생 => 추후조치
        ab_pro[procedure_name]['경보 및 증상'][5]['AutoClick'] = False

        # 경보 및 증상 6: 가압기 압력 ‘저’ 전열기 작동 경보(155.35kg/㎠) 발생
        if self.db_val('ZINST58') < 155.35 and self.db_val('KBHON') == 1:
            ab_pro[procedure_name]['경보 및 증상'][6]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][6]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 7: 가압기 수위 ‘저’ 경보(17%) 및 다음 증상 발생 -> 경보 및 증상 8~9 전체 만족 시
        if self.db_val('ZINST63') < self.db_val('CPZLOW')*100 and ab_pro[procedure_name]['경보 및 증상'][8]['AutoClick'] == True and ab_pro[procedure_name]['경보 및 증상'][9]['AutoClick'] == True:
            ab_pro[procedure_name]['경보 및 증상'][7]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][7]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 8: 가압기 모든 전열기 꺼짐 -> 추후조치
        # 후반에 보조전열기가 켜지나 초반에 꺼져있는 상태를 보고 만족사항으로 나타남.
        if self.db_val('QPRZB') < 0.001 and self.db_val('QPRZH') < 0.001: # 0으로 도달 안함, 때문에 < 0.001로 표현
            ab_pro[procedure_name]['경보 및 증상'][8]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][8]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 9: 유출수 차단발생(BG-LV459/LV460, BG-HV1/HV2/HV3 닫힘)
        if self.db_val('BLV459') == 0 and self.db_val('BHV1') == 0 and self.db_val('BHV2') == 0 and self.db_val('BHV3') == 0:
            ab_pro[procedure_name]['경보 및 증상'][9]['AutoClick'] = True
        else: ab_pro[procedure_name]['경보 및 증상'][9]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 10: 재생 열교환기 후단 유출수 온도(BG-TI140) 감소
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5:  # deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_decrease('URHXUT'):
                ab_pro[procedure_name]['경보 및 증상'][10]['AutoClick'] = True
            else: ab_pro[procedure_name]['경보 및 증상'][10]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 11: 재생 열교환기 후단 충전수 온도(BG-TI123) 감소
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5:  # deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_decrease('UCHGUT'):
                ab_pro[procedure_name]['경보 및 증상'][11]['AutoClick'] = True
            else: ab_pro[procedure_name]['경보 및 증상'][11]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 12: 격납용기 배수조 수위 증가
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5:  # deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_increase('ZSUMP'):
                ab_pro[procedure_name]['경보 및 증상'][12]['AutoClick'] = True
            else: ab_pro[procedure_name]['경보 및 증상'][12]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 13: 격납용기내 방사능준위 증가
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5:  # deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_increase('ZINST22'):
                ab_pro[procedure_name]['경보 및 증상'][13]['AutoClick'] = True
            else: ab_pro[procedure_name]['경보 및 증상'][13]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 경보 및 증상 14: 격납용기내 습도 증가
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5:  # deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_increase('ZINST23'):
                ab_pro[procedure_name]['경보 및 증상'][14]['AutoClick'] = True
            else: ab_pro[procedure_name]['경보 및 증상'][14]['AutoClick'] = False  # IF-THEN dummy 확인용

        '''
        자동 동작 사항 0~2
        '''
        # 자동 동작 사항 0: 유출수 열교환기 출구 압력지시계(BG-PI145) 지시치 감소 및 압력조절밸브(BG-PV145) 서서히 닫힘.
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5:  # deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_decrease('BPV145') and self.sym_decrease('ZINST36'):
                ab_pro[procedure_name]['자동 동작 사항'][0]['AutoClick'] = True
            else: ab_pro[procedure_name]['자동 동작 사항'][0]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 자동 동작 사항 1: 유출수 열교환기 출구 온도지시계(BG-TI144) 지시치 감소 및 유출수 열교환기 출구 온도 조절밸브(EG-TV144) 서서히 닫힘
        # 추후조치 -> 유출수 열교환기 출구 온도지시계 지시치 변수 확인 불가
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5:  # deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_decrease('UNRHXUT'):
                ab_pro[procedure_name]['자동 동작 사항'][1]['AutoClick'] = True
            else: ab_pro[procedure_name]['자동 동작 사항'][1]['AutoClick'] = False  # IF-THEN dummy 확인용

        # 자동 동작 사항 2: 가압기 수위 감소에 따라 충전수 유량제어기(BG-FK122) ‘자동’ 상태에서 충전수 유량 조절밸브(BG-FV122) 서서히 열림
        # 추후조치 -> 충전수 유량제어기 상태변수 확인 필요
        if len(self.shmem.get_shmem_vallist('KCNTOMS')) == 5:  # deque 사용시 필요 (5개가 할당되어 있는지 확인)
            if self.sym_increase('BFV122'):
                ab_pro[procedure_name]['자동 동작 사항'][2]['AutoClick'] = True
            else: ab_pro[procedure_name]['자동 동작 사항'][2]['AutoClick'] = False  # IF-THEN dummy 확인용