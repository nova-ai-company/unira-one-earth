"""UNIRA V7.2: voluntary joining — who gains materially, who must value peace/security/time, and
can a union of material gainers succeed on its own capacity?   python3 run.py

Material comparison per region at year 30: UNIRA (C levers, strong safeguards) vs staying in a
reformed market world (B levers). Material index = mean of log ratios C/B for final energy per person,
health workers per 10,000 and floor area per person (equal weights; stated, not estimated).
Regions with index < 0 lose materially; their break-even is the value of non-material gains
(peace, security, 30 h week, climate) needed, expressed as the equivalent % of material standard.
Union-of-gainers test: the transition is rerun for member regions only, with new capacity scaled to
members' share of world energy use (proxy for productive capacity), health training to members'
share of health workers, and building to members' share of population.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
U = ROOT.parents[1]
sys.path[:0] = [str(U / "v68" / "counterfactual"), str(U / "v67"), str(U / "v66" / "model")]
import compare  # noqa: E402
import transition as tr  # noqa: E402

LEAK = 0.08  # strong safeguards (v69)


def build_p(s, cfg, cap, regions_share=1.0, energy_share=1.0, health_share=1.0, pop_share=1.0):
    sh = cfg["shared"]
    flow = compare.health_flow(s["health_plan"])
    return {"energy_target": 40, "health_target": 131, "floor_target": 27,
            "excess_decline": s["rich_region_energy_decline"],
            "energy_new_ej_per_yr": sh["energy_new_ej_per_yr"] * energy_share,
            "energy_share_to_deficit": s["energy_share_to_regions_in_need"],
            "health_net_new": (lambda t: flow(t) * health_share), "health_share_to_deficit": s["health_share_to_regions_in_need"],
            "floor_new_m2_per_yr": cap["world_res_floor_added_m2_per_yr"][sh["housing_capacity"]] * s["housing_share_to_regions_in_need"] * pop_share,
            "kcal_eaten": {"decent": 2100, "comfortable": 2470}, "waste_now": 0.19, "waste_unira": 0.095, "waste_years": 10,
            "military_energy_share": s["military_energy_share_freed"], "military_years": 5, "leakage": LEAK}


def final_state(regions, p):
    rows, _ = tr.run(regions, p, 30)
    return p["_final_state"], rows


def main():
    cfg = compare.load_config()
    regions = compare.rt.load_regions()
    cap = json.loads((U / "v66" / "construction" / "capacity.json").read_text())
    sC = compare.settings(cfg, {k: "C" for k in cfg["lever_order"]})
    sB = compare.settings(cfg, {k: "B" for k in cfg["lever_order"]})
    stC, _ = final_state(regions, build_p(sC, cfg, cap))
    stB, _ = final_state(regions, build_p(sB, cfg, cap))
    per = {}
    for k in regions:
        ratios = [stC[k]["energy_gj"] / stB[k]["energy_gj"], stC[k]["health_10k"] / stB[k]["health_10k"],
                  stC[k]["floor_m2"] / stB[k]["floor_m2"]]
        idx = sum(math.log(x) for x in ratios) / 3
        per[k] = {"pop": regions[k]["pop0"], "energy_ratio": ratios[0], "health_ratio": ratios[1], "floor_ratio": ratios[2],
                  "material_index": idx, "material_change_pct": 100 * (math.exp(idx) - 1)}
    world = sum(v["pop"] for v in per.values())
    gainers = {k for k, v in per.items() if v["material_index"] > 0}
    losers = set(per) - gainers
    breakeven = sorted(((k, -per[k]["material_change_pct"]) for k in losers), key=lambda x: -x[1])
    # union of gainers only
    e_share = sum(regions[k]["energy_gj"] * regions[k]["pop0"] for k in gainers) / sum(r["energy_gj"] * r["pop0"] for r in regions.values())
    h_share = sum(regions[k]["health_10k"] * regions[k]["pop0"] for k in gainers) / sum(r["health_10k"] * r["pop0"] for r in regions.values())
    p_share = sum(regions[k]["pop0"] for k in gainers) / world
    sub = {k: regions[k] for k in gainers}
    _, rows_union = final_state(sub, build_p(sC, cfg, cap, energy_share=e_share, health_share=h_share, pop_share=p_share))
    _, rows_all = final_state(regions, build_p(sC, cfg, cap))
    pick = lambda rows: {"energy_closed_y15": rows[15]["energy_shortfall_closed"], "health_closed_y15": rows[15]["health_shortfall_closed"],
                         "housing_closed_y30": rows[30]["housing_shortfall_closed"]}
    show = ["FRA", "USA", "DEU", "CHN", "BRA", "IND", "NGA", "ETH", "PAK", "IDN", "RUS", "JPN"]
    res = {"material_index_definition": "mean log ratio UNIRA/market of final energy, health workers, floor area at year 30",
           "gainers_share_of_world_pop": sum(per[k]["pop"] for k in gainers) / world,
           "losers_share_of_world_pop": sum(per[k]["pop"] for k in losers) / world,
           "n_gainers": len(gainers), "n_losers": len(losers),
           "union_of_gainers": {"members_share_energy_use": e_share, "members_share_health_workers": h_share,
                                "members_share_population": p_share, "outcomes": pick(rows_union)},
           "whole_world_unira_outcomes": pick(rows_all),
           "breakeven_losers_top": breakeven[:15],
           "regions": {k: per[k] for k in show if k in per}}
    out = ROOT.parent / "outputs"
    out.mkdir(exist_ok=True)
    (out / "joining.json").write_text(json.dumps(res, indent=2))
    print(f"gainers {res['n_gainers']} regions, {res['gainers_share_of_world_pop']*100:.0f}% of people; losers {res['n_losers']}, {res['losers_share_of_world_pop']*100:.0f}%")
    for k, v in res["regions"].items():
        print(f"  {k}: energy x{v['energy_ratio']:.2f} health x{v['health_ratio']:.2f} floor x{v['floor_ratio']:.2f} -> material {v['material_change_pct']:+.0f}%")
    print("union of gainers: shares", {k: round(v, 2) for k, v in res["union_of_gainers"].items() if k != "outcomes"})
    print("  outcomes union-only:", {k: round(v * 100) for k, v in res["union_of_gainers"]["outcomes"].items()})
    print("  outcomes whole world:", {k: round(v * 100) for k, v in res["whole_world_unira_outcomes"].items()})
    print("largest material losses (must be outweighed by peace/security/time):", [(k, round(v)) for k, v in breakeven[:8]])


if __name__ == "__main__":
    main()
