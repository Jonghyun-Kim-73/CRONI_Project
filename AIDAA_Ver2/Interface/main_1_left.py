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
            padding:3px;
            padding-left:15px;
            background: rgb(128, 128, 128);
            font-size:14pt;
            border:0px solid;
        }
        QTableView::item {
            color:black;
            padding:50px;
            font-size:14pt;
        }
        QScrollBar:vertical {
            width:30px;
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

        label1 = FreezeTableWidget(self)
        self.btn_suppress = QPushButton("Suppress button")
        self.btn_suppress.setFixedHeight(35)
        layout.addWidget(label1)
        layout.addWidget(self.btn_suppress)
        self.setLayout(layout)


class FreezeTableWidget(QTableView):
    def __init__(self, parent):
        super(FreezeTableWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMinimumSize(800, 600)

        # set the table model
        tm = MyTableModel(self)
        self.setModel(tm)

        self.frozenTableView = QTableView(self)
        self.frozenTableView.setModel(tm)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.viewport().stackUnder(self.frozenTableView)

        # table 선택 불가
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)

        # hide grid
        self.setShowGrid(False)

        # header 설정
        self.hh = self.horizontalHeader()
        self.hh.setDefaultAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.hh.setSectionResizeMode(0, QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기

        self.frozenTableView.show()
        self.updateFrozenTableGeometry()

        # item 별 scroll
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.frozenTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)

        self.frozenTableView.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.frozenTableView.verticalScrollBar().setValue)

        # get scroll position
        self.scrollBar = self.frozenTableView.verticalScrollBar()
        self.scrollBar.valueChanged.connect(lambda value: self.scrolled(self.scrollBar, value))

    def scrolled(self, scrollbar, value):
        if value == scrollbar.maximum():
            print(value)  # that will be the bottom/right end
        if value == scrollbar.minimum():
            print(value)  # top/left end

    def updateFrozenTableGeometry(self):
        if self.verticalHeader().isVisible():
            self.frozenTableView.setGeometry(self.verticalHeader().width() + self.frameWidth(),
                                             self.frameWidth(), self.frameWidth(),
                                             self.viewport().height() + self.horizontalHeader().height())
        else:
            self.frozenTableView.setGeometry(self.frameWidth(),
                                             self.frameWidth(), self.frameWidth(),
                                             self.viewport().height() + self.horizontalHeader().height())

    def paintEvent(self, e: QPaintEvent) -> None:
        # tableview add line
        super(FreezeTableWidget, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        pen.setColor(QColor(128, 128, 128))
        # 가로선 set width
        for i in range(30):
            if i % 5 == 0: pen.setWidth(3)
            else: pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i * 30, 960, i * 30)
        qp.restore()

class MyTableModel(QAbstractTableModel):
    def __init__(self, parent):
        super(MyTableModel, self).__init__(parent)
        # header
        self.colLabels = ['DESCRIPTION', 'VALUE', 'SETPOINT', 'UNIT', 'DATE', 'TIME']
        # col_info = [('DESCRIPTION', 340), ('VALUE', 160), ('SETPOINT',160),('UNIT',100),('DATE',100),('TIME',93)]  # 475

        # data  rows[index.row()][index.column()]

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
            return Qt.AlignLeft and Qt.AlignVCenter
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main1Left()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()
