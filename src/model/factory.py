from typing import List

from PyQt5.QtWidgets import QWidget

from src.model.objects import (Point3D, Line, Wireframe,
                               BezierCurve, BezierCurveSetup)
from src.view.dialog import LineTab, PointTab, CurveTab, WireframeTab


def create_line(name: str, tab: LineTab) -> Line:
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


def create_point3D(name: str, tab: PointTab) -> Point3D:
    """
    Create Point3D object
    """
    x = int(tab.x_coord_pt_input.text())
    y = int(tab.y_coord_pt_input.text())
    z = int(tab.z_coord_pt_input.text())
    return Point3D(name, x, y, z)


def create_wireframe(name: str, tab: WireframeTab) -> Wireframe:
    """
    Create Wireframe object
    """
    points = []
    for i, point in enumerate(tab.points_list):
        x, y, z = point
        point = Point3D('Po' + str(i).zfill(3), x, y, z)
        points.append(point)

    return Wireframe(name, points)


def create_curve(name: str, tab: CurveTab) -> BezierCurve:
    """Create a bezier curve, compsoed by multipe P1 to P4 points"""
    points_groups = tab.curves_list

    setups: List[BezierCurveSetup] = []
    for group in points_groups:
        p1 = group['P1']
        p2 = group['P2']
        p3 = group['P3']
        p4 = group['P4']
        setup = BezierCurveSetup(
            P1=Point3D('__', x=p1['x'], y=p1['y'], z=p1['z']),
            P2=Point3D('__', x=p2['x'], y=p2['y'], z=p2['z']),
            P3=Point3D('__', x=p3['x'], y=p3['y'], z=p3['z']),
            P4=Point3D('__', x=p4['x'], y=p4['y'], z=p4['z']),
        )

        setups.append(setup)

    return BezierCurve(name=name, curve_setups=setups)


def new_object_factory(obj_name: str, tab_name: str, tab: QWidget):
    """
    Function to centralize object creation, mapped on dict
    """

    try:
        status = {
            'done': True,
            'error_msg': ''
        }

        if tab_name == 'Point':
            return status, create_point3D(obj_name, tab)
        elif tab_name == 'Line':
            return status, create_line(obj_name, tab)
        elif tab_name == 'Wireframe':
            return status, create_wireframe(obj_name, tab)
        elif tab_name == 'Curve':
            return status, create_curve(obj_name, tab)

        raise ValueError(f'Invalid tab name: {tab_name}')

    except ValueError as e:
        status = {
            'done': False,
            'error_msg': str(e)
        }

        return status, None
