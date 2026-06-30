"""Routing engine: assign deliveries to vehicles and sequence each route.

Pipeline:
1. **Sweep assignment** — sort stops by polar angle around the depot and fill
   each vehicle up to capacity (a classic VRP heuristic that yields compact,
   pie-slice clusters).
2. **Sequencing** — nearest-neighbour seed + **2-opt** improvement per vehicle.
3. **Scheduling** — walk the route from the depot start time computing arrival,
   waiting (if early) and whether each stop meets its time window.
"""

from __future__ import annotations

import math

from logistics.core import Delivery, Depot, Route, Stop, Vehicle
from logistics.geo import Coord, haversine_km, path_distance


def _angle(depot: Depot, d: Delivery) -> float:
    return math.atan2(d.lat - depot.lat, d.lon - depot.lon)


def sweep_assign(
    deliveries: list[Delivery], vehicles: list[Vehicle], depot: Depot
) -> tuple[dict[str, list[Delivery]], list[Delivery]]:
    """Assign deliveries to vehicles by angular sweep, respecting capacity."""
    ordered = sorted(deliveries, key=lambda d: _angle(depot, d))
    assignment: dict[str, list[Delivery]] = {v.id: [] for v in vehicles}
    unassigned: list[Delivery] = []
    idx = 0
    load = 0.0
    for d in ordered:
        placed = False
        while idx < len(vehicles):
            vehicle = vehicles[idx]
            if load + d.volume <= vehicle.capacity:
                assignment[vehicle.id].append(d)
                load += d.volume
                placed = True
                break
            idx += 1
            load = 0.0
        if not placed:
            unassigned.append(d)
    return assignment, unassigned


def optimize_sequence(depot: Depot, deliveries: list[Delivery]) -> list[Delivery]:
    """Order stops to minimise travel: nearest-neighbour then 2-opt."""
    if len(deliveries) <= 1:
        return list(deliveries)

    remaining = list(deliveries)
    route: list[Delivery] = []
    current: Coord = (depot.lat, depot.lon)
    while remaining:
        nxt = min(remaining, key=lambda d: haversine_km(current, (d.lat, d.lon)))
        route.append(nxt)
        remaining.remove(nxt)
        current = (nxt.lat, nxt.lon)
    return _two_opt(depot, route)


def _two_opt(depot: Depot, route: list[Delivery]) -> list[Delivery]:
    def length(seq: list[Delivery]) -> float:
        points: list[Coord] = [(depot.lat, depot.lon)] + [(d.lat, d.lon) for d in seq]
        return path_distance(points)

    best = route
    best_len = length(best)
    improved = True
    while improved:
        improved = False
        for i in range(len(best) - 1):
            for j in range(i + 1, len(best)):
                candidate = best[:i] + best[i : j + 1][::-1] + best[j + 1 :]
                cand_len = length(candidate)
                if cand_len < best_len - 1e-9:
                    best, best_len = candidate, cand_len
                    improved = True
    return best


def compute_route(vehicle: Vehicle, depot: Depot, ordered: list[Delivery]) -> Route:
    """Schedule an ordered list of deliveries into a timed :class:`Route`."""
    minute = float(depot.start_min)
    position: Coord = (depot.lat, depot.lon)
    stops: list[Stop] = []
    for d in ordered:
        leg = haversine_km(position, (d.lat, d.lon))
        arrival = minute + (leg / vehicle.speed_kmh) * 60.0
        on_time = arrival <= d.window_end
        service_start = max(arrival, float(d.window_start))
        departure = service_start + vehicle.service_min
        stops.append(Stop(d, arrival, departure, on_time, leg))
        minute = departure
        position = (d.lat, d.lon)
    return Route(vehicle=vehicle, depot=depot, stops=stops)


def plan(
    deliveries: list[Delivery], vehicles: list[Vehicle], depot: Depot
) -> tuple[list[Route], list[Delivery]]:
    """Full plan: assignment + sequencing + scheduling for every vehicle."""
    assignment, unassigned = sweep_assign(deliveries, vehicles, depot)
    routes = [
        compute_route(vehicle, depot, optimize_sequence(depot, assignment[vehicle.id]))
        for vehicle in vehicles
    ]
    return routes, unassigned


def summarize(routes: list[Route], unassigned: list[Delivery]) -> dict[str, float]:
    """Aggregate KPIs across all routes."""
    total_stops = sum(len(r.stops) for r in routes)
    on_time = sum(r.on_time_count for r in routes)
    total_km = sum(r.total_km for r in routes)
    used = sum(1 for r in routes if r.stops)
    return {
        "deliveries": total_stops,
        "on_time": on_time,
        "on_time_pct": (on_time / total_stops) if total_stops else 0.0,
        "total_km": total_km,
        "vehicles_used": used,
        "unassigned": len(unassigned),
    }
