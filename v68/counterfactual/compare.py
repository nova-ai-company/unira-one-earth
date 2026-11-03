"""UNIRA V6.8: reformed market economy (B) vs UNIRA (C) with matched resources.

Runs the existing models (v63 year-1 ledger for France and Europe, v67 world transition with
v66 health plan) under B and C lever settings, then switches each lever from B to C on its own
("one-at-a-time from B") to attribute C's advantage to institutions.
python3 compare.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
U = ROOT.parents[1]
sys.path[:0] = [str(U / "v63" / "ledger"), str(U / "v67"), str(U / "v66" / "model")]
import health_plan as hp  # noqa: E402
import ledger  # noqa: E402
import run_health  # noqa: E402
import run_transition as rt  # noqa: E402
import transition as tr  # noqa: E402


def load_config():
    cfg = json.loads((ROOT / "config.json").read_text())
    ver = ROOT.parent / "verification" / "parameters.json"
    cfg["verified_overrides"] = {}
    if ver.exists():
        v = json.loads(ver.read_text())
        for lever, key in (("energy_share_to_regions_in_need", "item7_clean_invest_share_EMDE_excl_China"),
                           ("housing_share_to_regions_in_need", "item11_new_res_construction_share_LIC_LMIC")):
            if key in v and isinstance(v[key], dict) and isinstance(v[key].get("value"), (int, float)):
                val = v[key]["value"]
                val = val / 100 if val > 1 else val
                side = "B"
                cfg["levers"][lever][side] = val
                cfg["verified_overrides"][lever] = {side: val, "evidence_class": v[key].get("evidence_class")}
    return cfg


def settings(cfg, which):
    """which: dict lever -> 'B' | 'C'."""
    return {k: cfg["levers"][k][which[k]] for k in cfg["lever_order"]}


def france_year1(s, inputs, region="FR"):
    case = {"theta": "central", "mobilisation": f"universal:{s['employment_rate_20_64']}",
            "avoidable": s["market_specific_activity_cut"], "rho": 0.75}
    r = ledger.ledger(region, "x", case, inputs)
    return r["residual_required_productivity_gain"]


def health_flow(scenario):
    stock0, wld, prev = run_health.world_inputs()
    p = run_health.scenarios(stock0, wld, prev)[f"central|{scenario}"]
    rows, _ = hp.simulate(p, 40)
    d = [rows[t + 1]["stock"] - rows[t]["stock"] for t in range(40)]
    return lambda t: max(0.0, d[min(t, 39)])


def world(s, regions, cfg, cap):
    sh = cfg["shared"]
    p = {"energy_target": 40, "health_target": 131, "floor_target": 27,
         "excess_decline": s["rich_region_energy_decline"], "energy_new_ej_per_yr": sh["energy_new_ej_per_yr"],
         "energy_share_to_deficit": s["energy_share_to_regions_in_need"],
         "health_net_new": health_flow(s["health_plan"]), "health_share_to_deficit": s["health_share_to_regions_in_need"],
         "floor_new_m2_per_yr": cap["world_res_floor_added_m2_per_yr"][sh["housing_capacity"]] * s["housing_share_to_regions_in_need"],
         "kcal_eaten": {"decent": 2100, "comfortable": 2470}, "waste_now": 0.19, "waste_unira": 0.095, "waste_years": 10,
         "military_energy_share": s["military_energy_share_freed"], "military_years": 5}
    rows, _ = tr.run(regions, p, 30)
    first = lambda dom: next((r["year"] for r in rows if r[f"{dom}_share_pop_at_target"] >= 0.999), None)
    return {"energy_all_by": first("energy"), "health_all_by": first("health"), "housing_all_by": first("housing"),
            "energy_closed_y15": rows[15]["energy_shortfall_closed"], "health_closed_y15": rows[15]["health_shortfall_closed"],
            "housing_closed_y30": rows[30]["housing_shortfall_closed"],
            "peak_world_energy_ej": max(r["world_energy_ej"] for r in rows), "world_energy_y30_ej": rows[30]["world_energy_ej"]}


def run_all():
    cfg = load_config()
    inputs = ledger.load_inputs()
    regions = rt.load_regions()
    cap = json.loads((U / "v66" / "construction" / "capacity.json").read_text())
    allB = {k: "B" for k in cfg["lever_order"]}
    allC = {k: "C" for k in cfg["lever_order"]}

    def evaluate(which):
        s = settings(cfg, which)
        return {"france_year1_gain_needed": france_year1(s, inputs),
                "europe_year1_gain_needed": france_year1(s, inputs, "EU27_2020"), **world(s, regions, cfg, cap)}

    res = {"B_reformed_market": evaluate(allB), "C_unira": evaluate(allC), "one_lever_from_B": {}}
    b2 = {k: v for k, v in cfg["B2_ambitious_cooperative_market"].items() if not k.startswith("_")}
    s2 = settings(cfg, allB)
    s2.update(b2)
    res["B2_ambitious_cooperative_market"] = {"france_year1_gain_needed": france_year1(s2, inputs),
                                              "europe_year1_gain_needed": france_year1(s2, inputs, "EU27_2020"),
                                              **world(s2, regions, cfg, cap)}
    for lever in cfg["lever_order"]:
        which = dict(allB, **{lever: "C"})
        res["one_lever_from_B"][lever] = evaluate(which)
    res["levers"] = cfg["levers"]
    res["verified_overrides"] = cfg["verified_overrides"]
    return res


def main():
    res = run_all()
    out = ROOT.parent / "outputs"
    out.mkdir(exist_ok=True)
    (out / "comparison.json").write_text(json.dumps(res, indent=2, default=str))
    fmt = lambda v: "-" if v is None else (f"{v*100:.1f}%" if isinstance(v, float) and v < 2 else f"{v:.0f}" if isinstance(v, float) else str(v))
    keys = ["france_year1_gain_needed", "europe_year1_gain_needed", "energy_all_by", "health_all_by", "housing_all_by",
            "energy_closed_y15", "health_closed_y15", "housing_closed_y30", "peak_world_energy_ej"]
    print(f"{'':42s}" + "".join(f"{k[:14]:>15s}" for k in keys))
    for name, r in [("B reformed market", res["B_reformed_market"]),
                    ("B2 ambitious cooperative market", res["B2_ambitious_cooperative_market"]), ("C UNIRA", res["C_unira"])] + \
                   [(f"  B + {k}", v) for k, v in res["one_lever_from_B"].items()]:
        print(f"{name[:42]:42s}" + "".join(f"{fmt(r[k]):>15s}" for k in keys))


if __name__ == "__main__":
    main()
