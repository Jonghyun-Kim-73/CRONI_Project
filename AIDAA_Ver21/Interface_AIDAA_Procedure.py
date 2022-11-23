import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Function_Simulator_CNS import *
from AIDAA_Ver21.Interface_Alarm import *
from AIDAA_Ver21.Interface_MainTabRight import *
from AIDAA_Ver21.Interface_AIDAA_Procedure_Search import *
import Interface_QSS as qss
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class Procedure(ABCWidget):
    def __init__(self, parent):
        super(Procedure, self).__init__(parent)
        # self.setStyleSheet(qss.AIDAA_Diagnosis2)
        # self.setObjectName("BG")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 15, 9, 15)
        lay.addWidget(ProcedureTop(self))
        lay.addWidget(ProcedureInfo(self))
        lay.addWidget(ProcedureWindow(self))
        lay.addWidget(ProcedureBottom(self))
        lay.setSpacing(15)

        self.procedure_name = ''

        self.widget_timer(iter_=500, funs=[self.update_procedure_sequence, self.update_procedure_sequence_cond])

    def set_procedure_name(self, procedure_name):
        self.procedure_name = procedure_name
        self.radiation = self.inmem.ShMem.get_pro_radiation(procedure_name)
        self.urgent_act = self.inmem.ShMem.get_pro_urgent_act(procedure_name)
        # 절차서 명 변경에 따른 인터페이스 업데이트
        self.inmem.widget_ids['RadiationBTN'].dis_update(self.radiation)
        self.inmem.widget_ids['UrgentBTN'].dis_update(self.urgent_act)
        self.inmem.widget_ids['ProcedureInfo'].dis_update(self.procedure_name)
        self.update_procedure_sequence()
        self.update_procedure_sequence_cond()
        self.update_procedure_contents()

    def update_procedure_sequence(self):
        # Blink 로 인해 timer와 연결
        if self.procedure_name != '':  # 초기 소프트웨어 구동 시 절차서 선택되지 않아서 동작 X
            self.SequenceTitleClickHis = self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClickHis']
            self.inmem.widget_ids['ProcedureSequenceTitlePu'].dis_update(self.SequenceTitleClickHis)
            self.inmem.widget_ids['ProcedureSequenceTitleAl'].dis_update(self.SequenceTitleClickHis)
            self.inmem.widget_ids['ProcedureSequenceTitleAu'].dis_update(self.SequenceTitleClickHis)
            self.inmem.widget_ids['ProcedureSequenceTitleUr'].dis_update(self.SequenceTitleClickHis)
            self.inmem.widget_ids['ProcedureSequenceTitleFo'].dis_update(self.SequenceTitleClickHis)

    def update_procedure_sequence_cond(self):
        # Blink 로 인해 timer와 연결
        if self.procedure_name != '':  # 초기 소프트웨어 구동 시 절차서 선택되지 않아서 동작 X
            self.SequenceTitleCondHis = self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleCondHis']
            self.inmem.widget_ids['ProcedureSequenceTitleCondAl'].dis_update(self.SequenceTitleCondHis)
            self.inmem.widget_ids['ProcedureSequenceTitleCondPu'].dis_update(self.SequenceTitleCondHis)
            self.inmem.widget_ids['ProcedureSequenceTitleCondAu'].dis_update(self.SequenceTitleCondHis)
            self.inmem.widget_ids['ProcedureSequenceTitleCondUr'].dis_update(self.SequenceTitleCondHis)
            self.inmem.widget_ids['ProcedureSequenceTitleCondFo'].dis_update(self.SequenceTitleCondHis)

    def update_procedure_contents(self):
        self.SequenceTitleClick = self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClick']
        self.ContentsClickHis = self.inmem.ProcedureHis[self.procedure_name]['ContentsClickHis']
        self.Contents = self.inmem.ProcedureHis[self.procedure_name]['Contents']
        self.inmem.widget_ids['ProcedureContents'].dis_update(self.SequenceTitleClick, self.ContentsClickHis, self.Contents)
        self.Rule_2_CheckComplete()

    def check_SequenceTitleCondHis(self):
        """현재 선택된 Title에 대한 SequenceTitleCondHis 반환

        Returns:
            int: 0 (진행 중), 1 (완료), 2 (병행), 3 (불만족)
        """
        current_title = self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClick']
        return self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleCondHis'][current_title]

    def change_SequenceTitleClickHis(self, title: str):
        """Sequence Area의 버튼 클릭 시 버튼을 활성화 시키고 해당 title(ex. 목적) 외의 버튼은 비활성화 시킴.

        Args:
            title (_str_): '목적'
        """
        for title_ in self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClickHis'].keys():
            if title_ == title:
                self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClickHis'][title_] = True
                self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClick'] = title_
            else:
                self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClickHis'][title_] = False
        self.update_procedure_sequence()
        self.update_procedure_contents()

    def change_SequenceNextTitle(self):
        """Sequence Area에서 현재 활성화된 버튼 다음 버튼으로 이동
        """
        current_title = self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClick']
        rule = {'목적': '경보 및 증상', '경보 및 증상': '자동 동작 사항',
                '자동 동작 사항': '긴급 조치 사항', '긴급 조치 사항': '후속 조치 사항', '후속 조치 사항': '후속 조치 사항'}
        self.change_SequenceTitleClickHis(rule[current_title])

    def change_SequenceTitleCondHis(self, Cond: int):
        """SequenceTitleCondHis를 Cond 로 업데이트

        Args:
            Cond (int): 0 (진행 중), 1 (완료), 2 (병행), 3 (불만족)
        """
        current_title = self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClick']
        self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleCondHis'][current_title] = Cond

    def change_SequenceTitleCondHis_then_SequenceNextTitle(self, Cond: int):
        """ProcedureComplete BTN 을 누른 경우 SequenceTitleCondHis를 Cond로 업데이트 하고 SequenceNextTitle 수행"""
        self.change_SequenceTitleCondHis(Cond)
        self.change_SequenceNextTitle()

    def change_ContentsClickHis(self, ContentsClickHis: int, ContentsClickHis_index: int):
        """Content Area 에서 Check 버튼 클릭 시 His 값 업데이트

        - Rule 1 : 만약 ContentsClickHis 가 2 (불만족) 이라면 SequenceTitleCondHis 를 3으로 업데이트 없다면 0
        - Rule 2 : 만약 모든 ContentsClickHis 가 1 (완료) 이라면 ProcedureComplete BTN Enable

        Args:
            ContentsClickHis (int): 0, 1, 2
            ContentsClickHis_inTitle_index (int): 해당 값이 위치한 index
        """
        current_title = self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClick']
        self.inmem.ProcedureHis[self.procedure_name]['ContentsClickHis'][current_title][
            ContentsClickHis_index] = ContentsClickHis

        if self.Rule_1_Change_SequenceTitleCondHis():
            self.change_SequenceTitleCondHis(3)
        elif self.Rule_2_CheckComplete():
            self.change_SequenceTitleCondHis(0)
        else:
            self.change_SequenceTitleCondHis(0)

    def Rule_1_Change_SequenceTitleCondHis(self):
        """Rule 1 : 만약 ContentsClickHis 가 2 (불만족) 이라면 SequenceTitleCondHis 를 3으로 업데이트 없다면 0"""
        current_title = self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClick']
        all_step_check = any([True if cond == 2 else False for cond in
                              self.inmem.ProcedureHis[self.procedure_name]['ContentsClickHis'][current_title]])
        return all_step_check

    def Rule_2_CheckComplete(self):
        """Rule 2 : 만약 모든 ContentsClickHis 가 1 (완료) 이라면 ProcedureComplete BTN Enable"""
        current_title = self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClick']
        all_step_check = all([True if cond == 1 else False for cond in
                              self.inmem.ProcedureHis[self.procedure_name]['ContentsClickHis'][current_title]])
        self.inmem.widget_ids['ProcedureComplete'].setEnabled(all_step_check)
        return all_step_check

    def clear_ContentsClickHis(self):
        """Content Area 에 저장된 모든 값을 초기화 한뒤 현재 SequenceTitleCondHis 상태를 0으로 바꾸고 다시 Content Area 생성한다.
        """
        current_title = self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClick']
        max_len = len(self.inmem.ProcedureHis[self.procedure_name]['ContentsClickHis'][current_title])

        for i in range(max_len):
            self.inmem.ProcedureHis[self.procedure_name]['ContentsClickHis'][current_title][i] = 0

        self.change_SequenceTitleCondHis(0)

        self.update_procedure_contents()
# ----------------------------------------------------------------------------------------------------------------------

class ProcedureTop(ABCWidget):
    def __init__(self, parent):
        super(ProcedureTop, self).__init__(parent)
        # qss확인 후 주석 해제
        # self.setStyleSheet(qss.Main_Tab)
        self.setFixedHeight(40)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(TopBTN(self, 'UrgentBTN', '긴급 조치'))
        lay.addWidget(TopBTN(self, 'RadiationBTN', '방사선비상'))
        lay.addWidget(AlarmFixPreTrip(self, 227))
        lay.addWidget(AlarmFixTrip(self, 228))
        lay.addSpacing(5)
        lay.addWidget(DiagnosisTopCallProcedureSearch(self))
        lay.addWidget(DiagnosisTopCallSystemSearch(self))
        lay.setSpacing(10)

class TopBTN(ABCLabel):
    def __init__(self, parent, widget_name, title):
        super(TopBTN, self).__init__(parent, widget_name)
        self.setObjectName("Label") # 실행 후 확인
        self.setFixedSize(227, 40)
        self.setText(title)

    def dis_update(self, trigger):
        if trigger:
            self.setStyleSheet('background-color: rgb(192,0,0);')
        else:
            self.setStyleSheet('background-color: lightgray;')

# 추후 알람파트 수정시 사용
# class PredictionBTN(ABCPushButton):
#     def __init__(self, parent):
#         super(PredictionBTN, self).__init__(parent)
#         self.setObjectName("Button")
#         self.setFixedSize(393, 55)
#         self.setText('Prediction')
#
# class TripBTN(ABCPushButton):
#     def __init__(self, parent):
#         super(TripBTN, self).__init__(parent)
#         self.setObjectName("Button")
#         self.setFixedSize(393, 55)
#         self.setText('Trip')

class DiagnosisTopCallProcedureSearch(ABCPushButton):
    def __init__(self, parent):
        super(DiagnosisTopCallProcedureSearch, self).__init__(parent)
        icon = os.path.join(ROOT_PATH, 'Img', 'search.png')
        self.setObjectName("Search")
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(25, 25))
        self.setFixedSize(468, 40)
        self.setText('비정상 절차서 검색')
        self.setContentsMargins(5, 0, 0, 0)
        # self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")  # 실행 후 호버 확인
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        print('비정상 절차서 검색 창으로 이동')
        ProcedureSearch(self).show()

class DiagnosisTopCallSystemSearch(ABCPushButton):
    def __init__(self, parent):
        super(DiagnosisTopCallSystemSearch, self).__init__(parent)
        icon = os.path.join(ROOT_PATH, 'Img', 'search.png')
        self.setObjectName("Search")
        self.setText('시스템 검색')
        # self.setStyleSheet("""QPushButton:hover {background-color: yellow;}""")  # 실행 후 호버 확인
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(25, 25))
        self.setFixedSize(468, 40)
        self.clicked.connect(self.dis_update)

    def dis_update(self):
        print('시스템 검색 창으로 이동')
        SystemSearch(self).show()
# ----------------------------------------------------------------------------------------------------------------------

class ProcedureInfo(ABCLabel):
    def __init__(self, parent):
        super(ProcedureInfo, self).__init__(parent)
        self.setObjectName("Title")
        self.setFixedHeight(40)

    def dis_update(self, procedure_name):
        self.setText(f" 비정상 절차서 이름: {procedure_name}")
# ----------------------------------------------------------------------------------------------------------------------

class ProcedureWindow(ABCWidget):
    def __init__(self, parent):
        super(ProcedureWindow, self).__init__(parent)
        # self.setStyleSheet('background-color: rgb(212, 245, 211);') # 실행 후 확인
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(ProcedureSequence(self))
        lay.addWidget(ProcedureScrollArea(self))
        lay.setSpacing(15)

class ProcedureSequence(ABCWidget):
    def __init__(self, parent):
        super(ProcedureSequence, self).__init__(parent)
        # self.setStyleSheet('background-color: rgb(212, 245, 211);') # 실행 후 확인
        self.setFixedWidth(319)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(ProcedureSequenceWidget(self, 'ProcedureSequenceTitlePu', 'ProcedureSequenceTitleCondPu', ' 1.0 ', '목적'))
        lay.addWidget(
            ProcedureSequenceWidget(self, 'ProcedureSequenceTitleAl', 'ProcedureSequenceTitleCondAl', ' 2.0 ', '경보 및 증상'))
        lay.addWidget(
            ProcedureSequenceWidget(self, 'ProcedureSequenceTitleAu', 'ProcedureSequenceTitleCondAu', ' 3.0 ', '자동 동작 사항'))
        lay.addWidget(
            ProcedureSequenceWidget(self, 'ProcedureSequenceTitleUr', 'ProcedureSequenceTitleCondUr', ' 4.0 ', '긴급 조치 사항'))
        lay.addWidget(
            ProcedureSequenceWidget(self, 'ProcedureSequenceTitleFo', 'ProcedureSequenceTitleCondFo', ' 5.0 ', '후속 조치 사항'))
        lay.setSpacing(15)
        lay.addStretch(1)

class ProcedureSequenceWidget(ABCWidget):
    def __init__(self, parent, title_w_name, title_cond_w_name, title_num, title):
        super(ProcedureSequenceWidget, self).__init__(parent)
        self.lay = QHBoxLayout(self)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(ProcedureSequenceTitleBTN(self, title_w_name, title_num, title))
        self.lay.addWidget(ProcedureSequenceTitleCond(self, title_cond_w_name, title))
        self.lay.setSpacing(15)

class ProcedureSequenceTitleBTN(ABCPushButton):
    def __init__(self, parent, widget_name='', title_num='', title=''):
        super().__init__(parent, widget_name)
        self.setObjectName("Tab")
        self.setFixedSize(264, 40)
        self.setText(title_num + title)
        self.blink = False
        self.clicked.connect(self.is_clicked)
        self.title = title

    def dis_update(self, SequenceTitleClickHis: dict):
        """상태 업데이트

        Args:
            SequenceTitleClickHis (_dict_): # {'목적': True, '경보 및 증상': False, ...}
        """
        # 0.
        self.procedure_name = self.inmem.widget_ids['Procedure'].procedure_name
        # 1. 현재 title 보다 상위 타이틀이 선택된 경우 동작
        RankList = ['목적', '경보 및 증상', '자동 동작 사항', '긴급 조치 사항', '후속 조치 사항']
        if self.title != '목적':  # 목적은 고려하지 않는다.
            ThisRank = RankList.index(self.title)
            CurrentRank = RankList.index(self.inmem.ProcedureHis[self.procedure_name]['SequenceTitleClick'])

            if ThisRank < CurrentRank:
                if self.step_check(self.title) and not self.step_all_check(self.title):
                    if not self.blink:
                        self.setStyleSheet('background-color: rgb(255, 255, 255)')
                        self.blink = True
                    else:
                        self.setStyleSheet('background-color: rgb(0, 176, 218)')
                        self.blink = False
                else:
                    self.do_hover(SequenceTitleClickHis)
                    self.blink = False
            else:
                self.do_hover(SequenceTitleClickHis)
        else:
            self.do_hover(SequenceTitleClickHis)

    def is_clicked(self):
        self.inmem.widget_ids['Procedure'].change_SequenceTitleClickHis(self.title)

    def do_hover(self, SequenceTitleClickHis):
        if SequenceTitleClickHis[self.title]:
            self.setStyleSheet("""QPushButton{background: rgb(0, 176, 218);}
                              QPushButton:hover {background: rgb(0, 176, 218);}""")
        else:
            self.setStyleSheet("""QPushButton{background: rgb(255, 255, 255);}
                                  QPushButton:hover {background: rgb(0, 176, 218);}""")

    def step_check(self, title):
        """하나라도 동작 중 이라면"""
        return any([True if cond >= 1 else False for cond in
                    self.inmem.ProcedureHis[self.procedure_name]['ContentsClickHis'][title]])

    def step_all_check(self, title):
        """모두 동작 중 이라면"""
        return all([True if cond == 1 else False for cond in
                    self.inmem.ProcedureHis[self.procedure_name]['ContentsClickHis'][title]])


class ProcedureSequenceTitleCond(ABCLabel):
    def __init__(self, parent, widget_name='', title=''):
        super().__init__(parent, widget_name)
        self.setFixedSize(40, 40)
        self.setObjectName("Check")
        self.blink = False
        self.title = title

    def dis_update(self, SequenceTitleCondHis:dict):
        """Title의 상태에 따라서 0 (진행 중), 1 (완료), 2 (병행), 3 (불만족)

        Args:
            SequenceTitleCondHis (dict): {'목적': 0, ...}
        """
        if SequenceTitleCondHis[self.title] == 0:
            self.setStyleSheet('background-color:rgb(255, 255, 255)')
        elif SequenceTitleCondHis[self.title] == 1:
            self.setStyleSheet('background-color: rgb(0,0,0)')
        elif SequenceTitleCondHis[self.title] == 2:
            if not self.blink:
                self.setStyleSheet('background-color: yellow')
                self.blink = True
            else:
                self.setStyleSheet('background-color: white')
                self.blink = False
        elif SequenceTitleCondHis[self.title] == 3:
            self.setStyleSheet('background-color: rgb(192,0,0)')
# ----------------------------------------------------------------------------------------------------------------------
# Scroll Bar 적용
class ProcedureScrollArea(ABCScrollArea):
    def __init__(self, parent):
        super(ProcedureScrollArea, self).__init__(parent)
        self.margins = QMargins(0, 0, 0, 0)    # header height
        self.setViewportMargins(self.margins)
        self.setFixedWidth(1562)

        self.scrollwidget = QWidget()
        self.scrollwidget.setObjectName("scroll")
        self.grid = QHBoxLayout(self.scrollwidget)
        self.grid.addWidget(ProcedureContents(self))
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.addStretch(1)
        self.setWidget(self.scrollwidget)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, event):
        rect = self.viewport().geometry()
        QScrollArea.resizeEvent(self, event)

class ProcedureContents(ABCWidget):
    def __init__(self, parent):
        super(ProcedureContents, self).__init__(parent)
        self.lay = QVBoxLayout(self)
        self.setObjectName("RightPG")
        self.setFixedWidth(1532)
        self.lay.setContentsMargins(0, 0, 0, 15)

    def dis_update(self, SequenceTitleClick:str, ContentsClickHis:dict, Contents:dict):
        """_summary_

        Args:
            SequenceTitleClick (str): '목적'
            ContentsClickHis (dict): '목적': [0, 0, 0, 1, ...]  # 0 (진행 중), 1 (완료), 2 (불만족)
            Contents (dict): '목적': {0: {'Des': ..., 'Nub': ..., }, ...}
        """
        self.clearLayout(self.lay)

        ContentsClickHis_inTitle: list = ContentsClickHis[SequenceTitleClick]  # [0, 0, 0, 1, ...]
        Contents_inTitle: dict = Contents[SequenceTitleClick]  # {0: {'Des': ..., 'Nub': ..., }, ...}

        self.widgets = {i: Procedure_Content(self, Contents_inTitle[i], ContentsClickHis_inTitle[i], i) for i in
                        range(len(ContentsClickHis_inTitle))}

        self.lay.addWidget(ProcedureTitleBar(self, SequenceTitleClick))
        [self.lay.addWidget(w) for w in self.widgets.values()]

        self.lay.setSpacing(15)
        self.lay.addStretch(1)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class ProcedureTitleBar(ABCWidget):
    def __init__(self, parent, title):
        super(ProcedureTitleBar, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(1, 0, 0, 0)
        title_conv = {'목적': '1.0', '경보 및 증상': '2.0', '자동 동작 사항': '3.0', '긴급 조치 사항': '4.0', '후속 조치 사항': '5.0'}
        [lay.addWidget(w) for w in [ProcedureTitleBar_1(self, title_conv[title]), ProcedureTitleBar_2(self, title)]]
        lay.setSpacing(10)

class ProcedureTitleBar_1(ABCLabel):
    def __init__(self, parent, title_conv):
        super(ProcedureTitleBar_1, self).__init__(parent)
        self.setObjectName("TitleBar")
        self.setFixedSize(120, 40)
        self.setText(title_conv)

class ProcedureTitleBar_2(ABCLabel):
    def __init__(self, parent, title):
        super(ProcedureTitleBar_2, self).__init__(parent)
        self.setObjectName("TitleBar")
        self.setFixedHeight(40)
        self.setText(title)

# ----------------------------------------------------------------------------------------------------------------------

class Procedure_Content(ABCWidget):
    def __init__(self, parent, Contents_inTitle:dict, ContentsClickHis_inTitle:int, ContentsClickHis_inTitle_index:int):
        super(Procedure_Content, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(1, 0, 10, 0) # 실행 후 확인
        lay.setAlignment(Qt.AlignRight)
        Max_FixedWidth = 0
        # label 상단 정렬 위해
        content1_lay = QHBoxLayout()
        content2_lay = QHBoxLayout()
        content1_lay.setAlignment(Qt.AlignTop)  # 실행 후 확인
        content2_lay.setAlignment(Qt.AlignTop)  # 실행 후 확인
        content1_lay.setContentsMargins(0, 0, 0, 0)
        content2_lay.setContentsMargins(0, 0, 0, 0)
        Des = Contents_inTitle['Des']
        Nub = Contents_inTitle['Nub']
        Nub_count = Nub.count('.')
        Nub_len = len(Nub)
        if Nub_count == 1:
            Max_FixedWidth = 1342
        elif Nub_count == 2:
            Max_FixedWidth = 1292
        elif Nub_count == 3:
            Max_FixedWidth = 1242
        elif Nub_count == 4:
            Max_FixedWidth = 1192

        if Nub[0] == '0': # '0.0.0' 에서 첫번째가 '0' 인 경우 주의사항 또는 참고사항
            # 주의 사항 및 참고 사항
            lay.addWidget(Procedure_Content_EM(self, Des, Max_FixedWidth))
        else:
            # 일반적 내용
            content1_lay.addWidget(Procedure_Content_Nub(self, Nub))
            lay.addLayout(content1_lay)
            lay.addWidget(Procedure_Content_Basic(self, Des, Max_FixedWidth))

        content2_lay.addWidget(Procedure_Content_Check(self, ContentsClickHis_inTitle, ContentsClickHis_inTitle_index))
        lay.addLayout(content2_lay)

        lay.setSpacing(10)


class Procedure_Content_Nub(ABCLabel):
    def __init__(self, parent, Nub):
        super(Procedure_Content_Nub, self).__init__(parent)
        self.setFixedSize(120, 40)
        self.setText(Nub)

# 참고사항 / 주의사항 label
class Procedure_Content_EM(ABCLabel):
    def __init__(self, parent, Des, Nub_len):
        super(Procedure_Content_EM, self).__init__(parent)
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
        self.setFixedWidth(Nub_len)

        self.label_title.setText("%s" % Des[:4])
        self.label_content.setText("%s" % Des[7:])

class Procedure_Content_Basic(ABCLabel):
    def __init__(self, parent, Des, Nub_len):
        super(Procedure_Content_Basic, self).__init__(parent)
        self.setWordWrap(True)
        self.setFixedWidth(Nub_len)
        self.setText(Des)


class Procedure_Content_Check(ABCPushButton):
    def __init__(self, parent, ContentsClickHis_inTitle, ContentsClickHis_inTitle_index):
        super(Procedure_Content_Check, self).__init__(parent)
        self.ContentsClickHis_inTitle = ContentsClickHis_inTitle
        self.ContentsClickHis_inTitle_index = ContentsClickHis_inTitle_index
        self.setFixedSize(40, 40)
        self.dis_update()
        self.clicked.connect(self.is_clicked)

    def dis_update(self):
        color_table = {0: 'background-color:rgb(255, 255, 255)',  # 0 (진행 중)
                       1: 'background-color: rgb(0,0,0)',  # 1 (완료)
                       2: 'background-color: rgb(192,0,0)'}  # 2 (불만족)
        self.setStyleSheet(color_table[self.ContentsClickHis_inTitle])

    def is_clicked(self):
        self.ContentsClickHis_inTitle = 0 if self.ContentsClickHis_inTitle == 2 else self.ContentsClickHis_inTitle + 1
        self.inmem.widget_ids['Procedure'].change_ContentsClickHis(self.ContentsClickHis_inTitle,
                                                                   self.ContentsClickHis_inTitle_index)
        self.dis_update()

class ProcedureBottom(ABCWidget):
    def __init__(self, parent):
        super(ProcedureBottom, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addStretch(1)
        lay.addWidget(ProcedureComplete(self))
        lay.addWidget(ProcedureParallel(self))
        lay.addWidget(ProcedureReconduct(self))
        lay.setSpacing(10)

class ProcedureComplete(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureComplete, self).__init__(parent)
        self.setFixedSize(227, 40)
        self.setObjectName("Bottom")
        self.setText('완료')
        self.clicked.connect(self.is_clicked)

    def is_clicked(self):
        self.inmem.widget_ids['Procedure'].change_SequenceTitleCondHis_then_SequenceNextTitle(1)

class ProcedureParallel(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureParallel, self).__init__(parent)
        self.setFixedSize(227, 40)
        self.setObjectName("Bottom")
        self.setText('병행')
        self.clicked.connect(self.is_clicked)

    def is_clicked(self):
        self.inmem.widget_ids['Procedure'].change_SequenceTitleCondHis_then_SequenceNextTitle(2)

class ProcedureReconduct(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(ProcedureReconduct, self).__init__(parent)
        self.setFixedSize(227, 40)
        self.setObjectName("Bottom")
        self.setText('재수행')
        self.clicked.connect(self.is_clicked)

    def is_clicked(self):
        self.inmem.widget_ids['Procedure'].clear_ContentsClickHis()


