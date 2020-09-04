import sys
from typing import List

from PyQt5.QtWidgets import QApplication, QMessageBox, QAction, QColorDialog
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

from src.view.main_window import MainWindow
from src.view.dialog import NewObjectDialog, TransformationDialog
from src.view.object_item import ObjectItem
from src.model import new_object_factory
from src.model.objects import Point3D, Line, Wireframe
from src.model.objects import ViewportObjectRepresentation
from src.control.transform import Transformator


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
        self.add_new_obj_dialog_handlers()

        # Instantiate dialog to input transformations
        self.transform_dialog = TransformationDialog()
        self.transform_dialog.show()
        self.transform_dialog.setVisible(False)
        self.add_transform_dialog_handlers()

        # Initial window settings
        self.window_xmin = -300
        self.window_ymin = -300
        self.window_xmax = 300
        self.window_ymax = 300

        # Viewport values
        self.xvp_min = 0
        self.yvp_min = 0
        self.xvp_max = 600
        self.yvp_max = 600

        self.add_object_to_list(
            Wireframe(name='Cubinho daora', points=[
                Point3D('', 0, 0, 0),
                Point3D('', 100, 0, 0),
                Point3D('', 100, 100, 0),
                Point3D('', 0, 100, 0),
                Point3D('', 0, 0, 0),
                Point3D('', 100, 0, 0),
                Point3D('', 150, 50, 0),
                Point3D('', 150, 150, 0),
                Point3D('', 100, 100, 0),
                Point3D('', 150, 150, 0),
                Point3D('', 50, 150, 0),
                Point3D('', 0, 100, 0),
            ])
        )

        self.process_viewport()

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

    def add_new_obj_dialog_handlers(self):
        """
        Add any needed handler to add objects dialog
        """
        # If "Ok" pressed, process data to add object
        self.add_object_dialog.buttonBox.accepted.connect(
            self.dialog_accepted_handler)

        # If "Cancel" pressed, just closes the dialog
        self.add_object_dialog.buttonBox.rejected.connect(
            self.dialog_rejected_handler)

    def add_transform_dialog_handlers(self):
        """
        Add any needed handler to input transformations parameters dialog
        """
        self.transform_dialog.buttonBox.accepted.connect(
            self.apply_transformation_handler
        )

        self.transform_dialog.buttonBox.rejected.connect(
            self.reject_transformation_handler
        )

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

        self.main_window.in_btn.clicked.connect(
            lambda: self.zoom_handler('in'))

        # self.main_window.zoom_in_btn.clicked.connect(
        #     lambda: )

        # self.main_window.zoom_out_btn.clicked.connect(
        #     lambda: )

        # self.main_window.set_window_btn.clicked.connect(
        #     lambda: )

        self.main_window.out_btn.clicked.connect(
            lambda: self.zoom_handler('out'))

        self.main_window.view_up_btn.clicked.connect(
            lambda: self.window_move_handler('up'))

        self.main_window.view_down_btn.clicked.connect(
            lambda: self.window_move_handler('down'))

        self.main_window.view_left_btn.clicked.connect(
            lambda: self.window_move_handler('left'))

        self.main_window.view_right_btn.clicked.connect(
            lambda: self.window_move_handler('right'))

        # self.main_window.rotate_x_btn.clicked.connect(
        #     lambda: )

        # self.main_window.rotate_y_btn.clicked.connect(
        #     lambda: )

        # self.main_window.rotate_z_btn.clicked.connect(
        #     lambda: )

        self.main_window.color_change_action.triggered.connect(
            self.color_picker_dialog)

        self.main_window.open_transformation_dialog_action.triggered.connect(
            self.transformation_dialog
        )

    def color_picker_dialog(self):
        """
        Pop up color picker window and apply new color to clicked object
        """
        item_clicked = self.main_window.objects_list_view.selectedIndexes()[0]
        item_name = item_clicked.data()
        color = QColorDialog.getColor()

        # Get object with same name as item clicked and change its color
        for obj in self.objects_list:
            if obj.name == item_name:
                obj.color = color
                break
        self.process_viewport()

    def transformation_dialog(self):
        """
        Open transformation dialog
        """
        item_clicked = self.main_window.objects_list_view.selectedIndexes()[0]
        # Set text on transform dialog
        self.transform_dialog.set_target_object(item_clicked.data())
        self.transform_dialog.setVisible(True)

    def window_move_handler(self, mode: str):
        """
        Take step value from input and apply window movementation

        Parameters
        ----------
        mode: str
            'right', 'left', 'up', 'down'
        """
        if mode not in ['right', 'left', 'up', 'down']:
            raise ValueError(
                f'Invalid mode. Receivevd {mode}')

        try:
            step = int(self.main_window.step_input.text())
        except ValueError:
            QMessageBox.information(
                self.add_object_dialog,
                'Error',
                'Step value invalid',
                QMessageBox.Ok
            )
            return

        window_size_x = self.window_xmax - self.window_xmin
        window_size_y = self.window_ymax - self.window_ymin
        offsetx = window_size_x * step/100
        offsety = window_size_y * step/100

        if mode == 'up':
            self.yvp_max += offsety
            self.yvp_min += offsety

        elif mode == 'down':
            self.yvp_max -= offsety
            self.yvp_min -= offsety

        elif mode == 'right':
            self.xvp_max -= offsetx
            self.xvp_min -= offsetx

        elif mode == 'left':
            self.xvp_max += offsetx
            self.xvp_min += offsetx

        self.process_viewport()

    def zoom_handler(self, mode: str):
        """
        Take step value from input and apply zoom

        Paramters
        ----------
        mode: str
            'in' or 'out'

        """
        if mode not in ['in', 'out']:
            raise ValueError(
                f'Invalid mode. Expect in or out, receivevd {mode}')
        try:
            step = int(self.main_window.step_input.text())
        except ValueError:
            QMessageBox.information(
                self.add_object_dialog,
                'Error',
                'Step value invalid',
                QMessageBox.Ok
            )
            return

        # Process step in pct
        if mode == 'in':
            self.window_xmax *= (1 - int(step/2)/100)
            self.window_xmin *= (1 - int(step/2)/100)

            self.window_ymax *= (1 - int(step/2)/100)
            self.window_ymin *= (1 - int(step/2)/100)

        elif mode == 'out':
            self.window_xmax *= (1 + int(step/2)/100)
            self.window_xmin *= (1 + int(step/2)/100)

            self.window_ymax *= (1 + int(step/2)/100)
            self.window_ymin *= (1 + int(step/2)/100)

        # Update objects on viewport
        self.process_viewport()

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

        grid = [Line('gx',
                     Point3D('_gx1', 0, -1000, 0),
                     Point3D('_gx2', 0, 1000, 0),
                     thickness=1),
                Line('gy',
                     Point3D('_gy1', -1000, 0, 0),
                     Point3D('_gy2', 1000, 0, 0),
                     thickness=1)]

        transformed_groups_of_points: List[ViewportObjectRepresentation] = []
        for obj in grid + self.objects_list:
            if isinstance(obj, Point3D):
                transformed_groups_of_points.append(
                    ViewportObjectRepresentation(
                        name=obj.name,
                        points=[self.transform_point(obj)],
                        color=obj.color)
                )

            else:
                pts = []
                for p in obj.points:
                    pts.append(self.transform_point(p))

                transformed_groups_of_points.append(
                    ViewportObjectRepresentation(name=obj.name,
                                                 points=pts,
                                                 color=obj.color,
                                                 thickness=obj.thickness)
                )
        self.main_window.viewport.draw_objects(transformed_groups_of_points)

    def transform_point(self, point: Point3D):
        """
        Apply viewport transformation to a point

        Parameters
        ----------
        p: Point3D

        Return
        ----------
        UnamedPoint3D(x, y) transformed to current viewport
        """
        xw = point.x
        yw = point.y

        xwmax = self.window_xmax
        ywmax = self.window_ymax
        xwmin = self.window_xmin
        ywmin = self.window_ymin

        xvpmax = self.xvp_max
        yvpmax = self.yvp_max
        xvpmin = self.xvp_min
        yvpmin = self.yvp_min

        xvp = ((xw - xwmin)/(xwmax - xwmin)) * (xvpmax - xvpmin) - self.xvp_min
        yvp = (1 - ((yw - ywmin)/(ywmax - ywmin))) * \
            (yvpmax - yvpmin) - self.yvp_min

        return Point3D(name=point.name, x=xvp, y=yvp, z=point.z)

    def apply_transformation_handler(self):
        '''Check active tab on transformation dialog and call correct handler
        '''
        tab_name, tab = self.transform_dialog.active_tab()
        target = self.transform_dialog.target_obj_lbl.text()

        obj = None

        for o in self.objects_list:
            if o.name == target:
                obj = o
                break

        if obj is None:  # obj not found
            raise Exception('Target object not found: ' + target)

        if tab_name == "Move":
            self.transform_move(obj, tab)

        elif tab_name == "Rotate":
            self.transform_rotate(obj, tab)

        else:  # tab_name == "Rescale"
            self.transform_rescale(obj, tab)

        self.transform_dialog.reset_values()
        self.transform_dialog.setVisible(False)
        self.process_viewport()

    def reject_transformation_handler(self):
        '''Reset dialog'''
        self.transform_dialog.setVisible(False)
        self.transform_dialog.reset_values()

    # Functions responsible for transforming objects

    def transform_move(self, obj, tab):
        '''Apply move/translation transformation'''
        transformator = Transformator(obj)

        x = float(tab.x_input.text())
        y = float(tab.y_input.text())
        # z = float(tab.z_input.text())
        option = tab.option_label.text()

        if option == "Vector":
            new_obj = transformator.translate_by_vector(x, y)
        else:  # option == "Point"
            new_obj = transformator.translate_to_point(x, y)

        # inserting new obj in the same index as the transformed obj
        index = self.objects_list.index(obj)
        self.objects_list.pop(index)
        self.objects_list.insert(index, new_obj)

    def transform_rotate(self, obj, tab):
        '''Apply rotate transformation'''
        transformator = Transformator(obj)
        angle = float(tab.degrees_input.text())

        if tab.over_obj_center_radio_btn.isChecked():
            new_obj = transformator.rotate_by_degrees_geometric_center(angle)

        elif tab.over_world_center_radio_btn.isChecked():
            new_obj = transformator.rotate_by_degrees_origin(angle)

        else:  # tab.over_point_radio_btn.isChecked()
            x = float(tab.x_input.text())
            y = float(tab.y_input.text())
            z = 0  # float(tab.z_input.text())
            new_obj = transformator.rotate_by_degrees_point(
                angle, Point3D('rotationPoint', x, y, z))

        # inserting new obj in the same index as the transformed obj
        index = self.objects_list.index(obj)
        self.objects_list.pop(index)
        self.objects_list.insert(index, new_obj)

    def transform_rescale(self, obj, tab):
        '''Apply scaling transformation'''
        scale_factor = float(tab.factor_input.text())
        transformator = Transformator(obj)
        new_obj = transformator.scale(scale_factor, scale_factor)

        # inserting new obj in the same index as the transformed obj
        index = self.objects_list.index(obj)
        self.objects_list.pop(index)
        self.objects_list.insert(index, new_obj)
