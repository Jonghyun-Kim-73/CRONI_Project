import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDA_Interface_brief_ver.main_title_bar import MainTitleBar

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class Mainwindow(QWidget):
    """메인 윈도우"""
    qss = """
        QWidget {
            background: rgb(14, 22, 24);
        }
    """

    def __init__(self, parnet):
        super(Mainwindow, self).__init__()
        self.top_window = parnet
        # --------------------------------------------------------------------------------------------------------------
        self.setGeometry(300, 300, 800, 700)    # initial window size
        self.setStyleSheet(self.qss)
        self.setObjectName('MainWin')

        # Main 프레임 모양 정의
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        # Main 프레임 특징 정의
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)   # 프레임 날리고 | 창은 항상 위
        self.setWindowOpacity(0.95)                                              # 프레임 투명도

        # 레이아웃과 타이틀바 위젯 생성
        window_vbox = QVBoxLayout(self)
        window_vbox.setContentsMargins(0, 0, 0, 0)

        titlebar_widget = MainTitleBar(self)

        content_vbox = QVBoxLayout()
        content_vbox.setContentsMargins(0, 0, 0, 0)

        # 타이틀바와 컨텐츠 박스 안의 내용물을 생성
        content_textedit = QTextEdit()

        # 각 항목을 레이아웃에 배치
        content_vbox.addWidget(content_textedit)

        window_vbox.addWidget(titlebar_widget)
        window_vbox.addLayout(content_vbox)


if __name__ == '__main__':
    print('test')
    app = QApplication(sys.argv)
    window = Mainwindow(None)
    window.show()
    app.exec_()