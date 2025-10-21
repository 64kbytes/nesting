from collections import defaultdict

from shapely import Polygon


class Shape:
    def __init__(self, *args, **kwargs):
        self.geometry = Polygon(*args, **kwargs)
        self.shape_nfps = defaultdict()  # keys are wkts of shapes + hole offset, values are NFPS
        self.name = "undefined"  # friendly name to identify the shape
        self.position = [0, 0]  # position of the shape on the board (reference point is circle_center)
        self.angle = 0  # angle of the shape
        self.origin = [0, 0]
        self.centroid = [0, 0]

    def simplify(self, *args, **kwargs):
        return Shape(self.geometry.simplify(*args, **kwargs))

    @property
    def convex_hull(self):
        return Shape(self.geometry.convex_hull)

    @property
    def area(self):
        return self.geometry.area

    def buffer(self, *args, **kwargs):
        return Shape(self.geometry.buffer(*args, **kwargs))

    @property
    def boundary(self):
        return self.geometry.boundary

    @property
    def exterior(self):
        return self.geometry.exterior

    def difference(self, polygon, **kwargs):
        return Shape(self.geometry.difference(polygon.geometry, **kwargs))

    @property
    def is_empty(self):
        return self.geometry.is_empty

    @property
    def has_z(self):
        return self.geometry.has_z

    def clone(self, obj):
        shape = Shape(obj)
        shape.shape_nfps = self.shape_nfps
        shape.name = self.name
        shape.position = self.position
        shape.angle = self.angle
        shape.origin = self.origin
        shape.centroid = self.centroid
        return shape

    @property
    def bounds(self):
        return self.geometry.bounds

    @property
    def wkt(self):
        return self.geometry.wkt