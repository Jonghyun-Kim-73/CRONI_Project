import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont, QPolygon
from PyQt5.QtCore import Qt, QPoint

# X축 범위
class Arrow(QWidget):
    def __init__(self, parent=None, x=None, y=None, x2=None, y2=None, type=None):
        super(Arrow, self).__init__(parent)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.type = type
        self.setGeometry(0, 0, 1500, 300)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_polygon(qp)
        qp.end()

    def draw_polygon(self, qp):
        points_L = [
            QPoint(self.x-8, self.y),
            QPoint(self.x, self.y-4),
            QPoint(self.x, self.y+4)
        ]
        # elif self.type == 3:
        points_R = [
            QPoint(self.x2+8, self.y2),
            QPoint(self.x2, self.y2-4),
            QPoint(self.x2, self.y2+4)
        ]
        polygon_left = QPolygon(points_L)
        polygon_right = QPolygon(points_R)
        qp.setPen(QPen(Qt.black, 2))
        qp.setBrush(QBrush(Qt.black))
        qp.drawPolygon(polygon_left)
        qp.drawPolygon(polygon_right)
        qp.drawLine(self.x, self.y, self.x2, self.y2)

        qp.setFont(QFont('Arial', 10, QFont.Bold))
        qp.drawText(self.x-8, self.y-7, "-2")

        if self.type == 0:
            qp.drawText(self.x2 - 5, self.y - 7, "2")
            qp.drawText((self.x + self.x2) / 2 - 3, self.y - 7, "0")
        else:
            qp.drawText(self.x2 - 13, self.y - 7, "120")
            qp.drawText(42, self.y - 7, "0")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win_main = Arrow(x=100, y=100, x2=200, y2=100, type=0)
    win_main.show()
    app.exec_()