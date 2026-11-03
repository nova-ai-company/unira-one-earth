"""UNIRA V6.5: world sufficiency by domain under needs x population (python3 run.py)."""
import csv
import json
from pathlib import Path

import sufficiency as s

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "data" / "world_indicators.csv"


def load():
    v = {}
    names = {}
    for r in csv.DictReader(DATA.open()):
        if r["iso3"] == "WLD":
            continue
        v[(r["iso3"], r["indicator_id"])] = float(r["value"])
        names[r["iso3"]] = r["country"]
    return v, names


def rows_for(v, isos, fn):
    out = []
    for i in isos:
        pop = v.get((i, "pop_total"))
        try:
            sp = fn(i)
        except (KeyError, TypeError):
            sp = None
        out.append({"region": i, "population": pop, "supply_pc": sp})
    return out


def main():
    cfg = json.loads((ROOT / "config.json").read_text())
    v, names = load()
    isos = sorted({k[0] for k in v if k[1] == "pop_total"})
    res = {}
    # --- food (kcal/person/day supply; threshold = eaten / (1 - consumer waste))
    f = cfg["food"]
    food = rows_for(v, isos, lambda i: v[(i, "food_kcal_per_cap_day")])
    for lvl, eaten in (("decent", f["decent_eaten_kcal"]), ("comfortable", f["comfortable_eaten_kcal"])):
        for wname in ("consumer_waste_status_quo", "consumer_waste_unira"):
            tau = eaten / (1 - f[wname]["value"])
            res[f"food|{lvl}|{wname}"] = {"threshold": tau, **s.domain_summary(food, tau)}
    # --- energy (final GJ/person/yr from primary kWh)
    e = cfg["energy"]
    conv = e["primary_to_final"]["value"]
    energy = rows_for(v, isos, lambda i: v[(i, "energy_primary_kwh_per_cap")] * 0.0036 * conv)
    for lvl in ("decent", "comfortable", "eu_today"):
        tau = e[f"{lvl}_final_gj"]
        res[f"energy|{lvl}"] = {"threshold": tau, **s.domain_summary(energy, tau)}
    # --- health workers (doctors + nurses/midwives per 10k; non-tradable: people)
    h = cfg["health"]
    health = rows_for(v, isos, lambda i: v[(i, "doctors_per_10k")] + v[(i, "nurses_midwives_per_10k")])
    for lvl in ("decent", "comfortable"):
        tau = h[f"{lvl}_per_10k"]
        d = s.domain_summary(health, tau)
        d["shortfall_workers"] = d["shortfall_volume"] / 1e4
        d["world_workers"] = d["world_supply"] / 1e4
        d["extra_workers_for_all_at_threshold"] = max(0.0, d["world_need"] - d["world_supply"]) / 1e4
        res[f"health|{lvl}"] = {"threshold": tau, **d}
    # --- labour: current hours vs 30 h with universal work
    lab = cfg["labour"]
    cur_h = cur_emp = cov_emp = 0.0
    for i in isos:
        emp = v.get((i, "employment_15plus_thousands"))
        hrs = v.get((i, "hours_actual_weekly_per_employed"))
        if emp:
            cur_emp += emp * 1e3
            if hrs:
                cur_h += emp * 1e3 * hrs
                cov_emp += emp * 1e3
    mean_hours = cur_h / cov_emp
    wap = sum(v[(i, "pop_total")] * v[(i, "pop_share_15_64")] / 100 for i in isos
              if (i, "pop_share_15_64") in v and (i, "pop_total") in v)
    unira_emp = lab["employment_rate_15_64_unira"]["value"] * wap
    res["labour"] = {"employment_now": cur_emp, "mean_weekly_hours_now_hours_covered_countries": mean_hours,
                     "hours_coverage_share_of_employment": cov_emp / cur_emp,
                     "weekly_hours_now_world": cur_emp * mean_hours,
                     "working_age_15_64": wap, "unira_employment": unira_emp,
                     "weekly_hours_unira_30h": unira_emp * lab["weekly_cap"],
                     "unira_vs_now": unira_emp * lab["weekly_cap"] / (cur_emp * mean_hours)}
    # --- region changes under equal shares
    changes = {}
    for dom, rows, tau in (("food_kcal", food, None), ("energy_final_gj", energy, e["decent_final_gj"]),
                           ("health_per_10k", health, h["decent_per_10k"])):
        changes[dom] = [s.region_change(rows, r, tau) for r in cfg["regions_shown"]]
    out = {"domains": res, "region_changes_equal_share": changes,
           "names": {r: names.get(r) for r in cfg["regions_shown"]}}
    (ROOT.parent / "outputs").mkdir(exist_ok=True)
    (ROOT.parent / "outputs" / "world_sufficiency.json").write_text(json.dumps(out, indent=2))
    for k, d in res.items():
        if k == "labour":
            continue
        print(f"{k:45s} tau={d['threshold']:8.1f} R={d['sufficiency_ratio']:.2f} below={d['share_people_below']*100:5.1f}% "
              f"({d['people_below_threshold']/1e9:.2f}bn) equal_share/tau={d['equal_share_vs_threshold']:.2f} moved={d['share_of_supply_moved']*100:4.1f}%"
              + (f" extra_workers={d['extra_workers_for_all_at_threshold']/1e6:.1f}m shortfall={d['shortfall_workers']/1e6:.1f}m world={d['world_workers']/1e6:.1f}m" if k.startswith('health') else ""))
    print(json.dumps(res["labour"], indent=1))
    for dom, lst in changes.items():
        print(dom, [(c["region"], round(c["today_pc"], 1), round(c["equal_share_pc"], 1), round(c["change_pct"])) for c in lst if c])


if __name__ == "__main__":
    main()
