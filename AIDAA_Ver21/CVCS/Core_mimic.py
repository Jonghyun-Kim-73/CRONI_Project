# ---------------------------------------------------------------- #
# CNS CVCS 미믹
# Make Daeil Lee
# Ref Conpact nuclear simulator
# ---------------------------------------------------------------- #

from math import sqrt
from pickle import dump


class CVCS:
    def __init__(self, init_pzr_level=55.156153, skip_frame=0):
        self.skip_frame = skip_frame
        self.call_init(init_pzr_level)

    def call_init(self, init_pzr_level=55.156153):
        self.mem = {
            'SISignal': {'V': 0, 'RF': [0], 'SF': [0]},             # SI signal / KSAFEI
            'DEPRZ': {'V': init_pzr_level / 100, 'RF': [init_pzr_level / 100], 'SF': [init_pzr_level / 100]}, # PZR level
            'ZPRZSP': {'V': 0.57, 'RF': [0.57], 'SF': [0.57]},      # PZR Set-point

            'LV459_Delay': {'V': 0, 'RF': [0], 'SF': [0]},          # Letdown Valve LV459 / KTLV459
            'LV459_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},      # Letdown Valve LV459 / KCLV459
            'LV459_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},     # Letdown Valve LV459 / KCLV459
            'LV459_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},    # Letdown Valve LV459 / KALV459
            'LV459_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},  # Letdown Valve LV459 Control Signal -1 Clsoe 0 1 Open
            'LV459': {'V': 1, 'RF': [1], 'SF': [1]},                # Letdown Valve LV459 / BLV459

            'LV460_Delay': {'V': 0, 'RF': [0], 'SF': [0]},
            'LV460_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},
            'LV460_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'LV460_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'LV460_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'LV460': {'V': 1, 'RF': [1], 'SF': [1]},

            'HV1_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},
            'HV1_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'HV1_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'HV1_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'HV1': {'V': 1, 'RF': [1], 'SF': [1]},

            'HV2_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},
            'HV2_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'HV2_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'HV2_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'HV2': {'V': 1, 'RF': [1], 'SF': [1]},

            'HV3_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},
            'HV3_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'HV3_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'HV3_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'HV3': {'V': 0, 'RF': [0], 'SF': [0]},

            'BPV145_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},
            'BPV145_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'BPV145_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'BPV145_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'BPV145': {'V': 0.64, 'RF': [0.64], 'SF': [0.64]},
            'BPV145I': {'V': 0.64, 'RF': [0.64], 'SF': [0.64]},
            'BPV145Mode': {'V': 0, 'RF': [0], 'SF': [0]},           # Auto(0), Man(1)

            'BFV122_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},
            'BFV122_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'BFV122_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'BFV122_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'BFV122': {'V': 0.49146140, 'RF': [0.49146140], 'SF': [0.49146140]},
            'BFV122I': {'V': 0.48647678, 'RF': [0.48647678], 'SF': [0.48647678]},
            'BFV122Mode': {'V': 0, 'RF': [0], 'SF': [0]},           # Auto(0), Man(1)

            'V084_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},
            'V084_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V084_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V084_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V084': {'V': 0, 'RF': [0], 'SF': [0]},
            'V084Mode': {'V': 0, 'RF': [0], 'SF': [0]},  # Auto(0), Man(1)

            'V082_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},
            'V082_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V082_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V082_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V082': {'V': 1, 'RF': [1], 'SF': [1]},

            'V083_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},
            'V083_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V083_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V083_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V083': {'V': 1, 'RF': [1], 'SF': [1]},

            'V054_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},       # 여과기 A
            'V054_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V054_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V054_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V054': {'V': 1, 'RF': [1], 'SF': [1]},

            'V055_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},       # 여과기 A + bypass
            'V055_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V055_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V055_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V055': {'V': 0, 'RF': [0], 'SF': [0]},

            'V056_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},       # 여과기 A
            'V056_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V056_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V056_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V056': {'V': 1, 'RF': [1], 'SF': [1]},

            'V057_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},  # 여과기 B
            'V057_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V057_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V057_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V057': {'V': 1, 'RF': [1], 'SF': [1]},

            'V058_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},  # 여과기 B + bypass
            'V058_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V058_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V058_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V058': {'V': 0, 'RF': [0], 'SF': [0]},

            'V059_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},  # 여과기 B
            'V059_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V059_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V059_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'V059': {'V': 1, 'RF': [1], 'SF': [1]},

            # 'WCHPFV122' = 'CWCHARG' * 'BFV122'
            'WCHPFV122': {'V': 4.81632181829228, 'RF': [4.81632181829228], 'SF': [4.81632181829228]},

            'RINOLD': {'V': 4.59163468E-41, 'RF': [4.59163468E-41], 'SF': [4.59163468E-41]},

            'BLV143': {'V': 1, 'RF': [1], 'SF': [1]},
            'BLV614': {'V': 0, 'RF': [0], 'SF': [0]},
            'WLV616': {'V': 4.7957101, 'RF': [4.7957101], 'SF': [4.7957101]},

            'LV616_AutoClose': {'V': 0, 'RF': [0], 'SF': [0]},
            'LV616_OpenSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'LV616_CloseSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'LV616_ControlSignal': {'V': 0, 'RF': [0], 'SF': [0]},
            'LV616': {'V': 1, 'RF': [1], 'SF': [1]},

            'CHP1': {'V': 1, 'RF': [1], 'SF': [1]},
            'CHP2': {'V': 0, 'RF': [0], 'SF': [0]},
            'CHP3': {'V': 0, 'RF': [0], 'SF': [0]},
            'CWCHARG': {'V': 9.8000002, 'RF': [9.8000002], 'SF': [9.8000002]},  # [0, 9.8000002, 13.857000, 16.954000]


            'WEXLD': {'V': 0, 'RF': [0], 'SF': [0]},
            'T_delta': {'V': 0.2, 'RF': [0.2], 'SF': [0.2]},        # 0.2 Sec,  5 loop = 1Sec

            'WLETDNO': {'V': 5.6410036, 'RF': [5.6410036], 'SF': [5.6410036]},      # NORMAL LETDOWN FLOW         # C
            'WLETDNO1': {'V': 5.6410036, 'RF': [5.6410036], 'SF': [5.6410036]},     # NORMAL LETDOWN FLOW         # C
            'WLETDNO2': {'V': 5.6410036, 'RF': [5.6410036], 'SF': [5.6410036]},     # NORMAL LETDOWN FLOW         # C
            'WLETDNO3': {'V': 5.6410036, 'RF': [5.6410036], 'SF': [5.6410036]},     # NORMAL LETDOWN FLOW         # C
            'WLETDNO4': {'V': 5.6410036, 'RF': [5.6410036], 'SF': [5.6410036]},     # NORMAL LETDOWN FLOW         # C
            'WLETDNO5UP': {'V': 5.6410036, 'RF': [5.6410036], 'SF': [5.6410036]},   # NORMAL LETDOWN FLOW         # C
            'WLETDNO5UPA': {'V': 2.8205018, 'RF': [2.8205018], 'SF': [2.8205018]},  # NORMAL LETDOWN FLOW         # C
            'WLETDNO5UPB': {'V': 2.8205018, 'RF': [2.8205018], 'SF': [2.8205018]},  # NORMAL LETDOWN FLOW         # C
            'WLETDNO5DOWN': {'V': 0, 'RF': [0], 'SF': [0]},                         # NORMAL LETDOWN FLOW         # C
            'WLETDNO6': {'V': 5.6410036, 'RF': [5.6410036], 'SF': [5.6410036]},     # NORMAL LETDOWN FLOW         # C

            'WDEMI': {'V': 5.6410036, 'RF': [5.6410036], 'SF': [5.6410036]},        # Demi water
            'PLETIN': {'V': 15012566.00, 'RF': [15012566.00], 'SF': [15012566.00]}, # Letdown Inlet Pressure      # C
            'PPRZN': {'V': 15305906.00, 'RF': [15305906.00], 'SF': [15305906.00]},  # PZR Pressure                # C
            'PLETDB': {'V': 2842650.3, 'RF': [2842650.3], 'SF': [2842650.3]},                                     # C
            'ZVCT': {'V': 72.865021, 'RF': [72.865021], 'SF': [72.865021]},         # VCT level                   # C
            'PVCT': {'V': 0, 'RF': [0], 'SF': [0]},                                 # VCT Pressure                # C
            'WRCPSI': {'V': 0.50499988, 'RF': [0.50499988], 'SF': [0.50499988]},    # RCP Seal inject
            # RCP Seal Return Flow
            'WRCPSR': {'V': 0.50499988 * 0.375, 'RF': [0.50499988 * 0.375], 'SF': [0.50499988 * 0.375]},
            'WCHARGT': {'V': 9.1457081, 'RF': [9.1457081], 'SF': [9.1457081]},                                    # C
            'WSWHX': {'V': 5.2949996, 'RF': [5.2949996], 'SF': [5.2949996]},
            'WCHGNO': {'V': 3.8525825, 'RF': [3.8525825], 'SF': [3.8525825]},
            'WCMINI': {'V': 3.78, 'RF': [3.78], 'SF': [3.78]},  # CHP Return Mini Flow3.78
            'WNETCH': {'V': 0, 'RF': [0], 'SF': [0]},
            'WTOFV122': {'V': 3.8525825, 'RF': [3.8525825], 'SF': [3.8525825]},
            'WTOV084': {'V': 0, 'RF': [0], 'SF': [0]},
            'WTOV083': {'V': 0, 'RF': [0], 'SF': [0]},
            # PZR heater
            'PZRHeater': {'V': 0, 'RF': [0], 'SF': [0]},
            'PZRMode': {'V': 0, 'RF': [0], 'SF': [0]}, # 0 Auto 1 Man

            # 'RTFLOW': ('WRCPSI' - 'WRCPSR') * 3.0
            'RTFLOW': {'V': 0.9468747749999998, 'RF': [0.9468747749999998], 'SF': [0.9468747749999998]},

            # Fix
            'CPPRZN': {'V': 15400000.00, 'RF': [15400000.00], 'SF': [15400000.00]}, # NOMINAL PRZ Pressure
            'CPLDBN': {'V': 1.0e5, 'RF': [1.0e5], 'SF': [1.0e5]},                   # NOMINAL Back Pressure
            'CPLETDB': {'V': 2410000.00, 'RF': [2410000.00], 'SF': [2410000.00]},   # NOMINAL L/D BACK PRESSURE
            'CLETNO': {'V': 6.25, 'RF': [6.25], 'SF': [6.25]},                      # NORMAL L/D FLOW ADMITTANCE
            'CWHV1': {'V': 2.839, 'RF': [2.839], 'SF': [2.839]},                    # 45 gpm
            'CWHV2': {'V': 3.785, 'RF': [3.785], 'SF': [3.785]},                    # 60 gpm
            'CWHV3': {'V': 4.732, 'RF': [4.732], 'SF': [4.732]},                    # 75 gpm
            'CWNETUT': {'V': 4.7347999, 'RF': [4.7347999], 'SF': [4.7347999]},      # L/D BACK PRESSURE SET POINT
            'CLDBP1': {'V': 0.15, 'RF': [0.15], 'SF': [0.15]},              # GAIN AND RESET TIME FOR L/D BACK PRESSURE
            'CLDBP2': {'V': 8.0, 'RF': [8.0], 'SF': [8.0]},                 # GAIN AND RESET TIME FOR L/D BACK PRESSURE
            'CVVCT': {'V': 8.85E-3, 'RF': [8.85E-3], 'SF': [8.85E-3]},      # VCT Volume to level

            # Alarm _ CNS
            'KLAMPO260': {'V': 0, 'RF': [0], 'SF': [0]},              # L10  L/D HX outlet flow lo(15 m3/hr)
            'KLAMPO263': {'V': 0, 'RF': [0], 'SF': [0]},              # L13  VCT level lo(20 %)
            'KLAMPO264': {'V': 0, 'RF': [0], 'SF': [0]},              # L14  VCT press lo(0.7 kg/cm2)
            'KLAMPO265': {'V': 0, 'RF': [0], 'SF': [0]},              # L15  RCP seal inj wtr flow lo(1.4 m3/hr)
            'KLAMPO266': {'V': 0, 'RF': [0], 'SF': [0]},              # L16  Charging flow cont flow lo(5 m3/hr)
            'KLAMPO268': {'V': 0, 'RF': [0], 'SF': [0]},              # L18  L/D HX outlet flow hi (30  m3/hr)
            'KLAMPO271': {'V': 0, 'RF': [0], 'SF': [0]},              # L21  VCT level hi(80 %)
            'KLAMPO272': {'V': 0, 'RF': [0], 'SF': [0]},              # L22  VCT press hi (4.5 kg/cm2)
            'KLAMPO274': {'V': 0, 'RF': [0], 'SF': [0]},              # L24  Charging flow cont flow hi(27 m3/hr)
            'KLAMPO301': {'V': 0, 'RF': [0], 'SF': [0]},              # R1   Rad hi alarm
            'KLAMPO307': {'V': 0, 'RF': [0], 'SF': [0]},              # R7   PRZ press hi alert(162.4 kg/cm2)
            'KLAMPO308': {'V': 0, 'RF': [0], 'SF': [0]},              # R8   PRZ press lo alert(153.6 kg/cm2)
            'KLAMPO310': {'V': 0, 'RF': [0], 'SF': [0]},              # R10  PRZ cont level hi heater on(over 5%)
            'KLAMPO311': {'V': 0, 'RF': [0], 'SF': [0]},              # R11  PRZ cont level lo heater off(17%)
            'KLAMPO312': {'V': 0, 'RF': [0], 'SF': [0]},              # R12  PRZ press lo back-up heater on(153.6 kg/cm2)

            'MAL01': {'V': 0, 'RF': [0], 'SF': [0]},                  # Leak RCS -*- 460 Valve
            'MAL02': {'V': 0, 'RF': [0], 'SF': [0]},                  # Leak 460 -*- 459
            'MAL03': {'V': 0, 'RF': [0], 'SF': [0]},                  # Leak 459 -*- Orifice Valve
            'MAL04': {'V': 0, 'RF': [0], 'SF': [0]},                  # Leak Orifice Valve -*- Letdown Heat EX Changer
            'MAL05': {'V': 0, 'RF': [0], 'SF': [0]},                  # Leak LV614 -> Hold-up tank
            'MAL06': {'V': 0, 'RF': [0], 'SF': [0]},                  # Leak FV122 -*- V083

            'MAL07A': {'V': 0, 'RF': [0], 'SF': [0]},                  # 여과기 A
            'MAL07B': {'V': 0, 'RF': [0], 'SF': [0]},                  # 여과기 B

            'SimTime': {'V': 0, 'RF': [0], 'SF': [0]},
        }

    def control(self, para, step=0.05):
        Rtemp = 0
        if self.mem[f'{para}_OpenSignal']['V'] == 1:
            Rtemp = 1
        if self.mem[f'{para}_CloseSignal']['V'] == 1:
            Rtemp = -1

        self.mem[f'{para}']['V'] = self.mem[f'{para}']['V'] + Rtemp * step
        self.mem[f'{para}']['V'] = 1 if self.mem[f'{para}']['V'] >= 1 else self.mem[f'{para}']['V']
        self.mem[f'{para}']['V'] = 0 if self.mem[f'{para}']['V'] <= 0 else self.mem[f'{para}']['V']

        self.mem[f'{para}_ControlSignal']['V'] = 0 if self.mem[f'{para}']['V'] >= 1 else self.mem[f'{para}_ControlSignal']['V']
        self.mem[f'{para}_ControlSignal']['V'] = 0 if self.mem[f'{para}']['V'] <= 0 else self.mem[f'{para}_ControlSignal']['V']

    def simple_control(self, para, step=0.05):
        if self.mem[f'{para}_ControlSignal']['V'] == 1:
            self.mem[f'{para}_OpenSignal']['V'] = 1
        else:
            self.mem[f'{para}_OpenSignal']['V'] = 0

        if self.mem[f'{para}_ControlSignal']['V'] == -1 or self.mem[f'{para}_AutoClose']['V'] == 1:
            self.mem[f'{para}_CloseSignal']['V'] = 1
        else:
            self.mem[f'{para}_CloseSignal']['V'] = 0

        self.control(para, step)

    def step(self):
        """
            skip 을 고려한 시뮬레이팅
            - 구조
                0. < --- 제어 계획 수립 -------------
                1. 현재 수정된 제어에 따라 1 step 돌기
                2. RF에 현 상태 저장
                3. 제어 신호 초기화
                4. skip frame 수에 따라서 n 회 반복 후 종료
                5. SF 에 현 상태 저장
        """
        for n in range(self.skip_frame + 1):
            # Leak RCS -*- 460 Valve
            if self.mem['MAL01']['V'] > 0:
                NEXTLET = self.mem['WLETDNO']['V'] - self.mem['MAL01']['V'] * 0.01
            else:
                NEXTLET = self.mem['WLETDNO']['V']
            self.mem['WLETDNO1']['V'] = NEXTLET
            # Letdown 460 Valve ----------------------------------------------------------------------------------------
            if True:
                # 가압기 수위 17 아래 시 10 Sec Delay
                if self.mem['DEPRZ']['V'] < 0.17:
                    self.mem['LV460_Delay']['V'] += 1
                    if self.mem['LV460_Delay']['V'] > 10 / self.mem['T_delta']['V']:
                        self.mem['LV460_Delay']['V'] = 10 / self.mem['T_delta']['V']
                else:
                    self.mem['LV460_Delay']['V'] = 0

                if self.mem['LV460_Delay']['V'] >= 10 / self.mem['T_delta']['V'] or self.mem['SISignal']['V'] == 1:
                    self.mem['LV460_AutoClose']['V'] = 1
                else:
                    self.mem['LV460_AutoClose']['V'] = 0

                if self.mem['LV460_ControlSignal']['V'] == 1:
                    self.mem['LV460_OpenSignal']['V'] = 1
                else:
                    self.mem['LV460_OpenSignal']['V'] = 0

                if self.mem['LV460_ControlSignal']['V'] == -1 or self.mem['LV460_AutoClose']['V'] == 1:
                    self.mem['LV460_CloseSignal']['V'] = 1
                else:
                    self.mem['LV460_CloseSignal']['V'] = 0

                self.control('LV460')
            # Letdown Pressure / Normal letdown flow  (back pressure is assumed to be 1 bar ?)
            if True:
                RPRCS = max(self.mem['PLETIN']['V'], self.mem['PPRZN']['V'])
                RPDIF = (RPRCS - self.mem['PLETDB']['V']) / (self.mem['CPPRZN']['V'] - self.mem['CPLDBN']['V'])
                RPDIF = 0 if RPDIF <= 0 else RPDIF

                RWLTDN = sqrt(RPDIF) * self.mem['LV460']['V'] * self.mem['CLETNO']['V']

                NEXTLET = (RWLTDN - NEXTLET) * 0.2 + NEXTLET
            # Leak 460 -*- 459
            if True:
                NEXTLET = NEXTLET - self.mem['MAL02']['V'] * 0.01
                self.mem['WLETDNO2']['V'] = NEXTLET
            # Letdown 459 Valve ----------------------------------------------------------------------------------------
            if True:
                # 가압기 수위 17 아래 시 10 Sec Delay
                if self.mem['DEPRZ']['V'] < 0.17:
                    self.mem['LV459_Delay']['V'] += 1
                    if self.mem['LV459_Delay']['V'] > 10 / self.mem['T_delta']['V']:
                        self.mem['LV459_Delay']['V'] = 10 / self.mem['T_delta']['V']
                else:
                    self.mem['LV459_Delay']['V'] = 0

                if self.mem['LV459_Delay']['V'] >= 10 / self.mem['T_delta']['V'] or self.mem['SISignal']['V'] == 1:
                    self.mem['LV459_AutoClose']['V'] = 1
                else:
                    self.mem['LV459_AutoClose']['V'] = 0

                if self.mem['LV459_ControlSignal']['V'] == 1:
                    self.mem['LV459_OpenSignal']['V'] = 1
                else:
                    self.mem['LV459_OpenSignal']['V'] = 0

                if self.mem['LV459_ControlSignal']['V'] == -1 or self.mem['LV459_AutoClose']['V'] == 1:
                    self.mem['LV459_CloseSignal']['V'] = 1
                else:
                    self.mem['LV459_CloseSignal']['V'] = 0

                self.control('LV459')
            # Letdown 459 out ->
            NEXTLET = NEXTLET * self.mem['LV459']['V']
            # Leak 459 -*- Orifice Valve
            if True:
                NEXTLET = NEXTLET - self.mem['MAL03']['V'] * 0.01
                self.mem['WLETDNO3']['V'] = NEXTLET
            # Orifice Valve --------------------------------------------------------------------------------------------
            if True:
                for i in range(1, 4):   # 1, 2, 3
                    if self.mem['DEPRZ']['V'] < 0.17:
                        self.mem[f'HV{i}_AutoClose']['V'] = 1
                    else:
                        self.mem[f'HV{i}_AutoClose']['V'] = 0

                    if self.mem['DEPRZ']['V'] >= 0.17 and self.mem[f'HV{i}_ControlSignal']['V'] == 1 and self.mem['LV459']['V'] >= 1:
                        self.mem[f'HV{i}_OpenSignal']['V'] = 1
                    else:
                        self.mem[f'HV{i}_OpenSignal']['V'] = 0

                    if self.mem[f'HV{i}_ControlSignal']['V'] == -1 or self.mem['LV459']['V'] < 0.95:
                        self.mem[f'HV{i}_CloseSignal']['V'] = 1
                    else:
                        self.mem[f'HV{i}_CloseSignal']['V'] = 0

                    temp = 0

                    if self.mem[f'HV{i}_OpenSignal']['V'] == 1:
                        temp = 1
                    if self.mem[f'HV{i}_CloseSignal']['V'] == 1:
                        temp = -1

                    self.mem[f'HV{i}']['V'] = self.mem[f'HV{i}']['V'] + temp * 0.05
                    self.mem[f'HV{i}']['V'] = 1 if self.mem[f'HV{i}']['V'] > 1 else self.mem[f'HV{i}']['V']
                    self.mem[f'HV{i}']['V'] = 0 if self.mem[f'HV{i}']['V'] < 0 else self.mem[f'HV{i}']['V']
                if self.mem['HV1']['V'] == 1 and self.mem['HV2']['V'] == 0 and self.mem['HV3']['V'] == 0 and RWLTDN > self.mem['CWHV1']['V']:
                    NEXTLET = self.mem['CWHV1']['V']
                elif self.mem['HV1']['V'] == 0 and self.mem['HV2']['V'] == 1 and self.mem['HV3']['V'] == 0 and RWLTDN > self.mem['CWHV2']['V']:
                    NEXTLET = self.mem['CWHV2']['V']
                elif self.mem['HV1']['V'] == 0 and self.mem['HV2']['V'] == 0 and self.mem['HV3']['V'] == 1 and RWLTDN > self.mem['CWHV3']['V']:
                    NEXTLET = self.mem['CWHV3']['V']
                elif self.mem['HV1']['V'] == 0 and self.mem['HV2']['V'] == 0 and self.mem['HV3']['V'] == 0:
                    NEXTLET = 0
                else:
                    NEXTLET = NEXTLET
            # Leak Orifice Valve -*- Letdown Heat EX Changer
            if True:
                NEXTLET = NEXTLET - self.mem['MAL04']['V'] * 0.01
                self.mem['WLETDNO4']['V'] = NEXTLET
            # L/D Back pressure ----------------------------------------------------------------------------------------
            if True:
                # PI controller
                RIN = (NEXTLET / self.mem['CWNETUT']['V'] - 1.0) + (1.0 - self.mem['PLETDB']['V'] / self.mem['CPLETDB']['V'])
                PIOut = self.PIREGL(RIN, -1.0, 1.0, 1, 0, self.mem['CLDBP1']['V'], self.mem['CLDBP2']['V'],
                                    self.mem['T_delta']['V'], 0.01 / self.mem['T_delta']['V'],
                                    self.mem['BPV145Mode']['V'], self.mem['BPV145_ControlSignal']['V'],
                                    self.mem['BPV145I']['V'], self.mem['BPV145']['V'])

                self.mem['BPV145I']['V'], self.mem['BPV145']['V'] = PIOut
                self.mem['BPV145']['V'] = round(self.mem['BPV145']['V'], 4)
                self.mem['PLETDB']['V'] = self.mem['BPV145']['V'] * 44.1e5
            # LV143 쪽 라인
            if True:
                self.mem['WLETDNO5UP']['V'] = NEXTLET * self.mem['BLV143']['V']
                # 여과기 A
                self.mem['WLETDNO5UPA']['V'] = self.mem['WLETDNO5UP']['V']/2

                self.simple_control('V054', step=0.01)
                self.simple_control('V055', step=0.01)
                self.simple_control('V056', step=0.01)
                if self.mem['V054']['V'] == 1 and self.mem['V055']['V'] == 1 and self.mem['V056']['V'] == 0:
                    UPA = self.mem['WLETDNO5UPA']['V'] - self.mem['MAL07A']['V']
                    UPABypass = (self.mem['WLETDNO5UPA']['V'] - UPA) * self.mem['V055']['V']
                    self.mem['WLETDNO5UPA']['V'] = UPABypass + UPA
                else:
                    UPA = self.mem['V054']['V'] * self.mem['WLETDNO5UPA']['V']
                    UPABypass = (self.mem['WLETDNO5UPA']['V'] - UPA) * self.mem['V055']['V']
                    UPA = (UPA - self.mem['MAL07A']['V']) * self.mem['V056']['V']
                    self.mem['WLETDNO5UPA']['V'] = UPABypass + UPA

                # 여과기 B
                self.mem['WLETDNO5UPB']['V'] = self.mem['WLETDNO5UP']['V']/2
                self.simple_control('V057', step=0.01)
                self.simple_control('V058', step=0.01)
                self.simple_control('V059', step=0.01)
                if self.mem['V057']['V'] == 1 and self.mem['V058']['V'] == 1 and self.mem['V059']['V'] == 0:
                    UPB = self.mem['WLETDNO5UPB']['V'] - self.mem['MAL07B']['V']
                    UPBBypass = (self.mem['WLETDNO5UPB']['V'] - UPB) * self.mem['V058']['V']
                    self.mem['WLETDNO5UPB']['V'] = UPABypass + UPB
                else:
                    UPB = self.mem['V057']['V'] * self.mem['WLETDNO5UPB']['V']
                    UPBBypass = (self.mem['WLETDNO5UPB']['V'] - UPB) * self.mem['V058']['V']
                    UPB = (UPB - self.mem['MAL07B']['V']) * self.mem['V059']['V']
                    self.mem['WLETDNO5UPB']['V'] = UPBBypass + UPB

                self.mem['WLETDNO5UPB']['V'] = self.mem['V057']['V'] * self.mem['WLETDNO5UPB']['V'] - self.mem['MAL07B']['V']
                self.mem['WLETDNO5UPB']['V'] = self.mem['V059']['V'] * self.mem['WLETDNO5UPB']['V']

                self.mem['WLETDNO5DOWN']['V'] = NEXTLET * abs(self.mem['BLV143']['V'] - 1)

                self.mem['WLETDNO6']['V'] = self.mem['WLETDNO5UPA']['V'] + self.mem['WLETDNO5UPB']['V'] + self.mem['WLETDNO5DOWN']['V']
            # Bypass Valve LV614 ---------------------------------------------------------------------------------------
            # VCT level high, bypass to hold-up tank
            if True:
                if self.mem['ZVCT']['V'] > 74.0:    # 74% Change
                    self.mem['BLV614']['V'] = 1
                elif self.mem['MAL05']['V'] != 0:
                    self.mem['BLV614']['V'] = self.mem['MAL05']['V']
                else:
                    self.mem['BLV614']['V'] = 0

                self.mem['WDEMI']['V'] = self.mem['WLETDNO6']['V'] * (1.0 - self.mem['BLV614']['V'])
            # VCT Level and Pressure -----------------------------------------------------------------------------------
            if True:
                self.mem['ZVCT']['V'] = self.mem['ZVCT']['V'] + (self.mem['WEXLD']['V'] + self.mem['WDEMI']['V'] - self.mem['WLV616']['V']) * self.mem['CVVCT']['V'] * self.mem['T_delta']['V']

                self.mem['ZVCT']['V'] = 0 if self.mem['ZVCT']['V'] < 0 else self.mem['ZVCT']['V']
                self.mem['ZVCT']['V'] = 100 if self.mem['ZVCT']['V'] > 100 else self.mem['ZVCT']['V']

                self.mem['PVCT']['V'] = 1.0 + self.mem['ZVCT']['V'] * 0.0099  # 1.2~2.0 kg/cm2
            # ----------------------------------------------------------------------------------------------------------

            # LV616 Valve Start ----------------------------------------------------------------------------------------
            if True:
                self.mem['LV616_AutoClose']['V'] = 1 if self.mem['ZVCT']['V'] <= 5.0 or self.mem['SISignal']['V'] == 1 else 0
                self.mem['LV616_OpenSignal']['V'] = 1 if self.mem['LV616_ControlSignal']['V'] == 1 else 0
                self.mem['LV616_CloseSignal']['V'] = 1 if self.mem['LV616_ControlSignal']['V'] == -1 else 0
                temp = 0
                temp = 1 if self.mem['LV616_OpenSignal']['V'] == 1 else temp
                temp = -1 if self.mem['LV616_CloseSignal']['V'] == 1 else temp
                self.mem['LV616']['V'] = self.mem['LV616']['V'] + temp * 0.05
                self.mem['LV616']['V'] = 1 if self.mem['LV616']['V'] >= 1 else self.mem['LV616']['V']
                self.mem['LV616']['V'] = 0 if self.mem['LV616']['V'] <= 0 else self.mem['LV616']['V']

                self.mem['LV616_ControlSignal']['V'] = 0 if self.mem['LV616']['V'] >= 1 else self.mem['LV616_ControlSignal']['V']
                self.mem['LV616_ControlSignal']['V'] = 0 if self.mem['LV616']['V'] <= 0 else self.mem['LV616_ControlSignal']['V']

                # LV616 -> Seal
                self.mem['RTFLOW']['V'] = (self.mem['WRCPSI']['V'] - self.mem['WRCPSR']['V']) * 3.0
                self.mem['WLV616']['V'] = (self.mem['WCHARGT']['V'] - self.mem['WSWHX']['V'] + self.mem['RTFLOW']['V']) * self.mem['LV616']['V']

            # Charging Pump --------------------------------------------------------------------------------------------
            if True:
                RRCPSL = self.mem['WRCPSI']['V'] * 3  # RCP Seal 에서 Return Flow
                self.mem['WCHARGT']['V'] = self.mem['WCHGNO']['V'] + RRCPSL + self.mem['WCMINI']['V']

                # Mini Flow pass

                # Charging Line Flow via FV122
                ChargingFlow = [0, 9.8000002, 13.857000, 16.954000]
                start_CHP = self.mem['CHP1']['V'] + self.mem['CHP2']['V'] + self.mem['CHP3']['V']
                self.mem['CWCHARG']['V'] = ChargingFlow[int(start_CHP)]

            # FV122 Charging Valve -------------------------------------------------------------------------------------
            if True:
                # PID Controller for FV122
                RIN = self.mem['ZPRZSP']['V'] - self.mem['DEPRZ']['V']
                PIDOUT = self.PIDREG(RIN, self.mem['RINOLD']['V'], -1.0, 0, 1.0, 0.1,
                                     0.2, 5.0, 0.01, self.mem['T_delta']['V'], 0.0075 / self.mem['T_delta']['V'],
                                     self.mem['BFV122Mode']['V'], self.mem['BFV122_ControlSignal']['V'],
                                     self.mem['BFV122I']['V'], self.mem['BFV122']['V'])

                self.mem['BFV122I']['V'], self.mem['BFV122']['V'] = PIDOUT
                self.mem['BFV122']['V'] = round(self.mem['BFV122']['V'], 2)

                self.mem['RINOLD']['V'] = RIN
            # V082/083
            self.simple_control('V082')
            self.simple_control('V083')
            # V084 Bypass Valve
            self.simple_control('V084', step=0.01)
            # Bypass Flow Calculation
            if True:
                self.mem['WTOFV122']['V'] = self.mem['CWCHARG']['V'] * self.mem['BFV122']['V'] * self.mem['V082']['V']
                self.mem['WTOV083']['V'] = self.mem['WTOFV122']['V'] - self.mem['MAL06']['V']
                self.mem['WTOV084']['V'] = (self.mem['CWCHARG']['V'] - self.mem['WTOFV122']['V']) * self.mem['V084']['V']
            # 최종 Chargning 유량 계산
            if True:
                if self.mem['PLETIN']['V'] < 182.0E5:
                    self.mem['WCHPFV122']['V'] = self.mem['WTOV083']['V'] + self.mem['WTOV084']['V']
                    self.mem['WCHGNO']['V'] = ((self.mem['WCHPFV122']['V'] - self.mem['RTFLOW']['V']) - self.mem['WCHGNO']['V']) * 0.1 + self.mem['WCHGNO']['V']
                else:
                    self.mem['WCHGNO']['V'] = 0
                self.mem['WCHGNO']['V'] = 0 if self.mem['WCHGNO']['V'] <= 0 else self.mem['WCHGNO']['V']
            # Net Charging / Letdown + 가압기 수위 반영
            if True:
                self.mem['WNETCH']['V'] = self.mem['WCHGNO']['V'] + self.mem['RTFLOW']['V']
                self.mem['WNETCH']['V'] = 0 if self.mem['WNETCH']['V'] <= 0 else self.mem['WNETCH']['V']

                # Letdown
                self.mem['WLETDNO']['V'] = NEXTLET

                delta = self.mem['WNETCH']['V'] - self.mem['WLETDNO']['V']

                # 가압기 수위에 반영
                # self.mem['DEPRZ']['V' += delta * 0.0000095
                self.mem['DEPRZ']['V'] += delta * 0.0000095 * 5
                self.mem['DEPRZ']['V'] = 1 if self.mem['DEPRZ']['V'] >= 1 else self.mem['DEPRZ']['V']

                if self.mem['PZRMode']['V'] == 0:
                    if self.mem['DEPRZ']['V'] < 0.17:
                        self.mem['PZRHeater']['V'] = 0          # 17% 이하 heat off
                    elif self.mem['ZPRZSP']['V'] + 0.05 < self.mem['DEPRZ']['V']:  # 0.62
                        self.mem['PZRHeater']['V'] = 1          # 17% 이하 heat on
                    elif self.mem['PPRZN']['V'] < 152.2E5:
                        self.mem['PZRHeater']['V'] = 1
                    else:
                        self.mem['PZRHeater']['V'] = 0
                else:
                    pass

                # 수위 상승에 따른 압력 증가 고려
                self.mem['PPRZN']['V'] += delta * 100 * 1 + self.mem['PZRHeater']['V'] * 10

                # 시간 추가
                self.mem['SimTime']['V'] += 1

            # ALARM update
            self.step_alarm()
            # ----------------------------------------------------------------------------------------------------------
            # SAVE RF and inital control signal
            for key in self.mem.keys():
                self.mem[key]['RF'].append(self.mem[key]['V'])
                if n == self.skip_frame:
                    self.mem[key]['SF'].append(self.mem[key]['V'])

                self.mem['BFV122_ControlSignal']['V'] = 0
                self.mem['V084_ControlSignal']['V'] = 0

    def step_alarm(self):
        self.mem['KLAMPO260']['V'] = 1 if self.mem['WLETDNO']['V'] < 4.16 else 0
        self.mem['KLAMPO263']['V'] = 1 if self.mem['ZVCT']['V'] < 20 else 0
        self.mem['KLAMPO264']['V'] = 1 if self.mem['PVCT']['V'] < 0.7 else 0
        self.mem['KLAMPO265']['V'] = 1 if self.mem['WRCPSI']['V'] < 0.4 else 0
        self.mem['KLAMPO266']['V'] = 1 if self.mem['WCHGNO']['V'] < 1.38 else 0
        self.mem['KLAMPO268']['V'] = 1 if self.mem['WLETDNO4']['V'] > 8.33 else 0
        self.mem['KLAMPO271']['V'] = 1 if self.mem['ZVCT']['V'] > 80 else 0
        self.mem['KLAMPO272']['V'] = 1 if self.mem['PVCT']['V'] > 4.5 else 0
        self.mem['KLAMPO274']['V'] = 1 if self.mem['WCHGNO']['V'] > 7.5 else 0

        self.mem['KLAMPO301']['V'] = 1 if self.mem['MAL01']['V'] > 0 or \
                                          self.mem['MAL02']['V'] > 0 or \
                                          self.mem['MAL03']['V'] > 0 or \
                                          self.mem['MAL04']['V'] > 0 or \
                                          self.mem['MAL05']['V'] > 0 or \
                                          self.mem['MAL06']['V'] > 0 or \
                                          self.mem['MAL07A']['V'] > 0 or \
                                          self.mem['MAL07B']['V'] > 0 else 0

        self.mem['KLAMPO307']['V'] = 1 if self.mem['PPRZN']['V'] > 159.E5 else 0
        self.mem['KLAMPO308']['V'] = 1 if self.mem['PPRZN']['V'] < 151.E5 else 0
        self.mem['KLAMPO310']['V'] = 1 if self.mem['ZPRZSP']['V'] + 0.05 < self.mem['DEPRZ']['V'] else 0
        self.mem['KLAMPO311']['V'] = 1 if self.mem['DEPRZ']['V'] < 0.17 else 0
        self.mem['KLAMPO312']['V'] = 1 if self.mem['PPRZN']['V'] < 152.2E5 else 0

    def PIREGL(self, RIN, RINLMH, RINLML, RUTLMH, RUTLML,
               RGAIN, RINTEG, RDT,
               RATE, IMODE, ICHANG, RIUOLD, ROUT):

        if RINLMH >= RINLML:
            RIN = RINLMH if RIN > RINLMH else RIN
            RIN = RINLML if RIN < RINLML else RIN

        if IMODE == 0: # Auto
            ICASE = 1
            ICASE = 2 if RGAIN == 0 else ICASE
            ICASE = 3 if RGAIN != 0 and RINTEG == 0 else ICASE

            if ICASE == 1:
                RTEMP = RIN * RGAIN
                RIOUT = RIUOLD + RTEMP * RDT / RINTEG
            elif ICASE == 2:
                RTEMP = 0.0
                RIOUT = 0.0
            elif ICASE == 3:
                RTEMP = RIN * RGAIN
                RIOUT = 0.0

            ROUT = RTEMP + RIUOLD

            if RUTLMH > RUTLML:
                if RTEMP >= 0:
                    RLIMIH = RUTLMH - RTEMP
                    RLIMIH = RUTLML if RLIMIH < RUTLML else RLIMIH
                    RLIMIL = RUTLML
                else:
                    RLIMIH = RUTLMH
                    RLIMIL = RUTLML - RTEMP
                    RLIMIL = RUTLMH if RLIMIL > RUTLMH else RLIMIL
                RIUOLD = RLIMIH if RIOUT > RLIMIH else RIUOLD
                RIUOLD = RLIMIL if RIOUT < RLIMIL else RIUOLD
                ROUT = RUTLMH if RIOUT > RLIMIH else ROUT
                ROUT = RUTLML if RIOUT < RLIMIL else ROUT
            return ROUT, RIUOLD

        elif IMODE == 1: # Manual
            # ROUT = ROUT + ICHANG * RDT * RATE if ICHANG != 0 else ROUT
            ROUT = ROUT + ICHANG * 0.0001 if ICHANG != 0 else ROUT
            if RUTLMH > RUTLML:
                ROUT = RUTLMH if ROUT > RUTLMH else ROUT
                ROUT = RUTLML if ROUT < RUTLML else ROUT

            RIOUT = ROUT - RIN * RGAIN
            return ROUT, RIOUT

    def PIDREG(self, RIN, RINOLD, RINLMH, RINLML, RUTLMH,
               RUTLML, RGAIN, RINTEG, RDIFF, RDT,
               RATE, IMODE, ICHANG, RIUOLD, ROUT):

        RTEMP = 0.0
        RDOUT = 0.0

        if RINLMH >= RINLML:
            RIN = RINLMH if RIN > RINLMH else RIN
            RIN = RINLML if RIN < RINLML else RIN

        if IMODE == 0:  # Auto
            ICASE = 1
            ICASE = 2 if RGAIN == 0 else ICASE
            ICASE = 3 if RGAIN != 0 and RINTEG == 0 else ICASE

            if ICASE == 1:
                RTEMP = RIN * RGAIN
                RIOUT = RIUOLD + RTEMP * RDT / RINTEG
                RDOUT = (RIN - RINOLD) * RGAIN * RDIFF / RDT
            elif ICASE == 2:
                RTEMP = 0.0
                RIOUT = 0.0
                RDOUT = 0.0
            elif ICASE == 3:
                RTEMP = RIN * RGAIN
                RIOUT = 0.0
                RDOUT = (RIN - RINOLD) * RGAIN * RDIFF / RDT

            ROUT = RTEMP + RIOUT + RDOUT

            if RUTLMH >= RUTLML:
                if RTEMP >= 0:
                    RLIMIH = RUTLMH - RTEMP
                    RLIMIH = RUTLML if RLIMIH < RUTLML else RLIMIH
                    RLIMIL = RUTLML
                else:
                    RLIMIH = RUTLMH
                    RLIMIL = RUTLML - RTEMP
                    RLIMIL = RUTLMH if RLIMIL > RUTLMH else RLIMIL


                RIOUT = RLIMIH if RIOUT > RLIMIH else RIOUT
                RIOUT = RLIMIL if RIOUT < RLIMIL else RIOUT
                ROUT = RUTLMH if ROUT > RUTLMH else ROUT
                ROUT = RUTLML if ROUT < RUTLML else ROUT

            return RIOUT, ROUT
        elif IMODE == 1:  # Manual
            ROUT = ROUT + ICHANG * RDT * RATE

            if RUTLMH > RUTLML:
                ROUT = RUTLMH if ROUT > RUTLMH else ROUT
                ROUT = RUTLML if ROUT < RUTLML else ROUT
            RIOUT = ROUT - RTEMP - RDOUT

            return RIOUT, ROUT

    def _dump_mem(self, file_path):
        with open(file_path, 'wb') as f:
            dump(self.mem, f)