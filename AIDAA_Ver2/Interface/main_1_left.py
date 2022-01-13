import os
import sys
from datetime import datetime
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver2.Interface import Flag
from AIDAA_Ver2.Interface.Custom_Popup import Popup
from AIDAA_Ver2.Interface.Procedure.alarm_procedure import alarm_pd


class Main1Left(QWidget):
    qss = """
        QWidget {
            background: rgb(231, 231, 234);
            border: 0px solid rgb(0, 0, 0); 
            font-size: 14pt;
            border-radius: 6px;
        }
        QTableWidget {
            color : white;
            background: rgb(231, 231, 234);
            border: 1px solid rgb(128, 128, 128);
            border-radius: 6px;
        }
        QPushButton{
            background: White;
            color: Black;
            border-radius:6px;
        }
        QHeaderView::section {
            padding:3px;
            padding-left:15px;
            background: rgb(128, 128, 128);
            font-size:14pt;
            border:0px solid;
        }
        QHeaderView {
            border:1px solid rgb(128, 128, 128);
            border-top-left-radius :6px;
            border-top-right-radius : 6px;
            border-bottom-left-radius : 0px;
            border-bottom-right-radius : 0px;
        }
        
        QTableView::item {
            padding:50px;
            font-size:14pt;
        }
        QScrollBar:vertical {
            width:30px;
        }
    """

    def __init__(self, parent):
        super(Main1Left, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mem = parent.mem  # <- CNS mem
        self.setStyleSheet(self.qss)
        # self.setFixedWidth(990)
        # 기본 속성
        # self.setMinimumHeight(750)

        # 레이아웃
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        label1 = FreezeTableWidget(self)
        self.btn_suppress = QPushButton("Suppress button")
        self.btn_suppress.setFixedHeight(35)
        self.btn_suppress.clicked.connect(self.suppress)
        layout.addWidget(label1)
        layout.addWidget(self.btn_suppress)
        self.setLayout(layout)

    # Alarm clear
    def suppress(self):
        Flag.alarm_clear = True



class FreezeTableWidget(QTableView):
    def __init__(self, parent):
        super(FreezeTableWidget, self).__init__(parent)
        self.mem = parent.mem
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMinimumSize(800, 600)

        # set the table model
        tm = MyTableModel(self)
        self.setModel(tm)

        self.frozenTableView = QTableView(self)
        self.frozenTableView.setModel(tm)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.viewport().stackUnder(self.frozenTableView)

        # table 선택 불가
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)

        # hide grid
        self.setShowGrid(False)

        # header 설정
        self.hh = self.horizontalHeader()
        self.hh.setDefaultAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.hh.setSectionResizeMode(0, QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기

        self.frozenTableView.show()
        self.updateFrozenTableGeometry()

        # item 별 scroll
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.frozenTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)

        self.frozenTableView.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.frozenTableView.verticalScrollBar().setValue)

        # get scroll position
        self.scrollBar = self.frozenTableView.verticalScrollBar()
        self.scrollBar.valueChanged.connect(lambda value: self.scrolled(self.scrollBar, value))

        # row 클릭
        self.frozenTableView.setSelectionBehavior(QTableView.SelectRows)
        self.doubleClicked.connect(self.mouseDoubleClick)

    def mouseDoubleClick(self, index):
        print("더블클릭")
        model = self.model()
        Flag.alarm_popup_name = model.click_alarm_name(index)
        print(Flag.alarm_popup_name)
        test_pdf = "test.pdf"
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), test_pdf))
        self.popup = Popup(file_path=file_path)
        self.popup.show()


    def scrolled(self, scrollbar, value):
        if value == scrollbar.maximum():
            print(value)  # that will be the bottom/right end
        if value == scrollbar.minimum():
            print(value)  # top/left end

    def updateFrozenTableGeometry(self):
        if self.verticalHeader().isVisible():
            self.frozenTableView.setGeometry(self.verticalHeader().width() + self.frameWidth(),
                                             self.frameWidth(), self.frameWidth(),
                                             self.viewport().height() + self.horizontalHeader().height())
        else:
            self.frozenTableView.setGeometry(self.frameWidth(),
                                             self.frameWidth(), self.frameWidth(),
                                             self.viewport().height() + self.horizontalHeader().height())

    def paintEvent(self, e: QPaintEvent) -> None:
        # tableview add line
        super(FreezeTableWidget, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        pen.setColor(QColor(128, 128, 128))
        # 가로선 set width
        for i in range(30):
            if i % 5 == 0: pen.setWidth(3)
            else: pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i * 30, 960, i * 30)
        qp.restore()

class MyTableModel(QAbstractTableModel):
    def __init__(self, parent):
        super(MyTableModel, self).__init__(parent)
        # header
        self.colLabels = ['DESCRIPTION', 'VALUE', 'SETPOINT', 'UNIT', 'DATE', 'TIME']
        # col_info = [('DESCRIPTION', 340), ('VALUE', 160), ('SETPOINT',160),('UNIT',100),('DATE',100),('TIME',93)]  # 475
        # data  rows[index.row()][index.column()]

        # 데이터 받아오기
        self.mem = parent.mem  # <- CNS mem
        self.dataCached = []

        timer1 = QTimer(self)
        timer1.setInterval(1)
        timer1.timeout.connect(self.update_alarm)
        timer1.start()

        # 1초 간격으로 blink
        blink_thread = Blink(self)
        blink_thread.start()

    def update_alarm(self):
        self.alarm_cnt = len(Flag.alarm_occur_list)
        # self.dataCached = []
        # 발생한 Alarm list(des)
        self.alarm_names = self.mem.get_occured_alarm_des()

        # 떠있는 Alarm
        self.current_alarm_name = []
        for i in range(len(self.dataCached)):
            self.current_alarm_name.append(self.dataCached[i][0])

        # Alarm 테이블에 넣기(중복 제외) - 알람 발생 time 초기화 문제 해결
        if len(self.alarm_names) != 0:
            for i in range(len(self.alarm_names)):
                if not self.alarm_names[i] in self.current_alarm_name:
                    # alarm blink 테스트용
                    if i == 0:
                        self.dataCached.append([self.alarm_names[i], 0.1, 0.3, "  kg/cm",
                                            datetime.now().strftime('%m.%d'),
                                            datetime.now().strftime('%H:%M:%S')])
                    if i == 1:
                        self.dataCached.append([self.alarm_names[i], 0.5, 0.2, "  kg/cm",
                                            datetime.now().strftime('%m.%d'),
                                            datetime.now().strftime('%H:%M:%S')])
        # 현재 발생한 전체 알람 cnt
        Flag.all_alarm_cnt = len(self.current_alarm_name)

        # 이상 알람 check
        for idx in range(Flag.all_alarm_cnt):
            # Value, SetPoint 값 비교
            if self.dataCached[idx][1] > self.dataCached[idx][2]:
                Flag.alarm_blink[idx] = True  # 이상 알람

        # alarm clear
        if Flag.alarm_clear:
            self.mem._make_mem_initial()
            self.dataCached = []
            Flag.alarm_clear = False

        # layout 업데이트
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()

    # 1초 간격 blink
    def resetBlink(self):
        for idx in range(Flag.all_alarm_cnt):
            print(Flag.alarm_color_change)
            if Flag.alarm_blink[idx]:
                if Flag.alarm_color_change[idx]:
                    Flag.alarm_color_change[idx] = False
                elif Flag.alarm_color_change[idx] == 1:
                    Flag.alarm_color_change[idx] = 2
            else:
                Flag.alarm_color_change[idx] = 0

    def rowCount(self, parent):
        return len(self.dataCached)

    def columnCount(self, parent):
        return len(self.colLabels)

    def get_value(self, index):
        i = index.row()
        j = index.column()
        return self.dataCached[i][j]

    def click_alarm_name(self, index):
        i = index.row()
        return self.dataCached[i][0]

    def data(self, index, role):
        # background color blink
        if role == Qt.BackgroundRole:
            for idx in range(Flag.all_alarm_cnt):
                if idx == index.row():
                    if Flag.alarm_blink[idx]:
                        if Flag.alarm_color_change[idx]:
                            return QBrush(QColor(255, 204, 0))
                        elif not Flag.alarm_color_change[idx]:
                            return QBrush(QColor(231, 230, 230))
                    else:
                        return QBrush(QColor(Qt.black))

        # text color blink
        if role == Qt.TextColorRole:
            for idx in range(Flag.all_alarm_cnt):
                if idx == index.row():
                    if Flag.alarm_blink[idx]:
                        if Flag.alarm_color_change[idx]:
                            return QBrush(QColor(128, 128, 128))
                        elif not Flag.alarm_color_change[idx]:
                            return QBrush(QColor(Qt.black))
                    else:
                        return QBrush(Qt.white)

        if not index.isValid():
            return None
        value = self.get_value(index)

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return value
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignLeft and Qt.AlignVCenter
        return None

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            self.dataCached[index.row()][index.column()] = value
            # self.dataChanged.emit(index, index)#원래 여기까지
            self.dataChanged.emit(index, index)
            return True
        else:
            return False

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = self.colLabels[section]
            return header
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section + 1)

        return None

class Blink(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        while True:
            for idx in range(Flag.all_alarm_cnt):
                print(Flag.alarm_color_change)
                if Flag.alarm_blink[idx]:
                    if Flag.alarm_color_change[idx]:
                        Flag.alarm_color_change[idx] = False
                    elif not Flag.alarm_color_change[idx]:
                        Flag.alarm_color_change[idx] = True
            self.sleep(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = Main1Left()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()
