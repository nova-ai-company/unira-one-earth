"""UNIRA V8.4 — sensitivity tests required before the hybrid enters the constitution (author, 2026-11-04).
Baseline comparison: D + C WITHOUT equality credit (removed from the baseline), D + C + Q (equal salaries + quotas),
and the hybrid (quotas for goods + converging service salaries). Tests:
    goods/services split   24/76 (France 2022), 35/65, 45/55
    quota enforcement      0%, 8%, 15% of quota goods diverted (lost to the poorer regions)
    work incentives        effort falls with unspendable money: 0, 0.2, 0.5
    distribution           at most 50%, 35%, 20% of world goods shipped between regions each year
python3 sensitivity.py  ->  ../outputs/quota_sensitivity.json"""
import json
from pathlib import Path

import compare

HERE = Path(__file__).resolve().parent
SCEN = {"DC_no_credit": ("s1_DC", {"credit_share": 0.0}), "DCQ_equal_salaries": ("s2_DCQ", {}), "hybrid": ("s3_hybrid", {})}
TESTS = {"goods_24": {"goods": 0.24}, "goods_35": {"goods": 0.35}, "goods_45": {"goods": 0.45},
         "leakage_8": {"leakage": 0.08}, "leakage_15": {"leakage": 0.15},
         "effort_0.2": {"effort": 0.2}, "effort_0.5": {"effort": 0.5},
         "transfer_50": {"transfer_cap": 0.50}, "transfer_35": {"transfer_cap": 0.35}, "transfer_20": {"transfer_cap": 0.20}}


def summary(r):
    y0, y20 = r["year_0"], r["year_20"]
    return {"poorer_half_y0": y0["real_poorer_half_vs_full"], "poorer_half_y20": y20["real_poorer_half_vs_full"],
            "year_poorer_half_90pct": r["year_poorer_half_reaches_90pct"], "gini_y0": y0["gini_real_between_regions"],
            "unspendable_y0": y0["unspendable_money_share_of_income"], "richest20_y0": y0["richest20_real_vs_today"]}


def main():
    reg = compare.wm.regions()
    out = {}
    for test, kw in TESTS.items():
        out[test] = {}
        for name, (scen, base) in SCEN.items():
            out[test][name] = summary(compare.simulate(reg, scen, **{**base, **kw}))
        h, d, q = out[test]["hybrid"], out[test]["DC_no_credit"], out[test]["DCQ_equal_salaries"]
        print(f"{test:12s} poorer half yr0/yr20 | 90% year: hybrid {100 * h['poorer_half_y0']:.0f}/{100 * h['poorer_half_y20']:.0f}% {h['year_poorer_half_90pct']} | "
              f"D+C {100 * d['poorer_half_y0']:.0f}/{100 * d['poorer_half_y20']:.0f}% {d['year_poorer_half_90pct']} | "
              f"Q {100 * q['poorer_half_y0']:.0f}/{100 * q['poorer_half_y20']:.0f}% {q['year_poorer_half_90pct']} (unspendable {100 * q['unspendable_y0']:.0f}%) "
              f"| richest20 hybrid {100 * h['richest20_y0']:.0f}% vs D+C {100 * d['richest20_y0']:.0f}%")
    (HERE.parent / "outputs" / "quota_sensitivity.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
