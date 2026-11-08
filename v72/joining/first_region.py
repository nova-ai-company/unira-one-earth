"""UNIRA V7.2 — which region could be first, and what would a one-member UNIRA be exposed to? (author, 2026-11-08)

The concept's fatal gap 5: no region has a reason to be first until it is shown that one member can run the U, fixed
prices and needs-based allocation while trading with a market world. This module does the screening part with the
project's data, region by region (179 regions):
  - material gain from joining (V7.2: 146 regions gain, 33 lose);
  - not in armed conflict today (World Bank FCS FY26 list, v88 raw data);
  - institutions at or above the world average (mean of four Worldwide Governance Indicators, v91 raw data);
  - border exposure: imports of goods and services as a share of GDP (World Bank NE.IMP.GNFS.ZS, frozen here);
  - people: share of the population better off at the UNIRA base salary (V7.4), and a minimum size.
It also summarises the exposure channels a first member faces: import dependence (the Trade Office must earn the foreign
currency), capital flight before the vote (money abroad is simply not converted; it does not remove workers or plants),
skilled emigration (the share of people who lose at the base salary), and smuggling (price wedge x openness, the wedge
not measurable here). It is a screen, not a prediction: it says where the conditions are least bad, not that a region
would vote to join.  python3 first_region.py  ->  ../outputs/first_region.json
"""
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
U = ROOT.parents[1]
sys.path[:0] = [str(U / "v68" / "counterfactual"), str(U / "v67"), str(U / "v66" / "model")]
import compare  # noqa: E402

WGI = ("GOV_WGI_VA.EST", "GOV_WGI_RL.EST", "GOV_WGI_CC.EST", "GOV_WGI_GE.EST")
SCREENS = {
    "material_gainer": "region gains materially from joining at year 30 (V7.2, not in the 33 losers)",
    "not_in_conflict": "not on the World Bank FCS FY26 conflict list",
    "institutions_above_world_average": "mean of WGI voice, rule of law, control of corruption and government effectiveness >= 0",
    "import_share_at_or_below_median_of_gainers": "imports of goods and services, % of GDP, at or below the median of gaining regions",
    "population_at_least_5_million": "large enough to run an economy of its own",
    "at_least_90pct_better_off_at_base_salary": "share of people better off at the lowest UNIRA salary >= 0.9 (V7.4)",
}


def latest(path):
    out = {}
    for r in json.loads(Path(path).read_text())[1]:
        if r["value"] is None or not r["countryiso3code"]:
            continue
        k = r["countryiso3code"]
        if k not in out or r["date"] > out[k][0]:
            out[k] = (r["date"], float(r["value"]))
    return {k: v for k, (d, v) in out.items()}


def main(write=True):
    regions = compare.rt.load_regions()
    losers = set(json.loads((U / "v72" / "outputs" / "joining.json").read_text())["losers_all"])  # dict keyed by region code
    fcs = json.loads((U / "v88" / "essential" / "data" / "raw" / "fcs_fy26.json").read_text())
    conflict, fragile = set(fcs["conflict"]), set(fcs["institutional_social_fragility"])
    wgi = [latest(U / "v91" / "institutions" / "data" / "raw" / f"wb_{c}.json") for c in WGI]
    imports = latest(ROOT / "data" / "raw" / "wb_NE.IMP.GNFS.ZS.json")
    better = {k: v["share_of_people_better_off_at_base"]
              for k, v in json.loads((U / "v74" / "outputs" / "distribution_world.json").read_text())["regions"].items()}
    gainers = [k for k in regions if k not in losers]
    med_imp = statistics.median(imports[k] for k in gainers if k in imports)
    rows = []
    for k, v in regions.items():
        w = [x[k] for x in wgi if k in x]
        wmean = sum(w) / len(w) if len(w) == len(WGI) else None
        r = {"region": k, "pop_m": round(v["pop0"] / 1e6, 1), "material_gainer": k not in losers,
             "in_conflict": k in conflict, "fragile": k in fragile, "wgi_mean": None if wmean is None else round(wmean, 2),
             "imports_pct_gdp": None if k not in imports else round(imports[k], 1),
             "share_better_off_at_base": better.get(k)}
        passes = {"material_gainer": r["material_gainer"], "not_in_conflict": not r["in_conflict"],
                  "institutions_above_world_average": wmean is not None and wmean >= 0,
                  "import_share_at_or_below_median_of_gainers": k in imports and imports[k] <= med_imp,
                  "population_at_least_5_million": v["pop0"] >= 5e6,
                  "at_least_90pct_better_off_at_base_salary": better.get(k) is not None and better[k] >= 0.9}
        r["passes"] = passes
        r["screens_passed"] = sum(passes.values())
        rows.append(r)
    passing = [r for r in rows if all(r["passes"].values())]
    passing.sort(key=lambda r: (-r["wgi_mean"], r["imports_pct_gdp"]))
    near = [r for r in rows if r["screens_passed"] == len(SCREENS) - 1 and r["material_gainer"] and not r["in_conflict"]]
    gain_imp = [imports[k] for k in gainers if k in imports]
    gain_wgi = [sum(x[k] for x in wgi) / len(WGI) for k in gainers if all(k in x for x in wgi)]
    world_pop = sum(v["pop0"] for v in regions.values())
    out = {"question": "author, 2026-11-08: how to solve the political-path gap; which region could be first and what is it exposed to",
           "screens": SCREENS, "median_import_share_of_gainers_pct_gdp": round(med_imp, 1),
           "counts": {"regions": len(regions), "gainers": len(gainers), "gainers_in_conflict": sum(1 for k in gainers if k in conflict),
                      "gainers_fragile_not_conflict": sum(1 for k in gainers if k in fragile and k not in conflict),
                      "gainers_with_institutions_above_average": sum(1 for x in gain_wgi if x >= 0),
                      "passing_all_screens": len(passing), "one_screen_short": len(near)},
           "passing_population_share_of_world": round(sum(r["pop_m"] for r in passing) * 1e6 / world_pop, 3),
           "exposure_of_gainers": {"imports_pct_gdp_p25_p50_p75": [round(statistics.quantiles(gain_imp, n=4)[i], 1) for i in (0, 1, 2)],
                                   "wgi_mean_p25_p50_p75": [round(statistics.quantiles(gain_wgi, n=4)[i], 2) for i in (0, 1, 2)]},
           "candidates": passing[:20], "one_screen_short": [{k: r[k] for k in ("region", "pop_m", "wgi_mean", "imports_pct_gdp", "share_better_off_at_base")}
                                                             | {"missing": [s for s, ok in r["passes"].items() if not ok]} for r in near][:20],
           "exposure_channels": {
               "import_dependence": "the Trade Office (12b) must earn in exports the foreign currency for imports; the larger the import share of GDP, the larger the share of consumption that depends on world prices and on export earnings",
               "capital_flight_before_the_vote": "money moved abroad is not converted into U (T-1.3 applies to wealth held on the voting day); it does not remove workers, land or plants, so the internal economy in hours is unaffected, but foreign-currency reserves are",
               "skilled_emigration": "people who lose at the base salary (1 - share better off) are the pool that may leave; multipliers up to 5x and salaries never cut (T-8.4) are the design's answer",
               "smuggling": "incentive = price wedge between fixed internal prices and world prices x openness; the wedge is not measurable in this project",
           },
           "reading": "the screen is passed by a small group of middle-income regions with working institutions, no armed conflict, "
                      "moderate trade openness and almost everyone better off at the base salary; most gaining regions fail on "
                      "institutions or conflict, and the most open economies fail on imports. A first member therefore exists on "
                      "the data, but it is not a poor region and not a rich one: it is a stable middle-income region whose people "
                      "gain and whose borders are manageable. Nothing here says such a region would vote to join.",
           "limits": ["WGI are perception-based indices; imports share is a crude proxy for border exposure (essential imports share "
                      "would be better, as in the French case of 12b)",
                      "the material gain is the V7.2 year-30 comparison with equal weights on energy, health and housing",
                      "the share better off at the base salary (V7.4) uses income distributions of 150 regions; regions without data "
                      "cannot pass that screen",
                      "a screen, not a model of the first member's economy: no simulation of trade balance, reserves or emigration"]}
    if write:
        (U / "v72" / "outputs" / "first_region.json").write_text(json.dumps(out, indent=2))
        c = out["counts"]
        print(f"gainers {c['gainers']} (in conflict {c['gainers_in_conflict']}, fragile {c['gainers_fragile_not_conflict']}, institutions above average "
              f"{c['gainers_with_institutions_above_average']}); median import share {out['median_import_share_of_gainers_pct_gdp']}% of GDP")
        print(f"passing all screens: {c['passing_all_screens']} regions, {out['passing_population_share_of_world']*100:.1f}% of humanity; one screen short: {c['one_screen_short']}")
        for r in passing[:20]:
            print(f"  {r['region']}  pop {r['pop_m']:>7} m  WGI {r['wgi_mean']:>5}  imports {r['imports_pct_gdp']:>5}%  better off {r['share_better_off_at_base']}")
    return out


if __name__ == "__main__":
    main()
