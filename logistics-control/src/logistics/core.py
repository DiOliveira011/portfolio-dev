"""Domain models for delivery routing.

Times are stored as **minutes since midnight** (ints) inside the engine and only
formatted to ``HH:MM`` for display.
"""

from __future__ import annotations

from dataclasses import dataclass, field


def hhmm_to_minutes(value: str) -> int:
    """Parse ``"HH:MM"`` into minutes since midnight."""
    hours, minutes = value.strip().split(":")
    return int(hours) * 60 + int(minutes)


def minutes_to_hhmm(minutes: float) -> str:
    """Format minutes since midnight as ``"HH:MM"`` (wraps at 24h defensively)."""
    total = int(round(minutes)) % (24 * 60)
    return f"{total // 60:02d}:{total % 60:02d}"


@dataclass(slots=True)
class Driver:
    """A driver that can be assigned to a vehicle."""

    id: str
    name: str
    phone: str = ""


@dataclass(slots=True)
class Delivery:
    """A stop at a client company: a delivery (drop-off) or a pickup/return.

    ``label`` is the client/company name. ``items`` is the romaneio (which goods
    go to this stop). ``receiver`` (the *conferente*) and ``status`` are filled
    as the route is executed.
    """

    id: str
    label: str
    lat: float
    lon: float
    volume: float                 # how much vehicle capacity it consumes
    window_start: int             # minutes since midnight
    window_end: int
    kind: str = "entrega"         # "entrega" | "retirada"
    items: list[str] = field(default_factory=list)   # merchandise / romaneio
    receiver: str | None = None   # conferente (quem recebeu)
    status: str = "pendente"      # "pendente" | "entregue" | "recusado"


@dataclass(slots=True)
class Vehicle:
    """A vehicle in the fleet."""

    id: str
    name: str
    capacity: float
    speed_kmh: float = 30.0
    service_min: float = 15.0     # time spent at each stop
    km_per_liter: float = 3.5     # fuel economy (km/L)
    plate: str = ""
    driver_id: str | None = None


@dataclass(slots=True)
class Depot:
    """Where vehicles start the day."""

    lat: float
    lon: float
    name: str = "Base"
    start_min: int = 8 * 60       # 08:00


@dataclass(slots=True)
class Stop:
    """A scheduled visit within a route."""

    delivery: Delivery
    arrival_min: float
    departure_min: float
    on_time: bool
    leg_km: float


@dataclass(slots=True)
class Route:
    """A vehicle's ordered set of stops."""

    vehicle: Vehicle
    depot: Depot
    stops: list[Stop] = field(default_factory=list)

    @property
    def total_km(self) -> float:
        return sum(stop.leg_km for stop in self.stops)

    @property
    def load(self) -> float:
        return sum(stop.delivery.volume for stop in self.stops)

    @property
    def on_time_count(self) -> int:
        return sum(1 for stop in self.stops if stop.on_time)

    @property
    def utilization(self) -> float:
        return self.load / self.vehicle.capacity if self.vehicle.capacity else 0.0

    @property
    def fuel_liters(self) -> float:
        kmpl = self.vehicle.km_per_liter
        return self.total_km / kmpl if kmpl > 0 else 0.0

    def fuel_cost(self, price_per_liter: float) -> float:
        return self.fuel_liters * price_per_liter
