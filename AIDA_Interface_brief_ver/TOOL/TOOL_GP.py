from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class Trend(QWidget):
    def __init__(self, parent, w, h):
        super(Trend, self).__init__()
        self.viewer = TrendView(self, w, h)
        vb_layout = QVBoxLayout(self)
        vb_layout.setContentsMargins(15, 15, 15, 15)
        vb_layout.addWidget(self.viewer)


class TrendView(QGraphicsView):
    def __init__(self, parent, w, h):
        super(TrendView, self).__init__()
        self.parent = parent
        # self.shmem = parent.shmem

        self.setGeometry(100, 100, w, h)
        self.setFrameStyle(0)   # Frame 바운더리로 인한 그래프 부분 제거

        self._scene = TrendScene(self)
        self.setScene(self._scene)
        # self._scene.clear()

        # Q Timer ------------------------------------------------------------------------------------------------------
        timer = QTimer(self)
        timer.setInterval(25)  # 500 ms run = 0.5 sec
        timer.timeout.connect(self.local_loop)
        timer.start()

        self.vallist = [0]

    def resizeEvent(self, event) -> None:
        # _scene rect update
        self._scene.setSceneRect(QRectF(self.rect()))
        self._scene.update_axis()
        # print(f'Win resize_{self.rect()}_{self._scene.sceneRect()}')

    def update_line(self, vallist):
        """ List 형태의 값을 받아서 라인으로 드로잉 """
        self._scene.update_line(vallist)

    def local_loop(self):
        self.update_line(self.vallist)
        self.vallist.append(self.vallist[-1] + 1)


class TrendScene(QGraphicsScene):
    def __init__(self, parent):
        super(TrendScene, self).__init__()
        self.parent = parent
        # self.shmem = parent.shmem

        self.setSceneRect(QRectF(parent.rect()))        # Same size of parent's rect()

        # 차트 x, y 축
        self.x_axis = AxisItem(0, self.height(), self.width(), self.height(), QPen(Qt.black, 2))
        self.y_axis = AxisItem(0, 0, 0, self.height(), QPen(Qt.black, 2))
        # Line
        self.line_ = LineItem(self, [0, 1], QPen(Qt.blue, 2))

        self.addItem(self.x_axis)
        self.addItem(self.y_axis)
        self.addItem(self.line_)

    def update_line(self, vallist):
        self.line_.line_update(vallist)

    def update_axis(self):
        self.x_axis.line_update(0, self.height(), self.width(), self.height())
        self.y_axis.line_update(0, 0, 0, self.height())
        self.line_.update_axis(self)


class AxisItem(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2, pen, parent=None):
        super(AxisItem, self).__init__(parent)
        self.setLine(QLineF(x1, y1, x2, y2))
        self.setPen(pen)

    def line_update(self, x1, y1, x2, y2):
        self.setLine(QLineF(x1, y1, x2, y2))


class LineItem(QGraphicsPolygonItem):
    def __init__(self, parent, val_list, pen):
        super(LineItem, self).__init__(None)
        self.h = parent.height()
        self.w = parent.width()

        self.points = QPolygonF()
        [self.points.append(QPointF(x, y)) for x, y in enumerate(val_list)]

        self.setPolygon(self.points)
        self.setPen(pen)

    def line_update(self, val_list):
        points = QPolygonF()
        max_len = len(val_list)
        for i in range(max_len):
            x = self.w - 1 * i
            y = self.h - val_list[max_len - i - 1]
            if x < 0: break

            points.append(QPointF(x, y))
        self.setPolygon(points)

    def update_axis(self, parent):
        self.h = parent.height()
        self.w = parent.width()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Trend(None, 200, 200)
    window.show()
    sys.exit(app.exec_())