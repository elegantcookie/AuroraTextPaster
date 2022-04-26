import traceback
from time import sleep

from PyQt5.QtCore import QThread
from pynput import keyboard
from connectors import _Connector, TToWConnector
from paster import Paster
from workers import Worker, SimpleWorker, SimpleCallableWorker


class SimpleEvents:
    """ Ивенты для кнопок """

    @staticmethod
    def stop(instance):
        """
        Приостановить/возобновить программу
        Получает состояние через коннектор и воркера
        """
        if instance.paste_connector:
            instance.paste_connector.get_worker().paster.ongoing = not instance.paste_connector.get_worker().paster.ongoing
            if instance.sbutton.text() == 'Приостановить':
                instance.sbutton.setText('Возобновить')
            else:
                instance.sbutton.setText('Приостановить')

    @staticmethod
    def exit():
        """ Выход из программы """
        exit()

    @staticmethod
    def bind_keys(instance):
        """
        Async функция
        Используется Callable воркер, чтобы получать результат функции edit_bind_key
        Чтобы менять название кнопки и заново запускать listener hotkey'я идут
        обращения к заверщенному потоку
        """
        thread = QThread()
        worker = SimpleCallableWorker(SimpleEvents.edit_bind_key)

        instance.bind_btn.setEnabled(False)

        instance.bind_connector = TToWConnector(thread, worker)

        instance.bind_connector.get_thread().finished.connect(
            lambda: instance.bind_btn.setEnabled(True)
        )

        instance.bind_connector.get_thread().finished.connect(
            lambda: instance.bind_btn.setText(instance.bind_connector.get_worker().get_info())
        )
        instance.bind_connector.get_thread().finished.connect(
            lambda: instance.configurator.edit_flag('bind_key', instance.bind_connector.get_worker().get_info())
        )

        instance.bind_connector.get_thread().finished.connect(
            lambda: instance.listener.stop()
        )
        instance.bind_connector.get_thread().finished.connect(
            lambda: instance.hotkey()
        )


    @staticmethod
    def edit_bind_key(instance: Worker):
        """
        Открывает listener пока вводится новый бинд, парсит кнопки и возвращает строку с hotkey

        @param instance: Worker
        @return: str
        """
        arr = []

        def on_release(key):
            #print(f'key pressed: {key}')
            return False

        def on_press(key):
            #print(f'key released: {key}')
            arr.append(key)

        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

        bind_val = ''
        for i in range(len(arr)):
            if isinstance(arr[i], keyboard.Key):
                if 'ctrl' in arr[i].name:
                    bind_val += '<ctrl>+'
                else:
                    bind_val += f'<{arr[i].name}>+'
            else:
                bind_val += chr(arr[i].vk) + '+'

        bind_val = bind_val[:len(bind_val)-1]
        instance.finished.emit()
        return bind_val

    @staticmethod
    def textpaste(instance: Worker):
        """
        Async функция
        Используется Simple воркер, чтобы изменять состояние кнопки идёт обращение к завершенному потоку

        @param instance: Worker
        @return: None
        """
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
        """ Запускает Paster'a/парсинг поля EditText и вывод"""
        instance.paster = Paster()

        sleep(3)

        instance.paster.read_from_file()
        instance.paster.strip_contents()
        instance.paster.start()
        instance.finished.emit()
