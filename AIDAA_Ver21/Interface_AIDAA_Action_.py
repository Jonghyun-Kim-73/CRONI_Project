from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
import pandas as pd
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
# from AIDAA_Ver21.Interface_AIDAA_Action_System_Mimic import *
# from AIDAA_Ver21.Interface_AIDAA_Action_alarm_area import *


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
        lay.addWidget(ActionTitleLabel(self), 0, 0, 1, 0)  # 1
        lay.addWidget(ActionAlarmArea(self), 2, 0)   # 2
        # lay.addWidget(ActionAlarmArea(self), 2, 0, 0, 0)   # 3
        # lay.addWidget(ActionAlarmArea(self), 1, 1, 2, 0)   # 4
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

        col_info = {'경보':300, '정상 상태': 200, '현재 상태': 200, '시간':self.size().width() - 700}

        lay_heading.addWidget(ActionAlarmAreaTableHeadingLabel(self, '경보', col_info['경보'], self.heading_height, 'F'))
        lay_heading.addWidget(ActionAlarmAreaTableHeadingLabel(self, '정상 상태', col_info['정상 상태'], self.heading_height, 'M'))
        lay_heading.addWidget(ActionAlarmAreaTableHeadingLabel(self, '현재 상태', col_info['현재 상태'], self.heading_height, 'M'))
        lay_heading.addWidget(ActionAlarmAreaTableHeadingLabel(self, '시간', col_info['시간'], self.heading_height, 'L'))
        
        lay.addWidget(ActionAlarmAreaTable(self, col_info))

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
            
        self.setSortingEnabled(True)  # 테이블 sorting

        [self.setRowHeight(i, 40) for i in range(self.rowCount())] # 테이블 행 높이 조절
# ----------------------------------------------------------------------------------------------------------------------
class ActionSuggestion(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)