from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class TrendView(QWidget):
    def __init__(self, parent):
        super(TrendView, self).__init__()
        self.parent = parent
        self.shmem = parent.shmem

        # Q Timer ------------------------------------------------------------------------------------------------------
        timer = QTimer(self)
        timer.setInterval(500)  # 500 ms run = 0.5 sec
        timer.timeout.connect(self.local_loop)
        timer.start()

    def local_loop(self):
        self.update()
