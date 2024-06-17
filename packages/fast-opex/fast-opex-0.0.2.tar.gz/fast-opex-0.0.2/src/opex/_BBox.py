from dataclasses import dataclass
from typing import Dict, List

from ._check_array_pair_polygon import check_array_pair_polygon


@dataclass
class BBox:
    """
    A rectangular region in an image.
    """
    # The x-coordinate of the left side
    left: int = None

    # The y-coordinate of the top
    top: int = None

    # The x-coordinate of the right side
    right: int = None

    # The y-coordinate of the bottom
    bottom: int = None

    def to_array_pair_polygon(self) -> Dict[str, List[int]]:
        """
        Converts this BBox into an array-pair polygon, which is a dict with 2 keys, 'x' and
        'y', which both produce lists of coordinates.

        :return:
                    The array-pair polygon representation of this BBox.
        """
        return {
            "y": [self.top, self.top, self.bottom, self.bottom],
            "x": [self.left, self.right, self.right, self.left]
        }

    def __str__(self):
        """
        Returns a short string representation of itself.

        :return: the string representation
        :rtype: str
        """
        return "left=%f, top=%f, right=%f, bottom=%f" % (self.left, self.top, self.right, self.bottom)

    def to_dict(self):
        """
        Returns its values as dictionary.

        :return: the generated dictionary
        :rtype: dict
        """
        return {
            "left": self.left,
            "top": self.top,
            "right": self.right,
            "bottom": self.bottom,
        }

    @classmethod
    def from_array_pair_polygon(cls, app: Dict[str, List[int]]) -> 'BBox':
        """
        Creates a BBox instance from an array-pair representation.

        :param app:
                    The array-pair representation.
        :return:
                    The BBox instance.
        """
        # Make sure the array-pair polygon is kosher
        check_array_pair_polygon(app)

        # Get the 'x' and 'y' coordinates
        x = app['x']
        y = app['y']

        # Make sure they are of length 4 (both lengths are equal so only test one)
        if len(x) != 4:
            raise ValueError(f"Array-pair polygon should have exactly 4 points, got {len(x)}")

        # Make sure the coordinates match where they should
        if x[0] != x[3]:
            raise ValueError(f"Array-pair polygon has conflicting left coordinates")
        if x[1] != x[2]:
            raise ValueError(f"Array-pair polygon has conflicting right coordinates")
        if y[0] != y[1]:
            raise ValueError(f"Array-pair polygon has conflicting top coordinates")
        if y[2] != y[3]:
            raise ValueError(f"Array-pair polygon has conflicting bottom coordinates")

        return BBox(
            left=x[0],
            right=x[1],
            top=y[0],
            bottom=y[2]
        )
