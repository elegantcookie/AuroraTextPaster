import time, os
from pynput.keyboard import Key, Controller


class Paster:
    """ Класс, который парсит строки и печатает их """
    def __init__(self):
        self.ongoing = True
        self.keyboard = Controller()
        self.contents = []

    def read_from_file(self):
        with open('file.txt', 'r', encoding='utf8') as f:
            self.contents = f.readlines()
        os.remove('file.txt')

    def strip_contents(self):
        for i in range(len(self.contents)):
            self.contents[i] = self.contents[i].rstrip('\n')
            self.contents[i] = self.contents[i].strip('\t')

    def start(self):

        for i in range(len(self.contents)):
            for j in range(len(self.contents[i])):
                if self.ongoing:                    # Параметр для остановки печати
                    if self.contents[i][j] == '.':  # Какие-то проблемы с точками, pynput заменяет их на "/"
                        self.keyboard.press('.')
                        self.keyboard.release('.')
                    else:
                        self.keyboard.press(self.contents[i][j])
                        self.keyboard.release(self.contents[i][j])
                        time.sleep(0.095)           # Магическое число, скорость работы печати, чтобы Аврора не вылетала
                else:
                    time.sleep(5)                   # Запуск работы через 5 секунд после паузы
            self.keyboard.press(Key.enter)
            self.keyboard.release(Key.enter)



