from multiprocessing.managers import BaseManager
from multiprocessing import Process
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from AIDAA_Ver21.Function_Mem_ShMem import ShMem
from AIDAA_Ver21.Interface_Main import Main
from AIDAA_Ver21.Function_Simulator_CNS import CNS


class Run:
    def __init__(self):
        pass

    def make_shmem(self):
        BaseManager.register('ShMem', ShMem)
        manager = BaseManager()
        manager.start()
        mem = manager.ShMem()
        return mem

    def start_process(self):
        """ MainProcess 동작 """
        mem = self.make_shmem()
        p_list = [InterfaceRun(mem)]
        [pr_.start() for pr_ in p_list]
        [pr_.join() for pr_ in p_list]  # finished at the same time


class InterfaceRun(Process):
    def __init__(self, mem):
        super(InterfaceRun, self).__init__()

        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        # font = QFont()
        # font.setFamily("Malgun Gothic")
        # app.setFont(font)
        cns = CNS(mem)
        cns.show()
        w = Main(mem)
        w.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    MainProcess = Run()
    MainProcess.start_process()