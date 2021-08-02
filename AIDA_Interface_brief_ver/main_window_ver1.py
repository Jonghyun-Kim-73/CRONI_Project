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
from AIDA_Interface_brief_ver.main_sys_area_ver1 import MainSysArea
from AIDA_Interface_brief_ver.main_proce_area_ver1 import MainProceArea


class Mainwindow(QWidget):
    """메인 윈도우"""
    def __init__(self, parent, mem=None):
        super(Mainwindow, self).__init__()
        self.mem = mem
        self.up_widget = parent
        self.selected_procedure: str = ''
        # --------------------------------------------------------------------------------------------------------------
        self.setGeometry(300, 50, 1300, 800)
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
        """ 메인프레임의 세팅 """
        self.t_h, self.l_w = 35, 600  # title height, left width

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)

        self.stack_widget = QStackedLayout()
        self.stack_widget.setContentsMargins(0, 0, 0, 0)
        self.stack_widget.setSpacing(0)

        self.set_stack1()
        self.set_stack2()
        self.set_stack3()
        self.set_stack4()

        self.stack_widget.addWidget(self.pp1)
        self.stack_widget.addWidget(self.pp2)
        self.stack_widget.addWidget(self.pp3)
        self.stack_widget.addWidget(self.pp4)

        self.title_bar = MainTitleBar(parent=self, mem=self.mem, h=self.t_h, w=self.width())
        self.vbox.addWidget(self.title_bar)
        self.vbox.addLayout(self.stack_widget)

        self.setLayout(self.vbox)

    def set_stack1(self):
        """ 알람 및 절차서 진단 파트 """
        self.pp1 = QWidget()
        self.setObjectName('Stack1')
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.l_area = MainLeftArea(parent=self, h=self.height() - self.t_h, w=self.l_w, mem=self.mem)
        self.r_area = MainRightArea(parent=self, h=self.height() - self.t_h, w=self.width() - self.l_w, mem=self.mem)

        layout.addWidget(self.l_area)
        layout.addWidget(self.r_area)

        self.pp1.setLayout(layout)

    def set_stack2(self):
        """ 선택된 절차서 파트 """
        self.pp2 = QWidget()
        self.setObjectName('Stack2')
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.MainProceArea = MainProceArea(self, 0, 0, 1300, 765)

        layout.addWidget(self.MainProceArea)

        self.pp2.setLayout(layout)

    def set_stack3(self):
        """ System 미믹 및 기능 복구 파트 """
        self.pp3 = QWidget()
        self.setObjectName('Stack3')
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sys_area = MainSysArea(parent=self, h=self.height() - self.t_h, w=self.width())

        layout.addWidget(self.sys_area)

        self.pp3.setLayout(layout)

    def set_stack4(self):
        """ 예지 그래프 파트 """
        self.pp4 = QWidget()
        self.setObjectName('Stack4')
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.progWidget = QWidget()

        layout.addWidget(self.progWidget)

        self.pp4.setLayout(layout)

    def closeEvent(self, QCloseEvent):
        p_(__file__, 'Close')
        self.up_widget.closeEvent(QCloseEvent)

    def update_selected_procedure(self, procedure: str, change_panel:bool):
        self.selected_procedure = procedure
        self.title_bar.changePP.update_selected_procedure(procedure, change_panel)    # 타이틀 이름 전환 및 화면 전환
        self.MainProceArea.update_selected_procedure(procedure)
