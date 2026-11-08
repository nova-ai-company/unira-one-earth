"""UNIRA V6.6 — training capacity when theory is taught online and the physical schools, laboratories and hospitals are
used in rotation for practice only (author's direction, 2026-11-08).

The health plan caps yearly intake at `intake_capacity_multiple` x today's intake, a synthetic 3x standing for "schools and
teachers can at most triple". This module splits that cap into four components and asks what each becomes when:
  - theory is taught online (lecture halls stop binding; blended learning is at least as effective for knowledge);
  - skills laboratories and simulation centres run in rotation, six or seven days a week, instead of at today's ~20%
    occupancy of university teaching space;
  - up to half of clinical placement hours are delivered in simulation (NCSBN randomised study: no difference in
    competency, knowledge or licensing pass rates at 50%), and placements rotate across all hospitals and regions;
  - educators keep teaching: online theory frees part of their time, but supervision still scales with students.
The effective cap is the smallest component. A second design treats every hospital as a teaching hospital, so that
placements and preceptors grow with the workforce itself (`capacity_scales_with_stock` in health_plan.py).
Run after run_health.py:  python3 training_capacity.py  ->  ../outputs/training_capacity.json
"""
import json
from pathlib import Path

import health_plan as hp
import run_health as rh

ROOT = Path(__file__).resolve().parent
BASE = "5_ambitious_10pct_50pct_prevention_high"
PUBLISHED_CAP = 3.0  # synthetic cap of the published plan: schools and teachers at most tripled by building and hiring

# Multiplier on the throughput of each EXISTING unit under the rotation design (new building and hiring continue at the
# published pace, so the component cap = multiplier x PUBLISHED_CAP). low / central / high.
COMPONENTS = {
    "lecture_space": {
        "rotation": {"low": 30.0, "central": 30.0, "high": 30.0},
        "basis": "theory online: lecture halls stop binding (set to 30x, i.e. never the smallest component). Blended learning "
                 "vs traditional: knowledge SMD 0.81 (Liu 2016, 56 articles; 0.26 after trim-and-fill) and 1.07 (Vallee 2020, "
                 "56 studies) - as effective or better, heterogeneity high. VERIFIED (abstracts)."},
    "practice_facilities": {
        "rotation": {"low": 1.7, "central": 2.5, "high": 3.5},
        "basis": "skills laboratories and simulation centres used in rotation: occupancy from ~20% (Smart Space Forum / SmartViz "
                 "analysis of 30+ UK universities, THE 23 Jul 2026, REPORTED) or 35% (Bristol target, unverified) to 60-70% with "
                 "shifts and six or seven days a week. SYNTHETIC targets."},
    "clinical_placements": {
        "rotation": {"low": 1.33, "central": 2.0, "high": 3.0},
        "basis": "simulation replaces 25% (low) or 50% (central, high) of clinical hours with no difference in outcomes (NCSBN "
                 "National Simulation Study, 10 programmes, 666 students, randomised, VERIFIED_OFFICIAL) -> x1.33 / x2 placement "
                 "capacity per student; high adds x1.5 for rotation across under-used hospitals and regions (SYNTHETIC). "
                 "Evidence is for pre-licensure nursing; extension to doctors and midwives is an assumption."},
    "educators": {
        "rotation": {"low": 1.1, "central": 1.3, "high": 1.5},
        "basis": "online theory frees 10 / 30 / 50% of educator time per student (one lecturer serves many; tutoring, assessment "
                 "and supervision still scale with students). SYNTHETIC. Educators, clinical sites and preceptors are the "
                 "barriers US nursing schools report (AACN, 15 Apr 2024: 65,766 qualified applications refused in 2023, "
                 "VERIFIED_OFFICIAL)."},
}


def component_caps(level):
    """Cap of each component as a multiple of today's intake, for a multiplier level (low/central/high)."""
    return {k: round(v["rotation"][level] * PUBLISHED_CAP, 3) for k, v in COMPONENTS.items()}


def effective_cap(level):
    caps = component_caps(level)
    binding = min(caps, key=caps.get)
    return caps[binding], binding, caps


DESIGNS = [  # key, label, overrides on the ambitious scenario (filled per level in main)
    ("published", "Published plan: schools and teachers at most tripled (cap 3x), +10%/yr for 15 years", lambda lvl: {}),
    ("rotation_same_educators", "Theory online, facilities in rotation, simulation for half of clinical hours; same educators",
     lambda lvl: {"intake_capacity_multiple": effective_cap(lvl)[0]}),
    ("rotation_every_hospital_teaches", "As above, and every hospital teaches: placements and preceptors grow with the workforce",
     lambda lvl: {"intake_capacity_multiple": effective_cap(lvl)[0], "capacity_scales_with_stock": True}),
    ("rotation_every_hospital_exp15", "As above, with +15%/yr expansion (faculties and trainers first, T-8.5)",
     lambda lvl: {"intake_capacity_multiple": effective_cap(lvl)[0], "capacity_scales_with_stock": True, "expansion": 0.15}),
    ("rotation_every_hospital_exp15_retention2", "As above, with exits 3% -> 2% a year (retention)",
     lambda lvl: {"intake_capacity_multiple": effective_cap(lvl)[0], "capacity_scales_with_stock": True, "expansion": 0.15,
                  "exit_rate": 0.02}),
]


def main(write=True):
    stock0, wld, prev = rh.world_inputs()
    sc = rh.scenarios(stock0, wld, prev)
    caps = {lvl: dict(zip(("effective_cap", "binding_component", "components"), effective_cap(lvl)))
            for lvl in ("low", "central", "high")}
    res = {}
    for key, label, over in DESIGNS:
        r = {"label": label, "years": {}, "per_10k_y30": {}, "intake_cap_multiple": {}}
        for cap in ("low", "central", "high"):  # cap = base-intake case; component multipliers at the same level
            o = over(cap)
            rows, closed = hp.simulate(dict(sc[f"{cap}|{BASE}"], **o), 80)
            r["years"][cap] = closed
            r["per_10k_y30"][cap] = round(rows[30]["per_10k"], 1)
            r["intake_cap_multiple"][cap] = o.get("intake_capacity_multiple", PUBLISHED_CAP)
        res[key] = r
    # sensitivity: central intake case, multipliers at low / central / high
    sens = {}
    for lvl in ("low", "central", "high"):
        for scale in (False, True):
            o = {"intake_capacity_multiple": caps[lvl]["effective_cap"], "capacity_scales_with_stock": scale}
            _, closed = hp.simulate(dict(sc[f"central|{BASE}"], **o), 80)
            sens[f"multipliers_{lvl}|{'every_hospital_teaches' if scale else 'same_educators'}"] = closed
    out = {"question": "author, 2026-11-08: theory online, physical schools and hospitals used in rotation for practice only; "
                       "trainees rotate across hospitals to learn with expert clinicians",
           "base_scenario": BASE, "published_cap": PUBLISHED_CAP, "component_caps": caps, "designs": res,
           "sensitivity_central_intake": sens,
           "reading": "with the same educators the cap rises only from 3x to about 3.3-4.5x because educators bind; the large gain "
                      "comes when every hospital teaches, so that placements and preceptors grow with the workforce. Facilities "
                      "stop being the limit; people who teach are.",
           "evidence": {k: v["basis"] for k, v in COMPONENTS.items()},
           "limits": ["simulation evidence is for pre-licensure nursing at 50% of clinical hours; it is applied to all cadres",
                      "supervising trainees costs clinicians' time; the model does not subtract it from care delivered",
                      "children's schooling is NOT covered: school closures cost about 0.19 SD of learning (Di Pietro 2023, 39 "
                      "studies, 19 countries, VERIFIED); online theory is for adult and professional education",
                      "trainees rotating across regions need housing, travel and language support, not modelled"]}
    if write:
        (ROOT.parent / "outputs" / "training_capacity.json").write_text(json.dumps(out, indent=2))
        for k, r in res.items():
            y = r["years"]
            print(f"{k:44s} cap {r['intake_cap_multiple']['central']:>5}x  years low/central/high = {y['low']} / {y['central']} / {y['high']}")
        print("binding component:", {l: caps[l]["binding_component"] for l in caps})
    return out


if __name__ == "__main__":
    main()
