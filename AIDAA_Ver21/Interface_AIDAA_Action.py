from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_AIDAA_ActionMimic import *
from AIDAA_Ver21.Interface_ABCWidget import *

class Action(ABCWidget):
    """ Action 미믹 화면 섹션
    
    Action의 구조는
    1. Diagnosis Table에서 또는 System Search 에서 온 System Name을 트리거로 하여 동작한다.
    2. System Name은 ActionTitleLabel의 Title을 바꾸고 ActionMimicArea은 Title 값에 기반하여 화면이 전환된다.
    3. ActionMimicArea는 알람 정보, 자동 조치 사항, 조치 제안의 내용을 포함하고 있어 
       ActionAlarmArea와 ActionSuggestionArea는 ActionMimicArea가 바꾼다.
       
    * Action Architecture   
    
    [*DiagnosisTable] ┬─> [ActionTitleLabel] ─> [**ActionMimicArea] ┬> [ActionAlarmArea]
    [*SystemSearch  ] ┘                                             └> [ActionSuggestion]

    """
    def __init__(self, parent):
        super(Action, self).__init__(parent)
        lay = QGridLayout(self)
        """
        [    1    ]
        [ 2 ]|[ 4 ]
        [ 3 ]|[ 4 ]
        """
        lay.addWidget(ActionTitleLabel(self),       0, 0, 1, 2)   # 1
        lay.addWidget(ActionAlarmArea(self),        1, 0, 1, 1)   # 2
        lay.addWidget(ActionSuggestionArea(self),   2, 0, 1, 1)   # 3
        lay.addWidget(ActionMimicArea(self),        1, 1, 2, 1)   # 4
class ActionTitleLabel(ABCLabel):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.update_text('화학 및 체적 제어계통')
        
    def update_text(self, sys_name):
        self.setText(sys_name)
# ----------------------------------------------------------------------------------------------------------------------
class ActionAlarmArea(ABCScrollArea):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.heading_height = 40
        self.setFixedWidth(800)
        
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(self.widget_name)
        return super().mousePressEvent(a0)
    
    def resizeEvent(self, a0: QResizeEvent) -> None:
        # resize 된 이후 수행
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay_heading = QHBoxLayout()
        lay_heading.setContentsMargins(0, 0, 0, 0)
        lay_heading.setSpacing(0)
        
        lay.addLayout(lay_heading)

        col_info = {'경보':self.size().width() - 490, '정상 상태': 140, '현재 상태': 140, '단위': 80, '시간': 130}

        lay_heading.addWidget(ActionAlarmAreaTableHeadingLabel(self, '경보', col_info['경보'], self.heading_height, 'F'))
        lay_heading.addWidget(ActionAlarmAreaTableHeadingLabel(self, '정상 상태', col_info['정상 상태'], self.heading_height, 'M'))
        lay_heading.addWidget(ActionAlarmAreaTableHeadingLabel(self, '현재 상태', col_info['현재 상태'], self.heading_height, 'M'))
        lay_heading.addWidget(ActionAlarmAreaTableHeadingLabel(self, '단위', col_info['단위'], self.heading_height, 'M'))
        lay_heading.addWidget(ActionAlarmAreaTableHeadingLabel(self, '시간', col_info['시간'], self.heading_height, 'L'))
        
        lay.addWidget(ActionAlarmAreaTable(self, col_info))
        lay.addSpacing(1)

        return super().resizeEvent(a0)
class ActionAlarmAreaTableHeadingLabel(ABCLabel):
    def __init__(self, parent, text, fix_width, fix_height, pos, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
        self.setFixedWidth(fix_width)
        self.setFixedHeight(fix_height)
        self.setProperty('Pos', pos)
        self.style().polish(self)    
class ActionAlarmAreaTable(ABCTableWidget):
    def __init__(self, parent, col_info:dict, widget_name=''):
        super().__init__(parent, widget_name)
        self.setRowCount(5)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setShowGrid(False)  # Grid 지우기
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.horizontalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
        self.setColumnCount(len(col_info))
        
        for i, (l, w) in enumerate(col_info.items()):
            self.setColumnWidth(i, w)

        self.alarm_line = {
            i: [ActionAlarmAreaTableItem(self, 'F'),
                ActionAlarmAreaTableItem(self, 'M'),
                ActionAlarmAreaTableChangedItem(self),
                ActionAlarmAreaTableItem(self, 'M'),
                ActionAlarmAreaTableItem(self, 'L')] for i in range(self.rowCount())
        }

        for i in range(self.rowCount()):
            for j, item in enumerate(self.alarm_line[i]):
                self.setCellWidget(i, j, item)

        # self.setCellWidget(1, 0, ActionAlarmAreaTableItem(self, 'VCT level lo', 'F'))
        # self.setCellWidget(1, 1, ActionAlarmAreaTableItem(self, '20~80', 'M'))
        # self.setCellWidget(1, 2, ActionAlarmAreaTableChangedItem(self, 'ZVCT'))
        # self.setCellWidget(1, 3, ActionAlarmAreaTableItem(self, '[%]', 'M'))
        # self.setCellWidget(1, 4, ActionAlarmAreaTableItem(self, '00:00:15', 'L'))
        
        [self.setRowHeight(i, 40) for i in range(self.rowCount())] # 테이블 행 높이 조절
        self.startTimer(1200)
    def timerEvent(self, event: QTimerEvent) -> None:
        # 1. 현재 발생한 알람 확인
        for alarm_para in ['A_ZVCT', 'A_PVCT', 'A_ZINST65', 'A_ZPRZNOAVGNO']:
            alarm_level = self.inmem.ShMem.get_CVCS_para_val(alarm_para)
        return super().timerEvent(event)
class ActionAlarmAreaTableItem(ABCLabel):
    def __init__(self, parent, pos, widget_name=''):
        super().__init__(parent, widget_name)
        self.setProperty('Pos', pos)
        self.style().polish(self)
        self.setText('')
class ActionAlarmAreaTableChangedItem(ABCLabel):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
    def update(self, para):
        _ = self.setText(f'{self.inmem.ShMem.get_CVCS_para_val(para):.2f}') if para.para != '' else self.setText('')
# ----------------------------------------------------------------------------------------------------------------------
class ActionSuggestionArea(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(840)
        self.setFixedWidth(self.inmem.widget_ids['ActionAlarmArea'].width() + 30) # 스트롤바 마진 30
        self.heading_height = 40
    
    def resizeEvent(self, a0: QResizeEvent) -> None:
        # resize 된 이후 수행
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)     
        lay.setSpacing(0)
        lay_heading = QHBoxLayout()
        lay_heading.setContentsMargins(0, 0, 30, 0) # 스트롤바 마진 30
        lay_heading.setSpacing(0)
        
        lay.addLayout(lay_heading)

        self.col_info = {'조치 제안':self.size().width() - 60, '상태': 60}

        lay_heading.addWidget(ActionAlarmAreaTableHeadingLabel(self, '조치 제안', self.col_info['조치 제안'], self.heading_height, 'F'))
        lay_heading.addWidget(ActionAlarmAreaTableHeadingLabel(self, '상태', self.col_info['상태'], self.heading_height, 'L'))
        lay.addWidget(ActionSuggestionAreaScroll(self))
        return super().resizeEvent(a0)
class ActionSuggestionAreaScroll(ABCScrollArea):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.w = QWidget()
        self.w.setObjectName('ActionSuggestionAreaScrollW')
        lay = QHBoxLayout(self.w)
        lay.setContentsMargins(0, 0, 10, 0)
        lay.addWidget(ActionSuggestionAreaTable(self))
        self.setWidget(self.w)
class ActionSuggestionAreaTableHeadingLabel(ABCLabel):
    def __init__(self, parent, text, fix_width, fix_height, pos, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
        self.setFixedWidth(fix_width)
        self.setFixedHeight(fix_height)
        self.setProperty('Pos', pos)
        self.style().polish(self)
class ActionSuggestionAreaTable(ABCWidget):
    def __init__(self, parent, widget_name=''):
        """ActionSuggestionArea

        SuggestionActionHis 에 발생 시간 별로 위젯 블럭이 추가되고 제거됨.
        """
        super().__init__(parent, widget_name)
        self.col_info = self.inmem.widget_ids['ActionSuggestionArea'].col_info
        self.SuggestionActionHis = {}

        self.vl = QVBoxLayout(self)
        self.vl.setContentsMargins(0, 10, 0, 0)
        self.vl.setSpacing(20)
    
    # def add_suggestion_action(self):
        self.vl.addWidget(ActionSuggestionAreaItem(self, 0, 'G1: 가압기 수위', 'False', 'Abnormal'))
        self.vl.addWidget(ActionSuggestionAreaItem(self, 1, 'F1: Letdown 유로 확보', 'False', 'Abnormal'))
        self.vl.addWidget(ActionSuggestionAreaItem(self, 2, 'A1.1.1: Letdown LV459 Open', 'False', 'AutoRun'))
        self.vl.addWidget(ActionSuggestionAreaItem(self, 2, 'A1.1.2: Letdown Flow', 'False', 'Abnormal'))
        self.vl.addWidget(ActionSuggestionAreaItem(self, 2, 'A1.2.1: Letdown Excess Valve', 'True', 'Stop'))
        self.vl.addWidget(ActionSuggestionAreaItem(self, 2, 'A1.2.2: Letdown Excess Flow', 'True', 'Stop'))
        self.vl.addWidget(ActionSuggestionAreaItem(self, 1, 'F2: Charging 유로 확보', 'False', 'AutoRun'))
        self.vl.addWidget(ActionSuggestionAreaItem(self, 2, 'A2.1.1: Charging Pump 1', 'False', 'AutoRun'))
        self.vl.addWidget(ActionSuggestionAreaItem(self, 2, 'A2.1.2: Charging Pump 2', 'False', 'Stop'))
        self.vl.addWidget(ActionSuggestionAreaItem(self, 2, 'A2.1.3: Charging Valve', 'False', 'AutoRun'))
        self.vl.addWidget(ActionSuggestionAreaItem(self, 2, 'A2.1.4: Charging Flow', 'False', 'AutoRun'))
        self.vl.addStretch(1)
class ActionSuggestionAreaItem(ABCWidget):
    def __init__(self, parent, level, text, activate, check_cond, widget_name=''):
        super().__init__(parent, widget_name)
        start_point = {0:730, 1:700, 2:670}[level] # 라인의 시작지점 셋팅
        self.hl = QHBoxLayout(self)
        self.hl.setContentsMargins(0, 0, 0, 0)
        self.hl.addStretch(1)
        self.hl.addWidget(ActionSuggestionAreaItemContent(self, start_point, text, activate))
        self.hl.addSpacing(10)
        self.hl.addWidget(ActionSuggestionAreaItemCheckBox(self, check_cond))
        self.hl.addSpacing(10)
class ActionSuggestionAreaItemContent(ABCLabel):
    def __init__(self, parent, fix_width, text, activate, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedHeight(40)
        self.setFixedWidth(fix_width)
        self.setText(text)
        self.setProperty('Activate', activate)
        self.style().polish(self)
class ActionSuggestionAreaItemCheckBox(ABCLabel):
    def __init__(self, parent, check_cond, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedHeight(40)
        self.setFixedWidth(40)
        self.setProperty('Condition', check_cond)
        self.style().polish(self)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if self.property('Condition') == 'AutoRun' or self.property('Condition') == 'ManRun':
            self.update_cond('ManRun' if self.property('Condition') == 'AutoRun' else 'AutoRun')
        return super().mousePressEvent(a0)
    
    def update_cond(self, cond):
        self.setProperty('Condition', cond)
        self.style().polish(self)