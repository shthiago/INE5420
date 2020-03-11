from PyQt5 import QtWidgets, QtCore, QtGui

from model.objects import Point3D, Line, Wireframe


class ViewPort(QtWidgets.QLabel):
    """
    Class to be the drawing area of applicviewportation
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
        self.objects = []

    def draw_objects(self, objects):
        """
        Redraw view, checking if objects are inside the viewport

        Parameters
        ----------
        objects: list
            List of objects to be draw
        """

        self.objects = objects
        self.update()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(0, 0, 0))
        for obj in self.objects:
            # In case it is a point
            if len(obj) == 1:
                x, y = obj
                qp.drawPoint(x, y)

            else:
                # In case is a multiple point object
                prev_p = obj[0]
                for p in obj[1:]:
                    xs, ys = prev_p
                    xe, ye = p
                    qp.drawLine(xs, ys, xe, ye)
                    prev_p = p

        qp.end()

    def point_inside_viewport(self, point: Point3D):
        """
        Check if point is inside current viewport

        Parameters
        --------
        point: Point3D

        Return
        --------
        True/False
        """
        return point.x >= self.current_base_x and \
            point.x <= self.current_base_x + self.current_width and \
            point.y >= self.current_base_y and \
            point.y <= self.current_base_y + self.current_height
