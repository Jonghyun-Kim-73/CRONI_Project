import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainTitleBar(QWidget):
    """제목 표시줄 위젯"""
    def __init__(self, parent, h, w):
        super(MainTitleBar, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainTitleBar')
        # --------------------------------------------------------------------------------------------------------------
        self.setFixedHeight(h)
        self.setFixedWidth(w)

        self.is_moved = False
        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        self.timebar = TimeBar(self, load_realtime=True, margin=5, w=200)
        self.condbar = ConditionBar(self, margin=5, w=100)
        btn_close = self.create_btn_with_image('close.png', margin=5)
        btn_close.setObjectName('Exit')
        # --------------------------------------------------------------------------------------------------------------
        btn_close.clicked.connect(self.close)

    def create_btn_with_image(self, icon_path, margin):
        icon = os.path.join(ROOT_PATH, 'interface_image', icon_path)
        btn = QPushButton(self)

        h = self.height() - margin * 2
        x = self.width() - h - margin
        y = margin
        w = h

        btn.setGeometry(x, y, w, h)
        btn.setIcon(QIcon(icon))
        btn.setIconSize(QSize(h*0.5, h*0.5))  # 아이콘 크기
        return btn

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
        else:
            self.is_moved = False

    def mouseMoveEvent(self, event):
        """오버로딩: 마우스 이동 이벤트
        - 제목 표시줄 드래그시 창 이동
        """
        if self.is_moved:
            curPos = self.mapToGlobal(self.parent().pos())  # 전체 창에서의 현재 위젯 위치 Pos 얻기
            globalPos = event.globalPos()  # 현재 클릭 지점의 전체 창에서의 위치 Pos 얻기
            diff = globalPos - self.mouseMovePos  # 움직인 거리 = 현재 - 이전 클릭 지점
            newPos = self.mapFromGlobal(curPos + diff)  # 전체 창에서의 위젯이 움직인 거리 계산 후 상위 위젯의 위치에 적합하게 값 변환
            self.parent().move(newPos)
            self.mouseMovePos = globalPos


class TimeBar(QWidget):
    def __init__(self, parent, load_realtime: bool = False, margin=5, w=100):
        super(TimeBar, self).__init__(parent)
        self.load_realtime = load_realtime
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
        if self.load_realtime:
            real_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.timebarlabel.setText(real_time)
        else:
            # TODO 나중에 CNS 변수 사용시 real_time 부분 수정할 것.
            real_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.timebarlabel.setText(real_time)


class ConditionBar(QLabel):
    def __init__(self, parent, init_condition: str = 'Normal', margin=5, w=100):
        super(ConditionBar, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 정렬

        h = parent.height() - margin * 2
        x = margin + parent.timebar.width()
        y = margin
        w = w

        self.setGeometry(x, y, w, h)

        self.setObjectName('ConditionBar')
        self.update_condition(init_condition)

    def update_condition(self, condition: str):
        self.setProperty("Condition", condition)
        self.setText(condition)
        self.style().polish(self)

    def contextMenuEvent(self, event) -> None:
        """ Condition Bar 기능 테스트 """
        menu = QMenu(self)
        test_action1 = menu.addAction("Emergency")
        test_action2 = menu.addAction("Normal")
        test_action3 = menu.addAction("Abnormal")

        test_action1.triggered.connect(lambda a, cond='Emergency': self.update_condition(cond))
        test_action2.triggered.connect(lambda a, cond='Normal': self.update_condition(cond))
        test_action3.triggered.connect(lambda a, cond='Abnormal': self.update_condition(cond))

        menu.exec_(event.globalPos())
