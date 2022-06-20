# Top Bar
Top_Bar = """
            QWidget#BG {
                background: rgb(128, 128, 128);
                border:0px;
            }
            QLabel#Title {
                background: rgb(255, 255, 255);
                border-radius: 5px;
                color: rgb(0, 0, 0);
                font: 27px Arial;
                qproperty-alignment: AlignCenter;
            }
            QPushButton#Tab {
                background: rgb(231, 231, 234);
                border-radius: 5px;
                color: rgb(0, 0, 0);
                font: 27px Arial;
                qproperty-alignment: AlignCenter;
            }
            QPushButton#Tab:hover {
                background: rgb(0, 176, 218);
            }
"""

# AIDAA Tab
AIDAA = """
            QWidget#BG {
                background: rgb(231, 231, 234);
                border:0px;
            }
"""

AIDAA_Diagnosis = """
            QWidget#BG {
                background: rgb(231, 231, 234);
                border:0px;
            }
            QPushButton#Button{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                font: 23px Arial;
            }
            QPushButton#Button:hover {
                background: rgb(0, 176, 218);
            }
            QTableWidget{
                background: rgb(231, 231, 234);
                border: 1px solid rgb(128, 128, 128); 
                font: 23px Arial;
            }
            QHeaderView::section {
                background: rgb(128, 128, 128);
                border: 0px;
                font: 23px Arial;
                padding-left:5px;
            }
            QTableWidget::item::selected {
                background-color: rgb(0, 176, 218);
                font: 23px Arial;
            }
            QTableWidget::item {
                padding: 5px 0px 0px 0px;
                font: 23px Arial;
                left:10px;
            }
            QTableWidget::item::selected#tab3 {
                height:32px;
                background-color: rgb(0, 176, 218);
                font: 23px Arial;
                border-radius: 5px;
            }
            QTableWidget::item#tab3 {
                background-color: rgb(178, 178, 178);
                margin:3px;
                font: 23px Arial;
                left:10px;
                
                margin: 5px 0px 5px 0px;
            }
            
            
            
           
"""

'''
           border-top-left-radius: 0;
    border-top-right-radius: 0;
    border-bottom-right-radius: 4px;
    border-bottom-left-radius: 4px;
           
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
                image : url(../img/check.png);
                height:22px;
                width:22px;
                border : 1px solid;
            }'''

''' QTableWidget{background: #e9e9e9;selection-color: white;border: 1px solid lightgrey;
                            selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);
                            color: #202020;
                            outline: 0;}
                            QTableWidget::item::hover{
                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);}
                            QTableWidget::item::focus
                            {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);border: 0px;}'''