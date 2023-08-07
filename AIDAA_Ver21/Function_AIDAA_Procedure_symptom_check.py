from collections import deque
class ProcedureDB:
    def __init__(self, Shmem):
        self.ShMem = Shmem
        self.proceduredb = self.init_procedure_db()
    def update_proceduredb_from_ShMem(self):
        self.proceduredb = self.update_procedure(self.ShMem.get_mem(), self.proceduredb)
    def init_procedure_db(self):
        procedure_dict = {
            'Normal': {0:{'Des': '정상', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '15_08': {0:{'Des': '해당 ‘SG WTR LEVEL DEVIATION HIGH/LOW’ 경보 발생(NR 50±5 %)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1:{'Des': '해당 ‘SG  WTR LEVELHIGH-HIGH’ 경보 발생(NR 78 %)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2:{'Des': '해당 SG 상태등에서 ‘STM GEN CH LEVEL HI-HI’ 점등 (AE-LT476/486/496 : 해당 SG의 CH C 점등)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3:{'Des': '증기발생기 수위 DCS Monitor에 해당 증기발생기 ‘LVL CH FAIL’ 경보등 점등 및 Buzzer 울림, 경보 프린터 출력', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': '해당 SG MFCV 닫힘 방향으로 진행 및 해당 SG 실제 급수유량 감소', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': '해당 ‘SG STM/FW FLOW DEVIATION’ 경보 발생(±10 %)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      6:{'Des': '해당 SG 실제 수위 감소', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      7:{'Des': '해당 ‘SG WATER LEVEL LOW’ 경보 발생(NR 25%)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      8:{'Des': '해당 SG WTR LEVEL LOW-LOW(NR 17%)에 의한 원자로정지 발생 가능', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '23_03': {0:{'Des': 'PZR 수위 또는 압력 감소', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1:{'Des': 'VCT 수위 감소 또는 보충횟수 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2:{'Des': '발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3:{'Des': 'CCW Hx 출구헤더에 설치된 방사선감시기(EG-RE364)의 지시치 증가 및 관련 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': 'CCW 완충탱크의 수위 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': 'RCP 열방벽(Thermal Barrier) 열교환기 누설 시 RCP 열방벽 열교환기(RCP T/B Hx) 출구온도(전산값) 증가 및 CCW 유량 증가 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '21_01': {0:{'Des': 'PZR ‘고’ 압력 지시(BB-PI444)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1:{'Des': 'PZR 살수밸브(BB-PV444C, 444D) 열림 지시(158.9㎏/㎠)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2:{'Des': 'PZR 비례전열기 꺼짐(158.1㎏/㎠)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3:{'Des': 'PZR 보조전열기 꺼짐(155.9㎏/㎠)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': 'PZR PRESS LOW"(BB-PT445) 경보 발생(153.7㎏/㎠) 및 PZR ‘저’ 압력 지시(BB-PI445, 455, 456, 457)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': '"PZR LO PRESS INTERLOCK" 경보발생(153.6㎏/㎠) 및 PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      6:{'Des': '"PZR PRESS NOT HI(P-11)" 경보 발생(138.5㎏/㎠)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      7:{'Des': '"PZR PRESS LOW ALERT" 경보 발생(136.8㎏/㎠) 및 Rx 트립 작동', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      8:{'Des': '"PZR PRESS LOW SI ALERT" 경보 발생(126.7㎏/㎠) 및 SI 작동', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '20_04': {0:{'Des': 'BB-LI459 ‘저’ 수위 지시', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1:{'Des': '“PZR CONT LVL LOW DEVIATION” 경보 발생(JP006, 기준 수위-5%)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2:{'Des': '“PZR LVL LOW” 및 “PZR CONT LVL LOW HTRS OFF” 경보 발생(JP006, 17%)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3:{'Des': '“LETDN HX OUTLET FLOW LOW” 경보 발생(JP005, 15㎥/hr)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': '“CHARGING LINE FLOW HI/LO” 경보 발생 및 충전 유량 증가 (JP005, Hi. 경보 : 26.57㎥/hr, Lo. 경보 : 4.77㎥/hr)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': '건전한 수위지시계(BB-LI460, 461)의 수위 지시치 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      6:{'Des': '“PZR CONT LVL HIGH HTRS ON” 경보 발생(JP006, 기준 수위+5%)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      7:{'Des': '“PZR LVL HIGH” 경보 발생(JP006, 70%)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      8:{'Des': '“PZR HI WTR LVL RX TRIP” 경보 발생 및 원자로 정지(JP006, 92%)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '15_07': {0:{'Des': '해당 ‘SG WTR LEVEL DEVIATION HIGH/LOW’ 경보 발생(NR 50±5 %)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1:{'Des': '해당 ‘SG WATER LEVEL LOW’ 경보 발생(NR 25 %)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2:{'Des': '해당 ‘SG  LOOP WTR LEVEL LOW-LOW’ 경보 발생(NR 17 %)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3:{'Des': '해당 SG 상태등에서 ‘STM GEN CH LEVEL LO-LO’ 점등 (AE-LT476/486/496, AE-LT473/483/493 : 해당 SG의 CH C, CH D 점등)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': '증기발생기 수위 DCS Monitor에 해당 증기발생기 ‘LVL CH FAIL’ 경보등 점등 및 Buzzer 울림, 경보 프린터 출력', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': '해당 SG MFCV 열림 방향으로 진행 및 해당 SG 실제 급수유량 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      6:{'Des': '해당 ‘SG STM/FW FLOW DEVIATION’ 경보 발생(±10 %)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      7:{'Des': '해당 SG 실제 수위 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      8:{'Des': '해당 ‘SG WTR LEVELHIGH-HIGH’에 의한 터빈 정지 및 원자로 정지발생 가능', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '63_04': {0:{'Des': '제어봉 위치 지시계의 바닥 지시등(RB)점등', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1:{'Des': '원자로 출력 감소', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2:{'Des': 'Tavg의 급격한 감소', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3:{'Des': '“RODS AT BOTTOM” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': '“RPI RODDEVIATION 및 ROD DEVIATION” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': '“T REF/AUCT T AVG HIGH" 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      6:{'Des': '“ROD BANKS LOW/LO-LO LIMIT” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      7:{'Des': '“TWO OR MORE RODS AT BOTTOM” 경보 발생(2개 이상 제어봉 낙하시)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      8:{'Des': '“ROD CONTROL URGENT FAILURE” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      9:{'Des': '“PR UPPER/LOWER HI FLUX DEV/AUTO DEFEAT” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      10:{'Des': '“COMPARATOR PWR RANGE DEVIATION” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      11:{'Des': '“DELTA FLUX” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      12:{'Des': '“RADIAL FLUX” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      13:{'Des': '“NIS HI FLUX RATE PWR RANGE" 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '63_02': {0:{'Des': '제어봉 위치 지시계와 스텝계수기상의 계속적인 제어봉 삽입', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1:{'Des': '원자로 출력 감소', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2:{'Des': '“T REF/AUCT T AVG HIGH” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3:{'Des': '“ROD BANKS LOW/LO-LO LIMIT” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': '“COMPARATOR PWR RANGE DEVIATION” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': '“PR UPPER/ LOWER HI FLUX DEV/AUTO DEFEAT” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      6:{'Des': '“DELTA FLUX” 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '21_12': {0:{'Des': 'PZR PORV(BB-PV444B, 445A, 445B) 열림 지시 및 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1:{'Des': 'PZR PORV 출구 고온 지시(BB-TI463/464/466) 및 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2:{'Des': 'PZR 저압력/보조전열기 켜짐 지시 및 경보 발생(155.4㎏/㎠)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3:{'Des': 'PZR 압력 보호채널(BB-PI455, 456, 457) ‘저’ 압력 연동 경보발생(153.6㎏/㎠) 및 PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': 'PZR ‘저’ 압력 지시(BB-PI444, 445, 455, 456, 457) 및 경보발생(153.6㎏/㎠)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': 'PRT 고온(45℃), 고압(0.6㎏/㎠), 고수위(85%) 지시 및 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '19_02': {0:{'Des': '가압기 안전밸브 출구 고온 경보(주위온도＋10℃ : JP006)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1:{'Des': '가압기 안전밸브 출구온도 기록계 지시치 증가(BB-TR465 : JP005)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2:{'Des': '가압기 보조전열기 지시등 켜짐 및 경보(155.4㎏/㎠ : JP006)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3:{'Des': '가압기 저압경보(153.7㎏/㎠ : JP006)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': '가압기 압력방출밸브(PORV) 차단 경보(153.7㎏/㎠ : JP004)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': '가압기 압력방출탱크(PRT) 고압력 경보(0.6㎏/㎠ : JP006)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      6:{'Des': '가압기 압력방출탱크(PRT) 고온 경보(45℃ : JP006)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      7:{'Des': '가압기 압력방출탱크(PRT) 고수위 경보(85% : JP006)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      8:{'Des': '가압기 수위 변화', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      9:{'Des': '충전유량 증가(BG-FI122A : JP001)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      10:{'Des': '체적제어탱크 수위감소 및 원자로보충수 보충횟수 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '21_11': {0:{'Des': 'PZR 살수밸브 ‘열림’ 지시 및 상태 표시등 점등', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1:{'Des': 'PZR 보조전열기 켜짐 지시 및 경보 발생(155.4㎏/㎠)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2:{'Des': 'PZR 살수관 온도(BB-TI451/452) 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3:{'Des': 'PZR 저압력 지시(BB-PI444, 445, 455, 456, 457) 및 경보 발생(153.6㎏/㎠)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': 'PZR 압력 보호채널(BB-PI455, 456, 457) ‘저’ 압력 연동 경보발생(153.6㎏/㎠) 및 PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': 'PZR 압력 138.5㎏/㎠(P-11) 이하시 "PZR PRESS NOT HI(P-11)" 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      6:{'Des': 'PZR 수위 급격한 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      7:{'Des': 'Rx 트립 작동 및 "PZR PRESS LOW ALERT" 경보 발생(136.8㎏/㎠)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      8:{'Des': 'SI 작동 및 "PZR PRESS LOW SI ALERT" 경보 발생(126.7㎏/㎠)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '60_02': {0:{'Des': '유출수 유량지시계(BG-FI150) 지시치 감소 및 유출수 열교환기 출구유량 ‘저’ 경보(15㎥/hr) 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1:{'Des': 'VCT 수위 30% 이하시 원자로보충수계통 ‘자동’ 위치에서 자동 보충', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2:{'Des': 'VCT 수위 20% 이하시 VCT 수위 ‘저’ 경보', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3:{'Des': 'VCT 수위 5% 이하시 충전펌프 흡입원이 VCT에서 RWST로 전환 BG-LV115B/LV115D Open, BG-LV115C/LV115E Close', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': '가압기 수위 ‘저’ 편차 경보(기준수위 - 5%) 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': '가압기 압력 ‘저’ 전열기 작동 경보(155.35kg/㎠) 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      6:{'Des': '가압기 모든 전열기 꺼짐', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      7:{'Des': '유출수 차단발생(BG-LV459/LV460, BG-HV1/HV2/HV3 닫힘)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      8:{'Des': '재생 열교환기 후단 유출수 온도(BG-TI140) 감소', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      9:{'Des': '재생 열교환기 후단 충전수 온도(BG-TI123) 감소', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      10:{'Des': '격납용기 배수조 수위 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      11:{'Des': '격납용기내 방사능준위 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      12:{'Des': '격납용기내 습도 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '59_02': {0:{'Des': 'CHG FLOW CONT FLOW HI/LO(JP005)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1:{'Des': 'PRZR CONT LEVEL LOW DEVIATION(JP006)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2:{'Des': 'VOL CONT TK LEVEL HIGH/LOW(JP005)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3:{'Des': 'REGEN HX LETDN LINE TEMP HIGH(JP005)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': 'RCP SEAL INJ WTR FLOW LOW(JP005)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': 'RAD WARN ＆ HIGH ALARM(JP004)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      6:{'Des': '충전유량 지시계 지시치 증가(BG-FI122A  JP001)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      7:{'Des': '가압기 수위 지시계 지시치 감소(BB-LI459A/460/461/460B  JP001/005)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      8:{'Des': '체적제어탱크 수위 지시계 지시치 감소(BG-LI115/112A  JP001/005)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      9:{'Des': '재생 열교환기 후단 유출수 온도 지시계 지시치 증가(BG-TI140  JP001)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      10:{'Des': '재생 열교환기 후단 충전수 온도 지시계 지시치 감소(BG-TI123  JP001)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      11:{'Des': 'RCP 밀봉수 주입유량 지시계 지시치 감소(BG-FR154A/155A/156A  JP005)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      12:{'Des': '격납건물 외부에서 누설 시 보조건물 배수조 수위 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      13:{'Des': '격납건물 내부에서 누설 시 격납건물 배수조 수위 및 온도/습도 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '23_01': {0:{'Des': 'PZR 수위 또는 압력 감소', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False, 'MV1': deque(maxlen=5), 'MV2': deque(maxlen=5)},
                      1:{'Des': 'VCT 수위 감소 또는 보충횟수 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False, 'MV1': deque(maxlen=5)},
                      2:{'Des': '발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False, 'MV1': deque(maxlen=5)},
                      3:{'Des': 'CV 대기 방사선감시기(GT-RE211) 또는 격납용기 배기계통 방사선감시기(GT-RE119)의 지시치 증가 및 경보', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False, 'MV1': deque(maxlen=5)},
                      4:{'Des': 'CV 지역 방사선감시기(GT-RE001, 002, 132, 133, 220)의 지시치증가 및 경보', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': 'CV 온도, 습도, 압력이 정상보다 높게 지시', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      6:{'Des': 'CV Sump 수위 증가 및 배수조 펌프의 기동횟수 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False, 'MV1': deque(maxlen=5)}},

            '23_06': {0:{'Des': 'PZR 수위 또는 압력 감소', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False, 'MV1': deque(maxlen=5), 'MV2': deque(maxlen=5)},
                      1:{'Des': 'VCT 수위 감소 또는 보충횟수 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False, 'MV1': deque(maxlen=5)},
                      2:{'Des': '발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False, 'MV1': deque(maxlen=5)},
                      3:{'Des': '복수기 공기추출계통 방사선감시기(CG-RE004/RE013)의 고방사선경보', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4:{'Des': '증기발생기 취출수계통 및 시료채취계통 방사선감지기(BM-RE410,RC-RE019/029 /039)의 고방사선경보', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      5:{'Des': '증기발생기의 급수 및 증기유량 편차 및 경보 발생', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      6:{'Des': '주증기관 방사선감지기(AB-RE801A/801B/801C)의 고방사선경보', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},

            '21_02': {0: {'Des': 'PZR ‘저’ 압력 지시(BB-PI444)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      1: {'Des': '"PZR PRESS LO/BACKUP HEATERS ON" 경보 발생(155.4㎏/㎠) 및 PZR 보조전열기 모두 켜짐 지시', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      2: {'Des': '"PZR PRESS HIGH"(BB-PT444B, 445) 경보 발생(162.4㎏/㎠) 및 PZR "고" 압력 지시(BB-PI445, 455, 456, 457)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      3: {'Des': 'PZR PORV(BB-PV444B, 445A, 445B) 열림 지시 및 경보 발생(164.2㎏/㎠)', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False},
                      4: {'Des': '실제 압력 감소로 PZR PORV(BB-PV444B, 445A, 445B) 닫힘', 'Val': '', 'Setpoint': '', 'Unit': '', 'Auto': False}},
        }
        return procedure_dict

    def update_procedure(self, mem, procedure_dict):
        # Ab23_01: RCS에서 1차기기 냉각수 계통(CCW)으로 누설
        # 0: PZR 수위 또는 압력 감소 - 이동평균 활용
        procedure_dict['23_01'][0]['MV1'].append(mem['ZINST63']['Val']/100)
        procedure_dict['23_01'][0]['MV2'].append(mem['PPRZN']['Val'])
        if len(procedure_dict['23_01'][0]['MV1']) == 5:
            procedure_dict['23_01'][0]['Val'] = mem['ZINST63']['Val']/100
            procedure_dict['23_01'][0]['Setpoint'] = sum(procedure_dict['23_01'][0]['MV1'])/5
            procedure_dict['23_01'][0]['Unit'] = '%'
            if mem['ZINST63']['Val']/100 < (sum(procedure_dict['23_01'][0]['MV1'])/5) or mem['PPRZN']['Val'] < (sum(procedure_dict['23_01'][0]['MV2'])/5):
                procedure_dict['23_01'][0]['Auto'] = True
        # 1: VCT 수위 감소 또는 보충횟수 증가
        procedure_dict['23_01'][1]['MV1'].append(mem['ZVCT']['Val'])
        if len(procedure_dict['23_01'][1]['MV1']) == 5:
            procedure_dict['23_01'][1]['Val'] = mem['ZVCT']['Val']
            procedure_dict['23_01'][1]['Setpoint'] = sum(procedure_dict['23_01'][1]['MV1'])/5
            procedure_dict['23_01'][1]['Unit'] = '%'
            if mem['ZVCT']['Val'] < (sum(procedure_dict['23_01'][1]['MV1'])/5):
                procedure_dict['23_01'][1]['Auto'] = True
        # 2: 발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가
        procedure_dict['23_01'][2]['MV1'].append(mem['WCHGNO']['Val'])
        if len(procedure_dict['23_01'][2]['MV1']) == 5:
            procedure_dict['23_01'][2]['Val'] = mem['WCHGNO']['Val']
            procedure_dict['23_01'][2]['Setpoint'] = sum(procedure_dict['23_01'][2]['MV1']) / 5
            procedure_dict['23_01'][2]['Unit'] = 'kg/sec'
            if mem['WCHGNO']['Val'] > (sum(procedure_dict['23_01'][2]['MV1']) / 5):
                procedure_dict['23_01'][2]['Auto'] = True
        # 3: CV 대기 방사선감시기(GT-RE211) 또는 격납용기 배기계통 방사선감시기(GT-RE119)의 지시치 증가 및 경보
        # 4: CV 지역 방사선감시기(GT-RE001, 002, 132, 133, 220)의 지시치증가 및 경보
        procedure_dict['23_01'][3]['MV1'].append(mem['DCTMT']['Val'])
        if len(procedure_dict['23_01'][3]['MV1']) == 5:
            procedure_dict['23_01'][3]['Val'] = mem['DCTMT']['Val']
            procedure_dict['23_01'][4]['Val'] = mem['DCTMT']['Val']
            procedure_dict['23_01'][3]['Setpoint'] = sum(procedure_dict['23_01'][3]['MV1']) / 5
            procedure_dict['23_01'][4]['Setpoint'] = sum(procedure_dict['23_01'][3]['MV1']) / 5
            procedure_dict['23_01'][3]['Unit'] = 'mRem/Hr'
            procedure_dict['23_01'][4]['Unit'] = 'mRem/Hr'
            if mem['DCTMT']['Val'] > (sum(procedure_dict['23_01'][3]['MV1']) / 5) or mem['DCTMT']['Val'] > mem['CRADHI']['Val']:
                procedure_dict['23_01'][3]['Auto'] = True
                procedure_dict['23_01'][4]['Auto'] = True
        # 5: CV 온도, 습도, 압력이 정상보다 높게 지시
        procedure_dict['23_01'][5]['Val'] = mem['UCTMT']['Val']
        procedure_dict['23_01'][5]['Setpoint'] = 0 #todo 정상 상태 평균 값 기재
        procedure_dict['23_01'][5]['Unit'] = '℃'
        if mem['UCTMT']['Val'] > 0 or mem['PCTMT']['Val'] > 0 or mem['HUCTMT']['Val'] > 0:
            procedure_dict['23_01'][5]['Auto'] = True
        # 6: CV Sump 수위 증가 및 배수조 펌프의 기동횟수 증가
        procedure_dict['23_01'][6]['MV1'].append(mem['ZSUMP']['Val'])
        if len(procedure_dict['23_01'][6]['MV1']) == 5:
            procedure_dict['23_01'][6]['Val'] = mem['ZSUMP']['Val']
            procedure_dict['23_01'][6]['Setpoint'] = sum(procedure_dict['23_01'][6]['MV1']) / 5
            procedure_dict['23_01'][6]['Unit'] = 'm'
            if mem['ZSUMP']['Val'] > (sum(procedure_dict['23_01'][6]['MV1']) / 5):
                procedure_dict['23_01'][6]['Auto'] = True

        # Ab23_06: 증기발생기 전열관 누설
        # 0: PZR 수위 또는 압력 감소 - 이동평균 활용
        procedure_dict['23_06'][0]['MV1'].append(mem['ZINST63']['Val'] / 100)
        procedure_dict['23_06'][0]['MV2'].append(mem['PPRZN']['Val'])
        if len(procedure_dict['23_06'][0]['MV1']) == 5:
            procedure_dict['23_06'][0]['Val'] = mem['ZINST63']['Val'] / 100
            procedure_dict['23_06'][0]['Setpoint'] = sum(procedure_dict['23_06'][0]['MV1']) / 5
            procedure_dict['23_06'][0]['Unit'] = '%'
            if mem['ZINST63']['Val'] / 100 < (sum(procedure_dict['23_06'][0]['MV1']) / 5) or mem['PPRZN']['Val'] < (sum(procedure_dict['23_06'][0]['MV2']) / 5):
                procedure_dict['23_06'][0]['Auto'] = True
        # 1: VCT 수위 감소 또는 보충횟수 증가
        procedure_dict['23_06'][1]['MV1'].append(mem['ZVCT']['Val'])
        if len(procedure_dict['23_06'][1]['MV1']) == 5:
            procedure_dict['23_06'][1]['Val'] = mem['ZVCT']['Val']
            procedure_dict['23_06'][1]['Setpoint'] = sum(procedure_dict['23_06'][1]['MV1']) / 5
            procedure_dict['23_06'][1]['Unit'] = '%'
            if mem['ZVCT']['Val'] < (sum(procedure_dict['23_06'][1]['MV1']) / 5):
                procedure_dict['23_06'][1]['Auto'] = True
        # 2: 발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가
        procedure_dict['23_06'][2]['MV1'].append(mem['WCHGNO']['Val'])
        if len(procedure_dict['23_06'][2]['MV1']) == 5:
            procedure_dict['23_06'][2]['Val'] = mem['WCHGNO']['Val']
            procedure_dict['23_06'][2]['Setpoint'] = sum(procedure_dict['23_06'][2]['MV1']) / 5
            procedure_dict['23_06'][2]['Unit'] = 'kg/sec'
            if mem['WCHGNO']['Val'] > (sum(procedure_dict['23_06'][2]['MV1']) / 5):
                procedure_dict['23_06'][2]['Auto'] = True
        # 3: 복수기 공기추출계통 방사선감시기(CG-RE004/RE013)의 고방사선경보
        # 4: 증기발생기 취출수계통 및 시료채취계통 방사선감지기(BM-RE410,RC-RE019/029 /039)의 고방사선경보
        # 5: 증기발생기의 급수 및 증기유량 편차 및 경보 발생
        # 6: 주증기관 방사선감지기(AB-RE801A/801B/801C)의 고방사선경보
        return procedure_dict

    def get_on_procedures(self, name):
        # 각 절차서별 만족한 증상 요건 개수 산출
        return sum([self.proceduredb[name][i]['Auto'] for i in range(len(self.proceduredb[name]))])

    def get_procedures(self, name):
        # 각 절차서별 전체 증상 요건 개수 산출
        return len(self.proceduredb[name].keys())