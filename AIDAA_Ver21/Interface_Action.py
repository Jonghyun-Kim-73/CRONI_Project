from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *


class Action(ABCWidget):
    def __init__(self, parent):
        super(Action, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(100, 185, 211);')
        lay = QHBoxLayout(self)
        llay = QVBoxLayout()
        llay.addWidget(Action_alarm_area(self))
        llay.addWidget(Action_suggestion_area(self))
        rlay = QVBoxLayout()
        rlay.addWidget(Action_system_mimic_area(self))
        lay.addLayout(llay)
        lay.addLayout(rlay)

class Action_alarm_area(ABCTabWidget):
    def __init__(self, parent):
        super(Action_alarm_area, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(149, 185, 211);')
        lay = QVBoxLayout(self)

class Action_suggestion_area(ABCWidget):
    def __init__(self, parent):
        super(Action_suggestion_area, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(149, 100, 211);')      
        
# =============================================================
# Mimic 화면
# =============================================================
class Action_system_mimic_area(ABCWidget):
    def __init__(self, parent):
        super(Action_system_mimic_area, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(149, 100, 100);')
        
        lay = QVBoxLayout(self)
        self.Action_system_scene_ = Action_system_scene(self)
        self.Action_system_view_ = QGraphicsView(self.Action_system_scene_, self)
        self.Action_system_view_.setStyleSheet('border: 0px')
        lay.addWidget(self.Action_system_view_)

        # ---------------------------------
        # 단축키 섹션
        # ---------------------------------
        self.shortcut_save_scene = QShortcut(QKeySequence('Ctrl+S'), self, self.inmem.widget_ids['Action_system_scene'].save_scene)
        self.shortcut_load_scene = QShortcut(QKeySequence('Ctrl+L'), self, self.inmem.widget_ids['Action_system_scene'].load_scene)
        self.shortcut_move_item_up = QShortcut(Qt.Key.Key_Up, self, self.inmem.widget_ids['Action_system_scene'].move_item_up)

    def resizeEvent(self, a0) -> None:
        w, h = self.Action_system_view_.size().width(), self.Action_system_view_.size().height()
        self.Action_system_scene_.setSceneRect(QRectF(0, 0, w, h))
        return super().resizeEvent(a0)

    def update(self):
        self.Action_system_scene_.update()

class Action_system_scene(ABCGraphicsScene):
    def __init__(self, parent):
        super(Action_system_scene, self).__init__(parent)
        self.setBackgroundBrush(QColor(231, 231, 234))
        self.svg_render = QSvgRenderer('./CVCS/Core_comp.svg')

    def save_scene(self):
        """
        현재 화면 저장 (Ctrl+S)
        """
        print('현재 화면 저장')

    def load_scene(self):
        """
        저장 화면 불러오기 (Ctrl+L)
        """
        print('화면 로딩')

    def move_item_up(self):
        """
        선택된 아이템이 있는 경우 Up
        """
        print('아이템 Up')

    def _update_line(self):
        with open('./CVCS/Core_pip_info.csv', 'r') as f:
            info = f.read().split('\n')
            for info_item in info:
                if info_item != '':
                    info_line = info_item.split(',')
                    if info_line[1] == 'PIP':
                        self.addItem(PipLine(QLineF(float(info_line[2]), float(info_line[3]),
                                                    float(info_line[4]), float(info_line[5])),
                                             QPen(Qt.black, 3),
                                             int(info_line[6])))
            for info_item in info:
                if info_item != '':
                    info_line = info_item.split(',')
                    if info_line[1] != 'PIP':
                        self.addItem(SVGnonitem(float(info_line[2]), float(info_line[3]),
                                                info_line[1],
                                                self.svg_render,
                                                info_line[4],
                                                info_line[5],
                                                info_line[6]))