import os
import sys
import math
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainProceArea(QWidget):
    """ 절차서 디스플레이 위젯 """
    def __init__(self, parent, x, y, w, h):
        super(MainProceArea, self).__init__(parent)
        self.mem = parent.mem
        self.Mainwindow = parent
        self.selected_procedure:str = parent.selected_procedure
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainProceArea')
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        self.procedure_name_label = QLabel(self, text=self.selected_procedure)
        self.procedure_name_label.setGeometry(10, 10, w, 30)
        self.procedure_name_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        layer = QVBoxLayout()
        layer.setContentsMargins(10, 10, 10, 10)
        layer.setSpacing(5)
        self.symptom_list1 = ProcedureStepsWarp(self, type='Symptom Check')
        self.symptom_list2 = ProcedureStepsWarp(self, type='긴급조치')
        self.symptom_list3 = ProcedureStepsWarp(self, type='후속조치')

        layer.addSpacerItem(QSpacerItem(0, 30, vPolicy=QSizePolicy.Fixed))
        layer.addWidget(self.symptom_list1)
        layer.addWidget(self.symptom_list2)
        layer.addWidget(self.symptom_list3)
        layer.addSpacerItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding))

        self.setLayout(layer)

    def paintEvent(self, e: QPaintEvent) -> None:
        qp = QPainter(self)
        qp.save()
        qp.setPen(QPen(QColor(127, 127, 127), 2, Qt.SolidLine))

        inside_rect = self.rect().adjusted(5, 5, -5, -5)

        qp.drawRoundedRect(inside_rect, 10, 10)
        #
        qp.drawLine(inside_rect.topLeft().x(),
                    inside_rect.topLeft().y() + 30,
                    inside_rect.topRight().x(),
                    inside_rect.topRight().y() + 30)
        #
        qp.restore()

    def update_selected_procedure(self, procedure):
        self.selected_procedure = procedure
        self.procedure_name_label.setText(procedure)
        self.symptom_list1.update_procedure_display()
        self.symptom_list2.update_procedure_display()
        self.symptom_list3.update_procedure_display()


class ProcedureStepsWarp(QWidget):
    def __init__(self, parent, type):
        super(ProcedureStepsWarp, self).__init__(parent)
        self.mem = parent.mem
        self.selected_procedure: str = parent.selected_procedure
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        l = QHBoxLayout()
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(0)

        self.ProcedureSteps = ProcedureSteps(self, type)
        l.addWidget(self.ProcedureSteps)

        self.setLayout(l)

    def paintEvent(self, e: QPaintEvent) -> None:
        qp = QPainter(self)
        qp.save()
        qp.setPen(QPen(QColor(127, 127, 127), 2, Qt.SolidLine))

        inside_rect = self.rect()

        qp.drawRoundedRect(inside_rect, 10, 10)

        qp.restore()

    def update_procedure_display(self):
        self.selected_procedure: str = self.parent().selected_procedure
        if self.selected_procedure != '':
            self.ProcedureSteps.update_procedure_display()


class ProcedureSteps(QTreeWidget):
    def __init__(self, parent, type):
        super(ProcedureSteps, self).__init__(parent)
        self.mem = parent.mem
        self.ProcedureStepsWarp = parent
        self.selected_procedure: str = self.parent().selected_procedure
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.NoFocus)
        self.setObjectName('MainRightProcedureSymptom')
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        self.setHeaderHidden(True)
        self.setColumnCount(1)  # '스텝' | 세부 절차내용 | 수행 여부 | 확 인

        self.top_level_items = {_: QTreeWidgetItem() for _ in [type]}
        [self._make_top_item(self.top_level_items[_], _) for _ in [type]]
        self._type = type
        self.expandAll()

        # TODO 개방되면 자동적으로 크기 조절하는 로직 만들기
        # self.expanded.connect(self.exp_)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        super(ProcedureSteps, self).mousePressEvent(e)

    def _make_top_item(self, top_level_item: QTreeWidgetItem, name: str):
        self.addTopLevelItem(top_level_item)
        l = QLabel(text=name)
        l.setFixedHeight(30)
        self.setItemWidget(top_level_item, 0, l)

    def _make_item(self, top_level_item: QTreeWidgetItem, key: str, step: int,
                   nub: str, content: str, autoclick: bool, manclick: bool):
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

        # 수동 수행 확인
        _man_check = QPushButton()

        _man_check._procedure = str(self.selected_procedure)
        _man_check._key = str(key)
        _man_check._step = int(step)

        _man_check.setCheckable(True)
        _man_check.setChecked(manclick)
        _man_check.clicked.connect(lambda a, btn=_man_check, cont=_content, nub=_nub: self._click_update_step(btn, cont, nub))
        _man_check.setParent(_step_widget)
        _man_check.setGeometry(585, 5, 20, 20)
        _man_check.setStyleSheet(""" background: rgb(127, 127, 127); border-radius:5px; border: 1px solid black; """)

        # 상태에 따른 창 색 변경
        if autoclick:
            _auto_check.setStyleSheet(""" background: rgb(255, 77, 79); border-radius:5px; border: 1px solid black; """)
        else:
            _auto_check.setStyleSheet(""" background: rgb(38, 55, 96); border-radius:5px; border: 1px solid black; """)

        if manclick:
            _man_check.setStyleSheet(""" background: rgb(38, 55, 96); border-radius:5px; border: 1px solid black; """)
            _content.setStyleSheet(""" background: rgb(24, 144, 255); border-radius:5px; border: 1px solid black; """)
            _nub.setStyleSheet(""" background: rgb(24, 144, 255); border-radius:5px; border: 1px solid black; """)
        else:
            _man_check.setStyleSheet(""" background: rgb(127, 127, 127); border-radius:5px; border: 1px solid black; """)
            _content.setStyleSheet(""" background: rgb(254, 245, 249); border-radius:5px; border: 1px solid black; """)
            _nub.setStyleSheet(""" background: rgb(254, 245, 249); border-radius:5px; border: 1px solid black; """)

        _step_widget.setFixedHeight(_content.height() + 5)

        # 상위 수준인 _item 에 _step_widget 을 추가함
        self.setItemWidget(_item, 0, _step_widget)
        return _content.height() + 5

    def _click_update_step(self, man_check: QPushButton, content: QLabel, nub: QLabel):
        """
        수동 확인 클릭 시 업데이트
            1. 수동 확인 버튼 클릭 시 번호, 절차서 부분의 색 변경
            2. 클릭된 수동 확인 버튼에 저장된 절차서명, 타입, 번호를 불러와서 메모리에 해당 부분 업데이트
        """
        # 1.
        if man_check.isChecked():
            man_check.setStyleSheet(""" background: rgb(38, 55, 96); border-radius:5px; border: 1px solid black; """)
            content.setStyleSheet(""" background: rgb(24, 144, 255); border-radius:5px; border: 1px solid black; """)
            nub.setStyleSheet(""" background: rgb(24, 144, 255); border-radius:5px; border: 1px solid black; """)
        else:
            man_check.setStyleSheet(""" background: rgb(127, 127, 127); border-radius:5px; border: 1px solid black; """)
            content.setStyleSheet(""" background: rgb(254, 245, 249); border-radius:5px; border: 1px solid black; """)
            nub.setStyleSheet(""" background: rgb(254, 245, 249); border-radius:5px; border: 1px solid black; """)
        # 2.
        self.mem.change_pro_mam_click(man_check._procedure, man_check._key, man_check._step, man_check.isChecked())

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
        for key in [self._type]:
            _top_level_item: QTreeWidgetItem = self.top_level_items[key]
            _steps = _info[key]     # key = 'Symptom Check'
            """
            _steps 는 해당 key 에 포함되어 있는 데이터임. step 은 0 부터 순회함.
            'Symptom Check': {
                0: {'ManClick': False, 'AutoClick': False, 'Nub': '1.1', 'Des': '정상'}
            }
            """
            tot, tot_auto = 0, 0
            accumulated_cell_h = 0
            for step in range(len(_steps)):
                accumulated_cell_h += self._make_item(_top_level_item, key, step, _steps[step]['Nub'],
                                                      _steps[step]['Des'],_steps[step]['AutoClick'],
                                                      _steps[step]['ManClick'])
                tot += 1
                tot_auto += 1 if _steps[step]['AutoClick'] else 0

        self.ProcedureStepsWarp.setFixedHeight(accumulated_cell_h + 35)