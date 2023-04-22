import numpy as np

CSF1_varlist = ['ZINST1', 'ZINST2', 'ZINST3', 'ZINST5']
CSF2_varlist = ['ZINST46', 'UHOLEGM']
CSF3_varlist = ['ZINST78', 'ZINST77', 'ZINST76', 'WFWLN1', 'WFWLN2', 'WFWLN3', 'ZINST75', 'ZINST74', 'ZINST73']
CSF4_varlist = ['UCOLEG1', 'UCOLEG2', 'UCOLEG3', 'ZINST63']
CSF5_varlist = ['ZINST26', 'ZINST17', 'ZINST22']
CSF6_varlist = ['ZINST63']

str1 = "CSF1"
str2 = "CSF2"
str3 = "CSF3"
str4 = "CSF4"
str5 = "CSF5"
str6 = "CSF6"

"""
################################### Function Definition #############################################


# def CSF_print_repeat(second):
#     SM = SharedMemory()
#     start = time.time()
#     data = SM.read(CSF4_varlist)
#     CL1T_start = data[0]
#     CL2T_start = data[1]
#     CL3T_start = data[2]
#     line = 0
#
#     while 1:
#         sleep(second)
#         del_t = time.time() - start
#
#         print(int(del_t),"seconds")
#
#         CSF1_data = SM.read(CSF1_varlist)
#         CSF2_data = SM.read(CSF2_varlist)
#         CSF3_data = SM.read(CSF3_varlist)
#         CSF4_data = SM.read(CSF4_varlist)
#         CSF5_data = SM.read(CSF5_varlist)
#         CSF6_data = SM.read(CSF6_varlist)
#
#         CLCR = cooling_rate(CSF4_data, del_t, CL1T_start, CL2T_start, CL3T_start)
#
#         CSF1 = CSF1_status(CSF1_data)
#         CSF2 = CSF2_status(CSF2_data)
#         CSF3 = CSF3_status(CSF3_data)
#         CSF4 = CSF4_status(CSF4_data, CLCR)
#         CSF5 = CSF5_status(CSF5_data)
#         CSF6 = CSF6_status(CSF6_data)
#         CSF_data = [CSF1, CSF2, CSF3, CSF4, CSF5, CSF6]
#         table_generation(line, del_t, CSF_data)
#
#         CSF_color(str1, CSF1)
#         CSF_color(str2, CSF2)
#         CSF_color(str3, CSF3)
#         CSF_color(str4, CSF4)
#         CSF_color(str5, CSF5)
#         CSF_color(str6, CSF6)
"""

class CSF_evaluation:
    def __init__(self, ShMem):
        super(CSF_evaluation,self).__init__()
        self.ShMem = ShMem

    def CSF_status(self):
        del_t = 30
        CL1T_start = self.ShMem.get_para_val('UCOLEG1')
        CL2T_start = self.ShMem.get_para_val('UCOLEG2')
        CL3T_start = self.ShMem.get_para_val('UCOLEG3')

        CSF1_data = self.ShMem.get_paras_val(CSF1_varlist)
        CSF2_data = self.ShMem.get_paras_val(CSF2_varlist)
        CSF3_data = self.ShMem.get_paras_val(CSF3_varlist)
        CSF4_data = self.ShMem.get_paras_val(CSF4_varlist)
        CSF5_data = self.ShMem.get_paras_val(CSF5_varlist)
        CSF6_data = self.ShMem.get_paras_val(CSF6_varlist)

        CLCR = cooling_rate(CSF4_data, del_t, CL1T_start, CL2T_start, CL3T_start)

        CSF1 = CSF1_status(CSF1_data)
        CSF2 = CSF2_status(CSF2_data)
        CSF3 = CSF3_status(CSF3_data)
        CSF4 = CSF4_status(CSF4_data, CLCR)
        CSF5 = CSF5_status(CSF5_data)
        CSF6 = CSF6_status(CSF6_data)
        CSF = [CSF1, CSF2, CSF3, CSF4, CSF5, CSF6]

        color = CSFcolor(CSF)

        # print("CSF score is")
        # print(CSF)

        return color

def CSFcolor(data):
    colorData = ['aaa','aaa','aaa','aaa','aaa','aaa']

    for i in range(0,6):
        colorData[i] = blockColor(data[i])
    return colorData

def blockColor(data):
    if data == 4:
        color = "green"
    elif data == 3:
        color = "yellow"
    elif data == 2:
        color = "orange"
    elif data == 1:
        color = "red"
    return color

def CSF1_status(data):
    PRNL = data[0] #Power Range Neutron Level
    IRNL = data[1] #Intermediate Range Neutron Level
    IRSR = data[3] #Intermediate Range Start-up Rate
    SRNL = data[2] #Source Range Neutron Level
    SRSR = data[3] #Source Range Start-up Rate

    if PRNL < 5:
        if IRSR <= 0:
            if IRNL <= 10e-9:
                if SRSR <= 0:
                    CSF1 = 4 #4 = Green
                else: CSF1 = 3 #3 = Yellow
            else:
                if NRSR <= -0.2:
                    CSF1 = 4
                else: CSF1 = 3
        else: CSF1 = 2 #2 = Orange
    else: CSF1 = 1 #1 = Red

    CSF1 = 4

    return CSF1

def CSF2_status(data):
    CET = data[0] #Core Exit Temperature
    ATHL = data[1] #Average Temperature in Hot Legs
    PTS = PT_status()

    if CET < 649:
        if PTS == 1:
            CSF2 = 4 # Green
        else:
            if CET < 371:
                CSF2 = 3 # Yellow
            else: CSF2 = 2 # Orange
    else: CSF2 = 1 # Red

    return CSF2

def CSF3_status(data):
    SG1NL = data[0]
    SG2NL = data[1]
    SG3NL = data[2]
    FWFR1 = data[3]
    FWFR2 = data[4]
    FWFR3 = data[5]
    SG1P  = data[6]
    SG2P  = data[7]
    SG3P  = data[8]

    FWFR_total = FWFR1 + FWFR2 + FWFR3

    if SG1NL >= 6 or SG2NL >= 6 or SG3NL >= 6 :
        if SG1P <= 88.6 and SG2P <= 88.6 and SG3P <= 88.6:
            if SG1NL <= 78 and SG2NL <= 78 and SG3NL <= 78:
                if SG1P <= 83.3 and SG2P <= 83.3 and SG3P <= 83.3:
                    if SG1NL >=6 and SG2NL >= 6 and SG3NL >= 6:
                        CSF3 = 4
                    else: CSF3 = 3
                else: CSF3 = 3
            else: CSF3 = 3
        else: CSF3 = 3
    else:
        if FWFR_total < 28: CSF3 = 1
        else: CSF3 = 3
    return CSF3

def CSF4_status(data, CLCR):
    CL1T = data[0]
    CL2T = data[1]
    CL3T = data[2]
    PRZP = data[3]
    Tavg = (CL1T+CL2T+CL3T)/3
    Add2 = 1 #addition 2 limit graph

    if CLCR == 1 :
        if Tavg >= 177 : #Tavg >= 177
            CSF4 = 4
        else:
            if PRZP < 143.5: CSF4 = 4
            else:
                if Tavg >= 106: CSF4 = 3
                else:  CSF4 = 2
    else:
        if Add2 == 1:
            if Tavg >= 106:
                if Tavg >= 136: CSF4 = 4
                else: CSF4 = 3
            else: CSF4 = 2
        else: CSF4 = 1

    return CSF4

def CSF5_status(data):
    CNTP = data[0]
    CNTSL = data[1]/5*100 # Sump Level is 5m (assumption)
    CNTR = data[2]

    if CNTP < 4.2 :
        if CNTP < 1.55:
            if CNTSL < 34.5:
                if CNTR < 10e4:
                    CSF5 = 4
                else: CSF5 = 3
            else: CSF5 = 2
        else: CSF5 = 2
    else: CSF5 = 1

    return CSF5

def CSF6_status(data):
    PWL = data[0]

    if PWL < 92:
        if PWL > 17:
            if 50 < PWL < 60: #assumption
                CSF6 = 4
            else: CSF6 = 3
        else: CSF6 = 3
    else: CSF6 = 3

    return CSF6

# def CSF_color(str, CSF):
#     C_END = "\033[0m"
#     C_BOLD = "\033[1m"
#     C_RED = "\033[31m"
#     C_GREEN = "\033[32m"
#     C_YELLOW = "\033[33m"
#     C_ORANGE = "\033[38;5;214m"
#     if CSF == 1:
#         print(C_BOLD + C_RED + str + C_END)
#     if CSF == 2:
#         print( C_BOLD + C_ORANGE + str + C_END)
#     if CSF == 3:
#         print( C_BOLD + C_YELLOW + str + C_END)
#     if CSF == 4:
#         print( C_BOLD + C_GREEN + str + C_END)

def PT_status():
    PTS = 1 #PT Curve Operation is satisfied (Assumption)
    return PTS

def cooling_rate(data, del_t, CL1T_start, CL2T_start, CL3T_start):
    CL1T = data[0]
    CL2T = data[1]
    CL3T = data[2]
    CL1CR = (CL1T_start - CL1T) / ((55.5 / 3600) * del_t)
    CL2CR = (CL2T_start - CL2T) / ((55.5 / 3600) * del_t)
    CL3CR = (CL3T_start - CL3T) / ((55.5 / 3600) * del_t)
    Cooling_rate1 = ((CL1T_start - CL1T) / del_t) * 3600
    Cooling_rate2 = ((CL2T_start - CL2T) / del_t) * 3600
    Cooling_rate3 = ((CL3T_start - CL3T) / del_t) * 3600

    # print("time:", del_t)
    # print("CL1O: ", format(CL1T_start, "16.6f"), ", CL2O: :", format(CL2T_start, "16.6f"), ", CL3O: ", format(CL3T_start, "16.6f"))
    # print("CL1O: ", format(CL1T, "16.6f"), ", CL2O: :", format(CL2T, "16.6f"), ", CL3O: ", format(CL3T, "16.6f"))
    # print("CL1: ", format(CL1CR,"26.16f"))
    # print("CL2: ", format(CL2CR,"26.16f"))

    # print("CL3L ", format(CL3CR,"26.16f"))
    if CL1CR >= 1 or CL2CR >= 1 or CL3CR >= 1:
        CLCR = 0
    else:
        CLCR = 1

    #print("Cooling Rate 1                     :", format(Cooling_rate1, "26.16f"))
    #print("Cooling Rate 2                     :", format(Cooling_rate2, "26.16f"))
    #print("Cooling Rate 3                     :", format(Cooling_rate3, "26.16f"))
    #print("Cooling Rate Success               :", format(CLCR, "26.16f"))

    return CLCR

# def table_generation(line, del_t, CSF_data):
#     a = line
#     b = del_t
#     c = CSF_data
#     data_set = [a,b,c]
#     return data_set

################################################## MAIN ######################################################
