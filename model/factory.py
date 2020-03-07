from PyQt5.QtWidgets import QWidget

from .objects import Point3D, Line


def new_object_factory(obj_name: str, tab_name: str, tab: QWidget):
    """
    Function to centralize object creation, mapped on dict
    """
    return specific_factory[tab_name](obj_name, tab)


def create_line(name: str, tab: QWidget):
    """
    Create Line object
    """
    # TODO
    # CONTINUE FROM HERE
    # extract values from panel
    p1 = Point3D('_p1', 0, 0, 0)
    p2 = Point3D('_p2', 1, 1, 1)
    return Line('L1', p1, p2)


def create_point3D(name: str, tab: QWidget):
    """
    Create Point3D object
    """
    # TODO
    return Point3D('P1', 0, 0, 0)


specific_factory = {
    'Point': create_point3D,
    'Line': create_line,
}
