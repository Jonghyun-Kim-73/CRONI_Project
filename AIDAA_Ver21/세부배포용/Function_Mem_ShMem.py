from datetime import timedelta
from collections import deque
import numpy as np
import pandas as pd
import socket

class ShMem:
    def __init__(self):
        self.mem = self.make_cns_mem(max_len=10)
        self.IFAPmem = self.make_IFAP_mem()

    # - Normal part -----------------------------------------------------------------------------------------------------
    def make_cns_mem(self, max_len, db_path='./db.txt', db_add_path='./db_add.txt'):
        # 초기 shared_mem의 구조를 선언한다.
        idx = 0
        shared_mem = {}
        for file_name in [db_path, db_add_path]:
            with open(file_name, 'r') as f:
                while True:
                    temp_ = f.readline().split('\t')
                    if temp_[0] == '':  # if empty space -> break
                        break
                    if temp_[0] == '#':  # Pass this value. We don't require this value.
                        pass  # These values are normally static values in SMABRES Code.
                    else:   
                        sig = 0 if temp_[1] == 'INTEGER' else 1
                        shared_mem[temp_[0]] = {'Sig': sig, 'Val': 0, 'Num': idx, 'List': deque(maxlen=max_len)}
                        idx += 1

        # 다음과정을 통하여 shared_mem 은 PID : { type. val, num }를 가진다.
        return shared_mem
    def make_IFAP_mem(self):
        mem_structure = {
            'V0'  : {'Sig': 0, 'Val': 5},   #10si  : string(10바이트), short(2바이트), value(int or float, 4바이트) = 10바이트
            'V1'  : {'Sig': 0, 'Val': 1},   # sig = 0 int , sig = 1 float
            'V2'  : {'Sig': 1, 'Val': 1.1},
        }
        return mem_structure

    def change_para_val(self, para, val):       self.mem[para]['Val'] = val

    def get_para_val(self, para):         return self.mem[para]['Val']
    def get_para_list(self, para):        return self.mem[para]['List']
    def get_mem(self):                    return self.mem
    def get_IFAP_para_val(self, para):    return self.IFAPmem[para]['Val']

    def check_para_name(self, para):      return True if para in self.mem.keys() else False
    def check_para_type(self, para):      return self.mem[para]['Sig']
    
    def update_IFAP_mem(self, mem):       self.IFAPmem = mem

class InterfaceMem:
    def __init__(self, Shmem, top_widget):
        self.ShMem: ShMem = Shmem
        self.widget_ids = {}
        # Top_widget 정보 등록
        self.add_widget_id(top_widget)
    
    # Widget 링크 용 ----------------------------------------------------------------------------------------------------
    def add_widget_id(self, widget, widget_name=''):
        """새롭게 생성된 위젯의 정보를 self.widget_ids:dict 에 저장하는 함수

        Args:
            widget (_type_): Qwidget, QPushButton를 기반한 ABC 클래스
            widget_name (str, optional): 클래스의 이름이 중복적으로 사용되는 경우 수동 할당을 위해서 존재. Defaults to '' 는 class 명을 따라감.
        """
        self.widget_ids[type(widget).__name__ if widget_name == '' else widget_name] = widget

    def show_widget_ids(self):
        return self.widget_ids