"""UNIRA V6.2 labour reserve: can people who do not work today fill the hours
a 30-hour week removes?

For each country (EU27 + IS/NO/CH), base year y, persons aged 20-64:

    gap      hours lost under the 30h cap, TOTAL economy, computed with the
             same constant-absence method as the France sector model
    T1       unemployed                                   -> enter at 30 h/week
    T2       extended labour force (seeking-not-available
             + available-not-seeking)                     -> enter at 30 h/week
    T3       underemployed part-timers (already employed) -> raised to 30 h/week
    BENCH    employment-rate convergence to a benchmark   -> enter at 30 h/week

T1, T2 and BENCH are persons who are not employed today; BENCH already contains
them, so the two framings are ALTERNATIVES and never summed:
    slack framing      = T1 + T2 (+ T3 hours)
    benchmark framing  = max(BENCH, T1 + T2) (+ T3 hours)

The cap and the entrants' weekly hours are the same parameter (30 = UNIRA
rule; 35 = France's legal reference week, tested as an alternative).

Every mobilisation share here is an UPPER bound on what is achievable: it assumes
every person in the pool takes a 30 h job, in the right place, sector and skill,
at incumbent hourly productivity unless `entrant_relative_productivity` < 1.
"""
from . import jsonstat, model

EXCLUDED_FROM_BENCHMARK = {"EU27_2020"}


class CountryData:
    """Lookups over the eu_* snapshots, keyed by (geo, year, ...)."""

    def __init__(self, raw):
        self.na, self.lfs_u, self.slack, self.emp, self.pt_reason, self.inact = ({} for _ in range(6))
        self.flags = {}
        for c, v, f in jsonstat.iter_cells(raw["eu_na_hours_total"][0]):
            self.na[(c["geo"], int(c["time"]), c["na_item"], c["unit"])] = v
        for c, v, f in jsonstat.iter_cells(raw["eu_lfs_usual_hours_total"][0]):
            self.lfs_u[(c["geo"], int(c["time"]), c["wstatus"], c["worktime"])] = v
            self.flags[("lfs_u", c["geo"], int(c["time"]), c["wstatus"], c["worktime"])] = f
        for c, v, f in jsonstat.iter_cells(raw["eu_lfs_slack"][0]):
            self.slack[(c["geo"], int(c["time"]), c["age"], c["wstatus"])] = v
        for c, v, f in jsonstat.iter_cells(raw["eu_lfs_employment"][0]):
            self.emp[(c["geo"], int(c["time"]), c["age"], c["unit"])] = v
        for c, v, f in jsonstat.iter_cells(raw["eu_lfs_parttime_reason"][0]):
            self.pt_reason[(c["geo"], int(c["time"]), c["reason"])] = v
        for c, v, f in jsonstat.iter_cells(raw["eu_lfs_inactive_reason"][0]):
            self.inact[(c["geo"], int(c["time"]), c["reason"])] = v

    def geos(self):
        return sorted({k[0] for k in self.emp})

    def single_country_tables(self, geo):
        """Adapter exposing one country's TOTAL economy in model.Tables shape."""
        t = type("T", (), {})()
        t.na_emp = {(y, "TOTAL", item, unit): v for (g, y, item, unit), v in self.na.items() if g == geo}
        t.lfs_u = {(y, "TOTAL", w, wt): v for (g, y, w, wt), v in self.lfs_u.items() if g == geo}
        t.na_out = {}
        return t


def population(cd, geo, year, age):
    e, rate = cd.emp.get((geo, year, age, "THS_PER")), cd.emp.get((geo, year, age, "PC_POP"))
    return e / (rate / 100) if e and rate else None


def benchmark_rate(cd, year, age, method):
    rates = {g: cd.emp.get((g, year, age, "PC_POP")) for g in cd.geos()
             if g not in EXCLUDED_FROM_BENCHMARK}
    rates = {g: r for g, r in rates.items() if r is not None}
    if method.startswith("top") and method.endswith("_mean"):
        n = int(method[3:-5])
        top = sorted(rates.values(), reverse=True)[:n]
        return sum(top) / len(top), sorted(rates, key=rates.get, reverse=True)[:n]
    return rates[method], [method]


def hours_gap(cd, geo, year, apply_to, cap=30):
    t = cd.single_country_tables(geo)
    cfg = {"sectors": ["TOTAL"], "trend_windows": [],
           "nonmarket_output_sectors": {"sectors": []}, "imputed_output_sectors": {"sectors": []}}
    scen = {"id": "gap", "cap": cap, "apply_to": apply_to, "annual_method": "constant_absence"}
    row = model.sector_rows(t, year, scen, cfg)[0]
    return row


def evaluate(cd, geo, year, params):
    """Return one result row for a country-year; None if core data are missing."""
    cap = params["entrant_weekly_hours"]
    rho = params["entrant_relative_productivity"]
    age = params["age_band"]
    try:
        row = hours_gap(cd, geo, year, params["apply_to"], cap)
    except (ValueError, TypeError):
        return None
    H0, H1 = row["hours_before_ths"], row["hours_after_ths"]
    weeks = row["SAL_implied_effective_weeks"]
    pop = population(cd, geo, year, age)
    s = {w: cd.slack.get((geo, year, age, w)) for w in ("UNE", "SEEK_NAVL", "NSEEK_AVL", "UEMP_PT")}
    if not (H0 and weeks and pop) or s["UNE"] is None:
        return None
    entrant_hours = cap * weeks  # hours/person/yr, thousand persons -> thousand hours
    u_pt = cd.lfs_u.get((geo, year, "SAL", "PT"))
    t1 = s["UNE"]
    t2 = (s["SEEK_NAVL"] or 0) + (s["NSEEK_AVL"] or 0)
    t3_hours = (s["UEMP_PT"] or 0) * max(0.0, cap - u_pt) * weeks if u_pt else 0.0
    own = cd.emp.get((geo, year, age, "PC_POP"))
    out = {"geo": geo, "year": year, "weekly_cap": cap, "apply_to": "+".join(params["apply_to"]),
           "hours_before_ths": H0, "hours_after_ths": H1, "hours_gap_ths": H0 - H1,
           "required_gain_no_mobilisation": H0 / H1 - 1,
           "employee_effective_weeks": weeks, "entrant_annual_hours": entrant_hours,
           "population_ths": pop, "employment_rate": own,
           "employment_rate_55_64": cd.emp.get((geo, year, "Y55-64", "PC_POP")),
           "lfs_usual_hours_all": cd.lfs_u.get((geo, year, "EMP", "TOTAL")),
           "t1_unemployed_ths": t1, "t2_extended_lf_ths": t2,
           "t3_underemployed_pt_ths": s["UEMP_PT"], "t3_extra_hours_ths": t3_hours,
           "pt_involuntary_share_pct": cd.pt_reason.get((geo, year, "NF_FTJOB")),
           "inactive_care_reason_pct_pop": cd.inact.get((geo, year, "FAM_CARE")),
           "inactive_illness_reason_pct_pop": cd.inact.get((geo, year, "ILL_DIS_OWN"))}
    for name, method in params["benchmarks"].items():
        rate, who = benchmark_rate(cd, year, age, method)
        bench = max(0.0, (rate - own) / 100 * pop)
        out[f"bench_{name}_rate"] = rate
        out[f"bench_{name}_countries"] = "+".join(who)
        out[f"bench_{name}_employment_gap_persons_ths"] = bench
    gap = H0 - H1
    framings = {"slack": t1 + t2}
    framings.update({f"bench_{n}": max(out[f"bench_{n}_employment_gap_persons_ths"], t1 + t2)
                     for n in params["benchmarks"]})
    for name, persons in framings.items():
        supplied = (persons * entrant_hours + t3_hours) * rho
        out[f"{name}_persons_ths"] = persons
        out[f"{name}_hours_supplied_ths"] = supplied
        out[f"{name}_gap_closed_share"] = supplied / gap if gap > 0 else None
        out[f"{name}_residual_gain"] = H0 / min(H0, H1 + supplied) - 1
    return out


def run(cd, cfg):
    """All countries x years x cap variants x entrant-productivity values."""
    rows = []
    lo, hi = cfg["weeks_plausible"]
    for y in cfg["years"]:
        for g in cd.geos():
            for apply_to, cap, rho in ((a, c, r) for a in cfg["apply_to_variants"]
                                       for c in cfg["weekly_caps"]
                                       for r in cfg["entrant_relative_productivity"]["values"]):
                params = {"apply_to": apply_to, "age_band": cfg["age_band"],
                          "entrant_weekly_hours": cap,
                          "entrant_relative_productivity": rho, "benchmarks": cfg["benchmarks"]}
                r = evaluate(cd, g, y, params)
                if r:
                    r["entrant_relative_productivity"] = rho
                    w = r["employee_effective_weeks"]
                    r["weeks_flag"] = "" if lo <= w <= hi else "NA_LFS_weeks_implausible"
                    rows.append(r)
    return rows
