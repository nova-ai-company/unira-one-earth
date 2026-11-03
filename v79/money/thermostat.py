"""UNIRA V7.9 — the money-cap thermostat under shocks (design 4).

Rule tested (proposed Article 17 amendment):
    each year  cap <- cap x (target deposits / actual deposits)^0.5, limited to +/-10% a year,
    never below 1 year of base salary; target = 12 months of the region's consumption.
The v64 lifecycle model (6,000 people, 60 years, French age/occupation structure) is run with:
    calm             no shock
    disaster         year 40: households spend 30% of their savings on rebuilding
    fear             year 40: everyone saves 15 points more of their income for 3 years (max 50%)
    baby_boom        year 40: an extra cohort of young adults equal to 15% of the population
    automation       productivity +2% a year (hours fall instead of prices)
Shocks hit at year 40, after the cap has phased in from its initial 10 years of salary; stability is measured from year 30.
each with the +/-10% limit (proposed) and without it (v64 rule), 3 seeds.
python3 thermostat.py  ->  ../outputs/thermostat.json"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
spec = importlib.util.spec_from_file_location("run_lifecycle", U / "v64" / "run_lifecycle.py")
rl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rl)

SHOCK_YEAR, STEADY_FROM, SEEDS, LIMIT = 40, 30, (1, 2, 3), 0.10
SCENARIOS = {"calm": ([], 0.0),
             "disaster": ([{"year": SHOCK_YEAR, "type": "disaster", "size": 0.30}], 0.0),
             "fear": ([{"year": SHOCK_YEAR, "type": "fear", "size": 0.15, "years": 3}], 0.0),
             "baby_boom": ([{"year": SHOCK_YEAR, "type": "baby_boom", "size": 0.15}], 0.0),
             "automation": ([], 0.02)}


def metrics(rows, target):
    after = [r for r in rows if r["year"] >= STEADY_FROM]  # after the phase-in from the initial cap of 10 years
    caps = [r["cap_u"] for r in rows]
    changes = [abs(b / a - 1) for a, b in zip(caps, caps[1:])]
    post = [r for r in rows if r["year"] >= SHOCK_YEAR]
    back = next((r["year"] - SHOCK_YEAR for r in post[1:] if abs(r["deposits_months_of_consumption"] - target) <= 2), None)
    return {"deposits_months_min": min(r["deposits_months_of_consumption"] for r in after),
            "deposits_months_max": max(r["deposits_months_of_consumption"] for r in after),
            "deposits_months_final": rows[-1]["deposits_months_of_consumption"],
            "max_yearly_cap_change_pct": 100 * max(changes),
            "cap_years_final": rows[-1]["cap_years_of_base_salary"],
            "share_at_cap_mean": sum(r["share_at_cap"] for r in after) / len(after),
            "first_homes_blocked_by_cap": sum(r["first_homes_blocked_by_cap"] for r in rows),
            "phase_in_years_to_target_band": next((r["year"] for r in rows if abs(r["deposits_months_of_consumption"] - target) <= 2), None),
            "years_back_within_2_months_of_target": back,
            "weekly_hours_final": rows[-1]["weekly_hours"]}


def main():
    cfg = json.loads((U / "v64" / "config" / "circuit_config.json").read_text())
    res = {"rule": {"adjust_speed": cfg["lifecycle"]["cap_adjust_speed"]["value"], "limit_per_year": LIMIT,
                    "floor_years_of_base_salary": 1.0, "target_months": cfg["lifecycle"]["deposit_target_months"]["value"]},
           "results": {}}
    target = res["rule"]["target_months"]
    for name, (shocks, prod) in SCENARIOS.items():
        for rule, lim in (("limited_10pct", LIMIT), ("unlimited_v64", None)):
            runs = []
            for seed in SEEDS:
                c = rl.sim_config(cfg, prod, True, "cap_low_credit")
                c["shocks"] = shocks
                if lim:
                    c["cap_max_change"] = lim
                runs.append(metrics(rl.lifecycle.simulate(c, seed), target))
            avg = {k: (sum(r[k] for r in runs) / len(runs) if all(r[k] is not None for r in runs) else None) for k in runs[0]}
            avg["max_yearly_cap_change_pct"] = max(r["max_yearly_cap_change_pct"] for r in runs)
            avg["first_homes_blocked_by_cap"] = sum(r["first_homes_blocked_by_cap"] for r in runs)
            res["results"][f"{name}/{rule}"] = avg
            print(f"{name:11s} {rule:14s} deposits {avg['deposits_months_min']:.1f}-{avg['deposits_months_max']:.1f} months "
                  f"(final {avg['deposits_months_final']:.1f}) | max cap change {avg['max_yearly_cap_change_pct']:.0f}%/yr | "
                  f"cap {avg['cap_years_final']:.2f} yrs | at cap {100 * avg['share_at_cap_mean']:.0f}% | "
                  f"back in band after {avg['years_back_within_2_months_of_target']} yrs | phase-in {avg['phase_in_years_to_target_band']} yrs | blocked {avg['first_homes_blocked_by_cap']}")
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "thermostat.json").write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
