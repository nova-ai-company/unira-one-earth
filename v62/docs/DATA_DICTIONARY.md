# V6.2 data dictionary

## `data/raw/` — frozen Eurostat snapshots (JSON-stat 2.0)

| file | Eurostat table | content used | note |
|---|---|---|---|
| `na_employment_hours.json` | `nama_10_a64_e` | hours worked (THS_HW) and persons (THS_PER); EMP_DC total, SAL_DC employees, SELF_DC self-employed; NACE sections; FR 2015–2025 | National accounts, **domestic concept**, all jobs (main + secondary) for hours. 2024–2025 provisional (`p`). |
| `na_output.json` | `nama_10_a64` | B1G gross value added, P1 output; current prices (CP_MEUR) and chain-linked volumes (CLV20_MEUR) | Chain-linked volumes are **not additive** across sectors; TOTAL is taken from the table, not summed. |
| `lfs_usual_hours.json` | `lfsa_ewhun2` | mean usual weekly hours in main job; wstatus EMP/SAL/NSAL × worktime TOTAL/FT/PT | LFS, **national concept**, main job only, published to 0.1 h. Series break 2021 (IESS regulation); only 2023–2025 used for policy arithmetic. |
| `lfs_actual_hours.json` | `lfsa_ewhan2` | mean actual weekly hours (persons at work in reference week) | Snapshot for cross-checks; not used in the scenario arithmetic. |
| `lfs_parttime_persons.json` | `lfsa_epgan2` | persons by full-/part-time and NACE | Used only to validate the part-time share inferred from hour means. |
| `lfs_slack.json` | `lfsi_sla_a` | unemployed, underemployed part-timers, seeking-not-available, available-not-seeking (15–74) | Context only; no skills or location matching. |

`raw_manifest.csv` records URL, retrieval time (UTC), SHA-256, byte size, licence. `run_all.py` refuses to run if any hash differs.

## `data/tidy/observations.csv`
Every raw cell in the handover evidence schema (`indicator_id, value, unit, year, … evidence_class, license`) plus `nace_r2`, `status_flag`. `evidence_class` is `VERIFIED_OFFICIAL` for final values retrieved from the named table (value identity only — conceptual fit is discussed in the research note) and `REPORTED_NEEDS_RECHECK` for provisional values.

## `outputs/labour_sector_year.csv` (workstream A contract output)
One row per year × scenario × NACE section, plus a `TOTAL_bottom_up` row.

| column | unit | definition | class |
|---|---|---|---|
| `SAL_*`, `SELF_*` `hours_before_ths` / `hours_after_ths` | thousand hours/yr | NA hours before / after the scenario, by group | before: official; after: MODEL_DERIVED |
| `*_persons_ths` | thousand persons | NA persons employed | official |
| `*_part_time_share` | share | q from `uT = q·uP + (1−q)·uF` | MODEL_DERIVED |
| `*_implied_effective_weeks` | weeks | (NA hours / NA persons) / LFS usual weekly hours | MODEL_DERIVED; diagnostic of NA/LFS consistency |
| `*_lfs_usual_weekly_hours` | h/week | LFS mean usual hours (all) used for the group | official |
| `hours_retention_ratio` | ratio | hours after / before | MODEL_DERIVED |
| `required_hourly_productivity_gain` | ratio | before/after − 1, holding output and persons fixed | MODEL_DERIVED arithmetic requirement, not a forecast |
| `additional_persons_same_profile_ths` | thousand persons | Σ_g N_g·(H_g/H'_g − 1): persons with the same hours profile needed to restore hours at unchanged productivity | MODEL_DERIVED |
| `va_current_prices_meur` | € million | B1G current prices | official, market benchmark only |
| `va_at_risk_fixed_productivity_meur` | € million | VA × (1 − retention) | MODEL_DERIVED market-price benchmark; **not a welfare or physical loss** |
| `real_va_per_hour_eur2020` | € (2020 chain-linked) / hour | CLV20 VA / hours | MODEL_DERIVED |
| `trend_va_per_hour_A_B` | %/yr | CAGR of real VA/hour between years A and B | MODEL_DERIVED |
| `years_of_trend_A_B_to_cover_gain` | years | ln(1+gain)/ln(1+trend); `inf` if trend ≤ 0 | MODEL_DERIVED |
| `breakeven_avoidable_output_share` | share | output share that would have to be genuinely avoidable to close the gap with zero productivity growth | MODEL_DERIVED; no evidence on avoidability is claimed |
| `output_measure_caveat` | text | `nonmarket_input_based` (O, P, Q), `imputed_output` (L, T) | — |
| `lfs_source` | text | `direct`, `imputed_from_<sector>_<status>` fallback, `NA_LFS_inconsistent` flags | — |
| `year_provisional` | bool | NA year carries Eurostat `p` flags | — |

## `outputs/summary.json`
Scenario totals, θ offset grid, labour-market slack, LFS rounding bounds, INSEE reconciliation, check counts.

## `outputs/checks.csv`
Machine-readable accounting/consistency checks (`passed` = True/False, or `diagnostic`).
