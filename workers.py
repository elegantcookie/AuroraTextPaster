from PyQt5.QtCore import *
from time import sleep
from paster import Paster


class Worker(QObject):
    """ Базовый класс """
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        pass


class SimpleWorker(Worker):
    def __init__(self, func):
        """
        Воркер для функций, когда они ничего не возвращают

        @param func: функция
        """
        super().__init__()
        self.func = func

    def run(self):
        """
        Запускает функцию и уведомляет о завершении её работы

        @return: None
        """
        self.func(self)
        self.finished.emit()


class SimpleCallableWorker(Worker):
    def __init__(self, func):
        """
        Воркер для функций, когда они что-нибудь возвращают

        @param func: функция
        """
        super().__init__()
        self.func = func
        self.info = None

    def run(self):
        """
        Запускает функцию и уведомляет о завершении её работы

        @return: Any type
        """
        self.info = self.func(self)
        self.finished.emit()

    def get_info(self):
        return self.info
