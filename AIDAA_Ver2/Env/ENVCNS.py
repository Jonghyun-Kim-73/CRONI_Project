import numpy as np
from AIDAA_Ver2.TOOL.TOOL_CNS_UDP_FAST import CNS
from AIDAA_Ver2.TOOL.TOOL_etc import AlarmCheck, Actprob, CLogic

import random


class CMem:
    def __init__(self, mem):
        self.m = mem  # Line CNSmem -> getmem

        self.StartRL = 0

        self.update()

    def update(self):
        self.CTIME = self.m['KCNTOMS']['Val']       # CNS Time

        # Physical
        self.SG1Nar = self.m['ZINST78']['Val']
        self.SG2Nar = self.m['ZINST77']['Val']
        self.SG3Nar = self.m['ZINST76']['Val']

        self.SG1Wid = self.m['ZINST72']['Val']
        self.SG2Wid = self.m['ZINST71']['Val']
        self.SG3Wid = self.m['ZINST70']['Val']

        self.SG1Pres = self.m['ZINST75']['Val']
        self.SG2Pres = self.m['ZINST74']['Val']
        self.SG3Pres = self.m['ZINST73']['Val']

        self.SG1Feed = self.m['WFWLN1']['Val']
        self.SG2Feed = self.m['WFWLN2']['Val']
        self.SG3Feed = self.m['WFWLN3']['Val']

        self.SG1FeedValveM = self.m['KLAMPO147']['Val']
        self.SG2FeedValveM = self.m['KLAMPO148']['Val']
        self.SG3FeedValveM = self.m['KLAMPO149']['Val']

        self.Aux1Flow = self.m['WAFWS1']['Val']
        self.Aux2Flow = self.m['WAFWS2']['Val']
        self.Aux3Flow = self.m['WAFWS3']['Val']

        self.SteamLine1 = self.m['BHV108']['Val']
        self.SteamLine2 = self.m['BHV208']['Val']
        self.SteamLine3 = self.m['BHV308']['Val']

        self.AVGTemp = self.m['UAVLEG2']['Val']
        self.PZRPres = self.m['ZINST65']['Val']         # display
        self.PZRPresRaw = self.m['PPRZ']['Val']         # raw
        self.PZRLevel = self.m['ZINST63']['Val']        # display
        self.PZRLevelRaw = self.m['ZPRZNO']['Val']      # raw

        # Signal
        self.Tavgref = self.m['ZINST15']['Val']
        self.Trip = self.m['KLAMPO9']['Val']
        self.SIS = self.m['KLAMPO6']['Val']
        self.MSI = self.m['KLAMPO3']['Val']
        self.NetBRK = self.m['KLAMPO224']['Val']

        # Comp
        self.RCP1 = self.m['KLAMPO124']['Val']
        self.RCP2 = self.m['KLAMPO125']['Val']
        self.RCP3 = self.m['KLAMPO126']['Val']

        self.TurningGear = self.m['KLAMPO165']['Val']
        self.OilSys = self.m['KLAMPO164']['Val']
        self.BHV311 = self.m['BHV311']['Val']

        self.SteamDumpPos = self.m['ZINST98']['Val']
        self.SteamDumpManAuto = self.m['KLAMPO150']['Val']

        self.PMSS = self.m['PMSS']['Val']

        # 강화학습을 위한 감시 변수
        self.PZRSprayManAuto = self.m['KLAMPO119']['Val']
        self.PZRSprayPos = self.m['ZINST66']['Val']
        self.PZRSprayPosControl = self.m['BPRZSP']['Val']

        self.PZRBackHeaterOnOff = self.m['KLAMPO118']['Val']
        self.PZRProHeaterManAuto = self.m['KLAMPO117']['Val']
        self.PZRProHeaterPos = self.m['QPRZH']['Val']

        self.SIValve = self.m['BHV22']['Val']

        self.ChargingManAUto = self.m['KLAMPO95']['Val']
        self.ChargingValvePos = round(self.m['BFV122']['Val'], 2)
        self.ChargingPump2State = self.m['KLAMPO70']['Val']

        self.LetdownLV459Pos = self.m['BLV459']['Val']
        self.LetdownHV1Pos = self.m['BHV1']['Val']
        self.LetdownHV2Pos = self.m['BHV2']['Val']
        self.LetdownHV3Pos = self.m['BHV3']['Val']

        self.HV41 = self.m['BHV41']['Val']
        self.HV43 = self.m['KHV43']['Val']

        # Logic
        if self.CTIME == 0:
            self.StartRL = 0

        # --------------------------------------------------------------------------------------------------------------
        # 현재 발생 비정상 확인
        self.abnub = {
            'AB2101': True if self.m['cMALC']['Val'] == 19 and self.m['cMALO']['Val'] > 155 else False,
            'AB2102': True if self.m['cMALC']['Val'] == 19 and self.m['cMALO']['Val'] < 155 else False,
            'AB2001': True if self.m['cMALC']['Val'] == 20 and self.m['cMALO']['Val'] > 95 else False,
            'AB2004': True if self.m['cMALC']['Val'] == 20 and self.m['cMALO']['Val'] < 15 else False,
            'AB1507': True if self.m['cMALC']['Val'] == 30 and (1000 < self.m['cMALO']['Val'] < 1050 or
                                                                2000 < self.m['cMALO']['Val'] < 2050 or
                                                                3000 < self.m['cMALO']['Val'] < 3050) else False,
            'AB1508': True if self.m['cMALC']['Val'] == 30 and (1050 < self.m['cMALO']['Val'] < 1100 or
                                                                2050 < self.m['cMALO']['Val'] < 2100 or
                                                                3050 < self.m['cMALO']['Val'] < 3100) else False,
            'AB6304': True if self.m['cMALC']['Val'] == 2 else False,
            'AB2112': True if self.m['cMALC']['Val'] == 15 else False,
            'AB1902': True if self.m['cMALC']['Val'] == 16 else False,  # No op
            'AB2111': True if self.m['cMALC']['Val'] == 22 else False,
            'AB5901': True if self.m['cMALC']['Val'] == 35 else False,
            'AB8002': True if self.m['cMALC']['Val'] == 67 else False,  # No op
            'AB6403': True if self.m['cMALC']['Val'] == 50 else False,
            'AB6002': True if self.m['cMALC']['Val'] == 36 else False,
            'AB2303': True if self.m['cMALC']['Val'] == 37 else False,  # Same 36
            'AB5902': True if self.m['cMALC']['Val'] == 38 else False,
            'AB2301': True if self.m['cMALC']['Val'] == 12 else False,
            'AB2306': True if self.m['cMALC']['Val'] == 13 else False,  # No op
        }
        self.curab = ''
        for key in self.abnub.keys():
            if self.abnub[key]:
                self.curab = key

        # ab_normal operator
        if self.CTIME == 0:
            self.ab2101 = {'S1': True, 'S2': False, 'S3': False, 'S4': False, 'S5': False}
            self.ab2102 = {'S1': True, 'S2': False, 'S3': False}
            self.ab2001 = {'S1': True, 'S2': False}
            self.ab2004 = {'S1': True, 'S2': False}
            self.ab1507 = {'S1': True, 'S2': False, 'S3': False, 'S4': False}
            self.ab1508 = {'S1': True, 'S2': False, 'S3': False, 'S4': False}
            self.ab6304 = {'S1': True, 'S2': False}
            self.ab2112 = {'S1': True, 'S2': False, 'S3': False, 'S3Try': 0, 'S4': False, 'S4Try': 0, 'S5': False}
            self.ab1902 = {'S1': True, 'S2': False}
            self.ab2111 = {'S1': True, 'S2': False, 'S3': False, 'S3Try': 0, 'S4': False}
            self.ab5901 = {'S1': True, 'S2': False, 'S2Try': 0, 'S3': False, 'S4': False}
            self.ab6403 = {'S1': True, 'S2': False, 'S2Try': 0, 'S3': False, 'S4': False}
            self.ab6002 = {'S1': True, 'S2': False, 'S3': False, 'S4': False, 'S5': False, 'S6': False,
                           'S7': False, 'S8': False}
            self.ab5902 = {'S1': True, 'S2': False, 'S3': False, 'S4': False, 'S5': False}
            self.ab2301 = {'S1': True, 'S2': False, 'S3': False, 'S4': False, 'S4Try': random.randint(1, 3) * 60,
                           'S5': False, 'S6': False}
        else:
            if self.abnub['AB2101']:
                # 알람 인지
                if self.ab2101['S1'] and self.m['KLAMPO308']['Val'] == 1:
                    if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                        self.ab2101['S1'], self.ab2101['S2'] = False, True
                elif self.ab2101['S2']:
                    if self.PZRProHeaterPos == 1:
                        self.ab2101['S2'], self.ab2101['S3'] = False, True
                elif self.ab2101['S3']:
                    if self.PZRPresRaw > 154 * 1e5:
                        self.ab2101['S3'], self.ab2101['S4'] = False, True
                elif self.ab2101['S4']:
                    if self.PZRProHeaterPos == 0:
                        self.ab2101['S4'], self.ab2101['S5'] = False, True
            if self.abnub['AB2102']:
                # 알람 인지
                if self.ab2102['S1'] and self.m['KLAMPO307']['Val'] == 1:
                    if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                        self.ab2102['S1'], self.ab2102['S2'] = False, True
                elif self.ab2102['S2']:
                    if self.PZRProHeaterPos == 0:
                        self.ab2102['S2'], self.ab2102['S3'] = False, True
            if self.abnub['AB2001']:
                if self.ab2001['S1'] and self.m['KLAMPO266']['Val'] == 1:
                    if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                        self.ab2001['S1'], self.ab2001['S2'] = False, True
            if self.abnub['AB2004']:
                if self.ab2004['S1'] and self.m['KLAMPO274']['Val'] == 1:
                    if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                        self.ab2004['S1'], self.ab2004['S2'] = False, True
            if self.abnub['AB1507']:
                if self.ab1507['S1'] and self.m['KLAMPO320']['Val'] == 1:
                    if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                        self.ab1507['S1'], self.ab1507['S2'] = False, True
                        if 1000 < self.m['cMALO']['Val'] < 1050:
                            self.abSG = 1
                        elif 2000 < self.m['cMALO']['Val'] < 2050:
                            self.abSG = 2
                        elif 3000 < self.m['cMALO']['Val'] < 3050:
                            self.abSG = 3
                        else:
                            self.abSG = 4  # error
                            print('Error AB 1507 SG')
                if self.ab1507['S2']:
                    if self.abSG == 1 and self.SG1FeedValveM == 1:
                        self.ab1507['S2'], self.ab1507['S3'] = False, True
                    if self.abSG == 2 and self.SG2FeedValveM == 1:
                        self.ab1507['S2'], self.ab1507['S3'] = False, True
                    if self.abSG == 3 and self.SG3FeedValveM == 1:
                        self.ab1507['S2'], self.ab1507['S3'] = False, True
                if self.ab1507['S3']:
                    targetBypass = self.m[{1: 'BFV479', 2: 'BFV489', 3: 'BFV499'}[self.abSG]]['Val']
                    if targetBypass < 0.44:
                        self.ab1507['S3'], self.ab1507['S4'] = False, True
            if self.abnub['AB1508']:
                if self.ab1508['S1'] and self.m['KLAMPO320']['Val'] == 1:
                    if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                        self.ab1508['S1'], self.ab1508['S2'] = False, True
                        if 1050 < self.m['cMALO']['Val'] < 1100:
                            self.abSG = 1
                        elif 2050 < self.m['cMALO']['Val'] < 2100:
                            self.abSG = 2
                        elif 3050 < self.m['cMALO']['Val'] < 3100:
                            self.abSG = 3
                        else:
                            self.abSG = 4  # error
                            print('Error AB 1507 SG')
                if self.ab1508['S2']:
                    if self.abSG == 1 and self.SG1FeedValveM == 1:
                        self.ab1508['S2'], self.ab1508['S3'] = False, True
                    if self.abSG == 2 and self.SG2FeedValveM == 1:
                        self.ab1508['S2'], self.ab1508['S3'] = False, True
                    if self.abSG == 3 and self.SG3FeedValveM == 1:
                        self.ab1508['S2'], self.ab1508['S3'] = False, True
                if self.ab1508['S3']:
                    targetBypass = self.m[{1: 'BFV479', 2: 'BFV489', 3: 'BFV499'}[self.abSG]]['Val']
                    if targetBypass > 0.44:
                        self.ab1508['S3'], self.ab1508['S4'] = False, True
            if self.abnub['AB6304']:
                if self.ab6304['S1'] and (self.m['KLAMPO313']['Val'] == 1 or self.m['QPROREL']['Val'] < 0.99):
                    if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                        self.ab6304['S1'], self.ab6304['S2'] = False, True
            if self.abnub['AB2112']:
                if self.ab2112['S1'] and self.m['BPORV']['Val'] != 0:
                    if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                        self.ab2112['S1'], self.ab2112['S2'] = False, True
                if self.ab2112['S2'] and self.m['KLAMPO110']['Val'] == 1:  # 메뉴얼 인지
                    if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                        self.ab2112['S2'], self.ab2112['S3'] = False, True
                if self.ab2112['S3Try'] > 5:
                    self.ab2112['S3'], self.ab2112['S4'] = False, True
                if self.ab2112['S4Try'] > 5:
                    self.ab2112['S4'], self.ab2112['S5'] = False, True
            if self.abnub['AB1902']:
                # no op
                pass
            if self.abnub['AB2111']:
                if self.ab2111['S1'] and self.m['KLAMPO312']['Val'] != 0: # PZR 보조 전열기 켜짐 인지
                    self.ab2111['S1'], self.ab2111['S2'] = CLogic(0.3)
                if self.ab2111['S2'] and self.PZRSprayManAuto == 1: # PZR 스프레이 Man 인지
                    self.ab2111['S2'], self.ab2111['S3'] = CLogic(0.3)
                if self.ab2111['S3'] and self.ab2111['S3Try'] > 5: # PZR 스프레이 감소 몇번 클릭 시도 후 종료
                    self.ab2111['S3'], self.ab2111['S4'] = CLogic(0.3)
            if self.abnub['AB5901']:
                if self.ab5901['S1'] and self.m['KLAMPO265']['Val'] != 0: # RCP Seal Inj wtr low 알람 인지
                    self.ab5901['S1'], self.ab5901['S2'] = CLogic(0.3)
                if self.ab5901['S2'] and self.ab5901['S2Try'] > 5: # 인지 후 Ch 1 기동 시도
                    self.ab5901['S2'], self.ab5901['S3'] = CLogic(0.3)
                if self.ab5901['S3'] and self.m['KLAMPO70']['Val'] == 1: # Charging 2 번 기동 인지
                    self.ab5901['S3'], self.ab5901['S4'] = CLogic(0.3)
            if self.abnub['AB6403']:
                if self.ab6403['S1'] and self.m['KLAMPO320']['Val'] != 0: # STM/FW Flow deviation 알람 인지
                    self.ab6403['S1'], self.ab6403['S2'] = CLogic(0.3)
                if self.ab6403['S2'] and self.ab6403['S2Try'] > 5: # 인지 후 잠긴 MSIB 기동 시도
                    self.ab6403['S2'], self.ab6403['S3'] = CLogic(0.3)
                if self.ab6403['S3'] and self.m['KLAMPO9']['Val'] == 1: # ManTrip 인지 후 종료
                    self.ab6403['S3'], self.ab6403['S4'] = CLogic(0.3)
            if self.abnub['AB6002']:
                if self.ab6002['S1'] and self.m['KLAMPO260']['Val'] != 0: # 유출유로 저 유랸 알람 인지
                    self.ab6002['S1'], self.ab6002['S2'] = CLogic(0.2)
                if self.ab6002['S2'] and self.LetdownHV1Pos == 0 and self.LetdownHV2Pos == 0 and self.LetdownHV3Pos == 0:
                    self.ab6002['S2'], self.ab6002['S3'] = CLogic(0.3) # 유출 유로 차단 후 Letdown Valve 차단
                if self.ab6002['S3'] and self.LetdownLV459Pos == 0:
                    self.ab6002['S3'], self.ab6002['S4'] = CLogic(0.3)  # Letdown Valve 차단
                if self.ab6002['S4'] and self.ChargingValvePos == 0.1:
                    self.ab6002['S4'], self.ab6002['S5'] = CLogic(0.3)  # Charging Valve 차단 + HV41 대체 유로
                if self.ab6002['S5'] and self.HV41 == 1:    # 대체 유로 전환 시작
                    self.ab6002['S5'], self.ab6002['S6'] = CLogic(0.3)
                if self.ab6002['S6'] and self.HV43 == 1:   # 대체 유로 전환 완료 및 charging 유량 조절
                    self.ab6002['S6'], self.ab6002['S7'] = CLogic(0.3)
                if self.ab6002['S7'] and self.ChargingManAUto == 1:
                    self.ab6002['S7'], self.ab6002['S8'] = CLogic(0.3)
            if self.abnub['AB5902']:
                if self.ab5902['S1'] and self.m['KLAMPO266']['Val'] != 0:  # 유출수 온도 지시계 증가
                    self.ab5902['S1'], self.ab5902['S2'] = CLogic(0.2)
                if self.ab5902['S2'] and self.LetdownHV1Pos == 0 and self.LetdownHV2Pos == 0 and self.LetdownHV3Pos == 0:
                    self.ab5902['S2'], self.ab5902['S3'] = CLogic(0.3) # 유출 유로 차단 후 Letdown Valve 차단
                if self.ab5902['S3'] and self.LetdownLV459Pos == 0:
                    self.ab5902['S3'], self.ab5902['S4'] = CLogic(0.3)  # Letdown 차단 후 Charging Valve Man 전환
                if self.ab5902['S4'] and self.ChargingManAUto == 1:
                    self.ab5902['S4'], self.ab5902['S5'] = CLogic(0.3)  # Charging Man -> Close 시작
            if self.abnub['AB2301']:
                if self.ab2301['S1'] and self.m['KLAMPO312']['Val'] != 0:  # 저압으로 히터 자동 기동 확인
                    self.ab2301['S1'], self.ab2301['S2'] = CLogic(0.2)
                if self.ab2301['S2'] and self.ChargingManAUto == 1:  # 충전 유량 수동 전환 확인 -> Open 시작
                    self.ab2301['S2'], self.ab2301['S3'] = CLogic(0.3)
                if self.ab2301['S3'] and self.ChargingValvePos == 1:    # 충전 100% open -> 1~3 min 대기 시작
                    self.ab2301['S3'], self.ab2301['S4'] = CLogic(0.3)
                if self.ab2301['S4'] and self.ab2301['S4Try'] < 0:
                    self.ab2301['S4'], self.ab2301['S5'] = CLogic(0.3)  # 1~3 min 대기 -> 유량 복구 (불가능) 인지 및 Chp 추가 기동
                if self.ab2301['S5'] and self.ChargingPump2State == 1:
                    self.ab2301['S5'], self.ab2301['S6'] = CLogic(0.3)  # Charging pump 추가 기동 인지. -> 가압기 수위 조절


class ENVCNS(CNS):
    def __init__(self, Name, IP, PORT, RIP, RPORT, Max_len):
        super(ENVCNS, self).__init__(threrad_name=Name,
                                     CNS_IP=IP, CNS_Port=PORT,
                                     Remote_IP=RIP, Remote_Port=RPORT, Max_len=Max_len)
        self.Name = Name  # = id
        self.ENVStep = 0
        self.LoggerPath = 'DB/Log'
        self.want_tick = 5  # 1sec

        self.Loger_txt = ''

        self.CMem = CMem(self.mem)

        self.input_info_EM = [
            # (para, x_round, x_min, x_max), (x_min=0, x_max=0 is not normalized.)
            ('ZINST98', 1, 0, 100),  # SteamDumpPos
        ]

        self.overwrite_acts = []
        # --------------------------------------------------------------------------------------------------------------

    def normalize(self, x, x_round, x_min, x_max):
        if x_max == 0 and x_min == 0:
            # It means X value is not normalized.
            x = x / x_round
        else:
            x = x_max if x >= x_max else x
            x = x_min if x <= x_min else x
            x = (x - x_min) / (x_max - x_min)
        return x

    def get_state(self, input_info):
        state = []
        for para, x_round, x_min, x_max in input_info:
            if para in self.mem.keys():
                _ = self.mem[para]['Val']
            else:
                if para == 'DSetPoint':
                    _ = 0
                else:
                    _ = None
                # ------------------------------------------------------------------------------------------------------
                if _ is None:
                    raise ValueError(f'{para} is not in self.input_info')
                # ------------------------------------------------------------------------------------------------------
            state.append(self.normalize(_, x_round, x_min, x_max))
        return np.array(state), state

    def _send_control_save(self, zipParaVal):
        for para_, para_val in zip(zipParaVal[0], zipParaVal[1]):
            self.overwrite_acts.append((para_, para_val))

        super(ENVCNS, self)._send_control_save(para=zipParaVal[0], val=zipParaVal[1])

    def _send_act_EM_Module(self, A):
        pass

    def _send_act_AB_DB_Module(self, A):
        print('Alarms : ', AlarmCheck(self.CMem.m))

        ActOrderBook = {
            'StopAllRCP': (['KSWO132', 'KSWO133', 'KSWO134'], [0, 0, 0]),
            'StopRCP1': (['KSWO132'], [0]),
            'StopRCP2': (['KSWO133'], [0]),
            'StopRCP3': (['KSWO134'], [0]),
            'NetBRKOpen': (['KSWO244'], [0]),
            'OilSysOff': (['KSWO190'], [0]),
            'TurningGearOff': (['KSWO191'], [0]),
            'CutBHV311': (['BHV311', 'FKAFWPI'], [0, 0]),

            'PZRSprayMan': (['KSWO128'], [1]), 'PZRSprayAuto': (['KSWO128'], [0]),

            'PZRSprayClose': (['BPRZSP'], [self.mem['BPRZSP']['Val'] + 0.015 * -1]),
            'PZRSprayOpen': (['BPRZSP'], [self.mem['BPRZSP']['Val'] + 0.015 * 1]),
            'PZRSprayOepnBtn': (['KSWO126', 'KSWO127'], [0, 1]),
            'PZRSprayCloseBtn': (['KSWO126', 'KSWO127'], [1, 0]),

            'PZRBackHeaterOff': (['KSWO125'], [0]), 'PZRBackHeaterOn': (['KSWO125'], [1]),

            'SteamDumpMan': (['KSWO176'], [1]), 'SteamDumpAuto': (['KSWO176'], [0]),

            'IFLOGIC_SteamDumpUp': (['PMSS'], [self.CMem.PMSS + 2.0E5 * 3 * 0.2]),
            'IFLOGIC_SteamDumpDown': (['PMSS'], [self.CMem.PMSS + 2.0E5 * (-3) * 0.2]),

            'DecreaseAux1Flow': (['KSWO142', 'KSWO143'], [1, 0]),
            'IncreaseAux1Flow': (['KSWO142', 'KSWO143'], [0, 1]),
            'DecreaseAux2Flow': (['KSWO151', 'KSWO152'], [1, 0]),
            'IncreaseAux2Flow': (['KSWO151', 'KSWO152'], [0, 1]),
            'DecreaseAux3Flow': (['KSWO154', 'KSWO155'], [1, 0]),
            'IncreaseAux3Flow': (['KSWO154', 'KSWO155'], [0, 1]),

            'SteamLine1Open': (['KSWO148', 'KSWO149'], [1, 0]),
            'SteamLine1Close': (['KSWO148', 'KSWO149'], [0, 1]),
            'SteamLine2Open': (['KSWO146', 'KSWO147'], [1, 0]),
            'SteamLine2Close': (['KSWO146', 'KSWO147'], [0, 1]),
            'SteamLine3Open': (['KSWO144', 'KSWO145'], [1, 0]),
            'SteamLine3Close': (['KSWO144', 'KSWO145'], [0, 1]),

            'ResetSI': (['KSWO7', 'KSWO5'], [1, 1]),
            'ManTrip': (['KSWO9'], [1]),

            'PZRProHeaterMan': (['KSWO120'], [1]), 'PZRProHeaterAuto': (['KSWO120'], [0]),
            'PZRProHeaterDown': (['KSWO121', 'KSWO122'], [1, 0]),
            'PZRProHeaterUp': (['KSWO121', 'KSWO122'], [0, 1]),

            'RL_IncreaseAux1Flow': (['WAFWS1'], [self.mem['WAFWS1']['Val'] + 0.04 * 1]),
            'RL_DecreaseAux1Flow': (['WAFWS1'], [self.mem['WAFWS1']['Val'] + 0.04 * (-1)]),
            'RL_IncreaseAux2Flow': (['WAFWS2'], [self.mem['WAFWS2']['Val'] + 0.04 * 1]),
            'RL_DecreaseAux2Flow': (['WAFWS2'], [self.mem['WAFWS2']['Val'] + 0.04 * (-1)]),
            'RL_IncreaseAux3Flow': (['WAFWS3'], [self.mem['WAFWS3']['Val'] + 0.04 * 1]),
            'RL_DecreaseAux3Flow': (['WAFWS3'], [self.mem['WAFWS3']['Val'] + 0.04 * (-1)]),

            'ChargingValveMan': (['KSWO100'], [1]), 'ChargingValveAUto': (['KSWO100'], [0]),
            'ChargingValveDown': (['KSWO101', 'KSWO102'], [1, 0]),
            'ChargingValveUp': (['KSWO101', 'KSWO102'], [0, 1]),
            'ChargingValveStay': (['KSWO101', 'KSWO102'], [0, 0]),

            'LetdownLV459Open': (['KSWO114', 'KSWO113'], [1, 0]),
            'LetdownLV459Close': (['KSWO114', 'KSWO113'], [0, 1]),

            'LetdownHV1Open': (['KSWO104', 'KSWO103'], [1, 0]),
            'LetdownHV1Close': (['KSWO104', 'KSWO103'], [0, 1]),
            'LetdownHV2Open': (['KSWO106', 'KSWO105'], [1, 0]),
            'LetdownHV2Close': (['KSWO106', 'KSWO105'], [0, 1]),
            'LetdownHV3Open': (['KSWO108', 'KSWO107'], [1, 0]),
            'LetdownHV3Close': (['KSWO108', 'KSWO107'], [0, 1]),

            'RunRCP2': (['KSWO130', 'KSWO133'], [1, 1]),
            'RunCHP1': (['KSWO71'], [1]), 'StopCHP1': (['KSWO71'], [0]),
            'RunCHP2': (['KSWO70'], [1]), 'StopCHP2': (['KSWO70'], [0]),
            'RunCHP3': (['KSWO69'], [1]), 'StopCHP3': (['KSWO69'], [0]),

            'OpenSI': (['KSWO81', 'KSWO82'], [1, 0]), 'CloseSI': (['KSWO81', 'KSWO82'], [0, 1]),

            'Feed1Man': (['KSWO171', 'KSWO168'], [1, 1]),
            'Feed1ValveClose': (['KSWO172', 'KSWO173'], [1, 0]),
            'Feed1ValveStay': (['KSWO172', 'KSWO173'], [0, 0]),
            'Feed1ValveOpen': (['KSWO172', 'KSWO173'], [0, 1]),
            'Feed1BypassClose': (['KSWO169', 'KSWO170'], [1, 0]),
            'Feed1BypassStay': (['KSWO169', 'KSWO170'], [0, 0]),
            'Feed1BypassOpen': (['KSWO169', 'KSWO170'], [0, 1]),

            'Feed2Man': (['KSWO165', 'KSWO162'], [1, 1]),
            'Feed2ValveClose': (['KSWO166', 'KSWO167'], [1, 0]),
            'Feed2ValveStay': (['KSWO166', 'KSWO167'], [0, 0]),
            'Feed2ValveOpen': (['KSWO166', 'KSWO167'], [0, 1]),
            'Feed2BypassClose': (['KSWO163', 'KSWO164'], [1, 0]),
            'Feed2BypassStay': (['KSWO163', 'KSWO164'], [0, 0]),
            'Feed2BypassOpen': (['KSWO163', 'KSWO164'], [0, 1]),

            'Feed3Man': (['KSWO159', 'KSWO156'], [1, 1]),
            'Feed3ValveClose': (['KSWO160', 'KSWO161'], [1, 0]),
            'Feed3ValveStay': (['KSWO160', 'KSWO161'], [0, 0]),
            'Feed3ValveOpen': (['KSWO160', 'KSWO161'], [0, 1]),
            'Feed3BypassClose': (['KSWO157', 'KSWO158'], [1, 0]),
            'Feed3BypassStay': (['KSWO157', 'KSWO158'], [0, 0]),
            'Feed3BypassOpen': (['KSWO157', 'KSWO158'], [0, 1]),

            'LoadSetDown': (['KSWO225', 'KSWO224'], [0, 1]),
            'LoadSetUp': (['KSWO225', 'KSWO224'], [1, 0]),

            'PZRPORVMan': (['KSWO115'], [1]),
            'PZRPORVAuto': (['KSWO115'], [0]),
            'PZRPORVClose': (['KSWO119', 'KSWO118'], [1, 0]),
            'PZRPORVOpen': (['KSWO119', 'KSWO118'], [0, 1]),
            'HV6Open': (['KSWO124', 'KSWO123'], [0, 1]),
            'HV6Close': (['KSWO124', 'KSWO123'], [1, 0]),

            'HV41Open': (['KSWO110', 'KSWO109'], [1, 0]),
            'HV41Close': (['KSWO110', 'KSWO109'], [0, 1]),
            'HV43Up': (['KSWO112', 'KSWO111'], [1, 0]),
            'HV43Right': (['KSWO112', 'KSWO111'], [0, 1]),
        }
        if self.CMem.abnub['AB2101']:
            if self.CMem.ab2101['S2']:
                # 1. 알람 발생 인지 가압기 히터 On
                self._send_control_save(ActOrderBook['PZRProHeaterMan'])
                self._send_control_save(ActOrderBook['PZRBackHeaterOn'])
                self._send_control_save(ActOrderBook['PZRProHeaterUp'])
            if self.CMem.ab2101['S3']:
                # 2. 히터 모두 킴. 스프레이 잠그기
                self._send_control_save(ActOrderBook['PZRSprayMan'])
                self._send_control_save(ActOrderBook['PZRSprayClose'])
            if self.CMem.ab2101['S4']:
                # 3. 압력 처음으로 정상화 히터 잠그기
                self._send_control_save(ActOrderBook['PZRBackHeaterOff'])
                self._send_control_save(ActOrderBook['PZRProHeaterDown'])
            if self.CMem.ab2101['S5']:
                # 4. 목표 압력 내로 유지하도록 스프레이 조절
                if self.CMem.PZRPresRaw > 154.05 * 1e5 and int(np.random.choice(2, 1, p=[0.6, 0.4])[0]) == 1:
                    self._send_control_save(ActOrderBook['PZRSprayOpen'])
                if self.CMem.PZRPresRaw < 154.00 * 1e5 and int(np.random.choice(2, 1, p=[0.6, 0.4])[0]) == 1:
                    self._send_control_save(ActOrderBook['PZRSprayClose'])
        if self.CMem.abnub['AB2102']:
            if self.CMem.ab2102['S2']:
                # 1. 알람 발생 인지 가압기 히터 Off
                self._send_control_save(ActOrderBook['PZRProHeaterMan'])
                self._send_control_save(ActOrderBook['PZRBackHeaterOff'])
                self._send_control_save(ActOrderBook['PZRProHeaterDown'])
            if self.CMem.ab2102['S3']:
                # 2. 목표 압력 내로 유지하도록 스프레이 조절
                self._send_control_save(ActOrderBook['PZRSprayMan'])
                if self.CMem.PZRPresRaw > 154.05 * 1e5 and int(np.random.choice(2, 1, p=[0.6, 0.4])[0]) == 1:
                    self._send_control_save(ActOrderBook['PZRSprayOpen'])
                if self.CMem.PZRPresRaw < 154.00 * 1e5 and int(np.random.choice(2, 1, p=[0.6, 0.4])[0]) == 1:
                    self._send_control_save(ActOrderBook['PZRSprayClose'])
        if self.CMem.abnub['AB2001'] or self.CMem.abnub['AB2004']:
            if self.CMem.ab2001['S2'] or self.CMem.ab2004['S2']:
                # 1. 알람 발생 인지 Charging Man 및 조절
                self._send_control_save(ActOrderBook['ChargingValveMan'])
                if self.CMem.PZRLevelRaw < 0.54:
                    self._send_control_save(ActOrderBook['ChargingValveUp'])
                if self.CMem.PZRLevelRaw > 0.56:
                    self._send_control_save(ActOrderBook['ChargingValveDown'])
        if self.CMem.abnub['AB1507']:
            if self.CMem.ab1507['S2']:
                # 관련 밸브 Manual
                self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}Man'])
                for i in range(1, 4):
                    self._send_control_save(ActOrderBook[f'Feed{i}ValveStay'])
                    self._send_control_save(ActOrderBook[f'Feed{i}BypassStay'])
            if self.CMem.ab1507['S3'] or self.CMem.ab1507['S4']:
                # 선 Bypass 정상화 후 Main feed 조작
                targetBypass = self.CMem.m[{1: 'BFV479', 2: 'BFV489', 3: 'BFV499'}[self.CMem.abSG]]['Val']
                if targetBypass > 0.44:
                    self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}BypassClose'])
                else:
                    self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}BypassStay'])
                if self.CMem.ab1507['S4']:
                    # Main feed 조작
                    targetSGW = self.CMem.m[{1: 'ZINST72', 2: 'ZINST71', 3: 'ZINST70'}[self.CMem.abSG]]['Val']
                    if targetSGW > 89.5:
                        if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                            self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}ValveClose'])
                        else:
                            self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}ValveStay'])
                    elif targetSGW < 86.5:
                        if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                            self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}ValveOpen'])
                        else:
                            self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}ValveStay'])
                    else:
                        self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}ValveStay'])
        if self.CMem.abnub['AB1508']:
            if self.CMem.ab1508['S2']:
                # 관련 밸브 Manual
                self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}Man'])
                for i in range(1, 4):
                    self._send_control_save(ActOrderBook[f'Feed{i}ValveStay'])
                    self._send_control_save(ActOrderBook[f'Feed{i}BypassStay'])
            if self.CMem.ab1508['S3'] or self.CMem.ab1508['S4']:
                # 선 Bypass 정상화 후 Main feed 조작
                targetBypass = self.CMem.m[{1: 'BFV479', 2: 'BFV489', 3: 'BFV499'}[self.CMem.abSG]]['Val']
                if targetBypass < 0.44:
                    self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}BypassOpen'])
                else:
                    self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}BypassStay'])
                if self.CMem.ab1508['S4']:
                    # Main feed 조작
                    targetSGW = self.CMem.m[{1: 'ZINST72', 2: 'ZINST71', 3: 'ZINST70'}[self.CMem.abSG]]['Val']
                    if targetSGW > 89.5:
                        if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                            self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}ValveClose'])
                        else:
                            self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}ValveStay'])
                    elif targetSGW < 86.5:
                        if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                            self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}ValveOpen'])
                        else:
                            self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}ValveStay'])
                    else:
                        self._send_control_save(ActOrderBook[f'Feed{self.CMem.abSG}ValveStay'])
        if self.CMem.abnub['AB6304']:
            if self.CMem.ab6304['S2']:
                # Tavg/ref +- 1 내로 터빈 출력 감소
                if self.CMem.Tavgref > 1:
                    if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                        self._send_control_save(ActOrderBook['LoadSetDown'])
        if self.CMem.abnub['AB2112']:
            if self.CMem.ab2112['S2']:
                # PZR PORV 개방 인지 후 매뉴얼 전환
                if int(np.random.choice(2, 1, p=[0.7, 0.3])[0]) == 1:
                    self._send_control_save(ActOrderBook['PZRPORVMan'])
            if self.CMem.ab2112['S3']:
                self.CMem.ab2112['S3Try'] += 1
                self._send_control_save(ActOrderBook['PZRPORVClose'])
            if self.CMem.ab2112['S4']:
                self.CMem.ab2112['S4Try'] += 1
                self._send_control_save(ActOrderBook['HV6Close'])
        if self.CMem.abnub['AB2111']:
            # PZR 보조 전열기 켜짐 인지 후 스프레이 Man
            if self.CMem.ab2111['S2']:
                Actprob(0.3, self._send_control_save(ActOrderBook['PZRSprayMan']))
            # PZR Spray 닫으려고 시도
            if self.CMem.ab2111['S3']:
                self.CMem.ab2111['S3Try'] += 1
                Actprob(0.3, self._send_control_save(ActOrderBook['PZRSprayCloseBtn']))
        if self.CMem.abnub['AB5901']:
            # 경보 인지 후 Ch 1 재기도 시도
            if self.CMem.ab5901['S2']:
                self.CMem.ab5901['S2Try'] += 1
                Actprob(0.3, self._send_control_save(ActOrderBook['RunCHP1']))
            if self.CMem.ab5901['S3']:
                Actprob(0.3, self._send_control_save(ActOrderBook['RunCHP2']))
        if self.CMem.abnub['AB6403']:
            # 경보 인지 후 고장난 MSIV 재기동 시도
            if self.CMem.ab6403['S2']:
                self.CMem.ab6403['S2Try'] += 1
                Actprob(0.3, self._send_control_save(ActOrderBook['RunCHP1']))
                if self.CMem.m['cMALO']['Val'] == 1:
                    self.overwrite_acts.append(('KSWO148', 1))
                if self.CMem.m['cMALO']['Val'] == 2:
                    self.overwrite_acts.append(('KSWO146', 1))
                if self.CMem.m['cMALO']['Val'] == 3:
                    self.overwrite_acts.append(('KSWO144', 1))
            if self.CMem.ab6403['S3']: # 수동 정지
                Actprob(0.3, self._send_control_save(ActOrderBook['ManTrip']))
        if self.CMem.abnub['AB6002']:
            # 경보 인지 후 유출수 계통 차단
            if self.CMem.ab6002['S2']:
                if self.CMem.LetdownHV3Pos == 1:
                    Actprob(0.3, self._send_control_save(ActOrderBook['LetdownHV3Close']))
                else:
                    if self.CMem.LetdownHV2Pos == 1:
                        Actprob(0.3, self._send_control_save(ActOrderBook['LetdownHV2Close']))
                    else:
                        if self.CMem.LetdownHV1Pos == 1:
                            Actprob(0.3, self._send_control_save(ActOrderBook['LetdownHV1Close']))
                        else:
                            pass
            # Letdown Valve 차단
            if self.CMem.ab6002['S3']:
                Actprob(0.3, self._send_control_save(ActOrderBook['LetdownLV459Close']))
            # Charging Valve 차단
            if self.CMem.ab6002['S4']:
                if self.CMem.ChargingManAUto == 1: # Manual Mode
                    if self.CMem.ChargingValvePos != 0.1:
                        Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveDown']))
                    else:
                        pass
                else:
                    Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveMan']))
            # 유로 개방
            if self.CMem.ab6002['S5']:
                if self.CMem.HV41 == 0:
                    Actprob(0.3, self._send_control_save(ActOrderBook['HV41Open']))
            # 유로 전환
            if self.CMem.ab6002['S6']:
                if self.CMem.HV43 == 0:
                    Actprob(0.3, self._send_control_save(ActOrderBook['HV43Right']))
            # Charging Valve Man
            if self.CMem.ab6002['S7']:
                Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveMan']))
            # 전환 완료 및 Charging 을 통한 유량 조절
            if self.CMem.ab6002['S8']:
                if self.CMem.PZRLevel > 55.1:
                    Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveDown']))
                elif self.CMem.PZRLevel < 55.1:
                    Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveUp']))
                else:
                    Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveStay']))
        if self.CMem.abnub['AB5902']:
            # 유출 유로 차단
            if self.CMem.ab5902['S2']:
                if self.CMem.LetdownHV3Pos == 1:
                    Actprob(0.3, self._send_control_save(ActOrderBook['LetdownHV3Close']))
                else:
                    if self.CMem.LetdownHV2Pos == 1:
                        Actprob(0.3, self._send_control_save(ActOrderBook['LetdownHV2Close']))
                    else:
                        if self.CMem.LetdownHV1Pos == 1:
                            Actprob(0.3, self._send_control_save(ActOrderBook['LetdownHV1Close']))
                        else:
                            pass
            # Letdown 차단
            if self.CMem.ab5902['S3']:
                Actprob(0.3, self._send_control_save(ActOrderBook['LetdownLV459Close']))
            # Charging Valve Man
            if self.CMem.ab5902['S4']:
                Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveMan']))
            # Charging Valve Close
            if self.CMem.ab5902['S5']:
                Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveDown']))
        if self.CMem.abnub['AB2301']:
            # 히터 가동 인지 충전 밸브 Man
            if self.CMem.ab2301['S2']:
                Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveMan']))
            # 충전 Man 인지 충전 밸브 100%
            if self.CMem.ab2301['S3']:
                if self.CMem.ChargingValvePos != 1:
                    Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveUp']))
            # 3~5 min 대기 시작
            if self.CMem.ab2301['S4']:
                self.CMem.ab2301['S4Try'] -= 1
            # Charging pp 추가 기동
            if self.CMem.ab2301['S5']:
                if self.CMem.ChargingPump2State == 0:
                    Actprob(0.3, self._send_control_save(ActOrderBook['RunCHP2']))
            # 가압기 수위 조절
            if self.CMem.ab2301['S6']:
                if self.CMem.PZRLevel > 55.1:
                    Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveDown']))
                elif self.CMem.PZRLevel < 55.1:
                    Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveUp']))
                else:
                    Actprob(0.3, self._send_control_save(ActOrderBook['ChargingValveStay']))

    def send_act(self, A):
        """
        A 에 해당하는 액션을 보내고 나머지는 자동
        E.x)
            self._send_control_save(['KSWO115'], [0])
            ...
            self._send_control_to_cns()
        :param A: A 액션 [0, 0, 0] <- act space에 따라서
        :return: AMod: 수정된 액션
        """
        AMod = A

        if isinstance(A, int):      # A=0 인경우
            pass
        elif isinstance(A, dict):   # A = { ... } 각 AI 모듈에 정보가 들어있는 경우
            if 'EM' in A.keys():
                pass
            elif 'AB' in A.keys():
                self._send_act_AB_DB_Module(A)
            else:
                print('-')
        else:
            print('Error')

        # Done Act
        self._send_control_to_cns()
        return AMod

    def save_line_with_act(self):
        """ t 상태에 t-1 액션을 오버라이드 """
        for key, val in self.overwrite_acts:    # 이전의 액션 값을 메모리에 업데이트
            self.mem[key]['Val'] = val
        self.save_line()    # 메모리에 저장된 값을 저장
        self.overwrite_acts.clear() # 액션 오버라이트용 청소

    def step(self, A):
        """
        A를 받고 1 step 전진
        :param A: A -> dict
        :return: 최신 state와 reward done 반환
        """
        # Old Data (time t) ---------------------------------------
        AMod = self.send_act(A)
        self.want_tick = int(5)
        print(self.want_tick, self.CMem.CTIME)

        # New Data (time t+1) -------------------------------------
        super(ENVCNS, self).step() # 전체 CNS mem run-Freeze 하고 mem 업데이트

        # 이전 액션이 CNS 내부에서 사라지는 경우 대응
        self.save_line_with_act()

        self.CMem.update()  # 선택 변수 mem 업데이트

        self._append_val_to_list()
        self.ENVStep += 1

        # next_state, next_state_list = self.get_state(self.input_info)  # [s(t+1)] #
        # ----------------------------------------------------------
        return 0

    def reset(self, file_name, initial_nub=1, mal=False, mal_case=1, mal_opt=0, mal_time=5):
        # 1] CNS 상태 초기화 및 초기화된 정보 메모리에 업데이트
        super(ENVCNS, self).reset(initial_nub=initial_nub, mal=False, mal_case=1, mal_opt=0, mal_time=5, file_name=file_name)
        # 2] 업데이트된 'Val'를 'List'에 추가 및 ENVLogging 초기화
        self._append_val_to_list()
        # 3] ENVStep 초기화
        self.ENVStep = 0
        # 5 FIX RADVAL
        self.FixedRad = random.randint(0, 20) * 5
        return 0


if __name__ == '__main__':
    # ENVCNS TEST
    env = ENVCNS(Name='Env1', IP='192.168.0.103', PORT=int(f'7101'))
    # Run
    for _ in range(1, 4):
        env.reset(file_name=f'Ep{_}')
        for __ in range(500):
            A = 0
            env.step(A)