import sys

from PyQt5 import QtWidgets

from main_ui import Ui_MainWindow


class Application(QtWidgets.QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.label_name = self.ui.labelHello
        self.edit_line = self.ui.lineEdit

        self.ui.pushButton.clicked.connect(self.btn_clicked)

    def btn_clicked(self) -> None:
        name = self.edit_line.text()
        if name != "":
            self.label_name.setText(f"Привет, {name}!!!")
            self.label_name.adjustSize()
        else:
            self.label_name.setText("Введите имя.")
            self.label_name.adjustSize()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Application()
    application.show()

    sys.exit(app.exec())
