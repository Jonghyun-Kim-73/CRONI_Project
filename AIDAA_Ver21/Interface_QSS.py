#-* encoding: UTF-8 -*-
# Top Bar
Top_Bar = """
            QWidget#BG {
                background: rgb(128, 128, 128);
                border:0px;
            }
            QLabel#Title {
                background: rgb(255, 255, 255);
                border-radius: 5px;
                border:0px;
                color: rgb(0, 0, 0);
                font: 27px;
                qproperty-alignment: AlignCenter;
            }
            QPushButton#Tab {
                background: rgb(231, 231, 234);
                border-radius: 5px;
                border:0px;
                color: rgb(0, 0, 0);
                font: 27px;
                qproperty-alignment: AlignCenter;
            }
            QPushButton#Tab:hover {
                background: rgb(0, 176, 218);
                 border-radius: 5px;
                border:0px;
                color: rgb(0, 0, 0);
                font: 27px;
                qproperty-alignment: AlignCenter;
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
            QToolTip { 
                background: white;
                border: 1px solid #808080;
           }
            QCheckBox::indicator { 
                width: 18px; 
                height: 18px; 
            } 
            QCheckBox::indicator:unchecked {
                image: url(./img/uncheck.png);
            }
            QCheckBox::indicator:checked {
                image: url(./img/check.png);
            }
            QPushButton#Button{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                font: 23px;
            }
            QPushButton#Button:hover {
                background: rgb(0, 176, 218);
                border-radius: 5px;
                font: 23px;
            }
            QTableWidget{
                background: rgb(231, 231, 234);
                border: 1px solid rgb(128, 128, 128); 
                font: 18px;
                font-weight: bold;
            }
            QHeaderView::section {
                background: rgb(128, 128, 128);
                border: 0px;
                font: 18px;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
            QTableWidget::item::selected {
                background-color: rgb(0, 176, 218);
                color:black;
                font-weight: bold;
                font: 18px;
                outline: 0;
            }
            
            QTableWidget::item {
                font: 18px;
                font-weight: bold;
            }
            QTableView
            {
                outline: 0;
            }
  
"""

AIDAA_Diagnosis2 = """
            QWidget#BG{
                background: rgb(231, 231, 234);
                border: 0px;
            }
            QWidget#RightPG{
                background: rgb(231, 231, 234);
                border-radius: 5px;
                border: 1px solid #808080;
            }
            QLabel#Label{
                background: rgb(192, 0, 0);
                border-radius: 5px;
                font: 23px;
                font-weight: bold;
                border:0px;
                qproperty-alignment: AlignCenter;
            }
            QLabel#Title{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                font: 23px;
                font-weight: bold;
                border:0px;
            }
            QPushButton#Button{
                background: rgb(0, 176, 86);
                border-radius: 5px;
                border:0px;
                font: 23px;
            }
            QPushButton#Search{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                border:0px;
                font: 23px;
                font-weight: bold;
            }
            QPushButton#Search::hover{
                background: rgb(0, 176, 218);
                border-radius: 5px;
                border:0px;
                font: 23px;
                font-weight: bold;
            }
            QPushButton#Tab{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                border:0px;
                font: 23px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton#Tab::hover{
                background: rgb(0, 176, 218);
                border-radius: 5px;
                border:0px;
                font: 23px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton#Check{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                border: 1px solid #707070;
            }
            QPushButton#Bottom{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                font-weight: bold;
                font: 23px;
            }
            QLabel{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                padding-left:5px;
                font: 23px;
                font-weight: bold;
                border:0px;
            }
            QLabel#TitleBar{
                background: rgb(112, 112, 112);
                border-radius: 5px;
                padding-left:5px;
                font: 23px;
                font-weight: bold;
                border:0px;
            }
            QPushButton{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                border: 1px solid #707070;
                border:0px;
            }
            QLabel#Notice{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                border: 1px solid #C00000;
                font: 23px;
                font-weight: bold;
            }
            QLabel#label_title{
                color: #C00000;
                font: 23px;
                font-weight: bold;
            }
            QLabel#label_content{
                color: rgb(0, 0, 0);
                font: 23px;
                font-weight: bold;
            }
            QLabel#Notice{
                background: rgb(255, 255, 255);
                border: 1px solid #C00000; 
                border-radius: 5px;
            }
            QScrollArea{
                background: rgb(231, 231, 234);
                border: 0px;
            }
            QWidget#scroll_bg{
                background: rgb(231, 231, 234);
                border: 1px solid #707070; 
                border-radius:5px;
            }
            QScrollBar
            {
                background : lightgray;
                border: 1px solid #707070; 
                width:25px;
            }
            QScrollBar::handle
            {
                background : white;
            }
            QScrollBar::handle::pressed
            {
                background : white;
            }
"""