"""UNIRA V7.4b: who gains inside each region, worldwide, against ONE absolute UNIRA basket.

v7.4 (run.py) compared each EU country's deciles with that country's own mean. Here every country is compared
with the same absolute basket, as UNIRA's salaries and fixed prices are the same everywhere:
    base basket (lowest salary, saving 50%) = 0.86 x France's mean household consumption per person (v64)
    region mean = household final consumption per person, PPP constant 2021 int$ (World Bank)
    base level relative to the region's mean = 0.86 x C_France / C_region
Income distribution: World Bank income shares (lowest 10%, quintiles, highest 10%), latest year 2005-2024.
Within-group levels are group means (Lorenz-curve slopes); the share of people below the base is interpolated
between group mid-points. Free health care, education and guaranteed housing come on top and are NOT counted,
so gains for the poorest are understated (especially where households pay for health care, as in the USA).
python3 world.py  ->  ../outputs/distribution_world.json, distribution_world.csv"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
U = ROOT.parents[1]
BASE_REL_FR = json.loads((U / "v64" / "outputs" / "summary.json").read_text())["fixed_price"]["base_basket_vs_today_average_person"]
GROUPS = [(0.0, 0.1, "SI.DST.FRST.10"), (0.1, 0.2, None), (0.2, 0.4, "SI.DST.02ND.20"), (0.4, 0.6, "SI.DST.03RD.20"),
          (0.6, 0.8, "SI.DST.04TH.20"), (0.8, 0.9, None), (0.9, 1.0, "SI.DST.10TH.10")]


def verify():
    with (RAW / "raw_manifest.csv").open() as f:
        for r in csv.DictReader(f):
            if r["file"].startswith("wb_") and hashlib.sha256((RAW / r["file"]).read_bytes()).hexdigest() != r["sha256"]:
                raise SystemExit(f"hash mismatch: {r['file']}")


def series(code):
    """{iso3: {year: value}}"""
    out = {}
    for x in json.loads((RAW / f"wb_{code}.json").read_text())[1]:
        if x["value"] is not None and x["countryiso3code"]:
            out.setdefault(x["countryiso3code"], {})[int(x["date"])] = float(x["value"])
    return out


def group_levels(sh):
    """Relative income level (1.0 = mean) of each population group, from the income shares of one year."""
    vals = {"SI.DST.FRST.10": sh["SI.DST.FRST.10"], "SI.DST.02ND.20": sh["SI.DST.02ND.20"],
            "SI.DST.03RD.20": sh["SI.DST.03RD.20"], "SI.DST.04TH.20": sh["SI.DST.04TH.20"],
            "SI.DST.10TH.10": sh["SI.DST.10TH.10"]}
    shares = [vals["SI.DST.FRST.10"], sh["SI.DST.FRST.20"] - vals["SI.DST.FRST.10"], vals["SI.DST.02ND.20"],
              vals["SI.DST.03RD.20"], vals["SI.DST.04TH.20"], sh["SI.DST.05TH.20"] - vals["SI.DST.10TH.10"],
              vals["SI.DST.10TH.10"]]
    tot = sum(shares)
    return [((a + b) / 2, (s / tot) / (b - a)) for (a, b, _), s in zip(GROUPS, shares)], tot


def share_below(levels, base):
    """Share of people whose income level is below `base` (interpolated between group mid-points)."""
    pts = [(0.0, 0.0)] + levels + [(1.0, levels[-1][1])]
    if base >= pts[-1][1]:
        return 1.0
    for (p0, r0), (p1, r1) in zip(pts, pts[1:]):
        if r0 <= base < r1:
            return p0 + (p1 - p0) * (base - r0) / (r1 - r0)
    return 0.0


def latest_complete(dist, iso):
    years = set.intersection(*[set(dist[c].get(iso, {})) for c in dist])
    return max(years) if years else None


def main():
    verify()
    codes = ["SI.DST.FRST.10", "SI.DST.FRST.20", "SI.DST.02ND.20", "SI.DST.03RD.20", "SI.DST.04TH.20",
             "SI.DST.05TH.20", "SI.DST.10TH.10"]
    dist = {c: series(c) for c in codes}
    hfce, pop = series("NE.CON.PRVT.PP.KD"), series("SP.POP.TOTL")
    losers = json.loads((U / "v72" / "outputs" / "joining.json").read_text())["losers_all"]

    def cons_pc(iso, year):
        ys = [y for y in hfce.get(iso, {}) if y in pop.get(iso, {}) and y <= year]
        y = max(ys) if ys else None
        return (hfce[iso][y] / pop[iso][y], y) if y else (None, None)

    ref_year = 2023
    c_fr, _ = cons_pc("FRA", ref_year)
    out = {"method": __doc__.split("python3")[0].strip(), "base_basket_vs_france_mean": BASE_REL_FR,
           "france_consumption_per_person_ppp": round(c_fr), "reference_year": ref_year, "regions": {}}
    rows = []
    for iso in sorted(set(dist["SI.DST.FRST.10"])):
        y = latest_complete(dist, iso)
        c, cy = cons_pc(iso, ref_year)
        if y is None or c is None:
            continue
        levels, tot = group_levels({k: dist[k][iso][y] for k in codes})
        base = BASE_REL_FR * c_fr / c
        r = {"income_year": y, "consumption_year": cy, "consumption_per_person_ppp": round(c),
             "mean_vs_france": round(c / c_fr, 3), "unira_base_vs_region_mean": round(base, 3),
             "share_of_people_better_off_at_base": round(share_below(levels, base), 3),
             "poorest_tenth_level_vs_mean": round(levels[0][1], 3),
             "poorest_tenth_gain_pct_at_base": round(100 * (base / levels[0][1] - 1), 1),
             "poorest_fifth_gain_pct_at_base": round(100 * (base / ((levels[0][1] + levels[1][1]) / 2) - 1), 1),
             "income_shares_sum_pct": round(tot, 1),
             "rich_region_average_change_pct": round(losers[iso], 1) if iso in losers else None}
        out["regions"][iso] = r
        rows.append({"iso3": iso, **r})
    rich = {k: v for k, v in out["regions"].items() if v["rich_region_average_change_pct"] is not None}
    tot_pop = {k: pop[k][max(pop[k])] for k in rich}
    out["rich_regions_summary"] = {
        "n_rich_regions": len(losers), "n_with_data": len(rich), "without_income_data": sorted(set(losers) - set(rich)),
        "population_weighted_share_better_off": round(sum(rich[k]["share_of_people_better_off_at_base"] * tot_pop[k] for k in rich) / sum(tot_pop.values()), 3),
        "people_better_off_millions": round(sum(rich[k]["share_of_people_better_off_at_base"] * tot_pop[k] for k in rich) / 1e6, 1),
        "poorest_tenth_gain_pct_range": [min(v["poorest_tenth_gain_pct_at_base"] for v in rich.values()),
                                         max(v["poorest_tenth_gain_pct_at_base"] for v in rich.values())]}
    # count PEOPLE, not regions: everyone in a gaining region (v72) plus those better off inside the rich regions
    j = json.loads((U / "v72" / "outputs" / "joining.json").read_text())
    world_pop = pop["WLD"][max(pop["WLD"])]
    rich_pop = sum(pop[k][max(pop[k])] for k in losers if k in pop)
    in_rich = sum(rich[k]["share_of_people_better_off_at_base"] * tot_pop[k] for k in rich)
    out["people_based"] = {
        "world_population": world_pop, "share_in_gaining_regions": round(j["gainers_share_of_world_pop"], 4),
        "people_in_rich_regions_millions": round(rich_pop / 1e6, 1),
        "better_off_in_rich_regions_millions": round(in_rich / 1e6, 1),
        "share_of_humanity_better_off": round(j["gainers_share_of_world_pop"] + in_rich / world_pop, 4),
        "note": "Regions that gain on average are counted whole; their richest residents may lose, which is not modelled. "
                "In rich regions only people already below the lowest UNIRA income are counted; others earning above the "
                "base salary, and the value of free health care, education and housing, are not."}
    print(out["people_based"])
    (ROOT.parent / "outputs").mkdir(exist_ok=True)
    (ROOT.parent / "outputs" / "distribution_world.json").write_text(json.dumps(out, indent=2))
    with (ROOT.parent / "outputs" / "distribution_world.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for iso in ("USA", "JPN", "FRA", "DEU", "ITA", "ESP", "GBR", "CAN", "AUS", "KOR", "NOR", "CHE", "POL"):
        if iso in out["regions"]:
            r = out["regions"][iso]
            print(f"{iso} income {r['income_year']} mean/FR {r['mean_vs_france']:.2f} base/mean {r['unira_base_vs_region_mean']:.2f} "
                  f"better off {100 * r['share_of_people_better_off_at_base']:.0f}%  poorest tenth +{r['poorest_tenth_gain_pct_at_base']:.0f}%  "
                  f"poorest fifth +{r['poorest_fifth_gain_pct_at_base']:.0f}%  region avg {r['rich_region_average_change_pct']}")
    print(out["rich_regions_summary"])


if __name__ == "__main__":
    main()
