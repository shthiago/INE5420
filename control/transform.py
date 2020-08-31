'''Transformations for object'''
from enum import Enum
from typing import List


import numpy as np
from PyQt5.QtWidgets import QWidget

from model.objects import Point3D, Wireframe, Line, BaseNamedColoredObject


def transform(points: List[Point3D], matrix: np.ndarray):
    '''Apply transformation'''
