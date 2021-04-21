qss = """
    /* ----------------------------------------------------------------------------- */
    /* 위젯 정보                                                                      */
    /* ----------------------------------------------------------------------------- */
    
    QWidget {background: rgb(128, 128, 128);}       /* 메인 위젯 Back color 색 */
    
    QWidget#SubW {                                  /* 서브 위젯 */
        background: rgb(128, 128, 128);             /* 서브 위젯 Back color */    
        border-style: outset;
        border-width: 0px;                          /* 서브 위젯 테두리 선 두께 */
        border-radius: 10px;
        border-color: rgb(0, 0, 0);                 /* 서브 위젯 테두리 선 색 */
    }
    
    QWidget#SubArea {                               /* 서브 Area 위젯 */
        background: rgb(128, 128, 128);             /* 서브 위젯 Back color */    
        border-style: outset;
        border-width: 2px;                          /* 서브 위젯 테두리 선 두께 */
        border-color: rgb(0, 0, 0);                 /* 서브 위젯 테두리 선 색 */
    }              
    
    QWidget#SymptomW{
        background: rgb(128, 128, 128);
        font: bold 12px;
        color: rgb(0, 0, 0);
    }
    
    /* ----------------------------------------------------------------------------- */
    /* 라벨 정보                                                                      */
    /* ----------------------------------------------------------------------------- */
    
    QLabel {                                        /* 기본 라벨 컨샙 */
        background: rgb(128, 128, 128);             /* 메인 위젯 Back color 색 */
        font: bold 14px;
        color: rgb(0, 0, 0);
    }
    
    /* Title Label */
    QLabel#TitleLabel {                             /* 기본 라벨 컨샙 */
        background: rgb(95, 91, 82);
        border-radius: 6px;
        font: bold 14px;
        color: rgb(255, 255, 255);
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
    
    /* AlarmTableItem Info and Timer */
    QLabel#AlarmItemInfo {
            background: rgb(58, 58, 58);
            font-size: 11px;
            color: rgb(212, 178, 46);
    }
    
    /* AlarmTableItem Empty */
    QLabel#AlarmItemEmpty {
            background: rgb(129, 122, 96);
    }
    
    /* ProcedureTableItem Info and Timer */
    QLabel#ProcedureItemInfo {
            background: rgb(128, 128, 128);
            font-size: 11px;
            color: rgb(0, 0, 0);
    }
    
    /* ProcedureTableItem Empty */
    QLabel#ProcedureItemEmpty {
            background: rgb(128, 128, 128);
    }
    
    /* ProcedureTableItem ProcedureAIProbCell */
    QLabel#ProcedureItemProgressLabel {                                        
        background: rgb(128, 128, 128);             
        font: bold 12px;
        color: rgb(0, 0, 0);
    }
    
    /* SymptomLabel */
    QLabel#SymptomLabel{
        background: rgb(128, 128, 128);
        font: bold 12px;
        color: rgb(0, 0, 0);
    }
    
    /* SymptomDisLabel */
    QLabel#SymptomDisLabel{
        background: rgb(128, 128, 128);
        border-style: outset;
        border-width: 1px;                          /* 서브 위젯 테두리 선 두께 */
        border-color: rgb(0, 0, 0);                 /* 서브 위젯 테두리 선 색 */
    }
    QLabel#SymptomDisLabel[Condition="False"] {
        background: rgb(128, 128, 128);
    }
    QLabel#SymptomDisLabel[Condition="True"] {
        background: rgb(184, 25, 28);
    }
    
    
    /* CircleProgress */
    QLabel#CircleProgress {
            background: rgb(0, 0, 0);
            border-radius: 6px;
            font: bold 8px;
            color: rgb(255, 255, 255);
    }
    
    /* ----------------------------------------------------------------------------- */
    /* 테이블 정보                                                                    */
    /* ----------------------------------------------------------------------------- */
    
    /* AlarmTable */
    QTableWidget#AlarmTable {
            border-style: outset;
            border-width: 2px;                          /* 서브 위젯 테두리 선 두께 */
            border-color: rgb(0, 0, 0);                 /* 서브 위젯 테두리 선 색 */ 
    }
    
    QTableWidget#AlarmTable QHeaderView{
            background: rgb(129, 122, 96);             /* 메인 위젯 Back color 색 */
    }
    QTableWidget#AlarmTable QHeaderView::section {
            background: rgb(200, 195, 169);             /* 테이블 위젯 Back color 색 */
            font: bord;
            border-style: outset;
            border-width: 1px;                          /* 서브 위젯 테두리 선 두께 */
            border-color: rgb(0, 0, 0);                 /* 서브 위젯 테두리 선 색 */    
    }
    
    /* ProcedureTable */
    QTableWidget#ProcedureTable {
            border-style: outset;
            border-width: 2px;                          /* 서브 위젯 테두리 선 두께 */
            border-color: rgb(0, 0, 0);                 /* 서브 위젯 테두리 선 색 */ 
    }
    QTableWidget#ProcedureTable QHeaderView{
            background: rgb(128, 128, 128);             /* 메인 위젯 Back color 색 */
    }
    QTableWidget#ProcedureTable QHeaderView::section {
            background: rgb(128, 128, 128);             /* 메인 위젯 Back color 색 */
            border-style: outset;
            border-width: 1px;                          /* 서브 위젯 테두리 선 두께 */
            border-color: rgb(0, 0, 0);                 /* 서브 위젯 테두리 선 색 */    
    }
    
    
    /* ----------------------------------------------------------------------------- */
    /* 버튼 정보                                                                      */
    /* ----------------------------------------------------------------------------- */
    
    
    QPushButton#Btn{
        background: rgb(180, 180, 180);
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
    
    /* ----------------------------------------------------------------------------- */
    /* 진단 바 정보                                                                    */
    /* ----------------------------------------------------------------------------- */
    
    QProgressBar#ProcedureItemProgress {       
        color: rgb(128, 128, 128);
    }
    QProgressBar#ProcedureItemProgress::chunk {
        background-color: rgb(58, 58, 58);
    }
    
    /* End ------------------------------------------------------------------------- */
"""