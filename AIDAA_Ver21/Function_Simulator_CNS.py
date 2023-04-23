from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
import pandas as pd
import numpy as np
import pickle
import socket
from struct import unpack, pack

class CNS(QWidget):
    def __init__(self, ShMem):
        super(CNS, self).__init__()
        self.ShMem: ShMem = ShMem
        self.setGeometry(50, 50, 300, 100)

        lay = QVBoxLayout(self)
        one_step_btn = QPushButton('OneStep', self)
        one_step_btn.clicked.connect(self.one_step)
        # one_step_btn.clicked.connect(self.ex)
        self.run_btn = QPushButton('Freeze', self)
        self.run_btn.clicked.connect(self.run_)
        self.run_trigger = False

        lay2 = QHBoxLayout()
        change_val_btn = QPushButton('ChangeVal', self)
        change_val_btn.clicked.connect(self.change_val)
        self.paraname = QLineEdit('para_name')
        self.paraval = QLineEdit('para_val')
        lay2.addWidget(change_val_btn)
        lay2.addWidget(self.paraname)
        lay2.addWidget(self.paraval)
        self.mes = QLabel('')
        
        lay3 = QHBoxLayout()
        change_val_cvcs_btn = QPushButton('ChangeVal_CVCS', self)
        change_val_cvcs_btn.clicked.connect(self.change_val_cvcs)
        self.paraname_cvcs = QLineEdit('para_name')
        self.paraval_cvcs = QLineEdit('para_val')
        lay3.addWidget(change_val_cvcs_btn)
        lay3.addWidget(self.paraname_cvcs)
        lay3.addWidget(self.paraval_cvcs)
        self.mes_cvcs = QLabel('')

        # ------------------------------------------------------------------
        # IP/Port 세팅
        # ------------------------------------------------------------------
        lay4 = QVBoxLayout()
        lay4_0 = QHBoxLayout()
        lay4_1 = QHBoxLayout()
        lay4_2 = QHBoxLayout()
        self.CNSMode = QCheckBox(self)
        call_init_btn = QPushButton('CallInit', self)
        call_init_btn.clicked.connect(lambda x:self.init_cns(1))
        fix_ip_port_btn  = QPushButton('Set IP/PORT', self)
        fix_ip_port_btn.clicked.connect(self.fix_ip_port)
        self.my_com_ip    = QLineEdit(f'{self.ShMem.get_udp_my_com_ip()}')
        self.my_com_port  = QLineEdit('7201')
        self.cns_com_ip   = QLineEdit('192.168.0.179')
        self.cns_com_port = QLineEdit('7201')
        
        lay4_0.addWidget(QLabel('CNS Mode'))
        lay4_0.addWidget(self.CNSMode)
        lay4_0.addWidget(call_init_btn)
        lay4_1.addWidget(QLabel('My IP/PORT'))
        lay4_1.addWidget(self.my_com_ip)
        lay4_1.addWidget(self.my_com_port)
        lay4_2.addWidget(QLabel('CNS IP/PORT'))
        lay4_2.addWidget(self.cns_com_ip)
        lay4_2.addWidget(self.cns_com_port)
        
        lay4.addLayout(lay4_0)
        lay4.addWidget(fix_ip_port_btn)
        lay4.addLayout(lay4_1)
        lay4.addLayout(lay4_2)
        # ------------------------------------------------------------------
        # Layer 구조 파트 
        # ------------------------------------------------------------------
        lay.addWidget(one_step_btn)
        lay.addWidget(self.run_btn)
        lay.addLayout(lay2)
        lay.addWidget(self.mes)
        lay.addLayout(lay3)
        lay.addWidget(self.mes_cvcs)
        lay.addLayout(lay4)
        
        self.startTimer(600) # 600ms로 one_step 호출함. self.run_ 함수 참고

# ----------------------------------------------------------------------------------------------------------------------
        # 컨트롤러 실행과 함께 AI 실행 준비
        self.AIProcedurePara = pd.read_csv('./AI/Final_parameter_200825.csv')['0'].tolist()
        self.AIProcedureModel = pickle.load(open('./AI/Ab_Diagnosis_model.h5', 'rb'))
        # ------------------------------------------------------------------
        # CNS 통신용 소켓 및 버퍼
        # ------------------------------------------------------------------ 
        self.resv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.size_buffer_mem = 46008
        self.want_tick = 5
        self.resv_sock.settimeout(5)
        self.resv_sock.bind(('192.168.0.29', 7201)) # 절대 중요 이거 바꿔야함. 컨트롤러에서 안바뀜. 절대 안바뀜.
        self.ShMem.update_cns_ip_port(self.cns_com_ip.text(), int(self.cns_com_port.text()))

    def one_step(self):
        if self.CNSMode.isChecked():
            if self.run_freeze_CNS() != 1: self.one_step_part()
        else:                           
            self.ShMem.change_para_val('KCNTOMS', self.ShMem.get_para_val('KCNTOMS') + 5)
            self.one_step_part()
    def one_step_part(self):
        self.ShMem.add_val_to_list()
        self.ShMem.update_alarmdb()
        self.ShMem.update_CVCS()
        self.mes.setText(f'OneStep 진행함. [KCNTOMS: {self.ShMem.get_para_val("KCNTOMS")}][CVCS: {self.ShMem.get_CVCS_para_val("SimTime")}]')
    def run_(self): 
        self.run_trigger = False if self.run_trigger == True else True
        _ = self.run_btn.setText('Run') if self.run_trigger == True else self.run_btn.setText('Freeze')
    def timerEvent(self, a0: 'QTimerEvent') -> None:
        _ = self.one_step() if self.run_trigger else None
        return super().timerEvent(a0)
    def change_val(self):
        if self.ShMem.check_para_name(self.paraname.text()):
            self.mes.setText(f'{self.paraname.text()} 변수 있음.')
            if self.paraval.text().isdigit():
                self.mes.setText(f'{self.paraname.text()} 변수는 {self.paraval.text()} 로 변경됨.')
                o = int(self.paraval.text()) if self.ShMem.check_para_type(self.paraname.text()) == 0 else float(self.paraval.text())
                self.ShMem.change_para_val(self.paraname.text(), o)
            else:
                self.mes.setText(f'{self.paraval_cvcs.text()} 은 숫자가 아님. 현재값:{self.ShMem.get_para_val(self.paraval.text())}')
        else:
            self.mes.setText(f'{self.paraname.text()} 변수 없음.')

        self.paraname.setText('para_name')
        self.paraval.setText('para_val')
    def change_val_cvcs(self):
        if self.ShMem.check_cvcs_para_name(self.paraname_cvcs.text()):
            self.mes_cvcs.setText(f'{self.paraname_cvcs.text()} 변수 있음.')
            if self.paraval_cvcs.text().isdigit():
                self.mes_cvcs.setText(f'{self.paraname_cvcs.text()} 변수는 {self.paraval_cvcs.text()} 로 변경됨.')
                o = int(self.paraval_cvcs.text()) if self.ShMem.check_cvcs_para_type(self.paraname_cvcs.text()) == 0 else float(self.paraval_cvcs.text())
                self.ShMem.change_cvcs_para_val(self.paraname_cvcs.text(), o)
            else:
                self.mes_cvcs.setText(f'{self.paraval_cvcs.text()} 은 숫자가 아님. 현재값:{self.ShMem.get_CVCS_para_val(self.paraname_cvcs.text())}')
        else:
            self.mes_cvcs.setText(f'{self.paraname_cvcs.text()} 변수 없음.')

        self.paraname_cvcs.setText('para_name')
        self.paraval_cvcs.setText('para_val')
    # ----------------------------------------------------------------------------------------------------------------------
    # CNS 통신용 소켓 및 버퍼 제어 함수
    # ----------------------------------------------------------------------------------------------------------------------
    def fix_ip_port(self):
        # ip / port 체크
        if self.CNSMode.isChecked():
            # try:
            #     self.resv_sock.bind((self.my_com_ip.text(), int(self.my_com_port.text())))
                
            #     # if self.resv_sock.connect_ex((self.my_com_ip.text(), int(self.my_com_port.text()))) == 0: # Success
            #     #     print('My_com_ip/port condition is good!')
            #     #     self.resv_sock.close()
            #     #     self.resv_sock.bind((self.my_com_ip.text(), int(self.my_com_port.text())))
            #     # else: print(f'[Error!] My_com_ip:{self.my_com_ip.text()} | My_com_port:{self.my_com_port.text()}')
            # except Exception as e: print(f'[Error!] My_com_ip:{self.my_com_ip.text()} | My_com_port:{self.my_com_port.text()} | {e}')
            try: 
                if self.send_sock.sendto(b'\x00\x00\x00\x10\xa8\x0f', (self.cns_com_ip.text(), int(self.cns_com_port.text()))) == 6:
                    print('CNS is connected.')
            except Exception as e: print(f'[Error!] CNS_com_ip:{self.cns_com_ip.text()} | CNS_com_port:{self.cns_com_port.text()} | {e}')
    def _update_mem(self):
        try:
            data, _ = self.resv_sock.recvfrom(self.size_buffer_mem)
            data = data[8:]
            # print(len(data)) data의 8바이트를 제외한 나머지 버퍼의 크기
            for i in range(0, len(data), 20):
                sig = unpack('h', data[16 + i: 18 + i])[0]
                para = '12sihh' if sig == 0 else '12sfhh'
                pid, val, sig, idx = unpack(para, data[i:20 + i])
                pid = pid.decode().rstrip('\x00')  # remove '\x00'
                if pid != '':
                    self.ShMem.change_para_val(pid, val)
            return 0
        except:
            print('CNS와 연결을 확인하세요...!')
            return 1
    def _send_control_signal(self, para, val):
        '''
        조작 필요없음
        :param para:
        :param val:
        :return:
        '''
        mem = self.ShMem.get_mem()
        for i in range(np.shape(para)[0]):
            mem[para[i]]['Val'] = val[i]
        UDP_header = b'\x00\x00\x00\x10\xa8\x0f'
        buffer = b'\x00' * 4008
        temp_data = b''

        # make temp_data to send CNS #
        for i in range(np.shape(para)[0]):
            pid_temp = b'\x00' * 12
            pid_temp = bytes(para[i], 'ascii') + pid_temp[len(para[i]):]  # pid + \x00 ..
            para_sw = '12sihh' if mem[para[i]]['Sig'] == 0 else '12sfhh'
            # 만약 para가 CNS DB에 포함되지 않은 Custom para이면 Pass
            if para[i][0] != 'c':
                temp_data += pack(para_sw,
                                  pid_temp,
                                  mem[para[i]]['Val'],
                                  mem[para[i]]['Sig'],
                                  mem[para[i]]['Num'])

        buffer = UDP_header + pack('h', np.shape(para)[0]) + temp_data + buffer[len(temp_data):]

        self.send_sock.sendto(buffer, (self.cns_com_ip.text(), int(self.cns_com_port.text())))
    def run_freeze_CNS(self):
        mem = self.ShMem.get_mem()
        old_cont = mem['KCNTOMS']['Val'] + self.want_tick
        self._send_control_signal(['KFZRUN'], [self.want_tick + 100])
        while True:
            break_point = self._update_mem()
            if break_point == 1: break
            mem = self.ShMem.get_mem()
            new_cont = mem['KCNTOMS']['Val']
            if old_cont == new_cont:
                if mem['KFZRUN']['Val'] == 4:
                    # 1회 run 완료 시 4로 변환
                    # 데이터가 최신으로 업데이트 되었음으로 val를 List에 append
                    # 이때 반드시 모든 Val은 업데이트 된 상태이며 Append 및 데이터 로깅도 이부분에서 수행된다.
                    self.ShMem.change_para_val('cMALA', 1 if mem['cMALT']['Val'] <= mem['KCNTOMS']['Val'] else 0)
                    self.ShMem.change_para_val('cMALCA', mem['cMALC']['Val'] if mem['cMALT']['Val'] <= mem['KCNTOMS']['Val'] else 0)
                    # self.save_line()
                    break
                else:
                    pass
            else:
                pass
        return break_point
    def init_cns(self, initial_nub):
        if self.CNSMode.isChecked():
            print(f'Call Init {initial_nub}')
            # UDP 통신에 쌇인 데이터를 새롭게 하는 기능
            self._send_control_signal(['KFZRUN', 'KSWO277'], [5, initial_nub])
            while True:
                break_point = self._update_mem()
                if break_point == 1: break
                mem = self.ShMem.get_mem()
                if mem['KFZRUN']['Val'] == 6:
                    # initial 상태가 완료되면 6으로 되고, break
                    break
                elif mem['KFZRUN']['Val'] == 5:
                    # 아직완료가 안된 상태
                    pass
                else:
                    # 4가 되는 경우: 이전의 에피소드가 끝나고 4인 상태인데
                    self._send_control_signal(['KFZRUN'], [5])
                    pass