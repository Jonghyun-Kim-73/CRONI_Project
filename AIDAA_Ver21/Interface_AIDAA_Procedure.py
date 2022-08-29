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
        lay.setContentsMargins(10, 15, 10, 15)
        lay.addWidget(ProcedureTop(self))
        lay.addWidget(ProcedureInfo(self))
        lay.addWidget(ProcedureWindow(self))
        lay.addWidget(ProcedureBottom(self))
        lay.setSpacing(15)
# ----------------------------------------------------------------------------------------------------------------------

class ProcedureTop(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureTop, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(149, 185, 211);')
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 66, 0)
        lay.addWidget(UrgentBTN(self))
        lay.addWidget(RadiationBTN(self))
        lay.addWidget(PredictionBTN(self))
        lay.addWidget(TripBTN(self))
        lay.addWidget(DiagnosisTopCallProcedureSearch(self))
        lay.addWidget(DiagnosisTopCallSystemSearch(self))
        lay.setSpacing(10)

class UrgentBTN(ABCLabel):
    def __init__(self, parent):
        super(UrgentBTN, self).__init__(parent)
        self.setText('긴급 조치')
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][1] is False:
            self.setStyleSheet('background-color: lightgray;')
        elif self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][1] is True:
            self.setStyleSheet('background-color: rgb(192,0,0);')

class RadiationBTN(ABCLabel):
    def __init__(self, parent):
        super(RadiationBTN, self).__init__(parent)
        self.setText('방사선비상')
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][2] is False:
            self.setStyleSheet('background-color: lightgray;')
        elif self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][2] is True:
            self.setStyleSheet('background-color: rgb(192,0,0);')

class PredictionBTN(ABCPushButton):
    def __init__(self, parent):
        super(PredictionBTN, self).__init__(parent)
        self.setText('Prediction')

class TripBTN(ABCPushButton):
    def __init__(self, parent):
        super(TripBTN, self).__init__(parent)
        self.setText('Trip')

class DiagnosisTopCallProcedureSearch(ABCPushButton):
    def __init__(self, parent):
        super(DiagnosisTopCallProcedureSearch, self).__init__(parent)
        self.setText('비정상 절차서 검색')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        print('비정상 절차서 검색 창으로 이동')
        ProcedureSearch(self).show()

class DiagnosisTopCallSystemSearch(ABCPushButton):
    def __init__(self, parent):
        super(DiagnosisTopCallSystemSearch, self).__init__(parent)
        self.setText('시스템 검색')
        self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        print('시스템 검색 창으로 이동')
        SystemSearch(self).show()
# ----------------------------------------------------------------------------------------------------------------------

class ProcedureInfo(ABCLabel):
    def __init__(self, parent):
        super(ProcedureInfo, self).__init__(parent)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        # self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0] ; 비정상 절차서 명 ex) Ab63_02: 제어봉의 계속적인 삽입
        self.setText(f" 비정상 절차서 이름: {self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]}")
# ----------------------------------------------------------------------------------------------------------------------

class ProcedureWindow(ABCWidget):
    def __init__(self, parent):
        super(ProcedureWindow, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.PS = ProcedureSequence(self)
        self.PC = Procedurecontents(self)
        lay.addWidget(self.PS)
        lay.addWidget(self.PC)
        lay.setSpacing(20)
        self.widget_timer(iter_=500, funs=[self.dis_update])
        
    def dis_update(self):
        self.PC.dis_update()
        self.PS.dis_update()
class ProcedureSequence(ABCWidget):
    def __init__(self, parent):
        super(ProcedureSequence, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.w = [ProcedureSequenceWidget(self, '목적', 1),
                  ProcedureSequenceWidget(self, '경보 및 증상', 2),
                  ProcedureSequenceWidget(self, '자동 동작 사항', 3),
                  ProcedureSequenceWidget(self, '긴급 조치 사항', 4),
                  ProcedureSequenceWidget(self, '후속 조치 사항', 5)]
        [lay.addWidget(w) for w in self.w]
        lay.setSpacing(15)
        lay.addStretch(1)
        
    def dis_update(self):
        [w.dis_update() for w in self.w]
        
class ProcedureSequenceWidget(ABCWidget):
    def __init__(self, parent, title, nub):
        super(ProcedureSequenceWidget, self).__init__(parent)
        self.lay = QHBoxLayout(self)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.PS_title = ProcedureSequenceTitle(self, title, nub)
        self.PS_button = ProcedureSequenceButton(self, title)
        self.lay.addWidget(self.PS_title)
        self.lay.addWidget(self.PS_button)
        self.lay.setSpacing(15)
        
    def dis_update(self):
        self.PS_title.dis_update()
        self.PS_button.dis_update()
        
class ProcedureSequenceTitle(ABCPushButton):
    def __init__(self, parent, title, nub):
        """_summary_

        Args:
            parent (_type_): _description_
            title (_type_): _description_
            nub (_type_): _description_
        """
        super(ProcedureSequenceTitle, self).__init__(parent)
        title_conv = {'목적':' 1.0 목적', '경보 및 증상':' 2.0 경보 및 증상', 
                      '자동 동작 사항': ' 3.0 자동 동작 사항', '긴급 조치 사항': ' 4.0 긴급 조치 사항', '후속 조치 사항': ' 5.0 후속 조치 사항'}
        self.setText(title_conv[title])
        self.nub = nub
        self.clicked.connect(self.dis_click_update)

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        if self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] == 2:
            self.setStyleSheet("""QPushButton{background: rgb(0, 176, 218);}
                                                QPushButton:hover {background: rgb(0, 176, 218);}""")
        else:
            self.setStyleSheet("""QPushButton{background: rgb(255, 255, 255);}
                                        QPushButton:hover {background: rgb(0, 176, 218);}""")
        if self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.title] == 2:  # 병행
            self.setStyleSheet('background-color: rgb(0, 176, 218)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.title] == 3:  # 불만족
            self.setStyleSheet('background-color: rgb(0, 176, 218)')
    def dis_click_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'] = self.nub
class ProcedureSequenceButton(ABCPushButton):
    def __init__(self, parent, title):
        super(ProcedureSequenceButton, self).__init__(parent)
        self.setFixedSize(55, 55)
        self.setObjectName("Check")
        self.title = title
        self.blink = False

    def dis_update(self):
        if self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.title] == 0: # 기본
            self.setStyleSheet('background-color:rgb(255, 255, 255)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.title] == 1: # 만족
            self.setStyleSheet('background-color: rgb(0,0,0)')
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.title] == 2: # 병행
            if not self.blink:
                self.setStyleSheet('background-color: yellow')
                self.blink = True
            else:
                self.setStyleSheet('background-color: white')
                self.blink = False
        elif self.inmem.procedure_progress_state[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]][
            self.title] == 3: # 불만족
            self.setStyleSheet('background-color: rgb(192,0,0)')
# ----------------------------------------------------------------------------------------------------------------------

class Procedurecontents(ABCWidget):
    def __init__(self, parent):
        super(Procedurecontents, self).__init__(parent)
        self.lay = QVBoxLayout(self)
        self.setObjectName("RightPG")
        self.setFixedWidth(1915)
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
        lay.setSpacing(15)

class ProcedureTitleBar_1(ABCLabel):
    def __init__(self, parent):
        super(ProcedureTitleBar_1, self).__init__(parent)
        self.setObjectName("TitleBar")
        self.setFixedSize(110, 55)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        # self.inmem.current_procedure['num'] ; global navigation (절차서 전환 스위치) ex) o, 1, 2, 3, 4, 5
        self.setText(f"{float(self.inmem.current_procedure[self.inmem.dis_AI['AI'][self.inmem.current_table['Procedure']][0]]['num'])}")

class ProcedureTitleBar_2(ABCLabel):
    def __init__(self, parent):
        super(ProcedureTitleBar_2, self).__init__(parent)
        self.setObjectName("TitleBar")
        #self.setFixedSize(1491, 35)
        self.setFixedHeight(55)
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
        # label 상단 정렬 위해
        content1_lay = QHBoxLayout(self)
        content1_lay.setAlignment(Qt.AlignTop)
        content2_lay = QHBoxLayout(self)
        content2_lay.setAlignment(Qt.AlignTop)
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
        content2_lay.addWidget(Procedure_Content_Check(self, self.content))
        lay.addLayout(content2_lay)
        lay.setSpacing(15)

class Procedure_Content1(ABCLabel):
    def __init__(self, parent, content=None):
        super(Procedure_Content1, self).__init__(parent)
        self.content = content
        self.setFixedSize(110, 55)
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
                    self.setFixedWidth(1674)
                elif num_len <= 5:
                    self.setFixedWidth(1634)
                elif num_len <= 7:
                    self.setFixedWidth(1498)
                elif num_len <= 9:
                    self.setFixedWidth(1458)

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
                    self.setFixedWidth(1674)
                elif num_len <= 5:
                    self.setFixedWidth(1634)
                elif num_len <= 7:
                    self.setFixedWidth(1498)
                elif num_len <= 9:
                    self.setFixedWidth(1458)
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
        self.setFixedSize(55, 55)
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


class ProcedureBottom(ABCWidget):
    def __init__(self, parent):
        super(ProcedureBottom, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addStretch(1)
        lay.addWidget(ProcedureComplet(self))
        lay.addWidget(ProcedureParallel(self))
        lay.addWidget(ProcedureReconduct(self))
        lay.setSpacing(12)

class ProcedureComplet(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureComplet, self).__init__(parent)
        self.setFixedSize(403, 60)
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
        self.setFixedSize(403, 60)
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
        self.setFixedSize(403, 60)
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

