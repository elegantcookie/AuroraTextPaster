import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt as qt
from PyQt5.QtGui import QKeyEvent
import logging
from events import SimpleEvents
from confs import Configurator
from pynput import keyboard

import os


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.configurator = Configurator()
        self.paste_connector = None
        self.bind_connector = None
        self.listener = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("AuroraTextPaster")

        self.grid = qtw.QGridLayout()

        delay_time = 3

        self.my_label = qtw.QLabel(f'Программа для автокопирования текста', self)
        self.my_label.setFont(qtg.QFont('Console', 16))

        self.my_text = qtw.QTextEdit(self,
                                     acceptRichText=False,
                                     lineWrapMode=qtw.QTextEdit.FixedColumnWidth,
                                     lineWrapColumnOrWidth=75,
                                     placeholderText="Вставьте сюда текст...",
                                     )

        self.pbutton = qtw.QPushButton("Начать вставку", self)
        self.pbutton.clicked.connect(lambda: SimpleEvents.textpaste(self))

        self.sbutton = qtw.QPushButton("Приостановить", self)
        self.sbutton.clicked.connect(lambda: SimpleEvents.stop(self))

        self.bind_lbl = qtw.QLabel("Вставка по:", self)

        self.shortcut_keyseq = self.configurator.flags['bind_key']
        self.shortcut = qtw.QShortcut(qtg.QKeySequence(self.shortcut_keyseq), self)
        self.shortcut.activated.connect(lambda: SimpleEvents.exit())

        self.bind_btn = qtw.QPushButton(self.shortcut_keyseq, self)
        self.bind_btn.clicked.connect(lambda: SimpleEvents.bind_keys(self))

        self.exit_btn = qtw.QPushButton("Выход", self)
        self.exit_btn.clicked.connect(lambda: SimpleEvents.exit())

        self.setup_grid(grid=self.grid)

        self.show()

    def setup_grid(self, grid):
        self.setLayout(self.grid)
        self.layout().addWidget(self.my_label, 0, 0, 1, 3)
        self.layout().addWidget(self.my_text, 1, 0, 1, 3)
        self.layout().addWidget(self.pbutton, 2, 0, 1, 3)
        self.layout().addWidget(self.sbutton, 3, 0, 1, 3)
        self.layout().addWidget(self.bind_lbl, 4, 0)
        self.bind_lbl.setStyleSheet("margin-left:auto;")
        self.layout().addWidget(self.bind_btn, 4, 1)
        self.bind_btn.setStyleSheet("")
        self.layout().addWidget(self.exit_btn, 4, 2)

    def hotkey(self):
        def on_activate():
            if self.paste_connector:
                SimpleEvents.stop(self)
            self.pbutton.click()

        def for_canonical(f):
            return lambda k: f(self.listener.canonical(k))

        hotkey_val = keyboard.HotKey(
            keyboard.HotKey.parse(self.configurator.flags['bind_key']),
            on_activate)
        self.listener = keyboard.Listener(
            on_press=for_canonical(hotkey_val.press),
            on_release=for_canonical(hotkey_val.release)
        )
        self.listener.start()

app = qtw.QApplication([])
mw = MainWindow()
mw.hotkey()
app.exec_()

