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
                'ManClick': False, 'AutoClick': False, 'Nub': 'x.1',
                'Des': 'Do ...',
            },
            1: {
                'ManClick': False, 'AutoClick': False, 'Nub': 'x.2',
                'Des': 'Do ...',
            },
        },
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