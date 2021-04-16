qss = """
    /* ----------------------------------------------------------------------------- */
    /* 위젯 정보                                                                      */
    /* ----------------------------------------------------------------------------- */
    
    QWidget {background: rgb(255, 255, 255);}       /* 메인 위젯 색 */
    
    QWidget#SubW {                                  /* 서브 위젯 색 */
        background: rgb(0, 249, 250);           
        border-style: outset;
        border-width: 2px;
        border-radius: 6px;
        border-color: beige;
    }          
    
    /* ----------------------------------------------------------------------------- */
    /* 라벨 정보                                                                      */
    /* ----------------------------------------------------------------------------- */
    
    QLabel {                                        /* 기본 라벨 컨샙 */
        background: rgb(62, 74, 84);
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