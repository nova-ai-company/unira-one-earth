"""UNIRA V7.8 — Does AI forecasting improve what people actually receive?

The 30-year world transition (v67) is rerun with the One Earth allocator seeing needs through
different information systems. Unlike v69 (noise on the needs gap), errors here hit what is really
measured: each region's LEVEL (energy per person, health workers per 10,000, floor area per person)
and its POPULATION. The needs gap seen = max(0, target - level_seen) * population_seen.

    perfect                  true data, no delay (upper bound)
    statistics_today         v69 'strong safeguards': published statistics one year late, 5% noise
    ai_nowcast               no delay: an AI model forecasts this year from data two years old, with the
                             out-of-sample errors MEASURED in forecast.py (h = 2, chosen model)
    *_information_only, integrity_failures_only: the same losses split into their two causes
    ai_nowcast_metered       as ai_nowcast, but energy is metered per unit (rule 23) so its level error
                             is small (2%, assumption) and anomaly checks detect misreporting faster
                             (audit 0.5 -> 0.8, assumption)
Misreporting regions, audit and leakage are those of v69 'strong safeguards' in every imperfect case:
AI does not remove corruption. 30 random seeds each.
python3 information.py  ->  ../outputs/information.json"""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
sys.path[:0] = [str(U / "v68" / "counterfactual"), str(U / "v67"), str(U / "v66" / "model"), str(U / "v69" / "coordination")]
import compare  # noqa: E402
import model as coord  # noqa: E402
import transition as tr  # noqa: E402

OUT = HERE.parents[0] / "outputs"
SEEDS = 30
DOMAINS = {"energy": ("energy_gj", 40.0, 1.0), "health": ("health_10k", 131.0, 1e-4), "housing": ("floor_m2", 27.0, 1.0)}
NORMAL_MAD = 0.6745  # median |z| of a standard normal: sigma = median absolute error / 0.6745


def measured_sigmas(h=2):
    """Log-level error sigma per domain from the out-of-sample backtest (chosen model, all regions)."""
    bt = json.loads((OUT / "backtest.json").read_text())["results"]

    def sig(series):
        r = bt[series][f"h{h}"]
        return r["test"][r["chosen_on_validation"]]["median_ape"] / NORMAL_MAD
    return {"population": sig("population"), "energy": sig("energy_pc"),
            "health": 0.5 * (sig("doctors_10k") + sig("nurses_10k")),
            "housing": sig("energy_pc")}  # no floor-area time series: assume as uncertain as energy (assumption)


def level_perceiver(regions, gov, seed, holder):
    """Perceived gap from perturbed levels and population; misreporting as in v69."""
    rng = random.Random(seed)
    keys = sorted(regions)
    cheaters = set(rng.sample(keys, int(round(gov["misreport_share"] * len(keys)))))

    def perceive(domain, t, true_def):
        st = holder["p"]["_state"]
        key, target, unit = DOMAINS[domain]
        for k in sorted(cheaters):  # sorted: same random draws on every run
            if rng.random() < gov["audit_detect"]:
                cheaters.discard(k)
        seen = {}
        for k in keys:
            r = st[k]
            lvl = r[key] * math.exp(rng.gauss(-gov["sigma_level"][domain] ** 2 / 2, gov["sigma_level"][domain]))
            pop = r["pop"] * math.exp(rng.gauss(-gov["sigma_pop"] ** 2 / 2, gov["sigma_pop"]))
            d = max(0.0, target - lvl) * unit * pop
            if k in cheaters:
                d = d * (1 + gov["inflation"]) + (gov["inflation"] * 0.05 * max(true_def.values()) if d == 0 else 0.0)
            seen[k] = d
        return seen
    return perceive


def world(s, regions, cfg, cap, gov, seed):
    sh = cfg["shared"]
    p = {"energy_target": 40, "health_target": 131, "floor_target": 27,
         "excess_decline": s["rich_region_energy_decline"], "energy_new_ej_per_yr": sh["energy_new_ej_per_yr"],
         "energy_share_to_deficit": s["energy_share_to_regions_in_need"],
         "health_net_new": compare.health_flow(s["health_plan"]), "health_share_to_deficit": s["health_share_to_regions_in_need"],
         "floor_new_m2_per_yr": cap["world_res_floor_added_m2_per_yr"][sh["housing_capacity"]] * s["housing_share_to_regions_in_need"],
         "kcal_eaten": {"decent": 2100, "comfortable": 2470}, "waste_now": 0.19, "waste_unira": 0.095, "waste_years": 10,
         "military_energy_share": s["military_energy_share_freed"], "military_years": 5, "leakage": gov.get("leakage", 0.0)}
    if "sigma_level" in gov:
        holder = {"p": p}
        p["perceive"] = level_perceiver(regions, gov, seed, holder)
    elif gov.get("sigma", 0) or gov.get("lag", 0) or gov.get("misreport_share", 0):
        p["perceive"] = coord.make_perceiver(regions, gov, seed)
    rows, _ = tr.run(regions, p, 30)
    first = lambda dom: next((r["year"] for r in rows if r[f"{dom}_share_pop_at_target"] >= 0.999), None)
    return {"energy_closed_y15": rows[15]["energy_shortfall_closed"], "health_closed_y15": rows[15]["health_shortfall_closed"],
            "housing_closed_y30": rows[30]["housing_shortfall_closed"], "energy_all_by": first("energy"),
            "health_all_by": first("health")}


def scenarios():
    strong = json.loads((U / "v69" / "coordination" / "config.json").read_text())["scenarios"]["C_strong_safeguards"]
    sg = measured_sigmas()
    common = {k: strong[k] for k in ("misreport_share", "inflation", "audit_detect", "leakage")}
    return {"perfect": {"sigma": 0.0, "lag": 0, "misreport_share": 0.0, "inflation": 0.0, "audit_detect": 0.0, "leakage": 0.0},
            "statistics_today": dict(strong),
            "ai_nowcast": {**common, "sigma_level": {d: sg[d] for d in DOMAINS}, "sigma_pop": sg["population"]},
            "ai_nowcast_metered": {**common, "audit_detect": 0.8,
                                   "sigma_level": {"energy": 0.02, "health": sg["health"], "housing": sg["housing"]},
                                   "sigma_pop": sg["population"]},
            # decomposition: information errors alone (no misreporting, no leakage)
            "statistics_information_only": {**strong, "misreport_share": 0.0, "inflation": 0.0, "leakage": 0.0},
            "ai_information_only": {"misreport_share": 0.0, "inflation": 0.0, "audit_detect": 0.0, "leakage": 0.0,
                                    "sigma_level": {d: sg[d] for d in DOMAINS}, "sigma_pop": sg["population"]},
            # decomposition: misreporting and leakage alone (perfect information)
            "integrity_failures_only": {"sigma": 0.0, "lag": 0, **common}}


def summarise(runs):
    out = {}
    for m in runs[0]:
        vals = [r[m] for r in runs]
        if m.endswith("_by"):
            got = [v for v in vals if v is not None]
            out[m] = {"share_of_runs_reached": len(got) / len(vals), "median_year": coord.quantiles(got)[1] if got else None}
        else:
            out[m] = dict(zip(("p10", "p50", "p90"), coord.quantiles(vals)))
    return out


def main():
    cfg = compare.load_config()
    regions = compare.rt.load_regions()
    cap = json.loads((U / "v66" / "construction" / "capacity.json").read_text())
    s = compare.settings(cfg, {k: "C" for k in cfg["lever_order"]})
    scen = scenarios()
    res = {"measured_sigmas_h2": measured_sigmas(), "scenarios": scen, "results": {}}
    for name, gov in scen.items():
        n = 1 if name == "perfect" else SEEDS
        res["results"][name] = summarise([world(s, regions, cfg, cap, gov, seed) for seed in range(n)])
        r = res["results"][name]
        print(f"{name:20s} energy y15 {100 * r['energy_closed_y15']['p50']:.1f}%  health y15 {100 * r['health_closed_y15']['p50']:.1f}%"
              f"  housing y30 {100 * r['housing_closed_y30']['p50']:.1f}%  energy all by {r['energy_all_by']['median_year']}"
              f"  health all by {r['health_all_by']['median_year']}")
    # what integrity is worth: same misreporting as 'strong safeguards', leakage varied, AI information
    res["leakage_sensitivity"] = {}
    for lk in (0.0, 0.02, 0.04, 0.08, 0.15):
        gov = {**scen["ai_nowcast"], "leakage": lk}
        r = summarise([world(s, regions, cfg, cap, gov, seed) for seed in range(SEEDS)])
        res["leakage_sensitivity"][str(lk)] = {m: r[m]["p50"] for m in ("energy_closed_y15", "health_closed_y15", "housing_closed_y30")}
        print(f"leakage {lk:.2f}: " + "  ".join(f"{m} {100 * v:.1f}%" for m, v in res["leakage_sensitivity"][str(lk)].items()))
    perfect = res["results"]["perfect"]
    for name, r in res["results"].items():
        r["share_of_perfect"] = {m: r[m]["p50"] / perfect[m]["p50"] for m in ("energy_closed_y15", "health_closed_y15", "housing_closed_y30")}
    OUT.mkdir(exist_ok=True)
    (OUT / "information.json").write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
