"""UNIRA V6.6: global health-workforce plan to an EU-like 131 per 10,000 for everyone (python3 run_health.py)."""
import csv
import json
from pathlib import Path

import health_plan as hp

ROOT = Path(__file__).resolve().parent
U = ROOT.parents[1]


def world_inputs():
    v65 = json.loads((U / "v65" / "outputs" / "world_sufficiency.json").read_text())
    stock0 = v65["domains"]["health|comfortable"]["world_workers"]
    wld = {r["indicator_id"]: float(r["value"]) for r in csv.DictReader((ROOT.parent / "data" / "indicators_v66.csv").open())
           if r["iso3"] == "WLD"}
    prev = json.loads((ROOT.parent / "evidence_health" / "parameters.json").read_text())["preventable_share"]
    return stock0, wld, prev


def scenarios(stock0, wld, prev):
    pop = {0: wld["pop_total"], 26: wld["pop_total_2050_wpp2024_medium"] * 1e3}
    mil = wld["armed_forces_personnel"]
    prev_c = {0: 0.0, 5: prev["y5"][1], 15: prev["y15"][1], 30: prev["y30"][1]}
    prev_h = {0: 0.0, 5: prev["y5"][2], 15: prev["y15"][2], 30: prev["y30"][2]}
    common = {"stock0": stock0, "lead_time": 4, "exit_rate": 0.03, "tau_per_10k": 131.0, "population": pop,
              "intake_capacity_multiple": 3.0, "conversion_years": 5}
    none = {0: 0.0}
    out = {}
    for label, share in (("low", 0.03), ("central", 0.045), ("high", 0.06)):
        base = dict(common, base_intake=share * stock0)
        out[f"{label}|1_status_quo_training"] = dict(base, expansion=0.0, ramp_years=0, military_pool=0.0,
                                                    military_volunteer_share=0.0, preventable_share=none)
        out[f"{label}|2_expand_training_7pct_15y"] = dict(base, expansion=0.07, ramp_years=15, military_pool=0.0,
                                                         military_volunteer_share=0.0, preventable_share=none)
        out[f"{label}|3_plus_disarmament_25pct_volunteer"] = dict(out[f"{label}|2_expand_training_7pct_15y"],
                                                                 military_pool=mil, military_volunteer_share=0.25)
        out[f"{label}|4_plus_prevention_central"] = dict(out[f"{label}|3_plus_disarmament_25pct_volunteer"],
                                                        preventable_share=prev_c)
        out[f"{label}|5_ambitious_10pct_50pct_prevention_high"] = dict(base, expansion=0.10, ramp_years=15,
                                                                       military_pool=mil, military_volunteer_share=0.5,
                                                                       preventable_share=prev_h)
    return out


def main():
    stock0, wld, prev = world_inputs()
    res, rows_all = {}, []
    for name, p in scenarios(stock0, wld, prev).items():
        rows, closed = hp.simulate(p, 80)
        res[name] = {"years_to_close": closed, "need_y26": rows[26]["need"], "stock_y26": rows[26]["stock"],
                     "per_10k_y10": rows[10]["per_10k"], "per_10k_y26": rows[26]["per_10k"]}
        rows_all += [{"scenario": name, **r} for r in rows]
    out = ROOT.parent / "outputs"
    out.mkdir(exist_ok=True)
    (out / "health_plan.json").write_text(json.dumps({"stock0": stock0, "results": res,
        "assumptions": {"base_intake_share_of_stock": "3/4.5/6% MODEL_DERIVED from OECD graduates per worker (~5.4-6.0/100), lower for world",
                        "exit_rate": "3%/yr MODEL_DERIVED (France nurses 3.3%)", "lead_time": "4 yr weighted nurses 3 / doctors 6-9 (REPORTED_NEEDS_RECHECK)",
                        "training_capacity_cap": "3x today's intake (teachers, schools) SYNTHETIC",
                        "military_volunteers": "25% / 50% of 27.4 m armed forces volunteer over 5 years (SYNTHETIC; voluntary)",
                        "population_after_2050": "held at 2050 level (SYNTHETIC; UN WPP peak ~2080s)"}}, indent=2))
    with (out / "health_plan_annual.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_all[0]))
        w.writeheader()
        w.writerows(rows_all)
    for k, r in res.items():
        print(f"{k:50s} closes in {r['years_to_close']} yrs | per10k y10={r['per_10k_y10']:.0f} y26(2050)={r['per_10k_y26']:.0f}")


if __name__ == "__main__":
    main()
