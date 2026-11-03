"""UNIRA V6.9 — Can needs-first allocation work with real-world information and governance failures?

The One Earth allocator sees each region's need through:
  measurement error  multiplicative lognormal noise, sigma (new draw each year)
  data lag           decisions use needs as they were `lag` years ago
  misreporting       a fixed share of regions inflate reported need by (1 + inflation);
                     audits catch each misreporting region with probability `audit_detect` per year,
                     after which it reports honestly
  leakage / capture  a share of each year's new capacity never reaches any region
Monte Carlo over seeds; outcomes compared with perfect UNIRA (C) and the market economies (B, B2).
"""
import math
import random


def make_perceiver(regions, gov, seed):
    rng = random.Random(seed)
    keys = sorted(regions)
    cheaters = set(rng.sample(keys, int(round(gov["misreport_share"] * len(keys)))))
    history = {"energy": [], "health": [], "housing": []}

    def perceive(domain, t, true_def):
        hist = history[domain]
        hist.append(dict(true_def))
        lagged = hist[max(0, len(hist) - 1 - gov["lag"])]
        for k in list(cheaters):
            if rng.random() < gov["audit_detect"]:
                cheaters.discard(k)
        seen = {}
        for k in keys:
            d = lagged.get(k, 0.0)
            if gov["sigma"] > 0:
                d *= math.exp(rng.gauss(-gov["sigma"] ** 2 / 2, gov["sigma"]))  # mean-preserving
            if k in cheaters:
                # misreporting regions claim need even when they have none (a floor of their size)
                d = max(d, 0.0) * (1 + gov["inflation"]) + (gov["inflation"] * 0.05 * max(true_def.values()) if d == 0 else 0.0)
            seen[k] = d
        return seen

    return perceive


def quantiles(xs, qs=(0.1, 0.5, 0.9)):
    v = sorted(xs)
    out = []
    for q in qs:
        i = q * (len(v) - 1)
        lo, hi = int(math.floor(i)), int(math.ceil(i))
        out.append(v[lo] + (v[hi] - v[lo]) * (i - lo))
    return out
