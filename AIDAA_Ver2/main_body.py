"""
Title       : AIDAA Ver2
Developer   : Daeil Lee
Date        : 2021.10.14
"""

import argparse
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))    # 콘솔용 절대 경로

import socket
from multiprocessing.managers import BaseManager

from AIDAA_Ver2.TOOL.TOOL_etc import p_
from AIDAA_Ver2.TOOL.TOOL_Shmem import SHMem
from AIDAA_Ver2.Interface.CNS_Controller.CNS_Platform_controller import InterfaceFun
from AIDAA_Ver2.Env.ENVCNSwithAI import All_Function_module

ip_reg = {
    # 자기 본래 아이피 : {'내부망 아이피' ...}
    '203.237.121.221': {'comip': '192.168.142.1', 'comport': 7101, 'cnsip': '192.168.142.133', 'cnsport': 7101},   # 상원
    '203.237.111.148': {'comip': '192.168.32.1', 'comport': 7101, 'cnsip': '192.168.32.135', 'cnsport': 7101},     # 혜선
    '192.168.0.29': {'comip': '192.168.0.29', 'comport': 7105, 'cnsip': '192.168.0.101', 'cnsport': 7105},       # 대일
    '192.168.0.10': {'comip': '192.168.0.29', 'comport': 7105, 'cnsip': '192.168.0.101', 'cnsport': 7105},       # 대일
    '192.168.72.1': {'comip': '192.168.0.192', 'comport': 7101, 'cnsip': '192.168.0.107', 'cnsport': 7101},        # 윤히
    '192.168.32.1': {'comip': '192.168.37.1', 'comport': 7101, 'cnsip': '192.168.37.129', 'cnsport': 7101},        # 상현
    '169.254.32.88': {'comip': '192.168.37.1', 'comport': 7101, 'cnsip': '192.168.37.129', 'cnsport': 7101},       # 지훈
}


class Body:
    def __init__(self):
        get_com_ip = socket.gethostbyname(socket.getfqdn())
        # 초기 입력 인자 전달 --------------------------------------------------------------------------------------------
        parser = argparse.ArgumentParser(description='CNS 플랫폼_Ver0')
        parser.add_argument('--test', default=False, required=False, action="store_true",
                            help='인터페이스 테스트 모드 [default=False]')
        parser.add_argument('--comip', type=str, default=ip_reg[get_com_ip]['comip'], required=False,
                            help="현재 컴퓨터의 ip [default='']")
        parser.add_argument('--comport', type=int, default=ip_reg[get_com_ip]['comport'], required=False,
                            help="현재 컴퓨터의 port [default=7001]")
        parser.add_argument('--cnsip', type=str, default=ip_reg[get_com_ip]['cnsip'], required=False,
                            help="CNS 컴퓨터의 ip [default='']")
        parser.add_argument('--cnsport', type=int, default=ip_reg[get_com_ip]['cnsport'], required=False,
                            help="CNS 컴퓨터의 port [default=7001]")
        self.args = parser.parse_args()
        print('=' * 25 + '초기입력 파라메터' + '=' * 25)

        if self.args.test:
            p_(__file__, 'Test Mode')
        # --------------------------------------------------------------------------------------------------------------

    def start(self):
        """ Main Body 메인 로직 시작 """
        max_len_deque = 20  # 공유 메모리에 쌓을 최대 buffer

        BaseManager.register('SHMem', SHMem)
        manager = BaseManager()
        manager.start()
        shmem = manager.SHMem(cnsinfo=(self.args.cnsip, self.args.cnsport),
                              remoteinfo=(self.args.comip, self.args.comport),
                              max_len_deque=max_len_deque)

        p_ai = All_Function_module(shmem, max_len_deque, self.args.test)

        # Build Interface
        p = InterfaceFun(shmem)

        p_list = [p_ai, p]

        # --------------------------------------------------------------------------------------------------------------
        [pr_.start() for pr_ in p_list]
        [pr_.join() for pr_ in p_list]  # finished at the same time
        # End ----------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main_process = Body()
    main_process.start()