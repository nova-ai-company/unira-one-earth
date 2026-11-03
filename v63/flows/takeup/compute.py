"""Compute year-1 take-up rates per V6.2 reserve pool from the frozen snapshots.

Rows produced (one per geo x year x pool x method); `role` says how to use them:
  proposed      the value to feed into the V6.2 mobilisation parameter
  lower_bound   a defensible floor for the pool
  alternative   a second model-derived estimate (sensitivity)
  cross_check   independent estimate shown for validation only
  benchmark     best-observed (top-3 country mean) upper bound for an active policy
"""
import json
from pathlib import Path

from ._v62 import fetch, jsonstat
from . import markov, queries

COLUMNS = ["geo", "year", "pool", "takeup_rate", "method", "source_dataset",
           "evidence_class", "notes", "role"]
AGGREGATES = {"EU27_2020"}
CODE = {"UNE": "U", "EMP": "E", "INAC": "I"}
BASELINE_NOTE = ("status-quo baseline incl. normal churn (people who would find work anyway); "
                 "NOT the effect of a mobilisation policy")


def load_raw(raw_dir):
    raw_dir = Path(raw_dir)
    return {stem: jsonstat.load(raw_dir / f"{stem}.json") for stem, _, _ in queries.QUERIES}


class Flows:
    """Lookups over the snapshots."""

    def __init__(self, raw):
        self.annual, self.q_levels, self.e06, self.e01, self.e08, self.silc, self.stock = (
            {} for _ in range(7))
        self.flags = {}
        for c, v, f in jsonstat.iter_cells(raw["flows_annual"]):
            self.annual[(c["geo"], int(c["time"]), c["wstatus"], c["unit"])] = v
            self.flags[("annual", c["geo"], int(c["time"]), c["wstatus"], c["unit"])] = f
        for c, v, f in jsonstat.iter_cells(raw["flows_quarterly"]):
            a, b = c["wstatus"].split("_")
            self.q_levels.setdefault((c["geo"], c["time"]), {})[(CODE[a], CODE[b])] = v
        for c, v, f in jsonstat.iter_cells(raw["flows_inactive_attachment"]):
            self.e06[(c["geo"], int(c["time"]), c["age"], c["wstatus"])] = v
        for c, v, f in jsonstat.iter_cells(raw["flows_unemp_duration"]):
            self.e01[(c["geo"], int(c["time"]), c["age"], c["duration"])] = v
        for c, v, f in jsonstat.iter_cells(raw["flows_pt_to_ft"]):
            self.e08[(c["geo"], int(c["time"]))] = v
        for c, v, f in jsonstat.iter_cells(raw["silc_labour_transitions"]):
            self.silc[(c["geo"], int(c["time"]), c["wstatusp"], c["wstatus"])] = v
            self.flags[("silc", c["geo"], int(c["time"]), c["wstatusp"], c["wstatus"])] = f
        for c, v, f in jsonstat.iter_cells(raw["lfs_slack_stocks"]):
            self.stock[(c["geo"], int(c["time"]), c["wstatus"])] = v

    # --- primitives -----------------------------------------------------------------
    def direct_annual(self, geo, year, transition, unit):
        v = self.annual.get((geo, year, transition, unit))
        return None if v is None else v / 100

    def quarter_matrices(self, geo, year):
        """NSA matrices for the 4 quarterly transitions published under `year`
        ((y-1)Q4->yQ1, ..., yQ3->yQ4). None if any quarter is incomplete."""
        mats = [markov.from_levels(self.q_levels.get((geo, f"{year}-Q{q}"), {}))
                for q in (1, 2, 3, 4)]
        return None if any(m is None for m in mats) else mats

    def markov_annual(self, geo, year, origin):
        mats = self.quarter_matrices(geo, year)
        return None if mats is None else markov.prob(markov.compound(mats), origin, "E")

    def mean_quarterly(self, geo, year, origin):
        mats = self.quarter_matrices(geo, year)
        return None if mats is None else sum(markov.prob(m, origin, "E") for m in mats) / 4

    def t2_quarterly(self, geo, year, age="Y15-74"):
        """Stock-weighted quarterly I->E probability of SEEK_NAVL + NSEEK_AVL (e06)."""
        parts = []
        for w in ("SEEK_NAVL", "NSEEK_AVL"):
            q, n = self.e06.get((geo, year, age, w)), self.stock.get((geo, year, w))
            if q is not None and n:
                parts.append((q / 100, n, w))
        if not parts:
            return None, ""
        tot = sum(n for _, n, _ in parts)
        used = "+".join(w for _, _, w in parts)
        return sum(q * n for q, n, _ in parts) / tot, used


def _row(geo, year, pool, rate, method, src, ev, notes, role):
    return {"geo": geo, "year": year, "pool": pool,
            "takeup_rate": None if rate is None else round(min(1.0, rate), 4),
            "method": method, "source_dataset": src,
            "evidence_class": ev if rate is not None else "MISSING",
            "notes": notes, "role": role}


def country_rows(fl, geo, year):
    rows = []
    # ---------------- T1: unemployed --------------------------------------------------
    t1 = fl.direct_annual(geo, year, "UNE_EMP", "PC_UNE")
    rows.append(_row(geo, year, "T1", t1, "direct_year_on_year_UNE_EMP_PC_UNE", "lfsi_long_a",
                     "VERIFIED_OFFICIAL",
                     f"ILO unemployed 15-74 in {year - 1} employed same quarter of {year}; "
                     f"flag='{fl.flags.get(('annual', geo, year, 'UNE_EMP', 'PC_UNE'), '')}'; "
                     + BASELINE_NOTE if t1 is not None else
                     f"lfsi_long_a has no value for {geo} {year}", "proposed"))
    mk = fl.markov_annual(geo, year, "U")
    rows.append(_row(geo, year, "T1", mk, "markov_4q_compound_NSA_levels", "lfsi_long_q",
                     "MODEL_DERIVED",
                     "product of the 4 quarterly U/E/I matrices published under the year; "
                     "Markov ignores duration dependence -> overstates" +
                     (f"; Markov minus direct = {mk - t1:+.3f}" if mk is not None and t1 is not None else ""),
                     "cross_check"))
    s = fl.silc.get((geo, year, "UNE", "EMP"))
    rows.append(_row(geo, year, "T1", None if s is None else s / 100, "silc_t-1_to_t_UNE_EMP",
                     "ilc_lvhl30", "VERIFIED_OFFICIAL",
                     "EU-SILC self-defined status, year t-1 -> t; different concept from ILO; "
                     f"flag='{fl.flags.get(('silc', geo, year, 'UNE', 'EMP'), '')}'", "cross_check"))

    # ---------------- T2: extended labour force (attached inactive) ------------------
    ie = fl.direct_annual(geo, year, "INAC_EMP", "PC_INAC")
    rows.append(_row(geo, year, "T2", ie, "direct_year_on_year_INAC_EMP_all_inactive", "lfsi_long_a",
                     "VERIFIED_OFFICIAL",
                     "ALL persons outside the labour force 15-74 (students, retirees, carers...); "
                     "LOWER bound for T2, whose members are attached to the labour market",
                     "lower_bound"))
    q2, used = fl.t2_quarterly(geo, year)
    qU, qU_src = fl.mean_quarterly(geo, year, "U"), "lfsi_long_q levels"
    if qU is None and fl.e01.get((geo, year, "Y15-74", "TOTAL")):
        # fallback when a quarterly cell is suppressed: e01 TOTAL (integer-% rounded)
        qU, qU_src = fl.e01[(geo, year, "Y15-74", "TOTAL")] / 100, "lfsi_long_e01 TOTAL (fallback)"
    fU = t1 / qU if (t1 is not None and qU) else None
    central = q2 * fU if (q2 is not None and fU is not None) else None
    rows.append(_row(geo, year, "T2", central, "e06_quarterly_T2_x_country_U_annualisation_factor",
                     "lfsi_long_e06+lfsi_sla_a+lfsi_long_a+lfsi_long_q|e01", "MODEL_DERIVED",
                     (f"q_T2={q2:.3f} (stock-weighted {used}, quarterly, 15-74) x f_U={fU:.3f} "
                      f"(direct annual U->E / mean quarterly U->E from {qU_src}, same country-year); assumes the "
                      "attached inactive share the unemployed's quarter->year profile; "
                      + ("EXCEEDS T1 here (low U annualisation factor / high q_T2); "
                         if (t1 is not None and central > t1) else "")
                      + BASELINE_NOTE) if central is not None else
                     "missing e06, slack stocks, or annual/quarterly U flows", "proposed"))
    tot = fl.e06.get((geo, year, "Y15-74", "TOTAL"))
    alt = ie * (q2 / (tot / 100)) if (ie is not None and q2 is not None and tot) else None
    rows.append(_row(geo, year, "T2", alt, "direct_annual_INAC_EMP_x_e06_relative_risk",
                     "lfsi_long_a+lfsi_long_e06+lfsi_sla_a", "MODEL_DERIVED",
                     (f"annual I->E x (q_T2 / q_TOTAL_inactive = {q2:.3f}/{tot / 100:.3f}); "
                      "assumes the T2/all-inactive relative risk is the same at 1 year as at 1 "
                      "quarter (proportional scaling) -> tends to be HIGHER than the proposed value")
                     if alt is not None else "missing inputs", "alternative"))
    mi = fl.markov_annual(geo, year, "I")
    rows.append(_row(geo, year, "T2", mi, "markov_4q_compound_all_inactive", "lfsi_long_q",
                     "MODEL_DERIVED", "all inactive, Markov 4-quarter compound; context only",
                     "cross_check"))

    # ---------------- T3: underemployed part-timers raising hours ---------------------
    pt = fl.silc.get((geo, year, "EMP_PT", "EMP_FT"))
    rows.append(_row(geo, year, "T3", None if pt is None else pt / 100, "silc_t-1_to_t_EMP_PT_EMP_FT",
                     "ilc_lvhl30", "VERIFIED_OFFICIAL",
                     ("PROXY: ALL part-timers (voluntary included), self-defined FT/PT, year t-1 -> t; "
                      "no official flow for UNDEREMPLOYED part-timers exists; likely a LOWER bound "
                      "for T3 (the underemployed want more hours); "
                      f"flag='{fl.flags.get(('silc', geo, year, 'EMP_PT', 'EMP_FT'), '')}'")
                     if pt is not None else "ilc_lvhl30 has no value", "proposed"))
    return rows


def benchmark_rows(rows, year, pool, method, n=3):
    vals = {r["geo"]: r["takeup_rate"] for r in rows
            if r["year"] == year and r["pool"] == pool and r["method"] == method
            and r["geo"] not in AGGREGATES and r["takeup_rate"] is not None}
    top = sorted(vals, key=vals.get, reverse=True)[:n]
    if len(top) < n:
        return None
    mean = sum(vals[g] for g in top) / n
    src = next(r["source_dataset"] for r in rows if r["method"] == method)
    return _row(f"TOP{n}_MEAN", year, pool, mean, f"top{n}_mean_of:{method}", src, "MODEL_DERIVED",
                f"best observed of {len(vals)} countries: " +
                ", ".join(f"{g}={vals[g]:.3f}" for g in top) +
                "; upper bound for an ACTIVE mobilisation policy, still status-quo flows "
                "shaped by each country's composition and institutions", "benchmark")


def compute(raw_dir):
    fl = Flows(load_raw(raw_dir))
    rows = []
    for year in (int(y) for y in queries.YEARS):
        for geo in queries.GEOS:
            rows += country_rows(fl, geo, year)
    for year in (int(y) for y in queries.YEARS):
        for pool, method in (("T1", "direct_year_on_year_UNE_EMP_PC_UNE"),
                             ("T2", "e06_quarterly_T2_x_country_U_annualisation_factor"),
                             ("T2", "direct_year_on_year_INAC_EMP_all_inactive")):
            # No T3 benchmark on purpose: the all-part-timer SILC proxy is dominated by
            # composition (RO 2023 = 0.935, subsistence part-time), not by policy.
            b = benchmark_rows(rows, year, pool, method)
            if b:
                rows.append(b)
    return fl, rows


def summary(fl, rows):
    def pick(geo, year, pool, role="proposed", method=None):
        for r in rows:
            if (r["geo"], r["year"], r["pool"], r["role"]) == (geo, year, pool, role) and \
                    (method is None or r["method"] == method):
                return r["takeup_rate"]
        return None

    out = {"description": "UNIRA V6.3 empirical year-1 take-up rates for the V6.2 labour-reserve pools",
           "baseline_caveat": BASELINE_NOTE, "years": {}}
    for year in (int(y) for y in queries.YEARS):
        y = {}
        for geo in ("FR", "EU27_2020"):
            y[geo] = {
                "T1_proposed": pick(geo, year, "T1"),
                "T1_markov_cross_check": pick(geo, year, "T1", "cross_check",
                                              "markov_4q_compound_NSA_levels"),
                "T1_silc_cross_check": pick(geo, year, "T1", "cross_check", "silc_t-1_to_t_UNE_EMP"),
                "T2_proposed": pick(geo, year, "T2"),
                "T2_lower_bound_all_inactive": pick(geo, year, "T2", "lower_bound"),
                "T2_alternative_relative_risk": pick(geo, year, "T2", "alternative"),
                "T3_proposed_proxy": pick(geo, year, "T3"),
                "context_quarterly_U_to_E_by_duration_15_74": {
                    d: (None if fl.e01.get((geo, year, "Y15-74", d)) is None
                        else fl.e01[(geo, year, "Y15-74", d)] / 100)
                    for d in ("TOTAL", "Y_LT1", "Y_GE1", "Y_GE2")},
                "context_quarterly_I_to_E_by_attachment_15_74": {
                    w: (None if fl.e06.get((geo, year, "Y15-74", w)) is None
                        else fl.e06[(geo, year, "Y15-74", w)] / 100)
                    for w in ("TOTAL", "SEEK_NAVL", "NSEEK_AVL", "OTH")},
                "context_quarterly_PT_to_FT_25_64_lfsi_long_e08": (
                    None if fl.e08.get((geo, year)) is None else fl.e08[(geo, year)] / 100),
            }
        bench = {}
        for r in rows:
            if r["year"] == year and r["role"] == "benchmark":
                bench[f"{r['pool']}:{r['method']}"] = {"rate": r["takeup_rate"], "notes": r["notes"]}
        y["benchmark_top3"] = bench
        diffs = [r for r in rows if r["year"] == year and r["method"] == "markov_4q_compound_NSA_levels"
                 and r["takeup_rate"] is not None and pick(r["geo"], year, "T1") is not None]
        d = [r["takeup_rate"] - pick(r["geo"], year, "T1") for r in diffs]
        y["markov_minus_direct_T1"] = {"n": len(d), "mean": round(sum(d) / len(d), 4) if d else None,
                                       "n_positive": sum(1 for x in d if x > 0)}
        y["coverage"] = {p: sorted({r["geo"] for r in rows if r["year"] == year and r["pool"] == p
                                    and r["role"] == "proposed" and r["takeup_rate"] is None})
                         for p in ("T1", "T2", "T3")}
        y["coverage"] = {f"{p}_missing": v for p, v in y["coverage"].items()}
        out["years"][str(year)] = y
    return out


def write_outputs(rows, summ, out_dir):
    import csv
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "takeup_rates.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r[k] is None else r[k]) for k in COLUMNS})
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=2, ensure_ascii=False) + "\n")


def verify_snapshots(raw_dir):
    return fetch.verify_manifest(raw_dir)
