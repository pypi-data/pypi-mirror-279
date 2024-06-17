"""
Helper to define methods for converting to and from geojson data

methods:
    - lat_lon_to_geojson_point
"""

from typing import Any


def lat_lon_to_geojson_point(latitude: Any, longitude: Any, operator=None, digits=5):
    """
    converts latt and long to a geojson dict.

    args:
        - latitude (float)      lattitude
        - longitude (float)     longitude
        - operator (str, optional)
            indicator for running an opteration on the lattitude / longitude
            before coverting it to a point field. Allowed operations:
                - divide_1234 -> divides the lat and lon value by 1234
        - digits (int, defaults to 5)
            nr of digits to be used in lat, lon coodinates


    returns
        dict
            geojson as dict
        None
            if no a proper geojson can be formed
    """
    try:
        lon = float(longitude)
        lat = float(latitude)
    except (ValueError, TypeError):
        return None

    if operator:
        lon = _operate(lon, operator)
        lat = _operate(lat, operator)

    return {
        "type": "Point",
        "coordinates": [round(float(lon), digits), round(float(lat), digits)],
    }


def _operate(value: float, operator: str) -> float:
    """
    runs a operation on a given value.

    args:
        - value     Value on which the operation must be done
        - operator (str)
            string indiciting operation to be done. Possible values
                - divide_XYZ -> divide value by XYZ
    """
    if operator.split("_")[0] == "divide":
        return float(value) / (int(operator.split("_")[1]))
    raise ValueError(f"Unkown operator {operator}")
