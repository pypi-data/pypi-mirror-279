from dataclasses import dataclass
from typing import Dict, List

from ._check_array_pair_polygon import check_array_pair_polygon


@dataclass
class Polygon:
    """
    A polygon around a predicted object.
    """
    # The (x, y) coordinates of the points of the polygon (at least 3)
    points: List[List[int]] = None

    def to_array_pair_polygon(self) -> Dict[str, List[int]]:
        """
        Converts this Polygon into an array-pair polygon, which is a dict with 2 keys, 'x' and
        'y', which both produce lists of coordinates.

        :return:
                    The array-pair polygon representation of this Polygon.
        """
        result = {
            "y": [],
            "x": []
        }

        for x, y in self.points:
            result["x"].append(x)
            result["y"].append(y)

        return result

    def __str__(self):
        """
        Returns a short string representation of itself.

        :return: the string representation
        :rtype: str
        """
        return "#points=%d" % len(self.points)

    def to_dict(self):
        """
        Returns its values as dictionary.

        :return: the generated dictionary
        :rtype: dict
        """
        return {
            "points": self.points,
        }

    @classmethod
    def from_array_pair_polygon(cls, app: Dict[str, List[int]]) -> 'Polygon':
        """
        Creates a Polygon instance from an array-pair representation.

        :param app:
                    The array-pair representation.
        :return:
                    The Polygon instance.
        """
        # Make sure the array-pair polygon is kosher
        check_array_pair_polygon(app)

        return Polygon(
            points=[[x, y] for x, y in zip(app['x'], app['y'])]
        )
