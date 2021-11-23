import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from AIDAA_Ver2.Interface import Flag
from AIDAA_Ver2.Interface.main.main_left import MainLeft
from AIDAA_Ver2.Interface.main.main_right import MainRight
from AIDAA_Ver2.Interface.main.main_top import MainTop


class Mainwindow(QWidget):
    """메인 윈도우"""
    qss = """
            QWidget {
                background: rgb(128, 128, 128);
            }

        """
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__()
        # self.shmem = parent.shmem   # <- myform.shmem
        self.W_myform = parent
        self.selected_procedure: str = ''
        # --------------------------------------------------------------------------------------------------------------
        # self.setGeometry(300, 50, 200, 200)
        # --------------------------------------------------------------------------------------------------------------
        # 프레임

        # Main 기본 속성
        self.setGeometry(0, 0, 1920, 1010)
        self.setStyleSheet(self.qss)
        # self.setWindowOpacity(0.95)  # 프레임 투명도

        # 레이아웃 설정
        window_vbox = QVBoxLayout(self)  # 세로 방향 레이아웃
        window_vbox.setContentsMargins(0, 0, 0, 0)  # 여백
        window_vbox.setSpacing(0)  # 각 객체 사이의 여백

        # 타이틀바 위젯
        self.BB = MainTop(self)
        # 하단 섹션
        content_hbox = QHBoxLayout(self)
        # 왼쪽
        self.GG = MainLeft(self)
        # 오른쪽
        self.DD = MainRight(self)

        # 각 항목을 레이아웃에 배치
        content_hbox.addWidget(self.GG)
        content_hbox.addWidget(self.DD)
        window_vbox.addWidget(self.BB)
        window_vbox.addLayout(content_hbox)

        self.setLayout(window_vbox)
        self.showMaximized()

    def set_frame(self):
        """ 메인프레임의 세팅 """
        pass

    def paintEvent(self, e):
        if Flag.main_close:
            Flag.main_close = False
            self.close()
    # def closeEvent(self, QCloseEvent):
    #     p_(__file__, 'Close')
    #     self.W_myform.closeEvent(QCloseEvent)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = Mainwindow()
    window.show()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    app.exec_()