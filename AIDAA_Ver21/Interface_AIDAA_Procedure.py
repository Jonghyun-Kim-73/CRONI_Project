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
        self.setText(f" 비정상 절차서 이름: {self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]}")
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

class ProcedureSequenceFirst_2(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFirst_2, self).__init__(parent)
        self.setFixedSize(35, 35)
        self.setObjectName("Check")
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '목적'] == 0: # 기본
            self.setStyleSheet('background-color:rgb(255, 255, 255)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '목적'] == 1: # 만족
            self.setStyleSheet('background-color: rgb(0,0,0)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '목적'] == 2: # 병행
            self.setStyleSheet('background-color: yellow')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '목적'] == 3: # 불만족
            self.setStyleSheet('background-color: rgb(192,0,0)')

class ProcedureSequenceSecond(ABCWidget):
    def __init__(self, parent):
        super(ProcedureSequenceSecond, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(ProcedureSequenceSecond_1(self))
        lay.addWidget(ProcedureSequenceSecond_2(self))
        lay.setSpacing(5)

class ProcedureSequenceSecond_1(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceSecond_1, self).__init__(parent)
        self.setText(' 2.0 경보 및 증상')
        self.setObjectName("Tab")
        self.setFixedSize(275, 35)
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


class ProcedureSequenceSecond_2(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceSecond_2, self).__init__(parent)
        self.setFixedSize(35, 35)
        self.setObjectName("Check")
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '경보 및 증상'] == 0:
            self.setStyleSheet('background-color:rgb(255, 255, 255)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '경보 및 증상'] == 1:
            self.setStyleSheet('background-color: 0,0,0')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '경보 및 증상'] == 2:
            self.setStyleSheet('background-color: yellow')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '경보 및 증상'] == 3:
            self.setStyleSheet('background-color: rgb(192,0,0)')

class ProcedureSequenceThird(ABCWidget):
    def __init__(self, parent):
        super(ProcedureSequenceThird, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(ProcedureSequenceThird_1(self))
        lay.addWidget(ProcedureSequenceThird_2(self))
        lay.setSpacing(5)


class ProcedureSequenceThird_1(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceThird_1, self).__init__(parent)
        self.setFixedSize(275, 35)
        self.setText(' 3.0 자동 동작 사항')
        self.setObjectName("Tab")
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.clicked.connect(self.dis_click_update)

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] == 3:
            self.setStyleSheet("""QPushButton{background: rgb(0, 176, 218);}
                                                        QPushButton:hover {background: rgb(0, 176, 218);}""")
        else:
            self.setStyleSheet("""QPushButton{background: rgb(255, 255, 255);}
                                        QPushButton:hover {background: rgb(0, 176, 218);}""")

    def dis_click_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] = 3


class ProcedureSequenceThird_2(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceThird_2, self).__init__(parent)
        self.setFixedSize(35, 35)
        self.setObjectName("Check")
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '자동 동작 사항'] == 0:
            self.setStyleSheet('background-color:rgb(255, 255, 255)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '자동 동작 사항'] == 1:
            self.setStyleSheet('background-color:rgb(0,0,0)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '자동 동작 사항'] == 2:
            self.setStyleSheet('background-color: yellow')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '자동 동작 사항'] == 3:
            self.setStyleSheet('background-color: rgb(192,0,0)')

class ProcedureSequenceFourth(ABCWidget):
    def __init__(self, parent):
        super(ProcedureSequenceFourth, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(ProcedureSequenceFourth_1(self))
        lay.addWidget(ProcedureSequenceFourth_2(self))
        lay.setSpacing(5)

class ProcedureSequenceFourth_1(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFourth_1, self).__init__(parent)
        self.setText(' 4.0 긴급 조치 사항')
        self.setObjectName("Tab")
        self.setFixedSize(275, 35)
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.clicked.connect(self.dis_click_update)

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] == 4:
            self.setStyleSheet("""QPushButton{background: rgb(0, 176, 218);}
                                                QPushButton:hover {background: rgb(0, 176, 218);}""")
        else:
            self.setStyleSheet("""QPushButton{background: rgb(255, 255, 255);}
                                        QPushButton:hover {background: rgb(0, 176, 218);}""")

    def dis_click_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] = 4


class ProcedureSequenceFourth_2(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFourth_2, self).__init__(parent)
        self.setFixedSize(35, 35)
        self.setObjectName("Check")
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '긴급 조치 사항'] == 0:
            self.setStyleSheet('background-color:rgb(255, 255, 255)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '긴급 조치 사항'] == 1:
            self.setStyleSheet('background-color: rgb(0,0,0)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '긴급 조치 사항'] == 2:
            self.setStyleSheet('background-color: yellow')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '긴급 조치 사항'] == 3:
            self.setStyleSheet('background-color: rgb(192,0,0)')

class ProcedureSequenceFifth(ABCWidget):
    def __init__(self, parent):
        super(ProcedureSequenceFifth, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(ProcedureSequenceFifth_1(self))
        lay.addWidget(ProcedureSequenceFifth_2(self))
        lay.setSpacing(5)

class ProcedureSequenceFifth_1(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFifth_1, self).__init__(parent)
        self.setFixedSize(275, 35)
        self.setObjectName("Tab")
        self.setText(' 5.0 후속 조치 사항')
        self.widget_timer(iter_=500, funs=[self.dis_update])
        self.clicked.connect(self.dis_click_update)

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] == 5:
            self.setStyleSheet("""QPushButton{background: rgb(0, 176, 218);}
                                        QPushButton:hover {background: rgb(0, 176, 218);}""")
        else:
            self.setStyleSheet("""QPushButton{background: rgb(255, 255, 255);}
                                        QPushButton:hover {background: rgb(0, 176, 218);}""")

    def dis_click_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] = 5


class ProcedureSequenceFifth_2(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSequenceFifth_2, self).__init__(parent)
        self.setFixedSize(35, 35)
        self.setObjectName("Check")
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '후속 조치 사항'] == 0:
            self.setStyleSheet('background-color:rgb(255, 255, 255)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '후속 조치 사항'] == 1:
            self.setStyleSheet('background-color: rgb(0,0,0)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '후속 조치 사항'] == 2:
            self.setStyleSheet('background-color: yellow')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            '후속 조치 사항'] == 3:
            self.setStyleSheet('background-color: rgb(192,0,0)')

# ----------------------------------------------------------------------------------------------------------------------

class Procedurecontents(ABCWidget):
    def __init__(self, parent):
        super(Procedurecontents, self).__init__(parent)
        self.lay = QVBoxLayout(self)
        self.setObjectName("RightPG")
        self.setFixedWidth(1591)
        self.lay.setContentsMargins(0, 0, 0, 0)

        # scroll 적용
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.setObjectName("scroll_bg")
        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.lay)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.vbox.addWidget(self.scroll)
        self.setLayout(self.vbox)

        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure_log ; self.inmem.current_procedure['num']의 변화를 비교하기 위한 이전 값 (default 0)
        3. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        4. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        '''

        current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if current_state == '내용 없음':
            self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] = 0
            self.clearLayout(self.lay)
        else:
            if self.inmem.current_procedure_log[0] != self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] or self.inmem.current_procedure_log[1] != self.inmem.current_table['Procedure']:
                self.clearLayout(self.lay)
                self.lay.addWidget(ProcedureTitleBar(self))
                self.func_dict = {i: Procedure_Content(self, i) for i in range(18)}
                try:
                    [self.lay.addWidget(self.func_dict[i]) for i in range(self.inmem.ShMem.get_pro_procedure_count(
                        self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state])]
                except: pass
                self.inmem.current_procedure_log[0] = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']
        self.inmem.current_procedure_log[1] = self.inmem.current_table['Procedure']
        self.lay.setSpacing(15)
        self.lay.addStretch(1)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

class ProcedureTitleBar(ABCWidget):
    def __init__(self, parent):
        super(ProcedureTitleBar, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(ProcedureTitleBar_1(self))
        lay.addWidget(ProcedureTitleBar_2(self))

class ProcedureTitleBar_1(ABCLabel):
    def __init__(self, parent):
        super(ProcedureTitleBar_1, self).__init__(parent)
        self.setObjectName("TitleBar")
        self.setFixedSize(105, 35)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        self.setText(f"{float(self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'])}")

class ProcedureTitleBar_2(ABCLabel):
    def __init__(self, parent):
        super(ProcedureTitleBar_2, self).__init__(parent)
        self.setObjectName("TitleBar")
        self.setFixedSize(1491, 35)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        # self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        self.setText(self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']])


# ----------------------------------------------------------------------------------------------------------------------

class Procedure_Content(ABCWidget):
    def __init__(self, parent, content=None):
        super(Procedure_Content, self).__init__(parent)
        self.content = content
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 40, 0)
        lay.addStretch(1)
        # num label 상단 정렬 위해
        content1_lay = QHBoxLayout(self)
        content1_lay.setAlignment(Qt.AlignTop)
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적':
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content + 1 <= self.inmem.ShMem.get_pro_procedure_count(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                if self.inmem.get_ab_procedure_num(self.content)[0] == "0":
                    lay.addWidget(Procedure_Content2_1(self, self.content))
                else:
                    content1_lay.addWidget(Procedure_Content1(self, self.content))
                    lay.addLayout(content1_lay)
                    lay.addWidget(Procedure_Content2_2(self, self.content))
        lay.addWidget(Procedure_Content_Check(self, self.content))
        lay.setSpacing(5)

class Procedure_Content1(ABCLabel):
    def __init__(self, parent, content=None):
        super(Procedure_Content1, self).__init__(parent)
        self.content = content
        self.setFixedSize(105, 35)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적':
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                self.setText(self.inmem.ShMem.get_pro_procedure(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][self.content]['Nub'])

# 참고사항 / 주의사항 label
class Procedure_Content2_1(ABCLabel):
    def __init__(self, parent, content):
        super(Procedure_Content2_1, self).__init__(parent)
        self.content = content
        self.lay = QVBoxLayout(self)
        self.label_title = QLabel("")
        self.label_content = QLabel("")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.setObjectName("Notice")
        self.label_title.setObjectName("label_title")
        self.label_content.setObjectName("label_content")
        self.label_content.setWordWrap(True)
        self.lay.addWidget(self.label_title)
        self.lay.addWidget(self.label_content)
        self.lay.addStretch(1)
        self.setLayout(self.lay)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적':
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:

                num_len = len(self.inmem.ShMem.get_pro_procedure(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][self.content]['Nub'])
                if num_len <= 3:
                    self.setFixedWidth(1364)
                elif num_len <= 5:
                    self.setFixedWidth(1326)
                elif num_len <= 7:
                    self.setFixedWidth(1288)
                elif num_len <= 9:
                    self.setFixedWidth(1250)

                if self.inmem.get_ab_procedure_num(self.content)[0] == "0":
                    # self.clearLayout(self.lay)
                    self.label_title.setText("%s" % self.inmem.get_ab_procedure_des(self.content)[:4])
                    self.label_content.setText("%s" % self.inmem.get_ab_procedure_des(self.content)[7:])


class Procedure_Content2_2(ABCLabel):
    def __init__(self, parent, content):
        super(Procedure_Content2_2, self).__init__(parent)
        self.content = content
        self.setWordWrap(True)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        1. self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        2. self.inmem.current_procedure['des'] ; global navigation btn name ex) '목적', '경보 및 증상' 등.
        --> inmem.get_pro_procedure와 inmem.get_pro_procedure_count dictionary 접속을 위해 활용
        3. self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        4. self.content ; 해당 행 번호 ex) 행 개수에 비해 내용이 많을 경우 오류 발생, 이를 방지하기위한 조건문
        '''
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '내용 없음' or self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']] == '목적':
            pass
        else:
            current_state = self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
            if self.content+1 <= self.inmem.ShMem.get_pro_procedure_count(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[current_state]:
                num_len = len(self.inmem.ShMem.get_pro_procedure(self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][self.content]['Nub'])
                if num_len <= 3:
                    self.setFixedWidth(1364)
                elif num_len <= 5:
                    self.setFixedWidth(1326)
                elif num_len <= 7:
                    self.setFixedWidth(1288)
                elif num_len <= 9:
                    self.setFixedWidth(1250)
                self.setText(self.inmem.ShMem.get_pro_procedure(
                    self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[
                                    self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]][
                                    self.content]['Des'])

class Procedure_Content_Check(ABCPushButton, QPushButton):
    def __init__(self, parent, content):
        super(Procedure_Content_Check, self).__init__(parent)
        self.check_btn_num = content
        self.current_state = \
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][
            self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        self.setFixedSize(35, 35)
        if self.check_btn_num >= self.inmem.ShMem.get_pro_procedure_count(
                self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0])[self.current_state]:
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
            self.setStyleSheet('background-color:rgb(255, 255, 255)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state][self.check_btn_num] == 1:
            self.setStyleSheet('background-color: rgb(0,0,0)')
        elif self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state][self.check_btn_num] == 2:
            self.setStyleSheet('background-color: rgb(192,0,0)')


class ProcedureBottom(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureBottom, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addStretch(1)
        lay.addWidget(ProcedureComplet(self))
        lay.addWidget(ProcedureParallel(self))
        lay.addWidget(ProcedureReconduct(self))
        lay.setSpacing(20)

class ProcedureComplet(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureComplet, self).__init__(parent)
        self.setFixedSize(274, 35)
        self.setObjectName("Bottom")
        self.setText('완료')
        self.widget_timer(iter_=500, funs=[self.dis_update1])
        self.clicked.connect(self.dis_update)

    def dis_update1(self):
        self.current_state = \
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][
            self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        if self.current_state == '내용 없음':
            pass
        else:
            if 2 in self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state]:
                self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][self.current_state] = 3  # 변경
                self.setEnabled(False)
            elif 0 in self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state]:
                self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                    self.current_state] = 0  # 변경
                self.setEnabled(False)
            else:
                self.setEnabled(True)

    def dis_update(self):
        self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state] = 1
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] != 5:
            self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] += 1

class ProcedureParallel(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureParallel, self).__init__(parent)
        self.setFixedSize(274, 35)
        self.setObjectName("Bottom")
        self.setText('병행')
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.current_state = \
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][
            self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state] = 2
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] != 5:
            self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] += 1

class ProcedureReconduct(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureReconduct, self).__init__(parent)
        self.setFixedSize(274, 35)
        self.setObjectName("Bottom")
        self.setText('재수행')
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        self.current_state = \
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['des'][
            self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num']]
        self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.current_state][:] = [0 for i in range(len(
            self.inmem.procedure_click_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
                self.current_state]))]

