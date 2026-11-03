"""Precompute simulator results with the SAME tested Python models (no re-implementation in the browser).
python3 build_grids.py  ->  grids.json  (consumed by explorer.html)"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
sys.path[:0] = [str(U / "v63" / "ledger"), str(U / "v68" / "counterfactual"), str(U / "v67"), str(U / "v66" / "model"),
                str(U / "v69" / "coordination")]
import compare  # noqa: E402
import ledger  # noqa: E402
import model as coord  # noqa: E402
import transition as tr  # noqa: E402


def year1_grid():
    inputs = ledger.load_inputs()
    out = []
    for region in ("FR", "EU27_2020"):
        for emp in range(76, 93, 2):
            for theta in ("low", "central", "high"):
                for avoid in ("modest", "moderate", "deep"):
                    for rho in (0.75, 1.0):
                        case = {"theta": theta, "mobilisation": f"universal:{emp}", "avoidable": avoid, "rho": rho}
                        r = ledger.ledger(region, "x", case, inputs)
                        out.append({"region": region, "employment": emp, "theta": theta, "avoidable": avoid, "rho": rho,
                                    "gain": round(r["residual_required_productivity_gain"] * 100, 2),
                                    "theta_share": round(r["share_gap_theta"] * 100, 1),
                                    "mob_share": round(r["share_gap_mobilisation"] * 100, 1),
                                    "avoid_share": round(r["share_gap_avoidable"] * 100, 1)})
    return out


GOV = {"perfect": {"sigma": 0.0, "lag": 0, "misreport_share": 0.0, "inflation": 0.0, "audit_detect": 0.0, "leakage": 0.0},
       "strong": {"sigma": 0.05, "lag": 1, "misreport_share": 0.25, "inflation": 0.07, "audit_detect": 0.5, "leakage": 0.08},
       "none": {"sigma": 0.15, "lag": 2, "misreport_share": 0.25, "inflation": 0.07, "audit_detect": 0.0, "leakage": 0.25},
       "worst": {"sigma": 0.30, "lag": 5, "misreport_share": 0.45, "inflation": 0.20, "audit_detect": 0.0, "leakage": 0.45}}


def world_grid():
    cfg = compare.load_config()
    regions = compare.rt.load_regions()
    cap = json.loads((U / "v66" / "construction" / "capacity.json").read_text())
    out = []
    for system in ("market", "cooperative_market", "unira"):
        if system == "unira":
            s = compare.settings(cfg, {k: "C" for k in cfg["lever_order"]})
        else:
            s = compare.settings(cfg, {k: "B" for k in cfg["lever_order"]})
            if system == "cooperative_market":
                s.update({k: v for k, v in cfg["B2_ambitious_cooperative_market"].items() if not k.startswith("_")})
        for energy in (3.9, 7.0, 10.5):
            for gov_name, gov in GOV.items():
                if system != "unira" and gov_name != "perfect":
                    continue  # governance failures apply to the One Earth allocator
                for growth in (0.0, 0.05, 0.10):
                    base = cap["world_res_floor_added_m2_per_yr"]["central"] * s["housing_share_to_regions_in_need"]
                    def floor(t, f_def, base=base, growth=growth):
                        need_pop = sum(regions[k]["pop0"] for k, d in f_def.items() if d > 0)
                        return min(base * (1 + growth) ** t, 1.468 * need_pop)
                    p = {"energy_target": 40, "health_target": 131, "floor_target": 27,
                         "excess_decline": s["rich_region_energy_decline"], "energy_new_ej_per_yr": energy,
                         "energy_share_to_deficit": s["energy_share_to_regions_in_need"],
                         "health_net_new": compare.health_flow(s["health_plan"]),
                         "health_share_to_deficit": s["health_share_to_regions_in_need"],
                         "floor_new_m2_per_yr": floor, "kcal_eaten": {"decent": 2100, "comfortable": 2470},
                         "waste_now": 0.19, "waste_unira": 0.095, "waste_years": 10,
                         "military_energy_share": s["military_energy_share_freed"], "military_years": 5,
                         "leakage": gov["leakage"]}
                    if gov_name != "perfect":
                        p["perceive"] = coord.make_perceiver(regions, gov, 0)
                    rows, _ = tr.run(regions, p, 30)
                    first = lambda dom: next((r["year"] for r in rows if r[f"{dom}_share_pop_at_target"] >= 0.999), None)
                    out.append({"system": system, "energy_build": energy, "governance": gov_name, "housing_growth": growth,
                                "energy_y15": round(rows[15]["energy_shortfall_closed"] * 100, 1),
                                "health_y15": round(rows[15]["health_shortfall_closed"] * 100, 1),
                                "housing_y30": round(rows[30]["housing_shortfall_closed"] * 100, 1),
                                "energy_all_by": first("energy"), "health_all_by": first("health"),
                                "housing_all_by": first("housing"),
                                "peak_energy_ej": round(max(r["world_energy_ej"] for r in rows), 0),
                                "series": [[r["year"], round(r["energy_shortfall_closed"] * 100, 1),
                                            round(r["health_shortfall_closed"] * 100, 1),
                                            round(r["housing_shortfall_closed"] * 100, 1)] for r in rows]})
    return out


def main():
    grids = {"year1": year1_grid(), "world": world_grid(),
             "money": json.loads((U / "v64" / "outputs" / "lifecycle_summary.json").read_text()),
             "voting": json.loads((U / "v75" / "outputs" / "voting.json").read_text()),
             "joining": json.loads((U / "v72" / "outputs" / "joining.json").read_text()),
             "distribution": json.loads((U / "v74" / "outputs" / "distribution.json").read_text())}
    (HERE / "grids.json").write_text(json.dumps(grids, separators=(",", ":")))
    print("year1 rows", len(grids["year1"]), "world rows", len(grids["world"]),
          "bytes", (HERE / "grids.json").stat().st_size)


if __name__ == "__main__":
    main()
