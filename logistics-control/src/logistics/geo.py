"""Geographic helpers (great-circle distance)."""

from __future__ import annotations

import math

_EARTH_RADIUS_KM = 6371.0088

Coord = tuple[float, float]  # (lat, lon)


def haversine_km(a: Coord, b: Coord) -> float:
    """Great-circle distance in kilometres between two ``(lat, lon)`` points."""
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * _EARTH_RADIUS_KM * math.asin(math.sqrt(h))


def path_distance(points: list[Coord]) -> float:
    """Total length of an open path visiting ``points`` in order."""
    return sum(haversine_km(points[i], points[i + 1]) for i in range(len(points) - 1))
