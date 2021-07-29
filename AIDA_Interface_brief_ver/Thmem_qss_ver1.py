
qss = """
    /* ----------------------------------------------------------------------------- */
    /* 위젯 정보                                                                      */
    /* ----------------------------------------------------------------------------- */
    QWidget#Mainwindow {
        background: rgb(254, 245, 249);                 /* 메인 위젯 Back color */
    }
    /* ------------ TopTitle                    -------- */
        QWidget#MainTitleBar {
            background: rgb(19, 27, 48);                    /* 메인 위젯 TitleBar color */
        }
        QWidget#ChangePP {
            background: rgb(127, 127, 127);                 /* 활성화 x */
            border-radius: 6px;
            font: bold 14px;                     
        }
        QWidget#ChangePP[Condition="Hover"] {
            background: rgb(24, 144, 255);                  /* 호버 임시 낮은 % 색상 */               
        }
        QWidget#ChangePP[Condition="Click"] {
            background: rgb(38, 55, 96);                    /* 활성화 o */                
        }
        QWidget#ChangePP[Condition="Non-Click"] {
            background: rgb(127, 127, 127);                 /* 활성화 x */                     
        }
        QWidget#ChangePPProg {
            background: rgb(127, 127, 127);                 /* 활성화 x */
            border-radius: 6px;
            text-align:left;
            padding-left:5px;
            font: bold 14px;                     
        }
        QWidget#ChangePPProg[Condition="Hover"] {
            background: rgb(24, 144, 255);                  /* 호버 임시 낮은 % 색상 */               
        }
        QWidget#ChangePPProg[Condition="Click"] {
            background: rgb(38, 55, 96);                    /* 활성화 o */                
        }
        QWidget#ChangePPProg[Condition="Non-Click"] {
            background: rgb(127, 127, 127);                 /* 활성화 x */                     
        }
        /* 종료 버튼 */
            QPushButton#Exit {
                background: rgb(184, 25, 28);
                border-radius: 6px;
                border: none;
            }
            QPushButton#Exit:hover {
                background: rgb(184, 25, 28);
            }
            QPushButton#Exit:pressed {
                background: rgb(215, 25, 28);
            }
        /* Title 버튼 */
            QPushButton#TittleBTN {
                background: rgb(74, 182, 146);
                border-radius: 6px;
                border: none;
            }
        /* Title Label */
            QLabel#TitleLabel {                             /* 기본 라벨 컨샙 */
                background: rgb(254, 254, 254);
                border-radius: 6px;
                font: bold 14px;
                color: rgb(0, 0, 0);
                padding: 4px 4px;
            }
        /* ConditionBar */
            QLabel#ConditionBar{
                border-radius: 6px;
                font: bold 14px;
            }
            QLabel#ConditionBar[Condition="Normal"] {
                background: rgb(74, 182, 146);
            }
            QLabel#ConditionBar[Condition="Emergency"] {
                background: rgb(184, 25, 28);
            }
            QLabel#ConditionBar[Condition="Abnormal"] {
                background: rgb(255, 181, 71);
            }
    /* ------------ Left                        -------- */
        QWidget#MainLeftArea {
            background: rgb(254, 245, 249);                 /* 메인 위젯 Left color -> Back color */
        }
        QTableWidget#MainLeftAlarmTable {
            background: rgb(254, 245, 249);                 /* 메인 위젯 LeftAlarmTable color -> Back color */
            border: none;                                
        }
        QTableWidget#MainLeftAlarmTable QHeaderView::section{
            background: rgb(41, 103, 159);                  /* 테이블 위젯 LeftAlarmTable HeadColor -> 차트바 color */
            border: none;
            font: bold 12px;                                /* 폰트 bold */
            color: rgb(255, 255, 255);                      /* 폰트 color */                        
        }
        QPushButton#MainLeftSupPresBtn {
            background: rgb(38, 55, 96);                    /* 활성화 o */ 
        }
    /* ------------ Right                       -------- */
        QWidget#MainRightArea {
            background: rgb(254, 245, 249);                 /* 메인 위젯 Right color -> Back color */
        }
        QTableWidget#MainRightProcedureTable {
            background: rgb(254, 245, 249);                 /* 메인 위젯 LeftAlarmTable color -> Back color */
            border: none;                                
        }
        QTableWidget#MainRightProcedureTable QHeaderView::section{
            background: rgb(41, 103, 159);                  /* 테이블 위젯 LeftAlarmTable HeadColor -> 차트바 color */
            border: none;
            font: bold 12px;                                /* 폰트 bold */
            color: rgb(255, 255, 255);                      /* 폰트 color */                        
        }
        QWidget#ProcedureItemInfo {
            border: none;
        }
        QProgressBar#Prob{
            background: rgb(254, 245, 249);                 /* 메인 위젯 Right color -> Back color */
            border: 2px solid rgb(19, 27, 48);              /*  -> TitleBar color */
            border-radius: 5px;
            margin-right:30px;
        }
        QProgressBar#Prob::chunk{
            background-color: rgb(19, 27, 48);              /* 청크 color -> TitleBar color */
        }
        QTableWidget#ProcedureExplainTable {
            background: rgb(254, 245, 249);                 /* 메인 위젯 LeftAlarmTable color -> Back color */
            border: none;                                
        }
        QTableWidget#ProcedureExplainTable QHeaderView::section{
            background: rgb(41, 103, 159);                  /* 테이블 위젯 LeftAlarmTable HeadColor -> 차트바 color */
            border: none;
            font: bold 12px;                                /* 폰트 bold */
            color: rgb(255, 255, 255);                      /* 폰트 color */                        
        }
        QTreeWidget#MainRightProcedureSymptom {
            background:transparent;
            border: none;                                
        }
        QTreeWidget::item:hover, QTreeWidget::item:selected{
            background:transparent;
            border:none;
        }
        QLabel#StepNub{
            background-color: rgb(127, 127, 127);                 /* 활성화 x */
            border-radius: 5px;
        }
    /* ------------ SystemM                     -------- */
        QWidget#Stack1 {
            background: rgb(254, 245, 249);                 /* 메인 위젯 SysArea color -> Back color */
        }
    /* -END- */
"""