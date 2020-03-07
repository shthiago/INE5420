import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from view.main_window import MainWindow
from view.dialog import NewObjectDialog
from view.object_item import ObjectItem
from model import new_object_factory


class Controller:
    """
    Controller for application
    """

    def __init__(self):
        # Init the models structure
        self.objects_list = []

        # Init main interface
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        self.main_window.show()
        self.add_main_window_handlers()

        # Instantiate dialog for adding objects
        self.add_object_dialog = NewObjectDialog()
        self.add_object_dialog.show()
        self.add_object_dialog.setVisible(False)
        self.add_dialog_handlers()

    def run(self):
        """
        Execute the app
        """
        self.app.exec()

    def add_object_handler(self):
        """
        Function to execute when action to create a button is called
        """
        self.add_object_dialog.setVisible(True)

    def add_dialog_handlers(self):
        """
        Add any needed handler to add objects dialog
        """
        # If "Ok" pressed, process data to add object
        self.add_object_dialog.buttonBox.accepted.connect(
            self.dialog_accepted_handler)

        # If "Cancel" pressed, just closes the dialog
        self.add_object_dialog.buttonBox.rejected.connect(
            self.dialog_rejected_handler)

    def dialog_accepted_handler(self):
        """
        Function to be called on accepted option at dialog
        """
        obj_name = self.add_object_dialog.name_input.text().strip()
        tab_name, tab = self.add_object_dialog.active_tab()

        # If name is let empty, mark it to be generate on creation
        if not obj_name:
            obj_name = self.create_unique_obj_name(tab_name)

        elif not self.validate_new_name(obj_name):
            # Popup to  notify user, then return to dialog
            QMessageBox.information(
                self.add_object_dialog,
                'Information',
                'Name already in use!',
                QMessageBox.Ok
            )
            return

        # Create object with a factory, that will identify object type based
        # on active tab, take its values and return object
        status, new_object = new_object_factory(obj_name, tab_name, tab)

        if status['done']:
            self.add_object_to_list(new_object)
            self.add_object_dialog.reset_values()
            self.add_object_dialog.setVisible(False)

        else:
            QMessageBox.information(
                self.add_object_dialog,
                'Error while creating object',
                status['error_msg'],
                QMessageBox.Ok
            )
            return

    def validate_new_name(self, name):
        """
        Validate name based on existing objects on objects list

        Return
        ----------
        True if name can be used, False otherwise
        """
        names = [o.name for o in self.objects_list]
        return not name in names

    def dialog_rejected_handler(self):
        """
        Function to be called on rejected option at dialog
        """
        self.add_object_dialog.reset_values()
        self.add_object_dialog.setVisible(False)

    def add_main_window_handlers(self):
        """
        Connect triggers on main window
        """
        self.main_window.actionAdd_object.triggered.connect(
            self.add_object_handler)

    def create_unique_obj_name(self, tab_name):
        """
        Create unique obj name based on first two letter of tab + number
        """

        i = 0
        while True:
            name = tab_name[0:2] + str(i).zfill(2)
            if self.validate_new_name(name):
                return name

            i += 1

    def add_object_to_list(self, object):
        """
        Add new object to objects list and to view object list
        """
        self.objects_list.append(object)

        item = ObjectItem(object)
        self.main_window.items_model.appendRow(item)


if __name__ == '__main__':
    Controller().run()
