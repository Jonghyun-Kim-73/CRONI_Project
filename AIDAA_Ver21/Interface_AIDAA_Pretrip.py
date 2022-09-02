from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import glob

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
from tqdm.notebook import tqdm
import math

x_test = []
test_x = []
for _ in tqdm(range(len(input_test))):
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
for _ in tqdm(range(len(output_test))):
    numpy_ytest=output_test[_].to_numpy()
    for i in range(math.trunc((len(numpy_ytest)-360))):
        test_y = numpy_ytest[i::3]
        test_y = test_y[0:120]
        y_test.append(test_y)
y_tttest = []
y_train_test = []
for i in range(len(y_test)):
    y_tttest = np.array(y_test[i])
    y_train_test.append(y_tttest)
ytest = np.array(y_train_test)

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

class PreTrip(ABCWidget, QWidget):
    def __init__(self, parent):
        super(PreTrip, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        lay = QHBoxLayout(self)
        lay.addWidget(LeftPrediction(self))
        lay.addWidget(RightPrediction(self))

class LeftPrediction(ABCWidget):
    def __init__(self, parent):
        super(LeftPrediction, self).__init__(parent)
        lay = QVBoxLayout(self)
        lay.addWidget(Parameter(self, id=1))
        lay.addWidget(Parameter(self, id=2))
        lay.addWidget(Parameter(self, id=3))
        lay.addWidget(Parameter(self, id=4))
        lay.addWidget(Parameter(self, id=5))

class RightPrediction(ABCWidget):
    def __init__(self, parent):
        super(RightPrediction, self).__init__(parent)
        lay = QVBoxLayout(self)
        lay.addWidget(Parameter(self, id=6))
        lay.addWidget(Parameter(self, id=7))
        lay.addWidget(Parameter(self, id=8))
        lay.addWidget(Parameter(self, id=9))
        lay.addWidget(Parameter(self, id=10))

class Parameter(ABCWidget): # 그래프 포함
    def __init__(self, parent, id=None):
        super(Parameter, self).__init__(parent)
        self.id = id
        lay = QVBoxLayout(self)
        lay.addWidget(Parameter_Info(self, id=self.id))
        lay.addWidget(Parameter_Graph(self, id=self.id))

class Parameter_Graph(ABCWidget):
    def __init__(self, parent, id=None):
        super(Parameter_Graph, self).__init__(parent)
        self.id = id
        past_data = {1: power_mean_past, 2: over_delta_T_mean_past, 3: prz_pressure_mean_past, 4:prz_level_mean_past, 5:loop3_flow_mean_past, 6:loop2_flow_mean_past, 7: loop1_flow_mean_past, 8:sg3_level_mean_past, 9:sg2_level_mean_past, 10:sg1_level_mean_past}
        grap = {1: power_mean, 2: over_delta_T_mean, 3: prz_pressure_mean, 4:prz_level_mean, 5:loop3_flow_mean, 6:loop2_flow_mean, 7: loop1_flow_mean, 8:sg3_level_mean, 9:sg2_level_mean, 10:sg1_level_mean}
        y_label = {1:'%',2:'%',3:'$Kg/cm^2$', 4:'%',5:'%',6:'%',7:'%',8:'%',9:'%',10:'%'}
        trip_setpoint = {1:[25, 109], 2:[1.3, 1.3],3:[136.78, 167.72],4:[92, 92],5:[90, 90],6:[90, 90],7:[90, 90],8:[17, 17],9:[17, 17],10:[17, 17]}
        lay = QHBoxLayout(self)
        #Shortterm prediction
        canvas = FigureCanvas(Figure())
        lay.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        x = np.arange(0, 120, 1)
        x_real = np.arange(-59, 1, 1)

        self.ax.plot(x_real, past_data[self.id],c='blue',linewidth = '2.5',label = 'Past values')
        self.ax.plot(x, grap[self.id],c='red',linewidth = '2.5',label = 'Prediction results')
        self.ax.set_xlim(-10, 10)
        self.ax.axvline(x=0, linestyle='--', c='black')
        self.ax.set_ylabel(y_label[self.id])
        self.ax.set_title('Short Term Prediction')
        self.ax.axhline(y=trip_setpoint[self.id][0])
        self.ax.axhline(y=trip_setpoint[self.id][1])

        # Longterm prediction
        canvas1 = FigureCanvas(Figure())
        lay.addWidget(canvas1)
        self.ax1 = canvas1.figure.subplots()
        self.ax1.plot(x_real, past_data[self.id],c='blue',linewidth = '2.5',label = 'Past values')
        self.ax1.plot(x, grap[self.id],c='red',linewidth = '2.5',label = 'Prediction results')
        self.ax1.set_xlim(-60, 120)
        self.ax1.axvline(x=0, linestyle='--', c='black')
        self.ax1.set_ylabel(y_label[self.id])
        self.ax1.axhline(y=trip_setpoint[self.id][0])
        self.ax1.axhline(y=trip_setpoint[self.id][1])
        self.ax1.set_title('Long Term Prediction')
        # self.ax1.grid()
        #
        # lay.addWidget(Parameter_ShortTerm(self, id))
asdf = 120
class Parameter_Info(ABCWidget):
    def __init__(self, parent, id=None):
        super(Parameter_Info, self).__init__(parent)
        self.id = id

        name = {1: 'POWER RANGE PERCENT POWER', 2: 'OVERTEMPERATURE DELTA-T', 3: 'PRZ PRESSURE', 4:'PRZ LEVEL', 5:'LOOP 3 FLOW', 6: 'LOOP 2 FLOW', 7: 'LOOP 1 FLOW', 8: 'SG#3 Narrow Range Level', 9: 'SG#2 Narrow Range Level', 10: 'SG#1 Narrow Range Level'}
        Trip_time = {1: '{}'.format(asdf), 2: '2', 3: '3', 4:'4', 5:'5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10'}

        lay = QHBoxLayout(self)
        lay.addWidget(Parameter_name(self, name[self.id]))
        lay.addWidget(TripTimeLabel(self))
        lay.addWidget(Parameter_TripTime(self, Trip_time[self.id]))

class TripTimeLabel(ABCLabel):
    def __init__(self, parent):
        super(TripTimeLabel, self).__init__(parent)
        self.setText('Trip 도달 시간')

class Parameter_name(ABCLabel):
    def __init__(self, parent, name=None):
        super(Parameter_name, self).__init__(parent)
        self.setText(name)

class Parameter_TripTime(ABCLabel):
    def __init__(self, parent, time=None):
        super(Parameter_TripTime, self).__init__(parent)
        self.setText(time)

