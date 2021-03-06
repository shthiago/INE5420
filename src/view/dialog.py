from PyQt5 import QtCore, QtGui, QtWidgets


class NewObjectDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.numeric_validator = QtGui.QIntValidator(-10000, 10000)

        self.initUi()

    def initUi(self):
        self.resize(400, 300)
        self.setWindowTitle("Create object")
        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setGeometry(QtCore.QRect(130, 260, 171, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)

        self.name_lbl = QtWidgets.QLabel(self)
        self.name_lbl.setGeometry(QtCore.QRect(10, 10, 41, 16))
        self.name_lbl.setText("Name:")

        self.name_input = QtWidgets.QLineEdit(self)
        self.name_input.setGeometry(QtCore.QRect(60, 10, 311, 23))

        self.tab_panel = QtWidgets.QTabWidget(self)
        self.tab_panel.setEnabled(True)
        self.tab_panel.setGeometry(QtCore.QRect(10, 50, 370, 200))

        # Add a point mechanism
        self.point_tab = PointTab()
        self.tab_panel.addTab(self.point_tab, "Point")

        # Add a line mechanism
        self.line_tab = LineTab()
        self.tab_panel.addTab(self.line_tab, "Line")

        # Add wireframe mechanism
        self.wireframe_tab = WireframeTab()
        self.tab_panel.addTab(self.wireframe_tab, "Wireframe")

        # Add wireframe mechanism
        self.curve_tab = CurveTab()
        self.tab_panel.addTab(self.curve_tab, "Curve")

        # Add B Spline mechanism
        self.bspline_tab = BSplineTab()
        self.tab_panel.addTab(self.bspline_tab, "BSpline")

        # Add 3D object
        self._3dobject_tab = _3dObjectTab()
        self.tab_panel.addTab(self._3dobject_tab, "3D Object")

        # Add 3D object
        self._bicub_tab = _BicubicTab()
        self.tab_panel.addTab(self._bicub_tab, "Bicubic")

        self.tab_panel.setCurrentIndex(0)

    def reset_values(self):
        """
        Reset texts on input
        """
        # Reset name
        self.name_input.setText('')

        # Reset inputs for line
        self.line_tab.reset_values()

        # Reset input for point
        self.point_tab.reset_values()

        # Reset input for wireframe
        self.wireframe_tab.reset_values()

        # Reset input for curve
        self.curve_tab.reset_values()

        # Reset input for bspline
        self.bspline_tab.reset_values()

        # Reset input for 3d objecto
        self._3dobject_tab.reset_values()

    def active_tab(self):
        """
        Get active tab from TabWidget
        """

        active_index = self.tab_panel.currentIndex()
        active_tab = self.tab_panel.currentWidget()
        active_tab_name = self.tab_panel.tabText(active_index)

        return active_tab_name, active_tab


class LineTab(QtWidgets.QWidget):
    """
    Tab for holding buttons and inputs for creating a line
    """

    def __init__(self):
        super().__init__()

        self.numeric_validator = QtGui.QIntValidator(-10000, 10000)

        self.start_lbl = QtWidgets.QLabel(self)
        self.start_lbl.setGeometry(QtCore.QRect(10, 10, 191, 16))
        self.start_lbl.setText('Begin')

        self.start_x_coord_line_input = QtWidgets.QLineEdit(self)
        self.start_x_coord_line_input.setGeometry(QtCore.QRect(10, 50, 41, 23))
        self.start_x_coord_line_input.setValidator(self.numeric_validator)

        self.start_y_coord_line_input = QtWidgets.QLineEdit(self)
        self.start_y_coord_line_input.setGeometry(QtCore.QRect(80, 50, 41, 23))
        self.start_y_coord_line_input.setValidator(self.numeric_validator)

        self.start_z_coord_line_input = QtWidgets.QLineEdit(self)
        self.start_z_coord_line_input.setGeometry(
            QtCore.QRect(150, 50, 41, 23))
        self.start_z_coord_line_input.setValidator(self.numeric_validator)

        self.x_lbl_2 = QtWidgets.QLabel(self)
        self.x_lbl_2.setGeometry(QtCore.QRect(20, 30, 21, 16))
        self.x_lbl_2.setText('X')

        self.z_lbl_2 = QtWidgets.QLabel(self)
        self.z_lbl_2.setGeometry(QtCore.QRect(160, 30, 21, 16))
        self.z_lbl_2.setText('Z')

        self.y_lbl_2 = QtWidgets.QLabel(self)
        self.y_lbl_2.setGeometry(QtCore.QRect(90, 30, 21, 16))
        self.y_lbl_2.setText('Y')

        self.end_lbl = QtWidgets.QLabel(self)
        self.end_lbl.setGeometry(QtCore.QRect(10, 90, 101, 16))
        self.end_lbl.setText("End")

        self.end_x_coord_line_input = QtWidgets.QLineEdit(self)
        self.end_x_coord_line_input.setGeometry(QtCore.QRect(10, 130, 41, 23))
        self.end_x_coord_line_input.setValidator(self.numeric_validator)

        self.end_y_coord_line_input = QtWidgets.QLineEdit(self)
        self.end_y_coord_line_input.setGeometry(QtCore.QRect(80, 130, 41, 23))
        self.end_y_coord_line_input.setValidator(self.numeric_validator)

        self.end_z_coord_line_input = QtWidgets.QLineEdit(self)
        self.end_z_coord_line_input.setGeometry(QtCore.QRect(150, 130, 41, 23))
        self.end_z_coord_line_input.setValidator(self.numeric_validator)

        self.x_lbl_3 = QtWidgets.QLabel(self)
        self.x_lbl_3.setGeometry(QtCore.QRect(20, 110, 21, 16))
        self.x_lbl_3.setText('X')

        self.z_lbl_3 = QtWidgets.QLabel(self)
        self.z_lbl_3.setGeometry(QtCore.QRect(160, 110, 21, 16))
        self.z_lbl_3.setText('Z')

        self.y_lbl_3 = QtWidgets.QLabel(self)
        self.y_lbl_3.setGeometry(QtCore.QRect(90, 110, 21, 16))
        self.y_lbl_3.setText('Y')

    def reset_values(self):
        """
        Reset inputs to empty value
        """

        self.start_x_coord_line_input.setText('')
        self.start_y_coord_line_input.setText('')
        self.start_z_coord_line_input.setText('')

        self.end_x_coord_line_input.setText('')
        self.end_y_coord_line_input.setText('')
        self.end_z_coord_line_input.setText('')


class PointTab(QtWidgets.QWidget):
    """
    Tab for holding buttons and inputs for creating a point
    """

    def __init__(self):
        super().__init__()

        self.numeric_validator = QtGui.QIntValidator(-10000, 10000)

        self.z_lbl_pt = QtWidgets.QLabel(self)
        self.z_lbl_pt.setGeometry(QtCore.QRect(160, 30, 21, 16))
        self.z_lbl_pt.setText("Z")

        self.x_lbl_pt = QtWidgets.QLabel(self)
        self.x_lbl_pt.setGeometry(QtCore.QRect(20, 30, 21, 16))
        self.x_lbl_pt.setText("X")

        self.coordinate_lbl_pt = QtWidgets.QLabel(self)
        self.coordinate_lbl_pt.setGeometry(QtCore.QRect(10, 10, 191, 16))
        self.coordinate_lbl_pt.setText("Coordinate")

        self.x_coord_pt_input = QtWidgets.QLineEdit(self)
        self.x_coord_pt_input.setGeometry(QtCore.QRect(10, 50, 41, 23))
        self.x_coord_pt_input.setValidator(self.numeric_validator)

        self.y_coord_pt_input = QtWidgets.QLineEdit(self)
        self.y_coord_pt_input.setGeometry(QtCore.QRect(80, 50, 41, 23))
        self.y_coord_pt_input.setValidator(self.numeric_validator)

        self.z_coord_pt_input = QtWidgets.QLineEdit(self)
        self.z_coord_pt_input.setGeometry(QtCore.QRect(150, 50, 41, 23))
        self.z_coord_pt_input.setValidator(self.numeric_validator)

        self.y_lbl_pt = QtWidgets.QLabel(self)
        self.y_lbl_pt.setGeometry(QtCore.QRect(90, 30, 21, 16))
        self.y_lbl_pt.setText("Y")

    def reset_values(self):
        """
        Reset inputs to empty value
        """
        # Reset inputs for point
        self.x_coord_pt_input.setText('')
        self.y_coord_pt_input.setText('')
        self.z_coord_pt_input.setText('')


class WireframeTab(QtWidgets.QWidget):
    """
    Tab for holding buttons and inputs for creating a point
    """

    def __init__(self):
        super().__init__()
        self.points_list = []

        self.numeric_validator = QtGui.QIntValidator(-10000, 10000)

        self.points_view = QtWidgets.QListView(self)
        self.points_view.setGeometry(QtCore.QRect(160, 10, 200, 150))

        self.points_model = QtGui.QStandardItemModel()
        self.points_view.setModel(self.points_model)

        self.x_lbl_pt = QtWidgets.QLabel(self)
        self.x_lbl_pt.setGeometry(QtCore.QRect(30, 10, 21, 16))
        self.x_lbl_pt.setText("X")

        self.y_lbl_pt = QtWidgets.QLabel(self)
        self.y_lbl_pt.setGeometry(QtCore.QRect(30, 50, 21, 16))
        self.y_lbl_pt.setText("Y")

        self.z_lbl_pt = QtWidgets.QLabel(self)
        self.z_lbl_pt.setGeometry(QtCore.QRect(30, 90, 21, 16))
        self.z_lbl_pt.setText("Z")

        self.x_coord_pt_input = QtWidgets.QLineEdit(self)
        self.x_coord_pt_input.setGeometry(QtCore.QRect(50, 10, 41, 23))
        self.x_coord_pt_input.setValidator(self.numeric_validator)

        self.y_coord_pt_input = QtWidgets.QLineEdit(self)
        self.y_coord_pt_input.setGeometry(QtCore.QRect(50, 50, 41, 23))
        self.y_coord_pt_input.setValidator(self.numeric_validator)

        self.z_coord_pt_input = QtWidgets.QLineEdit(self)
        self.z_coord_pt_input.setGeometry(QtCore.QRect(50, 90, 41, 23))
        self.z_coord_pt_input.setValidator(self.numeric_validator)

        self.add_point_btn = QtWidgets.QPushButton(self)
        self.add_point_btn.setGeometry(QtCore.QRect(30, 130, 100, 40))
        self.add_point_btn.setText('Add point')

        self.add_point_btn.clicked.connect(self.__add_input_values_to_list)

    def __add_input_values_to_list(self):

        try:
            x = int(self.x_coord_pt_input.text())
            y = int(self.y_coord_pt_input.text())
            z = int(self.z_coord_pt_input.text())
        except ValueError as e:
            QtWidgets.QMessageBox.information(
                self,
                'Error while creating point',
                str(e),
                QtWidgets.QMessageBox.Ok
            )
            return

        self.reset_values
        self.points_list.append((x, y, z))
        item = QtGui.QStandardItem(f'({x}, {y}, {z})')
        item.setEditable(False)
        self.points_model.appendRow(item)
        self.x_coord_pt_input.clear()
        self.y_coord_pt_input.clear()
        self.z_coord_pt_input.clear()

    def reset_values(self):
        """
        Reset inputs to empty value
        """

        self.x_coord_pt_input.clear()
        self.y_coord_pt_input.clear()
        self.z_coord_pt_input.clear()
        self.points_model.clear()
        self.points_list.clear()


class CurveTab(QtWidgets.QWidget):
    """
    Tab for holding buttons and inputs for creating a point
    """

    def __init__(self):
        super().__init__()
        self.curves_list = []

        self.numeric_validator = QtGui.QIntValidator(-10000, 10000)

        self.points_view = QtWidgets.QListView(self)
        self.points_view.setGeometry(QtCore.QRect(200, 10, 160, 150))
        self.points_model = QtGui.QStandardItemModel()
        self.points_view.setModel(self.points_model)

        self.x_lbl_pt = QtWidgets.QLabel(self)
        self.x_lbl_pt.setGeometry(QtCore.QRect(50, 10, 20, 15))
        self.x_lbl_pt.setText("X")

        self.y_lbl_pt = QtWidgets.QLabel(self)
        self.y_lbl_pt.setGeometry(QtCore.QRect(100, 10, 20, 15))
        self.y_lbl_pt.setText("Y")

        self.z_lbl_pt = QtWidgets.QLabel(self)
        self.z_lbl_pt.setGeometry(QtCore.QRect(150, 10, 20, 15))
        self.z_lbl_pt.setText("Z")

        dist_top_to_first_label = 35
        dist_left_to_label = 10
        dist_label_to_x_input = 30
        dist_from_input_to_input = 50
        dist_vertical_label_to_label = 25
        self.p1_lbl = QtWidgets.QLabel(self)
        self.p1_lbl.setText('P1')
        self.p1_lbl.setGeometry(QtCore.QRect(dist_left_to_label,
                                             dist_top_to_first_label,
                                             20, 23))
        self.x_coord_p1_input = QtWidgets.QLineEdit(self)
        self.x_coord_p1_input.setGeometry(
            QtCore.QRect(dist_left_to_label + dist_label_to_x_input,
                         dist_top_to_first_label,
                         40, 20))
        self.x_coord_p1_input.setValidator(self.numeric_validator)

        self.y_coord_p1_input = QtWidgets.QLineEdit(self)
        self.y_coord_p1_input.setGeometry(
            QtCore.QRect(dist_left_to_label + dist_label_to_x_input + dist_from_input_to_input,
                         dist_top_to_first_label,
                         40, 20))
        self.y_coord_p1_input.setValidator(self.numeric_validator)

        self.z_coord_p1_input = QtWidgets.QLineEdit(self)
        self.z_coord_p1_input.setGeometry(
            QtCore.QRect(dist_left_to_label + dist_label_to_x_input + 2 * dist_from_input_to_input,
                         dist_top_to_first_label,
                         40, 20))
        self.z_coord_p1_input.setValidator(self.numeric_validator)

        self.p2_lbl = QtWidgets.QLabel(self)
        self.p2_lbl.setText('P2')
        self.p2_lbl.setGeometry(QtCore.QRect(dist_left_to_label,
                                             dist_top_to_first_label + dist_vertical_label_to_label,
                                             20, 23))
        self.x_coord_p2_input = QtWidgets.QLineEdit(self)
        self.x_coord_p2_input.setGeometry(
            QtCore.QRect(dist_left_to_label + dist_label_to_x_input,
                         dist_top_to_first_label + dist_vertical_label_to_label,
                         40, 20))
        self.x_coord_p2_input.setValidator(self.numeric_validator)

        self.y_coord_p2_input = QtWidgets.QLineEdit(self)
        self.y_coord_p2_input.setGeometry(
            QtCore.QRect(dist_left_to_label + dist_label_to_x_input + dist_from_input_to_input,
                         dist_top_to_first_label + dist_vertical_label_to_label,
                         40, 20))
        self.y_coord_p2_input.setValidator(self.numeric_validator)

        self.z_coord_p2_input = QtWidgets.QLineEdit(self)
        self.z_coord_p2_input.setGeometry(
            QtCore.QRect(dist_left_to_label + dist_label_to_x_input + 2 * dist_from_input_to_input,
                         dist_top_to_first_label + dist_vertical_label_to_label,
                         40, 20))
        self.z_coord_p2_input.setValidator(self.numeric_validator)

        self.p3_lbl = QtWidgets.QLabel(self)
        self.p3_lbl.setText('P3')
        self.p3_lbl.setGeometry(QtCore.QRect(dist_left_to_label,
                                             dist_top_to_first_label + 2 * dist_vertical_label_to_label,
                                             20, 23))
        self.x_coord_p3_input = QtWidgets.QLineEdit(self)
        self.x_coord_p3_input.setGeometry(
            QtCore.QRect(dist_left_to_label + dist_label_to_x_input,
                         dist_top_to_first_label + 2 * dist_vertical_label_to_label,
                         40, 20))
        self.x_coord_p3_input.setValidator(self.numeric_validator)

        self.y_coord_p3_input = QtWidgets.QLineEdit(self)
        self.y_coord_p3_input.setGeometry(
            QtCore.QRect(dist_left_to_label + dist_label_to_x_input + dist_from_input_to_input,
                         dist_top_to_first_label + 2 * dist_vertical_label_to_label,
                         40, 20))
        self.y_coord_p3_input.setValidator(self.numeric_validator)

        self.z_coord_p3_input = QtWidgets.QLineEdit(self)
        self.z_coord_p3_input.setGeometry(
            QtCore.QRect(dist_left_to_label + dist_label_to_x_input + 2 * dist_from_input_to_input,
                         dist_top_to_first_label + 2 * dist_vertical_label_to_label,
                         40, 20))
        self.z_coord_p3_input.setValidator(self.numeric_validator)

        self.p4_lbl = QtWidgets.QLabel(self)
        self.p4_lbl.setText('P4')
        self.p4_lbl.setGeometry(QtCore.QRect(dist_left_to_label,
                                             dist_top_to_first_label + 3 * dist_vertical_label_to_label,
                                             20, 23))
        self.x_coord_p4_input = QtWidgets.QLineEdit(self)
        self.x_coord_p4_input.setGeometry(
            QtCore.QRect(dist_left_to_label + dist_label_to_x_input,
                         dist_top_to_first_label + 3 * dist_vertical_label_to_label,
                         40, 20))
        self.x_coord_p4_input.setValidator(self.numeric_validator)

        self.y_coord_p4_input = QtWidgets.QLineEdit(self)
        self.y_coord_p4_input.setGeometry(
            QtCore.QRect(dist_left_to_label + dist_label_to_x_input + dist_from_input_to_input,
                         dist_top_to_first_label + 3 * dist_vertical_label_to_label,
                         40, 20))
        self.y_coord_p4_input.setValidator(self.numeric_validator)

        self.z_coord_p4_input = QtWidgets.QLineEdit(self)
        self.z_coord_p4_input.setGeometry(
            QtCore.QRect(dist_left_to_label + dist_label_to_x_input + 2 * dist_from_input_to_input,
                         dist_top_to_first_label + 3 * dist_vertical_label_to_label,
                         40, 20))
        self.z_coord_p4_input.setValidator(self.numeric_validator)

        self.add_point_btn = QtWidgets.QPushButton(self)
        self.add_point_btn.setGeometry(QtCore.QRect(50, 140, 100, 25))
        self.add_point_btn.setText('Add curve')

        self.add_point_btn.clicked.connect(self.__add_input_values_to_list)

    def __add_input_values_to_list(self):

        try:
            p1_x = int(self.x_coord_p1_input.text())
            p1_y = int(self.y_coord_p1_input.text())
            p1_z = int(self.z_coord_p1_input.text())

            p2_x = int(self.x_coord_p2_input.text())
            p2_y = int(self.y_coord_p2_input.text())
            p2_z = int(self.z_coord_p2_input.text())

            p3_x = int(self.x_coord_p3_input.text())
            p3_y = int(self.y_coord_p3_input.text())
            p3_z = int(self.z_coord_p3_input.text())

            p4_x = int(self.x_coord_p4_input.text())
            p4_y = int(self.y_coord_p4_input.text())
            p4_z = int(self.z_coord_p4_input.text())

        except ValueError as e:
            QtWidgets.QMessageBox.information(
                self,
                'Error while creating point',
                str(e),
                QtWidgets.QMessageBox.Ok
            )
            return

        self.curves_list.append({
            'P1': {'x': p1_x, 'y': p1_y, 'z': p1_z},
            'P2': {'x': p2_x, 'y': p2_y, 'z': p2_z},
            'P3': {'x': p3_x, 'y': p3_y, 'z': p3_z},
            'P4': {'x': p4_x, 'y': p4_y, 'z': p4_z},
        })
        items = []
        items.append(QtGui.QStandardItem(f'P1 ({p1_x}, {p1_y}, {p1_z})'))
        items.append(QtGui.QStandardItem(f'P2 ({p2_x}, {p2_y}, {p2_z})'))
        items.append(QtGui.QStandardItem(f'P3 ({p3_x}, {p3_y}, {p3_z})'))
        items.append(QtGui.QStandardItem(f'P4 ({p4_x}, {p4_y}, {p4_z})'))
        for item in items:
            item.setEditable(False)
            self.points_model.appendRow(item)

        self.x_coord_p1_input.clear()
        self.y_coord_p1_input.clear()
        self.z_coord_p1_input.clear()
        self.x_coord_p2_input.clear()
        self.y_coord_p2_input.clear()
        self.z_coord_p2_input.clear()
        self.x_coord_p3_input.clear()
        self.y_coord_p3_input.clear()
        self.z_coord_p3_input.clear()
        self.x_coord_p4_input.clear()
        self.y_coord_p4_input.clear()
        self.z_coord_p4_input.clear()

    def reset_values(self):
        """
        Reset inputs to empty value
        """

        self.x_coord_p1_input.clear()
        self.y_coord_p1_input.clear()
        self.z_coord_p1_input.clear()
        self.x_coord_p2_input.clear()
        self.y_coord_p2_input.clear()
        self.z_coord_p2_input.clear()
        self.x_coord_p3_input.clear()
        self.y_coord_p3_input.clear()
        self.z_coord_p3_input.clear()
        self.x_coord_p4_input.clear()
        self.y_coord_p4_input.clear()
        self.z_coord_p4_input.clear()
        self.points_model.clear()
        self.curves_list.clear()

class _3dObjectTab(QtWidgets.QWidget):
    """
    Tab for holding buttons and inputs for creating a point
    """

    def __init__(self):
        super().__init__()
        self.points_list_3d = []
        self.faces_list_3d=[]

        self.numeric_validator = QtGui.QIntValidator(-10000, 10000)

        self.points_view_3d = QtWidgets.QListView(self)
        self.points_view_3d.setGeometry(QtCore.QRect(80, 10, 100, 150))

        self.points_model_3d = QtGui.QStandardItemModel()
        self.points_view_3d.setModel(self.points_model_3d)

        self.x_lbl_pt_3d = QtWidgets.QLabel(self)
        self.x_lbl_pt_3d.setGeometry(QtCore.QRect(10, 10, 21, 16))
        self.x_lbl_pt_3d.setText("X")

        self.y_lbl_pt_3d = QtWidgets.QLabel(self)
        self.y_lbl_pt_3d.setGeometry(QtCore.QRect(10, 50, 21, 16))
        self.y_lbl_pt_3d.setText("Y")

        self.z_lbl_pt_3d = QtWidgets.QLabel(self)
        self.z_lbl_pt_3d.setGeometry(QtCore.QRect(10, 90, 21, 16))
        self.z_lbl_pt_3d.setText("Z")

        self.x_coord_pt_input_3d = QtWidgets.QLineEdit(self)
        self.x_coord_pt_input_3d.setGeometry(QtCore.QRect(30, 10, 41, 23))
        self.x_coord_pt_input_3d.setValidator(self.numeric_validator)

        self.y_coord_pt_input_3d = QtWidgets.QLineEdit(self)
        self.y_coord_pt_input_3d.setGeometry(QtCore.QRect(30, 50, 41, 23))
        self.y_coord_pt_input_3d.setValidator(self.numeric_validator)

        self.z_coord_pt_input_3d = QtWidgets.QLineEdit(self)
        self.z_coord_pt_input_3d.setGeometry(QtCore.QRect(30, 90, 41, 23))
        self.z_coord_pt_input_3d.setValidator(self.numeric_validator)

        self.faces_lbl_3d = QtWidgets.QLabel(self)
        self.faces_lbl_3d.setGeometry(QtCore.QRect(190, 10, 200, 32))
        self.faces_lbl_3d.setText("Faces (separate \n# with ,)")

        self.faces_input_3d = QtWidgets.QLineEdit(self)
        self.faces_input_3d.setGeometry(QtCore.QRect(190, 50, 41, 23))

        self.add_face_btn_3d = QtWidgets.QPushButton(self)
        self.add_face_btn_3d.setGeometry(QtCore.QRect(190, 90, 60, 40))
        self.add_face_btn_3d.setText('Add face')

        self.add_face_btn_3d.clicked.connect(self.__add_input_faces_to_list)

        self.faces_view_3d = QtWidgets.QListView(self)
        self.faces_view_3d.setGeometry(QtCore.QRect(260, 52, 80, 100))

        self.faces_model_3d = QtGui.QStandardItemModel()
        self.faces_view_3d.setModel(self.faces_model_3d)

        self.add_point_btn_3d = QtWidgets.QPushButton(self)
        self.add_point_btn_3d.setGeometry(QtCore.QRect(10, 130, 60, 40))
        self.add_point_btn_3d.setText('Add point')

        self.add_point_btn_3d.clicked.connect(self.__add_input_values_to_list)

    def __add_input_values_to_list(self):

        try:
            x = int(self.x_coord_pt_input_3d.text())
            y = int(self.y_coord_pt_input_3d.text())
            z = int(self.z_coord_pt_input_3d.text())
        except ValueError as e:
            QtWidgets.QMessageBox.information(
                self,
                'Error while creating point',
                str(e),
                QtWidgets.QMessageBox.Ok
            )
            return

        self.reset_point_values
        self.points_list_3d.append((x, y, z))
        item = QtGui.QStandardItem(f'[{len(self.points_list_3d)}] = ({x}, {y}, {z})')
        item.setEditable(False)
        self.points_model_3d.appendRow(item)
        self.x_coord_pt_input_3d.clear()
        self.y_coord_pt_input_3d.clear()
        self.z_coord_pt_input_3d.clear()

    def __add_input_faces_to_list(self):

        try:
            points_on_face = []
            faces = self.faces_input_3d.text()
            for p in faces.split(','):
                if len(p)>0:
                    points_on_face.append(int(p)-1)
        except ValueError as e:
            QtWidgets.QMessageBox.information(
                self,
                'Error while inserting face',
                str(e),
                QtWidgets.QMessageBox.Ok
            )
            return

        self.reset_face_values
        self.faces_list_3d.append(points_on_face)
        item = QtGui.QStandardItem(self.faces_input_3d.text())
        item.setEditable(False)
        self.faces_model_3d.appendRow(item)
        self.faces_input_3d.clear()
    
    def reset_values(self):
        """
        Reset inputs to empty value
        """

        self.reset_point_values()
        self.reset_face_values()


    def reset_point_values(self):
        """
        Reset inputs to empty value
        """

        self.x_coord_pt_input_3d.clear()
        self.y_coord_pt_input_3d.clear()
        self.z_coord_pt_input_3d.clear()
        self.points_model_3d.clear()
        self.points_list_3d.clear()
    
    def reset_face_values(self):
        """
        Reset inputs to empty value
        """

        self.faces_input_3d.clear()

class BSplineTab(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.points_list = []

        self.numeric_validator = QtGui.QIntValidator(-10000, 10000)

        self.points_view = QtWidgets.QListView(self)
        self.points_view.setGeometry(QtCore.QRect(160, 10, 200, 150))

        self.points_model = QtGui.QStandardItemModel()
        self.points_view.setModel(self.points_model)

        self.x_lbl_pt = QtWidgets.QLabel(self)
        self.x_lbl_pt.setGeometry(QtCore.QRect(30, 10, 21, 16))
        self.x_lbl_pt.setText("X")

        self.y_lbl_pt = QtWidgets.QLabel(self)
        self.y_lbl_pt.setGeometry(QtCore.QRect(30, 50, 21, 16))
        self.y_lbl_pt.setText("Y")

        self.z_lbl_pt = QtWidgets.QLabel(self)
        self.z_lbl_pt.setGeometry(QtCore.QRect(30, 90, 21, 16))
        self.z_lbl_pt.setText("Z")

        self.x_coord_pt_input = QtWidgets.QLineEdit(self)
        self.x_coord_pt_input.setGeometry(QtCore.QRect(50, 10, 41, 23))
        self.x_coord_pt_input.setValidator(self.numeric_validator)

        self.y_coord_pt_input = QtWidgets.QLineEdit(self)
        self.y_coord_pt_input.setGeometry(QtCore.QRect(50, 50, 41, 23))
        self.y_coord_pt_input.setValidator(self.numeric_validator)

        self.z_coord_pt_input = QtWidgets.QLineEdit(self)
        self.z_coord_pt_input.setGeometry(QtCore.QRect(50, 90, 41, 23))
        self.z_coord_pt_input.setValidator(self.numeric_validator)

        self.add_point_btn = QtWidgets.QPushButton(self)
        self.add_point_btn.setGeometry(QtCore.QRect(30, 130, 100, 40))
        self.add_point_btn.setText('Add point')

        self.add_point_btn.clicked.connect(self.__add_input_values_to_list)

    def __add_input_values_to_list(self):

        try:
            x = int(self.x_coord_pt_input.text())
            y = int(self.y_coord_pt_input.text())
            z = int(self.z_coord_pt_input.text())
        except ValueError as e:
            QtWidgets.QMessageBox.information(
                self,
                'Error while creating point',
                str(e),
                QtWidgets.QMessageBox.Ok
            )
            return

        self.points_list.append((x, y, z))
        item = QtGui.QStandardItem(f'({x}, {y}, {z})')
        item.setEditable(False)
        self.points_model.appendRow(item)
        self.x_coord_pt_input.clear()
        self.y_coord_pt_input.clear()
        self.z_coord_pt_input.clear()

    def reset_values(self):
        """
        Reset inputs to empty value
        """

        self.x_coord_pt_input.clear()
        self.y_coord_pt_input.clear()
        self.z_coord_pt_input.clear()
        self.points_model.clear()
        self.points_list.clear()

class _BicubicTab(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.points_list = []

        self.numeric_validator = QtGui.QIntValidator(-10000, 10000)

        self.points_view = QtWidgets.QListView(self)
        self.points_view.setGeometry(QtCore.QRect(160, 10, 200, 150))

        self.points_model = QtGui.QStandardItemModel()
        self.points_view.setModel(self.points_model)

        self.x_lbl_pt = QtWidgets.QLabel(self)
        self.x_lbl_pt.setGeometry(QtCore.QRect(30, 10, 21, 16))
        self.x_lbl_pt.setText("X")

        self.y_lbl_pt = QtWidgets.QLabel(self)
        self.y_lbl_pt.setGeometry(QtCore.QRect(30, 50, 21, 16))
        self.y_lbl_pt.setText("Y")

        self.z_lbl_pt = QtWidgets.QLabel(self)
        self.z_lbl_pt.setGeometry(QtCore.QRect(30, 90, 21, 16))
        self.z_lbl_pt.setText("Z")

        self.x_coord_pt_input = QtWidgets.QLineEdit(self)
        self.x_coord_pt_input.setGeometry(QtCore.QRect(50, 10, 41, 23))
        self.x_coord_pt_input.setValidator(self.numeric_validator)

        self.y_coord_pt_input = QtWidgets.QLineEdit(self)
        self.y_coord_pt_input.setGeometry(QtCore.QRect(50, 50, 41, 23))
        self.y_coord_pt_input.setValidator(self.numeric_validator)

        self.z_coord_pt_input = QtWidgets.QLineEdit(self)
        self.z_coord_pt_input.setGeometry(QtCore.QRect(50, 90, 41, 23))
        self.z_coord_pt_input.setValidator(self.numeric_validator)

        self.add_point_btn = QtWidgets.QPushButton(self)
        self.add_point_btn.setGeometry(QtCore.QRect(30, 130, 100, 40))
        self.add_point_btn.setText('Add point')

        self.add_point_btn.clicked.connect(self.__add_input_values_to_list)

    def __add_input_values_to_list(self):

        try:
            x = int(self.x_coord_pt_input.text())
            y = int(self.y_coord_pt_input.text())
            z = int(self.z_coord_pt_input.text())
        except ValueError as e:
            QtWidgets.QMessageBox.information(
                self,
                'Error while creating point',
                str(e),
                QtWidgets.QMessageBox.Ok
            )
            return

        self.reset_values
        self.points_list.append((x, y, z))
        item = QtGui.QStandardItem(f'({x}, {y}, {z})')
        item.setEditable(False)
        self.points_model.appendRow(item)
        self.x_coord_pt_input.clear()
        self.y_coord_pt_input.clear()
        self.z_coord_pt_input.clear()

    def reset_values(self):
        """
        Reset inputs to empty value
        """

        self.x_coord_pt_input.clear()
        self.y_coord_pt_input.clear()
        self.z_coord_pt_input.clear()
        self.points_model.clear()
        self.points_list.clear()



# Transformation dialog items
class TransformationDialog(QtWidgets.QDialog):
    """
    Window to input transformations to points
    """

    def __init__(self):
        super().__init__()

        self.numeric_validator = QtGui.QIntValidator(-10000, 10000)

        self.initUi()

    def initUi(self):
        '''Initialize elements for dialog'''
        self.resize(400, 300)
        self.setWindowTitle("Apply transformation")
        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setGeometry(QtCore.QRect(130, 260, 171, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)

        self.name_lbl = QtWidgets.QLabel(self)
        self.name_lbl.setGeometry(QtCore.QRect(10, 10, 110, 16))
        self.name_lbl.setText("Modifying object:")

        self.target_obj_lbl = QtWidgets.QLabel(self)
        self.target_obj_lbl.setGeometry(QtCore.QRect(120, 10, 350, 16))

        self.tab_panel = QtWidgets.QTabWidget(self)
        self.tab_panel.setEnabled(True)
        self.tab_panel.setGeometry(QtCore.QRect(10, 50, 370, 200))

        self.rotate_tab = RotateTab()
        self.tab_panel.addTab(self.rotate_tab, 'Rotate')

        self.move_tab = MoveTab()
        self.tab_panel.addTab(self.move_tab, 'Move')

        self.rescale_tab = RescaleTab()
        self.tab_panel.addTab(self.rescale_tab, 'Rescale')

    def set_target_object(self, text):
        """
        Set text after "Modifying object"
        """

        self.target_obj_lbl.setText(text)

    def active_tab(self):
        """
        Get active tab from TabWidget
        """

        active_index = self.tab_panel.currentIndex()
        active_tab = self.tab_panel.currentWidget()
        active_tab_name = self.tab_panel.tabText(active_index)

        return active_tab_name, active_tab

    def get_axis(self):
        """
        Get selected axis to rotate
        """
        return self.rotate_tab.get_axis()

    def reset_values(self):
        '''Reset dialog values'''
        self.rescale_tab.reset_values()
        self.rotate_tab.reset_values()
        self.move_tab.reset_values()

class MoveTab(QtWidgets.QWidget):
    """
    Tab for input values to move a object
    """

    def __init__(self):
        super().__init__()
        self.points_list = []

        self.numeric_validator = QtGui.QIntValidator(-10000, 10000)

        # Label to indicate current operation
        self.option_label = QtWidgets.QLabel(self)
        self.option_label.setGeometry(QtCore.QRect(160, 20, 180, 20))

        self.absolut_point_radio_btn = QtWidgets.QRadioButton(
            'To absolut point', self)
        self.absolut_point_radio_btn.setGeometry(
            QtCore.QRect(10, 10, 180, 70))
        self.absolut_point_radio_btn.toggled.connect(
            lambda: self.option_label.setText('Point'))
        self.absolut_point_radio_btn.toggle()

        self.movement_vector_radio_btn = QtWidgets.QRadioButton(
            'Movement vector', self)
        self.movement_vector_radio_btn.setGeometry(
            QtCore.QRect(10, 50, 180, 70))
        self.movement_vector_radio_btn.toggled.connect(
            lambda: self.option_label.setText('Vector'))

        self.point_input_panel = QtWidgets.QWidget(self)
        self.point_input_panel.setGeometry(QtCore.QRect(160, 50, 180, 70))

        self.x_lbl = QtWidgets.QLabel('X', self.point_input_panel)
        self.x_lbl.setGeometry(QtCore.QRect(25, 0, 20, 20))

        self.x_input = QtWidgets.QLineEdit(self.point_input_panel)
        self.x_input.setGeometry(QtCore.QRect(10, 20, 40, 20))
        self.x_input.setValidator(self.numeric_validator)

        self.y_lbl = QtWidgets.QLabel('Y', self.point_input_panel)
        self.y_lbl.setGeometry(QtCore.QRect(75, 0, 20, 20))

        self.y_input = QtWidgets.QLineEdit(self.point_input_panel)
        self.y_input.setGeometry(QtCore.QRect(60, 20, 40, 20))
        self.y_input.setValidator(self.numeric_validator)

        # For 3D upgrade
        self.z_lbl = QtWidgets.QLabel('Z', self.point_input_panel)
        self.z_lbl.setGeometry(QtCore.QRect(125, 0, 20, 20))

        self.z_input = QtWidgets.QLineEdit(self.point_input_panel)
        self.z_input.setGeometry(QtCore.QRect(110, 20, 40, 20))
        self.z_input.setValidator(self.numeric_validator)

    def reset_values(self):
        '''Reset dialog values'''
        self.x_input.clear()
        self.y_input.clear()
        self.z_input.clear()

class RotateTab(QtWidgets.QWidget):
    """
    Tab for input values to rotate a object
    """

    def __init__(self):
        super().__init__()
        self.points_list = []

        self.numeric_validator = QtGui.QIntValidator(-10000, 10000)
        self.degree_validator = QtGui.QIntValidator(-360, 360)

        self.ref_lbl = QtWidgets.QLabel('Rotation reference:', self)
        self.ref_lbl.setGeometry(QtCore.QRect(10, 10, 180, 20))

        self.over_obj_center_radio_btn = QtWidgets.QRadioButton(
            'Over object center', self)
        self.over_obj_center_radio_btn.setGeometry(
            QtCore.QRect(10, 40, 180, 20))
        # Set default
        self.over_obj_center_radio_btn.toggle()

        self.over_world_center_radio_btn = QtWidgets.QRadioButton(
            'Over world center', self)
        self.over_world_center_radio_btn.setGeometry(
            QtCore.QRect(10, 60, 180, 20))

        self.over_point_radio_btn = QtWidgets.QRadioButton(
            'Over point', self)
        self.over_point_radio_btn.setGeometry(
            QtCore.QRect(10, 80, 180, 20))

        # Add point input
        self.point_to_rotate_panel = QtWidgets.QWidget(self)
        self.point_to_rotate_panel.setGeometry(
            QtCore.QRect(10, 100, 180, 70))

        # Hide by default
        self.point_to_rotate_panel.setVisible(False)

        self.x_lbl = QtWidgets.QLabel('X', self.point_to_rotate_panel)
        self.x_lbl.setGeometry(QtCore.QRect(25, 0, 20, 20))

        self.x_input = QtWidgets.QLineEdit(self.point_to_rotate_panel)
        self.x_input.setGeometry(QtCore.QRect(10, 20, 40, 20))
        self.x_input.setValidator(self.numeric_validator)

        self.y_lbl = QtWidgets.QLabel('Y', self.point_to_rotate_panel)
        self.y_lbl.setGeometry(QtCore.QRect(75, 0, 20, 20))

        self.y_input = QtWidgets.QLineEdit(self.point_to_rotate_panel)
        self.y_input.setGeometry(QtCore.QRect(60, 20, 40, 20))
        self.y_input.setValidator(self.numeric_validator)

        # For 3D upgrade
        self.z_lbl = QtWidgets.QLabel('Z', self.point_to_rotate_panel)
        self.z_lbl.setGeometry(QtCore.QRect(125, 0, 20, 20))

        self.z_input = QtWidgets.QLineEdit(self.point_to_rotate_panel)
        self.z_input.setGeometry(QtCore.QRect(110, 20, 40, 20))
        self.z_input.setValidator(self.numeric_validator)

        # Link this panel to rotation around point radio buton
        self.over_point_radio_btn.toggled.connect(
            lambda: self.point_to_rotate_panel.setVisible(
                not self.point_to_rotate_panel.isVisible()
            )
        )

        # Degrees input
        self.degrees_label = QtWidgets.QLabel('Degrees', self)
        self.degrees_label.setGeometry(
            QtCore.QRect(160, 0, 100, 20))

        self.degree_unit_label = QtWidgets.QLabel('º', self)
        self.degree_unit_label.setGeometry(
            QtCore.QRect(200, 20, 100, 20))

        self.degrees_input = QtWidgets.QLineEdit(self)
        self.degrees_input.setGeometry(
            QtCore.QRect(160, 20, 40, 20))
        self.degrees_input.setValidator(self.degree_validator)

        self.axis_panel = QtWidgets.QWidget(self)
        self.axis_panel.setGeometry(
            QtCore.QRect(200, 10, 180, 100))

        self.axis_label = QtWidgets.QLabel('Ref. axis', self.axis_panel)
        self.axis_label.setGeometry(QtCore.QRect(30, 0, 100, 20))

        self.x_axis = QtWidgets.QRadioButton(
            'X', self.axis_panel)
        self.x_axis.setGeometry(
            QtCore.QRect(35, 25, 50, 20))

        self.y_axis = QtWidgets.QRadioButton(
            'Y', self.axis_panel)
        self.y_axis.setGeometry(
            QtCore.QRect(80, 25, 50, 20))

        self.z_axis = QtWidgets.QRadioButton(
            'Z', self.axis_panel)
        self.z_axis.setGeometry(
            QtCore.QRect(115, 25, 50, 20))
        self.z_axis.setChecked(True)  # default

        self.arbitrary_axis_radio = QtWidgets.QRadioButton(
            'Arbitrary', self.axis_panel)
        self.arbitrary_axis_radio.setGeometry(
            QtCore.QRect(35, 50, 100, 20))

        self.arbitrary_axis_pane = QtWidgets.QWidget(self)
        self.arbitrary_axis_pane.setGeometry(
            QtCore.QRect(190, 85, 170, 100))
        self.arbitrary_axis_pane.setVisible(False)
        self.arbitrary_axis_radio.toggled.connect(
            lambda: self.arbitrary_axis_pane.setVisible(
                not self.arbitrary_axis_pane.isVisible()
            )
        )

        x_arbitrary_label = QtWidgets.QLabel('X', self.arbitrary_axis_pane)
        x_arbitrary_label.setGeometry(QtCore.QRect(30, 0, 16, 19))
        y_arbitrary_label = QtWidgets.QLabel('Y', self.arbitrary_axis_pane)
        y_arbitrary_label.setGeometry(QtCore.QRect(80, 0, 16, 19))
        z_arbitrary_label = QtWidgets.QLabel('Z', self.arbitrary_axis_pane)
        z_arbitrary_label.setGeometry(QtCore.QRect(130, 0, 16, 19))

        p_arbitrary_label = QtWidgets.QLabel('P', self.arbitrary_axis_pane)
        p_arbitrary_label.setGeometry(QtCore.QRect(0, 20, 16, 19))

        a_arbitrary_label = QtWidgets.QLabel('A', self.arbitrary_axis_pane)
        a_arbitrary_label.setGeometry(QtCore.QRect(0, 50, 16, 19))

        self.p_x_input = QtWidgets.QLineEdit(self.arbitrary_axis_pane)
        self.p_x_input.setGeometry(QtCore.QRect(20, 20, 41, 27))
        self.p_x_input.setValidator(self.numeric_validator)
        self.p_y_input = QtWidgets.QLineEdit(self.arbitrary_axis_pane)
        self.p_y_input.setGeometry(QtCore.QRect(70, 20, 41, 27))
        self.p_y_input.setValidator(self.numeric_validator)
        self.p_z_input = QtWidgets.QLineEdit(self.arbitrary_axis_pane)
        self.p_z_input.setGeometry(QtCore.QRect(120, 20, 41, 27))
        self.p_z_input.setValidator(self.numeric_validator)
        self.a_x_input = QtWidgets.QLineEdit(self.arbitrary_axis_pane)
        self.a_x_input.setGeometry(QtCore.QRect(20, 50, 41, 27))
        self.a_x_input.setValidator(self.numeric_validator)
        self.a_y_input = QtWidgets.QLineEdit(self.arbitrary_axis_pane)
        self.a_y_input.setGeometry(QtCore.QRect(70, 50, 41, 27))
        self.a_y_input.setValidator(self.numeric_validator)
        self.a_z_input = QtWidgets.QLineEdit(self.arbitrary_axis_pane)
        self.a_z_input.setGeometry(QtCore.QRect(120, 50, 41, 27))
        self.a_z_input.setValidator(self.numeric_validator)

    def get_axis(self):
        '''Return label indicating what axis is selected'''
        if self.x_axis.isChecked():
            return 'x'
        if self.y_axis.isChecked():
            return 'y'
        if self.z_axis.isChecked():
            return 'z'

        else:
            return 'arbitrary'

    def reset_values(self):
        '''Reset dialog values'''
        self.x_input.clear()
        self.y_input.clear()
        self.z_input.clear()
        self.degrees_input.clear()
        self.p_x_input.clear()
        self.p_y_input.clear()
        self.p_z_input.clear()
        self.a_x_input.clear()
        self.a_y_input.clear()
        self.a_z_input.clear()

class RescaleTab(QtWidgets.QWidget):
    """
    Tab for input values to rescale a object
    """

    def __init__(self):
        super().__init__()
        self.points_list = []

        self.double_validator = QtGui.QDoubleValidator(0, 1, 3, self)

        # Degrees input
        self.factor_label = QtWidgets.QLabel('Factor:', self)
        self.factor_label.setGeometry(
            QtCore.QRect(160, 60, 100, 20))

        self.factor_input = QtWidgets.QLineEdit(self)
        self.factor_input.setGeometry(
            QtCore.QRect(160, 80, 40, 20))
        self.factor_input.setValidator(self.double_validator)

    def reset_values(self):
        '''Reset dialog values'''
        self.factor_input.clear()
