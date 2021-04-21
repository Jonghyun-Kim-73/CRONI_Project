class CSFTree:
    @staticmethod
    def CSF1(TRIP, PR, IR, SR):
        """
        미임계 상태 추적도 만족 불만족
        :param TRIP: Trip 1: Trip 0: Operation
        :param PR: Power Range [100 ~ 0]
        :param IR: Intermediate Range [-3 ~ .. ]
        :param SR: Source Range [0.0 ~ ..]
        :return: {'L': 0 만족, 1: 노랑, 2: 주황, 3: 빨강, 'N': 탈출 단계, 'P': 절차서}
        """
        if TRIP == 1:
            if not PR < 5: # 5%
                return {'L': 3, 'N': 0, 'P': 'S1'}              # GOTO 회복 S.1
            else:
                if IR <= 0:
                    if IR < 1E-9:
                        if SR <= 2: # 원래는 1
                            return {'L': 0, 'N': 1, 'P': 'Ok'}  # OK!
                        else:
                            return {'L': 1, 'N': 2, 'P': 'S2'}  # GOTO 회복 S.2
                    else:
                        if IR < -0.2:
                            return {'L': 0, 'N': 3, 'P': 'Ok'}  # OK!
                        else:
                            return {'L': 1, 'N': 4, 'P': 'S2'}  # GOTO 회복 S.2
                else:
                    return {'L': 2, 'N': 5, 'P': 'S1'}          # GOTO 회복 S.1
        else:
            return {'L': 0, 'N': 6, 'P': 'Ok'}                  # Ok!

    @staticmethod
    def CSF2(TRIP, CET, PT):
        """
        노심냉각 상태 추적도
        :param TRIP: Trip 1: Trip 0: Operation
        :param CET: CoreExitTemp [ .. ~ 326 ]
        :param PT: PTCurve [ 0 만족, 1 불만족 ]
        :return: {'L': 0 만족, 1: 노랑, 2: 주황, 3: 빨강, 'N': 탈출 단계, 'P': 절차서}
        """
        if TRIP == 1:
            if CET < 649:
                if PT == 0:
                    return {'L': 0, 'N': 0, 'P': 'Ok'}            # OK!
                else:
                    if CET < 371:
                        return {'L': 1, 'N': 1, 'P': 'C3'}        # GOTO 회복 C.3
                    else:
                        return {'L': 2, 'N': 2, 'P': 'C2'}        # GOTO 회복 C.2
            else:
                return {'L': 3, 'N': 3, 'P': 'C1'}                # GOTO 회복 C.1
        else:
            return {'L': 0, 'N': 4, 'P': 'Ok'}                    # Ok!

    @staticmethod
    def CSF3(TRIP, SG1N, SG2N, SG3N, SG1P, SG2P, SG3P, SG1F, SG2F, SG3F):
        """
        열제거원 상태 추적도
        :param TRIP: Trip 1: Trip 0: Operation
        :param SG1N: SG 1 Narrow Level [0 ~ 50]
        :param SG2N: SG 2 Narrow Level [0 ~ 50]
        :param SG3N: SG 3 Narrow Level [0 ~ 50]
        :param SG1P: SG 1 Pressrue [ 0 ~ 100 ]
        :param SG2P: SG 2 Pressrue [ 0 ~ 100 ]
        :param SG3P: SG 3 Pressrue [ 0 ~ 100 ]
        :param SG1F: SG 1 Feedwater [ 0 ~ 25 ] in emergency
        :param SG2F: SG 2 Feedwater [ 0 ~ 25 ] in emergency
        :param SG3F: SG 3 Feedwater [ 0 ~ 25 ] in emergency
        :return: {'L': 0 만족, 1: 노랑, 2: 주황, 3: 빨강, 'N': 탈출 단계, 'P': 절차서}
        """
        if TRIP == 1:
            if SG1N >= 6 or SG2N >= 6 or SG3N >= 6:
                pass
            else:
                if SG1F + SG2F + SG3F >= 33:
                    pass
                else:
                    return {'L': 3, 'N': 1, 'P': 'H1'}            # GOTO 회복 H.1
            # --
            if not SG1P < 88.6 and not SG2P < 88.6 and not SG3P < 88.6:
                return {'L': 1, 'N': 2, 'P': 'H2'}                # GOTO 회복 H.2
            else:
                if not SG1N < 78 and not SG2N < 78 and not SG3N < 78:
                    return {'L': 1, 'N': 3, 'P': 'H3'}            # GOTO 회복 H.3
                else:
                    if not SG1P < 83.3 and not SG2P < 83.3 and not SG3P < 83.3:
                        return {'L': 1, 'N': 4, 'P': 'H4'}        # GOTO 회복 H.4
                    else:
                        if not SG1N > 6 and not SG2N > 6 and not SG3N > 6:
                            return {'L': 1, 'N': 5, 'P': 'H5'}    # GOTO 회복 H.5
                        else:
                            return {'L': 0, 'N': 6, 'P': 'Ok'}    # OK!
        else:
            return {'L': 0, 'N': 7, 'P': 'Ok'}                    # Ok!

    @staticmethod
    def CSF4(TRIP, RC1, RC2, RC3, RP, PT, TIME):
        """
        RCS 건전성 상태 추적도
        :param TRIP: Trip 1: Trip 0: Operation
        :param RC1: RCS Cool LOOP 1 [List] [270 ..]
        :param RC2: RCS Cool LOOP 2 [List] [270 ..]
        :param RC3: RCS Cool LOOP 3 [List] [270 ..]
        :param RP: RCS pressure [160 ~ ..]
        :param PT: PTCurve [ 0 만족, 1 불만족 ]
        :param TIME: CNS TIME [List] [5 tick ~ ..]
        :return: {'L': 0 만족, 1: 노랑, 2: 주황, 3: 빨강, 'N': 탈출 단계, 'P': 절차서}
        """
        if TRIP == 1:
            RC1AVG = sum(list(RC1)[:-1]) / len(list(RC1)[:-1])
            RC2AVG = sum(list(RC2)[:-1]) / len(list(RC2)[:-1])
            RC3AVG = sum(list(RC3)[:-1]) / len(list(RC3)[:-1])

            if not RC1[-1] < RC1AVG and not RC2[-1] < RC2AVG and not RC3[-1] < RC3AVG:
                if not PT == 0:
                    return {'L': 3, 'N': 0, 'P': 'P1'}            # GOTO 회복 P.1
                else:
                    if not RC1[-1] > 106 and not RC2[-1] > 106 and not RC3[-1] > 106:
                        return {'L': 2, 'N': 1, 'P': 'P1'}        # GOTO 회복 P.1
                    else:
                        if not RC1[-1] > 136 and not RC2[-1] > 136 and not RC3[-1] > 136:
                            return {'L': 1, 'N': 2, 'P': 'P2'}    # GOTO 회복 P.2
                        else:
                            return {'L': 0, 'N': 3, 'P': 'Ok'}    # Ok!
            else:
                if not RC1[-1] > 177 and not RC2[-1] > 177 and not RC3[-1] > 177:
                    if not PT == 0:
                        if not RC1[-1] > 106 and not RC2[-1] > 106 and not RC3[-1] > 106:
                            return {'L': 2, 'N': 4, 'P': 'P1'}    # GOTO 회복 P.1
                        else:
                            return {'L': 1, 'N': 5, 'P': 'P2'}    # GOTO 회복 P.2
                    else:
                        return {'L': 0, 'N': 6, 'P': 'Ok'}        # Ok!
                else:
                    return {'L': 0, 'N': 7, 'P': 'Ok'}            # Ok!
        else:
            return {'L': 0, 'N': 8, 'P': 'Ok'}                    # Ok!

    @staticmethod
    def CSF5(TRIP, CTP, CTS, CTR):
        """
        격납용기 건전상 상태 추적도
        :param TRIP: Trip 1: Trip 0: Operation
        :param CTP: CTMTPressre     [... ~ 0.2]
        :param CTS: CTMTSumpLevel   [0 ~ ... ]
        :param CTR: CTMTRad         [2.0 ~ ... ]
        :return: {'L': 0 만족, 1: 노랑, 2: 주황, 3: 빨강, 'N': 탈출 단계, 'P': 절차서}
        """
        if TRIP == 1:
            if not CTP < 4.2:
                    return {'L': 3, 'N': 0, 'P': 'Z1'}            # GOTO 회복 Z.1
            else:
                if not CTP < 1.55:
                    return {'L': 2, 'N': 1, 'P': 'Z1'}            # GOTO 회복 Z.1
                else:
                    if not CTS < 0.345:
                        return {'L': 2, 'N': 2, 'P': 'Z2'}        # GOTO 회복 Z.2
                    else:
                        if not CTR < 1E4:
                            return {'L': 1, 'N': 3, 'P': 'Z3'}    # GOTO 회복 Z.3
                        else:
                            return {'L': 0, 'N': 4, 'P': 'Ok'}    # Ok!
        else:
            return {'L': 0, 'N': 5, 'P': 'Ok'}                    # Ok!

    @staticmethod
    def CSF6(TRIP, PZRL):
        """
        RCS 재고량 상태 추적도
        :param TRIP: Trip 1: Trip 0: Operation
        :param PZRL: PZRLevel
        :return: {'L': 0 만족, 1: 노랑, 2: 주황, 3: 빨강, 'N': 탈출 단계, 'P': 절차서}
        """
        if TRIP == 1:
            if not PZRL < 101:  # <----------------------- 원래 92 임
                return {'L': 1, 'N': 0, 'P': 'I1'}            # GOTO 회복 I.1
            else:
                if not PZRL > 17:
                    return {'L': 1, 'N': 1, 'P': 'I2'}        # GOTO 회복 I.2
                else:
                    if not 17 <= PZRL <= 92:
                        return {'L': 1, 'N': 2, 'P': 'I2'}    # GOTO 회복 I.2
                    else:
                        return {'L': 0, 'N': 3, 'P': 'Ok'}    # Ok!
        else:
            return {'L': 0, 'N': 4, 'P': 'Ok'}                # Ok.