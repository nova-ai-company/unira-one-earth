"""UNIRA V9.1 — can fair institutions reduce armed conflict, independently of better living standards?

Country-level stochastic conflict model (179 countries, 80 years), coupled with the V8.9 living-standard model as in
V9.0, but with the conflict risk ESTIMATED from history (panel.py, UCDP/PRIO 2000-2024):
    onset  logit P = a + bE x LS* + bQ x Q* + bR x relapse     (bE, bQ, bR: panel estimates; a calibrated, see below)
    end    P = observed rate of conflict ending (14% a year; neither LS nor Q predicts it in the panel)
    LS* = LS(0) + cE x (LS(t) - LS(0))    Q* = Q(0) + cQ x (Q(t) - Q(0))
  cE  causal fraction of the living-standard association: 0.5 in EVERY scenario (V9.0 central), so scenario
      differences come from institutions only; the factorial test switches it off (cE = 0) to separate the two
  cQ  causal fraction of the institutional association: 0.5 central, 0.25 and 1.0 as the uncertainty band. The panel
      gives an ASSOCIATION (perception-based indicators, reverse causation), not a causal effect
Institutional quality Q (0..1, WGI 2024) changes by scenario at HISTORICAL paces (10-year changes 2004-2024):
  A  baseline: today's institutions continue (Q constant), no new mechanisms
  B  moderate reform (transparency, representation, grievance mechanisms): the pace of the top quarter of countries;
     power sharing and grievance redress lower relapse risk a little
  C  strong reform (independent justice, anti-corruption, civilian mediation): the pace of the top tenth; mediation
     prevents some local escalation and helps end conflicts; post-conflict institutions lower relapse
  D  comprehensive (C plus sustained cooperation between communities and effective conflict prevention): the pace of
     the top twentieth; HYPOTHETICAL at this scale - an upper bound, not a forecast
Risks of reform, in every reform scenario:
  reversal    each decade, a country's reform gains are undone with the historical probability (1 in 3 gains reversed
              2014-2024); protections against concentrated power lower it in C and D (ASSUMPTION, tested)
  tension     where institutions are weak (Q < 0.35) and change faster than the top-quarter pace, onset risk rises
              (Hegre et al. 2001; Cederman, Hug & Krebs 2010; the panel is inconclusive) - ASSUMPTION range 0-100%
  no progress during conflict years
Conflict affects min(25%, 30 million) of a country's people, and delivery falls in proportion (halved when a quarter
of the country is affected), so a local insurgency in a large country is not treated like a national war.
Reform also improves delivery: in fragile countries the delivery factor rises from 0.75 to 1 as Q reaches the median
of non-fragile countries. Corruption losses fall with Q (26% at Q <= 0.3, 10% at 0.5, 5% at >= 0.7; WIN 2016, 2024).
Civilian harm: UCDP battle deaths and one-sided violence per conflict-country-year 2015-2024 (mean and median).
Costs in workers (UNIRA counts hours, not money): judges, mediators, auditors per 100,000 people (evidence.csv).
Mechanism effects (ASSUMPTIONS informed by evidence.csv): mediation and early intervention cut onset by 10% (C) or
15% (D) at national scale (Blattman et al. 2014: violent land disputes -41% locally, gains faded by year 3) and raise
the chance of ending by 30-50%, but mediated settlements relapse 15% more (Beardsley 2011); power sharing, justice and,
in D, peace operations cut relapse by 15/30/50% (Hartzell & Hoddie 2003; Walter 2015; Fortna 2004: >55%);
cooperation between communities cuts onset by 5% in D (Mousa 2020: behaviour changed, attitudes did not generalise).
python3 model.py  ->  ../outputs/institutions.json"""
import importlib.util
import json
import math
import random
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
import sys
sys.path.insert(0, str(HERE))
import panel  # noqa: E402

spec = importlib.util.spec_from_file_location("v90", U / "v90" / "conflict" / "model.py")
V90 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V90)
V89 = V90.V89

YEARS = V89.YEARS
DELIVERY = V89.SCEN["accelerated"]
AFFECTED, RECUR_YEARS = 0.25, 10
ZONE_PEOPLE = 30e6  # ASSUMPTION: people inside the zone of one country's conflict (PRIO: about 1.2 bn people of all ages
                    # within 50 km of events in some 35-40 countries); a conflict affects at most a quarter of a country
WEAK_Q, TOP_Q = 0.35, 0.633          # weak institutions; reform ceiling = today's 75th percentile of countries (2024)
COMMON = {"cE": 0.5, "cQ": 0.5, "pace": 0.0, "reversal": 1 / 3, "tension": 0.3, "mediation": 0.0, "end_boost": 0.0,
          "relapse_cut": 0.0, "mediation_relapse": 0.0, "cooperation": 0.0}
SCEN = {  # pace = 10-year gain in Q (historical percentiles from panel.pace)
    "A_baseline": COMMON | {"tension": 0.0},
    "B_moderate_reform": COMMON | {"pace": "p75", "relapse_cut": 0.15},
    "C_strong_reform": COMMON | {"pace": "p90", "reversal": 0.25, "mediation": 0.10, "end_boost": 0.3, "relapse_cut": 0.3,
                                 "mediation_relapse": 0.15},
    "D_comprehensive_reform": COMMON | {"pace": "p95", "reversal": 0.15, "mediation": 0.15, "end_boost": 0.5, "relapse_cut": 0.5,
                                        "mediation_relapse": 0.15, "cooperation": 0.05}}
SENS_BASE = "C_strong_reform"
SENS = {"cQ_0.25": {"cQ": 0.25}, "cQ_1": {"cQ": 1.0}, "no_economic_channel": {"cE": 0.0},
        "tension_0": {"tension": 0.0}, "tension_1": {"tension": 1.0}, "reversal_historical": {"reversal": 1 / 3},
        "reversal_0.5": {"reversal": 0.5}, "pace_p75": {"pace": "p75"}, "mediation_0": {"mediation": 0.0, "end_boost": 0.0, "mediation_relapse": 0.0},
        "relapse_cut_0": {"relapse_cut": 0.0},
        # decomposition of C: the panel-estimated channel (institutional quality rising) versus the assumed mechanisms
        "only_institutional_quality": {"mediation": 0.0, "end_boost": 0.0, "relapse_cut": 0.0, "mediation_relapse": 0.0},
        "only_mechanisms": {"pace": 0.0, "tension": 0.0}}
RUNS, SENS_RUNS, ITER = 30, 10, 2
QS = ("90pct", "95pct", "99pct", "100pct")


def harm():
    """Deaths per conflict-country-year 2015-2024: state-based battle deaths plus one-sided violence against civilians."""
    cy = panel.conflict_years()
    bd, os_ = {}, {}
    for r in panel.ucdp_csv("ucdp-brd-conf-251-csv.zip"):
        if r["type_of_conflict"] in ("3", "4") and 2015 <= int(r["year"]) <= 2024:
            for g in r["gwno_loc"].split(","):
                iso = panel.GW.get(int(g))
                if iso:
                    bd[(iso, int(r["year"]))] = bd.get((iso, int(r["year"])), 0) + int(r["bd_best"]) / len(r["gwno_loc"].split(","))
    for r in panel.ucdp_csv("ucdp-onesided-251-csv.zip"):
        if 2015 <= int(r["year"]) <= 2024:
            for g in r["gwno_location"].split(","):
                iso = panel.GW.get(int(g))
                if iso:
                    os_[(iso, int(r["year"]))] = os_.get((iso, int(r["year"])), 0) + int(r["best_fatality_estimate"]) / len(r["gwno_location"].split(","))
    cys = [(k, y) for k, s in cy.items() for y in s if 2015 <= y <= 2024]
    b = [bd.get(x, 0.0) for x in cys]
    c = [os_.get(x, 0.0) for x in cys]
    return {"conflict_country_years_2015_2024": len(cys),
            "battle_deaths_per_conflict_year": {"mean": round(statistics.fmean(b)), "median": round(statistics.median(b))},
            "civilians_killed_one_sided_per_conflict_year": {"mean": round(statistics.fmean(c)), "median": round(statistics.median(c))},
            "one_sided_outside_conflict_years_share": round(sum(v for x, v in os_.items() if x not in set(cys)) / max(1, sum(os_.values())), 3)}


def leakage(q):
    pts = [(0.3, 0.26), (0.5, 0.10), (0.7, 0.05)]
    if q <= pts[0][0]:
        return pts[0][1]
    if q >= pts[-1][0]:
        return pts[-1][1]
    for (a, la), (b, lb) in zip(pts, pts[1:]):
        if a <= q <= b:
            return la + (lb - la) * (q - a) / (b - a)


class World:
    """Data shared by all runs."""

    def __init__(self):
        self.ctx = V89.context()
        gov0, st0 = self.ctx["gov"], self.ctx["status"]
        base = V89.core(self.ctx, DELIVERY, lambda k, t: gov0.get(k, 1.0),
                        lambda k, t: (1 - AFFECTED) if st0.get(k) == "conflict" else 1.0, keep_country=True)
        self.keys = sorted(base["per_country"]["L1"])
        self.today = V90.today_index(self.keys)
        self.ls0 = V90.ls_from(base, self.today)
        _, Q, _, _ = panel.indices()
        q = [Q[k][2024] for k in self.keys if 2024 in Q.get(k, {})]
        fill = statistics.median(q)
        self.q0 = {k: Q.get(k, {}).get(2024, fill) for k in self.keys}
        cy = panel.conflict_years()
        self.start = {k for k in self.keys if 2024 in cy.get(k, set())}
        # last conflict year before 2024, in model years (2024 = year 0); -999 if none since 1946
        self.last0 = {k: max([y - 2024 for y in cy.get(k, set()) if y < 2024], default=-999) for k in self.keys}
        self.pop = {k: self.ctx["cty"][k]["pop"] for k in self.keys}
        self.aff = {k: min(AFFECTED, ZONE_PEOPLE / self.pop[k]) for k in self.keys}
        self.frag = set(self.ctx["fcs"]["institutional_social_fragility"]) | set(self.ctx["fcs"]["conflict"])
        self.q_target = statistics.median(v for k, v in self.q0.items() if k not in self.frag)
        self.panel = panel.main()
        c = self.panel["onset"]["LS_and_Q"]["coefficients"]
        self.bE, self.bQ, self.bR = c["e"]["estimate"], c["q"]["estimate"], c["recent"]["estimate"]
        self.e0 = self.panel["sample"]["ending_rate_per_conflict_year"]
        self.pace = self.panel["pace_of_institutional_change"]["ten_year_change_percentiles"]
        self.harm = harm()
        self.a = None

    def calibrate(self, seeds=24):
        """Intercept a such that scenario A keeps, on average over 80 years, today's number of countries in conflict."""
        target = len(self.start)
        p = SCEN["A_baseline"]
        lo, hi = -8.0, 0.0
        for _ in range(18):
            self.a = (lo + hi) / 2
            tot = 0.0
            for s in range(seeds):
                path, *_ = simulate(self, p, self.ls0, {k: [self.q0[k]] * (YEARS + 1) for k in self.keys}, random.Random(10_000 + s))
                tot += sum(sum(v) for v in path.values()) / (YEARS + 1)
            lo, hi = (self.a, hi) if tot / seeds < target else (lo, self.a)
        self.a = round((lo + hi) / 2, 4)
        return self.a


def onset_p(w, p, k, ls, qp, t, recent, tense):
    lsx = w.ls0[k][0] + p["cE"] * (ls[k][t] - w.ls0[k][0])
    qx = w.q0[k] + p["cQ"] * (qp[k][t] - w.q0[k])
    # relapse: power sharing, justice and peace operations lower it; mediated settlements relapse more (Beardsley 2011)
    z = w.a + w.bE * lsx + w.bQ * qx + (w.bR + math.log((1 - p["relapse_cut"]) * (1 + p["mediation_relapse"])) if recent else 0.0)
    h = 1 / (1 + math.exp(-z))
    h *= (1 - p["mediation"] * min(1.0, t / 10)) * (1 - p["cooperation"] * min(1.0, t / 20))
    if tense:
        h *= 1 + p["tension"]
    return min(0.95, h)


def q_paths(w, p, rng, conflict=None):
    """Institutional paths: gains at the scenario's historical pace up to the ceiling, none during conflict years,
    and, each decade, a chance that the decade's gains are reversed."""
    gain = 0.0 if not p["pace"] else w.pace[p["pace"]] / 10
    out = {}
    for k in w.keys:
        q, path, dec_start = w.q0[k], [w.q0[k]], w.q0[k]
        for t in range(1, YEARS + 1):
            if not (conflict and conflict[k][t - 1]):
                q = min(TOP_Q, q + gain) if q < TOP_Q else q
            if gain and t % 10 == 0:
                if rng.random() < p["reversal"]:
                    q = dec_start
                dec_start = q
            path.append(q)
        out[k] = path
    return out


def simulate(w, p, ls, qp, rng):
    state = {k: k in w.start for k in w.keys}
    last = dict(w.last0)
    path = {k: [] for k in w.keys}
    onsets = ends = 0
    for t in range(YEARS + 1):
        for k in w.keys:
            path[k].append(state[k])
            if t == YEARS:
                continue
            if state[k]:
                if rng.random() < min(0.95, w.e0 * (1 + p["end_boost"] * min(1.0, t / 10))):
                    state[k] = False
                    ends += 1
                last[k] = t
            else:
                recent = t - last[k] <= RECUR_YEARS
                tense = qp[k][t] < WEAK_Q and t > 0 and (qp[k][t] - qp[k][max(0, t - 10)]) > w.pace["p75"]
                if rng.random() < onset_p(w, p, k, ls, qp, t, recent, tense):
                    state[k] = True
                    onsets += 1
    return path, onsets, ends


def run(w, p, seed):
    rng_q = random.Random(seed * 7919 + 1)
    qp = q_paths(w, p, rng_q)
    ls = w.ls0
    for _ in range(ITER):
        cpath, onsets, ends = simulate(w, p, ls, qp, random.Random(seed))
        qp = q_paths(w, p, random.Random(seed * 7919 + 1), cpath)  # no reform progress during conflict
        inc = lambda k, t, c=cpath: k in c and c[k][t]

        def govf(k, t, inc=inc, qp=qp):
            if inc(k, t):
                return 1 - 0.5 * w.aff[k] / AFFECTED
            if k in w.frag and k in qp:
                prog = (qp[k][t] - w.q0[k]) / max(1e-9, w.q_target - w.q0[k]) if w.q_target > w.q0[k] else 1.0
                return 0.75 + 0.25 * max(0.0, min(1.0, prog))
            return 1.0
        capfn = lambda k, t, inc=inc: (1 - w.aff[k]) if inc(k, t) else 1.0
        res = V89.core(w.ctx, DELIVERY, govf, capfn, conflict_status=inc, keep_country=True)
        ls = V90.ls_from(res, w.today)
    return cpath, onsets, ends, res, qp


def summarise(vals):
    return V90.summarise(vals)


def run_scenario(w, p, runs, detail=True):
    W = sum(w.pop.values())
    cy, ons, ends_l, d1, d2, cnt, zone, qbar, leak = [], [], [], [], [], [], [], [], []
    late = {k: 0.0 for k in w.keys}
    for seed in range(runs):
        cpath, onsets, ends, res, qp = run(w, p, seed)
        counts = [sum(cpath[k][t] for k in w.keys) for t in range(YEARS + 1)]
        cnt.append(counts)
        cy.append(sum(counts))
        ons.append(onsets)
        ends_l.append(ends)
        zone.append([sum(w.pop[k] * w.aff[k] for k in w.keys if cpath[k][t]) / W for t in range(YEARS + 1)])
        qbar.append([sum(w.pop[k] * qp[k][t] for k in w.keys) / W for t in range(YEARS + 1)])
        leak.append([sum(w.pop[k] * leakage(qp[k][t]) for k in w.keys) / W for t in range(YEARS + 1)])
        d1.append(V90.dates_from(res["cov"]["L1"]))
        d2.append(V90.dates_from(res["cov"]["L2"]))
        for k in w.keys:
            late[k] += sum(cpath[k][40:]) / (YEARS - 39) / runs
    mean = lambda rows, t: statistics.fmean(r[t] for r in rows)
    h = w.harm
    tot = statistics.fmean(cy)
    out = {"conflict_country_years_80y": round(tot, 1),
           "conflict_country_years_p10_p90": [summarise(cy)[x] for x in ("p10", "p90")],
           "L1_dates": {q: summarise([d[q] for d in d1]) for q in QS},
           "L2_dates": {q: summarise([d[q] for d in d2]) for q in QS}}
    if detail:
        out |= {
            "countries_in_conflict": {f"year_{t}": round(mean(cnt, t), 1) for t in (0, 5, 10, 20, 30, 40, 60, 80)},
            "onsets_80y": round(statistics.fmean(ons), 1), "endings_80y": round(statistics.fmean(ends_l), 1),
            "civilian_harm_80y": {
                "battle_deaths_mean_based_m": round(tot * h["battle_deaths_per_conflict_year"]["mean"] / 1e6, 2),
                "battle_deaths_median_based_m": round(tot * h["battle_deaths_per_conflict_year"]["median"] / 1e6, 2),
                "civilians_killed_one_sided_mean_based_m": round(tot * h["civilians_killed_one_sided_per_conflict_year"]["mean"] / 1e6, 2)},
            "share_of_humanity_in_conflict_zones": {f"year_{t}": round(mean(zone, t), 4) for t in (0, 10, 20, 40, 80)},
            "institutional_quality_population_weighted": {f"year_{t}": round(mean(qbar, t), 3) for t in (0, 10, 20, 40, 80)},
            "corruption_loss_share_population_weighted": {f"year_{t}": round(mean(leak, t), 3) for t in (0, 10, 20, 40, 80)},
            "highest_remaining_conflict_risk_years_40_80": [
                {"iso": k, "name": w.ctx["cty"][k].get("name", k), "share_of_years_in_conflict": round(v, 2), "Q_2024": round(w.q0[k], 2)}
                for k, v in sorted(late.items(), key=lambda x: (-x[1], x[0]))[:12]]}
    return out


def costs(w):
    """Workers needed for the institutions of reform, per 100,000 people (ASSUMPTION ranges anchored in evidence.csv),
    for the population of countries below the reform ceiling."""
    below = sum(w.pop[k] for k in w.keys if w.q0[k] < TOP_Q)
    per100k = {"judges": (10, 22),                          # CEPEJ 2024: European average 22 per 100,000
               "court_and_legal_aid_staff": (20, 66),       # ASSUMPTION: 2-3 staff per judge
               "civilian_mediators_and_early_warning": (1.2, 10),  # Ghana Peace Council needs ~400 staff for 34 m (1.2)
               "auditors_and_grievance_officers": (5, 15)}  # ASSUMPTION
    workers = {k: [round(below / 1e5 * v / 1e6, 2) for v in r] for k, r in per100k.items()}
    lo, hi = sum(v[0] for v in workers.values()), sum(v[1] for v in workers.values())
    return {"population_below_reform_ceiling_bn": round(below / 1e9, 2), "per_100k_assumed": per100k, "workers_m": workers,
            "total_workers_m": [round(lo, 1), round(hi, 1)],
            "share_of_world_labour_force": [round(lo * 1e6 / 3.6e9, 4), round(hi * 1e6 / 3.6e9, 4)]}


def fmt(d):
    return V90.fmt(d)


def main(runs=RUNS, sens_runs=SENS_RUNS, write=True, sens=True, world=None):
    w = world or World()
    if w.a is None:
        w.calibrate()
    out = {"panel_coefficients_used": {"bE": w.bE, "bQ": w.bQ, "bR": w.bR, "ending_rate": w.e0, "calibrated_intercept": w.a},
           "countries": len(w.keys), "countries_in_conflict_2024_ucdp": len(w.start), "reform_ceiling_Q": TOP_Q,
           "median_Q_non_fragile": round(w.q_target, 3), "historical_pace_10y": w.pace, "civilian_harm_rates_2015_2024": w.harm,
           "implementation_workers": costs(w), "runs": runs, "scenarios": {}, "factorial_economics_off": {}, "uncertainty_cQ": {}, "sensitivity": {}}
    print(f"intercept {w.a}; 2024 conflicts {len(w.start)}; harm {w.harm}")
    a_cy = None
    for name, p in SCEN.items():
        s = run_scenario(w, p, runs) | {"params": p}
        a_cy = a_cy or s["conflict_country_years_80y"]
        s["share_of_conflict_years_avoided_vs_A"] = round(1 - s["conflict_country_years_80y"] / a_cy, 3)
        out["scenarios"][name] = s
        c = s["countries_in_conflict"]
        print(f"\n== {name}: conflicts yr 0/10/20/40/80 {c['year_0']}/{c['year_10']}/{c['year_20']}/{c['year_40']}/{c['year_80']} | "
              f"avoided vs A {100 * s['share_of_conflict_years_avoided_vs_A']:.0f}% | Q {s['institutional_quality_population_weighted']} | "
              f"harm {s['civilian_harm_80y']}")
        for L in ("L1", "L2"):
            print(f"   {L}: " + " | ".join(f"{q}: {fmt(s[f'{L}_dates'][q])}" for q in QS))
        print("   remaining:", ", ".join(f"{r['iso']} {r['share_of_years_in_conflict']}" for r in s["highest_remaining_conflict_risk_years_40_80"][:8]))
    # separating economics from institutions: the same scenarios with the living-standard channel switched off
    for name, p in SCEN.items():
        r = run_scenario(w, p | {"cE": 0.0}, max(4, runs // 2), detail=False)
        out["factorial_economics_off"][name] = r
    a_off = out["factorial_economics_off"]["A_baseline"]["conflict_country_years_80y"]
    for name in SCEN:
        f = out["factorial_economics_off"][name]
        f["share_avoided_vs_A_economics_off"] = round(1 - f["conflict_country_years_80y"] / a_off, 3)
        print(f"economics off, {name}: conflict-years {f['conflict_country_years_80y']} (avoided vs A {100 * f['share_avoided_vs_A_economics_off']:.0f}%)")
    for cq in (0.25, 1.0):
        for name, p in SCEN.items():
            if name == "A_baseline":
                continue
            r = run_scenario(w, p | {"cQ": cq}, max(4, runs // 2), detail=False)
            out["uncertainty_cQ"][f"{name}/cQ_{cq}"] = r | {"share_avoided_vs_A": round(1 - r["conflict_country_years_80y"] / a_cy, 3)}
            print(f"cQ {cq}, {name}: avoided vs A {100 * (1 - r['conflict_country_years_80y'] / a_cy):.0f}%, "
                  f"L2 95% {r['L2_dates']['95pct']['median']}")
    if sens:
        pb = SCEN[SENS_BASE]
        ref = run_scenario(w, pb, sens_runs, detail=False)
        out["sensitivity"]["base_" + SENS_BASE] = ref
        print(f"\nsensitivity around {SENS_BASE} ({sens_runs} runs): conflict-years, L1 99%, L2 95%")
        for name, ch in SENS.items():
            r = run_scenario(w, pb | ch, sens_runs, detail=False)
            out["sensitivity"][name] = r
            print(f"   {name:22s} {r['conflict_country_years_80y']:7.1f}  {r['L1_dates']['99pct']['median']}  {r['L2_dates']['95pct']['median']}")
        print(f"   {'(base)':22s} {ref['conflict_country_years_80y']:7.1f}  {ref['L1_dates']['99pct']['median']}  {ref['L2_dates']['95pct']['median']}")
    if write:
        (HERE.parent / "outputs").mkdir(exist_ok=True)
        (HERE.parent / "outputs" / "institutions.json").write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main()
