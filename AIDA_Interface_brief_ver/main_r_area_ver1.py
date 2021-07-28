import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDA_Interface_brief_ver.TOOL.TOOL_etc import ToolEtc as T

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainRightArea(QWidget):
    """ 오른쪽 절차서 디스플레이 위젯 """
    def __init__(self, parent, h, w, mem=None):
        super(MainRightArea, self).__init__(parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainRightArea')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setFixedHeight(h)
        self.setFixedWidth(w)
        # 레이어 셋업 ---------------------------------------------------------------------------------------------------
        s, side_s = 5, 5
        self.ProcedureTable = ProcedureTable(self, x=side_s, y=side_s, w=w - side_s * 2, h=120)

    def paintEvent(self, e: QPaintEvent) -> None:
        qp = QPainter(self)
        qp.save()
        pen = QPen()
        pen.setColor(QColor(127, 127, 127))  # 가로선 -> 활성화 x color
        pen.setWidth(2)
        qp.setPen(pen)
        qp.drawRoundedRect(self.ProcedureTable.geometry(), 10, 10)
        qp.restore()


class ProcedureTable(QTableWidget):
    def __init__(self, parent, x, y, w, h):
        super(ProcedureTable, self).__init__(parent)
        self.mem = parent.mem
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setFocusPolicy(Qt.NoFocus)
        # self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setObjectName('MainRightProcedureTable')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        T.set_round_frame(self)
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        # 1. Colum 셋업
        self.col_info = [('비정상 절차서 명', 400), ('AI확신도', 145), ('진입 조건 확인', 145)] # 690
        self.setColumnCount(len(self.col_info))
        [self.setColumnWidth(i, w) for i, (l, w) in enumerate(self.col_info)]
        self.setHorizontalHeaderLabels([l for (l, w) in self.col_info])
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setFixedHeight(30)
        # 2. Row 셋업
        self.max_line = 3
        [self._add_empty_line(i) for i in range(self.max_line)]
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalScrollBar().setSingleStep(self.rowHeight(0))  # Click 시 이동하는 거리
        self.verticalScrollBar().setStyleSheet("""
                    QScrollBar:vertical{
                        border: none;
                        background: rgb(127, 127, 127);                 /* 활성화 x */
                        margin: 20 0 20 0;
                    }
                    QScrollBar::handle:vertical{
                        background: rgb(38, 55, 96);                    /* 활성화 o */
                    }
                    QScrollBar::sub-line:vertical{
                        background: rgb(38, 55, 96);                    /* 활성화 o */
                        height: 20;
                        border-image: url(./interface_image/U_arrow.svg);
                        subcontrol-position: top;
                        subcontrol-origin: margin;
                    }
                    QScrollBar::add-line:vertical{
                        background: rgb(38, 55, 96);                    /* 활성화 o */
                        height: 20;
                        border-image: url(./interface_image/D_arrow.svg);
                        subcontrol-position: bottom;
                        subcontrol-origin: margin;
                    }
                    """)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)  # Grid 지우기
        # display update -----------------------------------------------------------------------------------------------
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self._update_procedure_display)
        timer.start()
    # ==================================================================================================================
    # 함수 Overwrite

    def paintEvent(self, e: QPaintEvent) -> None:
        """ tabelview의 위에 라인 그리기 """
        super(ProcedureTable, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        for i in range(self.max_line):
            pen.setColor(QColor(127, 127, 127))  # 가로선 -> 활성화 x color
            pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i * 30, self.viewport().width(), i * 30)
        qp.restore()

    # ==================================================================================================================
    # Private functions

    def _add_empty_line(self, i):
        self.insertRow(i)
        self.setCellWidget(i, 0, ProcedureItemInfo(self, type='Name'))
        self.setCellWidget(i, 1, ProcedureItemInfo(self, type='Prob'))
        self.setCellWidget(i, 2, ProcedureItemInfo(self, type='Match'))

    def _update_procedure_display(self):
        """ AI 모듈에서 계산된 정보 업데이트"""
        ab_dig_result = self.mem.get_logic('Ab_Dig_Result')

        test_procedure_des = {
            0: 'Ab63_02: 제어봉의 계속적인 삽입',
            1: 'Ab21_01: 가압기 압력 채널 고장 (고)',
            2: 'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설',
        }
        test_procedure_prob = {
            0: 85,
            1: 15,
            2: 5,
        }
        test_procedure_match = {
            0: {'Tot': 10, 'Match': 9},
            1: {'Tot': 15, 'Match': 3},
            2: {'Tot': 7, 'Match': 2},
        }
        for i in range(self.rowCount()):
            self.cellWidget(i, 0).dis_update(test_procedure_des[i])
            self.cellWidget(i, 1).dis_update(test_procedure_prob[i])
            self.cellWidget(i, 2).dis_update(test_procedure_match[i])


class ProcedureItemInfo(QWidget):
    """ ProcedureTable 의 Item """
    def __init__(self, parent, type):
        super(ProcedureItemInfo, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setObjectName('ProcedureItemInfo')

        layer = QVBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)
        layer.setSpacing(0)

        self._type = type
        if self._type == 'Name' or self._type == 'Match':
            self.label = QLabel()
            layer.addWidget(self.label)
        if self._type == 'Prob':
            self.progress = ProbProgressBar(self)
            layer.addWidget(self.progress)
        self.setLayout(layer)
    # ==================================================================================================================
    # Public functions

    def dis_update(self, _info):
        """ 정보 디스플레이 업데이트 """
        if self._type == 'Name':
            self.label.setText(' ' + str(_info))
        elif self._type == 'Match':
            self.label.setText(f'{_info["Tot"]} / {_info["Match"]}')
            self.label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 정렬
        elif self._type == 'Prob':
            self.progress.setValue(_info)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        super(ProcedureItemInfo, self).mousePressEvent(ev)


class ProbProgressBar(QProgressBar):

    # TODO  여기서 07-29
    def __init__(self, parent):
        super(ProbProgressBar, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setObjectName('Prob')

    def mousePressEvent(self, *args, **kwargs):
        print('Clicked Progressbar')
        print(self.geometry())
        print(self.rect())
        super(ProbProgressBar, self).mousePressEvent(*args, **kwargs)

    def setValue(self, p_int):
        super(ProbProgressBar, self).setValue(p_int)