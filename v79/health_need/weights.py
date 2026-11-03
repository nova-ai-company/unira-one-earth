"""UNIRA V7.9 — how should health need be weighted between regions? (Article 10a.2)

Health workers are allocated needs-first (decent level first) in the 30-year world plan. The comfortable target
(131 health workers per 10,000) and the decent target (44.5) are scaled by a regional need weight (mean 1):
    equal            every person counts the same (no adjustment)
    age_2x/3x/4x     people 65+ count 2, 3 or 4 times (age structure only, World Bank SP.POP.65UP.TO.ZS)
    health_gap       years of healthy life lost: 88 - healthy life expectancy at birth (WHO HALE, latest year).
                     A proxy for the burden of disease and early death (DALYs per person); all-cause DALYs by
                     country are not available as open, redistributable data.
    combined         mean of age_3x and health_gap
Measured: the share of all new health workers each World Bank region receives over 30 years, density reached by
year 30, and when every region reaches its decent level.
python3 weights.py  ->  ../outputs/health_need.json"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
sys.path.insert(0, str(U / "v79" / "allocation"))
import formula  # noqa: E402

REF_LIFE = 88.0  # SYNTHETIC_ASSUMPTION: reference healthy lifespan (close to the highest life expectancies observed)


def hale():
    out = {}
    for x in json.loads((HERE / "data" / "raw" / "who_WHOSIS_000002.json").read_text())["value"]:
        if x["DIMENSION_MEMBER_1"] == "BTSX" and x["LOCATION_TYPE"] == "COUNTRY" and x["VALUE_NUMERIC"] is not None:
            y = int(x["PERIOD_CODE"])
            if y >= out.get(x["LOCATION_CODE"], (0, 0))[0]:
                out[x["LOCATION_CODE"]] = (y, x["VALUE_NUMERIC"])
    return {k: v for k, (_, v) in out.items()}


def normalise(w, regions):
    mean = sum(w[k] * regions[k]["pop0"] for k in regions) / sum(r["pop0"] for r in regions.values())
    return {k: v / mean for k, v in w.items()}


def age_weights(regions, factor):
    s = formula.share65()
    return normalise({k: (1 - s.get(k, 0.1)) + factor * s.get(k, 0.1) for k in regions}, regions)


def gap_weights(regions):
    h = hale()
    known = [h[k] for k in regions if k in h]
    fill = sorted(known)[len(known) // 2]  # median for the few regions without WHO data
    return normalise({k: REF_LIFE - h.get(k, fill) for k in regions}, regions)


def wb_regions():
    meta = json.loads((U / "v65" / "data" / "raw" / "wb_country_meta.json").read_text())[1]
    return {m["id"]: m["region"]["value"].strip() for m in meta}


def main():
    cfg = formula.compare.load_config()
    regions = formula.compare.rt.load_regions()
    cap = json.loads((U / "v66" / "construction" / "capacity.json").read_text())
    s = formula.compare.settings(cfg, {k: "C" for k in cfg["lever_order"]})
    wr = wb_regions()
    groups = sorted({wr.get(k, "other") for k in regions})
    pop = {g: sum(regions[k]["pop0"] for k in regions if wr.get(k, "other") == g) for g in groups}
    world_pop = sum(pop.values())
    a3, gw = age_weights(regions, 3.0), gap_weights(regions)
    schemes = {"equal": {k: 1.0 for k in regions}, "age_2x": age_weights(regions, 2.0), "age_3x": a3,
               "age_4x": age_weights(regions, 4.0), "health_gap": gw,
               "combined": normalise({k: 0.5 * (a3[k] + gw[k]) for k in regions}, regions)}
    out = {"reference_healthy_life_years": REF_LIFE, "population_share": {g: round(pop[g] / world_pop, 3) for g in groups},
           "schemes": {}}
    for name, w in schemes.items():
        r = formula.run(regions, s, True, False, cfg, cap, weights=w)
        given, final = r.pop("_health_given"), r.pop("_final")
        tot = sum(given.values())
        share = {g: round(sum(given[k] for k in regions if wr.get(k, "other") == g) / tot, 3) for g in groups}
        dens = {g: round(sum(final[k]["health_10k"] * final[k]["pop"] for k in regions if wr.get(k, "other") == g)
                         / sum(final[k]["pop"] for k in regions if wr.get(k, "other") == g), 1) for g in groups}
        wavg = {g: round(sum(w[k] * regions[k]["pop0"] for k in regions if wr.get(k, "other") == g) / pop[g], 2) for g in groups}
        out["schemes"][name] = {"weight_by_region": wavg, "share_of_new_health_workers": share,
                                "health_workers_per_10k_year30": dens,
                                "year_every_region_decent_health": r["year_everyone_decent"]["health"],
                                "person_years_below_decent_health_bn": r["person_years_below_decent_bn"]["health"]}
        ssa = "Sub-Saharan Africa"
        print(f"{name:11s} weight SSA {wavg.get(ssa)} EUR {wavg.get('Europe & Central Asia')} | new workers to SSA "
              f"{100 * share.get(ssa, 0):.0f}% S.Asia {100 * share.get('South Asia', 0):.0f}% Europe {100 * share.get('Europe & Central Asia', 0):.0f}% "
              f"| density yr30 SSA {dens.get(ssa)} Europe {dens.get('Europe & Central Asia')} | all decent by yr {r['year_everyone_decent']['health']}")
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "health_need.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
