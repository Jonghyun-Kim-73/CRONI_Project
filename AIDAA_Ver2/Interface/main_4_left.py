import sys
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic.properties import QtGui

from AIDAA_Ver2.Interface import Flag
from AIDAA_Ver2.Procedure.ab_procedure import ab_pro


class Main4Left(QWidget):
    qss = """
        QWidget {
            background: rgb(231, 231, 234);
            border: 0px solid rgb(0, 0, 0); 
            font-size: 14pt;
        }
        QPushButton{
            background: White;
            color: Black;
            border-radius:3px;
            padding:5px;
            font-size: 14pt;
            Text-align:left;
            padding-left:10px;
            margin-bottom:10px;
            border:0px;
        }

        QHeaderView::section {
            padding-left: 15px; 
            border: 0px;
        }

        QPushButton#circle{
            background-color: None;
            border: 0px;
        }
    """

    # background - image: url(.. / Interface / img / u_circle.png);
    def __init__(self, parent):
        super(Main4Left, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.shmem = parent.shmem  # <- myform.shmem
        self.parent = parent
        self.setStyleSheet(self.qss)
        self.setFixedWidth(350)
        # 기본 속성
        # self.setMinimumHeight(750)
        # 레이아웃
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 6, 0, 0)
        # print(ab_pro[list(Flag.selected_procedure)[0]]['경보 및 증상'])

        # 변수 받아와야함
        # item_list = ["2.0 경보 및 증상 [3/4]", "3.0 자동 동작 사항 [3/5]", "4.0 긴급 조치 사항 [3/5]", "5.0 후속 조치 사항 [3/5]"]

        # if Flag.call_bottom:
        #     item_list = ["2.0 경보 및 증상 [0/0]", "3.0 자동 동작 사항 [0/0]", "4.0 긴급 조치 사항 [0/0]", "5.0 후속 조치 사항 [0/0]"]
        # print(ab_pro[Flag.call_bottom_name])

        # self.item_list = ""
        #
        # self.btn = []
        #     # for item in item_list:
        #     #     btn.append(QPushButton(item))
        # self.btn.append(QPushButton("2.0"))
        # self.btn.append(QPushButton("3.0"))
        # self.btn.append(QPushButton("4.0"))
        # self.btn.append(QPushButton("5.0"))
        #
        # for cnt in range(4):
        #     self.btn[cnt].setFixedWidth(450)
        #     self.btn[cnt].clicked.connect(partial(self.click, cnt))
        #     self.layout.addWidget(self.btn[cnt])
        # self.layout.addStretch(1)
        # self.setLayout(self.layout)
        self.btn_titles = []
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.button_group.buttonClicked.connect(self.on_button_clicked)

        self.road_name = ""


        # 타이머
        timer1 = QTimer(self)
        timer1.setInterval(300)
        timer1.timeout.connect(self.update_item)
        timer1.start()
        #
        # timer2 = QTimer(self)
        # timer2.setInterval(1)
        # # timer2.timeout.connect(self.color_change)
        # timer2.start()

    # 비정상 절차서 left 업데이트
    def update_item(self):
        # 절차서 이동
        # if Flag.combo_click:
        #     Flag.combo_click = False

        if (Flag.call_bottom_name != "" and Flag.layout_clear_4) or Flag.combo_click_left or Flag.complete_btn:
            if Flag.combo_click_left:
                self.road_name = Flag.combo_click_text
                Flag.call_bottom_name = Flag.combo_click_text
            else:
                self.road_name = Flag.call_bottom_name

            self.item_list = list(
                self.shmem.get_pro_symptom_left(self.road_name))  # [경보 및 증상, 자동 동작 사항, 긴급 조치 사항, 후속 조치 사항]

            self.item_list_count = len(self.item_list)
            self.item_list_num = [0] * self.item_list_count

            # 원
            self.circle_list = []
            for num in range(self.item_list_count):
                if num == 0:
                    self.btn_titles = []

                self.item_list_num[num] = self.shmem.get_pro_symptom_num(self.road_name, self.item_list[num])
                # self.btn.append(SideBtn(num+2, self.item_list[num], Flag.check_count[num], self.item_list_num[num]))
                self.btn_titles.append(QPushButton(
                    "%d.0 %s [%d/%d]" % (num + 2, self.item_list[num], Flag.check_count[num], self.item_list_num[num])))
            if Flag.layout_clear_4 or Flag.combo_click_left or Flag.complete_btn:
                Flag.layout_clear_4 = False
                Flag.combo_click_left = False

                self.clearLayout(self.layout)

                for cnt in range(self.item_list_count):

                    # 왼쪽 레이아웃(수평)
                    self.left_layout = QHBoxLayout(self)
                    self.clearLayout(self.left_layout)
                    self.btn_titles[cnt].setFixedWidth(290)
                    self.btn_titles[cnt].setCheckable(True)
                    self.button_group.addButton(self.btn_titles[cnt], cnt)
                    # self.circle_list[cnt].setFixedWidth(30)
                    # self.circle_list[cnt].setFixedHeight(30)
                    self.circle_list.append(Circle_btn())
                    self.circle_list[cnt].setObjectName("circle")

                    # self.btn_titles[cnt].clicked.connect(partial(self.on_button_clicked, cnt))
                    # self.btn[cnt].clicked.connect(self.clickclick)
                    self.left_layout.addWidget(self.btn_titles[cnt])
                    self.left_layout.addWidget(self.circle_list[cnt])
                    self.layout.addLayout(self.left_layout)

                # if Flag.complete_btn:
                #     self.circle_list[Flag.combo_current].setIcon(QIcon("../Interface/img/c_circle.png"))
                #     Flag.complete_btn = False
                # else:
                #     self.circle_list[Flag.combo_current].setIcon(QIcon("../Interface/img/u_circle.png"))
                self.layout.addStretch(1)
                self.setLayout(self.layout)

                # buttons = [QPushButton(title) for title in self.btn_titles]
        # print(Flag.current_btn)
        # side button paint
        ## 수행 중

        # if Flag.current_btn != -1:
        #     self.btn[Flag.current_btn].setStyleSheet("QPushButton:{background:black;}")

    def on_button_clicked(self, btn):
        # combo_thread = buttoncolor(self)
        # combo_thread.start()
        self.btn_titles[0].setStyleSheet("background:white")
        self.btn_titles[1].setStyleSheet("background:white")
        self.btn_titles[2].setStyleSheet("background:white")
        self.btn_titles[3].setStyleSheet("background:white")
        btn.setStyleSheet("background:rgb(0, 176, 218)")

        Flag.combo_current = self.button_group.checkedId() #현재 체크된 버튼
        Flag.clear_layout_right_4 = True
        Flag.show_right_4 = True
        # btn.setStyleSheet("background:black;")
        # for i in range(4):
        #     if i!=id:
        #         self.btn_titles[i].setStyleSheet("")
        #     self.btn_titles[i].update()
        # print("%d Clicked!"%id)

    def clickclick(self):

        print("클릭했으여")

    def color_change(self):
        print(Flag.current_btn)

    # 레이아웃 초기화
    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # left button click -> right page 정보 띄워줌
    def click(self, btn_num):
        Flag.main2_btn[btn_num] = True
        Flag.current_btn = btn_num
        for i in range(0, 4):
            if i != Flag.current_btn:
                self.btn[i].setStyleSheet('')

        print("클릭함", btn_num)

class Circle_btn(QPushButton):
    def __init__(self):
        super(QPushButton, self).__init__()
        self.setObjectName("circle")
        self.setIcon(QIcon("../Interface/img/u_circle.png"))
        self.setIconSize(QSize(28, 28))


class buttoncolor(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.parent.btn_titles[0].setStyleSheet("background:yellow")
        self.parent.btn_titles[1].setStyleSheet("background:yellow")
        self.parent.btn_titles[2].setStyleSheet("background:yellow")
        self.parent.btn_titles[3].setStyleSheet("background:yellow")
        #
        # self.sleep(1)


class SideBtn(QPushButton):
    qss = """
    QPushButton { background-color: gray; }
    QPushButton:enabled { background-color: green; }

       """

    # (num + 2, self.item_list[num], Flag.check_count[num], self.item_list_num[num])))
    # "%d.0 %s [%d/%d]" %
    def __init__(self, num=None, item_list=None, check_count=None, item_list_num=None):
        super(QPushButton, self).__init__()

        # self.setStyleSheet(self.qss)
        self.setText("%d.0 %s [%d/%d]" % (num, item_list, check_count, item_list_num))
        self.state = False
        # self.setFixedSize(35, 35)
        # self.clicked.connect(self.close)

    def mousePressEvent(self, *args, **kwargs):
        self.state = not self.state
        if self.state:
            self.setStyleSheet('background: #bbffbb;')
        else:
            self.setStyleSheet('')

    def close(self):
        """버튼 명령: 닫기"""
        Flag.main_close = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main4Left()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()
