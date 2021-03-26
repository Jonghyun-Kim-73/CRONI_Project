"""윈도우 타이틀 꾸미기
https://soma0sd.tistory.com/
"""
import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QtWidgets.QWidget):
    """메인 윈도우"""
    qss = """
        QWidget {
            color: #000000;
            background: #888;
        }
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet(self.qss)

        # 레이아웃과 타이틀바 위젯 생성
        window_vbox = QtWidgets.QVBoxLayout(self)
        window_vbox.setContentsMargins(0, 0, 0, 0)
        titlebar_widget = MainTitleBar(self)
        titlebar_widget.setObjectName("windowTitle")
        content_vbox = QtWidgets.QVBoxLayout()
        content_vbox.setContentsMargins(3, 3, 3, 3)

        # 타이틀바와 컨텐츠 박스 안의 내용물을 생성
        content_textedit = QtWidgets.QTextEdit()

        # 각 항목을 레이아웃에 배치
        content_vbox.addWidget(content_textedit)
        window_vbox.addWidget(titlebar_widget)
        window_vbox.addLayout(content_vbox)


class MainTitleBar(QtWidgets.QWidget):
    """제목 표시줄 위젯"""
    qss = """
        QWidget {
            color: #FFFFFF;
            background: #333333;
            height: 32px;
        }
        QLabel {
            color: #FFFFFF;
            background: #333333;
            font-size: 16px;
            padding: 5px 5px;
        }
        QToolButton {
            background: #333333;
            border: none;
        }
        QToolButton:hover{
            background: #444444;
        }
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bar_height = 36
        self.parent = parent
        self.has_clicked = False
        self.is_maximized = False
        self.setStyleSheet(self.qss)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        label = QtWidgets.QLabel("AIDAA")
        label.setFixedHeight(self.bar_height)
        btn_minimize = self.create_tool_btn('minimize.png')
        btn_minimize.clicked.connect(self.show_minimized)
        btn_close = self.create_tool_btn('close.png')
        btn_close.clicked.connect(self.close)

        layout.addWidget(label)
        layout.addWidget(btn_minimize)
        layout.addWidget(btn_close)

    def create_tool_btn(self, icon_path):
        """제목표시줄 아이콘 생성"""
        icon = os.path.join(ROOT_PATH, 'img', icon_path)
        btn = QtWidgets.QToolButton(self)
        btn.setIcon(QtGui.QIcon(icon))
        btn.setIconSize(QtCore.QSize(self.bar_height, self.bar_height))
        btn.setFixedSize(self.bar_height, self.bar_height)
        return btn

    def show_minimized(self):
        """버튼 명령: 최소화"""
        self.parent.showMinimized()

    def close(self):
        """버튼 명령: 닫기"""
        self.parent.close()

    def mousePressEvent(self, event):
        """오버로딩: 마우스 클릭 이벤트
        - 제목 표시줄 클릭시 이동 가능 플래그
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.parent.is_moving = True
            self.parent.offset = event.pos()

    def mouseMoveEvent(self, event):
        """오버로딩: 마우스 이동 이벤트
        - 제목 표시줄 드래그시 창 이동
        """
        if self.parent.is_moving:
            self.parent.move(event.globalPos() - self.parent.offset)

    def mouseDoubleClickEvent(self, event):
        """오버로딩: 더블클릭 이벤트
        - 제목 표시줄 더블클릭시 최대화
        """
        if self.is_maximized:
            self.parent.showNormal()
            self.is_maximized = False
        else:
            self.parent.showMaximized()
            self.is_maximized = True

if __name__ == "__main__":
    APP = QtWidgets.QApplication(sys.argv)
    WINDOW = MainWindow()
    WINDOW.show()
    APP.exec()