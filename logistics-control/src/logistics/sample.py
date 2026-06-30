"""Synthetic sample scenario: a São Paulo delivery day for an events operation."""

from __future__ import annotations

import random

from logistics.core import Delivery, Depot, Driver, Vehicle, hhmm_to_minutes

# Depot near the centre of São Paulo.
SAMPLE_DEPOT = Depot(lat=-23.5505, lon=-46.6333, name="Base SP (Centro)", start_min=8 * 60)

_MERCHANDISE = [
    "Mesas (10)", "Cadeiras (40)", "Toalhas (20)", "Talheres", "Pratos (100)",
    "Taças (80)", "Tendas (2)", "Som", "Iluminação", "Buffet térmico",
    "Réchauds", "Toalhas de mesa", "Sousplat", "Bowls de vidro",
]

# (label/cliente, lat, lon, volume, window_start, window_end, kind)
_POINTS: list[tuple[str, float, float, float, str, str, str]] = [
    ("Buffet Jardins", -23.5670, -46.6680, 6, "09:00", "11:00", "entrega"),
    ("Salão Pinheiros", -23.5640, -46.7020, 4, "09:30", "12:00", "entrega"),
    ("Espaço Vila Mariana", -23.5890, -46.6340, 5, "10:00", "12:30", "entrega"),
    ("Hotel Paulista", -23.5610, -46.6560, 3, "08:30", "10:30", "entrega"),
    ("Centro de Eventos Norte", -23.5050, -46.6280, 7, "10:00", "13:00", "entrega"),
    ("Chácara Cotia", -23.6040, -46.9190, 8, "11:00", "15:00", "entrega"),
    ("Casa Tatuapé", -23.5400, -46.5760, 4, "13:00", "16:00", "entrega"),
    ("Buffet Santana", -23.5020, -46.6250, 5, "13:30", "17:00", "entrega"),
    ("Salão Moema", -23.6010, -46.6650, 3, "14:00", "17:30", "entrega"),
    ("Espaço Lapa", -23.5280, -46.7050, 6, "09:00", "12:00", "entrega"),
    ("Retirada Morumbi", -23.6230, -46.6990, 5, "15:00", "18:00", "retirada"),
    ("Retirada Itaim", -23.5840, -46.6770, 4, "15:30", "18:30", "retirada"),
    ("Buffet ABC (Sto André)", -23.6630, -46.5380, 9, "11:00", "15:00", "entrega"),
    ("Casa Perdizes", -23.5370, -46.6770, 3, "08:30", "11:00", "entrega"),
]


def sample_drivers() -> list[Driver]:
    return [
        Driver(id="M1", name="Carlos Souza", phone="(11) 98888-1010"),
        Driver(id="M2", name="João Pereira", phone="(11) 97777-2020"),
        Driver(id="M3", name="Marcos Lima", phone="(11) 96666-3030"),
    ]


def sample_vehicles() -> list[Vehicle]:
    return [
        Vehicle(id="V1", name="Caminhão 1", capacity=22, speed_kmh=28,
                service_min=15, km_per_liter=3.2, plate="ABC-1A23", driver_id="M1"),
        Vehicle(id="V2", name="Caminhão 2", capacity=22, speed_kmh=28,
                service_min=15, km_per_liter=3.4, plate="DEF-4B56", driver_id="M2"),
        Vehicle(id="V3", name="Van", capacity=14, speed_kmh=32,
                service_min=10, km_per_liter=7.5, plate="GHI-7C89", driver_id="M3"),
    ]


def sample_deliveries() -> list[Delivery]:
    rng = random.Random(7)
    deliveries: list[Delivery] = []
    for i, (label, lat, lon, vol, ws, we, kind) in enumerate(_POINTS):
        items = rng.sample(_MERCHANDISE, k=rng.randint(2, 4))
        deliveries.append(
            Delivery(
                id=f"D{i + 1:02d}", label=label, lat=lat, lon=lon, volume=vol,
                window_start=hhmm_to_minutes(ws), window_end=hhmm_to_minutes(we),
                kind=kind, items=items,
            )
        )
    return deliveries


def sample_depot() -> Depot:
    return SAMPLE_DEPOT
