"""UNIRA V7.0: housing acceleration — how fast can comfortable homes (27 m2/person) reach everyone?

Runs the v67 world transition (UNIRA levers, strong-safeguard leakage from v69) with a growing
housing capacity: capacity(t) = min(base * (1+g)^t, max_rate * population of regions below target).
Stock-first (Article 11): a share of the remaining shortfall each year is met by upgrading /
converting existing buildings, which needs a fraction of the materials, labour and embodied CO2.
Checks: construction labour vs workforce, cumulative embodied CO2 vs carbon budgets.
python3 run.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
U = ROOT.parents[1]
sys.path[:0] = [str(U / "v68" / "counterfactual"), str(U / "v67"), str(U / "v66" / "model")]
import compare  # noqa: E402
import transition as tr  # noqa: E402


def params():
    cfg = json.loads((ROOT / "config.json").read_text())
    ev = ROOT.parent / "evidence" / "parameters.json"
    if ev.exists():
        e = json.loads(ev.read_text())
        for key in ("embodied_co2_kg_m2", "labour_h_m2_low_cost", "upgrade_share_of_need",
                    "upgrade_material_ratio_vs_new", "max_build_m2_per_1000_per_yr"):
            if key in e:
                cfg["evidence"][key] = e[key]
    return cfg


def central(x):
    if isinstance(x, dict):
        return x.get("central", next(iter(v for v in x.values() if isinstance(v, (int, float))), None))
    return x


def run_case(case, cfg, regions, cmpcfg, cap):
    ev = cfg["evidence"]
    s = compare.settings(cmpcfg, {k: "C" for k in cmpcfg["lever_order"]})
    base = cap["world_res_floor_added_m2_per_yr"]["central"] * s["housing_share_to_regions_in_need"]
    max_rate = case.get("max_rate_m2_per_person", central(ev["max_build_m2_per_1000_per_yr"]) / 1000)
    up_share = central(ev["upgrade_share_of_need"]) if case.get("upgrade_from_evidence") else case.get("upgrade_share", 0.0)
    log = []

    def capacity(t, f_def):
        need_pop = sum(regions[k]["pop0"] for k, d in f_def.items() if d > 0)
        built = min(base * (1 + case["growth"]) ** t, max_rate * need_pop)
        upgraded = up_share * sum(f_def.values()) / case.get("upgrade_years", 30)
        log.append({"year": t, "new_m2": built, "upgraded_m2": upgraded})
        return built + upgraded

    sh = cmpcfg["shared"]
    p = {"energy_target": 40, "health_target": 131, "floor_target": 27,
         "excess_decline": s["rich_region_energy_decline"], "energy_new_ej_per_yr": sh["energy_new_ej_per_yr"],
         "energy_share_to_deficit": s["energy_share_to_regions_in_need"],
         "health_net_new": compare.health_flow(s["health_plan"]), "health_share_to_deficit": s["health_share_to_regions_in_need"],
         "floor_new_m2_per_yr": capacity, "leakage": cfg["leakage_strong_safeguards"],
         "kcal_eaten": {"decent": 2100, "comfortable": 2470}, "waste_now": 0.19, "waste_unira": 0.095, "waste_years": 10,
         "military_energy_share": s["military_energy_share_freed"], "military_years": 5}
    rows, _ = tr.run(regions, p, 30)
    first = next((r["year"] for r in rows if r["housing_share_pop_at_target"] >= 0.999), None)
    co2_new, co2_low = central(ev["embodied_co2_kg_m2"]["conventional"]), central(ev["embodied_co2_kg_m2"]["low_carbon"])
    mat_ratio = central(ev["upgrade_material_ratio_vs_new"])
    h_m2 = central(ev["labour_h_m2_low_cost"])
    co2_per_new = co2_low if case.get("low_carbon") else co2_new
    # use what was actually DELIVERED each year (allocation never exceeds true need), split new vs upgraded
    new_tot = up_tot = peak_m2 = 0.0
    for r, x in zip(rows, log):
        delivered = r.get("floor_built_m2", 0.0)
        cap_t = x["new_m2"] + x["upgraded_m2"]
        f_up = x["upgraded_m2"] / cap_t if cap_t else 0.0
        new_tot += delivered * (1 - f_up)
        up_tot += delivered * f_up
        peak_m2 = max(peak_m2, delivered)
    co2_gt = (new_tot * co2_per_new + up_tot * co2_per_new * mat_ratio) / 1e12
    peak_workers_m = peak_m2 * h_m2 / cfg["hours_per_worker_year"] / 1e6
    return {"housing_all_by": first, "housing_closed_y15": rows[15]["housing_shortfall_closed"],
            "housing_closed_y30": rows[30]["housing_shortfall_closed"], "new_bn_m2_30y": new_tot / 1e9,
            "upgraded_bn_m2_30y": up_tot / 1e9, "embodied_co2_gt_30y": co2_gt, "peak_bn_m2_per_yr": peak_m2 / 1e9,
            "peak_construction_workers_m": peak_workers_m}


def main():
    cfg = params()
    cmpcfg = compare.load_config()
    regions = compare.rt.load_regions()
    cap = json.loads((U / "v66" / "construction" / "capacity.json").read_text())
    res = {"evidence": cfg["evidence"], "cases": {}}
    for name, case in cfg["cases"].items():
        res["cases"][name] = run_case(case, cfg, regions, cmpcfg, cap)
    res["budgets_gt"] = cfg["co2_budgets_gt_from_2025"]
    out = ROOT.parent / "outputs"
    out.mkdir(exist_ok=True)
    (out / "housing.json").write_text(json.dumps(res, indent=2))
    print(f"{'case':44s}{'all by':>8s}{'y15':>7s}{'y30':>7s}{'new bn':>8s}{'upg bn':>8s}{'CO2 Gt':>8s}{'peak bn/yr':>11s}{'workers m':>10s}")
    for n, r in res["cases"].items():
        print(f"{n:44s}{str(r['housing_all_by']):>8s}{r['housing_closed_y15']*100:6.0f}%{r['housing_closed_y30']*100:6.0f}%"
              f"{r['new_bn_m2_30y']:8.0f}{r['upgraded_bn_m2_30y']:8.0f}{r['embodied_co2_gt_30y']:8.0f}{r['peak_bn_m2_per_yr']:11.1f}{r['peak_construction_workers_m']:10.0f}")
    print("CO2 budgets from 2025 (Gt):", res["budgets_gt"])


if __name__ == "__main__":
    main()
