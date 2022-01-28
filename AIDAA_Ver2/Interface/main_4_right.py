import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver2.Interface import Flag
from AIDAA_Ver2.Procedure.ab_procedure import ab_pro


class Main4Right(QWidget):
    qss = """
        QWidget{
            background: rgb(231, 231, 234);
            margin: 0px;
        }
        QScrollArea{
            border: None;
            border-left-color: rgb(128,128,128);
            border-left-width: 1px;
            border-left-style: solid;
            border-right-color: rgb(128,128,128);
            border-right-width: 1px;
            border-right-style: solid;
        }
        QWidget#scroll{
            background: None;
            border: None;
        }
        QWidget#box1{
            background: rgb(231, 231, 234);
            height:50px;
        }
        QWidget#box2{
            background: white;
            border : 2px solid rgb(190,10,10);
            margin-left: 154px;
            margin-bottom: 10px;
        }
        QWidget#box3{
            background: white;
            border : 2px solid rgb(190,10,10);
            margin-left: 160px;
            margin-bottom: 10px;
        }
        QWidget#main_4_right {
            background: rgb(231, 231, 234);
            border: 1px solid rgb(128,128,128);
            border-radius:5px;
            font-size: 14pt;
            margin:0px;
        }
        QLabel#title{
            background: rgb(128,128,128);
            color: Black;
            border-radius:5px;
            Text-align:left;
            padding-left:10px;
            margin:0px;
            font-size: 14pt;
        }
        
        QLabel#nub{
            background: white;
            color: Black;
            border-radius:5px;
            Text-align:left;
            padding-left:9px;
            font-size: 14pt;
        }
        QLabel#des{
            background: white;
            color: Black;
            Text-align:left;
            padding-left:10px;
            font-size: 14pt;
        }
        QLabel#label_title{
            background: None;
            color: rgb(190,10,10);
            Text-align:center;
            font-size: 14pt;
            font-weight: bold;
        }
        QLabel#label_content{
            background: None;
            color: Black;
            Text-align:left;
            padding-left:10px;
            font-size: 14pt;
        }
        QPushButton#circle{
            background-color: None;
            border: 0px;
        }
        QPushButton#bottom{
            background-color: White;
            border: 0px;
            border-radius:5px;
            margin:0px;
            font-size: 14pt;
        }
        QPushButton#bottom:disabled{
            color: black;
            background-color: rgb(128, 128, 128);
        }
    """

    def __init__(self, parent):
        super(Main4Right, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        # self.setFixedWidth(1450)
        self.shmem = parent.shmem  # <- myform.shmem

        self.parent = parent
        self.setStyleSheet(self.qss)
        self.layout = QHBoxLayout()
        self.layout.addWidget(Main4Right_content(self))
        self.setLayout(self.layout)

class Main4Right_content(QWidget):
    def __init__(self, parent):
        super(Main4Right_content, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        # self.parent = parent
        self.shmem = parent.shmem  # <- myform.shmem

        self.setObjectName("main_4_right")
        # self.setFixedWidth(1500)
        # 기본 속성
        # self.setMinimumHeight(750)

        # 레이아웃
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout_title = QHBoxLayout()
        self.layout_title.setContentsMargins(0, 0, 0, 0)

        self.layout_button = QHBoxLayout()
        self.layout_button.setContentsMargins(20, 0, 20, 5)

        self.title_btn = []
        self.title_item_list = []   # 왼쪽에서 받아와야함

        self.label_list = ["경보 및 증상", "자동 동작 사항", "긴급 조치 사항", "후속 조치 사항"]
        self.pro_num = 0
        self.nub = ""
        self.des = ""
        self.auto = False
        self.man = False

        self.ok = QPushButton("만족")
        self.together = QPushButton("병행")
        self.redo = QPushButton("재수행")
        self.complete = QPushButton("완료")
        self.complete.setDisabled(True)

        self.ok.setObjectName("bottom")
        self.together.setObjectName("bottom")
        self.redo.setObjectName("bottom")
        self.complete.setObjectName("bottom")

        self.ok.setFixedWidth(300)
        self.ok.setFixedHeight(33)
        self.together.setFixedWidth(300)
        self.together.setFixedHeight(33)
        self.redo.setFixedWidth(300)
        self.redo.setFixedHeight(33)
        self.complete.setFixedWidth(300)
        self.complete.setFixedHeight(33)

        self.ok.clicked.connect(self.ok_click)
        self.together.clicked.connect(self.together_click)
        self.redo.clicked.connect(self.redo_click)
        self.complete.clicked.connect(self.complete_click)

        self.layout_button.addWidget(self.ok)
        self.layout_button.addWidget(self.together)
        self.layout_button.addWidget(self.redo)
        self.layout_button.addWidget(self.complete)

        timer1 = QTimer(self)
        timer1.setInterval(300)
        timer1.timeout.connect(self.update_item)
        timer1.start()

    # def resizeEvent(self, event):
    #
    #     self.title_btn[0].resize(self.width()*3/10, 30)
        # self.title_btn[1].resize(self.width()*7/10, 30)

    def ok_click(self):
        self.pro_num = self.shmem.get_pro_symptom_num(Flag.combo_text_final,
                                                      self.label_list[Flag.combo_current])

        for idx in range(self.pro_num):
            ab_pro[Flag.combo_text_final][self.label_list[Flag.combo_current]][idx]['ManClick'] = True
        Flag.ok_btn = True


    def together_click(self):
        pass

    def redo_click(self):
        self.pro_num = self.shmem.get_pro_symptom_num(Flag.combo_text_final,
                                                      self.label_list[Flag.combo_current])

        for idx in range(self.pro_num):
            ab_pro[Flag.combo_text_final][self.label_list[Flag.combo_current]][idx]['ManClick'] = False
        Flag.redo_btn = True


    def complete_click(self):
        Flag.complete_btn = True
        pass

    def update_item(self):
        # 레이아웃 초기화
        if Flag.clear_layout_right_4 or Flag.combo_click_right:
            Flag.clear_layout_right_4 = False
            self.clearLayout(self.layout)
            self.clearLayout(self.layout_title)
            # self.clearLayout(self.layout_content)

        # 화면 업데이트
        if Flag.show_right_4 or Flag.ok_btn or Flag.redo_btn:
            Flag.ok_btn = False
            Flag.redo_btn = False
            if Flag.combo_click_right:
                Flag.combo_click_right = False
                self.road_name = Flag.combo_click_text
            else:
                self.road_name = Flag.call_bottom_name

            Flag.combo_text_final = self.road_name
            # scroll 적용
            self.scrollwidget = QWidget()
            self.scrollwidget.setObjectName("scroll")
            self.layout_content = QVBoxLayout()
            self.layout_content.setContentsMargins(0, 0, 0, 0)

            self.scroll = QScrollArea()
            self.scroll.setFixedHeight(815)
            self.scroll.setWidgetResizable(True)
            self.scroll.setWidget(self.scrollwidget)

            Flag.show_right_4 = False

            self.clearLayout(self.layout)
            self.clearLayout(self.layout_title)
            # self.clearLayout(self.layout_content)
            self.title_btn = []
            self.title_item_list = []  # 왼쪽에서 받아와야함
            if Flag.combo_current == 0:
                self.title_item_list = ["2.0", "경보 및 증상"]
            elif Flag.combo_current == 1:
                self.title_item_list = ["3.0", "자동 동작 사항"]
            elif Flag.combo_current == 2:
                self.title_item_list = ["4.0", "긴급 조치 사항"]
            elif Flag.combo_current == 3:
                self.title_item_list = ["5.0", "후속 조치 사항"]

            for cnt in self.title_item_list:
                self.title_btn.append(QLabel(cnt))
            for cnt in range(len(self.title_item_list)):
                self.title_btn[cnt].setObjectName("title")
                self.layout_title.addWidget(self.title_btn[cnt])
                self.title_btn[cnt].setFixedHeight(33)
            self.title_btn[0].setContentsMargins(0, 0, 10, 0)
            self.title_btn[0].setFixedWidth(100)

            self.title_btn[1].setMaximumWidth(self.width()-100)
            self.layout_title.setContentsMargins(0, 0, 0, 0)
            self.layout.addLayout(self.layout_title)

            # 선택된 절차서 "경보 및 증상"의 내부 단계 레이블 개수 받아오기
            self.pro_num = self.shmem.get_pro_symptom_num(self.road_name,
                                                          self.label_list[Flag.combo_current])  # 9
            self.Manclick_TF = True
            for num in range(self.pro_num):
                self.Manclick_TF = self.Manclick_TF * ab_pro[Flag.combo_text_final][self.label_list[Flag.combo_current]][num]['ManClick']
                if self.Manclick_TF:
                    self.complete.setEnabled(True)
                else:
                    self.complete.setEnabled(False)
                # 내부 단계 레이블 앞단 받아오기
                self.nub = self.shmem.get_pro_symptom_Nub(self.road_name, self.label_list[Flag.combo_current], num)  # 2.x ...
                self.des = self.shmem.get_pro_symptom_all_des(self.road_name, self.label_list[Flag.combo_current], num)  # des
                self.auto = self.shmem.get_pro_symptom_color2(self.road_name, self.label_list[Flag.combo_current], num)
                self.man = self.shmem.get_pro_manclick(self.road_name, self.label_list[Flag.combo_current], num)

                # 주의사항 / 참고사항
                if self.nub == "0.0": # 추후수정
                    self.layout_content.addWidget(Box2(self, self.des))
                elif self.nub == "0.0.0": # 추후수정
                    self.layout_content.addWidget(Box3(self, self.des))
                # 레벨 1 : 2.x ~ 2.xx
                elif len(self.nub) in [3, 4]:
                    self.layout_content.addWidget(Box1(self, self.road_name, self.label_list[Flag.combo_current], num, self.nub, self.des, 1, self.auto, self.man))
                # 레벨 2 : 2.x.x ~ 2.x.xx
                elif len(self.nub) in [5, 6]:
                    self.layout_content.addWidget(Box1(self, self.road_name, self.label_list[Flag.combo_current], num, self.nub, self.des, 50, self.auto, self.man))
                # 레벨 3 : 2.x.x.x ~
                elif len(self.nub) in [7, 8]:
                    self.layout_content.addWidget(Box1(self, self.road_name, self.label_list[Flag.combo_current], num, self.nub, self.des, 100, self.auto, self.man))
                # 레벨 4 : 2.x.x.x.x ~
                elif len(self.nub) in [9, 10]:
                    self.layout_content.addWidget(Box1(self, self.road_name, self.label_list[Flag.combo_current], num, self.nub, self.des, 150, self.auto, self.man))
            self.layout_content.addStretch(1)
            self.scrollwidget.setLayout(self.layout_content)
            self.layout.addWidget(self.scroll)
            self.layout.addStretch(1)

            self.layout.addLayout(self.layout_button)
            self.setLayout(self.layout)


    # 레이아웃 초기화
    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

# Box1
class Box1(QWidget):
    def __init__(self, parent, procedure, name, num, Nub, des, margin, auto, man):
        super(Box1, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.parent = parent
        self.shmem = parent.shmem  # <- myform.shmem
        self.setObjectName("box1")
        self.procedure = procedure
        self.name = name
        self.num = num
        self.Nub = Nub  # x.x
        self.des = des  # des
        self.margin = margin
        self.auto = auto
        self.man = man

        self.blink_thread = Blink(self)


        self.setContentsMargins(self.margin, 0, 0, 15)  # 테두리 겹침 오류
        # self.setFixedWidth(1500)
        # 기본 속성
        # self.setMinimumHeight(750)
        # 레이아웃
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout_nub = QHBoxLayout()
        self.layout_nub.setContentsMargins(0, 0, 0, 0)
        self.layout_nub.setAlignment(Qt.AlignTop)

        self.layout_circle = QHBoxLayout()
        self.layout_circle.setContentsMargins(0, 0, 0, 0)
        self.layout_circle.setAlignment(Qt.AlignTop)

        label_nub = QLabel("%s" % self.Nub)
        label_des = QLabel("%s" % self.des)
        label_nub.setObjectName("nub")
        label_des.setObjectName("des")
        label_nub.setFixedWidth(99)  # - 테두리
        label_nub.setFixedHeight(33)
        label_des.setFixedWidth(1350 - self.margin)
        label_nub.setWordWrap(True)
        label_des.setWordWrap(True)

        self.circle = QPushButton()
        self.circle.setObjectName("circle")
        self.circle.clicked.connect(self.man_click)
        self.circle.setIcon(QIcon("../Interface/img/u_circle.png"))
        self.circle.setIconSize(QSize(30, 30))
        self.circle.setContextMenuPolicy(Qt.CustomContextMenu)
        self.circle.customContextMenuRequested.connect(self.on_context_menu)

        self.popMenu = QMenu(self)
        self.together = QAction('병행', self)
        self.popMenu.addAction(self.together)
        self.together.triggered.connect(self.blink)
        if self.auto:
            label_des.setStyleSheet("background: rgb(0, 176, 218)")

        if self.man:
            ab_pro[self.procedure][self.name][self.num]['ManClick'] = True
            self.circle.setIcon(QIcon("../Interface/img/c_circle.png"))

        self.layout_nub.addWidget(label_nub)
        self.layout.addLayout(self.layout_nub)
        self.layout.addWidget(label_des)
        self.layout_circle.addWidget(self.circle)
        self.layout.addLayout(self.layout_circle)
        # self.layout.setAlignment(Qt.AlignTop)

        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def man_click(self):
        ab_pro[self.procedure][self.name][self.num]['BlinkStart'] = False
        self.blink_thread.quit()
        # if self.man:
        #     ab_pro[self.procedure][self.name][self.num]['ManClick'] = True
        #     self.circle.setIcon(QIcon("../Interface/img/c_circle.png"))

        #운전원 완료버튼 체크



        if ab_pro[self.procedure][self.name][self.num]['ManClick']:
            ab_pro[self.procedure][self.name][self.num]['ManClick'] = False
            # self.parent.complete.setEnabled(False)
            self.circle.setIcon(QIcon("../Interface/img/u_circle.png"))
        else:
            ab_pro[self.procedure][self.name][self.num]['ManClick'] = True
            self.circle.setIcon(QIcon("../Interface/img/c_circle.png"))

        self.pro_num = self.shmem.get_pro_symptom_num(self.procedure, self.name)
        self.Manclick_TF = True
        for idx in range(self.pro_num):
            self.Manclick_TF = self.Manclick_TF * ab_pro[self.procedure][self.name][idx]['ManClick']
        if self.Manclick_TF:
            self.parent.complete.setEnabled(True)
        else:
            self.parent.complete.setEnabled(False)

    def on_context_menu(self, point):
        self.popMenu.exec_(self.circle.mapToGlobal(point))

    def blink(self):
        ab_pro[self.procedure][self.name][self.num]['BlinkStart'] = True
        Flag.blink_manclick = True
        self.blink_thread.start()

class Blink(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        while True:
            if ab_pro[self.parent.procedure][self.parent.name][self.parent.num]['BlinkStart']:
                if ab_pro[self.parent.procedure][self.parent.name][self.parent.num]['Blink']:
                    ab_pro[self.parent.procedure][self.parent.name][self.parent.num]['Blink'] = False
                    self.parent.circle.setIcon(QIcon("../Interface/img/c_circle.png"))
                else:
                    ab_pro[self.parent.procedure][self.parent.name][self.parent.num]['Blink'] = True
                    self.parent.circle.setIcon(QIcon("../Interface/img/u_circle.png"))
            self.sleep(1)

class Box2(QWidget):
    def __init__(self, parent, des):
        super(Box2, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.shmem = parent.shmem  # <- myform.shmem
        self.setObjectName("box2")
        self.des = des  # des
        self.setContentsMargins(0, 5, 0, 5)
        self.setFixedWidth(1490)
        # 레이아웃
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(160, 0, 0, 20)

        # 주의사항 / 참고사항 분리
        label_title = QLabel("%s" % self.des[:4])
        label_content = QLabel("%s" % self.des[7:])
        label_title.setAlignment(Qt.AlignCenter)
        # label_title.setContentsMargins(160, 0, 0, 0)
        label_title.setObjectName("label_title")
        label_content.setObjectName("label_content")
        label_content.setWordWrap(True)
        # label_title.setFixedWidth(800)
        # label_content.setFixedWidth(800)

        # label_nub.setFixedWidth(99)  # - 테두리
        # label_nub.setFixedHeight(33)
        self.layout.addWidget(label_title)
        self.layout.addWidget(label_content)
        # self.layout.setAlignment(Qt.AlignTop)

        self.layout.addStretch(1)
        self.setLayout(self.layout)

class Box3(QWidget):
    def __init__(self, parent, des):
        super(Box3, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.shmem = parent.shmem  # <- myform.shmem
        self.setObjectName("box3")
        self.des = des  # des
        self.setContentsMargins(0, 5, 0, 5)
        self.setFixedWidth(1490)
        # 레이아웃
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(160, 0, 0, 20)

        # 주의사항 / 참고사항 분리
        label_title = QLabel("%s" % self.des[:4])
        label_content = QLabel("%s" % self.des[7:])
        label_title.setAlignment(Qt.AlignCenter)
        # label_title.setContentsMargins(160, 0, 0, 0)
        label_title.setObjectName("label_title")
        label_content.setObjectName("label_content")
        label_content.setWordWrap(True)
        # label_title.setFixedWidth(800)
        # label_content.setFixedWidth(800)

        # label_nub.setFixedWidth(99)  # - 테두리
        # label_nub.setFixedHeight(33)
        self.layout.addWidget(label_title)
        self.layout.addWidget(label_content)
        # self.layout.setAlignment(Qt.AlignTop)

        self.layout.addStretch(1)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main4Right()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()
