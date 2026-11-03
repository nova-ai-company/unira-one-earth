"""UNIRA V6.4b lifecycle simulation with the money cap: python3 run_lifecycle.py"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / "src"), str(ROOT.parent / "v62" / "src")]
from unira_circuit import lifecycle  # noqa: E402
from unira_v62 import jsonstat  # noqa: E402


def sim_config(cfg, productivity, cap_enabled=True, variant=None):
    lc = cfg["lifecycle"]
    pop = {c["age"]: v for c, v, _ in jsonstat.iter_cells(jsonstat.load(ROOT / "data" / "raw" / "population_age_fr.json"))}
    weights = [(int(k[1:]), v) for k, v in pop.items() if k[1:].isdigit() and int(k[1:]) >= 20]
    mults = cfg["multiplier_by_isco"]["values"]
    isco = {c["isco08"]: v for c, v, _ in jsonstat.iter_cells(jsonstat.load(ROOT / "data" / "raw" / "employment_isco_fr.json"))}
    keys = [k for k in mults if k in isco]
    return {"sample_size": lc["sample_size"], "years": lc["years"], "age_weights": weights,
            "employment_rate": lc["employment_rate"], "unable_share": lc["unable_share"],
            "mult_values": [min(mults[k], cfg["multiplier_cap"]["value"]) for k in keys],
            "mult_weights": [isco[k] for k in keys], "saving_range": lc["saving_range"]["value"],
            "base_salary": cfg["base_salary_u_month"]["value"], "retiree_basket_month": lc["retiree_basket_month"],
            "rent_month": lc["rent_month"], "disability_month": lc["disability_month"],
            "home_price": lc["home_price"], "initial_owner_share": lc["initial_owner_share"]["value"],
            "new_homes_per_person_year": lc["new_homes_per_adult_year"]["value"],
            "credit_repay_share": lc["credit_repay_share"]["value"], "credit_max_years": lc["credit_max_years"]["value"],
            "cap_coef_initial": lc["cap_coef_initial"]["value"] if cap_enabled else 1e9,
            "deposit_target_months": lc["deposit_target_months"]["value"] if cap_enabled else 1e9,
            "cap_adjust_speed": lc["cap_adjust_speed"]["value"] if cap_enabled else 0.0,
            "gompertz_a": lc["gompertz"]["a"], "gompertz_b": lc["gompertz"]["b"],
            "productivity_growth": productivity, "weekly_hours": lc["weekly_hours"],
            **(lc["variants"][variant] if variant else {})}


def main():
    cfg = json.loads((ROOT / "config" / "circuit_config.json").read_text())
    rows = []
    for variant in cfg["lifecycle"]["variants"]:
        for seed in cfg["lifecycle"]["seeds"]:
            for r in lifecycle.simulate(sim_config(cfg, 0.0, True, variant), seed):
                rows.append({"money_cap": variant, "productivity_growth": 0.0, "seed": seed, **r})
    for cap in (True, False):
        for g in cfg["lifecycle"]["productivity_growth"]["values"]:
            for seed in cfg["lifecycle"]["seeds"]:
                for r in lifecycle.simulate(sim_config(cfg, g, cap), seed):
                    rows.append({"money_cap": cap, "productivity_growth": g, "seed": seed, **r})
    out = ROOT / "outputs" / "lifecycle.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows({k: round(v, 6) if isinstance(v, float) else v for k, v in r.items()} for r in rows)
    summ = {}
    for cap in [True, False] + list(cfg["lifecycle"]["variants"]):
        for g in (cfg["lifecycle"]["productivity_growth"]["values"] if cap in (True, False) else [0.0]):
            for yr in (10, 30, 60):
                sel = [r for r in rows if r["money_cap"] == cap and r["productivity_growth"] == g and r["year"] == yr]
                avg = {k: sum(r[k] for r in sel) / len(sel) for k in ("deposits_months_of_consumption", "cap_years_of_base_salary",
                       "share_at_cap", "ownership_rate", "second_home_rate", "mean_wait_renters_years", "weekly_hours",
                       "excess_demand_share")}
                avg["one_earth_inflow_share_of_consumption"] = sum((r["to_one_earth_cap"] + r["to_one_earth_inheritance"]) / r["consumption"] for r in sel) / len(sel)
                summ[f"cap={cap}|g={g}|year={yr}"] = avg
    (ROOT / "outputs" / "lifecycle_summary.json").write_text(json.dumps(summ, indent=2))
    for k, v in summ.items():
        print(k, {a: round(b, 3) for a, b in v.items()})


if __name__ == "__main__":
    main()
