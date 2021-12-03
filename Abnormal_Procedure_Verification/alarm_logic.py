import multiprocessing
from copy import deepcopy
from struct import unpack
import socket
import sys

print('EX_RUN_Module_FAST_Call')
class RUN_FREEZE_FAST(multiprocessing.Process):
    def __init__(self, mem, IP, Port, tick=5):
        multiprocessing.Process.__init__(self)
        self.address = (IP, Port)

        self.mem = mem[0]   # main mem connection
        self.trig_mem = mem[-1]  # main mem connection
        self.call_cns_udp_sender()

        self.CNS_data = deepcopy(self.mem)

        # SIZE BUFFER
        self.size_buffer_mem = 46008
        # SEND TICK
        self.want_tick = tick

    # --------------------------------------------------------------------------------
    def call_cns_udp_sender(self):
        # CNS 정보 읽기
        with open('EX_pro.txt', 'r') as f:
            self.cns_ip, self.cns_port = f.read().split('\t')   # [cns ip],[cns port]
        from CNS_Monitoring_module.EX_CNS_Send_UDP import CNS_Send_Signal
        self.CNS_udp = CNS_Send_Signal(self.cns_ip, int(self.cns_port))

    # --------------------------------------------------------------------------------

    def update_mem(self, data):
        pid_list = []
        # print(len(data)) data의 8바이트를 제외한 나머지 버퍼의 크기
        for i in range(0, len(data), 20):
            sig = unpack('h', data[16 + i: 18 + i])[0]
            para = '12sihh' if sig == 0 else '12sfhh'
            pid, val, sig, idx = unpack(para, data[i:20 + i])

            pid = pid.decode().rstrip('\x00')  # remove '\x00'
            if pid != '':
                self.CNS_data[pid]['V'] = val
                self.CNS_data[pid]['type'] = sig
                # pid_list.append(pid)

        # Alarm reprocessing
        self.AlarmReprocessing()

        # Mal function 발생 시간 및 사고 기록
        if 'Normal_0' in self.CNS_data.keys():
            accident_neb = self.CNS_data['KSWO280']['V']
            # Nor / Ab
            if self.CNS_data['KSWO278']['V'] >= self.CNS_data['KCNTOMS']['V']:
                self.CNS_data['Normal_0']['V'] = 0
                self.CNS_data['Accident_nub']['V'] = 0
                self.CNS_data[f'Accident_{accident_neb}']['V'] = 0
            else:
                self.CNS_data['Normal_0']['V'] = 1
                condition_fun = {0:0, 12: 1, 15: 1, 13: 2, 18: 3, 52: 3, 17: 4} # LOCA, SGTR, MSLB, MFWB
                self.CNS_data['Accident_nub']['V'] = condition_fun[accident_neb]
                self.CNS_data[f'Accident_{accident_neb}']['V'] = 1

        return pid_list

    def update_cns_to_mem(self, key):
        self.mem[key] = self.CNS_data[key]

    def update_local_mem(self, key):
        self.CNS_data[key]['L'].append(self.CNS_data[key]['V'])
        self.CNS_data[key]['D'].append(self.CNS_data[key]['V'])

    def run(self):
        print('RUN EX_RUN_Module_FAST')
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSocket.bind(self.address)
        udpSocket.settimeout(5)     # 5초 대기 후 연결 없으면 연결 안됨을 호출

        while True:
            try:
                data, client = udpSocket.recvfrom(self.size_buffer_mem)
                pid_list = self.update_mem(data[8:])  # 주소값을 가지는 8바이트를 제외한 나머지 부분
                # Run 버튼 누르면 CNS 동작하는 모듈
                if self.trig_mem['Loop'] and self.trig_mem['Run'] is False:
                    self.CNS_udp._send_control_signal(['KFZRUN'], [self.want_tick+100]) # 400 - 100 -> 300 tick 20 sec
                    while True:
                        data, client = udpSocket.recvfrom(self.size_buffer_mem)
                        pid_list = self.update_mem(data[8:])  # 주소값을 가지는 8바이트를 제외한 나머지 부분
                        if self.CNS_data['KFZRUN']['V'] == 4 or self.CNS_data['KFZRUN']['V'] == 10:
                            [self.update_local_mem(key) for key in self.CNS_data.keys()]
                            self.trig_mem['Run'] = True
                            break

                # CNS 초기화 선언시 모든 메모리 초기화
                if self.CNS_data['KFZRUN']['V'] == 6:
                    [self.CNS_data[_]['L'].clear() for _ in self.CNS_data.keys()]
                    [self.CNS_data[_]['D'].clear() for _ in self.CNS_data.keys()]
                    print("CNS 메모리 초기화 완료")

                [self.update_cns_to_mem(key) for key in self.mem.keys()]  # 메인 메모리 업데이트
            except Exception as e:
                print(f"CNS time out {e}")
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    def AlarmReprocessing(self):
        """
        현재 파라 메터가 알람관련 변수라면 입력된 값을 Overwrite
        # -----------  Left panel : KLARML(3,II) -----------------------------------------------------------------------
        #
        #           ---------------------------------------------------
        #           | II = 1 |   9    |   17   |   25   |   33   |  41 |
        #           ---------------------------------------------------
        #           |   2    |   10   |   18   |   26   |   34   |  42|
        #           ---------------------------------------------------
        #           |   3    |   11   |   19   |   27   |   35   |  43 |
        #           ---------------------------------------------------
        #           |   4    |   12   |   20   |   28   |   36   |  44 |
        #           ---------------------------------------------------
        #           |   5    |   13   |   21   |   29   |   37   |  45 |
        #           ---------------------------------------------------
        #           |   6    |   14   |   22   |   30   |   38   |  46 |
        #           ---------------------------------------------------
        #           |   7    |   15   |   23   |   31   |   39   |  47 |
        #           ---------------------------------------------------
        #           |   8    |   16   |   24   |   32   |   40   |  48 |
        #           ---------------------------------------------------
        #
        # ==============================================================================================================
        # -----------  Right panel : KLARMR(3,IJ)
        #
        #       -----------------------------------------------------------------
        #       | IJ=1  |   7   |  13   |  18   |  21   |  26   |  32   |  38   |
        #       -----------------------------------------------------------------
        #       |   2   |   8   |  14   |  19   |  22   |  27   |  33   |  39   |
        #       -----------------------------------------------------------------
        #       |   3   |   9   |  15   |  20   |       |  28   |  34   |  40   |
        #       -----------------------------------------------------------------
        #       |   4   |   10  |  16   |       |  23   |  29   |  35   |  41   |
        #       -----------------------------------------------------------------
        #       |   5   |   11  |       |       |  24   |  30   |  36   |       |
        #       -----------------------------------------------------------------
        #       |   6   |   12  |  17   |       |  25   |  31   |  37   |  42   |
        #       -----------------------------------------------------------------
        #
        # ==============================================================================================================
        """
        #
        # Left panel
        #
        # --------- L1  Intermediate range high flux rod stop(20% of FP)
        if self.CNS_data['XPIRM']['V'] > self.CNS_data['CIRFH']['V']:
            self.CNS_data['KLAMPO251']['V'] = 1
        else:
            self.CNS_data['KLAMPO251']['V'] = 0
        # --------- L2  Power range overpower rod stop(103% of FP)
        if self.CNS_data['QPROREL']['V'] > self.CNS_data['CPRFH']['V']:
            self.CNS_data['KLAMPO252']['V'] = 1
        else:
            self.CNS_data['KLAMPO252']['V'] = 0
        # --------- L3  Control bank D full rod withdrawl(220 steps)
        if self.CNS_data['KZBANK4']['V'] > 220:
            self.CNS_data['KLAMPO253']['V'] = 1
        else:
            self.CNS_data['KLAMPO253']['V'] = 0
        # --------- L3  Control bank D full rod withdrawl(220 steps)
        if self.CNS_data['KZBANK4']['V'] > 220:
            self.CNS_data['KLAMPO253']['V'] = 1
        else:
            self.CNS_data['KLAMPO253']['V'] = 0
        # --------- L4  Control bank lo-lo limit
        # ******* Insertion limit(Reference : KNU 5&6 PLS)
        #
        RDTEMP = (self.CNS_data['UMAXDT']['V']/self.CNS_data['CDT100']['V']) * 100.0
        if RDTEMP >= 100.0: RDTEMP = 100.
        if RDTEMP <= 0.0: RDTEMP = 0.
        if True:
            CRIL = {1: 1.818, 2: 1.824, 3: 1.818, 4: 208.0,
                    5: 93.0, 6: -22.0, 7: 12.0}
            # Control A
            KRIL1 = 228
            # Control B
            KRIL2 = int(CRIL[1] * RDTEMP + CRIL[4])
            if KRIL2 >= 228: KRIL2 = 228
            # Control C
            KRIL3 = int(CRIL[2]*RDTEMP + CRIL[5])
            if KRIL3 >= 228: KRIL3 = 228
            # Control D
            if RDTEMP >= CRIL[7]:
                KRIL4 = int(CRIL[3] * RDTEMP + CRIL[6])
                if KRIL4 >= 160: KRIL4 = 160
                if KRIL4 <= 0: KRIL4 = 0
            else:
                KRIL4 = 0

            if self.CNS_data['KBNKSEL']['V'] == 1:
                KRILM = KRIL1
            elif self.CNS_data['KBNKSEL']['V'] == 2:
                KRILM = KRIL2
            elif self.CNS_data['KBNKSEL']['V'] == 3:
                KRILM = KRIL3
            elif self.CNS_data['KBNKSEL']['V'] == 4:
                KRILM = KRIL4
            else:
                KRILM = 0

            if ((self.CNS_data['KZBANK1']['V'] < KRIL1) or (self.CNS_data['KZBANK2']['V'] < KRIL2)
                    or (self.CNS_data['KZBANK3']['V'] < KRIL3) or (self.CNS_data['KZBANK4']['V'] < KRIL4)):
                self.CNS_data['KLAMPO254']['V'] = 1
            else:
                self.CNS_data['KLAMPO254']['V'] = 0
        # --------- L5  Two or more rod at bottom(ref:A-II-8 p.113 & KAERI87-39)
        IROD = 0
        for _ in range(1, 53):
            if self.CNS_data[f'KZROD{_}']['V'] < 0.0:
                IROD += 1
        if IROD > 2:
            self.CNS_data['KLAMPO255']['V'] = 1
        else:
            self.CNS_data['KLAMPO255']['V'] = 0
        # --------- L6  Axial power distribution limit(3% ~ -12%)
        if (self.CNS_data['CAXOFF']['V'] >= self.CNS_data['CAXOFDL']['V']) or \
                (self.CNS_data['CAXOFF']['V'] <= (self.CNS_data['CAXOFDL']['V'] - 0.75)):
            self.CNS_data['KLAMPO256']['V'] = 1
        else:
            self.CNS_data['KLAMPO256']['V'] = 0
        # --------- L7  CCWS outlet temp hi(49.0 deg C)
        if self.CNS_data['UCCWIN']['V'] >= self.CNS_data['CUCCWH']['V']:
            self.CNS_data['KLAMPO257']['V'] = 1
        else:
            self.CNS_data['KLAMPO257']['V'] = 0
        # --------- L8  Instrument air press lo(6.3 kg/cm2)
        if self.CNS_data['PINSTA']['V'] <= (self.CNS_data['CINSTP']['V'] - 1.5):
            self.CNS_data['KLAMPO258']['V'] = 1
        else:
            self.CNS_data['KLAMPO258']['V'] = 0
        # --------- L9  RWST level lo-lo(5%)
        if self.CNS_data['ZRWST']['V'] <= self.CNS_data['CZRWSLL']['V']:
            self.CNS_data['KLAMPO259']['V'] = 1
        else:
            self.CNS_data['KLAMPO259']['V'] = 0
        # --------- L10  L/D HX outlet flow lo(15 m3/hr)
        if self.CNS_data['WNETLD']['V'] < self.CNS_data['CWLHXL']['V']:
            self.CNS_data['KLAMPO260']['V'] = 1
        else:
            self.CNS_data['KLAMPO260']['V'] = 0
        # --------- L11  L/D HX outlet temp hi(58 deg C)
        if self.CNS_data['UNRHXUT']['V'] > self.CNS_data['CULDHX']['V']:
            self.CNS_data['KLAMPO261']['V'] = 1
        else:
            self.CNS_data['KLAMPO261']['V'] = 0
        # --------- L12  RHX L/D outlet temp hi(202 deg C)
        if self.CNS_data['URHXUT']['V'] > self.CNS_data['CURHX']['V']:
            self.CNS_data['KLAMPO262']['V'] = 1
        else:
            self.CNS_data['KLAMPO262']['V'] = 0
        # --------- L13  VCT level lo(20 %)
        if self.CNS_data['ZVCT']['V'] < self.CNS_data['CZVCT2']['V']:
            self.CNS_data['KLAMPO263']['V'] = 1
        else:
            self.CNS_data['KLAMPO263']['V'] = 0
        # --------- L14  VCT press lo(0.7 kg/cm2)
        if self.CNS_data['PVCT']['V'] < self.CNS_data['CPVCTL']['V']:
            self.CNS_data['KLAMPO264']['V'] = 1
        else:
            self.CNS_data['KLAMPO264']['V'] = 0
        # --------- L15  RCP seal inj wtr flow lo(1.4 m3/hr)
        if (self.CNS_data['WRCPSI1']['V'] < self.CNS_data['CWRCPS']['V'] or
                self.CNS_data['WRCPSI2']['V'] < self.CNS_data['CWRCPS']['V'] or
                self.CNS_data['WRCPSI2']['V'] < self.CNS_data['CWRCPS']['V']):
            self.CNS_data['KLAMPO265']['V'] = 1
        else:
            self.CNS_data['KLAMPO265']['V'] = 0
        # --------- L16  Charging flow cont flow lo(5 m3/hr)
        if self.CNS_data['WCHGNO']['V'] < self.CNS_data['CWCHGL']['V']:
            self.CNS_data['KLAMPO266']['V'] = 1
        else:
            self.CNS_data['KLAMPO266']['V'] = 0
        # --------- R17  Not used
        self.CNS_data['KLAMPO267']['V'] = 0
        # --------- L18  L/D HX outlet flow hi (30  m3/hr)
        if self.CNS_data['WNETLD']['V'] > self.CNS_data['CWLHXH']['V']:
            self.CNS_data['KLAMPO268']['V'] = 1
        else:
            self.CNS_data['KLAMPO268']['V'] = 0
        # --------- L19  PRZ press lo SI
        CSAFEI = {1: 124.e5, 2: 40.3e5}
        if (self.CNS_data['PPRZN']['V'] < CSAFEI[1]) and (self.CNS_data['KSAFEI']['V'] == 1):
            self.CNS_data['KLAMPO269']['V'] = 1
        else:
            self.CNS_data['KLAMPO269']['V'] = 0
        # --------- L20 CTMT spray actuated
        if self.CNS_data['KCTMTSP']['V'] == 1:
            self.CNS_data['KLAMPO270']['V'] = 1
        else:
            self.CNS_data['KLAMPO270']['V'] = 0
        # --------- L21  VCT level hi(80 %)
        if self.CNS_data['ZVCT']['V'] > self.CNS_data['CZVCT6']['V']:
            self.CNS_data['KLAMPO271']['V'] = 1
        else:
            self.CNS_data['KLAMPO271']['V'] = 0
        # --------- L22 VCT press hi (4.5 kg/cm2)
        if self.CNS_data['PVCT']['V'] > self.CNS_data['CPVCTH']['V']:
            self.CNS_data['KLAMPO272']['V'] = 1
        else:
            self.CNS_data['KLAMPO272']['V'] = 0
        # --------- L23  CTMT phase B iso actuated
        if self.CNS_data['KCISOB']['V'] == 1:
            self.CNS_data['KLAMPO273']['V'] = 1
        else:
            self.CNS_data['KLAMPO273']['V'] = 0
        # --------- L24  Charging flow cont flow hi(27 m3/hr)
        if self.CNS_data['WCHGNO']['V'] > self.CNS_data['CWCHGH']['V']:
            self.CNS_data['KLAMPO274']['V'] = 1
        else:
            self.CNS_data['KLAMPO274']['V'] = 0
        # ---------

        # --------- R43  Not used
        self.CNS_data['KLAMPO293']['V'] = 0
        # --------- R44  Not used
        self.CNS_data['KLAMPO294']['V'] = 0
        # --------- L45  CTMT sump level hi
        CZSMPH = {1: 2.492, 2: 2.9238}
        if self.CNS_data['ZSUMP']['V'] > CZSMPH[1]:
            self.CNS_data['KLAMPO295']['V'] = 1
        else:
            self.CNS_data['KLAMPO295']['V'] = 0
        # --------- L46 CTMT sump level hi-hi
        if self.CNS_data['ZSUMP']['V'] > CZSMPH[2]:
            self.CNS_data['KLAMPO296']['V'] = 1
        else:
            self.CNS_data['KLAMPO296']['V'] = 0
        # --------- L47  CTMT air temp hi(48.89 deg C)
        if self.CNS_data['UCTMT']['V'] > self.CNS_data['CUCTMT']['V']:
            self.CNS_data['KLAMPO297']['V'] = 1
        else:
            self.CNS_data['KLAMPO297']['V'] = 0
        # --------- L48  CTMT moisture hi(70% of R.H.)
        if self.CNS_data['HUCTMT']['V'] > self.CNS_data['CHCTMT']['V']:
            self.CNS_data['KLAMPO298']['V'] = 1
        else:
            self.CNS_data['KLAMPO298']['V'] = 0
        #
        # Right panel
        #
        # --------- R1  Rad hi alarm
        if (self.CNS_data['DCTMT']['V'] > self.CNS_data['CRADHI']['V']) or \
                (self.CNS_data['DSECON']['V'] >= 3.9E-3):
            self.CNS_data['KLAMPO301']['V'] = 1
        else:
            self.CNS_data['KLAMPO301']['V'] = 0
        # --------- R2  CTMT press hi 1 alert
        CPCMTH = {1: 0.3515, 2: 1.02, 3: 1.62}
        if self.CNS_data['PCTMT']['V'] * self.CNS_data['PAKGCM']['V'] > CPCMTH[1]:
            self.CNS_data['KLAMPO302']['V'] = 1
        else:
            self.CNS_data['KLAMPO302']['V'] = 0
        # --------- R3  CTMT press hi 2 alert
        if self.CNS_data['PCTMT']['V'] * self.CNS_data['PAKGCM']['V'] > CPCMTH[2]:
            self.CNS_data['KLAMPO303']['V'] = 1
        else:
            self.CNS_data['KLAMPO303']['V'] = 0
        # --------- R4  CTMT press hi 3 alert
        if self.CNS_data['PCTMT']['V'] * self.CNS_data['PAKGCM']['V'] > CPCMTH[3]:
            self.CNS_data['KLAMPO304']['V'] = 1
        else:
            self.CNS_data['KLAMPO304']['V'] = 0
        # --------- R5  Accum. Tk press lo (43.4 kg/cm2)
        if self.CNS_data['PACCTK']['V'] < self.CNS_data['CPACCL']['V']:
            self.CNS_data['KLAMPO305']['V'] = 1
        else:
            self.CNS_data['KLAMPO305']['V'] = 0
        # --------- R6  Accum. Tk press hi ( /43.4 kg/cm2)
        if self.CNS_data['PACCTK']['V'] > self.CNS_data['CPACCH']['V']:
            self.CNS_data['KLAMPO306']['V'] = 1
        else:
            self.CNS_data['KLAMPO306']['V'] = 0
        # --------- R7  PRZ press hi alert(162.4 kg/cm2)
        if self.CNS_data['PPRZ']['V'] > self.CNS_data['CPPRZH']['V']:
            self.CNS_data['KLAMPO307']['V'] = 1
        else:
            self.CNS_data['KLAMPO307']['V'] = 0
        # --------- R8  PRZ press lo alert(153.6 kg/cm2)
        if self.CNS_data['PPRZ']['V'] < self.CNS_data['CPPRZL']['V']:
            self.CNS_data['KLAMPO308']['V'] = 1
        else:
            self.CNS_data['KLAMPO308']['V'] = 0
        # --------- R9  PRZ PORV opening(164.2 kg/cm2)
        if self.CNS_data['BPORV']['V'] > 0.01:
            self.CNS_data['KLAMPO309']['V'] = 1
        else:
            self.CNS_data['KLAMPO309']['V'] = 0
        # --------- R10 PRZ cont level hi heater on(over 5%) !%deail....
        DEPRZ = self.CNS_data['ZINST63']['V'] / 100
        if (DEPRZ > (self.CNS_data['ZPRZSP']['V'] + self.CNS_data['CZPRZH']['V'])) and (self.CNS_data['QPRZB']['V'] > self.CNS_data['CQPRZP']['V']):
            self.CNS_data['KLAMPO310']['V'] = 1
        else:
            self.CNS_data['KLAMPO310']['V'] = 0
        # --------- R11  PRZ cont level lo heater off(17%) !%deail....
        if (DEPRZ < self.CNS_data['CZPRZL']['V']) and (self.CNS_data['QPRZ']['V'] >= self.CNS_data['CQPRZP']['V']):
            self.CNS_data['KLAMPO311']['V'] = 1
        else:
            self.CNS_data['KLAMPO311']['V'] = 0
        # --------- R12  PRZ press lo back-up heater on(153.6 kg/cm2)
        if (self.CNS_data['PPRZN']['V'] < self.CNS_data['CQPRZB']['V']) and (self.CNS_data['KBHON']['V'] == 1):
            self.CNS_data['KLAMPO312']['V'] = 1
        else:
            self.CNS_data['KLAMPO312']['V'] = 0
        # --------- R13  Tref/Auct. Tavg Deviation(1.67 deg C)
        if ((self.CNS_data['UAVLEGS']['V'] - self.CNS_data['UAVLEGM']['V']) > self.CNS_data['CUTDEV']['V']) or\
                ((self.CNS_data['UAVLEGM']['V'] - self.CNS_data['UAVLEGS']['V']) > self.CNS_data['CUTDEV']['V']):
            self.CNS_data['KLAMPO313']['V'] = 1
        else:
            self.CNS_data['KLAMPO313']['V'] = 0
        # --------- R14 RCS 1,2,3 Tavg hi(312.78 deg C)
        if self.CNS_data['UAVLEGM']['V'] > self.CNS_data['CUTAVG']['V']:
            self.CNS_data['KLAMPO314']['V'] = 1
        else:
            self.CNS_data['KLAMPO314']['V'] = 0
        # --------- R15  RCS 1,2,3 Tavg/auct Tavg hi/lo(1.1 deg C)
        RUAVMX = max(self.CNS_data['UAVLEG1']['V'], self.CNS_data['UAVLEG2']['V'],
                     self.CNS_data['UAVLEG3']['V'])
        RAVGT = {1: abs((self.CNS_data['UAVLEG1']['V']) - RUAVMX),
                 2: abs((self.CNS_data['UAVLEG2']['V']) - RUAVMX),
                 3: abs((self.CNS_data['UAVLEG3']['V']) - RUAVMX)}
        if max(RAVGT[1], RAVGT[2], RAVGT[3]) > self.CNS_data['CUAUCT']['V']:
            self.CNS_data['KLAMPO315']['V'] = 1
        else:
            self.CNS_data['KLAMPO315']['V'] = 0
        # --------- R16  RCS 1,2,3 lo flow alert(92% from KAERI87-37)
        CWSGRL = {1: 4232.0, 2: 0.0}
        if ((self.CNS_data['WSGRCP1']['V'] < CWSGRL[1] and self.CNS_data['KRCP1']['V'] == 1) or
                (self.CNS_data['WSGRCP1']['V'] < CWSGRL[1] and self.CNS_data['KRCP1']['V'] == 1) or
                (self.CNS_data['WSGRCP1']['V'] < CWSGRL[1] and self.CNS_data['KRCP1']['V'] == 1)):
            self.CNS_data['KLAMPO316']['V'] = 1
        else:
            self.CNS_data['KLAMPO316']['V'] = 0
        # --------- R17  PRT temp hi(45deg C )
        if self.CNS_data['UPRT']['V'] > self.CNS_data['CUPRT']['V']:
            self.CNS_data['KLAMPO317']['V'] = 1
        else:
            self.CNS_data['KLAMPO317']['V'] = 0
        # --------- R18  PRT  press hi( 0.6kg/cm2)
        if (self.CNS_data['PPRT']['V'] - 0.98E5) > self.CNS_data['CPPRT']['V']:
            self.CNS_data['KLAMPO318']['V'] = 1
        else:
            self.CNS_data['KLAMPO318']['V'] = 0
        # --------- R19  SG 1,2,3 level lo(25% of span)
        if (self.CNS_data['ZINST78']['V']*0.01 < self.CNS_data['CZSGW']['V']) \
                or (self.CNS_data['ZINST77']['V']*0.01 < self.CNS_data['CZSGW']['V']) \
                or (self.CNS_data['ZINST76']['V']*0.01 < self.CNS_data['CZSGW']['V']):
            self.CNS_data['KLAMPO319']['V'] = 1
        else:
            self.CNS_data['KLAMPO319']['V'] = 0
        # --------- R20  SG 1,2,3 stm/FW flow deviation(10% of loop flow)
        RSTFWD = {1: self.CNS_data['WSTM1']['V'] * 0.1,
                  2: self.CNS_data['WSTM2']['V'] * 0.1,
                  3: self.CNS_data['WSTM3']['V'] * 0.1}
        if (((self.CNS_data['WSTM1']['V'] - self.CNS_data['WFWLN1']['V']) > RSTFWD[1]) or
                ((self.CNS_data['WSTM2']['V'] - self.CNS_data['WFWLN2']['V']) > RSTFWD[1]) or
                ((self.CNS_data['WSTM3']['V'] - self.CNS_data['WFWLN3']['V']) > RSTFWD[1])):
            self.CNS_data['KLAMPO320']['V'] = 1
        else:
            self.CNS_data['KLAMPO320']['V'] = 0
        # --------- R21 RCP 1,2,3 trip
        if self.CNS_data['KRCP1']['V'] + self.CNS_data['KRCP2']['V'] + self.CNS_data['KRCP3']['V'] != 3:
            self.CNS_data['KLAMPO321']['V'] = 1
        else:
            self.CNS_data['KLAMPO321']['V'] = 0
        # --------- R22  Condensate stor Tk level  lo
        CZCTKL = {1: 8.55, 2: 7.57}
        if self.CNS_data['ZCNDTK']['V'] < CZCTKL[1]:
            self.CNS_data['KLAMPO322']['V'] = 1
        else:
            self.CNS_data['KLAMPO322']['V'] = 0
        # --------- R23  Condensate stor Tk level lo-lo
        if self.CNS_data['ZCNDTK']['V'] < CZCTKL[2]:
            self.CNS_data['KLAMPO323']['V'] = 1
        else:
            self.CNS_data['KLAMPO323']['V'] = 0
        # --------- R24  Condensate stor Tk level hi
        if self.CNS_data['ZCNDTK']['V'] > self.CNS_data['CZCTKH']['V']:
            self.CNS_data['KLAMPO324']['V'] = 1
        else:
            self.CNS_data['KLAMPO324']['V'] = 0
        # --------- R25  MSIV tripped
        if self.CNS_data['BHV108']['V'] == 0 or self.CNS_data['BHV208']['V'] == 0 or self.CNS_data['BHV308']['V'] == 0:
            self.CNS_data['KLAMPO325']['V'] = 1
        else:
            self.CNS_data['KLAMPO325']['V'] = 0
        # --------- R26  MSL press rate hi steam iso
        if len(self.CNS_data['KLAMPO325']['L']) >= 3:
            PSGLP = {1: self.CNS_data['PSG1']['L'][-2],
                     2: self.CNS_data['PSG2']['L'][-2],
                     3: self.CNS_data['PSG3']['L'][-2]}
            RMSLPR = {1: abs((PSGLP[1] - self.CNS_data['PSG1']['L'][-1]) * 5.0),
                      2: abs((PSGLP[2] - self.CNS_data['PSG2']['L'][-1]) * 5.0),
                      3: abs((PSGLP[3] - self.CNS_data['PSG3']['L'][-1]) * 5.0)}

            if (((RMSLPR[1] >= self.CNS_data['CMSLH']['V']) or
                (RMSLPR[2] >= self.CNS_data['CMSLH']['V']) or
                (RMSLPR[3] >= self.CNS_data['CMSLH']['V'])) and (self.CNS_data['KMSISO']['V'] == 1)):
                self.CNS_data['KLAMPO326']['V'] = 1
            else:
                self.CNS_data['KLAMPO326']['V'] = 0
        # --------- RK27  MSL 1,2,3 press rate hi(-7.03 kg/cm*2/sec = 6.89E5 Pa/sec)
            if ((RMSLPR[1] >= self.CNS_data['CMSLH']['V']) or
                (RMSLPR[2] >= self.CNS_data['CMSLH']['V']) or
                (RMSLPR[3] >= self.CNS_data['CMSLH']['V'])):
                self.CNS_data['KLAMPO327']['V'] = 1
            else:
                self.CNS_data['KLAMPO327']['V'] = 0
        # --------- R28  MSL 1,2,3 press low(41.1 kg/cm*2 = 0.403E7 pas)
        if ((self.CNS_data['PSG1']['V'] < self.CNS_data['CPSTML']['V']) or
            (self.CNS_data['PSG2']['V'] < self.CNS_data['CPSTML']['V']) or
            (self.CNS_data['PSG3']['V'] < self.CNS_data['CPSTML']['V'])):
            self.CNS_data['KLAMPO328']['V'] = 1
        else:
            self.CNS_data['KLAMPO328']['V'] = 0
        # --------- R29  AFW(MD) actuated
        if (self.CNS_data['KAFWP1']['V'] == 1) or (self.CNS_data['KAFWP3']['V'] == 1):
            self.CNS_data['KLAMPO329']['V'] = 1
        else:
            self.CNS_data['KLAMPO329']['V'] = 0
        # --------- R30  Condenser level lo(27")
        if self.CNS_data['ZCOND']['V'] < self.CNS_data['CZCNDL']['V']:
            self.CNS_data['KLAMPO330']['V'] = 1
        else:
            self.CNS_data['KLAMPO330']['V'] = 0
        # --------- R31  FW pump discharge header press hi
        if self.CNS_data['PFWPOUT']['V'] > self.CNS_data['CPFWOH']['V']:
            self.CNS_data['KLAMPO331']['V'] = 1
        else:
            self.CNS_data['KLAMPO331']['V'] = 0
        # --------- R32  FW pump trip
        if (self.CNS_data['KFWP1']['V'] + self.CNS_data['KFWP2']['V'] + self.CNS_data['KFWP3']['V']) == 0:
            self.CNS_data['KLAMPO332']['V'] = 1
        else:
            self.CNS_data['KLAMPO332']['V'] = 0
        # --------- R33  FW temp hi(231.1 deg C)
        if self.CNS_data['UFDW']['V'] > self.CNS_data['CUFWH']['V']:
            self.CNS_data['KLAMPO333']['V'] = 1
        else:
            self.CNS_data['KLAMPO333']['V'] = 0
        # --------- R34  Condensate pump flow lo(1400 gpm=88.324 kg/s)
        if self.CNS_data['WCDPO']['V'] > self.CNS_data['CWCDPO']['V']:
            self.CNS_data['KLAMPO334']['V'] = 1
        else:
            self.CNS_data['KLAMPO334']['V'] = 0
        # --------- R35  Condenser abs press hi(633. mmmHg)
        if self.CNS_data['PVAC']['V'] < self.CNS_data['CPVACH']['V']:
            self.CNS_data['KLAMPO335']['V'] = 1
        else:
            self.CNS_data['KLAMPO335']['V'] = 0
        # --------- R36  Condenser level hi (45" )
        if self.CNS_data['ZCOND']['V'] > self.CNS_data['CZCNDH']['V']:
            self.CNS_data['KLAMPO336']['V'] = 1
        else:
            self.CNS_data['KLAMPO336']['V'] = 0
        # --------- R37  TBN trip P-4
        if (self.CNS_data['KTBTRIP']['V'] == 1) and (self.CNS_data['KRXTRIP']['V'] == 1):
            self.CNS_data['KLAMPO337']['V'] = 1
        else:
            self.CNS_data['KLAMPO337']['V'] = 0
        # --------- R38  SG 1,2,3 wtr level hi-hi TBN trip
        CPERMS8 = 0.78
        if (self.CNS_data['ZSGNOR1']['V'] > CPERMS8) or \
                (self.CNS_data['ZSGNOR2']['V'] > CPERMS8) or \
                (self.CNS_data['ZSGNOR3']['V'] > CPERMS8):
            self.CNS_data['KLAMPO338']['V'] = 1
        else:
            self.CNS_data['KLAMPO338']['V'] = 0
        # --------- R39 Condenser vacuum lo TBN trip
        if (self.CNS_data['PVAC']['V'] < 620.0) and (self.CNS_data['KTBTRIP']['V'] == 1):
            self.CNS_data['KLAMPO339']['V'] = 1
        else:
            self.CNS_data['KLAMPO339']['V'] = 0
        # --------- R40  TBN overspeed hi TBN trip
        if (self.CNS_data['FTURB']['V'] > 1980.0) and (self.CNS_data['KTBTRIP']['V'] == 1):
            self.CNS_data['KLAMPO340']['V'] = 1
        else:
            self.CNS_data['KLAMPO340']['V'] = 0
        # --------- R42  Gen. brk open
        if self.CNS_data['KGENB']['V'] == 0:
            self.CNS_data['KLAMPO341']['V'] = 1
        else:
            self.CNS_data['KLAMPO341']['V'] = 0

        return 0