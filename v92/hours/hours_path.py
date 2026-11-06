"""UNIRA V9.2 — the working week during the transition (author's design question, 2026-11-06).

Rule tested: a region starts at the shortest whole-hour week its EXISTING labour reserve can cover without any
productivity gain, pays the full base salary from day one, and shortens the week as measured productivity rises
(Article 13.3), until the 30-hour standard of Article 6. The week never rises again.

Reuses the V6.2 labour-reserve model and its frozen Eurostat data (v62/data/raw, manifest-verified by v62/run_all.py).
Nothing random; outputs are byte-identical between runs.
python3 hours_path.py  ->  ../outputs/hours_path.json, ../outputs/starting_week.csv"""
import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
V62 = U / "v62"
OUT = HERE.parent / "outputs"
sys.path.insert(0, str(V62 / "src"))
from unira_v62 import labour_reserve, tidy  # noqa: E402

CAPS = list(range(30, 41))  # 30 h = the standard (Article 6); 40 h = ceiling, nobody works more than 8 h x 5
TARGET = 30
RHO = (1.0, 0.75)  # entrant productivity relative to incumbents (v62: 1.0 upper bound, 0.75 illustrative)
CENTRAL_RHO = 0.75
YEARS = (2023, 2024)
# productivity growth per year: France VA/hour trends measured in v62 (loaded below) + illustrative rates
ILLUSTRATIVE = {"1.0%": 0.01, "1.5%": 0.015, "2.0%": 0.02, "3.0%": 0.03}
AGGREGATES = ("EU27_2020",)


def load():
    cfg = json.loads((V62 / "config" / "v62_config.json").read_text())
    raw = tidy.load_raw(V62 / "data" / "raw")
    cd = labour_reserve.CountryData(raw)
    s = json.loads((V62 / "outputs" / "summary.json").read_text())["scenarios"]["2023:A_observed"]
    growth = {"FR_trend_2015_2019": s["trend_va_per_hour_2015_2019"],
              "FR_trend_2015_2023": s["trend_va_per_hour_2015_2023"]}
    growth.update(ILLUSTRATIVE)
    return cfg, cd, growth


def grid(cd, lr, geo, year, rho):
    """One row per weekly cap: hours lost, gain needed without mobilisation, and what the existing reserve
    (unemployed + available but not seeking, the v62 'slack' framing) covers. None if core data are missing."""
    base = {"apply_to": ["SAL"], "age_band": lr["age_band"], "benchmarks": lr["benchmarks"],
            "entrant_relative_productivity": rho}
    rows = []
    for cap in CAPS:
        try:
            r = labour_reserve.evaluate(cd, geo, year, dict(base, entrant_weekly_hours=cap))
        except (ValueError, TypeError, KeyError):
            r = None
        if r is None:
            return None
        gap = r["hours_gap_ths"]
        rows.append({"cap": cap, "hours_lost_share": gap / r["hours_before_ths"],
                     "gain_no_mobilisation": r["required_gain_no_mobilisation"],
                     "reserve_persons_ths": r["slack_persons_ths"],
                     "reserve_closes_share": (r["slack_hours_supplied_ths"] / gap) if gap > 0 else None,
                     "residual_gain": r["slack_residual_gain"],
                     "employment_rate": r["employment_rate"], "usual_hours_all": r["lfs_usual_hours_all"]})
    return rows


def starting_week(rows):
    """Shortest cap at which the existing reserve maintains the region's hours (no productivity gain needed)."""
    for r in rows:
        if r["residual_gain"] <= 1e-9:
            return r["cap"]
    return None  # not even 40 h: the residual at 40 h is reported


def years_to_target(start, g):
    """Whole years until the week reaches TARGET when hours fall as 1/(1+g) per year (output and pay unchanged)."""
    if start <= TARGET:
        return 0
    if g <= 0:
        return None
    return math.ceil(math.log(start / TARGET) / math.log(1 + g) - 1e-9)


def main(write=True):
    cfg, cd, growth = load()
    lr = cfg["labour_reserve"]
    starts, france, table = {}, {}, []
    for geo in sorted(cd.geos()):
        for year in YEARS:
            for rho in RHO:
                rows = grid(cd, lr, geo, year, rho)
                if rows is None:
                    continue
                sw = starting_week(rows)
                starts.setdefault(geo, {}).setdefault(str(year), {})[str(rho)] = sw
                if geo == "FR":
                    france.setdefault(str(year), {})[str(rho)] = rows
                at = rows[(sw or 40) - 30]
                table.append({"geo": geo, "year": year, "entrant_relative_productivity": rho, "starting_week": sw,
                              "residual_gain_at_40h": rows[-1]["residual_gain"] if sw is None else 0.0,
                              "employment_rate": at["employment_rate"], "usual_hours_all": at["usual_hours_all"],
                              "reserve_persons_ths": at["reserve_persons_ths"],
                              "hours_lost_share_at_start": at["hours_lost_share"],
                              **{f"years_to_30h_{k}": years_to_target(sw or 40, g) for k, g in growth.items()}})
    countries = [g for g in starts if g not in AGGREGATES and "2023" in starts[g]]
    dist = {str(rho): dict(sorted(Counter(str(starts[g]["2023"][str(rho)]) for g in countries).items()))
            for rho in RHO}
    res = {"question": "At what working week can a region start so that its existing labour reserve maintains output "
                       "without any productivity gain, and how long until 30 h as productivity rises, pay unchanged?",
           "rule": {"caps_tested": CAPS, "target_hours": TARGET, "reserve_framing": "slack = unemployed + available not seeking (v62)",
                    "entrant_relative_productivity": list(RHO), "central": CENTRAL_RHO,
                    "hours_fall_as": "cap_t = cap_0 / (1 + g)^t, output and pay unchanged (Article 13.3)"},
           "growth_rates_per_year": growth,
           "evidence_classes": {"hours and reserve": "VERIFIED_OFFICIAL (Eurostat, v62 manifest)",
                                "reserve take-up": "SYNTHETIC_ASSUMPTION (no hours cut created net jobs by itself, v62 §4c)",
                                "entrant productivity": "SYNTHETIC_ASSUMPTION (v62)",
                                "FR productivity trends": "MODEL_DERIVED from Eurostat national accounts (v62)",
                                "illustrative growth rates": "SYNTHETIC_ASSUMPTION (not forecasts; AI effects not assumed)"},
           "starting_week": starts, "distribution_2023_countries": {"n": len(countries), **dist},
           "france": france,
           "years_to_30h_by_start": {str(s): {k: years_to_target(s, g) for k, g in growth.items()} for s in (34, 35, 36, 38, 40)}}
    if write:
        OUT.mkdir(exist_ok=True)
        (OUT / "hours_path.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")
        with (OUT / "starting_week.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(table[0]))
            w.writeheader()
            w.writerows(table)
        fr = starts["FR"]["2023"]
        print(f"France 2023: starting week {fr['1.0']} h (entrants as productive) / {fr['0.75']} h (0.75); "
              f"{len(countries)} countries, central distribution {dist[str(CENTRAL_RHO)]}")
    return res


if __name__ == "__main__":
    main()
