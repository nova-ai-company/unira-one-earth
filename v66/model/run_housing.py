"""UNIRA V6.6: residential floor area sufficiency (python3 run_housing.py).
Floor area is MODELLED_REGIONAL (IMAGE, Deetman et al. 2020, 2020 values repeated per country of each region)."""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "v65" / "model"))
import sufficiency as s  # noqa: E402


def main():
    v = {}
    for r in csv.DictReader((ROOT.parent / "data" / "indicators_v66.csv").open()):
        if r["iso3"] != "WLD":
            v[(r["iso3"], r["indicator_id"])] = float(r["value"])
    pops = {}
    for r in csv.DictReader((ROOT.parents[1] / "v65" / "data" / "world_indicators.csv").open()):
        if r["indicator_id"] == "pop_total" and r["iso3"] != "WLD":
            pops[r["iso3"]] = float(r["value"])
    rows = [{"region": i, "population": p, "supply_pc": v.get((i, "floor_area_res_m2_per_cap_image_region"))}
            for i, p in pops.items()]
    out = {}
    for lvl, tau in (("decent_15m2", 15.0), ("comfortable_27m2", 27.0)):
        d = s.domain_summary(rows, tau)
        d["new_floor_area_needed_m2"] = d["shortfall_volume"]
        out[lvl] = d
    out["regions"] = {i: s.region_change(rows, i) for i in ("FRA", "USA", "CHN", "IND", "NGA", "ETH")}
    (ROOT.parent / "outputs" / "housing_sufficiency.json").write_text(json.dumps(out, indent=2))
    for k in ("decent_15m2", "comfortable_27m2"):
        d = out[k]
        print(f"{k}: R={d['sufficiency_ratio']:.2f} below={d['share_people_below']*100:.0f}% ({d['people_below_threshold']/1e9:.2f}bn) "
              f"new floor area needed={d['new_floor_area_needed_m2']/1e9:.1f} bn m2")
    for i, c in out["regions"].items():
        if c:
            print(i, round(c["today_pc"], 1))


if __name__ == "__main__":
    main()
