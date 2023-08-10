# ref : https://het.as.utexas.edu/HET/Software/html/stylesheet-reference.html
# ref : https://doc.qt.io/archives/qt-4.8/stylesheet-examples.html#customizing-qgroupbox
# ref : https://wikidocs.net/book/2957
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# Qss builder -------------------------------------------------
def builder(objecttype:str, objectname:str, contents:list):
    qss_info = f'{objecttype}#{objectname}' + '{'
    
    for content in contents:
        qss_info += f'{content};'
    
    qss_info += '}'
    
    return qss_info
def rgb_to_qCOLOR(color_code:str, alpha=250):
    color_code = color_code.replace('rgb(', '').replace(')', '').replace(' ', '').split(',')
    return QColor(int(color_code[0]), int(color_code[1]), int(color_code[2]), alpha)
def rgb_to_hex(color_code:str):
    color_code = color_code.replace('rgb(', '').replace(')', '').replace(' ', '').split(',')
    r = int(color_code[0])
    g = int(color_code[1])
    b = int(color_code[2])
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)
# Color Table -------------------------------------------------
DarkGray = 'rgb(80, 80, 80)'            # Title, Header
Gray = 'rgb(181, 181, 181)'
LightGray = 'rgb(231, 231, 234)'        # 배경
LightWhite = 'rgb(255, 255, 255)'
LightBlue = 'rgb(0, 178, 216)'
LightYellow = 'rgb(255, 235, 0)'        # Alarm 2 Background (Mimic)
DarkBlue = 'rgb(64, 61, 152)'
DarkRed = 'rgb(192, 0, 0)'
Yellow = 'rgb(255, 204, 0)'
DarkYellow = 'rgb(255, 192, 0)'
Black = 'rgb(0, 0, 0)'
Green = 'rgb(0, 170, 0)'
LightGreen = 'rgb(0, 176, 86)'
Orange = 'rgb(255, 192, 0)'
# Font Table --------------------------------------------------
Global_font_size_nub = 16
Content_font_size_nub = 10
Pre_trip_font_size_nub = 8
Mimic_font_size_nub = 10
Global_font_size = f'{Global_font_size_nub}pt'
Content_font_size = f'{Content_font_size_nub}pt'
Pre_trip_font_size_nub = f'{Content_font_size_nub}pt'
Global_font = 'Arial'
Global_font2 = '맑은 고딕'
# Qss ---------------------------------------------------------
QssMain = ''.join([
    builder('QWidget', 'Main', [
        f'background-color: {LightGray};',
        ]),
    builder('QWidget', 'MainTop', [
        f'background-color: {DarkGray};',
        'border:0px;',
        ]),
    builder('QLabel', 'MainTopTime', [
        f'background-color: {LightWhite};',
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        "qproperty-alignment: 'AlignCenter';",
        'font-weight: bold;',
        ]),
    builder('QLabel', 'MainTopSystemName', [
        f'background-color: {LightWhite};',
        'border:0px;',
        f'color: {Black};'
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        "qproperty-alignment: 'AlignCenter';",
        'font-weight: bold;',
        ]),
    builder('QPushButton', 'MainTopCallMain', [
        f'background-color: {LightWhite};',
        'border:0px;',
        'border-radius: 5px;',
        f'color: {Black};'
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        'font-weight: bold;',
        ]),
    builder('QPushButton', 'MainTopCallMain:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'MainTopCallMain:checked', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'MainTopCallIFAP', [
        f'background-color: {LightWhite};',
        'border:0px;',
        'border-radius: 5px;',
        f'color: {Black};'
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        'font-weight: bold;',
        ]),
    builder('QPushButton', 'MainTopCallIFAP:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'MainTopCallIFAP:checked', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'MainTopCallAIDAA', [
        f'background-color: {LightWhite};',
        'border:0px;',
        'border-radius: 5px;',
        f'color: {Black};'
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        'font-weight: bold;',
        ]),
    builder('QPushButton', 'MainTopCallAIDAA:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'MainTopCallAIDAA:checked', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'MainTopCallEGIS', [
        f'background-color: {LightWhite};',
        'border:0px;',
        'border-radius: 5px;',
        f'color: {Black};'
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        'font-weight: bold;',
        ]),
    builder('QPushButton', 'MainTopCallEGIS:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'MainTopCallEGIS:checked', [f'background-color: {LightBlue};']),
    builder('QWidget', 'MainTabIFAP', [f'background-color: {Gray};']),
    builder('QWidget', 'MainTabEGIS', [f'background-color: {Gray};']),
    # Interface_AIDAA_Main.py ------------------------------------------------------------------------------------------
    builder('QWidget', 'AIDAAMain', [
        f'background-color: {LightGray};',
        ]),
    builder('QWidget', 'AIDAAMainTop', [
        f'background-color: {DarkGray};',
        'border:0px;',
        ]),
    builder('QLabel', 'AIDAAMainTopTime', [
        f'background-color: {LightWhite};',
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        "qproperty-alignment: 'AlignCenter';",
        'font-weight: bold;',
        ]),
    builder('QLabel', 'AIDAAMainTopSystemName', [
        f'background-color: {LightWhite};',
        'border:0px;',
        f'color: {Black};'
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        "qproperty-alignment: 'AlignCenter';",
        'font-weight: bold;',
        ]),
    builder('QPushButton', 'AIDAAMainTopCallMain', [
        f'background-color: {LightWhite};',
        'border:0px;',
        'border-radius: 5px;',
        f'color: {Black};'
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        'font-weight: bold;',
        ]),
    builder('QPushButton', 'AIDAAMainTopCallMain:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'AIDAAMainTopCallMain:checked', [f'background-color: {LightBlue};']),
    # Interface_Alarm.py ------------------------------------------------------------------------------------------
    builder('QWidget', 'MainAlarm', [
        f'background-color: {LightGray};', 
        'border-radius: 5px;',
        ]),
    builder('QWidget', 'AIDAAAlarm', [f'background-color: {LightGray};']),
    builder('QWidget', 'AlarmFix', [f'background-color: {LightGray};']),
    builder('QPushButton', 'AlarmFixPreTrip', [
        f'background-color: {LightGreen};', 'border-radius: 5px;','border:0px;',
        f'color: {Black};'
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        'font-weight: bold;',
        ]),
    builder('QLabel', 'AlarmFixTrip', [
        f'background-color: {LightGreen};', 'border-radius: 5px;','border:0px;',
        f'color: {Black};'
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        "qproperty-alignment: 'AlignCenter';",
        'font-weight: bold;',
        ]),
    builder('QScrollArea', 'AlarmScrollArea', [f'background-color: {LightGray};', 'border: 0px;']),
    builder('QScrollArea', 'AlarmScrollArea,QScrollBar::sub-page:vertical', [f'background: {LightGray};', f'border: 1px solid {DarkGray}']),
    builder('QScrollArea', 'AlarmScrollArea,QScrollBar::add-page:vertical', [f'background: {LightGray};', f'border: 1px solid {DarkGray}']),
    builder('QScrollArea', 'AlarmScrollArea,QScrollBar::vertical', [f'background: {LightGray};', 'border: None;', 'width: 20px;']),
    builder('QScrollArea', 'AlarmScrollArea,QScrollBar::up-arrow::vertical', ['image: url(./img/Arrow_U.png);']),
    builder('QScrollArea', 'AlarmScrollArea,QScrollBar::down-arrow::vertical', ['image: url(./img/Arrow_D.png);']),
    builder('QTableWidget', 'AlarmTable', [f'background-color: {LightGray};', 
                                           f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    builder('QTableWidget', 'AlarmTable::item', [f'border-bottom: 1px solid {DarkGray};']),
    builder('QTableWidget', 'AlarmTable::item:selected', [
        f'background-color: {LightBlue};', f'color:{Black};', 'outline: 0;', 
        ]),
    builder('QWidget', 'AlarmTableWidget', [f'background-color: {LightGray};', f'border: 1px solid {DarkGray};',]),
    builder('QLabel', 'AlarmHeadingLabel', [
        f'background-color: {DarkGray};',
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        ]),
    builder('QLabel', 'AlarmHeadingLabel[Pos="F"]', ['border-top-left-radius:10px;']),
    builder('QLabel', 'AlarmHeadingLabel[Pos="M"]', ['']),
    builder('QLabel', 'AlarmHeadingLabel[Pos="L"]', ['border-top-right-radius:10px;']),
    builder('QPushButton', 'AlarmSystem_IFAP_SortPress', [
        f'background-color: {LightWhite};', 
        'border-radius: 5px;',
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        'font-weight: bold;',
        ]),
    builder('QPushButton', 'AlarmSystem_IFAP_SortPress:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'AlarmSystem_AIDAA_SortPress', [
        f'background-color: {LightWhite};', 
        'border-radius: 5px;',
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        'font-weight: bold;',
        ]),
    builder('QPushButton', 'AlarmSystem_AIDAA_SortPress:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'AlarmSystem_EGIS_SortPress', [
        f'background-color: {LightWhite};', 
        'border-radius: 5px;', 
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        'font-weight: bold;',
        ]),
    builder('QPushButton', 'AlarmSystem_EGIS_SortPress:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'AlarmSystem_Sortsystem_SortPress', [
        f'background-color: {LightWhite};', 
        'border-radius: 5px;', 
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        'font-weight: bold;',
        ]),
    builder('QPushButton', 'AlarmSystem_Sortsystem_SortPress:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'AlarmAIDAA_Suppress_SortPress', [
        f'background-color: {LightWhite};', 
        'border-radius: 5px;', 
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        'font-weight: bold;',
        ]),
    builder('QPushButton', 'AlarmAIDAA_Suppress_SortPress:hover', [f'background-color: {LightBlue};']),
    # Interface_MainTabRight.py -------------------------------------------------------------------------------------
    ### Pre-Abnormal
    builder('QWidget', 'MainTabRightPreAbnormalW', [
        f'background-color: {LightWhite};', 
        'border-radius: 10px;', f'border:1px solid {DarkGray};'
    ]),
    builder('QLabel', 'MainTabRightPreAbnormalWTitle', [
        'background: None;', 'border: None;', f'font-family: {Global_font};', 'font-size: 40px;',
    ]),
    builder('QPushButton', 'MainTabRightPreAbnormalWBTN', [f'background-color: {Gray};', 'border-radius: 5px;', f'font-family: {Global_font};', 'font-size: 40px;']),
    builder('QPushButton', 'MainTabRightPreAbnormalWBTN:hover', [f'background-color: {LightBlue};']),
    builder('QLabel', 'MainTabRightPreAbnormalWContent', [
        f'background-color: {LightGray};', f'border:1px solid {DarkGray};', f'font-family: {Global_font};', 'font-size: 40px;',
        'border-bottom-right-radius: 10px;', 'border-bottom-left-radius: 10px;'
    ]),
    ### Abnormal
    builder('QWidget', 'MainTabRightAbnormalW', [
        f'background-color: {Yellow};', 
        'border-radius: 10px;', f'border:1px solid {DarkGray};'
    ]),
    builder('QLabel', 'MainTabRightAbnormalWTitle', [
        'background: None;', 'border: None;', f'font-family: {Global_font};', 'font-size: 40px;',
    ]),
    builder('QPushButton', 'MainTabRightAbnormalWBTN', [f'background-color: {Gray};', 'border-radius: 5px;', f'font-family: {Global_font};', 'font-size: 40px;']),
    builder('QPushButton', 'MainTabRightAbnormalWBTN:hover', [f'background-color: {LightBlue};']),
    builder('QLabel', 'MainTabRightAbnormalWContent', [
        f'background-color: {LightGray};', f'border:1px solid {DarkGray};', f'font-family: {Global_font};', 'font-size: 40px;',
        'border-bottom-right-radius: 10px;', 'border-bottom-left-radius: 10px;'
    ]),
    ### Emergency
    builder('QWidget', 'MainTabRightEmergencyW', [
        f'background-color: {DarkRed};', 
        'border-radius: 10px;', f'border:1px solid {DarkGray};'
    ]),
    builder('QLabel', 'MainTabRightEmergencyWTitle', [
        'background: None;', 'border: None;', f'font-family: {Global_font};', 'font-size: 40px;',
    ]),
    builder('QPushButton', 'MainTabRightEmergencyWBTN', [f'background-color: {Gray};', 'border-radius: 5px;', f'font-family: {Global_font};', 'font-size: 40px;']),
    builder('QPushButton', 'MainTabRightEmergencyWBTN:hover', [f'background-color: {LightBlue};']),
    builder('QLabel', 'MainTabRightEmergencyWContent', [
        f'background-color: {LightGray};', f'border:1px solid {DarkGray};', f'font-family: {Global_font};', 'font-size: 40px;',
        'border-bottom-right-radius: 10px;', 'border-bottom-left-radius: 10px;'
    ]),
    # Interface_MainTabAIDAA.py -------------------------------------------------------------------------------------
    builder('QWidget', 'MainTabAIDAA', [f'background-color: {LightGray};']),
    # Interface_AIDAA_Diagnosis.py ----------------------------------------------------------------------------------
    builder('QWidget', 'Diagnosis', [f'background-color: {LightGray};', 'border:0px;']),
    builder('QPushButton', 'DiagnosisTopCallProcedureSearch', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'DiagnosisTopCallProcedureSearch:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'DiagnosisTopCallSystemSearch', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'DiagnosisTopCallSystemSearch:hover', [f'background-color: {LightBlue};']),
    # --
    builder('QScrollArea', 'DiagnosisProcedureTableScrollArea', ['border:0px;', f'background-color: {LightGray};']),
    builder('QTableWidget', 'DiagnosisProcedureTable', [f'background-color: {LightGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    builder('QTableWidget', 'DiagnosisProcedureTable::item', [f'border-bottom: 1px solid {DarkGray};']),
    builder('QTableWidget', 'DiagnosisProcedureTable[Block="On"]::item:selected', [f'background-color: {Gray};']),
    builder('QTableWidget', 'DiagnosisProcedureTable[Block="Off"]::item:selected', [f'background-color: {LightBlue};', f'color:{Black};', 'outline: 0;']),
    builder('QTableWidget', 'DiagnosisProcedureTable[Block="On"]', [f'background-color: {Gray};']),
    builder('QTableWidget', 'DiagnosisProcedureTable[Block="Off"]', [f'background-color: {LightGray};']),
    # --
    builder('QLabel', 'DiagnosisProcedureItem', ['border:0px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    builder('QLabel', 'DiagnosisProcedureItem[Block="On"]', [f'background-color: {DarkGray};', f'color:{DarkGray}']),
    builder('QLabel', 'DiagnosisProcedureItem[Block="Off"]', [f'color:{Black}']),
    builder('QCheckBox', 'DiagnosisProcedureCheckBox', ['margin-left:30%;', 'margin-right:60%;']),
    builder('QCheckBox', 'DiagnosisProcedureCheckBox[Block="Off"]::indicator', ['width: 25px;', 'height: 25px;']),
    builder('QCheckBox', 'DiagnosisProcedureCheckBox[Block="On"]::indicator', ['width: 0px;', 'height: 0px;']),
    builder('QCheckBox', 'DiagnosisProcedureCheckBox::indicator:checked', ['image: url(./Img/uncheck.png);']),
    builder('QCheckBox', 'DiagnosisProcedureCheckBox::indicator:unchecked', ['image: url(./Img/check.png);']),
    builder('QCheckBox', 'DiagnosisProcedureCheckBox::indicator', ['width: 0px;', 'height: 0px;']),
    builder('QWidget', 'DiagnosisProcedureTableWidget', ['border:0px;', f'background-color: {LightGray};']),
    builder('QLabel', 'DiagnosisProcedureHeadingLabel', [
        f'background-color: {DarkGray};',
        f'font-family: {Global_font};',
        f'font-size: {Global_font_size};',
        ]),
    builder('QLabel', 'DiagnosisProcedureHeadingLabel[Pos="F"]', ['border-top-left-radius:10px;']),
    builder('QLabel', 'DiagnosisProcedureHeadingLabel[Pos="M"]', ['']),
    builder('QLabel', 'DiagnosisProcedureHeadingLabel[Pos="L"]', ['border-top-right-radius:10px;']),
    # --
    builder('QScrollArea', 'DiagnosisSystemScrollArea', ['border:0px;', f'background-color: {LightGray};']),
    builder('QTableWidget', 'DiagnosisSystemTable', [f'background-color: {LightGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    builder('QTableWidget', 'DiagnosisSystemTable::item', [f'border-bottom: 1px solid {DarkGray};']),
    builder('QTableWidget', 'DiagnosisSystemTable[Block="On"]::item:selected', [f'background-color: {Gray};']),
    builder('QTableWidget', 'DiagnosisSystemTable[Block="Off"]::item:selected', [f'background-color: {LightBlue};', f'color:{Black};', 'outline: 0;']),
    builder('QTableWidget', 'DiagnosisSystemTable[Block="On"]', [f'background-color: {Gray};']),
    builder('QTableWidget', 'DiagnosisSystemTable[Block="Off"]', [f'background-color: {LightGray};']),
    builder('QLabel', 'DiagnosisSystemItem', ['border:0px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    builder('QLabel', 'DiagnosisSystemItem[Block="On"]', [f'background-color: {DarkGray};', f'color:{DarkGray}']),
    builder('QLabel', 'DiagnosisSystemItem[Block="Off"]', [f'color:{Black}']),
    builder('QWidget', 'DiagnosisSystemTableWidget', ['border:0px;', f'background-color: {LightGray};']),
    # --
    builder('QScrollArea', 'ProcedureCheckTableScrollArea', ['border:0px;', f'background-color: {LightGray};']),
    builder('QTableWidget', 'ProcedureCheckTable', [f'background-color: {LightGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    builder('QLabel', 'ProcedureCheckTableItem', ['border:0px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    builder('QLabel', 'ProcedureCheckTableItem[Activate="On"]', [f'background-color: {LightBlue};', f'border-bottom: 1px solid {DarkGray};']),
    builder('QLabel', 'ProcedureCheckTableItem[Activate="Off"]', [f'background-color: {LightGray};', f'border-bottom: 1px solid {DarkGray};']),
    builder('QWidget', 'DiagnosisSystemTableWidget', ['border:0px;', f'background-color: {LightGray};']),
    # Interface_AIDAA_Procedure_Search.py ---------------------------------------------------------------------------
    builder('QWidget', 'ProcedureSearch', [f'background-color: {LightGray};']),
    builder('QWidget', 'ProcedureSearchTitleBar', [f'background-color: {DarkGray};', 'border: 0px;']),
    builder('QLabel', 'ProcedureSearchTitleName', [f'background-color: {LightGray};', 'border: 0px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', 'qproperty-alignment: AlignCenter;', 'font-weight: bold;']),
    builder('QWidget', 'ProcedureSearchWindow', [f'background-color: {LightGray};', 'border: 0px;']),
    builder('QGroupBox', 'ProcedureSearchWindowGroupBox', [f'background-color: {LightGray};', f'border: 1px solid {DarkGray};', 'border-radius: 10px;', 'margin-top: 10px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};']),
    builder('QGroupBox', 'ProcedureSearchWindowGroupBox::title', ['subcontrol-origin: margin;', 'top: -5px;', 'left: 30px;', 'padding: 0px 2px 0px 2px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};']),
    builder('QLabel', 'ProcedureSearchLabel1', [f'background-color: {LightGray};', 'border: 0px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', 'qproperty-alignment: AlignCenter;', 'font-weight: bold;']),
    builder('QPlainTextEdit', 'ProcedureSearchInput1', [f'background-color: {LightWhite};', 'border: 0px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', 'font-weight: bold;']),
    builder('QPushButton', 'ProcedureSearchBTN', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};' 'font-weight: bold;']),
    builder('QLabel', 'ProcedureSearchLabel2', [f'background-color: {LightGray};', 'border: 0px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', 'qproperty-alignment: AlignCenter;', 'font-weight: bold;']),
    builder('QPlainTextEdit', 'ProcedureSearchInput2', [f'background-color: {LightWhite};', 'border: 0px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', 'font-weight: bold;']),
    builder('QPushButton', 'ProcedureSearchReset', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};' 'font-weight: bold;']),
    builder('QTableWidget', 'ProcedureSearchTable', [f'background-color: {LightGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    builder('QTableWidget', 'ProcedureSearchTable::item', [f'border-bottom: 1px solid {DarkGray};']),
    builder('QTableWidget', 'ProcedureSearchTable::item:selected', [
        f'background-color: {LightBlue};', f'color:{Black};', 'outline: 0;', 
        ]),
    builder('QWidget', 'ProcedureSearchTableWidget', [f'background-color: {LightGray};', f'border: 1px solid {DarkGray};',]),
    builder('QLabel', 'ProcedureHeadingLabel', [
        f'background-color: {DarkGray};',
        f'font-family: {Global_font};',
        f'font-size: {Content_font_size};',
        'font-weight: bold;',
        ]),
    builder('QLabel', 'ProcedureHeadingLabel[Pos="F"]', ['border-top-left-radius:10px;']),
    builder('QLabel', 'ProcedureHeadingLabel[Pos="M"]', ['']),
    builder('QLabel', 'ProcedureHeadingLabel[Pos="L"]', ['border-top-right-radius:10px;']),
    builder('QWidget', 'ProcedureSearchBottom', [f'background-color: {LightGray};']),
    builder('QPushButton', 'ProcedureSearchOpen', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'ProcedureSearchCancel', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};' 'font-weight: bold;']),
    # --
    builder('QWidget', 'SystemSearch', [f'background-color: {LightGray};']),
    builder('QWidget', 'SystemSearchTitleBar', [f'background-color: {DarkGray};', 'border: 0px;']),
    builder('QLabel', 'SystemSearchTitleName', [f'background-color: {LightGray};', 'border: 0px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', 'qproperty-alignment: AlignCenter;', 'font-weight: bold;']),
    builder('QWidget', 'SystemSearchWindow', [f'background-color: {LightGray};', 'border: 0px;']),
    builder('QGroupBox', 'SystemSearchWindowGroupBox', [f'background-color: {LightGray};', f'border: 1px solid {DarkGray};', 'border-radius: 10px;', 'margin-top: 10px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};']),
    builder('QGroupBox', 'SystemSearchWindowGroupBox::title', ['subcontrol-origin: margin;', 'top: -5px;', 'left: 30px;', 'padding: 0px 2px 0px 2px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};']),
    builder('QLabel', 'SystemSearchLabel', [f'background-color: {LightGray};', 'border: 0px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', 'qproperty-alignment: AlignCenter;', 'font-weight: bold;']),
    builder('QPlainTextEdit', 'SystemSearchInput', [f'background-color: {LightWhite};', 'border: 0px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', 'font-weight: bold;']),    
    builder('QPushButton', 'SystemSearchInput', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'SystemSearchBTN', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'SystemSearchReset', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};' 'font-weight: bold;']),
    builder('QTableWidget', 'SystemSearchTable', [f'background-color: {LightGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    builder('QTableWidget', 'SystemSearchTable::item', [f'border-bottom: 1px solid {DarkGray};']),
    builder('QTableWidget', 'SystemSearchTable::item:selected', [
        f'background-color: {LightBlue};', f'color:{Black};', 'outline: 0;', 
        ]),
    builder('QWidget', 'SystemSearchTableWidget', [f'background-color: {LightGray};', f'border: 1px solid {DarkGray};',]),
    builder('QLabel', 'SystemSearchHeadingLabel', [
        f'background-color: {DarkGray};',
        f'font-family: {Global_font};',
        f'font-size: {Content_font_size};',
        'font-weight: bold;',
        ]),
    builder('QLabel', 'SystemSearchHeadingLabel[Pos="F"]', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;']),
    builder('QWidget', 'SystemSearchBottom', [f'background-color: {LightGray};']),
    builder('QPushButton', 'SystemSearchOpen', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'SystemSearchCancel', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    #--
    builder('QWidget', 'XAISearch', [f'background-color: {LightGray};']),
    builder('QWidget', 'XAISearchTitleBar', [f'background-color: {DarkGray};', 'border: 0px;']),
    builder('QLabel', 'XAISearchTitleBarName', [f'background-color: {DarkGray};', 'border: 0px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};', 'qproperty-alignment: AlignCenter;', 'font-weight: bold;']),
    builder('QPushButton', 'XAISearchClose', ['border-radius: 5px;', 'border:0px;']),
    builder('QWidget', 'XAISearchWindow', [f'background-color: {LightGray};', 'border-radius: 5px;', f'border: 1px solid {DarkGray};']),
    builder('QLabel', 'XAISearchTitleName', [f'background-color: {LightGray};', 'border: 0px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};', 'qproperty-alignment: AlignCenter;', 'font-weight: bold;']),
    builder('QScrollArea', 'XAISearchScrollArea', ['border:0px;', f'background-color: {LightGray};']),
    builder('QLabel', 'XAISearchHeadingLabel', ['border:0px;', f'background-color: {DarkGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};', 'font-weight: bold;']),
    builder('QLabel', 'XAISearchHeadingLabel[Pos="F"]', ['border-top-left-radius:10px;']),
    builder('QLabel', 'XAISearchHeadingLabel[Pos="M"]', ['']),
    builder('QLabel', 'XAISearchHeadingLabel[Pos="L"]', ['border-top-right-radius:10px;']),
    builder('QTableWidget', 'XAISearchTable', [f'background-color: {LightGray};', 'border:0px;']),
    builder('QTableWidget', 'XAISearchTable::item', [f'background-color: {LightGray};', f'border-bottom: 1px solid {DarkGray};']),
    builder('QTableWidget', 'XAISearchTable::item:selected', [f'background-color: {LightBlue};']),
    builder('QLabel', 'XAISearchItem', ['border: 0px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};', 'font-weight: bold;']),
    builder('QLabel', 'XAISearchItem[Pos="F"]', [f'border-left: 1px solid {DarkGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};', 'font-weight: bold;']),
    builder('QLabel', 'XAISearchItem[Pos="L"]', [f'border-right: 1px solid {DarkGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};', 'font-weight: bold;']),
    builder('QPushButton', 'XAISearchCancel', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    # Interface_AIDAA_Procedure.py ----------------------------------------------------------------------------------
    builder('QWidget', 'Procedure', [f'background-color: {LightGray};', 'border: 0px;']),
    builder('QWidget', 'ProcedureTop', [f'background-color: {LightGray};']),
    builder('QLabel', 'UrgentBTN', [f'background-color: {Gray};', 'border:0px;', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'UrgentBTN[Condition="On"]', [f'background-color: {DarkRed};']),
    builder('QLabel', 'UrgentBTN[Condition="Off"]', [f'background-color: {Gray};']),
    builder('QLabel', 'RadiationBTN', [f'background-color: {Gray};', 'border:0px;', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'RadiationBTN[Condition="On"]', [f'background-color: {DarkRed};']),
    builder('QLabel', 'RadiationBTN[Condition="Off"]', [f'background-color: {Gray};']),
    builder('QLabel', 'ProcedureInfo', [f'background-color: {LightWhite};', 'border:0px;', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    # --
    builder('QWidget', 'ProcedureWindow', [f'background-color: {LightGray};']),
    builder('QWidget', 'ProcedureSequence', [f'background-color: {LightGray};']),
    builder('QWidget', 'ProcedureSequenceWidget', [f'background-color: {LightGray};']),
    builder('QPushButton', 'ProcedureSequenceTitlePu', [f'background-color: {LightWhite};', 'border-radius: 5px;', 'border:0px;', 'text-align: left;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'ProcedureSequenceTitlePu:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'ProcedureSequenceTitlePu[Blink="True"]', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'ProcedureSequenceTitlePu[Blink="False"]', [f'background-color: {LightWhite};']),
    builder('QPushButton', 'ProcedureSequenceTitleAl', [f'background-color: {LightWhite};', 'border-radius: 5px;', 'border:0px;', 'text-align: left;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'ProcedureSequenceTitleAl:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'ProcedureSequenceTitleAl[Blink="True"]', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'ProcedureSequenceTitleAl[Blink="False"]', [f'background-color: {LightWhite};']),
    builder('QPushButton', 'ProcedureSequenceTitleAu', [f'background-color: {LightWhite};', 'border-radius: 5px;', 'border:0px;', 'text-align: left;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'ProcedureSequenceTitleAu:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'ProcedureSequenceTitleAu[Blink="True"]', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'ProcedureSequenceTitleAu[Blink="False"]', [f'background-color: {LightWhite};']),
    builder('QPushButton', 'ProcedureSequenceTitleUr', [f'background-color: {LightWhite};', 'border-radius: 5px;', 'border:0px;', 'text-align: left;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'ProcedureSequenceTitleUr:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'ProcedureSequenceTitleUr[Blink="True"]', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'ProcedureSequenceTitleUr[Blink="False"]', [f'background-color: {LightWhite};']),
    builder('QPushButton', 'ProcedureSequenceTitleFo', [f'background-color: {LightWhite};', 'border-radius: 5px;', 'border:0px;', 'text-align: left;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'ProcedureSequenceTitleFo:hover', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'ProcedureSequenceTitleFo[Blink="True"]', [f'background-color: {LightBlue};']),
    builder('QPushButton', 'ProcedureSequenceTitleFo[Blink="False"]', [f'background-color: {LightWhite};']),
    # --
    builder('QLabel', 'ProcedureSequenceTitleCondPu', [f'background-color: {LightWhite};', f'border: 1px solid {DarkGray};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'ProcedureSequenceTitleCondPu[Condition="0"]', [f'background-color: {LightWhite};']),
    builder('QLabel', 'ProcedureSequenceTitleCondPu[Condition="1"]', [f'background-color: {Black};']),
    builder('QLabel', 'ProcedureSequenceTitleCondPu[Condition="2"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'ProcedureSequenceTitleCondPu[Condition="3"]', [f'background-color: {DarkRed};']),
    builder('QLabel', 'ProcedureSequenceTitleCondAl', [f'background-color: {LightWhite};', f'border: 1px solid {DarkGray};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'ProcedureSequenceTitleCondAl[Condition="0"]', [f'background-color: {LightWhite};']),
    builder('QLabel', 'ProcedureSequenceTitleCondAl[Condition="1"]', [f'background-color: {Black};']),
    builder('QLabel', 'ProcedureSequenceTitleCondAl[Condition="2"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'ProcedureSequenceTitleCondAl[Condition="3"]', [f'background-color: {DarkRed};']),
    builder('QLabel', 'ProcedureSequenceTitleCondAu', [f'background-color: {LightWhite};', f'border: 1px solid {DarkGray};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'ProcedureSequenceTitleCondAu[Condition="0"]', [f'background-color: {LightWhite};']),
    builder('QLabel', 'ProcedureSequenceTitleCondAu[Condition="1"]', [f'background-color: {Black};']),
    builder('QLabel', 'ProcedureSequenceTitleCondAu[Condition="2"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'ProcedureSequenceTitleCondAu[Condition="3"]', [f'background-color: {DarkRed};']),
    builder('QLabel', 'ProcedureSequenceTitleCondUr', [f'background-color: {LightWhite};', f'border: 1px solid {DarkGray};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'ProcedureSequenceTitleCondUr[Condition="0"]', [f'background-color: {LightWhite};']),
    builder('QLabel', 'ProcedureSequenceTitleCondUr[Condition="1"]', [f'background-color: {Black};']),
    builder('QLabel', 'ProcedureSequenceTitleCondUr[Condition="2"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'ProcedureSequenceTitleCondUr[Condition="3"]', [f'background-color: {DarkRed};']),
    builder('QLabel', 'ProcedureSequenceTitleCondFo', [f'background-color: {LightWhite};', f'border: 1px solid {DarkGray};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'ProcedureSequenceTitleCondFo[Condition="0"]', [f'background-color: {LightWhite};']),
    builder('QLabel', 'ProcedureSequenceTitleCondFo[Condition="1"]', [f'background-color: {Black};']),
    builder('QLabel', 'ProcedureSequenceTitleCondFo[Condition="2"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'ProcedureSequenceTitleCondFo[Condition="3"]', [f'background-color: {DarkRed};']),
    # --
    builder('QScrollArea', 'ProcedureScrollArea', [f'background: {LightGray};', 'border:0px;']),
    builder('QScrollArea', 'ProcedureScrollArea::sub-page:vertical', [f'background: {LightGray};', f'border: 1px solid {DarkGray};']),
    builder('QScrollArea', 'ProcedureScrollArea::add-page:vertical', [f'background: {LightGray};', f'border: 1px solid {DarkGray};']),
    builder('QScrollArea', 'ProcedureScrollArea:vertical', [f'background: {DarkGray};', 'width: 20px;']),
    builder('QScrollArea', 'ProcedureScrollArea::up-arrow::vertical', ['image: url(./img/Arrow_U.png);']),
    builder('QScrollArea', 'ProcedureScrollArea::down-arrow::vertical', ['image: url(./img/Arrow_D.png);']),
    builder('QWidget', 'ProcedureScrollAreaWidget', ['border:0px;', f'background-color: {LightGray};']),
    builder('QWidget', 'ProcedureContents', [f'background-color: {LightGray};', 'border-radius: 5px;', f'border: 1px solid {DarkGray};']),
    builder('QLabel', 'ProcedureTitleBar_1', [f'background-color: {DarkGray};', 'border:0px;', 'border-radius: 5px;', 'padding-left:5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QLabel', 'ProcedureTitleBar_2', [f'background-color: {DarkGray};', 'border:0px;', 'border-radius: 5px;', 'padding-left:5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    # --
    builder('QLabel', 'Procedure_Content_Nub', [f'background-color: {LightWhite};', 'border:0px;', 'border-radius: 5px;', 'padding-left:5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QLabel', 'Procedure_Content_EM', [f'background-color: {LightWhite};', f'border:1px solid {DarkRed};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QLabel', 'Procedure_Content_EM, QLabel#label_title', [f'color: {DarkRed};', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QLabel', 'Procedure_Content_EM, QLabel#label_content', [f'color: {Black};', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QLabel', 'Procedure_Content_OB', [f'background-color: {LightWhite};', f'border:1px solid {Black};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QLabel', 'Procedure_Content_OB, QLabel#label_title', [f'color: {Black};', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QLabel', 'Procedure_Content_OB, QLabel#label_content', [f'color: {Black};', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),

    builder('QLabel', 'Procedure_Content_Basic', [f'background-color: {LightWhite};', 'border:0px;', 'border-radius: 5px;', 'padding-left:5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'Procedure_Content_Check', [f'background-color: {LightWhite};', f'border:1px solid {DarkGray};', 'border-radius: 5px;']),
    builder('QPushButton', 'ProcedureComplete', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'ProcedureParallel', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    builder('QPushButton', 'ProcedureReconduct', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;']),
    # Interface_AIDAA_Pretrip.py ----------------------------------------------------------------------------------
    builder('QWidget', 'PreTrip', ['border:0px;', f'background-color: {LightGray};']),
    builder('QLabel', 'PreTripTitle', ['border-radius: 5px;', f'background-color: {LightGreen};', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QWidget', 'LeftPrediction', ['border:0px;', f'background-color: {LightGray};']),
    builder('QWidget', 'RightPrediction', ['border:0px;', f'background-color: {LightGray};']),
    builder('QWidget', 'Parameter_Graph', ['border-radius: 10px;', f'border: 1px solid {DarkGray};']),
    builder('QWidget', 'ParameterGraphSub', [f'background-color: {LightGray};', 'border-radius: 10px;', f'border: 1px solid {DarkGray};']),
    builder('QLabel', 'TripTimeLabel', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {Gray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_name', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {DarkGray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_name[Blink="True"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'Parameter_name[Blink="False"]', [f'background-color: {Gray};']),
    builder('QLabel', 'Parameter_TripTime', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {DarkGray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_TripTime[Blink="True"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'Parameter_TripTime[Blink="False"]', [f'background-color: {Gray};']),

    builder('QLabel', 'Parameter_TripTime1', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {DarkGray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_TripTime1[Blink="True"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'Parameter_TripTime1[Blink="False"]', [f'background-color: {Gray};']),
    builder('QLabel', 'Parameter_TripTime2', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {DarkGray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_TripTime2[Blink="True"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'Parameter_TripTime2[Blink="False"]', [f'background-color: {Gray};']),
    builder('QLabel', 'Parameter_TripTime3', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {DarkGray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_TripTime3[Blink="True"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'Parameter_TripTime3[Blink="False"]', [f'background-color: {Gray};']),
    builder('QLabel', 'Parameter_TripTime4', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {DarkGray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_TripTime4[Blink="True"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'Parameter_TripTime4[Blink="False"]', [f'background-color: {Gray};']),
    builder('QLabel', 'Parameter_TripTime5', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {DarkGray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_TripTime5[Blink="True"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'Parameter_TripTime5[Blink="False"]', [f'background-color: {Gray};']),
    builder('QLabel', 'Parameter_TripTime6', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {DarkGray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_TripTime6[Blink="True"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'Parameter_TripTime6[Blink="False"]', [f'background-color: {Gray};']),
    builder('QLabel', 'Parameter_TripTime7', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {DarkGray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_TripTime7[Blink="True"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'Parameter_TripTime7[Blink="False"]', [f'background-color: {Gray};']),
    builder('QLabel', 'Parameter_TripTime8', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {DarkGray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_TripTime8[Blink="True"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'Parameter_TripTime8[Blink="False"]', [f'background-color: {Gray};']),
    builder('QLabel', 'Parameter_TripTime9', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {DarkGray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_TripTime9[Blink="True"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'Parameter_TripTime9[Blink="False"]', [f'background-color: {Gray};']),
    builder('QLabel', 'Parameter_TripTime10', ['border-top-left-radius:10px;', 'border-top-right-radius:10px;', f'background-color: {DarkGray};', 'margin:0px;', f'font-family: {Global_font};', f'font-size: {Pre_trip_font_size_nub};' 'font-weight: bold;', 'qproperty-alignment: AlignCenter;']),
    builder('QLabel', 'Parameter_TripTime10[Blink="True"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'Parameter_TripTime10[Blink="False"]', [f'background-color: {Gray};']),
    # Interface_AIDAA_Action.py -----------------------------------------------------------------------------------
    builder('QWidget', 'Action', ['border:0px;', f'background-color: {LightGray};']),
    builder('QLabel', 'ActionTitleLabel', ['border:0px;', f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};' 'font-weight: bold;', 'qproperty-alignment: AlignLeft;']),
    builder('QScrollArea', 'ActionAlarmArea', ['border:0px;', f'background-color: {LightGray};']),
    builder('QLabel', 'ActionAlarmAreaTableHeadingLabel', ['border:0px;', f'background-color: {DarkGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};', 'font-weight: bold;']),
    builder('QLabel', 'ActionAlarmAreaTableHeadingLabel[Pos="F"]', ['border-top-left-radius:10px;']),
    builder('QLabel', 'ActionAlarmAreaTableHeadingLabel[Pos="M"]', ['']),
    builder('QLabel', 'ActionAlarmAreaTableHeadingLabel[Pos="L"]', ['border-top-right-radius:10px;']),
    builder('QTableWidget', 'ActionAlarmAreaTable', [f'background-color: {LightGray};', 'border:0px;']),
    builder('QTableWidget', 'ActionAlarmAreaTable::item', [f'background-color: {LightGray};', f'border-bottom: 1px solid {DarkGray};']),
    builder('QTableWidget', 'ActionAlarmAreaTable::item:selected', [f'background-color: {LightBlue};']),
    # --
    builder('QScrollArea', 'ActionSuggestionAreaScroll', ['border:0px;', f'background-color: {LightGray};']),
    builder('QWidget', 'ActionSuggestionAreaScrollW', ['border:0px;', f'background-color: {LightGray};']),
    builder('QLabel', 'ActionSuggestionAreaTableHeadingLabel', ['border:0px;', f'background-color: {DarkGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};', 'font-weight: bold;']),
    builder('QLabel', 'ActionSuggestionAreaTableHeadingLabel[Pos="F"]', ['border-top-left-radius:10px;']),
    builder('QLabel', 'ActionSuggestionAreaTableHeadingLabel[Pos="M"]', ['']),
    builder('QLabel', 'ActionSuggestionAreaTableHeadingLabel[Pos="L"]', ['border-top-right-radius:10px;']),
    builder('QWidget', 'ActionSuggestionAreaTable', [f'background-color: {LightGray};', 'border:0px;']),
    # --
    builder('QLabel', 'ActionAlarmAreaTableItem', ['border: 0px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    builder('QLabel', 'ActionAlarmAreaTableItem[Pos="F"]', [f'border-left: 1px solid {DarkGray};']),
    builder('QLabel', 'ActionAlarmAreaTableItem[Pos="M"]', ['']),
    builder('QLabel', 'ActionAlarmAreaTableItem[Pos="L"]', [f'border-right: 1px solid {DarkGray};']),
    builder('QLabel', 'ActionAlarmAreaTableChangedItem', ['border: 0px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    # --
    builder('QWidget', 'ActionSuggestionAreaTable', [f'border: 1px solid {DarkGray};']),
    builder('QWidget', 'ActionSuggestionAreaItem', ['border:0px;']),
    builder('QLabel', 'ActionSuggestionAreaItemContent', [f'background-color: {LightWhite};', 'border-radius: 10px;', f'border: 1px solid {DarkGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    builder('QLabel', 'ActionSuggestionAreaItemContent[Activate="True"]', [f'background-color: {LightBlue};']),
    builder('QLabel', 'ActionSuggestionAreaItemContent[Activate="False"]', [f'background-color: {LightGray};']),
    builder('QLabel', 'ActionSuggestionAreaItemCheckBox', [f'background-color: {LightWhite};', 'border-radius: 10px;', f'border: 1px solid {DarkGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};']),
    builder('QLabel', 'ActionSuggestionAreaItemCheckBox[Condition="Stop"]', [f'background-color: {LightWhite};']),
    builder('QLabel', 'ActionSuggestionAreaItemCheckBox[Condition="Abnormal"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'ActionSuggestionAreaItemCheckBox[Condition="AutoRun"]', [f'background-color: {Gray};']),
    builder('QLabel', 'ActionSuggestionAreaItemCheckBox[Condition="ManRun"]', [f'background-color: {Black};']),
    # Interface_AIDAA_ActionMimic.py > 해당 파일에서 수정 ----------------------------------------------------------
    
])
# final qss !! 
qss = ''.join(
    [QssMain]
)