import sys

from PyQt5.QtWidgets import QApplication

from view.main_window import MainWindow
from view.dialog import NewObjectDialog


class Controller:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.main_window = MainWindow()
        self.main_window.show()
        self.add_main_window_handlers()

        self.add_object_dialog = NewObjectDialog()
        self.add_object_dialog.show()
        self.add_object_dialog.setVisible(False)
        self.add_dialog_handlers()

    def run(self):
        self.app.exec()

    def add_object_handler(self):
        self.add_object_dialog.setVisible(True)

    def add_dialog_handlers(self):
        # CONTINUE FRUM HERE
        # TODO implement object creation. Need to formulate a Model
        pass

    def add_main_window_handlers(self):
        self.main_window.actionAdd_object.triggered.connect(
            self.add_object_handler)


if __name__ == '__main__':
    Controller().run()
