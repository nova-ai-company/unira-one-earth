"""UNIRA V8.2 (point 4) — the world money model under the author's choice C (2026-11-04):
needs are guaranteed in kind everywhere from year 1; each region's salary scale in U starts at its real production
level and rises to the full scale (5,000-25,000 U, fixed prices) within 20 years.

Regions = countries (World Bank). Full scale = what UNIRA salaries buy, set from France (v64): household consumption
per person equal to France's. Starting salary factor f_r = region's consumption per person / full level (max 1).
Schedule: f_r rises linearly to 1 by year 20.
Supply: a region's goods per person grow at its catch-up rate (scenarios); population follows UN/World Bank
projections to 2050. Demand: f_r x full level per person. Each year:
    regional gap = demand - own supply  (filled by the One Earth Fund: goods sent from regions with a surplus)
    world gap    = world demand - world supply  (cannot be filled by anyone -> shortages, empty shelves)
The capacity rule tested: f_r may not rise faster than the goods available to the region (own supply plus its share
of world surplus), so the world gap is never positive; then the year of full convergence is measured.
python3 model.py  ->  outputs/worldmoney.json"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
YEARS = 20
RICH_GROWTH = 0.01       # SYNTHETIC: yearly growth of goods per person in regions already at the full level
SCENARIOS = {"historical_catch_up": 0.02, "strong_catch_up": 0.04, "very_strong_catch_up": 0.06}  # extra yearly
#   growth for regions below the full level, falling as they approach it (SYNTHETIC; China sustained about 8%)


def wb(code, folder="v74/distribution/data/raw"):
    out = {}
    for x in json.loads((U / folder / f"wb_{code}.json").read_text())[1]:
        if x["value"] is not None and x["countryiso3code"]:
            out.setdefault(x["countryiso3code"], {})[int(x["date"])] = x["value"]
    return out


def regions(year=2023):
    c, p = wb("NE.CON.PRVT.PP.KD"), wb("SP.POP.TOTL")
    p50 = {}
    for x in json.loads((U / "v66" / "data" / "raw" / "wb40_SP.POP.TOTL_2050.json").read_text())[1]:
        if x["value"] is not None and x["countryiso3code"]:
            p50.setdefault(x["countryiso3code"], {})[int(x["date"])] = x["value"]
    meta = {m["id"]: m for m in json.loads((U / "v65" / "data" / "raw" / "wb_country_meta.json").read_text())[1]}
    out = {}
    for k in c:
        if k in meta and meta[k]["region"]["value"].strip() != "Aggregates" and year in c[k] and year in p.get(k, {}):
            pop2050 = p50.get(k, {}).get(2050, p[k][year])
            out[k] = {"pop": p[k][year], "pop2050": pop2050, "cons_pc": c[k][year] / p[k][year]}
    return out


def run(reg, extra, capacity_rule, years=YEARS):
    full = reg["FRA"]["cons_pc"]
    st = {k: {"supply_pc": r["cons_pc"], "f0": min(1.0, r["cons_pc"] / full), "f": min(1.0, r["cons_pc"] / full)} for k, r in reg.items()}
    rows = []
    for t in range(years + 1):
        pop = {k: r["pop"] + (r["pop2050"] - r["pop"]) * min(1.0, t / 27) for k, r in reg.items()}
        for k, s in st.items():
            sched = s["f0"] + (1 - s["f0"]) * min(1.0, t / YEARS)
            s["f"] = sched if not capacity_rule else s["f"]  # capacity rule: set below, after supply is known
        supply = {k: st[k]["supply_pc"] * pop[k] for k in st}
        world_supply = sum(supply.values())
        if capacity_rule:
            # scale every region's scheduled factor by one world ratio so world demand never exceeds world supply
            sched = {k: st[k]["f0"] + (1 - st[k]["f0"]) * min(1.0, t / YEARS) for k in st}
            lo, hi = 0.0, 1.0  # largest common ratio such that world demand <= world supply (floors included)
            for _ in range(50):
                mid = (lo + hi) / 2
                need = sum(max(st[k]["f0"], min(1.0, sched[k] * mid)) * full * pop[k] for k in st)
                lo, hi = (mid, hi) if need <= world_supply else (lo, mid)
            for k in st:
                st[k]["f"] = max(st[k]["f0"], min(1.0, sched[k] * lo))
        demand = {k: st[k]["f"] * full * pop[k] for k in st}
        world_demand = sum(demand.values())
        transfers = sum(max(0.0, demand[k] - supply[k]) for k in st)
        rows.append({"year": t, "world_supply_vs_demand": world_supply / world_demand,
                     "world_shortage_share": max(0.0, 1 - world_supply / world_demand),
                     "fund_transfers_share_of_world_supply": transfers / world_supply,
                     "people_at_full_scale_share": sum(pop[k] for k in st if st[k]["f"] >= 0.999) / sum(pop.values()),
                     "mean_salary_factor_pop_weighted": sum(st[k]["f"] * pop[k] for k in st) / sum(pop.values())})
        # goods per person grow for next year: catch-up regions faster, slowing as they approach the full level
        for k, s in st.items():
            gap = max(0.0, math.log(full / s["supply_pc"])) if s["supply_pc"] < full else 0.0
            g = RICH_GROWTH + extra * min(1.0, gap)
            s["supply_pc"] *= 1 + g
    return rows


def main():
    reg = regions()
    full = reg["FRA"]["cons_pc"]
    out = {"regions": len(reg), "full_level_cons_pc_ppp": round(full),
           "world_cons_pc_ppp_2023": round(sum(r["cons_pc"] * r["pop"] for r in reg.values()) / sum(r["pop"] for r in reg.values())),
           "start_mean_salary_factor": round(sum(min(1, r["cons_pc"] / full) * r["pop"] for r in reg.values()) / sum(r["pop"] for r in reg.values()), 3),
           "scenarios": {}}
    print({k: v for k, v in out.items() if k != "scenarios"})
    for name, extra in SCENARIOS.items():
        for rule in (False, True):
            rows = run(reg, extra, rule, 50 if rule else YEARS)
            key = f"{name}/{'capacity_rule' if rule else 'fixed_20y_schedule'}"
            full_year = next((r["year"] for r in rows if r["mean_salary_factor_pop_weighted"] >= 0.99), None)
            out["scenarios"][key] = {"year_10": rows[10], "year_20": rows[20], "max_world_shortage": max(r["world_shortage_share"] for r in rows),
                                     "year_all_at_full_scale": full_year, "path": rows}
            r20 = rows[20]
            print(f"full scale (mean factor 0.99) reached in year {full_year}")
            print(f"{key:44s} yr20: supply/demand {r20['world_supply_vs_demand']:.2f} | shortage {100 * r20['world_shortage_share']:.0f}% | "
                  f"Fund transfers {100 * r20['fund_transfers_share_of_world_supply']:.0f}% of world supply | mean salary factor "
                  f"{r20['mean_salary_factor_pop_weighted']:.2f} | at full scale {100 * r20['people_at_full_scale_share']:.0f}%")
    (HERE / "outputs").mkdir(exist_ok=True)
    (HERE / "outputs" / "worldmoney.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
