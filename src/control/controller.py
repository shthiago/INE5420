'''Cotroller class'''
import sys
import os
from typing import List, Union, Tuple, Set
from math import cos, sin, radians

from PyQt5.QtWidgets import (QApplication, QMessageBox,
                             QColorDialog, QFileDialog)
from PyQt5.QtGui import QColor
from loguru import logger

from src.control.transform import Transformator, Normalizer
from src.model import new_object_factory
from src.model.objects import Point3D, Line, Wireframe, BezierCurve, BSplineCurve, Object3D
from src.model.objects import ViewportObjectRepresentation, BezierCurveSetup
from src.tools.wavefront_reader import read_wavefront
from src.tools.clipper import Clipper, ClipperSetup
from src.view.main_window import MainWindow
from src.view.dialog import NewObjectDialog, TransformationDialog
from src.view.object_item import ObjectItem


class Controller:
    """
    Controller for application
    """

    def __init__(self):
        # Init the models structure
        self.display_file = []

        # Angle between the Vup vector and the world Y axis
        self._vup_angle_degrees = 0

        # Init main interface
        self.app = QApplication(sys.argv)

        self.main_window = MainWindow()
        self.main_window.show()
        self._add_main_window_handlers()

        # Instantiate dialog for adding objects
        self.add_object_dialog = NewObjectDialog()
        self.add_object_dialog.show()
        self.add_object_dialog.setVisible(False)
        self._add_new_obj_dialog_handlers()

        # Instantiate dialog to input transformations
        self.transform_dialog = TransformationDialog()
        self.transform_dialog.show()
        self.transform_dialog.setVisible(False)
        self._add_transform_dialog_handlers()

        # Initial window settings
        self.window_xmin = -300
        self.window_ymin = -300
        self.window_xmax = 300
        self.window_ymax = 300

        # Viewport values
        self.xvp_min = 10  # it was 0, changed for clipping proof
        self.yvp_min = 10  # it was 0, changed for clipping proof
        self.xvp_max = 590  # it was 600, changed for clipping proof
        self.yvp_max = 590  # it was 600, changed for clipping proof

        self.add_object_to_list(
            Object3D(
                name='Objeto3D',
                points=[
                    Point3D('0', x=0, y=0, z=0),
                    Point3D('1', x=100, y=0, z=0),
                    Point3D('2', x=100, y=100, z=0),
                    Point3D('3', x=0, y=100, z=0),
                    Point3D('4', x=0, y=0, z=100),
                    Point3D('5', x=100, y=0, z=100),
                    Point3D('6', x=100, y=100, z=100),
                    Point3D('7', x=0, y=100, z=100),
                ],
                faces=[
                    # [0, 1, 2, 3],
                    [0, 1, 5, 4],
                    [0, 4, 7, 3],
                    [3, 2, 6, 7],
                    [1, 5, 6, 2],
                    # [4, 5, 6, 7]
                ]
            )
        )

        # self.add_object_to_list(
        #     BSplineCurve('Spline',
        #                  points=[
        #                      Point3D('_', x=0, y=0, z=0),
        #                      Point3D('_', x=-100, y=200, z=0),
        #                      Point3D('_', x=-200, y=0, z=0),
        #                      Point3D('_', x=-300, y=-200, z=0),
        #                      Point3D('_', x=-400, y=0, z=0),
        #                      Point3D('_', x=-500, y=500, z=0),
        #                  ])
        # )

        self._process_viewport()

    def run(self):
        """
        Execute the app
        """
        self.app.exec()

    def _add_object_handler(self):
        """
        Function to execute when action to create a button is called
        """
        self.add_object_dialog.setVisible(True)

    def _add_new_obj_dialog_handlers(self):
        """
        Add any needed handler to add objects dialog
        """
        # If "Ok" pressed, process data to add object
        self.add_object_dialog.button_box.accepted.connect(
            self._dialog_accepted_handler)

        # If "Cancel" pressed, just closes the dialog
        self.add_object_dialog.button_box.rejected.connect(
            self._dialog_rejected_handler)

    def _add_transform_dialog_handlers(self):
        """
        Add any needed handler to input transformations parameters dialog
        """
        self.transform_dialog.button_box.accepted.connect(
            self.apply_transformation_handler
        )

        self.transform_dialog.button_box.rejected.connect(
            self.reject_transformation_handler
        )

    def _dialog_accepted_handler(self):
        """
        Function to be called on accepted option at dialog
        """
        obj_name = self.add_object_dialog.name_input.text().strip()
        tab_name, tab = self.add_object_dialog.active_tab()

        # If name is let empty, mark it to be generate on creation
        if not obj_name:
            obj_name = self.create_unique_obj_name(tab_name)

        elif not self._validate_new_name(obj_name):
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
            self._process_viewport()

        else:
            QMessageBox.information(
                self.add_object_dialog,
                'Error while creating object',
                status['error_msg'],
                QMessageBox.Ok
            )
            return

    def _validate_new_name(self, name):
        """
        Validate name based on existing objects on objects list

        Return
        ----------
        True if name can be used, False otherwise
        """
        names = [o.name for o in self.display_file]
        return not name in names

    def _dialog_rejected_handler(self):
        """
        Function to be called on rejected option at dialog
        """
        self.add_object_dialog.reset_values()
        self.add_object_dialog.setVisible(False)

    def _add_main_window_handlers(self):
        """
        Connect triggers on main window
        """
        self.main_window.action_add_object.triggered.connect(
            self._add_object_handler)

        self.main_window.action_export_all_objects.triggered.connect(
            self._export_all_objects_handler)

        self.main_window.action_import_wavefront.triggered.connect(
            self._import_from_file_handler)

        self.main_window.in_btn.clicked.connect(
            lambda: self._zoom_handler('in'))

        self.main_window.out_btn.clicked.connect(
            lambda: self._zoom_handler('out'))

        self.main_window.rotate_left.clicked.connect(
            lambda: self._rotate_handler('left'))

        self.main_window.rotate_right.clicked.connect(
            lambda: self._rotate_handler('right'))

        self.main_window.view_up_btn.clicked.connect(
            lambda: self._window_move_handler('up'))

        self.main_window.view_down_btn.clicked.connect(
            lambda: self._window_move_handler('down'))

        self.main_window.view_left_btn.clicked.connect(
            lambda: self._window_move_handler('left'))

        self.main_window.view_right_btn.clicked.connect(
            lambda: self._window_move_handler('right'))

        # self.main_window.rotate_x_btn.clicked.connect(
        #     lambda: )

        # self.main_window.rotate_y_btn.clicked.connect(
        #     lambda: )

        # self.main_window.rotate_z_btn.clicked.connect(
        #     lambda: )

        self.main_window.color_change_action.triggered.connect(
            self._color_picker_dialog)

        self.main_window.open_transformation_dialog_action.triggered.connect(
            self._transformation_dialog
        )

    def _import_from_file_handler(self):
        '''Get the .obj filepath and call the proper load functions'''
        file = QFileDialog.getOpenFileName()[0]
        self._import_from_file(file)
        self._process_viewport()

    def _import_from_file(self, file: str):
        '''Call wavefront loaders'''
        geoms = read_wavefront(file)

        for name, props in geoms.items():
            if not 'v' in props:
                logger.error(f'Failed to load: {name}, no vertexes')
                continue

            points: List[Point3D] = []
            for x, y, z in props['v']:
                points.append(Point3D(name='', x=x, y=y, z=z))

            color = QColor(0, 0, 0)
            if 'material' in props and 'Kd' in props['material']:
                r, g, b = props['material']['Kd']
                color = QColor(255 * r, 255 * g, 255 * b)

            if not self._validate_new_name(name):
                i = 1
                new_name = f'{name}({i})'
                while not self._validate_new_name(new_name):
                    i += 1
                    new_name = f'{name}({i})'

                name = new_name

            if len(points) == 1:
                # Is a point
                point = points[0]
                point.name = name
                point.color = color
                self.add_object_to_list(point)

            elif len(points) == 2:
                # Is a line
                line = Line(name=name, p1=points[0], p2=points[1])
                line.color = color
                self.add_object_to_list(line)

            elif len(points) > 2:
                # Is a wireframe
                wireframe = Wireframe(name=name, points=points)
                wireframe.color = color
                self.add_object_to_list(wireframe)

    def _export_all_objects_handler(self):
        '''Get a folder from user and call the effective export function'''
        folder = QFileDialog.getExistingDirectory()
        self._export_objects_to(folder)

    def _export_objects_to(self, folder: str):
        '''Save objects generated structure to files in files inside folder'''
        wf_objects, materials = self._generate_export_files()

        wf_objects_filename = 'wf_objects.obj'
        materials_filename = 'materials.mtl'

        wf_objects.insert(0, f'mtllib {materials_filename}')

        with open(os.path.join(folder, wf_objects_filename), 'w') as f:
            for row in wf_objects:
                f.write(row + '\n')

        with open(os.path.join(folder, materials_filename), 'w') as f:
            for row in materials:
                f.write(row + '\n')

    def _generate_export_files(self) -> Tuple[List[str], List[str]]:
        '''Generate list of points and object session for each object'''
        points = self._collect_all_points()
        colors = self._collect_all_colors()

        wf_objects = ['# Vertexes']
        for point in points:
            wf_objects.append(f'v {point[0]} {point[1]} {point[2]}')

        wf_objects += ['', '# Shapes']
        for obj in self.display_file:
            wf_objects.extend(obj.describe_export_with(points, colors))

        materials = ['# Materials lib']
        for color in colors:
            red = color.red()/255
            green = color.green()/255
            blue = color.blue()/255
            materials.extend([
                f'newmtl {color.name()[1:]}',
                f'Kd {red} {green} {blue}'
            ])

        return wf_objects, materials

    def _collect_all_points(self) -> List[Tuple[float, float, float]]:
        '''Read all unique used points by every object'''
        points = set()
        for obj in self.display_file:
            points.update(obj.as_list_of_tuples())

        return list(points)

    def _collect_all_colors(self) -> List[QColor]:
        '''Read all colors in objects'''
        colors = []
        color_names = []
        for obj in self.display_file:
            if obj.color.name()[1:] not in color_names:
                colors.append(obj.color)
                color_names.append(obj.color.name()[1:])

        return colors

    def _rotate_handler(self, direction: str):
        '''Change the vup vector angle'''
        if direction not in ['left', 'right']:
            raise ValueError(f'Invalid rotation direction: {direction}')

        angle = int(self.main_window.rotation_degrees_input.text())

        if direction == 'left':
            self._rotate_left(angle)
        else:
            self._rotate_right(angle)

        self._process_viewport()

    def _rotate_left(self, angle: int):
        '''Rotate vup to left'''
        self._vup_angle_degrees -= angle

    def _rotate_right(self, angle: int):
        '''Rotate vup to right'''
        self._vup_angle_degrees += angle

    def _color_picker_dialog(self):
        """
        Pop up color picker window and apply new color to clicked object
        """
        item_clicked = self.main_window.objects_list_view.selectedIndexes()[0]
        item_name = item_clicked.data()
        color = QColorDialog.getColor()

        # Get object with same name as item clicked and change its color
        for obj in self.display_file:
            if obj.name == item_name:
                obj.color = color
                break
        self._process_viewport()

    def _transformation_dialog(self):
        """
        Open transformation dialog
        """
        item_clicked = self.main_window.objects_list_view.selectedIndexes()[0]
        # Set text on transform dialog
        self.transform_dialog.set_target_object(item_clicked.data())
        self.transform_dialog.setVisible(True)

    def _window_move_handler(self, mode: str):
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

        if mode == 'down':
            rad_angle = radians(180 - self._vup_angle_degrees)
            sen_vup = sin(rad_angle)
            cos_vup = cos(rad_angle)

            self.window_ymax += offsety * cos(rad_angle)
            self.window_ymin += offsety * cos(rad_angle)

            self.window_xmax += offsety * sin(rad_angle)
            self.window_xmin += offsety * sin(rad_angle)

        elif mode == 'up':
            rad_angle = radians(180 - self._vup_angle_degrees)
            sen_vup = sin(rad_angle)
            cos_vup = cos(rad_angle)

            self.window_ymax -= offsety * cos(rad_angle)
            self.window_ymin -= offsety * cos(rad_angle)

            self.window_xmax -= offsety * sin(rad_angle)
            self.window_xmin -= offsety * sin(rad_angle)

        elif mode == 'right':
            rad_angle = radians(self._vup_angle_degrees)
            sen_vup = sin(rad_angle)
            cos_vup = cos(rad_angle)

            self.window_xmax += offsetx * cos_vup
            self.window_xmin += offsetx * cos_vup

            self.window_ymax += offsetx * sen_vup
            self.window_ymin += offsetx * sen_vup

        elif mode == 'left':
            rad_angle = radians(self._vup_angle_degrees)
            sen_vup = sin(rad_angle)
            cos_vup = cos(rad_angle)

            self.window_xmax -= offsetx * cos_vup
            self.window_xmin -= offsetx * cos_vup

            self.window_ymax -= offsetx * sen_vup
            self.window_ymin -= offsetx * sen_vup

        self._process_viewport()

    def _zoom_handler(self, mode: str):
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
        step_x = int((step/100) * (self.window_xmax - self.window_xmin))
        step_y = int((step/100) * (self.window_ymax - self.window_ymin))
        if mode == 'in':
            self.window_xmax -= step_x/2
            self.window_xmin += step_x/2

            self.window_ymax -= step_y/2
            self.window_ymin += step_y/2

        elif mode == 'out':
            self.window_xmax += step_x/2
            self.window_xmin -= step_x/2

            self.window_ymax += step_y/2
            self.window_ymin -= step_y/2

        # Update objects on viewport
        self._process_viewport()

    def create_unique_obj_name(self, tab_name):
        """
        Create unique obj name based on first two letter of tab + number
        """

        i = 0
        while True:
            name = tab_name[0:2] + str(i).zfill(2)
            if self._validate_new_name(name):
                return name

            i += 1

    def add_object_to_list(self, obj):
        """
        Add new object to objects list and to view object list
        """
        self.display_file.append(obj)

        item = ObjectItem(obj)
        self.main_window.items_model.appendRow(item)

    def _process_viewport(self):
        """
        Function to create the window that will be drew into viewport
        """

        grid = [Line('gx',
                     Point3D('_gx1', 0, -10000, 0),
                     Point3D('_gx2', 0, 10000, 0),
                     thickness=1),
                Line('gy',
                     Point3D('_gy1', -10000, 0, 0),
                     Point3D('_gy2', 10000, 0, 0),
                     thickness=1),
                Line('gz',
                     Point3D('_gz1', 0, 0, -10000),
                     Point3D('_gz2', 0, 0, 10000),
                     thickness=1),
                ]

        normalized_display_file = self.get_normalized_display_file(grid=grid)

        # Create clipper for normalized coordinates  system
        clipper_setup = ClipperSetup(xmax=1, xmin=-1, ymax=1, ymin=-1)
        clipper = Clipper(clipper_setup)

        clipped_normalized_display_file = clipper.clip_objects(
            normalized_display_file)

        transformed_groups_of_points: List[ViewportObjectRepresentation] = []
        for obj in clipped_normalized_display_file:
            if isinstance(obj, Point3D):
                transformed_groups_of_points.append(
                    ViewportObjectRepresentation(
                        name=obj.name,
                        points=[self.viewpoert_transform_point(obj)],
                        color=obj.color,
                        thickness=obj.thickness)
                )

            else:
                pts = []
                for p in obj.points:
                    pts.append(self.viewpoert_transform_point(p))
                transformed_groups_of_points.append(
                    ViewportObjectRepresentation(name=obj.name,
                                                 points=pts,
                                                 color=obj.color,
                                                 thickness=obj.thickness)
                )

        self.main_window.viewport.draw_objects(transformed_groups_of_points)

    def get_normalized_display_file(self, grid: List[Line]
                                    ) -> List[Union[Point3D, Line, Wireframe]]:
        '''Take internal Vup vector and rotate grid and internal list of objects'''

        window_center_x = (self.window_xmax + self.window_xmin)/2
        window_center_y = (self.window_ymax + self.window_ymin)/2
        window_width = self.window_ymax - self.window_ymin
        window_height = self.window_xmax - self.window_xmin

        normalizer = Normalizer(
            Point3D('_wc',
                    x=window_center_x,
                    y=window_center_y,
                    z=0),
            window_height,
            window_width,
            vup_angle=self._vup_angle_degrees
        )

        objects_list = []
        curve_step = 0.1
        for obj in self.display_file:
            if isinstance(obj, BezierCurve) or isinstance(obj, BSplineCurve):
                # Switch the curve by its lines
                objects_list.extend(obj.calculate_lines(curve_step))

            elif isinstance(obj, Object3D):
                # Switch object 3d by its wireframes
                objects_list.extend(obj.get_wireframes())

            else:
                objects_list.append(obj)

        objects_list.extend(grid)
        return normalizer.normalize_objects(objects_list)

    def viewpoert_transform_point(self, point: Point3D):
        """
        Apply viewport transformation to a point

        Parameters
        ----------
        p: Point3D

        Return
        ----------
        UnamedPoint3D(x, y) transformed to current viewport
        """

        # xwmax = self.window_xmax
        # ywmax = self.window_ymax
        # xwmin = self.window_xmin
        # ywmin = self.window_ymin
        xwmax = 1
        ywmax = 1
        xwmin = -1
        ywmin = -1

        xvpmax = self.xvp_max
        yvpmax = self.yvp_max
        xvpmin = self.xvp_min
        yvpmin = self.yvp_min

        xvp = ((point.x - xwmin)/(xwmax - xwmin)) * \
            (xvpmax - xvpmin) + xvpmin
        yvp = (1 - ((point.y - ywmin)/(ywmax - ywmin))) * \
            (yvpmax - yvpmin) + yvpmin

        return Point3D(name=point.name, x=xvp, y=yvp, z=point.z)

    def apply_transformation_handler(self):
        '''Check active tab on transformation dialog and call correct handler
        '''
        tab_name, tab = self.transform_dialog.active_tab()
        target = self.transform_dialog.target_obj_lbl.text()

        obj = None

        for o in self.display_file:
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
        self._process_viewport()

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
        z = float(tab.z_input.text())
        option = tab.option_label.text()

        if option == "Vector":
            new_obj = transformator.translate_by_vector(x, y, z)
        else:  # option == "Point"
            new_obj = transformator.translate_to_point(x, y, z)

        # inserting new obj in the same index as the transformed obj
        index = self.display_file.index(obj)
        self.display_file.pop(index)
        self.display_file.insert(index, new_obj)

    def transform_rotate(self, obj, tab):
        '''Apply rotate transformation'''
        transformator = Transformator(obj)
        angle = float(tab.degrees_input.text())
        axis = tab.get_axis()

        if tab.over_obj_center_radio_btn.isChecked():
            new_obj = transformator.rotate_by_degrees_geometric_center(
                angle, axis)

        elif tab.over_world_center_radio_btn.isChecked():
            new_obj = transformator.rotate_by_degrees_origin(angle, axis)

        else:  # tab.over_point_radio_btn.isChecked()
            x = float(tab.x_input.text())
            y = float(tab.y_input.text())
            z = 0  # float(tab.z_input.text())
            new_obj = transformator.rotate_by_degrees_point(
                angle, Point3D('rotationPoint', x, y, z), axis)

        # inserting new obj in the same index as the transformed obj
        index = self.display_file.index(obj)
        self.display_file.pop(index)
        self.display_file.insert(index, new_obj)

    def transform_rescale(self, obj, tab):
        '''Apply scaling transformation'''
        scale_factor = float(tab.factor_input.text())
        transformator = Transformator(obj)
        new_obj = transformator.scale(*3*[scale_factor])

        # inserting new obj in the same index as the transformed obj
        index = self.display_file.index(obj)
        self.display_file.pop(index)
        self.display_file.insert(index, new_obj)
