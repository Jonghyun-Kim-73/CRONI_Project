import datetime


class ToolEtc:
    @staticmethod
    def get_now_time() -> str:
        """
        현재 시간 정보를 str 로 반환함.

        :return:  str([2020-11-17][14_05_57])
        """
        _time = datetime.datetime.now()
        return f'[{_time.year}-{_time.month}-{_time.day}][{_time.hour}_{_time.minute}_{_time.second}]'

    @staticmethod
    def get_calculated_time(time_val=int) -> str:
        """
        Sec로 된 시간을 [00:00:00]으로 변환함.

        :param time_val: int(xxxx)
        :return: str([00:00:00])
        """
        t_sec = time_val % 60  # x sec
        t_min = time_val // 60  # x min
        t_hour = t_min // 60
        t_min = t_min % 60

        if t_min >= 10:
            t_min = '{}'.format(t_min)
        else:
            t_min = '0{}'.format(t_min)

        if t_sec >= 10:
            t_sec = '{}'.format(t_sec)
        else:
            t_sec = '0{}'.format(t_sec)

        if t_hour >= 10:
            t_hour = '{}'.format(t_hour)
        else:
            t_hour = '0{}'.format(t_hour)
        return '[{}:{}:{}]'.format(t_hour, t_min, t_sec)

    @staticmethod
    def get_op_mode(reactivity, power, cool_leg1_temp):
        """
        :param reactivity: 반응도  CRETIV
        :param power: ZINST1 [%]
        :param cool_leg1_temp: UCOLEG1
        :return:
        """
        if reactivity >= 0:
            if power > 5:
                mode = 1
            elif power <= 5:
                mode = 2
        elif reactivity < 0:
            if cool_leg1_temp >= 177:
                mode = 3
            elif 93 < cool_leg1_temp < 177:
                mode = 4
            elif cool_leg1_temp <= 93:
                mode = 5
        else:
            mode = 6

        return mode

    @staticmethod
    def get_lco_card(LCO_name, currnet_mode, St, Ct, Et, mem):
        cont = '[{}] 현재 운전 모드 : [Mode-{}]\n'.format(LCO_name, currnet_mode)
        cont += '=' * 50 + '\n'
        # --------------------------------------------------------------------------------------------------------------
        cont += 'Follow up action :\n'
        if LCO_name == 'LCO 3.4.4':
            cont += '  - Enter Mode 3\n'
        elif LCO_name == 'LCO 3.4.1':
            cont += '  - 154.7 < RCS Pressure < 161.6 [kg/cm²]\n'
            cont += '  - 286.7 < RCS Cold-leg Temp < 293.3 [℃]\n'
        else:
            cont += '  - None\n'
        # --------------------------------------------------------------------------------------------------------------
        cont += '=' * 50 + '\n'
        cont += '시작 시간\t:\t현재 시간\t:\t종료 시간\n'

        St_ = ToolEtc.get_calculated_time(int(St/5))
        Ct_ = ToolEtc.get_calculated_time(int(Ct/5))
        Et_ = ToolEtc.get_calculated_time(int(Et/5))

        cont += f'{St_}\t:\t{Ct_}\t:\t{Et_}\n'
        cont += '=' * 50 + '\n'
        # --------------------------------------------------------------------------------------------------------------
        ongo_succ = ''
        if LCO_name == 'LCO 3.4.4':
            if currnet_mode == 3:
                ongo_succ = 'Success'
            elif currnet_mode == 1 or currnet_mode == 2:
                ongo_succ = 'Ongoing'

        elif LCO_name == 'LCO 3.4.1':
            if 154.7 < mem['ZINST65']['Val'] < 161.6 and 286.7 < mem['UCOLEG1']['Val'] < 293.3:
                ongo_succ = 'Success'
            else:
                ongo_succ = 'Ongoing'
        else:
            ongo_succ = 'None'

        if Et <= Ct:
            cont += '현재 운전 상태 : Action Fail\n'
        else:
            cont += f'현재 운전 상태 : Action {ongo_succ}\n'

        # --------------------------------------------------------------------------------------------------------------
        cont += '=' * 50 + '\n'

        return cont