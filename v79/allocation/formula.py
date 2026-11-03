"""UNIRA V7.9 — the published allocation formula (design 1), tested in the 30-year world transition.

Formula (proposed amendment to Article 10):
  1. gap_r = (target_r - level_r) x population_r, for each need (energy, health workers, homes);
  2. need adjustment: health target scaled by age structure (people 65+ count AGE_WEIGHT times);
  3. two passes: new capacity first closes every region's gap to the DECENT level (Millward-Hopkins et al. 2020:
     15.3 GJ final energy, 15 m2; WHO 2016: 44.5 health workers per 10,000), then the remaining capacity goes to
     the comfortable gaps (40 GJ, 27 m2, 131 per 10,000), each pass by needs-first water-filling.
Compared with the single-pass rule of v67 (comfortable gaps only), with matched resources (central case).
Main fairness metric: person-years spent below the decent level over 30 years.
python3 formula.py  ->  ../outputs/allocation_formula.json"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
sys.path[:0] = [str(U / "v67"), str(U / "v68" / "counterfactual"), str(U / "v66" / "model")]
import compare  # noqa: E402
import transition as tr  # noqa: E402

DECENT = {"energy": ("energy_gj", 15.3, 1.0), "health": ("health_10k", 44.5, 1e-4), "housing": ("floor_m2", 15.0, 1.0)}
COMFORT = {"energy": 40.0, "health": 131.0, "housing": 27.0}
AGE_WEIGHT = 3.0  # SYNTHETIC_ASSUMPTION: health-care need of a person 65+ relative to a younger person (order of magnitude
#                   of the per-capita health spending ratio by age reported for OECD countries); to be calibrated


def share65():
    d = json.loads((U / "v65" / "data" / "raw" / "wb_SP.POP.65UP.TO.ZS.json").read_text())[1]
    out = {}
    for x in d:
        if x["value"] is not None and x["countryiso3code"] and x["countryiso3code"] not in out:
            out[x["countryiso3code"]] = x["value"] / 100
    return out


def health_weights(regions):
    s = share65()
    w = {k: (1 - s.get(k, 0.1)) + AGE_WEIGHT * s.get(k, 0.1) for k in regions}
    mean = sum(w[k] * regions[k]["pop0"] for k in regions) / sum(r["pop0"] for r in regions.values())
    return {k: v / mean for k, v in w.items()}


def run(regions, s, two_pass, age_adjust, cfg, cap):
    sh = cfg["shared"]
    p = {"energy_target": 40, "health_target": 131, "floor_target": 27,
         "excess_decline": s["rich_region_energy_decline"], "energy_new_ej_per_yr": sh["energy_new_ej_per_yr"],
         "energy_share_to_deficit": s["energy_share_to_regions_in_need"],
         "health_net_new": compare.health_flow(s["health_plan"]), "health_share_to_deficit": s["health_share_to_regions_in_need"],
         "floor_new_m2_per_yr": cap["world_res_floor_added_m2_per_yr"][sh["housing_capacity"]] * s["housing_share_to_regions_in_need"],
         "kcal_eaten": {"decent": 2100, "comfortable": 2470}, "waste_now": 0.19, "waste_unira": 0.095, "waste_years": 10,
         "military_energy_share": s["military_energy_share_freed"], "military_years": 5}
    hw = health_weights(regions) if age_adjust else {k: 1.0 for k in regions}
    below = {d: 0.0 for d in DECENT}
    reached = {d: None for d in DECENT}
    real = tr.allocate_perceived

    def alloc(pool, true_def, p_, domain, t):
        st = p_["_state"]
        key, decent, unit = DECENT[domain]
        if domain == "health":  # age-adjusted comfortable gap
            true_def = {k: max(0.0, (COMFORT["health"] * hw[k] - st[k][key]) * unit * st[k]["pop"]) for k in st}
        # fairness bookkeeping (before this year's allocation)
        dec = {k: max(0.0, (decent * (hw[k] if domain == "health" else 1.0) - st[k][key]) * unit * st[k]["pop"]) for k in st}
        below[domain] += sum(st[k]["pop"] for k in st if dec[k] > 0)
        if reached[domain] is None and not any(v > 0 for v in dec.values()):
            reached[domain] = t
        if not two_pass:
            return tr.allocate(pool, true_def)
        g1 = tr.allocate(pool, {k: min(dec[k], true_def[k]) for k in st})
        rest = pool - sum(g1.values())
        g2 = tr.allocate(rest, {k: true_def[k] - g1[k] for k in st})
        return {k: g1[k] + g2[k] for k in st}

    tr.allocate_perceived = alloc
    try:
        rows, _ = tr.run(regions, p, 30)
    finally:
        tr.allocate_perceived = real
    return {"person_years_below_decent_bn": {d: round(v / 1e9, 2) for d, v in below.items()},
            "year_everyone_decent": reached,
            "comfortable_gap_closed_y15": {d: round(rows[15][f"{d}_shortfall_closed"], 3) for d in DECENT},
            "comfortable_gap_closed_y30": {d: round(rows[30][f"{d}_shortfall_closed"], 3) for d in DECENT}}


def main():
    cfg = compare.load_config()
    regions = compare.rt.load_regions()
    cap = json.loads((U / "v66" / "construction" / "capacity.json").read_text())
    s = compare.settings(cfg, {k: "C" for k in cfg["lever_order"]})
    out = {"age_weight_65plus": AGE_WEIGHT, "decent": {d: v[1] for d, v in DECENT.items()}, "results": {}}
    for name, two, age in (("single_pass_v67", False, False), ("two_pass", True, False), ("two_pass_age_adjusted", True, True)):
        r = run(regions, s, two, age, cfg, cap)
        out["results"][name] = r
        print(name, json.dumps(r))
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "allocation_formula.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
