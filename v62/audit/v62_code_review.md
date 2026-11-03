# UNIRA V6.2 — independent adversarial code review

Reviewed: `src/unira_v62/{jsonstat,tidy,fetch,model,report}.py`, `run_all.py`, `config/v62_config.json`, `tests/`, frozen `data/raw/*.json`.
Run: `python3 run_all.py` (offline): exit 0, 30/30 checks pass. `python3 -m unittest discover -s tests`: 28 tests OK.
Note: `model.py`, `run_all.py`, `report.py` and the config were modified during the review (12:52; `residual_gain_with_offset`, offset grid, `REPORT_TABLES.md`). Line numbers below refer to the post-edit files. Headline numbers did not change.

Headline 2023 outputs: primary `cap30_employees_constant_absence` gain 20.10 % (rounding range 19.96–20.23 %), 6.81 m extra persons, 32.3 years of 2015–19 trend. Upper `cap30_all_constant_absence` 29.08 %. `cap30_employees_46w` 7.04 %.

---

## What was verified correct

- **JSON-stat decoding** (`jsonstat.py:17-33`). The row-major strides, the dimension order (taken from `id`), category order (taken from `index`), missing-cell skipping and per-cell status lookup are all correct. I decoded 6 cells independently, using a separate offset routine (`pos = pos*size + idx` over `id`). All 6 match `Tables`:
  - na_emp 2023 Q SAL_DC THS_HW = 4 676 271
  - na_emp 2023 Q SAL_DC THS_PER = 3 796.7
  - na_out 2019 C B1G CLV20_MEUR = 235 296.7
  - lfs_u 2023 Q SAL PT = 24.7 (flag `d`)
  - lfs_u 2023 T NSAL FT = suppressed (flag `u`, no value). The decoder correctly returns nothing for it.
  - na_emp 2025 TOTAL EMP_DC THS_HW = 45 954 911 (flag `p`)
- **Part-time share and cap formula** (`model.py:32-50`). The identity uT = q·uP + (1−q)·uF is solved correctly. No cell in the base year needs clipping, and `worktime=NRP` is empty in every snapshot.
- **`constant_absence`** (`model.py:74-78`). H·R/uT is correct under the stated assumption that full-time and part-time workers have equal effective weeks. In `extra_weeks_ft` the units are correct: thousand persons × weeks × h/week = thousand hours.
- **Productivity gain and additional persons.** The gain H/H′−1 is correct. Additional persons are computed per group as N·(H/h1−1) and summed (`model.py:149-150`, `184`). This is not double counted inside the code.
- **CAGR and years-to-cover** (`model.py:97-117`). Checked by hand: ln(1.2010)/ln(1.005679) = 32.3.
- **Chain-linked volumes are never summed across sectors.** The aggregate trend uses the published TOTAL CLV20 (`model.py:186` → `real_va_per_hour(..., "TOTAL")`). Only current-price VA is summed (`model.py:187`).

---

## Findings

### F1 — MAJOR — `normative_weeks` does not model a 30 h cap; it is roughly a 35.3 h cap. For the self-employed it moves in the opposite direction to the primary scenario
`model.py:79-82`, config scenarios `cap30_employees_46w` and `cap30_all_46w`.

The method takes full-time annual hours as `weeks × uF`, where `weeks = H/N/uT` is effective weeks from the national accounts (NA). It then caps them at 30 × 46 = 1 380 h. But NA effective weeks for employees are 38.7 (2023), not 46. The 1 380 h ceiling therefore allows 1 380/38.7 = 35.7 h in every week actually worked. The scenario keeps NA absences (sickness, RTT, public holidays) and then also grants a 46-week normative year.

Reproduction: run the primary scenario with `cap` set to 35, 35.5 and 36 for employees only. The gains are 7.81 %, 6.72 % and 5.65 %. `cap30_employees_46w` gives 7.04 %, which falls between 35 h and 35.5 h. `REPORT_TABLES.md` §1 still shows it on a row labelled "cap30".

The method also depends on absolute levels, where `constant_absence` does not:
- Implied full-time employee annual hours are 1 505 (NA × LFS), against 1 656 from INSEE (`summary.json` insee_reconciliation 2025, ratio 0.906). With the INSEE level the full-time cut would be 16.7 % instead of 8.3 %.
- For the self-employed, NA implied weeks are above 52 in 11 sections: F 73.6, J 74.2, D 63.7, N 63.7, … . In `cap30_all_46w`, self-employed retention is therefore 0.562, against 0.662 under `constant_absence`. The 46-week method cuts more than the "primary-style" method for this group.

So `normative_weeks` is neither a lower nor an upper bound. It is mainly an artefact of mixing NA and LFS concepts.

Fix: drop it from headline tables, or rename it ("≈35.7 h effective cap"). Add a check that `cap*weeks/implied_weeks` stays close to `cap`.

### F2 — MAJOR — The "lower bound" claim holds only for one bias. The primary scenario contains biases in both directions
`model.py:11-14`.

The concavity argument is correct within each full-time/part-time group: mean(min(x,c)) ≤ min(mean x, c). It also carries over to `extra_weeks_ft`, where the extra hours at min(uF,c) are overstated, and to `normative_weeks`, since min is still concave. But the primary number is not a lower bound on the true reduction overall:

- **Upward biases** (the reduction is overstated):
  - RTT and other compensatory leave for hours above 35 is kept as absence under "constant absence". The config's own `rtt2w` sensitivity lowers the gain by 4.1 pp, from 20.10 % to 15.99 %.
  - The model applies a hard, fully complied cap to *usual* hours. French full-time employees report 38.9 usual hours under a 35 h legal duration, so a legal cap does not behave as a hard cap.
  - NA hours include second-job hours. If the cap is per job, those hours should not be cut; the code scales all NA hours by the main-job ratio R/uT.
- **Downward biases:**
  - Dispersion within each group, including part-timers on 31.5–34 h contracts (the `pt_tail` scenario only partly covers this).
  - Second jobs, if the cap applies per person.
  - The `lfs_means` fallbacks (F6).
  - Full-time workers working more weeks than part-timers. INSEE's FT/PT annual ratio is 1.714 against a weekly ratio of 1.672, so full-timers carry a larger share of hours than assumed.
- `pt_tail` replaces the bound with an assumed tail distribution, so no bound statement applies to it.

The net direction is unknown. Restate as "lower bound *with respect to within-group dispersion only*", and say so in `REPORT_TABLES.md`, which currently says nothing about bias direction.

### F3 — MAJOR — Latent silent bug: hours with no matching persons cell vanish from "hours after"
`model.py:127-148`, together with `66-67`.

If `THS_HW` is present but `THS_PER` is missing or zero, the `else` branch sets `h1 = 0.0` while `H` still goes into `hours_before`. The lost hours are then reported as a required productivity gain.

Reproduction: delete `na_emp[(2023,'C','SAL_DC','THS_PER')]` and run `A_observed`. The gain is **9.52 %** for "no policy change". No check catches this:
- `observed_bottom_up_equals_na_total_hours` (`run_all.py:71-75`) compares `hours_before` only.
- `cap_never_increases_hours` cannot fire, because hours went down.

Fix: raise when exactly one of H or N is present. Add a check that `A_observed` has `hours_after == hours_before` in every row.

### F4 — MAJOR — NA self-employed hours are inconsistent with LFS, yet the upper scenario scales them by the LFS non-salaried (NSAL) main-job ratio
`model.py:29` (GROUPS), `run_all.py:80-83`.

NA hours per self-employed person are 2 352 in 2023, 1.21× INSEE's LFS figure of 1 903. Implied weeks exceed 52 in 11 of 20 sections, which is physically impossible. The check reports this as "INFO" and carries on.

A plausible cause is that `SELF_DC` hours include secondary self-employment, for example micro-entrepreneur activity of people whose main job is salaried, while `N` counts people by their main job. Applying NSAL main-job ratios to that hours block has no foundation, and the bias can go either way. The upper scenario (29.1 %) and `cap30_all_*` all depend on it.

Fix: reconcile NA `SELF_DC` with INSEE non-salariés sources before using it. At minimum, give the upper scenario's self-employed component the evidence class `SYNTHETIC_ASSUMPTION`.

### F5 — MAJOR (presentation) — Only the more favourable trend window is shown
`report.py:32,51-52`, `run_all.py:146-148`.

Years to cover on the 2015–19 trend (0.568 %/yr) are 32.3 for the primary scenario. On the 2015–23 trend (0.061 %/yr), which is also computed in `summary.json`, they are **301** (419 for the upper scenario). The generated report and the console output show only 32.

The 2015–19 figure is a 4-year CAGR between two single points, so it is sensitive to endpoints. Neither window is a credible forward trend.

Fix: show both windows, or a range. Better still, use a log-linear trend over 1995–2019 with a confidence interval.

### F6 — MINOR — LFS fallback discards published direct means and imputes self-employed hours from employee-dominated cells
`model.py:53-61`.

The fallback requires all three of TOTAL, FT and PT to be present. If PT is missing it throws away direct values that do exist:
- B SAL 2023: published uT = 41.0 and uF = 41.5 are replaced by the national TOTAL_SAL values (36.1/38.9/23.1). Retention becomes 0.797; using the direct value it would be about 0.732.
- D NSAL 2023: published uT = 59.9 (flag `u`) is replaced by D/EMP 39.7. Retention becomes 0.751 instead of about 0.50.

The `(nace, EMP)` fallback is tried before `(TOTAL, NSAL)`, so self-employed groups get employee hour profiles.

The affected hours are currently below 0.1 % of the total, so the effect is negligible today. It is silent, untested, and grows with any change to the sector list or year.

### F7 — MINOR — LFS status flags are discarded, and evidence classes break the project rule
`tidy.py:97-103` and `61-64`.

- `Tables` ignores LFS flags. All LFS 2024 cells are flagged `b` (break in series). The robustness year 2024 is therefore not a like-for-like check, and nothing in the outputs says so.
- Low-reliability cells are used directly, for example K NSAL PT for 2023 and 2024 (`du`/`bdu`).
- `observations()` assigns `VERIFIED_OFFICIAL` to every value without a `p` flag, including cells flagged `u`, `b` and `d`. Handover 03 says "Do not use VERIFIED_OFFICIAL without a source-table audit". In the evidence schema, `u` should at least map to `REPORTED_NEEDS_RECHECK`.
- Suppressed cells (a status with no value) are dropped rather than recorded as `MISSING`.
- `is_provisional` (`tidy.py:105-106`) checks only `na_emp`. It ignores `na_out` and the LFS `b` flags.

### F8 — MINOR — Domestic vs national concept, persons vs jobs, Mayotte
- NA EMP_DC persons are 30 376k in 2023, against 28 589k LFS employed from `lfsa_epgan2`: +6.3 %. Causes include cross-border workers (LFS residents working abroad, NA non-residents working in France), multiple jobs, and coverage.
- The LFS cells carry flag `d` (definition differs), for example the Mayotte coverage stated in INSEE's 2025 series.
- The ratio method is robust to this, but these outputs are not: `implied_effective_weeks`, `additional_persons_same_profile_ths` (expressed in NA persons units), F1 and F4.

### F9 — MINOR — "Additional persons" sits next to a slack table that already contains employed people
`report.py:59-63`.

The 6.81 m extra persons (in NA units) is printed beside LFS slack of 4.80 m. That slack figure includes 1.25 m underemployed part-timers, who are already counted in N. A reader who compares the two double counts them; those people supply hours (capped at 30), not new heads.

Two smaller points:
- The productivity gain and additional persons are alternative ways to close the gap. They must not be added together; the table does not say so.
- In the upper scenario, "same profile" means hiring new self-employed workers with the impossible NA hours profiles from F4.

### F10 — MINOR — `extra_weeks_ft` has no guards
`model.py:77-78`.

- It applies to self-employed workers whenever `apply_to` includes SELF, although RTT is an employee institution. Reproduction: `cap30_all_constant_absence` with `extra_weeks_ft=2` gives 23.8 % instead of 29.1 %.
- There is no check that implied weeks plus d stays at or below 52.
- It applies to every full-time employee in every sector, although not every full-time employee has RTT (for example those on forfait-jours or working ≤35 h).

### F11 — MINOR — Non-market and imputed sectors
O, P and Q are 24.3 % of hours. They are flagged, but they still show numeric years-to-cover of 19.6–27.6 in the sector table.

The aggregate trend includes their input-based near-zero growth, plus reallocation effects between sectors. Excluding O, P, Q, L and T gives a market-only gain of 20.14 %, almost the same, so the gain is robust. The years-to-cover denominator is not, and is not decomposed.

### F12 — MINOR — Weak checks and "bounds"
- `inferred_part_time_share_matches_lfsa_epgan2` compares two tables from the same LFS with the same self-declared classification, and NRP is empty. It confirms the arithmetic, not the concept. It is also run only for EMP, not for SAL or NSAL.
- `rounding_bounds` (`model.py:207-215`) covers only ±0.05 h publication rounding. It does not cover LFS sampling error, which is much larger for sector × status cells and especially for `u` cells. Labelling it "bounds" invites over-reading.

### F13 — MINOR — The JSON-stat reader assumes Eurostat-specific forms
`jsonstat.py:20-25`, `tidy.py:89-103`.

- It assumes `category.index` is a dict. The array form allowed by JSON-stat fails with AttributeError.
- It assumes `status` is a dict. String and list forms raise on `.get`.
- `Tables` keys drop age, sex, unit and freq without checking that those dimensions are singletons. A re-fetch that returned several ages or units would silently overwrite values ("last cell wins"). The hash pinning protects the current files, but `--fetch` does not.

Fix: in `Tables`, assert `size == 1` for every dimension that is not part of the key.

---

## Missing tests
- `A_observed` identity at the level of each sector and group on real data (would catch F3). A test with H present and N missing.
- `lfs_means` fallback order and source labels, including the partial-cell case (F6).
- JSON-stat decoding on a synthetic document with several non-singleton dimensions in non-alphabetical index order, dense `value` list, list/str `status`, and a status-only cell. The current `test_known_cell_decoded` only checks cells at position 0 or near it.
- `normative_weeks` on real data with an equivalence assertion (F1). `extra_weeks_ft` combined with SELF (F10).
- A pinned value for the `pt_tail` scenario. `retained_weekly` when `u_pt >= cap` together with a tail.
- `total_row` and `_derived`: the summed `va_at_risk` against TOTAL `va_cp`, and `years_to_cover` with `trend=None`/0.
- Regression pins on headline outputs, for example primary 2023 = 0.200951 ± 1e-6, so that silent changes from concurrent edits get caught.
- `report.build` handling of "inf", None and 0 % (the part-time cell appends "%" only when the value is truthy, `report.py:48`).
- `checks()` itself, for example that a corrupted table fails the intended checks.
