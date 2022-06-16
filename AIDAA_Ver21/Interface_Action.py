from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
import pandas as pd
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from CVCS.Core_mimic import CVCS


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
        self.Action_system_view_.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        lay.addWidget(self.Action_system_view_)

        # ---------------------------------
        # 단축키 섹션
        # ---------------------------------
        self.shortcut_save_scene = QShortcut(QKeySequence('Ctrl+S'), self, self.inmem.widget_ids['Action_system_scene'].save_scene)
        self.shortcut_load_scene = QShortcut(QKeySequence('Ctrl+L'), self, self.inmem.widget_ids['Action_system_scene'].load_scene)
        self.shortcut_show_sim__ = QShortcut(Qt.Key.Key_F1, self, self.show_controller)
        self.shortcut_move_item_up = QShortcut(Qt.Key.Key_Up, self, lambda: self.inmem.widget_ids['Action_system_scene'].move_item('up'))
        self.shortcut_move_item_up = QShortcut(Qt.Key.Key_Down, self, lambda: self.inmem.widget_ids['Action_system_scene'].move_item('down'))
        self.shortcut_move_item_up = QShortcut(Qt.Key.Key_Right, self, lambda: self.inmem.widget_ids['Action_system_scene'].move_item('right'))
        self.shortcut_move_item_up = QShortcut(Qt.Key.Key_Left, self, lambda: self.inmem.widget_ids['Action_system_scene'].move_item('left'))
        # ---------------------------------
        # CVCS Core
        # ---------------------------------
        self.CVCS = CVCS()
        self.TIME = 1           # 1: 1 Sec
        self.RUN = False        # 0: Freeze, 1: Run
        self.mal_info = {}
        
        self.widget_timer(100, [self.cvcs_run])
            
    def resizeEvent(self, a0) -> None:
        w, h = self.Action_system_view_.size().width(), self.Action_system_view_.size().height()
        self.Action_system_scene_.setSceneRect(QRectF(0, 0, w, h))
        return super().resizeEvent(a0)

    def update(self):
        self.Action_system_scene_.update()
        
    def show_controller(self):
        w = Action_system_controller(self)
        w.show()
        
    def cvcs_run(self):
        if self.RUN:
            self.CVCS.step()
            print(self.CVCS.mem['SimTime']['V'])
    
    def cvcs_call_run(self):
        self.RUN = False if self.RUN else True
        
    def cvcs_call_init(self):
        self.RUN = False
        self.CVCS.call_init()
        self.mal_info = {}

# =============================================================
# Mimic 화면 - CVCS 시뮬레이터 컨트롤러
# =============================================================

class Action_system_controller(ABCWidget):
    def __init__(self, parent):
        super(Action_system_controller, self).__init__(parent)
        self.setGeometry(0, 0, 100, 200)
        lay = QVBoxLayout(self)
        #------------------------------------------------------
        # Init + Run/Freeze
        layv1 = QHBoxLayout()
        self.init_btn = QPushButton("Init")
        self.init_btn.clicked.connect(self._click_init_btn)
        self.run_btn = QPushButton("Freeze")
        self.run_btn.clicked.connect(self._click_run_btn)
        layv1.addWidget(self.init_btn)
        layv1.addWidget(self.run_btn)
        lay.addLayout(layv1)
        #------------------------------------------------------
        # Mal
        
    def _click_init_btn(self):
        self.inmem.widget_ids['Action_system_mimic_area'].cvcs_call_init()
        self.run_btn.setText('Freeze')
    
    def _click_run_btn(self):
        self.inmem.widget_ids['Action_system_mimic_area'].cvcs_call_run()

# =============================================================
# Mimic 화면 - CVCS 화면
# =============================================================

class Action_system_scene(ABCGraphicsScene):
    def __init__(self, parent):
        super(Action_system_scene, self).__init__(parent)
        self.setBackgroundBrush(QColor(231, 231, 234))
        self.svg_render = QSvgRenderer('./CVCS/Core_comp.svg')
        self.load_scene()

    def save_scene(self):
        """
        현재 화면 저장 (Ctrl+S)
        """
        # Pipe line
        with open('./CVCS/Core_pip_info.csv', 'w') as f:
            f.writelines(f'Type,X1,Y1,X2,Y2,Opt\n')
            for item in self.items():
                if isinstance(item, Pipeline):
                    f.writelines(f'PIPE,{item.line().p1().x()},{item.line().p1().y()},{item.line().p2().x()},{item.line().p2().y()},{item.arrow_type}\n')
        # Non-item
        with open('./CVCS/Core_nonitem_info.csv', 'w') as f:
            f.writelines(f'Type,X1,Y1,Rota,Scal,Comment\n')
            for item in self.items():
                if isinstance(item, SVGnonitem):
                    f.writelines(f'{item.elementId()},{item.x()},{item.y()},{item.rotation()},{item.scale()},{item.comment}\n')

        print('현재 화면 저장')

    def load_scene(self):
        """
        저장 화면 불러오기 (Ctrl+L)
        """
        # If any items is added in scene, the items will be removed.
        for item in self.items():
            self.removeItem(item)
        # Draw
        self._update_line() # Update the pipes
        self._update_nonitem() # Update the non-item components
        print(f'{self.__module__}|CVCS 화면 로딩')

    def move_item(self, direction):
        # If one or more than one item is selected and Up key is pressed, the item selected will be moved up, down, right or left.
        for item in self.selectedItems():
            if direction == 'up':
                item.move_pos(0, -1)
            if direction == 'down':
                item.move_pos(0, 1)
            if direction == 'right':
                item.move_pos(1, 0)
            if direction == 'left':
                item.move_pos(-1, 0)

    def _update_line(self):
        # Load the pipe data from the CSV file
        info_ = pd.read_csv('./CVCS/Core_pip_info.csv')
        # Draw the pipe
        for idx, row in info_.iterrows():
            self.addItem(Pipeline(
                line=QLineF(float(row['X1']), float(row['Y1']), float(row['X2']), float(row['Y2'])), 
                pen=QPen(Qt.black, 3),
                arrow_type=int(row['Opt'])))

    def _update_nonitem(self):
        # Load the non-item component data from the CSV file
        info_ = pd.read_csv('./CVCS/Core_nonitem_info.csv')
        # Draw the non-item component
        for idx, row in info_.iterrows():
            self.addItem(SVGnonitem(
                x=float(row['X1']), y=float(row['Y1']), id=row['Type'], render=self.svg_render, 
                rota=row['Rota'], scal=row['Scal'], comment=row['Comment']
                ))

class Pipeline(QGraphicsLineItem):
    def __init__(self, line: QLineF, pen, arrow_type=0):
        self.line_info = line
        self.arrow_type = arrow_type

        super(Pipeline, self).__init__(line)

        self.setPen(pen)

        self.head_arrow = QGraphicsPolygonItem(QPolygonF([]), self)
        self.update_shape()

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)

        self.selected_line_pos = None
        self.selected_line = [False, False]

    def update_shape(self):
        if self.arrow_type == 0:
            arrow_points = QPolygonF([])
            transform = QTransform()
        elif self.arrow_type == 1:
            # Polygon
            arrow_points = QPolygonF([
                QPointF(self.line().p1().x() - 7, self.line().p1().y()),
                QPointF(self.line().p1().x() + 7, self.line().p1().y()),
                QPointF(self.line().p1().x(), self.line().p1().y() + 7),
            ])
            #
            transform = QTransform()
            transform.translate(self.line().p1().x(), self.line().p1().y())
            transform.rotate(- self.line().angle() + 90)
            transform.translate(-self.line().p1().x(), -self.line().p1().y())
        elif self.arrow_type == 2:
            # Polygon
            arrow_points = QPolygonF([
                QPointF(self.line().p2().x() - 7, self.line().p2().y()),
                QPointF(self.line().p2().x() + 7, self.line().p2().y()),
                QPointF(self.line().p2().x(), self.line().p2().y() + 7),
            ])
            #
            transform = QTransform()
            transform.translate(self.line().p2().x(), self.line().p2().y())
            transform.rotate(- self.line().angle() - 90)
            transform.translate(-self.line().p2().x(), -self.line().p2().y())

        self.head_arrow.setPolygon(arrow_points)
        self.head_arrow.setBrush(QBrush(Qt.black))
        self.head_arrow.setPen(QPen(Qt.black, 1))

        self.head_arrow.setTransform(transform)
        
    def move_pos(self, x, y):
        self.setLine(self.line().translated(x, y))
        self.update_shape()

class SVGnonitem(QGraphicsSvgItem):
    def __init__(self, x, y, id: str, render, rota, scal, comment, *args):
        super(SVGnonitem, self).__init__(*args)
        self.setSharedRenderer(render)
        self.setElementId(id)
        self.setX(x)
        self.setY(y)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setRotation(float(rota))
        self.setScale(float(scal))
        self.comment = comment

    # def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
    #     super(SVGnonitem, self).mousePressEvent(event)
    #     if event.buttons() == Qt.LeftButton:
    #         print(f'Get Press {self.pos().x()}, {self.pos().y()}')
    #         print(f'{self.boundingRect()}')

    def move_pos(self, x=0, y=0):
        self.setX(self.x() + x)
        self.setY(self.y() + y)
