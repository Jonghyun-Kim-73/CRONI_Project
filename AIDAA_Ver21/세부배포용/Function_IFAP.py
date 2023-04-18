import multiprocessing
import time
import socket
from struct import unpack

class FunctionIFAP(multiprocessing.Process):
    def __init__(self, mem):
        super().__init__()
        self.Shmem = mem
        self.resv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.resv_sock.settimeout(5)
        self.resv_sock.bind(('127.0.0.1', 7001)) # Main window의 ip
        self.size_buffer_mem = 16 * 10 # 10바이트 10개 변수
    
    def byte_to_dict(self, data):
        temp_dict = {}
        for i in range(0, len(data), 16): # 10바이트씩 파싱
            sig = unpack('h', data[10 + i: 12 + i])[0]
            para, sig, val = unpack('10shi', data[i:16 + i]) if sig == 0 else unpack('10shf', data[i:16 + i])
            para = para.decode().rstrip('\x00')  # remove '\x00'
            if para != '':
                temp_dict[para] = {'Sig': sig, 'Val': val}
        return temp_dict
    
    def run(self) -> None:
        while True:
            try:
                data, info = self.resv_sock.recvfrom(self.size_buffer_mem)
                self.Shmem.update_IFAP_mem(self.byte_to_dict(data))
            except Exception as e:
                print(f'Wait.. {e}')
                time.sleep(1)