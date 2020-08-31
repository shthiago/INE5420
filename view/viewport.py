from PyQt5 import QtWidgets, QtCore, QtGui

from model.objects import Point3D, Line, Wireframe


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
        self.objects = []

    def draw_objects(self, objects):
        """
        Redraw view, checking if objects are inside the viewport

        Parameters
        ----------
        objects: list
            List of objects to be draw
        """
        for obj in objects:
            if not isinstance(obj, dict):
                raise ValueError('Invalid object to be drawn')

            for point in obj['points']:
                if len(point) != 2:
                    raise ValueError('Invalid object to be drawn')

        self.objects = objects
        self.update()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        pen = QtGui.QPen()
        pen.setWidth(3)
        for obj in self.objects:
            # Get specific attributes
            color = obj['attr']['color']
            pen.setColor(color)
            qp.setPen(pen)

            # In case it is a point
            if len(obj['points']) == 1:
                x, y = obj['points'][0]
                qp.drawPoint(x, y)

            else:
                # In case is a multiple point object
                prev_p = obj['points'][0]
                for p in obj['points'][1:]:
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
