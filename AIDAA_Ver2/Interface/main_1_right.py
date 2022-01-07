import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver2.Interface import Flag
from AIDAA_Ver2.Procedure.ab_procedure import ab_pro


class Main1Right(QWidget):
    qss = """
        QWidget {
            background: rgb(231, 231, 234);
            border: 0px solid rgb(0, 0, 0); 
            font-size: 14pt;
            border-radius: 6px;
        }
        QTableWidget {
            background: rgb(231, 231, 234);
            border: 1px solid rgb(128,128,128);
            border-radius: 6px;
        }
        QHeaderView::section {
            padding-left: 15px; 
            border: 0px;
        }
        QPushButton{
            background: White;
            color: Black;
            border-radius:3px;
        }
        QGroupBox#main  {
            border : 1px solid rgb(128, 128, 128);
            margin-top: 20px;
            margin-left:0px;
            font-size: 14pt;
        }
        
        QGroupBox::title#main  {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 4px 900px 4px 10px;
            background-color: rgb(128, 128, 128);
            color: black;
            font-size: 14pt;       
        }
        QGroupBox#sub1  {
            border : 1px solid rgb(128, 128, 128);
            margin-top:20px;
            font-size: 14pt;
        }
        QGroupBox::title#sub1  {
            subcontrol-origin: margin;
            top: 7px;
            left: 7px;
            padding: 0px 5px 0px 5px;
        }
        QLabel#sub2  {
            margin-top: 3px;
            padding: 5px 0px 0px 0px;
        }
        QTableWidget::item::selected {
            background-color: rgb(0, 176, 218);
        }
        QTableWidget::item {
            padding-left: 15px; 
        }
        QLabel{
            background-color:None;
        }
        QProgressBar{
            border : 1px solid black;
            background-color:rgb(231, 231, 234); 
        }
        QCheckBox::indicator {
                width:  22px;
                height: 22px;
                background-color:rgb(231, 231, 234); 
        }
        QCheckBox::indicator::unchecked {
            width:  22px;
            height: 22px;
            border : 1px solid;
        }
        QCheckBox::indicator::checked {
            image : url(../interface/img/check.png);
            height:22px;
            width:22px;
            border : 1px solid;
        }
        QLabel#symptom{
            border : 0px solid;
            font-size: 12pt;
            border-radius: 6px;
            padding-left: 15px; 
        }
    """

    def __init__(self, parent):
        super(Main1Right, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.shmem = parent.shmem  # <- myform.shmem
        self.W_myform = parent

        self.setStyleSheet(self.qss)
        # self.setFixedWidth(990)
        # 기본 속성
        # self.setMinimumHeight(750)

        # 레이아웃
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        label1 = MainParaArea1(self, self.shmem)
        layout.addWidget(label1)
        label2 = MainParaArea2(self)
        layout.addWidget(label2)
        label3 = MainParaArea3(self, self.shmem)
        layout.addWidget(label3)
        self.setLayout(layout)


class MainParaArea1(QTableWidget):
    def __init__(self, parent, shmem):
        super(MainParaArea1, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.shmem = shmem  # <- myform.shmem
        # 테이블 헤더 모양 정의
        # self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)  # Grid 지우기
        self.setFixedHeight(170)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 테이블 셋업
        col_info = [('비정상 절차서 명', 450), ('긴급 여부', 140), ('진입 조건', 160), ('AI 확신도', 200)]
        self.setColumnCount(4)
        self.setRowCount(5)
        self.horizontalHeader().setFixedHeight(28)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        # self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setContentsMargins(0, 0, 0, 0)

        col_names = []
        for i, (l, w) in enumerate(col_info):
            self.setColumnWidth(i, w)
            col_names.append(l)

        # 테이블 row click
        self.setSelectionBehavior(QTableWidget.SelectRows)

        # 테이블 헤더
        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().setStyleSheet("::section {background: rgb(128, 128, 128);font-size:14pt;border:0px solid;}")
        self.horizontalHeader().sectionPressed.disconnect()
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft and Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 테이블 너비 변경 불가
        self.horizontalHeader().setHighlightSections(False)  # 헤더 font weight 조정

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 28)

        # 테이블 임시 데이터
        self.max_cell = 5
        # self.update_procedure() # 실시간으로 구동해야 IF-THEN Rule이 활성화됨.
        # 클릭 시 하단 비정상절차서 show
        self.cellClicked.connect(self.mouseClick)
        # 더블 클릭 시 절차서 화면 이동
        self.cellDoubleClicked.connect(self.mouseDoubleClick)

        timer1 = QTimer(self)
        timer1.setInterval(500) # 타이머 시간 조정 필요함.
        timer1.timeout.connect(self.update_procedure)
        timer1.start()


    def add_procedure(self, row, name, em, if_prob, ai_prob):
        """
        테이블 임시 데이터 추가

        :param name:        비정상 절차서 명
        :param em:          긴급 여부
        :param if_prob:     진입 조건
        :param ai_prob:     AI 확신도
        """
        item1 = ProcedureNameCell(self, name, row)
        item2 = ProcedureEmCell(self, em, row)
        item3 = ProcedureInfoCell(self, if_prob, row)
        item4 = ProcedureAIProbCell(self, name, ai_prob, row)
        self.setCellWidget(row, 0, item1)
        self.setCellWidget(row, 1, item2)
        self.setCellWidget(row, 2, item3)
        self.setCellWidget(row, 3, item4)

    def update_procedure(self): # 추후 비정상 절차서 이름 앞에 라벨 제거
        '''
        1. 인공지능 출력값 반영 -> 1) 확률, 2) 비정상 절차서 이름 (확률 오름차순 반영)
        2. 각 비정상 절차서 별 요구사항 리스트 반영
        3. IF-THEN rule 반영
        '''
        # 실제 인공지능 결과를 가져와 오름차순 후 테이블 반영 -> 추후 메모리로 값을 받아와야 함.
        global symp_satis
        ai_result = [1.04777455e-03, 1.87130286e-04, 1.96067709e-04, 3.04176280e-04,
                    3.51275333e-04, 4.60391938e-04, 1.85054867e-03, 1.70936875e-04,
                    5.40873585e-04, 8.78681517e-04, 1.25459874e-03, 9.90428406e-01,
                    1.32304912e-03, 8.37134484e-04, 9.51688051e-05, 7.37859320e-05] # 실제 인공지능 결과
        ai_proc = pd.DataFrame(list(enumerate(ai_result))).sort_values(by=1,ascending=False) # 인공지능 결과 전처리
        diagnosis_convert_text = {0: 'Normal: 정상', 1: 'Ab21_01: 가압기 압력 채널 고장 (고)', 2: 'Ab21_02: 가압기 압력 채널 고장 (저)', 3: 'Ab20_04: 가압기 수위 채널 고장 (저)', 4: 'Ab15_07: 증기발생기 수위 채널 고장 (저)', 5: 'Ab15_08: 증기발생기 수위 채널 고장 (고)',
                                  6: 'Ab63_04: 제어봉 낙하', 7: 'Ab63_02: 제어봉의 계속적인 삽입', 8: 'Ab21_12: 가압기 PORV (열림)', 9: 'Ab19_02: 가압기 안전밸브 고장', 10: 'Ab21_11: 가압기 살수밸브 고장 (열림)', 11: 'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설',
                                  12: 'Ab60_02: 재생열교환기 전단부위 파열', 13: 'Ab59_02: 충전수 유량조절밸즈 후단누설', 14: 'Ab23_01: RCS에서 1차기기 냉각수 계통(CCW)으로 누설', 15: 'Ab23_06: 증기발생기 전열관 누설'}
        list_sum = []
        for i in range(len(ai_result)):
            k = []
            for j in range(len(ab_pro[diagnosis_convert_text[int(ai_proc.iloc[i][0])]]["경보 및 증상"])):
                k.append(ab_pro[diagnosis_convert_text[int(ai_proc.iloc[i][0])]]["경보 및 증상"][j]["AutoClick"])
            print(k)
            list_sum.append(sum(k))
        symp_satis = {i:list_sum[i] for i in range(len(ai_result))}
        ai_ref = {i:{'name':diagnosis_convert_text[int(ai_proc.iloc[i][0])], 'em':len(ab_pro[diagnosis_convert_text[int(ai_proc.iloc[i][0])]]['긴급 조치 사항']), 'if_prob':f'{symp_satis[i]}/{self.shmem.get_pro_symptom_count(diagnosis_convert_text[int(ai_proc.iloc[i][0])])}', 'ai_prob':round(ai_proc.iloc[i][1]*100,2)} for i in range(len(ai_result))}
        for i in range(5):
            self.add_procedure(i, ai_ref[i]['name'], ai_ref[i]['em'], ai_ref[i]['if_prob'], ai_ref[i]['ai_prob'])

    def mouseClick(self):
        row = self.currentIndex().row()
        if self.cellWidget(row, 0) is not None:
            Flag.call_bottom_name = self.cellWidget(row, 0).currentText()
            Flag.call_bottom = True

        else:
            Flag.call_bottom_None = True

    def mouseDoubleClick(self):
        row = self.currentIndex().row()

        # set 비정상절차서명
        if self.cellWidget(row, 0) is not None:
            Flag.call_bottom_name = self.cellWidget(row, 0).currentText()
            Flag.call_prss_name = self.cellWidget(row, 0).currentText()
            Flag.call_prss = True
            # 더블클릭 시 리스트에 비정상절차서명 추가
            Flag.combobox_update = True
            Flag.return_list.append(Flag.call_prss_name)
            Flag.layout_clear_4 = True  # main_4_left 버튼 업데이트 위함


    def paintEvent(self, e: QPaintEvent) -> None:
        """ tabelview의 위에 라인 그리기 """
        super(MainParaArea1, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        for i in range(5):
            pen.setColor(QColor(128, 128, 128))         # 가로선 -> 활성화 x color
            pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i*28, 960, i*28)
        qp.restore()

        # self.update_procedure() # QTimer 활용해야 할듯

class ProcedureEmptyCell(QLabel):
    """ 공백 Cell """

    def __init__(self, parent):
        super(ProcedureEmptyCell, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('ProcedureItemEmpty')
        self.isempty = True

class ProcedureBaseCell(QLabel):
    """ 셀 Label 공통 """

    def __init__(self, parent, row):
        super(ProcedureBaseCell, self).__init__(parent=parent)
        # SymXai과 Nonpro 위젯 메모리 주소 받기

        self.procedure_name = ''
        self.row = row


class ProcedureBaseWidget(QWidget):
    """ 셀 Widget 공통 """

    def __init__(self, parent, row):
        super(ProcedureBaseWidget, self).__init__(parent=parent)


        self.procedure_name = ''
        self.row = row

class ProcedureNameCell(ProcedureBaseCell):
    """ 절차서 명 Cell """

    def __init__(self, parent, name, row):
        super(ProcedureNameCell, self).__init__(parent, row)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('ProcedureItemInfo')
        self.isempty = False

        self.procedure_name = name
        self.row = row
        self.setText(name)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

    def currentText(self):
        return self.procedure_name

class ProcedureAIProbCell(ProcedureBaseWidget):
    """ AI 확신도 """

    def __init__(self, parent, name, aiprob, row):
        super(ProcedureAIProbCell, self).__init__(parent, row)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setStyleSheet("background-color:rgba(231, 231, 234, 0); ")
        self.isempty = False

        self.procedure_name = name
        self.row = row

        layer = QHBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)
        layer.setSpacing(5)

        prg_bar = QProgressBar()
        prg_bar.setObjectName('ProcedureItemProgress')
        prg_bar.setValue(aiprob)
        prg_bar.setFixedHeight(20)
        if aiprob <= 50:
            prg_bar.setStyleSheet("QProgressBar::chunk {background-color: rgb(82, 82, 82);}"
                                  "QProgressBar{background-color:rgb(231, 231, 234);}")
        elif aiprob <= 75:
            prg_bar.setStyleSheet("QProgressBar::chunk {background-color: rgb(91, 155, 213);}"
                                  "QProgressBar{background-color:rgb(231, 231, 234);}")
        else:
            prg_bar.setStyleSheet("QProgressBar::chunk {background-color: rgb(190, 10, 10);}"
                                  "QProgressBar{background-color:rgb(231, 231, 234);}")

        prg_bar.setTextVisible(False)

        prg_label = QLabel()
        prg_label.setObjectName('ProcedureItemProgressLabel')
        prg_label.setFixedWidth(45)
        prg_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)  # 텍스트 가운데 정렬
        prg_label.setText(f'{aiprob}%')

        layer.addWidget(prg_bar)
        layer.addWidget(prg_label)

        self.setLayout(layer)

class ProcedureEmCell(ProcedureBaseCell):
    """ 절차서 Em Cell """

    def __init__(self, parent, name, row):
        super(ProcedureEmCell, self).__init__(parent, row)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('ProcedureEm')
        self.isempty = False
        self.setStyleSheet("background-color: rgba(231, 231, 234, 0);")
        layer = QHBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)

        self.checkbox = QCheckBox()
        if name: #긴급
            self.checkbox.setCheckState(Qt.Checked)
        layer.addWidget(self.checkbox)
        self.setLayout(layer)

        self.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)  # 텍스트 가운데 정렬


class ProcedureInfoCell(ProcedureBaseCell):
    """ 절차서 Info Cell """

    def __init__(self, parent, name, row):
        super(ProcedureInfoCell, self).__init__(parent, row)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('ProcedureItemInfo')
        self.isempty = False

        self.procedure_name = name
        self.row = row

        self.setText(name)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)  # 텍스트 가운데 정렬


class MainParaArea2(QTableWidget):
    def __init__(self, parent):
        super(MainParaArea2, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        # 테이블 헤더 모양 정의
        # self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)  # Grid 지우기
        self.setFixedHeight(170)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 테이블 셋업
        col_info = [('System', 550), ('관련 경보', 210), ('AI 확신도', 200)]
        self.setColumnCount(3)
        self.setRowCount(5)
        self.horizontalHeader().setFixedHeight(28)
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


        # 편집 불가
        # self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.setFocusPolicy(Qt.NoFocus)
        # self.setSelectionMode(QAbstractItemView.NoSelection)

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 28)
        self.setRowHeight(self.rowCount()-1, 25)

    def mousePressEvent(self, *args, **kwargs):
        print('Test 시스템 선택 시 화면 전환')
        Flag.call_recv = True
        super(MainParaArea2, self).mousePressEvent(*args, **kwargs)

    def paintEvent(self, e: QPaintEvent) -> None:
        """ tabelview의 위에 라인 그리기 """
        super(MainParaArea2, self).paintEvent(e)

        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        for i in range(5):
            pen.setColor(QColor(128, 128, 128))         # 가로선 -> 활성화 x color
            pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i*28, 960, i*28)
        qp.restore()


# 비정상절차서
class MainParaArea3(QGroupBox):
    def __init__(self, parent, shmem):
        super(MainParaArea3, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.shmem = shmem  # <- myform.shmem
        self.setTitle("비정상절차서:")
        self.setObjectName("main")
        layout = QHBoxLayout()
        self.gb_layout = QVBoxLayout()

        self.gb = QGroupBox("Symptom Check [0/0]")  # 개수 받아와야 함
        self.gb.setObjectName("sub1")
        self.gb.setFixedWidth(600)

        sublayout = QVBoxLayout()
        self.gb2 = QLabel("AI 확신도")
        self.gb2.setObjectName("sub2")
        sublayout.addWidget(self.gb2)
        sublayout.addWidget(MainParaArea3_1(self))

        #테스트
        self.symptom = []

        timer1 = QTimer(self)
        timer1.setInterval(100)
        timer1.timeout.connect(self.check_btn_press)
        timer1.start()

        # if len(self.symptom) != 0:
        #     for i in range(len(self.symptom)):
        #         gb_layout.addWidget(self.symptom[i])
        #
        #         self.symptom[i].setObjectName("symptom")
        # gb_layout.addStretch(1)
        # self.gb.setLayout(gb_layout)

        layout.addWidget(self.gb)
        layout.addLayout(sublayout)
        self.setLayout(layout)

        self.selected_ab = ''

    def check_btn_press(self):
        if Flag.call_bottom:
            self.symptom = []
            self.clearLayout(self.gb_layout)
            self.add_symptom(Flag.call_bottom_name)
            self.setTitle(f"비정상절차서 : {Flag.call_bottom_name}") # 테이블 클릭 시 비정상 절차서 이름을 Title로 반영
            self.selected_ab = Flag.call_bottom_name

            if len(self.symptom) != 0:
                for i in range(len(self.symptom)):
                    self.gb_layout.addWidget(self.symptom[i])

                    self.symptom[i].setObjectName("symptom")
            self.gb_layout.addStretch(1)
            self.gb.setLayout(self.gb_layout)

            Flag.call_bottom = False
            Flag.call_bottom_name = ""

        if Flag.call_bottom_None:
            self.clearLayout(self.gb_layout)
            self.gb.setLayout(self.gb_layout)
            Flag.call_bottom_None = False

        # Symptom Check 숫자 바꾸기.
        if self.selected_ab != '':
            self.symp_satis = []
            for i in range(len(ab_pro[self.selected_ab]['경보 및 증상'])):
                self.symp_satis.append(ab_pro[self.selected_ab]['경보 및 증상'][i]['AutoClick'])
            self.gb.setTitle(f"Symptom Check [{sum(self.symp_satis)}/{len(ab_pro[self.selected_ab]['경보 및 증상'])}]")  # 테이블 클릭 시 비정상 절차서의 "경보 및 증상" 요건의 개수를 반영

    # 레이아웃 초기화
    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def add_symptom(self, title):
        # 일단 label 추가 (Sympotom Check = '경보 및 증상'->'Des')
        aa = self.shmem.get_pro_symptom_count(title)
        for item in range(aa):
            self.symptom_des = self.shmem.get_pro_symptom_des(title, item)
            self.symptom_color = self.shmem.get_pro_symptom_color(title, item) # T/F
            self.symptom.append(QLabel("• %s" % self.symptom_des))
            self.symptom[item].setWordWrap(True)
            self.symptom[item].setFixedHeight(33)
            if len(self.symptom_des) > 55:
                self.symptom[item].setFixedHeight(59)
            if self.symptom_color:
                self.symptom[item].setStyleSheet("background-color : rgb(255,204,0)")
            else:
                self.symptom[item].setStyleSheet("background-color : rgb(178,178,178)")

    def paintEvent(self, e: QPaintEvent) -> None:
        super(MainParaArea3, self).paintEvent(e)
        'paintEvent에서 초마다 변경 안됨, Timer를 활용해야 할 듯함.'
        # # Symptom Check 숫자 바꾸기.
        # if self.selected_ab != '':
        #     self.symp_satis = []
        #     for i in range(len(ab_pro[self.selected_ab]['경보 및 증상'])):
        #         self.symp_satis.append(ab_pro[self.selected_ab]['경보 및 증상'][i]['AutoClick'])
        #     self.gb.setTitle(f"Symptom Check [{sum(self.symp_satis)}/{len(ab_pro[self.selected_ab]['경보 및 증상'])}]")  # 테이블 클릭 시 비정상 절차서의 "경보 및 증상" 요건의 개수를 반영


class MainParaArea3_1(QTableWidget):
    def __init__(self, parent):
        super(MainParaArea3_1, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        # 테이블 헤더 모양 정의
        # self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)  # Row 넘버 숨기기
        self.setShowGrid(False)  # Grid 지우기

        # 테이블 셋업
        col_info = [('변수명', 180), ('기여도', 147)]
        self.setColumnCount(2)
        self.setRowCount(16)
        self.horizontalHeader().setFixedHeight(29)
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


        # 편집 불가
        # self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.setFocusPolicy(Qt.NoFocus)
        # self.setSelectionMode(QAbstractItemView.NoSelection)
        self.para = pd.read_csv('./Final_parameter_200825.csv')['0'].tolist() # 경로 수정
        self.update_shap()

    def paintEvent(self, e: QPaintEvent) -> None:
        """ tabelview의 위에 라인 그리기 """
        super(MainParaArea3_1, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        pen = QPen()
        for i in range(17):
            pen.setColor(QColor(128, 128, 128))         # 가로선 -> 활성화 x color
            pen.setWidth(1)
            qp.setPen(pen)
            qp.drawLine(0, i*29, 960, i*29)
        qp.restore()

    def add_shap(self, row, name, shap_prob):
        '''
        테이블 임시 데이터 추가
        :param name: 변수명
        :param shap_prob: 변수 기여도
        '''
        item1 = ProcedureNameCell(self, name, row)
        item2 = ProcedureInfoCell(self, shap_prob, row) # 추후 수정
        self.setCellWidget(row, 0, item1)
        self.setCellWidget(row, 1, item2)

    def update_shap(self):
        self.shap_result = [np.array([[-3.31006987e-02, -3.36973963e-01, -2.08896416e-03,
                                       -1.61364092e-02, -9.82960399e-02, 6.26495166e-03,
                                       -4.44070779e-02, -6.48119616e-02, -4.90427708e-01,
                                       2.67651661e-02, -6.23174043e-05, -1.22979565e-03,
                                       2.78082854e-03, -1.22665362e-03, -2.97557710e-03,
                                       5.59970449e-03, 5.18632625e-04, 4.32063760e-02,
                                       0.00000000e+00, 0.00000000e+00, -4.13015274e-02,
                                       1.36479878e-05, 1.14105732e-02, 7.73145668e-02,
                                       -1.68455138e-03, 1.97836384e-03, -2.43421214e-04,
                                       1.47793645e-04, 1.17420383e-02, 2.86844622e-03,
                                       0.00000000e+00, -3.56702264e-05, 5.73426946e-04,
                                       5.03701431e-04, 4.23339283e-04, 1.09453827e-03,
                                       -1.25753091e-02, 1.18509295e-01, 4.54298989e-02,
                                       -5.74840383e-03, -6.12061264e-03, 1.45279815e-02,
                                       1.43563007e-02, 1.45052092e-03, 4.02144551e-02,
                                       -1.04266511e-03, 0.00000000e+00, 3.73545560e-04,
                                       3.29724759e-05, 3.17388104e-04, -3.20745039e-04,
                                       -8.94146821e-04, -8.02003608e-03, 3.80658393e-02,
                                       -2.85179777e-05, 2.08126081e-05, -9.04750221e-06,
                                       -1.53522601e-02, 1.08365992e-04, 1.99104710e-03,
                                       6.23581693e-04, 1.55388760e-05, 3.21641789e-05,
                                       4.69279988e-04, 0.00000000e+00, 1.28830123e-03,
                                       -1.37328180e-03, -4.23199665e-06, 1.15863555e-03,
                                       5.87316186e-05, 2.99231684e-04, 3.32217783e-03,
                                       -3.05339269e-03, 1.44195074e-05, 1.02656506e-04,
                                       7.33174805e-05, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, -5.60954260e-05, 2.97488260e-04,
                                       -5.55937955e-06, 1.09061240e-04, 1.10917782e-05,
                                       3.80014256e-04, 0.00000000e+00, 3.83255866e-04,
                                       1.71437752e-04, 0.00000000e+00, 8.47261473e-04,
                                       0.00000000e+00, 0.00000000e+00, 1.26497248e-04,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       -2.88313070e-06, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       2.05106442e-06, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, -4.73099759e-07, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[-3.59905967e-04, 4.04950169e-01, 3.16002794e-02,
                                       9.95240944e-03, -5.13614283e-02, 1.70428073e-01,
                                       -1.53205126e-02, 4.29334915e-02, -1.85516884e-03,
                                       6.25025174e-02, 9.68163380e-02, 2.23383726e-03,
                                       -3.62161749e-03, -1.10279027e-01, 8.26443710e-04,
                                       9.74749995e-04, 6.63383313e-04, -1.02020484e-02,
                                       -4.93212842e-02, 0.00000000e+00, 1.25346257e-02,
                                       -5.77789077e-02, 9.53588547e-04, -8.33381911e-04,
                                       1.10498762e-03, -9.12585292e-03, 4.04124512e-03,
                                       -2.14701763e-02, -1.02211358e-03, -2.39700051e-05,
                                       0.00000000e+00, -8.88284126e-04, -1.33033417e-03,
                                       -9.57758545e-03, 6.92371091e-04, 1.01431047e-03,
                                       -3.93305899e-02, -3.34089006e-05, 1.26159716e-05,
                                       -8.87748182e-04, 1.56294119e-04, -8.01909919e-05,
                                       1.47398810e-05, 3.09761107e-02, 1.12713016e-04,
                                       -9.29629885e-04, -2.41392523e-06, 1.95141395e-02,
                                       3.39930430e-06, 9.77955831e-06, 1.69055315e-06,
                                       4.09789537e-03, 3.20737502e-06, 0.00000000e+00,
                                       3.58302071e-04, 1.57930496e-05, -1.20298031e-06,
                                       -2.92839043e-04, 1.59873251e-05, 5.69704212e-05,
                                       2.60482087e-06, 2.06656529e-02, -1.76414914e-06,
                                       -1.85643381e-05, 0.00000000e+00, -1.24487255e-05,
                                       3.85721401e-02, 1.71893426e-04, 5.32616778e-06,
                                       6.18944244e-07, 3.50766566e-06, -6.79310522e-04,
                                       -6.82379173e-04, -8.55397483e-06, -1.37790616e-03,
                                       -2.81545709e-02, 6.18589260e-08, 0.00000000e+00,
                                       0.00000000e+00, -4.52951054e-06, 2.13617398e-05,
                                       -2.72887703e-02, -8.38172216e-06, -1.65117454e-06,
                                       -6.32554304e-08, 0.00000000e+00, -1.13197410e-07,
                                       6.44996933e-06, -1.13029335e-08, -4.78308137e-05,
                                       0.00000000e+00, 0.00000000e+00, -1.16441125e-01,
                                       -1.43775216e-05, -5.15920377e-07, -2.45674923e-08,
                                       0.00000000e+00, 0.00000000e+00, 1.63961459e-07,
                                       1.19726425e-02, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       2.69206149e-06, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[-2.34547810e-02, 1.06596325e-01, 1.33060139e-03,
                                       7.96083845e-03, -4.02365175e-03, 6.53387530e-03,
                                       2.88355466e-01, 1.16048461e-03, -2.15418487e-04,
                                       -1.07192095e+00, -3.28965229e-05, 1.26166880e-01,
                                       4.34805797e-02, 1.02527565e-02, 3.35106163e-05,
                                       6.87120425e-04, 1.02754035e-03, 6.53096542e-02,
                                       -4.45971791e-05, 0.00000000e+00, -8.25498482e-05,
                                       -1.52325531e-04, -5.52678892e-04, 4.86726388e-02,
                                       2.07683114e-03, 8.32009050e-05, 5.89985241e-04,
                                       4.06274150e-03, 2.36039976e-03, -1.94825064e-05,
                                       4.58400929e-03, -6.24583839e-03, 2.11402413e-03,
                                       1.83180700e-03, -3.46504521e-06, -8.39391495e-06,
                                       1.13879328e-03, -1.26850015e-03, 3.36631268e-04,
                                       -3.17565907e-05, -2.04832394e-06, 3.13432797e-04,
                                       -9.01636111e-03, 4.00480222e-05, 6.51903944e-02,
                                       2.74724426e-02, 9.34630488e-03, 1.12568345e-03,
                                       2.36351473e-02, 1.18628471e-03, -5.54913026e-06,
                                       3.92857915e-03, 1.30201983e-05, 2.62114540e-03,
                                       3.96786847e-04, -8.09640904e-07, -1.17643649e-06,
                                       1.53743278e-04, 4.36401739e-04, -1.10095072e-04,
                                       8.46704132e-04, 2.56898617e-05, -1.59383539e-05,
                                       -4.08961085e-04, 5.16254718e-03, 4.40821051e-05,
                                       3.13834172e-04, 2.84660357e-03, 1.77596040e-04,
                                       -8.40127473e-05, -1.18042059e-05, 7.88521954e-06,
                                       8.01452433e-06, -3.38204263e-04, -1.68709126e-06,
                                       1.77971138e-05, 2.86450735e-04, 0.00000000e+00,
                                       0.00000000e+00, -9.04211081e-06, 2.67471223e-04,
                                       3.78639304e-06, 2.45493857e-06, 2.71948019e-04,
                                       -6.12070815e-07, 0.00000000e+00, 7.78778523e-04,
                                       2.81395034e-04, 0.00000000e+00, -3.16602615e-07,
                                       5.87776793e-06, 1.28520853e-02, -2.05062254e-03,
                                       6.40228902e-05, 0.00000000e+00, -4.79301149e-06,
                                       0.00000000e+00, 0.00000000e+00, -2.70397524e-03,
                                       -1.16831735e-04, 0.00000000e+00, 7.09706645e-09,
                                       0.00000000e+00, 0.00000000e+00, 1.39190031e-05,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       -3.46741018e-05, 0.00000000e+00, -3.66872573e-03,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[3.97074712e-06, -5.88824900e-04, 3.89384368e-02,
                                       -1.11320663e-02, -2.60055427e-03, -1.39794781e-03,
                                       4.89294438e-04, -1.96446806e-01, 1.75714901e-03,
                                       4.23126864e-03, 3.81254070e-05, -2.66162342e-06,
                                       2.02041845e-04, 7.10084702e-05, 3.75939610e-04,
                                       -2.68689782e-04, 1.04437708e-03, 2.40454794e-06,
                                       -2.78842921e-06, 2.19030829e-04, -2.23608946e-04,
                                       -2.40291236e-05, 1.08676693e-05, -6.53077187e-07,
                                       3.47699405e-06, -1.71147231e-04, 2.70855291e-04,
                                       1.64538373e-03, -4.65909357e-05, 3.56115934e-06,
                                       0.00000000e+00, 1.07169389e-04, -6.70121515e-05,
                                       -1.82569208e-05, 1.47641385e-05, -8.16219655e-06,
                                       -1.69845733e-06, -5.70466175e-05, 5.62028818e-07,
                                       -1.17361340e-07, 1.74968673e-04, -4.03428009e-05,
                                       -2.20699269e-06, -3.86508931e-05, 2.52750969e-06,
                                       -6.42242047e-05, 2.06702236e-04, -4.36198366e-06,
                                       -4.01606476e-07, -9.83285473e-05, 1.11723134e-04,
                                       -5.76323371e-05, -1.24303746e-07, -3.25319274e-10,
                                       9.92046261e-05, -7.58324142e-05, -7.38651405e-05,
                                       -3.36709486e-05, -1.96136250e-06, -1.58920558e-05,
                                       -2.77125222e-06, -1.87138840e-06, -4.40341954e-07,
                                       7.05562602e-09, 0.00000000e+00, -3.66795095e-05,
                                       2.58176874e-06, -2.25711121e-03, 7.75311618e-06,
                                       8.21619852e-06, -4.62286618e-09, 2.00472600e-06,
                                       -2.56284514e-06, -2.91635471e-05, 5.56179300e-07,
                                       2.40876664e-05, -2.80728439e-10, -5.70099966e-09,
                                       -1.29416559e-07, -9.64056044e-09, 2.82965795e-07,
                                       3.41008849e-07, 1.95734322e-05, -5.69449806e-07,
                                       -2.77369853e-07, 1.85139896e-09, -8.82116706e-05,
                                       -4.70684007e-07, 2.50746044e-04, -1.39955899e-05,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       -9.25876850e-07, 0.00000000e+00, 0.00000000e+00,
                                       -4.81205336e-09, 3.96994627e-06, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 2.97774457e-04,
                                       0.00000000e+00, 2.49428377e-05, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[6.22454476e-03, -1.96038861e-03, 2.86995450e-02,
                                       -1.35947753e-05, 4.84033670e-04, -1.22484272e-03,
                                       -4.65447014e-04, -4.49042455e-04, 1.14820177e-03,
                                       -3.64764182e-05, 2.38006500e-04, 1.96827871e-06,
                                       -4.24334988e-04, 3.18096964e-07, -5.48080061e-05,
                                       4.68084346e-05, -1.65073101e-04, -1.08974685e-05,
                                       -1.18963191e-06, 4.96577662e-05, -3.52274945e-04,
                                       -3.03025555e-05, -2.35166973e-04, -3.85280531e-07,
                                       7.15626161e-07, -2.97396739e-04, 1.05119939e-05,
                                       6.67229096e-04, -6.32225379e-06, 8.43085879e-06,
                                       0.00000000e+00, 1.59448868e-04, 4.23904508e-05,
                                       3.88600799e-05, 5.23443344e-08, -7.46184881e-07,
                                       -3.16303842e-05, -1.71584129e-07, -1.12494953e-04,
                                       -3.67614878e-03, 4.62616407e-06, -3.75508647e-05,
                                       2.67789490e-06, -9.92561846e-07, -1.90335882e-05,
                                       -7.35376568e-06, 0.00000000e+00, -1.39174919e-05,
                                       -1.50788540e-06, 1.13634018e-04, -6.92042767e-07,
                                       1.84553931e-06, -3.15995679e-01, -1.05171833e-06,
                                       -7.73370106e-09, -6.92207360e-05, -2.27898109e-05,
                                       -1.65177181e-04, 3.74199738e-06, -9.66860868e-05,
                                       1.94196051e-07, -8.46130547e-06, -2.40554742e-06,
                                       6.51381094e-07, 0.00000000e+00, -4.93310366e-05,
                                       2.02336553e-06, -2.97432743e-06, -1.90962284e-05,
                                       -1.02938907e-05, 9.97258556e-08, 4.46898063e-06,
                                       -1.62660317e-05, 7.02279166e-06, 8.49535455e-07,
                                       -7.22317237e-07, -6.77977572e-05, -5.15740116e-09,
                                       3.33124282e-07, -1.28477958e-08, -3.95807687e-06,
                                       -3.09984891e-07, -4.97147099e-07, 1.85332475e-06,
                                       1.34860690e-05, 0.00000000e+00, -3.47358049e-07,
                                       1.68630651e-07, 0.00000000e+00, -2.78387688e-05,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       -1.65514404e-06, 0.00000000e+00, -1.79344795e-04,
                                       -5.60809913e-08, 2.50460292e-05, 0.00000000e+00,
                                       -3.19690621e-09, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[2.78430319e-03, -9.31653716e-03, -1.16546753e-06,
                                       5.61365827e-05, 5.95430032e-05, -1.48844084e-03,
                                       3.66372171e-06, -7.80716638e-05, 1.01783182e-03,
                                       9.65294684e-04, 1.51811707e-05, -1.02067912e-06,
                                       -3.86931789e-04, -1.71111259e-06, 1.25840143e-03,
                                       1.95481889e-03, -2.00157162e-04, 3.95310605e-06,
                                       0.00000000e+00, 7.00599103e-05, 3.51349507e-04,
                                       -1.30518616e-05, 8.69533443e-06, 4.66743140e-04,
                                       -2.43565751e-06, -5.12842200e-04, -2.06342681e-04,
                                       9.15223285e-06, -1.01980824e-04, 1.66793414e-06,
                                       0.00000000e+00, 3.80733683e-04, -8.23480491e-03,
                                       -8.90322056e-05, -2.09482317e-05, 1.39143182e-06,
                                       7.77571522e-07, -1.65784517e-04, 3.08302068e-07,
                                       1.49529529e-06, -3.57575726e-01, -3.20222916e-06,
                                       2.81727885e-07, 5.63757365e-06, -7.43933345e-08,
                                       -3.88521527e-06, -2.30745474e-07, -9.46308778e-06,
                                       -2.76377140e-07, 1.82254620e-05, 2.87645049e-04,
                                       -6.02606673e-05, -9.15206491e-06, -4.45257798e-06,
                                       1.65534772e-09, -1.14514181e-04, 1.58977141e-07,
                                       -4.59439839e-07, 4.06927812e-06, -2.58645043e-04,
                                       -6.43988942e-06, -6.52094719e-05, 4.17298752e-05,
                                       -3.45911483e-06, 0.00000000e+00, -3.25081544e-06,
                                       3.27056038e-06, -1.84348083e-06, 8.88962306e-06,
                                       -2.62075636e-06, -2.45393599e-06, 3.86427966e-06,
                                       4.46697081e-07, -8.37737340e-06, -1.73525433e-06,
                                       -1.69569915e-05, -1.65130254e-10, -1.39306792e-06,
                                       0.00000000e+00, -6.81824859e-07, -1.15639356e-06,
                                       -3.86289473e-05, -9.35429657e-05, -8.55734848e-05,
                                       -1.35477581e-06, 0.00000000e+00, -1.11306218e-07,
                                       -8.82138307e-07, 0.00000000e+00, -6.04646191e-06,
                                       0.00000000e+00, 7.89292314e-08, 0.00000000e+00,
                                       -7.06201109e-06, 0.00000000e+00, 0.00000000e+00,
                                       -2.64726328e-08, 0.00000000e+00, 0.00000000e+00,
                                       4.98711905e-07, 0.00000000e+00, -8.21909945e-08,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[3.64952102e-03, -7.25455084e-04, -1.05270098e-04,
                                       2.27605645e-03, 4.01031612e-03, -5.24345074e-03,
                                       3.74925194e-02, 2.13062340e-04, 5.38327099e-03,
                                       1.35277069e-02, 1.06912004e-05, 7.59247090e-03,
                                       -1.49351980e-01, -2.39454977e-04, -1.49196597e-01,
                                       8.09980446e-04, 2.39067437e-06, 4.77492052e-04,
                                       0.00000000e+00, 1.76732111e-03, 1.18286821e-03,
                                       -6.11262712e-05, 1.17088746e-02, 3.19639615e-04,
                                       -7.17893080e-04, 4.38435762e-03, -8.97417287e-05,
                                       2.08011216e-05, -2.37158275e-04, 7.36222405e-05,
                                       0.00000000e+00, 1.93946487e-03, -2.25205230e-04,
                                       -4.90205079e-04, -2.18272968e-04, -2.65451323e-03,
                                       4.02821757e-04, -1.34403974e-04, -2.78437683e-03,
                                       5.26556481e-04, 3.08057158e-05, -1.32791138e-04,
                                       1.11075799e-05, 3.46712849e-03, 1.59010446e-01,
                                       1.24313465e-04, 5.62455288e-02, -4.17685075e-02,
                                       -1.70221507e-01, -1.99870805e-04, 1.94750279e-04,
                                       -7.27649321e-01, -8.93321814e-06, 0.00000000e+00,
                                       1.62499949e-03, 1.74939660e-03, 2.76693906e-02,
                                       3.11916450e-04, 1.03176657e-05, -8.72500248e-02,
                                       -1.95508626e-03, 7.55452831e-05, 9.17981501e-04,
                                       1.52720947e-03, 0.00000000e+00, 2.38638971e-04,
                                       -2.59255008e-02, 2.03745485e-04, 1.19964845e-05,
                                       -9.49615088e-05, 9.69773917e-05, -2.14655273e-05,
                                       2.17686378e-04, 1.86028858e-03, 7.74591054e-06,
                                       -3.10619352e-05, -1.14907792e-05, 0.00000000e+00,
                                       -6.17740540e-06, 1.00375138e-05, 7.01843538e-04,
                                       -3.42844205e-07, -1.14998065e-04, 1.09845365e-03,
                                       -1.50063067e-02, 0.00000000e+00, -3.73023960e-05,
                                       3.01621669e-04, 0.00000000e+00, -3.60326539e-05,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 3.72333461e-05,
                                       2.81808362e-04, 6.64910878e-05, 0.00000000e+00,
                                       0.00000000e+00, 1.32253274e-04, 4.07084523e-05,
                                       0.00000000e+00, -2.28664672e-05, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 2.04716383e-04,
                                       -3.33538942e-06, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 2.08681554e-07, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[9.92789036e-03, 5.25041595e-02, 9.74924673e-05,
                                       -1.17428767e-04, -5.40648278e-02, 9.10718606e-04,
                                       2.43081268e-02, -7.32045010e-03, 7.55862602e-05,
                                       -1.85446302e-02, 1.94844238e-05, -8.09867726e-02,
                                       -1.85757382e-01, -3.90382969e-04, 2.89977477e-02,
                                       1.01135123e-04, 1.21703688e-02, 8.24503053e-05,
                                       0.00000000e+00, 0.00000000e+00, 1.08429718e-03,
                                       0.00000000e+00, 3.53204536e-04, -1.07736346e-05,
                                       3.62816851e-03, -3.74436361e-04, 1.52950461e-03,
                                       -5.37373797e-06, -4.88538719e-02, -8.10926630e-03,
                                       0.00000000e+00, -8.86984681e-04, 4.25123251e-04,
                                       1.41475261e-03, 3.84234524e-03, -1.81988353e-05,
                                       1.26032865e-02, -9.72087297e-03, 2.01863645e-03,
                                       2.14637716e-05, -1.69184313e-04, 5.81523345e-04,
                                       8.74373810e-03, 2.26733887e-03, 8.92543203e-05,
                                       -4.82054087e-05, 1.28446715e-02, 3.77613755e-03,
                                       9.61136560e-03, -2.34601592e-04, 3.10649543e-02,
                                       2.83321769e-05, 3.75579655e-04, 0.00000000e+00,
                                       2.82913752e-04, 2.55402071e-05, 1.17057292e-03,
                                       -2.64638001e-04, 6.93740688e-04, 2.33497247e-04,
                                       -1.41735734e-05, 1.03066048e-04, -6.16435173e-03,
                                       9.52800930e-05, 0.00000000e+00, 8.48660896e-04,
                                       2.26775543e-04, -3.52393403e-07, -5.29510262e-04,
                                       -7.80267751e-05, -7.35404449e-03, -2.10127907e-03,
                                       9.73213861e-04, -1.04585531e-05, 4.64463954e-04,
                                       -8.22817644e-05, -7.26805853e-04, 0.00000000e+00,
                                       0.00000000e+00, 6.40682476e-05, 6.58655194e-06,
                                       -8.21422347e-06, 9.66482830e-05, -3.59074613e-05,
                                       -8.81492839e-07, 0.00000000e+00, 3.10991530e-05,
                                       5.76064825e-06, 0.00000000e+00, -4.29245348e-06,
                                       0.00000000e+00, -3.19167278e-08, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, -2.60617775e-05,
                                       -4.92003755e-05, 0.00000000e+00, 0.00000000e+00,
                                       -3.28611980e-06, -4.65659823e-02, 6.87691895e-04,
                                       0.00000000e+00, -1.24855881e-04, -6.52349041e-08,
                                       0.00000000e+00, 0.00000000e+00, 5.52485731e-04,
                                       -1.03379191e-04, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, -4.74390430e-05, 0.00000000e+00,
                                       6.15613472e-08, 0.00000000e+00, 0.00000000e+00,
                                       1.16160987e-08, 0.00000000e+00, -2.00706620e-07,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[-9.88364049e-05, -3.12084825e-03, 5.18723458e-05,
                                       1.81861452e-04, 7.17969802e-04, -6.11028035e-03,
                                       -2.74717451e-06, -6.90766559e-04, 2.14124079e-03,
                                       -5.04888751e-03, 1.82599705e-05, 1.80920606e-06,
                                       -4.57566021e-04, 8.29661300e-07, -5.33996465e-05,
                                       2.34831907e-04, -1.48308240e-04, 6.09432000e-04,
                                       0.00000000e+00, 1.47000146e-04, -5.36097399e-04,
                                       -2.87677805e-05, 2.88305327e-05, -2.60945550e-07,
                                       6.24972222e-05, -3.13696298e-04, 5.68007262e-05,
                                       7.19021086e-06, -1.12378406e-04, 5.34015656e-06,
                                       -3.87856278e-01, 4.70949828e-04, -2.34475183e-05,
                                       -5.60973951e-05, 1.39124520e-05, 4.26549651e-06,
                                       -1.51411027e-05, -7.91696225e-05, 2.92748402e-06,
                                       1.89360556e-08, 5.63298717e-06, -6.02336313e-05,
                                       -4.47501819e-06, -5.32258077e-05, -6.06782431e-04,
                                       2.54980566e-06, -8.92034979e-08, -5.84079333e-06,
                                       -2.98899438e-06, -9.88924126e-06, 5.75131414e-06,
                                       -9.50846393e-05, -3.26830145e-06, 2.25450605e-06,
                                       6.39085369e-07, -1.43858730e-04, -2.51818455e-04,
                                       -4.25833318e-05, 4.91192286e-06, -1.14077661e-04,
                                       -1.30468836e-03, -5.28240438e-06, 1.45394113e-05,
                                       1.77610121e-06, 0.00000000e+00, -6.52556525e-05,
                                       -3.19410521e-05, -3.02584974e-06, -1.95958472e-05,
                                       -9.25635605e-05, 0.00000000e+00, 7.61419919e-06,
                                       -6.63276934e-06, -5.95078166e-05, 3.46992128e-07,
                                       1.65357904e-07, -4.57972382e-09, -7.75750834e-09,
                                       3.32990157e-08, -8.51547516e-06, 8.08561767e-08,
                                       -2.08374253e-07, -1.38441994e-05, -1.03140833e-06,
                                       -1.53882801e-08, 0.00000000e+00, -8.28466303e-05,
                                       -7.37358940e-05, 3.42066950e-09, -1.27581678e-05,
                                       4.80545414e-09, 5.59469884e-06, 0.00000000e+00,
                                       4.65780263e-05, -7.77942367e-09, 1.39527653e-07,
                                       -2.80598234e-09, 1.81064713e-06, 0.00000000e+00,
                                       -5.94543529e-08, 0.00000000e+00, 4.80746879e-09,
                                       1.27305967e-07, -2.71843705e-08, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, -1.27022057e-08,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[-7.68799156e-04, 4.12445507e-03, -5.53701153e-03,
                                       -1.18825982e-03, 9.28851993e-04, -5.77427833e-04,
                                       -4.75875054e-04, -4.50215523e-04, 9.05794846e-04,
                                       7.10965466e-04, -1.59829952e-04, 5.99719035e-07,
                                       -1.37112363e-04, 2.85152388e-05, 2.79182822e-04,
                                       -1.05642681e-02, 5.58964252e-05, 2.09139329e-06,
                                       9.46640610e-08, 1.82517123e-04, -1.27469701e-03,
                                       -6.14588001e-05, 3.32050469e-05, 3.25044976e-04,
                                       -5.47141489e-06, -9.18075048e-05, 6.60079620e-05,
                                       6.17522132e-05, -2.30716546e-04, -1.12161827e-05,
                                       0.00000000e+00, 1.30545935e-04, -3.58552085e-04,
                                       -8.68644556e-04, 4.00326504e-06, -2.09947207e-04,
                                       4.42848984e-04, -6.81517701e-04, 4.57520419e-07,
                                       3.95873661e-06, -2.52289438e-09, -5.19126002e-05,
                                       -2.49984980e-06, -1.93770507e-07, -7.03581899e-04,
                                       -6.45470067e-05, 1.63127075e-07, -4.47624882e-06,
                                       -8.78250377e-06, 2.71687118e-05, 3.20918849e-05,
                                       -1.90331543e-04, 1.05738181e-07, -1.50357353e-04,
                                       -1.47050038e-05, -6.75255097e-05, -1.21708801e-03,
                                       -1.24026714e-07, 8.14612734e-03, -8.56313242e-05,
                                       -1.35225503e-03, 1.50594141e-06, -2.32097598e-06,
                                       -2.31745127e-04, -2.93581353e-01, -4.62270046e-04,
                                       -2.74016524e-05, -7.44384796e-09, -1.25554902e-04,
                                       -1.13778530e-05, 0.00000000e+00, 1.05235855e-06,
                                       -1.73828428e-08, 2.76513690e-05, -5.64321671e-03,
                                       1.54186735e-07, 9.68091079e-09, -5.34927830e-09,
                                       3.04627892e-08, 9.08207536e-09, -3.03777045e-06,
                                       -3.95795315e-07, 1.56499808e-06, 1.07097524e-06,
                                       2.54284045e-05, 0.00000000e+00, -3.64196946e-05,
                                       -3.98735452e-07, 0.00000000e+00, -3.63804413e-04,
                                       0.00000000e+00, -8.36701736e-04, 0.00000000e+00,
                                       -1.08949615e-05, 0.00000000e+00, 0.00000000e+00,
                                       -1.30139666e-07, 4.47000983e-05, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 2.78045198e-09,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       -4.07801157e-09, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[9.70815796e-03, -2.26652493e-02, 2.89948112e-03,
                                       2.14404825e-03, 1.64974281e-03, -3.16870826e-02,
                                       1.13688421e-04, -2.63910791e-04, 5.33776190e-03,
                                       3.34697806e-02, -4.32429968e-06, 6.06609221e-07,
                                       -1.08345764e-03, -3.54092027e-02, -1.76226364e-05,
                                       3.74555738e-04, -1.50441570e-06, 5.66440589e-03,
                                       3.47073057e-03, 1.74913612e-03, -4.43998887e-05,
                                       -5.88056544e-01, 1.10229142e-04, 8.73749901e-04,
                                       -5.71344911e-04, -2.49445884e-04, 3.22413345e-04,
                                       6.56091087e-04, -4.54218256e-04, 8.00969290e-06,
                                       0.00000000e+00, 1.05741729e-03, 1.26998178e-04,
                                       -9.74814526e-05, -4.54633161e-07, -4.37730656e-05,
                                       2.71461637e-07, -2.87166110e-04, -4.86799223e-04,
                                       -3.75712377e-05, 4.91104880e-06, -2.50138518e-03,
                                       1.16203033e-05, -5.49752578e-04, 6.29914297e-06,
                                       -6.85415569e-06, 1.37090145e-03, -4.14376608e-08,
                                       4.25500664e-06, -4.36240993e-05, 2.73977557e-05,
                                       -5.24569599e-06, 8.05666795e-08, 1.89623384e-03,
                                       -4.18823162e-06, -8.79894828e-05, 1.76112440e-06,
                                       2.37821062e-06, 1.33090409e-06, -1.83363508e-04,
                                       -2.02506887e-04, -2.48711981e-05, 2.34968148e-05,
                                       -1.30902009e-06, 0.00000000e+00, -1.39465996e-03,
                                       1.76887765e-06, -6.70680976e-06, 1.18023127e-05,
                                       -8.97259790e-07, -2.03054398e-04, 6.47220463e-06,
                                       0.00000000e+00, 2.68140815e-06, 3.84263924e-06,
                                       -7.71490213e-09, -2.76705015e-09, -2.30878715e-08,
                                       -5.03230712e-07, -2.00254189e-05, -3.33515707e-08,
                                       -1.68061331e-05, -4.13705129e-05, -5.86731746e-06,
                                       -4.88919890e-08, 0.00000000e+00, -2.07100292e-04,
                                       3.34429096e-08, -2.00015981e-04, 1.07103680e-06,
                                       7.23766825e-04, 0.00000000e+00, 6.20643294e-07,
                                       2.96548094e-08, -2.42054740e-04, -1.92509770e-05,
                                       -2.12933168e-07, 0.00000000e+00, 1.57804370e-03,
                                       0.00000000e+00, 0.00000000e+00, -3.70037524e-07,
                                       0.00000000e+00, -2.04364454e-07, 0.00000000e+00,
                                       -2.06756671e-06, -1.44716565e-04, -2.31379826e-07,
                                       0.00000000e+00, -3.94026286e-06, -2.15074243e-08,
                                       -4.37932646e-04, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       -1.35181646e-07, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       -6.41771244e-07, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[2.70393827e+00, 4.12832177e-03, 1.24132158e-02,
                                       -8.85188760e-02, 9.23488552e-04, -2.40031352e-03,
                                       0.00000000e+00, 6.51155194e-01, 2.33145599e+00,
                                       -5.84416886e-03, -6.53809083e-03, -1.03507435e-03,
                                       1.76285407e-02, 7.50393193e-03, 5.27574170e-03,
                                       -1.17516034e-03, 2.39549600e-04, -3.03921218e-04,
                                       3.57435646e-02, -9.82619167e-02, 7.74199553e-04,
                                       -3.77884829e-02, -6.15181819e-03, -1.82175784e-03,
                                       3.78516115e-03, 9.49197237e-02, -2.90624561e-04,
                                       -1.48525562e-05, -6.14277620e-05, -5.78956603e-02,
                                       0.00000000e+00, 4.25951576e-04, -1.30656930e-02,
                                       6.07653819e-03, -1.01198504e-03, -3.14638532e-03,
                                       -3.59996426e-03, -2.83394868e-03, 5.14222456e-04,
                                       -5.98149478e-05, -6.67933389e-03, -1.08309962e-03,
                                       1.25216258e-01, 0.00000000e+00, -3.99123698e-02,
                                       -3.54685146e-03, 0.00000000e+00, -1.41786101e-03,
                                       0.00000000e+00, 6.32649731e-05, -9.31149941e-05,
                                       -1.38388535e-05, -1.79035233e-04, 0.00000000e+00,
                                       2.34647387e-02, -3.74456247e-05, -2.80249145e-05,
                                       2.79700085e-05, 3.09977058e-03, -3.03468249e-03,
                                       -3.26764672e-04, -2.04558307e-04, 6.14432832e-03,
                                       0.00000000e+00, 0.00000000e+00, 1.11364882e-04,
                                       -3.42770090e-05, -5.15528788e-03, -1.06287398e-03,
                                       -6.52142047e-04, 0.00000000e+00, 6.23979282e-03,
                                       8.02074309e-06, 2.04095312e-03, 0.00000000e+00,
                                       -6.72545079e-05, 0.00000000e+00, 0.00000000e+00,
                                       -2.61399570e-02, 0.00000000e+00, -4.32875419e-04,
                                       -1.39606900e-05, -4.08868292e-05, -1.92913221e-05,
                                       8.28953665e-05, -8.57251709e-04, 2.20653945e-05,
                                       -2.74922078e-05, 0.00000000e+00, -1.50277158e-04,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, -3.65463642e-02, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       -6.71156050e-04, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[-1.23863045e+00, -4.72133064e-04, 4.31599465e-03,
                                       5.37851548e-02, 5.26744617e-04, 8.73517765e-04,
                                       0.00000000e+00, 2.15659734e-01, 5.84149864e-04,
                                       8.10871156e-04, 1.38467677e-02, 1.04214604e-03,
                                       -8.30181215e-03, 1.73184941e-03, 3.93878570e-04,
                                       7.18865102e-03, -4.20890340e-04, -1.18390314e-04,
                                       -2.92525548e-02, 0.00000000e+00, 1.66888367e-03,
                                       5.14602337e-02, 3.40421210e-03, 1.67396760e-02,
                                       -8.96976731e-03, -6.45098035e-03, 8.68521983e-05,
                                       2.71576649e-05, -5.02301579e-05, 9.22803618e-03,
                                       0.00000000e+00, 2.25382472e-03, 1.23594421e-05,
                                       -2.24377723e-05, 1.33360856e-04, 1.42521599e-03,
                                       3.53399258e-03, 2.25451300e-03, -2.00674588e-03,
                                       7.36566151e-05, 1.03045993e-05, 3.47143732e-04,
                                       2.63910220e-03, -3.43303086e-05, 2.92911290e-04,
                                       4.18062866e-03, 2.66199849e-05, 7.64997182e-02,
                                       7.07973896e-06, -6.24927299e-04, 4.18672762e-05,
                                       1.78134379e-04, 4.45117742e-04, 0.00000000e+00,
                                       -7.00416435e-05, 1.64773256e-05, 1.74867423e-04,
                                       -1.99056503e-06, 3.50109316e-03, 2.84926705e-02,
                                       4.36112184e-03, 4.35467659e-05, 2.79355066e-04,
                                       0.00000000e+00, 0.00000000e+00, -2.35322879e-04,
                                       -2.76475901e-05, -2.61767083e-05, 8.74251947e-05,
                                       -1.07005196e-04, 0.00000000e+00, 1.22785580e-03,
                                       2.93099461e-05, 3.86744366e-05, 0.00000000e+00,
                                       1.21929687e-04, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 1.59335628e-05, -1.19449654e-05,
                                       1.99138678e-05, 1.21397319e-05, 2.04915771e-05,
                                       2.85742148e-04, 9.28833692e-03, 1.36877174e-03,
                                       -2.67272664e-04, 0.00000000e+00, 1.73707344e-03,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       -1.51598143e-04, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 6.05515782e-04, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       3.78094074e-06, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 6.26363220e-05, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[-2.78965666e-03, -2.65610817e-02, -2.80280825e-05,
                                       -2.50679067e-03, -7.51578304e-04, -3.49373009e-03,
                                       1.64296865e-03, 4.41638542e-04, 1.77338657e-03,
                                       -6.51474882e-04, -1.67743438e-06, 6.81079915e-04,
                                       -5.06737153e-04, -7.28068051e-02, -5.70645676e-03,
                                       2.05791534e-04, -6.33815182e-01, 1.51980377e-04,
                                       0.00000000e+00, 1.25216309e-04, 1.16593987e-01,
                                       6.95324620e-03, 4.97162010e-06, -7.33860047e-03,
                                       4.29534688e-06, 6.40025478e-05, -1.07810811e-04,
                                       -1.25565129e-04, -9.78599290e-02, 6.12850848e-02,
                                       0.00000000e+00, 9.44711495e-04, -4.01336980e-04,
                                       -1.93430158e-05, -4.11376721e-05, -2.82197802e-03,
                                       7.86652750e-05, 1.39393431e-04, -7.28593635e-07,
                                       1.19332257e-02, 6.05297086e-03, 9.61472642e-02,
                                       -1.04006602e-04, -1.26954458e-04, 7.55449923e-06,
                                       1.86008219e-04, -1.49451584e-08, -1.19073074e-04,
                                       6.55203537e-06, 6.02033633e-06, -4.18265684e-05,
                                       -1.00301844e-05, -4.82223255e-04, -7.29411774e-06,
                                       2.62581218e-06, -8.59851665e-05, -2.33728588e-03,
                                       3.44736220e-06, 3.43136874e-04, -6.79551225e-04,
                                       1.75669943e-07, -6.90618382e-05, 1.59201521e-04,
                                       1.22236121e-05, 0.00000000e+00, -1.63094696e-02,
                                       -5.69542652e-03, -1.57117912e-02, -3.53340116e-06,
                                       -2.85389931e-06, -5.19243154e-07, -2.08107876e-05,
                                       1.44108773e-04, -4.48504523e-06, -1.26528066e-06,
                                       -1.14971225e-04, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 1.56317676e-04, -9.10083323e-06,
                                       3.01300395e-06, -5.69120802e-04, -1.65170679e-06,
                                       -4.92998754e-04, 0.00000000e+00, 0.00000000e+00,
                                       -1.30280078e-05, 0.00000000e+00, 1.05951132e-06,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       7.31721785e-07, 0.00000000e+00, -2.18439738e-05,
                                       -2.93558341e-10, 2.74340819e-05, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       -9.60554196e-06, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[-8.44600775e-06, -5.15472239e-04, 1.88128776e-08,
                                       8.15593965e-05, 7.23400440e-05, -2.32129947e-04,
                                       4.57245259e-05, -7.44054253e-05, 4.76291389e-04,
                                       1.47695724e-05, 7.32384314e-06, 1.70875140e-06,
                                       -6.12927648e-05, 1.73520259e-07, -1.00450031e-05,
                                       4.99228839e-05, 2.25839492e-06, -1.60619399e-06,
                                       4.72847504e-09, 7.86309280e-05, -2.74834249e-06,
                                       -8.30645896e-06, 8.25414643e-06, -7.69616668e-07,
                                       2.74826293e-06, 1.15859715e-04, 4.81229970e-06,
                                       -1.29843287e-06, -5.79082742e-06, 1.49555747e-05,
                                       4.48144999e-09, 8.30632629e-05, -2.57748316e-06,
                                       -5.28778780e-05, 1.64511508e-05, 1.94636453e-06,
                                       6.85670843e-07, 7.88172422e-06, -1.26126244e-06,
                                       -7.13529435e-07, 1.36881969e-08, -1.34276194e-05,
                                       9.63953705e-06, -1.22102887e-05, 1.44341632e-05,
                                       5.52152612e-05, -1.87978767e-06, -7.60194662e-07,
                                       -7.19973254e-06, -2.12014359e-05, 4.63776745e-06,
                                       -8.76206343e-06, -4.88882129e-07, 2.18549097e-09,
                                       1.10292812e-05, -2.73169592e-05, -1.24456479e-05,
                                       -7.50690133e-06, 5.18485800e-05, -2.01870347e-05,
                                       1.89613637e-05, -2.42432187e-06, 1.21128151e-04,
                                       9.53268670e-07, 0.00000000e+00, -9.81063847e-06,
                                       1.04436998e-06, -1.18467540e-07, 7.29118383e-07,
                                       9.84358425e-07, 8.95801568e-08, 1.27055378e-05,
                                       -2.99032264e-06, -1.11829238e-05, 3.95742944e-06,
                                       -6.63022551e-08, -1.39282115e-01, -2.64712895e-09,
                                       -5.53701094e-07, -2.68195793e-07, -1.67795423e-07,
                                       2.97825607e-06, -3.63174912e-06, -4.97832043e-06,
                                       -3.95218381e-07, -1.16394654e-08, -5.87673065e-07,
                                       -3.94375233e-07, 0.00000000e+00, 7.85464613e-06,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       -2.64211909e-07, 0.00000000e+00, 0.00000000e+00,
                                       8.53422875e-07, 7.56593808e-06, 0.00000000e+00,
                                       1.27405289e-06, 0.00000000e+00, 6.65051430e-07,
                                       0.00000000e+00, 3.02324404e-05, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 1.49491161e-07,
                                       3.43398548e-08, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, -4.68353001e-07, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 6.63082448e-08, 0.00000000e+00,
                                       -2.03242303e-10, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]]),
                            np.array([[3.31698662e-03, 2.75840738e-04, 1.91721179e-06,
                                       4.66452955e-03, 1.63978784e-04, -2.63945161e-04,
                                       -1.03102377e-03, -4.47680263e-05, 2.24984667e-04,
                                       2.36948168e-06, 4.88550411e-07, 7.99415562e-07,
                                       -5.20233020e-05, -1.63899446e-06, -3.37958403e-06,
                                       -1.49197745e-03, -5.01504488e-05, -1.13594668e-04,
                                       0.00000000e+00, 8.10933208e-06, -1.16368495e-05,
                                       -3.28818883e-06, 5.08053793e-05, -5.46009093e-05,
                                       -4.30052263e-05, -2.23539752e-05, 8.52533287e-06,
                                       2.32359322e-06, -1.88116420e-05, 4.55237560e-05,
                                       0.00000000e+00, 6.56219459e-04, -7.13695282e-06,
                                       -5.50638191e-06, -1.72604418e-02, -2.71092279e-04,
                                       7.90749674e-07, -2.76296660e-05, 4.60341231e-07,
                                       2.67966644e-08, -2.05046257e-08, -1.51352484e-06,
                                       -2.77327206e-07, -2.37420045e-04, 7.76307340e-08,
                                       -7.65967286e-07, 3.96114157e-09, -1.50530920e-03,
                                       1.14253473e-07, -1.80470365e-06, 7.64606580e-05,
                                       -2.40607498e-05, 1.56651872e-07, -3.50755124e-07,
                                       -3.19307586e-05, -1.52265992e-04, -7.63635958e-05,
                                       -6.86177265e-05, -5.42233161e-07, -1.36576687e-04,
                                       6.37881934e-08, -5.50285028e-07, 2.35245493e-03,
                                       -7.65696747e-04, 0.00000000e+00, -3.70345000e-05,
                                       3.47422387e-06, 1.43867703e-03, 3.12852398e-06,
                                       -2.36983386e-07, -6.61014521e-06, 6.36215658e-07,
                                       2.71942026e-08, -7.22884226e-05, -5.23039187e-05,
                                       -1.66959065e-05, 1.76634441e-07, -1.21145750e-01,
                                       -1.10622811e-07, -2.85250352e-05, 2.32194581e-05,
                                       -3.35870357e-08, -9.25399477e-08, -4.13474385e-05,
                                       -2.45780884e-07, 0.00000000e+00, -1.26250255e-08,
                                       -5.13842451e-07, 0.00000000e+00, 2.54911763e-06,
                                       4.54225176e-08, 0.00000000e+00, 0.00000000e+00,
                                       -3.40790366e-07, 0.00000000e+00, 0.00000000e+00,
                                       -8.13931528e-06, 3.86345550e-07, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 2.04989231e-07,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                       0.00000000e+00, 0.00000000e+00]])]


        self.add_shap(0, 'PV145 VALVE POSITION (0.0-1.0)', '41.47%')
        self.add_shap(1, 'NRHX OUTLET TEMPERATURE', '36.06%')
        self.add_shap(2, 'PRZ LEVEL', '9.9%')
        self.add_shap(3, 'AVERAGE FUEL TEMPERATURE', '1.9%')


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main1Right()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()
