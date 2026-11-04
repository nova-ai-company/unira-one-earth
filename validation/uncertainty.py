"""Joint uncertainty propagation for the headline results (validation, not a new model).

Earlier versions report scenarios (low / central / high) and one-at-a-time sensitivity tests. Here every uncertain
assumption of three models is sampled TOGETHER, with a fixed random seed, and the outcome distribution is reported
with the rank correlation of each input and each outcome (which assumptions drive the result).
  v67  the 30-year world transition (energy, health workers, housing): 2,000 samples
       inputs: clean-energy build 3.9-10.5 EJ/yr (0.67-1.8 TW), health training plan low/central/high, home building
       low/central/high and the share sent to regions in deficit 0.5-0.9, rich-region energy decline 2-5%/yr,
       food waste after the transition 9.5-19%, military energy freed or not
  v89  the integrated living standard (Level 1 and Level 2 dates): 400 samples
       inputs: v87 delivery scenario, access-gain percentile 0.5-0.95, automation by year 30 0.1-0.6, local-services
       catch-up 0.02-0.06, car production growth 0-6%/yr and shared-car share 0.3-0.7, first-year functioning of new
       water 0.75-0.95 and sanitation/cooking 0.85-0.98, mature functioning 0.95-0.995 over 10-25 years, Level 2
       local services 0.5-0.8 of France's, share lacking shared cars 0.5-0.7, delivery factor in conflict 0.3-0.7 and
       in fragility 0.6-0.9
  v91  institutional reform and conflict (scenario C against its own baseline A): 40 samples x 2 random draws
       inputs: causal fractions cQ 0.25-1 and cE 0-1, reform pace p75/p90/p95, reversal 0.15-0.5, tension 0-1,
       mediation 0-0.15, ending boost 0-0.5, relapse cut 0-0.5, mediation relapse penalty 0-0.3
Dates not reached are coded as the horizon + 1 (31 or 81) for the quantiles and correlations.
python3 uncertainty.py -> outputs/uncertainty.json (about 5 minutes)"""
import importlib.util
import json
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parent
sys.path.insert(0, str(HERE))
from backtest import spearman  # noqa: E402

N67, N89, N91 = 2000, 400, 40


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def quantiles(v):
    v = sorted(v)
    q = lambda f: v[min(len(v) - 1, int(f * (len(v) - 1) + 0.5))]
    return {"p5": q(0.05), "p25": q(0.25), "median": q(0.5), "p75": q(0.75), "p95": q(0.95)}


def drivers(samples, inputs, outcome):
    y = [s["out"][outcome] for s in samples]
    rows = []
    for name in inputs:
        x = [s["in"][name] for s in samples]
        if isinstance(x[0], str):
            cats = sorted(set(x))
            x = [cats.index(v) for v in x]
        rows.append((name, round(spearman(x, y), 3)))
    return sorted(rows, key=lambda r: -abs(r[1]))


def summarise(samples, inputs, outcomes, horizon):
    out = {"n": len(samples), "outcomes": {}, "drivers": {}}
    for o in outcomes:
        vals = [s["out"][o] for s in samples]
        if all(isinstance(v, (int, float)) or v is None for v in vals) and any(v is None for v in vals):
            coded = [horizon + 1 if v is None else v for v in vals]
            out["outcomes"][o] = quantiles(coded) | {"share_reached_within_horizon": round(sum(v is not None for v in vals) / len(vals), 3)}
            for s in samples:
                s["out"][o] = horizon + 1 if s["out"][o] is None else s["out"][o]
        else:
            out["outcomes"][o] = quantiles(vals)
        out["drivers"][o] = drivers(samples, inputs, o)
    return out


def run67():
    sys.path[:0] = [str(U / "v67"), str(U / "v66" / "model")]
    import run_transition as R  # noqa: E402
    import transition as tr  # noqa: E402
    cfg = json.loads((U / "v67" / "config.json").read_text())
    regions = R.load_regions()
    cap = json.loads((U / "v66" / "construction" / "capacity.json").read_text())[cfg["housing_capacity_key"]]
    hf = {lab: R.health_flow(lab) for lab in ("low", "central", "high")}
    rng = random.Random(67)
    samples = []
    for _ in range(N67):
        x = {"energy_new_ej_per_yr": round(rng.uniform(3.9, 10.5), 3), "health_capacity": rng.choice(["low", "central", "high"]),
             "housing_capacity": rng.choice(["low", "central", "high"]), "housing_share_to_deficit": round(rng.uniform(0.5, 0.9), 3),
             "excess_decline": round(rng.uniform(0.02, 0.05), 4), "waste_unira": round(rng.uniform(0.095, 0.19), 4),
             "military_energy_freed": rng.choice([0, 1])}
        p = {"energy_target": cfg["energy_target_gj"], "health_target": cfg["health_target_per_10k"], "floor_target": cfg["floor_target_m2"],
             "excess_decline": x["excess_decline"], "energy_new_ej_per_yr": x["energy_new_ej_per_yr"], "health_net_new": hf[x["health_capacity"]],
             "floor_new_m2_per_yr": cap[x["housing_capacity"]] * x["housing_share_to_deficit"], "kcal_eaten": cfg["kcal_eaten"],
             "waste_now": cfg["waste_now"], "waste_unira": x["waste_unira"], "waste_years": cfg["waste_years"],
             "military_energy_share": 0.055 if x["military_energy_freed"] else 0.0, "military_years": 5 if x["military_energy_freed"] else 0}
        rows, _ = tr.run(regions, p, cfg["years"])
        o = {f"year_all_{d}": next((r["year"] for r in rows if r[f"{d}_share_pop_at_target"] >= 0.999), None) for d in ("energy", "health", "housing")}
        o |= {"peak_world_energy_ej": round(max(r["world_energy_ej"] for r in rows), 1),
              "energy_shortfall_closed_y15": round(rows[15]["energy_shortfall_closed"], 3),
              "health_shortfall_closed_y15": round(rows[15]["health_shortfall_closed"], 3),
              "housing_shortfall_closed_y30": round(rows[-1]["housing_shortfall_closed"], 3)}
        samples.append({"in": x, "out": o})
    res = summarise(samples, list(samples[0]["in"]), list(samples[0]["out"]), 30)
    res["probability"] = {"energy_for_all_within_30y": round(sum(s["out"]["year_all_energy"] <= 30 for s in samples) / N67, 3),
                          "health_for_all_within_30y": round(sum(s["out"]["year_all_health"] <= 30 for s in samples) / N67, 3),
                          "housing_for_all_within_30y": round(sum(s["out"]["year_all_housing"] <= 30 for s in samples) / N67, 3),
                          "peak_energy_at_or_below_409_ej": round(sum(s["out"]["peak_world_energy_ej"] <= 409 for s in samples) / N67, 3)}
    return res


def run89():
    S = load("v89u", U / "v89" / "integrated" / "simulate.py")
    ctx = S.context()
    status = ctx["status"]
    keep = {k: getattr(S, k) for k in ("DURABLE", "MATURE", "MATURE_YEARS", "SERVICES_L2", "CAR_LACKING")}
    rng = random.Random(89)
    samples = []
    try:
        for _ in range(N89):
            x = {"v87_scenario": rng.choice(["conservative", "moderate", "accelerated"]), "access_pctl": round(rng.uniform(0.5, 0.95), 3),
                 "auto30": round(rng.uniform(0.1, 0.6), 3), "service_catch_up": round(rng.uniform(0.02, 0.06), 4),
                 "car_growth": round(rng.uniform(0.0, 0.06), 4), "car_share": round(rng.uniform(0.3, 0.7), 3),
                 "durable_water": round(rng.uniform(0.75, 0.95), 3), "durable_sanitation_cooking": round(rng.uniform(0.85, 0.98), 3),
                 "mature": round(rng.uniform(0.95, 0.995), 4), "mature_years": rng.randint(10, 25),
                 "services_L2": round(rng.uniform(0.5, 0.8), 3), "car_lacking": round(rng.uniform(0.5, 0.7), 3),
                 "gov_conflict": round(rng.uniform(0.3, 0.7), 3), "gov_fragile": round(rng.uniform(0.6, 0.9), 3)}
            S.DURABLE = {"water": x["durable_water"], "sanitation": x["durable_sanitation_cooking"], "clean_cooking": x["durable_sanitation_cooking"]}
            S.MATURE, S.MATURE_YEARS, S.SERVICES_L2, S.CAR_LACKING = x["mature"], x["mature_years"], x["services_L2"], x["car_lacking"]
            sc = {"v87": x["v87_scenario"], "access_pctl": x["access_pctl"], "auto30": x["auto30"], "service_catch_up": x["service_catch_up"],
                  "car_growth": x["car_growth"], "car_share": x["car_share"]}
            gov = {"conflict": x["gov_conflict"], "fragile": x["gov_fragile"]}
            r = S.core(ctx, sc, lambda k, t, gov=gov: gov.get(status.get(k, "other"), 1.0))
            o = {f"{L}_{q}": r["dates"][L][q] for L in ("L1", "L2") for q in ("90pct", "95pct", "99pct")}
            samples.append({"in": x, "out": o})
    finally:
        for k, v in keep.items():
            setattr(S, k, v)
    return summarise(samples, list(samples[0]["in"]), list(samples[0]["out"]), 80)


def run91():
    M = load("v91u", U / "v91" / "institutions" / "model.py")
    w = M.World()
    w.calibrate()
    rng = random.Random(91)
    samples = []
    for _ in range(N91):
        x = {"cQ": round(rng.uniform(0.25, 1.0), 3), "cE": round(rng.uniform(0.0, 1.0), 3), "pace": rng.choice(["p75", "p90", "p95"]),
             "reversal": round(rng.uniform(0.15, 0.5), 3), "tension": round(rng.uniform(0.0, 1.0), 3), "mediation": round(rng.uniform(0.0, 0.15), 3),
             "end_boost": round(rng.uniform(0.0, 0.5), 3), "relapse_cut": round(rng.uniform(0.0, 0.5), 3),
             "mediation_relapse": round(rng.uniform(0.0, 0.3), 3)}
        pA = M.SCEN["A_baseline"] | {"cE": x["cE"]}
        pC = M.COMMON | {"cE": x["cE"], "cQ": x["cQ"], "pace": x["pace"], "reversal": x["reversal"], "tension": x["tension"],
                         "mediation": x["mediation"], "end_boost": x["end_boost"], "relapse_cut": x["relapse_cut"],
                         "mediation_relapse": x["mediation_relapse"]}
        cyA, cyC, l1 = [], [], []
        for seed in (0, 1):
            cpath, *_ = M.run(w, pA, seed)
            cyA.append(sum(sum(v) for v in cpath.values()))
            cpath, _, _, res, _ = M.run(w, pC, seed)
            cyC.append(sum(sum(v) for v in cpath.values()))
            l1.append(M.V90.dates_from(res["cov"]["L1"])["99pct"])
        o = {"share_conflict_years_avoided_C_vs_A": round(1 - statistics.fmean(cyC) / statistics.fmean(cyA), 3),
             "L1_99pct_year_C": None if any(v is None for v in l1) else round(statistics.fmean(l1))}
        samples.append({"in": x, "out": o})
    return summarise(samples, list(samples[0]["in"]), list(samples[0]["out"]), 80)


def main(write=True, n67=N67, n89=N89, n91=N91):
    global N67, N89, N91
    N67, N89, N91 = n67, n89, n91
    out = {"v67_transition": run67(), "v89_living_standard": run89(), "v91_institutions_and_conflict": run91()}
    for name, r in out.items():
        print(f"\n== {name} ({r['n']} samples)")
        for o, q in r["outcomes"].items():
            print(f"   {o:36s} median {q['median']}  5-95%: {q['p5']}-{q['p95']}" + (f"  reached {100 * q['share_reached_within_horizon']:.0f}%" if "share_reached_within_horizon" in q else ""))
            print(f"      drivers: " + ", ".join(f"{k} {v:+.2f}" for k, v in r["drivers"][o][:4]))
        if "probability" in r:
            print("   probability:", r["probability"])
    if write:
        (HERE / "outputs").mkdir(exist_ok=True)
        (HERE / "outputs" / "uncertainty.json").write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main()
