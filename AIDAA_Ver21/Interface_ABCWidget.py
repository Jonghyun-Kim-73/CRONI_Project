from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
import Interface_QSS as qss
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem

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
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.size()}')
        return super().mousePressEvent(a0)
class ABCDialog(QDialog, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCDialog, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.size()}')
        return super().mousePressEvent(a0)
class ABCScrollArea(QScrollArea, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCScrollArea, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)
    
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.size()}')
        return super().mousePressEvent(a0)
class ABCPushButton(QPushButton, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCPushButton, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)
    
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.size()}')
        return super().mousePressEvent(a0)
class ABCCheckBox(QCheckBox, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCCheckBox, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)
    
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.size()}')
        return super().mousePressEvent(a0)
class ABCLabel(QLabel, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCLabel, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)
    
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.size()}')
        return super().mousePressEvent(a0)
class ABCTabWidget(QTabWidget, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCTabWidget, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)
    
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.size()}')
        return super().mousePressEvent(a0)
class ABCTabWidgetItem(QTableWidgetItem, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCTabWidgetItem, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
class ABCPlainTextEdit(QPlainTextEdit, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCPlainTextEdit, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)
        
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.size()}')
        return super().mousePressEvent(a0)
class ABCGroupBox(QGroupBox, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCGroupBox, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.size()}')
        return super().mousePressEvent(a0)
class ABCTableWidget(QTableWidget, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCTableWidget, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)
    
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.size()}')
        return super().mousePressEvent(a0)
class ABCStackWidget(QStackedWidget, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCStackWidget, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
        self.setAttribute(Qt.WA_StyledBackground, True)
        
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.size()}')
        return super().mousePressEvent(a0)
class ABCGraphicsScene(QGraphicsScene, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCGraphicsScene, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
        
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(f'{self.widget_name}')
        return super().mousePressEvent(a0)
class ABCGraphicsView(QGraphicsView, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCGraphicsView, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.size()}')
        return super().mousePressEvent(event)
class ABCGraphicsRectItem(QGraphicsRectItem):
    def __init__(self, parent, widget_name=''):
        super(ABCGraphicsRectItem, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.shape()}')
        return super().mousePressEvent(event)
class ABCGraphicsSvgItem(QGraphicsSvgItem, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCGraphicsSvgItem, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.shape()}')
        return super().mousePressEvent(event)
class ABCGraphicsTextItem(QGraphicsTextItem, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCGraphicsTextItem, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.shape()}')
        return super().mousePressEvent(event)
class ABCGraphicsPolygonItem(QGraphicsPolygonItem, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCGraphicsPolygonItem, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.shape()}')
        return super().mousePressEvent(event)        
class ABCGraphicsPathItem(QGraphicsPathItem, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCGraphicsPathItem, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name
        self.setObjectName(self.widget_name)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.shape()}')
        return super().mousePressEvent(event)
class ABCGraphicsLineItem(QGraphicsLineItem, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCGraphicsLineItem, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.shape()}')
        return super().mousePressEvent(event)
class ABCGraphicsItemGroup(QGraphicsItemGroup, TOOL):
    def __init__(self, parent, widget_name=''):
        super(ABCGraphicsItemGroup, self).__init__()
        self.inmem: InterfaceMem = make_shmem(parent, self, widget_name)
        self.widget_name=type(self).__name__ if widget_name == '' else widget_name

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print(f'{self.widget_name}, {self.shape()}')
        return super().mousePressEvent(event)