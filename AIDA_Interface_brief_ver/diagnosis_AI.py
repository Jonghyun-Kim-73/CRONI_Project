import pickle
import numpy as np

class IC_Diagnosis_Pack:
    def __init__(self):
        self._set_up()

    def _set_up(self):
        # 1. Minmax_scaler 공통
        with open('./DB/min_max_scaler.pkl', 'rb') as f:
            self.minmax_scaler = pickle.load(f)
        # 2. 모델 로드
        self.multiple_xgbclassification = pickle.load(
            open('model/Lightgbm_max_depth_feature_137_200825.h5', 'rb'))  # multiclassova
        self.explainer = pickle.load(open('model/explainer.pkl', 'rb'))  # pickle로 저장하여 로드하면 더 빠름.

        # 3. 입렵 정보
        self.input_data = ['BPV145', 'ZCNDTK', 'CIODMPC', 'UCHGUT', 'BLV614', 'QPRZH', 'ZREAC', 'ZINST63', 'UNRHXUT',
                           'ZINST65', 'ZVCT', 'BHTV', 'CAXOFF', 'UPRZ', 'CRETIV', 'ZINST85', 'ZINST56', 'ZINST87',
                           'WSPRAY', 'BHV1', 'BRHCV', 'ZINST66', 'ZINST103', 'ZINST86', 'CXEMPCM', 'URHXUT', 'ZCOND',
                           'ZINST108', 'ZINST68', 'ZINST1', 'BPORV', 'BFV122', 'WBOAC', 'WFWLN1', 'WFWLN2', 'UHOLEG2',
                           'ZINST81', 'ZINST67', 'ULPHOUT', 'ZINST72', 'ZINST78', 'ZINST69', 'UFUELM', 'QOVER',
                           'UUPPPL',
                           'ZINST101', 'KBCDO15', 'ZINST79', 'KBCDO7', 'BFV488', 'WFWLN3', 'UAVLEG1', 'BFV479', 'UPRT',
                           'ZINST100', 'ZINST74', 'ZINST99', 'BFV478', 'ZINST2', 'ZINST80', 'UHOLEG1', 'ZINST71',
                           'WCHGNO',
                           'ZINST121', 'BPSV10', 'UCOLEG1', 'ZINST15', 'WDEWT', 'UAVLEG2', 'BFV498', 'UCOND', 'QPROLD',
                           'ZINST70', 'ZINST73', 'ZINST124', 'ZINST76', 'UCTMT', 'ZINST102', 'BLV459', 'BFV499',
                           'UCOLEG2',
                           'BFV489', 'ZINST77', 'ZINST75', 'UAVLEG3', 'EBOAC', 'UHOLEG3', 'UCOLEG3', 'ZAFWTK',
                           'UAVLEGM',
                           'BTV418', 'ZINST48', 'KLAMPO119', 'KLAMPO118', 'FRQGEN', 'PVAC', 'KBCDO22', 'BHV2',
                           'KLAMPO117',
                           'PVCT', 'KLAMPO28', 'KBCDO11', 'ZINST36', 'UAVLEGS', 'BHV6', 'ZINST3', 'KBCDO19', 'KBCDO6',
                           'ZINST26', 'KBCDO16', 'BHTBY', 'FSRMDPM', 'H2CONC', 'BHV22', 'BHV302', 'KLAMPO29', 'BFV13',
                           'KBCDO8', 'ZINST22', 'BHSV', 'KLAMPO15', 'BLV48', 'KBCDO5', 'KBCDO20', 'KBCDO10', 'BTV143',
                           'KLAMPO48', 'KLAMPO9', 'KLAMPO69', 'KBCDO4', 'KLAMPO221', 'KLAMPO241',
                           'KLAMPO234', 'KLAMPO198', 'BHV41', 'KLAMPO195', 'KFV610']
        self.text_set = {
            0: 'Normal: 정상',
            1: 'Ab21_01: 가압기 압력 채널 고장 "고"',
            2: 'Ab21_02: 가압기 압력 채널 고장 "저"',
            3: 'Ab20_04: 가압기 수위 채널 고장 "저"',
            4: 'Ab15_07: 증기발생기 수위 채널 고장 "저"',
            5: 'Ab15_08: 증기발생기 수위 채널 고장 "고"',
            6: 'Ab63_04: 제어봉 낙하',
            7: 'Ab63_02: 제어봉의 계속적인 삽입',
            8: 'Ab21_12: 가압기 PORV 열림',
            9: 'Ab19_02: 가압기 안전밸브 고장',
            10: 'Ab21_11: 가압기 살수밸브 고장 "열림"',
            11: 'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설 ',
            12: 'Ab60_02: 재생열교환기 전단부위 파열',
            13: 'Ab59_02: 충전수 유량조절밸즈 후단누설',
            14: 'Ab23_01: RCS에서 1차기기 냉각수 계통(CCW)으로 누설',
            15: 'Ab23_06: 증기발생기 전열관 누설'
        }
        self.parms_dict = {
            0: {'N': 'BPV145', 'D': 'PV145 VALVE POSITION (0.0-1.0)'},
            1: {'N': 'ZCNDTK', 'D': 'CONDENSATE STORAGE TANK LEVEL(M).'},
            2: {'N': 'CIODMPC', 'D': 'AVERAGE IODINE CONCENTRATION(%)'},
            3: {'N': 'UCHGUT', 'D': 'CHARGING LINE OUTLET TEMPERATURE'},
            4: {'N': 'BLV614', 'D': 'LV614, VCT LEVEL CONTROL VALVE POSITION'},
            5: {'N': 'QPRZH', 'D': 'PROPORTIONAL HEATER FRACTIONAL POWER.'},
            6: {'N': 'ZREAC', 'D': 'REACTOR VESSEL WATER LEVEL (M)'},
            7: {'N': 'ZINST63', 'D': 'PRZ LEVEL'},
            8: {'N': 'UNRHXUT', 'D': 'NRHX OUTLET TEMPERATURE.'},
            9: {'N': 'ZINST65', 'D': 'PRZ PRESSURE(WIDE RANGE)'},
            10: {'N': 'ZVCT', 'D': 'VOLUME CONTROL TANK LEVEL.'},
            11: {'N': 'BHTV', 'D': 'HP TURBIN CONTROL VALVE POSITION.'},
            12: {'N': 'CAXOFF', 'D': 'AXIAL OFFSET.'},
            13: {'N': 'UPRZ', 'D': 'PRZ TEMPERATURE.'},
            14: {'N': 'CRETIV', 'D': 'REACTIVITY.'},
            15: {'N': 'ZINST85', 'D': 'STEAM LINE 3 FLOW'},
            16: {'N': 'ZINST56', 'D': 'PRZ DELTA LEVEL'},
            17: {'N': 'ZINST87', 'D': 'STEAM LINE 1 FLOW'},
            18: {'N': 'WSPRAY', 'D': 'PRZ SPRAY FLOW FROM RCS LOOP#1 & #2'},
            19: {'N': 'BHV1', 'D': '45(HV1)  GPM ORIFICE VALVE POSITION'},
            20: {'N': 'BRHCV', 'D': 'REHEATER CONTROL VALVE POSITION (0-1)'},
            21: {'N': 'ZINST66', 'D': 'PRZ SPRAY FLOW'},
            22: {'N': 'ZINST103', 'D': 'FEEDWATER PUMP OUTLET PRESS'},
            23: {'N': 'ZINST86', 'D': 'STEAM LINE 2 FLOW'},
            24: {'N': 'CXEMPCM', 'D': 'AVERAGE XENON CONCENTRATION (PCM)'},
            25: {'N': 'URHXUT', 'D': 'RHX OUTLET TEMPERATURE.'},
            26: {'N': 'ZCOND', 'D': 'CONDENSER WATER LEVEL.'},
            27: {'N': 'ZINST108', 'D': 'CONDENSATE PUMP OUTLET PRESS'},
            28: {'N': 'ZINST68', 'D': 'LOOP 2 DELTA TEMP(NORM)'},
            29: {'N': 'ZINST1', 'D': 'POWER RANGE PERCENT POWER'},
            30: {'N': 'BPORV', 'D': 'POWER OPERATED RELIEF VALVE (PV445)POSITION.'},
            31: {'N': 'BFV122', 'D': 'CHARGING FLOW CONTROL VALVE(FV122) POSITION'},
            32: {'N': 'WBOAC', 'D': 'BORIC ACID FLOWRATE'},
            33: {'N': 'WFWLN1', 'D': 'FEEDWATER LINE #1 FLOW (KG/SEC).'},
            34: {'N': 'WFWLN2', 'D': 'FEEDWATER LINE #2 FLOW (KG/SEC).'},
            35: {'N': 'UHOLEG2', 'D': 'HOT-LEG #2 TEMPERATURE'},
            36: {'N': 'ZINST81', 'D': 'LOOP 1 FLOW'},
            37: {'N': 'ZINST67', 'D': 'LOOP 3 DELTA TEMP(NORM)'},
            38: {'N': 'ULPHOUT', 'D': 'TEMP OF LP HTR OUTLET WATER (DEG C)'},
            39: {'N': 'ZINST72', 'D': 'S/G 1 LEVEL(WIDE)'},
            40: {'N': 'ZINST78', 'D': 'S/G 1 LEVEL(NARROW)'},
            41: {'N': 'ZINST69', 'D': 'LOOP 1 DELTA TEMP(NORM)'},
            42: {'N': 'UFUELM', 'D': 'AVERAGE FUEL TEMPERATURE.'},
            43: {'N': 'QOVER', 'D': 'OVERPOWER DELTA-T.'},
            44: {'N': 'UUPPPL', 'D': 'CORE OUTLET TEMPERATURE.'},
            45: {'N': 'ZINST101', 'D': 'MAIN STEAM FLOW'},
            46: {'N': 'KBCDO15', 'D': 'SUBCOOLED TEMPERATURE MARGIN.'},
            47: {'N': 'ZINST79', 'D': 'LOOP 3 FLOW'},
            48: {'N': 'KBCDO7', 'D': 'CONTROL BANK D POSITION.'},
            49: {'N': 'BFV488', 'D': 'FW CONTROL VLV #2 POS (0-1)'},
            50: {'N': 'WFWLN3', 'D': 'FEEDWATER LINE #3 FLOW (KG/SEC).'},
            51: {'N': 'UAVLEG1', 'D': 'LOOP #1 AVERAGE TEMPERATURE.'},
            52: {'N': 'BFV479', 'D': 'FW BYPASS VLV #1 POS (0-1)'},
            53: {'N': 'UPRT', 'D': 'PRESSURE RELIEF TANK TEMPERATURE.'},
            54: {'N': 'ZINST100', 'D': 'FEEDWATER TEMP'},
            55: {'N': 'ZINST74', 'D': 'S/G 2 PRESSURE'},
            56: {'N': 'ZINST99', 'D': 'MAIN STEAM HEADER PRESSURE'},
            57: {'N': 'BFV478', 'D': 'FW CONTROL VLV #1 POS (0-1)'},
            58: {'N': 'ZINST2', 'D': 'INTERMEDIATE RANGE NEUTRON LEVEL'},
            59: {'N': 'ZINST80', 'D': 'LOOP 2 FLOW'},
            60: {'N': 'UHOLEG1', 'D': 'HOT-LEG #1 TEMPERATURE'},
            61: {'N': 'ZINST71', 'D': 'S/G 2 LEVEL(WIDE)'},
            62: {'N': 'WCHGNO', 'D': 'NORMAL CHARGING FLOW.'},
            63: {'N': 'ZINST121', 'D': 'CURRENT'},
            64: {'N': 'BPSV10', 'D': 'PSV10 VALVE POSITION.'},
            65: {'N': 'UCOLEG1', 'D': 'COLD-LEG #1 TEMPERATURE'},
            66: {'N': 'ZINST15', 'D': 'TEMP MISMATCH'},
            67: {'N': 'WDEWT', 'D': 'DEMI. WATER FLOWRATE'},
            68: {'N': 'UAVLEG2', 'D': 'LOOP #2 AVERAGE TEMPERATURE.'},
            69: {'N': 'BFV498', 'D': 'FW CONTROL VLV #3 POS (0-1)'},
            70: {'N': 'UCOND', 'D': 'TEMP OF WATER IN CONDENSER(DEG C)'},
            71: {'N': 'QPROLD', 'D': 'OLD VALUE OF QPROREL.'},
            72: {'N': 'ZINST70', 'D': 'S/G 3 LEVEL(WIDE)'},
            73: {'N': 'ZINST73', 'D': 'S/G 3 PRESSURE'},
            74: {'N': 'ZINST124', 'D': 'Generator Outpit (MWe)'},
            75: {'N': 'ZINST76', 'D': 'S/G 3 LEVEL(NARROW)'},
            76: {'N': 'UCTMT', 'D': 'CONTAINMENT TEMPERATURE.'},
            77: {'N': 'ZINST102', 'D': 'SECONDARY RADIATION'},
            78: {'N': 'BLV459', 'D': 'LETDOWN ISOLATION VALVE(LV459) POSITION'},
            79: {'N': 'BFV499', 'D': 'FW BYPASS VLV #3 POS (0-1)'},
            80: {'N': 'UCOLEG2', 'D': 'COLD-LEG #2 TEMPERATURE'},
            81: {'N': 'BFV489', 'D': 'FW BYPASS VLV #2 POS (0-1)'},
            82: {'N': 'ZINST77', 'D': 'S/G 2 LEVEL(NARROW)'},
            83: {'N': 'ZINST75', 'D': 'S/G 1 PRESSURE'},
            84: {'N': 'UAVLEG3', 'D': 'LOOP #3 AVERAGE TEMPERATURE.'},
            85: {'N': 'EBOAC', 'D': 'BORIC ACID BATCH'},
            86: {'N': 'UHOLEG3', 'D': 'HOT-LEG #3 TEMPERATURE'},
            87: {'N': 'UCOLEG3', 'D': 'COLD-LEG #3 TEMPERATURE'},
            88: {'N': 'ZAFWTK', 'D': 'AFW STORAGE TANK LEVEL (M)'},
            89: {'N': 'UAVLEGM', 'D': 'LOOP 1,2,3 AVERAGE TEMPERATURE(MEAN VALUE).'},
            90: {'N': 'BTV418', 'D': 'STEAM DUMP VALVE POS (0-1)'},
            91: {'N': 'ZINST48', 'D': 'PRT PRESSURE'},
            92: {'N': 'KLAMPO119', 'D': 'PRZ SPRAY FLOW AUTO/MANUAL'},
            93: {'N': 'KLAMPO118', 'D': 'BACK-UP HEATER ON'},
            94: {'N': 'FRQGEN', 'D': 'GENERATOR FREQUENCY (CYCLE/SEC)'},
            95: {'N': 'PVAC', 'D': 'VACCUM PRESSURE (MM HG)'},
            96: {'N': 'KBCDO22', 'D': 'GENERATOR OUTPUT MW'},
            97: {'N': 'BHV2', 'D': '60(HV2)  GPM ORIFICE VALVE POSITION'},
            98: {'N': 'KLAMPO117', 'D': 'PROP HEATERS MANUAL'},
            99: {'N': 'PVCT', 'D': 'VCT PRESSURE.'},
            100: {'N': 'KLAMPO28', 'D': 'CONTROL ROD MODE SELECT (AUTO)'},
            101: {'N': 'KBCDO11', 'D': 'INSERTION LIMIT.'},
            102: {'N': 'ZINST36', 'D': 'LETDOWN BACK PRESSURE'},
            103: {'N': 'UAVLEGS', 'D': 'SETPOINT FOR PRIMARY AVERAGE COOLANT TEMPERATURE (DEG. C).'},
            104: {'N': 'BHV6', 'D': 'HV6 VALVE POSITION'},
            105: {'N': 'ZINST3', 'D': 'SOURCE RANGE NEUTRON LEVEL'},
            106: {'N': 'KBCDO19', 'D': 'TURBINE SPEED RPM.'},
            107: {'N': 'KBCDO6', 'D': 'SHUTDOWN BANK A POSITION.'},
            108: {'N': 'ZINST26', 'D': 'CONTAINMENT PRESSURE'},
            109: {'N': 'KBCDO16', 'D': 'BORON CONCENTRATION.'},
            110: {'N': 'BHTBY', 'D': 'HP TURBINE BYPASS VALVE POSITION (0-1)'},
            111: {'N': 'FSRMDPM', 'D': 'START-UP RATE (DECADES/MIN).'},
            112: {'N': 'H2CONC', 'D': 'H2 CONCENTRATION.'},
            113: {'N': 'BHV22', 'D': 'SAFETY INJECTION VALVE(HV22) POSITION'},
            114: {'N': 'BHV302', 'D': 'COND STOR TK TO AFW SYS VLV POS (0-1).'},
            115: {'N': 'KLAMPO29', 'D': 'CONTROL ROD MODE SELECT (MANUAL SEQUENCE)'},
            116: {'N': 'BFV13', 'D': 'CONDENSATE RECIRCULATION VLV POSITION (0-1)'},
            117: {'N': 'KBCDO8', 'D': 'CONTROL BANK C POSITION.'},
            118: {'N': 'ZINST22', 'D': 'CONTAINMENT RADIATION'},
            119: {'N': 'BHSV', 'D': 'HP TURBINE STOP VALVE POSITION (0-1).'},
            120: {'N': 'KLAMPO15', 'D': 'CONTROL BANK D'},
            121: {'N': 'BLV48', 'D': 'COND TO COND STOR TK LVL CONT VLV (0-1)'},
            122: {'N': 'KBCDO5', 'D': 'SHUTDOWN BANK B POSITION.'},
            123: {'N': 'KBCDO20', 'D': 'LOAD SETPOINT MW.'},
            124: {'N': 'KBCDO10', 'D': 'CONTROL BANK A POSITION.'},
            125: {'N': 'BTV143', 'D': 'TV143, LETDOWN TEMP. DEMINERALIZER DEVERT VALVE POSITION'},
            126: {'N': 'KLAMPO48', 'D': 'FAN COOLERS(B)'},
            127: {'N': 'KLAMPO9', 'D': 'REACTOR TRIP'},
            128: {'N': 'KLAMPO69', 'D': 'CHARGING PUMP 3'},
            129: {'N': 'KBCDO4', 'D': 'SHUTDOWN BANK C POSITION.'},
            130: {'N': 'KLAMPO221', 'D': 'GEN BREAKER BREAKER'},
            131: {'N': 'KLAMPO241', 'D': 'FWP 1 START/STOP'},
            132: {'N': 'KLAMPO234', 'D': 'EXCITER BREAKER'},
            133: {'N': 'KLAMPO198', 'D': 'MAKE UP MODE START'},
            134: {'N': 'BHV41', 'D': 'EXCESS LETDOWN VALVE(HV41) POSITION'},
            135: {'N': 'KLAMPO195', 'D': 'TURBINE TRIP'},
            136: {'N': 'KFV610', 'D': 'BORIC ACID INJECTION VALVE (FV610) STATUS'}
        }

    def _minmax(self, mem):
        """ 데이터 min max 처리 """
        return self.minmax_scaler.transform([[mem[_]['Val'] for _ in self.input_data]])

    def _AI_abnormal_procedure_classifier(self, mem):
        """ 비정상 절차서 진단 AI """
        # 1. 진단 결과 생성
        ab_procedure_prediction=self.multiple_xgbclassification.predict(self._minmax(mem)) # Softmax 예측 값 출력
        sort_abnormal_procedure = np.argsort(ab_procedure_prediction, axis=1)[:,::-1]  # softmax 값에 대한 index 내림차순 정렬
        # 2. 결과 reshape
        ab_predict = ab_procedure_prediction[0]
        ab_sort_predict = sort_abnormal_procedure[0]
        return ab_predict, ab_sort_predict

    def get_Dig_result(self, mem):
        # 1. 비정상 절차서 진단
        ab_predict, ab_sort_predict = self._AI_abnormal_procedure_classifier(mem)
        # 2. 결과 반환
        # ab_dig_result = {0: {'N': 절차서명, 'P': 1번째 확률값}, ... }
        ab_dig_result = {i: {'N': self.text_set[ab_sort_predict[i]],
                             'P': round(ab_predict[ab_sort_predict[i]] * 100, 2)}
                         for i in [0, 1, 2]}
        return ab_dig_result

    def get_XAI_result(self, mem):
        """ 비정상 XAI """
        # 1. shap_value 생성
        shap_value = self.explainer.shap_values(self._minmax(mem))  # Shap_value 출력
        # 2. 비정상 절차서 진단
        ab_predict, ab_sort_predict = self._AI_abnormal_procedure_classifier(mem)
        # 3. 가공
        p_nub, v_nub = 3, 5 # 절차서 3개 shap 값 5개 # TODO  XAITable 의 Max Cell이 v_nub 임. 동일하게 값 맞출 것
        shap_ab = [abs(shap_value[ab_sort_predict[i]]) for i in range(p_nub)]  # 절차서 3개까지 보여줌
        shap_ab_sort = [np.argsort(_, axis=1)[:, ::-1][0] for _ in shap_ab]
        # 4. shap value, name 계산
        shap_result = {}
        for pro_nub in range(p_nub):
            for val_nub in range(v_nub):
                shap_result[pro_nub][f'SHAP_VAL{val_nub}'] = round(shap_ab[:, shap_ab_sort[val_nub]][0] / np.sum(shap_ab) * 100, 0)
                shap_result[pro_nub][f'SHAP_NAME{val_nub}'] = self.parms_dict[shap_ab_sort[val_nub]]['N']
                shap_result[pro_nub][f'SHAP_DESC{val_nub}'] = self.parms_dict[shap_ab_sort[val_nub]]['D']
        # shap_result { 0 번 절차서: {'SHAP_VAL1': .. , 'SHAP_NAME1': ... , 2.... 3... 4... 5...,
        #             { 1 번 ....
        #             { 2 번 ....
        return shap_result