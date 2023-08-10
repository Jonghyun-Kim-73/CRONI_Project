
ab_pro = {
    'Normal: 정상': {
        '긴급조치': False, '방사선': False,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '정상 :    ',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': '정상 :',
            }
        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': '정상 :',
            }
        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': '정상 : ',
            }
        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '정상 : ',
            }
        },
    },
    'Ab15_08: 증기발생기 수위 채널 고장 (고)': {
        '긴급조치': False, '방사선': False,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 SG 수위제어계통의 제어 채널 비정상 발생 시 신속한 조치를 통해 SG 수위를 복구하기 위한 절차임.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : 선택되지 않은 SG 수위 채널 고장 시는 경보만 발생',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': '해당 ‘SG WTR LEVEL DEVIATION HIGH/LOW’ 경보 발생(NR 50±5 %)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': '해당 ‘SG  WTR LEVELHIGH-HIGH’ 경보 발생(NR 78 %)',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': '해당 SG 상태등에서 ‘STM GEN CH LEVEL HI-HI’ 점등 (AE-LT476/486/496 : 해당 SG의 CH C 점등)',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': '증기발생기 수위 DCS Monitor에 해당 증기발생기 ‘LVL CH FAIL’ 경보등 점등 및 Buzzer 울림, 경보 프린터 출력',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5',
                'Des': '해당 SG의 ACS/DCS 제어 선택 스위치가 DCS 제어 Mode로 자동 전환 되지 않았거나 서서히 급수유량 감소가 진행되어 즉시 조치하지 않을 경우 아래 사항 진행됨',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5.1',
                'Des': '해당 SG MFCV 닫힘 방향으로 진행 및 해당 SG 실제 급수유량 감소',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5.2',
                'Des': '해당 ‘SG STM/FW FLOW DEVIATION’ 경보 발생(±10 %)',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5.3',
                'Des': '해당 SG 실제 수위 감소 [ZSGLEG1,2,3,으로 확인가능]',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5.4',
                'Des': '해당 ‘SG WTR LEVEL DEVIATION HIGH/LOW’ 경보 발생(NR 50±5%)',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5.5',
                'Des': '해당 ‘해당 ‘SG WATER LEVEL LOW’ 경보 발생(NR 25%)',
            },
            11: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5.6',
                'Des': '해당 SG WTR LEVEL LOW-LOW(NR 17%)에 의한 원자로정지 발생 가능',
            }
        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': '고장 채널 수위 지시치(AE-LI476/486/496, AE-LI473/483/493) 증가',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2',
                'Des': '해당 SG의 ACS/DCS 제어 선택 스위치(AE-HS478/488/498)가 DCS 제어 Mode로 자동 전환 및 해당 SG 수위 정상 복귀',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.3',
                'Des': '해당 SG의 ACS/DCS 제어 선택 스위치(AE-HS478/488/498)가 DCS 제어 Mode로 자동전환되지 않았을 경우 해당 SG 수위 편차 및 실제 수위 감소',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.4',
                'Des': '해당 SG 증기/급수유량 편차 증가',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : MFCV 제어기(AE-FIK478/488/498)를 자동에서 수동 전환 후 요구 신호가   제어 불능 상태로 변하면 즉시 해당 ACS/DCS 선택 스위치에서 MAN.B/U 스위치를 눌러 자동 DCS로 전환한다.',
            }
        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': '증기발생기 제어반(JP007) 경보창에서 해당 경보 확인',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': '고장난 SG 수위 지시계 확인, 선택된 채널 고장일 경우 아래 절차에 따라 확인 및 조치',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3',
                'Des': '해당 SG의 ACS/DCS 제어 선택 스위치(AE-HS478/488/498): ACS → DCS	자동 전환 확인, 전환되지 않았으면 아래 절차에 따라 수동으로 DCS 전환',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3.1',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)를 자동에서 수동으로 전환',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3.2',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498) 요구신호 변화 없으면 비정상 발생 전 요구신호 값으로 복구하여 SG 수위를 안정시킨 후 수동으로 DCS 전환',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.4',
                'Des': '모든 SG 수위가 정상 (50±5%)으로 유지되는지 확인',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.5',
                'Des': '해당 SG 수위 채널 선택스위치(AE-HS478Z/488Z/498Z)를 건전한 채널로 전환 ',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '즉시 고장난 SG 수위 채널 정비 의뢰',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 SG 수위 채널 정비 후, 해당 SG 수위 선택스위치를 정비한 채널 위치로 전환하여 건전성 확인',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.1',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)를 자동에서 수동으로 전환',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)의 요구신호 값이 변하지 않고 해당 SG 수위가 안정 유지되는지 확인',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3',
                'Des': '해당 SG 채널 선택 스위치(AE-HS478Y/488Y/498Y)에서 정비한 수위 채널로 수동 전환',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.4',
                'Des': '해당 SG의 ACS/DCS 제어 선택 스위치(AE-HS478/488/498)를 DCS → ACS로 수동 전환',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.5',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)를 수동에서 자동으로 전환',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.6',
                'Des': '해당 SG 수위 지시계 지시치 정상 복귀 확인',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.7',
                'Des': '해당 SG 수위가 정상(50±5%)으로 유지되는지 확인',
            }

        },
    },
    'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설': {
        '긴급조치': True, '방사선': True,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 충전펌프의 충전용량으로 가압기의 수위를 유지할 수 있는 범위 내에서 원자로냉각재계통 누설고장 발생시 해당 증상, 경보, 자동동작사항 및 조치사항을 기술한다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': '모든 원자로냉각재계통 누설 시 공통적 증상 ',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.1',
                'Des': 'PZR 수위 또는 압력 감소',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '주의사항 : PZR 증기영역 및 계기 접속부에서의 누설 시에는 수위 감소현상은 발생하지 않을 수도 있다. ',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.2',
                'Des': 'VCT 수위 감소 또는 보충횟수 증가',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.3',
                'Des': '발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '참고사항 : 위 사항은 모든 원자로냉각재계통 누설 시의 증상에 공통적으로 적용된다.',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': 'CCW Hx 출구헤더에 설치된 방사선감시기(EG-RE364)의 지시치 증가 및 경보'
                       '- "NON-1E RAD WARN(UA-901-C2)" 또는'
                       '- "NON-1E RAD HIGH ALARM(UA-901-C2)"',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': 'CCW 완충탱크의 수위 증가',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': 'RCP 열방벽(Thermal Barrier) 열교환기 누설 시 RCP 열방벽 열교환기(RCP T/B Hx) 출구온도(전산값) 증가 및 CCW 유량 증가 경보 발생'
                       '- “RCP A THER BARR CLG COIL FLOW HI/LO(UA-907-A1)" 또는'
                       '- “RCP B THER BARR CLG COIL FLOW HI/LO(UA-907-A2)" 또는'
                       '“RCP C THER BARR CLG COIL FLOW HI/LO(UA-907-A3)"',
            }
        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': 'RCP 열방벽 열교환기 출구 ‘고’ 유량(EG-FI435, 433, 431 : 3.78 ℓ/s) 시 해당 RCP 열방벽 열교환기 출구밸브 자동 닫힘',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2',
                'Des': 'RCP 열방벽 열교환기 출구 밸브(EG-FV435, 433, 431) 닫힘으로 인해 RCP 열방벽 열교환기 압력보호밸브(EG-PSV434, 432, 430) 동작으로 격납용기 배수조 수위 증가'
                       '※ EG-PSV434, 432, 430 개방 설정치 : 2500 psig (175.76 kg/㎠)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.3',
                'Des': 'RCP 열방벽 열교환기 누설로 인하여 1차기기 냉각수(CCW) 공통회수관의 유량전송기(EG-FT337) ‘고‘ 유량(13.5 ℓ/s) 시 격납용기 내부 CCW 차단밸브(EG-HV337) 자동 닫힘',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.4',
                'Des': '가압기 수위가 17％ 이하로 감소할 경우 유출수 밸브가(BG-HV001/002/003, BG-LV459/460 ) 자동으로 차단된다.',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.5',
                'Des': 'RCS 압력이 136.78㎏/㎠ 이하가 되면 원자로 트립(Rx Trip)이 발생한다.',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.6',
                'Des': 'RCS 압력이 126.57㎏/㎠ 이하가 되면 안전주입(SI)이 발생한다.',
            }
        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': '가압기 수위유지를 위해 필요할 경우 충전펌프를 추가 기동한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': '가압기 압력유지를 위해 필요할 경우 가압기 보조전열기를 수동 ‘ON‘ 한다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3',
                'Des': '충전펌프 추가기동 및 가압기 전열기 수동투입을 해도 가압기의 수위 및 압력을 유지할 수 없으면 원자로를 수동으로 정지시키고 비상-0(원자로 트립 또는 안전주입) 운전절차에 따른다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.4',
                'Des': '정기-발-13(원자로냉각재계통 누설량 평형점검) 점검 절차서에 따라 원자로냉각재 누설율을 계산한다.',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '참고사항 : 원자로냉각재 누설율이 운영기술지침서에서 정한 제한치 이내 인지 먼저 확인하고, 제한치를 초과하는 경우에는 붙임 6.5(원자로냉각재계통 누설율에 대한 운영기술지침서의 제한치 및 규제사항)의 해당 조치사항을 따른다.',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.5',
                'Des': '누설개소를 확인하고 확인된 누설개소에 대하여 후속 조치 사항사항을 수행한다.',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '1차기기 냉각수 계통으로 누설에 따른 해당 조치사항을 수행한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.1',
                'Des': '차기기 냉각수계통 완충탱크의 수위증가율 등을 감시하고, 누설율을 계산하여 붙임 6.5의 운영기술지침서에 따른다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.2',
                'Des': '1차기기 냉각수계통 열교환기 출구온도, 유량, 방사선계측기, 차단밸브의 조작등을 비교 검토하여 누설되는 위치를 찾아낸다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.3',
                'Des': '1차기기 냉각수계통의 방사성물질에 의한 오염을 최소로 하기 위하여 정상운전중 차단 가능한 곳은 아래의 해당 누설 부위에 따라 즉시 차단한다. ',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '참고사항 : 원자로냉각재가 1차기기 냉각수계통으로 누설 가능한 개소는 다음과 같은 곳이 있다.'
                       '◦ 결함연료 검출계통 시료 냉각기(GFFD Sample Cooler)'
                       '◦ 가압기 액체영역 시료 냉각기(PZR Liquid Sample Cooler)'
                       '◦ 가압기 증기영역 시료 냉각기(PZR Steam Sample Cooler)'
                       '◦ 잔열제거계통 시료 냉각기(RHR Sample Cooler)'
                       '◦ 유출수 열교환기(L/D Hx)'
                       '◦ 예비유출 열교환기(Excess L/D Hx)'
                       '◦ 원자로냉각재펌프 열방벽 열교환기(RCP Thermal Barrier Hx)'
                       ' 잔열제거 열교환기(RHR Hx)',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4',
                'Des': '시료 냉각기에서 누설시',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.1',
                'Des': '결함연료검출계통(GFFD) 시료 냉각기를 차단한다.',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.1.1',
                'Des': 'HI-HV201, HV202, HV101, V001, V002, V003, V029를 닫는다.',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.1.2',
                'Des': 'EG-V142, V156을 닫는다.',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.2',
                'Des': '가압기 액체영역(PZR Liquid) 시료 냉각기를 차단한다.',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.2.1',
                'Des': 'HI-HV203, HV102, V003, V004, V005를 닫는다.',
            },
            11: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.2.2',
                'Des': 'EG-V140, V154를 닫는다.',
            },
            12: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.3',
                'Des': '가압기 증기영역(PZR Steam) 시료 냉각기를 차단한다.',
            },
            13: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.3.1',
                'Des': 'HI-HV204, HV103, V006, V007을 닫는다.',
            },
            14: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.3.2',
                'Des': 'EG-V141, V155를 닫는다.',
            },
            15: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.4',
                'Des': '잔열제거계통(RHR) 시료 냉각기를 차단한다.',
            },
            16: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.4.1',
                'Des': 'HI-HV105, HV208, V059, V060을 닫는다.',
            },
            17: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.4.2',
                'Des': 'EG-V139, V153을 닫는다.',
            },
            18: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.5',
                'Des': '유출수 열교환기(L/D Hx)에서 누설시',
            },
            19: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.5.1',
                'Des': '유출수 오리피스 차단밸브(BG-HV001/002/003)를 먼저 닫고, 유출수 차단밸브(BG-LV459/460)를 닫아 정상유출을 차단시킨다.',
            },
            20: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.5.2',
                'Des': '유출수 열교환기(L/D Hx)의 1차기기 냉각수계통 차단밸브(EG-V094, V095, V096)를 닫아 CCW를 차단시킨다.',
            },
            21: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.5.3',
                'Des': '예비유출유로(Excess L/D Line)를 운전한다.',
            },
            22: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0.0',
                'Des': '주의사항 :  1. 예비유출유로를 운전할 경우 원자로냉각재계통의 수질(용존산소 등) 및 원자로냉각재펌프의 밀봉에 특별한 주의를 요한다.'
                       '2. 원자로냉각재계통의 수질 제한치를 유지할 수 없으면 발전소를 정지한다.',
            },
            23: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.6',
                'Des': '예비유출수 열교환기(Excess L/D Hx)에서 누설시',
            },
            24: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.6.1',
                'Des': '예비유출유로를 차단시킨다.',
            },
            25: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.6.2',
                'Des': '예비 유출수 열교환기에 공급되는 CCW를 차단시킨다.',
            },
            26: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.6.3',
                'Des': '정상유출유로가 운전되고 있지 않으면 정상유출유로를 운전한다.',
            },
            27: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.7',
                'Des': 'RCP 열방벽 열교환기에서 누설시',
            },
            28: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.7.1',
                'Des': 'RCP 열방벽 열교환기의 CCW 차단밸브(EG-FV435/433/431)가 "고"유량에 의해 닫혔는지 확인한다.',
            },
            29: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.7.2',
                'Des': '열교환기 출구의 안전밸브(EG-PSV430, 432, 434) 동작상태를 확인한다. ※ EG-PSV434, 432, 430 개방 설정치 : 2500 psig (175.76 kg/㎠)',
            },
            30: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.7.3',
                'Des': '밀봉수의 공급이 정상인지 확인하고, 하부 베어링온도(전산값)가 107℃ 이하인지 확인한다.',
            },
            31: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.7.4',
                'Des': '비정상-18(원자로냉각재펌프 고장) 운전절차서중 ‘1차기기 냉각수 상실’에 대한  운전절차를 따른다.',
            },
            32: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.8',
                'Des': '잔열제거 열교환기에서 누설시',
            },
            33: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.8.1',
                'Des': '해당 계열의 운전을 정지한다.',
            },
            34: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.8.2',
                'Des': '해당 계열의 CCW를 차단한다.',
            },
            35: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.8.3',
                'Des': '계통-19(잔열제거계통) 운전 절차서에 따라서 건전한 계열을 운전한다.',
            },
            36: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '충전펌프가 추가로 기동된 경우',
            },
            37: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.1',
                'Des': 'VCT 수위를 주의 깊게 감시하고 수위 유지를 위하여 필요한 경우 수동보충을 실시한다.',
            },
            38: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2',
                'Des': '상기의 조치 후에도 VCT 수위가 5% 이하로 감소 시 충전펌프의 흡입이 아래절차에 따라 VCT로부터 RWST로 자동 전환되는지 확인한다.',
            },
            39: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2.1',
                'Des': 'RWST 흡입밸브 (BG-LV115B, LV115D) 열림 확인.',
            },
            40: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2.2',
                'Des': 'VCT 흡입밸브 (BG-LV115C, LV115E) 닫힘 확인.',
            },
            41: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3',
                'Des': '상기 5.1.2항의 자동 유로전환 실패 시 충전펌프의 흡입을 아래절차에 따라 VCT로부터 RWST로 수동으로 전환한다.',
            },
            42: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3.1',
                'Des': 'RWST 흡입밸브 (BG-LV115B, LV115D)를 연다.',
            },
            43: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3.2',
                'Des': 'VCT 흡입밸브 (BG-LV115C, LV115E)를 닫는다.',
            },
            44: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.4',
                'Des': '가압기의 수위 및 압력을 유지할 수 없으면 원자로를 수동으로 정지시키고 비상-0(원자로 트립 또는 안전주입) 운전절차에 따른다.',
            }
        },
    },
    'Ab21_01: 가압기 압력 채널 고장 (고)': {
        '긴급조치': True, '방사선': False,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 가압기(PZR) 압력 제어계통 및 기기의 비정상 증상, 조치사항과 운전 절차를 기술한다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : BB-PT444 고장 ‘고’시 PZR 실제 압력은 급격히 감소한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': 'PZR ‘고’ 압력 지시(BB-PI444)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '2.2',
                'Des': 'PZR 살수밸브(BB-PV444C, 444D) 열림 지시(158.9㎏/㎠)',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '2.3',
                'Des': 'PZR 비례전열기 꺼짐(158.1㎏/㎠)',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': 'PZR 보조전열기 꺼짐(155.9㎏/㎠)',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '2.5',
                'Des': 'PZR PRESS LOW"(BB-PT445) 경보 발생(153.7㎏/㎠) 및 PZR ‘저’ 압력 지시(BB-PI445, 455, 456, 457)',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '2.6',
                'Des': '"PZR LO PRESS INTERLOCK" 경보발생(153.6㎏/㎠) 및 PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '2.7',
                'Des': '"PZR PRESS NOT HI(P-11)" 경보 발생(138.5㎏/㎠)',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '2.8',
                'Des': '"PZR PRESS LOW ALERT" 경보 발생(136.8㎏/㎠) 및 Rx 트립 작동',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.9',
                'Des': '"PZR PRESS LOW SI ALERT" 경보 발생(126.7㎏/㎠) 및 SI 작동',
            }
        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '3.1',
                'Des': 'PZR 전열기 모두 꺼짐(158.1㎏/㎠)',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '3.2',
                'Des': 'PZR 살수밸브(BB-PV444C, 444D) 열림(158.9㎏/㎠)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : 운전원이 계속하여 조치를 취하지 않으면 PZR PORV 차단밸브'
                       '(BB-HV005, 006, 007)는 닫히나 PZR 살수밸브(BB-PV444C,444D)는 계속 열려 다음과 같은 상태가 일어난다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '3.4',
                'Des': 'Rx 트립(136.8㎏/㎠)',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '3.5',
                'Des': 'SI 작동(126.7㎏/㎠)',
            }
        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : PZR 살수밸브(BB-PV444C/444D)가 닫혀 있는지 확인한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '4.1',
                'Des': 'PZR 압력 제어기 BB-PK444A를 수동으로 전환하여 압력을 조절한다. (동시확인)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '4.2',
                'Des': '압력이 회복되어 정상으로 유지되는지 확인한다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '4.3',
                'Des': 'Rx 트립이나 SI가 발생되었으면 비상-0(원자로 트립 또는 SI)를 수행한다.',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': 'PZR 압력이 정상으로 조절되는지 확인한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 압력계기(BB-PT444)는 정비를 의뢰한다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.3',
                'Des': '정비가 완료되면 BB-PK444A를 자동으로 전환한다.',
            }
        },
    },
    'Ab21_02: 가압기 압력 채널 고장 (저)': {
        '긴급조치': True, '방사선': False,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 가압기(PZR) 압력 제어계통 및 기기의 비정상 증상, 조치사항과 운전 절차를 기술한다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : BB-PT444 고장 ‘저’시 PZR 실제 압력은 증가한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': 'PZR ‘저’ 압력 지시(BB-PI444)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': '"PZR PRESS LO/BACKUP HEATERS ON" 경보 발생(155.4㎏/㎠) 및 PZR 보조전열기 모두 켜짐 지시',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': '"PZR PRESS HIGH"(BB-PT444B, 445) 경보 발생(162.4㎏/㎠) 및 PZR ‘고’ 압력 지시(BB-PI445, 455, 456, 457)',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': 'PZR PORV(BB-PV444B, 445A, 445B) 열림 지시 및 경보 발생(164.2㎏/㎠)'
                       '◦ 경보명 : PZR PORV PV-444B OPENING'
                       'PZR PORV PV-445A OPENING'
                       'PZR PORV PV-445B OPENING'
                       'PZR PORV ACTUATION PRESS',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5',
                'Des': '실제 압력 감소로 PZR PORV(BB-PV444B, 445A, 445B) 닫힘',
            }
        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': 'PZR 전열기 모두 켜짐(155.8㎏/㎠)',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2',
                'Des': 'PZR PORV(BB-PV444B, 445A, 445B) 열림(164.2㎏/㎠) 및 닫힘(162.8㎏/㎠) 반복',
            }
        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': 'PZR 압력 제어기 BB-PK444A를 수동으로 전환하여 압력을 조절한다. (동시확인)',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': 'PZR ‘고’ 압력에서 전열기가 켜져 있으면 전열기를 수동으로 꺼준다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3',
                'Des': 'PZR 압력이 정상으로 유지되는지 확인한다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.4',
                'Des': 'PZR PORV(BB-PV444B, 445A, 445B)가 열리지 않도록 압력을 조절한다.',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': 'PZR 압력이 정상으로 조절되는지 확인한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 압력계기(BB-PT444)는 정비를 의뢰한다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.3',
                'Des': '정비가 완료되면 BB-PK444A를 자동으로 전환한다.',
            }

        }
    },
    'Ab20_04: 가압기 수위 채널 고장 (저)': {
        '긴급조치': True, '방사선': False,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 가압기 수위제어계통 및 기기의 비정상시 증상, 자동 동작 사항, 조치 사항 및 운전 절차를 기술한다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': '수위선택스위치(BB-LS459Z)에 BB-LT459가 선택된 경우',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.1',
                'Des': 'BB-LI459 ‘저’ 수위 지시',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.2',
                'Des': '“PZR CONT LVL LOW DEVIATION” 경보 발생(JP006, 기준 수위-5%)',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.3',
                'Des': '“PZR LVL LOW” 및 “PZR CONT LVL LOW HTRS OFF” 경보 발생(JP006, 17%)',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.4',
                'Des': '“LETDN HX OUTLET FLOW LOW” 경보 발생(JP005, 15㎥/hr)',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.5',
                'Des': '“CHARGING LINE FLOW HI/LO” 경보 발생 및 충전 유량 증가 (JP005, Hi. 경보 : 26.57㎥/hr, Lo. 경보 : 4.77㎥/hr)',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.6',
                'Des': '건전한 수위지시계(BB-LI460, 461)의 수위 지시치 증가 [ZPRZNO로 실제 가압기 수위 파악 가능]',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.7',
                'Des': '“PZR CONT LVL HIGH HTRS ON” 경보 발생(JP006, 기준 수위+5%)',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.8',
                'Des': '“PZR LVL HIGH” 경보 발생(JP006, 70%)',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.9',
                'Des': '“PZR HI WTR LVL RX TRIP” 경보 발생 및 원자로 정지(JP006, 92%)',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': '수위선택스위치(BB-LS459Z)에 BB-LT459가 선택되지 않은 경우',
            },
            11: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2.1',
                'Des': 'BB-LI459 ‘저‘ 수위 지시',
            },
            12: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2.2',
                'Des': '“PZR LVL LOW” 경보 발생(JP006, 17%)',
            },
            13: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2.3',
                'Des': '“LETDN HX OUTLET FLOW LOW” 경보 발생(JP005, 15㎥/hr)',
            },
            14: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2.4',
                'Des': '유출관 차단 및 충전 유량 감소로 인해 “CHARGING LINE FLOW HI/LO” 경보 발생(JP005, Hi. 경보 : 26.57㎥/hr, Lo. 경보 : 4.77㎥/hr)',
            },
            15: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '주의사항 : 가압기 수위는 RCP 밀봉주입수에 의해 서서히 증가한다.',
            },
            16: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2.5',
                'Des': '건전한 수위지시계(BB-LI460, 461) 수위 지시치 증가',
            }

        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': '수위선택스위치(BB-LS459Z)에 BB-LT459가 선택된 경우',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.1',
                'Des': '가압기 전열기 꺼짐(17%)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.2',
                'Des': '유출수 오리피스 차단밸브(BG-HV1, 2, 3) 닫힘(17%)',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.3',
                'Des': '유출수 차단밸브(BG-LV459) 닫힘(17%)',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.4',
                'Des': '실제 가압기 수위 증가로 원자로 트립(92%)',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2',
                'Des': '수위선택스위치(BB-LS459Z)에 BB-LT459가 선택되지 않은 경우',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2.1',
                'Des': '유출수 오리피스 차단밸브(BG-HV1, 2, 3) 닫힘(17%)',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2.2',
                'Des': '유출수 차단밸브(BG-LV459) 닫힘',
            }
        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': '수위선택스위치(BB-LS459Z)에 BB-LT459가 선택된 경우',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1.1',
                'Des': '고장 채널 확인'
                       '◦ BB-LI459, 460, 461 상호 비교',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1.2',
                'Des': '유출수 차단 확인',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1.3',
                'Des': '충전유량 차단'
                       '◦ 충전유량제어 밸브(BG-FV122) Close'
                       '◦ 충전관 격리밸브(BG-HV036/037) Close',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1.4',
                'Des': '정비 주관 부서에 긴급 정비 요청',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1.5',
                'Des': '가압기 수위 증가시 예비유출계통을 사용하여 가압기 수위 유지',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': '수위선택스위치(BB-LS459Z)에 BB-LT459가 선택되지 않은 경우',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2.1',
                'Des': '고장 채널 확인'
                       '◦ BB-LI459, 460, 461 상호 비교',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2.2',
                'Des': '유출수 차단 확인',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2.3',
                'Des': '충전유량 차단'
                       '◦ 충전유량제어 밸브(BG-FV122) Close'
                       '◦ 충전관 격리밸브(BG-HV036/037) Close',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2.4',
                'Des': '정비 주관 부서에 긴급 정비 요청',
            },
            11: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2.5',
                'Des': '가압기 수위 증가시 예비유출계통을 사용하여 가압기 수위 유지',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '5.1',
                'Des': '수위기록계(BB-LR459)를 건전한 채널로 선택(BB-LS459Y)',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '5.2',
                'Des': '가압기 수위를 정상 수위로 유지',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '5.3',
                'Des': '운영기술지침서 표 3.3.1-1의 9항에서 정한 최소 운전 가능 채널의 요구 조건 확인 및 조치 수행',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '5.3.1',
                'Des': 'BB-LT459 고장 ‘저’(Fail Low)에 따라 해당 바이스테이블을 트립 모드에 두도록 정비주관부서에 요청하고 상태등 확인',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '5.4',
                'Des': '표준기행-정비-05(정비 작업 처리 관리)에 따라 정비 의뢰',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '5.5',
                'Des': 'BB-LT459의 정비가 완료되면 다음과 같이 계통 정상화',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '5.5.1',
                'Des': '정비 완료된 채널의 바이스테이블을 트립 모드에서 정상 모드로 전환하고 상태등 소등 확인',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '5.5.2',
                'Des': '가압기 수위선택스위치(BB-LS459Z)와 수위기록계(BB-LR459)를 정상 운전시 선택했던 채널로 전환',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '5.5.3',
                'Des': '충전 및 유출 계통을 정상화한다. '
                       '충전 유량 조절 밸브(BG-FV122)를 서서히 열어 충전 유량 형성'
                       '유출수 차단 밸브(BG-LV459, 460) 개방'
                       '고장 전에 운전 중이던 유출수 오리피스 차단밸브 개방(BG-HV1, 2, 3)',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': True, 'Nub': '5.6',
                'Des': '가압기 수위가 정상 수위로 조절되는지 확인한다.',
            }

        }
    },
    'Ab15_07: 증기발생기 수위 채널 고장 (저)': {
        '긴급조치': False, '방사선': False,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 SG 수위제어계통의 제어 채널 비정상 발생 시 신속한 조치를 통해 SG 수위를 복구하기 위한 절차이다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : 선택되지 않은 SG 수위 채널 고장 시는 경보만 발생 ',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': '해당 ‘SG WTR LEVEL DEVIATION HIGH/LOW’ 경보 발생(NR 50±5 %)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': '해당 ‘SG WATER LEVEL LOW’ 경보 발생(NR 25 %)',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': '해당 ‘SG  LOOP WTR LEVEL LOW-LOW’ 경보 발생(NR 17 %)',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': '해당 SG 상태등에서 ‘STM GEN CH LEVEL LO-LO’ 점등 (AE-LT476/486/496, AE-LT473/483/493 : 해당 SG의 CH C, CH D 점등)',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5',
                'Des': '증기발생기 수위 DCS Monitor에 해당 증기발생기 ‘LVL CH FAIL’ 경보등 점등 및 Buzzer 울림, 경보 프린터 출력',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.6',
                'Des': '해당 SG의 ACS/DCS 제어 선택 스위치가 DCS 제어 Mode로 자동 전환 되지 않았거나 서서히 급수유량 증가가 진행되어 즉시 조치하지 않을 경우 아래 사항 진행됨',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.6.1',
                'Des': '해당 SG MFCV 열림 방향으로 진행 및 해당 SG 실제 급수유량 증가',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.6.2',
                'Des': '해당 ‘SG STM/FW FLOW DEVIATION’ 경보 발생(±10 %)',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.6.3',
                'Des': '해당 SG 실제 수위 증가 [ZSGLEG1,2,3,으로 확인가능]',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.6.4',
                'Des': '해당 ‘SG WTR LEVELHIGH-HIGH’에 의한 터빈 정지 및 원자로 정지발생 가능(※ 원자로 출력 30% 이상에서 터빈 트립 시 P-8 신호 발생)',
            }
        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': '고장 채널 수위 지시치(AE-LI476/486/496, AE-LI473/483/493) 감소',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2',
                'Des': '해당 SG의 ACS/DCS 제어 선택 스위치(AE-HS478/488/498)가 DCS 제어 Mode로 자동 전환 및 해당 SG 수위 정상 복귀',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.3',
                'Des': '해당 SG의 ACS/DCS 제어 선택 스위치(AE-HS478/488/498)가 DCS 제어 Mode로 자동전환되지 않았을 경우 해당 SG 수위 편차 및 실제 수위 증가',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.4',
                'Des': '해당 SG 증기/급수유량 편차 증가',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : MFCV 제어기(AE-FIK478/488/498)를 자동에서 수동 전환 후 요구 신호가   제어 불능 상태로 변하면 즉시 해당 ACS/DCS 선택 스위치에서 MAN.B/U 스위치를 눌러 자동 DCS로 전환한다.',
            }
        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': '증기발생기 제어반(JP007) 경보창에서 해당 경보 확인',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': '고장난 SG 수위 지시계 확인, 선택된 채널 고장일 경우 아래 절차에 따라 확인 및 조치 ',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3',
                'Des': '해당 SG의 ACS/DCS 제어 선택 스위치(AE-HS478/488/498): ACS → DCS	자동 전환 확인, 전환되지 않았으면 아래 절차에 따라 수동으로 DCS 전환',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3.1',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)를 자동에서 수동으로 전환',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3.2',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498) 요구신호 변화 없으면 비정상 발생 전 요구신호 값으로 복구하여 SG 수위를 안정시킨 후 수동으로 DCS 전환',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.4',
                'Des': '모든 SG 수위가 정상 (50±5%)으로 유지되는지 확인',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.5',
                'Des': '해당 SG 수위 채널 선택스위치(AE-HS478Z/488Z/498Z)를 건전한 채널로 전환 ',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '즉시 고장난 SG 수위 채널 정비 의뢰',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 SG 수위 채널 정비 후, 해당 SG 수위 선택스위치를 정비한 채널 위치로 전환하여 건전성 확인',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.1',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)를 자동에서 수동으로 전환',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)의 요구신호 값이 변하지 않고 해당 SG 수위가 안정 유지되는지 확인',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3',
                'Des': '해당 SG 채널 선택 스위치(AE-HS478Y/488Y/498Y)에서 정비한 수위 채널로 수동 전환',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.4',
                'Des': '해당 SG의 ACS/DCS 제어 선택 스위치(AE-HS478/488/498)를 DCS → ACS로 수동 전환',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.5',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)를 수동에서 자동으로 전환',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.6',
                'Des': '해당 SG 수위 지시계 지시치 정상 복귀 확인',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.7',
                'Des': '해당 SG 수위가 정상(50±5%)으로 유지되는지 확인',
            }

        }
    },
    'Ab63_04: 제어봉 낙하': {
        '긴급조치': False, '방사선': False,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 발전소 운전중 제어봉 제어계통이 아래와 같이 비정상적일 때의 증상 및 조치사항에 대하여 기술한다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': '제어봉 위치 지시계의 바닥 지시등(RB)점등',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': '원자로 출력 감소',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': 'Tavg의 급격한 감소',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': '“RODS AT BOTTOM” 경보 발생',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5',
                'Des': '“RPI RODDEVIATION 및 ROD DEVIATION” 경보 발생',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.6',
                'Des': '“T REF/AUCT T AVG HIGH" 경보 발생',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.7',
                'Des': '“ROD BANKS LOW/LO-LO LIMIT” 경보 발생',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.8',
                'Des': '“TWO OR MORE RODS AT BOTTOM” 경보 발생(2개 이상 제어봉 낙하시)',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.9',
                'Des': '“ROD CONTROL URGENT FAILURE” 경보 발생',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.10',
                'Des': '“PR UPPER/LOWER HI FLUX DEV/AUTO DEFEAT” 경보 발생',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.11',
                'Des': '“COMPARATOR PWR RANGE DEVIATION” 경보 발생',
            },
            11: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.12',
                'Des': '“DELTA FLUX” 경보 발생',
            },
            12: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.13',
                'Des': '“RADIAL FLUX” 경보 발생',
            },
            13: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.14',
                'Des': '“NIS HI FLUX RATE PWR RANGE" 경보 발생',
            }
        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': '제어봉 제어계통 긴급 고장 경보가 발생',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.1',
                'Des': '제어봉의 자동 및 수동운전 불가능',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.2',
                'Des': '낙하된 제어봉에 의해 원자로 출력감소',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.3',
                'Des': 'Tavg가 감소된 만큼 터빈출력 감발',
            }

        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': '터빈출력을 조절하여 Tavg와 Tref를 일치',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': '축방향 출력편차가 목표치 내에 있는지 확인',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3',
                'Des': '사분출력 경사비를 확인',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.4',
                'Des': '원자로 정지가 발생하면 “비상운전절차서(비상-0 : 원자로 트립 또는 SI)”에 따라 조치',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '1시간 내에 “노심-2-2(정지여유도 계산) 절차서”에 따라 정지여유도 계산',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '1시간 내에 “고리 3,4호기 운영기술지침서 제1편 3.1.1(정지여유도)”에 따라 수행',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.3',
                'Des': '1개의 제어봉이 낙하된 경우 “제어봉 구동장치 작동불능시의 후속 조치사항 5.2.2항” 수행',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.4',
                'Des': '2개 이상의 제어봉이 낙하된 경우 “제어봉 구동장치 작동불능시의 후속 조치사항 5.2.3항” 수행',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.5',
                'Des': '사분출력 경사비를 계산하여 1.02 초과하면 “고리 3,4호기 운영기술지침서 1편 3.2.4(사분출력 경사비)”에 따라 조치',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.6',
                'Des': '필요시 터빈출력을 감발하여 Tavg와 Tref를 일치시킴',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7',
                'Des': '고리3,4,호기 운영기술지침서상 계속적인 출력운전이 허용되면 낙하된 제어봉을 다음 순서에 따라 인출',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : 운전원은 모든 핵계측 장치를 주의 깊게 감시',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.1',
                'Des': '발전소가 안정상태를 유지하면 제어봉 제어선택스위치를 낙하된 제어봉 뱅크에 선택',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.2',
                'Des': '낙하된 제어봉을 제외한 해당 뱅크 모든 제어봉의 올림권선(Lift Coil)을 개방(ROD DISCONNECTED)위치로 전환 (ZJ-P045)',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.3',
                'Des': '낙하된 제어봉 뱅크의 해당그룹 스텝 계수기 위치를 기록',
            },
            11: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.4',
                'Des': '낙하된 제어봉 뱅크의 해당그룹 스텝 계수기 위치를 ‘0’으로 조정',
            },
            12: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '주의사항 : 동일 뱅크의 반대 그룹(예 : 1AC 낙하시 2AC)의 스텝 계수기 위치는 조정할 필요 없음',
            },
            13: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.5',
                'Des': '낙하된 제어봉이 출력제어군(Control Bank)에 속하면 다음 방법에 따라 해당펄스-아날로그 변환기를 ‘0’으로 조정'
                       '1) 펄스-아날로그 변환기의 디지털 표시 스위치를 해당뱅크에 선택'
                       '2) 자동-수동 스위치를 수동으로 전환하고, 해당 뱅크의 디지털 표시가 ‘0’이 될 때까지 반복해서 하향(Down) 스위치 누름'
                       '3) 자동-수동 스위치를 놓아 자동으로 전환',
            },
            14: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '주의사항 : 자동/수동 선택스위치는 스프링 복귀형태이므로, 수동위치에서 계속 누르고 있어야 함',
            },
            15: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '주의사항 : “ROD BANKS LOW/LO-LO LIMIT” 경보 발생할 수 있음',
            },
            16: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.6',
                'Des': '제어봉 제어계통 긴급고장 경보를 원상복귀',
            },
            17: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '주의사항 : 긴급고장 경보를 원상복구하기 전 반드시 정지권선의 여자상태 확인',
            },
            18: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.7',
                'Des': '스텝 계수기 및 제어봉 위치 지시계를 감시하면서 제어봉을 약 6스텝 정도 인출',
            },
            19: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '주의사항 : 2스텝 정도 인출시 제어봉 제어계통 긴급고장 경보가 발생함'
                       '이유) 반대 그룹의 올림권선이 개방(ROD DISCONNECTED) 위치로 전환되어 있어, 전력함에 전류 신호가 공급되지 않음',
            },
            20: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.8',
                'Des': '낙하된 제어봉이 움직이지 않으면 다음사항에 따라 조치'
                       '1) 절차 5.7.2항에서 개방(ROD DISCONNECTED)위치로 전환했던 모든 올림 권선을 투입(ROD CONNECTED)위치로 전환 (ZJ-P045)'
                       '2) 낙하된 제어봉 그룹의 스텝계수기를 초기 기록된 위치로 원상복귀'
                       '3) 낙하된 제어봉이 출력 제어군이면 해당 뱅크의 펄스-아날로그 변환기를 초기 기록된 위치로 원상복귀'
                       '4) 제어봉 선택스위치를 수동 또는 자동으로 위치'
                       '5) “제어봉 구동장치 작동불능시의 후속 조치 사항 5.0항”을 수행',
            },
            21: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.9',
                'Des': '스텝 계수기 및 제어봉 위치 지시계를 감시하면서 초기 기록된 위치까지 낙하된 제어봉을 인출',
            },
            22: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '주의사항 : 낙하된 제어봉을 인출할 때 사분출력 경사비를 계속 감시',
            },
            23: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.10',
                'Des': 'Tavg가 증가하면 터빈출력을 증가 시키거나 붕소주입을 실시하여, Tref와 Tavg를 일치시킴',
            },
            24: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.11',
                'Des': '제어봉 위치 지시계를 이용하여 낙하된 제어봉이 동일 그룹의 다른 제어봉들과 같은 위치인지 확인',
            },
            25: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.12',
                'Des': '낙하된 제어봉이 원위치까지 인출되면 개방(ROD DISCONNECTED)위치로 전환했던 모든 제어봉의 올림권선을 투입(ROD CONNECTED)위치로 전환',
            },
            26: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.13',
                'Des': '제어봉 제어계통 긴급 고장 경보를 원상복귀',
            },
            27: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.14',
                'Des': '낙하된 제어봉에 의해 발생되었던 경보들이 원상복귀 되었는지 확인',
            },
            28: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.15',
                'Des': '다음 사항들이 정상으로 회복되었는가를 확인'
                       '1) 4개 채널간 원자로 출력영역 계측기 정상 확인'
                       '2) 각 유로간 평균온도와 ΔT의 지시상태'
                       '3) 각 유로간 급수와 증기유량의 지시상태'
                       '4) 노심출구 열전대를 이용한 제어봉 위치이상 여부확인 및 사분출력 경사비1.02이내 확인'
                       '5) 축방향 출력 편차가 제어범위이내 지시',
            },
            29: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.16',
                'Des': '제어봉 제어선택스위치를 자동으로 전환',
            },
            30: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.7.17',
                'Des': '발전소가 안정상태를 유지하면 필요시 다음과 같은 사항 확인'
                       '1) 제어군 제어선택스위치를 낙하되었던 뱅크에 선택'
                       '2) 제어봉 위치 지시계를 보면서 서서히 제어봉을 삽입하여 낙하되었던 제어봉 위치가 다른 제어봉 위치와 같이 정상적으로 움직이는지 확인'
                       '3) 동일 뱅크의 그룹간 스텝계수기 위치가 한 스텝 차이로 전환되는지 확인'
                       '4) 제어봉 제어선택 스위치를 자동으로 전환',
            }

        }
    },
    'Ab63_02: 제어봉의 계속적인 삽입': {
        '긴급조치': False, '방사선': False,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 발전소 운전중 제어봉 제어계통이 아래와 같이 비정상적일 때의 증상 및 조치사항에 대하여 기술한다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': True, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': '제어봉 위치 지시계와 스텝계수기상의 계속적인 제어봉 삽입',
            },
            1: {
                'SymptomActivate': True, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': '원자로 출력 감소',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': '“T REF/AUCT T AVG HIGH” 경보 발생',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': '“ROD BANKS LOW/LO-LO LIMIT” 경보 발생',
            },
            4: {
                'SymptomActivate': True, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5',
                'Des': '“COMPARATOR PWR RANGE DEVIATION” 경보 발생',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.6',
                'Des': '“PR UPPER/ LOWER HI FLUX DEV/AUTO DEFEAT” 경보 발생',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.7',
                'Des': '“DELTA FLUX” 경보 발생',
            }
        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': '가압기 보조전열기 켜짐'
                       'Group ‘A‘ : BB-HS103			Group ‘B‘ : BB-HS203B'
                       'Group ‘D‘ : BB-HS105			Group ‘E‘ : BB-HS205',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2',
                'Des': '충전 유량 증가',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.3',
                'Des': '가압기 저압력(136.7kg/cm2)이 발생될 경우 원자로가 정지됨',
            }
        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': '터빈런백(OTΔT, OPΔT, 복수펌프 2/4 정지, 주급수펌프 1/3 이상 정지, 가열기배수 펌프 2/2 정지, 고정자냉각수 저유량)에 의한 제어봉의 자동 삽입인지 확인',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': '터빈 런백이 아니면 제어봉 제어 선택스위치를 수동으로 전환',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3',
                'Des': '제어봉이 계속 삽입되어 원자로 정지가 발생하면 “비상운전절차서(비상-0 : 원자로 트립 또는 SI)”에 따라 조치',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.4',
                'Des': '제어봉의 삽입이 멈추면 원인을 규명',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.5',
                'Des': '수동으로 제어봉을 인출하여 Tavg와 Tref를 일치',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '제어봉이 수동 조작에 의해 작동될 때',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.1',
                'Des': '“제어봉 구동장치 작동불능시의 후속 조치 사항 5.1항”을 수행',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '제어봉이 수동 조작에 의해 작동되지 않을 때',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.1',
                'Des': '“제어봉 구동장치 작동불능시의 후속 조치 사항 5.2항”을 수행',
            }

        }
    },
    'Ab21_12: 가압기 PORV (열림)': {
        '긴급조치': True, '방사선': True,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 가압기(PZR) 압력 제어계통 및 기기의 비정상 증상, 조치사항과 운전 절차를 기술한다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': 'PZR PORV(BB-PV444B, 445A, 445B) 열림 지시 및 경보 발생'
                       '◦ BB-HS444B, 445A, 445B 열림 지시'
                       '◦ 경보명 : PZR PORV PV-444B OPENING'
                       'PZR PORV PV-445A OPENING'
                       'PZR PORV PV-445B OPENING'
                       'PZR PORV ACTUATION PRESS'
                       '(BB-PT444B, 445A, 445 : 164.2kg/㎠)',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': 'PZR PORV 출구 고온 지시(BB-TI463/464/466) 및 경보 발생'
                       '◦ 경보명 : PZR PWR RELIEF LN TEMP HIGH',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': 'PZR 저압력/보조전열기 켜짐 지시 및 경보 발생(155.4㎏/㎠)'
                       '◦ 경보명 : PZR PRESS LO/BACKUP HEATERS ON',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': 'PZR 압력 보호채널(BB-PI455, 456, 457) ‘저’ 압력 연동 경보발생(153.6㎏/㎠) 및 PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘'
                       '◦ 경보명 : PZR LO PRESS INTERLOCK',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5',
                'Des': 'PZR ‘저’ 압력 지시(BB-PI444, 445, 455, 456, 457) 및 경보발생(153.6㎏/㎠)'
                       '◦ 경보명 : PZR PRESS LOW(BB-PT445)',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.6',
                'Des': 'PRT 고온(45℃), 고압(0.6㎏/㎠), 고수위(85%) 지시 및 경보 발생'
                       '◦ 경보명 : PZR RELIEF TANK TEMP HIGH'
                       'PZR RELIEF TANK PRESS HIGH'
                       'PZR RELIEF TANK LEVEL HI/LO',
            }
        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': 'PZR 전열기 모두 켜짐(155.4㎏/㎠)',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2',
                'Des': 'PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘(153.6㎏/㎠)',
            }
        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': 'PZR PORV(BB-PV444B, 445A, 445B)중 열린 밸브를 수동으로 닫는다. (독립확인)',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': '수동닫힘이 불가능하면 PZR PORV가 열린 유로의 차단밸브(BB-HV005, 006, 007)를 수동으로 닫는다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3',
                'Des': 'PZR 전열기가 모두 켜져 있는지 확인한다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.4',
                'Des': 'PZR의 압력 강하가 중지되어 압력이 정상으로 회복되는지 확인한다.',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.5',
                'Des': 'Rx 트립이나 SI가 발생되었으면 비상-0(원자로 트립 또는 SI)를 수행한다.',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': 'PRT가 고온(45℃), 고압(0.6㎏/㎠), 고수위(85%)에 도달하면 계통-017(가압기 압력방출탱크 운전)에 따라 조치한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '오동작 기기는 정비를 의뢰한다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.3',
                'Des': '정비가 끝난 기기는 수동에서 자동으로 전환한다.(동시확인)',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.4',
                'Des': '정상으로 압력이 유지되는지 확인한다.',
            }

        }
    },
    'Ab19_02: 가압기 안전밸브 고장': {
        '긴급조치': True, '방사선': True,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 가압기 압력방출밸브(PORV) 및 안전밸브(Safety Valve)의 누설 및 고장 발생시의 증상 및 조치사항을 기술한다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': '가압기 안전밸브 출구 고온 경보(주위온도＋10℃ : JP006)',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': '가압기 안전밸브 출구온도 기록계 지시치 증가(BB-TR465 : JP005)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': '음향감시계기 주의 및 경보(주의 0.062Vrms, 경보 0.125Vrms : JP015)',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': '가압기 보조전열기 지시등 켜짐 및 경보(155.4㎏/㎠ : JP006)',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5',
                'Des': '가압기 저압경보(153.7㎏/㎠ : JP006)',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.6',
                'Des': '가압기 압력방출밸브(PORV) 차단 경보(153.7㎏/㎠ : JP004)',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.7',
                'Des': '가압기 압력방출탱크(PRT) 고압력 경보(0.6㎏/㎠ : JP006)',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.8',
                'Des': '가압기 압력방출탱크(PRT) 고온 경보(45℃ : JP006)',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.9',
                'Des': '가압기 압력방출탱크(PRT) 고수위 경보(85% : JP006)',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.10',
                'Des': '가압기 수위 변화',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '참고사항 : 가압기 수위는 증가하는 것처럼 보일 수도 있다.',
            },
            11: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.11',
                'Des': '충전유량 증가(BG-FI122A : JP001)',
            },
            12: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.12',
                'Des': '체적제어탱크 수위감소 및 원자로보충수 보충횟수 증가',
            }

        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': '가압기 보조전열기 켜짐(155.4㎏/㎠)',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2',
                'Des': '가압기 압력방출밸브의 차단밸브 닫힘(153.7㎏/㎠)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.3',
                'Des': '원자로 트립(136.7㎏/㎠)',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.4',
                'Des': '안전주입 작동(126.6㎏/㎠)',
            }
        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': '원자로냉각재 압력을 운전 가능한 최소 압력까지 내려서 누설이 차단되는지 확인한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': '누설이 차단되면 원자로냉각재 압력을 정상으로 복귀한다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3',
                'Des': '누설이 차단되지 않으면 후속 조치사항에 따른다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.4',
                'Des': '만일 원자로 트립이나 안전주입이 발생되었으면 비상운전 절차서 비상-0(원자로 트립 또는 안전주입)를 수행한다.',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '고리 3,4호기 운영기술지침서 3.4.10항(가압기 안전밸브)의 불만족시 조치사항에 따른다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 안전밸브를 15분 이내에 운전 가능한 상태로 복구 또는 6시간 이내 고온대기 상태로 진입하고 다음 6시간 이내 고온정지로 진입한다.',
            }

        }
    },
    'Ab21_11: 가압기 살수밸브 고장 (열림)': {
        '긴급조치': False, '방사선': True,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 가압기(PZR) 압력 제어계통 및 기기의 비정상 증상, 조치사항과 운전 절차를 기술한다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': 'PZR 살수밸브 ‘열림’ 지시 및 상태 표시등 점등'
                       '◦ 위치 지시등 : BB-ZL444C 또는 BB-ZL444D ‘열림’ 점등'
                       '◦ 상태 표시등(RL-QL-3G)'
                       'PRZR SPRAY V/V BB-PV-444C NOT CLOSED 점등 또는 PRZR SPRAY V/V BB-PV-444D NOT CLOSED 점등',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': 'PZR 보조전열기 켜짐 지시 및 경보 발생(155.4㎏/㎠)'
                       '◦ 보조전열기 A/B/D/E：자동 ‘ON’'
                       '◦ 경보명 : PZR PRESS LO/BACK UP HEATERS ON',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': 'PZR 살수관 온도(BB-TI451/452) 증가',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': 'PZR 저압력 지시(BB-PI444, 445, 455, 456, 457) 및 경보 발생(153.6㎏/㎠)'
                       '◦ 경보명 : PZR PRESS LOW(BB-PT445)',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5',
                'Des': 'PZR 압력 보호채널(BB-PI455, 456, 457) ‘저’ 압력 연동 경보발생(153.6㎏/㎠) 및 PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘'
                       '◦ 경보명 : PZR LO PRESS INTERLOCK',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.6',
                'Des': 'PZR 압력 138.5㎏/㎠(P-11) 이하시 "PZR PRESS NOT HI(P-11)" 경보 발생',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.7',
                'Des': 'PZR 수위 급격한 증가',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.8',
                'Des': 'Rx 트립 작동 및 "PZR PRESS LOW ALERT" 경보 발생(136.8㎏/㎠)',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.9',
                'Des': 'SI 작동 및 "PZR PRESS LOW SI ALERT" 경보 발생(126.7㎏/㎠)',
            }
        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': 'PZR 전열기 모두 켜짐(155.4㎏/㎠)',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2',
                'Des': 'PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘(153.6㎏/㎠)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.3',
                'Des': 'Rx 트립(136.8㎏/㎠)',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.4',
                'Des': 'SI 작동(126.7㎏/㎠)',
            }
        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': 'PZR 전열기 ‘ON’ 확인 및 불만족시 수동으로 켠다.'
                       '◦ 보조전열기 A/B/D/E 및 비례전열기 C : ‘ON’',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': 'PZR 살수밸브가 고장으로 열려 있으면 수동으로 닫는다.(독립확인)'
                       '◦ BB-PK444C/444D 수동 닫음',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3',
                'Des': 'PZR 살수밸브가 닫히지 않으면, 비상제어용 솔레노이드밸브(BB-SV444C/ 444D)의 핸드스위치(BB-HS444C/444D)를 ‘NORMAL’에서 ‘CLOSE’로 전환(비상제어용 솔레노이드 밸브 상태표시등 ‘소등’)하여 살수밸브에 공급되는 제어용 공기를 배기시킨다.(동시확인)',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : PZR 살수밸브가 닫혀 PZR 압력이 회복되면 후속조치사항 5.0을 수행하고, PZR 살수밸브가 닫히지 않으면 절차 4.4항을 계속 수행하여야 한다.',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.4',
                'Des': 'PZR 살수밸브 조작이 수동으로 불가능하면 고장 밸브의 유로를 확인한다.',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : PZR 압력이 급격하게 감소하여 P8 원상복귀 설정치(Rx 출력 28%) 미만으로 도달하기 전에 Rx 트립이 발생될 것으로 예측되면 4.6 및 4.7항의 해당 RCP를 사전에 정지할 수 있다. 이 경우 Rx 트립이 발생되므로 비상-0(원자로 트립 또는 SI)을 수행하여야 한다.',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.5',
                'Des': 'PZR 살수밸브 한 개 이상 열린 상태로 고착되어 압력이 계속 감소될 경우,  Rx 출력을 P8(28%) 미만으로 감발[LO POWER PERMISSIVE(P8) 상태 표시등 점등]한 후 첫 번째 RCP를 정지한다.(동시확인)',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.6',
                'Des': 'Rx 및 TBN 출력을 P7(Rx 출력 8％ 및 TBN 출력 8.72%) 미만으로 감발[LO POWER PERMISSIVE(P7) 상태 표시등 점등]한 후 열린 상태로 고착된 살수밸브와 관련된 두 번째 RCP를 정지한다.(동시확인)',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : Rx 및 TBN 출력이 P7 미만으로 감발된 후 Rx 출력을 6~9%, TBN-GEN 출력을 50MWe 이상에서 유지한다.',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.7',
                'Des': 'PZR 수위의 급격한 상승이 중지되고 안정상태로 유지되는지 확인한다.',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.8',
                'Des': 'PZR 압력 증가에 따라 PZR 밀림관 온도 및 살수관 온도가 PZR 살수밸브 고장 열림 전의 온도로 복귀되는지 확인한다.'
                       '◦ BB-TI450(PZR 밀림관 온도) : 증가되어 복귀'
                       '◦ BB-TI451/452(PZR 살수관 온도) : 감소되어 복귀',
            },
            11: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.9',
                'Des': 'PZR의 압력 강하가 중지되고 정상으로 회복되는지 확인한다.',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': 'PZR 압력이 정상으로 조절되는지 확인한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 기기는 정비를 의뢰한다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.3',
                'Des': 'PZR 살수밸브 비상제어용 솔레노이드밸브(BB-SV444C/444D)의 핸드스위치(BB-HS444C/444D)를 ‘CLOSE’로 전환하였다면, ‘NORMAL’로 전환(비상제어용 솔레노이드 밸브 상태표시등 ‘점등’)하여 살수밸브에 공급되는 제어용 공기를 정상화시킨다.(동시확인)',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.4',
                'Des': '정비가 완료된 PZR 살수밸브(BB-PV444C/444D)를 자동으로 전환한다.',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.5',
                'Des': 'PZR 보조 살수밸브(BG-HV040) 열림으로 인해 PZR 압력이 감소하면, PZR 보조 살수밸브(BG-HV040)를 닫는다.',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.6',
                'Des': 'PZR 보조 살수밸브(BG-HV040)가 닫히지 않으면 계통-020(화학 및 체적제어계통) 절차서에 따라 정상 유출유량을 차단하고, 충전유량을 차단하기 위해 충전유량 제어밸브(BG-FV122) 또는 충전유량 차단밸브(BG-HV036/037)를 닫는다.(독립확인)',
            }

        }
    },
    'Ab60_02: 재생열교환기 전단부위 파열': {
        '긴급조치': True, '방사선': True,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 정상운전 중 유출수 관로 고장으로 인하여 일어나는 계통의 과도 상태를 기술하고, 그 증상을 확실히 감지하여 신속하고 적절한 조치를 취할 수 있도록 하는데 그 목적이 있다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': '유출수 유량지시계(BG-FI150) 지시치 감소 및 유출수 열교환기 출구유량 ‘저’ 경보(15㎥/hr) 발생',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': 'VCT 수위지시계(BG-LI112A/LI115) 지시치 감소 및 다음 증상 발생',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2.1',
                'Des': 'VCT 수위 30% 이하시 원자로보충수계통 ‘자동’ 위치에서 자동 보충',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2.2',
                'Des': 'VCT 수위 20% 이하시 VCT 수위 ‘저’ 경보',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2.3',
                'Des': 'VCT 수위 5% 이하시 충전펌프 흡입원이 VCT에서 RWST로 전환 BG-LV115B/LV115D Open, BG-LV115C/LV115E Close',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': '가압기 수위 ‘저’ 편차 경보(기준수위 - 5%) 발생',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': '가압기 압력 ‘저’ 전열기 작동 경보(155.35kg/㎠) 발생',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5',
                'Des': '가압기 수위 ‘저’ 경보(17%) 및 다음 증상 발생',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5.1',
                'Des': '가압기 모든 전열기 꺼짐',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5.2',
                'Des': '유출수 차단발생(BG-LV459/LV460, BG-HV1/HV2/HV3 닫힘)',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.6',
                'Des': '재생 열교환기 후단 유출수 온도(BG-TI140) 감소',
            },
            11: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.7',
                'Des': '재생 열교환기 후단 충전수 온도(BG-TI123) 감소',
            },
            12: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.8',
                'Des': '격납용기 배수조 수위 증가',
            },
            13: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.9',
                'Des': '격납용기내 방사능준위 증가',
            },
            14: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.10',
                'Des': '격납용기내 습도 증가',
            }

        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': '유출수 열교환기 출구 압력지시계(BG-PI145) 지시치 감소 및 압력조절밸브(BG-PV145) 서서히 닫힘',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2',
                'Des': '유출수 열교환기 출구 온도지시계(BG-TI144) 지시치 감소 및 유출수 열교환기 출구 온도 조절밸브(EG-TV144) 서서히 닫힘',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.3',
                'Des': '가압기 수위 감소에 따라 충전수 유량제어기(BG-FK122) ‘자동’ 상태에서 충전수 유량 조절밸브(BG-FV122) 서서히 열림',
            }

        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : 1. VCT 수위 30% 이하 자동보충 상태에서도 수위복구가 어려우면 수위 감소율을 감안하여 5% 도달 이전이라도 충전펌프의 흡입원을 RWST로 수동 전환한다.'
                       '- 충전펌프 흡입원을 RWST로 수동 전환할 때는 RWST로부터의 흡입밸브(BG-LV115B/LV115D)를 먼저 열고 VCT 출구밸브(BG-LV115C/LV115E)를 닫는다.'
                       '2. 출력 증, 감발중일 경우 즉시 중지하고 현재 출력상태를 유지한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': '원자로보충수계통의 ‘자동’ 위치를 확인하고 VCT 수위가 30%에서 충수가 시작되는지를 확인한 다음 충수가 안되면 즉시 수동으로 충수한다.'
                       '주) VCT 수위가 30% 이상이라도 필요한 경우 수동 보충운전을 수행한다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': '가압기 수위를 유지하기 위해 다음과 같이 유출수계통을 차단한다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2.1',
                'Des': '유출수 오리피스차단밸브(BG-HV1/HV2/HV3)를 닫고 녹색지시등을 확인한다.',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2.2',
                'Des': '유출수 차단밸브(BG-LV459/LV460)를 닫고 녹색지시등을 확인한다.',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3',
                'Des': '가압기 수위가 계속 감소하면 ‘비정상-23(원자로냉각재계통 누설)’ 절차를 수행하고, 감소하지 않으면 다음 절차로 진행한다.',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.4',
                'Des': '가압기 수위가 정상수위(기준수위 ± 5%)로 회복되면 충전수 유량 조절밸브(BG-FV122)를 닫아 충전수를 차단한다',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.5',
                'Des': 'RCP 밀봉주입수 유량 조절밸브(BG-HV186)를 조절하여 각 펌프당 밀봉주입수 유량을 0.5～0.63ℓ/s(8～10gpm)로 맞춘다.',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '가압기 수위 증가를 방지하기 위해 계통-20(화학 및 체적제어계통 운전) 절차서에 따라 잉여유출수계통을 운전한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '파열 부위 정비 후 계통-20(화학 및 체적제어계통 운전) 절차서에 따라 충전 및 유출수계통을 정상화하고, 잉여유출수계통을 차단한다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.3',
                'Des': '충전수 유량 조절밸브(BG-FV122)를 조절하여 가압기 수위를 기준수위 ± 5% 이내로 맞춘 후 ‘자동’으로 전환한다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.4',
                'Des': 'RCP 밀봉주입수 유량 조절밸브(BG-HV186)를 조절하여 각 펌프당 밀봉주입수 유량을 0.5～0.63ℓ/s(8～10gpm)로 맞춘다.',
            }

        }
    },
    'Ab59_02: 충전수 유량조절밸브 후단누설': {
        '긴급조치': True, '방사선': True,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 정상운전 중 충전수 관로 및 그 부속계통의 고장으로 인하여 일어나는 계통의 과도상태를 기술하고, 그 증상을 확실히 감지하여 신속하고 적절한 조치를 취할 수 있도록 하는데 그 목적이 있다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': 'CHG FLOW CONT FLOW HI/LO(JP005)',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': 'PRZR CONT LEVEL LOW DEVIATION(JP006)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': 'VOL CONT TK LEVEL HIGH/LOW(JP005)',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': 'REGEN HX LETDN LINE TEMP HIGH(JP005)',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5',
                'Des': 'RCP SEAL INJ WTR FLOW LOW(JP005)',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.6',
                'Des': '1E RAD WARN ＆ HIGH ALARM(JP004)'
                       'NON-1E RAD WARN ＆ HIGH ALARM(JP004)'
                       '(격납건물:GT-RE001/002/119/211/132/133/220  JP014)'
                       '(보조건물:GL-RE015/069/087  JP014)',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.7',
                'Des': '충전유량 지시계 지시치 증가(BG-FI122A  JP001)',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.8',
                'Des': '가압기 수위 지시계 지시치 감소(BB-LI459A/460/461/460B  JP001/005)',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.9',
                'Des': '체적제어탱크 수위 지시계 지시치 감소(BG-LI115/112A  JP001/005)',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.10',
                'Des': '재생 열교환기 후단 유출수 온도 지시계 지시치 증가(BG-TI140  JP001)'
                       '(재생 열교환기 전단 충전수 관로 누설시)',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.11',
                'Des': '재생 열교환기 후단 충전수 온도 지시계 지시치 감소(BG-TI123  JP001)'
                       '(재생 열교환기 후단 충전수 관로 누설시)  ',
            },
            11: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.12',
                'Des': 'RCP 밀봉수 주입유량 지시계 지시치 감소(BG-FR154A/155A/156A  JP005)',
            },
            12: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.13',
                'Des': '격납건물 외부에서 누설 시 보조건물 배수조 수위 증가',
            },
            13: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.14',
                'Des': '격납건물 내부에서 누설 시 격납건물 배수조 수위 및 온도/습도 증가',
            }

        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': '가압기 수위지시계 및 기록계(BB-LI459A/460, BB-LR459) 지시치 17%이하로 감소되면 다음과 같은 자동 동작이 발생한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.1',
                'Des': '모든 가압기 전열기 꺼짐(OFF)',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.2',
                'Des': '유출수 오리피스차단밸브(BG-HV1/2/3) 자동 닫힘',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.3',
                'Des': '유출수 차단밸브(BG-LV459/460) 자동 닫힘',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.4',
                'Des': '충전수 유량 조절밸브(BG-FV122) 완전 열림',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.5',
                'Des': '유출수 열교환기 출구온도 증가에 따라 기기냉각수 조절밸브(EG-TV144) 서서히 열림',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.6',
                'Des': '저압 유출수 압력조절밸브(BG-PV145) 자동 닫힘',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1.7',
                'Des': '원자로보충수계통의 빈번한 자동 동작',
            }

        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': '원자로 보충수 제어선택스위치(BG-HS71)를 "자동"(AUTO)위치에 놓고 보충수 제어스위치(BG-HS70)를 "시작"(START) 위치에 놓아 체적제어탱크 수위를 정상상태로 회복시킨다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': '유출수 오리피스차단밸브(BG-HV1/BG-HV2/BG-HV3)를 닫고 유출수 차단밸브(BG-LV459/BG-LV460)를 닫음으로써 유출수를 차단한다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3',
                'Des': '충전수 차단밸브(BG-HV36/BG-HV37)를 닫는다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.4',
                'Des': '충전수 유량조절 밸브(BG-FV122)를 서서히 닫는다.',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.5',
                'Des': '초과 유출수 전환밸브(BG-HV43)를 "VCT"위치로 놓는다.',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : 초과 유출수 조절밸브(BG-HV137)를 열 때는 원자로 냉각재 펌프의 밀봉계통으로의 배압효과 때문에 매우 서서히 열어야 한다.',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.6',
                'Des': '초과 유출수 차단밸브(BG-HV41/BG-HV42)를 열고 초과 유출수 조절밸브(BG-HV137)를 서서히 열어 가압기 수위를 유지한다.',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.7',
                'Des': '가압기 수위와 원자로 냉각재 펌프의 밀봉수 유량을 유지하기 위하여 초과 유출수 조절밸브(BG-HV137)를 수시로 조절한다.',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.8',
                'Des': '원자로냉각재펌프 밀봉수 주입유량(BG-FR156A/155A/154A)이 각각 0.5～0.82ℓ/s가 되도록 밀봉수 주입유량 제어밸브(BG-HV186)를 조절한다.',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.9',
                'Des': '방사선비상계획서의 비상 발령기준을 확인 후 필요한 조치를 한다.',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '만약 충전관로의 고장 시 고장난 관로를 차단하여 격리시키고 계통을 정비할 수 있는 조치를 취한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 충전관로의 정비 완료 후 아래 항목에 따라 유출 및 충전유량을 형성시킨다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.1',
                'Des': '격납건물 충전수 차단밸브(BG-HV36/37) 연다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2',
                'Des': '충전수 유량 조절밸브(BG-FV122) 서서히 열어 충전유량을 형성한다.',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3',
                'Des': '유출수 차단밸브(BG-LV459/460) 연다.',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.4',
                'Des': '유출수 오리피스 차단밸브(BG-HV1/2/3) 중 적당한 밸브 1개 열어 유출유량을 형성한다.',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.5',
                'Des': '충전 유량 및 유출 유량이 정상적으로 유지되는 것을 확인한 후 잉여 유출수조절밸브(BG-HV137)를 서서히 닫는다.',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.6',
                'Des': '잉여 유출수 유로밸브(BG-HV41/42) 닫는다.',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.7',
                'Des': 'RCP #1 밀봉 주입수 유량이 0.5～0.82 ℓ/s(8～13 gpm)이 되도록 RCP 밀봉수 주입 조절밸브(BG-HV186)를 조절한다.(BG-FR154A/155A/156A)',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.8',
                'Des': '충전수 유량 제어기(BG-FK122)를 ‘수동‘위치에 놓고 가압기 수위를 원자로 냉각재 평균온도에 따라 프로그램된 수위(22～55.1 %)로 유지한다.',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.9',
                'Des': '가압기 수위(BB-LI459A/460)가 프로그램된 수위(22～55.1%)의 ±3% 이내로 회복되면 충전수 유량 제어기(BG-FK122) ‘자동‘으로 전환한다.',
            }

        }
    },
    'Ab23_01: RCS에서 1차기기 냉각수 계통(CCW)으로 누설': {
        '긴급조치': False, '방사선': True,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 충전펌프의 충전용량으로 가압기의 수위를 유지할 수 있는 범위 내에서 원자로냉각재계통 누설고장 발생시 해당 증상, 경보, 자동동작사항 및 조치사항을 기술한다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': '모든 원자로냉각재계통 누설 시 공통적 증상 ',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.1',
                'Des': 'PZR 수위 또는 압력 감소',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '주의사항 : PZR 증기영역 및 계기 접속부에서의 누설 시에는 수위 감소현상은 발생하지 않을 수도 있다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.2',
                'Des': 'VCT 수위 감소 또는 보충횟수 증가',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.3',
                'Des': '발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '주의사항 : 위 사항은 모든 원자로냉각재계통 누설 시의 증상에 공통적으로 적용된다.',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': 'CV 대기 방사선감시기(GT-RE211) 또는 격납용기 배기계통 방사선감시기(GT-RE119)의 지시치 증가 및 경보',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': 'CV 지역 방사선감시기(GT-RE001, 002, 132, 133, 220)의 지시치증가 및 경보'
                       '- "1E RAD WARN(UA-901-C1)" 또는'
                       '- "1E RAD HIGH ALARM(UA-901-B1)"',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '주의사항 : 각 지역별 구체적 방사선감시기의 현황은 붙임 6.6(계통 및 지역별 방사선 감시기 분포)를 참조한다.',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': 'CV 온도, 습도, 압력이 정상보다 높게 지시',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5',
                'Des': 'CV Sump 수위 증가 및 배수조 펌프의 기동횟수 증가',
            }

        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': '가압기 수위가 17％ 이하로 감소할 경우 유출수 밸브가(BG-HV001/002/003, BG-LV459/460 ) 자동으로 차단된다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2',
                'Des': '격납용기 환기차단 계측설비 관련 방사선감시기(GT-RE001/ 002/119/220)의 고방사선경보가 발생되면 격납용기 환기차단신호(CPIS) 및 주제어실 비상환기신호(CREVS)가 발생된다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.3',
                'Des': 'RCS 압력이 136.78㎏/㎠ 이하가 되면 원자로 트립(Rx Trip)이 발생한다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.4',
                'Des': 'RCS 압력이 126.57㎏/㎠ 이하가 되면 안전주입(SI)이 발생한다.',
            }

        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': '가압기 수위유지를 위해 필요할 경우 충전펌프를 추가 기동한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.2',
                'Des': '가압기 압력유지를 위해 필요할 경우 가압기 보조전열기를 수동 ‘ON‘ 한다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.3',
                'Des': '충전펌프 추가기동 및 가압기 전열기 수동투입을 해도 가압기의 수위 및 압력을 유지할 수 없으면 원자로를 수동으로 정지시키고 비상-0(원자로 트립 또는 안전주입) 운전절차에 따른다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.4',
                'Des': '정기-발-13(원자로냉각재계통 누설량 평형점검) 점검 절차서에 따라 원자로냉각재 누설율을 계산한다.',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0',
                'Des': '참고사항 :  원자로냉각재 누설율이 운영기술지침서에서 정한 제한치 이내 인지 먼저 확인하고, 제한치를 초과하는 경우에는 붙임 6.5(원자로냉각재계통 누설율에 대한 운영기술지침서의 제한치 및 규제사항)의 해당 조치사항을 따른다.',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.5',
                'Des': '누설개소를 확인하고 확인된 누설개소에 대하여 후속 조치 사항을 수행한다.',
            }

        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '격납용기 내로 누설에 따른 해당 조치사항을 수행한다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.1',
                'Des': '격납용기 관련 방사선감시기(GT-RE001, 002, 119, 211, 132, 133, 220)의 경보원인이 원자로냉각재의 누설인지 확인하고 각종 현장계기를 이용해서 누설 장소를 찾아내고 손상된 부분을 가능하면 차단하여 정비한다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.2',
                'Des': 'CV Sump 수위증가율을 감시하고, 정기-발-13(RCS 누설량 평형점검) 점검 절차서에 따라 원자로냉각재 누설율을 계산하여 계산된 누설율이 운영기술지침서에서 정한 제한치 이내인지 확인한다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '참고사항 : 누설율의 제한치는 붙임 6.5(원자로냉각재계통 누설율에 대한 운영기술지침서의 제한치 및 규제사항)을 참조한다.',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.3',
                'Des': '격납용기 내, 외부 누설 없이 배수조 수위가 계속 증가할 경우 배수조로 유입되는 밸브의 Stem Leak-off Line 공통관에서 누출수가 흐르는가를 확인하고 누출수가 확인되면 관련 밸브들의 Stem Leak-off Line을 점검 (촉수점검 등)하여 누설위치를 찾아 정비한다.',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4',
                'Des': '정비 후 CV Sump 수위 증가율 감시, 정기-발-13(RCS 누설량 평형점검)수행 등으로 누설 여부를 재확인한다.',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1.5',
                'Des': '누설이 차단되면 계산된 누설율이 ‘0’으로 접근하고 격납용기 내의 계기가 모두 정상으로 회복되는지 확인한다.',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '충전펌프가 추가로 기동된 경우',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.1',
                'Des': 'VCT 수위를 주의 깊게 감시하고 수위 유지를 위하여 필요한 경우 수동보충을 실시한다.',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '주의사항 : 충전유량을 최대로 하기 위하여 충전펌프의 최소 유량관 차단밸브(BG-HV024/025/026)를 닫아도 되나, 반드시 충분한 유량이 있음을 확인한 후에 닫아 펌프과열을 방지한다.',
            },
            10: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2',
                'Des': '상기의 조치 후에도 VCT 수위가 5% 이하로 감소 시 충전펌프의 흡입이 아래절차에 따라 VCT로부터 RWST로 자동 전환되는지 확인한다.',
            },
            11: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2.1',
                'Des': 'RWST 흡입밸브 (BG-LV115B, LV115D) 열림 확인.',
            },
            12: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2.2',
                'Des': 'VCT 흡입밸브 (BG-LV115C, LV115E) 닫힘 확인.',
            },
            13: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3',
                'Des': '상기 5.1.2항의 자동 유로전환 실패 시 충전펌프의 흡입을 아래절차에 따라 VCT로부터 RWST로 수동으로 전환한다.',
            },
            14: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3.1',
                'Des': 'RWST 흡입밸브 (BG-LV115B, LV115D)를 연다.',
            },
            15: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3.2',
                'Des': 'VCT 흡입밸브 (BG-LV115C, LV115E)를 닫는다.',
            },
            16: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.2.4',
                'Des': '가압기의 수위 및 압력을 유지할 수 없으면 원자로를 수동으로 정지시키고 비상-0(원자로 트립 또는 안전주입) 운전절차에 따른다.',
            }

        }
    },
    'Ab23_06: 증기발생기 전열관 누설': {
        '긴급조치': True, '방사선': True,
        '목적': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.0',
                'Des': '목적 : 이 절차서는 충전펌프의 충전용량으로 가압기의 수위를 유지할 수 있는 범위 내에서 원자로냉각재계통 누설고장 발생시 해당 증상, 경보, 자동동작사항 및 조치사항을 기술한다.',
            },
        },
        '경보 및 증상': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': '모든 원자로냉각재계통 누설 시 공통적 증상 ',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.1',
                'Des': 'PZR 수위 또는 압력 감소',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '주의사항 : PZR 증기영역 및 계기 접속부에서의 누설 시에는 수위 감소현상은 발생하지 않을 수도 있다. ',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.2',
                'Des': 'VCT 수위 감소 또는 보충횟수 증가',
            },
            4: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.1.3',
                'Des': '발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가',
            },
            5: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '0.0.0',
                'Des': '참고사항 : 위 사항은 모든 원자로냉각재계통 누설 시의 증상에 공통적으로 적용된다. ',
            },
            6: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': '복수기 공기추출계통 방사선감시기(CG-RE004/RE013)의 고방사선경보',
            },
            7: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': '증기발생기 취출수계통 및 시료채취계통 방사선감지기(BM-RE410,RC-RE019/029 /039)의 고방사선경보',
            },
            8: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': '증기발생기의 급수 및 증기유량 편차 및 경보 발생',
            },
            9: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '2.5',
                'Des': '주증기관 방사선감지기(AB-RE801A/801B/801C)의 고방사선경보',
            }
        },
        '자동 동작 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.1',
                'Des': '가압기 수위가 17％ 이하로 감소할 경우 유출수 밸브가(BG-HV001/002/003, BG-LV459/460 ) 자동으로 차단된다.',
            },
            1: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.2',
                'Des': '증기발생기 전열관 누설 시 증기발생기 취출수계통 고방사선경보가 발생하면 증기발생기 취출수 차단밸브(BM-HV103/203/303)와 시료채취 차단밸브(BM-HV107/207/307)가 닫히고 동시에 취출수 방사선감시기 시료채취 차단밸브(BM-RV410)가 자동으로 닫힌다.',
            },
            2: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.3',
                'Des': 'RCS 압력이 136.78㎏/㎠ 이하가 되면 원자로 트립(Rx Trip)이 발생한다.',
            },
            3: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '3.4',
                'Des': 'RCS 압력이 126.57㎏/㎠ 이하가 되면 안전주입(SI)이 발생한다.',
            }
        },
        '긴급 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '4.1',
                'Des': '원자로 냉각재가 증기발생기 전열관을 통하여 2차계통으로 누설되고 있으면 정상-76(증기발생기 전열관 누설) 절차서를 수행한다.',
            }
        },
        '후속 조치 사항': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '...',
            }
        }
    },

    'Intermediate range high flux rod stop': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Power range overpower rod stop': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Control bank D full rod withdrawl': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Control bank lo-lo limit': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Two or more rod at bottom': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Axial power distribution limit': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'CCWS outlet temp hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Instrument air press lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'RWST level lo-lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'L/D HX outlet flow lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'L/D HX outlet temp hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'RHX L/D outlet temp hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'VCT level lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'VCT press lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'RCP seal inj wtr flow lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Charging flow cont flow lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Not used': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'L/D HX outlet flow hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'PRZ press lo SI': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'CTMT spray actuated': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'VCT level hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'VCT press hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'CTMT phase B iso actuated': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Charging flow cont flow hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'CTMT sump level hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'CTMT sump level hi-hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'CTMT air temp hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'CTMT moisture hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Rad hi alarm': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'CTMT press hi 1 alert': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'CTMT press hi 2 alert': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'CTMT press hi 3 alert': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Accum. Tk press lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Accum. Tk press hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'PRZ press hi alert': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'PRZ press lo alert': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'PRZ PORV opening': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'PRZ cont level hi heater on': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'PRZ cont level lo heater off': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'PRZ press lo back-up heater on': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Tref/Auct. Tavg Deviation': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'RCS 1,2,3 Tavg hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'RCS 1,2,3 Tavg/auct Tavg hi/lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'RCS 1,2,3 lo flow alert': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'PRT temp hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'PRT press hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'SG 1,2,3 level lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'SG 1,2,3 stm/FW flow deviation': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'RCP 1,2,3 trip': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Condensate stor Tk level lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Condensate stor Tk level lo-lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Condensate stor Tk level hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'MSIV tripped': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'MSL press rate hi steam iso': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'MSL 1,2,3 press rate hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'MSL 1,2,3 press low': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'AFW(MD) actuated': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Condenser level lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'FW pump discharge header press hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'FW pump trip': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'FW temp hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Condensate pump flow lo': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Condenser abs press hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Condenser level hi': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'TBN trip P-4': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'SG 1,2,3 wtr level hi-hi TBN trip': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Condenser vacuum lo TBN trip': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'TBN overspeed hi TBN trip': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
    'Gen. brk open': {
        'Symptom Check': {
            0: {
                'SymptomActivate': False, 'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급 조치 사항': {}, '후속 조치 사항': {}
    },
}
