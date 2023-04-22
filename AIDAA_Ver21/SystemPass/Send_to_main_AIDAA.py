"""
AIDAA(조선대) -> MAIN(조선대)

3개 정보를 보냄.
send_message = 'True/False,메세지1,
                True/False,메세지2,
                True/False,메세지3,'
최대 바이트는 1000 미만으로 설정필요함.                
"""

import socket
import time

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 소켓 선언

main_server_ip = '127.0.0.1'
main_server_port = 7002

cns_time = 0 # 테스트 용. while 문을 10번 순회하였을 때, 메세지 전환용.
trip_time = 10
while True:
    if cns_time < 20:
        # 보내는 메세지 정의
        send_message = 'False,시스템 정상,False,-,False,-,'
        # 받는쪽에서는 메세지 상태(True 또는 False)와 정보(시스템 상태 string 값)을 구분하기 위해서 ',' 쉼표를 사용함.
        # 따라서 보내는 쪽에서도 "상태1,정보1, 상태2, 정보2, 상태3, 정보3," 구조로 보내줘야함. 
        # ! 230420 성승환 박사님과 논의된 사항 : (상태,정보) 3개 정도 ! #
        
        # MAIN으로 메세지를 보냄.
        send_socket.sendto(send_message.encode('utf-8'), (main_server_ip, main_server_port))
        print(f'AIDAA에서 MAIN Server로 메세지[{send_message}]를 보냈습니다.')
    elif 20 <= cns_time < 30:
        # 보내는 쪽에서 사고나 사건이 발생하여 새로운 메세지를 보내주는 경우도 위의 보내주는 메세지와 동일함.
        send_message = f'True,비정상 발생,True,비정상 절차서 AB-00 진단,True,원자로 Trip까지 {trip_time}초 남음.,'
        trip_time = trip_time - 1 if trip_time > 0 else 0

        # MAIN으로 메세지를 보냄.
        send_socket.sendto(send_message.encode('utf-8'), (main_server_ip, main_server_port))
        print(f'AIDAA에서 MAIN Server로 메세지[{send_message}]를 보냈습니다.')
    
    cns_time += 1 # 테스트 용.
    time.sleep(1) # 1초 대기