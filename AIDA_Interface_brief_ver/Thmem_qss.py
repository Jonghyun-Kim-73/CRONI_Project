qss = """
    /* ----------------------------------------------------------------------------- */
    /* 위젯 정보                                                                      */
    /* ----------------------------------------------------------------------------- */
    
    QWidget {background: rgb(128, 128, 128);}       /* 메인 위젯 Back color 색 */
    
    QWidget#SubW {                                  /* 서브 위젯 */
        background: rgb(180, 180, 180);             /* 서브 위젯 Back color */    
        border-style: outset;
        border-width: 1px;                          /* 서브 위젯 테두리 선 두께 */
        border-radius: 10px;
        border-color: rgb(120, 120, 120);           /* 서브 위젯 테두리 선 색 */
    }          
    
    /* ----------------------------------------------------------------------------- */
    /* 라벨 정보                                                                      */
    /* ----------------------------------------------------------------------------- */
    
    QLabel {                                        /* 기본 라벨 컨샙 */
        background: rgb(95, 91, 82);
        border-radius: 6px;
        font: bold 14px;
        color: rgb(255, 255, 255);
        padding: 4px 4px;
    }
    
    /* ConditionBar */
    QLabel#ConditionBar[Condition="Normal"] {
        background: rgb(96, 186, 70);
    }
    QLabel#ConditionBar[Condition="Emergency"] {
        background: rgb(248, 108, 107);
    }
    QLabel#ConditionBar[Condition="Abnormal"] {
        background: rgb(255, 193, 7);
    }
    
    /* CircleProgress */
    QLabel#CircleProgress {
            background: rgb(31, 39, 42);
            border-radius: 6px;
            font: bold 8px;
            color: rgb(255, 255, 255);
    }
    
    /* ----------------------------------------------------------------------------- */
    /* 테이블 정보                                                                    */
    /* ----------------------------------------------------------------------------- */
    
    
    /* AlarmTable */
    QTableWidget#AlarmTable {
            border: none;
            border-radius: 8px;
            padding: 1px 1px;
    }
    QTableWidget#AlarmTable QHeaderView{
            background: rgb(255, 255, 255);             /* 메인 위젯 Back color 색 */
    }
    QTableWidget#AlarmTable QHeaderView::section {
            background: rgb(255, 255, 255);             /* 메인 위젯 Back color 색 */
            border-style: outset;
            border-width: 1px;                          /* 서브 위젯 테두리 선 두께 */
            border-radius: 8px;
            border-color: rgb(120, 120, 120);           /* 서브 위젯 테두리 선 색 */    
    }
    
    
    /* ----------------------------------------------------------------------------- */
    /* 버튼 정보                                                                      */
    /* ----------------------------------------------------------------------------- */
    
    /* 종료 버튼 */
    QPushButton#Exit {
        background: rgb(248, 108, 107);
        border-radius: 6px;
        border: none;
    }
    QPushButton#Exit:hover {
        background: rgb(248, 108, 107);
    }
    QPushButton#Exit:pressed {
        background: rgb(220, 152, 162);
    }
    
    /* End ------------------------------------------------------------------------- */
"""