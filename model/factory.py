from PyQt5.QtWidgets import QWidget

from .objects import Point3D, Line
from view.dialog import LineTab, PointTab


def create_line(name: str, tab: LineTab):
    """
    Create Line object
    """
    x1 = int(tab.start_x_coord_line_input.text())
    y1 = int(tab.start_y_coord_line_input.text())
    z1 = int(tab.start_z_coord_line_input.text())

    x2 = int(tab.end_x_coord_line_input.text())
    y2 = int(tab.end_y_coord_line_input.text())
    z2 = int(tab.end_z_coord_line_input.text())

    p1 = Point3D('_p1', x1, y1, z1)
    p2 = Point3D('_p2', x2, y2, z2)

    return Line(name, p1, p2)


def create_point3D(name: str, tab: PointTab):
    """
    Create Point3D object
    """
    x = int(tab.x_coord_pt_input.text())
    y = int(tab.y_coord_pt_input.text())
    z = int(tab.z_coord_pt_input.text())
    return Point3D(name, x, y, z)


specific_factory = {
    'Point': create_point3D,
    'Line': create_line,
}


def new_object_factory(obj_name: str, tab_name: str, tab: QWidget):
    """
    Function to centralize object creation, mapped on dict
    """

    try:
        status = {
            'done': True,
            'error_msg': ''
        }

        obj = specific_factory[tab_name](obj_name, tab)
        return status, obj

    except ValueError as e:
        status = {
            'done': False,
            'error_msg': str(e)
        }

        return status, None
