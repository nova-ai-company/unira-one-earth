"""UNIRA V8.3 — stress test of the D + C transition before publication (author's requirement, 2026-11-04).

Central design: provisional 25% equality credit, 3% reserve margin kept as a stock of goods, credit payouts at most
5% of usable supply during the transition and 15% after convergence, salaries never cut, strong catch-up (+4%/yr).
Stresses:
    slow_productivity     catch-up +2%/yr (historical) and only +0.5%/yr growth at the full level
    population_high/low   projected population change x1.3 / x0.7
    supply_shocks         -5% of world supply in years 5, 13, 21, 29, 37 and -10% in year 15 (droughts, pandemics)
    regional_lag          Sub-Saharan Africa and South Asia catch up at half speed
    combined              slow productivity + high population + shocks + regional lag
Measured: year the full salary scale is reached, year all credits are paid, years with shortages left after reserves,
worst shortage, average salary factor in year 20, peak credit stock.
python3 stress.py  ->  ../outputs/stress.json"""
import json
from pathlib import Path

import model

HERE = Path(__file__).resolve().parent
SHOCKS = {5: 0.05, 13: 0.05, 15: 0.10, 21: 0.05, 29: 0.05, 37: 0.05}


def lagging(reg):
    meta = {m["id"]: m["region"]["value"].strip() for m in json.loads((model.U / "v65" / "data" / "raw" / "wb_country_meta.json").read_text())[1]}
    return {k: 0.5 for k in reg if meta.get(k) in ("Sub-Saharan Africa", "South Asia")}


def main():
    reg = model.wm.regions()
    lag = lagging(reg)
    base = dict(extra=0.04, share=0.25, cap_after=model.RELEASE_CAP_AFTER)
    cases = {"baseline": {}, "slow_productivity": {"extra": 0.02, "rich_growth": 0.005},
             "population_high": {"pop_scale": 1.3}, "population_low": {"pop_scale": 0.7},
             "supply_shocks": {"shocks": SHOCKS}, "regional_lag": {"lag_regions": lag},
             "combined": {"extra": 0.02, "rich_growth": 0.005, "pop_scale": 1.3, "shocks": SHOCKS, "lag_regions": lag},
             "slow_productivity_with_ceiling": {"extra": 0.02, "rich_growth": 0.005, "liability_ceiling": 2.0},
             "combined_with_ceiling": {"extra": 0.02, "rich_growth": 0.005, "pop_scale": 1.3, "shocks": SHOCKS, "lag_regions": lag,
                                       "liability_ceiling": 2.0},
             "baseline_with_ceiling": {"liability_ceiling": 2.0}}
    out = {"design": {"credit_share": 0.25, "reserve_margin": model.RESERVE_MARGIN, "release_cap_transition": model.RELEASE_CAP,
                      "release_cap_after": model.RELEASE_CAP_AFTER, "catch_up": 0.04, "salaries_never_cut": True},
           "lagging_regions": len(lag), "results": {}}
    for name, kw in cases.items():
        args = {**base, **kw}
        r = model.run(reg, args.pop("extra"), args.pop("share"), args.pop("cap_after"), **args)
        r.pop("path")
        out["results"][name] = r
        print(f"{name:18s} full scale yr {r['year_full_salary_scale']} | credits paid yr {r['year_credits_paid']} | shortage years "
              f"{r['shortage_years_after_reserves']} (worst {100 * r['worst_shortage_share']:.1f}%) | salary factor yr20 "
              f"{r['mean_salary_factor_year_20']} | peak credit {r['peak_credit_stock_years_of_world_consumption']}")
    (HERE.parent / "outputs" / "stress.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
