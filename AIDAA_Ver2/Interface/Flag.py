from AIDAA_Ver2.Interface.Procedure.alarm_procedure import alarm_pd
# FLAG

# 전체 화면 CLOSE
main_close = False

# 화면 Call
call_return = False

call_main = False       # Main 화면
call_prog = False       # 예지 화면
call_prss = False       # 절차서 화면
call_recv = False       # 시스템 복구 화면
call_click = False
# main2 left button click
main2_btn = [0] * 20

# 발생한 알람 리스트 및 알람 변수와 des 매핑
alarm_occur_list = ['KLAMPO268', 'KLAMPO269']     # 'KLAMPO268' CNS 변수로 입력됨.
alarm_des_mapping = alarm_pd                      # 'KLAMPO268':'L/D HX outlet flow hi' 으로 구성된 dict
