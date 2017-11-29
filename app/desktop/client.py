import sys
from PyQt5.QtWidgets import *


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        input_field = QLineEdit(self)
        input_field.move(30, 100)

        button = QPushButton(self)
        button.move(30, 130)
        button.setText('Отправить')

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Toolbar')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
