from typing import Dict, List


def check_array_pair_polygon(app: Dict[str, List[int]]):
    """
    Checks that an array-pair polygon is properly formed.

    :param app:
                The object to check.
    """
    # Must be a dict
    if not isinstance(app, dict):
        raise TypeError(f"Array-pair polygon is not a dict, got {app.__class__.__name__}")

    # Must have 'x' and 'y' keys
    if "x" not in app:
        raise ValueError(f"Array-pair polygon must have an 'x' key")
    if "y" not in app:
        raise ValueError(f"Array-pair polygon must have an 'y' key")

    # Extract 'x and 'y'
    x = app['x']
    y = app['y']

    # 'x' and 'y' must be lists
    if not isinstance(x, list):
        raise TypeError(f"Array-pair polygon's 'x' is not a list")
    if not isinstance(y, list):
        raise TypeError(f"Array-pair polygon's 'y' is not a list")

    # 'x' and 'y' must be the same length
    if len(x) != len(y):
        raise ValueError(f"Array-pair polygon has differing-length lists ({len(x)} vs. {len(y)})")

    # All coordinates must be integers
    if any(not isinstance(coord, int) for coord in x):
        raise TypeError(f"Array-pair polygon contains non-integer coordinates in 'x'")
    if any(not isinstance(coord, int) for coord in y):
        raise TypeError(f"Array-pair polygon contains non-integer coordinates in 'y'")

