from multiprocessing.managers import BaseManager
from multiprocessing import Process
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import socket

from Function_Mem_ShMem import ShMem
from Interface_Main import Main
from Function_IFAP import FunctionIFAP


class Run:
    def make_shmem(self):
        BaseManager.register('ShMem', ShMem)
        manager = BaseManager()
        manager.start()
        mem = manager.ShMem()
        return mem

    def start_process(self):
        """ MainProcess 동작 """
        mem = self.make_shmem()
        p_list = [InterfaceRun(mem), FunctionIFAP(mem)]
        #p_list = [InterfaceRun(mem)]
        #p_list = [FunctionIFAP(mem)]
        [pr_.start() for pr_ in p_list]
        [pr_.join() for pr_ in p_list]  # finished at the same time


class InterfaceRun(Process):
    def __init__(self, mem):
        super().__init__()
        self.Shmem = mem
        
    def run(self) -> None:
        app = QApplication(sys.argv)
        w = Main(self.Shmem)
        w.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    MainProcess = Run()
    MainProcess.start_process()