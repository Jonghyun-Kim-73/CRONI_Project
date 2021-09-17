import os
import sys
import math
import json
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer


# ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainSysRightArea(QGraphicsView):
    def __init__(self, parent, x, y, w, h):
        super(MainSysRightArea, self).__init__(parent)
        self.mem = parent.mem if parent is not None else None
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setObjectName('MainSysRightArea')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        self.setFixedHeight(h)
        self.setFixedWidth(w)
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        self.setFrameShape(QFrame.NoFrame)
        self._scene = MainSysRightScene(self)
        self.setScene(self._scene)
        self._scene.clear()
        self._scene.setSceneRect(0, 0, w, h)
        self.setMinimumSize(w, h)

        self.update_sys_mimic('CVCS')

    def update_sys_mimic(self, target_sys):
        self._scene.clear()
        self._scene.update_sys_mimic(target_sys)

    def keyPressEvent(self, QKeyEvent):
        super(MainSysRightArea, self).keyPressEvent(QKeyEvent)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super(MainSysRightArea, self).mousePressEvent(event)


class MainSysRightScene(QGraphicsScene):
    def __init__(self, parent):
        super(MainSysRightScene, self).__init__(parent)
        self.mem = parent.mem
        self.setBackgroundBrush(QColor(254, 245, 249))   # Back gorund color
        # SVG render ---------------------------------------------------------------------------------------------------
        self.svg_render = QSvgRenderer('./interface_image/comp.svg')
        # Sys page info ------------------------------------------------------------------------------------------------
        self.target_sys = ''
        with open('./interface_image/MMI.json', 'r', encoding='UTF-8-sig') as f:
            self.sys_mimic_info = json.load(f)

        self.current_opened_control_board = None

    def keyPressEvent(self, QKeyEvent):
        super(MainSysRightScene, self).keyPressEvent(QKeyEvent)
        if self.selectedItems() is not None:
            if QKeyEvent.key() == Qt.Key_Up:
                self.selectedItems()[0].setY(int(self.selectedItems()[0].y() - 1))
            elif QKeyEvent.key() == Qt.Key_Down:
                self.selectedItems()[0].setY(int(self.selectedItems()[0].y() + 1))
            elif QKeyEvent.key() == Qt.Key_Right:
                self.selectedItems()[0].setX(int(self.selectedItems()[0].x() + 1))
            elif QKeyEvent.key() == Qt.Key_Right:
                self.selectedItems()[0].setX(int(self.selectedItems()[0].x() - 1))

    def update_sys_mimic(self, target_sys):
        # 이전 아이템 제거
        for item in self.items():
            self.removeItem(item)

        # 시스템 외부 테두리와 제목 표기 Not Move
        self.boundary_item = BoundaryComp(self)
        print(self.boundary_item)
        self.addItem(self.boundary_item)

        # 하위 파이프, 기기, 등등 이 들어감.
        self.target_sys = target_sys
        _sys = self.sys_mimic_info[target_sys]
        for key in _sys.keys():
            if self.sys_mimic_info[self.target_sys][key]['type'] in ['valve', 'pump', 'HP', 'RVP', 'PZR']:
                item = SVGComp(self.svg_render, key, self)
                item.setZValue(1)
            else:
                item = LineComp(key, self)
                item.setZValue(0)
            self.addItem(item)

    def contextMenuEvent(self, event) -> None:
        item = self.itemAt(event.scenePos().toPoint(), QTransform())
        if item is not None and item != self.boundary_item:
            item.contextMenuEvent(event)
        else:
            menu = QMenu()
            # -----------------------------------------------------
            save_all = menu.addAction("SaveMMI")
            load_all = menu.addAction("LoadMMI")
            add_pump = menu.addAction("AddPump")
            add_valve = menu.addAction("AddValve")
            add_line = menu.addAction("AddLine")
            add_hp = menu.addAction("AddHP")
            add_RVP = menu.addAction("AddRVP")
            add_PZR = menu.addAction("AddPZR")
            save_all.triggered.connect(self.save_all_mmi)
            load_all.triggered.connect(self.load_all_mmi)
            add_pump.triggered.connect(lambda a, type='pump', pos=event.scenePos(): self.add_comp(type, pos))
            add_valve.triggered.connect(lambda a, type='valve', pos=event.scenePos(): self.add_comp(type, pos))
            add_line.triggered.connect(lambda a, type='line', pos=event.scenePos(): self.add_comp(type, pos))
            add_hp.triggered.connect(lambda a, type='HP', pos=event.scenePos(): self.add_comp(type, pos))
            add_RVP.triggered.connect(lambda a, type='RVP', pos=event.scenePos(): self.add_comp(type, pos))
            add_PZR.triggered.connect(lambda a, type='PZR', pos=event.scenePos(): self.add_comp(type, pos))
            # -----------------------------------------------------
            menu.exec_(event.screenPos())

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        item = self.itemAt(event.scenePos().toPoint(), QTransform())

        if item is not None and item != self.boundary_item:


        super(MainSysRightScene, self).mousePressEvent(event)

    def save_all_mmi(self):
        print('SaveMMI')
        with open('./interface_image/MMI.json', 'w', encoding='UTF-8-sig') as file:
            file.write(json.dumps(self.sys_mimic_info, ensure_ascii=False, indent="\t"))

    def load_all_mmi(self):
        print('LoadMMI')
        with open('./interface_image/MMI.json', 'r', encoding='UTF-8-sig') as f:
            self.sys_mimic_info = json.load(f)
        # update 현재 화면
        self.update_sys_mimic(self.target_sys)

    def add_comp(self, type, pos):
        max_nub = len(self.sys_mimic_info[self.target_sys].keys())
        if type == 'line':
            self.sys_mimic_info[self.target_sys][str(max_nub)] = {
                'name': "", 'type': f'{type}', 'thickness': '3', 'length': '50', 'direction': 'R',
                'textxpos': '', 'textypos': '',
                'xpos': f'{pos.x()}', 'ypos': f'{pos.y()}'
            }
        elif type == 'valve' or type == 'HP':
            self.sys_mimic_info[self.target_sys][str(max_nub)] = {
                'id': "", 'name': "", 'type': f'{type}', 'direction': 'V', 'textxpos': '', 'textypos': '',
                'xpos': f'{pos.x()}', 'ypos': f'{pos.y()}'
            }
        elif type == 'pump':
            self.sys_mimic_info[self.target_sys][str(max_nub)] = {
                'id': "", 'name': "", 'type': f'{type}', 'direction': 'R', 'textxpos': '', 'textypos': '',
                'xpos': f'{pos.x()}', 'ypos': f'{pos.y()}'
            }
        else:
            self.sys_mimic_info[self.target_sys][str(max_nub)] = {
                'id': "", 'name': "", 'type': f'{type}', 'direction': 'R', 'textxpos': '', 'textypos': '',
                'xpos': f'{pos.x()}', 'ypos': f'{pos.y()}'
            }
        # update 현재 화면
        self.update_sys_mimic(self.target_sys)


class SVGComp(QGraphicsSvgItem):
    def __init__(self, svg_render, i: str, parent):
        super(SVGComp, self).__init__(None)
        self.sys_mimic_info = parent.sys_mimic_info
        self.target_sys = parent.target_sys
        self.setSharedRenderer(svg_render)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)  # horrible selection-box
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        # --------------------------------------------------------------------------------------------------------------
        self.nub = i
        self.comp_id = self.sys_mimic_info[self.target_sys][i]['id']
        self.comp_name = self.sys_mimic_info[self.target_sys][i]['name']
        self.comp_type = self.sys_mimic_info[self.target_sys][i]['type']  # 'valve', 'pump'
        self.pen_direction = self.sys_mimic_info[self.target_sys][i]['direction']  # Right, Right / Vertical, Horizontal
        self.text_x = self.sys_mimic_info[self.target_sys][i]['textxpos']
        self.text_y = self.sys_mimic_info[self.target_sys][i]['textypos']
        self.setX(float(self.sys_mimic_info[self.target_sys][i]['xpos']))
        self.setY(float(self.sys_mimic_info[self.target_sys][i]['ypos']))
        # 초기 이미지 선택
        self.svg_info = {
            'valve': {'V': 'valve_v_c', 'H': 'valve_h_c'},
            'pump': {'R': 'pump_r_start', 'L': 'pump_l_stop'},
            'RVP': 'RVP', 'HP': {'V': 'HP_v', 'H': 'HP_h'}, 'PZR': 'PZR'
        }
        if self.comp_type == 'valve' or self.comp_type == 'HP':
            self.setElementId(self.svg_info[self.comp_type][self.pen_direction])
        elif self.comp_type == 'pump':
            self.setElementId(self.svg_info[self.comp_type][self.pen_direction])
        else:
            self.setElementId(self.svg_info[self.comp_type])

        # 기기 이름
        self.text = QGraphicsTextItem(f'{self.comp_name}', self)
        self.text.setFlag(QGraphicsItem.ItemIsSelectable, True)  # horrible selection-box
        self.text.setFlag(QGraphicsItem.ItemIsMovable, True)
        if self.text_x == "":
            self.text.setX(self.boundingRect().width() / 2 - self.text.boundingRect().width() / 2)
        else:
            self.text.setX(float(self.text_x))
        if self.text_y == "":
            self.text.setY(self.boundingRect().height() + 7)
        else:
            self.text.setY(float(self.text_y))

        # 이미지 스케일 선정
        # self.setScale(1.75)
        # self.text.setScale(1 / 1.75)

        self._update_info_to_mem()

    def mousePressEvent(self, *args, **kwargs):
        super(SVGComp, self).mousePressEvent(*args, **kwargs)
        print(f'{self.nub} - {self.comp_id} - {self.pos()} - {self.x()} - {self.y()}')

        print('Call Control Board')
        self.scene().addItem(ValveControlBoard(self, self.pos()))
        self._update_info_to_mem()

    def mouseReleaseEvent(self, *args, **kwargs):
        super(SVGComp, self).mouseReleaseEvent(*args, **kwargs)
        self._update_info_to_mem()

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        menu = QMenu()
        # -----------------------------------------------------
        menu_state = QMenu('State')
        if self.comp_type in ['valve', 'pump', 'HP']:
            update_rotation = menu_state.addAction("Rotation")
            update_rotation.triggered.connect(self._update_rotation)
        # -----------------------------------------------------
        menu.addMenu(menu_state)
        # -----------------------------------------------------
        menu.exec_(event.screenPos())
        event.setAccepted(True)

    def _update_info_to_mem(self):
        self.sys_mimic_info[self.target_sys][self.nub]['xpos'] = str(self.x())
        self.sys_mimic_info[self.target_sys][self.nub]['ypos'] = str(self.y())
        self.sys_mimic_info[self.target_sys][self.nub]['textxpos'] = str(self.text.x())
        self.sys_mimic_info[self.target_sys][self.nub]['textypos'] = str(self.text.y())

    def _update_rotation(self):
        if self.comp_type == 'valve':
            self.pen_direction = 'H' if self.pen_direction == 'V' else 'V'
        if self.comp_type == 'pump':
            self.pen_direction = 'R' if self.pen_direction == 'L' else 'L'
        if self.comp_type == 'HP':
            self.pen_direction = 'H' if self.pen_direction == 'V' else 'V'
        self.setElementId(self.svg_info[self.comp_type][self.pen_direction])


class LineComp(QGraphicsLineItem):
    def __init__(self, i: str, parent):
        super(LineComp, self).__init__(None)
        self.sys_mimic_info = parent.sys_mimic_info
        self.target_sys = parent.target_sys
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)  # horrible selection-box
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        # --------------------------------------------------------------------------------------------------------------
        # print(self.sys_mimic_info[self.target_sys][i])
        self.nub = i
        self.comp_name = self.sys_mimic_info[self.target_sys][i]['name']
        self.comp_type = self.sys_mimic_info[self.target_sys][i]['type']  # arrow, line
        self.text_x = self.sys_mimic_info[self.target_sys][i]['textxpos']
        self.text_y = self.sys_mimic_info[self.target_sys][i]['textypos']
        self.pen_thickness = int(self.sys_mimic_info[self.target_sys][i]['thickness'])
        self.pen_length = float(self.sys_mimic_info[self.target_sys][i]['length'])
        self.pen_direction = self.sys_mimic_info[self.target_sys][i]['direction']       # Up, Down, Right, Right

        self.start_x = float(self.sys_mimic_info[self.target_sys][i]['xpos'])
        self.start_y = float(self.sys_mimic_info[self.target_sys][i]['ypos'])

        if self.pen_direction == "R" or self.pen_direction == "L":
            self.end_x = self.start_x + self.pen_length if self.pen_direction == "R" else self.start_x - self.pen_length
            self.end_y = self.start_y
        else:
            self.end_x = self.start_x
            self.end_y = self.start_y + self.pen_length if self.pen_direction == "D" else self.start_y - self.pen_length

        self.setLine(self.start_x, self.start_y, self.end_x, self.end_y)

        # 기기 이름
        self.text = QGraphicsTextItem(f'{self.comp_name}', self)
        self.text.setFlag(QGraphicsItem.ItemIsSelectable, True)  # horrible selection-box
        self.text.setFlag(QGraphicsItem.ItemIsMovable, True)
        if self.text_x == "":
            self.text.setX(self.boundingRect().width() / 2 - self.text.boundingRect().width() / 2)
        else:
            self.text.setX(float(self.text_x))
        if self.text_y == "":
            self.text.setY(self.boundingRect().height() + 7)
        else:
            self.text.setY(float(self.text_y))
        self._update_info_to_mem()

        self.setPen(QPen(Qt.black, self.pen_thickness))

    def boundingRect(self):
        extra = (self.pen().width() + 26) / 2
        return QRectF(self.line().p1(),
                      QSizeF(self.line().p2().x() - self.line().p1().x(), self.line().p2().y() - self.line().p1().y())
                      ).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setRenderHint(painter.Antialiasing)
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(Qt.SolidPattern)
        if self.comp_type == 'arrow':
            if self.pen_direction == 'R':
                arrow = QPolygonF([QPointF(self.start_x - 8, self.start_y),
                                   QPointF(self.start_x, self.start_y - 6),
                                   QPointF(self.start_x, self.start_y + 6),
                                   QPointF(self.start_x - 8, self.start_y)])
            if self.pen_direction == 'L':
                arrow = QPolygonF([QPointF(self.start_x + 8, self.end_y),
                                   QPointF(self.start_x, self.end_y - 6),
                                   QPointF(self.start_x, self.end_y + 6),
                                   QPointF(self.start_x + 8, self.end_y)])
            if self.pen_direction == 'U':
                arrow = QPolygonF([QPointF(self.start_x, self.end_y - 8),
                                   QPointF(self.start_x - 6, self.end_y),
                                   QPointF(self.start_x + 6, self.end_y),
                                   QPointF(self.start_x, self.end_y - 8)])
            if self.pen_direction == 'D':
                arrow = QPolygonF([QPointF(self.start_x, self.end_y + 8),
                                   QPointF(self.start_x - 6, self.end_y),
                                   QPointF(self.start_x + 6, self.end_y),
                                   QPointF(self.start_x, self.end_y + 8)])
            painter.drawPolygon(arrow)

        super(LineComp, self).paint(painter, QStyleOptionGraphicsItem, widget)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent'):
        super(LineComp, self).mouseReleaseEvent(event)
        print(self.nub)
        self._update_info_to_mem()

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super(LineComp, self).mousePressEvent(event)
        self._update_info_to_mem()

    def _update_info_to_mem(self):
        self.sys_mimic_info[self.target_sys][self.nub]['xpos'] = str(self.x() + self.start_x)
        self.sys_mimic_info[self.target_sys][self.nub]['ypos'] = str(self.y() + self.start_y)
        self.sys_mimic_info[self.target_sys][self.nub]['textxpos'] = str(self.text.x())
        self.sys_mimic_info[self.target_sys][self.nub]['textypos'] = str(self.text.y())


class BoundaryComp(QGraphicsRectItem):
    def __init__(self, parent):
        super(BoundaryComp, self).__init__(parent.sceneRect().adjusted(5, 5, -5, -5), None)
        self.MainSysRightScene = parent
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)  # horrible selection-box
        self.setFlag(QGraphicsItem.ItemIsMovable, False)

    def paint(self, qp: QPainter, option, widget=None):
        # super(BoundaryComp, self).paint(qp, option, widget)
        qp.setRenderHint(qp.Antialiasing)
        qp.setPen(QPen(QColor(127, 127, 127), 2))
        qp.drawRoundedRect(self.rect(), 10, 10)


class ValveControlBoard(QGraphicsRectItem):
    def __init__(self, parent, pos):
        super(ValveControlBoard, self).__init__(None)
        self.p = parent
        self.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(200)

        self.w, self.h = 150, 200
        self.setRect(pos.x() + 25, pos.y(), self.w, self.h)

        self.close_btn = QGraphicsRectItem(self)
        self.close_btn.setRect(pos.x() + 25 + self.w - 20, pos.y() + 5, 15, 15)
        self.close_btn.setBrush(QBrush(Qt.darkRed, Qt.SolidPattern))
        self.close_btn.setPen(QPen(Qt.NoPen))
        #
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)  # horrible selection-box
        self.setFlag(QGraphicsItem.ItemIsMovable, True)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """ x 버튼 누르면 닫힘 """
        item = self.scene().itemAt(event.scenePos().toPoint(), QTransform())
        if item == self.close_btn:
            self.scene().removeItem(self)
        super(ValveControlBoard, self).mousePressEvent(event)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainSysRightArea(None, 0, 0, 900, 765)
    window.show()
    sys.exit(app.exec_())
