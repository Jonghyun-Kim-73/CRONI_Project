from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_QSS import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import animation
from matplotlib.figure import Figure
import numpy as np
from collections import deque


class PreTrip(ABCWidget):
    def __init__(self, parent):
        super(PreTrip, self).__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 0)

        lay = QHBoxLayout()
        lay.addWidget(LeftPrediction(self))
        lay.addWidget(RightPrediction(self))
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(18)

        layout.addWidget(PreTripTitle(self))
        layout.addLayout(lay)
        layout.setSpacing(15)


class PreTripTitle(ABCLabel):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Trip')
        self.setFixedSize(227, 40)


class LeftPrediction(ABCWidget):
    def __init__(self, parent):
        super(LeftPrediction, self).__init__(parent)
        self.setFixedWidth(941)
        lay = QVBoxLayout(self)
        lay.addWidget(Parameter(self, id=1))
        lay.addWidget(Parameter(self, id=2))
        lay.addWidget(Parameter(self, id=3))
        lay.addWidget(Parameter(self, id=4))
        lay.addWidget(Parameter(self, id=5))
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)


class RightPrediction(ABCWidget):
    def __init__(self, parent):
        super(RightPrediction, self).__init__(parent)
        self.setFixedWidth(941)
        lay = QVBoxLayout(self)
        lay.addWidget(Parameter(self, id=6))
        lay.addWidget(Parameter(self, id=7))
        lay.addWidget(Parameter(self, id=8))
        lay.addWidget(Parameter(self, id=9))
        lay.addWidget(Parameter(self, id=10))
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)


class Parameter(ABCWidget):  # 그래프 포함
    def __init__(self, parent, id=None):
        super(Parameter, self).__init__(parent)
        self.id = id
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(Parameter_Info(self, id=self.id))
        lay.addWidget(Parameter_Graph(self, id=self.id))
        lay.setSpacing(0)
        lay.addStretch(1)


class ParameterGraphSub(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)


class Parameter_Graph(ABCWidget):
    def __init__(self, parent, id=None):
        super(Parameter_Graph, self).__init__(parent)
        self.setFixedSize(941, 173)
        self.setContentsMargins(0, 0, 0, 0)
        self.id = id

        self.y_label = {1: '%', 2: '%', 3: '$Kg/cm^2$', 4: '%', 5: '%', 6: '%', 7: '%', 8: '%', 9: '%', 10: '%'}
        self.trip_setpoint = {1: [25, 109], 2: [1.3, 1.3], 3: [136.78, 167.72], 4: [92, 92], 5: [90, 90], 6: [90, 90],
                         7: [90, 90], 8: [17, 17], 9: [17, 17], 10: [17, 17]}

        lay = QHBoxLayout(self)
        layout_widget1 = ParameterGraphSub(self)
        lay_1 = QHBoxLayout()
        layout_widget1.setLayout(lay_1)
        layout_widget2 = ParameterGraphSub(self)
        lay_2 = QHBoxLayout()
        layout_widget2.setLayout(lay_2)
        lay.addWidget(layout_widget1)
        lay.addWidget(layout_widget2)
        lay.setSpacing(17)
        lay_1.setContentsMargins(5, 5, 5, 5)
        lay_2.setContentsMargins(5, 5, 5, 5)
        plt.rcParams['axes.facecolor'] = rgb_to_hex(LightGray)

        x = np.arange(0, 120, 1)
        x_real = np.arange(-59, 1, 1)

        # Short-Term prediction
        self.canvas = FigureCanvas(Figure(facecolor=rgb_to_hex(LightGray)))
        lay_1.addWidget(self.canvas)
        self.ax = self.canvas.figure.subplots()
        # self.ax.plot(x_real, past_data[self.id],c=rgb_to_hex(DarkGray), linewidth = '2',label = 'Past values')
        self.ax.plot(x_real, x_real, c=rgb_to_hex(DarkGray), linewidth='2', label='Past values')
        # self.ax.plot(x, grap[self.id],c=rgb_to_hex(DarkBlue), linewidth = '2',label = 'Prediction results')
        self.ax.plot(x, x, c=rgb_to_hex(DarkBlue), linewidth='2', label='Prediction results')
        self.ax.set_xlim(-120, 120)
        self.ax.axvline(x=0, linestyle='--', c=rgb_to_hex(DarkGray), linewidth='2')
        self.ax.set_xticks([-120, 0, 120])
        self.ax.set_xticklabels(['-2 min', '0', '2 min'])
        self.ax.tick_params(axis='x', direction='in', which='major', labelsize=7, bottom=False)
        self.ax.tick_params(axis='y', direction='in', which='major', labelsize=7, bottom=False)
        self.ax.set_ylabel(self.y_label[self.id], fontsize='10')
        self.ax.axhline(y=self.trip_setpoint[self.id][0], c=rgb_to_hex(DarkRed), linewidth='2')
        self.ax.axhline(y=self.trip_setpoint[self.id][1], c=rgb_to_hex(DarkRed), linewidth='2')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)

        # Long-Term prediction
        self.canvas1 = FigureCanvas(Figure(facecolor=rgb_to_hex(LightGray)))
        lay_2.addWidget(self.canvas1)
        self.ax1 = self.canvas1.figure.subplots()
        # self.ax1.plot(x_real, past_data[self.id],c=rgb_to_hex(DarkGray),linewidth = '2',label = 'Past values')
        self.ax1.plot(x_real, x_real, c=rgb_to_hex(DarkGray), linewidth='2', label='Past values')
        # self.ax1.plot(x, grap[self.id],c=rgb_to_hex(DarkBlue), linewidth = '2',label = 'Prediction results')
        self.ax1.plot(x, x, c=rgb_to_hex(DarkBlue), linewidth='2', label='Prediction results')
        self.ax1.set_xlim(-3600, 7200)
        self.ax1.axvline(x=0, linestyle='--', c=rgb_to_hex(DarkGray), linewidth='2')
        self.ax1.set_xticks([-3600, 0, 7200])
        self.ax1.set_xticklabels(['-60 min', '0', '120 min'])
        self.ax1.tick_params(axis='x', direction='in', which='major', labelsize=7)
        self.ax1.tick_params(axis='y', direction='in', which='major', labelsize=7)
        self.ax1.set_ylabel(self.y_label[self.id], fontsize='10')
        self.ax1.axhline(y=self.trip_setpoint[self.id][0], c=rgb_to_hex(DarkRed), linewidth='2')
        self.ax1.axhline(y=self.trip_setpoint[self.id][1], c=rgb_to_hex(DarkRed), linewidth='2')
        self.ax1.spines['top'].set_visible(False)
        self.ax1.spines['right'].set_visible(False)
        self.ax1.spines['left'].set_visible(False)

        self.startTimer(1000)

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        try: # Prediction을 눌러야 widget id에 이름이 등록됨.
            if self.inmem.widget_ids['AIDAAMainTopSystemName'].text() == 'Prediction':
                tt = int(self.inmem.ShMem.get_para_val('KCNTOMS') / 5) - (int(self.inmem.ShMem.get_para_val('KCNTOMS') / 5) % 20)
                if tt != 0:
                    # Short-Term Prediction
                    self.ax.cla()

                    self.ax.plot(np.arange(-120, 60, 60), self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(17400+tt*5, 18300+tt*5, 300)), c=rgb_to_hex(DarkGray), linewidth='2', label='Past values')
                    self.ax.plot(np.arange(0, 180, 60), self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000+tt*5, 18900+tt*5, 300)), c=rgb_to_hex(DarkBlue), linewidth='2', label='Prediction results')

                    self.ax.set_xlim(-120, 120)
                    self.ax.axvline(x=0, linestyle='--', c=rgb_to_hex(DarkGray), linewidth='2')
                    self.ax.set_xticks([-120, 0, 120])
                    self.ax.set_xticklabels(['-2 min', '0', '2 min'])
                    self.ax.tick_params(axis='x', direction='in', which='major', labelsize=7, bottom=False)
                    self.ax.tick_params(axis='y', direction='in', which='major', labelsize=7, bottom=False)
                    self.ax.set_ylabel(self.y_label[self.id], fontsize='10')
                    self.ax.axhline(y=self.trip_setpoint[self.id][0], c=rgb_to_hex(DarkRed), linewidth='2')
                    self.ax.axhline(y=self.trip_setpoint[self.id][1], c=rgb_to_hex(DarkRed), linewidth='2')
                    self.ax.spines['top'].set_visible(False)
                    self.ax.spines['right'].set_visible(False)
                    self.ax.spines['left'].set_visible(False)
                    self.canvas.draw()

                    # Long-Term Prediction
                    self.ax1.cla()

                    self.ax1.plot(np.arange(-3600, 60, 60), self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(0+tt*5, 18300+tt*5, 300)), c=rgb_to_hex(DarkGray), linewidth='2', label='Past values')
                    self.ax1.plot(np.arange(0, 7260, 60), self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000+tt*5, 54300+tt*5, 300)), c=rgb_to_hex(DarkBlue), linewidth='2', label='Prediction results')

                    self.ax1.set_xlim(-3600, 7200)
                    self.ax1.axvline(x=0, linestyle='--', c=rgb_to_hex(DarkGray), linewidth='2')
                    self.ax1.set_xticks([-3600, 0, 7200])
                    self.ax1.set_xticklabels(['-60 min', '0', '120 min'])
                    self.ax1.tick_params(axis='x', direction='in', which='major', labelsize=7)
                    self.ax1.tick_params(axis='y', direction='in', which='major', labelsize=7)
                    self.ax1.set_ylabel(self.y_label[self.id], fontsize='10')
                    self.ax1.axhline(y=self.trip_setpoint[self.id][0], c=rgb_to_hex(DarkRed), linewidth='2')
                    self.ax1.axhline(y=self.trip_setpoint[self.id][1], c=rgb_to_hex(DarkRed), linewidth='2')
                    self.ax1.spines['top'].set_visible(False)
                    self.ax1.spines['right'].set_visible(False)
                    self.ax1.spines['left'].set_visible(False)
                    self.canvas1.draw()
        except: pass
        return super().timerEvent(a0)

class Parameter_Info(ABCWidget):
    def __init__(self, parent, id=None):
        super(Parameter_Info, self).__init__(parent)
        self.setFixedHeight(30)
        self.id = id
        name = {1: 'POWER RANGE PERCENT POWER', 2: 'OVERTEMPERATURE DELTA-T', 3: 'PRZ PRESSURE', 4: 'PRZ LEVEL',
                5: 'LOOP 1 FLOW', 6: 'LOOP 2 FLOW', 7: 'LOOP 3 FLOW', 8: 'SG#1 Narrow Range Level',
                9: 'SG#2 Narrow Range Level', 10: 'SG#3 Narrow Range Level'}

        self.power_triptime = 'None'
        self.over_delta_T_triptime = 'None'
        self.prz_pressure_triptime = 'None'
        self.prz_level_triptime = 'None'
        self.loop3_flow_triptime = 'None'
        self.loop2_flow_triptime = 'None'
        self.loop1_flow_triptime = 'None'
        self.sg3_level_triptime = 'None'
        self.sg2_level_triptime = 'None'
        self.sg1_level_triptime = 'None'

        self.Trip_time = {1: f'{self.power_triptime}', 2: f'{self.over_delta_T_triptime}',
                          3: f'{self.prz_pressure_triptime}', 4: f'{self.prz_level_triptime}',
                          5: f'{self.loop3_flow_triptime}', 6: f'{self.loop2_flow_triptime}',
                          7: f'{self.loop1_flow_triptime}', 8: f'{self.sg3_level_triptime}',
                          9: f'{self.sg2_level_triptime}', 10: f'{self.sg1_level_triptime}'}

        self.blink = False
        self.lay = QHBoxLayout(self)
        self.lay.setContentsMargins(15, 0, 0, 0)

        self.parameter_name_w = Parameter_name(self, name[self.id])
        self.trip_time_label_w = TripTimeLabel(self)

        if self.id == 1:
            self.parameter_triptime_w = Parameter_TripTime1(self, self.Trip_time[self.id])
        elif self.id == 2:
            self.parameter_triptime_w = Parameter_TripTime2(self, self.Trip_time[self.id])
        elif self.id == 3:
            self.parameter_triptime_w = Parameter_TripTime3(self, self.Trip_time[self.id])
        elif self.id == 4:
            self.parameter_triptime_w = Parameter_TripTime4(self, self.Trip_time[self.id])
        elif self.id == 5:
            self.parameter_triptime_w = Parameter_TripTime5(self, self.Trip_time[self.id])
        elif self.id == 6:
            self.parameter_triptime_w = Parameter_TripTime6(self, self.Trip_time[self.id])
        elif self.id == 7:
            self.parameter_triptime_w = Parameter_TripTime7(self, self.Trip_time[self.id])
        elif self.id == 8:
            self.parameter_triptime_w = Parameter_TripTime8(self, self.Trip_time[self.id])
        elif self.id == 9:
            self.parameter_triptime_w = Parameter_TripTime9(self, self.Trip_time[self.id])
        elif self.id == 10:
            self.parameter_triptime_w = Parameter_TripTime10(self, self.Trip_time[self.id])

        self.lay.addWidget(self.parameter_name_w)
        self.lay.addWidget(self.trip_time_label_w)
        self.lay.addWidget(self.parameter_triptime_w)

        self.lay.setSpacing(30)
        self.lay.addStretch(1)

        self.counter = deque(maxlen=2)

        self.startTimer(600)

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        if self.inmem.ShMem.get_para_val(f'iPreTrip{self.id}') == 1:
            self.blink = not self.blink
        else:
            self.blink = False
        if self.inmem.ShMem.get_para_val('KLAMPO9') == 1:
            self.inmem.ShMem.change_para_val('iFixTrip', 1)

        self.counter.append(int(self.inmem.ShMem.get_para_val('KCNTOMS') / 5))
        tt = int(self.inmem.ShMem.get_para_val('KCNTOMS') / 5) - (int(self.inmem.ShMem.get_para_val('KCNTOMS') / 5) % 20)

        if tt != 0:
            if self.id == 1:
                if len(np.where(np.logical_or(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300)) < 25, self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300)) > 109))[0]) == 0:
                    self.inmem.widget_ids['Parameter_TripTime1'].setText('None')
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 0)
                else:
                    self.inmem.widget_ids['Parameter_TripTime1'].setText(f"{np.where(np.logical_or(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300)) < 25, self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300)) > 109))[0][0]} min")
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 1)
                    if len(self.counter) == 2 and self.counter[0]+1 == self.counter[-1]:
                        self.inmem.ShMem.change_para_val('iFixPreTrip', 1)
            elif self.id == 2:
                if len(np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))>1.3)[0])==0:
                    self.inmem.widget_ids['Parameter_TripTime2'].setText('None')
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 0)
                else:
                    self.inmem.widget_ids['Parameter_TripTime2'].setText(f"{np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))>1.3)[0][0]} min")
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 1)
                    if len(self.counter) == 2 and self.counter[0] + 1 == self.counter[-1]:
                        self.inmem.ShMem.change_para_val('iFixPreTrip', 1)
            elif self.id == 3:
                if len(np.where(np.logical_or(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))<136.78,self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))>167.72))[0])==0:
                    self.inmem.widget_ids['Parameter_TripTime3'].setText('None')
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 0)
                else:
                    self.inmem.widget_ids['Parameter_TripTime3'].setText(f"{np.where(np.logical_or(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))<136.78,self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))>167.72))[0][0]} min")
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 1)
                    if len(self.counter) == 2 and self.counter[0] + 1 == self.counter[-1]:
                        self.inmem.ShMem.change_para_val('iFixPreTrip', 1)
            elif self.id == 4:
                if len(np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))>92)[0])==0:
                    self.inmem.widget_ids['Parameter_TripTime4'].setText('None')
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 0)
                else:
                    self.inmem.widget_ids['Parameter_TripTime4'].setText(f"{np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))>92)[0][0]} min")
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 1)
                    if len(self.counter) == 2 and self.counter[0] + 1 == self.counter[-1]:
                        self.inmem.ShMem.change_para_val('iFixPreTrip', 1)
            elif self.id == 5:
                if len(np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))<90)[0])==0:
                    self.inmem.widget_ids['Parameter_TripTime5'].setText('None')
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 0)
                else:
                    self.inmem.widget_ids['Parameter_TripTime5'].setText(f"{np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300)) < 90)[0][0]} min")
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 1)
                    if len(self.counter) == 2 and self.counter[0] + 1 == self.counter[-1]:
                        self.inmem.ShMem.change_para_val('iFixPreTrip', 1)
            elif self.id == 6:
                if len(np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))<90)[0])==0:
                    self.inmem.widget_ids['Parameter_TripTime6'].setText('None')
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 0)
                else:
                    self.inmem.widget_ids['Parameter_TripTime6'].setText(f"{np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300)) < 90)[0][0]} min")
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 1)
                    if len(self.counter) == 2 and self.counter[0] + 1 == self.counter[-1]:
                        self.inmem.ShMem.change_para_val('iFixPreTrip', 1)
            elif self.id == 7:
                if len(np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))<90)[0])==0:
                    self.inmem.widget_ids['Parameter_TripTime7'].setText('None')
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 0)
                else:
                    self.inmem.widget_ids['Parameter_TripTime7'].setText(f"{np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300)) < 90)[0][0]} min")
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 1)
                    if len(self.counter) == 2 and self.counter[0] + 1 == self.counter[-1]:
                        self.inmem.ShMem.change_para_val('iFixPreTrip', 1)
            elif self.id == 8:
                if len(np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))<17)[0])==0:
                    self.inmem.widget_ids['Parameter_TripTime8'].setText('None')
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 0)
                else:
                    self.inmem.widget_ids['Parameter_TripTime8'].setText(f"{np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300)) < 17)[0][0]} min")
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 1)
                    if len(self.counter) == 2 and self.counter[0] + 1 == self.counter[-1]:
                        self.inmem.ShMem.change_para_val('iFixPreTrip', 1)
            elif self.id == 9:
                if len(np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))<17)[0])==0:
                    self.inmem.widget_ids['Parameter_TripTime9'].setText('None')
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 0)
                else:
                    self.inmem.widget_ids['Parameter_TripTime9'].setText(f"{np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300)) < 17)[0][0]} min")
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 1)
                    if len(self.counter) == 2 and self.counter[0] + 1 == self.counter[-1]:
                        self.inmem.ShMem.change_para_val('iFixPreTrip', 1)
            elif self.id == 10:
                if len(np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300))<17)[0])==0:
                    self.inmem.widget_ids['Parameter_TripTime10'].setText('None')
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 0)
                else:
                    self.inmem.widget_ids['Parameter_TripTime10'].setText(f"{np.where(self.inmem.get_prediction_result(id=f'{self.id}', time=np.arange(18000 + tt * 5, 54300 + tt * 5, 300)) < 17)[0][0]} min")
                    self.inmem.ShMem.change_para_val(f'iPreTrip{self.id}', 1)
                    if len(self.counter) == 2 and self.counter[0] + 1 == self.counter[-1]:
                        self.inmem.ShMem.change_para_val('iFixPreTrip', 1)

        self.parameter_name_w.setProperty('Blink', 'True' if self.blink else 'False')
        self.parameter_triptime_w.setProperty('Blink', 'True' if self.blink else 'False')
        self.parameter_name_w.style().polish(self.parameter_name_w)
        self.parameter_triptime_w.style().polish(self.parameter_triptime_w)
        return super().timerEvent(a0)

class TripTimeLabel(ABCLabel):
    def __init__(self, parent):
        super(TripTimeLabel, self).__init__(parent)
        self.setFixedSize(180, 30)
        self.setText('Trip 도달 시간')


class Parameter_name(ABCLabel):
    def __init__(self, parent, name=None):
        super(Parameter_name, self).__init__(parent)
        self.setFixedSize(339, 30)
        self.setText(name)

class Parameter_TripTime1(ABCLabel):
    def __init__(self, parent, time=None, widget_name=''):
        super(Parameter_TripTime1, self).__init__(parent, widget_name)
        self.setFixedSize(180, 30)
        self.setText(time)

class Parameter_TripTime2(ABCLabel):
    def __init__(self, parent, time=None, widget_name=''):
        super(Parameter_TripTime2, self).__init__(parent, widget_name)
        self.setFixedSize(180, 30)
        self.setText(time)

class Parameter_TripTime3(ABCLabel):
    def __init__(self, parent, time=None, widget_name=''):
        super(Parameter_TripTime3, self).__init__(parent, widget_name)
        self.setFixedSize(180, 30)
        self.setText(time)

class Parameter_TripTime4(ABCLabel):
    def __init__(self, parent, time=None, widget_name=''):
        super(Parameter_TripTime4, self).__init__(parent, widget_name)
        self.setFixedSize(180, 30)
        self.setText(time)

class Parameter_TripTime5(ABCLabel):
    def __init__(self, parent, time=None, widget_name=''):
        super(Parameter_TripTime5, self).__init__(parent, widget_name)
        self.setFixedSize(180, 30)
        self.setText(time)

class Parameter_TripTime6(ABCLabel):
    def __init__(self, parent, time=None, widget_name=''):
        super(Parameter_TripTime6, self).__init__(parent, widget_name)
        self.setFixedSize(180, 30)
        self.setText(time)

class Parameter_TripTime7(ABCLabel):
    def __init__(self, parent, time=None, widget_name=''):
        super(Parameter_TripTime7, self).__init__(parent, widget_name)
        self.setFixedSize(180, 30)
        self.setText(time)

class Parameter_TripTime8(ABCLabel):
    def __init__(self, parent, time=None, widget_name=''):
        super(Parameter_TripTime8, self).__init__(parent, widget_name)
        self.setFixedSize(180, 30)
        self.setText(time)

class Parameter_TripTime9(ABCLabel):
    def __init__(self, parent, time=None, widget_name=''):
        super(Parameter_TripTime9, self).__init__(parent, widget_name)
        self.setFixedSize(180, 30)
        self.setText(time)

class Parameter_TripTime10(ABCLabel):
    def __init__(self, parent, time=None, widget_name=''):
        super(Parameter_TripTime10, self).__init__(parent, widget_name)
        self.setFixedSize(180, 30)
        self.setText(time)