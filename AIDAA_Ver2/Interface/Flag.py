from AIDAA_Ver2.Interface.Procedure.alarm_procedure import alarm_pd
from collections import deque
# FLAG

# 전체 화면 CLOSE
main_close = False

# 화면 Call
call_return = False

call_main = False       # Main 화면
call_prog = False       # 예지 화면
call_prss = False       # 절차서 화면
call_recv = False       # 시스템 복구 화면

call_bottom = False     # Sympotom Check
call_bottom_None = False


# combobox 관련
combobox_update = False  # 절차서 combobox 추가 위함
combo_list = []  # 더블클릭한 절차서들 추가
combo_current = -1
combo_click_left = False
combo_click_right = False
combo_click_text = ""
combo_text_final = ""
combo_blink_start = False
combo_blink = False
combo_blink_idx = -1

# main4
show_right_4 = False
clear_layout_right_4 = False  # 오른쪽 레이아웃 초기화
blink_manclick_start = False  # 운전원 blink
blink_manclick = False  # 운전원 blink

ok_btn = False
together_btn = False
redo_btn = False
complete_btn = False

# 절차서 name call
call_bottom_name = ""   # 비정상 절차서 명
call_bottom_name_backup = ""
call_prss_name = ""     # 비정상 절차서 명

# main2 left button click
main2_btn = [0] * 20

# return list
return_list = ['Main']
return_page = False

# 비정상절차서 체크된 카운트 불러오기 - 수정 필요
check_count = [0] * 10

# main_4_left
layout_clear_4 = False  # layout 초기화 변수
current_btn = -1

# 알람 클리어
alarm_clear = False

# 알람 blink
all_alarm_cnt = 0  # 현재 발생한 전체 알람 cnt
alarm_blink = [False] * 100  # 이상 알람
alarm_color_change = [False] * 100  # 알람 color change  0:B  1:Y 2 G

# 알람 double click
alarm_popup_name = ""  # 팝업창 이름(더블 클릭한 알람)
# 발생한 알람 리스트 및 알람 변수와 des 매핑
alarm_occur_list = ['KLAMPO268', 'KLAMPO269']     # 'KLAMPO268' CNS 변수로 입력됨.
alarm_des_mapping = alarm_pd                      # 'KLAMPO268':'L/D HX outlet flow hi' 으로 구성된 dict
