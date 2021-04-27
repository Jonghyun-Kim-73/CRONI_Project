#
import sys
import multiprocessing
from copy import deepcopy
import time
import json

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
#
from AIDA_Interface_brief_ver import CNS_Platform_controller_interface as CNS_controller
from AIDA_Interface_brief_ver import main_window


class InterfaceFun(multiprocessing.Process):
    def __init__(self, shmem):
        multiprocessing.Process.__init__(self)
        self.shmem = shmem

    def run(self):
        app = QApplication(sys.argv)
        w = MyForm(self.shmem)
        sys.exit(app.exec_())


class MyForm(QWidget):
    def __init__(self, shmem):
        super(MyForm, self).__init__()
        # shmem
        self.shmem = shmem
        # ---- UI 호출
        self.pr_(f'[SHMem:{self.shmem}][Controller UI 호출]')
        self.ui = CNS_controller.Ui_Form()
        self.ui.setupUi(self)

        # ----------- ADD !!! -------------- (20210419 for 효진)
        self.setGeometry(0, 0, 269, 550)
        self.auto_data_info_list = AutoDataList(parent=self)
        self.auto_data_info_list.setGeometry(20, 380, 225, 100)

        # ----------- ADD 절차서 정보 입력 용 ---------------------
        self.call_procedure_editor = QPushButton('Show Procedure Editor', self)
        self.call_procedure_editor.setGeometry(20, 500, 225, 30)
        self.call_procedure_editor.clicked.connect(self.show_procedure_editor)

        # ---- UI 초기 세팅
        self.ui.Cu_SP.setText(str(self.shmem.get_logic('Speed')))
        self.ui.Se_SP.setText(str(self.shmem.get_logic('Speed')))
        # ---- 초기함수 호출
        # ---- 버튼 명령
        self.ui.Run.clicked.connect(self.run_cns)
        self.ui.Freeze.clicked.connect(self.freeze_cns)
        self.ui.Go_mal.clicked.connect(self.go_mal)
        self.ui.Initial.clicked.connect(self.go_init)
        self.ui.Apply_Sp.clicked.connect(self.go_speed)
        self.ui.Go_db.clicked.connect(self.go_save)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
        self.show()

        # Call
        self.cns_main_win = main_window.Mainwindow(parnet=self, mem=self.shmem)
        self.cns_main_win.show()

    def pr_(self, s):
        head_ = 'Main_UI'
        return print(f'[{head_:10}][{s}]')

    def run_cns(self):
        if self.shmem.get_logic('Initial_condition'):
            self.pr_('CNS 시작')
            self.shmem.change_logic_val('Run', True)
        else:
            self.pr_('먼저 초기 조건을 선언')

    def freeze_cns(self):
        if self.shmem.get_logic('Initial_condition'):
            self.pr_('CNS 일시정지')
            self.shmem.change_logic_val('Run', False)
        else:
            self.pr_('먼저 초기 조건을 선언')

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
            self.pr_('Malfunction 입력 완료')
        else:
            self.pr_('Malfunction 입력 실패')

    def go_init(self):
        self.pr_('CNS 초기 조건 선언')
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
        self.pr_('Ester_Egg_Run_ROD CONTROL TRICK')

    def go_speed(self):
        self.pr_('CNS 속도 조절')
        self.ui.Cu_SP.setText(self.shmem.get_speed(int(self.ui.Se_SP.text())))

    def show_main_window(self):
        # Controller와 동시 실행
        pass

    def show_procedure_editor(self):
        self.procedure_editor_wid = PrcedureEditor(self, mem=self.shmem)
        self.procedure_editor_wid.show()


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
        add_input1 = menu.addAction("Add input")
        add_input2 = menu.addAction("Run")

        add_input1.triggered.connect(self._add_input)
        add_input2.triggered.connect(self._run_cns)

        menu.exec_(event.globalPos())

    def _add_input(self):
        mal, ok = QInputDialog.getText(self, 'Input Man', 'Mal nub')

        #for i in range(10, 21):
        #    self.addItem(f'12_{mal}{i}_10800')
        self.addItem(f'{mal}')

        # self.addItem(mal)

    def _check_list(self):
        if self.__len__() > 0 and self.run_tirg:
            local_logic = self.parent().shmem.get_logic_info()
            if local_logic['Run']:
                pass
            else:
                get_first_row = self.item(0).text().split('_')
                print(get_first_row, 'Start first line mal function')
                self.parent().go_init()
                time.sleep(5)
                self.parent().ui.Mal_nub.setText(get_first_row[0])
                self.parent().ui.Mal_type.setText(get_first_row[1])
                self.parent().ui.Mal_time.setText(get_first_row[2])
                self.parent().go_mal()
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
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
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
