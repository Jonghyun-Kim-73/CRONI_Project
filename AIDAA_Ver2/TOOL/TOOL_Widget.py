from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


def WithNoMargin(layout, c_m=0, s_m=0):
    layout.setContentsMargins(c_m, c_m, c_m, c_m)
    layout.setSpacing(s_m)
    return layout


def make_shmem(parent, child):
    result = parent.inmem
    result.add_w_id(child)
    return result


class InterfaceMEM:
    def __init__(self, shmem, top_widget, parent):
        self.shmem = shmem
        self.Wid = {}
        # Top widet
        self.top_widget = top_widget
        # 첫 실행시 Mainwindow 저장
        self.add_w_id(parent)

    def get_w_id(self, name):
        return self.Wid[name]

    def add_w_id(self, widget):
        name = type(widget).__name__
        self.Wid[name] = widget

    def show_w(self):
        [print(f'{key:20}:{self.Wid[key]}') for key in self.Wid.keys()]


class ABCWidget(QWidget):
    def __init__(self, parent):
        super(ABCWidget, self).__init__()
        self.inmem: InterfaceMEM = make_shmem(parent, self)


class ABCPushButton(QPushButton):
    def __init__(self, parent, str):
        super(ABCPushButton, self).__init__(str)
        self.inmem: InterfaceMEM = make_shmem(parent, self)


class ABCTableView(QTableView):
    def __init__(self, parent):
        super(ABCTableView, self).__init__()
        self.inmem: InterfaceMEM = make_shmem(parent, self)


class ABCAbstractTableModel(QAbstractTableModel):
    def __init__(self, parent):
        super(ABCAbstractTableModel, self).__init__()
        self.inmem: InterfaceMEM = make_shmem(parent, self)