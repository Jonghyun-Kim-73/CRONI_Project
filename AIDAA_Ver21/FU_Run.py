"""

작성자  : 이대일
일자    : 230418 

개요    : Main 화면과 통신을 위한 Qt 기반 코드
"""
from PyQt5.QtWidgets import *
from multiprocessing import Process
from multiprocessing.managers import BaseManager
import time
import sys
import socket
from struct import pack

class Shmem:
    def __init__(self) -> None:
        self.mem_structure = {
            'V0'  : {'Sig': 0, 'Val': 5},   #10si  : string(10바이트), short(2바이트), value(int or float, 4바이트) = 10바이트
            'V1'  : {'Sig': 0, 'Val': 1},   # sig = 0 int , sig = 1 float
            'V2'  : {'Sig': 1, 'Val': 1.1},
        }
        """
        예상되는 변수
        1. 발전소 변수
            ex. 압력, 수위, ... : int, float 형태
        2. Bool 값
            ex. 알람 on/off, 펌프 on/off : int 형태 (0 과 1로 구분)
            : 받는 쪽(조선대 Main interface)에서 self.mem_structure 확인 후 수정 필요함.
        """

    # def send_mem(self):
    #     buffer = b'\x00' * 180 # 10개 변수 
        
    #     for key in self.mem_structure.keys:
    
    def update_mem(self, para, val):  self.mem_structure[para]['Val'] = val
    def get_val(self, para):   return self.mem_structure[para]['Val']
    def get_mem_binary(self):
        send_buffer = b''
        buffer = b'\x00' * 16 * 10 # 10바이트 10개 변수
        for key in self.mem_structure.keys():
            para_ = b'\x00' * 10
            para_ = bytes(key, 'ascii') + para_[len(key):]  # para + \x00 ..
            pack_structure_type = '10shi' if self.mem_structure[key]['Sig'] == 0 else '10shf'
            send_buffer += pack(pack_structure_type, para_, self.mem_structure[key]['Sig'], self.mem_structure[key]['Val'])
        send_buffer = send_buffer + buffer[len(send_buffer):]
        return send_buffer

class IFAP_interface(QWidget):
    """ Qt 위젯 파트 """
    def __init__(self, mem) -> None:
        super().__init__()
        self.Shmem = mem
        self.setGeometry(0, 0, 200, 200)
        
        ly = QVBoxLayout(self)
        title = QLabel('** Test Window **')
        self.btn = QPushButton('Call UpdateMem')
        self.btn.clicked.connect(self.push_btn)
        ly.addWidget(title)
        ly.addWidget(self.btn)
        
    def push_btn(self):
        """ 버튼 클릭 시 공유메모리의 값 변경 방법 """
        print('Ok! Update Mem')
        self.Shmem.update_mem('V0', self.Shmem.get_val('V0') + 1)

class InterfaceModule(Process):
    """ 멀티프로세스를 통한 Qt 위젯 호출 모듈  """
    def __init__(self, mem):
        super().__init__()
        self.Shmem = mem
        
    def run(self) -> None:
        app = QApplication(sys.argv)
        w = IFAP_interface(self.Shmem)
        w.show()
        sys.exit(app.exec_())
        
class UDPModule(Process):
    """ UDP 통신 모듈 """
    def __init__(self, mem):
        super().__init__()
        self.Shmem = mem
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def run(self) -> None:
        while True:
            print(f'Send Value : {self.Shmem.get_val("V0")}')
            self.send_sock.sendto(self.Shmem.get_mem_binary(), ('127.0.0.1', 7001))
            time.sleep(1)
            
class Run:
    def make_shmem(self):
        """ Interface 모듈과 UDP 통신 모듈 사이의 자료교환을 위한 공유메모리 선언 """
        BaseManager.register('Shmem', Shmem)
        manager = BaseManager()
        manager.start()
        mem = manager.Shmem()
        return mem
    
    def start_process(self):
        """ MainProcess 동작 """
        mem = self.make_shmem()
        p_list = [UDPModule(mem), InterfaceModule(mem)]
        [pr_.start() for pr_ in p_list]
        [pr_.join() for pr_ in p_list]
    
if __name__ == '__main__':
    MainProcess = Run()
    MainProcess.start_process()