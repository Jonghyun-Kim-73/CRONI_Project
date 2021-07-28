from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer


class MenuActWidget(QWidgetAction):
    def __init__(self, label_txt='', line_txt='', connected_f=None, parent=None):
        super(MenuActWidget, self).__init__(parent)

        w = QWidget()
        w_lay = QHBoxLayout()
        w_lay.setContentsMargins(0, 0, 0, 0)
        w_lay.setSpacing(5)
        self.label = QLabel(label_txt)
        self.label.setMinimumWidth(80)
        self.lineedit = QLineEdit(line_txt)
        self.lineedit.textChanged.connect(connected_f)
        w_lay.addWidget(self.label)
        w_lay.addWidget(self.lineedit)
        w.setLayout(w_lay)
        self.setDefaultWidget(w)

class SvgItem(QGraphicsSvgItem):
    def __init__(self, id, renderer, pos, parent=None):
        super().__init__(parent)
        self.id = id
        self.setSharedRenderer(renderer)
        self.setElementId(id)
        bounds = renderer.boundsOnElement(id)
        self.setPos(pos)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True) #horrible selection-box
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)

        # create an image based on the item size
        img = QtGui.QImage(bounds.size().toSize(), QtGui.QImage.Format_ARGB32)
        # clear its buffer (this is important!)
        img.fill(QtCore.Qt.transparent)
        # create a qpainter and ask the renderer to render it
        qp = QtGui.QPainter(img)
        renderer.render(qp, id)
        qp.end()

        # create the mask by adding a QRegion based on it
        mask = img.createAlphaMask()
        shape = QtGui.QPainterPath()
        shape.addRegion(QtGui.QRegion(QtGui.QBitmap.fromImage(mask)))
        # a QBitmap based region can be unnecessarily complex, let's
        # simplify it
        self._shape = shape.simplified()

        self.fault_level = 0    # 0 normal 1, 2, 3
        self.fault_max_level = 3

        self.text = QGraphicsTextItem('test_comp', self)
        self.text.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.text.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)

        self.text.setX(self.boundingRect().width()/2 - self.text.boundingRect().width()/2)
        self.text.setY(self.boundingRect().height() + 7)

        _w, _h = self.boundingRect().width(), self.boundingRect().height()
        self._bound = [
            QGraphicsLineItem(-5, -5, -5, 5, self),  QGraphicsLineItem(-5, -5, 5, -5, self),
            QGraphicsLineItem(-5, _h + 5, -5, _h - 5, self), QGraphicsLineItem(-5, _h + 5, 5, _h + 5, self),
            QGraphicsLineItem(_w + 5, -5, _w - 5, -5, self), QGraphicsLineItem(_w + 5, -5, _w + 5, 5, self),
            QGraphicsLineItem(_w + 5, _h + 5, _w - 5, _h + 5, self), QGraphicsLineItem(_w + 5, _h + 5, _w + 5, _h - 5, self),
        ]

    def shape(self):
        return self._shape

    def paint(self, painter, option, widget):
        # # keep track of the selected state and call the base painting
        # # implementation without it
        selected = option.state & QtWidgets.QStyle.State_Selected
        option.state &= ~QtWidgets.QStyle.State_Selected
        painter.setRenderHint(QPainter.Antialiasing)

        # super(SvgItem, self).paint(painter, option, widget)
        #
        if selected:
            # draw the selection based on the shape, using the right
            # amount of contrast with the background
            fgcolor = option.palette.windowText().color()
            bgcolor = QtGui.QColor(
                0 if fgcolor.red() > 127 else 255,
                0 if fgcolor.green() > 127 else 255,
                0 if fgcolor.blue() > 127 else 255,
            )
            # painter.fillPath(self._shape, QtGui.QBrush(QtGui.QColor("red")))

            painter.setPen(QtGui.QPen(bgcolor, 0, QtCore.Qt.SolidLine))
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawPath(self._shape)

            painter.setPen(QtGui.QPen(option.palette.windowText(), 0, QtCore.Qt.DashLine))
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawPath(self._shape)

        # 경보 바운더리
        pen = QPen()
        pen.setWidth(3)
        if self.fault_level == 0:
            pen.setColor(Qt.white)  # backcolor 넣기
        elif self.fault_level == 1:
            pen.setColor(Qt.black)
        elif self.fault_level == 2:
            pen.setColor(Qt.blue)
        elif self.fault_level == 3:
            pen.setColor(Qt.red)
        [_.setPen(pen) for _ in self._bound]
        super(SvgItem, self).paint(painter, option, widget)

    def mousePressEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent'):
        print('svg item: ' + str(self) + self.id + ' - mousePressEvent()')
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent'):
        print('svg item: ' + str(self) + self.id + ' - mouseReleaseEvent()')
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event) -> None:
        menu = QMenu()
        # -----------------------------------------------------
        menu_state = QMenu('State')
        update_state_close = menu_state.addAction("Close")
        update_state_half = menu_state.addAction("Half")
        update_state_open = menu_state.addAction("Open")
        update_state_close.triggered.connect(lambda a, s='V1_close': self._update_state(s))
        update_state_half.triggered.connect(lambda a, s='V1_half': self._update_state(s))
        update_state_open.triggered.connect(lambda a, s='V1_open': self._update_state(s))
        # -----------------------------------------------------
        menu_state = QMenu('State')
        update_state_close = menu_state.addAction("Close")
        update_state_open = menu_state.addAction("Open")
        update_state_close.triggered.connect(lambda b, k='Pump_close': self._update_state(k))
        update_state_open.triggered.connect(lambda b, k='Pump_open': self._update_state(k))

        menu_info = QMenu('Info')
        self.menu_info_list = [
            MenuActWidget(label_txt='comp_txt', line_txt=self.text.toPlainText(), connected_f=self._update_info_comp_txt),
            MenuActWidget(label_txt='x', line_txt=str(self.x()), connected_f=self._update_info_x),
            MenuActWidget(label_txt='y', line_txt=str(self.y()), connected_f=self._update_info_x),
            MenuActWidget(label_txt='fault_level', line_txt=str(self.fault_level), connected_f=self._update_fault_level),
        ]
        [menu_info.addAction(_) for _ in self.menu_info_list]
        # -----------------------------------------------------
        menu.addMenu(menu_state)
        menu.addMenu(menu_info)
        # -----------------------------------------------------
        menu.exec_(event.screenPos())
        event.setAccepted(True)

    def _update_state(self, state):
        self.id = state
        self.setElementId(self.id)

    def _update_info_comp_txt(self):
        get_txt = self.menu_info_list[0].lineedit.text()
        self.text.setPlainText(get_txt)
        self.text.setX(self.boundingRect().width() / 2 - self.text.boundingRect().width() / 2)
        self.text.setY(self.boundingRect().height() + 7)

    def _update_info_x(self):
        txt_ = self.menu_info_list[1].lineedit.text()
        if txt_.isdigit():
            self.setX(float(txt_))
        else:
            self.menu_info_list[1].lineedit.setText(str(0))

    def _update_info_y(self):
        txt_ = self.menu_info_list[2].lineedit.text()
        if txt_.isdigit():
            self.setY(float(txt_))
        else:
            self.menu_info_list[2].lineedit.setText(str(0))

    def _update_fault_level(self):
        txt_ = self.menu_info_list[3].lineedit.text()
        if txt_.isdigit():
            self.fault_level = int(txt_) if 0 <= int(txt_) <= self.fault_max_level else 0
            self.menu_info_list[3].lineedit.setText(str(self.fault_level))
            self.update(self.boundingRect())
        else:
            self.menu_info_list[3].lineedit.setText(str(0))


class LineItem(QGraphicsLineItem):
    def __init__(self, pos, parent=None):
        super(LineItem, self).__init__(parent)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)  # horrible selection-box
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)

        self.start_point = pos
        self.end_point = pos
        self.setLine(QLineF(self.start_point, self.end_point))

        self.text = QGraphicsTextItem('Value', self)
        # self.text.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        # self.text.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)

    def update_line(self, end_pos):
        self.end_point = end_pos
        self.setLine(QLineF(self.start_point, self.end_point))
        self.text.setPos(self.end_point + (self.start_point - self.end_point)/2 -
                         QPointF(self.text.boundingRect().width() / 2, 0))

    def paint(self, painter, option, widget) -> None:
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(10)
        self.setPen(pen)

        print(self.line().p1(), self.line().p2(), self.x())

        super(LineItem, self).paint(painter, option, widget)

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        self._update_line_pos()

        menu = QMenu()
        # -----------------------------------------------------
        menu_state = QMenu('State')
        # -----------------------------------------------------
        menu_info = QMenu('Info')
        menu_info.setFocusPolicy(Qt.TabFocus)
        self.menu_info_list = [
            MenuActWidget(label_txt='comp_txt', line_txt=self.text.toPlainText(), connected_f=self._update_info_comp_txt),
            MenuActWidget(label_txt='x1', line_txt=str(self.line().x1()), connected_f=self._update_info_point),
            MenuActWidget(label_txt='y1', line_txt=str(self.line().y1()), connected_f=self._update_info_point),
            MenuActWidget(label_txt='x2', line_txt=str(self.line().x2()), connected_f=self._update_info_point),
            MenuActWidget(label_txt='y2', line_txt=str(self.line().y2()), connected_f=self._update_info_point),
        ]
        [menu_info.addAction(_) for _ in self.menu_info_list]
        # -----------------------------------------------------
        menu.addMenu(menu_state)
        menu.addMenu(menu_info)
        # -----------------------------------------------------
        menu.exec_(event.screenPos())
        event.setAccepted(True)

    def _update_line_pos(self):
        self.start_point = self.start_point + self.pos()
        self.end_point = self.end_point + self.pos()
        self.setPos(0, 0)   # reset pos points
        self.setLine(QLineF(self.start_point, self.end_point))  # update new pos
        self.text.setPos(self.end_point + (self.start_point - self.end_point) / 2 -
                         QPointF(self.text.boundingRect().width() / 2, 0))

    def _update_info_comp_txt(self):
        get_txt = self.menu_info_list[0].lineedit.text()
        self.text.setPlainText(get_txt)
        self.text.setPos(self.end_point + (self.start_point - self.end_point) / 2 -
                         QPointF(self.text.boundingRect().width() / 2, 0))

    def _update_info_point(self):
        x1_ = self._check_float(self.menu_info_list[1].lineedit.text())
        y1_ = self._check_float(self.menu_info_list[2].lineedit.text())
        x2_ = self._check_float(self.menu_info_list[3].lineedit.text())
        y2_ = self._check_float(self.menu_info_list[4].lineedit.text())
        self.start_point = QPointF(float(x1_), float(y1_))
        self.end_point = QPointF(float(x2_), float(y2_))
        self.setPos(0, 0)
        self.setLine(QLineF(float(x1_), float(y1_), float(x2_), float(y2_)))

        self._update_info_comp_txt()

    def _check_float(self, v):
        try:
            return float(v)
        except:
            return float(0.0)


class SvgScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent):
        super(SvgScene, self).__init__(parent)
        self._renderer = QSvgRenderer('./interface_image/comp.svg')
        self._line = None

    def contextMenuEvent(self, event) -> None:
        item = self.itemAt(event.scenePos().toPoint(), QTransform())
        if item is not None:
            item.contextMenuEvent(event)
        else:
            menu = QMenu()
            add_valve = menu.addAction("Add valve")
            add_line = menu.addAction("Add line")
            add_pump = menu.addAction("Add pump") ### -------------펌프

            add_valve.triggered.connect(lambda a, pos=event.scenePos(): self._add_valve(pos))
            add_line.triggered.connect(lambda a, pos=event.scenePos(): self._add_line(pos))
            add_pump.triggered.connect(lambda a, pos=event.scenePos(): self._add_pump(pos)) ###---------펌프
            menu.exec_(event.screenPos())

    def _add_valve(self, pos):
        item = SvgItem('V1_open', self._renderer, pos)
        self.addItem(item)

    def _add_line(self, pos):
        self._line = LineItem(pos)
        self.addItem(self._line)

    def _add_pump(self, pos):
        item = SvgItem('Pump_open', self._renderer, pos) ### --------------펌프
        self.addItem(item)

    def mousePressEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        self._line = None
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """ 누르고 움직이는 경우 활성화 """
        if self._line is not None:
            self._line.update_line(event.scenePos())
        super().mouseMoveEvent(event)


class SvgViewer(QtWidgets.QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)
        self._scene = SvgScene(self)
        self.setScene(self._scene)
        self._scene.clear()
        self._scene.setSceneRect(0, 0, 640, 480)
        self.setMinimumSize(700, 500)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        super(SvgViewer, self).mouseMoveEvent(event)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # super(Window, self).__init__()
        self.viewer = SvgViewer(self)
        vb_layout = QtWidgets.QVBoxLayout(self)
        vb_layout.setContentsMargins(0, 0, 0, 0)
        vb_layout.addWidget(self.viewer)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 600, 400)
    window.show()
    sys.exit(app.exec_())