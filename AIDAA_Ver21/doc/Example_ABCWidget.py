from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *


class Mainwidget(QWidget):
    def __init__(self, ShMem):
        super(Mainwidget, self).__init__()
        self.inmem: InterfaceMem = InterfaceMem(ShMem, self)
        self.setGeometry(50, 50, 500, 500)
        """
        Widget A 와 Widget B는 동일 Level에 위치
        """
        layout = QHBoxLayout(self)
        self._widgetA = WidgetA(self)
        self._widgetB = WidgetB(self)
        layout.addWidget(self._widgetA)
        layout.addWidget(self._widgetB)

        # 등록된 Widget 들의 id 보기.
        print(self.inmem.show_widget_ids())


class WidgetA(ABCWidget, QWidget):
    def __init__(self, parent):
        super(WidgetA, self).__init__(parent)
        layout = QHBoxLayout(self)
        L = LabelA1(self)
        L.setStyleSheet('background: rgb(200, 100, 50);')
        layout.addWidget(L)

    def do_something(self):
        print('WidgetA Do Something')


class LabelA1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(LabelA1, self).__init__(parent)
        self.setText('0')
        self.val = 0

    def add_val_and_show(self):
        self.val += 1
        self.setText(f'{self.val}')


class WidgetB(ABCWidget, QWidget):
    def __init__(self, parent):
        super(WidgetB, self).__init__(parent)
        layout = QHBoxLayout(self)
        L = QLabel('WidgetB', self)
        L.setStyleSheet('background: rgb(24, 144, 255);')

        layout.addWidget(L)
        layout.addWidget(BtnB1(self))

    def do_something(self):
        print('WidgetB Do Something')


class BtnB1(ABCPushButton, QPushButton):
    def __init__(self, parent):
        super(BtnB1, self).__init__(parent)
        self.setStyleSheet('background: rgb(255, 255, 0);')
        self.clicked.connect(self.do)

    def do(self):
        print('Do!')

        """
        아래 코드를 보면, dict의 키 값을 사용함으로써 계층적 관계를 무시하고 id 값에 직접 접근하여 함수를 사용할 수 있음.
        """
        self.inmem.widget_ids['WidgetA'].do_something()
        self.inmem.widget_ids['WidgetB'].do_something()
        self.inmem.widget_ids['LabelA1'].add_val_and_show()


if __name__ == '__main__':
    mem = ShMem()
    app = QApplication(sys.argv)
    w = Mainwidget(mem)
    w.show()
    sys.exit(app.exec_())