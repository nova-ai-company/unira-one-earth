#!/usr/bin/env python3
"""UNIRA v79 - allocation of desirable homes at fixed prices.

Under UNIRA homes have fixed prices (Art. 18), so price cannot ration the
city centre or the seaside. This simulation compares five ways of choosing who
gets a desirable home when one becomes free:

  queue           pure first come, first served (registration date)
  points          published priority points, ties by registration date
  points_lottery  points grouped into bands; public lottery inside a band
  points_lottery_open  as points_lottery, but a share of vacancies (default
                  30%) goes to an open lottery among all applicants (HDB-style quota)
  lottery         pure lottery, one common draw per year
  market          highest bidder by income (benchmark: what UNIRA rejects)

Every year: occupied desirable homes turn over, empty-held homes are released
(and, under the must-live-in rule, detected and returned), new homes may be
built, new applicants arrive, some stop waiting, and the vacancies are matched
by applicant-proposing deferred acceptance (applicants rank the zones they
prefer to their fallback; zones rank applicants by the method's priority).

Income never enters UNIRA priorities; it is only used to label deciles and in
the market benchmark. Standard library only. Run:  python3 simulate.py
"""
import csv
import json
import math
import os
import random
import statistics
import sys
import time
from heapq import heappush, heapreplace
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
METHODS = ["queue", "points", "points_lottery", "points_lottery_open", "lottery", "market"]
POINT_METHODS = ("points", "points_lottery", "points_lottery_open")


def load_config(path=None):
    with open(path or os.path.join(HERE, "config.json")) as f:
        return json.load(f)


def _v(x):
    return x["value"] if isinstance(x, dict) and "value" in x else x


def binom(rng, n, p):
    if n <= 0 or p <= 0:
        return 0
    if p >= 1:
        return n
    if hasattr(rng, "binomialvariate"):
        return rng.binomialvariate(n, p)
    if n < 60:  # pragma: no cover - old Python fallback
        return sum(1 for _ in range(n) if rng.random() < p)
    k = int(round(rng.gauss(n * p, math.sqrt(n * p * (1 - p)))))  # pragma: no cover
    return max(0, min(n, k))  # pragma: no cover


class Household:
    __slots__ = ("hid", "arrive", "reg", "decile", "income", "adults", "children",
                 "disab", "care", "roots", "work", "prefs", "fallback", "spec",
                 "cheat", "deter_u", "drop_year", "static_pts", "high_need",
                 "housed_year", "housed_zone", "banned_until", "ever_caught", "applied")

    def __init__(self):
        self.housed_year = None
        self.housed_zone = None
        self.banned_until = -10**9
        self.ever_caught = False


# ----------------------------------------------------------------- population
def generate_population(cfg, seed, gaming_rate=0.0, spread_jobs=0.0):
    """All households that will ever apply, drawn up front from their own RNG so
    every method faces the identical population (common random numbers)."""
    rng = random.Random(seed * 7919 + 1)
    zones = _v(cfg["zones"])
    hh = cfg["household"]
    pts = cfg["points"]
    spec_cfg = cfg["speculation"]
    gm = cfg["gaming"]
    nz = len(zones)
    job = [z["job_share"] for z in zones]
    if spread_jobs:
        moved = job[0] * spread_jobs
        job[0] -= moved
        nd = [i for i, z in enumerate(zones) if not z["desirable"]]
        for i in nd:
            job[i] += moved / len(nd)
    jcum, acc = [], 0.0
    for j in job:
        acc += j
        jcum.append(acc / sum(job))
    dist = [[math.hypot(a["x"] - b["x"], a["y"] - b["y"]) for b in zones] for a in zones]
    desirable = [i for i, z in enumerate(zones) if z["desirable"]]
    other = [i for i, z in enumerate(zones) if not z["desirable"]]
    ccost = _v(cfg["commute_cost_per_km"])
    tsd = _v(cfg["taste_sd"])
    sigma = _v(hh["income_sigma"])
    kp = _v(hh["children_probs"])
    drop = _v(cfg["dropout_rate"])
    spec_share = _v(spec_cfg["speculator_share_of_applicants"])
    spec_min = _v(spec_cfg["speculator_min_decile"])
    g = _v(gm["income_gradient"])
    nd_ = NormalDist()

    def static_points(h):
        p = pts["per_child"] * min(h.children, pts["max_children_counted"])
        p += pts["per_extra_adult"] * (h.adults - 1)
        p += pts["disability"] * h.disab + pts["care"] * h.care + pts["roots"] * h.roots
        return p

    pop = []
    years = _v(cfg["years"])
    backlog = _v(cfg["initial_backlog_years"])
    ncand = _v(cfg["candidates_per_year"])
    hid = 0
    for year in range(-backlog, years):
        applied = []
        for _ in range(ncand):
            h = Household()
            h.decile = rng.randint(1, 10)
            r = rng.random()
            k, c = 0, kp[0]
            while r > c and k < len(kp) - 1:
                k += 1
                c += kp[k]
            h.children = k
            h.adults = 1 + (rng.random() < _v(hh["extra_adult_prob"]))
            tilt = 1 + _v(hh["disability_income_tilt"]) * (5.5 - h.decile) / 4.5
            h.disab = rng.random() < _v(hh["disability_prob"]) * tilt
            h.care = rng.random() < _v(hh["care_prob"])
            h.roots = rng.random() < _v(hh["roots_prob"])
            r = rng.random()
            h.work = next(i for i, c in enumerate(jcum) if r <= c)
            zq = nd_.inv_cdf((h.decile - rng.random()) / 10.0)
            h.income = math.exp(sigma * zq)
            u = [zones[z]["appeal"] + rng.gauss(0, tsd) - ccost * dist[z][h.work] for z in range(nz)]
            h.fallback = max(other, key=lambda z: u[z])
            h.prefs = sorted([z for z in desirable if u[z] > u[h.fallback]], key=lambda z: -u[z])
            h.spec = False
            # extra uniform draws kept in a fixed order for reproducibility
            h.reg = rng.random()
            cheat_u = rng.random()
            h.deter_u = rng.random()
            h.drop_year = year + 1 + int(math.log(1 - rng.random()) / math.log(1 - drop)) if drop > 0 else 10**9
            if not h.prefs:
                continue
            h.high_need = h.children > 0 or h.disab or h.care
            gp = gaming_rate * (1 + g * (h.decile - 5.5) / 4.5)
            h.cheat = (not h.care) and cheat_u < gp
            h.static_pts = static_points(h)
            applied.append(h)
        # speculators: owners of a home elsewhere seeking an (empty) desirable second home
        nspec = int(round(spec_share * len(applied) / (1 - spec_share)))
        for _ in range(nspec):
            h = Household()
            h.decile = rng.randint(spec_min, 10)
            h.children, h.adults = 0, 2
            h.disab = h.care = False
            h.roots = rng.random() < _v(hh["roots_prob"])
            r = rng.random()
            h.work = next(i for i, c in enumerate(jcum) if r <= c)
            h.income = math.exp(sigma * nd_.inv_cdf((h.decile - rng.random()) / 10.0))
            u = {z: zones[z]["appeal"] + rng.gauss(0, tsd) for z in desirable}
            h.prefs = sorted(desirable, key=lambda z: -u[z])
            h.fallback = h.work if h.work in other else other[0]
            h.spec = True
            h.reg = rng.random()
            cheat_u = rng.random()
            h.deter_u = rng.random()
            h.drop_year = year + 1 + int(math.log(1 - rng.random()) / math.log(1 - drop)) if drop > 0 else 10**9
            h.high_need = False
            h.cheat = cheat_u < gaming_rate * (1 + g * (h.decile - 5.5) / 4.5)
            h.static_pts = pts["per_extra_adult"] + pts["roots"] * h.roots
            applied.append(h)
        rng.shuffle(applied)
        for h in applied:
            h.hid = hid
            hid += 1
            h.arrive = year
            pop.append(h)
    return pop, dist


# ----------------------------------------------------------------- matching
def deferred_acceptance(applicants, vac, prio):
    """Applicant-proposing DA. prio(h, z) -> float, lower = higher priority.
    Returns {zone: [households]}; each household matched to at most one zone."""
    held = {z: [] for z in vac}
    nxt = [0] * len(applicants)
    free = list(range(len(applicants) - 1, -1, -1))
    while free:
        i = free.pop()
        prefs = applicants[i].prefs
        while nxt[i] < len(prefs):
            z = prefs[nxt[i]]
            nxt[i] += 1
            cap = vac.get(z, 0)
            if cap <= 0:
                continue
            p = prio(applicants[i], z)
            heap = held[z]
            if len(heap) < cap:
                heappush(heap, (-p, i))
                break
            if -heap[0][0] > p:
                _, j = heapreplace(heap, (-p, i))
                free.append(j)
                break
    return {z: [applicants[i] for _, i in heap] for z, heap in held.items()}


# ----------------------------------------------------------------- one run
def run(cfg, method, seed, rule=True, gaming_rate=0.0, audit=0.0, build_pct=0.0,
        spread_jobs=0.0, return_ledger=False, population=None):
    zones = _v(cfg["zones"])
    pts = cfg["points"]
    spec = cfg["speculation"]
    years = _v(cfg["years"])
    if population is None:
        population = generate_population(cfg, seed, gaming_rate, spread_jobs)
    pop, dist = population
    for h in pop:  # reset mutable state (population may be reused across methods)
        h.housed_year = h.housed_zone = None
        h.banned_until = -10**9
        h.ever_caught = False
        h.applied = True
    rng = random.Random(seed * 104729 + METHODS.index(method) * 31 + 7)
    desirable = [i for i, z in enumerate(zones) if z["desirable"]]
    stock = {z: zones[z]["stock"] for z in desirable}
    e0 = _v(spec["initial_empty_share"])
    empty = {z: int(round(stock[z] * e0)) for z in desirable}
    occ = {z: stock[z] - empty[z] for z in desirable}
    vacant = {z: 0 for z in desirable}
    extra = {z: int(round(stock[z] * build_pct / 100.0)) for z in desirable}
    built = {z: 0 for z in desirable}
    turnover = _v(cfg["turnover_rate"])
    release = _v(spec["empty_release_rate"])
    detect = _v(spec["rule_detection_rate"])
    deter = _v(spec["rule_deterrence"])
    ban = _v(cfg["gaming"]["ban_years"])
    cap_w, per_w = pts["max_waiting_points"], pts["per_year_waiting"]
    bw = pts["band_width"]
    open_share = _v(cfg["open_lottery_share"])
    near_km = pts["commute_near_km"]
    bid_sd = _v(cfg["market"]["bid_noise_sd"])
    spec_mult = _v(cfg["market"]["speculator_bid_multiplier"])

    def commute_pts(h, z):
        if h.work == z:
            return pts["commute_same_zone"]
        return pts["commute_near"] if dist[z][h.work] <= near_km else 0

    by_year = {}
    for h in pop:
        if h.spec and rule and h.deter_u < deter:
            h.applied = False
            continue  # deterred by the must-live-in rule: never applies
        by_year.setdefault(max(h.arrive, 0), []).append(h)
    pool = []
    ledger = []
    empty_share_by_year = []
    allocations = 0
    false_claim_allocs = 0
    caught_total = 0
    for t in range(years):
        # 1. stock flows
        for z in desirable:
            r_occ = binom(rng, occ[z], turnover)
            r_emp = binom(rng, empty[z], release)
            det = binom(rng, empty[z] - r_emp, detect) if rule else 0
            occ[z] -= r_occ
            empty[z] -= r_emp + det
            target = extra[z] * (t + 1) // years
            nb = target - built[z]
            built[z] = target
            stock[z] += nb
            vacant[z] += r_occ + r_emp + det + nb
        # 2. pool update
        pool.extend(by_year.get(t, []))
        pool = [h for h in pool if h.housed_year is None and h.drop_year > t]
        active = [h for h in pool if h.banned_until <= t]
        # 3. priorities for this year
        draw = {h.hid: rng.random() for h in active}
        if method == "market":
            bid = {h.hid: h.income * math.exp(rng.gauss(0, bid_sd)) * (spec_mult if h.spec else 1.0)
                   for h in active}

        def score(h, z):
            p = h.static_pts + min(t - h.arrive, cap_w) * per_w + commute_pts(h, z)
            if h.cheat and not h.ever_caught:
                p += pts["care"]
            return p

        if method == "queue":
            prio = lambda h, z: h.arrive + h.reg  # noqa: E731
        elif method == "points":
            prio = lambda h, z: -score(h, z) + (h.arrive + h.reg) * 1e-3  # noqa: E731
        elif method in ("points_lottery", "points_lottery_open"):
            prio = lambda h, z: -(score(h, z) // bw) + draw[h.hid]  # noqa: E731
        elif method == "lottery":
            prio = lambda h, z: draw[h.hid]  # noqa: E731
        elif method == "market":
            prio = lambda h, z: -bid[h.hid]  # noqa: E731
        else:
            raise ValueError(method)
        vac = {z: vacant[z] for z in desirable}
        # 4. match, audit successful claims, re-match until clean
        audited = set()
        uses_points = method in POINT_METHODS

        def audited_match(cands, capacity, pr):
            nonlocal caught_total
            while True:
                m = deferred_acceptance(cands, capacity, pr)
                caught = []
                if uses_points and audit > 0:
                    for hs in m.values():
                        for h in hs:
                            if h.cheat and not h.ever_caught and h.hid not in audited:
                                audited.add(h.hid)
                                if rng.random() < audit:
                                    caught.append(h)
                if not caught:
                    return m, cands
                for h in caught:
                    h.ever_caught = True
                    h.banned_until = t + ban
                caught_total += len(caught)
                cs = {h.hid for h in caught}
                cands = [h for h in cands if h.hid not in cs]

        if method == "points_lottery_open":
            # HDB-style quota: share q of vacancies by points bands, rest by open lottery
            vac_pts = {z: int(round(vac[z] * (1 - open_share))) for z in desirable}
            match, active = audited_match(active, vac_pts, prio)
            got = {h.hid for hs in match.values() for h in hs}
            rest = [h for h in active if h.hid not in got]
            vac_open = {z: vac[z] - len(match[z]) for z in desirable}
            m2 = deferred_acceptance(rest, vac_open, lambda h, z: draw[h.hid])
            for z in desirable:
                match[z] = match[z] + m2[z]
        else:
            match, active = audited_match(active, vac, prio)
        for z, hs in match.items():
            for h in hs:
                assert h.housed_year is None
                h.housed_year, h.housed_zone = t, z
                vacant[z] -= 1
                allocations += 1
                if h.cheat and not h.ever_caught and uses_points:
                    false_claim_allocs += 1
                if h.spec:
                    empty[z] += 1
                else:
                    occ[z] += 1
        tot_stock = sum(stock.values())
        empty_share_by_year.append(sum(empty.values()) / tot_stock)
        if return_ledger:
            ledger.append({z: {"stock": stock[z], "occ": occ[z], "empty": empty[z], "vacant": vacant[z]}
                           for z in desirable})
    metrics = compute_metrics(cfg, pop, dist, empty_share_by_year, allocations,
                              false_claim_allocs, caught_total)
    if return_ledger:
        metrics["_ledger"] = ledger
        metrics["_pop"] = pop
    return metrics


# ----------------------------------------------------------------- metrics
def _pct(xs, q):
    if not xs:
        return float("nan")
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def compute_metrics(cfg, pop, dist, empty_share_by_year, allocations, false_allocs, caught):
    c0, c1 = _v(cfg["cohort_first_year"]), _v(cfg["cohort_last_year"])
    coh = [h for h in pop if c0 <= h.arrive <= c1 and h.applied]
    res = [h for h in coh if not h.spec]
    waits = [h.housed_year - h.arrive for h in res if h.housed_year is not None]
    in5 = lambda h: h.housed_year is not None and h.housed_year - h.arrive <= 5  # noqa: E731
    hn = [h for h in res if h.high_need]
    lo = [h for h in res if not h.high_need]
    commute = []
    for h in res:
        home = h.housed_zone if in5(h) else h.fallback
        commute.append(dist[home][h.work])
    win_commute = [dist[h.housed_zone][h.work] for h in res if h.housed_year is not None]
    # income fairness: allocation rate by decile relative to overall (all applicants incl. speculators)
    n_d = [0] * 11
    w_d = [0] * 11
    for h in coh:
        n_d[h.decile] += 1
        w_d[h.decile] += h.housed_year is not None
    overall = sum(w_d) / max(1, sum(n_d))
    ratio = [(w_d[d] / n_d[d]) / overall if n_d[d] and overall else float("nan") for d in range(1, 11)]
    share = [w_d[d] / max(1, sum(w_d)) for d in range(1, 11)]
    xs = list(range(1, 11))
    mx = statistics.fmean(xs)
    my = statistics.fmean(ratio)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ratio)) / sum((x - mx) ** 2 for x in xs)
    spec_coh = [h for h in coh if h.spec]
    winners = [h for h in coh if h.housed_year is not None]
    return {
        "n_resident_applicants": len(res),
        "share_housed_ever": sum(h.housed_year is not None for h in res) / max(1, len(res)),
        "share_housed_within_5y": sum(in5(h) for h in res) / max(1, len(res)),
        "wait_mean_housed": statistics.fmean(waits) if waits else float("nan"),
        "wait_p90_housed": _pct(waits, 0.9),
        "high_need_housed_within_5y": sum(in5(h) for h in hn) / max(1, len(hn)),
        "low_need_housed_within_5y": sum(in5(h) for h in lo) / max(1, len(lo)),
        "commute_km_all_at_5y": statistics.fmean(commute),
        "commute_km_winners": statistics.fmean(win_commute) if win_commute else float("nan"),
        "decile_alloc_ratio": ratio,
        "decile_alloc_share": share,
        "income_gradient_slope": slope,
        "d10_over_d1": min(99.0, ratio[9] / ratio[0]) if ratio[0] else 99.0,
        "d10_minus_d1": ratio[9] - ratio[0],
        "speculator_share_of_allocations": sum(1 for h in spec_coh if h.housed_year is not None) / max(1, len(winners)),
        "empty_share_final": empty_share_by_year[-1],
        "empty_share_mean": statistics.fmean(empty_share_by_year),
        "false_claim_share_of_allocations": false_allocs / max(1, allocations),
        "cheaters_caught": caught,
    }


# ----------------------------------------------------------------- experiments
def aggregate(runs):
    out = {}
    for k in runs[0]:
        if k.startswith("_"):
            continue
        v = [r[k] for r in runs]
        if isinstance(v[0], list):
            out[k] = [round(statistics.fmean(col), 4) for col in zip(*v)]
        else:
            v = [x for x in v if isinstance(x, (int, float)) and math.isfinite(x)]
            if not v:
                out[k] = {"mean": None, "sd": None}
                continue
            m = statistics.fmean(v)
            sd = statistics.stdev(v) if len(v) > 1 else 0.0
            out[k] = {"mean": round(m, 4), "sd": round(sd, 4)}
    return out


def scenario(cfg, name, methods, seeds, **kw):
    res = {}
    pops = {s: generate_population(cfg, s, kw.get("gaming_rate", 0.0), kw.get("spread_jobs", 0.0))
            for s in seeds}
    for m in methods:
        res[m] = aggregate([run(cfg, m, s, population=pops[s], **kw) for s in seeds])
    return {"settings": kw, "seeds": seeds, "methods": res}


def run_all(cfg):
    sm, ss = _v(cfg["seeds_main"]), _v(cfg["seeds_sensitivity"])
    out = {}
    out["baseline"] = scenario(cfg, "baseline", METHODS, sm, rule=True)
    out["no_live_in_rule"] = scenario(cfg, "no_rule", METHODS, ss, rule=False)
    for r in _v(cfg["gaming"]["rates"])[1:]:
        for a in _v(cfg["gaming"]["audit_probs"]):
            out[f"gaming_{int(r*100)}pct_audit_{int(a*100)}pct"] = scenario(
                cfg, "gaming", list(POINT_METHODS), ss, rule=True, gaming_rate=r, audit=a)
    for b in _v(cfg["build_more_pct"]):
        out[f"build_more_{b}pct"] = scenario(cfg, "build", METHODS, ss, rule=True, build_pct=b)
    sj = _v(cfg["spread_jobs_share"])
    out["spread_jobs"] = scenario(cfg, "spread", METHODS, ss, rule=True, spread_jobs=sj)
    out["unira_package"] = scenario(cfg, "package", METHODS, ss, rule=True, build_pct=25,
                                    spread_jobs=sj, gaming_rate=0.10, audit=0.25)
    return out


SUMMARY_KEYS = ["wait_mean_housed", "wait_p90_housed", "share_housed_within_5y",
                "high_need_housed_within_5y", "low_need_housed_within_5y",
                "commute_km_all_at_5y", "commute_km_winners", "income_gradient_slope",
                "d10_over_d1", "d10_minus_d1", "speculator_share_of_allocations", "empty_share_final",
                "empty_share_mean", "false_claim_share_of_allocations"]


def write_outputs(results, cfg, elapsed):
    od = os.path.join(HERE, "outputs")
    os.makedirs(od, exist_ok=True)
    payload = {"about": "UNIRA v79 housing allocation simulation; see RESEARCH_NOTE.md",
               "scenarios": results}  # run time is printed, not stored, so outputs are byte-identical
    with open(os.path.join(od, "results.json"), "w") as f:
        json.dump(payload, f, indent=1)
    with open(os.path.join(od, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "method", "n_seeds"] + [f"{k}_mean" for k in SUMMARY_KEYS]
                   + [f"{k}_sd" for k in SUMMARY_KEYS] + [f"decile{d}_alloc_ratio" for d in range(1, 11)])
        for sc, body in results.items():
            for m, agg in body["methods"].items():
                w.writerow([sc, m, len(body["seeds"])] + [agg[k]["mean"] for k in SUMMARY_KEYS]
                           + [agg[k]["sd"] for k in SUMMARY_KEYS] + agg["decile_alloc_ratio"])


def main():
    t0 = time.time()
    cfg = load_config()
    results = run_all(cfg)
    el = time.time() - t0
    write_outputs(results, cfg, el)
    b = results["baseline"]["methods"]
    print(f"runtime {el:.1f}s")
    print(f"{'method':15s} wait  p90  hn<=5y  lo<=5y  commute  D10/D1  slope")
    for m in METHODS:
        a = b[m]
        print(f"{m:15s} {a['wait_mean_housed']['mean']:4.1f} {a['wait_p90_housed']['mean']:4.1f}"
              f"  {a['high_need_housed_within_5y']['mean']:.3f}   {a['low_need_housed_within_5y']['mean']:.3f}"
              f"   {a['commute_km_all_at_5y']['mean']:5.2f}   {a['d10_over_d1']['mean']:5.2f}  {a['income_gradient_slope']['mean']:+.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
