from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_QSS import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import glob
import math

# from prediction_model import create_model
# model0 = create_model()


# model0.load_weights("Context_variable_0.h5")
# model1 = model0
# model2=model0
# model3=model0
# model4=model0

sel_colums = pd.read_csv('abnormal_all_para_95.csv')
min_input = pd.read_csv('min_all.csv')
min_input=np.array(min_input).T[1]
max_input = pd.read_csv('max_all.csv')
max_input=np.array(max_input).T[1]
minmax_input = max_input-min_input
min_output = pd.read_csv('min_output.csv')
min_output=np.array(min_output).T[1]
max_output=pd.read_csv('max_output.csv')
max_output=np.array(max_output).T[1]
minmax_output = max_output-min_output

test_db = pd.read_pickle('abnormal_test.pkl')
test_X = []
test_Y = []
for q in range(len(test_db)):
    test_x = test_db[q][sel_colums[(sel_colums['Input']==1)]['CNS']][:-360]
    test_X.append(test_x)
    test_y = test_db[q][sel_colums[(sel_colums['Output']==1)]['CNS']][180:]
    test_Y.append(test_y)

x_1 = []
noise_x=[]
for i in range(len(test_X)):
    noise_x = np.random.normal(1,0.019,test_X[i].shape)
    X_1 = ((test_X[i])-min_input)/minmax_input
#     X_1 = ((test_X[i]*noise_x)-min_input)/minmax_input
    x_1.append(X_1)
input_test = pd.Series(x_1)
y_1 = []
noise_y=[]
for i in range(len(test_Y)):
    noise_y = np.random.normal(1,0.03,test_Y[i].shape)
#     Y_1 = ((test_Y[i]*noise_y)-min_output)/minmax_output
    Y_1 = (test_Y[i]-min_output)/minmax_output
    y_1.append(Y_1)
output_test = pd.Series(y_1)

x_test = []
test_x = []
for _ in range(len(input_test)):
    numpy_xtest=input_test[_].to_numpy()

    for i in range(math.trunc((len(numpy_xtest)-180))):
        test_x = numpy_xtest[i::3]
        test_x = test_x[0:60]
        x_test.append(test_x)
x_train_test = []
x_tttest = []
xtest = []
for i in range(len(x_test)):
    x_tttest = np.array(x_test[i])
    x_train_test.append(x_tttest)
xtest = np.array(x_train_test)
time = 0
x_train_test = []
x_tttest = []
y_test = []
test_y = []
for _ in range(len(output_test)):
    numpy_ytest=output_test[_].to_numpy()
    for i in range(math.trunc((len(numpy_ytest)-360))):
        test_y = numpy_ytest[i::3]
        test_y = test_y[0:120]
        y_test.append(test_y)

y_train_test = [np.array(y_test[i]) for i in range(len(y_test))]
ytest = np.array(y_train_test)
"""
# xest_divide = np.reshape(xtest[time], (1, 60, 100))
#
# predict0 = []
# predict1 = []
# predict2 = []
# predict3 = []
# predict4 = []
#
# power = []
# over_delta_T = []
# prz_pressure = []
# prz_level = []
# loop3_flow = []
# loop2_flow = []
# loop1_flow = []
# sg3_level = []
# sg2_level = []
# sg1_level = []
#
# power_mean = []
# over_delta_T_mean = []
# prz_pressure_mean = []
# prz_level_mean = []
# loop3_flow_mean = []
# loop2_flow_mean = []
# loop1_flow_mean = []
# sg3_level_mean = []
# sg2_level_mean = []
# sg1_level_mean = []
#
# power_var = []
# over_delta_T_var = []
# prz_pressure_var = []
# prz_level_var = []
# loop3_flow_var = []
# loop2_flow_var = []
# loop1_flow_var = []
# sg3_level_var = []
# sg2_level_var = []
# sg1_level_var = []
#
# power_sta = []
# over_delta_T_sta = []
# prz_pressure_sta = []
# prz_level_sta = []
# loop3_flow_sta = []
# loop2_flow_sta = []
# loop1_flow_sta = []
# sg3_level_sta = []
# sg2_level_sta = []
# sg1_level_sta = []
#
# i = 0
# forward_pass = 100
# while i < 20:
#     xest_divide_re0 = []
#     xest_divide_re1 = []
#     xest_divide_re2 = []
#     xest_divide_re3 = []
#     xest_divide_re4 = []
#     xest_divide_noise0 = np.random.normal(1, 0.019, xest_divide.shape)
#     xest_divide_re0 = xest_divide * xest_divide_noise0
#     xest_divide_noise1 = np.random.normal(1, 0.019, xest_divide.shape)
#     xest_divide_re1 = xest_divide * xest_divide_noise1
#     xest_divide_noise2 = np.random.normal(1, 0.019, xest_divide.shape)
#     xest_divide_re2 = xest_divide * xest_divide_noise2
#     xest_divide_noise3 = np.random.normal(1, 0.019, xest_divide.shape)
#     xest_divide_re3 = xest_divide * xest_divide_noise3
#     xest_divide_noise4 = np.random.normal(1, 0.019, xest_divide.shape)
#     xest_divide_re4 = xest_divide * xest_divide_noise4
#     predict0 = np.reshape(model0.predict(xest_divide_re0), (120, 10))
#     predict1 = np.reshape(model1.predict(xest_divide_re1), (120, 10))
#     predict2 = np.reshape(model2.predict(xest_divide_re2), (120, 10))
#     predict3 = np.reshape(model3.predict(xest_divide_re3), (120, 10))
#     predict4 = np.reshape(model4.predict(xest_divide_re4), (120, 10))
#
#     power.append(predict0.T[0].flatten())
#     power.append(predict1.T[0].flatten())
#     power.append(predict2.T[0].flatten())
#     power.append(predict3.T[0].flatten())
#     power.append(predict4.T[0].flatten())
#
#     over_delta_T.append(predict0.T[1].flatten())
#     over_delta_T.append(predict1.T[1].flatten())
#     over_delta_T.append(predict2.T[1].flatten())
#     over_delta_T.append(predict3.T[1].flatten())
#     over_delta_T.append(predict4.T[1].flatten())
#
#     prz_pressure.append(predict0.T[2].flatten())
#     prz_pressure.append(predict1.T[2].flatten())
#     prz_pressure.append(predict2.T[2].flatten())
#     prz_pressure.append(predict3.T[2].flatten())
#     prz_pressure.append(predict4.T[2].flatten())
#
#     prz_level.append(predict0.T[3].flatten())
#     prz_level.append(predict1.T[3].flatten())
#     prz_level.append(predict2.T[3].flatten())
#     prz_level.append(predict3.T[3].flatten())
#     prz_level.append(predict4.T[3].flatten())
#
#     loop3_flow.append(predict0.T[4].flatten())
#     loop3_flow.append(predict1.T[4].flatten())
#     loop3_flow.append(predict2.T[4].flatten())
#     loop3_flow.append(predict3.T[4].flatten())
#     loop3_flow.append(predict4.T[4].flatten())
#
#     loop2_flow.append(predict0.T[5].flatten())
#     loop2_flow.append(predict1.T[5].flatten())
#     loop2_flow.append(predict2.T[5].flatten())
#     loop2_flow.append(predict3.T[5].flatten())
#     loop2_flow.append(predict4.T[5].flatten())
#
#     loop1_flow.append(predict0.T[6].flatten())
#     loop1_flow.append(predict1.T[6].flatten())
#     loop1_flow.append(predict2.T[6].flatten())
#     loop1_flow.append(predict3.T[6].flatten())
#     loop1_flow.append(predict4.T[6].flatten())
#
#     sg3_level.append(predict0.T[7].flatten())
#     sg3_level.append(predict1.T[7].flatten())
#     sg3_level.append(predict2.T[7].flatten())
#     sg3_level.append(predict3.T[7].flatten())
#     sg3_level.append(predict4.T[7].flatten())
#
#     sg2_level.append(predict0.T[8].flatten())
#     sg2_level.append(predict1.T[8].flatten())
#     sg2_level.append(predict2.T[8].flatten())
#     sg2_level.append(predict3.T[8].flatten())
#     sg2_level.append(predict4.T[8].flatten())
#
#     sg1_level.append(predict0.T[9].flatten())
#     sg1_level.append(predict1.T[9].flatten())
#     sg1_level.append(predict2.T[9].flatten())
#     sg1_level.append(predict3.T[9].flatten())
#     sg1_level.append(predict4.T[9].flatten())
#
#     i += 1
#
# power_data = pd.DataFrame(power)
# over_delta_T_data = pd.DataFrame(over_delta_T)
# prz_pressure_data = pd.DataFrame(prz_pressure)
# prz_level_data = pd.DataFrame(prz_level)
# loop3_flow_data = pd.DataFrame(loop3_flow)
# loop2_flow_data = pd.DataFrame(loop2_flow)
# loop1_flow_data = pd.DataFrame(loop1_flow)
# sg3_level_data = pd.DataFrame(sg3_level)
# sg2_level_data = pd.DataFrame(sg2_level)
# sg1_level_data = pd.DataFrame(sg1_level)
#
# for j in range(len(power_data.T)):
#     power_mean.append(power_data[j].mean())
#     over_delta_T_mean.append(over_delta_T_data[j].mean())
#     prz_pressure_mean.append(prz_pressure_data[j].mean())
#     prz_level_mean.append(prz_level_data[j].mean())
#     loop3_flow_mean.append(loop3_flow_data[j].mean())
#     loop2_flow_mean.append(loop2_flow_data[j].mean())
#     loop1_flow_mean.append(loop1_flow_data[j].mean())
#     sg3_level_mean.append(sg3_level_data[j].mean())
#     sg2_level_mean.append(sg2_level_data[j].mean())
#     sg1_level_mean.append(sg1_level_data[j].mean())
#
#     power_var.append(power_data[j].var())
#     over_delta_T_var.append(over_delta_T_data[j].var())
#     prz_pressure_var.append(prz_pressure_data[j].var())
#     prz_level_var.append(prz_level_data[j].var())
#     loop3_flow_var.append(loop3_flow_data[j].var())
#     loop2_flow_var.append(loop2_flow_data[j].var())
#     loop1_flow_var.append(loop1_flow_data[j].var())
#     sg3_level_var.append(sg3_level_data[j].var())
#     sg2_level_var.append(sg2_level_data[j].var())
#     sg1_level_var.append(sg1_level_data[j].var())
#
# power_mean = pd.Series(power_mean)
# over_delta_T_mean = pd.Series(over_delta_T_mean)
# prz_pressure_mean = pd.Series(prz_pressure_mean)
# prz_level_mean = pd.Series(prz_level_mean)
# loop3_flow_mean = pd.Series(loop3_flow_mean)
# loop2_flow_mean = pd.Series(loop2_flow_mean)
# loop1_flow_mean = pd.Series(loop1_flow_mean)
# sg3_level_mean = pd.Series(sg3_level_mean)
# sg2_level_mean = pd.Series(sg2_level_mean)
# sg1_level_mean = pd.Series(sg1_level_mean)
#
# power_mean = power_mean*minmax_output[0]+min_output[0]
# over_delta_T_mean = over_delta_T_mean*minmax_output[1]+min_output[1]
# prz_pressure_mean = prz_pressure_mean*minmax_output[2]+min_output[2]
# prz_level_mean = prz_level_mean*minmax_output[3]+min_output[3]
# loop3_flow_mean = loop3_flow_mean*minmax_output[4]+min_output[4]
# loop2_flow_mean = loop2_flow_mean*minmax_output[5]+min_output[5]
# loop1_flow_mean = loop1_flow_mean*minmax_output[6]+min_output[6]
# sg3_level_mean = sg3_level_mean*minmax_output[7]+min_output[7]
# sg2_level_mean =sg2_level_mean*minmax_output[8]+min_output[8]
# sg1_level_mean = sg1_level_mean*minmax_output[9]+min_output[9]
# # result_mean = []
# # result_mean.append()
#
# power_var = pd.Series(power_var)
# over_delta_T_var = pd.Series(over_delta_T_var)
# prz_pressure_var = pd.Series(prz_pressure_var)
# prz_level_var = pd.Series(prz_level_var)
# loop3_flow_var = pd.Series(loop3_flow_var)
# loop2_flow_var = pd.Series(loop2_flow_var)
# loop1_flow_var = pd.Series(loop1_flow_var)
# sg3_level_var = pd.Series(sg3_level_var)
# sg2_level_var = pd.Series(sg2_level_var)
# sg1_level_var = pd.Series(sg1_level_var)
#
# power_sta = ((power_var * forward_pass) / (forward_pass - 1)) ** 0.5
# over_delta_T_sta = ((over_delta_T_var * forward_pass) / (forward_pass - 1)) ** 0.5
# prz_pressure_sta = ((prz_pressure_var * forward_pass) / (forward_pass - 1)) ** 0.5
# prz_level_sta = ((prz_level_var * forward_pass) / (forward_pass - 1)) ** 0.5
# loop3_flow_sta = ((loop3_flow_var * forward_pass) / (forward_pass - 1)) ** 0.5
# loop2_flow_sta = ((loop2_flow_var * forward_pass) / (forward_pass - 1)) ** 0.5
# loop1_flow_sta = ((loop1_flow_var * forward_pass) / (forward_pass - 1)) ** 0.5
# sg3_level_sta = ((sg3_level_var * forward_pass) / (forward_pass - 1)) ** 0.5
# sg2_level_sta = ((sg2_level_var * forward_pass) / (forward_pass - 1)) ** 0.5
# sg1_level_sta = ((sg1_level_var * forward_pass) / (forward_pass - 1)) ** 0.5
#
"""
power_mean = ytest[time][:,0]*minmax_output[0]+min_output[0]
over_delta_T_mean = ytest[time][:,1]*minmax_output[1]+min_output[1]
prz_pressure_mean = ytest[time][:,2]*minmax_output[2]+min_output[2]
prz_level_mean = ytest[time][:,3]*minmax_output[3]+min_output[3]
loop3_flow_mean = ytest[time][:,4]*minmax_output[4]+min_output[4]
loop2_flow_mean = ytest[time][:,5]*minmax_output[5]+min_output[5]
loop1_flow_mean = ytest[time][:,6]*minmax_output[6]+min_output[6]
sg3_level_mean = ytest[time][:,7]*minmax_output[7]+min_output[7]
sg2_level_mean =ytest[time][:,8]*minmax_output[8]+min_output[8]
sg1_level_mean = ytest[time][:,9]*minmax_output[9]+min_output[9]


power_mean_past = xtest[time][:,0]*minmax_output[0]+min_output[0]
over_delta_T_mean_past = xtest[time][:,1]*minmax_output[1]+min_output[1]
prz_pressure_mean_past = xtest[time][:,2]*minmax_output[2]+min_output[2]
prz_level_mean_past = xtest[time][:,3]*minmax_output[3]+min_output[3]
loop3_flow_mean_past = xtest[time][:,4]*minmax_output[4]+min_output[4]
loop2_flow_mean_past = xtest[time][:,5]*minmax_output[5]+min_output[5]
loop1_flow_mean_past = xtest[time][:,6]*minmax_output[6]+min_output[6]
sg3_level_mean_past = xtest[time][:,7]*minmax_output[7]+min_output[7]
sg2_level_mean_past =xtest[time][:,8]*minmax_output[8]+min_output[8]
sg1_level_mean_past = xtest[time][:,9]*minmax_output[9]+min_output[9]

power_mean=power_mean.astype(np.float32)
over_delta_T_mean=over_delta_T_mean.astype(np.float32)
prz_pressure_mean=prz_pressure_mean.astype(np.float32)
prz_level_mean=prz_level_mean.astype(np.float32)
loop3_flow_mean=loop3_flow_mean.astype(np.float32)
loop2_flow_mean=loop2_flow_mean.astype(np.float32)
loop1_flow_mean=loop1_flow_mean.astype(np.float32)
sg3_level_mean=sg3_level_mean.astype(np.float32)
sg2_level_mean=sg2_level_mean.astype(np.float32)
sg1_level_mean=sg1_level_mean.astype(np.float32)
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
class Parameter(ABCWidget): # 그래프 포함
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
        past_data = {1: power_mean_past, 2: over_delta_T_mean_past, 3: prz_pressure_mean_past, 
                     4:prz_level_mean_past, 5:loop3_flow_mean_past, 6:loop2_flow_mean_past, 
                     7: loop1_flow_mean_past, 8:sg3_level_mean_past, 9:sg2_level_mean_past, 10:sg1_level_mean_past}
        grap = {1: power_mean, 2: over_delta_T_mean, 3: prz_pressure_mean, 4:prz_level_mean, 5:loop3_flow_mean, 6:loop2_flow_mean, 7: loop1_flow_mean, 8:sg3_level_mean, 9:sg2_level_mean, 10:sg1_level_mean}
        y_label = {1:'%',2:'%',3:'$Kg/cm^2$', 4:'%',5:'%',6:'%',7:'%',8:'%',9:'%',10:'%'}
        trip_setpoint = {1:[25, 109], 2:[1.3, 1.3],3:[136.78, 167.72],4:[92, 92],5:[90, 90],6:[90, 90],7:[90, 90],8:[17, 17],9:[17, 17],10:[17, 17]}
        lay = QHBoxLayout(self)

        # stylesheet 적용 위함
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
        #Shortterm prediction
        canvas = FigureCanvas(Figure(facecolor=rgb_to_hex(LightGray)))
        lay_1.addWidget(canvas)
        self.ax = canvas.figure.subplots()

        x = np.arange(0, 120, 1)
        x_real = np.arange(-59, 1, 1)

        self.ax.plot(x_real, past_data[self.id],c=rgb_to_hex(DarkGray), linewidth = '2',label = 'Past values')
        self.ax.plot(x, grap[self.id],c=rgb_to_hex(DarkBlue), linewidth = '2',label = 'Prediction results')
        self.ax.set_xlim(-10, 10)
        self.ax.axvline(x=0, linestyle='--', c=rgb_to_hex(DarkGray), linewidth = '2')
        self.ax.set_xticks([-10, 0, 10])
        self.ax.set_xticklabels(['-10min', '0', '10min'])
        self.ax.tick_params(axis='x', direction='in', which='major', labelsize=7, bottom=False)
        self.ax.tick_params(axis='y', direction='in', which='major', labelsize=7, bottom=False)
        self.ax.set_ylabel(y_label[self.id], fontsize='10')
        self.ax.axhline(y=trip_setpoint[self.id][0], c=rgb_to_hex(DarkRed), linewidth = '2')
        self.ax.axhline(y=trip_setpoint[self.id][1], c=rgb_to_hex(DarkRed), linewidth = '2')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)

        # Longterm prediction
        canvas1 = FigureCanvas(Figure(facecolor=rgb_to_hex(LightGray)))
        lay_2.addWidget(canvas1)
        self.ax1 = canvas1.figure.subplots()
        self.ax1.plot(x_real, past_data[self.id],c=rgb_to_hex(DarkGray),linewidth = '2',label = 'Past values')
        self.ax1.plot(x, grap[self.id],c=rgb_to_hex(DarkBlue), linewidth = '2',label = 'Prediction results')
        self.ax1.set_xlim(-60, 120)
        self.ax1.axvline(x=0, linestyle='--', c=rgb_to_hex(DarkGray), linewidth = '2')
        self.ax1.set_xticks([-60, 0, 120])
        self.ax1.set_xticklabels(['-60min', '0', '120min'])
        self.ax1.tick_params(axis='x', direction='in', which='major', labelsize=7)
        self.ax1.tick_params(axis='y', direction='in', which='major', labelsize=7)
        self.ax1.set_ylabel(y_label[self.id], fontsize='10')
        self.ax1.axhline(y=trip_setpoint[self.id][0], c=rgb_to_hex(DarkRed), linewidth = '2')
        self.ax1.axhline(y=trip_setpoint[self.id][1], c=rgb_to_hex(DarkRed), linewidth = '2')
        self.ax1.spines['top'].set_visible(False)
        self.ax1.spines['right'].set_visible(False)
        self.ax1.spines['left'].set_visible(False)
        # self.ax1.grid()
        #
        # lay.addWidget(Parameter_ShortTerm(self, id))
if len(np.where(np.logical_or(power_mean<25,power_mean>109))[0])==0:
    power_triptime = '00:00:00'
else:
    power_triptime =np.where(np.logical_or(power_mean<25,power_mean>109))[0][0]

if len(np.where(over_delta_T_mean>1.3)[0])==0:
    over_delta_T_triptime = '00:00:00'
else:
    over_delta_T_triptime =np.where(over_delta_T_mean>1.3)[0][0]

if len(np.where(np.logical_or(prz_pressure_mean<136.78,prz_pressure_mean>167.72))[0])==0:
    prz_pressure_triptime = '00:00:00'
else:
    prz_pressure_triptime = np.where(np.logical_or(prz_pressure_mean<136.78,prz_pressure_mean>167.72))[0][0]

if len(np.where(prz_level_mean>92)[0])==0:
    prz_level_triptime = '00:00:00'
else:
    prz_level_triptime =np.where(prz_level_mean>92)[0][0]

if len(np.where(loop3_flow_mean<90)[0])==0:
    loop3_flow_triptime = '00:00:00'
else:
    loop3_flow_triptime =np.where(loop3_flow_mean<90)[0][0]

if len(np.where(loop2_flow_mean<90)[0])==0:
    loop2_flow_triptime = '00:00:00'
else:
    loop2_flow_triptime =np.where(loop2_flow_mean<90)[0][0]

if len(np.where(loop1_flow_mean<90)[0])==0:
    loop1_flow_triptime = '00:00:00'
else:
    loop1_flow_triptime =np.where(loop1_flow_mean<90)[0][0]

if len(np.where(sg3_level_mean<17)[0])==0:
    sg3_level_triptime = '00:00:00'
else:
    sg3_level_triptime =np.where(sg3_level_mean<17)[0][0]

if len(np.where(sg2_level_mean<17)[0])==0:
    sg2_level_triptime = '00:00:00'
else:
    sg2_level_triptime =np.where(sg2_level_mean<17)[0][0]

if len(np.where(sg1_level_mean<17)[0])==0:
    sg1_level_triptime = '00:00:00'
else:
    sg1_level_triptime =np.where(sg1_level_mean<17)[0][0]
class Parameter_Info(ABCWidget):
    def __init__(self, parent, id=None):
        super(Parameter_Info, self).__init__(parent)
        self.setFixedHeight(30)
        self.id = id
        name = {1: 'POWER RANGE PERCENT POWER', 2: 'OVERTEMPERATURE DELTA-T', 3: 'PRZ PRESSURE', 4:'PRZ LEVEL', 5:'LOOP 3 FLOW', 6: 'LOOP 2 FLOW', 7: 'LOOP 1 FLOW', 8: 'SG#3 Narrow Range Level', 9: 'SG#2 Narrow Range Level', 10: 'SG#1 Narrow Range Level'}
        self.Trip_time = {1: '{}'.format(power_triptime), 2: '{}'.format(over_delta_T_triptime), 3: '{}'.format(prz_pressure_triptime), 4:'{}'.format(prz_level_triptime),
                     5:'{}'.format(loop3_flow_triptime), 6: '{}'.format(loop2_flow_triptime), 7: '{}'.format(loop1_flow_triptime), 8: '{}'.format(sg3_level_triptime), 9: '{}'.format(sg2_level_triptime), 10: '{}'.format(sg1_level_triptime)}
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
        
        self.startTimer(300)
    
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