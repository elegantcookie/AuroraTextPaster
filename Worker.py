from PyQt5.QtCore import *
from time import sleep
from paster import Paster

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    paster = Paster()

    def run(self):
        sleep(3)

        self.paster.read_from_file()
        self.paster.strip_contents()
        self.paster.start()
        self.finished.emit()
