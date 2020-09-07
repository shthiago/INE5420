from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from src.view.viewport import ViewPort


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUi()

    def initUi(self):
        self.setObjectName('MainWindow')
        self.resize(850, 650)

        # Tools setup
        self.tools_menu_box = QtWidgets.QGroupBox(self)
        self.tools_menu_box.setGeometry(QtCore.QRect(10, 20, 171, 561))
        self.tools_menu_box.setTitle("Tools Menu")

        self.objects_lbl = QtWidgets.QLabel(self.tools_menu_box)
        self.objects_lbl.setGeometry(QtCore.QRect(10, 30, 57, 15))
        self.objects_lbl.setText("Objects")

        self.objects_list_view = QtWidgets.QListView(self.tools_menu_box)
        self.objects_list_view.setGeometry(QtCore.QRect(10, 50, 151, 121))

        self.items_model = QtGui.QStandardItemModel()
        self.objects_list_view.setModel(self.items_model)

        self.objects_list_view.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.objects_list_view.customContextMenuRequested.connect(
            self.custom_context_menu)

        self.objects_list_view_context_menu = QtWidgets.QMenu(
            self.objects_list_view)
        self.color_change_action = QtWidgets.QAction()
        self.color_change_action.setText('Change color')
        self.objects_list_view_context_menu.addAction(self.color_change_action)

        self.open_transformation_dialog_action = QtWidgets.QAction()
        self.open_transformation_dialog_action.setText('Transform...')
        self.objects_list_view_context_menu.addAction(
            self.open_transformation_dialog_action)

        self.objects_list_view.addAction(self.color_change_action)
        self.objects_list_view.addAction(
            self.open_transformation_dialog_action)

        self.window_lbl = QtWidgets.QLabel(self.tools_menu_box)
        self.window_lbl.setGeometry(QtCore.QRect(10, 180, 71, 16))
        self.window_lbl.setText("Window")

        self.step_lbl = QtWidgets.QLabel(self.tools_menu_box)
        self.step_lbl.setGeometry(QtCore.QRect(10, 200, 31, 16))
        self.step_lbl.setText("Step:")

        self.step_input = QtWidgets.QLineEdit(self.tools_menu_box)
        self.step_input.setText('10')
        self.step_input.setGeometry(QtCore.QRect(50, 200, 41, 23))
        self.step_input.setValidator(QtGui.QIntValidator(0, 99))

        self.step_pct_lbl = QtWidgets.QLabel(self.tools_menu_box)
        self.step_pct_lbl.setGeometry(QtCore.QRect(100, 200, 21, 16))
        self.step_pct_lbl.setText("%")

        self.view_up_btn = QtWidgets.QPushButton(self.tools_menu_box)
        self.view_up_btn.setGeometry(QtCore.QRect(30, 227, 41, 23))
        self.view_up_btn.setText("Up")

        self.view_left_btn = QtWidgets.QPushButton(self.tools_menu_box)
        self.view_left_btn.setGeometry(QtCore.QRect(10, 250, 41, 23))
        self.view_left_btn.setText("Left")

        self.view_right_btn = QtWidgets.QPushButton(self.tools_menu_box)
        self.view_right_btn.setGeometry(QtCore.QRect(52, 250, 41, 23))
        self.view_right_btn.setText("Right")

        self.view_down_btn = QtWidgets.QPushButton(self.tools_menu_box)
        self.view_down_btn.setGeometry(QtCore.QRect(30, 273, 41, 23))
        self.view_down_btn.setText("Down")

        self.in_btn = QtWidgets.QPushButton(self.tools_menu_box)
        self.in_btn.setGeometry(QtCore.QRect(100, 230, 31, 23))
        self.in_btn.setText("In")

        self.out_btn = QtWidgets.QPushButton(self.tools_menu_box)
        self.out_btn.setGeometry(QtCore.QRect(100, 270, 31, 23))
        self.out_btn.setText("Out")

        self.rotate_lbl = QtWidgets.QLabel(self.tools_menu_box)
        self.rotate_lbl.setGeometry(QtCore.QRect(10, 310, 57, 15))
        self.rotate_lbl.setText("Rotate")

        self.degrees_lbl = QtWidgets.QLabel(self.tools_menu_box)
        self.degrees_lbl.setGeometry(QtCore.QRect(10, 330, 62, 15))
        self.degrees_lbl.setText("Dregrees")

        self.rotation_degrees_input = QtWidgets.QLineEdit(self.tools_menu_box)
        self.rotation_degrees_input.setText('0')
        self.rotation_degrees_input.setGeometry(QtCore.QRect(75, 330, 41, 23))
        self.rotation_degrees_input.setValidator(QtGui.QIntValidator(0, 360))

        self.degrees_unit_lbl = QtWidgets.QLabel(self.tools_menu_box)
        self.degrees_unit_lbl.setGeometry(QtCore.QRect(125, 330, 16, 16))
        self.degrees_unit_lbl.setText("º")

        self.rotate_left = QtWidgets.QPushButton(self.tools_menu_box)
        self.rotate_left.setGeometry(QtCore.QRect(20, 360, 41, 23))
        self.rotate_left.setText("<")

        self.rotate_right = QtWidgets.QPushButton(self.tools_menu_box)
        self.rotate_right.setGeometry(QtCore.QRect(80, 360, 41, 23))
        self.rotate_right.setText(">")

        # self.rotate_x_btn = QtWidgets.QPushButton(self.tools_menu_box)
        # self.rotate_x_btn.setGeometry(QtCore.QRect(20, 370, 31, 23))
        # self.rotate_x_btn.setText("X")

        # self.rotate_y_btn = QtWidgets.QPushButton(self.tools_menu_box)
        # self.rotate_y_btn.setGeometry(QtCore.QRect(60, 370, 31, 23))
        # self.rotate_y_btn.setText("Y")

        # self.rotate_z_btn = QtWidgets.QPushButton(self.tools_menu_box)
        # self.rotate_z_btn.setGeometry(QtCore.QRect(100, 370, 31, 23))
        # self.rotate_z_btn.setText("Z")

        # self.zoom_lbl = QtWidgets.QLabel(self.tools_menu_box)
        # self.zoom_lbl.setGeometry(QtCore.QRect(30, 400, 57, 15))
        # self.zoom_lbl.setText("Zoom")

        # self.zoom_in_btn = QtWidgets.QPushButton(self.tools_menu_box)
        # self.zoom_in_btn.setGeometry(QtCore.QRect(70, 420, 31, 23))
        # self.zoom_in_btn.setText("+")

        # self.zoom_out_btn = QtWidgets.QPushButton(self.tools_menu_box)
        # self.zoom_out_btn.setGeometry(QtCore.QRect(20, 420, 31, 23))
        # self.zoom_out_btn.setText("-")

        # self.set_window_btn = QtWidgets.QPushButton(self.tools_menu_box)
        # self.set_window_btn.setGeometry(QtCore.QRect(20, 450, 80, 23))
        # self.set_window_btn.setText("Set Window")

        # self.projection_lbl = QtWidgets.QLabel(self.tools_menu_box)
        # self.projection_lbl.setGeometry(QtCore.QRect(10, 490, 81, 16))
        # self.projection_lbl.setText("Projection")

        # self.paralel_radio_btn = QtWidgets.QRadioButton(self.tools_menu_box)
        # self.paralel_radio_btn.setGeometry(QtCore.QRect(10, 510, 99, 21))
        # self.paralel_radio_btn.setText("Paralel")
        # # Default is paralel
        # self.paralel_radio_btn.toggle()
        # self.perspective_radio_btn = QtWidgets.QRadioButton(
        #     self.tools_menu_box)
        # self.perspective_radio_btn.setGeometry(QtCore.QRect(10, 530, 99, 21))
        # self.perspective_radio_btn.setText("Perspective")

        # Canvas setup
        self.viewport = ViewPort(self)
        self.viewport.setGeometry(QtCore.QRect(200, 30, 600, 600))

        # Setting up menu bar
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))

        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setTitle("File")
        self.setMenuBar(self.menubar)
        self.menubar.addAction(self.menu_file.menuAction())

        self.action_add_object = QtWidgets.QAction(self)
        self.action_add_object.setText("Add object")
        self.menu_file.addAction(self.action_add_object)

        self.action_export_all_objects = QtWidgets.QAction(self)
        self.action_export_all_objects.setText("Export all")
        self.menu_file.addAction(self.action_export_all_objects)

    def custom_context_menu(self, point):
        """
        Context menu for objects view list
        """
        # Check if any item is selected before open the menu
        si = self.objects_list_view.selectedIndexes()
        if len(si) < 1:
            return

        self.objects_list_view_context_menu.exec_(
            self.objects_list_view.mapToGlobal(point))
