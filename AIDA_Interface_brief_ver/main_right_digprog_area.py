import os
import sys
import pandas as pd
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainRightDiagnosisProgArea(QWidget):
    """ 오른쪽 진단 및 예지 디스플레이 위젯 """
    qss = """
        QWidget {
            background: rgb(14, 22, 24);
        }
        QLabel {
            background: rgb(31, 39, 42);
            border-radius: 6px;
            color: rgb(255, 255, 255);
        }
    """

    def __init__(self, parent=None):
        super(MainRightDiagnosisProgArea, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.parent = parent
        self.setMinimumHeight(self.parent.height() - 40)                              # 아래섹션의 기준 크기 <-
        # self.setMaximumWidth(int(self.parent.width()/5) * 2)                          # 1/3 부분을 차지

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 5, 5)                                         # 왼쪽 여백 고려 x

        label1 = DiagnosisArea(self)
        # label2 = CircleProgress(self, 100, 100)
        label2 = PrognosisArea(self)

        layout.addWidget(label1)
        layout.addWidget(label2)
        self.setLayout(layout)

# ======================================================================================================================


class DiagnosisArea(QWidget):
    def __init__(self, parent=None):
        super(DiagnosisArea, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.parent = parent
        # self.setObjectName('SubWin')

        self.setFixedHeight(int(self.parent.height() * 2 / 3))

        layer = QVBoxLayout()

        title = QLabel('Diagnosis Area')
        title.setFixedHeight(20)
        title.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)    # 텍스트 가운데 정렬

        self.canvases_widgets = DiagnosisAreaCanvases(self)

        layer.addWidget(title)
        layer.addWidget(self.canvases_widgets)
        self.setLayout(layer)


class DiagnosisAreaCanvases(QWidget):
    def __init__(self, parent=None):
        super(DiagnosisAreaCanvases, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.parent = parent

        for i in range(0, 4):
            for j in range(0, 4):
                CircleProgress(self, 70*i + 20, 70*j + 20, 70, 70)

        for i in range(0, 4):
            SlideButton(self, 350, 70 * i + 20, 50, 30)


    def contextMenuEvent(self, event) -> None:
        """ DiagnosisArea 에 기능 올리기  """
        menu = QMenu(self)
        add_circleprogress = menu.addAction("Add Circle Progress")
        add_slidebutton = menu.addAction("Add Slide Button")

        add_circleprogress.triggered.connect(lambda a, pos=event.pos(), ele='cir': self.make_circleprogress(pos, ele))
        add_slidebutton.triggered.connect(lambda a, pos=event.pos(), ele='slide': self.make_circleprogress(pos, ele))
        menu.exec_(event.globalPos())

    def make_circleprogress(self, pos, ele):
        """ 크릭한 위치에 요소 위치 시키기 """
        if ele == 'cir':
            cp = CircleProgress(self, pos.x(), pos.y(), 70, 70)
            cp.show()
        if ele == 'slide':
            sl = SlideButton(self, pos.x(), pos.y(), 50, 30)
            sl.show()


# ======================================================================================================================


class PrognosisArea(QWidget):
    qss = """
            QWidget {
                background: rgb(31, 39, 42);
                border-radius: 6px;
            }
        """

    def __init__(self, parent=None):
        super(PrognosisArea, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.parent = parent
        self.setStyleSheet(self.qss)

        self.prognosis_plot = PrognosisPlot(parent=self)

        layer = QHBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)# , 5, 5, 5)
        layer.addWidget(QLabel('Prognosis Area'))
        layer.addWidget(self.prognosis_plot)

        self.setLayout(layer)


class PrognosisPlot(QChartView):
    def __init__(self, parent=None):
        super(PrognosisPlot, self).__init__(parent)
        self.parent = parent

        self.series = QLineSeries()
        self.series.append(0, 0)
        self.series.append(1, 10)
        self.series.append(2, 20)

        self.chart_area = QChart()
        self.chart_area.legend().hide()
        self.chart_area.addSeries(self.series)
        
        axisX = QValueAxis()
        axisY = QValueAxis()
        self.chart_area.addAxis(axisX, Qt.AlignBottom)
        self.chart_area.addAxis(axisY, Qt.AlignRight)
        self.series.attachAxis(axisX)
        self.series.attachAxis(axisY)
        self.chart_area.layout().setContentsMargins(0, 0, 0, 0)

        self.setChart(self.chart_area)
        self.setRenderHint(QPainter.Antialiasing)

    def contextMenuEvent(self, event) -> None:
        """ ChartArea 에 기능 올리기  """
        menu = QMenu(self)
        add_input = menu.addAction("Add input")
        add_input.triggered.connect(self._add_input)
        menu.exec_(event.globalPos())

    def _add_input(self):
        print(self.series.__len__())
        self.series.append(self.series.__len__(), (self.series.__len__() ** 2) * 10)
        self._update_axis()

    def _update_axis(self):
        pvs = self.series.pointsVector()
        dtStart = pvs[0]
        dtEnd = pvs[-1]

        ax = self.chart_area.axisX()
        ax.setRange(dtStart.x(), dtEnd.x())

        ay = self.chart_area.axisY()
        ay.setRange(dtStart.y(), dtEnd.y())



# ======================================================================================================================
# TOOL


class CircleProgress(QWidget):
    """ 원형 프로그래스 바 """
    def __init__(self, parent=None, x=0, y=0, w=30, h=30):
        super(CircleProgress, self).__init__(parent=parent)     # 부모 클래스 상속
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속 <- 독자적으로 사용 예정..
        self.parent = parent
        # self.setObjectName('CircleProgress')

        # set-up circle size
        self.setGeometry(x, y, w, h)
        self.setFixedWidth(w)
        self.setFixedHeight(h)

        # info & display
        self.percent = 0
        self.percent_label = QLabel(f'{self.percent} [%]')
        self.parent.setObjectName('CircleProgress')
        self.percent_label.setFixedWidth(self.width() - 30)
        self.percent_label.setFixedHeight(20)
        self.percent_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)

        layer = QHBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)
        layer.addWidget(self.percent_label)
        self.setLayout(layer)

        #
        self.mouseMovePos = None
        self.is_moved = False

    def mousePressEvent(self, event) -> None:
        """ 테스트 용
        - 마우스 가운데 클릭 시 display 업데이트
        - 마우스 왼쪽 클릭 시 위젯이 움직임.
        """
        if event.button() == Qt.LeftButton:
            self.mouseMovePos = event.globalPos()
            self.is_moved = True
        else:
            self.is_moved = False

        if event.button() == Qt.MiddleButton:
            self.percent = 0 if self.percent >= 100 else self.percent.__add__(5)
            self.progress_info_update()
            self.update()

    def mouseMoveEvent(self, event) -> None:
        if self.is_moved:
            curPos = self.mapToGlobal(self.pos())       # 전체 창에서의 현재 위젯 위치 Pos 얻기
            globalPos = event.globalPos()               # 현재 클릭 지점의 전체 창에서의 위치 Pos 얻기
            diff = globalPos - self.mouseMovePos        # 움직인 거리 = 현재 - 이전 클릭 지점
            newPos = self.mapFromGlobal(curPos + diff)  # 전체 창에서의 위젯이 움직인 거리 계산 후 상위 위젯의 위치에 적합하게 값 변환
            self.move(newPos)
            self.mouseMovePos = globalPos

    def progress_update(self, p):
        """ p (%) 로 업데이트 """

        # p [0 ~ 100] -> percent[0 ~ 100]
        self.percent = p
        self.progress_info_update()
        self.update()

    def progress_info_update(self):
        self.percent_label.setText(f'{self.percent}[%]')

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(QColor(31, 39, 42), 8, Qt.SolidLine))
        painter.drawEllipse(5, 5, self.width() - 10, self.height() - 10)

        painter.setPen(QPen(QColor(255, 193, 7), 8, Qt.SolidLine))
        painter.drawArc(5, 5, self.width() - 10, self.height() - 10, 90 * 16, - int(self.percent * 16 * 3.6))
        painter.end()

        # re mask : 범위 지정
        path = QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)


class SlideButton(QWidget):
    qss = """
    No qss
    """

    def __init__(self, parent=None, x=0, y=0, w=50, h=30):
        super(SlideButton, self).__init__(parent=parent)     # 부모 클래스 상속
        # self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속 <- 독자적으로 사용 예정..
        self.parent = parent
        # self.setStyleSheet(self.qss)
        self.setObjectName('SlideButton')

        # set-up circle size
        self.setGeometry(x, y, w, h)
        self.setFixedWidth(w)
        self.setFixedHeight(h)

        # info & display
        self.on_off = False
        #
        self.mouseMovePos = None
        self.is_moved = False
        # ani
        self.__pos_ball = 5
        # self.setProperty('_pos_ball', self._update_pos_ball)    # 0 <-> self.width() - 25
        self.ani = QPropertyAnimation(self, b'_pos_ball')
        self.ani.setDuration(200)

    @pyqtProperty(int)
    def _pos_ball(self):
        return self.__pos_ball

    @_pos_ball.setter
    def _pos_ball(self, value):
        self.__pos_ball = value
        self.update()

    def mousePressEvent(self, event) -> None:
        """ 테스트 용
        - 마우스 가운데 클릭 시 display 업데이트
        - 마우스 왼쪽 클릭 시 위젯이 움직임.
        """
        if event.button() == Qt.LeftButton:
            self.mouseMovePos = event.globalPos()
            self.is_moved = True
        else:
            self.is_moved = False

        if event.button() == Qt.MiddleButton:
            # TODO 향후 업데이트 필요 가운데 클릭이 반응 하도록 만들 것
            if self.on_off:
                self.on_off = False
            else:
                self.on_off = True

    def mouseReleaseEvent(self, event) -> None:
        if self.on_off:
            self.ani.setStartValue(5)
            self.ani.setEndValue(25)
            self.ani.start()
        else:
            self.ani.setStartValue(25)
            self.ani.setEndValue(5)
            self.ani.start()

    def mouseMoveEvent(self, event) -> None:
        if self.is_moved:
            curPos = self.mapToGlobal(self.pos())       # 전체 창에서의 현재 위젯 위치 Pos 얻기
            globalPos = event.globalPos()               # 현재 클릭 지점의 전체 창에서의 위치 Pos 얻기
            diff = globalPos - self.mouseMovePos        # 움직인 거리 = 현재 - 이전 클릭 지점
            newPos = self.mapFromGlobal(curPos + diff)  # 전체 창에서의 위젯이 움직인 거리 계산 후 상위 위젯의 위치에 적합하게 값 변환
            self.move(newPos)
            self.mouseMovePos = globalPos

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # get boundary canvas
        # painter.setPen(QPen(QColor(31, 39, 42), 2, Qt.SolidLine))
        # painter.drawRect(0, 0, self.width(), self.height())

        if self.on_off:
            painter.setBrush(QBrush(QColor(255, 219, 117), Qt.SolidPattern))
            painter.drawRoundedRect(10, 10, self.width() - 20, 10, 5, 5)
            painter.setBrush(QBrush(QColor(255, 193, 7), Qt.SolidPattern))
            # painter.drawEllipse(self.width() - 25, 5, 20, 20)
            #
            # painter.setFont(QFont('Arial', 8))
            # painter.drawText(QRect(self.width() - 25, 5, 20, 20), Qt.AlignCenter, 'On')

            painter.drawEllipse(self.__pos_ball, 5, 20, 20)

            painter.setFont(QFont('Arial', 8))
            painter.drawText(QRect(self.__pos_ball, 5, 20, 20), Qt.AlignCenter, 'On')

        else:
            painter.setBrush(QBrush(QColor(31, 39, 42), Qt.SolidPattern))
            painter.drawRoundedRect(10, 10, self.width() - 20, 10, 5, 5)
            painter.setBrush(QBrush(QColor(227, 230, 233), Qt.SolidPattern))
            painter.drawEllipse(self.__pos_ball, 5, 20, 20)

            painter.setFont(QFont('Arial', 8))
            painter.drawText(QRect(self.__pos_ball, 5, 20, 20), Qt.AlignCenter, 'Off')

        painter.end()