from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer

from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.CVCS.Core_CVCS_mem import *

from AIDAA_Ver21.Interface_QSS import *

alarm_dict = {
    'KLAMPO260': {'des':'L/D HX OUTLET FLOW LOW(15 M3/HR)'},
    'KLAMPO263': {'des':'VCT LEVEL LOW(20 %)'},
    'KLAMPO264': {'des':'VCT PRESS LOW(0.7 KG/CM2)'},
    'KLAMPO265': {'des':'RCP SEAL INJ WTR FLOW LOW(1.4 M3/HR)'},
    'KLAMPO266': {'des':'CHARGING FLOW CONT FLOW LOW(5 M3/HR)'},
    'KLAMPO268': {'des':'L/D HX OUTLET FLOW HIGH(30 M3/HR)'},
    'KLAMPO271': {'des':'VCT LEVEL HIGH(80 %)'},
    'KLAMPO272': {'des':'VCT PRESS HIGH(4.5 KG/CM2)'},
    'KLAMPO274': {'des':'CHARGING FLOW CONT FLOW HIGH(27 M3/HR)'},
    'KLAMPO301': {'des':'RAD HIGH ALARM'},
    'KLAMPO307': {'des':'PRZ PRESS HIGH ALERT(162.4 KG/CM2)'},
    'KLAMPO308': {'des':'PRZ PRESS LOW ALERT(153.6 KG/CM2)'},
    'KLAMPO310': {'des':'PRZ CONT LEVEL HIGH HEATER ON(OVER 5%)'},
    'KLAMPO311': {'des':'PRZ CONT LEVEL LOW HEATER OFF(17%)'},
    'KLAMPO312': {'des':'PRZ PRESS LOW BACK-UP HEATER ON(153.6 KG/CM2)'},
    }

class ActionMimicArea(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        lay = QVBoxLayout(self)
        self.ActionMimicScene = ActionMimicScene(self)
        self.ActionMimicView = ActionMimicView(self, scene=self.ActionMimicScene)
        lay.addWidget(self.ActionMimicView)
        lay.setContentsMargins(0, 0, 0, 0)
    def resizeEvent(self, a0: QResizeEvent) -> None:
        w, h = self.ActionMimicView.size().width(), self.ActionMimicView.size().height()
        self.ActionMimicScene.setSceneRect(QRectF(0, 0, w, h))
class ActionMimicView(ABCGraphicsView):
    def __init__(self, parent, scene, widget_name=''):
        super().__init__(parent, widget_name)
        self.setScene(scene)
        self.setStyleSheet("border: 0px")
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
class ActionMimicScene(ABCGraphicsScene):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setBackgroundBrush(rgb_to_qCOLOR(LightGray))
        self.addItem(ActionMimicSceneBackground(self))
class ActionMimicSceneBackground(ABCGraphicsRectItem):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)

    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Outline RoundRect
        x = self.inmem.widget_ids['ActionMimicView'].rect().x() + 1
        y = self.inmem.widget_ids['ActionMimicView'].rect().y() + 1
        w = self.inmem.widget_ids['ActionMimicView'].rect().width() - 1 - 2
        h = self.inmem.widget_ids['ActionMimicView'].rect().height() -1 - 2
        painter.setPen(QPen(rgb_to_qCOLOR(DarkGray), 2, Qt.PenStyle.SolidLine))
        painter.drawRoundedRect(QRect(x, y, w, h), 10, 10)
        return super().paint(painter, option, widget)