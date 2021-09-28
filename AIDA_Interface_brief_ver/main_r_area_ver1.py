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
        self.Mainwindow = parent
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainRightArea')
        self.selected_procedure = ''
        # Size ---------------------------------------------------------------------------------------------------------
        self.setFixedHeight(h)
        self.setFixedWidth(w)
        # 레이어 셋업 ---------------------------------------------------------------------------------------------------
        s, side_s = 5, 5
        self.ProcedureTable = ProcedureTable(self, x=side_s, y=side_s, w=w - side_s * 2, h=180)
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
        self.Mainwindow = parent.Mainwindow
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
        self.col_info = [('비정상 절차서 명', 395), ('긴급 여부', 65), ('증상 확인', 65), ('AI 확신도', 145)] # 690
        self.setColumnCount(len(self.col_info))
        [self.setColumnWidth(i, w) for i, (l, w) in enumerate(self.col_info)]
        self.setHorizontalHeaderLabels([l for (l, w) in self.col_info])
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setFixedHeight(30)
        # 2. Row 셋업
        self.max_line = 5
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
        self.setCellWidget(i, 1, ProcedureItemInfo(self, type='Match'))
        self.setCellWidget(i, 2, ProcedureItemInfo(self, type='Match'))
        self.setCellWidget(i, 3, ProcedureItemInfo(self, type='Prob'))

    def _update_procedure_display(self):
        """ AI 모듈에서 계산된 정보 업데이트"""
        ab_dig_result = self.mem.get_logic('Ab_Dig_Result')
        """
        ad_dig_result = {0: {'index': ..., 'value': ...}} 
        """
        # print(ab_dig_result)
        if ab_dig_result != {}:
            test_procedure_des = {i: ab_dig_result[i]['index'] for i in range(5)}
            test_procedure_prob = {i: round(ab_dig_result[i]['value'], 2) * 100 for i in range(5)}
        else:
            test_procedure_des = {i: 'Normal: 정상' for i in range(5)}
            test_procedure_prob = {i: 0 for i in range(5)}
            # test_procedure_des = {
            #     0: 'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설',
            #     1: 'Ab21_01: 가압기 압력 채널 고장 (고)',
            #     2: 'Ab63_02: 제어봉의 계속적인 삽입',
            #     3: 'Ab63_02: 제어봉의 계속적인 삽입',
            #     4: 'Ab63_02: 제어봉의 계속적인 삽입',
            # }
            #
            # test_procedure_prob = {
            #     0: self.test_i,
            #     1: 95 - self.test_i,
            #     2: 5,
            #     3: 3,
            #     4: 2,
            # }

            self.test_i = self.test_i + 1 if self.test_i <= 95 else 0

        test_procedure_match = {}

        for i in range(5):
            _info = self.mem.get_procedure_info(test_procedure_des[i])
            _steps = _info['Symptom Check']
            """
            _steps 는 해당 key 에 포함되어 있는 데이터임. step 은 0 부터 순회함.
            'Symptom Check': {
                0: {'ManClick': False, 'AutoClick': False, 'Nub': '1.1', 'Des': '정상'}
            }
            """
            tot, auto_tot = 0, 0
            for step in range(len(_steps)):
                tot += 1
                auto_tot += 1 if _steps[step]['AutoClick'] else 0
            test_procedure_match[i] = {'Tot': tot, 'Match': auto_tot}

        for i in range(self.rowCount()):
            self.cellWidget(i, 0).dis_update(test_procedure_des[i], test_procedure_des[i])
            self.cellWidget(i, 1).dis_update(test_procedure_des[i], test_procedure_match[i])
            self.cellWidget(i, 2).dis_update(test_procedure_des[i], test_procedure_match[i])
            self.cellWidget(i, 3).dis_update(test_procedure_des[i], test_procedure_prob[i])


class ProcedureItemInfo(QWidget):
    """ ProcedureTable 의 Item """
    def __init__(self, parent, type):
        super(ProcedureItemInfo, self).__init__(parent=parent)
        self.mem = parent.mem
        self.Mainwindow = parent.Mainwindow
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

        if ev.button() == Qt.RightButton:
            self.Mainwindow.update_selected_procedure(str(self.procedure_name), change_panel=True)
        elif ev.button() == Qt.LeftButton:
            self.Mainwindow.update_selected_procedure(str(self.procedure_name), change_panel=False)

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
            self.label.setText(f'{_info["Match"]} / {_info["Tot"]}')
            self.label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 정렬
        elif self._type == 'Prob':
            self.progress.setValue(_info)
            self.progress.setAlignment(Qt.AlignVCenter | Qt.AlignRight)


class ProbProgressBar(QProgressBar):
    def __init__(self, parent):
        super(ProbProgressBar, self).__init__(parent)
        self.Mainwindow = parent.Mainwindow
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
        self.Mainwindow = parent.Mainwindow
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

        self.widget_sym_ = ProcedureSymptom(self,
                                            x=5, y=self.title_.y() + self.title_.height() + 5,
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
        qp.restore()

    def update_info(self):
        """ ProcedureItemInfo의 cell이 클릭 될때 동작함. """
        self.selected_procedure: str = self.parent().selected_procedure
        self.title_.setText(str('절차서 : ' + self.selected_procedure))
        self.widget_sym_.update_procedure_display()


class ProcedureSymptom(QTreeWidget):
    def __init__(self, parent, x, y, w, h):
        super(ProcedureSymptom, self).__init__(parent)
        self.mem = parent.mem
        self.selected_procedure: str = self.parent().selected_procedure
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.NoFocus)
        self.setObjectName('MainRightProcedureSymptom')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        T.set_round_frame(self)
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        self.setHeaderHidden(True)
        self.setColumnCount(1)  # '스텝' | 세부 절차내용 | 수행 여부 | 확 인

        self.top_level_items = {_: QTreeWidgetItem() for _ in ['Symptom Check']}
        [self._make_top_item(self.top_level_items[_], _) for _ in ['Symptom Check']]

        self.expandAll()

    def _make_top_item(self, top_level_item: QTreeWidgetItem, name: str):
        self.addTopLevelItem(top_level_item)
        self.l = QLabel(text=name)
        self.l.setFixedHeight(30)
        self.setItemWidget(top_level_item, 0, self.l)

    def _make_item(self, top_level_item: QTreeWidgetItem, nub: str, content: str, autoclick: bool, ):
        """ 하위 아이템 추가 """
        _item = QTreeWidgetItem()
        top_level_item.addChild(_item)

        # 일정 길이내에서 공백을 기준으로 텍스트 가공
        temp_line, temp_i_line = '', ''
        for s in content.split(' '):    # 공백으로 글자 분할
            if len(temp_i_line) + len(s) > 50:
                temp_line += temp_i_line + '\n'
                temp_i_line = s + ' '
            else:
                temp_i_line += s + ' '
        temp_line += temp_i_line

        _step_widget = QWidget()

        # 가공된 텍스트를 라벨에 부여하고, 텍스트의 모양에 맞춰서 크기 조정
        _content = QLabel(text=temp_line)
        _content.setParent(_step_widget)
        _content.setContentsMargins(5, 5, 5, 5)
        _content.adjustSize()
        _content.setGeometry(55, 5, 500, _content.height() + 5)

        # # 절차서 번호
        _nub = QLabel(text=nub)
        _nub.setParent(_step_widget)
        _nub.setContentsMargins(5, 5, 5, 5)
        _nub.setGeometry(0, 5, 50, _content.height())
        _nub.setAlignment(Qt.AlignTop | Qt.AlignRight)

        # 자동 수행 확인
        _auto_check = QPushButton()
        _auto_check.setCheckable(autoclick)
        _auto_check.setParent(_step_widget)
        _auto_check.setGeometry(560, 5, 20, 20)

        # 상태에 따른 창 색 변경
        if autoclick:
            _auto_check.setStyleSheet(""" background: rgb(255, 77, 79); border-radius:5px; border: 1px solid black; """)
        else:
            _auto_check.setStyleSheet(""" background: rgb(38, 55, 96); border-radius:5px; border: 1px solid black; """)

        _nub.setStyleSheet(""" border-radius:5px; border: 1px solid black; """)
        _content.setStyleSheet(""" border-radius:5px; border: 1px solid black; """)

        _step_widget.setFixedHeight(_content.height() + 5)

        # 상위 수준인 _item 에 _step_widget 을 추가함
        self.setItemWidget(_item, 0, _step_widget)

    def _clear_items(self):
        """ sym, emg, aft의 내용 모두 지우기 """
        for top_level_item in self.top_level_items.values():
            for child in top_level_item.takeChildren():
                top_level_item.removeChild(child)

    def update_procedure_display(self):
        # 창 초기화
        self._clear_items()
        # 메모리에서 선택된 절차서에 대한 절차서 정보 가져오기
        self.selected_procedure: str = self.parent().selected_procedure

        _info = self.mem.get_procedure_info(self.selected_procedure)
        for key in ['Symptom Check']:
            _top_level_item: QTreeWidgetItem = self.top_level_items[key]
            _steps = _info[key]     # key = 'Symptom Check'
            """
            _steps 는 해당 key 에 포함되어 있는 데이터임. step 은 0 부터 순회함.
            'Symptom Check': {
                0: {'ManClick': False, 'AutoClick': False, 'Nub': '1.1', 'Des': '정상'}
            }
            """
            tot, tot_auto = 0, 0
            for step in range(len(_steps)):
                self._make_item(_top_level_item, _steps[step]['Nub'], _steps[step]['Des'], _steps[step]['AutoClick'])
                tot += 1
                tot_auto += 1 if _steps[step]['AutoClick'] else 0

            self.l.setText(f'Symptom Check [{tot_auto:3}/{tot:3}]')
