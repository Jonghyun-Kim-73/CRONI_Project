from collections.abc import Callable, Iterable, Mapping
from multiprocessing.managers import BaseManager
from multiprocessing import Process
import sys
from typing import Any

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import socket
import time

from AIDAA_Ver21.Function_Mem_ShMem import ShMem
from AIDAA_Ver21.Interface_Main import Main
from AIDAA_Ver21.Function_Simulator_CNS import CNS
from AIDAA_Ver21.Interface_EGIS_Main import *

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
        t = time.time()
        mem = self.make_shmem()
        print(time.time() - t)
        p_list = [InterfaceRun_CNS(mem), InterfaceRun(mem), InterfaceRun_EGIS(mem)]
        [pr_.start() for pr_ in p_list]
        [pr_.join() for pr_ in p_list]  # finished at the same time

class InterfaceRun(Process):
    def __init__(self, mem):
        super(InterfaceRun, self).__init__()
        self.mem = mem
    def run(self) -> None:
        app = QApplication(sys.argv)
        w = Main(self.mem)
        w.show()
        sys.exit(app.exec_())
class InterfaceRun_CNS(Process):
    def __init__(self, mem):
        super(InterfaceRun_CNS, self).__init__()
        self.mem = mem
    def run(self) -> None:
        app = QApplication(sys.argv)
        cns = CNS(self.mem)
        cns.show()
        sys.exit(app.exec_())
class InterfaceRun_EGIS(Process):
    def __init__(self, mem):
        super().__init__()
        self.mem = mem
    def run(self) -> None:
        pass
        # app = QApplication(sys.argv)
        # egis = EGISmain(self)
        # egis.show()
        # sys.exit(app.exec_())

if __name__ == '__main__':
    MainProcess = Run()
    MainProcess.start_process()