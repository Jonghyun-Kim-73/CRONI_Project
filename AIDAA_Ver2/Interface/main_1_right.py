import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver2.Interface import Flag


class Main1Right(QWidget):
    qss = """
        QWidget {
            background: rgb(231, 231, 234);
            border: 0px solid rgb(0, 0, 0); 
            font-size: 14pt;
            border-radius: 6px;
        }
        QTableWidget {
            background: rgb(231, 231, 234);
            border: 1px solid rgb(128,128,128);
            border-radius: 6px;
        }
        QHeaderView::section {
            padding-left: 15px; 
            border: 0px;
        }
        QPushButton{
            background: White;
            color: Black;
            border-radius:3px;
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
        QGroupBox#sub1  {
            border : 1px solid rgb(128, 128, 128);
            margin-top:20px;
            font-size: 14pt;
        }
        QGroupBox::title#sub1  {
            subcontrol-origin: margin;
            top: 7px;
            left: 7px;
            padding: 0px 5px 0px 5px;
        }
        QLabel#sub2  {
            margin-top: 3px;
            padding: 5px 0px 0px 0px;
        }
    """

    def __init__(self, parent=None):
        super(Main1Right, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.parent = parent
        self.setStyleSheet(self.qss)
        # self.setFixedWidth(990)
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
        col_info = [('비정상 절차서 명', 340), ('긴급 여부', 210), ('진입 조건', 210), ('AI 확신도', 200)]
        self.setColumnCount(4)
        self.setRowCount(5)
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

    def mousePressEvent(self, *args, **kwargs):
        print('Test 절차서 선택 시 화면 전환')
        Flag.call_prss = True
        super(MainParaArea1, self).mousePressEvent(*args, **kwargs)

    def paintEvent(self, e: QPaintEvent) -> None:
        """ tabelview의 위에 라인 그리기 """
        super(MainParaArea1, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        for i in range(5):
            pen.setColor(QColor(128, 128, 128))         # 가로선 -> 활성화 x color
            pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i*28, 960, i*28)
        qp.restore()


class MainParaArea2(QTableWidget):
    def __init__(self, parent):
        super(MainParaArea2, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        # 테이블 헤더 모양 정의
        # self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)  # Grid 지우기
        self.setFixedHeight(170)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 테이블 셋업
        col_info = [('System', 550), ('관련 경보', 210), ('AI 확신도', 200)]
        self.setColumnCount(3)
        self.setRowCount(5)
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
        self.setRowHeight(self.rowCount()-1, 25)

    def mousePressEvent(self, *args, **kwargs):
        print('Test 시스템 선택 시 화면 전환')
        Flag.call_recv = True
        super(MainParaArea2, self).mousePressEvent(*args, **kwargs)

    def paintEvent(self, e: QPaintEvent) -> None:
        """ tabelview의 위에 라인 그리기 """
        super(MainParaArea2, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        for i in range(5):
            pen.setColor(QColor(128, 128, 128))         # 가로선 -> 활성화 x color
            pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i*28, 960, i*28)
        qp.restore()

# 비정상절차서
class MainParaArea3(QGroupBox):
    def __init__(self, parent):
        super(MainParaArea3, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setTitle("비정상절차서:")
        self.setObjectName("main")
        layout = QHBoxLayout()
        self.gb = QGroupBox("Symptom Check [0/0]")  # 개수 받아와야 함
        self.gb.setObjectName("sub1")
        self.gb.setFixedWidth(600)

        sublayout = QVBoxLayout()
        self.gb2 = QLabel("AI 확신도")
        self.gb2.setObjectName("sub2")
        sublayout.addWidget(self.gb2)
        sublayout.addWidget(MainParaArea3_1(self))

        layout.addWidget(self.gb)
        layout.addLayout(sublayout)
        self.setLayout(layout)


class MainParaArea3_1(QTableWidget):
    def __init__(self, parent):
        super(MainParaArea3_1, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        # 테이블 헤더 모양 정의
        # self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)  # Grid 지우기

        # 테이블 셋업
        col_info = [('변수명', 180), ('기여도', 142)]
        self.setColumnCount(2)
        self.setRowCount(16)
        self.horizontalHeader().setFixedHeight(29)
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


        # 편집 불가
        # self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.setFocusPolicy(Qt.NoFocus)
        # self.setSelectionMode(QAbstractItemView.NoSelection)

    def paintEvent(self, e: QPaintEvent) -> None:
        """ tabelview의 위에 라인 그리기 """
        super(MainParaArea3_1, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        for i in range(17):
            pen.setColor(QColor(128, 128, 128))         # 가로선 -> 활성화 x color
            pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i*29, 960, i*29)
        qp.restore()

class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main1Right()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()
