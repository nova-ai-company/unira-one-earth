"""UNIRA V8.7 — Level 2 (comfortable life, author's family-based definition, 2026-11-04): a reliable car and one
international holiday a year. What would they take, worldwide, and do they fit the ecological limits?

Approximate world figures (ASSUMPTION: rounded published orders of magnitude, to be verified against primary sources):
    cars in use about 1.5 bn; new cars produced about 90 m a year; international tourist arrivals about 1.3-1.4 bn a year.
Household: 2.5 people on average worldwide in 2050 (ASSUMPTION; 2 adults + 2 children is the author's example family).
Car options: one car per household owned; shared cars (one car per 3 households, as in car-sharing systems); electric.
Holiday options per person per year: 3,000 km return by air (abroad, far); 1,500 km by rail/coach (abroad, near);
every second year by air, otherwise by rail.
Energy intensities (ASSUMPTION, typical values): electric car about 0.6 MJ per vehicle-km (about 15 kWh per 100 km
at the plug plus losses), 10,000 km a year per household whatever the ownership (shared cars simply drive more); air about 1.8 MJ per passenger-km; rail/coach about 0.25 MJ per
passenger-km. Car life 15 years. Comfortable energy level: 40 GJ per person in all uses (Article 10c).
python3 level2.py  ->  ../outputs/level2.json"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
POP_2050 = 9.66e9           # UN WPP 2024 medium (v66)
HOUSEHOLD = 2.5             # ASSUMPTION
CARS_TODAY, CAR_PRODUCTION = 1.5e9, 90e6
TOURISM_TODAY = 1.4e9
EV_MJ_PER_KM, KM_PER_YEAR, LIFE = 0.6, 10_000, 15
AIR_MJ_PKM, RAIL_MJ_PKM = 1.8, 0.25
COMFORT_GJ = 40.0


def cars(per_household):
    fleet = POP_2050 / HOUSEHOLD * per_household
    energy_gj_pc = (POP_2050 / HOUSEHOLD) * EV_MJ_PER_KM * KM_PER_YEAR / 1000 / POP_2050  # same km per household in every option
    production = fleet / LIFE
    years_to_build = None
    for growth in (0.0, 0.03, 0.06):
        prod, stock, t = CAR_PRODUCTION, CARS_TODAY, 0
        while stock < fleet and t < 200:
            stock += prod - stock / LIFE
            prod *= 1 + growth
            t += 1
        years_to_build = years_to_build or {}
        years_to_build[f"production_growth_{int(growth * 100)}pct"] = t if stock >= fleet else None
    return {"fleet_bn": round(fleet / 1e9, 2), "vs_today": round(fleet / CARS_TODAY, 2),
            "new_cars_per_year_m": round(production / 1e6), "vs_today_production": round(production / CAR_PRODUCTION, 2),
            "energy_gj_per_person": round(energy_gj_pc, 2), "share_of_comfortable_energy": round(energy_gj_pc / COMFORT_GJ, 3),
            "years_to_reach_fleet": years_to_build}


def holidays(mode):
    if mode == "air_far":
        mj = 3000 * AIR_MJ_PKM
    elif mode == "rail_near":
        mj = 1500 * RAIL_MJ_PKM
    else:  # air every second year, rail otherwise
        mj = 0.5 * 3000 * AIR_MJ_PKM + 0.5 * 1500 * RAIL_MJ_PKM
    trips = POP_2050 * (0.5 if mode == "air_alternate" else 1.0)
    return {"energy_gj_per_person": round(mj / 1000, 2), "share_of_comfortable_energy": round(mj / 1000 / COMFORT_GJ, 3),
            "international_trips_bn_per_year": round(POP_2050 / 1e9, 1), "vs_today_tourism": round(POP_2050 / TOURISM_TODAY, 1),
            "air_trips_bn": round(trips / 1e9, 1) if mode != "rail_near" else 0.0}


def main():
    out = {"assumptions": {"pop_2050": POP_2050, "household": HOUSEHOLD, "cars_today": CARS_TODAY, "car_production": CAR_PRODUCTION,
                           "tourism_today": TOURISM_TODAY, "note": "rounded published orders of magnitude, to verify"},
           "cars": {"one_per_household_owned": cars(1.0), "shared_one_per_three_households": cars(1 / 3),
                    "one_per_two_households": cars(0.5)},
           "holidays": {m: holidays(m) for m in ("air_far", "rail_near", "air_alternate")}}
    for k, v in out["cars"].items():
        print(f"cars {k:34s} fleet {v['fleet_bn']} bn ({v['vs_today']}x today) | {v['new_cars_per_year_m']} m new/yr ({v['vs_today_production']}x today) | "
              f"{v['energy_gj_per_person']} GJ/person ({100 * v['share_of_comfortable_energy']:.0f}% of 40 GJ) | years to reach: {v['years_to_reach_fleet']}")
    for k, v in out["holidays"].items():
        print(f"holiday {k:14s} {v['energy_gj_per_person']} GJ/person ({100 * v['share_of_comfortable_energy']:.0f}% of 40 GJ) | "
              f"{v['international_trips_bn_per_year']} bn trips/yr = {v['vs_today_tourism']}x today's international tourism")
    (HERE.parent / "outputs" / "level2.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
