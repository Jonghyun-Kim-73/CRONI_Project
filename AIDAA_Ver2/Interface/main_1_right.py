import sys

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
        col_info = [('비정상 절차서 명', 340), ('긴급 여부', 210), ('진입 조건', 210), ('AI 확신도', 200)]
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

        # 테이블 행 높이 조절
        for i in range(0, self.rowCount()):
            self.setRowHeight(i, 28)

        # 테이블 임시 데이터
        self.max_cell = 5
        self.update_procedure()
        # self.data = []
        # for i in range(5):
        #     self.data.append(QTextEdit(''))
        # self.setcellWidget(1, 1, 'Ab15_08: 증기발생기 수위 채널 고장 (고)')
        # self.shmem.get_procedure_info('Ab15_08: 증기발생기 수위 채널 고장 (고)')
        # 클릭 시 하단 비정상절차서 show
        self.cellClicked.connect(self.mouseClick)
        # 더블 클릭 시 절차서 화면 이동
        self.cellDoubleClicked.connect(self.mouseDoubleClick)


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
        ai_result = [1.04777455e-03, 1.87130286e-04, 1.96067709e-04, 3.04176280e-04,
                    3.51275333e-04, 4.60391938e-04, 1.85054867e-03, 1.70936875e-04,
                    5.40873585e-04, 8.78681517e-04, 1.25459874e-03, 9.90428406e-01,
                    1.32304912e-03, 8.37134484e-04, 9.51688051e-05, 7.37859320e-05] # 실제 인공지능 결과
        ai_proc = pd.DataFrame(list(enumerate(ai_result))).sort_values(by=1,ascending=False) # 인공지능 결과 전처리
        diagnosis_convert_text = {0: 'Normal: 정상', 1: 'Ab21_01: 가압기 압력 채널 고장 (고)', 2: 'Ab21_02: 가압기 압력 채널 고장 (저)', 3: 'Ab20_04: 가압기 수위 채널 고장 (저)', 4: 'Ab15_07: 증기발생기 수위 채널 고장 (저)', 5: 'Ab15_08: 증기발생기 수위 채널 고장 (고)',
                                  6: 'Ab63_04: 제어봉 낙하', 7: 'Ab63_02: 제어봉의 계속적인 삽입', 8: 'Ab21_12: 가압기 PORV (열림)', 9: 'Ab19_02: 가압기 안전밸브 고장', 10: 'Ab21_11: 가압기 살수밸브 고장 (열림)', 11: 'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설',
                                  12: 'Ab60_02: 재생열교환기 전단부위 파열', 13: 'Ab59_02: 충전수 유량조절밸즈 후단누설', 14: 'Ab23_01: RCS에서 1차기기 냉각수 계통(CCW)으로 누설', 15: 'Ab23_06: 증기발생기 전열관 누설'}
        ai_ref = {i:{'name':diagnosis_convert_text[int(ai_proc.iloc[i][0])], 'em':len(ab_pro[diagnosis_convert_text[int(ai_proc.iloc[i][0])]]['긴급 조치 사항']), 'if_prob':f'2/{self.shmem.get_pro_symptom_count(diagnosis_convert_text[int(ai_proc.iloc[i][0])])}', 'ai_prob':round(ai_proc.iloc[i][1]*100,2)} for i in range(len(ai_result))}
        print()
        for i in range(5):
            self.add_procedure(i, ai_ref[i]['name'], ai_ref[i]['em'], ai_ref[i]['if_prob'], ai_ref[i]['ai_prob'])

        # self.add_procedure(0, 'Ab21_01: 가압기 압력 채널 고장 (고)', False,  '12/12', 50)
        # self.add_procedure(1, 'Ab63_04: 제어봉 낙하', True, '2/4', 80)
        # self.add_procedure(2, 'Ab63_02: 제어봉의 계속적인 삽입', False, '0/5',  60)

    def mouseClick(self):
        # print('Test 절차서 선택 시 화면 전환')
        row = self.currentIndex().row()
        if self.cellWidget(row, 0) is not None:
            Flag.call_bottom_name = self.cellWidget(row, 0).currentText()
            Flag.call_bottom = True
        else:
            Flag.call_bottom_None = True

    def mouseDoubleClick(self):
        # print('Test 절차서 선택 시 화면 전환')
        row = self.currentIndex().row()
        # set 비정상절차서명
        if self.cellWidget(row, 0) is not None:
            Flag.call_prss_name = self.cellWidget(row, 0).currentText()
            Flag.call_prss = True

        # print(self.item(row, 1))


        # Flag.call_prss = True

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
        #Flag.call_recv = True
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

    def check_btn_press(self):
        if Flag.call_bottom:
            self.symptom = []
            self.clearLayout(self.gb_layout)

            self.add_symptom(Flag.call_bottom_name)
            self.setTitle(f"비정상절차서: {Flag.call_bottom_name}") # 테이블 클릭 시 비정상 절차서 이름을 Title로 반영
            self.gb.setTitle(f"Symptom Check [2/{len(ab_pro[Flag.call_bottom_name]['경보 및 증상'])}]") # 테이블 클릭 시 비정상 절차서의 "경보 및 증상" 요건의 개수를 반영

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
