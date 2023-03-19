import typing
import ast
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
import json

from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.CVCS.Core_CVCS_mem import *
from AIDAA_Ver21.Interface_QSS import *

TEST = True
MOVE = True
def CPrint(txt):
    if TEST: print(txt)
class ActionMimicArea(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        lay = QVBoxLayout(self)
        self.ActionMimicScene = ActionMimicScene(self)
        self.ActionMimicView = ActionMimicView(self, scene=self.ActionMimicScene)
        lay.addWidget(self.ActionMimicView)
        lay.setContentsMargins(0, 0, 0, 0)
        # ---------------------------------
        # 단축키 섹션
        # ---------------------------------
        self.shortcut_save_scene = QShortcut(QKeySequence('Ctrl+S'), self, self.inmem.widget_ids['ActionMimicScene'].save_scene)
        self.shortcut_load_scene = QShortcut(QKeySequence('Ctrl+L'), self, self.inmem.widget_ids['ActionMimicScene'].load_scene)
        self.shortcut_move_item_up = QShortcut(Qt.Key.Key_Up, self, lambda: self.inmem.widget_ids['ActionMimicScene'].move_item('up'))
        self.shortcut_move_item_down = QShortcut(Qt.Key.Key_Down, self, lambda: self.inmem.widget_ids['ActionMimicScene'].move_item('down'))
        self.shortcut_move_item_right = QShortcut(Qt.Key.Key_Right, self, lambda: self.inmem.widget_ids['ActionMimicScene'].move_item('right'))
        self.shortcut_move_item_left = QShortcut(Qt.Key.Key_Left, self, lambda: self.inmem.widget_ids['ActionMimicScene'].move_item('left'))
        self.shortcut_move_item_delete = QShortcut(Qt.Key.Key_Delete, self, self.inmem.widget_ids['ActionMimicScene'].delete_item)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.ActionMimicScene.setSceneRect(QRectF(0, 0, self.ActionMimicView.size().width(), self.ActionMimicView.size().height()))
class ActionMimicView(ABCGraphicsView):
    def __init__(self, parent, scene, widget_name=''):
        super().__init__(parent, widget_name)
        self.setScene(scene)
        self.setStyleSheet("border: 0px")
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
class ActionMimicScene(ABCGraphicsScene):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setBackgroundBrush(rgb_to_qCOLOR(LightGray))
        self.edit_mode = False # 처음 edit-mode False
        self.ItemBox = {}
        self.ItemAgs = {}
        
        self.load_scene()
        self.startTimer(600)

    def load_scene(self):
        """
        저장 화면 불러오기 (Ctrl+L)
        """
        print('MainMiddle Mimic 화면 Load')
        # If any items is added in scene, the items will be removed.
        for item in self.items():
            self.removeItem(item)
        # Background
        self.addItem(ActionMimicSceneBackground(self))
        # Edit Mode
        _ = self.addItem(ActionMimicSceneEditModeIndicator(self)) if self.edit_mode else None
        # load json file
        with open('./Interface_AIDAA_ActionMimic.json', encoding='UTF8') as f:
            self.ItemAgs = json.load(f)

        for id in self.ItemAgs:
            if self.ItemAgs[id]['CType'] in ['Pump', 'RCP']:
                self.ItemBox[id] = PumpG(self, self.ItemAgs[id])
            elif self.ItemAgs[id]['CType'] == 'Img':
                self.ItemBox[id] = ImgG(self, self.ItemAgs[id])
            elif self.ItemAgs[id]['CType'] == 'Pipe':
                self.ItemBox[id] = LineG(self, self.ItemAgs[id])
            elif self.ItemAgs[id]['CType'] == 'Indicator':
                self.ItemBox[id] = IndiG(self, self.ItemAgs[id])
            elif self.ItemAgs[id]['CType'] in ['Valve', 'TValve']:
                self.ItemBox[id] = ValveG(self, self.ItemAgs[id])
            self.addItem(self.ItemBox[id])
    
    def save_scene(self):
        """
        현재 화면 저장 (Ctrl+S)
        """
        with open('./Interface_AIDAA_ActionMimic.json', 'w') as f:
            for id in self.ItemBox.keys():
                self.ItemAgs[id] = self.ItemBox[id].args
            json.dump(self.ItemAgs, f, indent=2)
        print('MainMiddle Mimic 화면 Save')

    def move_item(self, direction):
        # If edit_mode is True, items can be moved.
        # If one or more than one item is selected and Up key is pressed, the item selected will be moved up, down, right or left.
        if self.edit_mode:
            for item in self.selectedItems():
                if direction == 'up':
                    item.move_pos(0, -1)
                if direction == 'down':
                    item.move_pos(0, 1)
                if direction == 'right':
                    item.move_pos(1, 0)
                if direction == 'left':
                    item.move_pos(-1, 0)

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        [item.update_state() for item in self.ItemBox.values()]
        return super().timerEvent(a0)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        print(event.scenePos())
        return super().mousePressEvent(event)

    def delete_item(self):
        print(len(self.ItemAgs))
        for id_ in self.selectedItems():
            del self.ItemAgs[id_.args['Id']]
            del self.ItemBox[id_.args['Id']]
        print(len(self.ItemAgs))
        self.save_scene()
        self.load_scene()

    def max_id_nub(self, id_type):
        id_type_list = [int(id_name[1:]) if id_name[0] == id_type else 0 for id_name in self.ItemAgs.keys()]
        if len(id_type_list) == 0:
            return 0
        else:
            return max([int(id_name[1:]) if id_name[0] == id_type else 0 for id_name in self.ItemAgs.keys()])
    
    def find_empty_id(self, id_type):
        """ id_type 중 비어 있거나 채워지지 않는 곳을 먼저 id로 주고 다 차있으면 id + 1 값 반환 """
        max_val = self.max_id_nub(id_type) + 1
        for i in range(max_val): # [0, 1, 2, ... ] 최대 번호 만큼 id 순회
            if not f'{id_type}{i}'in self.ItemAgs.keys():
                return f'{id_type}{i}'
        return f'{id_type}{max_val + 1}'

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        if len(self.selectedItems()) == 0:
            menu = QMenu()
            if self.edit_mode:
                pump      = menu.addAction('Add Pump')
                valv      = menu.addAction('Add Valve')
                pipe      = menu.addAction('Add Pipe')
                imgs      = menu.addAction('Add ImgComp')
                indi      = menu.addAction('Add Indicator')
                edit_mode = menu.addAction('Off Edit Mode')
                x = event.scenePos().x()
                y = event.scenePos().y()
                act = menu.exec(event.screenPos())
                if act == pump:
                    Id = f'{self.find_empty_id("P")}'
                    self.ItemAgs[Id] = {"Id": f"{Id}", "CType": "Pump", "x": x, "y": y, "direction": "R",
                                        "alarm_name": "iTestA", "comp_name": "TEMP", "para_name": "iTestS",
                                        "connected_id": []}
                elif act == valv:
                    Id = f'{self.find_empty_id("V")}'
                    self.ItemAgs[Id] = {"Id": f"{Id}", "CType": "Valve", "x": x, "y": y, "direction": "V",
                                        "alarm_name": "iTestA", "comp_name": "TEMP", "comp_name_direction": "Right", 
                                        "para_name": "iTestS", "connected_id": []}
                elif act == pipe:
                    Id = f'{self.find_empty_id("L")}'
                    self.ItemAgs[Id] = {"Id": f"{Id}", "CType": "Pipe", "x1": x, "y1": y, 
                                        "x2": x + 50, "y2": y + 50, "arrow": "true","connected_id": []}
                elif act == imgs:
                    Id = f'{self.find_empty_id("N")}'
                    self.ItemAgs[Id] = {"Id": f"{Id}", "CType": "Img", "x": x, "y": y, "img_name": "Sump",
                                        "direction": "V", "comp_name": "TEMP", "comp_name_direction": "Top",
                                        "comp_name_size": 16, "alarm_name": "iTestA"}
                elif act == indi:
                    Id = f'{self.find_empty_id("I")}'
                    self.ItemAgs[Id] = {"Id": f"{Id}", "CType": "Indicator", "x": x, "y": y, "unit": "%",
                                        "comp_name": "P", "comp_name_size": 16, "para_name": "iTestS",
                                        "alarm_name": "iTestA", "connected_id": []}
                elif act == edit_mode: self.edit_mode_trigger()
                # 매번 편집 후 Save와 Load 방지 용.
                if act in [pump, valv, pipe, imgs, indi, edit_mode]:
                    self.save_scene()
                    self.load_scene()
            else: # If self.edit_mode is False.
                edit_mode = menu.addAction('On Edit Mode')
                act = menu.exec(event.screenPos())
                if act == edit_mode: 
                    self.edit_mode_trigger()
                    self.load_scene()
        return super().contextMenuEvent(event)
    # One_line Functions
    def edit_mode_trigger(self): self.edit_mode = True if self.edit_mode != True else False
# ==========================================================================================
# Comp element
# ==========================================================================================
class ActionMimicSceneBackground(ABCGraphicsRectItem):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)

    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Outline RoundRect
        x = self.inmem.widget_ids['ActionMimicView'].rect().x() + 1
        y = self.inmem.widget_ids['ActionMimicView'].rect().y() + 1
        w = self.inmem.widget_ids['ActionMimicView'].rect().width() - 1 - 2
        h = self.inmem.widget_ids['ActionMimicView'].rect().height() -1 - 2
        painter.setPen(QPen(rgb_to_qCOLOR(DarkGray), 2, Qt.PenStyle.SolidLine))
        painter.drawRoundedRect(QRect(x, y, w, h), 10, 10)
        return super().paint(painter, option, widget)
class ActionMimicSceneEditModeIndicator(ABCGraphicsRectItem):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        # Outline RoundRect
        x = self.inmem.widget_ids['ActionMimicView'].rect().x() + 10
        y = self.inmem.widget_ids['ActionMimicView'].rect().y() + 10
        w = 100
        h = 30
        self.setRect(x, y, w, h)
    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setFont(QFont(Global_font, 10, weight=QFont.Bold))
        painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignHCenter, 'Edit Mode')
        return super().paint(painter, option, widget)
class BasicLabel(ABCGraphicsRectItem):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name)
        self.update_args(args)
        
    def update_args(self, args):
        self.CompName = args['unit']
        font_size = args['comp_name_size'] if 'comp_name_size' in args.keys() else Mimic_font_size_nub
        self.CompNameFont = QFont(Global_font, font_size, weight=QFont.Bold)
        self.CompNameFontMatrix = QFontMetrics(self.CompNameFont)
        self.CompNameWidth = self.CompNameFontMatrix.width(self.CompName)
        self.CompNameHight = self.CompNameFontMatrix.height()
        
        self.AlarmLineTick = 3
        self.DistAlarmToName = 2
        
        self.Width = self.AlarmLineTick * 2 + self.DistAlarmToName * 2 + self.CompNameWidth
        self.Hight = self.AlarmLineTick * 2 + self.DistAlarmToName * 2 + self.CompNameHight
        
        self.setRect(0, 0, self.Width, self.Hight)
        
    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget) -> None:
        painter.setFont(self.CompNameFont)
        painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignHCenter, self.CompName)
class CompLabel(ABCGraphicsRectItem):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name)
        self.update_args(args)
        self.blink = False
    
    def update_args(self, args):
        self.CompName = args['comp_name']
        font_size = args['comp_name_size'] if 'comp_name_size' in args.keys() else Mimic_font_size_nub
        self.CompNameFont = QFont(Global_font, font_size, weight=QFont.Bold)
        self.CompNameFontMatrix = QFontMetrics(self.CompNameFont)
        self.CompNameWidth = self.CompNameFontMatrix.width(self.CompName)
        self.CompNameHight = self.CompNameFontMatrix.height()
        
        self.AlarmLineTick = 3
        self.AlarmLineDist = 8
        self.DistAlarmToName = 2
        
        self.Width = self.AlarmLineTick * 2 + self.DistAlarmToName * 2 + self.CompNameWidth
        self.Hight = self.AlarmLineTick * 2 + self.DistAlarmToName * 2 + self.CompNameHight
        
        self.alarm_name = args['alarm_name']
        self.setRect(0, 0, self.Width, self.Hight)
        
    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget) -> None:
        painter.setFont(self.CompNameFont)
        painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignHCenter, self.CompName)
        
        alarm_state = self.inmem.ShMem.get_CVCS_para_val(f'{self.alarm_name}')
        if alarm_state == 0: painter.setPen(QPen(rgb_to_qCOLOR(DarkYellow), self.AlarmLineTick, Qt.PenStyle.SolidLine))
        if alarm_state == 1: painter.setPen(QPen(rgb_to_qCOLOR(DarkBlue), self.AlarmLineTick, Qt.PenStyle.SolidLine))
        if alarm_state == 2: painter.setPen(QPen(rgb_to_qCOLOR(DarkYellow), self.AlarmLineTick, Qt.PenStyle.SolidLine))
        
        if self.inmem.ShMem.get_CVCS_para_val(f'{self.alarm_name}') != 0:
            self.blink = not self.blink
            if self.blink:
                # TopLine
                painter.drawLine(0, self.AlarmLineTick, 13, self.AlarmLineTick)
                painter.drawLine(self.Width - 13, self.AlarmLineTick, self.Width, self.AlarmLineTick)
                # BottomLine
                painter.drawLine(0, self.Hight - self.AlarmLineTick, 13, self.Hight - self.AlarmLineTick)
                painter.drawLine(self.Width - 13, self.Hight - self.AlarmLineTick, self.Width, self.Hight - self.AlarmLineTick)
                # RightLine
                painter.drawLine(0, self.AlarmLineTick, 0, self.AlarmLineTick + 8)
                painter.drawLine(0, self.Hight - self.AlarmLineTick, 0, self.Hight - self.AlarmLineTick - 8)
                # LeftLine
                painter.drawLine(self.Width, self.AlarmLineTick, self.Width, self.AlarmLineTick + 8)
                painter.drawLine(self.Width, self.Hight - self.AlarmLineTick, self.Width, self.Hight - self.AlarmLineTick - 8)
                
                # middleLine
                middle_width = self.Width - (13 + self.AlarmLineDist) * 2
                middle_bar_w = (middle_width - self.AlarmLineDist) * 0.5
                
                painter.drawLine(13 + self.AlarmLineDist, self.AlarmLineTick, 13 + self.AlarmLineDist + middle_bar_w, self.AlarmLineTick) # top right
                painter.drawLine(self.Width - 13 - self.AlarmLineDist - middle_bar_w, self.AlarmLineTick, self.Width - 13 - self.AlarmLineDist, self.AlarmLineTick) # top left
                
                painter.drawLine(13 + self.AlarmLineDist, self.Hight - self.AlarmLineTick, 13 + self.AlarmLineDist + middle_bar_w, self.Hight - self.AlarmLineTick) # bottom right
                painter.drawLine(self.Width - 13 - self.AlarmLineDist - middle_bar_w, self.Hight - self.AlarmLineTick, self.Width - 13 - self.AlarmLineDist, self.Hight - self.AlarmLineTick) # bottom left
        else:
            self.blink = False
class SvgPump(ABCGraphicsSvgItem):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name)
        self.setSharedRenderer(QSvgRenderer('./Img/images.svg'))
        self.setScale(3.7795275591)
        assert args['direction'] == 'R' or args['direction'] == 'L', f'Pump direction error : {args["direction"]}'
        # ---------------------------
        self.setElementId(f'{args["CType"]}_Off')
        self.InPoint = QPointF(0, 0)
        self.OutPoint = QPointF(0, 0)
        self.update_args(args)
        
    def update_direction(self, direction):
        if direction == 'R':
            trans_f = QTransform()
            trans_f.scale(-1, 1)
            trans_f.translate(- self.Width, 0)
            self.setTransform(trans_f)
        else:
            pass # Original image is left direction

    def update_InOutPoints(self):
        self.InPoint.setX(self.sceneBoundingRect().x() if self.direction == 'R' else self.Width + self.sceneBoundingRect().x())
        self.InPoint.setY(19.5 + self.sceneBoundingRect().y())
        self.OutPoint.setX(self.Width + self.sceneBoundingRect().x() if self.direction == 'R' else self.sceneBoundingRect().x())
        self.OutPoint.setY(8.5 + self.sceneBoundingRect().y())
        
    def update_state(self, state):
        state = "On" if state == 1 else "Off"
        self.setElementId(f'{self.CType}_{state}')
    
    def update_args(self, args):
        self.setElementId(f'{args["CType"]}_Off')
        self.Hight = self.sceneBoundingRect().height()
        self.Width = self.sceneBoundingRect().width()
        self.direction = args['direction']
        self.CType = args['CType']
        self.update_direction(args['direction'])
class SvgValve(ABCGraphicsSvgItem):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name)
        self.setSharedRenderer(QSvgRenderer('./Img/images.svg'))
        self.setScale(3.7795275591)
        self.args = args
        assert self.args['direction'] == 'V' or self.args['direction'] == 'H', f'Pump direction error : {self.args["direction"]}'
        # ---------------------------
        self.setElementId(f'{self.args["CType"]}_{self.args["direction"]}_Off')
        self.Hight = self.sceneBoundingRect().height()
        self.Width = self.sceneBoundingRect().width()
        self.InPoint = QPointF(0, 0)
        self.OutPoint = QPointF(0, 0)
    
    def update_InOutPoints(self):
        self.InPoint.setX(self.sceneBoundingRect().x() + self.Width * 0.5 if self.args['direction'] == 'V' else self.sceneBoundingRect().x())
        self.InPoint.setY(self.sceneBoundingRect().y() if self.args['direction'] == 'V' else self.sceneBoundingRect().y() + self.Hight * 0.5)
        self.OutPoint.setX(self.sceneBoundingRect().x() + self.Width * 0.5 if self.args['direction'] == 'V' else self.sceneBoundingRect().x() + self.Width)
        self.OutPoint.setY(self.sceneBoundingRect().y() + self.Hight if self.args['direction'] == 'V' else self.sceneBoundingRect().y() + self.Hight * 0.5)
    
    def update_state(self, state):
        if state >= 1:
            state = "On"
        elif state <= 0:
            state = "Off"
        else:
            state = "Half"
        self.setElementId(f'{self.args["CType"]}_{self.args["direction"]}_{state}')
        
    def update_args(self, args):
        self.args = args
        self.setElementId(f'{self.args["CType"]}_{self.args["direction"]}_Off')
        self.Hight = self.sceneBoundingRect().height()
        self.Width = self.sceneBoundingRect().width()
class SvgImg(ABCGraphicsSvgItem):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name)
        self.setSharedRenderer(QSvgRenderer('./Img/images.svg'))
        self.setScale(3.7795275591)
        assert args['direction'] == 'V' or args['direction'] == 'H', f'Pump direction error : {args["direction"]}'
        # ---------------------------
        self.update_args(args)
    
    def update_InOutPoints(self):
        if self.args['img_name'] == 'HX':
            self.InPoint.setX(self.sceneBoundingRect().x() + self.Width * 0.5 if self.direction == 'V' else 0)
            self.InPoint.setY(0 if self.direction == 'V' else self.sceneBoundingRect().y() + self.Hight * 0.5)
            self.OutPoint.setX(self.sceneBoundingRect().x() + self.Width * 0.5 if self.direction == 'V' else self.sceneBoundingRect().x() + self.Width)
            self.OutPoint.setY(self.sceneBoundingRect().y() + self.Hight if self.direction == 'V' else self.sceneBoundingRect().y() + self.Hight * 0.5)
    
    def update_args(self, args):
        self.setElementId(f'{args["img_name"]}_{args["direction"]}')
        self.Hight = self.sceneBoundingRect().height()
        self.Width = self.sceneBoundingRect().width()
        self.InPoint = QPointF(0, 0)
        self.OutPoint = QPointF(0, 0)
        self.args = args
        self.direction = args['direction']
class Indicator(ABCGraphicsRectItem):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name)
        self.update_args(args)

    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget) -> None:
        val = self.inmem.ShMem.get_CVCS_para_val(self.ParaName)
        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(rgb_to_qCOLOR(DarkGray), Qt.BrushStyle.SolidPattern))
        painter.drawRoundedRect(self.boundingRect(), 5.0, 5.0)
        
        painter.setPen(QPen(rgb_to_qCOLOR(LightWhite), Qt.PenStyle.SolidLine))
        painter.setFont(self.ParaNameFont)
        painter.drawText(QRectF(self.boundingRect().x() + 2, 
                                self.boundingRect().y() + 2,
                                self.Width - 4,
                                self.Hight - 4,
                                ),
                         Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter, f'{val:.1f}')
    
    def update_args(self, args):
        self.ParaName = args['para_name']
        font_size = args['comp_name_size'] if 'comp_name_size' in args.keys() else Mimic_font_size_nub
        self.ParaNameFont = QFont(Global_font, font_size, weight=QFont.Bold)
        self.ParaNameFontMatrix = QFontMetrics(self.ParaNameFont)
        self.ParaNameWidth = self.ParaNameFontMatrix.width('0000.0')
        self.ParaNameHight = self.ParaNameFontMatrix.height()
        
        self.AlarmLineTick = 1
        self.DistAlarmToName = 1
        
        self.Width = self.AlarmLineTick * 2 + self.DistAlarmToName * 2 + self.ParaNameWidth
        self.Hight = self.AlarmLineTick * 2 + self.DistAlarmToName * 2 + self.ParaNameHight
        
        self.setRect(0, 0, self.Width, self.Hight)
# ==========================================================================================
# Comp package
# ==========================================================================================
class PumpG(ABCGraphicsItemGroup):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name='')
        self.DistCompToName = 1.5
        self.args = args
        self.compLabel = CompLabel(self, args)
        self.comp = SvgPump(self, args)
        #
        self.update_args(args)
        #        
        self.addToGroup(self.compLabel)
        self.addToGroup(self.comp)
        self.setFlag(QGraphicsItem.ItemIsSelectable, self.inmem.widget_ids['ActionMimicScene'].edit_mode)
        self.setFlag(QGraphicsItem.ItemIsMovable, self.inmem.widget_ids['ActionMimicScene'].edit_mode)
        self.setPos(self.args['x'], self.args['y'])
        self.flow = 0.0
    
    def update_state(self):
        val = self.inmem.ShMem.get_CVCS_para_val(self.args['para_name'])
        self.comp.update_state(val)
        self.compLabel.update()
        if self.args['connected_id'] != []:
            for line_id in self.args['connected_id']:
                if line_id in self.inmem.widget_ids['ActionMimicScene'].ItemBox.keys():
                    self.inmem.widget_ids['ActionMimicScene'].ItemBox[line_id].flow = val
                else:
                    CPrint(f"{self.args['Id']}와 {line_id} 가 연결되지 않음. Json 파일 수정 필요함.")
    
    def update_args(self, args):
        self.compLabel.update_args(args)
        self.comp.update_args(args)
        
        self.compLabel.setPos(0, self.comp.Hight + self.DistCompToName)
        x_ = 0 if self.comp.Width > self.compLabel.Width else (self.compLabel.Width - self.comp.Width) * 0.5
        self.comp.setPos(x_, 0)
        
        self.comp.update_InOutPoints()
        self.InPoint = self.comp.InPoint
        self.OutPoint = self.comp.OutPoint
    
    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        CPrint(f'{self.args["Id"]:_^50}')
        CPrint(f'이전 Pos  x: {self.args["x"]}, y: {self.args["y"]}')
        CPrint(f'최종 Pos  x: {self.pos().x()}, y: {self.pos().y()}')
        self.args["x"] = self.pos().x()
        self.args["y"] = self.pos().y()
        self.comp.update_InOutPoints()
        CPrint(f'입력 Pos  x: {self.InPoint.x()}, y: {self.InPoint.y()}')
        CPrint(f'출력 Pos  x: {self.OutPoint.x()}, y: {self.OutPoint.y()}')
        return super().mouseReleaseEvent(event)
    
    def move_pos(self, dx, dy):
        CPrint(f'{self.args["Id"]:_^50}')
        CPrint(f'이전 Pos  x: {self.args["x"]}, y: {self.args["y"]}')
        self.setPos(self.pos().x() + dx, self.pos().y() + dy)
        CPrint(f'최종 Pos  x: {self.pos().x()}, y: {self.pos().y()}')
        self.args["x"] = self.pos().x()
        self.args["y"] = self.pos().y()
        self.comp.update_InOutPoints()
    
    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        menu = QMenu()
        menu_items = []
        for key, val in self.args.items():
            w = QWidget()
            l = QHBoxLayout(w)
            in_l = QLabel(f'{key}')
            in_t = QLineEdit(f'{val}')
            w.in_l = in_l
            w.in_t = in_t
            l.addWidget(in_l)
            l.addWidget(in_t)

            wa = QWidgetAction(menu)
            wa.setDefaultWidget(w)
            menu.addAction(wa)
            menu_items.append(w)

        act = menu.exec(event.screenPos())
        for w_ in menu_items:
            if w_.in_l.text() == 'x':
                dx = float(w_.in_t.text()) - self.args[w_.in_l.text()]
                self.args[w_.in_l.text()] = float(w_.in_t.text())
            elif w_.in_l.text() == 'y':
                dy = float(w_.in_t.text()) - self.args[w_.in_l.text()]
                self.args[w_.in_l.text()] = float(w_.in_t.text())
            elif w_.in_l.text() == "connected_id":
                self.args[w_.in_l.text()] = ast.literal_eval(w_.in_t.text())
            elif w_.in_l.text() == "comp_name_size":
                self.args[w_.in_l.text()] = int(w_.in_t.text())
            else:
                self.args[w_.in_l.text()] = w_.in_t.text()
        self.move_pos(dx, dy)
        self.update_args(self.args)
class ValveG(ABCGraphicsItemGroup):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name)
        self.DistCompToName = 1.5
        self.args = args
        self.compLabel = CompLabel(self, args)
        self.comp = SvgValve(self, args)
        #
        self.update_args(args)
        #        
        self.addToGroup(self.compLabel)
        self.addToGroup(self.comp)
        self.setFlag(QGraphicsItem.ItemIsSelectable, self.inmem.widget_ids['ActionMimicScene'].edit_mode)
        self.setFlag(QGraphicsItem.ItemIsMovable, self.inmem.widget_ids['ActionMimicScene'].edit_mode)
        self.setPos(self.args['x'], self.args['y'])
        self.flow = 0.0
        
    def update_state(self):
        val = self.inmem.ShMem.get_CVCS_para_val(self.args['para_name'])
        self.comp.update_state(val)
        self.compLabel.update()
        if self.args['connected_id'] != []:
            for line_id in self.args['connected_id']:
                if line_id in self.inmem.widget_ids['ActionMimicScene'].ItemBox.keys():
                    self.inmem.widget_ids['ActionMimicScene'].ItemBox[line_id].flow = val
                else:
                    CPrint(f"{self.args['Id']}와 {line_id} 가 연결되지 않음. Json 파일 수정 필요함.")
    
    def update_args(self, args):
        self.compLabel.update_args(self.args)
        self.comp.update_args(self.args)
        
        if args["comp_name_direction"] == 'Right':
            self.comp.setPos(0, 0)
            self.compLabel.setPos(self.comp.Width + self.DistCompToName * 3, (self.comp.Hight - self.compLabel.Hight) * 0.5)
        elif args["comp_name_direction"] == 'Bottom':
            self.compLabel.setPos(0, self.comp.Hight + self.DistCompToName)
            x_ = 0 if self.comp.Width > self.compLabel.Width else (self.compLabel.Width - self.comp.Width) * 0.5
            self.comp.setPos(x_, 0)
                
        self.comp.update_InOutPoints()
        self.InPoint = self.comp.InPoint
        self.OutPoint = self.comp.OutPoint
    
    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        CPrint(f'{self.args["Id"]:_^50}')
        CPrint(f'이전 Pos  x: {self.args["x"]}, y: {self.args["y"]}')
        CPrint(f'최종 Pos  x: {self.pos().x()}, y: {self.pos().y()}')
        self.args["x"] = self.pos().x()
        self.args["y"] = self.pos().y()
        self.comp.update_InOutPoints()
        CPrint(f'입력 Pos  x: {self.InPoint.x()}, y: {self.InPoint.y()}')
        CPrint(f'출력 Pos  x: {self.OutPoint.x()}, y: {self.OutPoint.y()}')
        return super().mouseReleaseEvent(event)
    
    def move_pos(self, dx, dy):
        CPrint(f'{self.args["Id"]:_^50}')
        CPrint(f'이전 Pos  x: {self.args["x"]}, y: {self.args["y"]}')
        self.setPos(self.pos().x() + dx, self.pos().y() + dy)
        CPrint(f'최종 Pos  x: {self.pos().x()}, y: {self.pos().y()}')
        self.args["x"] = self.pos().x()
        self.args["y"] = self.pos().y()
        self.comp.update_InOutPoints()

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        menu = QMenu()
        menu_items = []
        for key, val in self.args.items():
            w = QWidget()
            l = QHBoxLayout(w)
            in_l = QLabel(f'{key}')
            in_t = QLineEdit(f'{val}')
            w.in_l = in_l
            w.in_t = in_t
            l.addWidget(in_l)
            l.addWidget(in_t)

            wa = QWidgetAction(menu)
            wa.setDefaultWidget(w)
            menu.addAction(wa)
            menu_items.append(w)

        act = menu.exec(event.screenPos())
        for w_ in menu_items:
            if w_.in_l.text() == 'x':
                dx = float(w_.in_t.text()) - self.args[w_.in_l.text()]
                self.args[w_.in_l.text()] = float(w_.in_t.text())
            elif w_.in_l.text() == 'y':
                dy = float(w_.in_t.text()) - self.args[w_.in_l.text()]
                self.args[w_.in_l.text()] = float(w_.in_t.text())
            elif w_.in_l.text() == "connected_id":
                self.args[w_.in_l.text()] = ast.literal_eval(w_.in_t.text())
            elif w_.in_l.text() == "comp_name_size":
                self.args[w_.in_l.text()] = int(w_.in_t.text())
            else:
                self.args[w_.in_l.text()] = w_.in_t.text()
        self.move_pos(dx, dy)
        self.update_args(self.args)
class ImgG(ABCGraphicsItemGroup):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name)
        self.DistCompToName = 1.5
        self.args = args
        self.compLabel = CompLabel(self, args)
        self.comp = SvgImg(self, args)
        #
        self.update_args(args)
        #
        self.addToGroup(self.comp)
        self.addToGroup(self.compLabel)
        self.setFlag(QGraphicsItem.ItemIsSelectable, self.inmem.widget_ids['ActionMimicScene'].edit_mode)
        self.setFlag(QGraphicsItem.ItemIsMovable, self.inmem.widget_ids['ActionMimicScene'].edit_mode)
        self.setPos(self.args['x'], self.args['y'])
        self.flow = 0.0

    def update_state(self):
        self.compLabel.update()
    
    def update_args(self, args):
        self.compLabel.update_args(args)
        
        if args["comp_name_direction"] == 'Right':
            self.comp.setPos(0, 0)
            self.compLabel.setPos(self.comp.Width + self.DistCompToName * 3, (self.comp.Hight - self.compLabel.Hight) * 0.5)
        elif args["comp_name_direction"] == 'Top':
            self.comp.setPos(0, 0)
            if self.comp.Width > self.compLabel.Width:
                self.compLabel.setPos(self.comp.Width * 0.5 - self.compLabel.Width * 0.5, self.DistCompToName * 2)
            else:
                self.compLabel.setPos(-(self.compLabel.Width - self.comp.Width) * 0.5, self.DistCompToName * 2)
        elif args["comp_name_direction"] == 'Center':
            self.comp.setPos(0, 0)
            if self.comp.Width > self.compLabel.Width:
                self.compLabel.setPos(self.comp.Width * 0.5 - self.compLabel.Width * 0.5, self.compLabel.Hight * 0.5 + self.DistCompToName)
            else:
                self.compLabel.setPos(-(self.compLabel.Width - self.comp.Width) * 0.5, self.compLabel.Hight * 0.5 + self.DistCompToName)
        self.comp.update_InOutPoints()
        self.InPoint = self.comp.InPoint
        self.OutPoint = self.comp.OutPoint
    
    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        CPrint(f'{self.args["Id"]:_^50}')
        CPrint(f'이전 Pos  x: {self.args["x"]}, y: {self.args["y"]}')
        CPrint(f'최종 Pos  x: {self.pos().x()}, y: {self.pos().y()}')
        self.args["x"] = self.pos().x()
        self.args["y"] = self.pos().y()
        self.comp.update_InOutPoints()
        CPrint(f'입력 Pos  x: {self.InPoint.x()}, y: {self.InPoint.y()}')
        CPrint(f'출력 Pos  x: {self.OutPoint.x()}, y: {self.OutPoint.y()}')
        return super().mouseReleaseEvent(event)
    
    def move_pos(self, dx, dy):
        CPrint(f'{self.args["Id"]:_^50}')
        CPrint(f'이전 Pos  x: {self.args["x"]}, y: {self.args["y"]}')
        self.setPos(self.pos().x() + dx, self.pos().y() + dy)
        CPrint(f'최종 Pos  x: {self.pos().x()}, y: {self.pos().y()}')
        self.args["x"] = self.pos().x()
        self.args["y"] = self.pos().y()
        self.comp.update_InOutPoints()

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        menu = QMenu()
        menu_items = []
        for key, val in self.args.items():
            w = QWidget()
            l = QHBoxLayout(w)
            in_l = QLabel(f'{key}')
            in_t = QLineEdit(f'{val}')
            w.in_l = in_l
            w.in_t = in_t
            l.addWidget(in_l)
            l.addWidget(in_t)

            wa = QWidgetAction(menu)
            wa.setDefaultWidget(w)
            menu.addAction(wa)
            menu_items.append(w)

        act = menu.exec(event.screenPos())
        for w_ in menu_items:
            if w_.in_l.text() == 'x':
                dx = float(w_.in_t.text()) - self.args[w_.in_l.text()]
                self.args[w_.in_l.text()] = float(w_.in_t.text())
            elif w_.in_l.text() == 'y':
                dy = float(w_.in_t.text()) - self.args[w_.in_l.text()]
                self.args[w_.in_l.text()] = float(w_.in_t.text())
            elif w_.in_l.text() == "connected_id":
                self.args[w_.in_l.text()] = ast.literal_eval(w_.in_t.text())
            elif w_.in_l.text() == "comp_name_size":
                self.args[w_.in_l.text()] = int(w_.in_t.text())
            else:
                self.args[w_.in_l.text()] = w_.in_t.text()
        self.move_pos(dx, dy)
        self.update_args(self.args)
class IndiG(ABCGraphicsItemGroup):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name)
        self.DistCompToName = 1.5
        self.args = args
        self.compLabel = CompLabel(self, args)
        self.unitLabel = BasicLabel(self, args)
        self.comp = Indicator(self, args)
        #
        self.update_args(args)
        #
        self.addToGroup(self.compLabel)
        self.addToGroup(self.comp)
        self.addToGroup(self.unitLabel)
        self.setFlag(QGraphicsItem.ItemIsSelectable, self.inmem.widget_ids['ActionMimicScene'].edit_mode)
        self.setFlag(QGraphicsItem.ItemIsMovable, self.inmem.widget_ids['ActionMimicScene'].edit_mode)
        self.setPos(self.args['x'], self.args['y'])
        #
        self.flow = 0.0

    def update_state(self):
        val = self.inmem.ShMem.get_CVCS_para_val(self.args['para_name'])
        self.comp.update()
        self.compLabel.update()
        self.unitLabel.update()
        if self.args['connected_id'] != []:
            for line_id in self.args['connected_id']:
                if line_id in self.inmem.widget_ids['ActionMimicScene'].ItemBox.keys():
                    self.inmem.widget_ids['ActionMimicScene'].ItemBox[line_id].flow = val
                else:
                    CPrint(f"{self.args['Id']}와 {line_id} 가 연결되지 않음. Json 파일 수정 필요함.")
    
    def update_args(self, args):
        self.compLabel.update_args(args)
        self.unitLabel.update_args(args)
        self.comp.update_args(args)
        
        self.compLabel.setPos(0, 0)
        self.comp.setPos(self.compLabel.Width + self.DistCompToName * 3, (self.compLabel.Hight - self.comp.Hight) * 0.5)
        self.unitLabel.setPos(self.comp.pos().x() + self.comp.Width + self.DistCompToName, 0)
    
    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        CPrint(f'{self.args["Id"]:_^50}')
        CPrint(f'이전 Pos  x: {self.args["x"]}, y: {self.args["y"]}')
        CPrint(f'최종 Pos  x: {self.pos().x()}, y: {self.pos().y()}')
        self.args["x"] = self.pos().x()
        self.args["y"] = self.pos().y()
        return super().mouseReleaseEvent(event)
    
    def move_pos(self, dx, dy):
        CPrint(f'{self.args["Id"]:_^50}')
        CPrint(f'이전 Pos  x: {self.args["x"]}, y: {self.args["y"]}')
        self.setPos(self.pos().x() + dx, self.pos().y() + dy)
        CPrint(f'최종 Pos  x: {self.pos().x()}, y: {self.pos().y()}')
        self.args["x"] = self.pos().x()
        self.args["y"] = self.pos().y()

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        menu = QMenu()
        menu_items = []
        for key, val in self.args.items():
            w = QWidget()
            l = QHBoxLayout(w)
            in_l = QLabel(f'{key}')
            in_t = QLineEdit(f'{val}')
            w.in_l = in_l
            w.in_t = in_t
            l.addWidget(in_l)
            l.addWidget(in_t)

            wa = QWidgetAction(menu)
            wa.setDefaultWidget(w)
            menu.addAction(wa)
            menu_items.append(w)

        act = menu.exec(event.screenPos())
        for w_ in menu_items:
            if w_.in_l.text() == 'x':
                dx = float(w_.in_t.text()) - self.args[w_.in_l.text()]
                self.args[w_.in_l.text()] = float(w_.in_t.text())
            elif w_.in_l.text() == 'y':
                dy = float(w_.in_t.text()) - self.args[w_.in_l.text()]
                self.args[w_.in_l.text()] = float(w_.in_t.text())
            elif w_.in_l.text() == "connected_id":
                self.args[w_.in_l.text()] = ast.literal_eval(w_.in_t.text())
            elif w_.in_l.text() == "comp_name_size":
                self.args[w_.in_l.text()] = int(w_.in_t.text())
            else:
                self.args[w_.in_l.text()] = w_.in_t.text()
        self.move_pos(dx, dy)
        self.update_args(self.args)
# ==========================================================================================
# Line elements and package
# ==========================================================================================
class ArrowHead(ABCGraphicsPolygonItem):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name)
        self.update_arrow(args)

    def update_arrow(self, args):
        if args['arrow'] == 'True':
            self.setPolygon(QPolygonF([QPointF(-5, 0), QPointF(5, 0), QPointF(0, 10)]))
        else:
            self.setPolygon(QPolygonF([QPointF(-5, 0), QPointF(5, 0)]))
        self.setBrush(QBrush(rgb_to_qCOLOR(DarkGray), Qt.BrushStyle.SolidPattern))
        self.setPen(QPen(Qt.PenStyle.NoPen))
        self.setPos(QPointF(args['x2'], args['y2']))
        self.setRotation(- QLineF(QPointF(args['x1'], args['y1']), QPointF(args['x2'], args['y2'])).angle() - 90)
    
    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget: typing.Optional[QWidget] = ...) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        return super().paint(painter, option, widget)
class PipeLines(ABCGraphicsLineItem):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name)
        self.setPen(QPen(rgb_to_qCOLOR(DarkGray), 3))
        self.update_lines(args)
    
    def update_lines(self, args):
        self.setLine(args['x1'], args['y1'], args['x2'], args['y2'])
class LineG(ABCGraphicsItemGroup):
    def __init__(self, parent, args, widget_name=''):
        super().__init__(parent, widget_name)
        self.args = args
        self.Pipe = PipeLines(self, args)
        self.Arrowhead = ArrowHead(self, args)
        self.addToGroup(self.Pipe)
        self.addToGroup(self.Arrowhead)
        self.setFlag(QGraphicsItem.ItemIsSelectable, self.inmem.widget_ids['ActionMimicScene'].edit_mode)
        self.setFlag(QGraphicsItem.ItemIsMovable, self.inmem.widget_ids['ActionMimicScene'].edit_mode)
        self.flow = 0.0
        
    def update_state(self):
        if self.flow > 0:
            self.flow = 1 if self.flow >= 1 else self.flow
            self.Arrowhead.setBrush(QBrush(rgb_to_qCOLOR(LightWhite), Qt.BrushStyle.SolidPattern))
            self.Pipe.setPen(QPen(rgb_to_qCOLOR(LightWhite), 3))
        else:
            self.Arrowhead.setBrush(QBrush(rgb_to_qCOLOR(DarkGray), Qt.BrushStyle.SolidPattern))
            self.Pipe.setPen(QPen(rgb_to_qCOLOR(DarkGray), 3))
            
        self.update()
        
        if self.args['connected_id'] != []:
            for line_id in self.args['connected_id']:
                if line_id in self.inmem.widget_ids['ActionMimicScene'].ItemBox.keys():
                    self.inmem.widget_ids['ActionMimicScene'].ItemBox[line_id].flow += self.flow
                else:
                    CPrint(f"{self.args['Id']}와 {line_id} 가 연결되지 않음. Json 파일 수정 필요함.")
                    
    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        CPrint(f'{self.args["Id"]:_^50}')
        CPrint(f'이전 Pos  x1: {self.args["x1"]}, \
                           x2: {self.args["x2"]}, \
                           y1: {self.args["y1"]}, \
                           y2: {self.args["y2"]}, \
                           ')
        CPrint(f'Line Pos  x1: {self.Pipe.line().p1().x()}, \
                           x2: {self.Pipe.line().p2().x()}, \
                           y1: {self.Pipe.line().p1().y()}, \
                           y2: {self.Pipe.line().p2().y()}, \
                           ')
        CPrint(f'최종 Pos  x1: {self.Pipe.line().p1().x() + self.pos().x()}, \
                           x2: {self.Pipe.line().p2().x() + self.pos().x()}, \
                           y1: {self.Pipe.line().p1().y() + self.pos().y()}, \
                           y2: {self.Pipe.line().p2().y() + self.pos().y()}, \
                           ')

        self.args["x1"] = self.Pipe.line().p1().x() + self.pos().x()
        self.args["x2"] = self.Pipe.line().p2().x() + self.pos().x()
        self.args["y1"] = self.Pipe.line().p1().y() + self.pos().y()
        self.args["y2"] = self.Pipe.line().p2().y() + self.pos().y()

        self.Pipe.update_lines(self.args)
        self.Arrowhead.update_arrow(self.args)
        # 아이템 제거 후 재 그리기?
        self.removeFromGroup(self.Pipe)
        self.removeFromGroup(self.Arrowhead)

        self.addToGroup(self.Pipe)
        self.addToGroup(self.Arrowhead)
        self.setPos(0, 0)

        return super().mouseReleaseEvent(event)
    
    def move_pos(self, dx, dy):
        CPrint(f'{self.args["Id"]:_^50}')
        CPrint(f'이전 Pos  x1: {self.args["x1"]}, \
                           x2: {self.args["x2"]}, \
                           y1: {self.args["y1"]}, \
                           y2: {self.args["y2"]}, \
                           ')
        self.setPos(self.pos().x() + dx, self.pos().y() + dy)
        CPrint(f'최종 Pos  x1: {self.Pipe.line().p1().x() + self.pos().x()}, \
                           x2: {self.Pipe.line().p2().x() + self.pos().x()}, \
                           y1: {self.Pipe.line().p1().y() + self.pos().y()}, \
                           y2: {self.Pipe.line().p2().y() + self.pos().y()}, \
                           ')
        self.args["x1"] = self.Pipe.line().p1().x() + self.pos().x()
        self.args["x2"] = self.Pipe.line().p2().x() + self.pos().x()
        self.args["y1"] = self.Pipe.line().p1().y() + self.pos().y()
        self.args["y2"] = self.Pipe.line().p2().y() + self.pos().y()

        self.Pipe.update_lines(self.args)
        self.Arrowhead.update_arrow(self.args)
        # 아이템 제거 후 재 그리기?
        self.removeFromGroup(self.Pipe)
        self.removeFromGroup(self.Arrowhead)

        self.addToGroup(self.Pipe)
        self.addToGroup(self.Arrowhead)
        self.setPos(0, 0)

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        menu = QMenu()
        menu_items = []
        for key, val in self.args.items():
            w = QWidget()
            l = QHBoxLayout(w)
            in_l = QLabel(f'{key}')
            in_t = QLineEdit(f'{val}')
            w.in_l = in_l
            w.in_t = in_t
            l.addWidget(in_l)
            l.addWidget(in_t)

            wa = QWidgetAction(menu)
            wa.setDefaultWidget(w)
            menu.addAction(wa)
            menu_items.append(w)

        act = menu.exec(event.screenPos())

        for w_ in menu_items:
            if w_.in_l.text() in ['x1', 'x2', 'y1', 'y2']:
                self.args[w_.in_l.text()] = float(w_.in_t.text())
            elif w_.in_l.text() == "connected_id":
                try:
                    self.args[w_.in_l.text()] = ast.literal_eval(w_.in_t.text())
                except:
                    print(f'잘못된 입력 {w_.in_t.text()}')
            elif w_.in_l.text() == "comp_name_size":
                self.args[w_.in_l.text()] = int(w_.in_t.text())
            else:
                self.args[w_.in_l.text()] = w_.in_t.text()

        self.Pipe.update_lines(self.args)
        self.Arrowhead.update_arrow(self.args)
        # 아이템 제거 후 재 그리기?
        self.removeFromGroup(self.Pipe)
        self.removeFromGroup(self.Arrowhead)
        self.addToGroup(self.Pipe)
        self.addToGroup(self.Arrowhead)
        self.setPos(0, 0)