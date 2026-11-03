"""UNIRA V6.2 — France sector labour hours under a 30-hour weekly cap.

Accounting arithmetic, NOT a forecast. For each NACE section s and worker
group g (employees SAL, self-employed incl. family workers SELF):

    H[s,g]   national-accounts hours worked, all persons (nama_10_a64_e)
    N[s,g]   national-accounts persons employed
    uT,uF,uP LFS mean usual weekly hours: all / full-time / part-time (lfsa_ewhun2)
    q        part-time share implied by the means:  uT = q*uP + (1-q)*uF

Weekly cap c. Group-mean retained weekly hours:  R = q*min(uP,c) + (1-q)*min(uF,c).
By concavity of min(., c), mean(min(x,c)) <= min(mean(x),c), so R is an UPPER
bound on true retained hours. This makes the reduction a lower bound ONLY with
respect to hours dispersion within the FT and PT groups. Other simplifications
push the other way (full compliance with the cap is assumed; RTT absences are
kept; second-job hours are scaled by the main-job ratio), so the net direction
of bias of the headline figure is unknown (audit/v62_code_review.md).

Annual methods:
  constant_absence  H' = H * R / uT   (effective weeks per person unchanged;
                    level-invariant: only weekly ratios matter)
  constant_absence with extra_weeks_ft = d
                    full-timers additionally work d more weeks (e.g. RTT days that
                    compensate hours above 35h would no longer be granted);
                    SYNTHETIC sensitivity, not observed
  normative_weeks   full-time annual hours capped at c*W (V6.1 convention, W=46).
                    NOT a 30h cap: with ~38.7 observed effective weeks, 30*46 h/yr
                    allows ~35.7 h per week actually worked. It depends on absolute
                    NA hour levels and is neither a lower nor an upper bound.

Productivity requirement at fixed output and fixed persons: H/H' - 1.
"""
import math

GROUPS = {"SAL": ("SAL_DC", "SAL"), "SELF": ("SELF_DC", "NSAL")}


def split_parttime(u_tot, u_ft, u_pt):
    """Part-time share q solving u_tot = q*u_pt + (1-q)*u_ft, clipped to [0,1]."""
    if None in (u_tot, u_ft, u_pt) or u_ft <= u_pt:
        raise ValueError("need u_ft > u_pt and all means present")
    return min(1.0, max(0.0, (u_ft - u_tot) / (u_ft - u_pt)))


def retained_weekly(u_tot, u_ft, u_pt, cap, tail_share=0.0, tail_hours=None):
    """Mean usual weekly hours after the cap (group-mean approximation)."""
    if cap <= 0:
        raise ValueError("cap must be positive")
    q = split_parttime(u_tot, u_ft, u_pt)
    ft = min(u_ft, cap)
    pt = min(u_pt, cap)
    if tail_share and tail_hours and tail_hours > cap and u_pt < cap:
        if not 0 <= tail_share <= 1 or tail_share * tail_hours > u_pt:
            raise ValueError("tail inconsistent with part-time mean")
        pt = u_pt - tail_share * (tail_hours - cap)
    return q * pt + (1 - q) * ft


def lfs_means(tables, year, nace, wstatus, shift=(0.0, 0.0, 0.0)):
    """(uT, uF, uP, source) with documented fallback when LFS cells are missing."""
    for n, w in ((nace, wstatus), (nace, "EMP"), ("TOTAL", wstatus)):
        vals = [tables.lfs_u.get((year, n, w, t)) for t in ("TOTAL", "FT", "PT")]
        if None not in vals and vals[1] > vals[2]:
            vals = [v + d for v, d in zip(vals, shift)]
            src = "direct" if (n, w) == (nace, wstatus) else f"imputed_from_{n}_{w}"
            return vals[0], vals[1], vals[2], src
    return None


def group_hours(H, N, means, scen):
    """Return (H_after, part_time_share, implied_weeks) for one sector-group."""
    if not H or not N:
        return 0.0, None, None
    u_tot, u_ft, u_pt, _ = means
    q = split_parttime(u_tot, u_ft, u_pt)
    weeks = H / N / u_tot  # thousand hours / thousand persons = hours per person
    cap = scen.get("cap")
    if cap is None:
        return H, q, weeks
    if scen["annual_method"] == "constant_absence":
        r = retained_weekly(u_tot, u_ft, u_pt, cap,
                            scen.get("pt_above_cap_share", 0.0), scen.get("pt_above_cap_hours"))
        extra = scen.get("extra_weeks_ft", 0.0) if scen.get("group") == "SAL" else 0.0
        return H * r / u_tot + N * (1 - q) * extra * min(u_ft, cap), q, weeks
    if scen["annual_method"] == "normative_weeks":
        cap_annual = cap * scen["weeks"]
        a_ft, a_pt = weeks * u_ft, weeks * u_pt
        return N * ((1 - q) * min(a_ft, cap_annual) + q * min(a_pt, cap_annual)), q, weeks
    raise ValueError(f"unknown annual_method {scen['annual_method']}")


WEEKS_PLAUSIBLE = (28.0, 50.0)


def weeks_flag(weeks):
    """Flag NA/LFS combinations whose implied effective weeks are implausible."""
    if weeks is None:
        return ""
    lo, hi = WEEKS_PLAUSIBLE
    return "" if lo <= weeks <= hi else "NA_LFS_inconsistent"


def cagr(start, end, years):
    if not start or not end or years <= 0:
        return None
    return (end / start) ** (1 / years) - 1


def real_va_per_hour(tables, year, nace):
    va = tables.na_out.get((year, nace, "B1G", "CLV20_MEUR"))
    h = tables.na_emp.get((year, nace, "EMP_DC", "THS_HW"))
    return va * 1e6 / (h * 1e3) if va and h else None


def years_to_cover(gain, trend):
    """Years of historical trend hourly-productivity growth needed to absorb `gain`."""
    if gain is None or trend is None:
        return None
    if gain <= 0:
        return 0.0
    if trend <= 0:
        return math.inf
    return math.log1p(gain) / math.log1p(trend)


def sector_rows(tables, year, scen, cfg, shift=(0.0, 0.0, 0.0)):
    rows = []
    for s in cfg["sectors"]:
        row = {"year": year, "scenario": scen["id"], "nace_r2": s}
        H0 = H1 = N0 = add_persons = 0.0
        sources = []
        for g, (na_item, wstatus) in GROUPS.items():
            H = tables.na_emp.get((year, s, na_item, "THS_HW")) or 0.0
            N = tables.na_emp.get((year, s, na_item, "THS_PER")) or 0.0
            if bool(H) != bool(N):
                raise ValueError(f"{year} {s} {na_item}: hours and persons must both be present "
                                 f"(H={H}, N={N}); refusing to drop hours silently")
            if H and N:
                means = lfs_means(tables, year, s, wstatus, shift)
                if means is None:
                    raise ValueError(f"no LFS hours for {year} {s} {wstatus}")
                applied = scen.get("cap") is not None and g in scen.get("apply_to", [])
                h1, q, weeks = group_hours(H, N, means, dict(scen, group=g) if applied else {"cap": None})
                sources.append(f"{g}:{means[3]}")
                row[f"{g}_part_time_share"] = q
                row[f"{g}_implied_effective_weeks"] = weeks
                row[f"{g}_lfs_usual_weekly_hours"] = means[0]
                if weeks_flag(weeks):
                    sources.append(f"{g}:{weeks_flag(weeks)}")
            else:
                h1 = 0.0
                row[f"{g}_part_time_share"] = row[f"{g}_implied_effective_weeks"] = None
                row[f"{g}_lfs_usual_weekly_hours"] = None
            row[f"{g}_hours_before_ths"] = H
            row[f"{g}_hours_after_ths"] = h1
            row[f"{g}_persons_ths"] = N
            H0, H1, N0 = H0 + H, H1 + h1, N0 + N
            if h1:
                add_persons += N * (H / h1 - 1)
        row.update(_derived(tables, year, s, H0, H1, N0, add_persons, cfg))
        row["lfs_source"] = ";".join(sources)
        rows.append(row)
    return rows


def _derived(tables, year, s, H0, H1, N0, add_persons, cfg):
    va_cp = tables.na_out.get((year, s, "B1G", "CP_MEUR"))
    retention = H1 / H0 if H0 else None
    gain = (H0 / H1 - 1) if H1 else None
    out = {"hours_before_ths": H0, "hours_after_ths": H1, "persons_ths": N0,
           "hours_per_person_before": H0 / N0 if N0 else None,
           "hours_retention_ratio": retention,
           "required_hourly_productivity_gain": gain,
           "additional_persons_same_profile_ths": add_persons,
           "va_current_prices_meur": va_cp,
           "va_at_risk_fixed_productivity_meur": va_cp * (1 - retention) if va_cp and retention is not None else None,
           "real_va_per_hour_eur2020": real_va_per_hour(tables, year, s),
           "breakeven_avoidable_output_share": (1 - retention) if retention is not None else None}
    for a, b in cfg["trend_windows"]:
        tr = cagr(real_va_per_hour(tables, a, s), real_va_per_hour(tables, b, s), b - a)
        out[f"trend_va_per_hour_{a}_{b}"] = tr
        out[f"years_of_trend_{a}_{b}_to_cover_gain"] = years_to_cover(gain, tr)
    out["output_measure_caveat"] = (
        "nonmarket_input_based" if s in cfg["nonmarket_output_sectors"]["sectors"] else
        "imputed_output" if s in cfg["imputed_output_sectors"]["sectors"] else "")
    return out


def total_row(rows, tables, year, scen, cfg):
    H0 = sum(r["hours_before_ths"] for r in rows)
    H1 = sum(r["hours_after_ths"] for r in rows)
    N0 = sum(r["persons_ths"] for r in rows)
    add = sum(r["additional_persons_same_profile_ths"] for r in rows)
    row = {"year": year, "scenario": scen["id"], "nace_r2": "TOTAL_bottom_up"}
    row.update(_derived(tables, year, "TOTAL", H0, H1, N0, add, cfg))
    row["va_at_risk_fixed_productivity_meur"] = sum(r["va_at_risk_fixed_productivity_meur"] or 0 for r in rows)
    row["output_measure_caveat"] = "economy-wide trend includes non-market and imputed output"
    return row


def run_scenario(tables, year, scen, cfg, shift=(0.0, 0.0, 0.0)):
    rows = sector_rows(tables, year, scen, cfg, shift)
    return rows + [total_row(rows, tables, year, scen, cfg)]


def residual_gain_with_offset(hours_before, hours_after, theta):
    """Remaining hourly-productivity requirement if a fraction `theta` of lost hours
    is compensated by a behavioural hours->productivity response (0 none, 1 full).
    theta is NOT estimated here; see audit/hours_productivity_evidence.md."""
    if not 0 <= theta <= 1:
        raise ValueError("theta must be in [0, 1]")
    effective = hours_after + theta * (hours_before - hours_after)
    return hours_before / effective - 1


def rounding_bounds(tables, year, scen, cfg, half_step=0.05):
    """Bounds on total hours after the cap from LFS publication rounding (+-0.05 h)."""
    totals = []
    for a in (-half_step, half_step):
        for b in (-half_step, half_step):
            for c in (-half_step, half_step):
                rows = run_scenario(tables, year, scen, cfg, shift=(a, b, c))
                totals.append(rows[-1]["required_hourly_productivity_gain"])
    return min(totals), max(totals)


def slack(tables, year):
    keys = ["UNE", "UEMP_PT", "SEEK_NAVL", "NSEEK_AVL", "SLACK"]
    return {k: tables.slack.get((year, k)) for k in keys}


# INSEE "Emploi, chomage, revenus du travail" 2026 edition, page 8733071 (LFS 2025,
# France excl. Mayotte), verified in audit/source_verification.csv.
INSEE_LFS_ANNUAL_HOURS_2025 = {"full_time_employees": 1656, "part_time_employees": 966,
                               "self_employed": 1903}


def insee_reconciliation(tables, year):
    """Compare annual hours per person implied by NA hours x LFS weekly ratios
    with INSEE's LFS-based annual hours (published for 2025 only)."""
    H = tables.na_emp.get((year, "TOTAL", "SAL_DC", "THS_HW"))
    N = tables.na_emp.get((year, "TOTAL", "SAL_DC", "THS_PER"))
    Hs = tables.na_emp.get((year, "TOTAL", "SELF_DC", "THS_HW"))
    Ns = tables.na_emp.get((year, "TOTAL", "SELF_DC", "THS_PER"))
    m = lfs_means(tables, year, "TOTAL", "SAL")
    if not (H and N and m):
        return None
    out = {"year": year, "na_hours_per_employee": H / N, "lfs_usual_ft": m[1],
           "lfs_usual_pt": m[2], "lfs_usual_all_employees": m[0],
           "implied_ft_employee_annual_hours": H / N * m[1] / m[0],
           "implied_pt_employee_annual_hours": H / N * m[2] / m[0],
           "implied_employee_effective_weeks": H / N / m[0],
           "na_hours_per_self_employed": Hs / Ns if Hs and Ns else None}
    if year == 2025:
        ref = INSEE_LFS_ANNUAL_HOURS_2025
        out["insee_ft_employee_annual_hours"] = ref["full_time_employees"]
        out["insee_pt_employee_annual_hours"] = ref["part_time_employees"]
        out["insee_self_employed_annual_hours"] = ref["self_employed"]
        out["ratio_implied_to_insee_ft"] = out["implied_ft_employee_annual_hours"] / ref["full_time_employees"]
        out["ratio_implied_to_insee_pt"] = out["implied_pt_employee_annual_hours"] / ref["part_time_employees"]
        out["ratio_na_to_insee_self_employed"] = out["na_hours_per_self_employed"] / ref["self_employed"]
        out["insee_ft_over_pt_ratio"] = ref["full_time_employees"] / ref["part_time_employees"]
        out["lfs_weekly_ft_over_pt_ratio"] = m[1] / m[2]
    return out


def evidence_pathway(sector_rows_primary, reserve_row, case, care_sectors):
    """Residual required gain after (1) a sector-specific behavioural offset theta
    on incumbents' lost hours and (2) mobilisation of the labour reserve
    (benchmark framing) at a given take-up and entrant productivity."""
    H0 = sum(r["hours_before_ths"] for r in sector_rows_primary)
    H1 = sum(r["hours_after_ths"] for r in sector_rows_primary)
    offset = sum((case["theta_care"] if r["nace_r2"] in care_sectors else case["theta_market"])
                 * (r["hours_before_ths"] - r["hours_after_ths"]) for r in sector_rows_primary)
    persons = reserve_row["bench_top3_persons_ths"] * case["take_up"]
    supply = (persons * reserve_row["entrant_annual_hours"]
              + reserve_row["t3_extra_hours_ths"] * case["take_up"]) * case["entrant_relative_productivity"]
    effective = min(H0, H1 + offset + supply)
    return {"hours_gap_ths": H0 - H1, "theta_offset_hours_ths": offset, "mobilised_persons_ths": persons,
            "mobilised_hours_ths": supply, "share_closed_by_theta": offset / (H0 - H1),
            "share_closed_by_mobilisation": supply / (H0 - H1),
            "residual_required_gain": H0 / effective - 1}
