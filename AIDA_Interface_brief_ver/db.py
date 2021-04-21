from collections import deque


class db_make:
    def __init__(self):
        pass

    def make_mem_structure(self, max_len):
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


