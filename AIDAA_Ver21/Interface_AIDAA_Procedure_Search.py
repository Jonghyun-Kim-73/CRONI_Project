import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Function_Simulator_CNS import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# ----------------------------------------------------------------------------------------------------------------------

class ProcedureSearch(ABCWidget):
    def __init__(self, parent):
        super(ProcedureSearch, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 상단바 제거
        self.setStyleSheet(qss.Search_Popup)
        self.setObjectName("Search")
        self.setGeometry(454, 215, 1190, 840)
        lay = QVBoxLayout(self)
        lay_content = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.TitleBar = ProcedureSearchTitleBar(self)
        lay.addWidget(self.TitleBar)
        lay_content.addWidget(ProcedureSearchWindow(self))
        lay_content.addWidget(ProcedureSearchScrollArea(self))
        lay_content.addWidget(ProcedureSearchBottom(self))
        lay_content.setContentsMargins(10, 0, 10, 0)

        lay.addLayout(lay_content)

    # window drag
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton) and self.TitleBar.underMouse():
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag and self.TitleBar.underMouse():
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 윈도우 position 변경
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
# --------------------------------------------------------------------------------

class ProcedureSearchTitleBar(ABCWidget):
    def __init__(self, parent):
        super(ProcedureSearchTitleBar, self).__init__(parent)
        self.setFixedHeight(50)
        self.setObjectName("SearchTitleBar")
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureSearchTitleName(self))
        lay.addWidget(ProcedureSearchClose(self))

class ProcedureSearchTitleName(ABCLabel):
    def __init__(self, parent):
        super(ProcedureSearchTitleName, self).__init__(parent)
        self.setObjectName("SearchTitleBar")
        self.setText('Procedure Directory')

class ProcedureSearchClose(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSearchClose, self).__init__(parent)
        icon = os.path.join(ROOT_PATH, '../AIDAA_Ver21/Img/close.png')
        self.setObjectName("SearchTitleBar")
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(33, 33))  # 아이콘 크기
        self.setFixedSize(QSize(33, 33))
        self.setContentsMargins(1, 0, 0, 0)
        self.clicked.connect(self.close_ProcedureSearch)

    def close_ProcedureSearch(self):
        ProcedureSearch(self).close()

# --------------------------------------------------------------------------------

class ProcedureSearchWindow(ABCWidget):
    def __init__(self, parent):
        super(ProcedureSearchWindow, self).__init__(parent)
        lay = QVBoxLayout(self)
        lay.addWidget(ProcedureSearch1(self))
        lay.addWidget(ProcedureSearch2(self))
        lay.setContentsMargins(0, 10, 200, 10)
        lay.setSpacing(5)
        gb = QGroupBox('절차서 검색')
        gb.setObjectName("SearchWindow")
        gb.setContentsMargins(0, 0, 0, 0)
        gb.setFixedHeight(126)
        gb.setLayout(lay)

        search_lay = QHBoxLayout(self)
        search_lay.setContentsMargins(0, 0, 0, 0)
        search_lay.addWidget(gb)

class ProcedureSearch1(ABCWidget):
    def __init__(self, parent):
        super(ProcedureSearch1, self).__init__(parent)
        self.setFixedHeight(30)
        lay = QHBoxLayout(self)
        lay.addStretch(1)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(ProcedureSearchLabel1(self))
        lay.addWidget(ProcedureSearchInput1(self))
        lay.addWidget(ProcedureSearchBTN(self))
        lay.setSpacing(20)

class ProcedureSearchLabel1(ABCLabel):
    def __init__(self, parent):
        super(ProcedureSearchLabel1, self).__init__(parent)
        self.setFixedHeight(30)
        self.setObjectName("SearchLabel")
        self.setText('절차서 번호')

class ProcedureSearchInput1(ABCText):
    def __init__(self, parent):
        super(ProcedureSearchInput1, self).__init__(parent)
        self.setFixedSize(456, 30)
        self.setObjectName("SearchInput")
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
        self.setFixedSize(160, 30)
        self.setObjectName("SearchBTN")
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

class ProcedureSearch2(ABCWidget):
    def __init__(self, parent):
        super(ProcedureSearch2, self).__init__(parent)
        self.setFixedHeight(30)
        lay = QHBoxLayout(self)
        lay.addStretch(1)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(ProcedureSearchLabel2(self))
        lay.addWidget(ProcedureSearchInput2(self))
        lay.addWidget(ProcedureSearchReset(self))
        lay.setSpacing(20)

class ProcedureSearchLabel2(ABCLabel):
    def __init__(self, parent):
        super(ProcedureSearchLabel2, self).__init__(parent)
        self.setFixedHeight(30)
        self.setObjectName("SearchLabel")
        self.setText('절차서 명')

class ProcedureSearchInput2(ABCText):
    def __init__(self, parent):
        super(ProcedureSearchInput2, self).__init__(parent)
        self.setFixedSize(456, 30)
        self.setObjectName("SearchInput")
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
        self.setObjectName("SearchBTN")
        self.setFixedSize(160, 30)
        self.setText('리셋')
        self.clicked.connect(self.search_reset)

    def search_reset(self):
        self.inmem.current_search['reset_number'] = 0
        self.inmem.current_search['reset_name'] = 0
        self.inmem.current_search['Procedure']['number'] = ''
        self.inmem.current_search['Procedure']['name'] = ''

# --------------------------------------------------------------------------------
class ProcedureSearchScrollArea(ABCScrollArea):
    def __init__(self, parent):
        super(ProcedureSearchScrollArea, self).__init__(parent)
        self.margins = QMargins(0, 40, 0, 0)  # header height
        self.setViewportMargins(self.margins)
        # self.setFixedWidth(1170)
        self.setFixedSize(1170, 600)  # 초기 테이블 크기

        self.headings_widget = QWidget(self)
        self.headings_layout = QHBoxLayout()
        self.headings_widget.setLayout(self.headings_layout)
        self.headings_layout.setContentsMargins(0, 0, 10, 0)

        # header item
        self.heading_label = [0, 0]
        self.heading_label[0] = QLabel(" 절차서 번호")
        self.heading_label[1] = QLabel(" 절차서명")

        # size
        self.heading_label[0].setFixedWidth(200)
        self.heading_label[1].setFixedWidth(940)

        for label in range(2):
            self.headings_layout.addWidget(self.heading_label[label])
            self.heading_label[label].setObjectName("Alarm_Header_M")
            self.heading_label[label].setAlignment(Qt.AlignLeft and Qt.AlignVCenter)

        self.heading_label[0].setContentsMargins(5, 0, 0, 0)
        self.heading_label[0].setObjectName("Alarm_Header_F")
        self.heading_label[1].setObjectName("Alarm_Header_L")
        # self.headings_layout.addStretch(1)
        self.headings_layout.setSpacing(0)


        self.scrollwidget = QWidget()
        # self.scrollwidget.setObjectName("scroll")
        self.grid = QGridLayout(self.scrollwidget)
        self.grid.addWidget(ProcedureSearchTable(self))
        self.grid.setContentsMargins(0, 0, 10, 0)
        self.setWidget(self.scrollwidget)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, event):
        rect = self.viewport().geometry()
        self.headings_widget.setGeometry(0, 0, rect.width() - 1, self.margins.top())
        QScrollArea.resizeEvent(self, event)

class ProcedureSearchTable(ABCTableWidget):
    def __init__(self, parent):
        super(ProcedureSearchTable, self).__init__(parent)
        self.setFixedSize(1140, 640) # 초기 테이블 크기
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setShowGrid(False)  # Grid 지우기
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.horizontalHeader().setVisible(False)  # Col header 숨기기
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.column_labels = [(' 절차서 번호', 200), (' 절차서 명', 940)]
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(len(self.inmem.search_dict['Procedure']))
        self.col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            self.col_names.append(l)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setHorizontalHeaderLabels(self.col_names)
        self.setSortingEnabled(True)  # 테이블 sorting

        # header = self.horizontalHeader()
        # header.setSortIndicatorShown(True)
        # header.sortIndicatorChanged.connect(self.sortItems)
        self.horizontalHeader().setFixedHeight(40)
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeaderItem(1).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 65)

        self.selected_procedure_name =''

        self.doubleClicked.connect(self.dis_procedure)
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        search_result = []
        if self.inmem.current_search['reset_number'] == 1 and self.inmem.current_search['reset_name'] == 1:
            procedure_search_input, search_area = self.inmem.widget_ids['ProcedureSearchBTN'].search()
            if search_area == 0: # 0: 절차서 번호, 1: 절차서 이름
                for i in self.inmem.search_dict['Procedure']:
                    if procedure_search_input in i[0]:
                        search_result.append(i)
                self.setRowCount(len(search_result))
                [self.setItem(i, 0, QTableWidgetItem(" " + search_result[i][0])) for i in range(len(search_result))]
                [self.setItem(i, 1, QTableWidgetItem(search_result[i][1])) for i in range(len(search_result))]
            elif search_area == 1: # 0: 절차서 번호, 1: 절차서 이름
                for i in self.inmem.search_dict['Procedure']:
                    if procedure_search_input in i[1]:
                        search_result.append(i)
                self.setRowCount(len(search_result))
                [self.setItem(i, 0, QTableWidgetItem(" " + search_result[i][0])) for i in range(len(search_result))]
                [self.setItem(i, 1, QTableWidgetItem(search_result[i][1])) for i in range(len(search_result))]
        else:
            self.setRowCount(len(self.inmem.search_dict['Procedure']))
            [self.setItem(i, 0, QTableWidgetItem(" " + self.inmem.search_dict['Procedure'][i][0])) for i in range(len(self.inmem.search_dict['Procedure']))]
            [self.setItem(i, 1, QTableWidgetItem(self.inmem.search_dict['Procedure'][i][1])) for i in range(len(self.inmem.search_dict['Procedure']))]

        if self.currentRow() != -1:
            self.inmem.current_table['Procedure'] = self.currentRow()
            get_procedure_number = self.item(self.inmem.current_table['Procedure'], 0).text()
            get_procedure_name = self.item(self.inmem.current_table['Procedure'], 1).text()
            get_procedure_info = 'Ab'+get_procedure_number+': '+get_procedure_name
            self.inmem.current_table['procedure_name'] = get_procedure_info

    def dis_procedure(self):
        # 주석 부분은 Procedure 부분 업데이트 완료 후 활성화할 예정
        get_procedure_number = self.item(self.inmem.current_table['Procedure'], 0).text()
        get_procedure_name = self.item(self.inmem.current_table['Procedure'], 1).text()
        get_procedure_info = 'Ab'+get_procedure_number+': '+get_procedure_name
        self.inmem.change_current_system_name('Procedure')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()
        self.inmem.widget_ids['Procedure'].set_procedure_name(get_procedure_info)
        self.parent().close()  # 더블클릭 시 팝업 종료


# --------------------------------------------------------------------------------

class ProcedureSearchBottom(ABCWidget):
    def __init__(self, parent):
        super(ProcedureSearchBottom, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 5, 0, 10)
        lay.addStretch(1)
        lay.addWidget(ProcedureSearchOpen(self))
        lay.addWidget(ProcedureSearchCancel(self))
        lay.setSpacing(15)

class ProcedureSearchOpen(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSearchOpen, self).__init__(parent)
        self.setObjectName("Bottom")
        self.setFixedSize(160, 30)
        self.setText('열기')
        self.clicked.connect(self.dis_procedure)

    def dis_procedure(self):
        get_procedure_info = self.inmem.current_table['procedure_name']
        self.inmem.change_current_system_name('Procedure')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()
        self.inmem.widget_ids['Procedure'].set_procedure_name(get_procedure_info)
        # self.parent().close()  # 더블클릭 시 팝업 종료
        # self.inmem.change_current_system_name('Procedure')
        # self.inmem.widget_ids['MainTopSystemName'].dis_update()
        ProcedureSearch(self).close() # 절차서 전환 후 종료

class ProcedureSearchCancel(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSearchCancel, self).__init__(parent)
        self.setObjectName("Bottom")
        self.setFixedSize(160, 30)
        self.setText('취소')
        self.clicked.connect(self.close_ProcedureSearch)

    def close_ProcedureSearch(self):
        self.inmem.current_search['active_window'] = 0
        ProcedureSearch(self).close()

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class SystemSearch(ABCWidget):
    def __init__(self, parent):
        super(SystemSearch, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 상단바 제거
        self.setStyleSheet(qss.Search_Popup)
        self.setObjectName("Search")
        self.setGeometry(454, 215, 1190, 840)
        lay = QVBoxLayout(self)
        lay_content = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.TitleBar = SystemSearchTitleBar(self)
        lay.addWidget(self.TitleBar)
        lay_content.addWidget(SystemSearchWindow(self))
        lay_content.addWidget(SystemSearchScrollArea(self))
        lay_content.addWidget(SystemSearchBottom(self))
        lay_content.setContentsMargins(10, 0, 10, 0)
        lay.addLayout(lay_content)

    # window drag
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton) and self.TitleBar.underMouse():
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag and self.TitleBar.underMouse():
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 윈도우 position 변경
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
# --------------------------------------------------------------------------------

class SystemSearchTitleBar(ABCWidget):
    def __init__(self, parent):
        super(SystemSearchTitleBar, self).__init__(parent)
        self.setFixedHeight(50)
        self.setObjectName("SearchTitleBar")
        lay = QHBoxLayout(self)
        lay.addWidget(SystemSearchTitleName(self))
        lay.addWidget(SystemSearchClose(self))

class SystemSearchTitleName(ABCLabel):
    def __init__(self, parent):
        super(SystemSearchTitleName, self).__init__(parent)
        self.setObjectName("SearchTitleBar")
        self.setText('System Directory')

class SystemSearchClose(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchClose, self).__init__(parent)
        icon = os.path.join(ROOT_PATH, '../AIDAA_Ver21/Img/close.png')
        self.setObjectName("SearchTitleBar")
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(33, 33))  # 아이콘 크기
        self.setFixedSize(QSize(33, 33))
        self.setContentsMargins(1, 0, 0, 0)
        self.clicked.connect(self.close_SystemSearch)

    def close_SystemSearch(self):
        SystemSearch(self).close()

# --------------------------------------------------------------------------------

class SystemSearchWindow(ABCWidget):
    def __init__(self, parent):
        super(SystemSearchWindow, self).__init__(parent)
        self.setFixedHeight(130)
        lay = QHBoxLayout(self)
        lay.addStretch(1)
        lay.addWidget(SystemSearchLabel(self))
        lay.addWidget(SystemSearchInput(self))
        lay.addWidget(SystemSearchBTN(self))
        lay.addWidget(SystemSearchReset(self))
        lay.setContentsMargins(0, 10, 80, 10)
        lay.setSpacing(10)

        gb = QGroupBox('System 검색')
        gb.setObjectName("SearchWindow")
        gb.setContentsMargins(0, 0, 0, 0)
        gb.setFixedHeight(80)
        gb.setLayout(lay)

        search_lay = QHBoxLayout(self)
        search_lay.setContentsMargins(0, 0, 0, 0)
        search_lay.addWidget(gb)

class SystemSearchLabel(ABCLabel):
    def __init__(self, parent):
        super(SystemSearchLabel, self).__init__(parent)
        self.setFixedHeight(30)
        self.setObjectName("SearchLabel")
        self.setText('System 명')

class SystemSearchInput(ABCText):
    def __init__(self, parent):
        super(SystemSearchInput, self).__init__(parent)
        self.setFixedSize(456, 30)
        self.setObjectName("SearchInput")
        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        self.inmem.current_search['System'] = self.toPlainText()
        if self.inmem.current_search['system_reset'] == 0:
            self.clear()
            self.inmem.current_search['system_reset'] = -1

class SystemSearchBTN(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchBTN, self).__init__(parent)
        self.setFixedSize(160, 30)
        self.setObjectName("SearchBTN")
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
        self.setFixedSize(160, 30)
        self.setObjectName("SearchBTN")
        self.setText('리셋')
        self.clicked.connect(self.search_reset)

    def search_reset(self):
        self.inmem.current_search['system'] = ''
        self.inmem.current_search['system_reset'] = 0

# --------------------------------------------------------------------------------
class SystemSearchScrollArea(ABCScrollArea):
    def __init__(self, parent):
        super(SystemSearchScrollArea, self).__init__(parent)
        self.margins = QMargins(0, 40, 0, 0)  # header height
        self.setViewportMargins(self.margins)
        self.setFixedWidth(1170)
        # self.setFixedSize(1170, 600)  # 초기 테이블 크기

        self.headings_widget = QWidget(self)
        self.headings_layout = QHBoxLayout()
        self.headings_widget.setLayout(self.headings_layout)
        self.headings_layout.setContentsMargins(0, 0, 10, 0)

        # header item
        self.heading_label = QLabel(" System 명")
        self.heading_label.setFixedWidth(1140)

        self.headings_layout.addWidget(self.heading_label)
        self.heading_label.setObjectName("Alarm_Header")
        self.heading_label.setAlignment(Qt.AlignLeft and Qt.AlignVCenter)

        self.heading_label.setContentsMargins(5, 0, 0, 0)
        # self.headings_layout.addStretch(1)
        # self.headings_layout.setSpacing(0)


        self.scrollwidget = QWidget()
        self.grid = QGridLayout(self.scrollwidget)
        self.grid.addWidget(SystemSearchTable(self))
        self.grid.setContentsMargins(0, 0, 10, 0)
        self.setWidget(self.scrollwidget)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, event):
        rect = self.viewport().geometry()
        self.headings_widget.setGeometry(0, 0, rect.width() - 1, self.margins.top())
        QScrollArea.resizeEvent(self, event)

class SystemSearchTable(ABCTableWidget):
    def __init__(self, parent):
        super(SystemSearchTable, self).__init__(parent)
        self.column_labels = [(' System 명', 1140)]
        self.setColumnCount(len(self.column_labels))
        self.col_names = []
        self.setFixedSize(1140, 556)

        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            self.col_names.append(l)
        self.setHorizontalHeaderLabels(self.col_names)
        self.setRowCount(len(self.inmem.search_dict['System']))
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setShowGrid(False)  # Grid 지우기
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.horizontalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSortingEnabled(True)  # 테이블 sorting

        header = self.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.sortIndicatorChanged.connect(self.sortItems)
        self.horizontalHeader().setFixedHeight(40)
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 65)
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

class SystemSearchBottom(ABCWidget):
    def __init__(self, parent):
        super(SystemSearchBottom, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 5, 0, 10)
        lay.addStretch(1)
        lay.addWidget(SystemSearchOpen(self))
        lay.addWidget(SystemSearchCancle(self))
        lay.setSpacing(15)

class SystemSearchOpen(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchOpen, self).__init__(parent)
        self.setObjectName("Bottom")
        self.setFixedSize(160, 30)
        self.setText('열기')
        self.clicked.connect(self.dis_system)

    def dis_system(self): # CVCS만 구현되어 있기에, 무엇을 눌러도 CVCS 미믹창으로 전환됨.
        self.inmem.change_current_system_name('Action')
        self.inmem.widget_ids['MainTopSystemName'].dis_update()
        SystemSearch(self).close()

class SystemSearchCancle(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchCancle, self).__init__(parent)
        self.setObjectName("Bottom")
        self.setFixedSize(160, 30)
        self.setText('취소')
        self.clicked.connect(self.close_SystemSearch)

    def close_SystemSearch(self):
        SystemSearch(self).close()
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class XAISearch(ABCWidget):
    def __init__(self, parent):
        super(XAISearch, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 상단바 제거
        self.setStyleSheet(qss.Search_Popup)
        self.setObjectName("Search")
        self.setGeometry(454, 215, 800, 570)
        lay = QVBoxLayout(self)
        lay_content = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.TitleBar = XAISearchTitleBar(self)
        lay.addWidget(self.TitleBar)
        lay_content.addWidget(XAISearchWindow(self))
        lay_content.addWidget(XAISearchTable(self))
        lay_content.addWidget(XAISearchBottom(self))
        lay_content.setContentsMargins(10, 0, 10, 0)
        lay.addLayout(lay_content)

    # window drag
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton) and self.TitleBar.underMouse():
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag and self.TitleBar.underMouse():
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 윈도우 position 변경
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
# --------------------------------------------------------------------------------

class XAISearchTitleBar(ABCWidget):
    def __init__(self, parent):
        super(XAISearchTitleBar, self).__init__(parent)
        self.setFixedHeight(50)
        self.setObjectName("SearchTitleBar")
        lay = QHBoxLayout(self)
        lay.addWidget(XAISearchTitleName(self))
        lay.addWidget(XAISearchClose(self))

class XAISearchTitleName(ABCLabel):
    def __init__(self, parent):
        super(XAISearchTitleName, self).__init__(parent)
        self.setObjectName("SearchTitleBar3")
        self.setText('AI 기여도')

class XAISearchClose(ABCPushButton):
    def __init__(self, parent):
        super(XAISearchClose, self).__init__(parent)
        icon = os.path.join(ROOT_PATH, '../AIDAA_Ver21/Img/close.png')
        self.setObjectName("SearchTitleBar")
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(33, 33))  # 아이콘 크기
        self.setFixedSize(QSize(33, 33))
        self.setContentsMargins(1, 0, 0, 0)
        self.clicked.connect(self.close_XAISearch)

    def close_XAISearch(self):
        XAISearch(self).close()

# --------------------------------------------------------------------------------

class XAISearchWindow(ABCWidget):
    def __init__(self, parent):
        super(XAISearchWindow, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(XAISearchProcedureNumber(self))
        lay.addWidget(XAISearchProcedureName(self))
        lay.setContentsMargins(20, 10, 0, 10)
        lay.setSpacing(10)
        lay.addStretch(1)
        gb = QGroupBox(self)
        gb.setObjectName("SearchWindow")
        gb.setContentsMargins(0, 0, 0, 0)
        gb.setFixedHeight(80)
        gb.setLayout(lay)

        search_lay = QHBoxLayout(self)
        search_lay.setContentsMargins(0, 0, 0, 0)
        search_lay.addWidget(gb)

class XAISearchProcedureNumber(ABCLabel):
    def __init__(self, parent):
        super(XAISearchProcedureNumber, self).__init__(parent)
        self.setFixedHeight(30)
        self.setObjectName("SearchLabel")
        self.setText(f'{self.inmem.dis_AI["AI"][self.inmem.current_table["Procedure"]][0][2:7]}')

class XAISearchProcedureName(ABCLabel):
    def __init__(self, parent):
        super(XAISearchProcedureName, self).__init__(parent)
        self.setFixedHeight(30)
        self.setObjectName("SearchLabel")
        self.setText(f'{self.inmem.dis_AI["AI"][self.inmem.current_table["Procedure"]][0][9:]}')

# --------------------------------------------------------------------------------

class XAISearchTable(ABCTableWidget):
    def __init__(self, parent):
        super(XAISearchTable, self).__init__(parent)
        self.setRowCount(5)
        self.setFixedSize(780, 366)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setShowGrid(False)  # Grid 지우기
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.column_labels = [(' 변수 명', 200), (' 기여도', 940)]
        self.setColumnCount(len(self.column_labels))
        self.col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            self.col_names.append(l)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setHorizontalHeaderLabels(self.col_names)
        self.setSortingEnabled(True)  # 테이블 sorting

        header = self.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.sortIndicatorChanged.connect(self.sortItems)
        self.horizontalHeader().setFixedHeight(40)
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeaderItem(1).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 65)

        self.widget_timer(iter_=500, funs=[self.dis_update])

    def dis_update(self):
        try:
            if self.item(0, 0).text() == self.inmem.dis_AI['XAI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['XAI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['XAI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['XAI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['XAI'][4][0]:
                pass
            else:
                [self.setItem(i, 0, QTableWidgetItem(" " + self.inmem.dis_AI['XAI'][i][0])) for i in range(5)]
                [self.setItem(i, 1, QTableWidgetItem(" " +self.inmem.dis_AI['XAI'][i][1])) for i in range(5)]
        except:
            [self.setItem(i, 0, QTableWidgetItem(" " + self.inmem.dis_AI['XAI'][i][0])) for i in range(5)]
            [self.setItem(i, 1, QTableWidgetItem(" " + self.inmem.dis_AI['XAI'][i][1])) for i in range(5)]

# --------------------------------------------------------------------------------

class XAISearchBottom(ABCWidget):
    def __init__(self, parent):
        super(XAISearchBottom, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 5, 0, 10)
        lay.addStretch(1)
        lay.addWidget(XAISearchCancle(self))
        lay.setSpacing(15)

class XAISearchCancle(ABCPushButton):
    def __init__(self, parent):
        super(XAISearchCancle, self).__init__(parent)
        self.setObjectName("Bottom")
        self.setFixedSize(160, 30)
        self.setText('닫기')
        self.clicked.connect(self.close_XAISearch)

    def close_XAISearch(self):
        XAISearch(self).close()