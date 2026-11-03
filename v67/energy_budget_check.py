"""Does the clean-energy build rate cover both convergence AND decarbonisation? (review question 'double use')
The transition model sends every new clean EJ to regions below 40 GJ. Here we measure how much of the
build convergence actually absorbs and how much remains to replace fossil supply in the rest of the world.
python3 energy_budget_check.py  ->  outputs/energy_budget_check.json"""
import json
from pathlib import Path

import run_transition as rt
import transition as tr

ROOT = Path(__file__).resolve().parent
# Share of today's world final energy already from non-fossil sources (electricity from hydro, nuclear, wind,
# solar; modern bioenergy; IEA World Energy Outlook 2024: ~19% of total final consumption)
CLEAN_SHARE_TODAY = 0.19


def main():
    cfg = json.loads((ROOT / "config.json").read_text())
    regions = rt.load_regions()
    cap = json.loads((rt.U / "v66" / "construction" / "capacity.json").read_text())
    out = {"clean_share_today_assumed": CLEAN_SHARE_TODAY, "cases": {}}
    real = tr.allocate_perceived
    for case, c in cfg["cases"].items():
        used = []

        def spy(pool, deficits, p, domain, t):
            g = real(pool, deficits, p, domain, t)
            if domain == "energy":
                used.append(sum(g.values()) / 1e9)
            return g
        tr.allocate_perceived = spy
        p = {"energy_target": cfg["energy_target_gj"], "health_target": cfg["health_target_per_10k"],
             "floor_target": cfg["floor_target_m2"], "excess_decline": c["excess_decline"],
             "energy_new_ej_per_yr": c["energy_new_ej_per_yr"], "health_net_new": rt.health_flow(c["health_capacity"]),
             "floor_new_m2_per_yr": cap[cfg["housing_capacity_key"]][c["housing"]] * c["housing_share_to_deficit"],
             "kcal_eaten": cfg["kcal_eaten"], "waste_now": cfg["waste_now"], "waste_unira": cfg["waste_unira"],
             "waste_years": cfg["waste_years"],
             "military_energy_share": c.get("military_energy_share", 0.0), "military_years": c.get("military_years", 0)}
        rows, _ = tr.run(regions, p, cfg["years"])
        tr.allocate_perceived = real
        built = c["energy_new_ej_per_yr"] * len(used)
        convergence = sum(used)
        world_y30 = rows[-1]["world_energy_ej"]
        need_fossil_free = world_y30 * (1 - CLEAN_SHARE_TODAY) - convergence
        out["cases"][case] = {
            "clean_built_ej_per_yr_by_y30": round(built, 1),
            "absorbed_by_convergence_ej": round(convergence, 1),
            "left_for_replacing_fossil_ej": round(built - convergence, 1),
            "world_final_energy_y30_ej": round(world_y30, 1),
            "fossil_still_to_replace_ej": round(need_fossil_free, 1),
            "clean_share_y30_if_all_build_is_clean": round(min(1.0, (world_y30 * CLEAN_SHARE_TODAY + built) / world_y30), 3)}
    (ROOT / "outputs" / "energy_budget_check.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
