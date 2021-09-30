import os
import sys
from datetime import timedelta

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainTitleBar(QWidget):
    """제목 표시줄 위젯"""
    def __init__(self, parent, h, w):
        super(MainTitleBar, self).__init__(None)
        self.shmem = parent.shmem
        self.W_myform = parent.W_myform
        self.W_mainwindow = parent

        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainTitleBar')
        # --------------------------------------------------------------------------------------------------------------
        self.setFixedHeight(h)
        self.setFixedWidth(w)

        self.is_moved = False
        self.mouseMovePos = None
        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        self.timebar = TimeBar(self, margin=5, w=200)

        self.changePP = ChangePP(self, st=315, w=950, margin=5, name_list=['경보/증상', '절차서', '기능복구', '예지'])

        self.btn_close = CloseBTN(self, margin=5)
        # --------------------------------------------------------------------------------------------------------------

    def close(self):
        """버튼 명령: 닫기"""
        self.parent().close()

    def mousePressEvent(self, event):
        """오버로딩: 마우스 클릭 이벤트
        - 제목 표시줄 클릭시 이동 가능 플래그
        """
        if event.button() == Qt.LeftButton:
            self.mouseMovePos = event.globalPos()
            self.is_moved = True

    def mouseReleaseEvent(self, event) -> None:
        self.mouseMovePos = None
        self.is_moved = False

    def mouseMoveEvent(self, event):
        """오버로딩: 마우스 이동 이벤트
        - 제목 표시줄 드래그시 창 이동
        """
        if self.is_moved:
            curPos = self.mapToGlobal(self.W_mainwindow.pos())  # 전체 창에서의 현재 위젯 위치 Pos 얻기
            globalPos = event.globalPos()  # 현재 클릭 지점의 전체 창에서의 위치 Pos 얻기
            diff = globalPos - self.mouseMovePos  # 움직인 거리 = 현재 - 이전 클릭 지점
            newPos = self.mapFromGlobal(curPos + diff)  # 전체 창에서의 위젯이 움직인 거리 계산 후 상위 위젯의 위치에 적합하게 값 변환
            self.W_mainwindow.move(newPos)
            self.mouseMovePos = globalPos

    # def paintEvent(self, e: QPaintEvent) -> None:
    #     qp = QPainter(self)
    #     qp.save()
    #
    #     pen = QPen()
    #     pen.setColor(QColor(127, 127, 127))
    #     pen.setWidth(2)
    #     qp.setPen(pen)
    #
    #     qp.drawLine(self.timebar.x() + self.timebar.width() + 5, self.timebar.y() + 5,
    #                 self.timebar.x() + self.timebar.width() + 5, self.timebar.y() + self.timebar.height() - 5)
    #
    #     qp.drawLine(self.changePP.x() - 0, self.changePP.y() + 10,
    #                 self.changePP.x() - 0, self.changePP.y() + self.changePP.height() - 10)
    #
    #     qp.drawLine(self.btn_close.x() - 5, self.btn_close.y() + 5,
    #                 self.btn_close.x() - 5, self.btn_close.y() + self.btn_close.height() - 5)
    #
    #     qp.restore()

# Level 1 --------------------------------------------------------------------------------------------------------------


class TimeBar(QWidget):
    def __init__(self, parent, margin=5, w=100):
        super(TimeBar, self).__init__(parent)
        self.shmem = parent.shmem
        self.W_myform = parent.W_myform
        self.W_maintitlebar = parent

        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속

        h = parent.height() - margin * 2
        x = margin
        y = margin
        w = w

        self.setGeometry(x, y, w, h)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.timebarlabel = QLabel('test')
        self.timebarlabel.setObjectName('TitleLabel')
        self.timebarlabel.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 정렬
        self.dis_update()

        layout.addWidget(self.timebarlabel)

        self.setLayout(layout)

        # timer section
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self.dis_update)
        timer.start()

    def dis_update(self):
        """ 타이머 디스플레이 업데이트 """
        cns_time = str(timedelta(seconds=int(self.shmem.get_shmem_val('KCNTOMS')/5))).split(',')[-1].replace(" ", "")
        self.timebarlabel.setText(cns_time)

        # real_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # self.timebarlabel.setText(real_time)


class CloseBTN(QPushButton):
    def __init__(self, parent, margin=5):
        super(CloseBTN, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('Exit')

        icon = os.path.join(ROOT_PATH, 'interface_image', 'close.png')

        h = parent.height() - margin * 2
        x = parent.width() - h - margin
        y = margin
        w = h

        self.setGeometry(x, y, w, h)
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(h * 0.5, h * 0.5))  # 아이콘 크기
        # --------------------------------------------------------------------------------------------------------------
        self.clicked.connect(self.close)

    def close(self):
        """버튼 명령: 닫기"""
        self.parent().close()


class ChangePP(QWidget):
    def __init__(self, parent, st, w, margin, name_list):
        """
        Stack widget page 세팅
        :param parent: MainTitleBar
        :param st: 시작 지점 x
        :param w: 전체 길이
        :param margin: 위, 아래 양 사이드 마진
        :param name_list: 각 버튼에 들어갈 이름
        """
        super(ChangePP, self).__init__(parent)
        self.shmem = parent.shmem
        self.W_myform = parent.W_myform
        self.W_mainwindow = parent.W_mainwindow
        self.W_maintitlebar = parent

        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        # --------------------------------------------------------------------------------------------------------------
        h = parent.height()
        x = st
        y = 0
        w = w
        self.setGeometry(x, y, w, h)
        self.name_list = name_list
        # --------------------------------------------------------------------------------------------------------------
        layout = QHBoxLayout()
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(5)

        self.btn_ = {}
        self.main_stack_widget: QStackedWidget = self.W_mainwindow.stack_widget
        for i, name in enumerate(self.name_list):
            self.btn_[name] = ChangePP_BTN(self, name, cond='Non-Click')
            if name == '예지':
                self.btn_[name].setFixedWidth(350)
            if name == '절차서':
                self.btn_[name].setFixedWidth(420)

            layout.addWidget(self.btn_[name])

        # MainWindow 에서 선택된 화면과 해당하는 버튼 Click 으로 전환
        self.click_change_pp(self.name_list[self.main_stack_widget.currentIndex()])
        self.setLayout(layout)

        # timer section
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self.dis_update)
        timer.start()

        self.test_val = 10000

    def click_change_pp(self, name):
        for i, n in enumerate(self.name_list):
            if n == name:
                # print(f'{n} is clicked.')
                self.btn_[n].update_info('Click')
                self.main_stack_widget.setCurrentIndex(i)
            else:
                self.btn_[n].update_info('Non-Click')

    def dis_update(self):
        """ 예지 부분 업데이트 """

        h = int(self.test_val/3600)
        m = int((self.test_val / 60) % 60)
        s = int(self.test_val % 60)

        if self.shmem.get_shmem_val('KCNTOMS') > 30 * 5:
            self.btn_['예지'].setText(f' 가압기 압력 이상 | Trip 까지 [{h:02}:{m:02}:{s:02}]')
            self.test_val -= 1
        else:
            self.btn_['예지'].setText(f' 예지-주요 트립 변수 안정')

    def update_selected_procedure(self, procedure: str, change_panel: bool):
        """ 절차서 클릭 시 해당 버튼의 텍스트 변경 + 패널 변경 """
        self.btn_['절차서'].setText(f'{procedure}')
        if change_panel:
            self.click_change_pp('절차서')

# Level 2 --------------------------------------------------------------------------------------------------------------


class ChangePP_BTN(QPushButton):
    def __init__(self, parent, name: str, cond: str):
        super(ChangePP_BTN, self).__init__(parent)
        self.shmem = parent.shmem
        self.W_myform = parent.W_myform
        self.W_mainwindow = parent.W_mainwindow
        self.W_maintitlebar = parent.W_maintitlebar
        self.W_ChangePP = parent

        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.installEventFilter(self)

        if name == '예지':
            self.setObjectName('ChangePPProg')
        else:
            self.setObjectName('ChangePP')

        self._name = name
        self._cond = cond
        self.setText(name)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.is_moved = False
        self.mouseMovePos = None

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a1.type() == QEvent.MouseButtonPress:
            if self.text() != '절차서':
                # Clicked -> 다른 pp 비활성화
                self.W_ChangePP.click_change_pp(self._name)
        if a1.type() == QEvent.HoverEnter:
            self.update_info('Hover')
            return True
        if a1.type() == QEvent.HoverLeave:
            self.update_info(self._cond)
            return True
        return False

    def mousePressEvent(self, event):
        """오버로딩: 마우스 클릭 이벤트
        - 제목 표시줄 클릭시 이동 가능 플래그
        """
        if event.button() == Qt.LeftButton:
            self.mouseMovePos = event.globalPos()
            self.is_moved = True

    def mouseReleaseEvent(self, event) -> None:
        self.mouseMovePos = None
        self.is_moved = False

    def mouseMoveEvent(self, event):
        """오버로딩: 마우스 이동 이벤트
        - 제목 표시줄 드래그시 창 이동
        """
        if self.is_moved:
            curPos = self.mapToGlobal(self.W_mainwindow.pos())  # 전체 창에서의 현재 위젯 위치 Pos 얻기
            globalPos = event.globalPos()  # 현재 클릭 지점의 전체 창에서의 위치 Pos 얻기
            diff = globalPos - self.mouseMovePos  # 움직인 거리 = 현재 - 이전 클릭 지점
            newPos = self.mapFromGlobal(curPos + diff)  # 전체 창에서의 위젯이 움직인 거리 계산 후 상위 위젯의 위치에 적합하게 값 변환
            self.W_mainwindow.move(newPos)
            self.mouseMovePos = globalPos

    def update_info(self, condition):
        self.setProperty("Condition", condition)
        self.style().polish(self)
        if not condition == 'Hover':
            self._cond = condition


