import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import QThread
from Worker import Worker


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AuroraTextPaster")

        # Set Vertical layout
        self.setLayout(qtw.QVBoxLayout())

        delay_time = 3

        # Create A Label
        my_label = qtw.QLabel(f'Программа для автокопирования текста', self)
        # Change the font size of label
        my_label.setFont(qtg.QFont('Console', 16))
        self.layout().addWidget(my_label)

        # Create an Text box
        self.my_text = qtw.QTextEdit(self,
                                     acceptRichText=False,
                                     lineWrapMode=qtw.QTextEdit.FixedColumnWidth,
                                     lineWrapColumnOrWidth=75,
                                     placeholderText="Вставьте сюда текст...",
                                     )

        # Change font size of spinbox
        # my_spin.setFont(qtg.QFont('Helvetica', 18))

        # Put combobox on the screen
        self.layout().addWidget(self.my_text)

        # Create a button
        self.pbutton = qtw.QPushButton("Начать вставку", self)
        self.pbutton.clicked.connect(self.textpaste)
        self.layout().addWidget(self.pbutton)

        self.sbutton = qtw.QPushButton("Приостановить", self)
        self.sbutton.clicked.connect(self.stop)

        self.layout().addWidget(self.sbutton)

        # Show the app
        self.show()

    def textpaste(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)


        self.thread.start()
        self.pbutton.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.pbutton.setEnabled(True)
        )

        with open('file.txt', 'w', encoding='utf8') as f:
            stri = self.my_text.toPlainText()
            f.write(stri)
        # Add name to label

    def stop(self):
        self.worker.paster.ongoing = not self.worker.paster.ongoing
        if self.sbutton.text() == 'Приостановить':
            self.sbutton.setText('Возобновить')
        else:
            self.sbutton.setText('Приостановить')



app = qtw.QApplication([])
mw = MainWindow()
app.exec_()
