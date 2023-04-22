import numpy as np

class mfm():
    def __init__(self, B):
        self.B = B

        self.HPSI = np.zeros(1)
        self.LPSI = np.zeros(1)
        self.SIT = np.zeros(1)
        self.PRZ = np.zeros(1)
        self.RCSinventory = np.zeros(1)
        self.PrimaryHT = np.zeros(1)
        self.CoreCooling = np.zeros(1)

    def monitoring(self):
        # self.HPSI, self.LPSI, self.RCSinventory, self.PrimaryHT, self.CoreCooling = [], [], [], [] ,[]
        if self.B.pumpResult[0] >= 1 and self.B.pumpResult[0] < 4:
            self.HPSI = -1
        elif self.B.pumpResult[0] == 4:
            self.HPSI = -2

        if self.B.RWSTresult[0] == 1:
            self.HPSI = -1

        if self.B.pumpResult[1] == 1:
            self.LPSI = -1

        self.RCSinventory = min(self.HPSI, self.LPSI, self.SIT)
        self.PrimaryHT = self.RCSinventory
        self.CoreCooling = self.PrimaryHT

    def mfmcolor(self):

        self.HPSIcolor = blockcolor(self.HPSI)
        self.LPSIcolor = blockcolor(self.LPSI)
        self.RCSinventorycolor = blockcolor(self.RCSinventory)
        self.PrimaryHTcolor = blockcolor(self.PrimaryHT)
        self.CoreCoolingcolor = blockcolor(self.CoreCooling)

        return self.HPSIcolor, self.LPSIcolor, self.RCSinventorycolor, self.PrimaryHTcolor, self.CoreCoolingcolor

def blockcolor(data):
    if data == -2:
        color = "red"
    elif data == -1:
        color = "yellow"
    else: color = "rgp(239, 239, 239)"
    return color