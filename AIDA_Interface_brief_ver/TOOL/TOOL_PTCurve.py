import math


class PTCureve:
    """
        0 : 만족, 1: 불만족
        PTCureve().Check(Temp=110, Pres=0)
    """
    def __init__(self):
        self.UpTemp = [0, 37.000000, 65.500000, 93.000000, 104.400000, 110.000000,
                       115.500000, 121.000000, 148.800000, 176.500000, 186.500000, 350.0]
        self.UpPres = [29.5, 29.500000, 30.500000, 36.500000, 42.000000, 45.600000,
                       49.000000, 54.200000, 105.000000, 176.000000, 200.000000, 592]
        self.BotTemp = [0, 37.000000, 149.000000, 159.000000, 169.000000, 179.000000,
                        204.000000, 232.000000, 260.000000, 287.700000, 350.000000]
        self.BotPres = [17.0, 17.000000, 17.000000, 17.300000, 17.600000, 20.000000,
                        31.600000, 44.300000, 58.000000, 71.000000, 100.000000]
        self.UpLineFunc = []
        self.BotLineFunc = []
        # 직교 함수를 그려 현재 포인트에서 PT 커브까지 거리를 계산하기 위해서 사용
        self.UpLineOrtFunc = []
        self.BotLineOrtFunc = []

        self._make_bound_UpLine()
        self._make_bound_BotLine()

    def _make_bound_func(self, Temp, Pres):
        """
        2점에 대한 1차원 함수 반환
        :param Temp: [a1, a2] == x
        :param Pres: [b1, b2] == y
        :return: func
        """
        # y1 = ax1 + b
        # y2 = ax2 + b
        # a = (y1-y2)/(x1-x2)
        # b = y1 - {(y1-y2)/(x1-x2) * x1}
        get_a = (Pres[0] - Pres[1]) / (Temp[0] - Temp[1])
        get_b = Pres[0] - get_a * Temp[0]
        return lambda temp: get_a * temp + get_b

    def _make_bound_orthogonal_func(self, Temp, Pres):
        """
        2점에 대한 ax+by+c = 0
        :param Temp: [a1, a2] == x
        :param Pres: [b1, b2] == y
        :return: [a, b, c] List
        """
        # y1 = ax1 + b
        # y2 = ax2 + b
        # a = (y1-y2)/(x1-x2)
        # b = y1 - {(y1-y2)/(x1-x2) * x1}
        get_a = (Pres[0] - Pres[1]) / (Temp[0] - Temp[1])   # slop
        get_b = Pres[0] - get_a * Temp[0]
        # y = get_a * x + get_b ==> ax + by + c = 0
        a = - get_a
        b = 1
        c = - get_b
        return [a, b, c]

    def _make_bound_UpLine(self):
        for i in range(len(self.UpTemp) - 1):
            self.UpLineFunc.append(self._make_bound_func(Temp=self.UpTemp[i:i+2], Pres=self.UpPres[i:i+2]))
            self.UpLineOrtFunc.append(self._make_bound_orthogonal_func(Temp=self.UpTemp[i:i+2], Pres=self.UpPres[i:i+2]))

    def _make_bound_BotLine(self):
        for i in range(len(self.BotTemp) - 1):
            self.BotLineFunc.append(self._make_bound_func(Temp=self.BotTemp[i:i+2], Pres=self.BotPres[i:i+2]))
            self.BotLineOrtFunc.append(self._make_bound_orthogonal_func(Temp=self.BotTemp[i:i+2], Pres=self.BotPres[i:i+2]))

    def _call_fun(self, Temp):
        UpF, BotF = 0, 0
        for i in range(len(self.UpTemp) - 1):
            if self.UpTemp[i] <= Temp < self.UpTemp[i + 1]:
                UpF = self.UpLineFunc[i]
        for i in range(len(self.BotTemp) - 1):
            if self.BotTemp[i] <= Temp < self.BotTemp[i + 1]:
                BotF = self.BotLineFunc[i]
        return UpF, BotF

    def _call_ort_fun(self, Temp):
        UpOrtF, BotOrtF = 0, 0
        for i in range(len(self.UpTemp) - 1):
            if self.UpTemp[i] <= Temp < self.UpTemp[i + 1]:
                UpOrtF = self.UpLineOrtFunc[i]
        for i in range(len(self.BotTemp) - 1):
            if self.BotTemp[i] <= Temp < self.BotTemp[i + 1]:
                BotOrtF = self.BotLineOrtFunc[i]
        return UpOrtF, BotOrtF

    def _get_pres(self, Temp):
        """
        온도 받아서 위아래 Pres 조건 반환
        :param Temp: [0~..]
        :return: [Up_pres, Bot_pres]
        """
        UpF, BotF = self._call_fun(Temp=Temp)
        Up_pres, Bot_pres = UpF(Temp), BotF(Temp)
        return Up_pres, Bot_pres

    def _check_up_or_under(self, fun, Temp, Pres):
        Get_Pres = fun(Temp)
        if Get_Pres > Pres:
            return 0    # 입력된 Pres가 그래프보다 아래쪽에 존재
        elif Get_Pres == Pres:
            return 1    # 입력된 Pres가 그래프에 존재
        else:
            return 2    # 입력된 Pres가 그래프보다 위쪽에 존재

    def _check_in_or_out(self, Temp, Pres):
        UpF, BotF = self._call_fun(Temp=Temp)
        Upcond = self._check_up_or_under(UpF, Temp, Pres)
        Botcond = self._check_up_or_under(BotF, Temp, Pres)

        Reason = 0
        if Upcond == 2: Reason = 1      # Upcond 벗어난 경우
        if Botcond == 0: Reason = 2     # Botcond 벗어난 경우

        if Upcond == 2 or Botcond == 0:
            return [1, Reason]    # PT커브 초과
        else:
            return [0, Reason]    # PT커브에서 운전 중

    def _check_distance(self, Temp, Pres):
        """
        현재 온도 압력을 기준으로 Upline과 Botline과의 거리 계산
        :param Temp: 현재 온도
        :param Pres: 현재 압력
        :return: UpDis, BotDis
        """
        d = 0
        UpOrtF, BotOrtF = self._call_ort_fun(Temp=Temp)     # [a,b,c]
        # d = abs(a*x_1 + b*y_1 + c) / (math.sqrt(math.pow(a, 2) + math.pow(b, 2)))
        # x_1 = Temp
        # y_1 = Pres
        UpDis = abs(UpOrtF[0] * Temp + UpOrtF[1] * Pres + UpOrtF[2]) / \
                (math.sqrt(math.pow(UpOrtF[0], 2) + math.pow(UpOrtF[1], 2)))
        BotDis = abs(BotOrtF[0] * Temp + BotOrtF[1] * Pres + BotOrtF[2]) / \
                 (math.sqrt(math.pow(BotOrtF[0], 2) + math.pow(BotOrtF[1], 2)))
        return UpDis, BotDis

    def Check(self, Temp, Pres):
        """
        PT curve에 운전 중인지 확인
        :param Temp: 현재 온도
        :param Pres: 현재 압력
        :return: 0 만족, 1 불만족
        """
        return self._check_in_or_out(Temp, Pres)[0]

    def Check_Dis(self, Temp, Pres):
        """
        현재 온도 압력을 기준으로 PT 커브에서 벗어난 경우 벗어난 거리 제공
        :param Temp: 현재 온도
        :param Pres: 현재 압력
        :return: 벗어난 거리
        """
        Satisfiy, Reason =self._check_in_or_out(Temp, Pres)
        Updis, Botdis = self._check_distance(Temp, Pres)

        if Satisfiy == 0:
            return 0
        else:
            # 가장 짧은 거리
            return Updis if Updis < Botdis else Botdis
