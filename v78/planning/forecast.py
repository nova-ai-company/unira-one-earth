"""UNIRA V7.8 — Can machine learning forecast regional needs well enough to plan production?

Out-of-sample backtest on real history. Every model predicts g = log(y[T+h] / y[T]) for a region from
data known at origin T only, and the forecast is y[T] * exp(g).

    naive     g = 0 (next years equal the last observed year)
    drift     average log growth of the last 5 years, times h
    trend     least-squares slope of log y over the last 6 years, times h
    ridge     ML: one pooled linear model over all regions, features = log growth over 1..5 years,
              penalty chosen on a validation period
    knn       ML: average outcome of the 30 most similar past growth paths (any region, any earlier year)
    ensemble  mean of drift and ridge

Time split (no look-ahead): models are fitted on outcomes up to VAL_START-1, the model and penalty are
chosen on outcomes VAL_START..TEST_START-1, and accuracy is reported only on forecasts made from
TEST_START onward. The chosen model is then refitted on everything before TEST_START.
Rule ("science by default"): an ML model is adopted only if it beats the simple rules on the validation period.
python3 forecast.py  ->  ../outputs/backtest.json, ../outputs/backtest_errors.csv
"""
import csv
import json
import math
import random
from pathlib import Path

import data

OUT = Path(__file__).resolve().parents[1] / "outputs"
LAGS = 5
VAL_START, TEST_START = 2005, 2010
HORIZONS = (1, 2, 5)
MODELS = ("naive", "drift", "trend", "ridge", "knn", "ensemble")
ML = {"ridge", "knn", "ensemble"}
LAMBDAS = (0.001, 0.01, 0.1, 1.0, 10.0)
KNN_K, KNN_MAX_TRAIN = 30, 1500


def samples(series, h):
    """[(iso, origin T, features, target g, y_T, y_true)] for every origin with LAGS+1 consecutive years."""
    out = []
    for iso, s in series.items():
        for T in sorted(s):
            if T + h not in s or any(T - i not in s for i in range(LAGS + 1)):
                continue
            lv = [math.log(s[T - i]) for i in range(LAGS + 1)]
            x = [lv[0] - lv[i] for i in range(1, LAGS + 1)]  # log growth over 1..5 years
            out.append((iso, T, x, math.log(s[T + h]) - lv[0], s[T], s[T + h], lv))
    return out


def solve(a, b):
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[piv] = m[piv], m[c]
        for r in range(n):
            if r != c and m[c][c]:
                f = m[r][c] / m[c][c]
                for k in range(c, n + 1):
                    m[r][k] -= f * m[c][k]
    return [m[i][n] / m[i][i] if m[i][i] else 0.0 for i in range(n)]


def fit_ridge(train, lam):
    """Intercept + LAGS slopes; the intercept is not penalised."""
    p = LAGS + 1
    xtx = [[0.0] * p for _ in range(p)]
    xty = [0.0] * p
    for s in train:
        z = [1.0] + s[2]
        for i in range(p):
            xty[i] += z[i] * s[3]
            for j in range(p):
                xtx[i][j] += z[i] * z[j]
    for i in range(1, p):
        xtx[i][i] += lam * len(train)
    return solve(xtx, xty)


def knn_model(train, seed=0):
    pool = train if len(train) <= KNN_MAX_TRAIN else random.Random(seed).sample(train, KNN_MAX_TRAIN)
    sd = [max(1e-9, math.sqrt(sum(s[2][i] ** 2 for s in pool) / len(pool))) for i in range(LAGS)]
    pts = [([s[2][i] / sd[i] for i in range(LAGS)], s[3]) for s in pool]

    def predict(x):
        z = [x[i] / sd[i] for i in range(LAGS)]
        near = sorted(pts, key=lambda q: sum((q[0][i] - z[i]) ** 2 for i in range(LAGS)))[:KNN_K]
        return sum(q[1] for q in near) / len(near)
    return predict


def simple(name, s, h):
    lv = s[6]
    if name == "naive":
        return 0.0
    if name == "drift":
        return h * (lv[0] - lv[LAGS]) / LAGS
    # trend: OLS slope of log level on time over the last LAGS+1 years
    ts = list(range(LAGS + 1))  # 0 = T, 1 = T-1, ...
    tm, ym = sum(ts) / len(ts), sum(lv) / len(lv)
    slope = -sum((t - tm) * (y - ym) for t, y in zip(ts, lv)) / sum((t - tm) ** 2 for t in ts)
    return h * slope


def predictors(train, val):
    """Fit ML models on `train`, choosing the ridge penalty on `val`."""
    best = None
    for lam in LAMBDAS:
        w = fit_ridge(train, lam)
        err = median([abs(math.exp(sum(a * b for a, b in zip(w, [1.0] + s[2])) - s[3]) - 1) for s in val]) if val else 0
        if best is None or err < best[0]:
            best = (err, lam, w)
    return best[1], best[2]


def predict_all(model, rows, h, w, knn):
    out = []
    for s in rows:
        if model == "ridge":
            g = sum(a * b for a, b in zip(w, [1.0] + s[2]))
        elif model == "knn":
            g = knn(s[2])
        elif model == "ensemble":
            g = 0.5 * (simple("drift", s, h) + sum(a * b for a, b in zip(w, [1.0] + s[2])))
        else:
            g = simple(model, s, h)
        out.append(s[4] * math.exp(g))
    return out


def median(xs):
    return quantile(xs, 0.5)


def quantile(xs, q):
    v = sorted(xs)
    if not v:
        return None
    i = q * (len(v) - 1)
    lo, hi = int(math.floor(i)), int(math.ceil(i))
    return v[lo] + (v[hi] - v[lo]) * (i - lo)


def scores(rows, preds):
    ape = [abs(p - s[5]) / s[5] for s, p in zip(rows, preds)]
    signed = [(p - s[5]) / s[5] for s, p in zip(rows, preds)]
    short = [s[5] / p - 1 for s, p in zip(rows, preds)]  # stock above forecast needed to cover the true need
    return {"n": len(rows), "median_ape": median(ape), "p90_ape": quantile(ape, 0.9), "p95_ape": quantile(ape, 0.95),
            "mean_signed_error": sum(signed) / len(signed), "buffer_for_95pct_coverage": max(0.0, quantile(short, 0.95))}


def backtest(series, h, groups=None):
    allrows = samples(series, h)
    fit = [s for s in allrows if s[1] + h < VAL_START]
    val = [s for s in allrows if VAL_START <= s[1] + h < TEST_START]
    test = [s for s in allrows if s[1] >= TEST_START]
    lam, w = predictors(fit, val)
    knn = knn_model(fit)
    val_scores = {m: scores(val, predict_all(m, val, h, w, knn))["median_ape"] for m in MODELS}
    chosen = min(MODELS, key=lambda m: val_scores[m])
    # refit on everything known before the test period
    pre = fit + val
    w2 = fit_ridge(pre, lam)
    knn2 = knn_model(pre)
    res = {"lambda": lam, "n_fit": len(pre), "validation_median_ape": val_scores, "chosen_on_validation": chosen,
           "ml_adopted": chosen in ML, "test": {}}
    preds = {m: predict_all(m, test, h, w2, knn2) for m in MODELS}
    for m in MODELS:
        res["test"][m] = scores(test, preds[m])
    if groups:
        res["equity_by_income_group"] = {}
        for g in ("LIC", "LMC", "UMC", "HIC"):
            idx = [i for i, s in enumerate(test) if groups.get(s[0]) == g]
            if len(idx) >= 20:
                res["equity_by_income_group"][g] = scores([test[i] for i in idx], [preds[chosen][i] for i in idx])
    res["_test_rows"] = [(s[0], s[1], s[5], preds[chosen][i]) for i, s in enumerate(test)]
    return res


def world_total_error(series, h, res):
    """Planning the WORLD total: errors of single regions partly cancel."""
    by_origin = {}
    for iso, T, true, pred in res["_test_rows"]:
        a = by_origin.setdefault(T, [0.0, 0.0])
        a[0] += true
        a[1] += pred
    errs = [abs(p - t) / t for t, p in by_origin.values()]
    return {"origins": len(errs), "median_ape": median(errs), "max_ape": max(errs)} if errs else None


def main():
    series = data.load_all()
    groups = data.income_groups()
    out = {"split": {"fit_outcomes_before": VAL_START, "validation": [VAL_START, TEST_START - 1],
                     "test_origins_from": TEST_START}, "models": MODELS, "results": {}}
    rows = []
    for name, s in series.items():
        out["results"][name] = {}
        for h in HORIZONS:
            r = backtest(s, h, groups)
            if name == "population":
                r["world_total"] = world_total_error(s, h, r)
            for iso, T, true, pred in r.pop("_test_rows"):
                rows.append({"series": name, "h": h, "iso": iso, "origin": T, "true": round(true, 4),
                             "forecast": round(pred, 4), "model": r["chosen_on_validation"]})
            out["results"][name][f"h{h}"] = r
            t = r["test"]
            print(f"{name:12s} h={h} chosen={r['chosen_on_validation']:8s} test medAPE: " +
                  " ".join(f"{m}={100 * t[m]['median_ape']:.2f}%" for m in MODELS))
    OUT.mkdir(exist_ok=True)
    (OUT / "backtest.json").write_text(json.dumps(out, indent=2))
    with (OUT / "backtest_errors.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
