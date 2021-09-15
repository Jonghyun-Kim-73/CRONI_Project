from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class Trend(QWidget):
    def __init__(self, parent, w, h):
        super(Trend, self).__init__()
        self.parent = parent
        if parent is not None:
            self.shmem = parent.shmem
        self.setGeometry(10, 10, w, h)

        self.max_time_leg = 30
        # figure
        self.fig = plt.Figure(facecolor='green')
        self.fig.subplots_adjust(left=0.1, right=0.98, top=0.95, bottom=0.05)
        self.canvas = FigureCanvas(self.fig)
        # ax
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Parameter name')
        self.ax.set_xlim(- self.max_time_leg, 0)
        self.ax.set_ylim(0, 5)
        self.ax.grid()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.max_time_leg = 10

        # Line
        self.line1, = self.ax.plot([], [], color='black', linewidth=1)
        #Q Timer ------------------------------------------------------------------------------------------------------
        timer = QTimer(self)
        timer.setInterval(500)  # 500 ms run = 0.5 sec
        timer.timeout.connect(self.local_loop)
        timer.start()

        self.vallist = [0]  # For test

    def local_loop(self):
        if self.parent is not None:
            saved_db = self.shmem.get_shmem_save_db()
            self._update_trend(saved_db['KCNTOMS'])
        else:
            self.vallist.append(self.vallist[-1] + 1)
            self._update_trend(self.vallist)

    def _update_trend(self, val_list):
        if len(val_list) > 2:
            x = list(reversed([- i for i in range(len(val_list))]))
            self.line1.set_data(x, val_list)

            ratio = 0.05   # 2%
            h_margin = (max(val_list) - min(val_list)) * ((100 * ratio)/(100 - ratio))

            self.ax.set_ylim(min(val_list) - h_margin, max(val_list) + h_margin)
            self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Trend(None, 500, 500)
    window.show()
    sys.exit(app.exec_())