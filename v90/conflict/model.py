"""UNIRA V9.0 — can fair distribution of resources reduce armed conflict, and does that speed up universal prosperity?

Country-level stochastic model of conflict, coupled both ways with the V8.9 living-standard model (v89 core):
  conflict -> UNIRA:  in conflict, delivery is halved (as in V8.9) and the quarter of the population living in conflict
                      zones (PRIO: 473 m of 1.9 bn children in conflict-affected countries) gets no service but food
  UNIRA -> conflict:  a living-standard index LS (0.7 x Level 1 + 0.3 x Level 2 coverage of the country) lowers the
                      deprivation-linked part of the onset risk and raises the chance that a conflict ends

Each country-year (two-state Markov chain):
    onset  h_k(t) = H x [ s_ne x g(LS_k(0)) + (1 - s_ne) x g(LS*_k(t)) ] x prevention x relapse x backlash
    end    e_k(t) = E0 x (1 + tau x (LS*_k(t) - LS_k(0))) x diplomacy
    g(x) = exp(-beta x x) / mean_k exp(-beta x LS_k(0))     (observed gradient: poorer countries fight more)
    LS*  = LS_k(0) + c x (LS_k(t) - LS_k(0))                (c = causal fraction of that gradient)
  LS_k(0) today's living standards from OBSERVED data: mean access to basic water, basic sanitation, clean cooking and
         electricity (World Bank WDI / JMP, latest year; v87 raw data). Later years: the higher of that and the
         UNIRA coverage index 0.7 x Level 1 + 0.3 x Level 2 of the country
  beta   steepness of the cross-country gradient, FITTED by maximum likelihood to which countries are in conflict today
         (World Bank FY26) given LS_k(0). This is an ASSOCIATION, and inflated by reverse causation (conflict destroys
         services), which is why the causal fraction c below is separate and uncertain
  s_ne   share of risk that does not move with living standards even if the gradient were causal: territory, identity,
         political exclusion (Cederman et al. 2011), state weakness (Fearon & Laitin read income as state capacity).
         ASSUMPTION range 0.3-0.6
  c      how much of the observed gradient is causal. Miguel et al. (2004) show income shocks cause conflict;
         Berman et al. (2011) find no unemployment-insurgency link. ASSUMPTION range 0-1: this is THE key unknown
  relapse x4 for 10 years after a conflict ends (about 40% relapse in 10 years; literature 20-57%)
  backlash x(1 + b) on onset in conflict and fragile countries in programme years 1-3 (Crost et al. 2014 measured
         +110-185% insurgent attacks locally; the national effect is an ASSUMPTION)
  E0 = 0.10 a year (median duration 6-7 years). H is calibrated so that scenario A keeps today's number of
  countries in conflict (World Bank FY26 list) on average over 80 years.
Scenarios (delivery as V8.9 accelerated, so only conflict differs):
  A  no conflict reduction: c = 0 (risks stay at today's level in every country; conflicts end and start as today)
  B  moderate: c = 0.5, s_ne = 0.5, tau = 1, backlash 0.5
  C  strong: c = 1, s_ne = 0.3, tau = 1, backlash 0.25 (participation and protection safeguards)
  D  conditional long-term peace (UPPER BOUND, not a forecast): as C, plus HYPOTHETICAL diplomacy and reconciliation
     that cut the non-economic risk to a tenth over 50 years and triple the chance of ending a conflict
Monte Carlo over random draws (common random numbers across scenarios); the two-way coupling is solved by iterating
conflict paths and living-standard paths three times.
python3 model.py  ->  ../outputs/conflict.json"""
import importlib.util
import json
import math
import random
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
spec = importlib.util.spec_from_file_location("v89", U / "v89" / "integrated" / "simulate.py")
V89 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V89)

YEARS = V89.YEARS
BACKLASH_YEARS, RECUR_YEARS = 3, 10
COMMON = {"beta": None, "e0": 0.10, "recur": 4.0, "affected": 0.25, "tau": 1.0, "diplomacy": False}
SCEN = {
    "A_no_reduction": COMMON | {"c": 0.0, "s_ne": 0.5, "tau": 0.0, "backlash": 0.0},
    "B_moderate": COMMON | {"c": 0.5, "s_ne": 0.5, "backlash": 0.5},
    "C_strong": COMMON | {"c": 1.0, "s_ne": 0.3, "backlash": 0.25},
    "D_long_term_peace": COMMON | {"c": 1.0, "s_ne": 0.3, "backlash": 0.25, "diplomacy": True}}
SENS_BASE = "B_moderate"
SENS = {  # one change at a time from scenario B
    "beta_half": {"beta_mult": 0.5}, "beta_x1.5": {"beta_mult": 1.5},  # multiples of the fitted value
    "c_0.25": {"c": 0.25}, "c_1": {"c": 1.0},
    "s_ne_0.3": {"s_ne": 0.3}, "s_ne_0.7": {"s_ne": 0.7},
    "backlash_0": {"backlash": 0.0}, "backlash_1.85": {"backlash": 1.85},
    "relapse_x2": {"recur": 2.0}, "relapse_x6": {"recur": 6.0},
    "end_rate_0.07": {"e0": 0.07}, "end_rate_0.15": {"e0": 0.15},
    "affected_0.15": {"affected": 0.15}, "affected_0.40": {"affected": 0.40}}
DELIVERY = V89.SCEN["accelerated"]
RUNS, SENS_RUNS, ITER = 30, 10, 3
ACCESS = ("SH.H2O.BASW.ZS", "SH.STA.BASS.ZS", "EG.CFT.ACCS.ZS", "EG.ELC.ACCS.ZS")


def today_index(keys):
    """Observed living-standard index today: mean of the latest access rates (0-1) available for the country."""
    ser = {c: V89.L87.series(c) for c in ACCESS}
    out = {}
    for k in keys:
        v = [s[k][max(s[k])] / 100 for s in ser.values() if s.get(k)]
        out[k] = min(1.0, statistics.fmean(v)) if v else None
    fill = statistics.median(x for x in out.values() if x is not None)
    return {k: (fill if v is None else v) for k, v in out.items()}


def fit_beta(ctx, today, e0=0.10):
    """Maximum-likelihood slope of today's conflict state on LS(0): stationary chance of being in conflict
    h / (h + e0), h = H exp(-beta LS) / mean exp(-beta LS), H set so the expected count equals today's."""
    conf = set(ctx["fcs"]["conflict"])
    target = sum(1 for k in today if k in conf)
    best = None
    for i in range(0, 81):
        beta = i * 0.25
        norm = statistics.fmean(math.exp(-beta * x) for x in today.values())
        lo, hi = 1e-5, 5.0
        for _ in range(60):
            H = (lo + hi) / 2
            pi = {k: min(0.95, H * math.exp(-beta * x) / norm) for k, x in today.items()}
            n = sum(h / (h + e0) for h in pi.values())
            lo, hi = (H, hi) if n < target else (lo, H)
        ll = sum(math.log(h / (h + e0)) if k in conf else math.log(e0 / (h + e0)) for k, h in pi.items())
        if best is None or ll > best[0]:
            best = (ll, beta)
    return best[1], round(best[0], 2)
QS = ("90pct", "95pct", "99pct", "100pct")


class Risk:
    """Onset and end probabilities for one parameter set."""

    def __init__(self, p, H, ls0):
        self.p, self.H, self.ls0 = p, H, ls0
        self.norm = statistics.fmean(math.exp(-p["beta"] * v[0]) for v in ls0.values())
        self.g0 = {k: self.g(v[0]) for k, v in ls0.items()}

    def g(self, x):
        return math.exp(-self.p["beta"] * x) / self.norm

    def ls_star(self, k, ls, t):
        a = self.ls0[k][0]
        return a + self.p["c"] * (ls[k][t] - a)

    def parts(self, k, ls, t):
        """(frozen part, responsive part) of the onset risk before multipliers."""
        p = self.p
        s_ne = p["s_ne"] * (1 - 0.9 * min(1.0, t / 50)) if p["diplomacy"] else p["s_ne"]
        resp = self.g0[k] if not p["c"] else self.g(self.ls_star(k, ls, t))
        return self.H * s_ne * self.g0[k], self.H * (1 - p["s_ne"]) * resp

    def onset(self, k, ls, t, recent, exposed):
        h = sum(self.parts(k, ls, t))
        if recent:
            h *= self.p["recur"]
        if exposed and 1 <= t <= BACKLASH_YEARS:
            h *= 1 + self.p["backlash"]
        return min(0.95, h)

    def end(self, k, ls, t):
        p = self.p
        e = p["e0"] * (1 + p["tau"] * (self.ls_star(k, ls, t) - self.ls0[k][0]))
        if p["diplomacy"]:
            e *= 1 + 2 * min(1.0, t / 30)
        return min(0.95, e)


def simulate_conflict(ctx, risk, ls, rng):
    """Country conflict paths given living-standard paths {iso: [LS per year]}."""
    keys = sorted(ls)
    start = set(ctx["fcs"]["conflict"])
    exposed = start | set(ctx["fcs"]["institutional_social_fragility"])
    state = {k: k in start for k in keys}
    since = {k: 99 for k in keys}
    path = {k: [] for k in keys}
    onsets = ends = 0
    for t in range(YEARS + 1):
        for k in keys:
            path[k].append(state[k])
            if t == YEARS:
                continue
            if state[k]:
                if rng.random() < risk.end(k, ls, t):
                    state[k], since[k] = False, 0
                    ends += 1
            else:
                if rng.random() < risk.onset(k, ls, t, since[k] < RECUR_YEARS, k in exposed):
                    state[k] = True
                    onsets += 1
                since[k] += 1
    return path, onsets, ends


def ls_from(core_res, today):
    """Living-standard paths: today's observed index in year 0, then the higher of it and UNIRA coverage."""
    pc = core_res["per_country"]
    return {k: [today[k]] + [max(today[k], 0.7 * a + 0.3 * b) for a, b in zip(pc["L1"][k][1:], pc["L2"][k][1:])] for k in pc["L1"]}


def couple(ctx, risk, ls0, today, seed):
    """Solve the two-way coupling for one random draw: conflict paths <-> living-standard paths."""
    p = risk.p
    frag = set(ctx["fcs"]["institutional_social_fragility"])
    ls = ls0
    for _ in range(ITER if p["c"] else 1):  # with c = 0 living standards do not feed back
        cpath, onsets, ends = simulate_conflict(ctx, risk, ls, random.Random(seed))  # same draws each pass
        inc = lambda k, t, cpath=cpath: k in cpath and cpath[k][t]
        govf = lambda k, t, inc=inc: 0.5 if inc(k, t) else (0.75 if k in frag else 1.0)
        capfn = lambda k, t, inc=inc: (1 - p["affected"]) if inc(k, t) else 1.0
        res = V89.core(ctx, DELIVERY, govf, capfn, conflict_status=inc, keep_country=True)
        ls = ls_from(res, today)
    return cpath, onsets, ends, res, ls


def calibrate(ctx, p, ls0, seeds=24):
    """H such that with today's living standards held fixed (scenario A), the mean number of countries in conflict over
    80 years equals today's (World Bank FY26 conflict list), relapse included: bisection on the simulated mean."""
    target = sum(1 for k in ctx["fcs"]["conflict"] if k in ls0)
    pa = p | {"c": 0.0, "tau": 0.0, "backlash": 0.0, "diplomacy": False}
    lo, hi = 1e-4, 0.1
    for _ in range(18):
        H = (lo + hi) / 2
        risk = Risk(pa, H, ls0)
        tot = 0.0
        for s in range(seeds):
            path, _, _ = simulate_conflict(ctx, risk, ls0, random.Random(10_000 + s))
            tot += sum(sum(v) for v in path.values()) / (YEARS + 1)
        lo, hi = (H, hi) if tot / seeds < target else (lo, H)
    return round((lo + hi) / 2, 6)


def dates_from(cov):
    return {f"{int(100 * q)}pct": next((t for t, v in enumerate(cov) if v >= q - 1e-12), None) for q in (0.9, 0.95, 0.99, 1.0)}


def summarise(vals):
    v = sorted(x for x in vals if x is not None)
    if not v:
        return {"median": None, "p10": None, "p90": None, "share_of_runs_reached": 0.0}
    q = lambda f: v[min(len(v) - 1, int(f * (len(v) - 1) + 0.5))]
    return {"median": q(0.5), "p10": q(0.1), "p90": q(0.9), "share_of_runs_reached": round(len(v) / len(vals), 2)}


def run_scenario(ctx, p, H, ls0, today, runs, pop, detail=True):
    W = sum(pop.values())
    risk = Risk(p, H, ls0)
    counts_all, zone_all, cy, ons, ends_l, d1, d2, l1p, l2p = [], [], [], [], [], [], [], [], []
    late = {k: 0.0 for k in ls0}
    frozen_share, bneck = [], None
    for seed in range(runs):
        cpath, onsets, ends, res, ls = couple(ctx, risk, ls0, today, seed)
        counts = [sum(cpath[k][t] for k in cpath) for t in range(YEARS + 1)]
        counts_all.append(counts)
        zone_all.append([sum(pop[k] * p["affected"] for k in cpath if cpath[k][t]) / W for t in range(YEARS + 1)])
        cy.append(sum(counts))
        ons.append(onsets)
        ends_l.append(ends)
        for k in cpath:
            late[k] += sum(cpath[k][40:]) / (YEARS - 39) / runs
        fz = rs = 0.0
        for k in ls0:  # which part of the remaining onset risk in the last decade does not move with living standards?
            for t in range(YEARS - 10, YEARS):
                a, b = risk.parts(k, ls, t)
                fz, rs = fz + a, rs + b
        frozen_share.append(fz / (fz + rs))
        if seed == 0:  # yearly bottleneck of one representative draw
            bneck = {f"year_{t}": {L: {x: res["bottleneck"][t][L][x] for x in ("domain", "type", "people_short_m", "share_in_conflict_states")}
                                   for L in ("L1", "L2")} for t in (1, 5, 10, 20, 30, 40, 60, 80)}
        d1.append(dates_from(res["cov"]["L1"]))
        d2.append(dates_from(res["cov"]["L2"]))
        l1p.append(res["cov"]["L1"])
        l2p.append(res["cov"]["L2"])
    mean = lambda rows, t: statistics.fmean(r[t] for r in rows)
    out = {"conflict_country_years_80y": round(statistics.fmean(cy), 1),
           "L1_dates": {q: summarise([d[q] for d in d1]) for q in QS},
           "L2_dates": {q: summarise([d[q] for d in d2]) for q in QS}}
    if detail:
        cty = ctx["cty"]
        out |= {
            "countries_in_conflict": {f"year_{t}": round(mean(counts_all, t), 1) for t in (0, 5, 10, 20, 30, 40, 60, 80)},
            "countries_in_conflict_p10_p90_year_40": [summarise([c[40] for c in counts_all])[x] for x in ("p10", "p90")],
            "share_of_humanity_in_conflict_zones": {f"year_{t}": round(mean(zone_all, t), 4) for t in (0, 5, 10, 20, 30, 40, 60, 80)},
            "onsets_80y": round(statistics.fmean(ons), 1), "resolutions_80y": round(statistics.fmean(ends_l), 1),
            "countries_in_conflict_year_80": round(mean(counts_all, YEARS), 1), "yearly_bottleneck_first_draw": bneck,
            "share_of_remaining_onset_risk_not_linked_to_living_standards_last_decade": round(statistics.fmean(frozen_share), 2),
            "highest_remaining_conflict_risk_years_40_80": [
                {"iso": k, "name": cty[k].get("name", k), "share_of_years_in_conflict": round(v, 2),
                 "today": ctx["status"].get(k, "other")} for k, v in sorted(late.items(), key=lambda x: (-x[1], x[0]))[:12]],
            "L1_mean_coverage": {f"year_{t}": round(mean(l1p, t), 4) for t in (5, 10, 20, 30, 40, 60, 80)},
            "L2_mean_coverage": {f"year_{t}": round(mean(l2p, t), 4) for t in (5, 10, 20, 30, 40, 60, 80)}}
    return out


def deprivation_share(p, ls0):
    """Q1: share of today's onset risk that would disappear if every country had full Level 1 and Level 2 (LS = 1),
    if the observed gradient were fully causal (c = 1); scaled by c it is the plausibly causal share."""
    risk = Risk(p | {"c": 1.0, "diplomacy": False}, 1.0, ls0)
    now = sum(sum(risk.parts(k, ls0, 0)) for k in ls0)
    full = {k: [1.0] * (YEARS + 1) for k in ls0}
    after = sum(sum(risk.parts(k, full, 0)) for k in ls0)
    return 1 - after / now


def fmt(d):
    return f"{d['median']} ({d['p10']}-{d['p90']}; {100 * d['share_of_runs_reached']:.0f}% of runs)" if d["median"] is not None else "not reached"


def main(runs=RUNS, sens_runs=SENS_RUNS, write=True, sens=True):
    ctx = V89.context()
    gov0, status0 = ctx["gov"], ctx["status"]
    base = V89.core(ctx, DELIVERY, lambda k, t: gov0.get(k, 1.0),
                    lambda k, t: (1 - COMMON["affected"]) if status0.get(k) == "conflict" else 1.0, keep_country=True)
    today = today_index(sorted(base["per_country"]["L1"]))
    ls0 = ls_from(base, today)  # starting living-standard paths: today's conflicts held fixed
    beta, ll = fit_beta(ctx, today)
    scen = {n: p | {"beta": beta} for n, p in SCEN.items()}
    pop = {k: ctx["cty"][k]["pop"] for k in ls0}
    v89 = V89.core(ctx, DELIVERY, lambda k, t: gov0.get(k, 1.0))["dates"]
    v89_end = V89.core(ctx, V89.SCEN["accelerated_if_conflicts_end"], lambda k, t: 1.0)["dates"]
    Hc = {}
    def hz(p):  # with c = 0 the share s_ne does not change the risk, so H depends only on these
        key = (p["beta"], p["e0"], p["recur"])
        if key not in Hc:
            Hc[key] = calibrate(ctx, p, ls0)
        return Hc[key]
    conf = set(ctx["fcs"]["conflict"])
    q = sorted(today.values())
    quart = [q[int(f * (len(q) - 1))] for f in (0.25, 0.5, 0.75)]
    band = lambda x: sum(x > b for b in quart)
    out = {"fitted_beta": beta, "log_likelihood": ll,
           "observed_conflict_rate_today_by_living_standard_quartile": [
               round(sum(1 for k in today if band(today[k]) == i and k in conf) / max(1, sum(1 for k in today if band(today[k]) == i)), 3) for i in range(4)],
           "countries": len(ls0), "countries_in_conflict_today": sum(1 for k in ctx["fcs"]["conflict"] if k in ls0),
           "runs": runs, "sensitivity_runs": sens_runs,
           "v89_reference": {"accelerated_todays_conflicts_never_end": v89, "accelerated_if_all_conflicts_end_now": v89_end},
           "deprivation_linked_share_of_todays_onset_risk": {}, "scenarios": {}, "sensitivity": {}}
    for s_ne in (0.3, 0.5, 0.7):
        for m in (0.5, 1.0, 1.5):
            out["deprivation_linked_share_of_todays_onset_risk"][f"s_ne_{s_ne}/beta_x{m}"] = round(
                deprivation_share(COMMON | {"s_ne": s_ne, "beta": beta * m}, ls0), 3)
    print(f"fitted beta {beta} (log-likelihood {ll}); conflict rate today by living-standard quartile (lowest first):",
          out["observed_conflict_rate_today_by_living_standard_quartile"])
    print("share of today's onset risk linked to deprivation if the gradient were fully causal:",
          out["deprivation_linked_share_of_todays_onset_risk"])
    print(f"V8.9 accelerated (today's conflicts never end): L1 {v89['L1']}, L2 {v89['L2']}")
    a_cy = None
    for name, p in scen.items():
        H = hz(p)
        s = run_scenario(ctx, p, H, ls0, today, runs, pop) | {"params": p, "calibrated_onset_H": H}
        a_cy = a_cy or s["conflict_country_years_80y"]
        s["conflict_country_years_avoided_vs_A"] = round(a_cy - s["conflict_country_years_80y"], 1)
        s["share_of_conflict_burden_avoided_vs_A"] = round(1 - s["conflict_country_years_80y"] / a_cy, 3)
        a_on = out["scenarios"]["A_no_reduction"]["onsets_80y"] if out["scenarios"] else s["onsets_80y"]
        s["conflicts_prevented_vs_A"] = round(a_on - s["onsets_80y"], 1)  # onsets that do not happen
        s["years_of_conflict_reduced_vs_A"] = s.pop("conflict_country_years_avoided_vs_A")
        out["scenarios"][name] = s
        c = s["countries_in_conflict"]
        print(f"\n== {name}: countries in conflict yr 0/10/20/40/80: {c['year_0']}/{c['year_10']}/{c['year_20']}/{c['year_40']}/{c['year_80']}"
              f" | burden avoided vs A {100 * s['share_of_conflict_burden_avoided_vs_A']:.0f}% | onsets {s['onsets_80y']}, ended {s['resolutions_80y']}")
        for L in ("L1", "L2"):
            print(f"   {L}: " + " | ".join(f"{q}: {fmt(s[f'{L}_dates'][q])}" for q in QS))
        print("   highest remaining risk:", ", ".join(f"{r['iso']} {r['share_of_years_in_conflict']}" for r in s["highest_remaining_conflict_risk_years_40_80"][:8]),
              f"| remaining risk not linked to living standards: {100 * s['share_of_remaining_onset_risk_not_linked_to_living_standards_last_decade']:.0f}%")
    if not sens:
        return out
    pb = scen[SENS_BASE]
    ref = run_scenario(ctx, pb, hz(pb), ls0, today, sens_runs, pop, detail=False)
    out["sensitivity"]["base_" + SENS_BASE] = ref
    print(f"\nsensitivity (one change at a time from {SENS_BASE}, {sens_runs} runs; median year L1 90/95%, L2 90/95%, conflict-years):")
    for name, ch in SENS.items():
        p = pb | ch
        p["beta"] = round(beta * p.pop("beta_mult", 1.0), 3)
        r = run_scenario(ctx, p, hz(p), ls0, today, sens_runs, pop, detail=False)
        out["sensitivity"][name] = r
        print(f"   {name:15s} L1 {r['L1_dates']['90pct']['median']}/{r['L1_dates']['95pct']['median']}  "
              f"L2 {r['L2_dates']['90pct']['median']}/{r['L2_dates']['95pct']['median']}  conflict-years {r['conflict_country_years_80y']}")
    print(f"   {'(base)':15s} L1 {ref['L1_dates']['90pct']['median']}/{ref['L1_dates']['95pct']['median']}  "
          f"L2 {ref['L2_dates']['90pct']['median']}/{ref['L2_dates']['95pct']['median']}  conflict-years {ref['conflict_country_years_80y']}")
    if write:
        (HERE.parent / "outputs").mkdir(exist_ok=True)
        (HERE.parent / "outputs" / "conflict.json").write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main()
