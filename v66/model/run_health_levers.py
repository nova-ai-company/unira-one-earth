"""UNIRA V6.6 — which levers shorten the time to EU-level health care for everyone? (author's question, 2026-11-06)

Sensitivity of the ambitious plan (scenario 5 of run_health.py: training +10%/yr for 15 years, 50% of armed-forces
personnel volunteer, strong prevention) to retention, course length, training capacity and the target itself.
Each lever is a parameter change on the published model; none is a new mechanism. Run after run_health.py.
python3 run_health_levers.py  ->  ../outputs/health_levers.json"""
import json
from pathlib import Path

import health_plan as hp
import run_health as rh

ROOT = Path(__file__).resolve().parent
BASE = "5_ambitious_10pct_50pct_prevention_high"
LEVERS = [  # key, label, overrides on the ambitious scenario
    ("ambitious", "Ambitious plan as published (exits 3%/yr, 4-year courses, capacity cap 3x, +10%/yr)", {}),
    ("retention_2pct", "Exits 3% -> 2% a year (retention)", {"exit_rate": 0.02}),
    ("retention_1p5pct", "Exits 3% -> 1.5% a year", {"exit_rate": 0.015}),
    ("courses_3y", "Courses 4 -> 3 years (shorter tracks)", {"lead_time": 3}),
    ("courses_2y", "Courses 4 -> 2 years", {"lead_time": 2}),
    ("capacity_4x", "Training capacity cap 3x -> 4x today's intake", {"intake_capacity_multiple": 4.0}),
    ("capacity_5x_exp15", "Capacity cap 5x and +15%/yr expansion (faculties and trainers first)",
     {"intake_capacity_multiple": 5.0, "expansion": 0.15}),
    ("target_100", "Target 131 -> 100 per 10,000", {"tau_per_10k": 100.0}),
    ("target_80", "Target 131 -> 80 per 10,000", {"tau_per_10k": 80.0}),
    ("target_decent", "Target 44.5 per 10,000 (decent; world total only, regions differ)", {"tau_per_10k": 44.5}),
    ("retention_courses_capacity", "Retention 2% + courses 3 years + capacity 4x",
     {"exit_rate": 0.02, "lead_time": 3, "intake_capacity_multiple": 4.0}),
    ("all", "All levers: retention 2%, courses 3 years, capacity 5x, +15%/yr",
     {"exit_rate": 0.02, "lead_time": 3, "intake_capacity_multiple": 5.0, "expansion": 0.15}),
]
EVIDENCE = {"exit_rate": "3%/yr MODEL_DERIVED (France nurses); 2% and 1.5% are SYNTHETIC targets, untested",
            "lead_time": "4 yr weighted (REPORTED_NEEDS_RECHECK); 3 and 2 yr illustrate task shifting / shorter tracks, SYNTHETIC",
            "intake_capacity_multiple": "3x SYNTHETIC; 4x and 5x SYNTHETIC (faculties and trainers must be built first)",
            "tau_per_10k": "131 = EU density (medium confidence, not outcome-based); 100 and 80 are illustrative; 44.5 = WHO threshold",
            "reading": "the capacity cap binds, so course length matters little; the target definition and retention matter most"}


def main(write=True):
    stock0, wld, prev = rh.world_inputs()
    sc = rh.scenarios(stock0, wld, prev)
    res = {}
    for key, label, over in LEVERS:
        r = {"label": label, "overrides": over, "years": {}, "per_10k_y30": {}}
        for cap in ("low", "central", "high"):
            rows, closed = hp.simulate(dict(sc[f"{cap}|{BASE}"], **over), 80)
            r["years"][cap] = closed
            r["per_10k_y30"][cap] = round(rows[30]["per_10k"], 1)
        res[key] = r
    out = {"base_scenario": BASE, "stock0": stock0, "need_at_131_for_2050_population_m": round(131 / 1e4 * wld["pop_total_2050_wpp2024_medium"] * 1e3 / 1e6, 1),
           "levers": res, "evidence": EVIDENCE}
    if write:
        (ROOT.parent / "outputs" / "health_levers.json").write_text(json.dumps(out, indent=2))
        for k, r in res.items():
            y = r["years"]
            print(f"{k:28s} low/central/high = {y['low']} / {y['central']} / {y['high']}  (central per 10k at y30: {r['per_10k_y30']['central']})")
    return out


if __name__ == "__main__":
    main()
