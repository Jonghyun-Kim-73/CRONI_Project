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
        self.ax1.set_xlim(-7200, 7200)
        self.ax1.axvline(x=0, linestyle='--', c=rgb_to_hex(DarkGray), linewidth='2')
        self.ax1.set_xticks([-7200, 0, 7200])
        self.ax1.set_xticklabels(['-120 min', '0', '120 min'])
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
                self.time = np.arange(1, tt + 1)
                if tt != 0:
                    # Short-Term Prediction
                    self.ax.cla()
                    if tt <= 120:
                        self.ax.plot(self.time, self.inmem.get_prediction_result(id=f'{self.id}', time=self.time), c=rgb_to_hex(DarkBlue), linewidth='2', label='Prediction results')
                    elif tt > 120:
                        residual = tt-120
                        temp = np.array(self.time-residual)
                        past_time = np.array(temp[temp < 0])
                        future_time = np.array(temp[temp >= 0])
                        self.ax.plot(past_time, self.inmem.get_prediction_result(id=f'{self.id}', time=self.time[:residual-1]), c=rgb_to_hex(DarkGray), linewidth='2', label='Past values')
                        self.ax.plot(future_time, self.inmem.get_prediction_result(id=f'{self.id}', time=self.time[residual-1:]), c=rgb_to_hex(DarkBlue), linewidth='2', label='Prediction results')
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
                    if tt <= 7200:
                        self.ax.plot(self.time, self.inmem.get_prediction_result(id=f'{self.id}', time=self.time), c=rgb_to_hex(DarkBlue), linewidth='2', label='Prediction results')
                    elif tt > 7200:
                        residual1 = tt - 7200
                        temp1 = np.array(self.time - residual1)
                        past_time1 = np.array(temp1[temp1 < 0])
                        future_time1 = np.array(temp1[temp1 >= 0])
                        self.ax.plot(past_time1, self.inmem.get_prediction_result(id=f'{self.id}', time=self.time[:residual1 - 1]), c=rgb_to_hex(DarkGray), linewidth='2', label='Past values')
                        self.ax.plot(future_time1, self.inmem.get_prediction_result(id=f'{self.id}', time=self.time[residual1 - 1:]), c=rgb_to_hex(DarkBlue), linewidth='2', label='Prediction results')
                    self.ax1.plot(self.time, self.inmem.get_prediction_result(id=f'{self.id}', time=self.time), c=rgb_to_hex(DarkGray), linewidth='2', label='Past values')
                    self.ax1.plot(self.time, self.inmem.get_prediction_result(id=f'{self.id}', time=self.time), c=rgb_to_hex(DarkBlue), linewidth='2', label='Prediction results')
                    self.ax1.set_xlim(-7200, 7200)
                    self.ax1.axvline(x=0, linestyle='--', c=rgb_to_hex(DarkGray), linewidth='2')
                    self.ax1.set_xticks([-7200, 0, 7200])
                    self.ax1.set_xticklabels(['-120 min', '0', '120 min'])
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

    def cal_trip_time(self, id):
        # if len(np.where(np.logical_or(power_mean<25,power_mean>109))[0])==0:
        #     power_triptime = '00:00:00'
        # else:
        #     power_triptime =np.where(np.logical_or(power_mean<25,power_mean>109))[0][0]
        #
        # if len(np.where(over_delta_T_mean>1.3)[0])==0:
        #     over_delta_T_triptime = '00:00:00'
        # else:
        #     over_delta_T_triptime =np.where(over_delta_T_mean>1.3)[0][0]
        #
        # if len(np.where(np.logical_or(prz_pressure_mean<136.78,prz_pressure_mean>167.72))[0])==0:
        #     prz_pressure_triptime = '00:00:00'
        # else:
        #     prz_pressure_triptime = np.where(np.logical_or(prz_pressure_mean<136.78,prz_pressure_mean>167.72))[0][0]
        #
        # if len(np.where(prz_level_mean>92)[0])==0:
        #     prz_level_triptime = '00:00:00'
        # else:
        #     prz_level_triptime =np.where(prz_level_mean>92)[0][0]
        #
        # if len(np.where(loop3_flow_mean<90)[0])==0:
        #     loop3_flow_triptime = '00:00:00'
        # else:
        #     loop3_flow_triptime =np.where(loop3_flow_mean<90)[0][0]
        #
        # if len(np.where(loop2_flow_mean<90)[0])==0:
        #     loop2_flow_triptime = '00:00:00'
        # else:
        #     loop2_flow_triptime =np.where(loop2_flow_mean<90)[0][0]
        #
        # if len(np.where(loop1_flow_mean<90)[0])==0:
        #     loop1_flow_triptime = '00:00:00'
        # else:
        #     loop1_flow_triptime =np.where(loop1_flow_mean<90)[0][0]
        #
        # if len(np.where(sg3_level_mean<17)[0])==0:
        #     sg3_level_triptime = '00:00:00'
        # else:
        #     sg3_level_triptime =np.where(sg3_level_mean<17)[0][0]
        #
        # if len(np.where(sg2_level_mean<17)[0])==0:
        #     sg2_level_triptime = '00:00:00'
        # else:
        #     sg2_level_triptime =np.where(sg2_level_mean<17)[0][0]
        #
        # if len(np.where(sg1_level_mean<17)[0])==0:
        #     sg1_level_triptime = '00:00:00'
        # else:
        #     sg1_level_triptime =np.where(sg1_level_mean<17)[0][0]
        pass


class Parameter_Info(ABCWidget):
    def __init__(self, parent, id=None):
        super(Parameter_Info, self).__init__(parent)
        self.setFixedHeight(30)
        self.id = id
        name = {1: 'POWER RANGE PERCENT POWER', 2: 'OVERTEMPERATURE DELTA-T', 3: 'PRZ PRESSURE', 4: 'PRZ LEVEL',
                5: 'LOOP 1 FLOW', 6: 'LOOP 2 FLOW', 7: 'LOOP 3 FLOW', 8: 'SG#1 Narrow Range Level',
                9: 'SG#2 Narrow Range Level', 10: 'SG#3 Narrow Range Level'}
        # self.Trip_time = {1: '{}'.format(power_triptime), 2: '{}'.format(over_delta_T_triptime), 3: '{}'.format(prz_pressure_triptime), 4:'{}'.format(prz_level_triptime),
        #              5:'{}'.format(loop1_flow_triptime), 6: '{}'.format(loop2_flow_triptime), 7: '{}'.format(loop3_flow_triptime), 8: '{}'.format(sg1_level_triptime), 9: '{}'.format(sg2_level_triptime), 10: '{}'.format(sg3_level_triptime)}
        aa = '00:00:00'
        self.Trip_time = {1: f'{aa}', 2: f'{aa}',
                          3: f'{aa}', 4: f'{aa}',
                          5: f'{aa}', 6: f'{aa}',
                          7: f'{aa}', 8: f'{aa}',
                          9: f'{aa}', 10: f'{aa}'}
        self.blink = False
        self.lay = QHBoxLayout(self)
        self.lay.setContentsMargins(15, 0, 0, 0)

        self.parameter_name_w = Parameter_name(self, name[self.id])
        self.trip_time_label_w = TripTimeLabel(self)
        self.parameter_triptime_w = Parameter_TripTime(self, self.Trip_time[self.id])

        self.lay.addWidget(self.parameter_name_w)
        self.lay.addWidget(self.trip_time_label_w)
        self.lay.addWidget(self.parameter_triptime_w)

        self.lay.setSpacing(30)
        self.lay.addStretch(1)

        self.startTimer(600)

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        if self.inmem.ShMem.get_para_val(f'iPreTrip{self.id}') == 1:
            self.blink = not self.blink
        else:
            self.blink = False
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


class Parameter_TripTime(ABCLabel):
    def __init__(self, parent, time=None):
        super(Parameter_TripTime, self).__init__(parent)
        self.setFixedSize(180, 30)
        self.setText(time)