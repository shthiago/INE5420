from PyQt5 import QtCore, QtGui, QtWidgets


class NewObjectDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.numeric_validator = QtGui.QIntValidator(0, 1000)

        self.initUi()

    def initUi(self):
        self.resize(400, 300)
        self.setWindowTitle("Create object")
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(130, 260, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)

        self.name_lbl = QtWidgets.QLabel(self)
        self.name_lbl.setGeometry(QtCore.QRect(10, 10, 41, 16))

        self.name_input = QtWidgets.QLineEdit(self)
        self.name_input.setGeometry(QtCore.QRect(60, 10, 311, 23))
        self.name_lbl.setText("Name:")

        self.tab_panel = QtWidgets.QTabWidget(self)
        self.tab_panel.setEnabled(True)
        self.tab_panel.setGeometry(QtCore.QRect(10, 50, 371, 201))

        # Add a point mechanism
        self.point_tab = PointTab()
        self.tab_panel.addTab(self.point_tab, "Point")

        # Add a line mechanism
        self.line_tab = LineTab()
        self.tab_panel.addTab(self.line_tab, "Line")

        self.tab_panel.setCurrentIndex(0)

    def reset_values(self):
        """
        Reset texts on input
        """
        # Reset name
        self.name_input.setText('')

        # Reset inputs for line
        self.line_tab.reset_values()

        self.point_tab.reset_values()

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

        self.numeric_validator = QtGui.QIntValidator(0, 1000)

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

        self.numeric_validator = QtGui.QIntValidator(0, 1000)

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
