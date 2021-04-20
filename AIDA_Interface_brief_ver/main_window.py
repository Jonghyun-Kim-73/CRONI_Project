import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDA_Interface_brief_ver.main_title_bar import MainTitleBar
from AIDA_Interface_brief_ver.main_left_alarm_area import MainLeftAlarmArea
from AIDA_Interface_brief_ver.main_center_procedure_area import MainCenterProcedureArea
from AIDA_Interface_brief_ver.main_right_digprog_area import MainRightDiagnosisProgArea


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

from AIDA_Interface_brief_ver.Thmem_qss import qss


class Mainwindow(QWidget):
    """메인 윈도우"""
    def __init__(self, parnet):
        super(Mainwindow, self).__init__()
        self.top_window = parnet
        # --------------------------------------------------------------------------------------------------------------
        self.setGeometry(300, 300, 1200, 700)    # initial window size
        self.setStyleSheet(qss)
        self.setObjectName('MainWin')

        # Main 프레임 모양 정의
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        # Main 프레임 특징 정의
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)   # 프레임 날리고 | 창은 항상 위
        self.setWindowOpacity(0.99)                                             # 프레임 투명도

        # 레이아웃과 타이틀바 위젯 생성
        window_vbox = QVBoxLayout()
        window_vbox.setContentsMargins(0, 0, 0, 0)
        window_vbox.setSpacing(0)
        titlebar_widget = MainTitleBar(self)

        # 1] 하단 섹션
        content_hbox = QHBoxLayout()
        content_hbox.setContentsMargins(5, 5, 5, 5)
        content_hbox.setSpacing(0)
        # 1.1] 왼족 알람 섹션
        self.alarm_area = MainLeftAlarmArea(self)

        # 1.2] 가운데 진단 영역
        self.procedure_area = MainCenterProcedureArea(self)

        # 1.3] 오른쪽 절차서 진단 및 예지 섹션
        self.diagnosis_prog_area = MainRightDiagnosisProgArea(self)

        # 각 항목을 레이아웃에 배치
        content_hbox.addWidget(self.alarm_area)
        content_hbox.addWidget(self.procedure_area)
        # content_hbox.addWidget(self.diagnosis_prog_area)

        window_vbox.addWidget(titlebar_widget)
        window_vbox.addLayout(content_hbox)

        self.setLayout(window_vbox)
        self.setContentsMargins(0, 0, 0, 0)


if __name__ == '__main__':
    print('test')
    app = QApplication(sys.argv)
    window = Mainwindow(None)
    window.show()
    app.exec_()