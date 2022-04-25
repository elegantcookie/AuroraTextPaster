import time, os
from pynput.keyboard import Key, Controller


class Paster:
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

    def start(self):

        for i in range(len(self.contents)):
            for j in range(len(self.contents[i])):
                if self.ongoing:
                    if self.contents[i][j] == '.':
                        self.keyboard.press('.')
                        self.keyboard.release('.')
                    else:
                        self.keyboard.press(self.contents[i][j])
                        self.keyboard.release(self.contents[i][j])
                        time.sleep(0.095)
                else:
                    time.sleep(5)
            self.keyboard.press(Key.enter)
            self.keyboard.release(Key.enter)



