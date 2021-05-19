import pickle
import numpy as np


class Data_module:
    def __init__(self):
        with open('./DB/min_max_scaler.pkl', 'rb') as f:
            self.minmax_scaler = pickle.load(f)

    def make_input_data(self, mem):
        # input_data = [
        #     mem['BPV145']['Val'], mem['ZCNDTK']['Val'], mem['CIODMPC']['Val'], mem['UCHGUT']['Val'],
        #     mem['BLV614']['Val'],
        #     mem['QPRZH']['Val'], mem['ZREAC']['Val'], mem['ZINST63']['Val'], mem['UNRHXUT']['Val'],
        #     mem['ZINST65']['Val'],
        #     mem['ZVCT']['Val'], mem['BHTV']['Val'], mem['CAXOFF']['Val'], mem['UPRZ']['Val'], mem['CRETIV']['Val'],
        #     mem['ZINST85']['Val'], mem['ZINST56']['Val'], mem['ZINST87']['Val'], mem['WSPRAY']['Val'],
        #     mem['BHV1']['Val'],
        #     mem['BRHCV']['Val'], mem['ZINST66']['Val'], mem['ZINST103']['Val'], mem['ZINST86']['Val'],
        #     mem['CXEMPCM']['Val'],
        #     mem['URHXUT']['Val'], mem['ZCOND']['Val'], mem['ZINST108']['Val'], mem['ZINST68']['Val'],
        #     mem['ZINST1']['Val'],
        #     mem['BPORV']['Val'], mem['BFV122']['Val'], mem['WBOAC']['Val'], mem['WFWLN1']['Val'], mem['WFWLN2']['Val'],
        #     mem['UHOLEG2']['Val'], mem['ZINST81']['Val'], mem['ZINST67']['Val'], mem['ULPHOUT']['Val'],
        #     mem['ZINST72']['Val'],
        #     mem['ZINST78']['Val'], mem['ZINST69']['Val'], mem['UFUELM']['Val'], mem['QOVER']['Val'],
        #     mem['UUPPPL']['Val'],
        #     mem['ZINST101']['Val'], mem['KBCDO15']['Val'], mem['ZINST79']['Val'], mem['KBCDO7']['Val'],
        #     mem['BFV488']['Val'],
        #     mem['WFWLN3']['Val'], mem['UAVLEG1']['Val'], mem['BFV479']['Val'], mem['UPRT']['Val'],
        #     mem['ZINST100']['Val'],
        #     mem['ZINST74']['Val'], mem['ZINST99']['Val'], mem['BFV478']['Val'], mem['ZINST2']['Val'],
        #     mem['ZINST80']['Val'],
        #     mem['UHOLEG1']['Val'], mem['ZINST71']['Val'], mem['WCHGNO']['Val'], mem['ZINST121']['Val'],
        #     mem['BPSV10']['Val'],
        #     mem['UCOLEG1']['Val'], mem['ZINST15']['Val'], mem['WDEWT']['Val'], mem['UAVLEG2']['Val'],
        #     mem['BFV498']['Val'],
        #     mem['UCOND']['Val'], mem['QPROLD']['Val'], mem['ZINST70']['Val'], mem['ZINST73']['Val'],
        #     mem['ZINST124']['Val'],
        #     mem['ZINST76']['Val'], mem['UCTMT']['Val'], mem['ZINST102']['Val'], mem['BLV459']['Val'],
        #     mem['BFV499']['Val'],
        #     mem['UCOLEG2']['Val'], mem['BFV489']['Val'], mem['ZINST77']['Val'], mem['ZINST75']['Val'],
        #     mem['UAVLEG3']['Val'],
        #     mem['EBOAC']['Val'], mem['UHOLEG3']['Val'], mem['UCOLEG3']['Val'], mem['ZAFWTK']['Val'],
        #     mem['UAVLEGM']['Val'],
        #     mem['BTV418']['Val'], mem['ZINST48']['Val'], mem['KLAMPO119']['Val'], mem['KLAMPO118']['Val'],
        #     mem['FRQGEN']['Val'],
        #     mem['PVAC']['Val'], mem['KBCDO22']['Val'], mem['BHV2']['Val'], mem['KLAMPO117']['Val'], mem['PVCT']['Val'],
        #     mem['KLAMPO28']['Val'], mem['KBCDO11']['Val'], mem['ZINST36']['Val'], mem['UAVLEGS']['Val'],
        #     mem['BHV6']['Val'],
        #     mem['ZINST3']['Val'], mem['KBCDO19']['Val'], mem['KBCDO6']['Val'], mem['ZINST26']['Val'],
        #     mem['KBCDO16']['Val'],
        #     mem['BHTBY']['Val'], mem['FSRMDPM']['Val'], mem['H2CONC']['Val'], mem['BHV22']['Val'], mem['BHV302']['Val'],
        #     mem['KLAMPO29']['Val'], mem['BFV13']['Val'], mem['KBCDO8']['Val'], mem['ZINST22']['Val'],
        #     mem['BHSV']['Val'],
        #     mem['KLAMPO15']['Val'], mem['BLV48']['Val'], mem['KBCDO5']['Val'], mem['KBCDO20']['Val'],
        #     mem['KBCDO10']['Val'],
        #     mem['BTV143']['Val'], mem['KLAMPO48']['Val'], mem['KLAMPO9']['Val'], mem['KLAMPO69']['Val'],
        #     mem['KBCDO4']['Val'],
        #     mem['KLAMPO221']['Val'], mem['KLAMPO241']['Val'], mem['KLAMPO234']['Val'], mem['KLAMPO198']['Val'],
        #     mem['BHV41']['Val'],
        #     mem['KLAMPO195']['Val'], mem['KFV610']['Val']
        # ]

        self.input_data = [
            mem.get_shmem_val('BPV145'), mem.get_shmem_val('ZCNDTK'), mem.get_shmem_val('CIODMPC'),
            mem.get_shmem_val('UCHGUT'), mem.get_shmem_val('BLV614'), mem.get_shmem_val('QPRZH'),
            mem.get_shmem_val('ZREAC'), mem.get_shmem_val('ZINST63'), mem.get_shmem_val('UNRHXUT'),
            mem.get_shmem_val('ZINST65'), mem.get_shmem_val('ZVCT'), mem.get_shmem_val('BHTV'),
            mem.get_shmem_val('CAXOFF'), mem.get_shmem_val('UPRZ'), mem.get_shmem_val('CRETIV'),
            mem.get_shmem_val('ZINST85'), mem.get_shmem_val('ZINST56'), mem.get_shmem_val('ZINST87'),
            mem.get_shmem_val('WSPRAY'), mem.get_shmem_val('BHV1'), mem.get_shmem_val('BRHCV'),
            mem.get_shmem_val('ZINST66'), mem.get_shmem_val('ZINST103'), mem.get_shmem_val('ZINST86'),
            mem.get_shmem_val('CXEMPCM'), mem.get_shmem_val('URHXUT'), mem.get_shmem_val('ZCOND'),
            mem.get_shmem_val('ZINST108'), mem.get_shmem_val('ZINST68'), mem.get_shmem_val('ZINST1'),
            mem.get_shmem_val('BPORV'), mem.get_shmem_val('BFV122'), mem.get_shmem_val('WBOAC'),
            mem.get_shmem_val('WFWLN1'), mem.get_shmem_val('WFWLN2'), mem.get_shmem_val('UHOLEG2'),
            mem.get_shmem_val('ZINST81'), mem.get_shmem_val('ZINST67'), mem.get_shmem_val('ULPHOUT'),
            mem.get_shmem_val('ZINST72'), mem.get_shmem_val('ZINST78'), mem.get_shmem_val('ZINST69'),
            mem.get_shmem_val('UFUELM'), mem.get_shmem_val('QOVER'), mem.get_shmem_val('UUPPPL'),
            mem.get_shmem_val('ZINST101'), mem.get_shmem_val('KBCDO15'), mem.get_shmem_val('ZINST79'),
            mem.get_shmem_val('KBCDO7'), mem.get_shmem_val('BFV488'), mem.get_shmem_val('WFWLN3'),
            mem.get_shmem_val('UAVLEG1'), mem.get_shmem_val('BFV479'), mem.get_shmem_val('UPRT'),
            mem.get_shmem_val('ZINST100'), mem.get_shmem_val('ZINST74'), mem.get_shmem_val('ZINST99'),
            mem.get_shmem_val('BFV478'), mem.get_shmem_val('ZINST2'), mem.get_shmem_val('ZINST80'),
            mem.get_shmem_val('UHOLEG1'), mem.get_shmem_val('ZINST71'), mem.get_shmem_val('WCHGNO'),
            mem.get_shmem_val('ZINST121'), mem.get_shmem_val('BPSV10'), mem.get_shmem_val('UCOLEG1'),
            mem.get_shmem_val('ZINST15'), mem.get_shmem_val('WDEWT'), mem.get_shmem_val('UAVLEG2'),
            mem.get_shmem_val('BFV498'), mem.get_shmem_val('UCOND'), mem.get_shmem_val('QPROLD'),
            mem.get_shmem_val('ZINST70'), mem.get_shmem_val('ZINST73'), mem.get_shmem_val('ZINST124'),
            mem.get_shmem_val('ZINST76'), mem.get_shmem_val('UCTMT'), mem.get_shmem_val('ZINST102'),
            mem.get_shmem_val('BLV459'), mem.get_shmem_val('BFV499'), mem.get_shmem_val('UCOLEG2'),
            mem.get_shmem_val('BFV489'), mem.get_shmem_val('ZINST77'), mem.get_shmem_val('ZINST75'),
            mem.get_shmem_val('UAVLEG3'), mem.get_shmem_val('EBOAC'), mem.get_shmem_val('UHOLEG3'),
            mem.get_shmem_val('UCOLEG3'), mem.get_shmem_val('ZAFWTK'), mem.get_shmem_val('UAVLEGM'),
            mem.get_shmem_val('BTV418'), mem.get_shmem_val('ZINST48'), mem.get_shmem_val('KLAMPO119'),
            mem.get_shmem_val('KLAMPO118'), mem.get_shmem_val('FRQGEN'), mem.get_shmem_val('PVAC'),
            mem.get_shmem_val('KBCDO22'), mem.get_shmem_val('BHV2'), mem.get_shmem_val('KLAMPO117'),
            mem.get_shmem_val('PVCT'), mem.get_shmem_val('KLAMPO28'), mem.get_shmem_val('KBCDO11'),
            mem.get_shmem_val('ZINST36'), mem.get_shmem_val('UAVLEGS'), mem.get_shmem_val('BHV6'),
            mem.get_shmem_val('ZINST3'), mem.get_shmem_val('KBCDO19'), mem.get_shmem_val('KBCDO6'),
            mem.get_shmem_val('ZINST26'), mem.get_shmem_val('KBCDO16'), mem.get_shmem_val('BHTBY'),
            mem.get_shmem_val('FSRMDPM'), mem.get_shmem_val('H2CONC'), mem.get_shmem_val('BHV22'),
            mem.get_shmem_val('BHV302'), mem.get_shmem_val('KLAMPO29'), mem.get_shmem_val('BFV13'),
            mem.get_shmem_val('KBCDO8'), mem.get_shmem_val('ZINST22'), mem.get_shmem_val('BHSV'),
            mem.get_shmem_val('KLAMPO15'), mem.get_shmem_val('BLV48'), mem.get_shmem_val('KBCDO5'),
            mem.get_shmem_val('KBCDO20'), mem.get_shmem_val('KBCDO10'), mem.get_shmem_val('BTV143'),
            mem.get_shmem_val('KLAMPO48'), mem.get_shmem_val('KLAMPO9'), mem.get_shmem_val('KLAMPO69'),
            mem.get_shmem_val('KBCDO4'), mem.get_shmem_val('KLAMPO221'), mem.get_shmem_val('KLAMPO241'),
            mem.get_shmem_val('KLAMPO234'), mem.get_shmem_val('KLAMPO198'), mem.get_shmem_val('BHV41'),
            mem.get_shmem_val('KLAMPO195'), mem.get_shmem_val('KFV610')
        ]
        self.out_minmax = self.minmax_scaler.transform([self.input_data])
        return self.out_minmax

class Model_module:
    def __init__(self):
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

    def load_model(self):
        self.multiple_xgbclassification = pickle.load(
            open('model/Lightgbm_max_depth_feature_137_200825.h5', 'rb'))  # multiclassova
        self.explainer = pickle.load(open('model/explainer.pkl', 'rb'))  # pickle로 저장하여 로드하면 더 빠름.

    def AI_abnormal_procedure_classifier(self, data):
        self.abnormal_procedure_prediction = self.multiple_xgbclassification.predict(data) # Softmax 예측 값 출력
        self.sort_abnormal_procedure = np.argsort(self.abnormal_procedure_prediction, axis=1)[:,::-1] # softmax 값에 대한 index 내림차순 정렬
        # return self.abnormal_procedure_prediction, self.diagnosed_scenario
        return self.abnormal_procedure_prediction, self.sort_abnormal_procedure

    def XAI_explainer(self, data):
        self.shap_value = self.explainer.shap_values(data)  # Shap_value 출력

        self.shap_1stab = abs(self.shap_value[self.sort_abnormal_procedure[0][0]])
        self.shap_1stab_sort = np.argsort(self.shap_1stab, axis=1)[:, ::-1]

        self.shap_2ndab = abs(self.shap_value[self.sort_abnormal_procedure[0][1]])
        self.shap_2ndab_sort = np.argsort(self.shap_2ndab, axis=1)[:, ::-1]

        self.shap_3rdab = abs(self.shap_value[self.sort_abnormal_procedure[0][2]])
        self.shap_3rdab_sort = np.argsort(self.shap_3rdab, axis=1)[:, ::-1]

        return self.shap_1stab, self.shap_2ndab, self.shap_3rdab, self.shap_1stab_sort, self.shap_2ndab_sort, self.shap_3rdab_sort

    def shap_val_1(self):
        self.shap_val_1stab = [
            round(self.shap_1stab[:, self.shap_1stab_sort[0][0]][0] / np.sum(self.shap_1stab) * 100, 0),
            round(self.shap_1stab[:, self.shap_1stab_sort[0][1]][0] / np.sum(self.shap_1stab) * 100, 0),
            round(self.shap_1stab[:, self.shap_1stab_sort[0][2]][0] / np.sum(self.shap_1stab) * 100, 0),
            round(self.shap_1stab[:, self.shap_1stab_sort[0][3]][0] / np.sum(self.shap_1stab) * 100, 0),
            round(self.shap_1stab[:, self.shap_1stab_sort[0][4]][0] / np.sum(self.shap_1stab) * 100, 0)
        ]
        return self.shap_val_1stab

    def shap_val_2(self):
        self.shap_val_2ndab = [
            round(self.shap_2ndab[:, self.shap_2ndab_sort[0][0]][0] / np.sum(self.shap_2ndab) * 100, 0),
            round(self.shap_2ndab[:, self.shap_2ndab_sort[0][1]][0] / np.sum(self.shap_2ndab) * 100, 0),
            round(self.shap_2ndab[:, self.shap_2ndab_sort[0][2]][0] / np.sum(self.shap_2ndab) * 100, 0),
            round(self.shap_2ndab[:, self.shap_2ndab_sort[0][3]][0] / np.sum(self.shap_2ndab) * 100, 0),
            round(self.shap_2ndab[:, self.shap_2ndab_sort[0][4]][0] / np.sum(self.shap_2ndab) * 100, 0)
        ]
        return self.shap_val_2ndab

    def shap_val_3(self):
        self.shap_val_3rdab = [
            round(self.shap_3rdab[:, self.shap_3rdab_sort[0][0]][0] / np.sum(self.shap_3rdab) * 100, 0),
            round(self.shap_3rdab[:, self.shap_3rdab_sort[0][1]][0] / np.sum(self.shap_3rdab) * 100, 0),
            round(self.shap_3rdab[:, self.shap_3rdab_sort[0][2]][0] / np.sum(self.shap_3rdab) * 100, 0),
            round(self.shap_3rdab[:, self.shap_3rdab_sort[0][3]][0] / np.sum(self.shap_3rdab) * 100, 0),
            round(self.shap_3rdab[:, self.shap_3rdab_sort[0][4]][0] / np.sum(self.shap_3rdab) * 100, 0)
        ]
        return self.shap_val_3rdab

    def shap_name_1(self):
        self.shap_name_1stab = [
            str(self.parms_dict[self.shap_1stab_sort[0][0]]['N'].strip()),
            str(self.parms_dict[self.shap_1stab_sort[0][1]]['N'].strip()),
            str(self.parms_dict[self.shap_1stab_sort[0][2]]['N'].strip()),
            str(self.parms_dict[self.shap_1stab_sort[0][3]]['N'].strip()),
            str(self.parms_dict[self.shap_1stab_sort[0][4]]['N'].strip())
        ]
        return self.shap_name_1stab

    def shap_name_2(self):
        self.shap_name_2ndab = [
            str(self.parms_dict[self.shap_2ndab_sort[0][0]]['N'].strip()),
            str(self.parms_dict[self.shap_2ndab_sort[0][1]]['N'].strip()),
            str(self.parms_dict[self.shap_2ndab_sort[0][2]]['N'].strip()),
            str(self.parms_dict[self.shap_2ndab_sort[0][3]]['N'].strip()),
            str(self.parms_dict[self.shap_2ndab_sort[0][4]]['N'].strip())
        ]
        return self.self.shap_name_2ndab

    def shap_name_3(self):
        self.shap_name_3rdab = [
            str(self.parms_dict[self.shap_3rdab_sort[0][0]]['N'].strip()),
            str(self.parms_dict[self.shap_3rdab_sort[0][1]]['N'].strip()),
            str(self.parms_dict[self.shap_3rdab_sort[0][2]]['N'].strip()),
            str(self.parms_dict[self.shap_3rdab_sort[0][3]]['N'].strip()),
            str(self.parms_dict[self.shap_3rdab_sort[0][4]]['N'].strip())
        ]
        return self.shap_name_3rdab

    def shap_descr_1(self):
        self.shap_desc_1stab = [
            self.parms_dict[self.shap_1stab_sort[0][0]]['D'].strip(),
            self.parms_dict[self.shap_1stab_sort[0][1]]['D'].strip(),
            self.parms_dict[self.shap_1stab_sort[0][2]]['D'].strip(),
            self.parms_dict[self.shap_1stab_sort[0][3]]['D'].strip(),
            self.parms_dict[self.shap_1stab_sort[0][4]]['D'].strip()
        ]
        return self.shap_desc_1stab

    def shap_descr_2(self):
        self.shap_desc_2ndab = [
            self.parms_dict[self.shap_2ndab_sort[0][0]]['D'].strip(),
            self.parms_dict[self.shap_2ndab_sort[0][1]]['D'].strip(),
            self.parms_dict[self.shap_2ndab_sort[0][2]]['D'].strip(),
            self.parms_dict[self.shap_2ndab_sort[0][3]]['D'].strip(),
            self.parms_dict[self.shap_2ndab_sort[0][4]]['D'].strip()
        ]
        return self.shap_desc_2ndab

    def shap_descr_3(self):
        self.shap_desc_3rdab = [
            self.parms_dict[self.shap_3rdab_sort[0][0]]['D'].strip(),
            self.parms_dict[self.shap_3rdab_sort[0][1]]['D'].strip(),
            self.parms_dict[self.shap_3rdab_sort[0][2]]['D'].strip(),
            self.parms_dict[self.shap_3rdab_sort[0][3]]['D'].strip(),
            self.parms_dict[self.shap_3rdab_sort[0][4]]['D'].strip()
        ]
        return self.shap_desc_3rdab




        # # 상위 첫번째 시나리오에 대한 XAI 결과
        # shap_1stab = abs(self.shap_value[self.abnormal_procedure_prediction[0][0]])
        # shap_1stab_sort = np.argsort(shap_1stab)[:, ::-1]
        # # 상위 5개 진단 근거
        # self.shap_1st_1 = round(shap_1stab[:, shap_1stab_sort[0][0]][0] / np.sum(shap_1stab)*100, 2)
        # self.shap_1st_2 = round(shap_1stab[:, shap_1stab_sort[0][1]][0] / np.sum(shap_1stab)*100, 2)
        # self.shap_1st_3 = round(shap_1stab[:, shap_1stab_sort[0][2]][0] / np.sum(shap_1stab)*100, 2)
        # self.shap_1st_4 = round(shap_1stab[:, shap_1stab_sort[0][3]][0] / np.sum(shap_1stab)*100, 2)
        # self.shap_1st_5 = round(shap_1stab[:, shap_1stab_sort[0][4]][0] / np.sum(shap_1stab)*100, 2)
        #
        # # 상위 두번째 시나리오에 대한 XAI 결과
        # shap_2ndab = abs(self.shap_value[self.abnormal_procedure_prediction[0][1]])
        # shap_2ndab_sort = np.argsort(shap_2ndab)[:, ::-1]
        # self.shap_2nd_1 = round(shap_2ndab[:, shap_2ndab_sort[0][0]][0] / np.sum(shap_2ndab)*100, 2)
        # self.shap_2nd_2 = round(shap_2ndab[:, shap_2ndab_sort[0][1]][0] / np.sum(shap_2ndab)*100, 2)
        # self.shap_2nd_3 = round(shap_2ndab[:, shap_2ndab_sort[0][2]][0] / np.sum(shap_2ndab)*100, 2)
        # self.shap_2nd_4 = round(shap_2ndab[:, shap_2ndab_sort[0][3]][0] / np.sum(shap_2ndab)*100, 2)
        # self.shap_2nd_5 = round(shap_2ndab[:, shap_2ndab_sort[0][4]][0] / np.sum(shap_2ndab)*100, 2)
        #
        # # 상위 세번째 시나리오에 대한 XAI 결과
        # shap_3rdab = abs(self.shap_value[self.abnormal_procedure_prediction[0][2]])
        # shap_3rdab_sort = np.argsort(shap_3rdab)[:, ::-1]
        # self.shap_3rd_1 = round(shap_3rdab[:, shap_3rdab_sort[0][0]][0] / np.sum(shap_3rdab)*100, 2)
        # self.shap_3rd_2 = round(shap_3rdab[:, shap_3rdab_sort[0][1]][0] / np.sum(shap_3rdab)*100, 2)
        # self.shap_3rd_3 = round(shap_3rdab[:, shap_3rdab_sort[0][2]][0] / np.sum(shap_3rdab)*100, 2)
        # self.shap_3rd_4 = round(shap_3rdab[:, shap_3rdab_sort[0][3]][0] / np.sum(shap_3rdab)*100, 2)
        # self.shap_3rd_5 = round(shap_3rdab[:, shap_3rdab_sort[0][4]][0] / np.sum(shap_3rdab)*100, 2)

    def Determine_procedure(self):
        self.first_ab_name = self.text_set[self.sort_abnormal_procedure[0][0]]
        self.second_ab_name = self.text_set[self.sort_abnormal_procedure[0][1]]
        self.third_ab_name = self.text_set[self.sort_abnormal_procedure[0][2]]
        self.first_ab_prob = round(self.abnormal_procedure_prediction[0][self.sort_abnormal_procedure[0][0]]*100, 2)
        self.second_ab_prob = round(self.abnormal_procedure_prediction[0][self.sort_abnormal_procedure[0][1]]*100, 2)
        self.third_ab_prob = round(self.abnormal_procedure_prediction[0][self.sort_abnormal_procedure[0][2]]*100, 2)
        print(self.first_ab_prob)
        print(self.second_ab_prob)
        print(self.third_ab_prob)
        self.diagnosis_result = {
            0: {'N': self.first_ab_name, 'P': self.first_ab_prob},
            1: {'N': self.second_ab_name, 'P': self.second_ab_prob},
            2: {'N': self.third_ab_name, 'P': self.third_ab_prob}
        }
        return self.diagnosis_result