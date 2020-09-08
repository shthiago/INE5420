"""
File for modeling objects to be stored
"""
from typing import List, NamedTuple, Tuple, Set

from PyQt5.QtGui import QColor


class BaseNamedColoredObject:
    '''Base class for objects'''

    def __init__(self, name: str, color: QColor):
        self.color: QColor = color
        self.name: str = name

    def as_list_of_tuples(self) -> List[Tuple[float, float, float]]:
        '''Return points as [(x, y, z)]'''
        raise NotImplementedError()

    def describe_export_with(self, points: List[Tuple[float, float, float]],
                             colors: List[QColor]) -> List[str]:
        '''Return lines that describe object in .obj file, using indexes
        from points and names from colors'''
        raise NotImplementedError()


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
        return f'({self.x} {self.y} {self.z})'

    def as_list_of_tuples(self) -> List[Tuple[float, float, float]]:
        '''Return points as [(x, y, z)]'''
        return [(self.x, self.y, self.z)]

    def describe_export_with(self, points: List[Tuple[float, float, float]],
                             colors: List[QColor]) -> List[str]:
        '''Return lines that describe object in .obj file, using indexes
        from points and names from colors'''
        point_index = points.index((self.x, self.y, self.z)) + 1
        return ['# Point3D',
                f'o {self.name}',
                f'usemtl {self.color.name()[1:]}',
                f'f {point_index}']

    def as_tuple(self):
        '''Return point as (x, y, x)'''
        return (self.x, self.y, self.z)


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

    def as_list_of_tuples(self) -> List[Tuple[float, float, float]]:
        '''Return points as [(x, y, z)]'''
        return [p.as_tuple() for p in self.points]

    def describe_export_with(self, points: List[Tuple[float, float, float]],
                             colors: List[QColor]) -> List[str]:
        '''Return lines that describe object in .obj file, using indexes
        from points and names from colors'''
        index_p1 = points.index(self.p1.as_tuple()) + 1
        index_p2 = points.index(self.p2.as_tuple()) + 1
        return ['# Line',
                f'o {self.name}',
                f'usemtl {self.color.name()[1:]}',
                f'f {index_p1} {index_p2}', ]


class Wireframe(BaseNamedColoredObject):
    """
    Class to hold polygons
    """

    def __init__(self, name: str, points: List[Point3D], thickness: int = 3):
        super().__init__(name, QColor(0, 0, 0))
        self.points = points
        self.thickness = thickness

    def as_list_of_tuples(self) -> List[Tuple[float, float, float]]:
        '''Return points as [(x, y, z)]'''
        return [p.as_tuple() for p in self.points]

    def describe_export_with(self, points: List[Tuple[float, float, float]],
                             colors: List[QColor]) -> List[str]:
        '''Return lines that describe object in .obj file, using indexes
        from points and names from colors'''
        indexes = [str(points.index(p) + 1) for p in self.as_list_of_tuples()]
        return ['# Wireframe',
                f'o {self.name}',
                f'usemtl {self.color.name()[1:]}',
                f'f {" ".join(indexes)}']


class ViewportObjectRepresentation(NamedTuple):
    '''Class to hold data of a object ready to be draw at viewport'''
    name: str
    points: List[Point3D]
    color: QColor
    thickness: int
