"""
File for modeling objects to be stored
"""

from collections import namedtuple

# Class for holding the three values with gettings/setters
Point3D = namedtuple('Point3D', ['name', 'x', 'y', 'z'])

# Class for holding the two points of a line
Line = namedtuple('Line', ['name', 'p1', 'p2'])
