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

combobox_update = False  # 절차서 combobox 추가위함

# 절차서 name call
call_bottom_name = ""   # 비정상 절차서 명
call_prss_name = ""     # 비정상 절차서 명

# main2 left button click
main2_btn = [0] * 20

# return list
return_list = ['Main']
return_page = False

# 비정상절차서 박스 체크 카운트
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

# 발생한 알람 리스트 및 알람 변수와 des 매핑
alarm_occur_list = ['KLAMPO268', 'KLAMPO269']     # 'KLAMPO268' CNS 변수로 입력됨.
alarm_des_mapping = alarm_pd                      # 'KLAMPO268':'L/D HX outlet flow hi' 으로 구성된 dict
