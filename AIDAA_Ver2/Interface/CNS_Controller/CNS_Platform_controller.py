#
import sys
import multiprocessing
from copy import deepcopy
import time
import json

import random

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#
from AIDAA_Ver2.Interface.CNS_Controller import CNS_Platform_controller_interface as CNS_controller
from AIDAA_Ver2.Interface.main_window import Mainwindow
from AIDAA_Ver2.TOOL.TOOL_etc import p_, pc_
from AIDAA_Ver2.Interface.Graph.MatGP import Trend


class InterfaceFun(multiprocessing.Process):
    def __init__(self, shmem):
        multiprocessing.Process.__init__(self)
        self.shmem = shmem

    def run(self):
        app = QApplication(sys.argv)
        app.setStyle("fusion")

        w = MyForm(self.shmem)

        font = QFontDatabase()
        font.addApplicationFont('./Arial.ttf')
        app.setFont(QFont('Arial'))

        sys.exit(app.exec_())


class myQpush(QPushButton):
    def __init__(self, geo, str, parent=None, connect_fun=None):
        super(myQpush, self).__init__(str, parent)
        self.setGeometry(geo[0], geo[1], geo[2], geo[3])
        if connect_fun is not None:
            self.clicked.connect(connect_fun)


class MyForm(QWidget):
    def __init__(self, shmem):
        super(MyForm, self).__init__()
        # shmem
        self.shmem = shmem
        # ---- UI 호출
        pc_(self, f'[SHMem:{self.shmem}][Controller UI 호출]')
        self.ui = CNS_controller.Ui_Form()
        self.ui.setupUi(self)

        # ----------- ADD !!! -------------- (20210419 for 효진)
        self.setGeometry(0, 0, 269, 620)
        self.auto_data_info_list = AutoDataList(parent=self)
        self.auto_data_info_list.setGeometry(20, 380, 225, 100)
        # ------------------------------------------------------
        self.call_procedure_editor = myQpush([20, 500, 225, 30], 'Show Procedure Editor', self, self.show_procedure_editor)
        self.call_val_change_editor = myQpush([20, 540, 225, 30], 'Change Val Editor', self, self.go_val_change)
        self.call_trend_view = myQpush([20, 580, 225, 30], 'Call Trend View', self, self.go_trend_view)
        # ---- UI 초기 세팅
        self.ui.Cu_SP.setText(str(self.shmem.get_logic('Speed')))
        self.ui.Se_SP.setText(str(self.shmem.get_logic('Speed')))
        # ---- 버튼 명령
        self.ui.Run.clicked.connect(self.run_cns)
        self.ui.Freeze.clicked.connect(self.freeze_cns)
        self.ui.Go_mal.clicked.connect(self.go_mal)
        self.ui.Initial.clicked.connect(self.go_init)
        self.ui.Apply_Sp.clicked.connect(self.go_speed)
        self.ui.Go_db.clicked.connect(self.go_save)

        # self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
        self.show()

        # Call
        self.cns_main_win = Mainwindow(shmem, self)
        self.cns_main_win.show()

    def run_cns(self):
        if self.shmem.get_logic('Initial_condition'):
            pc_(self, 'CNS 시작')
            self.shmem.change_logic_val('Run', True)
        else:
            pc_(self, '먼저 초기 조건을 선언')

    def freeze_cns(self):
        if self.shmem.get_logic('Initial_condition'):
            pc_(self, 'CNS 일시정지')
            self.shmem.change_logic_val('Run', False)
        else:
            pc_(self, '먼저 초기 조건을 선언')

    def go_mal(self):
        if self.ui.Mal_nub.text() != '' and self.ui.Mal_type.text() != '' and self.ui.Mal_time.text() != '':
            # 1. 입력된 내용 List에 저장
            self.ui.Mal_list.addItem('{}_{}_{}'.format(self.ui.Mal_nub.text(),
                                                       self.ui.Mal_type.text(),
                                                       self.ui.Mal_time.text()))
            # 2. 입력된 내용 Trig mem에 저장
            Mal_index = self.ui.Mal_list.count()
            Mal_dict = {'Mal_nub': int(self.ui.Mal_nub.text()),
                        'Mal_opt': int(self.ui.Mal_type.text()),
                        'Mal_time': int(self.ui.Mal_time.text()) * 5,
                        'Mal_done': False}
            self.shmem.change_mal_val(mal_index=Mal_index, mal_dict=Mal_dict)
            # 3. 입력하는 레이블 Clear
            self.ui.Mal_nub.clear()
            self.ui.Mal_type.clear()
            self.ui.Mal_time.clear()
            pc_(self, 'Malfunction 입력 완료')
        else:
            pc_(self, 'Malfunction 입력 실패')

    def go_init(self):
        pc_(self, 'CNS 초기 조건 선언')
        # 1. Mal list clear
        self.ui.Mal_list.clear()
        # 2. Mal trig_mem clear
        self.shmem.call_init(int(self.ui.Initial_list.currentIndex()) + 1)
        # 3. Controller interface update
        self.ui.Cu_SP.setText(str(self.shmem.get_logic('Speed')))
        self.ui.Se_SP.setText(str(self.shmem.get_logic('Speed')))
        # Main window 초기화

    def go_save(self):
        # 실시간 레코딩 중 ...
        self.shmem.change_logic_val('Run_rc', True)
        pc_(self, 'Ester_Egg_Run_ROD CONTROL TRICK')

    def go_speed(self):
        pc_(self, 'CNS 속도 조절')
        self.ui.Cu_SP.setText(self.shmem.get_speed(int(self.ui.Se_SP.text())))

    def go_val_change(self):
        if not self.shmem.get_logic('Run'):
            self.val_editor = ValEditor(self)
            self.val_editor.show()

    def go_trend_view(self):
        self.TrendView = Trend(self, 500, 500, para_name='Flow', para_id='KCNTOMS', para_range=[0, 300],
                               xtitle='Time Since Reactor Shutdown (Hours)', ytitle='Minimum Injection Flowrate (gpm)')
        self.TrendView.show()

    def show_main_window(self):
        # Controller와 동시 실행
        pass

    def show_procedure_editor(self):
        print('TEST!!')
        # self.procedure_editor_wid = PrcedureEditor(self, mem=self.shmem)
        # self.procedure_editor_wid.show()

    def closeEvent(self, QCloseEvent):
        pc_(self, 'Close')
        self.shmem.send_close()
        sys.exit()


# # 자동 데이터 수집하는 구간 # #
class AutoDataList(QListWidget):
    def __init__(self, parent):
        super(AutoDataList, self).__init__(parent=parent)
        self.run_tirg = False

        # Q Timer ------------------------------------------------------------------------------------------------------
        timer = QTimer(self)
        for _ in [self._check_list]:
            timer.timeout.connect(_)
        timer.start(1000)

    def contextMenuEvent(self, event) -> None:
        """ ChartArea 에 기능 올리기  """
        menu = QMenu(self)
        menu.addAction('Add_input').triggered.connect(self._add_input)
        menu_emergency = QMenu('Emergency')
        menu_emergency.addAction("Gen LOCA")
        menu_emergency.addAction("Gen LOCA+SI")

        menu_abnormal = QMenu('Abnormal')
        menu_abnormal.addAction("Gen 2101").triggered.connect(lambda: self._gen_ab(19, random.randint(158, 170), 100))
        menu_abnormal.addAction("Gen 2102").triggered.connect(lambda: self._gen_ab(19, random.randint(140, 150), 100))
        menu_abnormal.addAction("Gen 2001").triggered.connect(lambda: self._gen_ab(20, random.randint(96, 100), 100))
        menu_abnormal.addAction("Gen 2004").triggered.connect(lambda: self._gen_ab(20, random.randint(0, 14), 50))
        menu_abnormal.addAction("Gen 1507").triggered.connect(lambda: self._gen_ab1507)
        menu_abnormal.addAction("Gen 1508").triggered.connect(lambda: self._gen_ab1508)
        menu_abnormal.addAction("Gen 6304").triggered.connect(lambda: self._gen_ab6304)
        menu_abnormal.addAction("Gen 2112").triggered.connect(lambda: self._gen_ab(15, random.randint(1, 100) * 5, 100))
        menu_abnormal.addAction("Gen 1902").triggered.connect(lambda: self._gen_ab(16, random.randint(1, 100) * 5, 100))
        menu_abnormal.addAction("Gen 2111").triggered.connect(lambda: self._gen_ab(22, random.randint(1, 50) * 2, 100))
        menu_abnormal.addAction("Gen 5901").triggered.connect(lambda: self._gen_ab(35, 1, 100))
        menu_abnormal.addAction("Gen 8002").triggered.connect(lambda: self._gen_ab8002)
        menu_abnormal.addAction("Gen 6403").triggered.connect(lambda: self._gen_ab(50, random.randint(1, 3), 30))
        menu_abnormal.addAction("Gen 6002").triggered.connect(lambda: self._gen_ab(36, random.randint(1, 20) * 30, 100))
        menu_abnormal.addAction("Gen 2303").triggered.connect(lambda: self._gen_ab(37, random.randint(1, 50) * 2, 100))
        menu_abnormal.addAction("Gen 5902").triggered.connect(lambda: self._gen_ab(38, random.randint(20, 40) * 5, 100))
        menu_abnormal.addAction("Gen 2301").triggered.connect(lambda: self._gen_ab2301)
        menu_abnormal.addAction("Gen 2306").triggered.connect(lambda: self._gen_ab2306)

        menu.addAction("Run").triggered.connect(self._run_cns)
        menu.addMenu(menu_emergency)
        menu.addMenu(menu_abnormal)
        # -------------------------------------------------------
        menu.exec_(event.globalPos())

    def _add_input(self):
        mal, ok = QInputDialog.getText(self, 'Input Man', 'Mal nub')
        #for i in range(10, 21):
        #    self.addItem(f'12_{mal}{i}_10800')
        self.addItem(f'{mal}')
        # self.addItem(mal)

    def _gen_ab(self, case, opt, nub):
        [self.addItem(f'{case}_{opt}_{random.randint(5, 10) * 60}') for i in range(0, nub)]

    def _gen_ab1507(self):
        self._gen_ab(30, random.randint(1, 25) * 2 + 1000, 30)
        self._gen_ab(30, random.randint(1, 25) * 2 + 2000, 30)
        self._gen_ab(30, random.randint(1, 25) * 2 + 3000, 30)

    def _gen_ab1508(self):
        self._gen_ab(30, random.randint(26, 50) * 2 + 1000, 30)
        self._gen_ab(30, random.randint(26, 50) * 2 + 2000, 30)
        self._gen_ab(30, random.randint(26, 50) * 2 + 3000, 30)

    def _gen_ab6304(self):
        for j in range(1, 5):
            [self.addItem(f'2_{random.randint(11, 44) + 100 * j}_{random.randint(5, 10) * 60}') for i in range(0, 20)]

    def _gen_ab8002(self):
        case = [11, 12, 13, 22, 23, 33]
        [self.addItem(f'67_{case[random.randint(0, 5)]}_{random.randint(5, 10) * 60}') for i in range(0, 50)]

    def _gen_ab2301(self):
        case = [10000, 80000, 140000, 70000, 330000, 200000]
        [self.addItem(f'12_{case[random.randint(0, 5)] + random.randint(1, 3)}_{random.randint(5, 10) * 60}') for i in range(100)]

    def _gen_ab2306(self):
        case = [10000, 20000, 30000]
        [self.addItem(f'13_{case[random.randint(0, 2)] + random.randint(1, 3)}_{random.randint(5, 10) * 60}') for i in range(50)]

    def _check_list(self):
        if self.__len__() > 0 and self.run_tirg:
            local_logic = self.parent().shmem.get_logic_info()
            if local_logic['Run']:
                pass
            else:
                """ Mal function 1개 이상 입력 방법"""
                self.parent().go_init()
                time.sleep(5)

                # 12_10010_30-12_10010_30- ... 형태를 가짐
                split_malcase = self.item(0).text().split('-')
                for i, malcase in enumerate(split_malcase):
                    print(malcase, f'Start [{i}] line mal function')
                    malcase_info = malcase.split('_')
                    self.parent().ui.Mal_nub.setText(malcase_info[0])
                    self.parent().ui.Mal_type.setText(malcase_info[1])
                    self.parent().ui.Mal_time.setText(malcase_info[2])
                    self.parent().go_mal()
                    time.sleep(2)

                # get_first_row = self.item(0).text().split('_')                    # Old version
                # print(get_first_row, 'Start first line mal function')
                # self.parent().go_init()
                # time.sleep(5)
                # self.parent().ui.Mal_nub.setText(get_first_row[0])
                # self.parent().ui.Mal_type.setText(get_first_row[1])
                # self.parent().ui.Mal_time.setText(get_first_row[2])
                # self.parent().go_mal()

                time.sleep(5)
                self.parent().run_cns()
                time.sleep(5)
                self.takeItem(0)
        else:
            self.run_tirg = False

    def _run_cns(self):
        self.run_tirg = True


class PrcedureEditor(QWidget):
    def __init__(self, parent, mem):
        super(PrcedureEditor, self).__init__()
        # self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(500, 100, 1000, 500)

        layer = QVBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)
        # --------------------------------------------------------------------------------------------------------------
        self.cns_para_info = {}
        with open('db.txt', 'r') as f:
            while True:
                temp_ = f.readline().split('\t')
                if temp_[0] == '':  # if empty space -> break
                    break
                if temp_[0] == '#':  # Pass this value. We don't require this value.
                    pass  # These values are normally static values in SMABRES Code.
                else:
                    self.cns_para_info[temp_[0]] = {'Des': temp_[2]}
        # --------------------------------------------------------------------------------------------------------------
        with open('Procedure/procedure.json', 'r', encoding='UTF-8-sig') as f:
            self.procedure_db = json.load(f)

        # 절차서 콤보 박스
        layer_top = QHBoxLayout()
        layer_top.setContentsMargins(0, 0, 0, 0)

        self.procedure_combo = QComboBox(self)
        self.procedure_combo.setMinimumWidth(200)

        for procedure_name in self.procedure_db.keys():
            self.procedure_combo.addItem(procedure_name)

        self.procedure_combo.currentTextChanged.connect(self.change_procedure_name)

        self.procedure_combo_add = QPushButton('Add Prcedure', self)
        self.procedure_combo_add.clicked.connect(self.add_procedure)

        layer_top.addWidget(self.procedure_combo)
        layer_top.addWidget(self.procedure_combo_add)

        # --------------------------------------------------------------------------------------------------------------
        self.procedure_table = QTableWidget(self)
        self.procedure_table.itemChanged.connect(self.change_cell_info)

        col_info = [('단계', 50), ('절차', 400), ('CNS 변수', 100), ('CNS 실제 값', 100), ('CNS 변수 Des', 0)]
        self.procedure_table.setColumnCount(len(col_info))

        col_names = []
        for i, (l, w) in enumerate(col_info):
            self.procedure_table.setColumnWidth(i, w)
            col_names.append(l)

        self.procedure_table.setHorizontalHeaderLabels(col_names)
        self.procedure_table.horizontalHeader().setStretchLastSection(True)
        self.procedure_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        # --------------------------------------------------------------------------------------------------------------
        layer.addLayout(layer_top)
        layer.addWidget(self.procedure_table)

        self.setLayout(layer)

        # CNS info
        self.mem = mem

    def keyPressEvent(self, e) -> None:
        if e.key() == QtCore.Qt.Key_Insert:
            # Row 삽입
            self.add_row()

        if e.key() == QtCore.Qt.Key_Delete:
            # Row 삭제
            self.remove_select_row()

    def contextMenuEvent(self, event) -> None:
        """ Procedure Editor 에 기능 올리기  """
        menu = QMenu(self)
        remove_procedure = menu.addAction("Remove Select Row [Delete]")
        add_procedure = menu.addAction("Add Row [Insert]")
        save_all = menu.addAction("Save DB")

        save_all.triggered.connect(self.save_all_db)
        remove_procedure.triggered.connect(self.remove_select_row)
        add_procedure.triggered.connect(self.add_row)
        menu.exec_(event.globalPos())

    def change_cell_info(self):
        items = self.procedure_table.selectedItems()
        for item in items:
            if item is None:
                pass
            else:
                col = item.column()
                row = item.row()

                step_ = '' if self.procedure_table.item(row, 0) is None else self.procedure_table.item(row, 0).text()
                proc_ = '' if self.procedure_table.item(row, 1) is None else self.procedure_table.item(row, 1).text()
                para_ = '' if self.procedure_table.item(row, 2) is None else self.procedure_table.item(row, 2).text()
                cnsv_ = '' if self.procedure_table.item(row, 3) is None else self.procedure_table.item(row, 3).text()
                desc_ = '' if self.procedure_table.item(row, 4) is None else self.procedure_table.item(row, 4).text()

                if col == 0:
                    step_ = self.procedure_table.item(row, col).text()
                elif col == 1:
                    proc_ = self.procedure_table.item(row, col).text()
                elif col == 2:
                    para_ = self.procedure_table.item(row, col).text()
                    if para_ in self.cns_para_info.keys():

                        self.local_mem = self.mem.get_shmem_db()
                        cnsv_ = self.local_mem[para_]['Val']

                        self.procedure_table.item(row, col + 1).setText(f'{cnsv_}')
                        self.procedure_table.item(row, col + 2).setText(f'{self.cns_para_info[para_]["Des"]}')
                    else:
                        self.procedure_table.item(row, col).setText('ERROR')

            combo_ = self.procedure_combo.currentText()
            self.procedure_db[combo_][f'{item.row()}'] = {'단계': f'{step_}',
                                                          '절차': f'{proc_}',
                                                          'CNS변수': f'{para_}'}

    def change_procedure_name(self):
        get_procedure_name = self.procedure_combo.currentText()

        for _ in range(0, self.procedure_table.rowCount()):
            self.procedure_table.removeRow(0)

        # reload db

        for row, str_row in enumerate(self.procedure_db[get_procedure_name]):

            info = self.procedure_db[get_procedure_name][str_row]
            step_ = QTableWidgetItem(info['단계'])
            proc_ = QTableWidgetItem(info['절차'])
            para_ = QTableWidgetItem(info['CNS변수'])
            cnsv_ = QTableWidgetItem('0')

            cns_para = info['CNS변수']
            if cns_para in self.cns_para_info.keys():
                des__ = QTableWidgetItem(self.cns_para_info[cns_para]['Des'])
            else:
                des__ = QTableWidgetItem('')
                para_ = QTableWidgetItem('ERROR')

            self.procedure_table.insertRow(row)

            self.procedure_table.setItem(row, 0, step_)
            self.procedure_table.setItem(row, 1, proc_)
            self.procedure_table.setItem(row, 2, para_)
            self.procedure_table.setItem(row, 3, cnsv_)
            self.procedure_table.setItem(row, 4, des__)

    def remove_select_row(self):
        """ 선택된 열 지우기 """
        indexes = self.procedure_table.selectionModel().selectedIndexes()

        for index in sorted(indexes):
            self.procedure_table.removeRow(index.row())
            get_index_row = index.row()

        get_procedure_name = self.procedure_combo.currentText()

        del self.procedure_db[get_procedure_name][f'{get_index_row}']
        print(self.procedure_db[get_procedure_name], get_index_row)

        new_info = {}
        for i, _ in enumerate(self.procedure_db[get_procedure_name].keys()):
            new_info[f'{i}'] = self.procedure_db[get_procedure_name][_]

        self.procedure_db[get_procedure_name] = new_info

    def add_row(self):
        self.procedure_table.insertRow(self.procedure_table.rowCount())

        self.procedure_table.setItem(self.procedure_table.rowCount() - 1, 0, QTableWidgetItem('-'))
        self.procedure_table.setItem(self.procedure_table.rowCount() - 1, 1, QTableWidgetItem('-'))
        self.procedure_table.setItem(self.procedure_table.rowCount() - 1, 2, QTableWidgetItem('-'))
        self.procedure_table.setItem(self.procedure_table.rowCount() - 1, 3, QTableWidgetItem('-'))
        self.procedure_table.setItem(self.procedure_table.rowCount() - 1, 4, QTableWidgetItem('-'))

    def save_all_db(self):
        print('Save')
        with open('Procedure/procedure.json', 'w', encoding='UTF-8-sig') as file:
            file.write(json.dumps(self.procedure_db, ensure_ascii=False, indent="\t"))

    def add_procedure(self):
        text, ok = QInputDialog.getText(self, '신규 절차서 추가', '신규절차서 명을 입력하세요.:')

        if ok:
            self.procedure_db[text] = {}
            self.procedure_combo.addItem(str(text))


class ValEditor(QWidget):
    def __init__(self, parent):
        super(ValEditor, self).__init__()
        self.shmem = parent.shmem
        self.setGeometry(0, 0, 300, 50)

        h_layer = QHBoxLayout()
        v_layer = QVBoxLayout()

        name_h_layer = QHBoxLayout()
        self.name_label = QLabel('Name')
        self.name_label.setFixedWidth(50)
        self.name_text = QLineEdit('')
        name_h_layer.addWidget(self.name_label)
        name_h_layer.addWidget(self.name_text)

        val_h_layer = QHBoxLayout()
        self.val_label = QLabel('Val')
        self.val_label.setFixedWidth(50)
        self.val_text = QLineEdit('')
        val_h_layer.addWidget(self.val_label)
        val_h_layer.addWidget(self.val_text)

        v_layer.addLayout(name_h_layer)
        v_layer.addLayout(val_h_layer)

        self.change_btn = QPushButton('Change')
        self.change_btn.clicked.connect(self.change_val)

        h_layer.addLayout(v_layer)
        h_layer.addWidget(self.change_btn)

        self.setLayout(h_layer)

    def change_val(self):
        if self.shmem.check_para(str(self.name_text.text())):
            orgin = self.shmem.get_shmem_val(self.name_text.text())
            try:
                get_val = int(float(self.val_text.text())) if type(orgin) is int else float(self.val_text.text())
                self.shmem.change_shmem_val(self.name_text.text(), get_val)

                self.close()
            except:
                print('잘못된 파라메터 값 입력')
                self.val_text.clear()
        else:
            print('잘못된 파라메터 이름 입력')
            self.name_text.clear()