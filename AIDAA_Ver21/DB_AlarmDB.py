class AlarmDB:
    def __init__(self, Shmem):
        self.ShMem = Shmem
        self.alarmdb = self.init_alarm_db()

    def update_alarmdb_from_ShMem(self):
        self.alarmdb = self.update_alarm(self.ShMem.get_mem(), self.alarmdb)

    def init_alarm_db(self):
        alarm_dict = {
            'KLAMPO251': {'Val': 0, 'Value': 'XPIRM', 'Des': 'Intermediate range high flux rod stop', 'Setpoint': 'CIRFH', 'Unit': 'A', 'System': '제어봉 제어 계통'},
            'KLAMPO252': {'Val': 0, 'Value': 'QPROREL', 'Des': 'Power range overpower rod stop', 'Setpoint': 'CPRFH', 'Unit': '%', 'System': '제어봉 제어 계통'},
            'KLAMPO253': {'Val': 0, 'Value': 'KZBANK4', 'Des': 'Control bank D full rod withdrawl','Setpoint': 220, 'Unit': 'Steps', 'System': '제어봉 제어 계통'},

            # 'KLAMPO254': {'Val': 0, 'Value': 'KZBANK4', 'Des': 'Control bank lo-lo limit', 'Setpoint': 228, 'Unit': 'Steps', 'System': '제어봉 제어 계통'}, #변수 Control Bank D 기준, setpoint 특이 조건, 분할 경보
            'KLAMPO254_1': {'Val': 0, 'Value': 'KZBANK1', 'Des': 'Control bank A lo-lo limit', 'Setpoint': 'KBNKSEL', 'Unit': 'Steps', 'System': '제어봉 제어 계통'}, #변수 Control Bank D 기준, setpoint 특이 조건, 분할 경보
            'KLAMPO254_2': {'Val': 0, 'Value': 'KZBANK2', 'Des': 'Control bank B lo-lo limit', 'Setpoint': 'KBNKSEL', 'Unit': 'Steps', 'System': '제어봉 제어 계통'}, #변수 Control Bank D 기준, setpoint 특이 조건, 분할 경보
            'KLAMPO254_3': {'Val': 0, 'Value': 'KZBANK3', 'Des': 'Control bank C lo-lo limit', 'Setpoint': 'KBNKSEL', 'Unit': 'Steps', 'System': '제어봉 제어 계통'}, #변수 Control Bank D 기준, setpoint 특이 조건, 분할 경보
            'KLAMPO254_4': {'Val': 0, 'Value': 'KZBANK4', 'Des': 'Control bank D lo-lo limit', 'Setpoint': 'KBNKSEL', 'Unit': 'Steps', 'System': '제어봉 제어 계통'}, #변수 Control Bank D 기준, setpoint 특이 조건, 분할 경보


            'KLAMPO255': {'Val': 0, 'Value': 'KZROD1', 'Des': 'Two or more rod at bottom', 'Setpoint': 2, 'Unit': 'EA', 'System': '제어봉 제어 계통'},    #다중 변수 확인(Control Rod별 존재)

            # 'KLAMPO256': {'Val': 0, 'Value': ['CAXOFF', 'CAXOFF'], 'Des': 'Axial power distribution limit', 'Setpoint': ['CAXOFDL', 'CAXOFDL'], 'Unit': ['%', '%'], 'System': '제어봉 제어 계통'},  #Setpoint 값이 서류와 데이터값이 상이합니다. (계산식: CAXOFDL - 0.15)
            'KLAMPO256': {'Val': 0, 'Value': 'CAXOFF', 'Des': 'Axial power distribution limit', 'Setpoint': 'CAXOFDL', 'Unit': '%', 'System': '제어봉 제어 계통'},  #Setpoint 값이 서류와 데이터값이 상이합니다. (계산식: CAXOFDL - 0.15)

            'KLAMPO257': {'Val': 0, 'Value': 'UCCWIN', 'Des': 'CCWS outlet temp hi', 'Setpoint': 'CUCCWH', 'Unit': '℃', 'System': '화학 및 체적 제어계통'},
            'KLAMPO258': {'Val': 0, 'Value': 'PINSTA', 'Des': 'Instrument air press lo', 'Setpoint': 'CINSTP', 'Unit': 'kg/cm²', 'System': '화학 및 체적 제어계통'},
            'KLAMPO259': {'Val': 0, 'Value': 'ZRWST', 'Des': 'RWST level lo-lo', 'Setpoint': 'CZRWSLL', 'Unit': '%', 'System': '화학 및 체적 제어계통'},
            'KLAMPO260': {'Val': 0, 'Value': 'WNETLD', 'Des': 'L/D HX outlet flow lo', 'Setpoint': 'CWLHXL', 'Unit': 'kg/sec', 'System': '화학 및 체적 제어계통'},       # Lee : CVCS Leak 시 동작.
            'KLAMPO261': {'Val': 0, 'Value': 'UNRHXUT', 'Des': 'L/D HX outlet temp hi', 'Setpoint': 'CULDHX', 'Unit': '℃', 'System': '화학 및 체적 제어계통'},    
            'KLAMPO262': {'Val': 0, 'Value': 'URHXUT', 'Des': 'RHX L/D outlet temp hi', 'Setpoint': 'CURHX', 'Unit': '℃', 'System': '화학 및 체적 제어계통'},
            'KLAMPO263': {'Val': 0, 'Value': 'ZVCT', 'Des': 'VCT level lo', 'Setpoint': 'CZVCT2', 'Unit': '%', 'System': '화학 및 체적 제어계통'},
            'KLAMPO264': {'Val': 0, 'Value': 'PVCT', 'Des': 'VCT press lo', 'Setpoint': 'CPVCTL', 'Unit': 'kg/cm²', 'System': '화학 및 체적 제어계통'},

            # 'KLAMPO265': {'Val': 0, 'Value': ['CWRCPSI', 'WRCPSI1', 'WRCPSI2', 'WRCPSI3' ], 'Des': 'RCP seal inj wtr flow lo', 'Setpoint': '0.400000005960464', 'Unit': 'kg/sec'},  # 분할 경보, 다중 변수 확인(RCP,RCP seal별 존재) (원본 경보)
            'KLAMPO265_1': {'Val': 0, 'Value': 'WRCPSI1', 'Des': 'RCP 1 seal inj wtr flow lo', 'Setpoint': 'CWRCPS', 'Unit': 'kg/sec', 'System': '원자로 냉각재 계통'},  # 분할 경보
            'KLAMPO265_2': {'Val': 0, 'Value': 'WRCPSI2', 'Des': 'RCP 2 seal inj wtr flow lo', 'Setpoint': 'CWRCPS', 'Unit': 'kg/sec', 'System': '원자로 냉각재 계통'},  # 분할 경보
            'KLAMPO265_3': {'Val': 0, 'Value': 'WRCPSI3', 'Des': 'RCP 3 seal inj wtr flow lo', 'Setpoint': 'CWRCPS', 'Unit': 'kg/sec', 'System': '원자로 냉각재 계통'},  # 분할 경보

            'KLAMPO266': {'Val': 0, 'Value': 'WCHGNO', 'Des': 'Charging flow cont flow lo', 'Setpoint': 'CWCHGL', 'Unit': 'kg/sec', 'System': '화학 및 체적 제어계통'},  # Lee : CVCS Leak 시 동작.
            'KLAMPO267': {'Val': 0, 'Value': 0, 'Des': 'Not used',  'Setpoint': '', 'Unit': '', 'System': ''}, # Not used
            'KLAMPO268': {'Val': 0, 'Value': 'WNETLD', 'Des': 'L/D HX outlet flow hi', 'Setpoint': 'CWLHXH', 'Unit': 'kg/sec', 'System': '화학 및 체적 제어계통'},

            # 'KLAMPO269': {'Val': 0, 'Value': ['PPRZN', 'KSAFEI'], 'Des': 'PRZ press lo SI', 'Setpoint': [126.44481, 1], 'Unit': ['kg/cm²',''], 'System': '원자로 냉각재 계통'}, #다중 변수 확인(PRZ,SI 조건 2개), KSAFEI=1 조건2개, 12400000Pa -> kg/cm² 단위 변환
            'KLAMPO269_1': {'Val': 0, 'Value': 'PPRZN', 'Des': 'PRZ press lo', 'Setpoint': 126.44481, 'Unit': 'kg/cm²', 'System': '원자로 냉각재 계통'}, #다중 변수 확인(PRZ,SI 조건 2개), KSAFEI=1 조건2개, 12400000Pa -> kg/cm² 단위 변환
            'KLAMPO269_2': {'Val': 0, 'Value': 'KSAFEI', 'Des': 'SI Actuation', 'Setpoint': 1, 'Unit': '', 'System': '원자로 냉각재 계통'}, #다중 변수 확인(PRZ,SI 조건 2개), KSAFEI=1 조건2개, 12400000Pa -> kg/cm² 단위 변환

            'KLAMPO270': {'Val': 0, 'Value': 'KCTMTSP', 'Des': 'CTMT spray actuated', 'Setpoint': 1, 'Unit': '', 'System': '잔열 제거 계통'},
            'KLAMPO271': {'Val': 0, 'Value': 'ZVCT', 'Des': 'VCT level hi', 'Setpoint': 'CZVCT6', 'Unit': '%', 'System': '화학 및 체적 제어계통'},
            'KLAMPO272': {'Val': 0, 'Value': 'PVCT', 'Des': 'VCT press hi', 'Setpoint': 'CPVCTH', 'Unit': 'kg/cm²', 'System': '화학 및 체적 제어계통'},
            'KLAMPO273': {'Val': 0, 'Value': 'KCISOB', 'Des': 'CTMT phase B iso actuated', 'Setpoint': 1, 'Unit': '', 'System': '잔열 제거 계통'},
            'KLAMPO274': {'Val': 0, 'Value': 'WCHGNO', 'Des': 'Charging flow cont flow hi', 'Setpoint': 'CWCHGH', 'Unit': 'kg/sec', 'System': '화학 및 체적 제어계통'},
            # -------------------------------------------------------Trip--------------------------------------------------------------------------------------------
            # Trip 변수 제외
            # 'KLAMPO275': {'Val': 0, 'Value': 'UOVER', 'Des': 'OT DELTA-T RX TRIP', 'Setpoint': '1.08099997043609', 'Unit': '℃'},
            # 'KLAMPO276': {'Val': 0, 'Value': 'QOVER', 'Des': 'OP DELTA-T RX TRIP', 'Setpoint': '1.08780002593994', 'Unit': '%'},
            # 'KLAMPO277': {'Val': 0, 'Value': 'PCTMT', 'Des': 'CTMT PRESS HIGH SI RX TRIP', 'Setpoint': '0.351500004529953', 'Unit': 'kg/cm²'},
            # 'KLAMPO278': {'Val': 0, 'Value': 'KMANRX', 'Des': 'MANUAL RX TRIP', 'Setpoint': '1', 'Unit': '-'},
            # 'KLAMPO279': {'Val': 0, 'Value': 'KMANSI', 'Des': 'MANUAL SI RX TRIP', 'Setpoint': '1', 'Unit': '-'},
            # 'KLAMPO280': {'Val': 0, 'Value': 'ZPRZNO', 'Des': 'PRZ HIGH LEVEL RX TRIP', 'Setpoint': '92', 'Unit': '%'},
            # 'KLAMPO281': {'Val': 0, 'Value': 'PPRZN', 'Des': 'PRZ HIGH PRESS RX TRIP', 'Setpoint': '167.72', 'Unit': 'kg/cm²'},
            # 'KLAMPO282': {'Val': 0, 'Value': 'PPRZN', 'Des': 'PRZ LOW PRESS & P-7 RX TRIP', 'Setpoint': '136.78', 'Unit': 'kg/cm²'},
            # 'KLAMPO283': {'Val': 0, 'Value': 'XPSRM', 'Des': 'SOURCE RANGE HIGH FLUX RX TRIP', 'Setpoint': '1.00E + 05', 'Unit': 'CPS'},
            # 'KLAMPO284': {'Val': 0, 'Value': 'XPIRM', 'Des': 'ALARM: INTERMEDIATE RANGE HIGH FLUX RX TRIP', 'Setpoint': '2.08E -04', 'Unit': 'A'},
            # 'KLAMPO285': {'Val': 0, 'Value': 'QPROREL', 'Des': 'PWR RANGE HIGH FLUX HIGH SETPT RX TRIP', 'Setpoint': '109', 'Unit': '%'},
            # 'KLAMPO286': {'Val': 0, 'Value': 'QPROREL', 'Des': 'PWR RANGE HIGH FLUX LOW SETPT RX TRIP', 'Setpoint': '25', 'Unit': '%'},
            #
            # 'KLAMPO287': {'Val': 0, 'Value': ['QPROREL', 'PWRHFX'], 'Des': 'PWR RANGE HIGH FLUX RATE RX TRIP', 'Setpoint': ['5', '-5'], 'Unit': ['%', '%']},  # val: QPROREL-PWRHFX(계산식)
            #
            # 'KLAMPO288': {'Val': 0, 'Value': ['WSGRCP1', 'WSGRCP2', 'WSGRCP3'], 'Des': 'RCS FLOW LOW AT HIGH PWR RX TRIP', 'Setpoint': '5060', 'Unit': 'kg/sec'},  # 다중 변수 확인, Setpoint 확인필요
            #
            # 'KLAMPO289': {'Val': 0, 'Value': ['WSGRCP1', 'WSGRCP2', 'WSGRCP3'], 'Des': 'RCS FLOW LOW AT LOW PWR RX TRIP', 'Setpoint': '4140', 'Unit': 'kg/sec'},  # 다중 변수 확인, Setpoint 확인필요
            #
            # 'KLAMPO290': {'Val': 0, 'Value': ['ZSGNOR1', 'ZSGNOR2', 'ZSGNOR3'], 'Des': 'SG 1,2,3 WTR LEVEL LOW-LOW RX TRIP', 'Setpoint': '17', 'Unit': '%'},  # 다중 변수 확인(SG별 존재)
            #
            # 'KLAMPO291': {'Val': 0, 'Value': 'KTBTRIP', 'Des': 'TBN TRIP & P-7 RX TRIP', 'Setpoint': '1', 'Unit': '-'},
            # 'KLAMPO292': {'Val': 0, 'Value': 0, 'Des': 'MSL PRESS MSL ISO SI RX TRIP ', 'Setpoint': '4.03E+06', 'Unit': 'Pa'},  # setpoint 찾았으나 변수 못찾음_ 포트란 검색시에도 안나옴
            # ------------------------------------------------------------------------------------------------------------------------------------------------------
            'KLAMPO293': {'Val': 0, 'Value': 0, 'Des': 'Not used',  'Setpoint': '', 'Unit': '', 'System': ''}, # Not used
            'KLAMPO294': {'Val': 0, 'Value': 0, 'Des': 'Not used', 'Setpoint': '', 'Unit': '', 'System': ''}, # Not used


            'KLAMPO295': {'Val': 0, 'Value': 'ZSUMP', 'Des': 'CTMT sump level hi', 'Setpoint': 2.492, 'Unit': 'm', 'System': '잔열 제거 계통'},
            'KLAMPO296': {'Val': 0, 'Value': 'ZSUMP', 'Des': 'CTMT sump level hi-hi', 'Setpoint': 2.9238, 'Unit': 'm', 'System': '잔열 제거 계통'},  #Setpoint 문서상 표기 없음, 서류 확인 후 기입 필요
            'KLAMPO297': {'Val': 0, 'Value': 'UCTMT', 'Des': 'CTMT air temp hi','Setpoint': 'CUCTMT', 'Unit': '℃', 'System': '잔열 제거 계통'},
            'KLAMPO298': {'Val': 0, 'Value': 'HUCTMT', 'Des': 'CTMT moisture hi', 'Setpoint': 'CHCTMT', 'Unit': '%', 'System': '잔열 제거 계통'},
            # ------------------------------------------------------------------------------------------------------------------------------------------------------
            # 'KLAMPO301': {'Val': 0, 'Value': ['DCTMT', 'DSECON'], 'Des': 'Rad hi alarm', 'Setpoint': ['CRADHI', 3.9E-3], 'Unit': 'mRem/Hr', 'System': '잔열 제거 계통'},
            'KLAMPO301_1': {'Val': 0, 'Value': 'DCTMT', 'Des': 'Containment Rad hi alarm', 'Setpoint': 'CRADHI', 'Unit': 'mRem/Hr', 'System': '잔열 제거 계통'},
            'KLAMPO301_2': {'Val': 0, 'Value': 'DSECON', 'Des': 'Secondary Rad hi alarm', 'Setpoint': 3.9E-3, 'Unit': 'mRem/Hr', 'System': '잔열 제거 계통'},

            'KLAMPO302': {'Val': 0, 'Value': ['PCTMT', 'PAKGCM'], 'Des': 'CTMT press hi 1 alert', 'Setpoint': 0.3515, 'Unit': 'kg/cm²', 'System': '잔열 제거 계통'}, # 계산식

            'KLAMPO303': {'Val': 0, 'Value': ['PCTMT', 'PAKGCM'], 'Des': 'CTMT press hi 2 alert', 'Setpoint': 1.02, 'Unit': 'kg/cm²', 'System': '잔열 제거 계통'}, # 계산식

            'KLAMPO304': {'Val': 0, 'Value': ['PCTMT', 'PAKGCM'], 'Des': 'CTMT press hi 3 alert', 'Setpoint': 1.62, 'Unit': 'kg/cm²', 'System': '잔열 제거 계통'}, # 계산식

            'KLAMPO305': {'Val': 0, 'Value': 'PACCTK', 'Des': 'Accum. Tk press lo', 'Setpoint': 'CPACCL', 'Unit': 'kg/cm²', 'System': '화학 및 체적 제어계통'},
            'KLAMPO306': {'Val': 0, 'Value': 'PACCTK', 'Des': 'Accum. Tk press hi', 'Setpoint': 'CPACCH', 'Unit': 'kg/cm²', 'System': '화학 및 체적 제어계통'},
            'KLAMPO307': {'Val': 0, 'Value': 'PPRZ', 'Des': 'PRZ press hi alert', 'Setpoint': 'CPPRZH', 'Unit': 'kg/cm²', 'System': '원자로 냉각재 계통'},
            'KLAMPO308': {'Val': 0, 'Value': 'PPRZ', 'Des': 'PRZ press lo alert', 'Setpoint': 'CPPRZL', 'Unit': 'kg/cm²', 'System': '원자로 냉각재 계통'},
            'KLAMPO309': {'Val': 0, 'Value': 'BPORV', 'Des': 'PRZ PORV opening', 'Setpoint': 0.01, 'Unit': '', 'System': '원자로 냉각재 계통'},

            # 'KLAMPO310': {'Val': 0, 'Value': ['ZINST63', 'QPRZB'], 'Des': 'PRZ cont level hi heater on', 'Setpoint': ['ZPRZSP', 'CZPRZH', 'CQPRZP'], 'Unit': ['', ''], 'System': '원자로 냉각재 계통'},
            'KLAMPO310': {'Val': 0, 'Value': 'ZINST63', 'Des': 'PRZ cont level hi heater on', 'Setpoint': ['ZPRZSP', 'CZPRZH'], 'Unit': '%', 'System': '원자로 냉각재 계통'},
            # 'KLAMPO310_1': {'Val': 0, 'Value': 'ZINST63', 'Des': 'PRZ cont level hi', 'Setpoint': ['ZPRZSP', 'CZPRZH'], 'Unit': '', 'System': '원자로 냉각재 계통'},
            # 'KLAMPO310_2': {'Val': 0, 'Value': 'QPRZB', 'Des': 'PRZ Back-up heater on', 'Setpoint': 'CQPRZP', 'Unit': '', 'System': '원자로 냉각재 계통'},

            # 'KLAMPO311': {'Val': 0, 'Value': ['ZINST63', 'QPRZ'], 'Des': 'PRZ cont level lo heater off', 'Setpoint': ['CZPRZL', 'CQPRZP'], 'Unit': ['', ''], 'System': '원자로 냉각재 계통'},
            'KLAMPO311': {'Val': 0, 'Value': 'ZINST63', 'Des': 'PRZ cont level lo heater off', 'Setpoint': 'CZPRZL', 'Unit': '%', 'System': '원자로 냉각재 계통'},
            # 'KLAMPO311_1': {'Val': 0, 'Value': 'ZINST63', 'Des': 'PRZ cont level lo', 'Setpoint': 'CZPRZL', 'Unit': '', 'System': '원자로 냉각재 계통'},
            # 'KLAMPO311_2': {'Val': 0, 'Value': 'QPRZ', 'Des': 'PRZ All heater off', 'Setpoint': 'CQPRZP', 'Unit': '', 'System': '원자로 냉각재 계통'},

            # 'KLAMPO312': {'Val': 0, 'Value': ['PPRZN', 'KBHON'], 'Des': 'PRZ press lo back-up heater on', 'Setpoint':['CQPRZB', 1], 'Unit': ['kg/cm²', ''], 'System': '원자로 냉각재 계통'},
            'KLAMPO312': {'Val': 0, 'Value': 'PPRZN', 'Des': 'PRZ press lo back-up heater on', 'Setpoint':'CQPRZB', 'Unit': 'kg/cm²', 'System': '원자로 냉각재 계통'},
            # 'KLAMPO312_1': {'Val': 0, 'Value': 'PPRZN', 'Des': 'PRZ press lo', 'Setpoint':'CQPRZB', 'Unit': 'kg/cm²', 'System': '원자로 냉각재 계통'},
            # 'KLAMPO312_2': {'Val': 0, 'Value': 'KBHON', 'Des': 'PRZ back-up heater on', 'Setpoint': 1, 'Unit': '', 'System': '원자로 냉각재 계통'},

            # 'KLAMPO313': {'Val': 0, 'Value': ['UAVLEGS', 'UAVLEGM', 'UAVLEGM', 'UAVLEGS'], 'Des': 'Tref/Auct. Tavg Deviation', 'Setpoint': ['CUTDEV', 'CUTDEV'], 'Unit': ['℃', '℃'], 'System': '원자로 냉각재 계통'},
            'KLAMPO313': {'Val': 0, 'Value': ['UAVLEGS', 'UAVLEGM'], 'Des': 'Tref/Auct. Tavg Deviation', 'Setpoint': 'CUTDEV', 'Unit': '℃', 'System': '원자로 냉각재 계통'},

            # 'KLAMPO314': {'Val': 0, 'Value': 'UAVLEGS', 'Des': 'RCS 1,2,3 Tavg hi', 'Setpoint': '312.78', 'Unit': '℃'}, # 분할 경보, 분할 변수는 없음. (원본 경보)
            'KLAMPO314_1': {'Val': 0, 'Value': 'UAVLEGM', 'Des': 'RCS 1 Tavg hi', 'Setpoint': 'CUTAVG', 'Unit': '℃', 'System': '원자로 냉각재 계통'},  # 분할 경보, 분할 변수는 없음.
            'KLAMPO314_2': {'Val': 0, 'Value': 'UAVLEGM', 'Des': 'RCS 2 Tavg hi', 'Setpoint': 'CUTAVG', 'Unit': '℃', 'System': '원자로 냉각재 계통'},  # 분할 경보, 분할 변수는 없음.
            'KLAMPO314_3': {'Val': 0, 'Value': 'UAVLEGM', 'Des': 'RCS 3 Tavg hi', 'Setpoint': 'CUTAVG', 'Unit': '℃', 'System': '원자로 냉각재 계통'},  # 분할 경보, 분할 변수는 없음.

            # 'KLAMPO315': {'Val': 0, 'Value': ['UAVLEG1', 'UAVLEG2', 'UAVLEG3'], 'Des': 'RCS 1,2,3 Tavg/auct Tavg hi/lo', 'Setpoint': '1.11', 'Unit': '℃'}, # 분할 경보 (원본 경보)
            'KLAMPO315_1': {'Val': 0, 'Value': 'UAVLEG1', 'Des': 'RCS 1 Tavg/auct Tavg hi/lo', 'Setpoint': 'CUAUCT', 'Unit': '℃', 'System': '원자로 냉각재 계통'}, # 분할 경보, 계산식
            'KLAMPO315_2': {'Val': 0, 'Value': 'UAVLEG2', 'Des': 'RCS 2 Tavg/auct Tavg hi/lo', 'Setpoint': 'CUAUCT', 'Unit': '℃', 'System': '원자로 냉각재 계통'}, # 분할 경보, 계산식
            'KLAMPO315_3': {'Val': 0, 'Value': 'UAVLEG3', 'Des': 'RCS 3 Tavg/auct Tavg hi/lo', 'Setpoint': 'CUAUCT', 'Unit': '℃', 'System': '원자로 냉각재 계통'}, # 분할 경보, 계산식

            # 'KLAMPO316': {'Val': 0, 'Value': ['WSGRCP1', 'WSGRCP2', 'WSGRCP3'], 'Des': 'RCS 1,2,3 lo flow alert', 'Setpoint': '92', 'Unit': 'Kg/sec'}, # 분할 경보, setpoint 변수가 있으나 CNS에 변수가 구현되어 있지 않음. (원본 경보)
            'KLAMPO316_1': {'Val': 0, 'Value': 'WSGRCP1', 'Des': 'RCS 1 lo flow alert', 'Setpoint': 4232, 'Unit': 'Kg/sec', 'System': '원자로 냉각재 계통'},  # 분할 경보
            'KLAMPO316_2': {'Val': 0, 'Value': 'WSGRCP2', 'Des': 'RCS 2 lo flow alert', 'Setpoint': 4232, 'Unit': 'Kg/sec', 'System': '원자로 냉각재 계통'},  # 분할 경보
            'KLAMPO316_3': {'Val': 0, 'Value': 'WSGRCP3', 'Des': 'RCS 3 lo flow alert', 'Setpoint': 4232, 'Unit': 'Kg/sec', 'System': '원자로 냉각재 계통'},  # 분할 경보
            # 'KLAMPO316_4': {'Val': 0, 'Value': 'KRCP1', 'Des': 'RCP 1 Actuation', 'Setpoint': 1, 'Unit': '', 'System': '원자로 냉각재 계통'},  # 분할 경보
            # 'KLAMPO316_5': {'Val': 0, 'Value': 'KRCP2', 'Des': 'RCP 2 Actuation', 'Setpoint': 1, 'Unit': '', 'System': '원자로 냉각재 계통'},  # 분할 경보
            # 'KLAMPO316_6': {'Val': 0, 'Value': 'KRCP3', 'Des': 'RCP 3 Actuation', 'Setpoint': 1, 'Unit': '', 'System': '원자로 냉각재 계통'},  # 분할 경보

            'KLAMPO317': {'Val': 0, 'Value': 'UPRT', 'Des': 'PRT temp hi', 'Setpoint': 'CUPRT', 'Unit': '℃', 'System': '원자로 냉각재 계통'},
            'KLAMPO318': {'Val': 0, 'Value': 'PPRT', 'Des': 'PRT press hi', 'Setpoint': 'CPPRT', 'Unit': 'kg/cm2', 'System': '원자로 냉각재 계통'},

            # 'KLAMPO319': {'Val': 0, 'Value': ['ZSGNOR1', 'ZSGNOR2', 'ZSGNOR3'], 'Des': 'SG 1,2,3 level lo', 'Setpoint': '0.25', 'Unit': '-'}, # 분할 경보 (원본 경보)
            'KLAMPO319_1': {'Val': 0, 'Value': 'ZINST78', 'Des': 'SG 1 level lo', 'Setpoint': 'CZSGW', 'Unit': '', 'System': '주증기 계통'},  # 분할 경보, 계산식 포함
            'KLAMPO319_2': {'Val': 0, 'Value': 'ZINST77', 'Des': 'SG 2 level lo', 'Setpoint': 'CZSGW', 'Unit': '', 'System': '주증기 계통'},  # 분할 경보, 계산식 포함
            'KLAMPO319_3': {'Val': 0, 'Value': 'ZINST76', 'Des': 'SG 3 level lo', 'Setpoint': 'CZSGW', 'Unit': '', 'System': '주증기 계통'},  # 분할 경보, 계산식 포함

            # 'KLAMPO320': {'Val': 0, 'Value': ['WSTM1', 'WSTM2', 'WSTM3', 'WFWLN1', 'WFWLN2', 'WFWLN3'], 'Des': 'SG 1,2,3 stm/FW flow deviation', 'Setpoint': '0', 'Unit': ['kg/sec', 'kg/sec', 'kg/sec']},  # 분할 경보, value 및 setpoint 계산식 (원본 경보)
            'KLAMPO320_1': {'Val': 0, 'Value': ['WSTM1', 'WFWLN1'], 'Des': 'SG 1 stm/FW flow deviation', 'Setpoint': 'WSTM1', 'Unit': 'kg/sec', 'System': '주증기 계통'},  # 분할 경보, 계산식 포함
            'KLAMPO320_2': {'Val': 0, 'Value': ['WSTM2', 'WFWLN2'], 'Des': 'SG 2 stm/FW flow deviation', 'Setpoint': 'WSTM2', 'Unit': 'kg/sec', 'System': '주증기 계통'},  # 분할 경보, 계산식 포함
            'KLAMPO320_3': {'Val': 0, 'Value': ['WSTM3', 'WFWLN3'], 'Des': 'SG 3 stm/FW flow deviation', 'Setpoint': 'WSTM3', 'Unit': 'kg/sec', 'System': '주증기 계통'},  # 분할 경보, 계산식 포함

            # 'KLAMPO321': {'Val': 0, 'Value': ['KRCP1', 'KRCP2', 'KRCP3'], 'Des': 'RCP 1,2,3 trip', 'Setpoint': '0', 'Unit': ''},
            'KLAMPO321_1': {'Val': 0, 'Value': 'KRCP1', 'Des': 'RCP 1 trip', 'Setpoint': 0, 'Unit': '', 'System': '원자로 냉각재 계통'}, # 분할 경보
            'KLAMPO321_2': {'Val': 0, 'Value': 'KRCP2', 'Des': 'RCP 2 trip', 'Setpoint': 0, 'Unit': '', 'System': '원자로 냉각재 계통'}, # 분할 경보
            'KLAMPO321_3': {'Val': 0, 'Value': 'KRCP3', 'Des': 'RCP 3 trip', 'Setpoint': 0, 'Unit': '', 'System': '원자로 냉각재 계통'}, # 분할 경보

            'KLAMPO322': {'Val': 0, 'Value': 'ZCNDTK', 'Des': 'Condensate stor Tk level lo', 'Setpoint': 8.55, 'Unit': 'M', 'System': '복수 계통'},
            'KLAMPO323': {'Val': 0, 'Value': 'ZCNDTK', 'Des': 'Condensate stor Tk level lo-lo', 'Setpoint': 7.57, 'Unit': 'M', 'System': '복수 계통'},
            'KLAMPO324': {'Val': 0, 'Value': 'ZCNDTK', 'Des': 'Condensate stor Tk level hi', 'Setpoint': 'CZCTKH', 'Unit': 'M', 'System': '복수 계통'},

            'KLAMPO325': {'Val': 0, 'Value': 'BHV108', 'Des': 'MSIV tripped', 'Setpoint': '', 'Unit': '', 'System': ''}, # 분할 경보
            'KLAMPO325_1': {'Val': 0, 'Value': 'BHV108', 'Des': 'MSIV 1 tripped', 'Setpoint': 0, 'Unit': '', 'System': '주증기 계통'}, # 분할 경보
            'KLAMPO325_2': {'Val': 0, 'Value': 'BHV208', 'Des': 'MSIV 2 tripped', 'Setpoint': 0, 'Unit': '', 'System': '주증기 계통'}, # 분할 경보
            'KLAMPO325_3': {'Val': 0, 'Value': 'BHV308', 'Des': 'MSIV 3 tripped', 'Setpoint': 0, 'Unit': '', 'System': '주증기 계통'}, # 분할 경보


            # 'KLAMPO326': {'Val': 0, 'Value': ['PSGLP', 'PSG1', 'PSG2', 'PSG3'], 'Des': 'MSL press rate hi steam iso', 'Setpoint': '689000', 'Unit': 'Pa/sec'}, # 분할 경보
            'KLAMPO326_1': {'Val': 0, 'Value': 'PSG1', 'Des': 'MSL 1 press rate hi', 'Setpoint': ['CMSLH', 1], 'Unit': 'Pa/sec', 'System': '주증기 계통'}, # 분할 경보
            'KLAMPO326_2': {'Val': 0, 'Value': 'PSG2', 'Des': 'MSL 2 press rate hi', 'Setpoint': ['CMSLH', 1], 'Unit': 'Pa/sec', 'System': '주증기 계통'}, # 분할 경보
            'KLAMPO326_3': {'Val': 0, 'Value': 'PSG3', 'Des': 'MSL 3 press rate hi', 'Setpoint': ['CMSLH', 1], 'Unit': 'Pa/sec', 'System': '주증기 계통'}, # 분할 경보
            'KLAMPO326_4': {'Val': 0, 'Value': 'KMSISO', 'Des': 'MSL Isolation', 'Setpoint': ['CMSLH', 1], 'Unit': 'Pa/sec', 'System': '주증기 계통'}, # 분할 경보


            # 'KLAMPO327': {'Val': 0, 'Value': ['PSGLP', 'PSG1', 'PSG2', 'PSG3'], 'Des': 'MSL 1,2,3 press rate hi', 'Setpoint': '689000', 'Unit': 'Pa/sec'}, # 분할 경보
            # 중복 알람
            # 'KLAMPO327_1': {'Val': 0, 'Value': 'PSG1', 'Des': 'MSL 1 press rate hi', 'Setpoint': 'CMSLH', 'Unit': 'Pa/sec', 'System': '주증기 계통'}, # 분할 경보
            # 'KLAMPO327_2': {'Val': 0, 'Value': 'PSG2', 'Des': 'MSL 2 press rate hi', 'Setpoint': 'CMSLH', 'Unit': 'Pa/sec', 'System': '주증기 계통'}, # 분할 경보
            # 'KLAMPO327_3': {'Val': 0, 'Value': 'PSG3', 'Des': 'MSL 3 press rate hi', 'Setpoint': 'CMSLH', 'Unit': 'Pa/sec', 'System': '주증기 계통'}, # 분할 경보

            # 'KLAMPO328': {'Val': 0, 'Value': ['ZINST73', 'ZINST74', 'ZINST75'], 'Des': 'MSL 1,2,3 press low', 'Setpoint': '41.1', 'Unit': 'kg/cm2'}, # 분할 경보
            'KLAMPO328_1': {'Val': 0, 'Value': 'PSG1', 'Des': 'MSL 1 press low', 'Setpoint': 'CPSTML', 'Unit': 'kg/cm2', 'System': '주증기 계통'}, # 분할 경보
            'KLAMPO328_2': {'Val': 0, 'Value': 'PSG2', 'Des': 'MSL 2 press low', 'Setpoint': 'CPSTML', 'Unit': 'kg/cm2', 'System': '주증기 계통'}, # 분할 경보
            'KLAMPO328_3': {'Val': 0, 'Value': 'PSG3', 'Des': 'MSL 3 press low', 'Setpoint': 'CPSTML', 'Unit': 'kg/cm2', 'System': '주증기 계통'}, # 분할 경보

            # 'KLAMPO329': {'Val': 0, 'Value': ['KAFWP1', 'KAFWP2', 'KAFWP3'], 'Des': 'AFW(MD) actuated', 'Setpoint': '-', 'Unit': '-'}, # 분할 경보
            'KLAMPO329_1': {'Val': 0, 'Value': 'KAFWP1', 'Des': 'AFW(MD) 1 actuated', 'Setpoint': 1, 'Unit': '', 'System': '보조 급수 계통'}, # 분할 경보
            'KLAMPO329_2': {'Val': 0, 'Value': 'KAFWP2', 'Des': 'AFW(MD) 2 actuated', 'Setpoint': 1, 'Unit': '', 'System': '보조 급수 계통'}, # 분할 경보
            'KLAMPO329_3': {'Val': 0, 'Value': 'KAFWP3', 'Des': 'AFW(MD) 3 actuated', 'Setpoint': 1, 'Unit': '', 'System': '보조 급수 계통'}, # 분할 경보

            'KLAMPO330': {'Val': 0, 'Value': 'ZCOND', 'Des': 'Condenser level lo', 'Setpoint': 'CZCNDL', 'Unit': 'M', 'System': '복수 계통'},
            'KLAMPO331': {'Val': 0, 'Value': 'PFWPOUT', 'Des': 'FW pump discharge header press hi', 'Setpoint': 'CPFWOH', 'Unit': 'kg/cm2', 'System': '주급수 계통'},

            # 'KLAMPO332': {'Val': 0, 'Value': ['KFWP1', 'KFWP2', 'KFWP3'], 'Des': 'FW pump trip', 'Setpoint': '-', 'Unit': '-'}, # 분할 경보
            'KLAMPO332_1': {'Val': 0, 'Value': 'KFWP1', 'Des': 'FW pump 1 trip', 'Setpoint': 0, 'Unit': '', 'System': '주급수 계통'}, # 분할 경보
            'KLAMPO332_2': {'Val': 0, 'Value': 'KFWP2', 'Des': 'FW pump 2 trip', 'Setpoint': 0, 'Unit': '', 'System': '주급수 계통'}, # 분할 경보
            'KLAMPO332_3': {'Val': 0, 'Value': 'KFWP3', 'Des': 'FW pump 3 trip', 'Setpoint': 0, 'Unit': '', 'System': '주급수 계통'}, # 분할 경보

            'KLAMPO333': {'Val': 0, 'Value': 'UFDW', 'Des': 'FW temp hi', 'Setpoint': 'CUFWH', 'Unit': '℃', 'System': '주급수 계통'},
            'KLAMPO334': {'Val': 0, 'Value': 'WCDPO', 'Des': 'Condensate pump flow lo', 'Setpoint': 'CWCDPO', 'Unit': 'kg/s', 'System': '복수 계통'},
            'KLAMPO335': {'Val': 0, 'Value': 'PVAC', 'Des': 'Condenser abs press hi', 'Setpoint': 'CPVACH', 'Unit': 'mmHg', 'System': '복수 계통'},
            'KLAMPO336': {'Val': 0, 'Value': 'ZCOND', 'Des': 'Condenser level hi', 'Setpoint': 'CZCNDH', 'Unit': 'M', 'System': '복수 계통'},
            'KLAMPO337_1': {'Val': 0, 'Value': 'KTBTRIP', 'Des': 'TBN trip P-4 (TBN Trip)', 'Setpoint': 1, 'Unit': '', 'System': '터빈 계통'},
            'KLAMPO337_2': {'Val': 0, 'Value': 'KRXTRIP', 'Des': 'TBN trip P-4 (Rx Trip)', 'Setpoint': 1, 'Unit': '', 'System': '터빈 계통'},

            # 'KLAMPO338': {'Val': 0, 'Value': ['ZSGNOR1', 'ZSGNOR2', 'ZSGNOR3'], 'Des': 'SG 1,2,3 wtr level hi-hi TBN trip', 'Setpoint': '0.78', 'Unit': '-'}, # 분할 경보
            'KLAMPO338_1': {'Val': 0, 'Value': 'ZSGNOR1', 'Des': 'SG 1 wtr level hi-hi TBN trip', 'Setpoint': 0.78, 'Unit': '', 'System': '주증기 계통'}, # 분할 경보
            'KLAMPO338_2': {'Val': 0, 'Value': 'ZSGNOR2', 'Des': 'SG 2 wtr level hi-hi TBN trip', 'Setpoint': 0.78, 'Unit': '', 'System': '주증기 계통'}, # 분할 경보
            'KLAMPO338_3': {'Val': 0, 'Value': 'ZSGNOR3', 'Des': 'SG 3 wtr level hi-hi TBN trip', 'Setpoint': 0.78, 'Unit': '', 'System': '주증기 계통'}, # 분할 경보

            'KLAMPO339': {'Val': 0, 'Value': 'PVAC', 'Des': 'Condenser vacuum lo', 'Setpoint': 620, 'Unit': 'mmHg', 'System': '복수 계통'},
            'KLAMPO340': {'Val': 0, 'Value': 'FTURB', 'Des': 'TBN overspeed hi', 'Setpoint': 1980, 'Unit': 'rpm', 'System': '터빈 계통'},
            'KLAMPO341': {'Val': 0, 'Value': 'KGENB', 'Des': 'Gen. brk open', 'Setpoint': 0, 'Unit': '', 'System': '전기 계통'},
        }
        return alarm_dict

    def update_alarm(self, mem, alarm_dict):
        """
                현재 파라 메터가 알람관련 변수라면 입력된 값을 Overwrite
                # -----------  Left panel : KLARML(3,II) -----------------------------------------------------------------------
                #
                #           ---------------------------------------------------
                #           | II = 1 |   9    |   17   |   25   |   33   |  41 |
                #           ---------------------------------------------------
                #           |   2    |   10   |   18   |   26   |   34   |  42|
                #           ---------------------------------------------------
                #           |   3    |   11   |   19   |   27   |   35   |  43 |
                #           ---------------------------------------------------
                #           |   4    |   12   |   20   |   28   |   36   |  44 |
                #           ---------------------------------------------------
                #           |   5    |   13   |   21   |   29   |   37   |  45 |
                #           ---------------------------------------------------
                #           |   6    |   14   |   22   |   30   |   38   |  46 |
                #           ---------------------------------------------------
                #           |   7    |   15   |   23   |   31   |   39   |  47 |
                #           ---------------------------------------------------
                #           |   8    |   16   |   24   |   32   |   40   |  48 |
                #           ---------------------------------------------------
                #
                # ==============================================================================================================
                # -----------  Right panel : KLARMR(3,IJ)
                #
                #       -----------------------------------------------------------------
                #       | IJ=1  |   7   |  13   |  18   |  21   |  26   |  32   |  38   |
                #       -----------------------------------------------------------------
                #       |   2   |   8   |  14   |  19   |  22   |  27   |  33   |  39   |
                #       -----------------------------------------------------------------
                #       |   3   |   9   |  15   |  20   |       |  28   |  34   |  40   |
                #       -----------------------------------------------------------------
                #       |   4   |   10  |  16   |       |  23   |  29   |  35   |  41   |
                #       -----------------------------------------------------------------
                #       |   5   |   11  |       |       |  24   |  30   |  36   |       |
                #       -----------------------------------------------------------------
                #       |   6   |   12  |  17   |       |  25   |  31   |  37   |  42   |
                #       -----------------------------------------------------------------
                #
                # ==============================================================================================================

                """
        #
        # Left panel
        #
        # --------- L1  Intermediate range high flux rod stop(20% of FP)
        if mem['XPIRM']['Val'] > mem['CIRFH']['Val']:
            alarm_dict['KLAMPO251']['Value'] = mem['XPIRM']['Val']
            alarm_dict['KLAMPO251']['Setpoint'] = mem['CIRFH']['Val']
            alarm_dict['KLAMPO251']['Val'] = 1
        else:
            alarm_dict['KLAMPO251']['Val'] = 0
        # --------- L2  Power range overpower rod stop(103% of FP)
        if mem['QPROREL']['Val'] > mem['CPRFH']['Val']:
            alarm_dict['KLAMPO252']['Value'] = mem['QPROREL']['Val']
            alarm_dict['KLAMPO252']['Setpoint'] = mem['CPRFH']['Val']
            alarm_dict['KLAMPO252']['Val'] = 1
        else:
            alarm_dict['KLAMPO252']['Val'] = 0
        # --------- L3  Control bank D full rod withdrawl(220 steps)
        if mem['KZBANK4']['Val'] > 220:
            alarm_dict['KLAMPO253']['Value'] = mem['KZBANK4']['Val']
            alarm_dict['KLAMPO253']['Setpoint'] = 220
            alarm_dict['KLAMPO253']['Val'] = 1
        else:
            alarm_dict['KLAMPO253']['Val'] = 0
        # --------- L4  Control bank lo-lo limit
        # ******* Insertion limit(Reference : KNU 5&6 PLS)
        #
        if mem['UMAXDT']['Val'] == 0 or mem['CDT100']['Val'] == 0:
            RDTEMP = 0
        else:
            RDTEMP = (mem['UMAXDT']['Val'] / mem['CDT100']['Val']) * 100.0
        if RDTEMP >= 100.0: RDTEMP = 100.
        if RDTEMP <= 0.0: RDTEMP = 0.
        if True:
            CRIL = {1: 1.818, 2: 1.824, 3: 1.818, 4: 208.0,
                    5: 93.0, 6: -22.0, 7: 12.0}
            # Control A
            KRIL1 = 228
            # Control B
            KRIL2 = int(CRIL[1] * RDTEMP + CRIL[4])
            if KRIL2 >= 228: KRIL2 = 228
            # Control C
            KRIL3 = int(CRIL[2] * RDTEMP + CRIL[5])
            if KRIL3 >= 228: KRIL3 = 228
            # Control D
            if RDTEMP >= CRIL[7]:
                KRIL4 = int(CRIL[3] * RDTEMP + CRIL[6])
                if KRIL4 >= 160: KRIL4 = 160
                if KRIL4 <= 0: KRIL4 = 0
            else:
                KRIL4 = 0

            if mem['KBNKSEL']['Val'] == 1:
                KRILM = KRIL1
            elif mem['KBNKSEL']['Val'] == 2:
                KRILM = KRIL2
            elif mem['KBNKSEL']['Val'] == 3:
                KRILM = KRIL3
            elif mem['KBNKSEL']['Val'] == 4:
                KRILM = KRIL4
            else:
                KRILM = 0

            # if ((mem['KZBANK1']['Val'] < KRIL1) or (mem['KZBANK2']['Val'] < KRIL2)
            #         or (mem['KZBANK3']['Val'] < KRIL3) or (mem['KZBANK4']['Val'] < KRIL4)):
            #     alarm_dict['KLAMPO254']['Val'] = 1
            # else:
            #     alarm_dict['KLAMPO254']['Val'] = 0

            if mem['KZBANK1']['Val'] < KRIL1:
                alarm_dict['KLAMPO254_1']['Value'] = mem['KZBANK1']['Val']
                alarm_dict['KLAMPO254_1']['Setpoint'] = KRIL1
                alarm_dict['KLAMPO254_1']['Val'] = 1
            else:
                alarm_dict['KLAMPO254_1']['Val'] = 0

            if mem['KZBANK2']['Val'] < KRIL2:
                alarm_dict['KLAMPO254_2']['Value'] = mem['KZBANK2']['Val']
                alarm_dict['KLAMPO254_2']['Setpoint'] = KRIL2
                alarm_dict['KLAMPO254_2']['Val'] = 1
            else:
                alarm_dict['KLAMPO254_2']['Val'] = 0

            if mem['KZBANK3']['Val'] < KRIL3:
                alarm_dict['KLAMPO254_3']['Value'] = mem['KZBANK3']['Val']
                alarm_dict['KLAMPO254_3']['Setpoint'] = KRIL3
                alarm_dict['KLAMPO254_3']['Val'] = 1
            else:
                alarm_dict['KLAMPO254_3']['Val'] = 0

            if mem['KZBANK4']['Val'] < KRIL4:
                alarm_dict['KLAMPO254_4']['Value'] = mem['KZBANK4']['Val']
                alarm_dict['KLAMPO254_4']['Setpoint'] = KRIL4
                alarm_dict['KLAMPO254_4']['Val'] = 1
            else:
                alarm_dict['KLAMPO254_4']['Val'] = 0
        # --------- L5  Two or more rod at bottom(ref:A-II-8 p.113 & KAERI87-39)
        IROD = 0
        for _ in range(1, 53):
            if mem[f'KZROD{_}']['Val'] < 0.0:
                IROD += 1
        if IROD > 2:
            alarm_dict['KLAMPO255']['Value'] = IROD
            alarm_dict['KLAMPO255']['Setpoint'] = 2
            alarm_dict['KLAMPO255']['Val'] = 1
        else:
            alarm_dict['KLAMPO255']['Val'] = 0
        # --------- L6  Axial power distribution limit(3% ~ -12%)
        if (mem['CAXOFF']['Val'] >= mem['CAXOFDL']['Val']) or \
                (mem['CAXOFF']['Val'] <= (mem['CAXOFDL']['Val'] - 0.75)):
            # alarm_dict['KLAMPO256']['Value'] = [mem['CAXOFF']['Val'], mem['CAXOFF']['Val']]
            alarm_dict['KLAMPO256']['Value'] = mem['CAXOFF']['Val']
            # alarm_dict['KLAMPO256']['Setpoint'] = [mem['CAXOFDL']['Val'], mem['CAXOFDL']['Val'] - 0.75]
            alarm_dict['KLAMPO256']['Setpoint'] = mem['CAXOFDL']['Val']
            alarm_dict['KLAMPO256']['Val'] = 1
        else:
            alarm_dict['KLAMPO256']['Val'] = 0
        # --------- L7  CCWS outlet temp hi(49.0 deg C)
        if mem['UCCWIN']['Val'] >= mem['CUCCWH']['Val']:
            alarm_dict['KLAMPO257']['Value'] = mem['UCCWIN']['Val']
            alarm_dict['KLAMPO257']['Setpoint'] = mem['CUCCWH']['Val']
            alarm_dict['KLAMPO257']['Val'] = 1
        else:
            alarm_dict['KLAMPO257']['Val'] = 0
        # --------- L8  Instrument air press lo(6.3 kg/cm2)
        if mem['PINSTA']['Val'] <= (mem['CINSTP']['Val'] - 1.5):
            alarm_dict['KLAMPO258']['Value'] = mem['PINSTA']['Val']
            alarm_dict['KLAMPO258']['Setpoint'] = mem['CINSTP']['Val'] - 1.5
            alarm_dict['KLAMPO258']['Val'] = 1
        else:
            alarm_dict['KLAMPO258']['Val'] = 0
        # --------- L9  RWST level lo-lo(5%)
        if mem['ZRWST']['Val'] <= mem['CZRWSLL']['Val']:
            alarm_dict['KLAMPO259']['Value'] = mem['ZRWST']['Val']
            alarm_dict['KLAMPO259']['Setpoint'] = mem['CZRWSLL']['Val']
            alarm_dict['KLAMPO259']['Val'] = 1
        else:
            alarm_dict['KLAMPO259']['Val'] = 0
        # --------- L10  L/D HX outlet flow lo(15 m3/hr)
        if mem['WNETLD']['Val'] < mem['CWLHXL']['Val']:
            alarm_dict['KLAMPO260']['Value'] = mem['WNETLD']['Val']
            alarm_dict['KLAMPO260']['Setpoint'] = mem['CWLHXL']['Val']
            alarm_dict['KLAMPO260']['Val'] = 1
        else:
            alarm_dict['KLAMPO260']['Val'] = 0
        # --------- L11  L/D HX outlet temp hi(58 deg C)
        if mem['UNRHXUT']['Val'] > mem['CULDHX']['Val']:
            alarm_dict['KLAMPO261']['Value'] = mem['UNRHXUT']['Val']
            alarm_dict['KLAMPO261']['Setpoint'] = mem['CULDHX']['Val']
            alarm_dict['KLAMPO261']['Val'] = 1
        else:
            alarm_dict['KLAMPO261']['Val'] = 0
        # --------- L12  RHX L/D outlet temp hi(202 deg C)
        if mem['URHXUT']['Val'] > mem['CURHX']['Val']:
            alarm_dict['KLAMPO262']['Value'] = mem['URHXUT']['Val']
            alarm_dict['KLAMPO262']['Setpoint'] = mem['CURHX']['Val']
            alarm_dict['KLAMPO262']['Val'] = 1
        else:
            alarm_dict['KLAMPO262']['Val'] = 0
        # --------- L13  VCT level lo(20 %)
        if mem['ZVCT']['Val'] < mem['CZVCT2']['Val']:
            alarm_dict['KLAMPO263']['Value'] = mem['ZVCT']['Val']
            alarm_dict['KLAMPO263']['Setpoint'] = mem['CZVCT2']['Val']
            alarm_dict['KLAMPO263']['Val'] = 1
        else:
            alarm_dict['KLAMPO263']['Val'] = 0
        # --------- L14  VCT press lo(0.7 kg/cm2)
        if mem['PVCT']['Val'] < mem['CPVCTL']['Val']:
            alarm_dict['KLAMPO264']['Value'] = mem['PVCT']['Val']
            alarm_dict['KLAMPO264']['Setpoint'] = mem['CPVCTL']['Val']
            alarm_dict['KLAMPO264']['Val'] = 1
        else:
            alarm_dict['KLAMPO264']['Val'] = 0
        # --------- L15  RCP seal inj wtr flow lo(1.4 m3/hr)
        # if (mem['WRCPSI1']['Val'] < mem['CWRCPS']['Val'] or
        #         mem['WRCPSI2']['Val'] < mem['CWRCPS']['Val'] or
        #         mem['WRCPSI2']['Val'] < mem['CWRCPS']['Val']):
        #     alarm_dict['KLAMPO265']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO265']['Val'] = 0

        if mem['WRCPSI1']['Val'] < mem['CWRCPS']['Val']:
            alarm_dict['KLAMPO265_1']['Value'] = mem['WRCPSI1']['Val']
            alarm_dict['KLAMPO265_1']['Setpoint'] = mem['CWRCPS']['Val']
            alarm_dict['KLAMPO265_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO265_1']['Val'] = 0

        if mem['WRCPSI2']['Val'] < mem['CWRCPS']['Val']:
            alarm_dict['KLAMPO265_2']['Value'] = mem['WRCPSI2']['Val']
            alarm_dict['KLAMPO265_2']['Setpoint'] = mem['CWRCPS']['Val']
            alarm_dict['KLAMPO265_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO265_2']['Val'] = 0

        if mem['WRCPSI3']['Val'] < mem['CWRCPS']['Val']:
            alarm_dict['KLAMPO265_3']['Value'] = mem['WRCPSI3']['Val']
            alarm_dict['KLAMPO265_3']['Setpoint'] = mem['CWRCPS']['Val']
            alarm_dict['KLAMPO265_3']['Val'] = 1
        else:
            alarm_dict['KLAMPO265_3']['Val'] = 0

        # --------- L16  Charging flow cont flow lo(5 m3/hr)
        if mem['WCHGNO']['Val'] < mem['CWCHGL']['Val']:
            alarm_dict['KLAMPO266']['Value'] = mem['WCHGNO']['Val']
            alarm_dict['KLAMPO266']['Setpoint'] = mem['CWCHGL']['Val']
            alarm_dict['KLAMPO266']['Val'] = 1
        else:
            alarm_dict['KLAMPO266']['Val'] = 0
        # --------- R17  Not used
        alarm_dict['KLAMPO267']['Val'] = 0
        # --------- L18  L/D HX outlet flow hi (30  m3/hr)
        if mem['WNETLD']['Val'] > mem['CWLHXH']['Val']:
            alarm_dict['KLAMPO268']['Value'] = mem['WNETLD']['Val']
            alarm_dict['KLAMPO268']['Setpoint'] = mem['CWLHXH']['Val']
            alarm_dict['KLAMPO268']['Val'] = 1
        else:
            alarm_dict['KLAMPO268']['Val'] = 0
        # --------- L19  PRZ press lo SI
        CSAFEI = {1: 124.e5, 2: 40.3e5}
        # if (mem['PPRZN']['Val'] < CSAFEI[1]) and (mem['KSAFEI']['Val'] == 1):
        #     alarm_dict['KLAMPO269']['Value'] = [mem['PPRZN']['Val'], mem['KSAFEI']['Val']]
        #     alarm_dict['KLAMPO269']['Setpoint'] = [CSAFEI[1], 1]
        #     alarm_dict['KLAMPO269']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO269']['Val'] = 0
        if mem['PPRZN']['Val'] < CSAFEI[1]:
            alarm_dict['KLAMPO269_1']['Value'] = mem['PPRZN']['Val']
            alarm_dict['KLAMPO269_1']['Setpoint'] = CSAFEI[1]
            alarm_dict['KLAMPO269_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO269_1']['Val'] = 0

        if mem['KSAFEI']['Val'] == 1:
            alarm_dict['KLAMPO269_2']['Value'] = mem['KSAFEI']['Val']
            alarm_dict['KLAMPO269_2']['Setpoint'] = 1
            alarm_dict['KLAMPO269_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO269_2']['Val'] = 0
        # --------- L20 CTMT spray actuated
        if mem['KCTMTSP']['Val'] == 1:
            alarm_dict['KLAMPO270']['Value'] = mem['KCTMTSP']['Val']
            alarm_dict['KLAMPO270']['Setpoint'] = 1
            alarm_dict['KLAMPO270']['Val'] = 1
        else:
            alarm_dict['KLAMPO270']['Val'] = 0
        # --------- L21  VCT level hi(80 %)
        if mem['ZVCT']['Val'] > mem['CZVCT6']['Val']:
            alarm_dict['KLAMPO271']['Value'] = mem['ZVCT']['Val']
            alarm_dict['KLAMPO271']['Setpoint'] = mem['CZVCT6']['Val']
            alarm_dict['KLAMPO271']['Val'] = 1
        else:
            alarm_dict['KLAMPO271']['Val'] = 0
        # --------- L22 VCT press hi (4.5 kg/cm2)
        if mem['PVCT']['Val'] > mem['CPVCTH']['Val']:
            alarm_dict['KLAMPO272']['Value'] = mem['PVCT']['Val']
            alarm_dict['KLAMPO272']['Setpoint'] = mem['CPVCTH']['Val']
            alarm_dict['KLAMPO272']['Val'] = 1
        else:
            alarm_dict['KLAMPO272']['Val'] = 0
        # --------- L23  CTMT phase B iso actuated
        if mem['KCISOB']['Val'] == 1:
            alarm_dict['KLAMPO273']['Value'] = mem['KCISOB']['Val']
            alarm_dict['KLAMPO273']['Setpoint'] = 1
            alarm_dict['KLAMPO273']['Val'] = 1
        else:
            alarm_dict['KLAMPO273']['Val'] = 0
        # --------- L24  Charging flow cont flow hi(27 m3/hr)
        if mem['WCHGNO']['Val'] > mem['CWCHGH']['Val']:
            alarm_dict['KLAMPO274']['Value'] = mem['WCHGNO']['Val']
            alarm_dict['KLAMPO274']['Setpoint'] = mem['CWCHGH']['Val']
            alarm_dict['KLAMPO274']['Val'] = 1
        else:
            alarm_dict['KLAMPO274']['Val'] = 0
        # ---------

        # --------- R43  Not used
        # alarm_dict['KLAMPO293']['Val'] = 0
        # --------- R44  Not used
        # alarm_dict['KLAMPO294']['Val'] = 0
        # --------- L45  CTMT sump level hi
        CZSMPH = {1: 2.492, 2: 2.9238}
        if mem['ZSUMP']['Val'] > CZSMPH[1]:
            alarm_dict['KLAMPO295']['Value'] = mem['ZSUMP']['Val']
            alarm_dict['KLAMPO295']['Setpoint'] = CZSMPH[1]
            alarm_dict['KLAMPO295']['Val'] = 1
        else:
            alarm_dict['KLAMPO295']['Val'] = 0
        # --------- L46 CTMT sump level hi-hi
        if mem['ZSUMP']['Val'] > CZSMPH[2]:
            alarm_dict['KLAMPO296']['Value'] = mem['ZSUMP']['Val']
            alarm_dict['KLAMPO296']['Setpoint'] = CZSMPH[2]
            alarm_dict['KLAMPO296']['Val'] = 1
        else:
            alarm_dict['KLAMPO296']['Val'] = 0
        # --------- L47  CTMT air temp hi(48.89 deg C)
        if mem['UCTMT']['Val'] > mem['CUCTMT']['Val']:
            alarm_dict['KLAMPO297']['Value'] = mem['UCTMT']['Val']
            alarm_dict['KLAMPO297']['Setpoint'] = mem['CUCTMT']['Val']
            alarm_dict['KLAMPO297']['Val'] = 1
        else:
            alarm_dict['KLAMPO297']['Val'] = 0
        # --------- L48  CTMT moisture hi(70% of R.H.)
        if mem['HUCTMT']['Val'] > mem['CHCTMT']['Val']:
            alarm_dict['KLAMPO298']['Value'] = mem['HUCTMT']['Val']
            alarm_dict['KLAMPO298']['Setpoint'] = mem['CHCTMT']['Val']
            alarm_dict['KLAMPO298']['Val'] = 1
        else:
            alarm_dict['KLAMPO298']['Val'] = 0
        #
        # Right panel
        #
        # --------- R1  Rad hi alarm
        # if (mem['DCTMT']['Val'] > mem['CRADHI']['Val']) or \
        #         (mem['DSECON']['Val'] >= 3.9E-3):
        #     alarm_dict['KLAMPO301']['Value'] = [mem['DCTMT']['Val'], mem['DSECON']['Val']]
        #     alarm_dict['KLAMPO301']['Setpoint'] = [mem['CRADHI']['Val'], 3.9E-3]
        #     alarm_dict['KLAMPO301']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO301']['Val'] = 0

        if (mem['DCTMT']['Val'] > mem['CRADHI']['Val']):
            alarm_dict['KLAMPO301_1']['Value'] = mem['DCTMT']['Val']
            alarm_dict['KLAMPO301_1']['Setpoint'] = mem['CRADHI']['Val']
            alarm_dict['KLAMPO301_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO301_1']['Val'] = 0

        if mem['DSECON']['Val'] >= 3.9E-3:
            alarm_dict['KLAMPO301_2']['Value'] = mem['DSECON']['Val']
            alarm_dict['KLAMPO301_2']['Setpoint'] = 3.9E-3
            alarm_dict['KLAMPO301_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO301_2']['Val'] = 0
        # --------- R2  CTMT press hi 1 alert
        CPCMTH = {1: 0.3515, 2: 1.02, 3: 1.62}
        if mem['PCTMT']['Val'] * mem['PAKGCM']['Val'] > CPCMTH[1]:
            alarm_dict['KLAMPO302']['Value'] = mem['PCTMT']['Val'] * mem['PAKGCM']['Val']
            alarm_dict['KLAMPO302']['Setpoint'] = CPCMTH[1]
            alarm_dict['KLAMPO302']['Val'] = 1
        else:
            alarm_dict['KLAMPO302']['Val'] = 0
        # --------- R3  CTMT press hi 2 alert
        if mem['PCTMT']['Val'] * mem['PAKGCM']['Val'] > CPCMTH[2]:
            alarm_dict['KLAMPO303']['Value'] = mem['PCTMT']['Val'] * mem['PAKGCM']['Val']
            alarm_dict['KLAMPO303']['Setpoint'] = CPCMTH[2]
            alarm_dict['KLAMPO303']['Val'] = 1
        else:
            alarm_dict['KLAMPO303']['Val'] = 0
        # --------- R4  CTMT press hi 3 alert
        if mem['PCTMT']['Val'] * mem['PAKGCM']['Val'] > CPCMTH[3]:
            alarm_dict['KLAMPO304']['Value'] = mem['PCTMT']['Val'] * mem['PAKGCM']['Val']
            alarm_dict['KLAMPO304']['Setpoint'] = CPCMTH[3]
            alarm_dict['KLAMPO304']['Val'] = 1
        else:
            alarm_dict['KLAMPO304']['Val'] = 0
        # --------- R5  Accum. Tk press lo (43.4 kg/cm2)
        if mem['PACCTK']['Val'] < mem['CPACCL']['Val']:
            alarm_dict['KLAMPO305']['Value'] = mem['PACCTK']['Val']
            alarm_dict['KLAMPO305']['Setpoint'] = mem['CPACCL']['Val']
            alarm_dict['KLAMPO305']['Val'] = 1
        else:
            alarm_dict['KLAMPO305']['Val'] = 0
        # --------- R6  Accum. Tk press hi ( /43.4 kg/cm2)
        if mem['PACCTK']['Val'] > mem['CPACCH']['Val']:
            alarm_dict['KLAMPO306']['Value'] = mem['PACCTK']['Val']
            alarm_dict['KLAMPO306']['Setpoint'] = mem['CPACCH']['Val']
            alarm_dict['KLAMPO306']['Val'] = 1
        else:
            alarm_dict['KLAMPO306']['Val'] = 0
        # --------- R7  PRZ press hi alert(162.4 kg/cm2)
        if mem['PPRZ']['Val'] > mem['CPPRZH']['Val']:
            alarm_dict['KLAMPO307']['Value'] = mem['PPRZ']['Val']
            alarm_dict['KLAMPO307']['Setpoint'] = mem['CPPRZH']['Val']
            alarm_dict['KLAMPO307']['Val'] = 1
        else:
            alarm_dict['KLAMPO307']['Val'] = 0
        # --------- R8  PRZ press lo alert(153.6 kg/cm2)
        if mem['PPRZ']['Val'] < mem['CPPRZL']['Val']:
            alarm_dict['KLAMPO308']['Value'] = mem['PPRZ']['Val']
            alarm_dict['KLAMPO308']['Setpoint'] = mem['CPPRZL']['Val']
            alarm_dict['KLAMPO308']['Val'] = 1
        else:
            alarm_dict['KLAMPO308']['Val'] = 0
        # --------- R9  PRZ PORV opening(164.2 kg/cm2)
        if mem['BPORV']['Val'] > 0.01:
            alarm_dict['KLAMPO309']['Value'] = mem['BPORV']['Val']
            alarm_dict['KLAMPO309']['Setpoint'] = 0.01
            alarm_dict['KLAMPO309']['Val'] = 1
        else:
            alarm_dict['KLAMPO309']['Val'] = 0
        # --------- R10 PRZ cont level hi heater on(over 5%) !%deail....
        DEPRZ = mem['ZINST63']['Val'] / 100
        # if (DEPRZ > (mem['ZPRZSP']['Val'] + mem['CZPRZH']['Val'])) and (
        #         mem['QPRZB']['Val'] > mem['CQPRZP']['Val']):
        #     alarm_dict['KLAMPO310']['Value'] = [DEPRZ, mem['QPRZB']['Val']]
        #     alarm_dict['KLAMPO310']['Setpoint'] = [mem['ZPRZSP']['Val'] + mem['CZPRZH']['Val'], mem['CQPRZP']['Val']]
        #     alarm_dict['KLAMPO310']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO310']['Val'] = 0

        if (DEPRZ > (mem['ZPRZSP']['Val'] + mem['CZPRZH']['Val'])) and (
                mem['QPRZB']['Val'] > mem['CQPRZP']['Val']):
            alarm_dict['KLAMPO310']['Value'] = DEPRZ
            alarm_dict['KLAMPO310']['Setpoint'] = mem['ZPRZSP']['Val'] + mem['CZPRZH']['Val']
            alarm_dict['KLAMPO310']['Val'] = 1
        else:
            alarm_dict['KLAMPO310']['Val'] = 0

        # if (DEPRZ > (mem['ZPRZSP']['Val'] + mem['CZPRZH']['Val'])):
        #     alarm_dict['KLAMPO310_1']['Value'] = DEPRZ
        #     alarm_dict['KLAMPO310_1']['Setpoint'] = mem['ZPRZSP']['Val'] + mem['CZPRZH']['Val']
        #     alarm_dict['KLAMPO310_1']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO310_1']['Val'] = 0
        #
        # if (mem['QPRZB']['Val'] > mem['CQPRZP']['Val']):
        #     alarm_dict['KLAMPO310_2']['Value'] = mem['QPRZB']['Val']
        #     alarm_dict['KLAMPO310_2']['Setpoint'] = mem['CQPRZP']['Val']
        #     alarm_dict['KLAMPO310_2']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO310_2']['Val'] = 0
        # --------- R11  PRZ cont level lo heater off(17%) !%deail....
        # if (DEPRZ < mem['CZPRZL']['Val']) and (mem['QPRZ']['Val'] >= mem['CQPRZP']['Val']):
        #     alarm_dict['KLAMPO311']['Value'] = [DEPRZ, mem['QPRZ']['Val']]
        #     alarm_dict['KLAMPO311']['Setpoint'] = [mem['CZPRZL']['Val'], mem['CQPRZP']['Val']]
        #     alarm_dict['KLAMPO311']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO311']['Val'] = 0

        if (DEPRZ < mem['CZPRZL']['Val']) and (mem['QPRZ']['Val'] >= mem['CQPRZP']['Val']):
            alarm_dict['KLAMPO311']['Value'] = DEPRZ
            alarm_dict['KLAMPO311']['Setpoint'] = mem['CZPRZL']['Val']
            alarm_dict['KLAMPO311']['Val'] = 1
        else:
            alarm_dict['KLAMPO311']['Val'] = 0

        # if (DEPRZ < mem['CZPRZL']['Val']):
        #     alarm_dict['KLAMPO311_1']['Value'] = DEPRZ
        #     alarm_dict['KLAMPO311_1']['Setpoint'] = mem['CZPRZL']['Val']
        #     alarm_dict['KLAMPO311_1']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO311_1']['Val'] = 0
        #
        # if (mem['QPRZ']['Val'] >= mem['CQPRZP']['Val']):
        #     alarm_dict['KLAMPO311_2']['Value'] = mem['QPRZ']['Val']
        #     alarm_dict['KLAMPO311_2']['Setpoint'] = mem['CQPRZP']['Val']
        #     alarm_dict['KLAMPO311_2']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO311_2']['Val'] = 0
        # --------- R12  PRZ press lo back-up heater on(153.6 kg/cm2)
        # if (mem['PPRZN']['Val'] < mem['CQPRZB']['Val']) and (mem['KBHON']['Val'] == 1):
        #     alarm_dict['KLAMPO312']['Value'] = [mem['PPRZN']['Val'], mem['KBHON']['Val']]
        #     alarm_dict['KLAMPO312']['Setpoint'] = [mem['CQPRZB']['Val'], 1]
        #     alarm_dict['KLAMPO312']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO312']['Val'] = 0

        if (mem['PPRZN']['Val'] < mem['CQPRZB']['Val']) and (mem['KBHON']['Val'] == 1):
            alarm_dict['KLAMPO312']['Value'] = mem['PPRZN']['Val']
            alarm_dict['KLAMPO312']['Setpoint'] = mem['CQPRZB']['Val']
            alarm_dict['KLAMPO312']['Val'] = 1
        else:
            alarm_dict['KLAMPO312']['Val'] = 0

        # if (mem['PPRZN']['Val'] < mem['CQPRZB']['Val']) :
        #     alarm_dict['KLAMPO312_1']['Value'] = mem['PPRZN']['Val']
        #     alarm_dict['KLAMPO312_1']['Setpoint'] = mem['CQPRZB']['Val']
        #     alarm_dict['KLAMPO312_1']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO312_1']['Val'] = 0
        #
        # if (mem['KBHON']['Val'] == 1):
        #     alarm_dict['KLAMPO312_2']['Value'] = mem['KBHON']['Val']
        #     alarm_dict['KLAMPO312_2']['Setpoint'] = 1
        #     alarm_dict['KLAMPO312_2']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO312_2']['Val'] = 0
        # --------- R13  Tref/Auct. Tavg Deviation(1.67 deg C)
        # if ((mem['UAVLEGS']['Val'] - mem['UAVLEGM']['Val']) > mem['CUTDEV']['Val']) or \
        #         ((mem['UAVLEGM']['Val'] - mem['UAVLEGS']['Val']) > mem['CUTDEV']['Val']):
        #     alarm_dict['KLAMPO313']['Value'] = [mem['UAVLEGS']['Val'] - mem['UAVLEGM']['Val'], mem['UAVLEGM']['Val'] - mem['UAVLEGS']['Val']]
        #     alarm_dict['KLAMPO313']['Setpoint'] = [mem['CUTDEV']['Val'], mem['CUTDEV']['Val']]
        #     alarm_dict['KLAMPO313']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO313']['Val'] = 0

        if ((mem['UAVLEGS']['Val'] - mem['UAVLEGM']['Val']) > mem['CUTDEV']['Val']):
            alarm_dict['KLAMPO313']['Value'] = mem['UAVLEGS']['Val'] - mem['UAVLEGM']['Val']
            alarm_dict['KLAMPO313']['Setpoint'] = mem['CUTDEV']['Val']
            alarm_dict['KLAMPO313']['Val'] = 1
        else:
            alarm_dict['KLAMPO313']['Val'] = 0
        # --------- R14 RCS 1,2,3 Tavg hi(312.78 deg C)
        # if mem['UAVLEGM']['Val'] > mem['CUTAVG']['Val']:
        #     alarm_dict['KLAMPO314']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO314']['Val'] = 0

        if mem['UAVLEGM']['Val'] > mem['CUTAVG']['Val']:
            alarm_dict['KLAMPO314_1']['Value'] = mem['UAVLEGM']['Val']
            alarm_dict['KLAMPO314_1']['Setpoint'] = mem['CUTAVG']['Val']
            alarm_dict['KLAMPO314_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO314_1']['Val'] = 0

        if mem['UAVLEGM']['Val'] > mem['CUTAVG']['Val']:
            alarm_dict['KLAMPO314_2']['Value'] = mem['UAVLEGM']['Val']
            alarm_dict['KLAMPO314_2']['Setpoint'] = mem['CUTAVG']['Val']
            alarm_dict['KLAMPO314_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO314_2']['Val'] = 0

        if mem['UAVLEGM']['Val'] > mem['CUTAVG']['Val']:
            alarm_dict['KLAMPO314_3']['Value'] = mem['UAVLEGM']['Val']
            alarm_dict['KLAMPO314_3']['Setpoint'] = mem['CUTAVG']['Val']
            alarm_dict['KLAMPO314_3']['Val'] = 1
        else:
            alarm_dict['KLAMPO314_3']['Val'] = 0
        # --------- R15  RCS 1,2,3 Tavg/auct Tavg hi/lo(1.1 deg C)
        RUAVMX = max(mem['UAVLEG1']['Val'], mem['UAVLEG2']['Val'],
                     mem['UAVLEG3']['Val'])
        RAVGT = {1: abs((mem['UAVLEG1']['Val']) - RUAVMX),
                 2: abs((mem['UAVLEG2']['Val']) - RUAVMX),
                 3: abs((mem['UAVLEG3']['Val']) - RUAVMX)}
        # if max(RAVGT[1], RAVGT[2], RAVGT[3]) > mem['CUAUCT']['Val']:
        #     alarm_dict['KLAMPO315']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO315']['Val'] = 0

        if RAVGT[1] > mem['CUAUCT']['Val']:
            alarm_dict['KLAMPO315_1']['Value'] = RAVGT[1]
            alarm_dict['KLAMPO315_1']['Setpoint'] = mem['CUAUCT']['Val']
            alarm_dict['KLAMPO315_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO315_1']['Val'] = 0

        if RAVGT[2] > mem['CUAUCT']['Val']:
            alarm_dict['KLAMPO315_2']['Value'] = RAVGT[2]
            alarm_dict['KLAMPO315_2']['Setpoint'] = mem['CUAUCT']['Val']
            alarm_dict['KLAMPO315_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO315_2']['Val'] = 0

        if RAVGT[3] > mem['CUAUCT']['Val']:
            alarm_dict['KLAMPO315_3']['Value'] = RAVGT[3]
            alarm_dict['KLAMPO315_3']['Setpoint'] = mem['CUAUCT']['Val']
            alarm_dict['KLAMPO315_3']['Val'] = 1
        else:
            alarm_dict['KLAMPO315_3']['Val'] = 0
        # --------- R16  RCS 1,2,3 lo flow alert(92% from KAERI87-37)
        CWSGRL = {1: 4232.0, 2: 0.0}
        # if ((mem['WSGRCP1']['Val'] < CWSGRL[1] and mem['KRCP1']['Val'] == 1) or
        #         (mem['WSGRCP2']['Val'] < CWSGRL[1] and mem['KRCP2']['Val'] == 1) or
        #         (mem['WSGRCP3']['Val'] < CWSGRL[1] and mem['KRCP3']['Val'] == 1)):
        #     alarm_dict['KLAMPO316']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO316']['Val'] = 0

        if (mem['WSGRCP1']['Val'] < CWSGRL[1] and mem['KRCP1']['Val'] == 1):
            alarm_dict['KLAMPO316_1']['Value'] = mem['WSGRCP1']['Val']
            alarm_dict['KLAMPO316_1']['Setpoint'] = CWSGRL[1]
            alarm_dict['KLAMPO316_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO316_1']['Val'] = 0

        if (mem['WSGRCP2']['Val'] < CWSGRL[1] and mem['KRCP2']['Val'] == 1):
            alarm_dict['KLAMPO316_2']['Value'] = mem['WSGRCP2']['Val']
            alarm_dict['KLAMPO316_2']['Setpoint'] = CWSGRL[1]
            alarm_dict['KLAMPO316_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO316_2']['Val'] = 0

        if (mem['WSGRCP3']['Val'] < CWSGRL[1] and mem['KRCP3']['Val'] == 1):
            alarm_dict['KLAMPO316_3']['Value'] = mem['WSGRCP3']['Val']
            alarm_dict['KLAMPO316_3']['Setpoint'] = CWSGRL[1]
            alarm_dict['KLAMPO316_3']['Val'] = 1
        else:
            alarm_dict['KLAMPO316_3']['Val'] = 0

        # if (mem['KRCP1']['Val'] == 1):
        #     alarm_dict['KLAMPO316_4']['Value'] = mem['KRCP1']['Val']
        #     alarm_dict['KLAMPO316_4']['Setpoint'] = 1
        #     alarm_dict['KLAMPO316_4']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO316_4']['Val'] = 0
        #
        # if (mem['KRCP2']['Val'] == 1):
        #     alarm_dict['KLAMPO316_5']['Value'] = mem['KRCP2']['Val']
        #     alarm_dict['KLAMPO316_5']['Setpoint'] = 1
        #     alarm_dict['KLAMPO316_5']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO316_5']['Val'] = 0
        #
        # if (mem['KRCP3']['Val'] == 1):
        #     alarm_dict['KLAMPO316_6']['Value'] = mem['KRCP3']['Val']
        #     alarm_dict['KLAMPO316_6']['Setpoint'] = 1
        #     alarm_dict['KLAMPO316_6']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO316_6']['Val'] = 0
        # --------- R17  PRT temp hi(45deg C )
        if mem['UPRT']['Val'] > mem['CUPRT']['Val']:
            alarm_dict['KLAMPO317']['Value'] = mem['UPRT']['Val']
            alarm_dict['KLAMPO317']['Setpoint'] = mem['CUPRT']['Val']
            alarm_dict['KLAMPO317']['Val'] = 1
        else:
            alarm_dict['KLAMPO317']['Val'] = 0
        # --------- R18  PRT  press hi( 0.6kg/cm2)
        if (mem['PPRT']['Val'] - 0.98E5) > mem['CPPRT']['Val']:
            alarm_dict['KLAMPO318']['Value'] = mem['PPRT']['Val'] - 0.98E5
            alarm_dict['KLAMPO318']['Setpoint'] = mem['CPPRT']['Val']
            alarm_dict['KLAMPO318']['Val'] = 1
        else:
            alarm_dict['KLAMPO318']['Val'] = 0
        # --------- R19  SG 1,2,3 level lo(25% of span)
        # if (mem['ZINST78']['Val'] * 0.01 < mem['CZSGW']['Val']) \
        #         or (mem['ZINST77']['Val'] * 0.01 < mem['CZSGW']['Val']) \
        #         or (mem['ZINST76']['Val'] * 0.01 < mem['CZSGW']['Val']):
        #     alarm_dict['KLAMPO319']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO319']['Val'] = 0

        if mem['ZINST78']['Val'] * 0.01 < mem['CZSGW']['Val']:
            alarm_dict['KLAMPO319_1']['Value'] = mem['ZINST78']['Val'] * 0.01
            alarm_dict['KLAMPO319_1']['Setpoint'] = mem['CZSGW']['Val']
            alarm_dict['KLAMPO319_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO319_1']['Val'] = 0

        if mem['ZINST77']['Val'] * 0.01 < mem['CZSGW']['Val']:
            alarm_dict['KLAMPO319_2']['Value'] = mem['ZINST77']['Val'] * 0.01
            alarm_dict['KLAMPO319_2']['Setpoint'] = mem['CZSGW']['Val']
            alarm_dict['KLAMPO319_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO319_2']['Val'] = 0

        if mem['ZINST76']['Val'] * 0.01 < mem['CZSGW']['Val']:
            alarm_dict['KLAMPO319_3']['Value'] = mem['ZINST76']['Val'] * 0.01
            alarm_dict['KLAMPO319_3']['Setpoint'] = mem['CZSGW']['Val']
            alarm_dict['KLAMPO319_3']['Val'] = 1
        else:
            alarm_dict['KLAMPO319_3']['Val'] = 0
        # --------- R20  SG 1,2,3 stm/FW flow deviation(10% of loop flow)
        RSTFWD = {1: mem['WSTM1']['Val'] * 0.1,
                  2: mem['WSTM2']['Val'] * 0.1,
                  3: mem['WSTM3']['Val'] * 0.1}
        # if (((mem['WSTM1']['Val'] - mem['WFWLN1']['Val']) > RSTFWD[1]) or
        #         ((mem['WSTM2']['Val'] - mem['WFWLN2']['Val']) > RSTFWD[2]) or
        #         ((mem['WSTM3']['Val'] - mem['WFWLN3']['Val']) > RSTFWD[3])):
        #     alarm_dict['KLAMPO320']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO320']['Val'] = 0

        if (mem['WSTM1']['Val'] - mem['WFWLN1']['Val']) > RSTFWD[1]:
            alarm_dict['KLAMPO320_1']['Value'] = mem['WSTM1']['Val'] - mem['WFWLN1']['Val']
            alarm_dict['KLAMPO320_1']['Setpoint'] = RSTFWD[1]
            alarm_dict['KLAMPO320_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO320_1']['Val'] = 0

        if (mem['WSTM2']['Val'] - mem['WFWLN2']['Val']) > RSTFWD[2]:
            alarm_dict['KLAMPO320_2']['Value'] = mem['WSTM2']['Val'] - mem['WFWLN2']['Val']
            alarm_dict['KLAMPO320_2']['Setpoint'] = RSTFWD[2]
            alarm_dict['KLAMPO320_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO320_2']['Val'] = 0

        if (mem['WSTM3']['Val'] - mem['WFWLN3']['Val']) > RSTFWD[3]:
            alarm_dict['KLAMPO320_3']['Value'] = mem['WSTM3']['Val'] - mem['WFWLN3']['Val']
            alarm_dict['KLAMPO320_3']['Setpoint'] = RSTFWD[3]
            alarm_dict['KLAMPO320_3']['Val'] = 1
        else:
            alarm_dict['KLAMPO320_3']['Val'] = 0
        # --------- R21 RCP 1,2,3 trip
        # if mem['KRCP1']['Val'] + mem['KRCP2']['Val'] + mem['KRCP3']['Val'] != 3:
        #     alarm_dict['KLAMPO321']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO321']['Val'] = 0

        if mem['KRCP1']['Val'] != 1:
            alarm_dict['KLAMPO321_1']['Value'] = mem['KRCP1']['Val']
            alarm_dict['KLAMPO321_1']['Setpoint'] = 1
            alarm_dict['KLAMPO321_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO321_1']['Val'] = 0

        if mem['KRCP2']['Val'] != 1:
            alarm_dict['KLAMPO321_2']['Value'] = mem['KRCP2']['Val']
            alarm_dict['KLAMPO321_2']['Setpoint'] = 1
            alarm_dict['KLAMPO321_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO321_2']['Val'] = 0

        if mem['KRCP3']['Val'] != 1:
            alarm_dict['KLAMPO321_3']['Value'] = mem['KRCP3']['Val']
            alarm_dict['KLAMPO321_3']['Setpoint'] = 1
            alarm_dict['KLAMPO321_3']['Val'] = 1
        else:
            alarm_dict['KLAMPO321_3']['Val'] = 0
        # --------- R22  Condensate stor Tk level  lo
        CZCTKL = {1: 8.55, 2: 7.57}
        if mem['ZCNDTK']['Val'] < CZCTKL[1]:
            alarm_dict['KLAMPO322']['Value'] = mem['ZCNDTK']['Val']
            alarm_dict['KLAMPO322']['Setpoint'] = CZCTKL[1]
            alarm_dict['KLAMPO322']['Val'] = 1
        else:
            alarm_dict['KLAMPO322']['Val'] = 0
        # --------- R23  Condensate stor Tk level lo-lo
        if mem['ZCNDTK']['Val'] < CZCTKL[2]:
            alarm_dict['KLAMPO323']['Value'] = mem['ZCNDTK']['Val']
            alarm_dict['KLAMPO323']['Setpoint'] = CZCTKL[2]
            alarm_dict['KLAMPO323']['Val'] = 1
        else:
            alarm_dict['KLAMPO323']['Val'] = 0
        # --------- R24  Condensate stor Tk level hi
        if mem['ZCNDTK']['Val'] > mem['CZCTKH']['Val']:
            alarm_dict['KLAMPO324']['Value'] = mem['ZCNDTK']['Val']
            alarm_dict['KLAMPO324']['Setpoint'] = mem['CZCTKH']['Val']
            alarm_dict['KLAMPO324']['Val'] = 1
        else:
            alarm_dict['KLAMPO324']['Val'] = 0
        # --------- R25  MSIV tripped
        if mem['BHV108']['Val'] == 0 or mem['BHV208']['Val'] == 0 or mem['BHV308']['Val'] == 0:
            alarm_dict['KLAMPO325']['Val'] = 0
        else:
            alarm_dict['KLAMPO325']['Val'] = 0

        if mem['BHV108']['Val'] == 0:
            alarm_dict['KLAMPO325_1']['Value'] = mem['BHV108']['Val']
            alarm_dict['KLAMPO325_1']['Setpoint'] = 0
            alarm_dict['KLAMPO325_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO325_1']['Val'] = 0

        if mem['BHV208']['Val'] == 0:
            alarm_dict['KLAMPO325_2']['Value'] = mem['BHV208']['Val']
            alarm_dict['KLAMPO325_2']['Setpoint'] = 0
            alarm_dict['KLAMPO325_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO325_2']['Val'] = 0

        if mem['BHV308']['Val'] == 0:
            alarm_dict['KLAMPO325_3']['Value'] = mem['BHV308']['Val']
            alarm_dict['KLAMPO325_3']['Setpoint'] = 0
            alarm_dict['KLAMPO325_3']['Val'] = 1
        else:
            alarm_dict['KLAMPO325_3']['Val'] = 0
        # --------- R26  MSL press rate hi steam iso
        if len(mem['KLAMPO325']['List']) >= 3:
            PSGLP = {1: mem['PSG1']['List'][-2],
                     2: mem['PSG2']['List'][-2],
                     3: mem['PSG3']['List'][-2]}
            RMSLPR = {1: abs((PSGLP[1] - mem['PSG1']['List'][-1]) * 5.0),
                      2: abs((PSGLP[2] - mem['PSG2']['List'][-1]) * 5.0),
                      3: abs((PSGLP[3] - mem['PSG3']['List'][-1]) * 5.0)}

            # if (((RMSLPR[1] >= mem['CMSLH']['Val']) or
            #      (RMSLPR[2] >= mem['CMSLH']['Val']) or
            #      (RMSLPR[3] >= mem['CMSLH']['Val'])) and (mem['KMSISO']['Val'] == 1)):
            #     alarm_dict['KLAMPO326']['Val'] = 1
            # else:
            #     alarm_dict['KLAMPO326']['Val'] = 0

            if (RMSLPR[1] >= mem['CMSLH']['Val']):
                alarm_dict['KLAMPO326_1']['Value'] = RMSLPR[1]
                alarm_dict['KLAMPO326_1']['Setpoint'] = mem['CMSLH']['Val']
                alarm_dict['KLAMPO326_1']['Val'] = 1
            else:
                alarm_dict['KLAMPO326_1']['Val'] = 0

            if (RMSLPR[2] >= mem['CMSLH']['Val']):
                alarm_dict['KLAMPO326_2']['Value'] = RMSLPR[2]
                alarm_dict['KLAMPO326_2']['Setpoint'] = mem['CMSLH']['Val']
                alarm_dict['KLAMPO326_2']['Val'] = 1
            else:
                alarm_dict['KLAMPO326_2']['Val'] = 0

            if (RMSLPR[3] >= mem['CMSLH']['Val']):
                alarm_dict['KLAMPO326_3']['Value'] = RMSLPR[3]
                alarm_dict['KLAMPO326_3']['Setpoint'] = mem['CMSLH']['Val']
                alarm_dict['KLAMPO326_3']['Val'] = 1
            else:
                alarm_dict['KLAMPO326_3']['Val'] = 0

            if (mem['KMSISO']['Val'] == 1):
                alarm_dict['KLAMPO326_4']['Value'] = mem['KMSISO']['Val']
                alarm_dict['KLAMPO326_4']['Setpoint'] = 1
                alarm_dict['KLAMPO326_4']['Val'] = 1
            else:
                alarm_dict['KLAMPO326_4']['Val'] = 0
            # --------- RK27  MSL 1,2,3 press rate hi(-7.03 kg/cm*2/sec = 6.89E5 Pa/sec)
            # if ((RMSLPR[1] >= mem['CMSLH']['Val']) or
            #         (RMSLPR[2] >= mem['CMSLH']['Val']) or
            #         (RMSLPR[3] >= mem['CMSLH']['Val'])):
            #     alarm_dict['KLAMPO327']['Val'] = 1
            # else:
            #     alarm_dict['KLAMPO327']['Val'] = 0

            # 중복 알람
            # if RMSLPR[1] >= mem['CMSLH']['Val']:
            #     alarm_dict['KLAMPO327_1']['Value'] = RMSLPR[1]
            #     alarm_dict['KLAMPO327_1']['Setpoint'] = mem['CMSLH']['Val']
            #     alarm_dict['KLAMPO327_1']['Val'] = 1
            # else:
            #     alarm_dict['KLAMPO327_1']['Val'] = 0
            #
            # if RMSLPR[2] >= mem['CMSLH']['Val']:
            #     alarm_dict['KLAMPO327_2']['Value'] = RMSLPR[2]
            #     alarm_dict['KLAMPO327_2']['Setpoint'] = mem['CMSLH']['Val']
            #     alarm_dict['KLAMPO327_2']['Val'] = 1
            # else:
            #     alarm_dict['KLAMPO327_2']['Val'] = 0
            #
            # if RMSLPR[3] >= mem['CMSLH']['Val']:
            #     alarm_dict['KLAMPO327_3']['Value'] = RMSLPR[3]
            #     alarm_dict['KLAMPO327_3']['Setpoint'] = mem['CMSLH']['Val']
            #     alarm_dict['KLAMPO327_3']['Val'] = 1
            # else:
            #     alarm_dict['KLAMPO327_3']['Val'] = 0
        # --------- R28  MSL 1,2,3 press low(41.1 kg/cm*2 = 0.403E7 pas)
        # if ((mem['PSG1']['Val'] < mem['CPSTML']['Val']) or
        #         (mem['PSG2']['Val'] < mem['CPSTML']['Val']) or
        #         (mem['PSG3']['Val'] < mem['CPSTML']['Val'])):
        #     alarm_dict['KLAMPO328']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO328']['Val'] = 0

        if mem['PSG1']['Val'] < mem['CPSTML']['Val']:
            alarm_dict['KLAMPO328_1']['Value'] = mem['PSG1']['Val']
            alarm_dict['KLAMPO328_1']['Setpoint'] = mem['CPSTML']['Val']
            alarm_dict['KLAMPO328_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO328_1']['Val'] = 0

        if mem['PSG2']['Val'] < mem['CPSTML']['Val']:
            alarm_dict['KLAMPO328_2']['Value'] = mem['PSG2']['Val']
            alarm_dict['KLAMPO328_2']['Setpoint'] = mem['CPSTML']['Val']
            alarm_dict['KLAMPO328_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO328_2']['Val'] = 0

        if mem['PSG3']['Val'] < mem['CPSTML']['Val']:
            alarm_dict['KLAMPO328_3']['Value'] = mem['PSG3']['Val']
            alarm_dict['KLAMPO328_3']['Setpoint'] = mem['CPSTML']['Val']
            alarm_dict['KLAMPO328_3']['Val'] = 1
        else:
            alarm_dict['KLAMPO328_3']['Val'] = 0
        # --------- R29  AFW(MD) actuated
        # if (mem['KAFWP1']['Val'] == 1) or (mem['KAFWP2']['Val'] == 1) or (mem['KAFWP3']['Val'] == 1):
        #     alarm_dict['KLAMPO329']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO329']['Val'] = 0

        if mem['KAFWP1']['Val'] == 1:
            alarm_dict['KLAMPO329_1']['Value'] = mem['KAFWP1']['Val']
            alarm_dict['KLAMPO329_1']['Setpoint'] = 1
            alarm_dict['KLAMPO329_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO329_1']['Val'] = 0

        if mem['KAFWP2']['Val'] == 1:
            alarm_dict['KLAMPO329_2']['Value'] = mem['KAFWP2']['Val']
            alarm_dict['KLAMPO329_2']['Setpoint'] = 1
            alarm_dict['KLAMPO329_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO329_2']['Val'] = 0

        if mem['KAFWP3']['Val'] == 1:
            alarm_dict['KLAMPO329_3']['Value'] = mem['KAFWP3']['Val']
            alarm_dict['KLAMPO329_3']['Setpoint'] = 1
            alarm_dict['KLAMPO329_3']['Val'] = 1
        else:
            alarm_dict['KLAMPO329_3']['Val'] = 0
        # --------- R30  Condenser level lo(27")
        if mem['ZCOND']['Val'] < mem['CZCNDL']['Val']:
            alarm_dict['KLAMPO330']['Value'] = mem['ZCOND']['Val']
            alarm_dict['KLAMPO330']['Setpoint'] = mem['CZCNDL']['Val']
            alarm_dict['KLAMPO330']['Val'] = 1
        else:
            alarm_dict['KLAMPO330']['Val'] = 0
        # --------- R31  FW pump discharge header press hi
        if mem['PFWPOUT']['Val'] > mem['CPFWOH']['Val']:
            alarm_dict['KLAMPO331']['Value'] = mem['PFWPOUT']['Val']
            alarm_dict['KLAMPO331']['Setpoint'] = mem['CPFWOH']['Val']
            alarm_dict['KLAMPO331']['Val'] = 1
        else:
            alarm_dict['KLAMPO331']['Val'] = 0
        # --------- R32  FW pump trip
        # if (mem['KFWP1']['Val'] + mem['KFWP2']['Val'] + mem['KFWP3']['Val']) == 0:
        #     alarm_dict['KLAMPO332']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO332']['Val'] = 0

        if mem['KFWP1']['Val'] == 0:
            alarm_dict['KLAMPO332_1']['Value'] = mem['KFWP1']['Val']
            alarm_dict['KLAMPO332_1']['Setpoint'] = 0
            alarm_dict['KLAMPO332_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO332_1']['Val'] = 0

        if mem['KFWP2']['Val'] == 0:
            alarm_dict['KLAMPO332_2']['Value'] = mem['KFWP2']['Val']
            alarm_dict['KLAMPO332_2']['Setpoint'] = 0
            alarm_dict['KLAMPO332_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO332_2']['Val'] = 0

        if mem['KFWP3']['Val'] == 0:
            alarm_dict['KLAMPO332_3']['Value'] = mem['KFWP3']['Val']
            alarm_dict['KLAMPO332_3']['Setpoint'] = 0
            alarm_dict['KLAMPO332_3']['Val'] = 1
        else:
            alarm_dict['KLAMPO332_3']['Val'] = 0
        # --------- R33  FW temp hi(231.1 deg C)
        if mem['UFDW']['Val'] > mem['CUFWH']['Val']:
            alarm_dict['KLAMPO333']['Value'] = mem['UFDW']['Val']
            alarm_dict['KLAMPO333']['Setpoint'] = mem['CUFWH']['Val']
            alarm_dict['KLAMPO333']['Val'] = 1
        else:
            alarm_dict['KLAMPO333']['Val'] = 0
        # --------- R34  Condensate pump flow lo(1400 gpm=88.324 kg/s)
        if mem['WCDPO']['Val'] * 0.047 > mem['CWCDPO']['Val']:
            alarm_dict['KLAMPO334']['Value'] = mem['WCDPO']['Val'] * 0.047
            alarm_dict['KLAMPO334']['Setpoint'] = mem['CWCDPO']['Val']
            alarm_dict['KLAMPO334']['Val'] = 1
        else:
            alarm_dict['KLAMPO334']['Val'] = 0
        # --------- R35  Condenser abs press hi(633. mmmHg)
        if mem['PVAC']['Val'] < mem['CPVACH']['Val']:
            alarm_dict['KLAMPO335']['Value'] = mem['PVAC']['Val']
            alarm_dict['KLAMPO335']['Setpoint'] = mem['CPVACH']['Val']
            alarm_dict['KLAMPO335']['Val'] = 1
        else:
            alarm_dict['KLAMPO335']['Val'] = 0
        # --------- R36  Condenser level hi (45" )
        if mem['ZCOND']['Val'] > mem['CZCNDH']['Val']:
            alarm_dict['KLAMPO336']['Value'] = mem['ZCOND']['Val']
            alarm_dict['KLAMPO336']['Setpoint'] = mem['CZCNDH']['Val']
            alarm_dict['KLAMPO336']['Val'] = 1
        else:
            alarm_dict['KLAMPO336']['Val'] = 0
        # --------- R37  TBN trip P-4
        # if (mem['KTBTRIP']['Val'] == 1) and (mem['KRXTRIP']['Val'] == 1):
        #     alarm_dict['KLAMPO337']['Value'] = [mem['KTBTRIP']['Val'], mem['KRXTRIP']['Val']]
        #     alarm_dict['KLAMPO337']['Setpoint'] = [1, 1]
        #     alarm_dict['KLAMPO337']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO337']['Val'] = 0

        if (mem['KTBTRIP']['Val'] == 1):
            alarm_dict['KLAMPO337_1']['Value'] = mem['KTBTRIP']['Val']
            alarm_dict['KLAMPO337_1']['Setpoint'] = 1
            alarm_dict['KLAMPO337_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO337_1']['Val'] = 0

        if (mem['KRXTRIP']['Val'] == 1):
            alarm_dict['KLAMPO337_2']['Value'] = mem['KRXTRIP']['Val']
            alarm_dict['KLAMPO337_2']['Setpoint'] = 1
            alarm_dict['KLAMPO337_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO337_2']['Val'] = 0
        # --------- R38  SG 1,2,3 wtr level hi-hi TBN trip
        CPERMS8 = 0.78
        # if (mem['ZSGNOR1']['Val'] > CPERMS8) or \
        #         (mem['ZSGNOR2']['Val'] > CPERMS8) or \
        #         (mem['ZSGNOR3']['Val'] > CPERMS8):
        #     alarm_dict['KLAMPO338']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO338']['Val'] = 0

        if mem['ZSGNOR1']['Val'] > CPERMS8:
            alarm_dict['KLAMPO338_1']['Value'] = mem['ZSGNOR1']['Val']
            alarm_dict['KLAMPO338_1']['Setpoint'] = CPERMS8
            alarm_dict['KLAMPO338_1']['Val'] = 1
        else:
            alarm_dict['KLAMPO338_1']['Val'] = 0

        if mem['ZSGNOR2']['Val'] > CPERMS8:
            alarm_dict['KLAMPO338_2']['Value'] = mem['ZSGNOR2']['Val']
            alarm_dict['KLAMPO338_2']['Setpoint'] = CPERMS8
            alarm_dict['KLAMPO338_2']['Val'] = 1
        else:
            alarm_dict['KLAMPO338_2']['Val'] = 0

        if mem['ZSGNOR3']['Val'] > CPERMS8:
            alarm_dict['KLAMPO338_3']['Value'] = mem['ZSGNOR3']['Val']
            alarm_dict['KLAMPO338_3']['Setpoint'] = CPERMS8
            alarm_dict['KLAMPO338_3']['Val'] = 1
        else:
            alarm_dict['KLAMPO338_3']['Val'] = 0
        # --------- R39 Condenser vacuum lo TBN trip
        # if (mem['PVAC']['Val'] < 620.0) and (mem['KTBTRIP']['Val'] == 1):
        #     alarm_dict['KLAMPO339']['Value'] = [mem['PVAC']['Val'], mem['KTBTRIP']['Val']]
        #     alarm_dict['KLAMPO339']['Setpoint'] = [620.0, 1]
        #     alarm_dict['KLAMPO339']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO339']['Val'] = 0

        if (mem['PVAC']['Val'] < 620.0):
            alarm_dict['KLAMPO339']['Value'] = mem['PVAC']['Val']
            alarm_dict['KLAMPO339']['Setpoint'] = 620.0
            alarm_dict['KLAMPO339']['Val'] = 1
        else:
            alarm_dict['KLAMPO339']['Val'] = 0
        # --------- R40  TBN overspeed hi TBN trip
        # if (mem['FTURB']['Val'] > 1980.0) and (mem['KTBTRIP']['Val'] == 1):
        #     alarm_dict['KLAMPO340']['Value'] = [mem['FTURB']['Val'], mem['KTBTRIP']['Val']]
        #     alarm_dict['KLAMPO340']['Setpoint'] = [1980.0, 1]
        #     alarm_dict['KLAMPO340']['Val'] = 1
        # else:
        #     alarm_dict['KLAMPO340']['Val'] = 0

        if (mem['FTURB']['Val'] > 1980.0):
            alarm_dict['KLAMPO340']['Value'] = mem['FTURB']['Val']
            alarm_dict['KLAMPO340']['Setpoint'] = 1980.0
            alarm_dict['KLAMPO340']['Val'] = 1
        else:
            alarm_dict['KLAMPO340']['Val'] = 0
        # --------- R42  Gen. brk open
        if mem['KGENB']['Val'] == 0:
            alarm_dict['KLAMPO341']['Value'] = mem['KGENB']['Val']
            alarm_dict['KLAMPO341']['Setpoint'] = 0
            alarm_dict['KLAMPO341']['Val'] = 1
        else:
            alarm_dict['KLAMPO341']['Val'] = 0

        return alarm_dict
    
    def get_on_alarms(self):
        # alarms = [k if self.alarmdb[k]['Val'] == 0 else 0 for k in self.alarmdb.keys()] # Alarm Table Test용
        alarms = [k if self.alarmdb[k]['Val'] == 1 else 0 for k in self.alarmdb.keys()]
        return [] if alarms is None else [i for i in alarms if i != 0]

    def get_alarms(self):
        return self.alarmdb.keys()

    def get_on_alarms_val(self):
        return [self.alarmdb[k]['Value'] for k in self.get_on_alarms()]

    def get_alarm_val(self, para):
        return self.alarmdb[para]['Value']

    def get_on_alarms_des(self):
        return [self.alarmdb[k]['Des'] for k in self.get_on_alarms()]

    def get_alarm_des(self, para):
        return self.alarmdb[para]['Des']

    def get_on_alarms_unit(self):
        return [self.alarmdb[k]['Unit'] for k in self.get_on_alarms()]

    def get_alarms_unit(self, para):
        return self.alarmdb[para]['Unit']

    def get_on_alarms_setpoint(self):
        return [self.alarmdb[k]['Setpoint'] for k in self.get_on_alarms()]

    def get_alarms_setpoint(self, para):
        return self.alarmdb[para]['Setpoint']