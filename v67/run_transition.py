"""UNIRA V6.7: run the 30-year world transition plan (python3 run_transition.py)."""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
U = ROOT.parent
sys.path[:0] = [str(ROOT), str(U / "v66" / "model")]
import health_plan as hp  # noqa: E402
import run_health  # noqa: E402
import transition as tr  # noqa: E402

SHOW = ["FRA", "USA", "DEU", "CHN", "BRA", "IND", "NGA", "ETH", "COD", "PAK"]


def load_regions():
    v = {}
    for path in (U / "v65" / "data" / "world_indicators.csv", U / "v66" / "data" / "indicators_v66.csv"):
        for r in csv.DictReader(path.open()):
            if r["iso3"] != "WLD":
                v[(r["iso3"], r["indicator_id"])] = float(r["value"])
    conv = json.loads((U / "v65" / "model" / "config.json").read_text())["energy"]["primary_to_final"]["value"]
    regions = {}
    for iso in {k[0] for k in v if k[1] == "pop_total"}:
        need = ["pop_total", "pop_total_2050_wpp2024_medium", "energy_primary_kwh_per_cap", "doctors_per_10k",
                "nurses_midwives_per_10k", "floor_area_res_m2_per_cap_image_region", "food_kcal_per_cap_day"]
        if all((iso, n) in v for n in need):
            regions[iso] = {"pop0": v[(iso, "pop_total")], "pop50": v[(iso, "pop_total_2050_wpp2024_medium")] * 1e3,
                            "energy_gj": v[(iso, "energy_primary_kwh_per_cap")] * 0.0036 * conv,
                            "health_10k": v[(iso, "doctors_per_10k")] + v[(iso, "nurses_midwives_per_10k")],
                            "floor_m2": v[(iso, "floor_area_res_m2_per_cap_image_region")],
                            "kcal": v[(iso, "food_kcal_per_cap_day")]}
    return regions


def health_flow(label="central", scenario="5_ambitious_10pct_50pct_prevention_high"):
    stock0, wld, prev = run_health.world_inputs()
    p = run_health.scenarios(stock0, wld, prev)[f"{label}|{scenario}"]
    rows, _ = hp.simulate(p, 40)
    d = [rows[t + 1]["stock"] - rows[t]["stock"] for t in range(40)]
    return lambda t: max(0.0, d[min(t, 39)])


def main():
    cfg = json.loads((ROOT / "config.json").read_text())
    regions = load_regions()
    cap = json.loads((U / "v66" / "construction" / "capacity.json").read_text())
    floor_key = cfg["housing_capacity_key"]
    results = {}
    for case, c in cfg["cases"].items():
        p = {"energy_target": cfg["energy_target_gj"], "health_target": cfg["health_target_per_10k"],
             "floor_target": cfg["floor_target_m2"], "excess_decline": c["excess_decline"],
             "energy_new_ej_per_yr": c["energy_new_ej_per_yr"], "health_net_new": health_flow(c["health_capacity"]),
             "floor_new_m2_per_yr": cap[floor_key][c["housing"]] * c["housing_share_to_deficit"],
             "kcal_eaten": cfg["kcal_eaten"], "waste_now": cfg["waste_now"], "waste_unira": cfg["waste_unira"],
             "waste_years": cfg["waste_years"],
             "military_energy_share": c.get("military_energy_share", 0.0), "military_years": c.get("military_years", 0)}
        rows, reached = tr.run(regions, p, cfg["years"])
        first_all = {}
        for dom in ("energy", "health", "housing"):
            first_all[dom] = next((r["year"] for r in rows if r[f"{dom}_share_pop_at_target"] >= 0.999), None)
        first_all["food"] = next((r["year"] for r in rows if r["food_comfortable_for_all_feasible"]), None)
        results[case] = {"peak_world_energy_ej": max(r["world_energy_ej"] for r in rows),
                         "world_energy_ej_y30": rows[-1]["world_energy_ej"], "timeline": rows, "year_all_regions_reach": first_all,
                         "regions": {iso: reached.get(iso, {}) for iso in SHOW},
                         "params": {k: (v if not callable(v) else "health_plan flow") for k, v in p.items()}}
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    (out / "transition.json").write_text(json.dumps({"regions_modelled": len(regions), "results": results}, indent=2))
    with (out / "transition_timeline.csv").open("w", newline="") as f:
        keys = ["case"] + list(results["central"]["timeline"][0])
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for case, r in results.items():
            for row in r["timeline"]:
                w.writerow({"case": case, **{k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items()}})
    print("regions modelled:", len(regions))
    for case, r in results.items():
        print(case, "year everyone reaches:", r["year_all_regions_reach"])
        for y in (0, 10, 20, 30):
            t = r["timeline"][y]
            print(f"   year {y:2d}: closed energy {t['energy_shortfall_closed']*100:5.1f}% health {t['health_shortfall_closed']*100:5.1f}% "
                  f"housing {t['housing_shortfall_closed']*100:5.1f}% | at target E {t['energy_share_pop_at_target']*100:4.0f}% "
                  f"H {t['health_share_pop_at_target']*100:4.0f}% F {t['housing_share_pop_at_target']*100:4.0f}% | world energy {t['world_energy_ej']:.0f} EJ")
        print("   regions:", {k: v for k, v in r["regions"].items()})


if __name__ == "__main__":
    main()
