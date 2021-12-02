ab_pro = {
    'Normal: 정상': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.1',
                'Des': '정상',
            }
        },
        '긴급조치': {

        },
        '후속조치': {

        },
    },
    'Ab15_08: 증기발생기 수위 채널 고장 (고)': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '2.5.1',
                'Des': '해당 SG MFCV 닫힘 방향으로 진행 및 해당 SG 실제 급수유량 감소',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '2.5.2',
                'Des': '해당 ‘SG STM/FW FLOW DEVIATION’ 경보 발생(±10 %)',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '2.5.3',
                'Des': '해당 SG 실제 수위 감소',
            },
            3: {
                'ManClick': False, 'AutoClick': False, 'Nub': '3.4',
                'Des': '해당 SG 증기/급수유량 편차 증가',
            }
        },
        '긴급조치': {


        },
        '후속조치': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '즉시 고장난 SG 수위 채널 정비 의뢰',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 SG 수위 채널 정비 후, 해당 SG 수위 선택스위치를 정비한 채널 위치로 전환하여 건전성 확인',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.1',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)를 자동에서 수동으로 전환',
            },
            3: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)의 요구신호 값이 변하지 않고 해당 SG 수위가 안정 유지되는지 확인',
            },
            4: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3',
                'Des': '해당 SG 채널 선택 스위치(AE-HS478Y/488Y/498Y)에서 정비한 수위 채널로 수동 전환',
            },
            5: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.4',
                'Des': '해당 SG의 ACS/DCS 제어 선택 스위치(AE-HS478/488/498)를 DCS → ACS로 수동 전환',
            },
            6: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.5',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)를 수동에서 자동으로 전환',
            },
            7: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.6',
                'Des': '해당 SG 수위 지시계 지시치 정상 복귀 확인',
            },
            8: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.7',
                'Des': '해당 SG 수위가 정상(50±5%)으로 유지되는지 확인',
            }


        },
    },
    'Ab23_03: CVCS에서 1차기기 냉각수 계통(CCW)으로 누설': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '2.1.1',
                'Des': 'PZR 수위 또는 압력 감소',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '2.1.2',
                'Des': 'VCT 수위 감소 또는 보충횟수 증가',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '2.1.3',
                'Des': '발전소 제반요소의 변동이 없는 상태에서 충전유량의 증가',
            }

        },
        '긴급조치': {

        },
        '후속조치': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '1차기기 냉각수 계통으로 누설에 따른 해당 조치사항을 수행한다.',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.1',
                'Des': '차기기 냉각수계통 완충탱크의 수위증가율 등을 감시하고, 누설율을 계산하여 붙임 6.5의 운영기술지침서에 따른다.',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.2',
                'Des': '1차기기 냉각수계통 열교환기 출구온도, 유량, 방사선계측기, 차단밸브의 조작등을 비교 검토하여 누설되는 위치를 찾아낸다.',
            },
            3: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.3',
                'Des': '1차기기 냉각수계통의 방사성물질에 의한 오염을 최소로 하기 위하여 정상운전중 차단 가능한 곳은 아래의 해당 누설 부위에 따라 즉시 차단한다. ',
            },
            4: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4',
                'Des': '시료 냉각기에서 누설시',
            },
            5: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.1',
                'Des': '결함연료검출계통(GFFD) 시료 냉각기를 차단한다.',
            },
            6: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.1.1',
                'Des': 'HI-HV201, HV202, HV101, V001, V002, V003, V029를 닫는다.',
            },
            7: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.1.2',
                'Des': 'EG-V142, V156을 닫는다.',
            },
            8: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.2',
                'Des': '가압기 액체영역(PZR Liquid) 시료 냉각기를 차단한다.',
            },
            9: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.2.1',
                'Des': 'HI-HV203, HV102, V003, V004, V005를 닫는다.',
            },
            10: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.2.2',
                'Des': 'EG-V140, V154를 닫는다.',
            },
            11: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.3',
                'Des': '가압기 증기영역(PZR Steam) 시료 냉각기를 차단한다.',
            },
            12: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.3.1',
                'Des': 'HI-HV204, HV103, V006, V007을 닫는다.',
            },
            13: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.3.2',
                'Des': 'EG-V141, V155를 닫는다.',
            },
            14: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.4',
                'Des': '잔열제거계통(RHR) 시료 냉각기를 차단한다.',
            },
            15: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.4.1',
                'Des': 'HI-HV105, HV208, V059, V060을 닫는다.',
            },
            16: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4.4.2',
                'Des': 'EG-V139, V153을 닫는다.',
            },
            17: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.5',
                'Des': '유출수 열교환기(L/D Hx)에서 누설시',
            },
            18: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.5.1',
                'Des': '유출수 오리피스 차단밸브(BG-HV001/002/003)를 먼저 닫고, 유출수 차단밸브(BG-LV459/460)를 닫아 정상유출을 차단시킨다.',
            },
            19: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.5.2',
                'Des': '유출수 열교환기(L/D Hx)의 1차기기 냉각수계통 차단밸브(EG-V094, V095, V096)를 닫아 CCW를 차단시킨다.',
            },
            20: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.5.3',
                'Des': '예비유출유로(Excess L/D Line)를 운전한다.',
            },
            21: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.6',
                'Des': '예비유출수 열교환기(Excess L/D Hx)에서 누설시',
            },
            22: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.6.1',
                'Des': '예비유출유로를 차단시킨다.',
            },
            23: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.6.2',
                'Des': '예비 유출수 열교환기에 공급되는 CCW를 차단시킨다.',
            },
            24: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.6.3',
                'Des': '정상유출유로가 운전되고 있지 않으면 정상유출유로를 운전한다.',
            },
            25: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.7',
                'Des': 'RCP 열방벽 열교환기에서 누설시',
            },
            26: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.7.1',
                'Des': 'RCP 열방벽 열교환기의 CCW 차단밸브(EG-FV435/433/431)가 "고"유량에 의해 닫혔는지 확인한다.',
            },
            27: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.7.2',
                'Des': '열교환기 출구의 안전밸브(EG-PSV430, 432, 434) 동작상태를 확인한다. ※ EG-PSV434, 432, 430 개방 설정치 : 2500 psig (175.76 kg/㎠)',
            },
            28: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.7.3',
                'Des': '밀봉수의 공급이 정상인지 확인하고, 하부 베어링온도(전산값)가 107℃ 이하인지 확인한다.',
            },
            29: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.7.4',
                'Des': '비정상-18(원자로냉각재펌프 고장) 운전절차서중 ‘1차기기 냉각수 상실’에 대한  운전절차를 따른다.',
            },
            30: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.8',
                'Des': '잔열제거 열교환기에서 누설시',
            },
            31: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.8.1',
                'Des': '해당 계열의 운전을 정지한다.',
            },
            32: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.8.2',
                'Des': '해당 계열의 CCW를 차단한다.',
            },
            33: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.8.3',
                'Des': '계통-19(잔열제거계통) 운전 절차서에 따라서 건전한 계열을 운전한다.',
            },
            34: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '충전펌프가 추가로 기동된 경우',
            },
            35: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.1',
                'Des': 'VCT 수위를 주의 깊게 감시하고 수위 유지를 위하여 필요한 경우 수동보충을 실시한다.',
            },
            36: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2',
                'Des': '상기의 조치 후에도 VCT 수위가 5% 이하로 감소 시 충전펌프의 흡입이 아래절차에 따라 VCT로부터 RWST로 자동 전환되는지 확인한다.',
            },
            37: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2.1',
                'Des': 'RWST 흡입밸브 (BG-LV115B, LV115D) 열림 확인.',
            },
            38: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2.2',
                'Des': 'VCT 흡입밸브 (BG-LV115C, LV115E) 닫힘 확인.',
            },
            39: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3',
                'Des': '상기 5.1.2항의 자동 유로전환 실패 시 충전펌프의 흡입을 아래절차에 따라 VCT로부터 RWST로 수동으로 전환한다.',
            },
            40: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3.1',
                'Des': 'RWST 흡입밸브 (BG-LV115B, LV115D)를 연다.',
            },
            41: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3.2',
                'Des': 'VCT 흡입밸브 (BG-LV115C, LV115E)를 닫는다.',
            },
            42: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.4',
                'Des': '가압기의 수위 및 압력을 유지할 수 없으면 원자로를 수동으로 정지시키고 비상-0(원자로 트립 또는 안전주입) 운전절차에 따른다.',
            }


        },
    },
    'Ab21_01: 가압기 압력 채널 고장 (고)': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': 'PZR ‘고’ 압력 지시(BB-PI444)',
            },
            1: {
                'ManClick': False, 'AutoClick': True, 'Nub': '2.2',
                'Des': 'PZR 살수밸브(BB-PV444C, 444D) 열림 지시(158.9㎏/㎠)',
            },
            2: {
                'ManClick': False, 'AutoClick': True, 'Nub': '2.3',
                'Des': 'PZR 비례전열기 꺼짐(158.1㎏/㎠)',
            },
            3: {
                'ManClick': False, 'AutoClick': False, 'Nub': '2.4',
                'Des': 'PZR 보조전열기 꺼짐(155.9㎏/㎠)',
            },
            4: {
                'ManClick': False, 'AutoClick': True, 'Nub': '2.5',
                'Des': 'PZR PRESS LOW"(BB-PT445) 경보 발생(153.7㎏/㎠) 및 PZR ‘저’ 압력 지시(BB-PI445, 455, 456, 457)',
            },
            5: {
                'ManClick': False, 'AutoClick': True, 'Nub': '2.6',
                'Des': 'PZR PORV 차단밸브(BB-HV005, 006, 007) 닫힘',
            },
            6: {
                'ManClick': False, 'AutoClick': True, 'Nub': '2.8',
                'Des': '"PZR PRESS LOW ALERT" 경보 발생(136.8㎏/㎠) 및 Rx 트립 작동',
            },
            7: {
                'ManClick': False, 'AutoClick': False, 'Nub': '2.9',
                'Des': '"PZR PRESS LOW SI ALERT" 경보 발생(126.7㎏/㎠) 및 SI 작동',
            },
            8: {
                'ManClick': False, 'AutoClick': True, 'Nub': '3.1',
                'Des': 'PZR 전열기 모두 꺼짐(158.1㎏/㎠)',
            },
            9: {
                'ManClick': False, 'AutoClick': True, 'Nub': '3.2',
                'Des': 'PZR 살수밸브(BB-PV444C, 444D) 열림(158.9㎏/㎠)',
            },
            10: {
                'ManClick': False, 'AutoClick': True, 'Nub': '3.4',
                'Des': 'Rx 트립(136.8㎏/㎠)',
            },
        },
        '긴급조치': {
            0: {
                'ManClick': False, 'AutoClick': True, 'Nub': 'x.1',
                'Des': 'Do ...',
            },
            1: {
                'ManClick': False, 'AutoClick': True, 'Nub': 'x.2',
                'Des': 'Do ...',
            },
        },
        '후속조치': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': 'PZR 압력이 정상으로 조절되는지 확인한다.',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 압력계기(BB-PT444)는 정비를 의뢰한다.',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.3',
                'Des': '정비가 완료되면 BB-PK444A를 자동으로 전환한다.',
            }
        },
    },
    'Ab21_02: 가압기 압력 채널 고장 (저)': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        },
        '긴급조치': {

        },
        '후속조치': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': 'PZR 압력이 정상으로 조절되는지 확인한다.',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 압력계기(BB-PT444)는 정비를 의뢰한다.',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.3',
                'Des': '정비가 완료되면 BB-PK444A를 자동으로 전환한다.',
            }


        }
    },
    'Ab20_04: 가압기 수위 채널 고장 (저)': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        },
        '긴급조치': {

        },
        '후속조치': {
            0: {
                'ManClick': False, 'AutoClick': True, 'Nub': '5.1',
                'Des': '수위기록계(BB-LR459)를 건전한 채널로 선택(BB-LS459Y)',
            },
            1: {
                'ManClick': False, 'AutoClick': True, 'Nub': '5.2',
                'Des': '가압기 수위를 정상 수위로 유지',
            },
            2: {
                'ManClick': False, 'AutoClick': True, 'Nub': '5.3',
                'Des': '운영기술지침서 표 3.3.1-1의 9항에서 정한 최소 운전 가능 채널의 요구 조건 확인 및 조치 수행',
            },
            3: {
                'ManClick': False, 'AutoClick': True, 'Nub': '5.3.1',
                'Des': 'BB-LT459 고장 ‘저’(Fail Low)에 따라 해당 바이스테이블을 트립 모드에 두도록 정비주관부서에 요청하고 상태등 확인',
            },
            4: {
                'ManClick': False, 'AutoClick': True, 'Nub': '5.4',
                'Des': '표준기행-정비-05(정비 작업 처리 관리)에 따라 정비 의뢰',
            },
            5: {
                'ManClick': False, 'AutoClick': True, 'Nub': '5.5',
                'Des': 'BB-LT459의 정비가 완료되면 다음과 같이 계통 정상화',
            },
            6: {
                'ManClick': False, 'AutoClick': True, 'Nub': '5.5.1',
                'Des': '정비 완료된 채널의 바이스테이블을 트립 모드에서 정상 모드로 전환하고 상태등 소등 확인',
            },
            7: {
                'ManClick': False, 'AutoClick': True, 'Nub': '5.5.2',
                'Des': '가압기 수위선택스위치(BB-LS459Z)와 수위기록계(BB-LR459)를 정상 운전시 선택했던 채널로 전환',
            },
            8: {
                'ManClick': False, 'AutoClick': True, 'Nub': '5.5.3',
                'Des': '충전 및 유출 계통을 정상화한다. '
                       '충전 유량 조절 밸브(BG-FV122)를 서서히 열어 충전 유량 형성'
                       '유출수 차단 밸브(BG-LV459, 460) 개방'
                       '고장 전에 운전 중이던 유출수 오리피스 차단밸브 개방(BG-HV1, 2, 3)',
            },
            9: {
                'ManClick': False, 'AutoClick': True, 'Nub': '5.6',
                'Des': '가압기 수위가 정상 수위로 조절되는지 확인한다.',
            }

        }
    },
    'Ab15_07: 증기발생기 수위 채널 고장 (저)': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            },
        },
        '긴급조치': {

        },
        '후속조치': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '즉시 고장난 SG 수위 채널 정비 의뢰',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 SG 수위 채널 정비 후, 해당 SG 수위 선택스위치를 정비한 채널 위치로 전환하여 건전성 확인',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.1',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)를 자동에서 수동으로 전환',
            },
            3: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)의 요구신호 값이 변하지 않고 해당 SG 수위가 안정 유지되는지 확인',
            },
            4: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3',
                'Des': '해당 SG 채널 선택 스위치(AE-HS478Y/488Y/498Y)에서 정비한 수위 채널로 수동 전환',
            },
            5: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.4',
                'Des': '해당 SG의 ACS/DCS 제어 선택 스위치(AE-HS478/488/498)를 DCS → ACS로 수동 전환',
            },
            6: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.5',
                'Des': '해당 MFCV 제어기(AE-FIK478/488/498)를 수동에서 자동으로 전환',
            },
            7: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.6',
                'Des': '해당 SG 수위 지시계 지시치 정상 복귀 확인',
            },
            8: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.7',
                'Des': '해당 SG 수위가 정상(50±5%)으로 유지되는지 확인',
            }

        }
    },
    'Ab63_04: 제어봉 낙하': {
        'Symptom Check': {
            0: { # KLAMPO15
                'ManClick': False, 'AutoClick': False, 'Nub': '2.1',
                'Des': '제어봉 위치 지시계의 바닥 지시등(RB)점등',
            },
            1: { # KBCDO22
                'ManClick': False, 'AutoClick': False, 'Nub': '2.2',
                'Des': '원자로 출력 감소',
            },
            2: { # UAVLEGM
                'ManClick': False, 'AutoClick': False, 'Nub': '2.3',
                'Des': 'Tavg의 급격한 감소',
            },
            3: {  # KLAMPO313
                'ManClick': False, 'AutoClick': False, 'Nub': '2.9',
                'Des': '“T REF/AUCT T AVG HIGH" 경보 발생',
            },
            4: {  # KLAMPO255
                'ManClick': False, 'AutoClick': False, 'Nub': '2.8',
                'Des': '“TWO OR MORE RODS AT BOTTOM” 경보 발생(2개 이상 제어봉 낙하시)',
            },
            5: {  # KBCDO23
                'ManClick': False, 'AutoClick': False, 'Nub': '3.1.2',
                'Des': '“낙하된 제어봉에 의해 원자로 출력감소',
            },
            6: {  # KBCDO22
                'ManClick': False, 'AutoClick': False, 'Nub': '3.1.3',
                'Des': '“Tavg가 감소된 만큼 터빈출력 감발',
            },
        },
        '긴급조치': {

        },
        '후속조치': {
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '1시간 내에 “노심-2-2(정지여유도 계산) 절차서”에 따라 정지여유도 계산',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '1시간 내에 “고리 3,4호기 운영기술지침서 제1편 3.1.1(정지여유도)”에 따라 수행',
            },
            3: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.3',
                'Des': '1개의 제어봉이 낙하된 경우 “제어봉 구동장치 작동불능시의 후속 조치사항 5.2.2항” 수행',
            },
            4: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.4',
                'Des': '2개 이상의 제어봉이 낙하된 경우 “제어봉 구동장치 작동불능시의 후속 조치사항 5.2.3항” 수행',
            },
            5: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.5',
                'Des': '사분출력 경사비를 계산하여 1.02 초과하면 “고리 3,4호기 운영기술지침서 1편 3.2.4(사분출력 경사비)”에 따라 조치',
            },
            6: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.6',
                'Des': '필요시 터빈출력을 감발하여 Tavg와 Tref를 일치시킴',
            },
            7: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7',
                'Des': '고리3,4,호기 운영기술지침서상 계속적인 출력운전이 허용되면 낙하된 제어봉을 다음 순서에 따라 인출',
            },
            8: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.1',
                'Des': '발전소가 안정상태를 유지하면 제어봉 제어선택스위치를 낙하된 제어봉 뱅크에 선택',
            },
            9: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.2',
                'Des': '낙하된 제어봉을 제외한 해당 뱅크 모든 제어봉의 올림권선(Lift Coil)을 개방(ROD DISCONNECTED)위치로 전환 (ZJ-P045)',
            },
            10: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.3',
                'Des': '낙하된 제어봉 뱅크의 해당그룹 스텝 계수기 위치를 기록',
            },
            11: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.4',
                'Des': '낙하된 제어봉 뱅크의 해당그룹 스텝 계수기 위치를 ‘0’으로 조정',
            },
            12: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.5',
                'Des': '낙하된 제어봉이 출력제어군(Control Bank)에 속하면 다음 방법에 따라 해당펄스-아날로그 변환기를 ‘0’으로 조정'
                       '1) 펄스-아날로그 변환기의 디지털 표시 스위치를 해당뱅크에 선택'
                       '2) 자동-수동 스위치를 수동으로 전환하고, 해당 뱅크의 디지털 표시가 ‘0’이 될 때까지 반복해서 하향(Down) 스위치 누름'
                       '3) 자동-수동 스위치를 놓아 자동으로 전환',
            },
            13: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.6',
                'Des': '제어봉 제어계통 긴급고장 경보를 원상복귀',
            },
            14: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.7',
                'Des': '스텝 계수기 및 제어봉 위치 지시계를 감시하면서 제어봉을 약 6스텝 정도 인출',
            },
            15: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.8',
                'Des': '낙하된 제어봉이 움직이지 않으면 다음사항에 따라 조치'
                       '1) 절차 5.7.2항에서 개방(ROD DISCONNECTED)위치로 전환했던 모든 올림 권선을 투입(ROD CONNECTED)위치로 전환 (ZJ-P045)'
                       '2) 낙하된 제어봉 그룹의 스텝계수기를 초기 기록된 위치로 원상복귀'
                       '3) 낙하된 제어봉이 출력 제어군이면 해당 뱅크의 펄스-아날로그 변환기를 초기 기록된 위치로 원상복귀'
                       '4) 제어봉 선택스위치를 수동 또는 자동으로 위치'
                       '5) “제어봉 구동장치 작동불능시의 후속조치사항 5.0항”을 수행',
            },
            16: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.9',
                'Des': '스텝 계수기 및 제어봉 위치 지시계를 감시하면서 초기 기록된 위치까지 낙하된 제어봉을 인출',
            },
            17: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.10',
                'Des': 'Tavg가 증가하면 터빈출력을 증가 시키거나 붕소주입을 실시하여, Tref와 Tavg를 일치시킴',
            },
            18: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.11',
                'Des': '제어봉 위치 지시계를 이용하여 낙하된 제어봉이 동일 그룹의 다른 제어봉들과 같은 위치인지 확인',
            },
            19: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.12',
                'Des': '낙하된 제어봉이 원위치까지 인출되면 개방(ROD DISCONNECTED)위치로 전환했던 모든 제어봉의 올림권선을 투입(ROD CONNECTED)위치로 전환',
            },
            20: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.13',
                'Des': '제어봉 제어계통 긴급 고장 경보를 원상복귀',
            },
            21: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.14',
                'Des': '낙하된 제어봉에 의해 발생되었던 경보들이 원상복귀 되었는지 확인',
            },
            22: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.15',
                'Des': '다음 사항들이 정상으로 회복되었는가를 확인'
                       '1) 4개 채널간 원자로 출력영역 계측기 정상 확인'
                       '2) 각 유로간 평균온도와 ΔT의 지시상태'
                       '3) 각 유로간 급수와 증기유량의 지시상태'
                       '4) 노심출구 열전대를 이용한 제어봉 위치이상 여부확인 및 사분출력 경사비1.02이내 확인'
                       '5) 축방향 출력 편차가 제어범위이내 지시',
            },
            23: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.16',
                'Des': '제어봉 제어선택스위치를 자동으로 전환',
            },
            24: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.7.17',
                'Des': '발전소가 안정상태를 유지하면 필요시 다음과 같은 사항 확인'
                       '1) 제어군 제어선택스위치를 낙하되었던 뱅크에 선택'
                       '2) 제어봉 위치 지시계를 보면서 서서히 제어봉을 삽입하여 낙하되었던 제어봉 위치가 다른 제어봉 위치와 같이 정상적으로 움직이는지 확인'
                       '3) 동일 뱅크의 그룹간 스텝계수기 위치가 한 스텝 차이로 전환되는지 확인'
                       '4) 제어봉 제어선택 스위치를 자동으로 전환',
            }

        }
    },
    'Ab63_02: 제어봉의 계속적인 삽입': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        },
        '긴급조치': {

        },
        '후속조치': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '제어봉이 수동 조작에 의해 작동될 때',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.1',
                'Des': '“제어봉 구동장치 작동불능시의 후속조치사항 5.1항”을 수행',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '제어봉이 수동 조작에 의해 작동되지 않을 때',
            },
            3: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.1',
                'Des': '“제어봉 구동장치 작동불능시의 후속조치사항 5.2항”을 수행',
            }

        }
    },
    'Ab21_12: 가압기 PORV (열림)': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        },
        '긴급조치': {

        },
        '후속조치': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': 'PRT가 고온(45℃), 고압(0.6㎏/㎠), 고수위(85%)에 도달하면 계통-017(가압기 압력방출탱크 운전)에 따라 조치한다.',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '오동작 기기는 정비를 의뢰한다.',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.3',
                'Des': '정비가 끝난 기기는 수동에서 자동으로 전환한다.(동시확인)',
            },
            3: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.4',
                'Des': '정상으로 압력이 유지되는지 확인한다.',
            }

        }
    },
    'Ab19_02: 가압기 안전밸브 고장': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        },
        '긴급조치': {

        },
        '후속조치': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '고리 3,4호기 운영기술지침서 3.4.10항(가압기 안전밸브)의 불만족시 조치사항에 따른다.',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 안전밸브를 15분 이내에 운전 가능한 상태로 복구 또는 6시간 이내 고온대기 상태로 진입하고 다음 6시간 이내 고온정지로 진입한다.',
            }

        }
    },
    'Ab21_11: 가압기 살수밸브 고장 (열림)': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        },
        '긴급조치': {

        },
        '후속조치': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': 'PZR 압력이 정상으로 조절되는지 확인한다.',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 기기는 정비를 의뢰한다.',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.3',
                'Des': 'PZR 살수밸브 비상제어용 솔레노이드밸브(BB-SV444C/444D)의 핸드스위치(BB-HS444C/444D)를 ‘CLOSE’로 전환하였다면, ‘NORMAL’로 전환(비상제어용 솔레노이드 밸브 상태표시등 ‘점등’)하여 살수밸브에 공급되는 제어용 공기를 정상화시킨다.(동시확인)',
            },
            3: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.4',
                'Des': '정비가 완료된 PZR 살수밸브(BB-PV444C/444D)를 자동으로 전환한다.',
            },
            4: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.5',
                'Des': 'PZR 보조 살수밸브(BG-HV040) 열림으로 인해 PZR 압력이 감소하면, PZR 보조 살수밸브(BG-HV040)를 닫는다.',
            },
            5: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.6',
                'Des': 'PZR 보조 살수밸브(BG-HV040)가 닫히지 않으면 계통-020(화학 및 체적제어계통) 절차서에 따라 정상 유출유량을 차단하고, 충전유량을 차단하기 위해 충전유량 제어밸브(BG-FV122) 또는 충전유량 차단밸브(BG-HV036/037)를 닫는다.(독립확인)',
            }

        }
    },
    'Ab60_02: 재생열교환기 전단부위 파열': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        },
        '긴급조치': {

        },
        '후속조치': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '가압기 수위 증가를 방지하기 위해 계통-20(화학 및 체적제어계통 운전) 절차서에 따라 잉여유출수계통을 운전한다.',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '파열 부위 정비 후 계통-20(화학 및 체적제어계통 운전) 절차서에 따라 충전 및 유출수계통을 정상화하고, 잉여유출수계통을 차단한다.',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.3',
                'Des': '충전수 유량 조절밸브(BG-FV122)를 조절하여 가압기 수위를 기준수위 ± 5% 이내로 맞춘 후 ‘자동’으로 전환한다.',
            },
            3: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.4',
                'Des': 'RCP 밀봉주입수 유량 조절밸브(BG-HV186)를 조절하여 각 펌프당 밀봉주입수 유량을 0.5～0.63ℓ/s(8～10gpm)로 맞춘다.',
            }

        }
    },
    'Ab59_02: 충전수 유량조절밸즈 후단누설': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        },
        '긴급조치': {

        },
        '후속조치': {
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '만약 충전관로의 고장 시 고장난 관로를 차단하여 격리시키고 계통을 정비할 수 있는 조치를 취한다.',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '고장난 충전관로의 정비 완료 후 아래 항목에 따라 유출 및 충전유량을 형성시킨다.',
            },
            3: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.1',
                'Des': '격납건물 충전수 차단밸브(BG-HV36/37) 연다.',
            },
            4: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2',
                'Des': '충전수 유량 조절밸브(BG-FV122) 서서히 열어 충전유량을 형성한다.',
            },
            5: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3',
                'Des': '유출수 차단밸브(BG-LV459/460) 연다.',
            },
            6: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.4',
                'Des': '유출수 오리피스 차단밸브(BG-HV1/2/3) 중 적당한 밸브 1개 열어 유출유량을 형성한다.',
            },
            7: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.5',
                'Des': '충전 유량 및 유출 유량이 정상적으로 유지되는 것을 확인한 후 잉여 유출수조절밸브(BG-HV137)를 서서히 닫는다.',
            },
            8: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.6',
                'Des': '잉여 유출수 유로밸브(BG-HV41/42) 닫는다.',
            },
            9: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.7',
                'Des': 'RCP #1 밀봉 주입수 유량이 0.5～0.82 ℓ/s(8～13 gpm)이 되도록 RCP 밀봉수 주입 조절밸브(BG-HV186)를 조절한다.(BG-FR154A/155A/156A)',
            },
            10: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.8',
                'Des': '충전수 유량 제어기(BG-FK122)를 ‘수동‘위치에 놓고 가압기 수위를 원자로 냉각재 평균온도에 따라 프로그램된 수위(22～55.1 %)로 유지한다.',
            },
            11: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.9',
                'Des': '가압기 수위(BB-LI459A/460)가 프로그램된 수위(22～55.1%)의 ±3% 이내로 회복되면 충전수 유량 제어기(BG-FK122) ‘자동‘으로 전환한다.',
            }

        }
    },
    'Ab23_01: RCS에서 1차기기 냉각수 계통(CCW)으로 누설': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        },
        '긴급조치': {

        },
        '후속조치': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1',
                'Des': '격납용기 내로 누설에 따른 해당 조치사항을 수행한다.',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.1',
                'Des': '격납용기 관련 방사선감시기(GT-RE001, 002, 119, 211, 132, 133, 220)의 경보원인이 원자로냉각재의 누설인지 확인하고 각종 현장계기를 이용해서 누설 장소를 찾아내고 손상된 부분을 가능하면 차단하여 정비한다.',
            },
            2: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.2',
                'Des': 'CV Sump 수위증가율을 감시하고, 정기-발-13(RCS 누설량 평형점검) 점검 절차서에 따라 원자로냉각재 누설율을 계산하여 계산된 누설율이 운영기술지침서에서 정한 제한치 이내인지 확인한다.',
            },
            3: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.3',
                'Des': '격납용기 내, 외부 누설 없이 배수조 수위가 계속 증가할 경우 배수조로 유입되는 밸브의 Stem Leak-off Line 공통관에서 누출수가 흐르는가를 확인하고 누출수가 확인되면 관련 밸브들의 Stem Leak-off Line을 점검 (촉수점검 등)하여 누설위치를 찾아 정비한다.',
            },
            4: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.4',
                'Des': '정비 후 CV Sump 수위 증가율 감시, 정기-발-13(RCS 누설량 평형점검)수행 등으로 누설 여부를 재확인한다.',
            },
            5: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.1.5',
                'Des': '누설이 차단되면 계산된 누설율이 ‘0’으로 접근하고 격납용기 내의 계기가 모두 정상으로 회복되는지 확인한다.',
            },
            6: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2',
                'Des': '충전펌프가 추가로 기동된 경우',
            },
            7: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.1',
                'Des': 'VCT 수위를 주의 깊게 감시하고 수위 유지를 위하여 필요한 경우 수동보충을 실시한다.',
            },
            8: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2',
                'Des': '상기의 조치 후에도 VCT 수위가 5% 이하로 감소 시 충전펌프의 흡입이 아래절차에 따라 VCT로부터 RWST로 자동 전환되는지 확인한다.',
            },
            9: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2.1',
                'Des': 'RWST 흡입밸브 (BG-LV115B, LV115D) 열림 확인.',
            },
            10: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.2.2',
                'Des': 'VCT 흡입밸브 (BG-LV115C, LV115E) 닫힘 확인.',
            },
            11: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3',
                'Des': '상기 5.1.2항의 자동 유로전환 실패 시 충전펌프의 흡입을 아래절차에 따라 VCT로부터 RWST로 수동으로 전환한다.',
            },
            12: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3.1',
                'Des': 'RWST 흡입밸브 (BG-LV115B, LV115D)를 연다.',
            },
            13: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.3.2',
                'Des': 'VCT 흡입밸브 (BG-LV115C, LV115E)를 닫는다.',
            },
            14: {
                'ManClick': False, 'AutoClick': False, 'Nub': '5.2.4',
                'Des': '가압기의 수위 및 압력을 유지할 수 없으면 원자로를 수동으로 정지시키고 비상-0(원자로 트립 또는 안전주입) 운전절차에 따른다.',
            }


        }
    },
    'Ab23_06: 증기발생기 전열관 누설': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        },
        '긴급조치': {

        },
        '후속조치': {

        }
    },

    'Intermediate range high flux rod stop': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Power range overpower rod stop': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Control bank D full rod withdrawl': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Control bank lo-lo limit': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Two or more rod at bottom': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Axial power distribution limit': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'CCWS outlet temp hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Instrument air press lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'RWST level lo-lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'L/D HX outlet flow lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'L/D HX outlet temp hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'RHX L/D outlet temp hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'VCT level lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'VCT press lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'RCP seal inj wtr flow lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Charging flow cont flow lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Not used': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'L/D HX outlet flow hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'PRZ press lo SI': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'CTMT spray actuated': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'VCT level hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'VCT press hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'CTMT phase B iso actuated': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Charging flow cont flow hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'CTMT sump level hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'CTMT sump level hi-hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'CTMT air temp hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'CTMT moisture hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Rad hi alarm': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'CTMT press hi 1 alert': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'CTMT press hi 2 alert': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'CTMT press hi 3 alert': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Accum. Tk press lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Accum. Tk press hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'PRZ press hi alert': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'PRZ press lo alert': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'PRZ PORV opening': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'PRZ cont level hi heater on': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'PRZ cont level lo heater off': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'PRZ press lo back-up heater on': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Tref/Auct. Tavg Deviation': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'RCS 1,2,3 Tavg hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'RCS 1,2,3 Tavg/auct Tavg hi/lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'RCS 1,2,3 lo flow alert': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'PRT temp hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'PRT press hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'SG 1,2,3 level lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'SG 1,2,3 stm/FW flow deviation': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'RCP 1,2,3 trip': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Condensate stor Tk level lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Condensate stor Tk level lo-lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Condensate stor Tk level hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'MSIV tripped': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'MSL press rate hi steam iso': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'MSL 1,2,3 press rate hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'MSL 1,2,3 press low': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'AFW(MD) actuated': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Condenser level lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'FW pump discharge header press hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'FW pump trip': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'FW temp hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Condensate pump flow lo': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Condenser abs press hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Condenser level hi': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'TBN trip P-4': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'SG 1,2,3 wtr level hi-hi TBN trip': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Condenser vacuum lo TBN trip': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'TBN overspeed hi TBN trip': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
    'Gen. brk open': {
        'Symptom Check': {
            0: {
                'ManClick': False, 'AutoClick': False, 'Nub': '1.3',
                'Des': '테스트 3',
            }
        }, '긴급조치': {}, '후속조치': {}
    },
}