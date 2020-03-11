import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from view.main_window import MainWindow
from view.dialog import NewObjectDialog
from view.object_item import ObjectItem
from model import new_object_factory
from model.objects import Point3D, Line, Wireframe


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

        # Initial window settings
        self.window_xmin = 0
        self.window_ymin = 0
        self.window_xmax = 600
        self.window_ymax = 600

        # Viewport values
        self.xvp_min = 0
        self.yvp_min = 0
        self.xvp_max = 600
        self.yvp_max = 600

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
            self.process_viewport()

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

    def process_viewport(self):
        """
        Function to create the window that will be drew into viewport
        """

        # TODO
        # Process what is inside viewport, cuting what should not be drew
        # setting new points and just pass to viewport what it should draw
        transformed_groups_of_points = []
        for obj in self.objects_list:
            if isinstance(obj, Point3D):
                transformed_groups_of_points.append(self.transform_point(obj))

            else:
                pts = []
                for p in obj.points:
                    pts.append(self.transform_point(p))

                transformed_groups_of_points.append(pts)

        self.main_window.viewport.draw_objects(transformed_groups_of_points)

    def transform_point(self, p: Point3D):
        xw = p.x
        yw = p.y

        xwmax = self.window_xmax
        ywmax = self.window_ymax
        xwmin = self.window_xmin
        ywmin = self.window_ymin

        xvpmax = self.xvp_max
        yvpmax = self.yvp_max
        xvpmin = self.xvp_min
        yvpmin = self.yvp_min

        xvp = ((xw - xwmin)/(xwmax - xwmin)) * (xvpmax - xvpmin)
        yvp = (1 - ((yw - ywmin)/(ywmax - ywmin))) * (yvpmax - yvpmin)

        return (xvp, yvp)


if __name__ == '__main__':
    Controller().run()
