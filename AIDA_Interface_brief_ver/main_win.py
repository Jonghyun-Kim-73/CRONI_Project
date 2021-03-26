import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class StatusPanel(QListWidget):
    def __init__(self):
        super(StatusPanel, self).__init__()


class AlarmPanel(QListWidget):
    def __init__(self):
        super(AlarmPanel, self).__init__()

    def add_alarm(self):
        alarm_itme = QListWidgetItem(f'Alarm_{self.parent().db["Count"]}')
        self.parent().db["AlarmList"].append(f'Alarm_{self.parent().db["Count"]}')
        self.parent().db["Count"] += 1
        self.addItem(alarm_itme)
        # --------------------------------------------------------------------------------------------------------------
        self.parent().update()

    def remove_all_alarm(self):
        self.parent().db["Count"] = 1
        self.parent().db["AlarmList"].clear()
        self.parent().db["Selected_Alarm_Procedure"] = ''
        self.clear()
        # --------------------------------------------------------------------------------------------------------------
        self.parent().update()

    def contextMenuEvent(self, event) -> None:
        menu = QMenu(self)
        menu.addAction("Add Alarm", self.add_alarm)
        menu.addAction("Clear Alarm", self.remove_all_alarm)
        menu.exec_(event.globalPos())


class AlarmProcedurePanel(QListWidget):
    def __init__(self):
        super(AlarmProcedurePanel, self).__init__()
        self.itemClicked.connect(self.select_alarm_procedure)

    def select_alarm_procedure_color(self):
        for i in range(self.count()):
            if self.item(i).text() == self.parent().db['Selected_Alarm_Procedure']:
                self.item(i).setBackground(QColor(192, 80, 70))
            else:
                self.item(i).setBackground(QColor(255, 255, 255))

    def select_alarm_procedure(self, item):
        self.parent().db['Selected_Alarm_Procedure'] = item.text()
        self.select_alarm_procedure_color()
        self.parent().update_sub()

    def update(self) -> None:
        self.clear()

        for alarm_name in self.parent().db['AlarmList']:
            alarm_procedure = QListWidgetItem(f'{alarm_name}_Procedure')
            self.addItem(alarm_procedure)

        self.select_alarm_procedure_color()


class AlarmReasonPanel(QListWidget):
    def __init__(self):
        super(AlarmReasonPanel, self).__init__()

    def update(self) -> None:
        self.clear()

        selected_procedure = self.parent().db['Selected_Alarm_Procedure']
        check_reason = True if selected_procedure in self.parent().info_procedure.keys() else False

        if selected_procedure != '' and check_reason:
            for reason in self.parent().info_procedure[selected_procedure]['Reason']:
                alarm_reason = QListWidgetItem(f'{reason:40}\t| Expected State : True | Current State : True')
                self.addItem(alarm_reason)


class AlarmResultPanel(QListWidget):
    def __init__(self):
        super(AlarmResultPanel, self).__init__()

    def update(self) -> None:
        self.clear()

        selected_procedure = self.parent().db['Selected_Alarm_Procedure']
        check_reason = True if selected_procedure in self.parent().info_procedure.keys() else False

        if selected_procedure != '' and check_reason:
            for result in self.parent().info_procedure[selected_procedure]['Result']:
                alarm_result = QListWidgetItem(f'Exoected Result : {result:40}')
                self.addItem(alarm_result)


class AlarmActionPanel(QListWidget):
    def __init__(self):
        super(AlarmActionPanel, self).__init__()
        self.itemChanged.connect(self.change_check_box)

    def change_check_box(self, item):
        # check box 변경되면 저장

        selected_procedure = self.parent().db['Selected_Alarm_Procedure']
        item_type = item.info['type']
        item_name = item.info['name']

        for key in self.parent().info_procedure[selected_procedure][item_type].keys():
            if self.parent().info_procedure[selected_procedure][item_type][key]['name'] == item_name:
                self.parent().info_procedure[selected_procedure][item_type][key]['condition'] = item.checkState()

    def update(self) -> None:
        self.clear()

        selected_procedure = self.parent().db['Selected_Alarm_Procedure']
        check_reason = True if selected_procedure in self.parent().info_procedure.keys() else False

        if selected_procedure != '' and check_reason:
            for action_type_name in ['AutoAction', 'EmergencyAction', 'FollowUpAction']:
                for i in self.parent().info_procedure[selected_procedure][action_type_name].keys():
                    name = self.parent().info_procedure[selected_procedure][action_type_name][i]['name']
                    condition = self.parent().info_procedure[selected_procedure][action_type_name][i]['condition']

                    alarm_action = QListWidgetItem(f'[{action_type_name:30}\t] Exoected Result : {name:40}')
                    alarm_action.info = {'type': action_type_name, 'name': name, 'condition': condition}

                    # 운전원 체크 금지
                    if action_type_name == 'AutoAction':
                        alarm_action.setFlags(alarm_action.flags() ^ Qt.ItemIsUserCheckable)

                    alarm_action.setCheckState(condition)
                    self.addItem(alarm_action)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("AIDA")
        # initial window size
        self.setGeometry(100, 100, 600, 600)

        # initial data Box
        self.db = {
            'Count': 1,
            'Selected_Alarm_Procedure': '',
            'AlarmList': [],
        }

        self.info_procedure = {
            'Alarm_1_Procedure': {
                'Reason': ['Temp > 100', 'Valve 1 Open'],
                'AutoAction': {
                    0: {'name': 'Pump 1 On', 'condition': Qt.Checked},
                    1: {'name': 'Valve 1 Open', 'condition': Qt.Checked},
                },
                'EmergencyAction': {
                    0: {'name': 'Valve 1 Close', 'condition': Qt.Unchecked}
                },
                'FollowUpAction': {
                    0: {'name': 'Call Maintenance', 'condition': Qt.Unchecked},
                },
                'Result': ['Pump 2 is not available.'],
            },
            'Alarm_2_Procedure': {
                'Reason': ['Pres == 50', 'Valve 1 Open', 'Valve 2 Close'],
                'AutoAction': {
                },
                'EmergencyAction': {
                    0: {'name': 'Pump 1 On', 'condition': Qt.Unchecked},
                    1: {'name': 'Valve 2 Close', 'condition': Qt.Unchecked},
                },
                'FollowUpAction': {
                    0: {'name': 'Heater On', 'condition': Qt.Unchecked},
                },
                'Result': ['Connection Line 1 is not connected.'],
            },
        }

        # initial frame
        main_window_layout = QVBoxLayout()
        main_window_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_window_layout)

        # --------------------------------------------------------------------------------------------------------------
        # Alarm panel
        self.status_panel = StatusPanel()
        self.alarm_panel = AlarmPanel()
        self.alarm_procedure_panel = AlarmProcedurePanel()
        self.alarm_reason_panel = AlarmReasonPanel()
        self.alarm_result_panel = AlarmResultPanel()
        self.alarm_auto_action_panel = AlarmActionPanel()
        # --------------------------------------------------------------------------------------------------------------
        main_window_layout.addWidget(QLabel('Status Panel'))
        main_window_layout.addWidget(self.status_panel)
        main_window_layout.addWidget(QLabel('Alarm Panel'))
        main_window_layout.addWidget(self.alarm_panel)
        main_window_layout.addWidget(QLabel('Alarm Suggested Procedure Panel'))
        main_window_layout.addWidget(self.alarm_procedure_panel)
        main_window_layout.addWidget(QLabel('Alarm Reason Panel'))
        main_window_layout.addWidget(self.alarm_reason_panel)
        main_window_layout.addWidget(QLabel('Alarm Result Panel'))
        main_window_layout.addWidget(self.alarm_result_panel)
        main_window_layout.addWidget(QLabel('Alarm Action Panel'))
        main_window_layout.addWidget(self.alarm_auto_action_panel)

    def update(self) -> None:
        self.alarm_procedure_panel.update()
        self.update_sub()

    def update_sub(self) -> None:
        self.alarm_reason_panel.update()
        self.alarm_result_panel.update()
        self.alarm_auto_action_panel.update()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()




