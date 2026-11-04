"""Backtest of the delivery pace rule used in V8.7-V9.1 against real history (validation, not a new model).

The living-standard models (v87/v89/v90/v91) project each country's access to basic services with
    yearly gain = max(own gain measured 2010-latest, the p-th percentile of all countries' positive gains) x factors
where the factors (programme scale, automation, governance) describe UNIRA conditions. A backtest can only test the
historical part of that rule: with scale 1 and no automation, does it reproduce what actually happened?
Test: fit on 2000-2012 (own gain and the percentiles of gains over that period), predict 2024, compare with the data.
Variants: own gain only (p = none), and p = 0.5 / 0.75 / 0.9 (the conservative / moderate / accelerated floors), each
without and with the governance factors (conflict 0.5, fragility 0.75, applied with the FY26 list: anachronistic, so
only a rough check). Metrics per domain: mean absolute error, bias, shares over- and under-predicted by more than
5 points, and population-weighted world coverage (predicted versus actual). Also: whether countries kept their pace
(rank correlation of 2000-12 and 2012-24 gains) and whether the gain percentiles were stable between the two periods.
python3 backtest.py -> outputs/backtest.json"""
import importlib.util
import json
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parent
spec = importlib.util.spec_from_file_location("v87", U / "v87" / "livingstandard" / "simulate.py")
L87 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L87)

DOMAINS = {"water": "SH.H2O.BASW.ZS", "sanitation": "SH.STA.BASS.ZS", "clean_cooking": "EG.CFT.ACCS.ZS",
           "electricity": "EG.ELC.ACCS.ZS", "internet": "IT.NET.USER.ZS", "secondary_school": "SE.SEC.ENRR"}
Y0, Y1, Y2 = 2000, 2012, 2024
VARIANTS = {"own_only": None, "p50": 0.5, "p75": 0.75, "p90": 0.9}
GOV = {"conflict": 0.5, "fragile": 0.75}


def value_near(s, k, year, tol):
    """Value at the year closest to `year` within tol years; (year, value) or (None, None)."""
    ys = [y for y in s.get(k, {}) if abs(y - year) <= tol]
    if not ys:
        return None, None
    y = min(ys, key=lambda a: (abs(a - year), -a))
    return y, s[k][y]


def spearman(a, b):
    def ranks(x):
        order = sorted(range(len(x)), key=lambda i: x[i])
        r = [0.0] * len(x)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]:
                j += 1
            for m in range(i, j + 1):
                r[order[m]] = (i + j) / 2 + 1
            i = j + 1
        return r
    ra, rb = ranks(a), ranks(b)
    ma, mb = statistics.fmean(ra), statistics.fmean(rb)
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return sum((x - ma) * (y - mb) for x, y in zip(ra, rb)) / den if den else 0.0


def main(write=True):
    cty = L87.countries()
    fcs = json.loads((U / "v88" / "essential" / "data" / "raw" / "fcs_fy26.json").read_text())
    status = {k: "conflict" for k in fcs["conflict"]} | {k: "fragile" for k in fcs["institutional_social_fragility"]}
    out = {"fit_period": [Y0, Y1], "test_year": Y2, "domains": {}}
    for dom, code in DOMAINS.items():
        s = L87.series(code)
        target = 99.0
        if dom == "secondary_school":
            target = L87.B["domains"]["education"]["essential_secondary_enrolment"]
        if dom == "internet":
            target = L87.B["domains"]["internet"]["essential"]
        rows = []
        for k in cty:
            y0, v0 = value_near(s, k, Y0, 2)
            y1, v1 = value_near(s, k, Y1, 1)
            y2, v2 = value_near(s, k, Y2, 2)
            if v0 is None or v1 is None or v2 is None or y1 <= y0 or y2 <= y1:
                continue
            rows.append({"k": k, "pop": cty[k]["pop"], "v1": v1, "v2": v2, "own": (v1 - v0) / (y1 - y0), "later": (v2 - v1) / (y2 - y1),
                         "h": y2 - y1, "status": status.get(k, "other")})
        if len(rows) < 30:
            continue
        gains_fit = sorted(r["own"] for r in rows if r["own"] > 0 and r["v1"] < target)
        gains_later = sorted(r["later"] for r in rows if r["later"] > 0 and r["v1"] < target)
        pctl = lambda g, p: g[min(len(g) - 1, int(p * len(g)))] if g else 0.0
        res = {"countries": len(rows), "target": target,
               "actual_world_coverage_2024": round(sum(r["pop"] * min(r["v2"], target) for r in rows) / sum(r["pop"] for r in rows) / target, 4),
               "gain_percentiles_fit_vs_later_points_per_year": {f"p{int(100 * p)}": [round(pctl(gains_fit, p), 3), round(pctl(gains_later, p), 3)]
                                                                 for p in (0.5, 0.75, 0.9)},
               "rank_correlation_own_pace_2000_12_vs_2012_24": round(spearman([r["own"] for r in rows], [r["later"] for r in rows]), 3),
               "variants": {}}
        for name, p in VARIANTS.items():
            floor = pctl(gains_fit, p) if p is not None else 0.0
            for gov_label, use_gov in (("no_governance_factor", False), ("with_governance_factor", True)):
                errs, by_status = [], {}
                pred_cov = 0.0
                for r in rows:
                    rate = max(r["own"], floor)
                    if use_gov:
                        rate *= GOV.get(r["status"], 1.0)
                    pred = min(target, r["v1"] + rate * r["h"]) if r["v1"] < target else min(target, max(r["v1"], r["v1"]))
                    e = pred - min(r["v2"], target)
                    errs.append(e)
                    by_status.setdefault(r["status"], []).append(e)
                    pred_cov += r["pop"] * pred
                W = sum(r["pop"] for r in rows)
                res["variants"][f"{name}/{gov_label}"] = {
                    "mae_points": round(statistics.fmean(abs(e) for e in errs), 2),
                    "bias_points_pred_minus_actual": round(statistics.fmean(errs), 2),
                    "share_over_by_5pts": round(sum(e > 5 for e in errs) / len(errs), 3),
                    "share_under_by_5pts": round(sum(e < -5 for e in errs) / len(errs), 3),
                    "predicted_world_coverage_2024": round(pred_cov / W / target, 4),
                    "bias_by_status": {st: round(statistics.fmean(v), 2) for st, v in sorted(by_status.items())}}
        out["domains"][dom] = res
        print(f"{dom:16s} n={res['countries']:3d} actual world coverage {100 * res['actual_world_coverage_2024']:.1f}% | pace persistence rho={res['rank_correlation_own_pace_2000_12_vs_2012_24']} | "
              f"percentiles fit->later {res['gain_percentiles_fit_vs_later_points_per_year']}")
        for vn, v in res["variants"].items():
            print(f"   {vn:32s} MAE {v['mae_points']:5.2f} bias {v['bias_points_pred_minus_actual']:+6.2f} over>5 {100 * v['share_over_by_5pts']:4.0f}% under>5 {100 * v['share_under_by_5pts']:4.0f}% "
                  f"world {100 * v['predicted_world_coverage_2024']:.1f}% | bias by status {v['bias_by_status']}")
    # summary across domains for the variant the models use most (own vs p75 floor without governance)
    summ = {}
    for vn in ("own_only/no_governance_factor", "p50/no_governance_factor", "p75/no_governance_factor", "p90/no_governance_factor",
               "p75/with_governance_factor"):
        vals = [d["variants"][vn] for d in out["domains"].values()]
        summ[vn] = {"mean_mae_points": round(statistics.fmean(v["mae_points"] for v in vals), 2),
                    "mean_bias_points": round(statistics.fmean(v["bias_points_pred_minus_actual"] for v in vals), 2),
                    "world_coverage_error_points": round(100 * statistics.fmean(
                        v["predicted_world_coverage_2024"] - d["actual_world_coverage_2024"] for v, d in zip(vals, out["domains"].values())), 2)}
    out["summary"] = summ
    print("summary:", json.dumps(summ, indent=1))
    if write:
        (HERE / "outputs").mkdir(exist_ok=True)
        (HERE / "outputs" / "backtest.json").write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main()
