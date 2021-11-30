import sys
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver2.Interface import Flag


class MainLeft(QWidget):
    qss = """
            QWidget {
                background: rgb(231, 231, 234);
                border: 0px solid rgb(0, 0, 0); 
                font-size: 14pt;
            }
            QTableWidget {
                background: rgb(231, 231, 234);
                border: 1px solid rgb(128, 128, 128);
            }
            QPushButton{
                background: White;
                color: Black;
                border-radius:3px;
            }
            QHeaderView::section {
                padding-left: 15px; 
                border: 0px;
            }
            QGroupBox#main  {
                border : 1px solid rgb(128, 128, 128);
                margin-top: 20px;
                margin-left:0px;
                font-size: 14pt;
            }
            QGroupBox::title#main  {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 4px 900px 4px 10px;
                background-color: rgb(128, 128, 128);
                color: black;
                font-size: 14pt;
            }
            QGroupBox#sub2_1{
                border : 1px solid rgb(128, 128, 128);
                margin: 3px;
            }
            QGroupBox#sub2_2_title  {
                border : 2px solid rgb(190,10,10);
                padding: 4px 10px 20px 10px;
                font-size: 14pt;
                background: white;
                margin-left: 20px;
                margin-right: 20px;
                margin-bottom: 10px;
            }
            QGroupBox::title#sub1  {
                subcontrol-origin: margin;
                top: 7px;
                left: 7px;
                padding: 0px 5px 0px 5px;
            }
            QLabel#sub2_1_text  {
                padding: 0px 0px 0px 180px;
                color: rgb(190,10,10);
                font-size: 14pt;
                font-weight: bold;
                background: white;
            }
            QTextEdit#text2_2 {
                color: white;
                background: rgb(190,10,10);
                border-radius:5px;
                padding: 4px 0px 0px 10px;
            }
            QTextEdit#text1 {
                color: white;
                background: rgb(82,82,82);
                border-radius:5px;
                padding: 4px 0px 0px 10px;
                margin-top:5px;
            }
            QTextEdit#text3 {
                margin-left: 20px;
                margin-right: 20px;
                margin-bottom: 10px;
                border : 2px solid rgb(82,82,82);
            }
            QTextEdit#text4 {
                border-radius:5px;
                background:white;
            }
        """
    def __init__(self, parent = None):
        super(MainLeft, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.parent = parent
        self.setStyleSheet(self.qss)
        self.setFixedWidth(560)
        # 기본 속성
        # self.setMinimumHeight(750)

        # 레이아웃
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        label1 = MainParaArea1(self.parent)
        layout.addWidget(label1)
        label2 = MainParaArea2(self.parent)
        layout.addWidget(label2)
        label3 = MainParaArea3(self.parent)
        layout.addWidget(label3)
        self.setLayout(layout)

class MainParaArea1(QTableWidget):
    def __init__(self, parent):
        super(MainParaArea1, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        # 테이블 헤더 모양 정의
        # self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)  # Grid 지우기
        self.setFixedHeight(170)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 테이블 셋업
        col_info = [('비정상 기기 및 변수', 200), ('정상 상태', 130), ('현재 상태', 130), ('Unit', 100)]
        self.setColumnCount(4)
        self.setRowCount(6)
        self.horizontalHeader().setFixedHeight(28)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setContentsMargins(0, 0, 0, 0)

        col_names = []
        for i, (l, w) in enumerate(col_info):
            self.setColumnWidth(i, w)
            col_names.append(l)

        # 테이블 헤더
        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().setStyleSheet("::section {background: rgb(128, 128, 128);font-size:14pt;border:0px solid;}")
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        # 편집 불가
        # self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.setFocusPolicy(Qt.NoFocus)
        # self.setSelectionMode(QAbstractItemView.NoSelection)

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 28)

    def paintEvent(self, e: QPaintEvent) -> None:
        """ tabelview의 위에 라인 그리기 """
        super(MainParaArea1, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        for i in range(6):
            pen.setColor(QColor(128, 128, 128))         # 가로선 -> 활성화 x color
            pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i*28, 560, i*28)
        qp.restore()
# 조치 제안
class MainParaArea2(QGroupBox):
    def __init__(self, parent):
        super(MainParaArea2, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setTitle("조치 제안")
        self.setObjectName("main")
        layout = QVBoxLayout()

        #대기 중인 Charging Pump 가동
        self.gb2 = Sub2_1(self)

        self.gb3 = Sub3_1(self)

        layout.addWidget(self.gb2)
        layout.addWidget(self.gb3)

        self.setLayout(layout)
class Sub2_1(QGroupBox):
    def __init__(self, parent):
        super(Sub2_1, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("sub2_1")
        layout = QVBoxLayout()
        self.title = QLabel("대기 중인 Charging Pump 기동")

        self.gb2_2 = Sub2_2_Title(self)
        self.gb2_2.setObjectName("sub2_2_title")

        self.text2_2 = QTextEdit("text edit~")
        self.text2_2.setObjectName("text2_2")
        layout.addWidget(self.title)
        layout.addWidget(self.gb2_2)
        layout.addWidget(self.text2_2)
        self.setLayout(layout)


class Sub2_2_Title(QGroupBox):
    def __init__(self, parent):
        super(Sub2_2_Title, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("sub2_2_title")

        layout = QVBoxLayout(self)
        self.sub2_1_text = QLabel("주의 사항")
        self.sub2_1_text.setObjectName("sub2_1_text")
        layout.addWidget(self.sub2_1_text)
        self.sub2_2_text = QTextEdit("1. 대기 중인 충전펌프의 윤활유 냉각기에 기기 냉각수가")
        self.sub2_2_text.setStyleSheet("background: white")
        layout.addWidget(self.sub2_2_text)

        self.setLayout(layout)


class Sub3_1(QGroupBox):
    def __init__(self, parent):
        super(Sub3_1, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("sub2_1")
        layout = QVBoxLayout()
        self.title = QLabel("Charging Value 개도 감소")

        self.text1 = QTextEdit("충전수 유량 제어기(BG-FK122)를 수동위치")
        self.text1.setObjectName("text1")
        self.text1.setFixedHeight(45)
        self.text2 = QTextEdit("가압기 수위를 노냉각재 평균온도에 따라 프로그램 된 수위(22～55.1%)로 유지")
        self.text2.setObjectName("text1")
        self.text2.setFixedHeight(70)
        self.text3 = QTextEdit("현재 가압기 수위 : 60 %")
        self.text3.setObjectName("text3")
        self.text3.setFixedHeight(50)
        self.text4 = QTextEdit("가압기 수위가 계속 감소 중이면 비정상-23 (원자로 냉각재 계통 누설)을  적용")
        self.text4.setObjectName("text4")
        self.text4.setFixedHeight(60)
        layout.addWidget(self.title)
        layout.addWidget(self.text1)
        layout.addWidget(self.text2)
        layout.addWidget(self.text3)
        layout.addWidget(self.text4)
        # layout.addStretch(1)
        self.setLayout(layout)

class MainParaArea3(QGroupBox):
    def __init__(self, parent):
        super(MainParaArea3, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setTitle("후속 조치")
        self.setObjectName("main")
        layout = QVBoxLayout()

        #대기 중인 Charging Pump 가동
        self.label = QTextEdit("고장난 충전펌프의 전원을 차단하고 정비 및 조치")
        self.label.setObjectName("text1")
        self.label.setFixedHeight(45)
        layout.addWidget(self.label)
        self.setLayout(layout)

class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainLeft()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()
