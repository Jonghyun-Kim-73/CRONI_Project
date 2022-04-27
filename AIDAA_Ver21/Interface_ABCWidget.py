from PyQt5.QtWidgets import *
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem


def make_shmem(parent, child, widget_name):
    result = parent.inmem
    result.add_widget_id(child, widget_name)
    return result


class ABCWidget(QWidget):
    def __init__(self, parent, widget_name=''):
        super(ABCWidget, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)


class ABCPushButton(QPushButton):
    def __init__(self, parent, widget_name=''):
        super(ABCPushButton, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)


class ABCLabel(QLabel):
    def __init__(self, parent, widget_name=''):
        super(ABCLabel, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
