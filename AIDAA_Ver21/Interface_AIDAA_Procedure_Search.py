from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Function_Simulator_CNS import *

# ----------------------------------------------------------------------------------------------------------------------

class ProcedureSearch(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSearch, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        self.setGeometry(200, 200, 390, 300)
        lay = QVBoxLayout(self)
        lay.addWidget(ProcedureSearchTitleBar(self))
        lay.addWidget(ProcedureSearchWindow(self))
        lay.addWidget(ProcedureSearchTable(self))
        lay.addWidget(ProcedureSearchBottom(self))

# --------------------------------------------------------------------------------

class ProcedureSearchTitleBar(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSearchTitleBar, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureSearchTitleName(self))
        lay.addWidget(ProcedureSearchClose(self))

class ProcedureSearchTitleName(ABCLabel, QLabel):
    def __init__(self, parent):
        super(ProcedureSearchTitleName, self).__init__(parent)
        self.setText('Procedure Directory')

class ProcedureSearchClose(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSearchClose, self).__init__(parent)
        self.setText('X')
        self.clicked.connect(self.close_ProcedureSearch)

    def close_ProcedureSearch(self):
        self.inmem.current_search['active_window'] = 0
        ProcedureSearch(self).close()

# --------------------------------------------------------------------------------

class ProcedureSearchWindow(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSearchWindow, self).__init__(parent)
        lay = QVBoxLayout(self)
        lay.addWidget(ProcedureSearch1(self))
        lay.addWidget(ProcedureSearch2(self))

        gb = QGroupBox('절차서 검색')
        gb.setLayout(lay)

        search_lay = QHBoxLayout(self)
        search_lay.addWidget(gb)

class ProcedureSearch1(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSearch1, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureSearchLabel1(self))
        lay.addWidget(ProcedureSearchInput1(self))
        lay.addWidget(ProcedureSearchBTN(self))

class ProcedureSearchLabel1(ABCLabel, QLabel):
    def __init__(self, parent):
        super(ProcedureSearchLabel1, self).__init__(parent)
        self.setText('절차서 번호')

class ProcedureSearchInput1(ABCText, QTextEdit):
    def __init__(self, parent):
        super(ProcedureSearchInput1, self).__init__(parent)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.current_search['reset_number'] == 0:
            self.clear()
            self.inmem.current_search['reset_number'] = -1

        if self.inmem.current_search['Procedure']['name'] != '':
            self.setReadOnly(True)
        else:
            self.setReadOnly(False)

        self.inmem.current_search['Procedure']['number'] = self.toPlainText()


class ProcedureSearchBTN(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSearchBTN, self).__init__(parent)
        self.setText('검색')
        self.clicked.connect(self.search)
        self.procedure_search_input = ''
        self.search_area = ''

    def search(self) -> str:
        self.inmem.current_search['reset_number'] = 1
        self.inmem.current_search['reset_name'] = 1
        if self.inmem.current_search['Procedure']['number'] != '':
            self.procedure_search_input = self.inmem.current_search['Procedure']['number']
            self.search_area = 0 # 0: 절차서 번호, 1: 절차서 이름
        elif self.inmem.current_search['Procedure']['name'] != '':
            self.procedure_search_input = self.inmem.current_search['Procedure']['name']
            self.search_area = 1  # 0: 절차서 번호, 1: 절차서 이름
        return self.procedure_search_input, self.search_area

class ProcedureSearch2(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSearch2, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureSearchLabel2(self))
        lay.addWidget(ProcedureSearchInput2(self))
        lay.addWidget(ProcedureSearchReset(self))

class ProcedureSearchLabel2(ABCLabel, QLabel):
    def __init__(self, parent):
        super(ProcedureSearchLabel2, self).__init__(parent)
        self.setText('절차서 명')

class ProcedureSearchInput2(ABCText, QTextEdit):
    def __init__(self, parent):
        super(ProcedureSearchInput2, self).__init__(parent)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        if self.inmem.current_search['reset_name'] == 0:
            self.clear()
            self.inmem.current_search['reset_name'] = -1

        if self.inmem.current_search['Procedure']['number'] != '':
            self.setReadOnly(True)
        else:
            self.setReadOnly(False)

        self.inmem.current_search['Procedure']['name'] = self.toPlainText()


class ProcedureSearchReset(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSearchReset, self).__init__(parent)
        self.setText('초기화')
        self.clicked.connect(self.search_reset)

    def search_reset(self):
        self.inmem.current_search['reset_number'] = 0
        self.inmem.current_search['reset_name'] = 0
        self.inmem.current_search['Procedure']['number'] = ''
        self.inmem.current_search['Procedure']['name'] = ''


# --------------------------------------------------------------------------------

class ProcedureSearchTable(ABCTableWidget, QTableWidget):
    def __init__(self, parent):
        super(ProcedureSearchTable, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.column_labels = ['절차서 번호', '절차서 명']
        self.setColumnCount(len(self.column_labels))
        self.setHorizontalHeaderLabels([l for l in self.column_labels])
        self.setRowCount(len(self.inmem.search_dict['Procedure']))
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSortingEnabled(True)
        self.setStyleSheet("""QTableWidget{background: #e9e9e9;selection-color: white;border: 1px solid lightgrey;
                                    selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);
                                    color: #202020;
                                    outline: 0;}
                                    QTableWidget::item::hover{
                                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);}
                                    QTableWidget::item::focus
                                    {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);border: 0px;}""")
        self.doubleClicked.connect(self.dis_procedure)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        '''
        절차서 접속 부분 이중화 -> 1) 진단 부분, 2) 절차서 검색 부분
        문제점: 진단 부분에서 클릭 시, 클릭된 절차서 정보 업데이트로 인해 절차서 검색 부분과 충돌
        -> 절차서 접속 부분을 단일화로 구성: 팝업창 활성화 시 팝업창으로만 절차서 부분 제어 가능하도록 개선
        '''
        search_result = []
        if self.inmem.current_search['reset_number'] == 1 and self.inmem.current_search['reset_name'] == 1:
            procedure_search_input, search_area = self.inmem.widget_ids['ProcedureSearchBTN'].search()
            if search_area == 0: # 0: 절차서 번호, 1: 절차서 이름
                for i in self.inmem.search_dict['Procedure']:
                    if procedure_search_input in i[0]:
                        search_result.append(i)
                self.setRowCount(len(search_result))
                [self.setItem(i, 0, QTableWidgetItem(search_result[i][0])) for i in range(len(search_result))]
                [self.setItem(i, 1, QTableWidgetItem(search_result[i][1])) for i in range(len(search_result))]
            elif search_area == 1: # 0: 절차서 번호, 1: 절차서 이름
                for i in self.inmem.search_dict['Procedure']:
                    if procedure_search_input in i[1]:
                        search_result.append(i)
                self.setRowCount(len(search_result))
                [self.setItem(i, 0, QTableWidgetItem(search_result[i][0])) for i in range(len(search_result))]
                [self.setItem(i, 1, QTableWidgetItem(search_result[i][1])) for i in range(len(search_result))]
        else:
            self.setRowCount(len(self.inmem.search_dict['Procedure']))
            [self.setItem(i, 0, QTableWidgetItem(self.inmem.search_dict['Procedure'][i][0])) for i in range(len(self.inmem.search_dict['Procedure']))]
            [self.setItem(i, 1, QTableWidgetItem(self.inmem.search_dict['Procedure'][i][1])) for i in range(len(self.inmem.search_dict['Procedure']))]

        if self.currentRow() != -1:
            self.inmem.current_table['Procedure'] = self.currentRow()

    def dis_procedure(self):
        get_procedure_number = self.item(self.inmem.current_table['Procedure'], 0).text()
        get_procedure_name = self.item(self.inmem.current_table['Procedure'], 1).text()
        get_procedure_info = 'Ab'+get_procedure_number+': '+get_procedure_name
        self.inmem.change_current_system_name('Procedure')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()
        self.inmem.widget_ids['Procedure'].set_procedure_name(get_procedure_info)
        self.parent().close()  # 더블클릭 시 팝업 종료

# --------------------------------------------------------------------------------

class ProcedureSearchBottom(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSearchBottom, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureSearchOpen(self))
        lay.addWidget(ProcedureSearchCancel(self))

class ProcedureSearchOpen(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSearchOpen, self).__init__(parent)
        self.setText('열기')
        self.clicked.connect(self.dis_procedure)

    def dis_procedure(self):
        self.inmem.change_current_system_name('Procedure')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()
        ProcedureSearch(self).close() # 절차서 전환 후 종료

class ProcedureSearchCancel(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSearchCancel, self).__init__(parent)
        self.setText('취소')
        self.clicked.connect(self.close_ProcedureSearch)

    def close_ProcedureSearch(self):
        self.inmem.current_search['active_window'] = 0
        ProcedureSearch(self).close()

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class SystemSearch(ABCWidget, QWidget):
    def __init__(self, parent):
        super(SystemSearch, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        self.setGeometry(200, 200, 390, 300)
        lay = QVBoxLayout(self)
        lay.addWidget(SystemSearchTitleBar(self))
        lay.addWidget(SystemSearchWindow(self))
        lay.addWidget(SystemSearchTable(self))
        lay.addWidget(SystemSearchBottom(self))

# --------------------------------------------------------------------------------

class SystemSearchTitleBar(ABCWidget, QWidget):
    def __init__(self, parent):
        super(SystemSearchTitleBar, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(SystemSearchTitleName(self))
        lay.addWidget(SystemSearchClose(self))

class SystemSearchTitleName(ABCLabel, QLabel):
    def __init__(self, parent):
        super(SystemSearchTitleName, self).__init__(parent)
        self.setText('System Directory')

class SystemSearchClose(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchClose, self).__init__(parent)
        self.setText('X')
        self.clicked.connect(self.close_SystemSearch)

    def close_SystemSearch(self):
        SystemSearch(self).close()

# --------------------------------------------------------------------------------

class SystemSearchWindow(ABCWidget, QWidget):
    def __init__(self, parent):
        super(SystemSearchWindow, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(SystemSearchLabel(self))
        lay.addWidget(SystemSearchInput(self))
        lay.addWidget(SystemSearchBTN(self))
        lay.addWidget(SystemSearchReset(self))

        gb = QGroupBox('System 검색')
        gb.setLayout(lay)

        search_lay = QHBoxLayout(self)
        search_lay.addWidget(gb)

class SystemSearchLabel(ABCLabel, QLabel):
    def __init__(self, parent):
        super(SystemSearchLabel, self).__init__(parent)
        self.setText('System 명')

class SystemSearchInput(ABCText, QTextEdit):
    def __init__(self, parent):
        super(SystemSearchInput, self).__init__(parent)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        self.inmem.current_search['System'] = self.toPlainText()
        if self.inmem.current_search['system_reset'] == 0:
            self.clear()
            self.inmem.current_search['system_reset'] = -1

class SystemSearchBTN(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchBTN, self).__init__(parent)
        self.setText('검색')
        self.clicked.connect(self.search)
        self.system_search_input = ''

    def search(self) -> str:
        self.inmem.current_search['system_reset'] = 1
        search_keyword = self.inmem.current_search['System']
        self.system_search_input = search_keyword
        return self.system_search_input

class SystemSearchReset(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchReset, self).__init__(parent)
        self.setText('초기화')
        self.clicked.connect(self.search_reset)

    def search_reset(self):
        self.inmem.current_search['system'] = ''
        self.inmem.current_search['system_reset'] = 0

# --------------------------------------------------------------------------------

class SystemSearchTable(ABCTableWidget, QTableWidget):
    def __init__(self, parent):
        super(SystemSearchTable, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.column_labels = ['System 명']
        self.setColumnCount(len(self.column_labels))
        self.setHorizontalHeaderLabels([l for l in self.column_labels])
        self.setRowCount(len(self.inmem.search_dict['System']))
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSortingEnabled(True)
        self.setStyleSheet("""QTableWidget{background: #e9e9e9;selection-color: white;border: 1px solid lightgrey;
                                    selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);
                                    color: #202020;
                                    outline: 0;}
                                    QTableWidget::item::hover{
                                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);}
                                    QTableWidget::item::focus
                                    {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);border: 0px;}""")
        self.doubleClicked.connect(self.dis_system)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        search_result = []
        if self.inmem.current_search['system_reset'] == 1:
            for i in self.inmem.search_dict['System']:
                if self.inmem.widget_ids['SystemSearchBTN'].search() in i:
                    search_result.append(i)
            self.setRowCount(len(search_result))
            [self.setItem(j, 0, QTableWidgetItem(search_result[j])) for j in range(len(search_result))]
        else:
            self.setRowCount(len(self.inmem.search_dict['System']))
            [self.setItem(i, 0, QTableWidgetItem(self.inmem.search_dict['System'][i])) for i in range(len(self.inmem.search_dict['System']))]

    def dis_system(self): # 미믹 창 활성화 이후 닫기 기능 추가해야 함.
        self.inmem.change_current_system_name('Action')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()
        self.parent().close()  # 더블클릭 시 팝업 종료

# --------------------------------------------------------------------------------

class SystemSearchBottom(ABCWidget, QWidget):
    def __init__(self, parent):
        super(SystemSearchBottom, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(SystemSearchOpen(self))
        lay.addWidget(SystemSearchCancle(self))

class SystemSearchOpen(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchOpen, self).__init__(parent)
        self.setText('열기')
        self.clicked.connect(self.dis_system)

    def dis_system(self): # CVCS만 구현되어 있기에, 무엇을 눌러도 CVCS 미믹창으로 전환됨.
        self.inmem.change_current_system_name('Action')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()
        SystemSearch(self).close()

class SystemSearchCancle(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchCancle, self).__init__(parent)
        self.setText('취소')
        self.clicked.connect(self.close_SystemSearch)

    def close_SystemSearch(self):
        SystemSearch(self).close()

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class XAISearch(ABCWidget, QWidget):
    def __init__(self, parent):
        super(XAISearch, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        self.setGeometry(200, 200, 390, 300)
        lay = QVBoxLayout(self)
        lay.addWidget(XAISearchTitleBar(self))
        lay.addWidget(XAISearchWindow(self))
        lay.addWidget(XAISearchTable(self))
        lay.addWidget(XAISearchBottom(self))

# --------------------------------------------------------------------------------

class XAISearchTitleBar(ABCWidget, QWidget):
    def __init__(self, parent):
        super(XAISearchTitleBar, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(XAISearchTitleName(self))
        lay.addWidget(XAISearchClose(self))

class XAISearchTitleName(ABCLabel, QLabel):
    def __init__(self, parent):
        super(XAISearchTitleName, self).__init__(parent)
        self.setText('AI 기여도')

class XAISearchClose(ABCPushButton):
    def __init__(self, parent):
        super(XAISearchClose, self).__init__(parent)
        self.setText('X')
        self.clicked.connect(self.close_XAISearch)

    def close_XAISearch(self):
        XAISearch(self).close()

# --------------------------------------------------------------------------------

class XAISearchWindow(ABCWidget, QWidget):
    def __init__(self, parent):
        super(XAISearchWindow, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(XAISearchProcedureNumber(self))
        lay.addWidget(XAISearchProcedureName(self))

        gb = QGroupBox(self)
        gb.setLayout(lay)

        search_lay = QHBoxLayout(self)
        search_lay.addWidget(gb)

class XAISearchProcedureNumber(ABCLabel, QLabel):
    def __init__(self, parent):
        super(XAISearchProcedureNumber, self).__init__(parent)
        self.setText(f'{self.inmem.dis_AI["AI"][self.inmem.current_table["Procedure"]][0][2:7]}')

class XAISearchProcedureName(ABCLabel, QLabel):
    def __init__(self, parent):
        super(XAISearchProcedureName, self).__init__(parent)
        self.setText(f'{self.inmem.dis_AI["AI"][self.inmem.current_table["Procedure"]][0][9:]}')

# --------------------------------------------------------------------------------

class XAISearchTable(ABCTableWidget, QTableWidget):
    def __init__(self, parent):
        super(XAISearchTable, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(238, 238, 238);')
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.column_labels = ['변수 명', '기여도']
        self.setColumnCount(len(self.column_labels))
        self.setHorizontalHeaderLabels([l for l in self.column_labels])
        self.setRowCount(5)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setStyleSheet("""QTableWidget{background: #e9e9e9;selection-color: white;border: 1px solid lightgrey;
                                    selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);
                                    color: #202020;
                                    outline: 0;}
                                    QTableWidget::item::hover{
                                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);}
                                    QTableWidget::item::focus
                                    {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);border: 0px;}""")
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        try:
            if self.item(0, 0).text() == self.inmem.dis_AI['XAI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['XAI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['XAI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['XAI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['XAI'][4][0]:
                pass
            else:
                [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['XAI'][i][0])) for i in range(5)]
                [self.setItem(i, 1, QTableWidgetItem(self.inmem.dis_AI['XAI'][i][1])) for i in range(5)]
        except:
            [self.setItem(i, 0, QTableWidgetItem(self.inmem.dis_AI['XAI'][i][0])) for i in range(5)]
            [self.setItem(i, 1, QTableWidgetItem(self.inmem.dis_AI['XAI'][i][1])) for i in range(5)]

# --------------------------------------------------------------------------------

class XAISearchBottom(ABCWidget, QWidget):
    def __init__(self, parent):
        super(XAISearchBottom, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(XAISearchCancle(self))

class XAISearchCancle(ABCPushButton):
    def __init__(self, parent):
        super(XAISearchCancle, self).__init__(parent)
        self.setText('닫기')
        self.clicked.connect(self.close_XAISearch)

    def close_XAISearch(self):
        XAISearch(self).close()