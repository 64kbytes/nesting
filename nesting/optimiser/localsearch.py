import random
import numpy as np
from shapely import affinity
from shapely.geometry import Polygon
from shapely.strtree import STRtree
from nesting.optimiser.structs import Shape


class LocalSearch:
    def __init__(self, shape: Shape, center, angle, radius, holes, board, hole_offset, edge_offset):
        # self.optimiser = optimiser
        self.offset = center
        self.angle = angle
        self._shape = shape.buffer(hole_offset)
        self.board = Shape(Polygon(board).buffer(hole_offset).buffer(-edge_offset))
        self.shape_buffer = shape.buffer(radius / 2)
        self.current_max = float("-inf")
        self.fail_counter = 0
        self.tree = STRtree([h.geometry for h in holes])

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        if type(shape) is not Shape:
            breakpoint()
        self._shape = shape

    def getRandomNeighbor(self, center, rand_func):
        return [c + rand_func() for c in center]

    def getDeterminedVicinity(self, point=None, angle=None):
        if not point:
            point = self.offset
        if not angle:
            angle = self.angle
        center = np.array([*point, angle])
        magic = 10 * np.array(
            [
                [0, 0, 0],
                [0, 0, 1],
                [0, 0, -1],
                [0, 1, 0],
                [0, 1, 1],
                [0, 1, -1],
                [0, -1, 0],
                [0, -1, 1],
                [0, -1, -1],
                [1, 0, 0],
                [1, 0, 1],
                [1, 0, -1],
                [1, 1, 0],
                [1, 1, 1],
                [1, 1, -1],
                [1, -1, 0],
                [1, -1, 1],
                [1, -1, -1],
                [-1, 0, 0],
                [-1, 0, 1],
                [-1, 0, -1],
                [-1, 1, 0],
                [-1, 1, 1],
                [-1, 1, -1],
                [-1, -1, 0],
                [-1, -1, 1],
                [-1, -1, -1],
            ]
        )
        magic.reshape([1, 27 * 3])
        magicmatrix = np.array([c * random.random() for c in magic.reshape([1, 27 * 3])[0]]).reshape([27, 3])
        return (magicmatrix + center).tolist()

    def generateVicinity(self, point=None, angle=None, mode="uniform", count=20):
        if not point:
            point = self.offset
        if not angle:
            angle = self.angle
        center = [*point, angle]
        vicinity = [center]
        if mode == "uniform":
            rf = lambda: random.uniform(-10, 10)
        elif mode == "uniform-int":
            rf = lambda: random.randint(-10, 10)
        elif mode == "gauss":
            rf = lambda: random.gauss(0, 3)
        vicinity.extend([self.getRandomNeighbor(center, rand_func=rf) for _ in range(count)])
        return vicinity

    def getOverlapArea(self, shape: Shape = None, offset=None, angle=None):
        if not shape:
            shape = self.shape_buffer
        if not offset:
            offset = self.offset
        if not angle:
            angle = self.angle
        area = 0
        shape = affinity.translate(affinity.rotate(shape.geometry, angle, origin=(0, 0)), *offset)
        overlaps = [h for h in self.tree.query(shape)]

        for h in [h for h in overlaps if h > 0]:
            try:
                area += shape.intersection(self.tree.geometries.take(h)).area
            except Exception as err:
                breakpoint()
                raise

        area += shape.difference(self.board.geometry).area
        return area

    def getFitness(self, center=None, offset=None, angle=None):
        if center:
            offset = center[0:2]
            angle = center[2]
        if not offset:
            offset = self.offset
        if not angle:
            angle = self.angle
        area_shape = self.getOverlapArea(shape=self.shape, offset=offset, angle=angle)
        area_buffer = self.getOverlapArea(shape=self.shape_buffer, offset=offset, angle=angle)
        return area_buffer * (not area_shape) - area_shape

    def step(self):
        vicinity = self.generateVicinity()
        # vicinity = self.getDeterminedVicinity()
        fitness = [self.getFitness(center=v) for v in vicinity]
        max_index, max_area = max(enumerate(fitness), key=lambda f: f[1])
        if max_index == 0:  # no better place found
            self.fail_counter += 1
            return False
        else:
            self.current_max = max_area
            self.offset = vicinity[max_index][0:2]
            self.angle = vicinity[max_index][2]
            return True


if __name__ == "__main__":
    pass
