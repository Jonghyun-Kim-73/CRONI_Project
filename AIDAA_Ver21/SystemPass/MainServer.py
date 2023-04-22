"""
IFAP(연구소)   -|
AIDAA(조선대)   |-> MAIN(조선대)
EGIS(유니스트) -|

해당 파일은 테스트를 위한 서버 파일임.
따라서 세부에서는 변경할 필요없음.

"""

import socket
from multiprocessing import Process

class UDP_receiver(Process):
    def __init__(self, name, ip, port):
        super().__init__()
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver.bind((ip, port))
        self.name = name
    def run(self) -> None:
        while True:
            # 수신부 받기 시도 -> 받을 때 까지 대기
            message, _ = self.receiver.recvfrom(1000)
            # 메세지 받은 것을 decode
            print(f'{self.name}에서 보낸 메세지: {message.decode("utf-8")}')

if __name__ == '__main__':
    print('Main Server가 동작합니다.')
    p_list = [UDP_receiver('IFAP',  '127.0.0.1', 7001),
              UDP_receiver('AIDAA', '127.0.0.1', 7002),
              UDP_receiver('EGIS',  '127.0.0.1', 7003)]
    [pr_.start() for pr_ in p_list]
    [pr_.join() for pr_ in p_list]  # finished at the same time
    