'''Clipper class'''
from enum import Enum, auto
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Union, Tuple, Optional
from math import isclose

from src.model.objects import Point3D, Line, Wireframe


@dataclass
class ClipperSetup:
    '''Object to configure clipper

    Attributes:
    - xmax: float
    - xmin: float
    - ymax: float
    - ymin: float
    '''
    xmax: float
    xmin: float
    ymax: float
    ymin: float


def close_to_zero(num: float) -> bool:
    '''Centralzie comparisons with zero for this module'''
    return isclose(num, 0, abs_tol=1e-6)


class Clipper:
    '''Centralize clipping processess'''

    def __init__(self, setup: ClipperSetup):
        '''Receive the setup with needed information for clipping algorithms
        '''
        self.setup = setup

    def clip_objects(self, objects: List[Union[Point3D, Line, Wireframe]]
                     ) -> List[Union[Point3D, Line, Wireframe]]:
        '''Receive a list of objects and return another list with objects
        cliped
        '''

        cliped_objects: List[Union[Point3D, Line, Wireframe]] = []
        for obj in objects:
            if isinstance(obj, Point3D):
                inside_window, new_obj = self._clip_point(obj)
                if inside_window:
                    cliped_objects.append(new_obj)

            elif isinstance(obj, Line):
                inside_window, new_obj = self._clip_line(obj)
                if inside_window:
                    cliped_objects.append(new_obj)

            elif isinstance(obj, Wireframe):
                inside_window, new_objs = self._clip_wireframe(obj)
                if inside_window:
                    cliped_objects.extend(new_objs)

            else:
                raise ValueError(f'Clipping not implemented for `{obj}`')

        return cliped_objects

    def _clip_point(self, point: Point3D) -> Tuple[bool, Optional[Point3D]]:
        '''Clip a point based on clipper setup'''
        in_x_range = self.setup.xmin <= point.x <= self.setup.xmax
        in_y_range = self.setup.ymin <= point.y <= self.setup.ymax

        if in_x_range and in_y_range:
            return True, point

        return False, None

    def _clip_line(self, line: Line) -> Tuple[bool, Optional[Line]]:
        '''Clip a line based on clipper setup'''
        lb_clipper = LiangBarskyLineClipping(line, self.setup)

        clipped = lb_clipper.get_clipped()

        return clipped is not None, clipped

    def _clip_wireframe(self, wireframe: Wireframe
                        ) -> Tuple[bool, Optional[Line]]:
        '''Clip a wireframe based on clipper setup'''
        wa_clipper = WeilerAthertonPolygonClipping(wireframe, self.setup)
        wireframes = wa_clipper.get_clipped()
        if wireframe:
            return True, wireframes

        return False, None


class LiangBarskyLineClipping:
    '''Class to centralize operations with Liang-Barsky'''

    def __init__(self, line: Line, clipper_setup: ClipperSetup):
        '''Initialize values for equations'''
        self.pq_list = [
            {
                'p': -(line.p2.x - line.p1.x),
                'q': line.p1.x - clipper_setup.xmin
            },
            {
                'p': (line.p2.x - line.p1.x),
                'q': clipper_setup.xmax - line.p1.x
            },
            {
                'p': -(line.p2.y - line.p1.y),
                'q': line.p1.y - clipper_setup.ymin
            },
            {
                'p': (line.p2.y - line.p1.y),
                'q': clipper_setup.ymax - line.p1.y
            }
        ]

        self.is_inside = not any([close_to_zero(k['p'])
                                  and k['q'] < 0
                                  for k in self.pq_list])

        self.line = line

    def get_clipped(self) -> Optional[Line]:
        '''Return the line clipped if is inside the setup'''
        if not self.is_inside:
            return None

        positives = [d for d in self.pq_list if not close_to_zero(
            d['p']) and d['p'] > 0]
        negatives = [d for d in self.pq_list if not close_to_zero(
            d['p']) and d['p'] < 0]

        positives = [d['q']/d['p'] for d in positives]
        negatives = [d['q']/d['p'] for d in negatives]

        u1 = max([0] + negatives)
        u2 = min([1] + positives)

        if u1 > u2:
            return None

        new_line = deepcopy(self.line)

        new_line.p1 = Point3D(
            name='_p1',
            x=self.line.p1.x + self.pq_list[1]['p'] * u1,
            y=self.line.p1.y + self.pq_list[3]['p'] * u1,
            z=self.line.p1.z
        )

        new_line.p2 = Point3D(
            name='_p2',
            x=self.line.p1.x + self.pq_list[1]['p'] * u2,
            y=self.line.p1.y + self.pq_list[3]['p'] * u2,
            z=self.line.p1.z
        )

        return new_line


class _Type(Enum):
    ORIGINAL = auto()
    ENTERING = auto()
    EXITING = auto()


class WeilerAthertonPolygonClipping:
    '''Functions to make the Weiler Atherton clipping'''

    def __init__(self, wireframe: Wireframe, setup: ClipperSetup):
        '''Initialize with internal properties'''
        self.setup = setup

        self.wireframe = wireframe

        self.top_left = Point3D('tl', x=setup.xmin, y=setup.ymax, z=0)
        self.top_right = Point3D('tr', x=setup.xmax, y=setup.xmax, z=0)
        self.bot_right = Point3D('br', x=setup.xmax, y=setup.ymin, z=0)
        self.bot_left = Point3D('bl', x=setup.xmin, y=setup.ymin, z=0)

    def point_inside_window(self, point: Point3D) -> bool:
        '''Check if point is inside window received a setup'''
        inside_x_range = self.setup.xmin <= point.x <= self.setup.xmax
        inside_y_range = self.setup.ymin <= point.y <= self.setup.ymax

        return inside_x_range and inside_y_range

    def copy_wireframe(self, points: Optional[List[Point3D]] = None) -> Wireframe:
        '''Return copy of internal object, optionally setting its point'''
        if points is None:
            return deepcopy(self.wireframe)

        nwf = deepcopy(self.wireframe)
        nwf.points = points
        return nwf

    def insert_into_edges(self, edges: List[Tuple[Point3D, _Type]],
                          point: Point3D, p_type: _Type
                          ) -> List[Tuple[Point3D, _Type]]:
        '''Insert the point into edges list based on what edge
        line the point is from, considering a clockwise path'''
        print(point)

        if point.x == self.setup.xmax:
            # Right edge
            index = edges.index((self.bot_right, _Type.ORIGINAL))
            edges.insert(index, (point, p_type))

        elif point.x == self.setup.xmin:
            # Left edge
            index = edges.index((self.top_left, _Type.ORIGINAL))
            edges.insert(index, (point, p_type))

        elif point.y == self.setup.ymin:
            # Bottom edge
            index = edges.index((self.bot_left, _Type.ORIGINAL))
            edges.insert(index, (point, p_type))

        elif point.y == self.setup.ymax:
            # Top edge
            index = edges.index((self.top_right, _Type.ORIGINAL))
            edges.insert(index, (point, p_type))

        return edges

    def order_edges(self, edges: List) -> List:
        '''Take the list of edges and return it ordering the points between
        each edge, using the extreme of edge to order'''
        # Left border
        slice_0 = edges[
            0:
            edges.index((self.top_left, _Type.ORIGINAL))+1
        ]
        if len(slice_0) > 1:
            slice_0.sort(key=lambda k: k[0].y)

        # Top border
        slice_1 = edges[
            edges.index((self.top_left, _Type.ORIGINAL))+1:
            edges.index((self.top_right, _Type.ORIGINAL))+1
        ]
        if len(slice_1) > 1:
            slice_1.sort(key=lambda k: k[0].x)

        # Right border
        slice_2 = edges[
            edges.index((self.top_right, _Type.ORIGINAL))+1:
            edges.index((self.bot_right, _Type.ORIGINAL))+1
        ]
        if len(slice_2) > 1:
            slice_2.sort(key=lambda k: k[0].y, reverse=True)

        # Bottom border
        slice_3 = edges[
            edges.index((self.bot_right, _Type.ORIGINAL))+1:
        ]
        if len(slice_3) > 1:
            slice_3.sort(key=lambda k: k[0].x, reverse=True)

        return slice_0 + slice_1 + slice_2 + slice_3

    def get_clipped(self) -> Optional[List[Wireframe]]:
        '''Apply the clipping algorithm'''

        subject = [(p, _Type.ORIGINAL) for p in self.wireframe.points]
        edges = [(self.top_left, _Type.ORIGINAL),
                 (self.top_right, _Type.ORIGINAL),
                 (self.bot_right, _Type.ORIGINAL),
                 (self.bot_left, _Type.ORIGINAL)]

        entries = []

        for line in self.wireframe.lines():
            lb_line_clipper = LiangBarskyLineClipping(line, self.setup)
            clipped = lb_line_clipper.get_clipped()
            if clipped is not None:
                if line.p2 != clipped.p2:
                    index = subject.index((line.p1, _Type.ORIGINAL))
                    subject.insert(index + 1, (clipped.p2, _Type.EXITING))
                    edges = self.insert_into_edges(edges, clipped.p2,
                                                   _Type.EXITING)

                if line.p1 != clipped.p1:
                    index = subject.index((line.p1, _Type.ORIGINAL))
                    subject.insert(index + 1, (clipped.p1, _Type.ENTERING))
                    entries.append((clipped.p1, _Type.ENTERING))
                    edges = self.insert_into_edges(edges, clipped.p1,
                                                   _Type.ENTERING)
        out = []

        edges = self.order_edges(edges)

        for point, t in entries:
            new_polygon_points = [point]
            sub_len = len(subject)
            index = (subject.index((point, t)) + 1) % sub_len
            curr_type = None
            while True:
                sub_point, curr_type = subject[index]
                new_polygon_points.append(sub_point)
                if curr_type != _Type.ORIGINAL:
                    break
                index = (index + 1) % sub_len

            edges_len = len(edges)
            index = (edges.index(
                (new_polygon_points[-1], curr_type)) + 1) % edges_len

            while True:
                edge_point, curr_type = edges[index]
                new_polygon_points.append(edge_point)
                if curr_type != _Type.ORIGINAL:
                    break

                index = (index + 1) % edges_len

            out.append(new_polygon_points)

        if len(out) == 0 and self.point_inside_window(subject[0][0]):
            return [self.copy_wireframe()]

        return [
            self.copy_wireframe(points=points)
            for points in out
        ]
