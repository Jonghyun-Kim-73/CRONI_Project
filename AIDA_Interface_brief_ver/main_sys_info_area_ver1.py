import os
import sys
import math
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import QGraphicsSvgItem

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainSysArea(QWidget):
    """ 시스템 디스플레이 위젯 """
    def __init__(self, parent, h, w):
        super(MainSysArea, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setObjectName('MainSysArea')
        # --------------------------------------------------------------------------------------------------------------
        self.setFixedHeight(h)
        self.setFixedWidth(w)

        # --------------------------------------------------------------------------------------------------------------
        self.shortcut_F2 = QShortcut(QKeySequence('F2'), self)
        self.shortcut_F2.activated.connect(self._shortcut_F2)
        self._F2_label = QLabel('N', self)
        self._F2_label.setGeometry(0, 0, 15, 15)
        self._F2_mode = False

        self._make_line = False
        self._make_line_pos = None

        self.w_info = {'l': {}, 's': {}}
        self._line_nub = 0              # 새롭게 그려지는 Line
        self._line_move_nub = -1        # 라인이 선택된 경우
        self._line_move_pos = None      # 라인이 선택된 경우 마우스 위치
        self._line_move_side = 'N'       # 라인이 선택된 경우 길이 조정인지
        self._svg_nub = 0

    def _shortcut_F2(self):
        """ shortcut_F2: 수정모드 """
        if self._F2_mode:
            self._F2_label.setText('N')
            self._F2_mode = False
        else:
            self._F2_label.setText('E')
            self._F2_mode = True

    def contextMenuEvent(self, event) -> None:
        menu = QMenu(self)
        add_line = menu.addAction("Add Line")
        add_svg = menu.addAction("Add Svg")
        add_line.triggered.connect(lambda a, pos=event.pos(): self._line_make(pos))
        add_svg.triggered.connect(lambda a, pos=event.pos(): self._svg_make(pos))

        # Add -------------------------------------------------------------------------------------
        lc, i, s = self._line_check_fun(event.pos())  # 선 이동 or 길이 변환에 대한 정보얻음
        if lc is not None:
            if i < 2:
                add_changeLine = menu.addAction("ChangeLine")
                add_changeLine.triggered.connect(lambda a, lc=lc, g_pos=event.globalPos(): self._line_change_info(lc, g_pos))

        menu.exec_(event.globalPos())

    # - Line -----------------------------------------------------------------------------------------------------------
    def _line_make(self, pos):
        self._make_line = True
        self._make_line_pos = pos

    def _line_check_fun(self, pos):
        """ 선택된 위치와 가장 가까운 선 반환 -> 선택된 선에서 오른쪽 왼쪽 길이 수정인지 판단 """
        d_ = None
        pos_ = None
        for i in self.w_info['l']:
            obj = self.w_info['l'][i]
            a = - (obj.y2() - obj.y1())/(obj.x2() - obj.x1())
            c = - obj.y1() + obj.x1() * ((obj.y2() - obj.y1())/(obj.x2() - obj.x1()))
            sq = a**2 + 1
            d = abs(a*pos.x() + 1*pos.y() + c) / math.sqrt(sq)
            if d_ is None:
                d_ = d
                pos_ = i
            elif d_ > d:
                d_ = d
                pos_ = i
            else:
                pass
        # --------------------------------------------------------------------------------------------------------------
        # 선 길이 수정 or 이동
        side = 'N'
        if pos_ != None:
            obj = self.w_info['l'][pos_]
            p1_d = math.sqrt((obj.x1() - pos.x())**2 + (obj.y1() - pos.y())**2)
            p2_d = math.sqrt((obj.x2() - pos.x())**2 + (obj.y2() - pos.y())**2)
            if p1_d < 2:
                side = 'P1'
            if p2_d < 2:
                side = 'P2'

        return pos_, d_, side

    def _line_change_info(self, lc, g_pos):
        self._line_info = [self.w_info['l'][lc].x1(), self.w_info['l'][lc].x2(),
                           self.w_info['l'][lc].y1(), self.w_info['l'][lc].y2()]
        _ = InfoLine(self, g_pos)
        _.exec_()
        _.show()

        self.w_info['l'][lc] = QLine(self._line_info[0], self._line_info[2], self._line_info[1], self._line_info[3])

    def eventFilter(self, obj, event) -> bool:
        if event.type() == QEvent.MouseMove:
            if event.buttons() == Qt.NoButton and self._make_line:
                self.w_info['l'][self._line_nub] = QLine(self._make_line_pos.x(), self._make_line_pos.y(), event.x(), event.y())
                self.update()
            if event.buttons() == Qt.LeftButton and self._line_move_nub != -1:
                _l = self.w_info['l'][self._line_move_nub]
                diff = event.pos() - self._line_move_pos

                if self._line_move_side == 'P1' or self._line_move_side == 'N':
                    _l.setP1(_l.p1() + diff)
                if self._line_move_side == 'P2' or self._line_move_side == 'N':
                    _l.setP2(_l.p2() + diff)

                self._line_move_pos = event.pos()
                self.update()

        if event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton:
            if self._make_line:    # 오른쪽 누르면
                self._make_line = False
                self._line_nub += 1
            else:
                if self._line_move_nub == -1:
                    lc, i, s = self._line_check_fun(event.pos()) # 선 이동 or 길이 변환에 대한 정보얻음
                    if lc is not None:
                        if i < 2:
                            self._line_move_nub = lc
                            self._line_move_pos = event.pos()
                            self._line_move_side = s

        if event.type() == QEvent.MouseButtonRelease:
            # 라인 관련 초기화
            self._line_move_nub = -1
            self._line_move_pos = None
            self._line_move_side = 'N'

        return QWidget.eventFilter(self, obj, event)

    def paintEvent(self, event) -> None:
        print('Call paintEvent')
        pen = QPen()
        brush = QBrush(Qt.darkCyan, Qt.Dense7Pattern)
        painter = QPainter(self)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)

        for key in self.w_info['l']:
            painter.drawLine(self.w_info['l'][key])


class InfoLine(QDialog):
    def __init__(self, parent, g_pos):
        super(InfoLine, self).__init__(parent)
        self.setGeometry(g_pos.x(), g_pos.y(), 200, 200)

        vl = QVBoxLayout()
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(0)

        hv1 = QHBoxLayout()
        lx1 = QLabel('x1', self)
        self.ex1 = QLineEdit(self)
        self.ex1.setText(f'{self.parent()._line_info[0]}')
        lx2 = QLabel('x2', self)
        self.ex2 = QLineEdit(self)
        self.ex2.setText(f'{self.parent()._line_info[1]}')
        hv1.addWidget(lx1)
        hv1.addWidget(self.ex1)
        hv1.addWidget(lx2)
        hv1.addWidget(self.ex2)

        hv2 = QHBoxLayout()
        ly1 = QLabel('y1', self)
        self.ey1 = QLineEdit(self)
        self.ey1.setText(f'{self.parent()._line_info[2]}')
        ly2 = QLabel('y2', self)
        self.ey2 = QLineEdit(self)
        self.ey2.setText(f'{self.parent()._line_info[3]}')
        hv2.addWidget(ly1)
        hv2.addWidget(self.ey1)
        hv2.addWidget(ly2)
        hv2.addWidget(self.ey2)

        hv3 = QHBoxLayout()
        self.ok_btn = QPushButton('Ok', self)
        self.ok_btn.clicked.connect(self.ok)
        self.can_btn = QPushButton('Cancer', self)
        self.can_btn.clicked.connect(self.can)
        hv3.addWidget(self.ok_btn)
        hv3.addWidget(self.can_btn)

        vl.addLayout(hv1)
        vl.addLayout(hv2)
        vl.addLayout(hv3)

        self.setLayout(vl)

    def ok(self):
        self.parent()._line_info = [int(self.ex1.text()),
                                    int(self.ex2.text()),
                                    int(self.ey1.text()),
                                    int(self.ey2.text())]
        self.close()

    def can(self):
        self.close()
