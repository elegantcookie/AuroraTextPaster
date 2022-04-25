import traceback
from time import sleep

from PyQt5.QtCore import QThread

from connectors import _Connector, TToWConnector
from paster import Paster
from workers import Worker, SimpleWorker


class SimpleEvents:
    @staticmethod
    def stop(instance):
        if instance.paste_connector:
            instance.paste_connector.get_worker().paster.ongoing = not instance.paste_connector.get_worker().paster.ongoing
            if instance.sbutton.text() == 'Приостановить':
                instance.sbutton.setText('Возобновить')
            else:
                instance.sbutton.setText('Приостановить')

    @staticmethod
    def exit():
        exit()

    @staticmethod
    def bind_keys():
        thread = QThread()
        worker = Worker()

        bind_connector = _Connector(thread, worker)

    @staticmethod
    def textpaste(instance):

        with open('file.txt', 'w', encoding='utf8') as f:
            stri = instance.my_text.toPlainText()
            f.write(stri)

        thread = QThread()
        worker = SimpleWorker(SimpleEvents.func)

        instance.pbutton.setEnabled(False)

        instance.paste_connector = TToWConnector(thread, worker)

        instance.paste_connector.get_thread().finished.connect(
            lambda: instance.pbutton.setEnabled(True)
        )

    @staticmethod
    def func(instance):
        instance.paster = Paster()

        sleep(3)

        instance.paster.read_from_file()
        instance.paster.strip_contents()
        instance.paster.start()
        instance.finished.emit()

