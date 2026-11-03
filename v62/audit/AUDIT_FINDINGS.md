# UNIRA audit findings — consolidated at V6.2 (2026-11-03)

Four independent audits ran in parallel as separate agents. Each was given the code and sources, not the lead researcher's conclusions. Full reports:

| audit | report | machine-readable |
|---|---|---|
| Archive integrity and reproducibility (V0.1–V6.1) | `reproducibility_audit.md` | `reproducibility_checks.csv` (100 checks) |
| Primary-source verification of the evidence register | `source_verification.md` | `source_verification.csv` (23 rows), `source_cache/` |
| Adversarial code review of V6.2 | `v62_code_review.md` | — |
| Evidence review: hours → productivity and employment | `hours_productivity_evidence.md` | `hours_productivity_evidence.csv` (22 rows) |

## A. Archive (V0.1–V6.1)
- **Integrity:** 125/125 manifest hashes match. The handover documents themselves are not hashed.
- **Reproducibility:** 11 of 14 source_tree suites pass (90/90 tests). v49, v50 and v53 need unpinned numpy and scipy and were not run. An independent stdlib brute-force solver reproduces their archived optima exactly. Every regenerable output is byte-identical to the archive.
- **Corrections to `handover/02`:**
  1. **V5.6 public shortfall (300,000 U) is in the baseline, not an independent stress case.** The `public_fund_shortage` scenario equals the baseline (`v56/model.py:34` vs `:60`).
  2. **V6.1 output contradicts its own caveat.** `additional_workers_at_unchanged_productivity` (6.1 m) applies the full-time-only 1,656 h ratio to all 30.5 m workers (`v61/model.py:19`). Superseded by V6.2.
  3. **"Stock-flow consistency" (V5.6/V5.7) holds by construction only.** Money issuance has no matching liability. A = L + E cannot fail because equity is the residual. Inventories and capital are booked without counterparties. **V5.6/V5.7 should not be described as SFC.**
  4. **V5.0 lexicographic stock-first optimisation changes nothing on the shipped data.** Stock-first, cost-min and carbon-weighted all give 5 new builds. The "optimisation" findings are data-driven ties.
  5. **V4.8 is a greedy fill, not an optimiser.**
  6. **V6.0's RTE/INSEE constants are unused by its computation.**
- **Confirmed:** V5.9 is a genuine Leontief solve (agrees with exact inverse to 1e-14). All other quoted numbers in 02 match outputs.
- **Gaps:** V3.7 and V4.2 have no package. V2 and V2.2 code exists only in the ZIPs. `v51/build.py` hard-codes `/mnt/data`, and its tests are self-generated.

## B. Primary sources (evidence register, handover/03)
- **0 contradictions.** 16 CONFIRMED and 7 CONFIRMED_WITH_CAVEAT out of 23.
- **France labour:**
  - 30.5 m employed: the exact figure is 30,483 k (excl. Mayotte, provisional 2025).
  - 1,656 h and 38.9 h refer to full-time employees.
  - **New:** part-time employees work 966 h/yr; self-employed 1,903 h/yr. INSEE publishes no all-worker annual average.
- **Caveats:**
  - GDP €2,822.5 bn is the first estimate; revisions are unchecked.
  - Paris 2023 census vacant = 139,075 (the register uses 2022, 136,957).
  - London 93,602 is in MHCLG Live Table 615, not on the GLA page.
  - London 105,138 includes council-tax-exempt homes.
  - London's 6.7% overcrowding figure is a 3-year average and probably an underestimate.
  - Tokyo omits second homes (9,600).
  - England's £7,480 is a modelled mean for the 42% of homes that can reach band C.

## C. V6.2 code review — findings and disposition
| # | severity | finding | disposition |
|---|---|---|---|
| 1 | major | `normative_weeks` (V6.1 46-week convention) is not a 30 h cap (≈35.7 h/week actually worked) and is neither a lower nor an upper bound | **Fixed in documentation:** relabelled in model docstring, research note table and §5.1; kept only as a V6.1 comparator |
| 2 | major | "lower bound" claim overstated | **Fixed:** narrowed to within-group dispersion; opposing biases listed; net direction declared unknown |
| 3 | major | hours silently dropped if persons cell missing (A_observed would show 9.5% "gain") | **Fixed:** raises `ValueError`; regression test added |
| 4 | major | NA self-employed hours/person 1.21× INSEE LFS | **Documented:** primary scenario leaves self-employed uncapped; all-workers scenario labelled less reliable; INFO diagnostic in checks |
| 5 | major | 2015–23 trend (≈301 years) computed but not displayed | **Fixed:** both windows shown in all tables and the note |
| 6 | minor | LFS flags (`u`, `b`) discarded | **Fixed:** propagated into `observations.csv` uncertainty; `u` → REPORTED_NEEDS_RECHECK |
| 7 | minor | `extra_weeks_ft` also applied to self-employed | **Fixed:** employees only; test added |
| 8 | minor | 6.8 m extra persons shown next to slack that includes 1.25 m already employed | **Fixed:** wording, plus the new labour-reserve module treats underemployed part-timers as extra hours, not persons |
| 9 | minor | LFS fallback discards published direct means in some cells | **Open:** affects small sections (B, D, E self-employed); recorded in `lfs_source` column |

## D. Self-audit finding during the labour-reserve extension
- A first draft of `labour_reserve_framings_*` was a tautological check (the same failure mode as V5.7). Rewriting it exposed a **real bug**: the benchmark framing overwrote the raw benchmark-gap column. Fixed (`bench_*_employment_gap_persons_ths` vs `bench_*_persons_ths`), with known-answer tests.

## E. Evidence review — implications adopted
- θ ranges adopted in `config/v62_config.json → evidence_pathway`:
  - market sectors, short run: 0.10–0.35;
  - care sectors (P, Q): 0–0.15.
- **Hours cuts do not create net jobs without subsidies.** Labour-reserve take-up is therefore an explicit SYNTHETIC policy parameter, not an induced effect.
- Volunteer-firm pilots (UK 2022, Iceland trials) are excluded as parameter sources because of selection bias.
