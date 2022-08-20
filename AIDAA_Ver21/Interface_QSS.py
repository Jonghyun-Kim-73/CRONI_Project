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
                font: 30px;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
            QPushButton#Tab {
                background: rgb(231, 231, 234);
                border-radius: 5px;
                border:0px;
                font: 30px;
                font-weight: bold;
                color: rgb(0, 0, 0);
            }
            QPushButton#Tab:hover {
                background: rgb(0, 176, 218);
                border-radius: 5px;
                border:0px;
                font: 30px;
                font-weight: bold;
                color: rgb(0, 0, 0);
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
                width: 30px; 
                height: 30px; 
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
                font: 30px;
                font-weight: bold;   
            }
            QPushButton#Button:hover {
                background: rgb(0, 176, 218);
                border-radius: 5px;
                font: 30px;
                font-weight: bold;   
            }
            QTableWidget{
                background: rgb(231, 231, 234);
                border: 1px solid rgb(128, 128, 128); 
                font: 30px;           
                border-top-left-radius :5px;
                border-top-right-radius : 5px;
                border-bottom-left-radius : 5px;
                border-bottom-right-radius : 5px;    
            }
            QHeaderView {
                background: rgb(128, 128, 128);
                border: 0px;
            }
            QHeaderView::section {
                background: rgb(128, 128, 128);
                font: 30px;
                font-weight: bold;        
                qproperty-alignment: AlignCenter;
            }
            QHeaderView::section:horizontal:first {
                border: 1px solid rgb(128, 128, 128);
                border-top-left-radius:5px;
                border-top-right-radius:0px;
                border-bottom-left-radius:0px;
                border-bottom-right-radius:0px;
            }
            QHeaderView::section:horizontal:middle {
                border: 2px solid rgb(128, 128, 128);
                border-radius:0px;
            }
            QHeaderView::section:horizontal:last {
                border: 1px solid rgb(128, 128, 128);
                border-top-left-radius:0px;
                border-top-right-radius:5px;
                border-bottom-left-radius:0px;
                border-bottom-right-radius:0px;
            }
            QTableWidget::item::selected {
                background-color: rgb(0, 176, 218);
                color:black;
                font: 30px;
                outline: 0;
            }
            QTableWidget::item {
                font: 30px;
                border-bottom: 1px solid rgb(128, 128, 128);
            }

            QScrollBar:vertical {
                border-left: 1px solid rgb(128, 128, 128);
                background-color: rgb(80, 80, 80);
                width: 21px;    
                margin: 0px 0px 0px 0px;
                border-top-left-radius:0px;
                border-top-right-radius:5px;
                border-bottom-left-radius:0px;
                border-bottom-right-radius:5px;
            }
            QScrollBar::handle:vertical {         
                min-height: 0px;
                border: 0px;
                background-color: rgb(255, 255, 255);
                border-top-left-radius:5px;
                border-top-right-radius:5px;
                border-bottom-left-radius:5px;
                border-bottom-right-radius:5px;
            }
            QScrollBar::add-line:vertical {       
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-page:vertical { 
                border-top-right-radius:5px;
                background: rgb(128,128,128);
            }
            QScrollBar::add-page:vertical { 
                border-bottom-right-radius:5px;
                background: rgb(128,128,128);
            }
            QTableWidget#Tab3::item::selected {
                margin-top: 5px;
                background-color: rgb(0, 176, 218);
                color:black;
                font: 30px;
                outline: 0;
            }
            QTableWidget#Tab3::item {
                font: 30px;
                margin-top: 5px;
                background-color: rgb(178, 178, 178);
            }
            QTableView{
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
                font: 30px;
                font-weight: bold;
                border:0px;
                qproperty-alignment: AlignCenter;
            }
            QLabel#Title{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                font: 30px;
                font-weight: bold;
                border:0px;
            }
            QPushButton#Button{
                background: rgb(0, 176, 86);
                border-radius: 5px;
                border:0px;
                font: 30px;
                font-weight: bold;
            }
            QPushButton#Search{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                border:0px;
                font: 30px;
                font-weight: bold;
                
            }
            QPushButton#Search::hover{
                background: rgb(0, 176, 218);
                border-radius: 5px;
                border:0px;
                font: 30px;
                font-weight: bold;
            }
            QPushButton#Tab{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                border:0px;
                font: 30px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton#Tab::hover{
                background: rgb(0, 176, 218);
                border-radius: 5px;
                border:0px;
                font: 30px;
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
                font: 30px;
                font-weight: bold;
            }
            QLabel{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                padding-left:5px;
                font: 30px;
                font-weight: bold;
                border:0px;
            }
            QLabel#TitleBar{
                background: rgb(112, 112, 112);
                border-radius: 5px;
                padding-left:5px;
                font: 30px;
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
                font: 30px;
                font-weight: bold;
            }
            QLabel#label_title{
                color: #C00000;
                font: 30px;
                font-weight: bold;
            }
            QLabel#label_content{
                color: rgb(0, 0, 0);
                font: 30px;
                font-weight: bold;
            }
            QLabel#Notice{
                background: rgb(255, 255, 255);
                border: 1px solid #C00000; 
                border-radius: 5px;
            }
            QScrollBar:vertical {
                border-left: 1px solid rgb(128, 128, 128);
                background-color: rgb(80, 80, 80);
                width: 25px;    
            }
            QScrollBar::handle:vertical {         
                min-height: 0px;
                border: 0px;
                background-color: rgb(255, 255, 255);
            }
            QScrollBar::add-line:vertical {       
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-page:vertical { 
                background: rgb(128,128,128);
            }
            QScrollBar::add-page:vertical { 
                background: rgb(128,128,128);
            }
"""

Main_Tab = """
            QPushButton#Left{
                background: rgb(0, 176, 86);
                border-radius: 5px;
                border:0px;
                color: rgb(0, 0, 0);
                font: 30px;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
            QLabel#Left{
                background: rgb(0, 176, 86);
                border-radius: 5px;
                border:0px;
                color: rgb(0, 0, 0);
                font: 30px;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
            QPushButton#Bottom{
                background: rgb(255, 255, 255);
                border-radius: 5px;
                border:0px;
                font: 30px;
                font-weight: bold;
                color: rgb(0, 0, 0);
            }
            QPushButton#Bottom::hover{
                background: rgb(0, 178, 218);
                border-radius: 5px;
                border:0px;
                font: 30px;
                font-weight: bold;
                color: rgb(0, 0, 0);
            }
            QPushButton#Right{
                background: rgb(128, 128, 128);
                border-radius: 5px;
                border:0px;
                color: rgb(0, 0, 0);
                font: 23px;
            }
            QPushButton#Right::hover{
                background: rgb(0, 178, 128);
                border-radius: 5px;
                border:0px;
                color: rgb(0, 0, 0);
                font: 23px;
            }
            QLabel#RightTabTitle{
                background-color: rgb(128, 128, 128);
                border-radius: 5px;
                border:0px;
                color: rgb(0, 0, 0);
                font: 23px;
            }
            QLabel#RightTabTitle:disabled{
                color: rgb(231, 231, 231);
            }
            QLabel#RightTabcont{
                background-color: rgb(128, 128, 128);
                border-radius: 5px;
                border:0px;
                color: rgb(0, 0, 0);
                font: 23px;
            }
            QLabel#RightTabcont:disabled{
                color: rgb(128, 128, 128);
            }
"""