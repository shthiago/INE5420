"""
File for modeling objects to be stored
"""

from collections import namedtuple

# Class for holding the three values with gettings/setters
Point3D = namedtuple('Point3D', ['name', 'x', 'y', 'z'])


class Line:
    """
    Class for holding the two points of a line
    """

    def __init__(self, name: str, p1: Point3D, p2: Point3D):
        if not isinstance(p1, Point3D):
            raise ValueError(f'p1 shoulf be of type Point3D, got {type(p1)}')
        if not isinstance(p2, Point3D):
            raise ValueError(f'p2 shoulf be of type Point3D, got {type(p2)}')

        self._name = name
        self._p1 = p1
        self._p2 = p2

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, p1):
        self._p1 = p1

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, p2):
        self._p2 = p2

    @property
    def points(self):
        return [self._p1, self._p2]


class Wireframe:
    """
    Class to hold polygons
    """

    def __init__(self, name: str, points: list):
        """
        Parameters
        ----------
        points: list
            List of Point3D
        """

        for i in points:
            if not isinstance(i, Point3D):
                raise ValueError('Wireframe must be constructed ' +
                                 'from Point3D list')

        self._points = points
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points
