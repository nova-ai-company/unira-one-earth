"""UNIRA V6.9: needs-first allocation under errors, delays, misreporting and leakage (python3 run.py)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
U = ROOT.parents[1]
sys.path[:0] = [str(ROOT), str(U / "v68" / "counterfactual"), str(U / "v67"), str(U / "v66" / "model")]
import compare  # noqa: E402
import model  # noqa: E402
import transition as tr  # noqa: E402

METRICS = ["energy_closed_y15", "health_closed_y15", "housing_closed_y30", "energy_all_by", "health_all_by"]


def world_with_gov(s, regions, cfg, cap, gov, seed):
    sh = cfg["shared"]
    p = {"energy_target": 40, "health_target": 131, "floor_target": 27,
         "excess_decline": s["rich_region_energy_decline"], "energy_new_ej_per_yr": sh["energy_new_ej_per_yr"],
         "energy_share_to_deficit": s["energy_share_to_regions_in_need"],
         "health_net_new": compare.health_flow(s["health_plan"]), "health_share_to_deficit": s["health_share_to_regions_in_need"],
         "floor_new_m2_per_yr": cap["world_res_floor_added_m2_per_yr"][sh["housing_capacity"]] * s["housing_share_to_regions_in_need"],
         "kcal_eaten": {"decent": 2100, "comfortable": 2470}, "waste_now": 0.19, "waste_unira": 0.095, "waste_years": 10,
         "military_energy_share": s["military_energy_share_freed"], "military_years": 5,
         "leakage": gov["leakage"], "perceive": model.make_perceiver(regions, gov, seed)}
    rows, _ = tr.run(regions, p, 30)
    first = lambda dom: next((r["year"] for r in rows if r[f"{dom}_share_pop_at_target"] >= 0.999), None)
    return {"energy_closed_y15": rows[15]["energy_shortfall_closed"], "health_closed_y15": rows[15]["health_shortfall_closed"],
            "housing_closed_y30": rows[30]["housing_shortfall_closed"], "energy_all_by": first("energy"),
            "health_all_by": first("health")}


def summarise(runs):
    out = {}
    for m in METRICS:
        vals = [r[m] for r in runs]
        if m.endswith("_by"):
            reached = [v for v in vals if v is not None]
            out[m] = {"share_of_runs_reached": len(reached) / len(vals),
                      "median_year_if_reached": model.quantiles(reached)[1] if reached else None}
        else:
            out[m] = dict(zip(("p10", "p50", "p90"), model.quantiles(vals)))
    return out


def main():
    gcfg = json.loads((ROOT / "config.json").read_text())
    cfg = compare.load_config()
    regions = compare.rt.load_regions()
    cap = json.loads((U / "v66" / "construction" / "capacity.json").read_text())
    allC = {k: "C" for k in cfg["lever_order"]}
    sC = compare.settings(cfg, allC)
    res = {"governance_scenarios": gcfg["scenarios"], "results": {}}
    for name, gov in gcfg["scenarios"].items():
        runs = [world_with_gov(sC, regions, cfg, cap, gov, seed) for seed in range(gcfg["seeds"])]
        res["results"][name] = summarise(runs)
    comp = json.loads((U / "v68" / "outputs" / "comparison.json").read_text())
    res["market_reference"] = {k: {m: comp[k][m] for m in METRICS} for k in ("B_reformed_market", "B2_ambitious_cooperative_market")}
    out = ROOT.parent / "outputs"
    out.mkdir(exist_ok=True)
    (out / "coordination.json").write_text(json.dumps(res, indent=2))
    pct = lambda d: f"{d['p50']*100:5.0f}% [{d['p10']*100:.0f}-{d['p90']*100:.0f}]"
    print(f"{'scenario':38s}{'energy y15':>20s}{'health y15':>20s}{'housing y30':>20s}  energy-all-reached")
    for name, r in res["results"].items():
        print(f"{name:38s}{pct(r['energy_closed_y15']):>20s}{pct(r['health_closed_y15']):>20s}{pct(r['housing_closed_y30']):>20s}  "
              f"{r['energy_all_by']['share_of_runs_reached']*100:.0f}% yr {r['energy_all_by']['median_year_if_reached']}")
    for k, r in res["market_reference"].items():
        print(f"{k:38s}{r['energy_closed_y15']*100:19.0f}%{r['health_closed_y15']*100:19.0f}%{r['housing_closed_y30']*100:19.0f}%")


if __name__ == "__main__":
    main()
