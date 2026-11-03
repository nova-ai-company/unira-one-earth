"""UNIRA V6.3 flows: empirical year-1 take-up rates for the V6.2 labour-reserve pools.

Public interface (see README.md):
    takeup.api.load_takeup(csv_path=None) -> list[dict]
    takeup.api.get_takeup(geo, year, pool, role="proposed", csv_path=None) -> float | None
"""
