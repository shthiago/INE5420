"""
File for modeling objects to be stored
"""
from typing import List, NamedTuple

from PyQt5.QtGui import QColor


class BaseNamedColoredObject:
    '''Base class for objects'''

    def __init__(self, name: str, color: QColor):
        self._color: QColor = color
        self._name: str = name

    @property
    def color(self) -> QColor:
        '''Getter for object color'''
        return self._color

    @color.setter
    def color(self, color: QColor):
        '''Setter for object color'''
        self._color = color

    @property
    def name(self) -> str:
        '''Getter for object name'''
        return self._name

    @name.setter
    def name(self, name: str):
        '''Setter for object name'''
        self._name = name


class Point3D(BaseNamedColoredObject):
    """
    Class for holding the three values with gettings/setters
    """

    def __init__(self, name: str, x: int, y: int, z: int):
        super().__init__(name, QColor(0, 0, 0))
        self._x: int = x
        self._y: int = y
        self._z: int = z

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int):
        self._x = x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int):
        self._y = y

    @property
    def z(self) -> int:
        return self._z

    @z.setter
    def z(self, z: int):
        self._z = z


class Line(BaseNamedColoredObject):
    """
    Class for holding the two points of a line
    """

    def __init__(self, name: str, p1: Point3D, p2: Point3D):
        super().__init__(name, QColor(0, 0, 0))
        self._p1: Point3D = p1
        self._p2: Point3D = p2

    @property
    def p1(self) -> Point3D:
        return self._p1

    @p1.setter
    def p1(self, p1: Point3D):
        self._p1 = p1

    @property
    def p2(self) -> Point3D:
        return self._p2

    @p2.setter
    def p2(self, p2: Point3D):
        self._p2 = p2

    @property
    def points(self) -> List[Point3D]:
        return [self._p1, self._p2]


class Wireframe(BaseNamedColoredObject):
    """
    Class to hold polygons
    """

    def __init__(self, name: str, points: List[Point3D]):
        super().__init__(name, QColor(0, 0, 0))
        self._points = points

    @property
    def points(self) -> List[Point3D]:
        return self._points

    @points.setter
    def points(self, points: List[Point3D]):
        self._points = points


class ViewportObjectRepresentation(NamedTuple):
    '''Class to hold data of a object ready to be draw at viewport'''
    name: str
    points: List[Point3D]
    color: QColor
