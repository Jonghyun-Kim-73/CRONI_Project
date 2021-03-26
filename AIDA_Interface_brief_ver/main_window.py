import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class Mainwindow(QWidget):
    """메인 윈도우"""
    qss = """
        QWidget {
            color: #000000;
            background: #888;
        }
    """

    def __init__(self, parnet):
        super(Mainwindow, self).__init__()
        self.top_window = parnet
        # --------------------------------------------------------------------------------------------------------------
        self.setGeometry(300, 300, 600, 600)    # initial window size
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(self.qss)

        # 레이아웃과 타이틀바 위젯 생성
        window_vbox = QVBoxLayout(self)
        window_vbox.setContentsMargins(0, 0, 0, 0)
        titlebar_widget = MainTitleBar(self)
        titlebar_widget.setObjectName("windowTitle")

        content_vbox = QVBoxLayout()
        content_vbox.setContentsMargins(0, 0, 0, 0)

        # 타이틀바와 컨텐츠 박스 안의 내용물을 생성
        content_textedit = QTextEdit()

        # 각 항목을 레이아웃에 배치
        content_vbox.addWidget(content_textedit)
        window_vbox.addWidget(titlebar_widget)
        window_vbox.addLayout(content_vbox)


class MainTitleBar(QWidget):
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
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        label = QLabel("AIDAA")
        label.setFixedHeight(self.bar_height)
        # btn_minimize = self.create_tool_btn('minimize.png')
        # btn_minimize.clicked.connect(self.show_minimized)
        btn_close = self.create_tool_btn('close.PNG')
        btn_close.clicked.connect(self.close)

        layout.addWidget(label)
        # layout.addWidget(btn_minimize)
        layout.addWidget(btn_close)

    def create_tool_btn(self, icon_path):
        """제목표시줄 아이콘 생성"""
        icon = os.path.join(ROOT_PATH, 'interface_image', icon_path)
        print(icon)
        btn = QToolButton(self)
        btn.setIcon(QIcon(icon))
        btn.setIconSize(QSize(self.bar_height, self.bar_height))
        btn.setFixedSize(self.bar_height, self.bar_height)
        return btn

    def close(self):
        """버튼 명령: 닫기"""
        self.parent.close()

    def mousePressEvent(self, event):
        """오버로딩: 마우스 클릭 이벤트
        - 제목 표시줄 클릭시 이동 가능 플래그
        """
        if event.button() == Qt.LeftButton:
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


if __name__ == '__main__':
    print('test')
    app = QApplication(sys.argv)
    window = Mainwindow(None)
    window.show()
    app.exec_()