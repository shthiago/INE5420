"""
File for modeling objects to be stored
"""
from typing import List, NamedTuple

from PyQt5.QtGui import QColor


class BaseNamedColoredObject:
    '''Base class for objects'''

    def __init__(self, name: str, color: QColor):
        self.color: QColor = color
        self.name: str = name


class Point3D(BaseNamedColoredObject):
    """
    Class for holding the three values with gettings/setters
    """

    def __init__(self, name: str, x: float, y: float, z: float, thickness: int = 3):
        super().__init__(name, QColor(0, 0, 0))
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.thickness = thickness

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'


class Line(BaseNamedColoredObject):
    """
    Class for holding the two points of a line
    """

    def __init__(self, name: str, p1: Point3D, p2: Point3D, thickness: int = 3):
        super().__init__(name, QColor(0, 0, 0))
        self.p1: Point3D = p1
        self.p2: Point3D = p2
        self.thickness = thickness

    @property
    def points(self) -> List[Point3D]:
        '''Getter to get points from Line'''
        return [self.p1, self.p2]


class Wireframe(BaseNamedColoredObject):
    """
    Class to hold polygons
    """

    def __init__(self, name: str, points: List[Point3D], thickness: int = 3):
        super().__init__(name, QColor(0, 0, 0))
        self.points = points
        self.thickness = thickness


class ViewportObjectRepresentation(NamedTuple):
    '''Class to hold data of a object ready to be draw at viewport'''
    name: str
    points: List[Point3D]
    color: QColor
    thickness: int
