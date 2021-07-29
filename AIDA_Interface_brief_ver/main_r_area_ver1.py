import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDA_Interface_brief_ver.TOOL.TOOL_etc import ToolEtc as T

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainRightArea(QWidget):
    """ 오른쪽 절차서 디스플레이 위젯 """
    def __init__(self, parent, h, w, mem=None):
        super(MainRightArea, self).__init__(parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainRightArea')
        self.selected_procedure = ''
        # Size ---------------------------------------------------------------------------------------------------------
        self.setFixedHeight(h)
        self.setFixedWidth(w)
        # 레이어 셋업 ---------------------------------------------------------------------------------------------------
        s, side_s = 5, 5
        self.ProcedureTable = ProcedureTable(self, x=side_s, y=side_s, w=w - side_s * 2, h=120)
        self.ProcedureExplain = ProcedureExplain(self, x=side_s, y=side_s * 2 + self.ProcedureTable.height(),
                                                 w=w - side_s * 2,
                                                 h=h - side_s * 3 - self.ProcedureTable.height())
        # --

    def paintEvent(self, e: QPaintEvent) -> None:
        qp = QPainter(self)
        qp.save()
        pen = QPen()
        pen.setColor(QColor(127, 127, 127))  # 가로선 -> 활성화 x color
        pen.setWidth(2)
        qp.setPen(pen)
        qp.drawRoundedRect(self.ProcedureTable.geometry(), 10, 10)
        qp.drawRoundedRect(self.ProcedureExplain.geometry(), 10, 10)
        qp.restore()

# ----------------------------------------------------------------------------------------------------------------------


class ProcedureTable(QTableWidget):
    def __init__(self, parent, x, y, w, h):
        super(ProcedureTable, self).__init__(parent)
        self.mem = parent.mem
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setFocusPolicy(Qt.NoFocus)
        # self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setObjectName('MainRightProcedureTable')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        T.set_round_frame(self)
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        # 1. Colum 셋업
        self.col_info = [('비정상 절차서 명', 400), ('AI확신도', 145), ('진입 조건 확인', 145)] # 690
        self.setColumnCount(len(self.col_info))
        [self.setColumnWidth(i, w) for i, (l, w) in enumerate(self.col_info)]
        self.setHorizontalHeaderLabels([l for (l, w) in self.col_info])
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setFixedHeight(30)
        # 2. Row 셋업
        self.max_line = 3
        [self._add_empty_line(i) for i in range(self.max_line)]
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalScrollBar().setSingleStep(self.rowHeight(0))  # Click 시 이동하는 거리
        self.verticalScrollBar().setStyleSheet("""
                    QScrollBar:vertical{
                        border: none;
                        background: rgb(127, 127, 127);                 /* 활성화 x */
                        margin: 20 0 20 0;
                    }
                    QScrollBar::handle:vertical{
                        background: rgb(38, 55, 96);                    /* 활성화 o */
                    }
                    QScrollBar::sub-line:vertical{
                        background: rgb(38, 55, 96);                    /* 활성화 o */
                        height: 20;
                        border-image: url(./interface_image/U_arrow.svg);
                        subcontrol-position: top;
                        subcontrol-origin: margin;
                    }
                    QScrollBar::add-line:vertical{
                        background: rgb(38, 55, 96);                    /* 활성화 o */
                        height: 20;
                        border-image: url(./interface_image/D_arrow.svg);
                        subcontrol-position: bottom;
                        subcontrol-origin: margin;
                    }
                    """)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)  # Grid 지우기
        # display update -----------------------------------------------------------------------------------------------
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self._update_procedure_display)
        timer.start()

        self.test_i = 0
    # ==================================================================================================================
    # 함수 Overwrite

    def paintEvent(self, e: QPaintEvent) -> None:
        """ tabelview의 위에 라인 그리기 """
        super(ProcedureTable, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        for i in range(self.max_line):
            pen.setColor(QColor(127, 127, 127))  # 가로선 -> 활성화 x color
            pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i * 30, self.viewport().width(), i * 30)
        qp.restore()

    # ==================================================================================================================
    # Private functions

    def _add_empty_line(self, i):
        self.insertRow(i)
        self.setCellWidget(i, 0, ProcedureItemInfo(self, type='Name'))
        self.setCellWidget(i, 1, ProcedureItemInfo(self, type='Prob'))
        self.setCellWidget(i, 2, ProcedureItemInfo(self, type='Match'))

    def _update_procedure_display(self):
        """ AI 모듈에서 계산된 정보 업데이트"""
        ab_dig_result = self.mem.get_logic('Ab_Dig_Result')

        test_procedure_des = {
            0: 'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설',
            1: 'Ab21_01: 가압기 압력 채널 고장 (고)',
            2: 'Ab63_02: 제어봉의 계속적인 삽입',
        }
        test_procedure_prob = {
            0: self.test_i,
            1: 95 - self.test_i,
            2: 5,
        }
        self.test_i = self.test_i + 1 if self.test_i <= 95 else 0

        test_procedure_match = {
            0: {'Tot': 10, 'Match': 9},
            1: {'Tot': 15, 'Match': 3},
            2: {'Tot': 7, 'Match': 2},
        }
        for i in range(self.rowCount()):
            self.cellWidget(i, 0).dis_update(test_procedure_des[i], test_procedure_des[i])
            self.cellWidget(i, 1).dis_update(test_procedure_des[i], test_procedure_prob[i])
            self.cellWidget(i, 2).dis_update(test_procedure_des[i], test_procedure_match[i])


class ProcedureItemInfo(QWidget):
    """ ProcedureTable 의 Item """
    def __init__(self, parent, type):
        super(ProcedureItemInfo, self).__init__(parent=parent)
        self.mem = parent.mem
        self.MainRightArea: MainRightArea = self.parent().parent()
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setObjectName('ProcedureItemInfo')
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        layer = QVBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)
        layer.setSpacing(0)

        self.procedure_name = ''
        self._type = type
        if self._type == 'Name' or self._type == 'Match':
            self.label = QLabel()
            layer.addWidget(self.label)
        if self._type == 'Prob':
            self.progress = ProbProgressBar(self)
            self.progress.setAlignment(Qt.AlignRight)
            layer.addWidget(self.progress)

        self.setLayout(layer)

    # ==================================================================================================================
    # 함수 Overwrite

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        super(ProcedureItemInfo, self).mousePressEvent(ev)
        self.MainRightArea.selected_procedure = str(self.procedure_name)

        # Click 시 -> ProcedureExplain.upate_info와 연결
        self.MainRightArea.ProcedureExplain.update_info()

    # ==================================================================================================================
    # Public functions

    def dis_update(self, procedure_name, _info):
        """ 정보 디스플레이 업데이트 """
        self.procedure_name = procedure_name
        if self._type == 'Name':
            self.label.setText(' ' + str(_info))
        elif self._type == 'Match':
            self.label.setText(f'{_info["Tot"]} / {_info["Match"]}')
            self.label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 정렬
        elif self._type == 'Prob':
            self.progress.setValue(_info)
            self.progress.setAlignment(Qt.AlignVCenter | Qt.AlignRight)


class ProbProgressBar(QProgressBar):
    def __init__(self, parent):
        super(ProbProgressBar, self).__init__(parent)
        self.MainRightArea: MainRightArea = self.parent().parent()
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setObjectName('Prob')

    # ==================================================================================================================
    # 함수 Overwrite

    def paintEvent(self, e: QPaintEvent) -> None:
        super(ProbProgressBar, self).paintEvent(e)

        qp = QPainter(self)
        qp.save()
        pen = QPen()
        if self.value() > 50:
            pen.setColor(QColor(254, 245, 249))  # 세로선 -> Back color
        else:
            pen.setColor(QColor(19, 27, 48))     # 세로선 -> TitleBar color
        pen.setWidth(2)
        pen.setStyle(Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(114/2, 0, 114/2, 24)
        qp.restore()

# ----------------------------------------------------------------------------------------------------------------------
# AI 확신도 top 5 + Symptom


class ProcedureExplain(QWidget):
    def __init__(self, parent, x, y, w, h):
        super(ProcedureExplain, self).__init__(parent)
        self.mem = parent.mem
        self.ProcedureItemInfo: ProcedureItemInfo = self.parent().ProcedureTable
        self.selected_procedure: str = self.parent().selected_procedure
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setObjectName('MainRightProcedureExplain')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        T.set_round_frame(self)
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        self.title_ = QLabel(self, text='절차서 : ')
        self.title_.setGeometry(5, 5, w - 10, 25)

        self.title_ai_ = QLabel(self, text='AI\n확신도\nTop5')
        self.title_ai_.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_ai_.setGeometry(5, 35, 50, 120)
        self.table_ai_ = ProcedureExplainTable(self,
                                               x=self.title_ai_.x() + self.title_ai_.width() + 5, y=self.title_ai_.y(),
                                               w=self.width() - 5*3 - self.title_ai_.width(),
                                               h=self.title_ai_.height())

        self.widget_sym_ = ProcedureSymptom(self,
                                            x=5, y=self.title_ai_.y() + self.title_ai_.height() + 5,
                                            w=w - 10, h=465)

    # ==================================================================================================================
    # 함수 Overwrite

    def paintEvent(self, e: QPaintEvent) -> None:
        super(ProcedureExplain, self).paintEvent(e)
        qp = QPainter(self)
        qp.save()
        pen = QPen()
        qp.setPen(pen)

        pen.setColor(QColor(127, 127, 127))  # 가로선 -> 활성화 x color
        pen.setWidth(2)
        # 절차서:
        qp.drawLine(0, 30, self.width(), 30)

        # AI 확신도 top5
        pen.setWidth(1)
        qp.drawRoundedRect(self.title_ai_.geometry().adjusted(0, 0, self.width() - 60, 0), 10, 10)
        qp.drawLine(5 + self.title_ai_.width() + 2.5, self.title_ai_.y(),
                    5 + self.title_ai_.width() + 2.5, self.title_ai_.y() + self.title_ai_.height(),)
        qp.drawLine(5 + self.title_ai_.width() + 5, self.title_ai_.y(),
                    5 + self.title_ai_.width() + 5, self.title_ai_.y() + self.title_ai_.height(), )
        # Symptom
        qp.drawRoundedRect(self.widget_sym_.geometry(), 10, 10)

        qp.restore()

    def update_info(self):
        """ ProcedureItemInfo의 cell이 클릭 될때 동작함. """
        self.selected_procedure: str = self.parent().selected_procedure
        self.title_.setText(str('절차서 : ' + self.selected_procedure))
        self.table_ai_.update_procedure_display()


class ProcedureExplainTable(QTableWidget):
    def __init__(self, parent, x, y, w, h):
        super(ProcedureExplainTable, self).__init__(parent)
        self.mem = parent.mem
        self.selected_procedure: str = self.parent().selected_procedure
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setObjectName('ProcedureExplainTable')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect().adjusted(-10, 0, 0, 0)), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        # 1. Colum 셋업
        self.col_info = [('변수명', 480), ('AI확신도', 145)] # 625
        self.setColumnCount(len(self.col_info))
        [self.setColumnWidth(i, w) for i, (l, w) in enumerate(self.col_info)]
        self.setHorizontalHeaderLabels([l for (l, w) in self.col_info])
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setFixedHeight(20)
        # 2. Row 셋업
        self.max_line = 5
        [self._add_empty_line(i) for i in range(self.max_line)]
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)  # Grid 지우기
        # display update -----------------------------------------------------------------------------------------------
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self.update_procedure_display)
        timer.start()

        self.test_para = {
            '': ['', '', '', '', ''],
            'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설': ['가압기 수위', '가압기 압력', 'VCT 수위', '유출 유량', 'Charging Valve'],
            'Ab21_01: 가압기 압력 채널 고장 (고)': ['가압기 수위', '가압기 압력', 'VCT 수위', '유출 유량', 'Charging Valve'],
            'Ab63_02: 제어봉의 계속적인 삽입': ['가압기 수위', '가압기 압력', 'VCT 수위', '유출 유량', 'Charging Valve'],
        }
        self.test_val = {
            '': [0, 0, 0, 0, 0],
            'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설': [80, 10, 5, 3, 2],
            'Ab21_01: 가압기 압력 채널 고장 (고)': [80, 10, 5, 3, 2],
            'Ab63_02: 제어봉의 계속적인 삽입': [50, 30, 10, 5, 5],
        }

    # ==================================================================================================================
    # 함수 Overwrite

    def paintEvent(self, e: QPaintEvent) -> None:
        """ tabelview의 위에 라인 그리기 """
        super(ProcedureExplainTable, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        for i in range(self.max_line):
            pen.setColor(QColor(127, 127, 127))  # 가로선 -> 활성화 x color
            pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i * 20, self.viewport().width(), i * 20)

        l, w = self.col_info[0]
        qp.drawLine(w, 0, w, self.height())
        qp.restore()

    # ==================================================================================================================
    # Private functions

    def _add_empty_line(self, i):
        self.insertRow(i)
        self.setRowHeight(i, 20)
        self.setCellWidget(i, 0, QLabel(self, text=''))
        self.setCellWidget(i, 1, ProcedureExplainProgressBar(self))

    def update_procedure_display(self):
        self.selected_procedure: str = self.parent().selected_procedure
        for i in range(self.max_line):
            self.cellWidget(i, 0).setText(self.test_para[self.selected_procedure][i])
            self.cellWidget(i, 1).setValue(self.test_val[self.selected_procedure][i])


class ProcedureExplainProgressBar(QProgressBar):
    def __init__(self, parent):
        super(ProcedureExplainProgressBar, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.setObjectName('Prob')
        self.setValue(10)

    def paintEvent(self, e: QPaintEvent) -> None:
        super(ProcedureExplainProgressBar, self).paintEvent(e)

        qp = QPainter(self)
        qp.save()
        pen = QPen()
        if self.value() > 50:
            pen.setColor(QColor(254, 245, 249))  # 세로선 -> Back color
        else:
            pen.setColor(QColor(19, 27, 48))     # 세로선 -> TitleBar color
        pen.setWidth(2)
        pen.setStyle(Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(114/2, 0, 114/2, 24)
        qp.restore()


class ProcedureSymptom(QTreeWidget):
    def __init__(self, parent, x, y, w, h):
        super(ProcedureSymptom, self).__init__(parent)
        self.mem = parent.mem
        self.selected_procedure: str = self.parent().selected_procedure
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setObjectName('MainRightProcedureSymptom')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        T.set_round_frame(self)
        print(self.geometry())
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        self.setAnimated(True)
        self.setHeaderHidden(True)
        self.setColumnCount(4)  # '스텝' | 세부 절차내용 | 수행 여부 | 확 인
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 400)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 100)

        sym = QTreeWidgetItem()
        self.addTopLevelItem(sym)
        l = QLabel(text='Symptom')
        l.setFixedHeight(30)
        self.setItemWidget(sym, 0, l)

        sym1 = QTreeWidgetItem()
        sym.addChild(sym1)
        l = QLabel(text='Test')

        l2 = QTextBrowser()
        txt = '이대일 이대일 이대일 이대일 이대일 이대일 이대일 이대일 이대일 이대일 이대일 이대일 이대일 이대일 이대일 이대일 이대일'
        l2.setMarkdown(txt)
        l2.document().setPlainText(txt)

        font = l2.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        textSize = fontMetrics.size(0, l2.toPlainText())

        l2.setFixedHeight(textSize.height() + 15)
        l.setFixedHeight(textSize.height() + 15)

        self.setItemWidget(sym1, 0, l)
        self.setItemWidget(sym1, 1, l2)

        emg = QTreeWidgetItem()
        self.addTopLevelItem(emg)
        l = QLabel(text='긴급조치')
        l.setFixedHeight(30)
        self.setItemWidget(emg, 0, l)

        aft = QTreeWidgetItem()
        self.addTopLevelItem(aft)
        l = QLabel(text='후속조치')
        l.setFixedHeight(30)
        self.setItemWidget(aft, 0, l)

        # sym = QTreeWidgetItem(['Symptom', '', '', ''])
        # emg = QTreeWidgetItem(['긴급 조치', '', '', ''])
        # aft = QTreeWidgetItem(['후속 조치', '', '', ''])
        #
        # self.addTopLevelItem(sym)
        # self.addTopLevelItem(emg)
        # self.addTopLevelItem(aft)
        #
        # a = QTreeWidgetItem()
        # a.setText(0, 'Test')
        # sym.addChild(a)
        #
        # t_ = QTextBrowser()
        # t_.setFixedHeight(100)
        #
        # self.setItemWidget(a, 1, t_)