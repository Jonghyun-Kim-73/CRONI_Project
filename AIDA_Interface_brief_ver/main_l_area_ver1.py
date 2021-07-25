import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainLeftArea(QWidget):
    """ 왼쪽 알람 디스플레이 위젯 """
    def __init__(self, parent, h, w, mem=None):
        super(MainLeftArea, self).__init__(parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainLeftArea')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setFixedHeight(h)
        self.setFixedWidth(w)
        # 레이어 셋업 ---------------------------------------------------------------------------------------------------
        sp_h, s, side_s = 30, 5, 5
        # 1. 알람 Table
        self.AlarmTable = AlarmTable(self, x=side_s, y=side_s, w=w-side_s*2, h=h-(side_s*2+s+sp_h), mem=self.mem)
        # 2. Subpress Btn
        self.SubPressBtm = SupPresBtn(self, x=side_s, y=h-sp_h-side_s, w=w-side_s*2, h=sp_h, mem=self.mem)


class AlarmTable(QTableWidget):
    def __init__(self, parent, x=0, y=0, w=0, h=0, mem=None):
        super(AlarmTable, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainLeftAlarmTable')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        self._set_frame()
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        # 1. Column 셋업
        col_info = [('경보명', 280), ('현재값', 50), ('설정치', 50), ('Unit', 10), ('발생시간', 100), ('경보절차서', 0)]
        self.setColumnCount(len(col_info))
        [self.setColumnWidth(i, w) for i, (l, w) in enumerate(col_info)]
        self.setHorizontalHeaderLabels([l for (l, w) in col_info])
        self.horizontalHeader().setStretchLastSection(True)
        # 2. Row 셋업
        # TODO 여기서

    def _set_frame(self):
        """ 라운드 테두리 """
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)


class SupPresBtn(QPushButton):
    def __init__(self, parent, x=0, y=0, w=0, h=0, mem=None):
        super(SupPresBtn, self).__init__(parent=parent)
        self.mem = mem
        self._AlarmTable:QTableWidget = self.parent().AlarmTable
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainLeftSupPresBtn')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        self._set_frame()
        # 레이어 셋업 ---------------------------------------------------------------------------------------------------
        self.setText('Suppression Button')

    def _set_frame(self):
        """ 라운드 테두리 """
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def mousePressEvent(self, *args, **kwargs):
        """ Btn 클릭 시 -> AlarmTable clear"""
        self._AlarmTable.clear()
        super(SupPresBtn, self).mousePressEvent(*args, **kwargs)