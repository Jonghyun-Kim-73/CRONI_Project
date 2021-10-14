class CoolingRATE:
    def __init__(self):
        self.rate = - 50 / (60 * 60 * 5)     # 시간당 55도 감소

        self.saved = False

        self.saved_temp = 0
        self.saved_time = 0

    def save_info(self, temp, time):
        self.saved_temp = float(temp)
        self.saved_time = int(time)

    def reset_info(self):
        self.saved_temp = 0
        self.saved_time = 0

    def get_temp(self, cur_time):
        if self.saved_time != 0:
            return self.rate * (cur_time - self.saved_time) + self.saved_temp
        else:
            return 0