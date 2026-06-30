"""Fleet & driver analytics: fuel costs and km/fuel reports by period.

The day-to-day planning is in :mod:`logistics.routing`; here we cover the
**management** side the user asked for: driver km in the day/week/month and how
much fuel was spent — fed by a synthetic operation history (or a real one with
the same schema).
"""

from __future__ import annotations

import random
from datetime import date, timedelta

import pandas as pd

from logistics.core import Driver, Vehicle


def generate_history(
    drivers: list[Driver], vehicles: list[Vehicle], *, days: int = 30, seed: int = 11
) -> pd.DataFrame:
    """Synthetic past operation: one route per driver per working day.

    Schema: ``date, driver, driver_id, vehicle, km, deliveries, fuel_liters,
    fuel_cost``.
    """
    rng = random.Random(seed)
    vehicle_by_driver = {v.driver_id: v for v in vehicles if v.driver_id}
    today = date.today()
    rows: list[dict[str, object]] = []
    for offset in range(days):
        day = today - timedelta(days=offset)
        if day.weekday() == 6:  # skip Sundays
            continue
        for driver in drivers:
            vehicle = vehicle_by_driver.get(driver.id)
            kmpl = vehicle.km_per_liter if vehicle else 3.5
            km = round(rng.uniform(40, 180), 1)
            liters = round(km / kmpl, 1)
            price = rng.uniform(5.8, 6.4)
            rows.append({
                "date": day,
                "driver": driver.name,
                "driver_id": driver.id,
                "vehicle": vehicle.name if vehicle else "-",
                "km": km,
                "deliveries": rng.randint(5, 14),
                "fuel_liters": liters,
                "fuel_cost": round(liters * price, 2),
            })
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


def summarize_drivers(history: pd.DataFrame, *, reference: object | None = None) -> pd.DataFrame:
    """Per-driver km (day/week/month), fuel cost and deliveries for the month."""
    columns = ["driver_id", "driver", "km_dia", "km_semana", "km_mes",
               "combustivel_mes", "entregas_mes"]
    if history.empty:
        return pd.DataFrame(columns=columns)

    ref = pd.Timestamp(reference) if reference is not None else history["date"].max()
    start_week = ref - pd.Timedelta(days=int(ref.weekday()))
    start_month = ref.replace(day=1)
    last_day = history["date"].max()

    rows: list[dict[str, object]] = []
    for (driver_id, driver), group in history.groupby(["driver_id", "driver"]):
        rows.append({
            "driver_id": driver_id,
            "driver": driver,
            "km_dia": float(group.loc[group["date"] == last_day, "km"].sum()),
            "km_semana": float(group.loc[group["date"] >= start_week, "km"].sum()),
            "km_mes": float(group.loc[group["date"] >= start_month, "km"].sum()),
            "combustivel_mes": float(group.loc[group["date"] >= start_month, "fuel_cost"].sum()),
            "entregas_mes": int(group.loc[group["date"] >= start_month, "deliveries"].sum()),
        })
    report = pd.DataFrame(rows, columns=columns)
    return report.sort_values("km_mes", ascending=False).reset_index(drop=True)
