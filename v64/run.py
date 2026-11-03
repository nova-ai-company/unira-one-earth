"""UNIRA V6.4 money circuit (France region pilot): python3 run.py [--fetch]."""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UNIRA = ROOT.parent
sys.path[:0] = [str(ROOT / "src"), str(UNIRA / "v62" / "src"), str(UNIRA / "v63" / "io" / "src"),
                str(UNIRA / "v63" / "io")]

from unira_circuit import fetch, model  # noqa: E402
from unira_v62 import jsonstat  # noqa: E402

RAW, OUT = ROOT / "data" / "raw", ROOT / "outputs"


def cells(stem):
    return list(jsonstat.iter_cells(jsonstat.load(RAW / f"{stem}.json")))


def physical_inputs():
    """Household goods supply and residential construction, in hour-equivalents (v63/io, 2022)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("v63_io_run", UNIRA / "v63" / "io" / "run.py")
    iorun = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(iorun)
    from unira_io import model as iomodel
    c, h = iorun.load()
    io = iomodel.IOSystem(c, h, 2022)
    hh_dom = io.embodied(io.F["household_consumption"])
    hh_imp = io.embodied(io.F_imp["household_consumption"])
    f = io.products.index("CPA_F")
    gfcf_f = io.m[f] * io.F["gross_fixed_capital_formation"][f]
    return {"household_supply_h": (hh_dom + hh_imp) * 1e3, "household_dom_h": hh_dom * 1e3,
            "household_imp_h": hh_imp * 1e3, "construction_gfcf_h": gfcf_f * 1e3}


def build_inputs(cfg):
    pop = {c["age"]: v for c, v, _ in cells("population_age_fr")}
    groups = model.population_groups(pop)
    isco = {c["isco08"]: v for c, v, _ in cells("employment_isco_fr")}
    dist = model.wage_distribution(isco, cfg["multiplier_by_isco"]["values"], cfg["multiplier_cap"]["value"])
    hh = {(c["phhcomp"], c["n_child"]): v * 1e3 for c, v, _ in cells("households_children_fr")}
    ca = cfg["child_allowance"]
    nmap = {"1": 1, "2": 2, "GE3": ca["ge3_children_count"]}
    e = cfg["employment_rate_20_64"]["value"]
    base = cfg["base_salary_u_month"]["value"]
    cb = 0.0
    for comp, adults in (("CPL_CH", 2), ("A1_CH", 1)):
        for k, n in nmap.items():
            cb += hh.get((comp, k), 0.0) * model.expected_child_benefit(
                n, adults, dist, e, base, ca["per_child"], ca["household_threshold"])
    ten = {(c["hhcomp"], c["tenure"]): v for c, v, _ in cells("tenure_fr")}
    single_share = ten[("A1_GE65", "OWN")] + ten[("A1_GE65", "RENT")]           # % of population
    couple_share = ten[("A2_GE1_GE65", "OWN")] + ten[("A2_GE1_GE65", "RENT")]
    total_pop = pop["TOTAL"]
    singles = single_share / 100 * total_pop
    rest = max(0.0, groups["retired_65_plus"] - singles)
    renter = (ten[("A1_GE65", "RENT")] + ten[("A2_GE1_GE65", "RENT")]) / (single_share + couple_share)
    retirees = {"single_units": singles, "couple_units": rest / 2, "renter_share": renter,
                "note": "65+ not living alone are grouped in couple units (approximation)"}
    phys = physical_inputs()
    phys["residential_construction_h"] = phys["construction_gfcf_h"] * \
        cfg["housing"]["residential_share_of_construction_gfcf"]["value"]
    return {"groups": groups, "wage_dist": dist, "child_benefit_month": cb, "retirees": retirees,
            "households_total": hh.get(("TOTAL", "TOTAL")), **phys}


def main():
    if "--fetch" in sys.argv:
        fetch.fetch_all(RAW)
    if fetch.verify_manifest(RAW):
        raise SystemExit("raw snapshot hash mismatch")
    cfg = json.loads((ROOT / "config" / "circuit_config.json").read_text())
    inp = build_inputs(cfg)
    c = model.annual_circuit(inp, cfg)
    rows, cols = model.transaction_matrix(c)
    checks = [{"check": f"row_sums_zero:{k}", "passed": abs(sum(r.values())) < 1e-3} for k, r in rows.items()]
    checks.append({"check": "sector_net_lending_sums_zero", "passed": abs(sum(cols.values())) < 1e-3})
    checks.append({"check": "reg_balance_equals_minus_unspent_saving",
                   "passed": abs(c["reg_balance"] + c["unspent_saving"]) < 1e-3 * c["household_income"]})
    checks.append({"check": "base_year_no_excess_demand", "passed": abs(c["excess_demand_share"]) < 1e-12})
    base = cfg["base_salary_u_month"]["value"]
    hc = cfg["housing"]
    housing = []
    for m in (1.0, 1.5, round(c["mean_multiplier"], 2), 3.0, 5.0):
        for earners in (1, 2):
            housing.append({"multiplier": m, "earners": earners, **{
                f"years_to_buy_{p//1000}k": model.years_to_buy(p, base * m, cfg["saving_rate_adults_20_64"]["value"], earners)
                for p in (hc["price_range_u"][0], hc["average_price_u"], hc["price_range_u"][1])}})
    hours_per_avg_home = hc["average_price_u"] / c["pi_u_per_hour"]
    homes_per_year = inp["residential_construction_h"] / hours_per_avg_home
    dyn = [r for cr in cfg["dynamics"]["experience_creep_per_year"]["values"]
           for pg in cfg["dynamics"]["productivity_growth_per_year"]["values"]
           for r in model.dynamics(inp, cfg, cr, pg)]
    per_capita_today_h = inp["household_supply_h"] / sum(inp["groups"].values())
    base_basket_h = base * (1 - cfg["saving_rate_adults_20_64"]["value"]) * 12 / c["pi_u_per_hour"]
    summary = {"inputs": {k: v for k, v in inp.items() if k != "wage_dist"},
               "wage_distribution": {k: {"share": s, "multiplier": m} for k, (s, m) in inp["wage_dist"].items()},
               "circuit_base_year": c, "transaction_matrix": rows, "sector_net_lending": cols,
               "fixed_price": {"pi_u_per_hour_equivalent": c["pi_u_per_hour"],
                               "base_worker_basket_h_per_year": base_basket_h,
                               "average_person_consumption_today_h_per_year": per_capita_today_h,
                               "base_basket_vs_today_average_person": base_basket_h / per_capita_today_h},
               "housing": {"hours_per_average_home": hours_per_avg_home,
                           "new_or_renovated_homes_per_year_capacity": homes_per_year,
                           "years_to_buy": housing},
               "checks": checks}
    OUT.mkdir(exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    with (OUT / "dynamics.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(dyn[0]))
        w.writeheader()
        w.writerows({k: round(v, 6) if isinstance(v, float) else v for k, v in r.items()} for r in dyn)
    for ck in checks:
        print(("PASS " if ck["passed"] else "FAIL ") + ck["check"])
    if not all(ck["passed"] for ck in checks):
        raise SystemExit("checks failed")
    B = 1e9
    print(f"pop groups (m): " + ", ".join(f"{k}={v/1e6:.2f}" for k, v in inp["groups"].items()))
    print(f"workers {c['workers']/1e6:.2f}m, mean multiplier {c['mean_multiplier']:.2f}, unable {c['unable_to_work']/1e6:.2f}m")
    for k in ("wages", "disability_guarantees", "retiree_income", "child_allowances", "household_income", "saving",
              "consumption", "new_home_capacity_u", "new_home_spending", "unspent_saving", "enterprise_surplus",
              "reg_outflows", "reg_balance"):
        print(f"  {k:24s} {c[k]/B:10.1f} bn U/yr")
    print(json.dumps(summary["fixed_price"], indent=1))
    print("hours per avg home", round(hours_per_avg_home), "homes/yr capacity", round(homes_per_year))
    for h in housing:
        print(h)
    for r in dyn:
        if r["year"] in (10, 30):
            print(r)


if __name__ == "__main__":
    main()
