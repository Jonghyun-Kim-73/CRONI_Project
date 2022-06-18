from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
import pandas as pd

from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from CVCS.Core_mimic import CVCS

Top_CVCS = CVCS()
gray_a = QColor(191, 206, 220, 255)
alarm_a = QColor(255, 183, 0, 255)

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
        if True:
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
        self.CVCS = Top_CVCS
        self.TIME = 1           # 1: 1 Sec
        self.RUN = 'Freeze'     
        self.mal_info = {}
        self.timer_ = self.widget_timer(self.TIME * 1000, [self.cvcs_run]) # 1000 ms run = 1 sec
            
    def resizeEvent(self, a0) -> None:
        w, h = self.Action_system_view_.size().width(), self.Action_system_view_.size().height()
        self.Action_system_scene_.setSceneRect(QRectF(0, 0, w, h))
        return super().resizeEvent(a0)

    def update(self):
        self.Action_system_scene_.update()
        
    def show_controller(self):
        w = Action_system_controller(self)
        w.show()
    
    # ----------------------------------------------------------------
    # CVCS Control
    # ----------------------------------------------------------------

    def cvcs_run(self):
        if self.RUN == 'Run':
            if self.mal_info != {}:
                for mal_name in self.mal_info.keys():
                    if self.CVCS.mem['SimTime']['V'] == self.mal_info[mal_name]['Time']:
                        self.CVCS.mem[mal_name]['V'] = self.mal_info[mal_name]['Opti']
            self.CVCS.step()
            self.inmem.widget_ids['Action_system_scene'].update_scene()
            print(self.CVCS.mem['SimTime']['V'])
    
    def cvcs_call_run(self):
        self.RUN = 'Freeze' if self.RUN == 'Run' else 'Run'
        
    def cvcs_call_init(self):
        self.RUN = 'Freeze'
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
        if True:
            layh1 = QHBoxLayout()
            self.init_btn = QPushButton("Init")
            self.init_btn.clicked.connect(self._click_init_btn)
            self.run_btn = QPushButton(f"{self.inmem.widget_ids['Action_system_mimic_area'].RUN}")
            self.run_btn.clicked.connect(self._click_run_btn)
            layh1.addWidget(self.init_btn)
            layh1.addWidget(self.run_btn)
            lay.addLayout(layh1)
        #------------------------------------------------------
        # SimTime
        if True:
            layh2 = QHBoxLayout()
            self.sleep_time = QLineEdit(f"{self.inmem.widget_ids['Action_system_mimic_area'].TIME}")
            self.sleep_time.textChanged.connect(self._changed_sleep_time)
            self.sleep_time.setFixedWidth(30)
            sleep_label = QLabel("[Sec]")
            sleep_label.setFixedWidth(50)
            layh2.addWidget(self.sleep_time)
            layh2.addWidget(sleep_label)
            lay.addLayout(layh2)
        #------------------------------------------------------
        # Malfunction
        if True:
            self.mal_btn = QPushButton('Mal')
            self.mal_btn.clicked.connect(self._click_mal_btn)
            lay.addWidget(self.mal_btn)
        
    def _click_init_btn(self):
        self.inmem.widget_ids['Action_system_mimic_area'].cvcs_call_init()
        self.run_btn.setText('Freeze')
    
    def _click_run_btn(self):
        self.inmem.widget_ids['Action_system_mimic_area'].cvcs_call_run()
        self.run_btn.setText(f'{self.inmem.widget_ids["Action_system_mimic_area"].RUN}')

    def _changed_sleep_time(self):
        self.inmem.widget_ids['Action_system_mimic_area'].TIME = float(self.sleep_time.text())
        self.inmem.widget_ids['Action_system_mimic_area'].timer_.setInterval(float(self.sleep_time.text()) * 1000)
    
    def _click_mal_btn(self):
        print(self.inmem.widget_ids['Action_system_mimic_area'].mal_info)

        mal_list = []
        for key in self.inmem.widget_ids['Action_system_mimic_area'].CVCS.mem.keys():
            if 'MAL' in key:
                mal_list.append(key)

        ex = Malfun()
        if ex.exec_() == 0:
            if ex.mal_name_.text() in mal_list:
                try:
                    mal_time = float(ex.mal_time_.text())
                    mal_opti = float(ex.mal_opti_.text())
                    self.inmem.widget_ids['Action_system_mimic_area'].mal_info[ex.mal_name_.text()] = {'Time': mal_time, 'Opti': mal_opti}
                    print(self.inmem.widget_ids['Action_system_mimic_area'].mal_info)
                except:
                    print('Error')
            else:
                print('Error No Mal')
        
class Malfun(QDialog):
    def __init__(self):
        super(Malfun, self).__init__()
        self.setGeometry(0, 0, 200, 100)

        h1_layout = QHBoxLayout()
        h1_layout.setContentsMargins(0, 0, 0, 0)
        self.mal_name = QLabel('MAL_Name')
        self.mal_name.setFixedWidth(100)
        self.mal_name_ = QLineEdit()
        h1_layout.addWidget(self.mal_name)
        h1_layout.addWidget(self.mal_name_)

        h2_layout = QHBoxLayout()
        h2_layout.setContentsMargins(0, 0, 0, 0)
        self.mal_time = QLabel('MAL_Time')
        self.mal_time.setFixedWidth(100)
        self.mal_time_ = QLineEdit()
        h2_layout.addWidget(self.mal_time)
        h2_layout.addWidget(self.mal_time_)

        h3_layout = QHBoxLayout()
        h3_layout.setContentsMargins(0, 0, 0, 0)
        self.mal_opti = QLabel('MAL_Opti')
        self.mal_opti.setFixedWidth(100)
        self.mal_opti_ = QLineEdit()
        h3_layout.addWidget(self.mal_opti)
        h3_layout.addWidget(self.mal_opti_)

        v1_layout = QVBoxLayout()
        v1_layout.addLayout(h1_layout)
        v1_layout.addLayout(h2_layout)
        v1_layout.addLayout(h3_layout)
        self.setLayout(v1_layout)

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
        # Comp
        with open('./CVCS/Core_comp_info.csv', 'w') as f:
            f.writelines(f'Type,X1,Y1,Id,ControlType\n')
            for item in self.items():
                if isinstance(item, SVGitem):
                    f.writelines(f'{item.para_name},{item.x()},{item.y()},{item.elementId()},{item.control_type}\n')
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
        self._update_comp(init=True) # Update the components
        self._update_indi(init=True) # Update the indicators
        print(f'{self.__module__}|CVCS 화면 로딩')

    def update_scene(self):
        # comp 업데이트
        self._update_comp()
        self._update_indi()

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

    def _update_comp(self, init=False):
        if init:
            self.comp_dict = {}
            # Load the component data from the CSV file
            info_ = pd.read_csv('./CVCS/Core_comp_info.csv')
            # Draw the component
            for idx, row in info_.iterrows():
                self.comp_dict[row['Type']] = SVGitem(
                    x=float(row['X1']), y=float(row['Y1']), para_name=row['Type'], id=row['Id'], control_type=row['ControlType'],
                    render=self.svg_render
                    )
            # self.comp_dict = {
            #     'LV459': SVGitem(499.0, 326.0, 'LV459', 'valve_v_c', self.svg_render),
            # }
            # [self.addItem(instance_) for key, instance_ in self.comp_dict.items()]
            [self.addItem(instance_) for instance_ in self.comp_dict.values()]
        
        for comp_item in self.comp_dict.values():
            comp_item.dis_update()

    def _update_indi(self, init=False):
        if init:
            self.indicators_dict = {}
            # Load the component data from the CSV file
            info_ = pd.read_csv('./CVCS/Core_indi_info.csv')
            for idx, row in info_.iterrows():
                self.indicators_dict[row['Type']] = Indicator(
                    x=float(row['X1']), y=float(row['Y1']), para_name=row['Type'], indi_type=row['Id'], Comment=row['Comment']
                    )
            # self.indicators_dict = {
            #     'DEPRZ': Indicator(623, 366, 'L', 'DEPRZ', 'PZR Level'),
            # }
            [self.addItem(instance_) for instance_ in self.indicators_dict.values()]
        for indi_item in self.indicators_dict.values():
            indi_item.dis_update()

class Pipeline(QGraphicsLineItem):
    def __init__(self, line: QLineF, pen, arrow_type=0):
        self.line_info = line
        self.arrow_type = arrow_type

        super(Pipeline, self).__init__(line)

        self.setPen(pen)
        # Arrow type
        self.head_arrow = QGraphicsPolygonItem(QPolygonF([]), self)
        self.update_shape()    

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        
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

    def mousePressEvent(self, e: 'QGraphicsSceneMouseEvent'):
        super(Pipeline, self).mousePressEvent(e)
        if e.buttons() == Qt.RightButton:
            # Change Type
            self.arrow_type = 0 if self.arrow_type == 2 else self.arrow_type + 1
            self.update_shape()
        else:
            self.selected_line_pos = e.scenePos()

            line_: QLineF = self.line()
            val1 = line_.p1() - e.scenePos()
            val2 = line_.p2() - e.scenePos()

            if val1.manhattanLength() < 20:
                self.selected_line = [True, False]
            elif val2.manhattanLength() < 20:
                self.selected_line = [False, True]
            else:
                self.selected_line = [False, False]

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent):
        super(Pipeline, self).mouseMoveEvent(e)
        if e.buttons() == Qt.RightButton:
            pass
        else:
            delta = e.scenePos() - self.selected_line_pos
            line_: QLineF = self.line()

            if self.selected_line[0]:
                # 왼쪽 부분 클릭
                line_.setPoints(line_.p1() + delta, line_.p2())
            elif self.selected_line[1]:
                # 오른쪽 부분 클릭
                line_.setPoints(line_.p1(), line_.p2() + delta)
            else:
                line_.setPoints(line_.p1() + delta, line_.p2() + delta)

            self.setLine(line_)

            self.update_shape()

            self.selected_line_pos = e.scenePos()

            self.line().setPoints(self.line().p1() + delta, self.line().p2())

    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent):
        super(Pipeline, self).mouseReleaseEvent(e)
        # 15도씩
        line_: QLineF = self.line()

        fin_deg = 0
        for angle_, deg in zip(range(40, 360, 40), range(45, 360, 45)):
            if angle_ <= line_.angle() < angle_ + 40:
                fin_deg = deg

        line_.setAngle(fin_deg)

        self.setLine(line_)
        self.update_shape()
        self.selected_line_pos = None

    def paint(self, p: QPainter, opt: QStyleOptionGraphicsItem, widget=None):
        p.setRenderHint(QPainter.Antialiasing)
        super(Pipeline, self).paint(p, opt, widget)

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
        
class SVGitem(QGraphicsSvgItem):
    def __init__(self, x, y, para_name, id: str, control_type, render, *args):
        # 초기 Bounding Rect 선언
        self.CompType = id.split('_')[0]     # valve_v_h -> valve
        self.CompDirt = id.split('_')[1]     # valve_v_h -> v
        comp_size_hint = {
            'valve_v': {'x': -19, 'y': 0, 'w': 51, 'h': 46},
            'valve_h': {'x': -10, 'y': 0, 'w': 51, 'h': 28},
            'valve_b': {'x': -10, 'y': 0, 'w': 51, 'h': 46},
            'pump_r': {'x': -13, 'y': 0, 'w': 51, 'h': 45},
            'Btn_h': {'x': -22, 'y': 0, 'w': 70, 'h': 40},      # On / Off
            'Btn_v': {'x': -22, 'y': 0, 'w': 70, 'h': 40},      # Man / Auto
        }
        self.CompSizeX = comp_size_hint[f'{self.CompType}_{self.CompDirt}']['x']
        self.CompSizeY = comp_size_hint[f'{self.CompType}_{self.CompDirt}']['y']
        self.CompSizeW = comp_size_hint[f'{self.CompType}_{self.CompDirt}']['w']
        self.CompSizeH = comp_size_hint[f'{self.CompType}_{self.CompDirt}']['h']

        super(SVGitem, self).__init__(*args)
        self.setSharedRenderer(render)
        self.setElementId(id)
        self.setX(x)
        self.setY(y)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.alarm = False
        self.alarm_blink = False
        self.val_his = []
        self.para_name = para_name
        self.control_type = control_type

        # self.GP = Trend(para_name)

        # if control_type == 'PID':
        #     self.controller = PIDController(para_name)
        # elif control_type == 'ONOFF':
        #     self.controller = OnController(para_name)
        # elif control_type == 'REGULAR':
        #     self.controller = RegularController(para_name)

    def dis_update(self):
        # self.GP.update_val_his(MimicMem.CVCS.mem[self.para_name]['SF'])
        # self.controller.dis_update()
        val = Top_CVCS.mem[self.para_name]['V']

        if self.CompType == 'valve':
            if val >= 1:
                self.setElementId(f'{self.CompType}_{self.CompDirt}_o')
            elif val <= 0:
                self.setElementId(f'{self.CompType}_{self.CompDirt}_c')
            else:
                self.setElementId(f'{self.CompType}_{self.CompDirt}_h')
        if self.CompType == 'pump':
            if val == 1:
                self.setElementId(f'{self.CompType}_{self.CompDirt}_start')
            else:
                self.setElementId(f'{self.CompType}_{self.CompDirt}_stop')
        if self.CompType == 'Btn' and self.CompDirt == 'h':
            if val == 1:
                self.setElementId(f'{self.CompType}_{self.CompDirt}_ON')
            else:
                self.setElementId(f'{self.CompType}_{self.CompDirt}_OFF')
        if self.CompType == 'Btn' and self.CompDirt == 'v':
            if val == 1:
                self.setElementId(f'{self.CompType}_{self.CompDirt}_M')
            else:
                self.setElementId(f'{self.CompType}_{self.CompDirt}_A')

    def paint(self, p: QPainter, opt: 'QStyleOptionGraphicsItem', w: QWidget) -> None:
        super(SVGitem, self).paint(p, opt, w)
        # Name
        p.setBrush(QBrush(Qt.black))
        if self.CompType == 'valve':
            p.drawText(QRectF(self.CompSizeX, self.CompSizeH - 11, 51, 11), f'{self.para_name}',
                       QTextOption(Qt.AlignVCenter | Qt.AlignHCenter))
        elif self.CompType == 'Btn':
            p.drawText(QRectF(self.CompSizeX, self.CompSizeH - 11, 70, 11), f'{self.para_name}',
                       QTextOption(Qt.AlignVCenter | Qt.AlignHCenter))
        else:
            p.drawText(QRectF(self.CompSizeX, self.CompSizeH - 11, 50, 11), f'{self.para_name}',
                       QTextOption(Qt.AlignVCenter | Qt.AlignHCenter))

    def boundingRect(self) -> QRectF:
        return QRectF(self.CompSizeX, self.CompSizeY, self.CompSizeW, self.CompSizeH)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super(SVGitem, self).mousePressEvent(event)
        if event.buttons() == Qt.LeftButton:
            print(f'Get Press {self.pos().x()}, {self.pos().y()}')
            print(f'{self.boundingRect()}')
        if event.buttons() == Qt.RightButton:
            print('Show GP')
            # self.GP.show_with_pos(event.screenPos())
        if event.buttons() == Qt.MidButton:
            print('Show Controller')
            # self.controller.show(event.screenPos())

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super(SVGitem, self).mouseDoubleClickEvent(event)

    def move_pos(self, x=0, y=0):
        self.setX(self.x() + x)
        self.setY(self.y() + y)

class Indicator(QGraphicsRectItem):
    def __init__(self, x, y, para_name, indi_type, Comment):
        super(Indicator, self).__init__()
        self.setX(x)
        self.setY(y)
        self.w = 70
        self.h = 20
        self.setRect(QRectF(0, 0, self.w, self.h))
        self.setPen(QPen(Qt.NoPen))
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.inditype = indi_type
        self.alarm = False
        self.alarm_blink = False
        self.val_his = []
        self.para_name = para_name
        self.title_name = Comment
        # self.GP = Trend(title_name)
        self.call_draw = False

    def dis_update(self):
        # self.GP.update_val_his(MimicMem.CVCS.mem[self.para_name]['SF'])
        self.update()

    def paint(self, p: QPainter, opt: 'QStyleOptionGraphicsItem', w: QWidget) -> None:
        v = Top_CVCS.mem[self.para_name]["V"]
        if v > 100:
            v = v / 1e6

        if self.alarm:
            _ = p.setBrush(QBrush(alarm_a)) if self.alarm_blink else p.setBrush(QBrush(gray_a))
            self.alarm_blink = False if self.alarm_blink else True
        else:
            p.setBrush(QBrush(gray_a))
        p.drawRoundedRect(QRectF(20, 0, 50, 20), 2.0, 2.0)
        p.drawText(QRectF(20, 1, 47, 20), f'{v:8.4f}', QTextOption(Qt.AlignVCenter | Qt.AlignRight))

        p.drawRoundedRect(QRectF(0, 0, 20, 20), 2.0, 2.0)

        p.setBrush(QBrush(Qt.black))
        p.drawText(QRectF(0, 1, 20, 20), f'{self.inditype}', QTextOption(Qt.AlignVCenter | Qt.AlignHCenter))

        super(Indicator, self).paint(p, opt, w)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super(Indicator, self).mousePressEvent(event)
        if event.buttons() == Qt.LeftButton:
            print(f'Get Press {self.pos().x()}, {self.pos().y()}')
            print(f'{self.boundingRect()}')
        if event.buttons() == Qt.RightButton:
            print('Show GP')
            # self.GP.show_with_pos(event.screenPos())

    def move_pos(self, x=0, y=0):
        self.setX(self.x() + x)
        self.setY(self.y() + y)