"""
File for modeling objects to be stored
"""
from typing import List, NamedTuple, Tuple

import numpy as np
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
                f'p {point_index}']

    def as_tuple(self):
        '''Return point as (x, y, x)'''
        return (self.x, self.y, self.z)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


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
                f'l {index_p1} {index_p2}', ]


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

    def lines(self):
        '''Iterator for getting lines of wireframe'''
        i = 0
        size = len(self.points)

        for i in range(size-1):
            yield Line(name='__',
                       p1=self.points[i],
                       p2=self.points[i+1])

        yield Line(name='__', p1=self.points[-1], p2=self.points[0])


class BezierCurveSetup(NamedTuple):
    '''Setup to create a Bezier blending function'''
    P1: Point3D
    P2: Point3D
    P3: Point3D
    P4: Point3D


class BezierCurve(BaseNamedColoredObject):
    '''Class to hold points used to calculate a curve'''

    def __init__(self, name: str, curve_setups: List[BezierCurveSetup],
                 thickness: int = 3):
        super().__init__(name, QColor(0, 0, 0))
        self.curves = curve_setups
        self.thickness = thickness

    def points(self, step: float):
        '''Calculate curve points

        Parameters
        ----------
        step: float
            step for t calculation, must be in 0 < step < 1
        '''
        points_to_return = []
        for curve_setup in self.curves:
            points_to_return.extend(
                self._calculate_points(curve_setup, step))

        return points_to_return

    def _calculate_points(self, setup: BezierCurveSetup, step: float
                          ) -> List[Point3D]:
        '''Calcualte points for setup and step'''
        MB = np.array([[-1,  3, -3,  1],
                       [3, -6,  3,  0],
                       [-3,  3,  0,  0],
                       [1,  0,  0,  0]])
        GB = np.array([[setup.P1.x, setup.P1.y],
                       [setup.P2.x, setup.P2.y],
                       [setup.P3.x, setup.P3.y],
                       [setup.P4.x, setup.P4.y]])

        points: List[Point3D] = []
        for t in list(np.arange(0, 1, step)) + [1]:
            T = self._t_vec(t)
            x, y = T.dot(MB).dot(GB)
            point = Point3D('__p', x=x, y=y, z=0,
                            thickness=self.thickness)
            point.color = self.color
            points.append(point)

        return points

    def as_list_of_tuples(self):
        '''Return points from curve as list of tuples'''
        tuples = []
        for setup in self.curves:
            tuples.extend([
                (setup.P1.x, setup.P1.y, setup.P1.z),
                (setup.P2.x, setup.P2.y, setup.P2.z),
                (setup.P3.x, setup.P3.y, setup.P3.z),
                (setup.P4.x, setup.P4.y, setup.P4.z),
            ])

    def _t_vec(self, t_value: float) -> np.ndarray:
        '''Calcualte the T vector for points

        Parameters
        ----------
        t: float
            0 <= t <= 1
        '''
        values = [1, t_value]
        for i in range(1, 3):
            values.append(values[i] * t_value)

        values.reverse()
        return np.array(values)


class ViewportObjectRepresentation(NamedTuple):
    '''Class to hold data of a object ready to be draw at viewport'''
    name: str
    points: List[Point3D]
    color: QColor
    thickness: int
