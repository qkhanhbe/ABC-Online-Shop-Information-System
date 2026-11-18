from __future__ import annotations

from .product import Product


class Watch(Product):

    def __init__(self, movement: str | None = None, strap: str | None = None, water_resistance_m: int | None = None, battery_days: int | None = None) -> None:
        super().__init__()
        self.movement: str | None = movement
        self.strap: str | None = strap
        self.water_resistance_m: int | None = water_resistance_m
        self.battery_days: int | None = battery_days
