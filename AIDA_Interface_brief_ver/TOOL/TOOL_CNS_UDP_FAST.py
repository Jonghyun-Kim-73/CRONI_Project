import socket
import logging
from struct import unpack, pack
from time import sleep
from numpy import shape
from collections import deque


class CNS:
    def __init__(self, threrad_name, CNS_IP, CNS_Port, Remote_IP, Remote_Port, Max_len=10):
        # thread name
        self.th_name = threrad_name
        # Ip, Port
        self.Remote_ip, self.Remote_port = Remote_IP, Remote_Port
        self.CNS_ip, self.CNS_port = CNS_IP, CNS_Port
        # Read Socket
        self.resv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.resv_sock.bind((self.Remote_ip, self.Remote_port))
        # Send Socket
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # SIZE BUFFER
        self.size_buffer_mem = 46008
        # SEND TICK
        self.want_tick = 5

        # memory
        self.max_len = Max_len
        self.mem = self._make_mem_structure(max_len=self.max_len)
        # logger path
        self.LoggerPath = ''
        self.file_name = 0

        # Control
        self.SaveControlPara = []
        self.SaveControlVal = []

    def _make_mem_initial(self):
        for pid_ in self.mem.keys():
            self.mem[pid_]['Val'] = 0

    def _make_mem_structure(self, max_len):
        # 초기 shared_mem의 구조를 선언한다.
        idx = 0
        shared_mem = {}
        for file_name in ['./db.txt', './db_add.txt']:
            with open(file_name, 'r') as f:
                while True:
                    temp_ = f.readline().split('\t')
                    if temp_[0] == '':  # if empty space -> break
                        break
                    if temp_[0] == '#': # Pass this value. We don't require this value.
                        pass            # These values are normally static values in SMABRES Code.
                    else:
                        sig = 0 if temp_[1] == 'INTEGER' else 1
                        shared_mem[temp_[0]] = {'Sig': sig, 'Val': 0, 'Num': idx, 'List': deque(maxlen=max_len)}
                        idx += 1

        # 다음과정을 통하여 shared_mem 은 PID : { type. val, num }를 가진다.
        return shared_mem

    def _update_mem(self):
        data, _ = self.resv_sock.recvfrom(self.size_buffer_mem)
        data = data[8:]
        # print(len(data)) data의 8바이트를 제외한 나머지 버퍼의 크기
        for i in range(0, len(data), 20):
            sig = unpack('h', data[16 + i: 18 + i])[0]
            para = '12sihh' if sig == 0 else '12sfhh'
            pid, val, sig, idx = unpack(para, data[i:20 + i])
            pid = pid.decode().rstrip('\x00')  # remove '\x00'
            if pid != '':
                self.mem[pid]['Val'] = val

        # Alarm reprocessing
        self._AlarmReprocessing()

    def _append_val_to_list(self):
        [self.mem[pid]['List'].append(self.mem[pid]['Val']) for pid in self.mem.keys()]
        return 0

    # -------
    def _send_control_initial(self):
        self.SaveControlPara = []
        self.SaveControlVal = []

    def _send_control_signal(self, para, val):
        '''
        조작 필요없음
        :param para:
        :param val:
        :return:
        '''
        for i in range(shape(para)[0]):
            self.mem[para[i]]['Val'] = val[i]
        UDP_header = b'\x00\x00\x00\x10\xa8\x0f'
        buffer = b'\x00' * 4008
        temp_data = b''

        # make temp_data to send CNS #
        for i in range(shape(para)[0]):
            pid_temp = b'\x00' * 12
            pid_temp = bytes(para[i], 'ascii') + pid_temp[len(para[i]):]  # pid + \x00 ..

            para_sw = '12sihh' if self.mem[para[i]]['Sig'] == 0 else '12sfhh'

            # 만약 para가 CNS DB에 포함되지 않은 Custom para이면 Pass
            if para[i][0] != 'c':
                temp_data += pack(para_sw,
                                  pid_temp,
                                  self.mem[para[i]]['Val'],
                                  self.mem[para[i]]['Sig'],
                                  self.mem[para[i]]['Num'])

        buffer = UDP_header + pack('h', shape(para)[0]) + temp_data + buffer[len(temp_data):]

        self.send_sock.sendto(buffer, (self.CNS_ip, self.CNS_port))

    def _send_control_save(self, para, val):
        """
        para와 val을 받아서 save
        :param para: [a, b, c]
        :param val: [1, 2, 3]
        :return: -
        """
        for _ in range(len(para)):
            self.SaveControlPara.append(para[_])
            self.SaveControlVal.append(val[_])

    def _send_control_to_cns(self):
        """
        Close send function
        ex.
            _send_control_save(['Para', 'Para'],[1, 1])
            _send_control_to_cns()
        :return: 0 or 1
        """
        if self.SaveControlPara != []:
            self._send_control_signal(self.SaveControlPara, self.SaveControlVal)
            self._send_control_initial()
            return 0    # Send function Success
        else:
            return 1    # Send function Fail due to no value in self.SaveControlPara

    def _send_malfunction_signal(self, Mal_nub, Mal_opt, Mal_time):
        '''
        CNS_04_18.tar 버전에서 동작함.
        :param Mal_nub: Malfunction 번호
        :param Mal_opt: Malfunction operation
        :param Mal_time: Malfunction의 동작하는 시간
        :return:
        '''
        if Mal_time == 0:
            Mal_time = 5
        else:
            Mal_time = Mal_time ## 1초 * 5Tick 고려해서 넣을 것
        return self._send_control_signal(['KFZRUN', 'KSWO280', 'KSWO279', 'KSWO278'],
                                         [10, Mal_nub, Mal_opt, Mal_time])

    def _AlarmReprocessing(self):
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
        if self.mem['XPIRM']['Val'] > self.mem['CIRFH']['Val']:
            self.mem['KLAMPO251']['Val'] = 1
        else:
            self.mem['KLAMPO251']['Val'] = 0
        # --------- L2  Power range overpower rod stop(103% of FP)
        if self.mem['QPROREL']['Val'] > self.mem['CPRFH']['Val']:
            self.mem['KLAMPO252']['Val'] = 1
        else:
            self.mem['KLAMPO252']['Val'] = 0
        # --------- L3  Control bank D full rod withdrawl(220 steps)
        if self.mem['KZBANK4']['Val'] > 220:
            self.mem['KLAMPO253']['Val'] = 1
        else:
            self.mem['KLAMPO253']['Val'] = 0
        # --------- L4  Control bank lo-lo limit
        # ******* Insertion limit(Reference : KNU 5&6 PLS)
        #
        RDTEMP = (self.mem['UMAXDT']['Val']/self.mem['CDT100']['Val']) * 100.0
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

            if self.mem['KBNKSEL']['Val'] == 1:
                KRILM = KRIL1
            elif self.mem['KBNKSEL']['Val'] == 2:
                KRILM = KRIL2
            elif self.mem['KBNKSEL']['Val'] == 3:
                KRILM = KRIL3
            elif self.mem['KBNKSEL']['Val'] == 4:
                KRILM = KRIL4
            else:
                KRILM = 0

            if ((self.mem['KZBANK1']['Val'] < KRIL1) or (self.mem['KZBANK2']['Val'] < KRIL2)
                    or (self.mem['KZBANK3']['Val'] < KRIL3) or (self.mem['KZBANK4']['Val'] < KRIL4)):
                self.mem['KLAMPO254']['Val'] = 1
            else:
                self.mem['KLAMPO254']['Val'] = 0
        # --------- L5  Two or more rod at bottom(ref:A-II-8 p.113 & KAERI87-39)
        IROD = 0
        for _ in range(1, 53):
            if self.mem[f'KZROD{_}']['Val'] < 0.0:
                IROD += 1
        if IROD > 2:
            self.mem['KLAMPO255']['Val'] = 1
        else:
            self.mem['KLAMPO255']['Val'] = 0
        # --------- L6  Axial power distribution limit(3% ~ -12%)
        if (self.mem['CAXOFF']['Val'] >= self.mem['CAXOFDL']['Val']) or \
                (self.mem['CAXOFF']['Val'] <= (self.mem['CAXOFDL']['Val'] - 0.75)):
            self.mem['KLAMPO256']['Val'] = 1
        else:
            self.mem['KLAMPO256']['Val'] = 0
        # --------- L7  CCWS outlet temp hi(49.0 deg C)
        if self.mem['UCCWIN']['Val'] >= self.mem['CUCCWH']['Val']:
            self.mem['KLAMPO257']['Val'] = 1
        else:
            self.mem['KLAMPO257']['Val'] = 0
        # --------- L8  Instrument air press lo(6.3 kg/cm2)
        if self.mem['PINSTA']['Val'] <= (self.mem['CINSTP']['Val'] - 1.5):
            self.mem['KLAMPO258']['Val'] = 1
        else:
            self.mem['KLAMPO258']['Val'] = 0
        # --------- L9  RWST level lo-lo(5%)
        if self.mem['ZRWST']['Val'] <= self.mem['CZRWSLL']['Val']:
            self.mem['KLAMPO259']['Val'] = 1
        else:
            self.mem['KLAMPO259']['Val'] = 0
        # --------- L10  L/D HX outlet flow lo(15 m3/hr)
        if self.mem['WNETLD']['Val'] < self.mem['CWLHXL']['Val']:
            self.mem['KLAMPO260']['Val'] = 1
        else:
            self.mem['KLAMPO260']['Val'] = 0
        # --------- L11  L/D HX outlet temp hi(58 deg C)
        if self.mem['UNRHXUT']['Val'] > self.mem['CULDHX']['Val']:
            self.mem['KLAMPO261']['Val'] = 1
        else:
            self.mem['KLAMPO261']['Val'] = 0
        # --------- L12  RHX L/D outlet temp hi(202 deg C)
        if self.mem['URHXUT']['Val'] > self.mem['CURHX']['Val']:
            self.mem['KLAMPO262']['Val'] = 1
        else:
            self.mem['KLAMPO262']['Val'] = 0
        # --------- L13  VCT level lo(20 %)
        if self.mem['ZVCT']['Val'] < self.mem['CZVCT2']['Val']:
            self.mem['KLAMPO263']['Val'] = 1
        else:
            self.mem['KLAMPO263']['Val'] = 0
        # --------- L14  VCT press lo(0.7 kg/cm2)
        if self.mem['PVCT']['Val'] < self.mem['CPVCTL']['Val']:
            self.mem['KLAMPO264']['Val'] = 1
        else:
            self.mem['KLAMPO264']['Val'] = 0
        # --------- L15  RCP seal inj wtr flow lo(1.4 m3/hr)
        if (self.mem['WRCPSI1']['Val'] < self.mem['CWRCPS']['Val'] or
                self.mem['WRCPSI2']['Val'] < self.mem['CWRCPS']['Val'] or
                self.mem['WRCPSI2']['Val'] < self.mem['CWRCPS']['Val']):
            self.mem['KLAMPO265']['Val'] = 1
        else:
            self.mem['KLAMPO265']['Val'] = 0
        # --------- L16  Charging flow cont flow lo(5 m3/hr)
        if self.mem['WCHGNO']['Val'] < self.mem['CWCHGL']['Val']:
            self.mem['KLAMPO266']['Val'] = 1
        else:
            self.mem['KLAMPO266']['Val'] = 0
        # --------- R17  Not used
        self.mem['KLAMPO267']['Val'] = 0
        # --------- L18  L/D HX outlet flow hi (30  m3/hr)
        if self.mem['WNETLD']['Val'] > self.mem['CWLHXH']['Val']:
            self.mem['KLAMPO268']['Val'] = 1
        else:
            self.mem['KLAMPO268']['Val'] = 0
        # --------- L19  PRZ press lo SI
        CSAFEI = {1: 124.e5, 2: 40.3e5}
        if (self.mem['PPRZN']['Val'] < CSAFEI[1]) and (self.mem['KSAFEI']['Val'] == 1):
            self.mem['KLAMPO269']['Val'] = 1
        else:
            self.mem['KLAMPO269']['Val'] = 0
        # --------- L20 CTMT spray actuated
        if self.mem['KCTMTSP']['Val'] == 1:
            self.mem['KLAMPO270']['Val'] = 1
        else:
            self.mem['KLAMPO270']['Val'] = 0
        # --------- L21  VCT level hi(80 %)
        if self.mem['ZVCT']['Val'] > self.mem['CZVCT6']['Val']:
            self.mem['KLAMPO271']['Val'] = 1
        else:
            self.mem['KLAMPO271']['Val'] = 0
        # --------- L22 VCT press hi (4.5 kg/cm2)
        if self.mem['PVCT']['Val'] > self.mem['CPVCTH']['Val']:
            self.mem['KLAMPO272']['Val'] = 1
        else:
            self.mem['KLAMPO272']['Val'] = 0
        # --------- L23  CTMT phase B iso actuated
        if self.mem['KCISOB']['Val'] == 1:
            self.mem['KLAMPO273']['Val'] = 1
        else:
            self.mem['KLAMPO273']['Val'] = 0
        # --------- L24  Charging flow cont flow hi(27 m3/hr)
        if self.mem['WCHGNO']['Val'] > self.mem['CWCHGH']['Val']:
            self.mem['KLAMPO274']['Val'] = 1
        else:
            self.mem['KLAMPO274']['Val'] = 0
        # ---------

        # --------- R43  Not used
        self.mem['KLAMPO293']['Val'] = 0
        # --------- R44  Not used
        self.mem['KLAMPO294']['Val'] = 0
        # --------- L45  CTMT sump level hi
        CZSMPH = {1: 2.492, 2: 2.9238}
        if self.mem['ZSUMP']['Val'] > CZSMPH[1]:
            self.mem['KLAMPO295']['Val'] = 1
        else:
            self.mem['KLAMPO295']['Val'] = 0
        # --------- L46 CTMT sump level hi-hi
        if self.mem['ZSUMP']['Val'] > CZSMPH[2]:
            self.mem['KLAMPO296']['Val'] = 1
        else:
            self.mem['KLAMPO296']['Val'] = 0
        # --------- L47  CTMT air temp hi(48.89 deg C)
        if self.mem['UCTMT']['Val'] > self.mem['CUCTMT']['Val']:
            self.mem['KLAMPO297']['Val'] = 1
        else:
            self.mem['KLAMPO297']['Val'] = 0
        # --------- L48  CTMT moisture hi(70% of R.H.)
        if self.mem['HUCTMT']['Val'] > self.mem['CHCTMT']['Val']:
            self.mem['KLAMPO298']['Val'] = 1
        else:
            self.mem['KLAMPO298']['Val'] = 0
        #
        # Right panel
        #
        # --------- R1  Rad hi alarm
        if (self.mem['DCTMT']['Val'] > self.mem['CRADHI']['Val']) or \
                (self.mem['DSECON']['Val'] >= 3.9E-3):
            self.mem['KLAMPO301']['Val'] = 1
        else:
            self.mem['KLAMPO301']['Val'] = 0
        # --------- R2  CTMT press hi 1 alert
        CPCMTH = {1: 0.3515, 2: 1.02, 3: 1.62}
        if self.mem['PCTMT']['Val'] * self.mem['PAKGCM']['Val'] > CPCMTH[1]:
            self.mem['KLAMPO302']['Val'] = 1
        else:
            self.mem['KLAMPO302']['Val'] = 0
        # --------- R3  CTMT press hi 2 alert
        if self.mem['PCTMT']['Val'] * self.mem['PAKGCM']['Val'] > CPCMTH[2]:
            self.mem['KLAMPO303']['Val'] = 1
        else:
            self.mem['KLAMPO303']['Val'] = 0
        # --------- R4  CTMT press hi 3 alert
        if self.mem['PCTMT']['Val'] * self.mem['PAKGCM']['Val'] > CPCMTH[3]:
            self.mem['KLAMPO304']['Val'] = 1
        else:
            self.mem['KLAMPO304']['Val'] = 0
        # --------- R5  Accum. Tk press lo (43.4 kg/cm2)
        if self.mem['PACCTK']['Val'] < self.mem['CPACCL']['Val']:
            self.mem['KLAMPO305']['Val'] = 1
        else:
            self.mem['KLAMPO305']['Val'] = 0
        # --------- R6  Accum. Tk press hi ( /43.4 kg/cm2)
        if self.mem['PACCTK']['Val'] > self.mem['CPACCH']['Val']:
            self.mem['KLAMPO306']['Val'] = 1
        else:
            self.mem['KLAMPO306']['Val'] = 0
        # --------- R7  PRZ press hi alert(162.4 kg/cm2)
        if self.mem['PPRZ']['Val'] > self.mem['CPPRZH']['Val']:
            self.mem['KLAMPO307']['Val'] = 1
        else:
            self.mem['KLAMPO307']['Val'] = 0
        # --------- R8  PRZ press lo alert(153.6 kg/cm2)
        if self.mem['PPRZ']['Val'] < self.mem['CPPRZL']['Val']:
            self.mem['KLAMPO308']['Val'] = 1
        else:
            self.mem['KLAMPO308']['Val'] = 0
        # --------- R9  PRZ PORV opening(164.2 kg/cm2)
        if self.mem['BPORV']['Val'] > 0.01:
            self.mem['KLAMPO309']['Val'] = 1
        else:
            self.mem['KLAMPO309']['Val'] = 0
        # --------- R10 PRZ cont level hi heater on(over 5%) !%deail....
        DEPRZ = self.mem['ZINST63']['Val'] / 100
        if (DEPRZ > (self.mem['ZPRZSP']['Val'] + self.mem['CZPRZH']['Val'])) and (self.mem['QPRZB']['Val'] > self.mem['CQPRZP']['Val']):
            self.mem['KLAMPO310']['Val'] = 1
        else:
            self.mem['KLAMPO310']['Val'] = 0
        # --------- R11  PRZ cont level lo heater off(17%) !%deail....
        if (DEPRZ < self.mem['CZPRZL']['Val']) and (self.mem['QPRZ']['Val'] >= self.mem['CQPRZP']['Val']):
            self.mem['KLAMPO311']['Val'] = 1
        else:
            self.mem['KLAMPO311']['Val'] = 0
        # --------- R12  PRZ press lo back-up heater on(153.6 kg/cm2)
        if (self.mem['PPRZN']['Val'] < self.mem['CQPRZB']['Val']) and (self.mem['KBHON']['Val'] == 1):
            self.mem['KLAMPO312']['Val'] = 1
        else:
            self.mem['KLAMPO312']['Val'] = 0
        # --------- R13  Tref/Auct. Tavg Deviation(1.67 deg C)
        if ((self.mem['UAVLEGS']['Val'] - self.mem['UAVLEGM']['Val']) > self.mem['CUTDEV']['Val']) or\
                ((self.mem['UAVLEGM']['Val'] - self.mem['UAVLEGS']['Val']) > self.mem['CUTDEV']['Val']):
            self.mem['KLAMPO313']['Val'] = 1
        else:
            self.mem['KLAMPO313']['Val'] = 0
        # --------- R14 RCS 1,2,3 Tavg hi(312.78 deg C)
        if self.mem['UAVLEGM']['Val'] > self.mem['CUTAVG']['Val']:
            self.mem['KLAMPO314']['Val'] = 1
        else:
            self.mem['KLAMPO314']['Val'] = 0
        # --------- R15  RCS 1,2,3 Tavg/auct Tavg hi/lo(1.1 deg C)
        RUAVMX = max(self.mem['UAVLEG1']['Val'], self.mem['UAVLEG2']['Val'],
                     self.mem['UAVLEG3']['Val'])
        RAVGT = {1: abs((self.mem['UAVLEG1']['Val']) - RUAVMX),
                 2: abs((self.mem['UAVLEG2']['Val']) - RUAVMX),
                 3: abs((self.mem['UAVLEG3']['Val']) - RUAVMX)}
        if max(RAVGT[1], RAVGT[2], RAVGT[3]) > self.mem['CUAUCT']['Val']:
            self.mem['KLAMPO315']['Val'] = 1
        else:
            self.mem['KLAMPO315']['Val'] = 0
        # --------- R16  RCS 1,2,3 lo flow alert(92% from KAERI87-37)
        CWSGRL = {1: 4232.0, 2: 0.0}
        if ((self.mem['WSGRCP1']['Val'] < CWSGRL[1] and self.mem['KRCP1']['Val'] == 1) or
                (self.mem['WSGRCP1']['Val'] < CWSGRL[1] and self.mem['KRCP1']['Val'] == 1) or
                (self.mem['WSGRCP1']['Val'] < CWSGRL[1] and self.mem['KRCP1']['Val'] == 1)):
            self.mem['KLAMPO316']['Val'] = 1
        else:
            self.mem['KLAMPO316']['Val'] = 0
        # --------- R17  PRT temp hi(45deg C )
        if self.mem['UPRT']['Val'] > self.mem['CUPRT']['Val']:
            self.mem['KLAMPO317']['Val'] = 1
        else:
            self.mem['KLAMPO317']['Val'] = 0
        # --------- R18  PRT  press hi( 0.6kg/cm2)
        if (self.mem['PPRT']['Val'] - 0.98E5) > self.mem['CPPRT']['Val']:
            self.mem['KLAMPO318']['Val'] = 1
        else:
            self.mem['KLAMPO318']['Val'] = 0
        # --------- R19  SG 1,2,3 level lo(25% of span)
        if (self.mem['ZINST78']['Val']*0.01 < self.mem['CZSGW']['Val']) \
                or (self.mem['ZINST77']['Val']*0.01 < self.mem['CZSGW']['Val']) \
                or (self.mem['ZINST76']['Val']*0.01 < self.mem['CZSGW']['Val']):
            self.mem['KLAMPO319']['Val'] = 1
        else:
            self.mem['KLAMPO319']['Val'] = 0
        # --------- R20  SG 1,2,3 stm/FW flow deviation(10% of loop flow)
        RSTFWD = {1: self.mem['WSTM1']['Val'] * 0.1,
                  2: self.mem['WSTM2']['Val'] * 0.1,
                  3: self.mem['WSTM3']['Val'] * 0.1}
        if (((self.mem['WSTM1']['Val'] - self.mem['WFWLN1']['Val']) > RSTFWD[1]) or
                ((self.mem['WSTM2']['Val'] - self.mem['WFWLN2']['Val']) > RSTFWD[2]) or
                ((self.mem['WSTM3']['Val'] - self.mem['WFWLN3']['Val']) > RSTFWD[3])):
            self.mem['KLAMPO320']['Val'] = 1
        else:
            self.mem['KLAMPO320']['Val'] = 0
        # --------- R21 RCP 1,2,3 trip
        if self.mem['KRCP1']['Val'] + self.mem['KRCP2']['Val'] + self.mem['KRCP3']['Val'] != 3:
            self.mem['KLAMPO321']['Val'] = 1
        else:
            self.mem['KLAMPO321']['Val'] = 0
        # --------- R22  Condensate stor Tk level  lo
        CZCTKL = {1: 8.55, 2: 7.57}
        if self.mem['ZCNDTK']['Val'] < CZCTKL[1]:
            self.mem['KLAMPO322']['Val'] = 1
        else:
            self.mem['KLAMPO322']['Val'] = 0
        # --------- R23  Condensate stor Tk level lo-lo
        if self.mem['ZCNDTK']['Val'] < CZCTKL[2]:
            self.mem['KLAMPO323']['Val'] = 1
        else:
            self.mem['KLAMPO323']['Val'] = 0
        # --------- R24  Condensate stor Tk level hi
        if self.mem['ZCNDTK']['Val'] > self.mem['CZCTKH']['Val']:
            self.mem['KLAMPO324']['Val'] = 1
        else:
            self.mem['KLAMPO324']['Val'] = 0
        # --------- R25  MSIV tripped
        if self.mem['BHV108']['Val'] == 0 or self.mem['BHV208']['Val'] == 0 or self.mem['BHV308']['Val'] == 0:
            self.mem['KLAMPO325']['Val'] = 1
        else:
            self.mem['KLAMPO325']['Val'] = 0
        # --------- R26  MSL press rate hi steam iso
        if len(self.mem['KLAMPO325']['List']) >= 3:
            PSGLP = {1: self.mem['PSG1']['List'][-2],
                     2: self.mem['PSG2']['List'][-2],
                     3: self.mem['PSG3']['List'][-2]}
            RMSLPR = {1: abs((PSGLP[1] - self.mem['PSG1']['List'][-1]) * 5.0),
                      2: abs((PSGLP[2] - self.mem['PSG2']['List'][-1]) * 5.0),
                      3: abs((PSGLP[3] - self.mem['PSG3']['List'][-1]) * 5.0)}

            if (((RMSLPR[1] >= self.mem['CMSLH']['Val']) or
                (RMSLPR[2] >= self.mem['CMSLH']['Val']) or
                (RMSLPR[3] >= self.mem['CMSLH']['Val'])) and (self.mem['KMSISO']['Val'] == 1)):
                self.mem['KLAMPO326']['Val'] = 1
            else:
                self.mem['KLAMPO326']['Val'] = 0
        # --------- RK27  MSL 1,2,3 press rate hi(-7.03 kg/cm*2/sec = 6.89E5 Pa/sec)
            if ((RMSLPR[1] >= self.mem['CMSLH']['Val']) or
                (RMSLPR[2] >= self.mem['CMSLH']['Val']) or
                (RMSLPR[3] >= self.mem['CMSLH']['Val'])):
                self.mem['KLAMPO327']['Val'] = 1
            else:
                self.mem['KLAMPO327']['Val'] = 0
        # --------- R28  MSL 1,2,3 press low(41.1 kg/cm*2 = 0.403E7 pas)
        if ((self.mem['PSG1']['Val'] < self.mem['CPSTML']['Val']) or
            (self.mem['PSG2']['Val'] < self.mem['CPSTML']['Val']) or
            (self.mem['PSG3']['Val'] < self.mem['CPSTML']['Val'])):
            self.mem['KLAMPO328']['Val'] = 1
        else:
            self.mem['KLAMPO328']['Val'] = 0
        # --------- R29  AFW(MD) actuated
        if (self.mem['KAFWP1']['Val'] == 1) or (self.mem['KAFWP3']['Val'] == 1):
            self.mem['KLAMPO329']['Val'] = 1
        else:
            self.mem['KLAMPO329']['Val'] = 0
        # --------- R30  Condenser level lo(27")
        if self.mem['ZCOND']['Val'] < self.mem['CZCNDL']['Val']:
            self.mem['KLAMPO330']['Val'] = 1
        else:
            self.mem['KLAMPO330']['Val'] = 0
        # --------- R31  FW pump discharge header press hi
        if self.mem['PFWPOUT']['Val'] > self.mem['CPFWOH']['Val']:
            self.mem['KLAMPO331']['Val'] = 1
        else:
            self.mem['KLAMPO331']['Val'] = 0
        # --------- R32  FW pump trip
        if (self.mem['KFWP1']['Val'] + self.mem['KFWP2']['Val'] + self.mem['KFWP3']['Val']) == 0:
            self.mem['KLAMPO332']['Val'] = 1
        else:
            self.mem['KLAMPO332']['Val'] = 0
        # --------- R33  FW temp hi(231.1 deg C)
        if self.mem['UFDW']['Val'] > self.mem['CUFWH']['Val']:
            self.mem['KLAMPO333']['Val'] = 1
        else:
            self.mem['KLAMPO333']['Val'] = 0
        # --------- R34  Condensate pump flow lo(1400 gpm=88.324 kg/s)
        if self.mem['WCDPO']['Val'] * 0.047 > self.mem['CWCDPO']['Val']:
            self.mem['KLAMPO334']['Val'] = 1
        else:
            self.mem['KLAMPO334']['Val'] = 0
        # --------- R35  Condenser abs press hi(633. mmmHg)
        if self.mem['PVAC']['Val'] < self.mem['CPVACH']['Val']:
            self.mem['KLAMPO335']['Val'] = 1
        else:
            self.mem['KLAMPO335']['Val'] = 0
        # --------- R36  Condenser level hi (45" )
        if self.mem['ZCOND']['Val'] > self.mem['CZCNDH']['Val']:
            self.mem['KLAMPO336']['Val'] = 1
        else:
            self.mem['KLAMPO336']['Val'] = 0
        # --------- R37  TBN trip P-4
        if (self.mem['KTBTRIP']['Val'] == 1) and (self.mem['KRXTRIP']['Val'] == 1):
            self.mem['KLAMPO337']['Val'] = 1
        else:
            self.mem['KLAMPO337']['Val'] = 0
        # --------- R38  SG 1,2,3 wtr level hi-hi TBN trip
        CPERMS8 = 0.78
        if (self.mem['ZSGNOR1']['Val'] > CPERMS8) or \
                (self.mem['ZSGNOR2']['Val'] > CPERMS8) or \
                (self.mem['ZSGNOR3']['Val'] > CPERMS8):
            self.mem['KLAMPO338']['Val'] = 1
        else:
            self.mem['KLAMPO338']['Val'] = 0
        # --------- R39 Condenser vacuum lo TBN trip
        if (self.mem['PVAC']['Val'] < 620.0) and (self.mem['KTBTRIP']['Val'] == 1):
            self.mem['KLAMPO339']['Val'] = 1
        else:
            self.mem['KLAMPO339']['Val'] = 0
        # --------- R40  TBN overspeed hi TBN trip
        if (self.mem['FTURB']['Val'] > 1980.0) and (self.mem['KTBTRIP']['Val'] == 1):
            self.mem['KLAMPO340']['Val'] = 1
        else:
            self.mem['KLAMPO340']['Val'] = 0
        # --------- R42  Gen. brk open
        if self.mem['KGENB']['Val'] == 0:
            self.mem['KLAMPO341']['Val'] = 1
        else:
            self.mem['KLAMPO341']['Val'] = 0

        return 0

    # -------

    def run_cns(self):
        para = []
        sig = []
        # if self.mem['QPROREL']['Val'] >= 0.04 and self.mem['KBCDO17']['Val'] <= 1800:
        #     if self.mem['KBCDO17']['Val'] < 1780: # 1780 -> 1872
        #         para.append('KSWO213')
        #         sig.append(1)
        #     elif self.mem['KBCDO17']['Val'] >= 1780:
        #         para.append('KSWO213')
        #         sig.append(0)
        # if self.mem['KBCDO19']['Val'] >= 1780 and self.mem['KLAMPO224']['Val'] == 0: # and self.mem['QPROREL']['Val'] >= 0.15:
        #     para.append('KSWO244')
        #     sig.append(1)
        para.append('KFZRUN')
        # sig.append(3)
        sig.append(self.want_tick+100)     # 400 - 100 -> 300 tick 20 sec
        return self._send_control_signal(para, sig)

    def init_cns(self, initial_nub):
        # UDP 통신에 쌇인 데이터를 새롭게 하는 기능
        self._send_control_signal(['KFZRUN', 'KSWO277'], [5, initial_nub])
        while True:
            self._update_mem()
            if self.mem['KFZRUN']['Val'] == 6:
                # initial 상태가 완료되면 6으로 되고, break
                break
            elif self.mem['KFZRUN']['Val'] == 5:
                # 아직완료가 안된 상태
                pass
            else:
                # 4가 되는 경우: 이전의 에피소드가 끝나고 4인 상태인데
                self._send_control_signal(['KFZRUN'], [5])
                pass

    def run_freeze_CNS(self):
        old_cont = self.mem['KCNTOMS']['Val'] + self.want_tick
        self.run_cns()
        while True:
            self._update_mem()
            new_cont = self.mem['KCNTOMS']['Val']
            if old_cont == new_cont:
                if self.mem['KFZRUN']['Val'] == 4:
                    # 1회 run 완료 시 4로 변환
                    # 데이터가 최신으로 업데이트 되었음으로 val를 List에 append
                    # 이때 반드시 모든 Val은 업데이트 된 상태이며 Append 및 데이터 로깅도 이부분에서 수행된다.
                    self.mem['cMALA']['Val'] = 1 if self.mem['cMALT']['Val'] <= self.mem['KCNTOMS']['Val'] else 0
                    self.mem['cMALCA']['Val'] = self.mem['cMALC']['Val'] if self.mem['cMALT']['Val'] <= self.mem['KCNTOMS']['Val'] else 0
                    self.save_line()
                    break
                else:
                    pass
            else:
                pass

    def get_CNS_time(self):
        return self.mem['KCNTOMS']['Val']

    # logger
    def init_line(self):
        with open(f"./{self.LoggerPath}/{self.file_name}.txt", 'w') as f:
            DIS = ''
            for para_name in self.mem.keys():
                DIS += f'{para_name},'
            f.write(f'{DIS}\n')

    def save_line(self):
        with open(f"./{self.LoggerPath}/{self.file_name}.txt", 'a') as f:
            DIS = ''
            for para_name in self.mem.keys():
                DIS += f"{self.mem[para_name]['Val']},"
            f.write(f'{DIS}\n')

    # 실제 사용 Level
    def reset(self, initial_nub=1, mal=False, mal_case=0, mal_opt=0, mal_time=0, file_name=0):
        self.file_name = file_name # Update ep number
        self.init_line()

        # mem reset
        # self.mem = self._make_mem_structure(max_len=self.max_len)
        self._make_mem_initial()

        self.mem['cINIT']['Val'] = initial_nub
        self.mem['cMAL']['Val'] = 1 if mal is True else 0
        self.mem['cMALA']['Val'] = 0

        self.mem['cMALC']['Val'] = mal_case
        self.mem['cMALO']['Val'] = mal_opt
        self.mem['cMALT']['Val'] = mal_time

        self.init_cns(initial_nub=initial_nub)
        sleep(1)
        if mal:
            self._send_malfunction_signal(Mal_nub=mal_case, Mal_opt=mal_opt, Mal_time=mal_time)
            sleep(2)
            # if mal_case2 != 0:
            #     self._send_malfunction_signal(Mal_nub=mal_case2, Mal_opt=mal_opt2, Mal_time=mal_time2)
            #     sleep(2)

    def step(self):
        self.run_freeze_CNS()


if __name__ == '__main__':
    module = CNS('Main', '192.168.0.103', 7101, '192.168.0.29', 7101)
    module.init_cns(1)
    print(module.mem['KFZRUN']['Val'], module.mem['KCNTOMS']['Val'])
    module._send_malfunction_signal(12, 100100, 10)
    sleep(1)
    print(module.mem['KFZRUN']['Val'], module.mem['KCNTOMS']['Val'])
    for _ in range(20):
        module.run_freeze_CNS()
        print(module.mem['KFZRUN']['Val'], module.mem['KCNTOMS']['Val'])

    module.init_cns(2)
    print(module.mem['KFZRUN']['Val'], module.mem['KCNTOMS']['Val'])
    for _ in range(5):
        module.run_freeze_CNS()
        print(module.mem['KFZRUN']['Val'], module.mem['KCNTOMS']['Val'])