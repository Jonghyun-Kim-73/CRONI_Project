import datetime
import os
import sys
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


def p_(c:str, s:str):
    """ 현재 실행 중인 파일의 Prtint 문 호출 """
    file_name = c.split('\\')[-1].split('.')[0]
    print(f'[{file_name:30}][{s}]')


def pc_(class_, s):
    file_name = type(class_).__name__
    print(f'[{file_name:30}][{s}]')


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

    @staticmethod
    def cm_to_px(cm):
        return float(cm * 37.7952755906)

    @staticmethod
    def set_round_frame(target):
        """ 라운드 테두리 """
        path = QPainterPath()
        path.addRoundedRect(QRectF(target.rect()), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        target.setMask(mask)


def AlarmCheck(mem):
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
    alarm_list = []
    for i in range(51, 75):
        if mem[f'KLAMPO2{i}']['Val'] == 1:
            alarm_list.append(f'KLAMPO2{i}')
    for i in range(93, 99):
        if mem[f'KLAMPO2{i}']['Val'] == 1:
            alarm_list.append(f'KLAMPO2{i}')
    #
    # Right panel
    #
    for i in range(1, 10):
        if mem[f'KLAMPO30{i}']['Val'] == 1:
            alarm_list.append(f'KLAMP30{i}')
    for i in range(10, 42):
        if mem[f'KLAMPO3{i}']['Val'] == 1:
            alarm_list.append(f'KLAMPO3{i}')
    return alarm_list


def CLogic(prob):
    if int(np.random.choice(2, 1, p=[1 - prob, prob])[0]) == 1:
        return False, True
    else:
        return True, False


def Actprob(prob, f):
    """ prob % 확률로 1 이 나오면 동작함. """
    if int(np.random.choice(2, 1, p=[1 - prob, prob])[0]) == 1:
        return f
    else:
        return 0


def GetTop(raw_list, get_top):
    """ 리스트에서 최대값 랭크와 인덱스 제공 """
    result = []
    index_ = [i for i in range(len(raw_list))]

    for i in range(get_top):
        max_idx = np.array(raw_list).argmax()

        maxv_ = np.array(raw_list).max()
        maxv_id = index_[max_idx]

        index_.pop(max_idx)
        raw_list.pop(max_idx)

        result.append((maxv_, maxv_id))
    return result


if __name__ == '__main__':
    print(GetTop([1, 1, 4, 5, 10, 2, 3, 6, 2, 3], 5))