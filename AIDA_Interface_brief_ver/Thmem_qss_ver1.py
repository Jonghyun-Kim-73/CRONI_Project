
qss = """
    /* ----------------------------------------------------------------------------- */
    /* 위젯 정보                                                                      */
    /* ----------------------------------------------------------------------------- */
    QWidget#Mainwindow {
        background: rgb(254, 245, 249);                 /* 메인 위젯 Back color */
    }
    QWidget#MainTitleBar {
        background: rgb(19, 27, 48);                    /* 메인 위젯 TitleBar color */
    }
    /* -- */
    QWidget#MainLeftArea {
        background: rgb(254, 245, 249);                 /* 메인 위젯 Left color -> Back color */
    }
    QTableWidget#MainLeftAlarmTable {
        background: rgb(254, 0, 100);                   /* 메인 위젯 LeftAlarmTable color -> Back color */
        border: 0px;                                
    }
    QTableWidget#MainLeftAlarmTable QHeaderView{
        background: rgb(19, 27, 48);                   /* 메인 위젯 LeftAlarmTable color -> Back color */  
        # TODO 여기서                      
    }
    QPushButton#MainLeftSupPresBtn {
        background: rgb(38, 55, 96);                    /* 활성화 o */ 
    }
    /* -- */
    QWidget#MainRightArea {
        background: rgb(254, 245, 249);                 /* 메인 위젯 Right color -> Back color */
    }
    /* -- */
    QWidget#Stack1 {
        background: rgb(254, 245, 249);                 /* 메인 위젯 SysArea color -> Back color */
    }
    /* -------------------------------- */
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
"""