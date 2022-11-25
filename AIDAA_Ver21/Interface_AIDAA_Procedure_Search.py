import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Function_Simulator_CNS import *
from Interface_QSS import qss

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# ----------------------------------------------------------------------------------------------------------------------
class ProcedureSearch(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setStyleSheet(qss)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 상단바 제거
        self.setGeometry(454, 215, 1190, 840)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.TitleBar = ProcedureSearchTitleBar(self)
        lay.addWidget(self.TitleBar)

        lay_content = QVBoxLayout()
        lay_content.addWidget(ProcedureSearchWindow(self))
        lay_content.addWidget(ProcedureSearchScrollArea(self))
        lay_content.addWidget(ProcedureSearchBottom(self))
        lay_content.setContentsMargins(10, 0, 10, 0)

        lay.addLayout(lay_content)
        
        self.m_flag = False
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
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedHeight(50)
        lay = QHBoxLayout(self)
        lay.addWidget(ProcedureSearchTitleName(self))
        lay.addWidget(ProcedureSearchClose(self))
class ProcedureSearchTitleName(ABCLabel):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Procedure Directory')
class ProcedureSearchClose(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        icon = os.path.join(ROOT_PATH, '../AIDAA_Ver21/Img/close.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(33, 33))  # 아이콘 크기
        self.setFixedSize(QSize(33, 33))
        self.setContentsMargins(1, 0, 0, 0)
        self.clicked.connect(self.inmem.widget_ids['ProcedureSearch'].close)
# --------------------------------------------------------------------------------
class ProcedureSearchWindow(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        search_lay = QHBoxLayout(self)
        search_lay.setContentsMargins(0, 0, 0, 0)
        search_lay.addWidget(ProcedureSearchWindowGroupBox(self))
class ProcedureSearchWindowGroupBox(ABCGroupBox):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setTitle('절차서 검색')
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(126)

        lay = QVBoxLayout(self)
        lay.addWidget(ProcedureSearch1(self))
        lay.addWidget(ProcedureSearch2(self))
        lay.setContentsMargins(0, 10, 200, 10)
        lay.setSpacing(5)
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
        self.setText('절차서 번호')
class ProcedureSearchInput1(ABCPlainTextEdit):
    def __init__(self, parent):
        super(ProcedureSearchInput1, self).__init__(parent)
        self.setFixedSize(456, 30)
class ProcedureSearchBTN(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSearchBTN, self).__init__(parent)
        self.setFixedSize(160, 30)
        self.setText('검색')
        self.clicked.connect(lambda :self.inmem.widget_ids['ProcedureSearchTable'].show_procedure_list_in_table())
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
        self.setText('절차서 명')
class ProcedureSearchInput2(ABCPlainTextEdit):
    def __init__(self, parent):
        super(ProcedureSearchInput2, self).__init__(parent)
        self.setFixedSize(456, 30)
class ProcedureSearchReset(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSearchReset, self).__init__(parent)
        self.setFixedSize(160, 30)
        self.setText('초기화')
        self.clicked.connect(self.search_reset)

    def search_reset(self):
        self.inmem.widget_ids['ProcedureSearchInput1'].clear()
        self.inmem.widget_ids['ProcedureSearchInput2'].clear()
        self.inmem.widget_ids['ProcedureSearchTable'].show_procedure_list_in_table()
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
        self.heading_label = [
            ProcedureHeadingLabel(self, " 절차서 번호", 200, 'F'),
            ProcedureHeadingLabel(self, " 절차서명", 940, 'L'),
        ]
        for label in self.heading_label:
            self.headings_layout.addWidget(label)
            label.setAlignment(Qt.AlignLeft and Qt.AlignVCenter)

        self.heading_label[0].setContentsMargins(5, 0, 0, 0)
        
        # self.headings_layout.addStretch(1)
        self.headings_layout.setSpacing(0)
        
        self.setWidget(ProcedureSearchTableWidget(self))
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
        
        self.setShowGrid(False)  # Grid 지우기
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.horizontalHeader().setVisible(False)  # Col header 숨기기
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QTableView.SelectRows)  # 테이블 row click
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
        self.column_labels = [(' 절차서 번호', 200), (' 절차서 명', 940)]
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(len(list(self.inmem.abnormal_procedure_list)))
        self.col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            self.col_names.append(l)
        
        # 테이블 헤더
        self.setHorizontalHeaderLabels(self.col_names)
        self.setSortingEnabled(True)  # 테이블 sorting
        self.horizontalHeader().setFixedHeight(40)
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeaderItem(1).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정
        
        [self.setRowHeight(i, 65) for i in range(self.rowCount())] # 테이블 행 높이 조절
        
        self.itemDoubleClicked.connect(self.open_clicked_item_procedure)
        self.show_procedure_list_in_table()

    def show_procedure_list_in_table(self):
        [self.removeRow(0) for _ in range(self.rowCount())]
        
        selected_procedure_name = self.inmem.widget_ids['ProcedureSearchInput2'].toPlainText()
        selected_procedure_num = self.inmem.widget_ids['ProcedureSearchInput1'].toPlainText()
        
        find_procedure_names, is_procedure_name_in_db = self.inmem.is_procedure_name_in_db(selected_procedure_name)
        find_procedure_nubs, is_procedure_nub_in_db = self.inmem.is_procedure_name_in_db(selected_procedure_num)
        
        if is_procedure_name_in_db and not is_procedure_nub_in_db:
            final_procedure_list = find_procedure_names
        elif is_procedure_nub_in_db and not is_procedure_name_in_db:
            final_procedure_list = find_procedure_nubs
        elif is_procedure_nub_in_db and is_procedure_name_in_db:
            final_procedure_list = list(set(find_procedure_nubs) - set(find_procedure_names))
        else:
            final_procedure_list = list(self.inmem.abnormal_procedure_list)
        
        self.setRowCount(len(final_procedure_list))
        [self.setItem(i, 0, ProcedureSearchItem(self, f' {pro_name.split(":")[0]}', pro_name)) for i, pro_name in enumerate(final_procedure_list)]
        [self.setItem(i, 1, ProcedureSearchItem(self, f' {pro_name.split(":")[1]}', pro_name)) for i, pro_name in enumerate(final_procedure_list)]
        [self.setRowHeight(i, 65) for i in range(self.rowCount())]
    
    def open_clicked_item_procedure(self):
        if not len(self.selectedItems()) == 0:
            pro_name = self.selectedItems()[0].pro_name
            self.inmem.widget_ids['Procedure'].set_procedure_name(pro_name)
            self.inmem.widget_ids['MainTab'].change_system_page('Procedure')
            self.inmem.widget_ids['ProcedureSearch'].close()
        else:
            pass
# ----------------------------------------------------------------------------------------------------------------------        
class ProcedureSearchItem(ABCTabWidgetItem):
    def __init__(self, parent, text, pro_name, widget_name=''):
        super().__init__(parent, widget_name)
        self.pro_name = pro_name
        self.setText(text)
class ProcedureSearchTableWidget(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        
        self.proceduresearchtable = ProcedureSearchTable(self)
        self.setFixedWidth(self.proceduresearchtable.width())
        
        vl = QVBoxLayout(self)
        vl.addWidget(self.proceduresearchtable)
        vl.addStretch(1)
        vl.setContentsMargins(0, 0, 10, 0)
class ProcedureHeadingLabel(ABCLabel):
    def __init__(self, parent, text, fix_width, pos, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedWidth(fix_width)
        self.setText(text)
        self.setProperty('Pos', pos)
        self.style().polish(self)
# ----------------------------------------------------------------------------------------------------------------------
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
        self.setFixedSize(160, 30)
        self.setText('열기')
        self.clicked.connect(self.inmem.widget_ids['ProcedureSearchTable'].open_clicked_item_procedure)
class ProcedureSearchCancel(ABCPushButton):
    def __init__(self, parent):
        super(ProcedureSearchCancel, self).__init__(parent)
        self.setFixedSize(160, 30)
        self.setText('취소')
        self.clicked.connect(self.inmem.widget_ids['ProcedureSearch'].close)
# ----------------------------------------------------------------------------------------------------------------------
class SystemSearch(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setStyleSheet(qss)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 상단바 제거
        self.setGeometry(454, 215, 1190, 840)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.TitleBar = SystemSearchTitleBar(self)
        lay.addWidget(self.TitleBar)
        
        lay_content = QVBoxLayout()
        lay_content.addWidget(SystemSearchWindow(self))
        lay_content.addWidget(SystemSearchScrollArea(self))
        lay_content.addWidget(SystemSearchBottom(self))
        lay_content.setContentsMargins(10, 0, 10, 0)
        
        lay.addLayout(lay_content)

        self.m_flag = False
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
        lay = QHBoxLayout(self)
        lay.addWidget(SystemSearchTitleName(self))
        lay.addWidget(SystemSearchClose(self))
class SystemSearchTitleName(ABCLabel):
    def __init__(self, parent):
        super(SystemSearchTitleName, self).__init__(parent)
        self.setText('System Directory')
class SystemSearchClose(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchClose, self).__init__(parent)
        icon = os.path.join(ROOT_PATH, '../AIDAA_Ver21/Img/close.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(33, 33))  # 아이콘 크기
        self.setFixedSize(QSize(33, 33))
        self.setContentsMargins(1, 0, 0, 0)
        self.clicked.connect(self.inmem.widget_ids['SystemSearch'].close)
# --------------------------------------------------------------------------------
class SystemSearchWindow(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedHeight(130)
        search_lay = QHBoxLayout(self)
        search_lay.setContentsMargins(0, 0, 0, 0)
        search_lay.addWidget(SystemSearchWindowGroupBox(self))
class SystemSearchWindowGroupBox(ABCGroupBox):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setTitle('System 검색')
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(80)

        lay = QHBoxLayout(self)
        lay.addStretch(1)
        lay.addWidget(SystemSearchLabel(self))
        lay.addWidget(SystemSearchInput(self))
        lay.addWidget(SystemSearchBTN(self))
        lay.addWidget(SystemSearchReset(self))
        lay.setContentsMargins(0, 10, 80, 10)
        lay.setSpacing(10)
class SystemSearchLabel(ABCLabel):
    def __init__(self, parent):
        super(SystemSearchLabel, self).__init__(parent)
        self.setFixedHeight(30)
        self.setText('System 명')
class SystemSearchInput(ABCPlainTextEdit):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedSize(456, 30)
class SystemSearchBTN(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchBTN, self).__init__(parent)
        self.setFixedSize(160, 30)
        self.setText('검색')
        self.clicked.connect(lambda :self.inmem.widget_ids['SystemSearchTable'].show_system_list_in_table())
class SystemSearchReset(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchReset, self).__init__(parent)
        self.setFixedSize(160, 30)
        self.setText('초기화')
        self.clicked.connect(self.search_reset)
    
    def search_reset(self):
        self.inmem.widget_ids['SystemSearchInput'].clear()
        self.inmem.widget_ids['SystemSearchTable'].show_system_list_in_table()
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
        self.heading_label = SystemSearchHeadingLabel(self, " System 명", 1140, 'F')
        self.headings_layout.addWidget(self.heading_label)
        self.heading_label.setAlignment(Qt.AlignLeft and Qt.AlignVCenter)

        self.heading_label.setContentsMargins(5, 0, 0, 0)

        self.setWidget(SystemSearchTableWidget(self))
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
        self.setFixedSize(1140, 556)
        
        self.setShowGrid(False)  # Grid 지우기
        # self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.horizontalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QTableView.SelectRows)  # 테이블 row click
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
        self.column_labels = [(' System 명', 1140)]
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(len(self.inmem.abnormal_system_list))
        self.col_names = []
        for i, (l, w) in enumerate(self.column_labels):
            self.setColumnWidth(i, w)
            self.col_names.append(l)
        
        # 테이블 헤더
        self.setHorizontalHeaderLabels(self.col_names)
        # header = self.horizontalHeader()
        # header.setSortIndicatorShown(True)
        # header.sortIndicatorChanged.connect(self.sortItems)
        self.setSortingEnabled(True)  # 테이블 sorting
        self.horizontalHeader().setFixedHeight(40)
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정

        [self.setRowHeight(i, 65) for i in range(self.rowCount())] # 테이블 행 높이 조절
        
        self.itemDoubleClicked.connect(self.open_clicked_item_system)
        self.show_system_list_in_table()

    def show_system_list_in_table(self):
        [self.removeRow(0) for _ in range(self.rowCount())]
        
        selected_system_name = self.inmem.widget_ids['SystemSearchInput'].toPlainText()
        
        find_system_names, is_system_name_in_db = self.inmem.is_system_name_in_db(selected_system_name)
        
        if is_system_name_in_db:
            final_system_list = find_system_names
        else:
            final_system_list = self.inmem.abnormal_system_list
        
        self.setRowCount(len(final_system_list))
        [self.setItem(i, 0, SystemSearchItem(self, f' {sys_name}', sys_name)) for i, sys_name in enumerate(final_system_list)]
        [self.setRowHeight(i, 65) for i in range(self.rowCount())]

    def open_clicked_item_system(self):
        if not len(self.selectedItems()) == 0:
            sys_name = self.selectedItems()[0].sys_name
            self.inmem.widget_ids['ActionTitleLabel'].update_text(sys_name)
            self.inmem.widget_ids['MainTab'].change_system_page('Action')
            self.inmem.widget_ids['SystemSearch'].close()
        else:
            pass
# --------------------------------------------------------------------------------
class SystemSearchItem(ABCTabWidgetItem):
    def __init__(self, parent, text, sys_name, widget_name=''):
        super().__init__(parent, widget_name)
        self.sys_name = sys_name
        self.setText(text)
class SystemSearchTableWidget(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        
        self.SystemSearchtable = SystemSearchTable(self)
        self.setFixedWidth(self.SystemSearchtable.width())
        
        vl = QVBoxLayout(self)
        vl.addWidget(self.SystemSearchtable)
        vl.addStretch(1)
        vl.setContentsMargins(0, 0, 10, 0)
class SystemSearchHeadingLabel(ABCLabel):
    def __init__(self, parent, text, fix_width, pos, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedWidth(fix_width)
        self.setText(text)
        self.setProperty('Pos', pos)
        self.style().polish(self)
# --------------------------------------------------------------------------------
class SystemSearchBottom(ABCWidget):
    def __init__(self, parent):
        super(SystemSearchBottom, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 5, 0, 10)
        lay.addStretch(1)
        lay.addWidget(SystemSearchOpen(self))
        lay.addWidget(SystemSearchCancel(self))
        lay.setSpacing(15)
class SystemSearchOpen(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchOpen, self).__init__(parent)
        self.setFixedSize(160, 30)
        self.setText('열기')
        self.clicked.connect(self.inmem.widget_ids['SystemSearchTable'].open_clicked_item_system)
class SystemSearchCancel(ABCPushButton):
    def __init__(self, parent):
        super(SystemSearchCancel, self).__init__(parent)
        self.setFixedSize(160, 30)
        self.setText('취소')
        self.clicked.connect(self.inmem.widget_ids['SystemSearch'].close)
# ----------------------------------------------------------------------------------------------------------------------
class XAISearch(ABCWidget):
    def __init__(self, parent):
        super(XAISearch, self).__init__(parent)
        self.setStyleSheet(qss)
        
        self.setWindowFlags(Qt.FramelessWindowHint)  # 상단바 제거
        self.setGeometry(454, 215, 800, 570)
        
        lay = QVBoxLayout(self)
        lay_content = QVBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)
        self.TitleBar = XAISearchTitleBar(self)
        lay.addWidget(self.TitleBar)
        lay.addLayout(lay_content)
        lay_content.addWidget(XAISearchWindow(self))
        lay_content.addWidget(XAISearchScrollArea(self))
        lay_content.addWidget(XAISearchBottom(self))
        lay_content.setContentsMargins(10, 0, 10, 0)
        self.name = ''
        self.m_flag = False
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
    
    def show(self, name) -> None:
        self.name = name # 절차서 명 또는 시스템 명을 전달받은 뒤 업데이트
        self.inmem.widget_ids['XAISearchTitleName'].setText(name)
        return super().show()
# --------------------------------------------------------------------------------
class XAISearchTitleBar(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedHeight(50)
        lay = QHBoxLayout(self)
        lay.addWidget(XAISearchTitleBarName(self))
        lay.addWidget(XAISearchClose(self))
class XAISearchTitleBarName(ABCLabel):
    def __init__(self, parent):
        super(XAISearchTitleBarName, self).__init__(parent)
        self.setText('AI 기여도')
class XAISearchClose(ABCPushButton):
    def __init__(self, parent):
        super(XAISearchClose, self).__init__(parent)
        icon = os.path.join(ROOT_PATH, '../AIDAA_Ver21/Img/close.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(33, 33))  # 아이콘 크기
        self.setFixedSize(QSize(33, 33))
        self.setContentsMargins(1, 0, 0, 0)
        self.clicked.connect(self.inmem.widget_ids['XAISearch'].close)
# --------------------------------------------------------------------------------
class XAISearchWindow(ABCWidget):
    def __init__(self, parent):
        super(XAISearchWindow, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(XAISearchTitleName(self))
        lay.setContentsMargins(20, 10, 0, 10)
        lay.setSpacing(10)
        lay.addStretch(1)
class XAISearchTitleName(ABCLabel):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('')
# --------------------------------------------------------------------------------
class XAISearchScrollArea(ABCScrollArea):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.heading_height = 40

    def resizeEvent(self, a0: QResizeEvent) -> None:
        # resize 된 이후 수행
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay_heading = QHBoxLayout()
        lay_heading.setContentsMargins(0, 0, 0, 0)
        lay_heading.setSpacing(0)
        
        lay.addLayout(lay_heading)

        col_info = {' 변수 명':200, ' 기여도': self.size().width() - 200}

        lay_heading.addWidget(XAISearchHeadingLabel(self, ' 변수 명', col_info[' 변수 명'], self.heading_height, 'F'))
        lay_heading.addWidget(XAISearchHeadingLabel(self, ' 기여도', col_info[' 기여도'], self.heading_height, 'L'))
        
        lay.addWidget(XAISearchTable(self, col_info))

        return super().resizeEvent(a0)
class XAISearchHeadingLabel(ABCLabel):
    def __init__(self, parent, text, fix_width, fix_height, pos, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
        self.setFixedWidth(fix_width)
        self.setFixedHeight(fix_height)
        self.setProperty('Pos', pos)
        self.style().polish(self)
class XAISearchTable(ABCTableWidget):
    def __init__(self, parent, col_info:dict, widget_name=''):
        super().__init__(parent, widget_name)
        self.setRowCount(5)
        # self.setFixedSize(780, 366)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setShowGrid(False)  # Grid 지우기
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.horizontalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
        self.setColumnCount(len(col_info))

        for i, (l, w) in enumerate(col_info.items()):
            self.setColumnWidth(i, w)

        self.setSortingEnabled(True)  # 테이블 sorting

        [self.setRowHeight(i, 65) for i in range(self.rowCount())] # 테이블 행 높이 조절

        try:
            if self.item(0, 0).text() == self.inmem.dis_AI['XAI'][0][0] and self.item(1, 0).text() == self.inmem.dis_AI['XAI'][1][0] and self.item(2, 0).text() == self.inmem.dis_AI['XAI'][2][0] and self.item(3, 0).text() == self.inmem.dis_AI['XAI'][3][0] and self.item(4, 0).text() == self.inmem.dis_AI['XAI'][4][0]:
                pass
            else:
                [self.setCellWidget(i, 0, XAISearchItem(self, " " + self.inmem.dis_AI['XAI'][i][0], Qt.AlignmentFlag.AlignCenter, 'F')) for i in range(5)]
                [self.setCellWidget(i, 1, XAISearchItem(self, " " +self.inmem.dis_AI['XAI'][i][1], Qt.AlignmentFlag.AlignLeft, 'L')) for i in range(5)]
        except:
            [self.setCellWidget(i, 0, XAISearchItem(self, " " + self.inmem.dis_AI['XAI'][i][0], Qt.AlignmentFlag.AlignCenter, 'F')) for i in range(5)]
            [self.setCellWidget(i, 1, XAISearchItem(self, " " + self.inmem.dis_AI['XAI'][i][1], Qt.AlignmentFlag.AlignLeft, 'L')) for i in range(5)]
class XAISearchItem(ABCLabel):
    def __init__(self, parent, text, alignment, pos, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(text)
        self.setProperty('Pos', pos)
        self.setAlignment(Qt.AlignVCenter | alignment)
# --------------------------------------------------------------------------------
class XAISearchBottom(ABCWidget):
    def __init__(self, parent):
        super(XAISearchBottom, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 5, 0, 10)
        lay.addStretch(1)
        lay.addWidget(XAISearchCancel(self))
        lay.setSpacing(15)
class XAISearchCancel(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setFixedSize(160, 30)
        self.setText('닫기')
        self.clicked.connect(self.inmem.widget_ids['XAISearch'].close)