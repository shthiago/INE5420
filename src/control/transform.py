'''Transformations for objects'''
from typing import List, Union
from math import cos, sin, radians
from statistics import mean
from copy import deepcopy

import numpy as np
from src.model.objects import Point3D, Line, Wireframe, BezierCurve, BezierCurveSetup, BSplineCurve


def transform(points: List[Point3D], matrix: np.ndarray) -> List[Point3D]:
    '''Apply transformation'''
    new_points: List[Point3D] = []

    for point in points:
        np_point = np.array([point.x, point.y, point.z, 1])
        new_point = np_point.dot(matrix)

        new_points.append(Point3D(
            name=point.name,
            x=new_point[0],
            y=new_point[1],
            z=new_point[2]
        ))

    return new_points


def get_translation_matrix(desloc_x: float, desloc_y: float, desloc_z: float) -> np.ndarray:
    '''Create the translation matrix from the deslocation vector'''
    return np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [desloc_x, desloc_y, desloc_z, 1]
        ]
    )


def get_scaling_matrix(scale_x: float, scale_y: float, scale_z: float) -> np.ndarray:
    '''Create the scaling matrix from the scale factors'''
    return np.array(
        [
            [scale_x, 0, 0, 0],
            [0, scale_y, 0, 0],
            [0, 0, scale_z, 0],
            [0, 0, 0, 1]
        ]
    )


def get_rz_rotation_matrix_from_degrees(angle: float) -> np.ndarray:
    '''Create the rotation matrix from the angle in degrees, for z axis'''
    rad_angle = radians(angle)
    return np.array(
        [
            [cos(rad_angle), -sin(rad_angle), 0, 0],
            [sin(rad_angle), cos(rad_angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    )


def get_ry_rotation_matrix_from_degrees(angle: float) -> np.ndarray:
    '''Create the rotation matrix from the angle in degrees, for y axis'''
    rad_angle = radians(angle)
    return np.array(
        [
            [cos(rad_angle), 0, sin(rad_angle), 0],
            [0, 1, 0, 0],
            [-sin(rad_angle), 0, cos(rad_angle), 0],
            [0, 0, 0, 1]
        ]
    )


def get_rx_rotation_matrix_from_degrees(angle: float) -> np.ndarray:
    '''Create the rotation matrix from the angle in degrees, for x axis'''
    rad_angle = radians(angle)
    return np.array(
        [
            [1, 0, 0, 0],
            [0, cos(rad_angle), sin(rad_angle), 0],
            [0, -sin(rad_angle), cos(rad_angle), 0],
            [0, 0, 0, 1]
        ]
    )


def concat_transformation_matrixes(matrixes: List[np.ndarray]) -> np.ndarray:
    '''Concatenate transformation matrixes, ordered as input'''
    final_matrix = matrixes[0]
    for matrix in matrixes[1:]:
        final_matrix = final_matrix.dot(matrix)

    return final_matrix


def rotate_points_over_point_by_degrees(points: List[Point3D],
                                        point: Point3D,
                                        angle: float,
                                        rotation_axis: str) -> List[Point3D]:
    '''Rotate list of points over a input point'''
    if rotation_axis not in ['x', 'y', 'z']:
        raise ValueError(f'Invalid rotation axis: {rotation_axis}')

    if rotation_axis == 'x':
        rotation_matrix = get_rx_rotation_matrix_from_degrees(angle)
    elif rotation_axis == 'y':
        rotation_matrix = get_ry_rotation_matrix_from_degrees(angle)
    else:  # z axis
        rotation_matrix = get_rz_rotation_matrix_from_degrees(angle)

    transformation_matrix = concat_transformation_matrixes([
        get_translation_matrix(-point.x, -point.y, -point.z),
        rotation_matrix,
        get_translation_matrix(point.x, point.y, point.z),
    ])

    return transform(points, transformation_matrix)


def translate_points(points: List[Point3D],
                     desloc_x: float, desloc_y: float, desloc_z: float) -> List[Point3D]:
    '''Translate list of points by deslocation values'''
    translation_matrix = get_translation_matrix(desloc_x, desloc_y, desloc_z)

    return transform(points, translation_matrix)


def scale_points_by_point(points: List[Point3D], scale_x: float,
                          scale_y: float, scale_z: float, point: Point3D
                          ) -> List[Point3D]:
    '''Scale points, moving their origin to point before'''
    transformation_matrix = concat_transformation_matrixes([
        get_translation_matrix(-point.x, -point.y, -point.z),
        get_scaling_matrix(scale_x, scale_y, scale_z),
        get_translation_matrix(point.x, point.y, point.z)
    ])

    return transform(points, transformation_matrix)


class Transformator:
    '''Apply transform operations over objects'''

    def __init__(self, obj: Union[Point3D, Line, Wireframe, BezierCurve]):
        '''Initialize with a intern target object'''
        self._object: Union[Point3D, Line, Wireframe, BezierCurve] = obj

        # Internal value to define rotation axis
        self._rotation_axis = 'z'

    def get_object_geometric_center(self) -> Point3D:
        '''Get geometrix center of intern object'''
        if isinstance(self._object, Point3D):
            points = [self._object]

        elif isinstance(self._object, BezierCurve):
            points = []
            for setup in self._object.curves:
                points.extend([setup.P1, setup.P2, setup.P3, setup.P4])

        else:  # Wireframe and BSpline
            points = self._object.points

        return Point3D(
            name='_geometric_center',
            x=mean(map(lambda p: p.x, points)),
            y=mean(map(lambda p: p.y, points)),
            z=mean(map(lambda p: p.z, points))
        )

    def rotate_by_degrees_geometric_center(self, angle: float,
                                           rotation_axis: str
                                           ) -> Union[Point3D,
                                                      Line,
                                                      Wireframe,
                                                      BezierCurve]:
        '''Rotate over center intern object in by angle an input angle

        Parameters
        ----------
        angle: float
            Angle in degrees
        rotation_axis: str
            x, y or z
        '''

        self._rotation_axis = rotation_axis

        if isinstance(self._object, Point3D):
            # Rotating and Point3D over its center makes no difference
            return self._object

        if isinstance(self._object, Line):
            return self._rotate_internal_line_over_center(angle)

        if isinstance(self._object, BezierCurve):
            return self._rotate_internal_bezier_curve_over_center(angle)

        elif isinstance(self._object, BSplineCurve):
            return self._rotate_internal_bspline_curve_over_center(angle)

        return self._rotate_internal_wireframe_over_center(angle)

    def _rotate_internal_line_over_center(self, angle: float) -> Line:
        '''Rotate over center when internal is a Line and
            return copy of object'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        center = self.get_object_geometric_center()

        new_points = rotate_points_over_point_by_degrees(
            points=self._object.points,
            point=center,
            angle=angle,
            rotation_axis=self._rotation_axis
        )

        line = Line(
            name=self._object.name,
            p1=new_points[0],
            p2=new_points[1],
        )
        line.color = self._object.color

        return line

    def _rotate_internal_bezier_curve_over_center(self, angle: float) -> BezierCurve:
        '''Rotate a bezier curve over the center os the points from setups'''

        center = self.get_object_geometric_center()

        new_setups = []
        for setup in self._object.curves:
            points = [setup.P1, setup.P2, setup.P3, setup.P4]
            new_points = rotate_points_over_point_by_degrees(
                points, center, angle, self._rotation_axis)
            new_setups.append(BezierCurveSetup(
                P1=new_points[0],
                P2=new_points[1],
                P3=new_points[2],
                P4=new_points[3]
            ))

        new_curve = deepcopy(self._object)

        new_curve.curves = new_setups

        return new_curve

    def _rotate_internal_bspline_curve_over_center(self, angle: float) -> BSplineCurve:
        '''Rotate intrnal BSpline and return copy of object'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        center = self.get_object_geometric_center()

        new_points = rotate_points_over_point_by_degrees(
            points=self._object.points,
            point=center,
            angle=angle,
            rotation_axis=self._rotation_axis
        )

        new_spline = self._intern_copy()
        new_spline.points = new_points

        return new_spline

    def _rotate_internal_wireframe_over_center(self, angle: float) -> Wireframe:
        '''Rotate over centerwhen internal is a Wireframe and
            return copy of object'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        center = self.get_object_geometric_center()

        new_points = rotate_points_over_point_by_degrees(
            points=self._object.points,
            point=center,
            angle=angle,
            rotation_axis=self._rotation_axis
        )

        wireframe = self._intern_copy()
        wireframe.points = new_points

        return wireframe

    def rotate_by_degrees_origin(self, angle: float,
                                 rotation_axis: str) -> Union[Point3D, Line, Wireframe, BezierCurve]:
        '''Rotate intern object in by angle an input angle

        Parameters
        ----------
        angle: float
            Angle in degrees
        rotation_axis: str
            x, y or z
        '''

        self._rotation_axis = rotation_axis

        if isinstance(self._object, Point3D):
            # Rotating and Point3D over its center makes no difference
            return self._rotate_internal_point_over_origin(angle)

        if isinstance(self._object, Line):
            return self._rotate_internal_line_over_origin(angle)

        if isinstance(self._object, BezierCurve):
            return self._rotate_internal_bezier_curve_over_origin(angle)

        if isinstance(self._object, BSplineCurve):
            return self._rotate_internal_bspline_curve_over_origin(angle)

        return self._rotate_internal_wireframe_over_origin(angle)

    def _rotate_internal_bezier_curve_over_origin(self, angle: float) -> BezierCurve:
        '''Rotate when internal is a curve and return copy of object'''
        new_setups = []
        for setup in self._object.curves:
            points = [setup.P1, setup.P2, setup.P3, setup.P4]
            new_points = rotate_points_over_point_by_degrees(
                points, Point3D('_', 0, 0, 0), angle, self._rotation_axis)
            new_setups.append(BezierCurveSetup(
                P1=new_points[0],
                P2=new_points[1],
                P3=new_points[2],
                P4=new_points[3]
            ))

        new_curve = deepcopy(self._object)

        new_curve.curves = new_setups

        return new_curve

    def _rotate_internal_line_over_origin(self, angle: float) -> Line:
        '''Rotate when internal is a Line and return copy of object'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        new_points = rotate_points_over_point_by_degrees(
            points=self._object.points,
            point=Point3D('_', 0, 0, 0),
            angle=angle,
            rotation_axis=self._rotation_axis
        )

        line = Line(
            name=self._object.name,
            p1=new_points[0],
            p2=new_points[1],
        )
        line.color = self._object.color

        return line

    def _rotate_internal_bspline_curve_over_origin(self, angle: float) -> BSplineCurve:
        '''Rotate when internal is a Wireframe and return copy of object'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        new_points = rotate_points_over_point_by_degrees(
            points=self._object.points,
            point=Point3D('_', 0, 0, 0),
            angle=angle,
            rotation_axis=self._rotation_axis
        )

        new_spline = self._intern_copy()
        new_spline.points = new_points

        return new_spline

    def _rotate_internal_wireframe_over_origin(self, angle: float) -> Wireframe:
        '''Rotate when internal is a Wireframe and return copy of object'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        new_points = rotate_points_over_point_by_degrees(
            points=self._object.points,
            point=Point3D('_', 0, 0, 0),
            angle=angle,
            rotation_axis=self._rotation_axis
        )

        wireframe = self._intern_copy()
        wireframe.points = new_points

        return wireframe

    def _rotate_internal_point_over_origin(self, angle: float) -> Point3D:
        '''Rotate when internal is a point and return copy of object'''
        if not isinstance(self._object, Point3D):
            error = 'Trying to operate as point over:'
            raise TypeError(error + str(type(self._object)))

        rotated = rotate_points_over_point_by_degrees(
            points=[self._object],
            point=Point3D('_', 0, 0, 0),
            angle=angle,
            rotation_axis=self._rotation_axis)[0]

        rotated.color = self._object.color
        return rotated

    def rotate_by_degrees_point(self, angle: float, point: Point3D,
                                rotation_axis: str) -> Union[Point3D, Line, Wireframe, BezierCurve]:
        '''Rotate intern object in by an input angle over point

        Parameters
        ----------
        angle: float
            Angle in degrees
        point: Point3D
            Point to ratate over
        rotation_axis: str
            x, y or z
        '''

        self._rotation_axis = rotation_axis

        if isinstance(self._object, Point3D):
            # Rotating and Point3D over its center makes no difference
            return self._rotate_internal_point_over_point(angle, point)

        if isinstance(self._object, Line):
            return self._rotate_internal_line_over_point(angle, point)

        if isinstance(self._object, BezierCurve):
            return self._rotate_internal_bezier_curve_over_point(angle, point)

        if isinstance(self._object, BSplineCurve):
            return self._rotate_internal_bspline_curve_over_point(angle, point)

        return self._rotate_internal_wireframe_over_point(angle, point)

    def _rotate_internal_bezier_curve_over_point(self, angle: float,
                                                 point: Point3D) -> Line:
        '''Rotate when internal is a Line and return copy of object'''
        new_setups = []
        for setup in self._object.curves:
            points = [setup.P1, setup.P2, setup.P3, setup.P4]
            new_points = rotate_points_over_point_by_degrees(
                points, point, angle, self._rotation_axis)
            new_setups.append(BezierCurveSetup(
                P1=new_points[0],
                P2=new_points[1],
                P3=new_points[2],
                P4=new_points[3]
            ))

        new_curve = deepcopy(self._object)

        new_curve.curves = new_setups

        return new_curve

    def _rotate_internal_line_over_point(self, angle: float,
                                         point: Point3D) -> Line:
        '''Rotate when internal is a Line and return copy of object'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        new_points = rotate_points_over_point_by_degrees(
            points=self._object.points,
            point=point,
            angle=angle,
            rotation_axis=self._rotation_axis
        )

        line = Line(
            name=self._object.name,
            p1=new_points[0],
            p2=new_points[1],
        )
        line.color = self._object.color

        return line

    def _rotate_internal_wireframe_over_point(self, angle: float,
                                              point: Point3D) -> Wireframe:
        '''Rotate when internal is a Wireframe and return copy of object'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        new_points = rotate_points_over_point_by_degrees(
            points=self._object.points,
            point=point,
            angle=angle,
            rotation_axis=self._rotation_axis
        )

        wireframe = self._intern_copy()
        wireframe.points = new_points

        return wireframe

    def _rotate_internal_bspline_curve_over_point(self, angle: float,
                                                  point: Point3D) -> BSplineCurve:
        '''Rotate when internal is a Wireframe and return copy of object'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        new_points = rotate_points_over_point_by_degrees(
            points=self._object.points,
            point=point,
            angle=angle,
            rotation_axis=self._rotation_axis
        )

        new_spline = self._intern_copy()
        new_spline.points = new_points

        return new_spline

    def _rotate_internal_point_over_point(self, angle: float,
                                          point: Point3D) -> Point3D:
        '''Rotate when internal is a point and return copy of object'''
        if not isinstance(self._object, Point3D):
            error = 'Trying to operate as point over:'
            raise TypeError(error + str(type(self._object)))

        rotated = rotate_points_over_point_by_degrees(
            points=[self._object],
            point=point,
            angle=angle,
            rotation_axis=self._rotation_axis)[0]

        rotated.color = self._object.color
        return rotated

    def translate_by_vector(self, desloc_x: float, desloc_y: float, desloc_z: float
                            ) -> Union[Point3D, Line, Wireframe, BezierCurve]:
        '''Translate internal object by deslocation values'''
        if isinstance(self._object, Point3D):
            return self._translate_point_by_vector(desloc_x, desloc_y, desloc_z)

        if isinstance(self._object, Line):
            return self._translate_line_by_vector(desloc_x, desloc_y, desloc_z)

        if isinstance(self._object, BezierCurve):
            return self._translate_bezier_curve_by_vector(desloc_x, desloc_y, desloc_z)

        if isinstance(self._object, BSplineCurve):
            return self._translate_spline_curve_by_vector(desloc_x, desloc_y, desloc_z)

        return self._translate_wireframe_and_obj3d(desloc_x, desloc_y, desloc_z)

    def translate_to_point(self, point_x: float, point_y: float, point_z: float):
        '''Translate internal object to absolute point'''
        # Calcualte vector to take object to target position
        center = self.get_object_geometric_center()

        return self.translate_by_vector(point_x - center.x,
                                        point_y - center.y,
                                        point_z - center.z)

    def _translate_point_by_vector(self, desloc_x: float, desloc_y: float, desloc_z: float) -> Point3D:
        '''Translate internal object when is a point and return copy'''
        if not isinstance(self._object, Point3D):
            error = 'Trying to operate as point over:'
            raise TypeError(error + str(type(self._object)))

        translated = translate_points(
            points=[self._object],
            desloc_x=desloc_x,
            desloc_y=desloc_y,
            desloc_z=desloc_z
        )[0]
        translated.color = self._object.color

        return translated

    def _translate_bezier_curve_by_vector(self, desloc_x: float, desloc_y: float, desloc_z: float) -> Line:
        '''Translate internal object when is a curve and return copy'''
        new_setups = []
        for setup in self._object.curves:
            points = [setup.P1, setup.P2, setup.P3, setup.P4]
            new_points = translate_points(
                points, desloc_x, desloc_y, desloc_z)
            new_setups.append(BezierCurveSetup(
                P1=new_points[0],
                P2=new_points[1],
                P3=new_points[2],
                P4=new_points[3]
            ))

        new_curve = deepcopy(self._object)

        new_curve.curves = new_setups

        return new_curve

    def _translate_line_by_vector(self, desloc_x: float, desloc_y: float, desloc_z: float) -> Line:
        '''Translate internal object when is a line and return copy'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        new_points = translate_points(
            points=self._object.points,
            desloc_x=desloc_x,
            desloc_y=desloc_y,
            desloc_z=desloc_z
        )

        line = Line(
            name=self._object.name,
            p1=new_points[0],
            p2=new_points[1]
        )
        line.color = self._object.color

        return line

    def _translate_spline_curve_by_vector(self, desloc_x: float, desloc_y: float, desloc_z: float
                                          ) -> BSplineCurve:
        '''Translate internal object when is a wireframe and return copy'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        new_points = translate_points(
            points=self._object.points,
            desloc_x=desloc_x,
            desloc_y=desloc_y,
            desloc_z=desloc_z
        )

        new_spline = self._intern_copy()
        new_spline.points = new_points

        return new_spline

    def _translate_wireframe_and_obj3d(self, desloc_x: float, desloc_y: float, desloc_z: float
                                       ) -> Wireframe:
        '''Translate internal object when is a wireframe and return copy'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        new_points = translate_points(
            points=self._object.points,
            desloc_x=desloc_x,
            desloc_y=desloc_y,
            desloc_z=desloc_z
        )

        wireframe = self._intern_copy()
        wireframe.points = new_points

        return wireframe

    def scale(self, scale_x: float, scale_y: float, scale_z: float
              ) -> Union[Point3D, Line, Wireframe, BezierCurve]:
        '''Scale internal object by deslocation values'''
        if isinstance(self._object, Point3D):
            # A scaled point is itself
            return self._object

        if isinstance(self._object, Line):
            return self._scale_line(scale_x, scale_y, scale_z)

        if isinstance(self._object, BezierCurve):
            return self._scale_bezier_curve(scale_x, scale_y, scale_z)

        if isinstance(self._object, BSplineCurve):
            return self._scale_bspline_curve(scale_x, scale_y, scale_z)

        return self._scale_wireframe_and_obj3d(scale_x, scale_y, scale_z)

    def _scale_line(self, scale_x: float, scale_y: float, scale_z: float) -> Line:
        '''Scale internal when is a line and return copy'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        new_points = scale_points_by_point(
            points=self._object.points,
            point=self.get_object_geometric_center(),
            scale_x=scale_x,
            scale_y=scale_y,
            scale_z=scale_z
        )

        line = self._intern_copy()
        if not isinstance(line, Line):
            raise TypeError('Internal object is not line')

        line.p1 = new_points[0]
        line.p2 = new_points[1]
        return line

    def _scale_bezier_curve(self, scale_x: float, scale_y: float, scale_z: float) -> BezierCurve:
        '''Scale internal when is a wireframe and return copy'''
        new_setups = []
        for setup in self._object.curves:
            points = [setup.P1, setup.P2, setup.P3, setup.P4]
            new_points = scale_points_by_point(
                points=points,
                point=self.get_object_geometric_center(),
                scale_x=scale_x,
                scale_y=scale_y,
                scale_z=scale_z)
            new_setups.append(BezierCurveSetup(
                P1=new_points[0],
                P2=new_points[1],
                P3=new_points[2],
                P4=new_points[3]
            ))

        new_curve = deepcopy(self._object)

        new_curve.curves = new_setups

        return new_curve

    def _scale_bspline_curve(self, scale_x: float, scale_y: float, scale_z: float) -> BSplineCurve:
        '''Scale internal when is a wireframe and return copy'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        new_points = scale_points_by_point(
            points=self._object.points,
            point=self.get_object_geometric_center(),
            scale_x=scale_x,
            scale_y=scale_y,
            scale_z=scale_z
        )

        new_spline = self._intern_copy()
        new_spline.points = new_points
        return new_spline

    def _scale_wireframe_and_obj3d(self, scale_x: float, scale_y: float, scale_z: float) -> Wireframe:
        '''Scale internal when is a wireframe and return copy'''
        if isinstance(self._object, Point3D):
            error = 'Trying to operate as line/wireframe over point'
            raise TypeError(error)

        new_points = scale_points_by_point(
            points=self._object.points,
            point=self.get_object_geometric_center(),
            scale_x=scale_x,
            scale_y=scale_y,
            scale_z=scale_z
        )

        wireframe = self._intern_copy()
        if not isinstance(wireframe, Wireframe):
            raise TypeError('Internal object is not wireframe')

        wireframe.points = new_points
        return wireframe

    def _intern_copy(self) -> Union[Point3D, Line, Wireframe, BezierCurve]:
        '''Return deepcopy of internal object'''
        return deepcopy(self._object)


class Normalizer:
    '''Object to hold information to normalize coordinateds'''

    def __init__(self, window_center: Point3D, window_height: int,
                 window_width: int, vup_angle: int):
        '''Take the window measurements and v_up_angle to
            keep as internal values'''
        self._vup_angle: int = vup_angle
        self._window_center: Point3D = window_center
        self._window_height: int = window_height
        self._window_width: int = window_width

        self._normalization_matrix = self._mount_normalization_matrix()

    def _mount_normalization_matrix(self):
        '''Base on angle and window center, get the
            transformation matrix'''
        return concat_transformation_matrixes([
            get_translation_matrix(-self._window_center.x,
                                   -self._window_center.y,
                                   0),
            get_rz_rotation_matrix_from_degrees(self._vup_angle),
            get_scaling_matrix(1/self._window_width, 1/self._window_height, 1)
        ])

    def normalize_objects(self, objects: List[Union[Point3D, Line, Wireframe]]
                          ) -> List[Union[Point3D, Line, Wireframe]]:
        '''Return objects in the normalized coordinates'''
        normalized_objects: List[Union[Point3D, Line, Wireframe]] = []

        for obj in objects:
            normalized_objects.append(self.normalize_object(obj))

        return normalized_objects

    def normalize_object(self, obj: Union[Point3D, Line, Wireframe]
                         ) -> Union[Point3D, Line, Wireframe]:
        '''Direct a object to be transformed by specific function'''
        if isinstance(obj, Point3D):
            return self._normalize_point(obj)

        if isinstance(obj, Line):
            return self._normalize_line(obj)

        if isinstance(obj, Wireframe):
            return self._normalize_wireframe_and_obj3d(obj)

        raise TypeError(f'Invaldi type for normalization: {obj}')

    def _normalize_point(self, point: Point3D) -> Point3D:
        '''Apply transformation to single point'''
        return transform([point], self._normalization_matrix)[0]

    def _normalize_line(self, line: Line) -> Line:
        '''Apply normalizato to line'''
        points = transform(line.points, self._normalization_matrix)

        new_line = deepcopy(line)
        if not isinstance(new_line, Line):
            raise TypeError('Internal object is not line')

        new_line.p1 = points[0]
        new_line.p2 = points[1]

        return new_line

    def _normalize_wireframe_and_obj3d(self, wireframe: Wireframe) -> Wireframe:
        '''Apply normalization to wireframe'''
        points = transform(wireframe.points, self._normalization_matrix)

        new_wireframe = deepcopy(wireframe)

        if not isinstance(new_wireframe, Wireframe):
            raise TypeError('Internal object is not wireframe')

        new_wireframe.points = points

        return new_wireframe
