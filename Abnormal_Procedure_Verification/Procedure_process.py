import pandas as pd
import numpy as np



class procedure:
    def __init__(self):
        self.aop_15 = {f'15_{str(i).zfill(2)}': {e: [] for e in range(0, 10)} for i in range(1, 19)}
        self.aop_15_auto = {f'15_{str(i).zfill(2)}': {e: [] for e in range(0, 10)} for i in range(1, 19)}
        self.aop_19 = {f'19_{str(i).zfill(2)}': {e: [] for e in range(0, 10)} for i in range(1, 3)}
        self.aop_19_auto = {f'19_{str(i).zfill(2)}': {e: [] for e in range(0, 10)} for i in range(1, 3)}
        self.aop_20 = {f'20_{str(i).zfill(2)}': {e: [] for e in range(0, 10)} for i in range(1, 8)}
        self.aop_20_auto = {f'20_{str(i).zfill(2)}': {e: [] for e in range(0, 10)} for i in range(1, 8)}
        self.aop_21 = {f'21_{str(i).zfill(2)}':{e:[] for e in range(0,10)} for i in range(1, 14)}
        self.aop_21_auto = {f'21_{str(i).zfill(2)}': {e: [] for e in range(0, 10)} for i in range(1, 14)}
        self.aop_23 = {f'23_{str(i).zfill(2)}':{e:[] for e in range(0,10)} for i in range(1, 9)}
        self.aop_23_auto = {f'23_{str(i).zfill(2)}': {e: [] for e in range(0, 10)} for i in range(1, 9)}
        print('절차서 분석 시스템이 연결되었습니다.')

    def control_abnormal_procedure(self, db):
        self.abnormal_procedure_15(db=db)
        self.abnormal_procedure_19(db=db)
        self.abnormal_procedure_20(db=db)
        self.abnormal_procedure_21(db=db)
        self.abnormal_procedure_23(db=db)

    def abnormal_procedure_15(self, db): # todo: 공통 증상 격리
        '''
        15. SG 수위제어계통 비정상
        15-01. SG 증기유량 채널(AB-FT 474, 484, 494  또는 FT 475, 485, 495) 고장-저
        15-02. SG 증기유량 채널(AB-FT 474, 484, 494  또는 FT 475, 485, 495) 고장-고
        15-03. SG 압력채널(AB-PT 476, 486, 496 또는 PT 475, 485, 495) 고장-저
        15-04. SG 압력채널(AB-PT 476, 486, 496 또는 PT 475, 485, 495) 고장-고
        15-05. SG 급수유량 채널(AE-FT 476, 486, 496 또는 FT 477, 487, 497) 고장-저
        15-06. SG 급수유량 채널(AE-FT 476, 486, 496 또는 FT 477, 487, 497) 고장-고
        15-07. SG 수위채널(AE-LT 476, 486, 496 또는 LT 473, 483, 493) 고장-저
        15-08. SG 수위채널(AE-LT 476, 486, 496 또는 LT 473, 483, 493) 고장-고
        15-09. 주증기모관 압력채널(AB-PT 464) 고장-저
        15-10. 주증기모관 압력채널(AB-PT 464) 고장-고
        15-11. 주급수모관 압력채널(AE-PT 508) 고장-저
        15-12. 주급수모관 압력채널(AE-PT 508) 고장-고
        15-13. 출력영역 채널(SE-NI 42B, 43B, 44B) 고장-저
        15-14. 출력영역 채널(SE-NI 42B, 43B, 44B) 고장-고
        15-15. MFCV의 Main 제어 Loop 고장
        15-16. SG 수위 제어용 M/A Station NCD Card 고장
        15-17. DCS Module 고장에 의한 SG 수위 감소
        15-18. DCS Module 고장에 의한 SG 수위 증가
        '''
        self.abnormal_procedure_15_07(db=db)
        self.abnormal_procedure_15_08(db=db)

    def abnormal_procedure_15_07(self, db):
        # 15-07. SG 수위채널(AE-LT 476, 486, 496 또는 LT 473, 483, 493) 고장-저
        print('AOP 15-07 Anaysis start')
        # 15_07 증상 1. 해당 ‘SG WATER LEVEL LOW’ 경보 발생(NR 25 %)
        symptom1 = 'SG Low level indication (channel)' # todo: SG 번호 마킹
        if ((db[-1]['ZINST76']*0.01) < db[-1]['CZSGW']) or ((db[-1]['ZINST77']*0.01) < db[-1]['CZSGW']) or ((db[-1]['ZINST78']*0.01) < db[-1]['CZSGW']):
            if np.shape(self.aop_15['15_07'][0])[0] < 1:
                self.aop_15['15_07'][0].append([int(db[-1]['KCNTOMS'] / 5), symptom1])
        print(self.aop_15['15_07'][0])

        # 15_07 증상 2. 해당 ‘SG  LOOP WTR LEVEL LOW-LOW’ 경보 발생(NR 17 %)
        symptom2 = 'SG Low-Low level indication (channel)'  # todo: SG 번호 마킹
        if ((db[-1]['ZINST76'] * 0.01) < 0.17) or ((db[-1]['ZINST77'] * 0.01) < 0.17) or ((db[-1]['ZINST78'] * 0.01) < 0.17):
            if np.shape(self.aop_15['15_07'][1])[0] < 1:
                self.aop_15['15_07'][1].append([int(db[-1]['KCNTOMS'] / 5), symptom2])
        print(self.aop_15['15_07'][1])

        # 15_07 증상 3. 해당 SG MFCV 열림 방향으로 진행 및 해당 SG 실제 급수유량 증가
        symptom3 = 'SG FW flow increased'
        if (db[-1]['BFV478'] > 1 and db[-1]['WFWLN1'] > db[-1]['WFWLN2']) or (db[-1]['BFV488'] > 1 and db[-1]['WFWLN2'] > db[-1]['WFWLN3']) or (db[-1]['BFV498'] > 1 and db[-1]['WFWLN3'] > db[-1]['WFWLN1']):
            if np.shape(self.aop_15['15_07'][2])[0] < 1:
                self.aop_15['15_07'][2].append([int(db[-1]['KCNTOMS'] / 5), symptom3])
        print(self.aop_15['15_07'][2])

        # 15_07 증상 4. 해당 ‘SG STM/FW FLOW DEVIATION’ 경보 발생(±10 %)
        symptom4 = 'SG STM/FW Flow Deviation alert'
        RSTFWD = {1: db[-1]['WSTM1']*0.1, 2: db[-1]['WSTM2']*0.1, 3: db[-1]['WSTM3']*0.1}
        if ((db[-1]['WSTM1']-db[-1]['WFWLN1']) > RSTFWD[1]) or ((db[-1]['WSTM2']-db[-1]['WFWLN2']) > RSTFWD[2]) or ((db[-1]['WSTM3']-db[-1]['WFWLN3']) > RSTFWD[3]):
            if np.shape(self.aop_15['15_07'][3])[0] < 1:
                self.aop_15['15_07'][3].append([int(db[-1]['KCNTOMS'] / 5), symptom4])
        print(self.aop_15['15_07'][3])

        # 15_07 증상 5. 해당 SG 실제 수위 증가 [ZINST70,71,72로 확인가능] todo: 증가 부분은 추후 결정
        symptom5 = 'SG Level increased (real)'
        if (db[0]['ZSGN1'] < db[1]['ZSGN1'] < db[2]['ZSGN1'] < db[3]['ZSGN1'] < db[-1]['ZSGN1']) or (db[0]['ZSGN2'] < db[1]['ZSGN2'] < db[2]['ZSGN2'] < db[3]['ZSGN2'] < db[-1]['ZSGN2']) or (db[0]['ZSGN3'] < db[1]['ZSGN3'] < db[2]['ZSGN3'] < db[3]['ZSGN3'] < db[-1]['ZSGN3']):
            if np.shape(self.aop_15['15_07'][4])[0] < 1:
                self.aop_15['15_07'][4].append([int(db[-1]['KCNTOMS'] / 5), symptom5])
        print(self.aop_15['15_07'][4])

        # 15_07 증상 6. 해당 ‘SG WTR LEVEL HIGH-HIGH’에 의한 터빈 정지 및 원자로 정지 발생 가능(※ 원자로 출력 30% 이상에서 터빈 트립 시 P-8 신호 발생)
        symptom6 = 'Turbine trip and Reactor trip'
        if db[-1]['KLAMPO338'] == 1 and db[-1]['KLAMPO214'] == 1:
            if np.shape(self.aop_15['15_07'][5])[0] < 1:
                self.aop_15['15_07'][5].append([int(db[-1]['KCNTOMS'] / 5), symptom6])
        print(self.aop_15['15_07'][5])

        # 15_07 자동 동작사항 1. 해당 SG 증기/급수유량 편차 증가 todo: 추후 다시 확인
        auto1 = 'SG steam and FW flow deviation increased'
        if db[-1]['ZINST87'] < db[-1]['ZINST86'] and db[-1]['WFWLN1'] > db[-1]['WFWLN2'] or \
            db[-1]['ZINST86'] < db[-1]['ZINST87'] and db[-1]['WFWLN2'] > db[-1]['WFWLN1'] or \
            db[-1]['ZINST85'] < db[-1]['ZINST86'] and db[-1]['WFWLN3'] > db[-1]['WFWLN2']:
            if np.shape(self.aop_15_auto['15_07'][0])[0] < 1:
                self.aop_15_auto['15_07'][0].append([int(db[-1]['KCNTOMS'] / 5), auto1])
        print(self.aop_15_auto['15_07'][0])

    def abnormal_procedure_15_08(self, db):
        # 15-08. SG 수위채널(AE-LT 476, 486, 496 또는 LT 473, 483, 493) 고장-고
        print('AOP 15-08 Anaysis start')
        # 15_08 증상 1. 해당 SG MFCV 닫힘 방향으로 진행 및 해당 SG 실제 급수유량 감소
        symptom1 = 'SG FW flow decreased' # todo: SG 번호 마킹
        if (db[-1]['BFV478'] < 0.5 and db[-1]['WFWLN1'] > db[-1]['WFWLN2']) or (db[-1]['BFV488'] < 0.5 and db[-1]['WFWLN2'] > db[-1]['WFWLN2']) or (db[-1]['BFV498'] < 0.5 and db[-1]['WFWLN3'] > db[-1]['WFWLN1']):
            if np.shape(self.aop_15['15_08'][0])[0] < 1:
                self.aop_15['15_08'][0].append([int(db[-1]['KCNTOMS'] / 5), symptom1])
        print(self.aop_15['15_08'][0])

        # 15_08 증상 2. 해당 ‘SG STM/FW FLOW DEVIATION’ 경보 발생(±10 %)
        symptom2 = 'SG STM/FW Flow Deviation alert'  # todo: SG 번호 마킹
        RSTFWD = {1: db[-1]['WSTM1'] * 0.1, 2: db[-1]['WSTM2'] * 0.1, 3: db[-1]['WSTM3'] * 0.1}
        if ((db[-1]['WSTM1'] - db[-1]['WFWLN1']) > RSTFWD[1]) or ((db[-1]['WSTM2'] - db[-1]['WFWLN2']) > RSTFWD[2]) or ((db[-1]['WSTM3'] - db[-1]['WFWLN3']) > RSTFWD[3]):
            if np.shape(self.aop_15['15_08'][1])[0] < 1:
                self.aop_15['15_08'][1].append([int(db[-1]['KCNTOMS'] / 5), symptom2])
        print(self.aop_15['15_08'][1])

        # 15_08 증상 3. 해당 SG 실제 수위 감소 [ZSGLEG1,2,3,으로 확인가능]
        symptom3 = 'SG Level decreased (real)'  # todo: 추후 감소 수정
        if (db[0]['ZSGN1'] > db[1]['ZSGN1'] > db[2]['ZSGN1'] > db[3]['ZSGN1'] > db[-1]['ZSGN1']) or (db[0]['ZSGN2'] > db[1]['ZSGN2'] > db[2]['ZSGN2'] > db[3]['ZSGN2'] > db[-1]['ZSGN2']) or (db[0]['ZSGN3'] > db[1]['ZSGN3'] > db[2]['ZSGN3'] > db[3]['ZSGN3'] > db[-1]['ZSGN3']):
            if np.shape(self.aop_15['15_08'][2])[0] < 1:
                self.aop_15['15_08'][2].append([int(db[-1]['KCNTOMS'] / 5), symptom3])
        print(self.aop_15['15_08'][2])

        # 15_08 자동 동작사항 1. 해당 SG 증기/급수유량 편차 증가 todo: 추후 다시 확인
        auto1 = 'SG steam and FW flow deviation increased'
        if db[-1]['ZINST87'] < db[-1]['ZINST86'] and db[-1]['WFWLN1'] > db[-1]['WFWLN2'] or \
                db[-1]['ZINST86'] < db[-1]['ZINST87'] and db[-1]['WFWLN2'] > db[-1]['WFWLN1'] or \
                db[-1]['ZINST85'] < db[-1]['ZINST86'] and db[-1]['WFWLN3'] > db[-1]['WFWLN2']:
            if np.shape(self.aop_15_auto['15_08'][0])[0] < 1:
                self.aop_15_auto['15_08'][0].append([int(db[-1]['KCNTOMS'] / 5), auto1])
        print(self.aop_15_auto['15_08'][0])

    def abnormal_procedure_19(self, db): # todo: 공통 증상 격리
        '''
        19. 가압기 압력방출밸브(PORV) 및 안전밸브(Safety Valve) 고장
        19-01. 가압기 압력방출밸브(BB-PV444B/445A/445B) 고장
        19-02. 가압기 안전밸브(BB-PSV008/009/010) 고장
        '''
        self.abnormal_procedure_19_02(db=db)

    def abnormal_procedure_19_02(self, db):
        # 19-02. 가압기 안전밸브(BB-PSV008/009/010) 고장
        print('AOP 19-02 Anaysis start')
        # 19_02 증상 1. 가압기 보조전열기 지시등 켜짐 및 경보(155.4㎏/㎠ : JP006)
        symptom1 = 'PRZ Backup heater on'
        if db[-1]['QPRZB'] > 0:
            if np.shape(self.aop_19['19_02'][0])[0] < 1:
                self.aop_19['19_02'][0].append([int(db[-1]['KCNTOMS'] / 5), symptom1])
        print(self.aop_19['19_02'][0])

        # 19_02 증상 2. 가압기 저압경보(153.7㎏/㎠ : JP006)
        symptom2 = 'PRZ Low pressure indication (real)'
        if db[-1]['PPRZ'] < db[-1]['CPPRZL']:
            if np.shape(self.aop_19['19_02'][1])[0] < 1:
                self.aop_19['19_02'][1].append([int(db[-1]['KCNTOMS'] / 5), symptom2])
        print(self.aop_19['19_02'][1])

        # 19_02 증상 3. 가압기 압력방출탱크(PRT) 고압력 경보(0.6㎏/㎠ : JP006)
        symptom3 = 'PRT High pressure'
        if (db[-1]['PPRT'] - 0.98E5) > db[-1]['CPPRT']:
            if np.shape(self.aop_19['19_02'][2])[0] < 1:
                self.aop_19['19_02'][2].append([int(db[-1]['KCNTOMS'] / 5), symptom3])
        print(self.aop_19['19_02'][2])

        # 19_02 증상 4. 가압기 압력방출탱크(PRT) 고온 경보(45℃ : JP006)
        symptom4 = 'PRT High temperature'
        if db[-1]['UPRT'] >= 45:
            if np.shape(self.aop_19['19_02'][3])[0] < 1:
                self.aop_19['19_02'][3].append([int(db[-1]['KCNTOMS'] / 5), symptom4])
        print(self.aop_19['19_02'][3])

        # 19_02 증상 5. 가압기 수위 변화: 가압기 수위는 증가하는 것처럼 보일 수도 있다.
        symptom5 = 'PRZ Level increased'
        if db[0]['ZINST63'] < db[1]['ZINST63'] < db[2]['ZINST63'] < db[3]['ZINST63'] < db[-1]['ZINST63']:
            if np.shape(self.aop_19['19_02'][4])[0] < 1:
                self.aop_19['19_02'][4].append([int(db[-1]['KCNTOMS'] / 5), symptom5])
        print(self.aop_19['19_02'][4])

        # 19_02 증상 6. 충전유량 증가(BG-FI122A : JP001)
        symptom6 = 'Charging flow increased'
        if db[0]['WCHGNO'] < db[1]['WCHGNO'] < db[2]['WCHGNO'] < db[3]['WCHGNO'] < db[-1]['WCHGNO']:
            if np.shape(self.aop_19['19_02'][5])[0] < 1:
                self.aop_19['19_02'][5].append([int(db[-1]['KCNTOMS'] / 5), symptom6])
        print(self.aop_19['19_02'][5])

        # 19_02 증상 7. VCT 수위 감소 또는 보충횟수 증가
        symptom7 = 'VCT Level decreased'
        if db[0]['ZVCT'] > db[1]['ZVCT'] > db[2]['ZVCT'] > db[3]['ZVCT'] > db[-1]['ZVCT']:
            if np.shape(self.aop_19['19_02'][6])[0] < 1:
                self.aop_19['19_02'][6].append([int(db[-1]['KCNTOMS'] / 5), symptom7])
        print(self.aop_19['19_02'][6])

        # 19_02 자동 동작사항 1. 가압기 보조전열기 켜짐(155.4㎏/㎠)
        auto1 = 'PRZ Backup heater on'
        if db[-1]['QPRZB'] > 0:
            if np.shape(self.aop_19_auto['19_02'][0])[0] < 1:
                self.aop_19_auto['19_02'][0].append([int(db[-1]['KCNTOMS'] / 5), auto1])
        print(self.aop_19_auto['19_02'][0])

        # 19_02 자동 동작사항 2. PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘
        auto2 = 'PRZ PORV isolation valve (HV6) closed'
        if db[-1]['BHV6'] == 0:
            if np.shape(self.aop_19_auto['19_02'][1])[0] < 1:
                self.aop_19_auto['19_02'][1].append([int(db[-1]['KCNTOMS'] / 5), auto2])
        print(self.aop_19_auto['19_02'][1])

        # 19_02 자동 동작사항 3. Rx 트립(136.8㎏/㎠)
        auto3 = 'Reactor trip'
        if db[-1]['KLAMPO9'] == 1:
            if np.shape(self.aop_19_auto['19_02'][2])[0] < 1:
                self.aop_19_auto['19_02'][2].append([int(db[-1]['KCNTOMS'] / 5), auto3])
        print(self.aop_19_auto['19_02'][2])

        # 19_02 자동 동작사항 4. SI 작동(126.7㎏/㎠)
        auto4 = 'Safety Injection actuation'
        if db[-1]['KLAMPO6'] == 1:
            if np.shape(self.aop_19_auto['19_02'][3])[0] < 1:
                self.aop_19_auto['19_02'][3].append([int(db[-1]['KCNTOMS'] / 5), auto4])
        print(self.aop_19_auto['19_02'][3])

    def abnormal_procedure_20(self, db):  # todo: 공통 증상 격리
        '''
        20. 가압기 수위제어계통 비정상
        20-01. 가압기 수위 채널 BB-LT459 고장 '고'(Fail High)
        20-02. 가압기 수위 채널 BB-LT459 고장 '고'(Fail High)
        20-03. 가압기 수위 채널 BB-LT461 고장 '고'(Fail High)
        20-04. 가압기 수위 채널 BB-LT459 고장 '저'(Fail Low)
        20-05. 가압기 수위 채널 BB-LT460 고장 '저'(Fail Low)
        20-06. 가압기 수위 채널 BB-LT461 고장 '저'(Fail Low)
        20-07. 가압기 수위제어기 BB-LK459F 고장(Fail)
        '''
        self.abnormal_procedure_20_04(db=db)

    def abnormal_procedure_20_04(self, db):
        # 20-04. 가압기 수위 채널 BB-LT459 고장 '저'(Fail Low)
        print('AOP 20-04 Anaysis start')
        # 20_04 증상 1. BB-LI459 ‘저’ 수위 지시
        symptom1 = 'PRZ Low level indication (channel)'
        if (db[-1]['ZINST63']/100) < db[-1]['CZPRZL']:
            if np.shape(self.aop_20['20_04'][0])[0] < 1:
                self.aop_20['20_04'][0].append([int(db[-1]['KCNTOMS'] / 5), symptom1])
        print(self.aop_20['20_04'][0])

        # 20_04 증상 2. “LETDN HX OUTLET FLOW LOW” 경보 발생(JP005, 15㎥/hr)
        symptom2 = 'LETDN HX outlet flow low indication'
        if db[-1]['WNETLD'] < db[-1]['CWLHXL']:
            if np.shape(self.aop_20['20_04'][1])[0] < 1:
                self.aop_20['20_04'][1].append([int(db[-1]['KCNTOMS'] / 5), symptom2])
        print(self.aop_20['20_04'][1])

        # 20_04 증상 3. “CHARGING LINE FLOW HI/LO” 경보 발생 및 충전 유량 증가 (JP005, Hi. 경보 : 26.57㎥/hr, Lo. 경보 : 4.77㎥/hr)
        symptom3 = 'Charging flow increased'
        if db[-1]['WCHGNO'] > db[-1]['CWCHGH'] or db[-1]['WCHGNO'] < db[-1]['CWCHGL']:
            if db[0]['WCHGNO'] < db[1]['WCHGNO'] < db[2]['WCHGNO'] < db[3]['WCHGNO'] < db[-1]['WCHGNO']:
                if np.shape(self.aop_20['20_04'][2])[0] < 1:
                    self.aop_20['20_04'][2].append([int(db[-1]['KCNTOMS'] / 5), symptom3])
        print(self.aop_20['20_04'][2])

        # 20_04 증상 4. 건전한 수위지시계(BB-LI460, 461)의 수위 지시치 증가
        symptom4 = 'PRZ Level increased (real)'
        if db[0]['ZPRZNO'] < db[1]['ZPRZNO'] < db[2]['ZPRZNO'] < db[3]['ZPRZNO'] < db[-1]['ZPRZNO']:
            if np.shape(self.aop_20['20_04'][3])[0] < 1:
                self.aop_20['20_04'][3].append([int(db[-1]['KCNTOMS'] / 5), symptom4])
        print(self.aop_20['20_04'][3])

        # 20_04 증상 5. “PZR CONT LVL HIGH HTRS ON” 경보 발생(JP006, 기준 수위+5%)
        symptom5 = 'PZR Control level high heater on alert'
        if (db[0]['ZINST63']/100) > (db[-1]['ZPRZSP']+db[-1]['CZPRZH']) and db[-1]['QPRZB'] > db[-1]['CQPRZP']:
            if np.shape(self.aop_20['20_04'][4])[0] < 1:
                self.aop_20['20_04'][4].append([int(db[-1]['KCNTOMS'] / 5), symptom5])
        print(self.aop_20['20_04'][4])

    def abnormal_procedure_21(self, db): # todo: 공통 증상 격리
        '''
        21. 가압기 (PZR) 압력제어계통 비정상
        21-01. 가압기 압력채널 고장 '고' (BB-PT444)
        21-02. 가압기 압력채널 고장 '저' (BB-PT444)
        21-03. 가압기 압력채널 고장 '고' (BB-PT444A)
        21-04. 가압기 압력채널 고장 '저' (BB-PT444A)
        21-05. 가압기 압력채널 고장 '고' (BB-PT444B)
        21-06. 가압기 압력채널 고장 '저' (BB-PT444B)
        21-07. 가압기 압력채널 고장 '고' (BB-PT445)
        21-08. 가압기 압력채널 고장 '저' (BB-PT445)
        21-09. 가압기 압력 제어기 고장 '고' (BB-PK444A)
        21-10. 가압기 압력 제어기 고장 '저' (BB-PK444A)
        21-11. 가압기 살수밸브 고장 '열림' (BB-PV444C, 444D)
        21-12. 가압기 PORV '열림' (BB-PV444B, 445A, 445B)
        21-13. 가압기 전열기 고장
        '''
        self.abnormal_procedure_21_01(db=db)
        self.abnormal_procedure_21_02(db=db)
        self.abnormal_procedure_21_11(db=db)
        self.abnormal_procedure_21_12(db=db)

    def abnormal_procedure_21_01(self, db):
        # 21-01. 가압기 압력채널 고장 '고' (BB-PT444)
        print('AOP 21-01 Anaysis start')
        # 21_01 증상 1. PZR ‘고’ 압력 지시(BB-PI444)
        symptom1 = 'PRZ High pressure indication (channel)'
        if db[-1]['PPRZN'] > db[-1]['CPPRZH']:
            if np.shape(self.aop_21['21_01'][0])[0] < 1:
                self.aop_21['21_01'][0].append([int(db[-1]['KCNTOMS']/5), symptom1])
        print(self.aop_21['21_01'][0])

        # 21_01 증상 2. PZR 살수밸브(BB-PV444C, 444D) 열림 지시(158.9㎏/㎠)
        symptom2 = 'PRZ Spray valve open indication'
        if db[-1]['BPRZSP'] > 0:
            if np.shape(self.aop_21['21_01'][1])[0] < 1:
                self.aop_21['21_01'][1].append([int(db[-1]['KCNTOMS']/5), symptom2])
        print(self.aop_21['21_01'][1])

        # 21_01 증상 3. PZR 비례전열기 꺼짐(158.1㎏/㎠)
        symptom3 = 'PRZ Proportion heater off'
        if db[-1]['QPRZH'] <= 0.0000000001:
            if np.shape(self.aop_21['21_01'][2])[0] < 1:
                self.aop_21['21_01'][2].append([int(db[-1]['KCNTOMS'] / 5), symptom3])
        print(self.aop_21['21_01'][2])

        # 21_01 증상 4. PZR 보조전열기 꺼짐(155.9㎏/㎠)
        symptom4 = 'PRZ Backup heater off'
        if db[-1]['QPRZB'] == 0 and db[-1]['ZINST58'] <= 155.9:
            if np.shape(self.aop_21['21_01'][3])[0] < 1:
                self.aop_21['21_01'][3].append([int(db[-1]['KCNTOMS'] / 5), symptom4])
        print(self.aop_21['21_01'][3])

        # 21_01 증상 5. "PZR PRESS LOW"(BB-PT445) 경보 발생(153.7㎏/㎠) 및 PZR ‘저’ 압력 지시(BB-PI445, 455, 456, 457)
        symptom5 = 'PRZ Low pressure indication (real)'
        if db[-1]['PPRZ'] < db[-1]['CPPRZL']:
            if np.shape(self.aop_21['21_01'][4])[0] < 1:
                self.aop_21['21_01'][4].append([int(db[-1]['KCNTOMS'] / 5), symptom5])
        print(self.aop_21['21_01'][4])

        # 21_01 증상 6. "PZR LO PRESS INTERLOCK" 경보발생(153.6㎏/㎠) 및 PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘
        symptom6 = 'PRZ PORV isolation valve (HV6) closed'
        if db[-1]['BHV6'] == 0 and db[-1]['ZINST58'] <= 153.6:
            if np.shape(self.aop_21['21_01'][5])[0] < 1:
                self.aop_21['21_01'][5].append([int(db[-1]['KCNTOMS'] / 5), symptom6])
        print(self.aop_21['21_01'][5])

        # 21_01 증상 7. "PZR PRESS LOW ALERT" 경보 발생(136.8㎏/㎠) 및 Rx 트립 작동
        symptom7 = 'PRZ Pressure low alert indication'
        if db[-1]['KLAMPO9'] == 1:
            if np.shape(self.aop_21['21_01'][6])[0] < 1:
                self.aop_21['21_01'][6].append([int(db[-1]['KCNTOMS'] / 5), symptom7])
        print(self.aop_21['21_01'][6])

        # 21_01 증상 8. "PZR PRESS LOW SI ALERT" 경보 발생(126.7㎏/㎠) 및 SI 작동
        symptom8 = 'PRZ Pressure low SI alert indication'
        if db[-1]['KLAMPO269'] == 1:
            if np.shape(self.aop_21['21_01'][7])[0] < 1:
                self.aop_21['21_01'][7].append([int(db[-1]['KCNTOMS'] / 5), symptom8])
        print(self.aop_21['21_01'][7])

        # 21_01 자동 동작사항 1. PZR 전열기 모두 꺼짐(158.1㎏/㎠)
        auto1 = 'PRZ Entire heater off'
        if db[-1]['QPRZH'] <= 0.0000000001 and db[-1]['QPRZB'] == 0:
            if np.shape(self.aop_21_auto['21_01'][0])[0] < 1:
                self.aop_21_auto['21_01'][0].append([int(db[-1]['KCNTOMS'] / 5), auto1])
        print(self.aop_21_auto['21_01'][0])

        # 21_01 자동 동작사항 2. PZR 살수밸브(BB-PV444C, 444D) 열림(158.9㎏/㎠)
        auto2 = 'PRZ Spray valve opened'
        if db[-1]['BPRZSP'] > 0 :
            if np.shape(self.aop_21_auto['21_01'][1])[0] < 1:
                self.aop_21_auto['21_01'][1].append([int(db[-1]['KCNTOMS'] / 5), auto2])
        print(self.aop_21_auto['21_01'][1])

        # 21_01 자동 동작사항 3. Rx 트립(136.8㎏/㎠)
        auto3 = 'Reactor trip'
        if db[-1]['KLAMPO9'] == 1 :
            if np.shape(self.aop_21_auto['21_01'][2])[0] < 1:
                self.aop_21_auto['21_01'][2].append([int(db[-1]['KCNTOMS'] / 5), auto3])
        print(self.aop_21_auto['21_01'][2])

        # 21_01 자동 동작사항 4. SI 작동(126.7㎏/㎠)
        auto4 = 'Safety Injection actuation'
        if db[-1]['KLAMPO6'] == 1 :
            if np.shape(self.aop_21_auto['21_01'][3])[0] < 1:
                self.aop_21_auto['21_01'][3].append([int(db[-1]['KCNTOMS'] / 5), auto4])
        print(self.aop_21_auto['21_01'][3])

    def abnormal_procedure_21_02(self, db):
        # 21-02. 가압기 압력채널 고장 '저' (BB-PT444)
        print('AOP 21-02 Anaysis start')
        # 21_02 증상 1. PZR ‘저’ 압력 지시(BB-PI444)
        symptom1 = 'PRZ Low pressure indication (channel)'
        if db[-1]['PPRZN'] < db[-1]['CPPRZL']:
            if np.shape(self.aop_21['21_02'][0])[0] < 1:
                self.aop_21['21_02'][0].append([int(db[-1]['KCNTOMS']/5), symptom1])
        print(self.aop_21['21_02'][0])

        # 21_02 증상 2. "PZR PRESS LO/BACKUP HEATERS ON" 경보 발생(155.4㎏/㎠) 및 PZR 보조전열기 모두 켜짐 지시
        symptom2 = 'PRZ Backup heater on'
        if db[-1]['QPRZB'] > 0:
            if np.shape(self.aop_21['21_02'][1])[0] < 1:
                self.aop_21['21_02'][1].append([int(db[-1]['KCNTOMS']/5), symptom2])
        print(self.aop_21['21_02'][1])

        # 21_02 증상 3. "PZR PRESS HIGH"(BB-PT444B, 445) 경보 발생(162.4㎏/㎠) 및 PZR ‘고’ 압력 지시(BB-PI445, 455, 456, 457)
        symptom3 = 'PRZ High pressure indication (real)'
        if db[-1]['PPRZ'] > db[-1]['CPPRZH']:
            if np.shape(self.aop_21['21_02'][2])[0] < 1:
                self.aop_21['21_02'][2].append([int(db[-1]['KCNTOMS']/5), symptom3])
        print(self.aop_21['21_02'][2])

        # 21_02 증상 4. PZR PORV(BB-PV444B, 445A, 445B) 열림 지시 및 경보 발생(164.2㎏/㎠)
        symptom4 = 'PRZ PORV opened'
        if db[-1]['BPORV'] > 0:
            if np.shape(self.aop_21['21_02'][3])[0] < 1:
                self.aop_21['21_02'][3].append([int(db[-1]['KCNTOMS']/5), symptom4])
        print(self.aop_21['21_02'][3])

        # 21_02 증상 5. 실제 압력 감소로 PZR PORV(BB-PV444B, 445A, 445B) 닫힘
        symptom5 = 'PRZ PORV closed'
        if np.shape(self.aop_21['21_02'][3])[0] > 0:
            if db[-1]['BPORV'] == 0 and int(db[-1]['KCNTOMS']/5) >= self.aop_21['21_02'][3][0][0]:
                if np.shape(self.aop_21['21_02'][4])[0] < 1:
                    self.aop_21['21_02'][4].append([int(db[-1]['KCNTOMS'] / 5), symptom5])
        print(self.aop_21['21_02'][4])

        # 21_02 자동 동작사항 1. PZR 전열기 모두 켜짐(155.8㎏/㎠)
        auto1 = 'PRZ Entire heater on'
        if db[-1]['QPRZH'] > 0.5 and db[-1]['QPRZB'] > 0:
            if np.shape(self.aop_21_auto['21_02'][0])[0] < 1:
                self.aop_21_auto['21_02'][0].append([int(db[-1]['KCNTOMS'] / 5), auto1])
        print(self.aop_21_auto['21_02'][0])

        # 21_02 자동 동작사항 2. PZR PORV(BB-PV444B, 445A, 445B) 열림(164.2㎏/㎠) 및 닫힘(162.8㎏/㎠) 반복
        auto2 = 'PRZ PORV opening and closing repeating'
        if np.shape(self.aop_21['21_02'][4])[0] > 0:
            if np.shape(self.aop_21_auto['21_02'][1])[0] < 1:
                self.aop_21_auto['21_02'][1].append([int(db[-1]['KCNTOMS'] / 5), auto2])
        print(self.aop_21_auto['21_02'][1])

    def abnormal_procedure_21_11(self, db):
        # 21-11. 가압기 살수밸브 고장 '열림' (BB-PV444C, 444D)
        print('AOP 21-11 Anaysis start')
        # 21_11 증상 1. PZR 살수밸브 열림
        symptom1 = 'PRZ Spray valve opened'
        if db[-1]['BPRZSP'] > 0:
            if np.shape(self.aop_21['21_11'][0])[0] < 1:
                self.aop_21['21_11'][0].append([int(db[-1]['KCNTOMS']/5), symptom1])
        print(self.aop_21['21_11'][0])

        # 21_11 증상 2. PZR 보조전열기 켜짐 지시 및 경보 발생(155.4㎏/㎠)
        symptom2 = 'PRZ Backup heater on'
        if db[-1]['QPRZB'] > 0:
            if np.shape(self.aop_21['21_11'][1])[0] < 1:
                self.aop_21['21_11'][1].append([int(db[-1]['KCNTOMS'] / 5), symptom2])
        print(self.aop_21['21_11'][1])

        # 21_11 증상 3. PZR 저압력 지시(BB-PI444, 445, 455, 456, 457) 및 경보 발생(153.6㎏/㎠)
        symptom3 = 'PRZ Low pressure indication (real)'
        if db[-1]['PPRZ'] < db[-1]['CPPRZL']:
            if np.shape(self.aop_21['21_11'][2])[0] < 1:
                self.aop_21['21_11'][2].append([int(db[-1]['KCNTOMS'] / 5), symptom3])
        print(self.aop_21['21_11'][2])

        # 21_11 증상 4. PZR 압력 보호채널(BB-PI455, 456, 457) ‘저’ 압력 연동 경보발생(153.6㎏/㎠) 및 PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘
        symptom4 = 'PRZ PORV isolation valve (HV6) closed'
        if db[-1]['BHV6'] == 0 and db[-1]['ZINST58'] <= 153.6:
            if np.shape(self.aop_21['21_11'][3])[0] < 1:
                self.aop_21['21_11'][3].append([int(db[-1]['KCNTOMS'] / 5), symptom4])
        print(self.aop_21['21_11'][3])

        # 21_11 증상 5. PZR 압력 138.5㎏/㎠(P-11) 이하시 "PZR PRESS NOT HI(P-11)" 경보 발생
        symptom5 = 'PRZ Pressure Not high (P-11) alert'
        if db[-1]['KLAMPO216'] > 0:
            if np.shape(self.aop_21['21_11'][4])[0] < 1:
                self.aop_21['21_11'][4].append([int(db[-1]['KCNTOMS'] / 5), symptom5])
        print(self.aop_21['21_11'][4])

        # 21_11 증상 6. PZR 수위 급격한 증가 todo: 급격한 증가 수정
        symptom6 = 'PRZ Level dramatic rise'
        if db[0]['ZINST63'] < db[1]['ZINST63'] < db[2]['ZINST63'] < db[3]['ZINST63'] < db[-1]['ZINST63'] and (db[-1]['ZINST63']-db[0]['ZINST63']) > 0.02:
            if np.shape(self.aop_21['21_11'][5])[0] < 1:
                self.aop_21['21_11'][5].append([int(db[-1]['KCNTOMS'] / 5), symptom6])
        print(self.aop_21['21_11'][5])

        # 21_11 증상 7. "PZR PRESS LOW ALERT" 경보 발생(136.8㎏/㎠) 및 Rx 트립 작동
        symptom7 = 'PRZ Pressure low alert indication'
        if db[-1]['KLAMPO9'] == 1:
            if np.shape(self.aop_21['21_11'][6])[0] < 1:
                self.aop_21['21_11'][6].append([int(db[-1]['KCNTOMS'] / 5), symptom7])
        print(self.aop_21['21_11'][6])

        # 21_11 증상 8. "PZR PRESS LOW SI ALERT" 경보 발생(126.7㎏/㎠) 및 SI 작동
        symptom8 = 'PRZ Pressure low SI alert indication'
        if db[-1]['KLAMPO269'] == 1:
            if np.shape(self.aop_21['21_11'][7])[0] < 1:
                self.aop_21['21_11'][7].append([int(db[-1]['KCNTOMS'] / 5), symptom8])
        print(self.aop_21['21_11'][7])

        # 21_11 자동 동작사항 1. PZR 전열기 모두 켜짐(155.8㎏/㎠)
        auto1 = 'PRZ Entire heater on'
        if db[-1]['QPRZH'] > 0.5 and db[-1]['QPRZB'] > 0:
            if np.shape(self.aop_21_auto['21_11'][0])[0] < 1:
                self.aop_21_auto['21_11'][0].append([int(db[-1]['KCNTOMS'] / 5), auto1])
        print(self.aop_21_auto['21_11'][0])

        # 21_11 자동 동작사항 2. PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘
        auto2 = 'PRZ PORV isolation valve (HV6) closed'
        if db[-1]['BHV6'] == 0:
            if np.shape(self.aop_21_auto['21_11'][1])[0] < 1:
                self.aop_21_auto['21_11'][1].append([int(db[-1]['KCNTOMS'] / 5), auto2])
        print(self.aop_21_auto['21_11'][1])

        # 21_11 자동 동작사항 3. Rx 트립(136.8㎏/㎠)
        auto3 = 'Reactor trip'
        if db[-1]['KLAMPO9'] == 1:
            if np.shape(self.aop_21_auto['21_11'][2])[0] < 1:
                self.aop_21_auto['21_11'][2].append([int(db[-1]['KCNTOMS'] / 5), auto3])
        print(self.aop_21_auto['21_11'][2])

        # 21_11 자동 동작사항 4. SI 작동(126.7㎏/㎠)
        auto4 = 'Safety Injection actuation'
        if db[-1]['KLAMPO6'] == 1:
            if np.shape(self.aop_21_auto['21_11'][3])[0] < 1:
                self.aop_21_auto['21_11'][3].append([int(db[-1]['KCNTOMS'] / 5), auto4])
        print(self.aop_21_auto['21_11'][3])

    def abnormal_procedure_21_12(self, db):
        # 21-12. 가압기 PORV '열림' (BB-PV444B, 445A, 445B)
        print('AOP 21-12 Anaysis start')
        # 21_12 증상 1. PZR PORV(BB-PV444B, 445A, 445B) 열림 지시 및 경보 발생
        symptom1 = 'PRZ PORV opened'
        if db[-1]['BPORV'] > 0:
            if np.shape(self.aop_21['21_12'][0])[0] < 1:
                self.aop_21['21_12'][0].append([int(db[-1]['KCNTOMS'] / 5), symptom1])
        print(self.aop_21['21_12'][0])

        # 21_12 증상 2. PZR 저압력/보조전열기 켜짐 지시 및 경보 발생(155.4㎏/㎠)
        symptom2 = 'PRZ Backup heater on'
        if db[-1]['QPRZB'] > 0 and db[-1]['ZINST58'] <= 155.4:
            if np.shape(self.aop_21['21_12'][1])[0] < 1:
                self.aop_21['21_12'][1].append([int(db[-1]['KCNTOMS'] / 5), symptom2])
        print(self.aop_21['21_12'][1])

        # 21_12 증상 3. "PZR LO PRESS INTERLOCK" 경보발생(153.6㎏/㎠) 및 PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘
        symptom3 = 'PRZ PORV isolation valve (HV6) closed'
        if db[-1]['BHV6'] == 0 and db[-1]['ZINST58'] <= 153.6:
            if np.shape(self.aop_21['21_12'][2])[0] < 1:
                self.aop_21['21_12'][2].append([int(db[-1]['KCNTOMS'] / 5), symptom3])
        print(self.aop_21['21_12'][2])

        # 21_12 증상 4. PZR ‘저’ 압력 지시(BB-PI444, 445, 455, 456, 457) 및 경보발생(153.6㎏/㎠)
        symptom4 = 'PRZ Low pressure indication (real)'
        if db[-1]['PPRZN'] < db[-1]['CPPRZL']:
            if np.shape(self.aop_21['21_12'][3])[0] < 1:
                self.aop_21['21_12'][3].append([int(db[-1]['KCNTOMS'] / 5), symptom4])
        print(self.aop_21['21_12'][3])

        # 21_12 증상 5. PRT 고온(45℃), 고압(0.6㎏/㎠), 고수위(85%) 지시 및 경보 발생 / PRT level은 없음 todo: PRT temp 및 pressure 분할
        symptom5 = 'PRT High temperature'
        if db[-1]['UPRT'] >= 45:
            if np.shape(self.aop_21['21_12'][4])[0] < 1:
                self.aop_21['21_12'][4].append([int(db[-1]['KCNTOMS'] / 5), symptom5])
        print(self.aop_21['21_12'][4])

        # 21_12 증상 5. PRT 고온(45℃), 고압(0.6㎏/㎠), 고수위(85%) 지시 및 경보 발생 / PRT level은 없음 todo: PRT temp 및 pressure 분할
        symptom6 = 'PRT High pressure'
        if (db[-1]['PPRT'] - 0.98E5) > db[-1]['CPPRT']:
            if np.shape(self.aop_21['21_12'][5])[0] < 1:
                self.aop_21['21_12'][5].append([int(db[-1]['KCNTOMS'] / 5), symptom6])
        print(self.aop_21['21_12'][5])

        # 21_12 자동 동작사항 1. PZR 전열기 모두 켜짐(155.8㎏/㎠)
        auto1 = 'PRZ Entire heater on'
        if db[-1]['QPRZH'] > 0.5 and db[-1]['QPRZB'] > 0:
            if np.shape(self.aop_21_auto['21_12'][0])[0] < 1:
                self.aop_21_auto['21_12'][0].append([int(db[-1]['KCNTOMS'] / 5), auto1])
        print(self.aop_21_auto['21_12'][0])

        # 21_12 자동 동작사항 2. PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘(153.6㎏/㎠)
        auto2 = 'PRZ PORV isolation valve (HV6) closed'
        if db[-1]['BHV6'] == 0 and db[-1]['ZINST58'] <= 153.6:
            if np.shape(self.aop_21_auto['21_12'][1])[0] < 1:
                self.aop_21_auto['21_12'][1].append([int(db[-1]['KCNTOMS'] / 5), auto2])
        print(self.aop_21_auto['21_12'][1])

    def abnormal_procedure_23(self, db): # todo: 공통 증상 격리
        '''
        23. 원자로냉각재계통 누설
        23-01. 격납용기 내로 누설 시
        23-02. 보조건물로 누설 시
        23-03. 1차기기 냉각수계통으로 누설 시
        23-04. 가압기 압력방출밸브 및 안전밸브를 통한 누설 시
        23-05. 원자로용기 플랜지 밀봉계통으로 누설 시
        23-06. 증기발생기 전열관으로 누설 시
        23-07. 원자로냉각재펌프 밀봉을 통한 누설 시
        23-08. 각종 계기배관 및 가압기 증기영역 파열시
        '''
        self.abnormal_procedure_23_01(db=db)
        self.abnormal_procedure_23_03(db=db)
        self.abnormal_procedure_23_06(db=db)

    def abnormal_procedure_23_01(self, db):
        # 23-01. 격납용기 내로 누설 시 (1차기기 냉각수(CCW)계통으로 누설 시 [RCS에서])
        print('AOP 23-01 Anaysis start')
        # 23_01 증상 1. PZR 수위 또는 압력 감소
        symptom1 = 'PRZ Level or Pressure decreased'
        if (db[0]['ZINST63'] > db[1]['ZINST63'] > db[2]['ZINST63'] > db[3]['ZINST63'] > db[-1]['ZINST63']) or (db[0]['ZINST58'] > db[1]['ZINST58'] > db[2]['ZINST58'] > db[3]['ZINST58'] > db[-1]['ZINST58']):
            if np.shape(self.aop_23['23_01'][0])[0] < 1:
                self.aop_23['23_01'][0].append([int(db[-1]['KCNTOMS']/5), symptom1])
        print(self.aop_23['23_01'][0])

        # 23_01 증상 2. VCT 수위 감소 또는 보충횟수 증가
        symptom2 = 'VCT Level decreased'
        if (db[0]['ZVCT'] > db[1]['ZVCT'] > db[2]['ZVCT'] > db[3]['ZVCT'] > db[-1]['ZVCT']):
            if np.shape(self.aop_23['23_01'][1])[0] < 1:
                self.aop_23['23_01'][1].append([int(db[-1]['KCNTOMS'] / 5), symptom2])
        print(self.aop_23['23_01'][1])

        # 23_01 증상 3. 발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가
        symptom3 = 'Charging flow increased'
        if (db[0]['WCHGNO'] < db[1]['WCHGNO'] < db[2]['WCHGNO'] < db[3]['WCHGNO'] < db[-1]['WCHGNO']):
            if np.shape(self.aop_23['23_01'][2])[0] < 1:
                self.aop_23['23_01'][2].append([int(db[-1]['KCNTOMS'] / 5), symptom3])
        print(self.aop_23['23_01'][2])

        # 23_01 증상 4. CV 대기 방사선감지기(GT-RE211) 또는 격납용기 배기계통 방사선감지기(GT-RE119)의 지시치 증가 및 경보
        symptom4 = 'CTMT radiation increased'
        if (db[0]['ZINST22'] < db[1]['ZINST22'] < db[2]['ZINST22'] < db[3]['ZINST22'] < db[-1]['ZINST22']):
            if np.shape(self.aop_23['23_01'][3])[0] < 1:
                self.aop_23['23_01'][3].append([int(db[-1]['KCNTOMS'] / 5), symptom4])
        print(self.aop_23['23_01'][3])

        # 23_01 증상 5. CV온도가 정상보다 높게 지시 / todo: 절차서 다시 확인
        symptom5 = 'CTMT temperature increased'
        if (db[0]['UCTMT'] < db[1]['UCTMT'] < db[2]['UCTMT'] < db[3]['UCTMT'] < db[-1]['UCTMT']):
            if np.shape(self.aop_23['23_01'][4])[0] < 1:
                self.aop_23['23_01'][4].append([int(db[-1]['KCNTOMS'] / 5), symptom5])
        print(self.aop_23['23_01'][4])

        # 23_01 증상 6. CV Sump 수위 증가 및 배수조 펌프의 기동횟수 증가 / todo: CNS 구현 여부 확인

        # 23_01 자동 동작사항 1. 가압기 수위가 17% 이하로 감소할 경우 유출수 밸브가(BG-HV001/002/003,BG-LV459/460) 자동으로 차단된다.
        auto1 = 'Letdown valve closed'
        if db[-1]['BHV1'] == 0 and db[-1]['BHV2'] == 0 and db[-1]['BHV3'] == 0 and db[-1]['BLV459'] == 0:
            if np.shape(self.aop_23_auto['23_01'][0])[0] < 1:
                self.aop_23_auto['23_01'][0].append([int(db[-1]['KCNTOMS'] / 5), auto1])
        print(self.aop_23_auto['23_01'][0])

        # 23_01 자동 동작사항 2. Rx 트립(136.8㎏/㎠)
        auto2 = 'Reactor trip'
        if db[-1]['KLAMPO9'] == 1:
            if np.shape(self.aop_23_auto['23_01'][1])[0] < 1:
                self.aop_23_auto['23_01'][1].append([int(db[-1]['KCNTOMS'] / 5), auto2])
        print(self.aop_23_auto['23_01'][1])

        # 23_01 자동 동작사항 3. SI 작동(126.7㎏/㎠)
        auto3 = 'Safety Injection actuation'
        if db[-1]['KLAMPO6'] == 1:
            if np.shape(self.aop_23_auto['23_01'][2])[0] < 1:
                self.aop_23_auto['23_01'][2].append([int(db[-1]['KCNTOMS'] / 5), auto3])
        print(self.aop_23_auto['23_01'][2])

    def abnormal_procedure_23_03(self, db):
        # 23-03. 1차기기 냉각수계통으로 누설 시
        print('AOP 23-03 Anaysis start')
        # 23_03 증상 1. PZR 수위 또는 압력 감소
        symptom1 = 'PRZ Level or Pressure decreased'
        if (db[0]['ZINST63'] > db[1]['ZINST63'] > db[2]['ZINST63'] > db[3]['ZINST63'] > db[-1]['ZINST63']) or (db[0]['ZINST58'] > db[1]['ZINST58'] > db[2]['ZINST58'] > db[3]['ZINST58'] > db[-1]['ZINST58']):
            if np.shape(self.aop_23['23_03'][0])[0] < 1:
                self.aop_23['23_03'][0].append([int(db[-1]['KCNTOMS'] / 5), symptom1])
        print(self.aop_23['23_03'][0])

        # 23_03 증상 2. VCT 수위 감소 또는 보충횟수 증가
        symptom2 = 'VCT Level decreased'
        if (db[0]['ZVCT'] > db[1]['ZVCT'] > db[2]['ZVCT'] > db[3]['ZVCT'] > db[-1]['ZVCT']):
            if np.shape(self.aop_23['23_03'][1])[0] < 1:
                self.aop_23['23_03'][1].append([int(db[-1]['KCNTOMS'] / 5), symptom2])
        print(self.aop_23['23_03'][1])

        # 23_03 증상 3. 발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가
        symptom3 = 'Charging flow increased'
        if (db[0]['WCHGNO'] < db[1]['WCHGNO'] < db[2]['WCHGNO'] < db[3]['WCHGNO'] < db[-1]['WCHGNO']):
            if np.shape(self.aop_23['23_03'][2])[0] < 1:
                self.aop_23['23_03'][2].append([int(db[-1]['KCNTOMS'] / 5), symptom3])
        print(self.aop_23['23_03'][2])

        # 23_03 자동 동작사항 1. 가압기 수위가 17% 이하로 감소할 경우 유출수 밸브가(BG-HV001/002/003,BG-LV459/460) 자동으로 차단된다.
        auto1 = 'Letdown valve closed'
        if db[-1]['BHV1'] == 0 and db[-1]['BHV2'] == 0 and db[-1]['BHV3'] == 0 and db[-1]['BLV459'] == 0:
            if np.shape(self.aop_23_auto['23_03'][0])[0] < 1:
                self.aop_23_auto['23_03'][0].append([int(db[-1]['KCNTOMS'] / 5), auto1])
        print(self.aop_23_auto['23_03'][0])

        # 23_03 자동 동작사항 2. Rx 트립(136.8㎏/㎠)
        auto2 = 'Reactor trip'
        if db[-1]['KLAMPO9'] == 1:
            if np.shape(self.aop_23_auto['23_03'][1])[0] < 1:
                self.aop_23_auto['23_03'][1].append([int(db[-1]['KCNTOMS'] / 5), auto2])
        print(self.aop_23_auto['23_03'][1])

        # 23_03 자동 동작사항 3. SI 작동(126.7㎏/㎠)
        auto3 = 'Safety Injection actuation'
        if db[-1]['KLAMPO6'] == 1:
            if np.shape(self.aop_23_auto['23_03'][2])[0] < 1:
                self.aop_23_auto['23_03'][2].append([int(db[-1]['KCNTOMS'] / 5), auto3])
        print(self.aop_23_auto['23_03'][2])

    def abnormal_procedure_23_06(self, db):
        # 23-06. 증기발생기 전열관으로 누설 시
        print('AOP 23-06 Anaysis start')
        # 23_06 증상 1. PZR 수위 또는 압력 감소
        symptom1 = 'PRZ Level or Pressure decreased'
        if (db[0]['ZINST63'] > db[1]['ZINST63'] > db[2]['ZINST63'] > db[3]['ZINST63'] > db[-1]['ZINST63']) or (db[0]['ZINST58'] > db[1]['ZINST58'] > db[2]['ZINST58'] > db[3]['ZINST58'] > db[-1]['ZINST58']):
            if np.shape(self.aop_23['23_06'][0])[0] < 1:
                self.aop_23['23_06'][0].append([int(db[-1]['KCNTOMS'] / 5), symptom1])
        print(self.aop_23['23_06'][0])

        # 23_06 증상 2. VCT 수위 감소 또는 보충횟수 증가
        symptom2 = 'VCT Level decreased'
        if (db[0]['ZVCT'] > db[1]['ZVCT'] > db[2]['ZVCT'] > db[3]['ZVCT'] > db[-1]['ZVCT']):
            if np.shape(self.aop_23['23_06'][1])[0] < 1:
                self.aop_23['23_06'][1].append([int(db[-1]['KCNTOMS'] / 5), symptom2])
        print(self.aop_23['23_06'][1])

        # 23_06 증상 3. 발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가
        symptom3 = 'Charging flow increased'
        if (db[0]['WCHGNO'] < db[1]['WCHGNO'] < db[2]['WCHGNO'] < db[3]['WCHGNO'] < db[-1]['WCHGNO']):
            if np.shape(self.aop_23['23_06'][2])[0] < 1:
                self.aop_23['23_06'][2].append([int(db[-1]['KCNTOMS'] / 5), symptom3])
        print(self.aop_23['23_06'][2])

        # 23_06 증상 4. 해당 ‘SG STM/FW FLOW DEVIATION’ 경보 발생(±10 %)
        symptom4 = 'SG STM/FW Flow Deviation alert'
        RSTFWD = {1: db[-1]['WSTM1'] * 0.1, 2: db[-1]['WSTM2'] * 0.1, 3: db[-1]['WSTM3'] * 0.1}
        if ((db[-1]['WSTM1'] - db[-1]['WFWLN1']) > RSTFWD[1]) or ((db[-1]['WSTM2'] - db[-1]['WFWLN2']) > RSTFWD[2]) or ((db[-1]['WSTM3'] - db[-1]['WFWLN3']) > RSTFWD[3]):
            if np.shape(self.aop_23['23_06'][3])[0] < 1:
                self.aop_23['23_06'][3].append([int(db[-1]['KCNTOMS'] / 5), symptom4])
        print(self.aop_23['23_06'][3])

        # 23_06 증상 5. 2차측 방사선 증가 todo: 임의로 추가한 사항임.
        symptom5 = 'Secondary radiation increased'
        if (db[0]['ZINST102'] < db[1]['ZINST102'] < db[2]['ZINST102'] < db[3]['ZINST102'] < db[-1]['ZINST102']):
            if np.shape(self.aop_23['23_06'][4])[0] < 1:
                self.aop_23['23_06'][4].append([int(db[-1]['KCNTOMS'] / 5), symptom5])
        print(self.aop_23['23_06'][4])

        # 23_06 자동 동작사항 1. 가압기 수위가 17% 이하로 감소할 경우 유출수 밸브가(BG-HV001/002/003,BG-LV459/460) 자동으로 차단된다.
        auto1 = 'Letdown valve closed'
        if db[-1]['BHV1'] == 0 and db[-1]['BHV2'] == 0 and db[-1]['BHV3'] == 0 and db[-1]['BLV459'] == 0:
            if np.shape(self.aop_23_auto['23_06'][0])[0] < 1:
                self.aop_23_auto['23_06'][0].append([int(db[-1]['KCNTOMS'] / 5), auto1])
        print(self.aop_23_auto['23_06'][0])

        # 23_06 자동 동작사항 2. 증기발생기 전열관 누설 시 증기발생기 취출수계통 고방사선경보가 발생하면 증기발생기 취출수 차단밸브(BM-HV103/203/303)와 시료채취 차단밸브(BM-HV107/207/307)가 닫히고 동시에 취출수 방사선감시기 시료채취 차단밸브(BM-RV410)가 자동으로 닫힌다.
        auto2 = 'Letdown valve closed'
        if db[-1]['BHV108'] == 0 and db[-1]['BHV208'] == 0 and db[-1]['BHV308'] == 0 and db[-1]['BLV459'] == 0:
            if np.shape(self.aop_23_auto['23_06'][1])[0] < 1:
                self.aop_23_auto['23_06'][1].append([int(db[-1]['KCNTOMS'] / 5), auto2])
        print(self.aop_23_auto['23_06'][1])

        # 23_06 자동 동작사항 3. Rx 트립(136.8㎏/㎠)
        auto3 = 'Reactor trip'
        if db[-1]['KLAMPO9'] == 1:
            if np.shape(self.aop_23_auto['23_06'][2])[0] < 1:
                self.aop_23_auto['23_06'][2].append([int(db[-1]['KCNTOMS'] / 5), auto3])
        print(self.aop_23_auto['23_06'][2])

        # 23_06 자동 동작사항 4. SI 작동(126.7㎏/㎠)
        auto4 = 'Safety Injection actuation'
        if db[-1]['KLAMPO6'] == 1:
            if np.shape(self.aop_23_auto['23_06'][3])[0] < 1:
                self.aop_23_auto['23_06'][3].append([int(db[-1]['KCNTOMS'] / 5), auto4])
        print(self.aop_23_auto['23_06'][3])


