"""
File for modeling objects to be stored
"""
from typing import List, NamedTuple, Tuple
from math import isclose

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
        return f'"{self.name}"->({self.x} {self.y} {self.z})'

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
        if not isinstance(other, Point3D):
            return False

        return all([isclose(other.x, self.x, abs_tol=1e-4),
                    isclose(other.y, self.y, abs_tol=1e-4)])

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

    def __repr__(self):
        return self.p1.__repr__() + ' -> ' + self.p2.__repr__()


class Wireframe(BaseNamedColoredObject):
    """
    Class to hold polygons
    """

    def __init__(self, name: str, points: List[Point3D], thickness: int = 3):
        super().__init__(name, QColor(0, 0, 0))
        self.points = self.points_clockwise(points)
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

    def points_clockwise(self, points: List[Point3D]) -> List[Point3D]:
        '''Return the points in a clockwise sequence'''
        edges_calc = 0
        for i, p2 in enumerate(points, 1):
            p1 = points[i-1]

            edges_calc += (p2.x - p1.x) * (p2.y + p1.y)

        p2 = points[0]
        p1 = points[-1]
        edges_calc += (p2.x - p1.x) * (p2.y + p1.y)

        if edges_calc > 0:
            return points

        else:
            return list(reversed(points))


class BezierCurveSetup(NamedTuple):
    '''Setup to create a Bezier blending function'''
    P1: Point3D
    P2: Point3D
    P3: Point3D
    P4: Point3D


class BezierCurve(BaseNamedColoredObject):
    '''Class to hold points used to calculate a Bezier curve'''

    def __init__(self, name: str, curve_setups: List[BezierCurveSetup],
                 thickness: int = 3):
        super().__init__(name, QColor(0, 0, 0))
        self.curves = curve_setups
        self.thickness = thickness

    def calculate_lines(self, alpha: float):
        '''Create a line with function at every alpha step'''
        lines_to_return = []
        for curve_setup in self.curves:
            lines_to_return.extend(
                self._calculate_for_setup(curve_setup, alpha))

        return lines_to_return

    def _calculate_for_setup(self, setup: BezierCurveSetup, step: float) -> List[Line]:
        '''Calculate lines for this part os line segment'''
        MB = np.array([[-1,  3, -3,  1],
                       [3, -6,  3,  0],
                       [-3,  3,  0,  0],
                       [1,  0,  0,  0]])
        GB = np.array([[setup.P1.x, setup.P1.y],
                       [setup.P2.x, setup.P2.y],
                       [setup.P3.x, setup.P3.y],
                       [setup.P4.x, setup.P4.y]])

        lines: List[Line] = []
        t_values = list(np.arange(0, 1, step)) + [1]
        p_start = t_values[0]
        T0 = self._t_vec(p_start)
        for i, p_end in enumerate(t_values, 1):
            T1 = self._t_vec(p_end)

            start_x, start_y = T0.dot(MB).dot(GB)
            end_x, end_y = T1.dot(MB).dot(GB)

            line = Line(
                name='__l',
                p1=Point3D('__p', x=start_x, y=start_y, z=0),
                p2=Point3D('__p', x=end_x, y=end_y, z=0),
                thickness=self.thickness
            )
            line.color = self.color

            lines.append(line)

            T0 = T1
            p_start = p_end

        return lines

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

        return tuples

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

    def describe_export_with(self, points: List[Tuple[float, float, float]],
                             colors: List[QColor]) -> List[str]:
        '''Return lines that describe object in .obj file, using indexes
        from points and names from colors'''
        indexes = [str(points.index(p) + 1) for p in self.as_list_of_tuples()]
        return ['# Bezier',
                f'o {self.name}',
                f'usemtl {self.color.name()[1:]}',
                f'cstype bezier',
                f'curv2 {" ".join(indexes)}']


class BSplineCurve(BaseNamedColoredObject):
    '''BSpline object descriptor'''

    def __init__(self, name: str, control_points: List[Point3D], thickness: int = 3):
        if len(control_points) < 4:
            raise ValueError('BSpline needs at least 4 points')
        super().__init__(name, QColor(0, 0, 0))
        self.thickness = thickness

        self.points = control_points
        self.line_as_points = self.calculate_lines(0.1)

    def as_list_of_tuples(self) -> List[Tuple[int, int, int]]:
        '''Return points as list of tuples'''
        tuples = []
        # if you are exporting all the lines
        #tuples.append((self.line_as_points[0].p1.x, self.line_as_points[0].p1.y, self.line_as_points[0].p1.z))
        # for line in self.line_as_points:
        #    tuples.append((line.p2.x, line.p2.y, line.p2.z))

        # if you are exporting the control points
        for points in self.points:
            tuples.append((points.x, points.y, points.z))

        return tuples

    def _e_coef(self, delta: float) -> np.array:
        '''Generate the E matrix for calculating curve plot'''
        return np.array([
            [0, 0, 0, 1],
            [delta**3, delta**2, delta, 0],
            [6*delta**3, 2*delta**2, 0, 0],
            [6*delta**3, 0, 0, 0]
        ])

    def calc_curve_points(self, steps: int, points: np.array, E: np.array, Mbs: np.array):
        '''Calculate points for curve'''
        coefs = Mbs.dot(points)
        diffs = E.dot(coefs)
        x, y = diffs[0]
        dx, dy = diffs[1]
        dx2, dy2 = diffs[2]
        dx3, dy3 = diffs[3]

        curve_points = [(x, y)]
        for i in range(steps):
            x += dx
            y += dy
            curve_points.append((x, y))

            dx += dx2
            dy += dy2
            dx2 += dx3
            dy2 += dy3

        return np.array(curve_points)

    def calculate_lines(self, delta: float) -> List[Line]:
        '''Plot the curve to lines'''
        Mbs = np.array([[-1, 3, -3, 1],
                        [3, -6, 3, 0],
                        [-3, 0, 3, 0],
                        [1, 4, 1, 0]])
        Mbs = Mbs / 6

        G = np.array([[p.x, p.y] for p in self.points])
        E = self._e_coef(delta)
        steps = int(1/delta)
        points = []
        for i in range(3, len(G)):
            base_points = G[i-3: i+1]
            points.extend(self.calc_curve_points(steps, base_points, E, Mbs))

        points3d = [
            Point3D('_p', x=p[0], y=p[1], z=0)
            for p in points
        ]
        lines = []
        for i, point in enumerate(points3d[:-1]):
            line = Line('__',
                        p1=point,
                        p2=points3d[i+1],
                        thickness=self.thickness)
            line.color = self.color
            lines.append(line)

        return lines

    def describe_export_with(self, points: List[Tuple[float, float, float]],
                             colors: List[QColor]) -> List[str]:
        '''Return lines that describe object in .obj file, using indexes
        from points and names from colors'''

        # index from all points
        indexes = [str(points.index(p) + 1) for p in self.as_list_of_tuples()]

        return ['# BSpline',
                f'o {self.name}',
                f'usemtl {self.color.name()[1:]}',
                f'cstype bspline',
                f'curv2 {" ".join(indexes)}']


class Object3D(BaseNamedColoredObject):
    '''Object composed by 3D Points and faces'''

    def __init__(self, name: str, points: List[Point3D],
                 faces: List[List[int]], thickness: int = 3):
        super().__init__(name, QColor(0, 0, 0))
        self.thickness = thickness

        self.faces = faces
        self.points = points

    def get_wireframes(self) -> List[Wireframe]:
        '''Connect the points for each face and return list of wireframes'''
        wireframes = []
        for face in self.faces:
            points = []
            for index in face:
                points.append(self.points[index])

            wireframe = Wireframe(
                name='__',
                points=points,
                thickness=self.thickness
            )
            wireframe.color = self.color

            wireframes.append(wireframe)
        return wireframes


class ViewportObjectRepresentation(NamedTuple):
    '''Class to hold data of a object ready to be draw at viewport'''
    name: str
    points: List[Point3D]
    color: QColor
    thickness: int
