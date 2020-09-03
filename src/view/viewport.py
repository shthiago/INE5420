'''Viewport object, used to draw objects into user interface'''
from typing import List

from PyQt5 import QtWidgets, QtCore, QtGui

from src.model.objects import ViewportObjectRepresentation


class ViewPort(QtWidgets.QLabel):
    """
    Class to be the drawing area of application viewport
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Object style sheet
        stylesheet = '''
            QLabel {
                background-color: white;
                border: 1px solid black
            }
        '''
        self.setStyleSheet(stylesheet)

        # Varaible to hold objects to be drew
        self.objects: List[ViewportObjectRepresentation] = []

    def draw_objects(self, objects: List[ViewportObjectRepresentation]):
        """
        Redraw view, checking if objects are inside the viewport

        Parameters
        ----------
        objects: List[ViewportObjectRepresentation]
            List of objects to be draw
        """

        self.objects = objects
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent):
        '''Reimplementing paint event function, that is called by update'''
        painter = QtGui.QPainter()
        painter.begin(self)
        pen = QtGui.QPen()
        pen.setWidth(3)
        for obj in self.objects:
            # Get specific attributes
            pen.setColor(obj.color)
            painter.setPen(pen)

            # In case it is a point
            if len(obj.points) == 1:
                point = obj.points[0]
                painter.drawPoint(point.x, point.y)

            # In case it is a line
            elif len(obj.points) == 2:
                init_p, end_p = obj.points
                painter.drawLine(init_p.x, init_p.y,
                                 end_p.x, end_p.y)

            # In case it is a wireframe
            else:
                init_p = obj.points[0]
                prev_p = init_p
                for current_p in obj.points[1:]:
                    painter.drawLine(prev_p.x, prev_p.y,
                                     current_p.x, current_p.y)
                    prev_p = current_p

                last_p = obj.points[-1]
                painter.drawLine(last_p.x, last_p.y,
                                 init_p.x, init_p.y)

        painter.end()
