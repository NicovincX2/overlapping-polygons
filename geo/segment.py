# -*- coding: utf-8 -*-
#!/usr/bin/env python3

"""
segment between two points.
"""


from geo.quadrant import Quadrant
from geo.utils import almostEqual


def ccw(A, B, C):
    """A, B, C 3 points, renvoie s'il sont orienté counterclockwise"""
    return (C.coordinates[1] - A.coordinates[1]) * (
        B.coordinates[0] - A.coordinates[0]
    ) > (B.coordinates[1] - A.coordinates[1]) * (C.coordinates[0] - A.coordinates[0])


class Segment:
    """
    oriented segment between two points.

    for example:

    - create a new segment between two points:

        segment = Segment([point1, point2])

    - create a new segment from coordinates:

        segment = Segment([Point([1.0, 2.0]), Point([3.0, 4.0])])

    - does self intersect with an other segment:

        segment1.intersect(segment2) (bool)

    """

    __slots__ = "endpoints"

    def __init__(self, points):
        """
        create a segment from an array of two points.
        """
        self.endpoints = points

    def __eq__(self, other):
        return self.endpoints == other.endpoints

    def __lt__(self, other):
        """
        lexicographical comparison % abscisse
        """
        ax = self.endpoints[0].coordinates[0]
        bx = self.endpoints[1].coordinates[0]
        cx = other.endpoints[0].coordinates[0]
        dx = other.endpoints[1].coordinates[0]
        return (ax < cx and ax < dx) or (bx < cx and bx < dx)

    def copy(self):
        """
        return duplicate of given segment (no shared points with original,
        they are also copied).
        """
        return Segment([p.copy() for p in self.endpoints])

    def length(self):
        """
        return length of segment.
        example:
            segment = Segment([Point([1, 1]), Point([5, 1])])
            distance = segment.length() # distance is 4
        """
        return self.endpoints[0].distance_to(self.endpoints[1])

    def bounding_quadrant(self):
        """
        return min quadrant containing self.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for point in self.endpoints:
            quadrant.add_point(point)
        return quadrant

    def intersect(self, other):
        """Return true if line segments AB and CD intersect"""
        return ccw(self.endpoints[0], other.endpoints[0], other.endpoints[1]) != ccw(
            self.endpoints[1], other.endpoints[0], other.endpoints[1]
        ) and ccw(self.endpoints[0], self.endpoints[1], other.endpoints[0]) != ccw(
            self.endpoints[0], self.endpoints[1], other.endpoints[1]
        )


    def is_vertical(self):
        """
        return if we are a truly vertical segment.
        """
        return self.endpoints[0].coordinates[0] == self.endpoints[1].coordinates[0]

    def svg_content(self):
        """
        svg for tycat.
        """
        return '<line x1="{}" y1="{}" x2="{}" y2="{}"/>\n'.format(
            *self.endpoints[0].coordinates, *self.endpoints[1].coordinates
        )

    def endpoint_not(self, point):
        """
        return first endpoint which is not given point.
        """
        if self.endpoints[0] == point:
            return self.endpoints[1]

        return self.endpoints[0]

    def contains(self, possible_point):
        """
        is given point inside us ?
        be careful, determining if a point is inside a segment is a difficult problem
        (it is in fact a meaningless question in most cases).
        you might get wrong results for points extremely near endpoints.
        """
        distance = sum(possible_point.distance_to(p) for p in self.endpoints)
        return almostEqual(distance, self.length())

    def __str__(self):
        return (
            "Segment([" + str(self.endpoints[0]) + ", " + str(self.endpoints[1]) + "])"
        )

    def __repr__(self):
        return "[" + repr(self.endpoints[0]) + ", " + repr(self.endpoints[1]) + "])"

