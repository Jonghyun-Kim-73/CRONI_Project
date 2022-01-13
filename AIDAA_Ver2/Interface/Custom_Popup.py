import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView

from AIDAA_Ver2.Interface import Flag


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

source1 = resource_path(".//img/close.png")
class Popup(QWidget):
    qss = """
            QDialog{
            background:white;
            border: 1px solid rgb(128,128,128);             
            }
        """

    def __init__(self, file_path=None):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(self.qss)
        self.layout.addStretch(-1)
        self.setWindowTitle(f"{Flag.alarm_popup_name}")
        # self.setGeometry(0, 0, 1000, 750)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # self.centralWidget = QWidget(self)

        # test_pdf = "test.pdf"
        # file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), test_pdf))
        # print(file_path)

        self.webView = QWebEngineView()
        self.webView.setUrl(QUrl.fromLocalFile(file_path))
        self.webView.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.webView.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)

        self.layout.addWidget(self.webView)

    def showModal(self):
        return super().exec_()

    def url_changed(self):
        self.setWindowTitle(self.webView.title())

    def go_back(self):
        self.webView.back()

class MyBar(QWidget):
    qss = """
        QPushButton {
            background: rgb(100, 25, 28);
            border-radius: 6px;
            border: none;
            margin-right:5px;
        }
        QPushButton:hover {
            background: rgb(184, 25, 28);
        }
        QPushButton:pressed {
            background: rgb(215, 25, 28);
        }
        """
    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        self.setStyleSheet(self.qss)
        self.setMinimumHeight(40)
        self.setMinimumWidth(400)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Flag.alarm_popup_name 받아오기
        self.title = QLabel(f"{Flag.alarm_popup_name}")

        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedSize(50,40)
        self.title.setStyleSheet("""
            background-color: rgb(128, 128, 128);
            border: 1px solid rgb(128, 128, 128);       
            color: black;
            font-size: 14pt;
        """)

        btn_close = QPushButton()
        btn_close.setIcon(QIcon(source1))
        btn_close.setStyleSheet("border:0px")
        btn_close.clicked.connect(self.close)
        btn_close.setIconSize(QSize(30,35))

        self.layout.addWidget(self.title)
        self.layout.addWidget(btn_close)
        self.setLayout(self.layout)


    def showModal(self):
        return super().exec_()

    def close(self):
        self.setDisabled(True)
        self.parent.close()

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Popup(file_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "test.pdf")))
    ex.show()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    sys.exit(app.exec_())