from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.CVCS.Core_CVCS_mem import *


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

class Action_alarm_area(ABCTabWidget):
    def __init__(self, parent):
        super(Action_alarm_area, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(149, 185, 211);')
        
        self.column_labels = ['Alarm', '현재값', '정상범위']

        # TODO  =============== 2022-06-18
        
        self.widget_timer(iter_=100, funs=[self.get_info])

    def get_info(self):
        # print(f"H : {Top_CVCS.mem['SimTime']['V']}")
        pass