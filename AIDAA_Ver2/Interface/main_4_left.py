import sys
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

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
        }
        
        QHeaderView::section {
            padding-left: 15px; 
            border: 0px;
        }
    """

    def __init__(self, parent):
        super(Main4Left, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.shmem = parent.shmem  # <- myform.shmem
        self.parent = parent
        self.setStyleSheet(self.qss)
        # self.setFixedWidth(990)
        # 기본 속성
        # self.setMinimumHeight(750)

        # 레이아웃
        self.layout = QVBoxLayout(self)
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

        # 타이머
        timer1 = QTimer(self)
        timer1.setInterval(1)
        timer1.timeout.connect(self.update_item)
        timer1.start()

    # 비정상 절차서 left 업데이트
    def update_item(self):
        if Flag.call_bottom_name != "":
            self.item_list = list(self.shmem.get_pro_symptom_left(Flag.call_bottom_name))  #[경보 및 증상, 자동 동작 사항, 긴급 조치 사항, 후속 조치 사항]

            self.item_list_count = len(self.item_list)
            self.item_list_num = [0] * self.item_list_count
            self.btn = []
            for num in range(self.item_list_count):
                self.item_list_num[num] = self.shmem.get_pro_symptom_num(Flag.call_bottom_name, self.item_list[num])
                self.btn.append(SideBtn(num+2, self.item_list[num], Flag.check_count[num], self.item_list_num[num]))
                # self.btn.append(QPushButton("%d.0 %s [%d/%d]" % (num+2, self.item_list[num], Flag.check_count[num], self.item_list_num[num])))

            if Flag.layout_clear_4:
                self.clearLayout(self.layout)
                for cnt in range(self.item_list_count):
                    self.btn[cnt].setFixedWidth(450)
                    self.btn[cnt].clicked.connect(partial(self.click, cnt))
                    self.layout.addWidget(self.btn[cnt])
                self.layout.addStretch(1)
                self.setLayout(self.layout)
                Flag.layout_clear_4 = False
        # print(Flag.current_btn)
            # side button paint
            ## 수행 중

        # if Flag.current_btn != -1:
        #     self.btn[Flag.current_btn].setStyleSheet("QPushButton:{background:black;}")



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

class TogglePushButtonWidget(QPushButton):
    """Toggles between on and off text

    Changes color when in on state"""
    def __init__(self, on, off):
        super().__init__()
        self.on = on
        self.off = off
        self.state = True

        # self.rotate_state()
        self.clicked().connect(self.toggle_state)

    def toggle_state(self):
        self.state = not self.state
        if self.state:
            self.setText(self.on)
            self.connect_w.setStyleSheet('background: #bbffbb;')
        else:
            self.setText(self.off)
            self.connect_w.setStyleSheet('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main4Left()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()
