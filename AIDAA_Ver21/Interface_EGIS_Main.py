from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Function_EGIS_CSF_checker import CSF_evaluation
from AIDAA_Ver21.Function_EGIS_Monitoring_SIAS import monitoring6
from AIDAA_Ver21.Function_EGIS_MFM import mfm

EGISui = "UI_EGISwidget7.ui"
SIASui = "UI_SIASdialog.ui"
HPSIui = "UI_HPSIdialog.ui"
DAui = "UI_DA.ui"
class EGISmain(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        uic.loadUi(EGISui, self)
        self.initUI()
        self.SIASpushButton.clicked.connect(self.SIASclicked)
        self.HPSIpushButton.clicked.connect(self.HPSIclicked)
        self.DApushButton.clicked.connect(self.DAclicked)
        #EGIS 타이머
        self.i = 0
        self.old_time = self.inmem.ShMem.get_para_val('KCNTOMS')
        self.startTimer(600)
        #GUI 사전에 등록
        self.SIASwindow = SIASwindow(self)
        self.HPSIwindow = HPSIwindow(self)
        self.DAwindow = DAwindow(self)
        
    def initUI(self):
        self.setGeometry(0,0,970,1000)
        self.setWindowTitle("Emergency Guidance Intelligent System")
        self.DApushButton.setStyleSheet('background:red; font:bold 20px;')
        self.DApushButton.setText('SPTA tasks are \nnot finished...')
        # self.label_2.setPixmap(QPixmap("./resources/XAI_interface.png"))  # image path
        self.k = 0
        
    def timerEvent(self, a0: 'QTimerEvent') -> None:
        if self.old_time != self.inmem.ShMem.get_para_val('KCNTOMS'): self.getCSFcolor() # Call Function
        return super().timerEvent(a0)

    #CSF Procedure Status Checker
    def getCSFcolor(self):
        self.i += 1
        A = CSF_evaluation(self.inmem.ShMem)
        B = monitoring6(self.inmem.ShMem)
        C = mfm(B)
        self.time = self.i*0.5
        # print("\n\ntime: %d" %self.time)

        # CSF 색상 상태 받기
        # self.CSF1pushButton.setStyleSheet('background:%s' %A.CSF_status()[0])
        # self.CSF2pushButton.setStyleSheet('background:%s' %A.CSF_status()[1])
        # self.CSF3pushButton.setStyleSheet('background:%s' %A.CSF_status()[2])
        # self.CSF4pushButton.setStyleSheet('background:%s' %A.CSF_status()[3])
        # self.CSF5pushButton.setStyleSheet('background:%s' %A.CSF_status()[4])
        # self.CSF6pushButton.setStyleSheet('background:%s' %A.CSF_status()[5])

        [self.CSFstatus(i, A) for i in [1, 2, 3, 4, 5, 6]]
        self.CSFstatus_blink(6, A, B)

        # if self.i%2 == 1 and B.totalTaskNum != 0:
        #     self.CSF6pushButton.setStyleSheet('background:%s; border-color: red; border-style: outset; border-width: 3px;' %A.CSF_status()[5])

        self.RPSpushButton.setStyleSheet('background:%s' %B.getRPScolor())
        self.SIASpushButton.setStyleSheet('background:%s' %B.getSIAScolor())
        self.MSISpushButton.setStyleSheet('background:%s' %B.getMSIScolor())
        self.AFASpushButton.setStyleSheet('background:%s' %B.getAFAScolor())
        self.CIASpushButton.setStyleSheet('background:%s' %B.getCIAScolor())
        self.CSASpushButton.setStyleSheet('background:%s' %B.getCSAScolor())

        # MLD 정보 받아오기
        C.monitoring()
        style = 'border-style: outset; border-width: 4px; border-radius: 20px; border-color: black; font:bold 20px;'

        self.HPSIpushButton.setStyleSheet('background:%s' %C.mfmcolor()[0])
        self.LPSIpushButton.setStyleSheet('background:%s' %C.mfmcolor()[1])
        self.RCSpushButton.setStyleSheet('background:%s; %s' % (C.mfmcolor()[2], style))
        self.PSHTpushButton.setStyleSheet('background:%s' % C.mfmcolor()[3])
        self.CCpushButton.setStyleSheet('background-color:%s; %s' %(C.mfmcolor()[4], style))

        # Button Blinking
        if self.i%2 == 1 and B.pumpTaskNum != 0:
            self.HPSIpushButton.setStyleSheet(
                'background:%s; border-color: red; border-style: outset; border-width: 3px;' %C.mfmcolor()[0])

        if self.i%2 == 1 and B.getSIAScolor() == "red":
            self.SIASpushButton.setStyleSheet(
                'background:%s; border-color: red; border-style: outset; border-width: 3px;' % B.getSIAScolor())

        # Total Task List
        self.tableWidget.setRowCount(len(B.result()[:, 0]))
        self.tableWidget.setColumnCount(4)

        for i in range(len(B.result()[:, 0])):

            self.tableWidget.setCellWidget(i, 0, QCheckBox())

            for j in range(3):
                k = j + 1
                self.tableWidget.setItem(i, k, QTableWidgetItem("%s" % B.result()[i, j]))

        self.tableWidget.setRowHeight(0,40)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setFont(QFont('Cantarell',14,QFont.Normal, italic=False))

        # Diagnosis Block
        if B.totalTaskNum == 0:
            self.k += 1
            # print(self.k)

        if B.totalTaskNum == 0 and self.k >= 30:
            self.DApushButton.setStyleSheet('background:green; font:bold 20px;')
            self.DApushButton.setText('Transfer to \nLOCA(E-01)')
            #
            # self.label_2.setPixmap(QPixmap("./resources/ESDE_1_IN_0280.png"))  # LDP Change
            # self.XAIpushButton_1.setText('CTMT P')
            # self.XAIpushButton_2.setText('SG#3 L')
            # self.XAIpushButton_3.setText('CTMT T')
            # self.XAIpushButton_4.setText('PRZ P')
            # self.XAIpushButton_5.setText('SG#1 L')
            # self.XAIpushButton_6.setText('HL#2 T')
            # self.XAIpushButton_7.setText('CL#2 T')
            # self.XAIpushButton_8.setText('SL#1 F')
            # self.XAIpushButton_9.setText('CL#2 T')
            # self.XAIpushButton_10.setText('SG#1 WL')

        if self.k >= 3:
            self.TTpushButton.setStyleSheet('background: green')
   
    def CSFstatus(self, n, A):
        if A.CSF_status()[n-1] == "red":
            exec("self.CSF%dpushButton_2.setStyleSheet('background: %s')" %(n, A.CSF_status()[n-1]))
            exec("self.CSF%dpushButton_2.setText('Level 4')" %n)


        elif A.CSF_status()[n-1] == "orange":
            exec("self.CSF%dpushButton_2.setStyleSheet('background: %s')" %(n, A.CSF_status()[n-1]))
            exec("self.CSF%dpushButton_2.setText('Level 3')" % n)

        elif A.CSF_status()[n-1] == "yellow":
            exec("self.CSF%dpushButton_2.setStyleSheet('background: %s')" %(n, A.CSF_status()[n-1]))
            exec("self.CSF%dpushButton_2.setText('Level 2')" % n)


        elif A.CSF_status()[n - 1] == "green":
            exec("self.CSF%dpushButton_2.setStyleSheet('background: %s')" %(n, A.CSF_status()[n-1]))
            exec("self.CSF%dpushButton_2.setText('Level 1')" % n)
            
    def CSFstatus_blink(self, n, A, B):
        if self.i%2 == 1 and B.totalTaskNum != 0:
            if A.CSF_status()[n - 1] == "red":
                exec("self.CSF%dpushButton_2.setStyleSheet('background: %s; border-color: red; border-style: outset; border-width: 3px;')" % (n, A.CSF_status()[n - 1]))

            elif A.CSF_status()[n - 1] == "orange":
                exec("self.CSF%dpushButton_2.setStyleSheet('background: %s; border-color: red; border-style: outset; border-width: 3px;')" % (n, A.CSF_status()[n - 1]))

            elif A.CSF_status()[n - 1] == "yellow":
                exec("self.CSF%dpushButton_2.setStyleSheet('background: %s; border-color: red; border-style: outset; border-width: 3px;')" % (n, A.CSF_status()[n - 1]))

            elif A.CSF_status()[n - 1] == "green":
                exec("self.CSF%dpushButton_2.setStyleSheet('background: %s; border-color: red; border-style: outset; border-width: 3px;')" % (n, A.CSF_status()[n - 1]))

    # Click Part    
    def SIASclicked(self): self.SIASwindow.show()
    def HPSIclicked(self): self.HPSIwindow.show()
    def DAclicked(self): self.DAwindow.show()
class SIASwindow(ABCDialog):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.initUI()
        self.i = 0
        self.old_time = self.inmem.ShMem.get_para_val('KCNTOMS')
        self.startTimer(600)

    def initUI(self):
        uic.loadUi(SIASui, self)
        self.setGeometry(280,750,720,250)
        self.setWindowTitle("SIAS")
        self.SIASpushButton3.clicked.connect(self.SIASbtnclicked)

        # self.PUMPtab.layout = QVBoxLayout(self)
        #
        # self.tblock = QPushButton(self)
        # self.tblock.setText('love')

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        if self.old_time != self.inmem.ShMem.get_para_val('KCNTOMS'): self.getSIASinfo()
        return super().timerEvent(a0)

    def getSIASinfo(self):
        self.i += 1
        B = monitoring6(self.inmem.ShMem)

        self.PRZP = self.inmem.ShMem.get_para_val('PPRZN')/1e5
        self.PCTMT = self.inmem.ShMem.get_para_val('PCTMT')/1e5
        self.MSLP = min(self.inmem.ShMem.get_para_val('PSG1'), 
                        self.inmem.ShMem.get_para_val('PSG2'), 
                        self.inmem.ShMem.get_para_val('PSG3'))/1e5

        self.PRZ_Pbar.setValue(self.PRZP*10)
        self.CTMT_Pbar.setValue(self.PCTMT*10)
        self.MSL_Pbar.setValue(self.MSLP*10)

        self.lcdNumber1.display('%.1f' %self.PRZP)
        self.lcdNumber2.display('%.1f' %self.PCTMT)
        self.lcdNumber3.display('%.1f' %self.MSLP)

        self.SIASpushButton3.setStyleSheet('background:%s' % B.getSIAScolor())
        if B.getSIAScolor() == "red" and self.i%2 == 1:
            self.SIASpushButton3.setStyleSheet(
                'background:%s; border-color: red; border-style: outset; border-width: 3px;' % B.getSIAScolor())

    def SIASbtnclicked(self):
        self.inmem.ShMem.send_control_signal(['KMANSI'], [1]) # 동작 확인 필요함.
        print('Send')
        # integer_set('KMANSI', 1)
class HPSIwindow(ABCDialog):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.initUI()
        self.i = 0
        self.old_time = self.inmem.ShMem.get_para_val('KCNTOMS')
        self.startTimer(600)

    def initUI(self):
        uic.loadUi(HPSIui, self)
        self.setGeometry(400,500,600,500)
        self.setWindowTitle("HPSI")

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        if self.old_time != self.inmem.ShMem.get_para_val('KCNTOMS'): self.getHPSIinfo()
        return super().timerEvent(a0)

    def getHPSIinfo(self):
        self.i += 1
        B = monitoring6(self.inmem.ShMem)
        # print(B.pumpResult[0])
        if B.pumpResult[0] == 4:
            if self.i%2 == 0:
                self.CHPpushButton.setStyleSheet('background:red')
            else:
                self.CHPpushButton.setStyleSheet(
                'background:red; border-color: red; border-style: outset; border-width: 3px;')
        if B.pumpResult[0] >= 1 and B.pumpResult[0] <= 3:
            if self.i%2 == 0:
                self.CHPpushButton.setStyleSheet('background:yellow')
            else:
                self.CHPpushButton.setStyleSheet(
                'background:yellow; border-color: red; border-style: outset; border-width: 3px;')

        if B.RWSTresult[0] == 1:
            if self.i%2 == 0:
                self.RWSTpushButton.setStyleSheet('background:yellow')
            else:
                self.RWSTpushButton.setStyleSheet(
                'background:yellow; border-color: red; border-style: outset; border-width: 3px;')

        if B.pumpResult[0] == 0:
            self.CHPpushButton.setStyleSheet('background: white')

        self.tableWidget.setRowCount(len(B.result()[:, 0]))
        self.tableWidget.setColumnCount(4)

        for i in range(len(B.result()[:, 0])):

            self.tableWidget.setCellWidget(i, 0, QCheckBox())

            for j in range(3):
                k = j + 1
                self.tableWidget.setItem(i, k, QTableWidgetItem("%s" % B.result()[i, j]))

        self.tableWidget.setRowHeight(0, 40)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setFont(QFont('Cantarell', 14, QFont.Normal, italic=False))
class DAwindow(ABCDialog):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.initUI()
        self.i = 0
        self.old_time = self.inmem.ShMem.get_para_val('KCNTOMS')
        self.startTimer(600)

    def initUI(self):
        uic.loadUi(DAui, self)

        self.setGeometry(0,0,970,1100)
        self.setWindowTitle("DA Window")
        
    def timerEvent(self, a0: 'QTimerEvent') -> None:
        if self.old_time != self.inmem.ShMem.get_para_val('KCNTOMS'): self.getDAinfo()
        return super().timerEvent(a0)
    
    def getDAinfo(self):
        self.i += 1

        if self.i%2 == 1:
            self.label.setPixmap(QPixmap("./Img/LOCA_LL6_069_XAI_3.png"))  # LDP Change

        if self.i%2 == 0:
            self.label.setPixmap(QPixmap("./Img/XAI_interface_2.png"))