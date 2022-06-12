from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Simulator_CNS import *
from AIDAA_Ver21.Interface_Alarm import *
from AIDAA_Ver21.Interface_MainTabSystem import *
from AIDAA_Ver21.Interface_Search import *

class Procedure(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QVBoxLayout(self)
        lay.addWidget(ProcedureTop(self))
        lay.addWidget(ProcedureInfo(self))
        lay.addWidget(ProcedureWindow(self))
        lay.addWidget(ProcedureBottom(self))

class ProcedureTop(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureTop, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(149, 185, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(UrgentBTN(self))
        lay.addWidget(RadiationBTN(self))
        lay.addWidget(PredictionBTN(self))
        lay.addWidget(TripBTN(self))
        lay.addWidget(DiagnosisTopCallProcedureSearch(self))
        lay.addWidget(DiagnosisTopCallSystemSearch(self))

class UrgentBTN(ABCLabel, QLabel):
    def __init__(self, parent):
        super(UrgentBTN, self).__init__(parent)
        self.setText('긴급 조치')

class RadiationBTN(ABCLabel, QLabel):
    def __init__(self, parent):
        super(RadiationBTN, self).__init__(parent)
        self.setText('방사선비상')

class PredictionBTN(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(PredictionBTN, self).__init__(parent)
        self.setText('Prediction')

class TripBTN(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(TripBTN, self).__init__(parent)
        self.setText('Trip')

class DiagnosisTopCallProcedureSearch(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(DiagnosisTopCallProcedureSearch, self).__init__(parent)
        self.setText('비정상 절차서 검색')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        print('비정상 절차서 검색 창으로 이동')
        ProcedureSearch(self).show()

class DiagnosisTopCallSystemSearch(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(DiagnosisTopCallSystemSearch, self).__init__(parent)
        self.setText('시스템 검색')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        print('시스템 검색 창으로 이동')
        SystemSearch(self).show()

class ProcedureInfo(ABCLabel, QLabel):
    def __init__(self, parent):
        super(ProcedureInfo, self).__init__(parent)
        self.setText('비정상 절차서 이름')

class ProcedureWindow(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureWindow, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureSequence(self))
        lay.addWidget(Procedurecontents(self))

class ProcedureSequence(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSequence, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QVBoxLayout(self)
        lay.addWidget(ProcedureSequenceFirst(self))
        lay.addWidget(ProcedureSequenceSecond(self))
        lay.addWidget(ProcedureSequenceThird(self))
        lay.addWidget(ProcedureSequenceFourth(self))
        lay.addWidget(ProcedureSequenceFifth(self))

class ProcedureSequenceFirst(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFirst, self).__init__(parent)
        self.setText('1.0 목적')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")

class ProcedureSequenceSecond(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceSecond, self).__init__(parent)
        self.setText('2.0 경보 및 증상')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")

class ProcedureSequenceThird(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceThird, self).__init__(parent)
        self.setText('3.0 자동 동작 사항')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")

class ProcedureSequenceFourth(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFourth, self).__init__(parent)
        self.setText('4.0 긴급 조치 사항')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")

class ProcedureSequenceFifth(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFifth, self).__init__(parent)
        self.setText('5.0 후속 조치 사항')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")

class Procedurecontents(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedurecontents, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QVBoxLayout(self)



class ProcedureBottom(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureBottom, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureComplet(self))
        lay.addWidget(ProcedureParallel(self))
        lay.addWidget(ProcedureReconduct(self))

class ProcedureComplet(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureComplet, self).__init__(parent)
        self.setText('완료')

class ProcedureParallel(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureParallel, self).__init__(parent)
        self.setText('병행')

class ProcedureReconduct(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureReconduct, self).__init__(parent)
        self.setText('재수행')

