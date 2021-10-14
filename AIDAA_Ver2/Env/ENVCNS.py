import numpy as np
from AIDAA_Ver2.TOOL.TOOL_CNS_UDP_FAST import CNS

import random


class CMem:
    def __init__(self, mem):
        self.m = mem  # Line CNSmem -> getmem
        self.CoolingRateSW = 0
        self.CoolingRateFixTemp = 0
        self.CoolingRateFixTime = 0

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

        self.Aux1Flow = self.m['WAFWS1']['Val']
        self.Aux2Flow = self.m['WAFWS2']['Val']
        self.Aux3Flow = self.m['WAFWS3']['Val']

        self.SteamLine1 = self.m['BHV108']['Val']
        self.SteamLine2 = self.m['BHV208']['Val']
        self.SteamLine3 = self.m['BHV308']['Val']

        self.AVGTemp = self.m['UAVLEG2']['Val']
        self.PZRPres = self.m['ZINST65']['Val']
        self.PZRLevel = self.m['ZINST63']['Val']

        # Signal
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
        self.ChargingValvePos = self.m['BFV122']['Val']
        self.ChargingPump2State = self.m['KLAMPO70']['Val']

        self.LetdownLV459Pos = self.m['BLV459']['Val']
        self.LetdownHV1Pos = self.m['BHV1']['Val']
        self.LetdownHV2Pos = self.m['BHV2']['Val']
        self.LetdownHV3Pos = self.m['BHV3']['Val']

        # Logic
        if self.CTIME == 0:
            self.CoolingRateSW = 0
            self.StartRL = 0

        if self.CoolingRateSW == 1:         # 2.0] Cooling rage 계산 시작
            self.CoolingRateSW += 1     # 값 2로 바뀜으로써 이 로직은 1번만 동작함.


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
            ('ZINST87', 1, 0, 50),  # Steam Flow 1
            ('ZINST86', 1, 0, 50),  # Steam Flow 2
            ('ZINST85', 1, 0, 50),  # Steam Flow 3
            ('KLAMPO70', 1, 0, 1),  # Charging Pump2 State
            ('BHV22', 1, 0, 1),  # SI Valve State
            ('ZINST66', 1, 0, 25),  # PZRSprayPos
            ('UAVLEG2', 1, 150, 320),  # PTTemp
            ('ZINST65', 1, 0, 160),  # PTPressure
            ('ZINST78', 1, 0, 70),  # SG1Nar
            ('ZINST77', 1, 0, 70),  # SG2Nar
            ('ZINST76', 1, 0, 70),  # SG3Nar
            ('ZINST75', 1, 0, 80),  # SG1Pres
            ('ZINST74', 1, 0, 80),  # SG2Pres
            ('ZINST73', 1, 0, 80),  # SG3Pres
            ('ZINST72', 1, 0, 100),  # SG1Wid
            ('ZINST71', 1, 0, 100),  # SG2Wid
            ('ZINST70', 1, 0, 100),  # SG3Wid
            ('UUPPPL', 1, 100, 350),  # CoreExitTemp
            ('WFWLN1', 1, 0, 25),  # SG1Feed
            ('WFWLN2', 1, 0, 25),  # SG2Feed
            ('WFWLN3', 1, 0, 25),  # SG3Feed
            ('UCOLEG1', 1, 0, 100),  # RCSColdLoop1
            ('UCOLEG2', 1, 0, 100),  # RCSColdLoop2
            ('UCOLEG3', 1, 0, 100),  # RCSColdLoop3
            ('ZINST65', 1, 0, 160),  # RCSPressure
            ('ZINST63', 1, 0, 100),  # PZRLevel
        ]

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
        super(ENVCNS, self)._send_control_save(para=zipParaVal[0], val=zipParaVal[1])

    def _send_act_EM_Module(self, A):
        pass

    def _send_act_AB_DB_Module(self, A):
        pass

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
                print('ok')
            else:
                print('-')
        else:
            print('Error')

        # Done Act
        self._send_control_to_cns()
        return AMod

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