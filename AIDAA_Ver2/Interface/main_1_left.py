import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Main1Left(QWidget):
    qss = """
        QWidget {
            background: rgb(231, 231, 234);
            border: 0px solid rgb(0, 0, 0); 
            font-size: 14pt;
        }
        QTableWidget {
            background: rgb(231, 231, 234);
            border: 1px solid rgb(128, 128, 128);
            border-radius: 6px;
        }
        QPushButton{
            background: White;
            color: Black;
            border-radius:6px;
        }
        QHeaderView::section {
            padding-left: 15px; 
            border: 0px;
        }
    """

    def __init__(self, parent=None):
        super(Main1Left, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.parent = parent
        self.setStyleSheet(self.qss)
        # self.setFixedWidth(990)
        # 기본 속성
        # self.setMinimumHeight(750)

        # 레이아웃
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        label1 = MainParaArea(self)
        self.btn_suppress = QPushButton("Suppress button")
        self.btn_suppress.setFixedHeight(35)
        layout.addWidget(label1)
        layout.addWidget(self.btn_suppress)
        self.setLayout(layout)


class MainParaArea(QTableWidget):
    def __init__(self, parent=None):
        super(MainParaArea, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        # 테이블 헤더 모양 정의
        # self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)  # Grid 지우기
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 테이블 셋업
        col_info = [('DESCRIPTION', 340), ('VALUE', 160), ('SETPOINT',160),('UNIT',100),('DATE',100),('TIME',93)]  # 475
        self.setColumnCount(6)
        self.setRowCount(29)
        self.horizontalHeader().setFixedHeight(30)
        # 편집 불가
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setContentsMargins(0, 0, 0, 0)

        col_names = []
        for i, (l, w) in enumerate(col_info):
            self.setColumnWidth(i, w)
            col_names.append(l)

        # 테이블 헤더
        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().setStyleSheet("::section {background: rgb(128, 128, 128);font-size:14pt;border:0px solid;}")
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft and Qt.AlignVCenter)

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 30)

    def paintEvent(self, e: QPaintEvent) -> None:
        """ tabelview의 위에 라인 그리기 """
        super(MainParaArea, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        for i in range(30):
            if i % 5 == 0:
                pen.setColor(QColor(128, 128, 128))            # 가로선 -> 버튼 color
                pen.setWidth(3)
            else:
                pen.setColor(QColor(127, 127, 127))         # 가로선 -> 활성화 x color
                pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i*30, 960, i*30)
        qp.restore()


class FreezeTableWidget(QTableView):
    def __init__(self, parent=None, *args):
        QTableView.__init__(self, parent, *args)

        self.setMinimumSize(800, 600)

        # set the table model
        tm = MyTableModel(self)

        # set the proxy model
        pm = QSortFilterProxyModel(self)
        pm.setSourceModel(tm)

        self.setModel(pm)

        self.frozenTableView = QTableView(self)
        self.frozenTableView.setModel(pm)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.setFocusPolicy(Qt.NoFocus)
        # self.frozenTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.frozenTableView.setStyleSheet('''border: none;''')
        self.frozenTableView.setSelectionModel(QAbstractItemView.selectionModel(self))
        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.viewport().stackUnder(self.frozenTableView)

        self.setEditTriggers(QAbstractItemView.SelectedClicked)

        # hide grid
        self.setShowGrid(False)

        # self.setStyleSheet('font: 10pt "Courier New"')

        hh = self.horizontalHeader()
        hh.setDefaultAlignment(Qt.AlignCenter)
        hh.setStretchLastSection(True)

        # self.resizeColumnsToContents()

        ncol = tm.columnCount(self)
        # for col in range(ncol):
        #     if col == 0:
        #         self.horizontalHeader().resizeSection(col, 60)
        #         # self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)
        #         self.frozenTableView.setColumnWidth(col, self.columnWidth(col))
        #     elif col == 1:
        #         self.horizontalHeader().resizeSection(col, 150)
        #         # self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)
        #         self.frozenTableView.setColumnWidth(col, self.columnWidth(col))
        #     else:
        #         self.horizontalHeader().resizeSection(col, 100)
        #         self.frozenTableView.setColumnHidden(col, True)

        self.frozenTableView.setSortingEnabled(True)
        self.frozenTableView.sortByColumn(0, Qt.AscendingOrder)

        #self.setAlternatingRowColors(True)

        vh = self.verticalHeader()
        vh.setDefaultSectionSize(30)
        vh.setDefaultAlignment(Qt.AlignCenter)
        vh.setVisible(True)
        self.frozenTableView.verticalHeader().setDefaultSectionSize(vh.defaultSectionSize())

        # nrows = tm.rowCount(self)
        # for row in range(nrows):
        #     self.setRowHeight(row, 25)

        self.frozenTableView.show()
        self.updateFrozenTableGeometry()

        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.frozenTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # connect the headers and scrollbars of both tableviews together
        # self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.horizontalHeader().setStyleSheet("::section {background: rgb(128, 128, 128);font-size:14pt;border:0px solid;}")
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)  # Grid 지우기
        self.frozenTableView.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.frozenTableView.verticalScrollBar().setValue)

        qf = QFrame(self.viewport())
        qf.setFrameShape(QFrame.HLine)
        qf.setFrameShadow(QFrame.Plain)
        qf.show()
        # self.frozenTableView.setIndexWidget(index=(0,0), qf)
        # self.frozenTableView.setCell
        # QFrame(ui->tableWidget->viewport());
        # qf->setFrameShape(QFrame::HLine);
        # qf->setFrameShadow(QFrame::Plain);
        # qf->show();

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self, event):
        QTableView.resizeEvent(self, event)
        # self.updateFrozenTableGeometry()

    def scrollTo(self, index, hint):
        if index.column() > 1:
            QTableView.scrollTo(self, index, hint)

    def updateFrozenTableGeometry(self):
        if self.verticalHeader().isVisible():
            self.frozenTableView.setGeometry(self.verticalHeader().width() + self.frameWidth(),
                                             self.frameWidth(), self.frameWidth(),
                                             self.viewport().height() + self.horizontalHeader().height())
        else:
            self.frozenTableView.setGeometry(self.frameWidth(),
                                             self.frameWidth(), self.frameWidth(),
                                             self.viewport().height() + self.horizontalHeader().height())

    def moveCursor(self, cursorAction, modifiers):
        current = QTableView.moveCursor(self, cursorAction, modifiers)
        x = self.visualRect(current).topLeft().x()
        frozen_width = self.frozenTableView.columnWidth(0) + self.frozenTableView.columnWidth(1)
        if cursorAction == self.MoveLeft and current.column() > 1 and x < frozen_width:
            new_value = self.horizontalScrollBar().value() + x - frozen_width
            self.horizontalScrollBar().setValue(new_value)
        return current


    # def paintEvent(self, e: QPaintEvent) -> None:
    #     """ tabelview의 위에 라인 그리기 """
    #     super(FreezeTableWidget, self).paintEvent(e)
    #     qp = QPainter(self.viewport())
    #     qp.save()
    #     pen = QPen()
    #     for i in range(30):
    #         if i % 5 == 0:
    #             pen.setColor(QColor(128, 128, 128))            # 가로선 -> 버튼 color
    #             pen.setWidth(3)
    #         else:
    #             pen.setColor(QColor(127, 127, 127))         # 가로선 -> 활성화 x color
    #             pen.setWidth(1)
    #         qp.setPen(pen)
    #         qp.drawLine(0, i*30, 960, i*30)
    #     qp.restore()


class MyTableModel(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.colLabels = ['DESCRIPTION', 'VALUE', 'SETPOINT', 'UNIT', 'DATE', 'TIME']
        self.dataCached = [['cell%02d,%02d' % (i, j) for i in range(1, 7)]
                           for j in range(1, 51)]

    def rowCount(self, parent):
        return len(self.dataCached)

    def columnCount(self, parent):
        return len(self.colLabels)

    def get_value(self, index):
        i = index.row()
        j = index.column()
        return self.dataCached[i][j]

    def data(self, index, role):
        if not index.isValid():
            return None
        value = self.get_value(index)
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return value
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return None

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            self.dataCached[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        else:
            return False

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = self.colLabels[section]
            return header
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section + 1)

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        elif index.column() > 1:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main1Left()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()
