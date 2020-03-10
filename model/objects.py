"""
File for modeling objects to be stored
"""

from collections import namedtuple

# Class for holding the three values with gettings/setters
Point3D = namedtuple('Point3D', ['name', 'x', 'y', 'z'])

# Class for holding the two points of a line
Line = namedtuple('Line', ['name', 'p1', 'p2'])


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

        self.points = points
        self.name = name
