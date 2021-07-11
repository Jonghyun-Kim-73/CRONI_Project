import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDA_Interface_brief_ver.Thmem_qss_ver1 import qss
from AIDA_Interface_brief_ver.TOOL.TOOL_etc import p_
from AIDA_Interface_brief_ver.main_title_bar_ver1 import MainTitleBar
from AIDA_Interface_brief_ver.main_r_area_ver1 import MainRightArea
from AIDA_Interface_brief_ver.main_l_area_ver1 import MainLeftArea


class Mainwindow(QWidget):
    """메인 윈도우"""
    def __init__(self, parent, mem=None):
        super(Mainwindow, self).__init__()
        self.mem = mem
        self.up_widget = parent
        # --------------------------------------------------------------------------------------------------------------
        self.setGeometry(300, 50, 1000, 800)
        self.setStyleSheet(qss)
        self.setObjectName('Mainwindow')

        self.set_main_frame()
        # --------------------------------------------------------------------------------------------------------------
        # 프레임
        self.set_frame()

    def set_main_frame(self):
        """ 라운드 테두리 """
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def set_frame(self):
        t_h, r_w = 30, 100

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)

        self.title_bar = MainTitleBar(parent=self, h=t_h)

        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        self.r_area = MainRightArea(parent=self, h=self.height()-t_h, w=r_w)
        self.l_area = MainLeftArea(parent=self, h=self.height()-t_h, w=self.width() - r_w)

        self.vbox.addWidget(self.title_bar)
        self.hbox.addWidget(self.r_area)
        self.hbox.addWidget(self.l_area)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

    def closeEvent(self, QCloseEvent):
        p_(__file__, 'Close')
        self.up_widget.closeEvent(QCloseEvent)