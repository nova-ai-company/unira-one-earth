"""UNIRA V6.2 pipeline: frozen raw snapshots -> tidy evidence -> scenarios -> checks.

    python3 run_all.py            # offline, from data/raw (default)
    python3 run_all.py --fetch    # re-download Eurostat snapshots first (changes hashes)
"""
import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from unira_v62 import fetch, labour_reserve, model, report, tidy  # noqa: E402

KNOWN_EMPLOYEE_WEEKS_EXCEPTIONS = {"T"}
RAW, TIDY, OUT = ROOT / "data" / "raw", ROOT / "data" / "tidy", ROOT / "outputs"


def clean(v):
    if isinstance(v, float):
        if math.isinf(v):
            return "inf"
        return round(v, 6)
    return v


def write_csv(path, rows):
    fields = []
    for r in rows:
        fields += [k for k in r if k not in fields]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows({k: clean(v) for k, v in r.items()} for r in rows)


def checks(tables, cfg, results):
    out = []

    def add(name, year, ok, detail):
        out.append({"check": name, "year": year, "passed": ok, "detail": detail})

    for y in [cfg["base_year"]] + cfg["robustness_years"]:
        for unit in ("THS_HW", "THS_PER"):
            tot = tables.na_emp[(y, "TOTAL", "EMP_DC", unit)]
            ssum = sum(tables.na_emp.get((y, s, "EMP_DC", unit)) or 0 for s in cfg["sectors"] + ["U"])
            add(f"sections_sum_to_total_{unit}", y, abs(ssum / tot - 1) < 1e-3, f"sum={ssum:.1f} total={tot:.1f}")
        worst = 0.0
        for s in cfg["sectors"] + ["TOTAL"]:
            for unit in ("THS_HW", "THS_PER"):
                e = tables.na_emp.get((y, s, "EMP_DC", unit)) or 0
                p = (tables.na_emp.get((y, s, "SAL_DC", unit)) or 0) + (tables.na_emp.get((y, s, "SELF_DC", unit)) or 0)
                if e:
                    worst = max(worst, abs(p / e - 1))
        add("employees_plus_selfemployed_equals_total", y, worst < 1e-3, f"max rel. dev={worst:.2e}")
        worst, where = 0.0, ""
        for s in cfg["sectors"] + ["TOTAL"]:
            m = model.lfs_means(tables, y, s, "EMP")
            pt = tables.lfs_pt.get((y, s, "PT"))
            tot = tables.lfs_pt.get((y, s, "TOTAL"))
            if m and m[3] == "direct" and pt and tot:
                d = abs(model.split_parttime(*m[:3]) - pt / tot)
                if d > worst:
                    worst, where = d, s
        add("inferred_part_time_share_matches_lfsa_epgan2", y, worst < 0.02, f"max abs diff={worst:.4f} (sector {where})")
    for scen_id, rows in results.items():
        bad = [r["nace_r2"] for r in rows if r["hours_after_ths"] > r["hours_before_ths"] + 1e-9]
        add(f"cap_never_increases_hours[{scen_id}]", rows[0]["year"], not bad, ",".join(bad) or "ok")
    for y in [cfg["base_year"]] + cfg["robustness_years"]:
        rows = results[f"{y}:A_observed"]
        tot = tables.na_emp[(y, "TOTAL", "EMP_DC", "THS_HW")]
        add("observed_bottom_up_equals_na_total_hours", y, abs(rows[-1]["hours_before_ths"] / tot - 1) < 1e-3,
            f"{rows[-1]['hours_before_ths']:.0f} vs {tot:.0f} (section U excluded)")
        sal = [r["nace_r2"] for r in rows if "SAL:NA_LFS_inconsistent" in r.get("lfs_source", "")]
        add("employee_implied_effective_weeks_plausible", y, set(sal) <= KNOWN_EMPLOYEE_WEEKS_EXCEPTIONS,
            "flagged: " + (",".join(sal) or "none") + f" outside {model.WEEKS_PLAUSIBLE}; "
            f"documented exception {sorted(KNOWN_EMPLOYEE_WEEKS_EXCEPTIONS)} (households as employers)")
        slf = [r["nace_r2"] for r in rows if "SELF:NA_LFS_inconsistent" in r.get("lfs_source", "")]
        add("DIAGNOSTIC_selfemployed_implied_weeks", y, "diagnostic",
            f"{len(slf)} sectors outside {model.WEEKS_PLAUSIBLE}: {','.join(slf)}; NA self-employed hours/person "
            "exceed LFS main-job hours (see insee_reconciliation)")
    return out


def main():
    if "--fetch" in sys.argv:
        fetch.fetch_all(RAW)
    bad = fetch.verify_manifest(RAW)
    if bad:
        raise SystemExit(f"raw snapshot hash mismatch: {bad}")
    cfg = json.loads((ROOT / "config" / "v62_config.json").read_text())
    raw = tidy.load_raw(RAW)
    TIDY.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    tidy.write_observations(tidy.observations(raw), TIDY / "observations.csv")
    tables = tidy.Tables(raw)

    results, all_rows = {}, []
    for y in [cfg["base_year"]] + cfg["robustness_years"]:
        for scen in cfg["scenarios"]:
            rows = model.run_scenario(tables, y, scen, cfg)
            for r in rows:
                r["year_provisional"] = tables.is_provisional(y)
            results[f"{y}:{scen['id']}"] = rows
            all_rows += rows
    write_csv(OUT / "labour_sector_year.csv", all_rows)

    summary = {"base_year": cfg["base_year"], "scenarios": {}, "slack_ths": {}, "insee_reconciliation": [],
               "rounding_bounds_required_gain": {}}
    for key, rows in results.items():
        t = rows[-1]
        summary["scenarios"][key] = {k: clean(t[k]) for k in (
            "hours_before_ths", "hours_after_ths", "persons_ths", "hours_retention_ratio",
            "required_hourly_productivity_gain", "additional_persons_same_profile_ths",
            "va_at_risk_fixed_productivity_meur", "trend_va_per_hour_2015_2019",
            "years_of_trend_2015_2019_to_cover_gain", "trend_va_per_hour_2015_2023",
            "years_of_trend_2015_2023_to_cover_gain")}
    for y in [cfg["base_year"]] + cfg["robustness_years"]:
        summary["slack_ths"][y] = model.slack(tables, y)
        for sid in (cfg["primary_scenario"], cfg["upper_scenario"]):
            scen = next(s for s in cfg["scenarios"] if s["id"] == sid)
            summary["rounding_bounds_required_gain"][f"{y}:{sid}"] = [
                clean(v) for v in model.rounding_bounds(tables, y, scen, cfg)]
    summary["offset_grid"] = {}
    for sid in (cfg["primary_scenario"], cfg["upper_scenario"]):
        t = results[f"{cfg['base_year']}:{sid}"][-1]
        summary["offset_grid"][sid] = {
            str(th): clean(model.residual_gain_with_offset(t["hours_before_ths"], t["hours_after_ths"], th))
            for th in cfg["offset_grid_theta"]}
    for y in range(2019, 2026):
        rec = model.insee_reconciliation(tables, y)
        if rec:
            summary["insee_reconciliation"].append({k: clean(v) for k, v in rec.items()})
    cd = labour_reserve.CountryData(raw)
    reserve = labour_reserve.run(cd, cfg["labour_reserve"])
    write_csv(OUT / "labour_reserve_country_year.csv", reserve)
    def fr_row(cap):
        return next(r for r in reserve if r["geo"] == "FR" and r["year"] == cfg["base_year"]
                    and r["apply_to"] == "SAL" and r["weekly_cap"] == cap
                    and r["entrant_relative_productivity"] == 1.0)
    fr = fr_row(30)
    summary["labour_reserve_FR_primary"] = {k: clean(v) for k, v in fr.items()}
    ep = cfg["evidence_pathway"]
    summary["evidence_pathway_FR"] = {}
    for cap, spec in ep["by_cap"].items():
        key = f"{cfg['base_year']}:{spec['scenario']}"
        sectors = results[key][:-1]
        trend = summary["scenarios"][key]["trend_va_per_hour_2015_2019"]
        summary["evidence_pathway_FR"][cap] = {}
        for name, case in spec["cases"].items():
            r = {k: clean(v) for k, v in model.evidence_pathway(sectors, fr_row(int(cap)), case,
                                                                ep["care_sectors"]).items()}
            r["years_of_2015_2019_trend"] = clean(model.years_to_cover(r["residual_required_gain"], trend))
            summary["evidence_pathway_FR"][cap][name] = r
    chk = checks(tables, cfg, results)
    bottom_up = results[f"{cfg['base_year']}:{cfg['primary_scenario']}"][-1]["required_hourly_productivity_gain"]
    chk.append({"check": "FR_top_down_gap_matches_sector_bottom_up", "year": cfg["base_year"],
                "passed": abs(fr["required_gain_no_mobilisation"] - bottom_up) < 0.01,
                "detail": f"top-down {fr['required_gain_no_mobilisation']:.4f} vs bottom-up {bottom_up:.4f}"})
    bad = [f"{r['geo']}{r['year']}" for r in reserve
           if abs(r["bench_top3_persons_ths"] - max(r["bench_top3_employment_gap_persons_ths"],
                                                    r["t1_unemployed_ths"] + r["t2_extended_lf_ths"])) > 1e-6
           or abs(r["slack_persons_ths"] - r["t1_unemployed_ths"] - r["t2_extended_lf_ths"]) > 1e-6]
    chk.append({"check": "labour_reserve_framings_are_alternatives_not_sums", "year": cfg["base_year"],
                "passed": not bad, "detail": ",".join(bad) or "benchmark = max(gap, T1+T2); slack = T1+T2"})
    weird = sorted({r["geo"] for r in reserve if r["weeks_flag"]})
    chk.append({"check": "DIAGNOSTIC_reserve_countries_with_implausible_weeks", "year": cfg["base_year"],
                "passed": "diagnostic", "detail": ",".join(weird) or "none"})
    summary["checks_passed"] = sum(c["passed"] is True for c in chk)
    summary["checks_total"] = sum(c["passed"] in (True, False) for c in chk)
    summary["checks_failed"] = [c["check"] for c in chk if c["passed"] is False]
    write_csv(OUT / "checks.csv", chk)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    report.build(OUT, cfg)
    for c in chk:
        print({True: "PASS ", False: "FAIL "}.get(c["passed"], "INFO ") + c["check"], c["year"], c["detail"])
    for key, s in summary["scenarios"].items():
        print(f"{key:55s} gain={s['required_hourly_productivity_gain']*100:6.2f}%  "
              f"extra persons={s['additional_persons_same_profile_ths']:7.0f}k  "
              f"years(2015-19 trend)={s['years_of_trend_2015_2019_to_cover_gain']}")
    print(json.dumps({k: summary[k] for k in ("slack_ths", "insee_reconciliation", "rounding_bounds_required_gain")}, indent=1))


if __name__ == "__main__":
    main()
