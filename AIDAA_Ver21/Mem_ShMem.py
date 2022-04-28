from AIDAA_Ver21.DB_AlarmDB import AlarmDB
from collections import deque
from datetime import timedelta


class ShMem:
    def __init__(self):
        self.mem = self.make_cns_mem(max_len=10)
        self.AlarmDB: AlarmDB = AlarmDB(self)
        self.add_val_to_list()

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

    def update_alarmdb(self):
        self.AlarmDB.update_alarmdb_from_ShMem()

    def add_val_to_list(self):
        [self.mem[para]['List'].append(self.mem[para]['Val']) for para in self.mem.keys()]

    def change_para_val(self, para, val):
        self.mem[para]['Val'] = val

    def get_para_val(self, para):
        return self.mem[para]['Val']

    def get_para_list(self, para):
        return self.mem[para]['List']

    def get_mem(self):
        return self.mem

    def get_alarmdb(self):
        return self.AlarmDB.alarmdb

    def check_para_name(self, para):
        return True if para in self.mem.keys() else False

    def check_para_type(self, para):
        return self.mem[para]['Sig']


class InterfaceMem:
    def __init__(self, Shmem, top_widget):
        self.ShMem: ShMem = Shmem
        self.widget_ids = {}
        # Top_widget 정보 등록
        self.add_widget_id(top_widget)
        # Current system
        self.system_switch = {'Main': 1, 'IFAP': 0, 'AIDAA': 0, 'EGIS': 0}
        self.system_state_switch = {'Normal': 1, 'Pre-abnormal': 0, 'Abnormal': 0, 'Emergency': 0}

    # Widget 링크 용 ----------------------------------------------------------------------------------------------------
    def add_widget_id(self, widget, widget_name=''):
        self.widget_ids[type(widget).__name__ if widget_name == '' else widget_name] = widget

    def show_widget_ids(self):
        return self.widget_ids

    def change_current_system_name(self, system_name):
        for name in self.system_switch.keys():
            self.system_switch[name] = 1 if system_name == name else 0
        self.widget_ids['MainTab'].change_system_page(system_name)

    def get_time(self):
        return str(timedelta(seconds=self.ShMem.get_para_val('KCNTOMS')/5))

    def get_current_system_name(self):
        return list(self.system_switch.keys())[list(self.system_switch.values()).index(1)]