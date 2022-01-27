import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver2.Interface import Flag


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(""), relative_path)


class MainTop2(QWidget):
    qss = """
            QWidget{
                background: rgb(231, 231, 234);
                margin: 0px;
            }
            QComboBox{
                background: white;
                border: 0px solid rgb(0, 0, 0); 
                border-radius: 3px;
                color: black;
                font-size: 14pt;
                padding: 5px 0px 5px 10px;
            }
            QListView{
                background-color: white;
            }
            QComboBox::drop-down 
            {
                width: 40px; 
                border: 0px; 
            }
            QComboBox::down-arrow {
                image: url(../interface/img/down.png);
                top: 3px;
                width: 60px;
                height: 60px;
            }
            QComboBox QAbstractItemView {
              border: 1px solid grey;
              background: white;
              selection-background-color: blue;
            }
            
            """
    def __init__(self, parent):
        super(MainTop2, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)

        # self.setFixedWidth(1450)
        self.parent = parent
        self.setStyleSheet(self.qss)
        self.layout = QHBoxLayout()
        self.layout.addWidget(MainTop2_combo(self))
        self.layout.setContentsMargins(5, 5, 2, 2)
        self.setLayout(self.layout)

class MainTop2_combo(QComboBox):
    def __init__(self, parent):
        super(MainTop2_combo, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(45)

        self.setContentsMargins(0, 0, 0, 0)
        self.activated[str].connect(self.onActivated)

        # const
        # QModelIndex
        # idx = colorComboBox->model()->index(x, y);
        # colorComboBox->model()->setData(idx, Qt: red, Qt::BackgroundColorRole);
        # colorComboBox->model()->setData(idx, Qt::blue, Qt::ForegroundRole);
        self.idx = -1
        self.blink_thread = Blink(self)

        timer = QTimer(self)
        timer.setInterval(1)
        timer.timeout.connect(self.list_update)
        timer.start()

        self.idx = self.model().index(0, 0)
        self.model().setData(self.idx, Qt.red, Qt.BackgroundColorRole)
        self.model().setData(self.idx, Qt.yellow, Qt.ForegroundRole)

        self.showPopup()
        # combo_thread = ComboBoxList(self)
        # combo_thread.start()


    def showPopup(self):
        super().showPopup()
        # find the widget that contains the list; note that this is *not* the view
        # that QComboBox.view() returns, but what is used to show it.
        popup = self.view().window()
        rect = popup.geometry()
        if not rect.contains(self.mapToGlobal(self.rect().center())):
            # the popup is not over the combo, there's no need to move it
            return
        # move the popup at the bottom left of the combo
        rect.moveTopLeft(self.mapToGlobal(self.rect().bottomLeft()))
        # ensure that the popup is always inside the edges of the screen
        # we use the center of the popup as a reference, since with multiple
        # screens the combo might be between two screens, but that position
        # could also be completely outside the screen, so the cursor position
        # is used as a fallback to decide on what screen we'll show it
        done = False
        for i, pos in enumerate((rect.center(), QCursor.pos())):
            for screen in QApplication.screens():
                if pos in screen.geometry():
                    screen = screen.geometry()
                    if rect.x() < screen.x():
                        rect.moveLeft(screen.x())
                    elif rect.right() > screen.right():
                        rect.moveRight(screen.right())
                    if rect.y() < screen.y():
                        rect.moveTop(screen.y())
                    elif rect.bottom() > screen.bottom():
                        # if the popup goes below the screen, move its bottom
                        # *over* the combo, so that the its current selected
                        # item will always be visible
                        rect.moveBottom(self.mapToGlobal(QPoint()).y())
                    done = True
                    break
            if done:
                break
        popup.move(rect.topLeft())


    def onActivated(self, text):
        # 절차서간 이동
        Flag.combo_click_text = text
        Flag.call_prss_name = text


        if (Flag.call_bottom_name_backup in Flag.combo_list) and (Flag.call_bottom_name_backup != Flag.combo_click_text):
            Flag.combo_blink_idx = Flag.combo_list.index(Flag.call_bottom_name_backup)
            # 1초 간격으로 blink
            Flag.combo_blink_start = True
            self.blink_thread.start()
        elif Flag.call_bottom_name_backup == Flag.combo_click_text:
            print("같음")
            Flag.combo_blink_start = False
            self.blink_thread.quit()

        Flag.combo_click_left = True
        Flag.combo_click_right = True

    def list_update(self):
        if Flag.combobox_update:
            # Flag.combobox_update = False
            self.clear()  # delete all items from comboBox
            self.addItems(Flag.combo_list)
            self.setCurrentText(Flag.call_prss_name)
            Flag.combobox_update = False
        if Flag.combo_blink_start:
            if Flag.combo_blink:
                self.setItemData(Flag.combo_blink_idx, QColor(255, 204, 0), Qt.BackgroundRole)
            else:
                self.setItemData(Flag.combo_blink_idx, QColor(Qt.white), Qt.BackgroundRole)
        else:
            self.setItemData(Flag.combo_blink_idx, QColor(Qt.white), Qt.BackgroundRole)
        # if Flag.combobox_update:
        #     Flag.combobox_update = False
        #     # self.clear()
        #     # list = Flag.return_list
        #     # self.addItems(list)
        #     self.addItem(Flag.return_list[-1])
        #     print("업데이트)")
        #     #combobox 가장 최신 클릭 text로 업데이트
        #     self.setCurrentText(Flag.call_bottom_name)


class Blink(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        while True:
            if Flag.combo_blink_start:
                if Flag.combo_blink:
                    Flag.combo_blink = False
                else:
                    Flag.combo_blink = True
            else:
                Flag.combo_blink = False
            self.sleep(1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainTop2()
    window.show()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    app.exec_()