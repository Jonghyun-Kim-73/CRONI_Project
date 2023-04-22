import pandas as pd
import numpy as np
class monitoring6:
    def __init__(self, ShMem):
        self.ShMem = ShMem
        self.df = np.array(pd.read_excel('EGIS_Level_Infromation_DB.xlsx'))
        self.npp_variable = self.df[:, 0]
        self.npp_state = self.ShMem.get_paras_val(self.npp_variable)
       
        self.npp_state[0] = self.npp_state[0] / 1e5
        self.npp_state[1] = self.npp_state[1] / 1e5
        self.npp_state[2] = self.npp_state[2] / 1e5
        self.npp_state[3] = self.npp_state[3] / 1e5
        
        # self.npp_state[0:4] = self.npp_state[0:4]/1e5
        # print(self.npp_state[0])
        # print(self.npp_variable[0])
        self.pumpTaskNum = 0
        self.valTaskNum = 0
        self.HPSItaskNum = 0
        self.LPSItaskNum = 0
        self.RWSTtaskNum = 0
        # result = 각 함수별 상태, taskNum = 각 함수별 직무 수
        self.sigResult, self.sigTaskNum = self.signal()

        self.pumpResult = np.zeros(6)
        self.valResult = np.zeros(6)
        self.HPSIresult = np.zeros(6)
        self.LPSIresult = np.zeros(6)
        self.RWSTresult = np.zeros(6)

        if self.sigResult[0] == 1: #SI가 켜져야하는 상황

            self.pumpResult, self.pumpTaskNum = self.pump()

            self.valResult, self.valTaskNum = self.valve_alignment()
            self.HPSIresult, self.HPSItaskNum, self.LPSIresult, self.LPSItaskNum = self.flow_rate()
            self.RWSTresult, self.RWSTtaskNum = self.RWST_level()

            # print("SIG: ", np.shape(self.sigResult))
            # print("PUM: ", np.shape(self.pumpResult))
            # print("VAL: ", np.shape(self.valResult))
            # print("HPS: ", np.shape(self.HPSIresult))
            # print("LPS: ", np.shape(self.LPSIresult))

            self.totalTaskNum = self.sigTaskNum + self.pumpTaskNum + self.valTaskNum + self.HPSItaskNum + self.LPSItaskNum + self.RWSTtaskNum
            # print("total#: ", self.totalTaskNum)
        elif self.sigResult[0] == 0: #SI가 불필요한 상황
            self.totalTaskNum = 0

    def signal(self):
        result = np.zeros(6)
        result[1] = self.npp_state[5]
        if self.npp_state[0] < 126.59:  # PPRZ 기준 kg/cm2
            state1 = 1
            result[2] = 1
        else:
            state1 = 0

        if self.npp_state[1] > 0.3515:  # 격납건물 압력 kg/cm2
            state2 = 1
            result[3] = 1
        else:
            state2 = 0

        if self.npp_state[2] < 41.1 or self.npp_state[3] < 41.1 or self.npp_state[4] < 41.1: #MSLP 기준
            state3 = 1
            result[4] = 1
        else:
            state3 = 0
        # print(state1, state2, state3)
        # result = [SI 필요여부, SI 발생여부, state1, state2, state3]
        # taskNum = sig 발생유무이므로 1 or 0
        if state1 + state2 + state3 > 0:
            result[0] = 1
            if self.npp_state[5] == 0:
                taskNum = 1

                # print("SIAS is not activated. Please check SI")
                #
                # if state1 == 1:

                #     print("SI required due to PRZ pressure")
                #
                # if state2 == 1:
                #     print("SI required due to CTMT Pressure")
                #
                # if state3 == 1:
                #     print("SI required due to MSL Pressure")

            else:
                taskNum = 0
        else:
            taskNum = 0
            result[0] = 0

        return result, taskNum

    def pump(self):
        # result =
        chp_state = self.npp_state[6] + self.npp_state[7] + self.npp_state[8]
        taskNum = 0
        result = np.zeros(6)
        if chp_state == 0:
            #print("All CHP is turned off.")
            taskNum += 1
            result[0] = 4
        elif chp_state == 1:
            if self.npp_state[6] == 1:
                #print("CHP2&3 is turned off.")
                result[0] = 3
                taskNum += 1
            elif self.npp_state[7] == 1:
                #print("CHP1&3 is turned off.")
                result[0] = 2
                taskNum += 1
            elif self.npp_state[8] == 1:
                #print("CHP1&2 is turned off.")
                result[0] = 1
                taskNum += 1
        else:
            result[0] = 0

        rhrp_state = self.npp_state[9]

        if rhrp_state == 0:
            #print("RHRP is turned off")
            taskNum += 1
            result[1] = 1
        else:
            result[1] = 0

        return result,taskNum

    def RWST_level(self):
        self.RWSTlevel = self.ShMem.get_para_val('ZRWST')
        taskNum = 0
        result = np.zeros(6)
        if self.RWSTlevel < 40:
            taskNum += 1
            result[0] = 1

        return result, taskNum

    def valve_alignment(self):
        self.valve_value = self.df[:,6]
        taskNum = 0
        result = np.zeros(6)
        for i in range(10,16):
            # print("i is:", i)
            # print(self.npp_state[i])
            # print(self.valve_value[i])
            if self.npp_state[i] != self.valve_value[i]:
                #print(self.df[i,1], "has problem.")
                taskNum += 1
                result[i-10] = 1
                # if self.valve_value[i] == 1:
                #     print(self.df[i,1], "is need to be opened.")
                # else:
                #     print(self.df[i,1], "is need to be closed.")

        return result, taskNum

    def flow_rate(self):
        HPSIresult, HPSItaskNum = self.compare_HPSI()
        LPSIresult, LPSItaskNum = self.compare_LPSI()

        return HPSIresult, HPSItaskNum, LPSIresult, LPSItaskNum

    def compare_HPSI(self):
        result = np.zeros(6)
        taskNum = 0
        if self.npp_state[0] > 120:
            result[0] = 0
        elif self.npp_state[0] <= 120 and self.npp_state[0] >= 20:
            if self.npp_state[16] < 60:
                hpsi_goal = self.HPSI_flowrate(self.npp_state[0])
                if self.npp_state[16] < hpsi_goal:
                    gap = hpsi_goal - self.npp_state[16]
                    #print("HPSI flow rate is lower than goal value")
                    #print("HPSI flow rate is required to increase", gap, "kg/sec")
                    result[0], result[1] = 1, gap
                    taskNum = 1
                else: result[0] = 0
            else: result[0] = 0

        elif self.npp_state[0] < 20 and self.npp_state[0] >= 0:
            if self.npp_state[16] < 60:
                hpsi_goal = 60
                if self.npp_state[16] < hpsi_goal:
                    gap = hpsi_goal - self.npp_state[16]
                    #print("HPSI flow rate is lower than goal value")
                    #print("HPSI flow rate is required to increase", gap, "kg/sec")
                    result[0], result[1] = 1, gap
                    taskNum = 1
                else:
                    result[0] = 0
            else:
                result[0] = 0
        return result, taskNum

    def compare_LPSI(self):
        result = np.zeros(6)
        taskNum = 0
        if self.npp_state[0] > 40:
            result[0] = 0
        elif self.npp_state[0] <= 40:
            lpsi_goal = self.LPSI_flowrate(self.npp_state[0])
            if self.npp_state[28] < lpsi_goal:
                gap = lpsi_goal - self.npp_state[28]
                #print("LPSI flow rate is lower than goal value")
                #print("LPSI flow rate is required to increase", gap, "kg/sec")
                result[0], result[1] = 1, gap
                taskNum = 1
            else: result[0] = 0
        return result, taskNum

    def HPSI_flowrate(self, x1):

        # HV22 flow rate const

        a1 = 63.57
        b1 = 0.01502
        c1 = 1.097
        a2 = 15.02
        b2 = 0.04426
        c2 = 0.9848
        a3 = 15.73
        b3 = 0.06519
        c3 = 2.71
        a4 = 1.337
        b4 = 0.1975
        c4 = -4.553
        a5 = 3.954
        b5 = 0.1296
        c5 = 2.467

        # HV22 flow rate function

        y1 = a1 * np.sin(b1 * x1 + c1) + a2 * np.sin(b2 * x1 + c2) + a3 * np.sin(b3 * x1 + c3) + a4 * np.sin(
            b4 * x1 + c4) + a5 * np.sin(b5 * x1 + c5)-1

        return y1

    def LPSI_flowrate(self, x1):

        # WRHREC ECCS flow rate const

        p1 = -1.025
        p2 = 231.7

        # WRHREC ECCS flow rate function

        y2 = p1 * x1 + p2

        return y2



    # PPRZN = npp_state[0]
    # PCTMT = npp_state[1]
    # PSG1 = npp_state[2]
    # PSG2 = npp_state[3]
    # PSG3 = npp_state[4]
    # SI_SIG = npp_state[5]
    # CHP1 = npp_state[6]
    # CHP2 = npp_state[7]
    # CHP3 = npp_state[8]
    # KRHRP = npp_state[9]
    # PO_HV39 = npp_state[10]
    # PO_LV615 = npp_state[11]
    # PO_HV22 = npp_state[12]
    # PO_LV616 = npp_state[13]
    # PO_LV603 = npp_state[14]
    # PO_HV8 = npp_state[15]
    # WHV22 = npp_state[16]
    # WSISC1 = npp_state[17]
    # WSISC2 = npp_state[18]
    # WSISC3 = npp_state[19]
    # WSISH1 = npp_state[20]
    # WSISH2 = npp_state[21]
    # WLV615 = npp_state[22]
    # WRHRCL1 = npp_state[23]
    # WRHRCL2 = npp_state[24]
    # WRHRCL3 = npp_state[25]
    # WRHRWST = npp_state[26]
    # WRHRSMP = npp_state[27]
    # WRHREC = npp_state[28]

    def result(self):
        # 200420 새로 추가

        self.sigResult1 = self.sigResult.reshape(1, 6)
        self.pumpResult1 = self.pumpResult.reshape(1, 6)
        self.valResult1 = self.valResult.reshape(1, 6)
        self.HPSIresult1 = self.HPSIresult.reshape(1, 6)
        self.LPSIresult1 = self.LPSIresult.reshape(1, 6)
        self.RWSTresult1 = self.RWSTresult.reshape(1, 6)
        self.result_num = np.zeros((5, 6))
        self.result_num = np.vstack(
            (self.sigResult1, self.pumpResult1, self.valResult1, self.HPSIresult1, self.LPSIresult1, self.RWSTresult1))
        # print(self.totalResult)

        self.textresult = []
        if self.totalTaskNum == 0:
            self.textresult.append(['No tasks required','N/A','N/A'])
        else:
            if self.result_num[0, 0] == 1 and self.result_num[0, 1] == 0:
                self.textresult.append(['SIAS Manual Activation Required', 'SIAS', 'SIGNAL'])

            if self.result_num[1, 0] != 0:
                if self.result_num[1, 0] == 1 or 2 or 3:
                    self.textresult.append(['At least 1 CHP required to operate', 'HPSI', 'PUMP'])
                if self.result_num[1, 0] == 4:
                    self.textresult.append(['At least 2 CHP required to operate', 'HPSI', 'PUMP'])

            if self.result_num[1, 1] == 1:
                self.textresult.append(['RHRP required to operate', 'LPSI', 'PUMP'])

            if self.result_num[2, 0] == 1:
                self.textresult.append(['ACCUM VALVE(HV39) required to open', 'ACCUM', 'VALVE'])
            if self.result_num[2, 1] == 1:
                self.textresult.append(['RWST ISO VALVE(LV615) required to open', 'HPSI', 'VALVE'])
            if self.result_num[2, 2] == 1:
                self.textresult.append(['SI ISO VALVE(HV22) required to open', 'HPSI', 'VALVE'])
            if self.result_num[2, 3] == 1:
                self.textresult.append(['VCT ISO VALVE(LV616) required to close', 'CVCS', 'VALVE'])
            if self.result_num[2, 4] == 1:
                self.textresult.append(['RHR HX TO RCS ISO VALVE(LV603) required to close', 'LPSI', 'VALVE'])
            if self.result_num[2, 5] == 1:
                self.textresult.append(['RWST TO RHRP ISO VALVE(HV8) required to open', 'LPSI', 'VALVE'])

            if self.result_num[3, 0] == 1:
                self.textresult.append(
                    ['HPSI flow rate required to increase until %4.2f kg/sec' % self.result_num[3, 1], 'HPSI', 'FLOW'])
            if self.result_num[4, 0] == 1:
                self.textresult.append(
                    ['LPSI flow rate required to increase until %4.2f kg/sec' % self.result_num[4, 1], 'LPSI', 'FLOW'])
            if self.result_num[5, 0] == 1:
                self.textresult.append(
                    ['RWST level is too low. Setpoint: 37.4%%, RWST level: %2.2f%%' % self.RWSTlevel, 'HPSI', 'TANK'])

        self.totalResult = np.array(self.textresult)

        return self.totalResult

    def getRPScolor(self):
        RPScolor = []
        RPSsig = self.ShMem.get_para_val('KLAMPO9')
        if RPSsig== 1:
            RPScolor = "green"
        return RPScolor

    def getSIAScolor(self):
        SIAScolor = []
        
        SIASreq = self.sigResult[0]
        SIASsig = self.ShMem.get_para_val('KSAFEI')

        if SIASreq == 1 and SIASsig == 1:
            SIAScolor = "green"
        elif SIASreq == 1 and SIASsig == 0:
            SIAScolor = "red"

        return SIAScolor

    def getMSIScolor(self):
        MSIScolor = []

        MSISsig = self.ShMem.get_para_val('KLAMPO3')

        if MSISsig == 1:
            MSIScolor = "green"

        return MSIScolor

    def getAFAScolor(self):
        AFAScolor = []

        AFASsig = self.ShMem.get_para_val('KFWISO')

        if AFASsig == 1:
            AFAScolor = "green"

        return AFAScolor

    def getCIAScolor(self):
        CIAScolor = []

        CIASAsig = self.ShMem.get_para_val('KCISOA')
        CIASBsig = self.ShMem.get_para_val('KCISOB')

        if CIASAsig == 1 or CIASBsig == 1:
            CIAScolor = "green"

        return CIAScolor

    def getCSAScolor(self):
        CSAScolor = []

        CSASsig = self.ShMem.get_para_val('KCSAS')

        if CSASsig == 1:
            CSAScolor = "green"

        return CSAScolor

class test():
    def __init__(self):
        print('test')

if  __name__ == '__main__':
    a = monitoring6()
    b = test()
    # a.pump()
    # a.valve_alignment()
    # a.flow_rate()

