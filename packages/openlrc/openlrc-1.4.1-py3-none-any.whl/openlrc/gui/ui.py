from PySide6.QtWidgets import QApplication, QMainWindow

from myui import Ui_Dialog  # This imports the generated class


class MainWindow(QMainWindow, Ui_Dialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)


# Main entry point
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
