"""UNIRA V7.0 — which "out of the box" levers make comfortable homes for everyone faster and cheaper in people?
(author's question, 2026-11-08). Each lever is a parameter change on the published housing model (run.py); none is a
new mechanism. Base case: +10%/yr capacity growth in regions of need, stock-first, low-carbon.

Levers tested:
  - factory (modular) building: fewer hours of work per m2 (McKinsey 2019 reports up to 20% lower cost and 20-50% shorter
    schedules; applied here to labour as 20% / 35%, SYNTHETIC);
  - decent core first, extension later: a 15 m2 core for everyone, then growth to 27 m2;
  - households build part of the extension themselves with professional supervision and materials (mutual self-help
    programmes require about 65% of labour from families, REPORTED; sites-and-services neighbourhoods in Tanzania grew
    into better housing than control areas over 30-40 years, VERIFIED);
  - faster capacity growth (15%/yr) and, as a flagged assumption, a build rate 1.5x the highest ever observed (China 2011).
Reuse of empty and under-occupied homes is reported but not a lever on the world gap: the empty homes are in Japan,
Spain, Portugal and the EU (Japan 2023: 9.0 m vacant, 13.8%; EU 2023: 33.3% of people in under-occupied homes), not where
the floor area is missing (v70: about 0.5% of the need in deficit regions).
python3 run_levers.py  ->  ../outputs/housing_levers.json
"""
import json
from pathlib import Path

import run

ROOT = Path(__file__).resolve().parent
U = ROOT.parents[1]
BASE_CASE = "ramp_10pct_stock_first_low_carbon"
DECENT_M2, COMFORTABLE_M2 = 15.0, 27.0

LEVERS = [  # key, label, case overrides, self-build share of labour on the increment above the decent level
    ("base", "Published: +10%/yr, stock-first, low-carbon", {}, 0.0),
    ("factory_20", "Factory building: 20% fewer hours per m2", {"labour_multiplier": 0.8}, 0.0),
    ("factory_35", "Factory building: 35% fewer hours per m2", {"labour_multiplier": 0.65}, 0.0),
    ("self_build_50", "Households build half of the extension above 15 m2 (supervised, materials supplied)", {}, 0.5),
    ("self_build_65", "Households build 65% of the extension (mutual self-help practice)", {}, 0.65),
    ("decent_core_first", "Decent core (15 m2) for everyone first", {"floor_target": DECENT_M2}, 0.0),
    ("growth_15", "Capacity +15%/yr (standard record cap)", {"growth": 0.15}, 0.0),
    ("growth_15_record_1_5x", "Capacity +15%/yr and build rate up to 1.5x the China 2011 record (SYNTHETIC)",
     {"growth": 0.15, "max_rate_m2_per_person": 1.468 * 1.5}, 0.0),
    ("all", "All levers: factory 20%, households build half of the extension, +15%/yr, 1.5x record",
     {"labour_multiplier": 0.8, "growth": 0.15, "max_rate_m2_per_person": 1.468 * 1.5}, 0.5),
]
EVIDENCE = {
    "labour_multiplier": "McKinsey 2019 (via Construction Dive 24 Jun 2019, secondary, VERIFIED text): modular 20-50% faster, cost "
                         "savings up to 20%, risk of 10% loss; applied to hours per m2 as 0.8 / 0.65 SYNTHETIC",
    "self_build_share": "USDA mutual self-help housing: families provide at least 65% of labour (RCAC, REPORTED, page refused "
                        "fetch); applied to the increment above 15 m2 only; household hours are counted separately",
    "sites_and_services": "Michaels et al. 2017 (LSE SERC DP222, VERIFIED abstract): de novo sites-and-services neighbourhoods "
                          "in seven Tanzanian cities developed better housing than control areas (larger footprints, more "
                          "storeys, water, electricity, sanitation, roads); upgrading areas if anything worse",
    "reuse": "Japan 2023 Housing and Land Survey: 9.0 m vacant, 13.8% (Jiji/Kyodo, REPORTED); EU 2023: 33.3% in under-occupied "
             "homes (Eurostat housing 2024, VERIFIED); India urban vacant 11.1 m (v70): ~0.5% of the need in deficit regions",
    "record_1_5x": "SYNTHETIC: factory production could exceed the China 2011 site-built record; no observation supports it",
    "3d_printing": "no independently audited whole-project cost or schedule figures found (prototype and print-time claims "
                   "only); not used as a lever",
}


def increment_share(regions, target=COMFORTABLE_M2, decent=DECENT_M2):
    """Share of the 30-year floor-area need that is the increment above the decent level (extension, not core)."""
    inc = tot = 0.0
    for v in regions.values():
        gap_pp = max(0.0, target - v["floor_m2"])
        if gap_pp <= 0:
            continue
        backlog = gap_pp * v["pop0"]
        growth = target * max(0.0, v["pop50"] - v["pop0"])
        inc += max(0.0, min(gap_pp, target - decent)) * v["pop0"] + (target - decent) / target * growth
        tot += backlog + growth
    return inc / tot if tot else 0.0


def main(write=True):
    cfg = run.params()
    cmpcfg = run.compare.load_config()
    regions = run.compare.rt.load_regions()
    cap = json.loads((U / "v66" / "construction" / "capacity.json").read_text())
    base_case = cfg["cases"][BASE_CASE]
    inc_share = increment_share(regions)
    h_m2 = run.central(cfg["evidence"]["labour_h_m2_low_cost"])
    res = {}
    for key, label, over, sb in LEVERS:
        case = dict(base_case, **over)
        r = run.run_case(case, cfg, regions, cmpcfg, cap)
        pro_share = 1.0 - sb * (inc_share if case.get("floor_target", COMFORTABLE_M2) > DECENT_M2 else 0.0)
        delivered = (r["new_bn_m2_30y"] + r["upgraded_bn_m2_30y"]) * 1e9
        household_h = delivered * inc_share * sb * h_m2 * case.get("labour_multiplier", 1.0)
        res[key] = {"label": label, "overrides": over, "self_build_share_of_extension_labour": sb,
                    "housing_all_by": r["housing_all_by"], "housing_closed_y15": round(r["housing_closed_y15"], 4),
                    "housing_closed_y30": round(r["housing_closed_y30"], 4), "peak_bn_m2_per_yr": round(r["peak_bn_m2_per_yr"], 3),
                    "peak_construction_workers_m": round(r["peak_construction_workers_m"], 1),
                    "peak_professional_workers_m": round(r["peak_construction_workers_m"] * pro_share, 1),
                    "household_hours_bn_30y": round(household_h / 1e9, 1), "embodied_co2_gt_30y": round(r["embodied_co2_gt_30y"], 1)}
    out = {"question": "author, 2026-11-08: out-of-the-box ways to build homes at low cost and fast",
           "base_case": BASE_CASE, "increment_above_decent_share_of_need": round(inc_share, 4),
           "labour_h_per_m2_central": h_m2, "world_construction_workers_m": 294, "workers_south_asia_africa_m": 116,
           "levers": res, "evidence": EVIDENCE,
           "reading": "the date is set by how fast building capacity grows and by the record build rate, not by cost; factory "
                      "building and household self-build cut the professional workforce needed at the peak, which is the "
                      "binding limit found in v70 (240-265 m workers against 116 m in South Asia and Africa)",
           "limits": ["labour hours per m2 for self-built extensions unknown (set equal to professional hours)",
                      "self-build needs a core designed for extension, land tenure, supervision and materials logistics",
                      "the model has one world capacity; regional bottlenecks (cement, skilled trades) are not represented",
                      "the 1.5x record case has no observational support and is shown only to test whether the cap binds"]}
    if write:
        (ROOT.parent / "outputs" / "housing_levers.json").write_text(json.dumps(out, indent=2))
        print(f"increment above decent = {inc_share*100:.0f}% of the need")
        for k, r in res.items():
            print(f"{k:24s} all by {str(r['housing_all_by']):>5s}  y15 {r['housing_closed_y15']*100:4.0f}%  peak {r['peak_bn_m2_per_yr']:.1f} bn m2/yr"
                  f"  workers {r['peak_construction_workers_m']:.0f} m (professional {r['peak_professional_workers_m']:.0f} m)"
                  f"  household {r['household_hours_bn_30y']:.0f} bn h")
    return out


if __name__ == "__main__":
    main()
