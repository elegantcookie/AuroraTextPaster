import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import time
from paster import Paster

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # Add a title
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
        my_text = qtw.QTextEdit(self,
                                acceptRichText=False,
                                lineWrapMode=qtw.QTextEdit.FixedColumnWidth,
                                lineWrapColumnOrWidth=75,
                                placeholderText="Вставьте сюда текст...",
                                )

        # Change font size of spinbox
        # my_spin.setFont(qtg.QFont('Helvetica', 18))

        # Put combobox on the screen
        self.layout().addWidget(my_text)

        # Create a button
        pbutton = qtw.QPushButton("Начать вставку",
                                    clicked=lambda: textpaste())
        self.layout().addWidget(pbutton)

        sbutton = qtw.QPushButton("Приостановить",
                                  clicked=lambda: stop())

        self.layout().addWidget(sbutton)
        self.paster = Paster()

        # Show the app
        self.show()

        def textpaste():
            # Add name to label
            time.sleep(3)

            with open('file.txt', 'w', encoding='utf8') as f:
                stri = my_text.toPlainText()
                f.write(stri)

            self.paster.read_from_file()
            self.paster.strip_contents()
            self.paster.start()

        def stop():
            self.paster.ongoing = not self.paster.ongoing



app = qtw.QApplication([])
mw = MainWindow()

# Run The App
app.exec_()