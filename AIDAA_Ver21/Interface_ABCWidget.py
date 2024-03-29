from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem


def make_shmem(parent, child, widget_name):
    result = parent.inmem
    result.add_widget_id(child, widget_name)
    return result


class TOOL:
    def widget_timer(self, iter_, funs):
        """
        위젯 안에서 timer 로 함수들 업데이트
        :param parent: 위젯 -> self
        :param iter_: 간격
        :param funs: 함수 List
        :return:
        """
        result = QTimer(self)
        result.setInterval(iter_)
        for f_ in funs:
            result.timeout.connect(f_)
        result.start()
        return result


class ABCWidget(QWidget, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCWidget, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)


class ABCPushButton(QPushButton, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCPushButton, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)


class ABCLabel(QLabel, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCLabel, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)


class ABCTabWidget(QTabWidget, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCTabWidget, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)


class ABCTableWidget(QTableWidget, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCTableWidget, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)


class ABCStackWidget(QStackedWidget, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCStackWidget, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)
