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
        self.shmem = parent.shmem if parent is not None else None
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
        # Shortcut -----------------------------------------------------------------------------------------------------
        self.F2_key = QShortcut(QKeySequence('F2'), self)
        self.F2_key.activated.connect(self._keyPressEvent_F2)
        self.edit_mode = False

        self.update_sys_mimic('RCS')

    def update_sys_mimic(self, target_sys):
        self._scene.clear()
        self._scene.update_sys_mimic(target_sys)

    def keyPressEvent(self, QKeyEvent):
        super(MainSysRightArea, self).keyPressEvent(QKeyEvent)

    def _keyPressEvent_F2(self):
        self.edit_mode = False if self.edit_mode else True
        self._scene.keyPressEvent_F2(self.edit_mode)
        print(f'Edit Mode is {self.edit_mode}.')

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super(MainSysRightArea, self).mousePressEvent(event)


class MainSysRightScene(QGraphicsScene):
    def __init__(self, parent):
        super(MainSysRightScene, self).__init__(None)
        self.shmem = parent.shmem
        self.parent = parent
        self.setBackgroundBrush(QColor(254, 245, 249))   # Back gorund color
        # SVG render ---------------------------------------------------------------------------------------------------
        self.svg_render = QSvgRenderer('./interface_image/comp.svg')
        # Sys page info ------------------------------------------------------------------------------------------------
        self.target_sys = ''
        with open('./interface_image/MMI.json', 'r', encoding='UTF-8-sig') as f:
            self.sys_mimic_info = json.load(f)
        # 요소 추가 및 제거 시 ... ----------------------------------------------------
        # for sys in  self.sys_mimic_info.keys():
        #     for i in self.sys_mimic_info[sys].keys():
        #         if self.sys_mimic_info[sys][i]['type'] == 'arrow' or self.sys_mimic_info[sys][i]['type'] == 'line':
        #             self.sys_mimic_info[sys][i]['gate'] = 'N'
                    # del self.sys_mimic_info[sys][i]['flow_from']
        # ---------------------------------------------------------------------------
        self.current_opened_control_board = []
        # Shortcut -----------------------------------------------------------------------------------------------------
        self.edit_mode = False
        # Comp display update ------------------------------------------------------------------------------------------
        # if self.shmem is not None:
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self.update_mimic_info)
        timer.start()

    def keyPressEvent(self, QKeyEvent):
        super(MainSysRightScene, self).keyPressEvent(QKeyEvent)
        if self.selectedItems() is not None:
            if QKeyEvent.key() == Qt.Key_Up:
                self.selectedItems()[0].setY(int(self.selectedItems()[0].y() - 1))
            elif QKeyEvent.key() == Qt.Key_Down:
                self.selectedItems()[0].setY(int(self.selectedItems()[0].y() + 1))
            elif QKeyEvent.key() == Qt.Key_Right:
                self.selectedItems()[0].setX(int(self.selectedItems()[0].x() + 1))
            elif QKeyEvent.key() == Qt.Key_Left:
                self.selectedItems()[0].setX(int(self.selectedItems()[0].x() - 1))

    def update_sys_mimic(self, target_sys):
        # 이전 아이템 제거
        for item in self.items():
            self.removeItem(item)

        # 시스템 외부 테두리와 제목 표기 Not Move
        self.boundary_item = BoundaryComp(self)
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

    def update_mimic_info(self):
        """ 메모리에서 각 기기 값 업데이트 """
        if self.shmem is not None:
            # print('Update mimic_info')
            local_mem = self.shmem.get_shmem_db()
            # print(local_mem['KCNTOMS']['Val'])
            for item in self.items():
                if isinstance(item, SVGComp) and item.comp_id in local_mem.keys():
                    item.update_mimic_dis_info(local_mem[item.comp_id]['Val'])
                if isinstance(item, LineComp):
                    item.update_flow_color()
        else:
            # Test 용
            for item in self.items():
                if isinstance(item, SVGComp):
                    # print(f'Test mimic_info: {item.comp_id}_{item.comp_type}')
                    pass
                if isinstance(item, LineComp):
                    item.update_flow_color()

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
            menu_test_mem = QMenu()
            test_mem_ = menu_test_mem.addAction("TestMem")
            test_mem_.triggered.connect(self.testmem)
            menu.addMenu(menu_test_mem)
            # -----------------------------------------------------
            menu.exec_(event.screenPos())

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        item = self.itemAt(event.scenePos().toPoint(), QTransform())
        if item is not None and event.button() == Qt.LeftButton:
            # boundary_item 클릭
            if item is self.boundary_item:
                print('Bound Click')
            elif isinstance(item, SVGComp):
                # SVGComp 의 경우
                # 사전에 열려있는 Control Board 모두 Close
                if len(self.current_opened_control_board) != 0:
                    [self.removeItem(opened_item) for opened_item in self.current_opened_control_board]
                    self.current_opened_control_board = []
                # print(f'Comp Click {self.sceneRect()}')
                # Comp type 별 동작
                if item.comp_type == 'valve':
                    control_board = ValveControlBoard(item)
                    control_board.move_to_inside(self.boundary_item)
                    self.addItem(control_board)
                    self.current_opened_control_board.append(control_board)
                    pass

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
                'xpos': f'{pos.x()}', 'ypos': f'{pos.y()}',
                'flow_from': "0", 'comp_val': 0, 'gate': 'N'
            }
        elif type == 'valve' or type == 'HP':
            self.sys_mimic_info[self.target_sys][str(max_nub)] = {
                'id': "", 'name': "", 'type': f'{type}', 'direction': 'V', 'textxpos': '', 'textypos': '',
                'xpos': f'{pos.x()}', 'ypos': f'{pos.y()}', 'comp_val': 0,
            }
        elif type == 'pump':
            self.sys_mimic_info[self.target_sys][str(max_nub)] = {
                'id': "", 'name': "", 'type': f'{type}', 'direction': 'R', 'textxpos': '', 'textypos': '',
                'xpos': f'{pos.x()}', 'ypos': f'{pos.y()}', 'comp_val': 0,
            }
        else:
            self.sys_mimic_info[self.target_sys][str(max_nub)] = {
                'id': "", 'name': "", 'type': f'{type}', 'direction': 'R', 'textxpos': '', 'textypos': '',
                'xpos': f'{pos.x()}', 'ypos': f'{pos.y()}', 'comp_val': 0,
            }
        # update 현재 화면
        self.update_sys_mimic(self.target_sys)

    def keyPressEvent_F2(self, tig):
        """ 모든 아이템의 Flag 수정 """
        self.edit_mode = tig
        for item in self.items():
            if not isinstance(item, BoundaryComp):
                item.setFlag(QGraphicsItem.ItemIsMovable, tig)

    def testmem(self):
        self.update_mimic_info()
        # print('Test mem update')


class SVGComp(QGraphicsSvgItem):
    def __init__(self, svg_render, i: str, parent):
        super(SVGComp, self).__init__(None)
        self.sys_mimic_info = parent.sys_mimic_info
        self.target_sys = parent.target_sys
        self.parent = parent
        self.setSharedRenderer(svg_render)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)  # horrible selection-box
        self.setFlag(QGraphicsItem.ItemIsMovable, parent.edit_mode)
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

        self.comp_val = self.sys_mimic_info[self.target_sys][i]['comp_val']
        # 초기 이미지 선택
        self.svg_info = {
            'valve': {'V': 'valve_v_c', 'H': 'valve_h_c'},
            'pump': {'R': 'pump_r_stop', 'L': 'pump_l_stop'},
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
        print(f'{self.nub} - {self.comp_id} - {self.comp_val} - {self.pos()} - {self.x()} - {self.y()}')
        self._update_info_to_mem()
        super(SVGComp, self).mousePressEvent(*args, **kwargs)

    def mouseReleaseEvent(self, *args, **kwargs):
        super(SVGComp, self).mouseReleaseEvent(*args, **kwargs)
        self._update_info_to_mem()

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        menu = QMenu()
        # -----------------------------------------------------
        menu_state = QMenu('State')
        if self.comp_type in ['valve', 'pump', 'HP', ]:
            update_rotation = menu_state.addAction("Rotation")
            update_rotation.triggered.connect(self._update_rotation)
            update_id = menu_state.addAction("Edit Id")
            update_id.triggered.connect(self._update_id)
            update_comp_val = menu_state.addAction("Edit Comp Val")
            update_comp_val.triggered.connect(self._update_comp_val)
            remove_item = menu.addAction("Remove Item")
            remove_item.triggered.connect(self._remove_item)
        # -----------------------------------------------------
        menu.addMenu(menu_state)
        # -----------------------------------------------------
        menu.exec_(event.screenPos())
        event.setAccepted(True)

    def _remove_item(self):
        """ item 삭제 """
        # 메커니즘: 1. self.sys_mimic_info 에서 해당 아이템 정보 제거 2. 관련된 파이프 정보 업데이트. 3. 메모리 저장 및 Re-load
        del self.sys_mimic_info[self.target_sys][self.nub]

        temp_mimic_info = {}

        for new_nub, old_nub in enumerate(self.sys_mimic_info[self.target_sys].keys()):
            temp_mimic_info[new_nub] = self.sys_mimic_info[self.target_sys][old_nub]
            if temp_mimic_info[new_nub]['type'] == 'line' or temp_mimic_info[new_nub]['type'] == 'arrow':
                if temp_mimic_info[new_nub]['flow_from'] == str(self.nub):
                    # 삭제된 파이프에 연결된 flow_from 이므로 "N" 할당 및 자동적으로 -1 로 변환
                    temp_mimic_info[new_nub]['flow_from'] = "N"
                elif temp_mimic_info[new_nub]['flow_from'].isdigit():
                    # 다른 기기와 연결된 경우, 이 경우 "1" 과 같이 숫자형인 str 값임.
                    if int(temp_mimic_info[new_nub]['flow_from']) > int(self.nub):
                        # 지워지는 값보다 flow_from 이 크면 숫자를 감산해 줘야함. (DB가 밀림)
                        temp_mimic_info[new_nub]['flow_from'] = str(int(temp_mimic_info[new_nub]['flow_from']) - 1)
                else:
                    if "," in temp_mimic_info[new_nub]['flow_from']:
                        # "1,2" 같이 2개의 입력을 소스를 받는 경우가 있음.
                        connected_nubs = temp_mimic_info[new_nub]['flow_from'].split(',')
                        out_str = ''

                        for i, v in enumerate(connected_nubs):
                            if int(v) > int(self.nub):  # 위와 동일한 로직
                                out_str += f'{int(v) - 1},'
                            elif int(v) < int(self.nub):
                                out_str += f'{v},'
                        out_str = out_str[:-1]  # , 제외

                        if out_str == '':
                            # out_str = ''
                            out_str = 'N'
                        else:
                            # out_str = '1,2,3'
                            pass

                        temp_mimic_info[new_nub]['flow_from'] = out_str

                    else:
                        # flow_from 이 소스("S") 이거나 타 기기 변수를 지칭하는 경우
                        pass
            else:
                pass  # 펌프나 벨브와 같이 색이 안변하는 기기 경우

        # 메모리 업데이트
        self.sys_mimic_info[self.target_sys] = temp_mimic_info

        # 저장 및 Re-load
        self.parent.save_all_mmi()
        self.parent.load_all_mmi()

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

    def _update_id(self):
        text, ok = QInputDialog.getText(None, 'Change Id', f'Curent Id [{self.comp_id}]:')
        if ok:
            self.comp_id = text
            self.sys_mimic_info[self.target_sys][self.nub]['id'] = text

    def _update_comp_val(self):
        current_val = self.sys_mimic_info[self.target_sys][self.nub]['comp_val']
        text, ok = QInputDialog.getText(None, f'Change Val', f'Curent Num [{self.nub}] Val [{current_val}]:')
        if ok:
            self.comp_val = float(text)
            self.sys_mimic_info[self.target_sys][self.nub]['comp_val'] = float(text)

    def update_mimic_dis_info(self, value):
        self.sys_mimic_info[self.target_sys][self.nub]['comp_val'] = value
        self.comp_val = value
        if self.comp_type == 'valve':
            if value == 1.0:
                self.setElementId(f'valve_{self.pen_direction.lower()}_o')
            elif 0 < value < 1:
                self.setElementId(f'valve_{self.pen_direction.lower()}_h')
            else:
                self.setElementId(f'valve_{self.pen_direction.lower()}_c')
        elif self.comp_type == 'pump':
            if value == 1.0:
                self.setElementId(f'pump_{self.pen_direction.lower()}_start')
            else:
                self.setElementId(f'pump_{self.pen_direction.lower()}_stop')
        # print(f'[{self.comp_id}][{value}]')


class LineComp(QGraphicsLineItem):
    def __init__(self, i: str, parent):
        super(LineComp, self).__init__(None)
        self.sys_mimic_info = parent.sys_mimic_info
        self.target_sys = parent.target_sys
        self.parent = parent
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)  # horrible selection-box
        self.setFlag(QGraphicsItem.ItemIsMovable, parent.edit_mode)
        # --------------------------------------------------------------------------------------------------------------
        # print(self.sys_mimic_info[self.target_sys][i])
        self.nub = i
        self.comp_name = self.sys_mimic_info[self.target_sys][i]['name']
        self.comp_type = self.sys_mimic_info[self.target_sys][i]['type']  # arrow, line
        self.text_x = self.sys_mimic_info[self.target_sys][i]['textxpos']
        self.text_y = self.sys_mimic_info[self.target_sys][i]['textypos']
        self.pen_thickness = int(self.sys_mimic_info[self.target_sys][i]['thickness'])
        self.pen_length = float(self.sys_mimic_info[self.target_sys][i]['length'])
        self.pen_direction = self.sys_mimic_info[self.target_sys][i]['direction']       # Up, Down, Right, Left

        self.start_x = float(self.sys_mimic_info[self.target_sys][i]['xpos'])
        self.start_y = float(self.sys_mimic_info[self.target_sys][i]['ypos'])

        self.flow_from = self.sys_mimic_info[self.target_sys][i]['flow_from']
        self.flow_val = self.sys_mimic_info[self.target_sys][i]['comp_val']

        self.gate = self.sys_mimic_info[self.target_sys][i]['gate']

        # Line V = (R, L), H = (D, U)
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

        self.flow_color = Qt.blue if self.flow_val > 0 else Qt.black
        self.setPen(QPen(self.flow_color, self.pen_thickness))

    def boundingRect(self):
        extra = (self.pen().width() + 26) / 2
        return QRectF(self.line().p1(),
                      QSizeF(self.line().p2().x() - self.line().p1().x(), self.line().p2().y() - self.line().p1().y())
                      ).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setRenderHint(painter.Antialiasing)
        painter.setPen(QPen(self.flow_color, 1))
        painter.setBrush(QBrush(self.flow_color, Qt.SolidPattern))
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
        print(f'{self.nub} - {self.comp_name} - {self.comp_type} - {self.flow_from} - {self.flow_val}')
        self._update_info_to_mem()

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super(LineComp, self).mousePressEvent(event)
        self._update_info_to_mem()

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        menu = QMenu()
        # -----------------------------------------------------
        update_flow_from = menu.addAction("Edit Flow ID")
        update_flow_from.triggered.connect(self._update_flow_id)
        update_rotation = menu.addAction("Rotation")
        update_rotation.triggered.connect(self._update_rotation)
        shape = 'Arrow' if self.comp_type == 'line' else 'Line'
        update_arrow = menu.addAction(f"Change Shape to {shape}")
        update_arrow.triggered.connect(self._update_shape)
        remove_item = menu.addAction("Remove Item")
        remove_item.triggered.connect(self._remove_item)
        change_length = menu.addAction('Change Length')
        change_length.triggered.connect(self._change_length)
        change_gate = menu.addAction('Change Gate')
        change_gate.triggered.connect(self._change_gate)
        # -----------------------------------------------------
        menu.exec_(event.screenPos())

    def _update_flow_id(self):
        text, ok = QInputDialog.getText(None, 'Flow Id', f'Current Id [{self.flow_from}]|Val [{self.flow_val}]:')
        if ok:
            self.flow_from = text
            self.sys_mimic_info[self.target_sys][self.nub]['flow_from'] = text

    def _update_rotation(self):
        # Shape 전환
        if self.comp_type == 'line':
            self.pen_direction = "D" if self.pen_direction == "R" or self.pen_direction == "L" else "R"
        elif self.comp_type == 'arrow':
            _rot_pos = {'R': 0, 'U': 1, 'L': 2, 'D': 3}
            _rot_valpos = {0: 'R', 1: 'U', 2: 'L', 3: 'D'}
            _pos_nub = 0 if _rot_pos[self.pen_direction] + 1 == 4 else _rot_pos[self.pen_direction] + 1
            self.pen_direction = _rot_valpos[_pos_nub]

        # 위치 재 계산
        if self.pen_direction == "R" or self.pen_direction == "L":
            self.end_x = self.start_x + self.pen_length if self.pen_direction == "R" else self.start_x - self.pen_length
            self.end_y = self.start_y
        else:
            self.end_x = self.start_x
            self.end_y = self.start_y + self.pen_length if self.pen_direction == "D" else self.start_y - self.pen_length

        # 업데이트
        self.setLine(self.start_x, self.start_y, self.end_x, self.end_y)

        # 메모리 업데이트
        self.sys_mimic_info[self.target_sys][self.nub]['direction'] = self.pen_direction
        self.sys_mimic_info[self.target_sys][self.nub]['xpos'] = str(self.x() + self.start_x)
        self.sys_mimic_info[self.target_sys][self.nub]['ypos'] = str(self.y() + self.start_y)

    def _update_shape(self):
        # Shape 전환
        self.comp_type = 'arrow' if self.comp_type == 'line' else 'line'

        self.update()

        # 메모리 업데이트
        self.sys_mimic_info[self.target_sys][self.nub]['type'] = self.comp_type

    def _change_length(self):
        text, ok = QInputDialog.getText(None, 'Change length', f'Current Length [{self.pen_length}] =>')
        if ok:
            self.pen_length = float(text)
            self.sys_mimic_info[self.target_sys][self.nub]['length'] = float(text)

            # 위치 재 계산
            if self.pen_direction == "R" or self.pen_direction == "L":
                self.end_x = self.start_x + self.pen_length if self.pen_direction == "R" else self.start_x - self.pen_length
                self.end_y = self.start_y
            else:
                self.end_x = self.start_x
                self.end_y = self.start_y + self.pen_length if self.pen_direction == "D" else self.start_y - self.pen_length

            # 업데이트
            self.setLine(self.start_x, self.start_y, self.end_x, self.end_y)

    def _change_gate(self):
        text, ok = QInputDialog.getText(None, 'Change gate', f'Current gate [{self.gate}] =>')
        if ok:
            self.gate = text
            self.sys_mimic_info[self.target_sys][self.nub]['gate'] = text

    def _update_info_to_mem(self):
        self.sys_mimic_info[self.target_sys][self.nub]['xpos'] = str(self.x() + self.start_x)
        self.sys_mimic_info[self.target_sys][self.nub]['ypos'] = str(self.y() + self.start_y)
        self.sys_mimic_info[self.target_sys][self.nub]['textxpos'] = str(self.text.x())
        self.sys_mimic_info[self.target_sys][self.nub]['textypos'] = str(self.text.y())

    def _remove_item(self):
        """ item 삭제 """
        # 메커니즘: 1. self.sys_mimic_info 에서 해당 아이템 정보 제거 2. 관련된 파이프 정보 업데이트. 3. 메모리 저장 및 Re-load
        del self.sys_mimic_info[self.target_sys][self.nub]

        temp_mimic_info = {}

        for new_nub, old_nub in enumerate(self.sys_mimic_info[self.target_sys].keys()):
            temp_mimic_info[new_nub] = self.sys_mimic_info[self.target_sys][old_nub]
            # if temp_mimic_info[new_nub]['type'] == 'line' or temp_mimic_info[new_nub]['type'] == 'arrow':
            if temp_mimic_info[new_nub]['flow_from'] == str(self.nub):
                # 삭제된 파이프에 연결된 flow_from 이므로 "N" 할당 및 자동적으로 -1 로 변환
                temp_mimic_info[new_nub]['flow_from'] = "N"
            elif temp_mimic_info[new_nub]['flow_from'].isdigit():
                # 다른 기기와 연결된 경우, 이 경우 "1" 과 같이 숫자형인 str 값임.
                if int(temp_mimic_info[new_nub]['flow_from']) > int(self.nub):
                    # 지워지는 값보다 flow_from 이 크면 숫자를 감산해 줘야함. (DB가 밀림)
                    temp_mimic_info[new_nub]['flow_from'] = str(int(temp_mimic_info[new_nub]['flow_from']) - 1)
            else:
                if "," in temp_mimic_info[new_nub]['flow_from']:
                    # "1,2" 같이 2개의 입력을 소스를 받는 경우가 있음.
                    connected_nubs = temp_mimic_info[new_nub]['flow_from'].split(',')
                    out_str = ''

                    for i, v in enumerate(connected_nubs):
                        if int(v) > int(self.nub):              # 위와 동일한 로직
                            out_str += f'{int(v) - 1},'
                        elif int(v) < int(self.nub):
                            out_str += f'{v},'
                    out_str = out_str[:-1]      # , 제외

                    if out_str == '':
                        # out_str = ''
                        out_str = 'N'
                    else:
                        # out_str = '1,2,3'
                        pass

                    temp_mimic_info[new_nub]['flow_from'] = out_str

                else:
                    # flow_from 이 소스("S") 이거나 타 기기 변수를 지칭하는 경우
                    pass
            # else:
            #     pass  # 펌프나 벨브와 같이 색이 안변하는 기기 경우

        # 메모리 업데이트
        self.sys_mimic_info[self.target_sys] = temp_mimic_info

        # 저장 및 Re-load
        self.parent.save_all_mmi()
        self.parent.load_all_mmi()

    def update_flow_color(self):
        if self.flow_from == "S" or self.flow_from == "N":   # Source or None
            self.flow_val = 1 if self.flow_from == "S" else -1      # -1 is None
        else:
            if ',' in self.flow_from:
                # 초기 파이프내 유량 0
                self.flow_val = 0
                
                # "1,2" 같이 2개의 입력을 소스를 받는 경우가 있음.
                _logic_box = []
                connected_nubs = self.flow_from.split(',')
                for nub_ in connected_nubs:
                    if self.sys_mimic_info[self.target_sys][nub_]['comp_val'] > 0:
                        _logic_box.append(True)
                    else:
                        _logic_box.append(False)
                # 로직
                if self.gate == "OR" or self.gate == 'N':
                    self.flow_val = 1 if any(_logic_box) else 0
                elif self.gate == "AND":
                    self.flow_val = 1 if all(_logic_box) else 0
            else:
                self.flow_val = self.sys_mimic_info[self.target_sys][self.flow_from]['comp_val']

        self.sys_mimic_info[self.target_sys][self.nub]['comp_val'] = self.flow_val

        if self.flow_val == 0:
            self.flow_color = Qt.black
        elif self.flow_val > 0:
            self.flow_color = Qt.blue
        else:
            self.flow_color = Qt.red

        self.setPen(QPen(self.flow_color, self.pen_thickness))


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
    def __init__(self, parent):
        super(ValveControlBoard, self).__init__(None)
        self.p = parent
        self.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(200)

        self.w, self.h = 150, 200
        self.setRect(parent.x() + 25, parent.y(), self.w, self.h)

        self.close_btn = QGraphicsRectItem(self)
        self.close_btn.setRect(parent.x() + 25 + self.w - 20, parent.y() + 5, 15, 15)
        self.close_btn.setBrush(QBrush(Qt.darkRed, Qt.SolidPattern))
        self.close_btn.setPen(QPen(Qt.NoPen))

        self.up_btn = ValveControlBoardBtn(self, parent.x() + 20, parent.y() + 20)
        #
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)  # horrible selection-box
        self.setFlag(QGraphicsItem.ItemIsMovable, True)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """ x 버튼 누르면 닫힘 """
        item = self.scene().itemAt(event.scenePos().toPoint(), QTransform())
        if item == self.close_btn:
            self.scene().removeItem(self)
        super(ValveControlBoard, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """ 컨트롤 보드 움직이는 경우 scene 경계 내에서 움직임 """
        self.move_to_inside(self.scene().boundary_item)
        super(ValveControlBoard, self).mouseReleaseEvent(event)

    def _inside_delta(self, boundary_itme):
        new_pos: QRect = self.mapRectToScene(self.rect())
        new_pos_x: QRect = self.mapRectToScene(self.close_btn.rect())

        boundary: QRect = boundary_itme.rect()  # < ---  self.scene().boundary_item.rect()

        if new_pos.y() + new_pos.height() > boundary.y() + boundary.height():
            # Out Boundary (y)
            delta_y = (new_pos.y() + new_pos.height()) - (boundary.y() + boundary.height())
        elif new_pos.y() < boundary.y():
            # Out boundary (y) left
            delta_y = (new_pos.y() - boundary.y())
        else:
            delta_y = 0

        if new_pos.x() + new_pos.width() > boundary.x() + boundary.width():
            # Out boundary (x) right
            delta_x = (new_pos.x() + new_pos.width()) - (boundary.x() + boundary.width())
        elif new_pos.x() < boundary.x():
            # Out boundary (x) left
            delta_x = (new_pos.x() - boundary.x())
        else:
            delta_x = 0

        return delta_x, delta_y

    def move_to_inside(self, boundary_itme):
        # 바운더리 넘어간 경우 -------------------------------------------------------------------------------------------
        new_pos: QRect = self.mapRectToScene(self.rect())
        new_pos_x: QRect = self.mapRectToScene(self.close_btn.rect())
        new_pos_up: QRect = self.mapRectToScene(self.up_btn.boundingRect())

        boundary: QRect = boundary_itme.rect()  # < ---  self.scene().boundary_item.rect()

        delta_x, delta_y = self._inside_delta(boundary_itme)

        new_pos.moveTop(new_pos.y() - delta_y)
        new_pos_x.moveTop(new_pos_x.y() - delta_y)
        new_pos_up.moveTop(new_pos_up.y() - delta_y)

        new_pos.moveLeft(new_pos.x() - delta_x)
        new_pos_x.moveLeft(new_pos_x.x() - delta_x)
        new_pos_up.moveLeft(new_pos_up.x() - delta_x)

        self.setPos(0, 0)  # 이전 pos 리셋
        self.close_btn.setPos(0, 0)
        self.up_btn.setPos(0, 0)

        self.setRect(new_pos)
        self.close_btn.setRect(new_pos_x)

        # 기기를 가리는 경우 ---------------------------------------------------------------------------------------------
        new_pos: QRect = self.mapRectToScene(self.rect())
        new_pos_x: QRect = self.mapRectToScene(self.close_btn.rect())

        if self.rect().x() + self.rect().width() + 5 > self.p.sceneBoundingRect().x() and self.rect().x() < self.p.sceneBoundingRect().x():
            target_x = self.p.sceneBoundingRect().x() - 5

            delta_x = self.rect().x() + self.rect().width() - target_x

            new_pos.moveLeft(new_pos.x() - delta_x)
            new_pos_x.moveLeft(new_pos_x.x() - delta_x)

            self.setPos(0, 0)  # 이전 pos 리셋
            self.close_btn.setPos(0, 0)

            self.setRect(new_pos)
            self.close_btn.setRect(new_pos_x)

        # 바운더리 넘어간 경우 -------------------------------------------------------------------------------------------
        new_pos: QRect = self.mapRectToScene(self.rect())
        new_pos_x: QRect = self.mapRectToScene(self.close_btn.rect())

        boundary: QRect = boundary_itme.rect()  # < ---  self.scene().boundary_item.rect()

        delta_x, delta_y = self._inside_delta(boundary_itme)

        new_pos.moveTop(new_pos.y() - delta_y)
        new_pos_x.moveTop(new_pos_x.y() - delta_y)

        new_pos.moveLeft(new_pos.x() - delta_x)
        new_pos_x.moveLeft(new_pos_x.x() - delta_x)

        self.setPos(0, 0)  # 이전 pos 리셋
        self.close_btn.setPos(0, 0)

        self.setRect(new_pos)
        self.close_btn.setRect(new_pos_x)


class ValveControlBoardBtn(QGraphicsPolygonItem):
    def __init__(self, parent, x=0, y=0):
        super(ValveControlBoardBtn, self).__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setAcceptHoverEvents(True)
        self.start_x, self.start_y = 100, 100
        #print(x, y)
        x, y = self.start_x, self.start_y
        arrow = QPolygonF([QPointF(x - 8, y),
                           QPointF(x, y - 6),
                           QPointF(x, y + 6),
                           QPointF(x - 8, y)])

        self.setPolygon(arrow)
        self.setScale(2)
        self.setBrush(QBrush(Qt.darkRed, Qt.SolidPattern))

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None) -> None:
        painter.setRenderHint(painter.Antialiasing)
        super(ValveControlBoardBtn, self).paint(painter, QStyleOptionGraphicsItem, widget)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.setBrush(QBrush(Qt.darkGreen, Qt.SolidPattern))

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.setBrush(QBrush(Qt.darkRed, Qt.SolidPattern))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainSysRightArea(None, 0, 0, 900, 765)
    window.show()
    sys.exit(app.exec_())
