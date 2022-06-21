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
                margin: 1px 0px 1px 0px;
                background-color: rgb(0, 176, 218);
                font: 23px Arial;
                border-radius: 2px;
            }
            QTableWidget::item#tab3 {
                margin: 1px 0px 1px 0px;
                background-color: rgb(178, 178, 178);
                font: 23px Arial;
                border-radius: 2px;
            }
           
"""