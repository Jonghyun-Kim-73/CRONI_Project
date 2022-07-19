from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Function_Simulator_CNS import *
from AIDAA_Ver21.Interface_Alarm import *
from AIDAA_Ver21.Interface_MainTabRight import *
from AIDAA_Ver21.Interface_AIDAA_Procedure_Search import *


class Procedure(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QVBoxLayout(self)
        lay.addWidget(ProcedureTop(self))
        lay.addWidget(ProcedureInfo(self))
        lay.addWidget(ProcedureWindow(self))
        lay.addWidget(ProcedureBottom(self))
# ----------------------------------------------------------------------------------------------------------------------

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
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][1] is False:
            self.setStyleSheet('background-color: lightgray;')
        elif self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][1] is True:
            self.setStyleSheet('background-color: rgb(255,0,0);')

class RadiationBTN(ABCLabel, QLabel):
    def __init__(self, parent):
        super(RadiationBTN, self).__init__(parent)
        self.setText('방사선비상')
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][2] is False:
            self.setStyleSheet('background-color: lightgray;')
        elif self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][2] is True:
            self.setStyleSheet('background-color: rgb(255,0,0);')

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
# ----------------------------------------------------------------------------------------------------------------------

class ProcedureInfo(ABCLabel, QLabel):
    def __init__(self, parent):
        super(ProcedureInfo, self).__init__(parent)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        # self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        self.setText(f"비정상 절차서 이름: {self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]}")
# ----------------------------------------------------------------------------------------------------------------------



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

class ProcedureSequenceFirst(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSequenceFirst, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureSequenceFirst_1(self))
        lay.addWidget(ProcedureSequenceFirst_2(self))

class ProcedureSequenceFirst_1(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFirst_1, self).__init__(parent)
        self.setText('1.0 목적')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.clicked.connect(self.dis_click_update)

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] == 1:
            self.setStyleSheet('background-color: lightgray')
        else:
            self.setStyleSheet('background-color: rgb(212, 245, 211);')

    def dis_click_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] = 1


class ProcedureSequenceFirst_2(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFirst_2, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['목적'] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['목적'] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['목적'] == 2:
            self.setStyleSheet('background-color: yellow')

class ProcedureSequenceSecond(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSequenceSecond, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureSequenceSecond_1(self))
        lay.addWidget(ProcedureSequenceSecond_2(self))

class ProcedureSequenceSecond_1(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceSecond_1, self).__init__(parent)
        self.setText('2.0 경보 및 증상')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.clicked.connect(self.dis_click_update)

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] == 2:
            self.setStyleSheet('background-color: lightgray')
        else:
            self.setStyleSheet('background-color: rgb(212, 245, 211);')

    def dis_click_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] = 2

class ProcedureSequenceSecond_2(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceSecond_2, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '경보 및 증상'] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '경보 및 증상'] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '경보 및 증상'] == 2:
            self.setStyleSheet('background-color: yellow')

class ProcedureSequenceThird(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSequenceThird, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureSequenceThird_1(self))
        lay.addWidget(ProcedureSequenceThird_2(self))


class ProcedureSequenceThird_1(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceThird_1, self).__init__(parent)
        self.setText('3.0 자동 동작 사항')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.clicked.connect(self.dis_click_update)

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] == 3:
            self.setStyleSheet('background-color: lightgray')
        else:
            self.setStyleSheet('background-color: rgb(212, 245, 211);')

    def dis_click_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] = 3

class ProcedureSequenceThird_2(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceThird_2, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '자동 동작 사항'] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '자동 동작 사항'] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '자동 동작 사항'] == 2:
            self.setStyleSheet('background-color: yellow')

class ProcedureSequenceFourth(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSequenceFourth, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureSequenceFourth_1(self))
        lay.addWidget(ProcedureSequenceFourth_2(self))

class ProcedureSequenceFourth_1(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFourth_1, self).__init__(parent)
        self.setText('4.0 긴급 조치 사항')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.clicked.connect(self.dis_click_update)

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] == 4:
            self.setStyleSheet('background-color: lightgray')
        else:
            self.setStyleSheet('background-color: rgb(212, 245, 211);')

    def dis_click_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] = 4

class ProcedureSequenceFourth_2(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFourth_2, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '긴급 조치 사항'] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '긴급 조치 사항'] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '긴급 조치 사항'] == 2:
            self.setStyleSheet('background-color: yellow')

class ProcedureSequenceFifth(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSequenceFifth, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureSequenceFifth_1(self))
        lay.addWidget(ProcedureSequenceFifth_2(self))

class ProcedureSequenceFifth_1(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFifth_1, self).__init__(parent)
        self.setText('5.0 후속 조치 사항')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.clicked.connect(self.dis_click_update)

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] == 5:
            self.setStyleSheet('background-color: lightgray')
        else:
            self.setStyleSheet('background-color: rgb(212, 245, 211);')

    def dis_click_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] = 5

class ProcedureSequenceFifth_2(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFifth_2, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '후속 조치 사항'] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '후속 조치 사항'] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '후속 조치 사항'] == 2:
            self.setStyleSheet('background-color: yellow')

# ----------------------------------------------------------------------------------------------------------------------

class Procedurecontents(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedurecontents, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(149, 100, 100);')
        self.lay = QVBoxLayout(self)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure_log ; self.inmem.current_procedure['num']의 변화를 비교하기 위한 이전 값 (default 0)
        3. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        4. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        '''

        # if self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] in list(set(self.inmem.access_procedure)):
        current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        # else:
        #     current_state = '내용 없음'

        if current_state == '내용 없음':
            # pass
            self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] = 0
            self.clearLayout(self.lay)
        else:
            if self.inmem.current_procedure_log[0] != self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] or self.inmem.current_procedure_log[1] != self.inmem.current_table['Procedure']:
                self.clearLayout(self.lay)
                self.lay.addWidget(ProcedureTitleBar(self))
                self.func_dict = {0: Procedure0(self), 1: Procedure1(self), 2: Procedure2(self), 3: Procedure3(self),
                                  4: Procedure4(self), 5: Procedure5(self), 6: Procedure6(self), 7: Procedure7(self),
                                  8: Procedure8(self),
                                  9: Procedure9(self), 10: Procedure10(self), 11: Procedure11(self), 12: Procedure12(self),
                                  13: Procedure13(self),
                                  14: Procedure14(self), 15: Procedure15(self), 16: Procedure16(self),
                                  17: Procedure17(self)}

                try:
                    [self.lay.addWidget(self.func_dict[i]) for i in range(self.inmem.ShMem.get_pro_procedure_count(
                        self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state])]
                except:
                    pass
                self.inmem.current_procedure_log[0] = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']
        self.inmem.current_procedure_log[1] = self.inmem.current_table['Procedure']
        # self.inmem.access_procedure.append(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

class ProcedureTitleBar(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureTitleBar, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureTitleBar_1(self))
        lay.addWidget(ProcedureTitleBar_2(self))

class ProcedureTitleBar_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(ProcedureTitleBar_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        self.setText(f"{float(self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'])}")

class ProcedureTitleBar_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(ProcedureTitleBar_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        # self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        self.setText(self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']])

class Procedure0(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure0, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure0_1(self))
        lay.addWidget(Procedure0_2(self))
        lay.addWidget(Procedure0_check(self))

class Procedure0_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure0_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 0
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''
        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'): pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][self.content]['Nub'])

class Procedure0_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure0_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 0
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''
        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])

class Procedure0_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure0_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
        self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
        self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
        current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
        check_btn_num: 운전원 puch버튼 
        '''
        self.check_btn_num = 0
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state][self.check_btn_num] = self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')

class Procedure1(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure1, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure1_1(self))
        lay.addWidget(Procedure1_2(self))
        lay.addWidget(Procedure1_check(self))

class Procedure1_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure1_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 1
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])

class Procedure1_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure1_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 1
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])

class Procedure1_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure1_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
        self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
        self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
        current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
        check_btn_num: 운전원 puch버튼 
        '''
        self.check_btn_num = 1
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
                self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                    self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')

class Procedure2(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure2, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure2_1(self))
        lay.addWidget(Procedure2_2(self))
        lay.addWidget(Procedure2_check(self))

class Procedure2_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure2_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 2
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])

class Procedure2_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure2_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 2
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])

class Procedure2_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure2_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
        self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
        self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
        current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
        check_btn_num: 운전원 puch버튼 
        '''
        self.check_btn_num = 2
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')

class Procedure3(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure3, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure3_1(self))
        lay.addWidget(Procedure3_2(self))
        lay.addWidget(Procedure3_check(self))

class Procedure3_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure3_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 3
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])

class Procedure3_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure3_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 3
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])

class Procedure3_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure3_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 3
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')

class Procedure4(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure4, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure4_1(self))
        lay.addWidget(Procedure4_2(self))
        lay.addWidget(Procedure4_check(self))

class Procedure4_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure4_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 4
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])

class Procedure4_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure4_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 4
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])

class Procedure4_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure4_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 4
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')

class Procedure5(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure5, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure5_1(self))
        lay.addWidget(Procedure5_2(self))
        lay.addWidget(Procedure5_check(self))

class Procedure5_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure5_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 5
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])

class Procedure5_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure5_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 5
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])

class Procedure5_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure5_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 5
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')

class Procedure6(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure6, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure6_1(self))
        lay.addWidget(Procedure6_2(self))
        lay.addWidget(Procedure6_check(self))

class Procedure6_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure6_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 6
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])

class Procedure6_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure6_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 6
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])

class Procedure6_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure6_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 6
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')


class Procedure7(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure7, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure7_1(self))
        lay.addWidget(Procedure7_2(self))
        lay.addWidget(Procedure7_check(self))


class Procedure7_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure7_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 7
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])


class Procedure7_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure7_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 7
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])


class Procedure7_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure7_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 7
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])

        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')


class Procedure8(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure8, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure8_1(self))
        lay.addWidget(Procedure8_2(self))
        lay.addWidget(Procedure8_check(self))


class Procedure8_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure8_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 8
        # self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])


class Procedure8_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure8_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 8
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])


class Procedure8_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure8_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 8
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')


class Procedure9(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure9, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure9_1(self))
        lay.addWidget(Procedure9_2(self))
        lay.addWidget(Procedure9_check(self))


class Procedure9_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure9_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 9
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])


class Procedure9_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure9_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 9
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])


class Procedure9_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure9_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 9
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')


class Procedure10(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure10, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure10_1(self))
        lay.addWidget(Procedure10_2(self))
        lay.addWidget(Procedure10_check(self))


class Procedure10_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure10_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 10
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])


class Procedure10_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure10_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 10
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])


class Procedure10_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure10_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 10
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')


class Procedure11(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure11, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure11_1(self))
        lay.addWidget(Procedure11_2(self))
        lay.addWidget(Procedure11_check(self))


class Procedure11_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure11_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 11
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])


class Procedure11_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure11_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 11
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])


class Procedure11_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure11_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 11
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')


class Procedure12(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure12, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure12_1(self))
        lay.addWidget(Procedure12_2(self))
        lay.addWidget(Procedure12_check(self))


class Procedure12_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure12_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 12
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])


class Procedure12_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure12_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 12
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])


class Procedure12_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure12_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 12
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')


class Procedure13(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure13, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure13_1(self))
        lay.addWidget(Procedure13_2(self))
        lay.addWidget(Procedure13_check(self))


class Procedure13_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure13_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 13
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])


class Procedure13_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure13_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 13
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])


class Procedure13_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure13_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 13
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')


class Procedure14(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure14, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure14_1(self))
        lay.addWidget(Procedure14_2(self))
        lay.addWidget(Procedure14_check(self))


class Procedure14_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure14_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 14
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])


class Procedure14_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure14_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 14
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])


class Procedure14_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure14_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 14
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')


class Procedure15(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure15, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure15_1(self))
        lay.addWidget(Procedure15_2(self))
        lay.addWidget(Procedure15_check(self))


class Procedure15_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure15_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 15
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])


class Procedure15_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure15_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 15
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])


class Procedure15_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure15_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        '''
                self.inmem.procedure_click_state: 절차서명, 절차 순서에 따른 운전원 버튼 상태를 저장하기 위한 딕셔너리
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]: 선택된 절차서 명
                current_state: self.inmem.current_procedure['des'][self.inmem.current_procedure['num']] : 현재 선택된 절차 순서 ex) 목적, 경보 및 증상
                check_btn_num: 운전원 puch버튼 
                '''
        self.check_btn_num = 15
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
            pass
        else:
            self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = 0
        else:
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] = \
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state][self.check_btn_num] + 1

    def dis_update1(self):
        if self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 0:
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: lightgray')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: yellow')


class Procedure16(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure16, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure16_1(self))
        lay.addWidget(Procedure16_2(self))
        lay.addWidget(Procedure16_check(self))


class Procedure16_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure16_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 16
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])


class Procedure16_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure16_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 16
        # self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])


class Procedure16_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure16_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.clicked.connect(self.dis_update)
        self.clicked_state = 0

    def dis_update(self):
        if self.clicked_state == 2:
            self.clicked_state = 0
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        else:
            self.clicked_state = self.clicked_state + 1
            if self.clicked_state == 1:
                self.setStyleSheet('background-color: lightgray')
            elif self.clicked_state == 2:
                self.setStyleSheet('background-color: yellow')


class Procedure17(ABCWidget, QWidget):
    def __init__(self, parent):
        super(Procedure17, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(Procedure17_1(self))
        lay.addWidget(Procedure17_2(self))
        lay.addWidget(Procedure17_check(self))


class Procedure17_1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure17_1, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 17
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Nub'])


class Procedure17_2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(Procedure17_2, self).__init__(parent)
        self.setStyleSheet('background-color: white;')
        self.content = 17
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''

        if (self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or
                self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적'):
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                 self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                 self.content]['Des'])


class Procedure17_check(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(Procedure17_check, self).__init__(parent)
        self.setText('')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.clicked_state = 0
        self.clicked.connect(self.dis_update)


    def dis_update(self):
        if self.clicked_state == 2:
            self.clicked_state = 0
            self.setStyleSheet('background-color:rgb(212, 245, 211)')
        else:
            self.clicked_state = self.clicked_state + 1
            if self.clicked_state == 1:
                self.setStyleSheet('background-color: lightgray')
            elif self.clicked_state == 2:
                self.setStyleSheet('background-color: yellow')


# ----------------------------------------------------------------------------------------------------------------------




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
        self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update1(self):
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.current_state == '내용 없음':
            pass
        else:
            if 0 in self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state]:
                self.setEnabled(False)
            elif 2 in self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state]:
                self.setEnabled(False)
            else:
                self.setEnabled(True)

    def dis_update(self):
        self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state] = 1
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] += 1

class ProcedureParallel(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureParallel, self).__init__(parent)
        self.setText('병행')
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state] = 2
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] += 1



class ProcedureReconduct(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureReconduct, self).__init__(parent)
        self.setText('재수행')
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state][:] = [0 for i in range(len(self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state]))]



