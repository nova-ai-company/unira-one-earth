# UNIRA Phase 0: Reproducibility Audit

**Date:** 2026-11-03 · **Environment:** macOS (Darwin 24.6), Python 3.14.8, standard library only (numpy, scipy and pulp are not installed and were not installed).
**Scope:** archive integrity, test and model re-runs, comparison of outputs against the archive, tracing of handover claims, and a code audit of the "exact / SFC / Leontief" claims.
**Nothing under `handover/`, `source_tree/`, `historical_packages/` or `historical_documents/` was modified.** All work was done in `v62/audit/repro_work/`:

| Path | Contents |
|---|---|
| `repro_work/source_tree/` | fresh copy of `source_tree`; models were run here, so it now holds the regenerated outputs |
| `repro_work/zips/` | pristine extraction of all 34 historical ZIPs |
| `repro_work/zips_run/` | copy of `zips/` where the stdlib-only zip versions were run |
| `repro_work/logs/` | stdout/stderr of every run and test |
| `repro_work/stdlib_verifiers/` | independent audit scripts: `compare_outputs.py`, `verify_milp_bruteforce.py`, `verify_v59_leontief.py`, `verify_v47_dp.py` |

Machine-readable results: `v62/audit/reproducibility_checks.csv` (100 checks).

---

## Summary table

| Version | Tests pass/total | Outputs reproduce? | Handover claims match? | Notes |
|---|---|---|---|---|
| V0.1 simulator (`unira_simulator_v01.py`) | asserts pass (no unittest) | prints only; values match 02 | **Yes** (18.6%, 261 tn U, 130.5/154.8 bn h) | Not in any ZIP; source_tree only |
| V2 | no tests | **Yes**, byte-identical (zip code) | n/a | `unira_v2.py` exists **only in ZIP**, not in source_tree |
| V2.1 (`unira_v21.py`) | no tests | **Yes**, byte-identical | n/a | |
| V2.2 | no tests | **Yes**, byte-identical (zip code) | n/a | `unira_v22.py` exists **only in ZIP** |
| V3, V3.1 | – | not run (network fetchers) | – | `build_v3.py` and `fetch_world_bank_v31.py` call urllib |
| V3.2, V3.3 | V3.3 0/1 run (import error) | not run (numpy) | – | |
| V3.4 | 5/5 | Yes | – | |
| V3.5 | 0 run (scipy import error) | not run (scipy) | – | |
| V3.6 | 4/4 | runs (no archived output) | – | |
| V3.7 | – | – | – | **No package or code in the archive** |
| V3.8 | 7/7 | Yes | – | |
| V3.9 | 10/10 | Yes | **Yes** ("10 tests") | |
| V4.0 | 0 run (numpy import error) | not run (numpy) | – | |
| V4.1 | no tests | Yes | **Yes** (124/483/898) | |
| V4.2 | – | – | – | **No package or code in the archive** |
| V4.3–V4.6 | no tests | Yes | not checked in detail | |
| V4.7 | 5/5 | Yes | – | DP optimiser; brute force agrees in 250/250 cases |
| V4.8 (v48) | 5/5 | **Yes**, byte-identical | Yes (£7,480, 56%, EPC 70 are input constants) | "Optimiser" is a greedy fill |
| V4.9 (v49) | **0/7 (not run: numpy/scipy missing)** | Cannot regenerate; **independent stdlib brute force reproduces the archive exactly** | **Yes** (€8.565m, 4,416 t) | Genuine MILP |
| V5.0 (v50) | **0/7 (not run: numpy/scipy missing)** | Cannot regenerate; brute force reproduces the archive exactly | Yes | Lexicographic stage changes nothing on this data |
| V5.1 (v51) | 5/5 | Yes (CSV/README) | Yes (city figures present) | `build.py` crashes on hard-coded `/mnt/data/...zip` (line 23); the test file is self-generated |
| V5.2 (v52) | 5/5 | Yes | Yes (overcrowding figures) | |
| V5.3 (v53) | **0/6 (not run: numpy/scipy missing)** | Cannot regenerate; brute force reproduces all 5 scenarios exactly | **Yes** (20/35/25/20, €14.6m; 74/26 at €8m) | No requirements.txt |
| V5.4 (v54) | 7/7 | Yes | **Yes** | |
| V5.5 (v55) | 11/11 | Yes | **Yes** | |
| V5.6 (v56) | 12/12 | Yes | **Partly**: food 30 and labour 2,000h match; the **300,000 U public shortfall is the baseline**, not an independent stress case | Ledger balance is true by construction only |
| V5.7 (v57) | 13/13 | Yes | **Yes** (30 / 3,000h / 310,000 U) | A = L + E audit is tautological |
| V5.8 (v58) | 10/10 | Yes | **Yes** (0 yrs/20m U; 19; 19; 1) | Credit limit is a flag only |
| V5.9 (v59) | 10/10 | Yes | **Yes** (0/1/16/14/11/20) | Leontief solution verified exact to 1e-14 |
| V6.0 (v60) | 7/7 | Yes | Values match archived **inputs**; they are not computed | TWh constants are unused by the computation |
| V6.1 (v61) | 5/5 | Yes | **Yes** (1.45/8.70/15.94/20.00%) | One output column contradicts a handover caveat |

**Totals (source_tree):** 11 of 14 suites run and pass (90/90 tests). 3 suites (20 tests: v49, v50, v53) cannot run without numpy and scipy. Every output that could be regenerated is **byte-identical** to the archive.

---

## 1. Archive integrity (manifest)

- All **125** entries in `handover/08_ARCHIVE_MANIFEST.csv` exist, and their SHA-256 hashes and byte sizes match. There are **0 mismatches and 0 missing files**.
- **Present but unlisted:** only the 10 files in `handover/` (00–09). The manifest does not cover the handover documents themselves, so there is no integrity hash for them.
- `09_ARCHIVE_BUILD_INFO.json` counts are consistent: 125 files, 34 ZIPs, 88 source files, 3 documents.
- **source_tree vs the ZIPs:** every file in v48–v61 is byte-identical to the corresponding historical ZIP member, with no extra or missing files (`.pyc` ignored).
  - V2 and V2.2 code (`unira_v2.py`, `unira_v22.py`) and `UNIRA_V2_scenarios.json` / `UNIRA_V22_results.json` exist **only inside the ZIPs**. The source_tree copies of these versions are notes and CSVs without the code that produced them.
  - `unira_simulator_v01.py` is in no ZIP.

## 2. Test and model runs (source_tree copy)

| Dir | Test command | Result | Model command | Result |
|---|---|---|---|---|
| v48 | `python3 -m unittest -v test_model` | 5/5 OK | `model.py` | exit 0 |
| v49 | same | ERROR: `ModuleNotFoundError: numpy` (7 tests) | `model.py` | exit 1 (numpy) |
| v50 | same | ERROR: numpy (7 tests) | `model.py` | exit 1 |
| v51 | `test_evidence` | 5/5 OK | `build.py` | exit 1 after writing CSV/README/test: `FileNotFoundError: /mnt/data/unira/UNIRA_V51_Metropolitan_Evidence.zip` (build.py:23) |
| v52 | | 5/5 OK | | exit 0 |
| v53 | | ERROR: numpy (6 tests) | | exit 1 |
| v54 | | 7/7 OK | | exit 0 |
| v55 | | 11/11 OK | | exit 0 |
| v56 | | 12/12 OK | | exit 0 |
| v57 | | 13/13 OK | | exit 0 |
| v58 | | 10/10 OK | | exit 0 |
| v59 | | 10/10 OK | | exit 0 |
| v60 | | 7/7 OK | | exit 0 |
| v61 | | 5/5 OK | | exit 0 |
| top level | n/a | n/a | `unira_v21.py`, `unira_simulator_v01.py` | exit 0 (simulator's internal asserts pass) |

**Dependency missing, not run:** v49, v50 and v53.
- `v49/requirements.txt`: `numpy>=1.26`, `scipy>=1.11`
- `v50/requirements.txt`: `numpy`, `scipy` (unpinned)
- v53 has no `requirements.txt`; its docstring says "Requires scipy >=1.9".

Neither file pins exact versions, and no lock file or environment specification exists.

**v51 test circularity:** `build.py` rewrites `test_evidence.py` (line 22). The tests then check the CSV that `build.py` hard-coded moments earlier, so they verify consistency of the build, not the data.

## 3. Output comparison (tolerance 1e-9 relative)

`stdlib_verifiers/compare_outputs.py` compares every CSV, JSON and MD in the archive with its regenerated counterpart.

- **Byte-identical after regeneration (mtime confirmed rewritten):**
  - v48 `scenario_results.csv`
  - v51 `city_evidence.csv`, `screening_scenarios.csv`, `README.md`, `test_evidence.py`
  - v52 both CSVs
  - v54, v55, v56 `results.csv` + `results.json`
  - v57 `results.json`
  - v58 `annual_results.csv`, `summary.json`, `assumptions.json`
  - v59 `annual_results.csv`, `results.json`
  - v60 `scenario_results.csv`
  - v61 `scenarios.csv`
  - V2.1 CSV + JSON
- **ZIP-only versions re-run from `zips_run/`, all byte-identical:** V2, V2.2 (both packs), V3.4, V3.8, V3.9, V4.1, V4.3, V4.4, V4.5, V4.6, V4.7.
- **Not regenerable here:** v49, v50, v53, V3.2, V3.3, V3.5, V4.0 (numpy/scipy), V3 and V3.1 (network).
  - For **v49, v50 and v53**, `verify_milp_bruteforce.py` re-solves every scenario by exhaustive integer enumeration (stdlib, about 9 s). It reproduces all 4 + 6 + 5 archived scenario rows **exactly**: cost, carbon, new-build count, units and allocation. This is independent evidence that the archived MILP outputs are correct optima. It does not replace running the original code under a pinned scipy.

No numerical discrepancies were found in any regenerated output.

## 4. Handover claims (02_RESEARCH_HISTORY_AND_FINDINGS.md) vs outputs

| Version | Claim | Traced to | Verdict |
|---|---|---|---|
| V4.9 | min-cost €8.565m, 4,416 tCO2e; 100 households, 20 accessible | `v49/results.csv` row `cost_min` = 8565000.0 / 4416.0; demand at `v49/model.py:46` | MATCH (also confirmed by brute force) |
| V5.0 | lexicographic minimise new, then cost/carbon | `v50/model.py:28-33` | MATCH in code. **On this dataset stock_first = cost-min = carbon_weighted (5 new builds in all)**, so the lexicographic step has no effect. Only the operational-emissions scaling scenarios differ. |
| V5.3 | 20/35/25/20, €14.6m | `v53/results.csv` `minimum_cost` | MATCH |
| V5.3 | €8m → 74 housed / 26 unmet | `tight_budget`: 20+35+19 = 74, unmet 26, cost €7.98m | MATCH. Min-cost, carbon_price_200 and stock_first are all identical. |
| V5.4 | UNIRA 19,700h / 66t / 347.5t vs current-style 25,700h / 117t / 670t | `v54/results.csv` rows C and A | MATCH (inputs are synthetic coefficients in `scenarios.json`) |
| V5.5 | 10.2m U income, 7.65m U spending, 5.484m U basket | `v55/results.csv` | MATCH |
| V5.6 | food shortage 30 units | `food_shortage` | MATCH |
| V5.6 | **public shortfall 300,000 U "in independent synthetic stress cases"** | `public_unpaid_U = 300000` appears in **baseline**, food_shortage, labour_shock and money_creation. The `public_fund_shortage` scenario passes `public_cost=500_000`, which equals the default (`v56/model.py:34` vs `:60`), so it is **identical to baseline**. | **MISLEADING.** The shortfall is built into the baseline; only `public_cost_low` has none. `test_public_gap` (test_model.py:13) asserts this baseline gap on purpose. |
| V5.6 | labour shortage 2,000 h | `labour_shock` | MATCH. The shortfall does not reduce food output in V5.6. |
| V5.7 | food 30, labour 3,000 h, public 310,000 U | `results.json` food_shock / labour_shock / public_shortfall | MATCH. The labour shock also produces 18 units of unmet food, which 02 does not mention. |
| V5.8 | baseline 0 shortage years, 20m U borrowing | `summary.json` | MATCH. 20m equals the limit exactly, so `credit_limit_breached` is false because the test is a strict `>`. |
| V5.8 | 2.5% growth 19; no replacement 19; severe shock 1 | `population_growth` 19, `lower_investment` 19, `food_supply_shock` 1 | MATCH |
| V5.8 | borrowing ceiling diagnostic only | `v58/model.py:74`; `restricted_credit` (limit 5m) still borrows 20m | MATCH |
| V5.9 | 0 / 1 / 16 / 14 / 11 / 20 shortage years | `results.json`, recounted in `verify_v59_leontief.py` | MATCH |
| V6.0 | 494.7 / 445.7 / 32.6 TWh, €2,822.5bn | `v60/evidence.csv`; `model.py:8-10` | MATCH to archived **inputs**. Not code output, the constants are unused by the computation, and the external sources were not re-verified in this phase. |
| V6.1 | 30.5m; 1,656h; 1,380h; 1.45 / 8.70 / 15.94 / 20.00% | `v61/scenarios.csv` | MATCH |
| V6.1 | "Do not multiply 30.5m by 1,656" | `scenarios.csv` column `additional_workers_at_unchanged_productivity` applies the full-time 1,656h ratio to all 30.5m workers, giving **6.1m** extra workers (`v61/model.py:19`) | **CODE CONTRADICTS HANDOVER CAVEAT** (population extrapolation of a full-time-only benchmark) |
| V1–V3.3 | 18.6%, 261 tn U, 130.5 / 154.8 bn h | `unira_simulator_v01.py` output | MATCH |
| V3.9 | 10 tests | ZIP v39 suite: 10/10 pass | MATCH |
| V4.1 | Vallauris 124/483/898 | ZIP `v41/pilot.py` re-run | MATCH |

**Claims not traceable to code output:**
- All empirical statistics (V4.1–V4.8 and V5.1/V5.2 city figures, V6.0 RTE/INSEE, V6.1 INSEE) are **hard-coded constants** in CSVs or scripts, with source URLs. They are traceable to the archive, not derived. Their correctness against the primary sources was not checked in Phase 0.
- V3.4–V4.0 qualitative statements, such as "no new housing/appliance production under chosen stock assumptions", were not cross-checked against outputs. Of their code, V3.4, V3.8 and V3.9 run; V3.5 and V4.0 need numpy/scipy.

**Versions without source_tree code** (full `unzip -l` listing is in the CSV and logs):

| Version | Code in the archive |
|---|---|
| V2, V2.2 | ZIP only |
| V3 | `build_v3.py` |
| V3.1 | `fetch_world_bank_v31.py` (network) |
| V3.2 | `unira_v32.py` (numpy) |
| V3.3 | `unira_v33.py` (numpy) + test |
| V3.4 | `unira_stock_flow.py` + test |
| V3.5 | `unira_v35.py` (scipy) + test |
| V3.6 | `payment_resilience.py` + test |
| **V3.7** | **none: no package exists** |
| V3.8 | code + tests |
| V3.9 | code + tests |
| V4.0 | numpy, + test |
| V4.1 | `pilot.py` |
| **V4.2** | **none: no package exists** |
| V4.3 | `build.py` |
| V4.4 | `sensitivity.py` |
| V4.5, V4.6 | `model.py` |
| V4.7 | `model.py` + tests |

The final package (`UNIRA_Research_Package.zip`) contains the working paper and `unira_v22.py`.

## 5. Code audit of "exact", "stock-flow consistent" and "Leontief"

**V4.9: is it integer optimisation?** **Yes.** It calls `scipy.optimize.milp` with `integrality=np.ones(n)` (`v49/model.py:38`). Caveats:
- `mip_rel_gap` is not set, so the HiGHS default gap applies, with a 30 s time limit.
- Stock-first uses a big-M penalty (`:29-31`), which is valid here.
- The problem is separable by cohort and has no coupling constraint, so cheapest-first greedy gives the same optimum.
- The "100 households" are cohort demand counts. There is no household-to-dwelling matching. Demand is `>=` (`:35`).

**V5.0.** A genuine two-stage lexicographic MILP with `mip_rel_gap: 0` (`v50/model.py:26`, `:28-33`). Demand is an equality (`:20`).

**V5.3.** MILP (`v53/model.py:24, 31`) with an unmet-need slack penalised at 1e9 (`:20`). If the stock-first stage 1 is infeasible, the constraints are **silently reset** and stock-first is dropped (`:28`).

**V4.8.** **Not an optimiser.** It sorts by cost + carbon_price × carbon and fills greedily (`v48/model.py:17-23`). It is correct only because the problem has a single separable constraint.

**V4.7.** Dynamic programming over units covered (`v47/model.py:42-56`).
- It is exact without a budget.
- With a budget, keeping only the minimum-score state per key could in theory prune a cheaper feasible path.
- Brute force over 250 budget × carbon-price cases found **0 mismatches** (`verify_v47_dp.py`).

**V5.6: does every transaction balance?** Only trivially, by construction.
- `transfer` debits and credits the same amount (`v56/model.py:19`).
- `check()` only asserts non-negative deposits and `sum(deposits) == issued` (`:27-30`).
- `issue()` creates deposits with **no liability or equity counter-entry**, although the docstring claims monetary-authority equity changes (`:2-3`, `:22-26`). The monetary authority's balance stays 0.
- There are no balance sheets and no transaction-flow matrix.
- The physical results (food, labour) are computed independently of the money flows (`:46-50`).

**V5.7.**
- The audit `assets == liabilities + equity` (`v57/model.py:94`) is **tautological**, because `sheets()` defines equity as assets − liabilities (`:79-89`).
- The substantive checks are bank equity == 0 and authority equity == 0 (`:95`). These hold by construction, since loans create equal deposits (`:29`) and advances create equal reserves (`:41`).
- There is no check that each sector's change in net worth equals its net saving plus revaluation, and no transaction-flow matrix.
- `produce()` books 200,000 U of inventory value with no counterpart payment (`:45-50`).
- `invest()` transfers cash from the investment fund to firms **and** books the same amount as firm capital. No capital-goods seller exists and no labour or materials are used (`:63-67`).
- The model is not stock-flow consistent in the Godley–Lavoie sense. The handover's own caveat ("balance-sheet identities alone ≠ macro closure") is correct.

**V5.8.** Asserts aggregate `deposits == debt` every year (`v58/model.py:83`). This is a real but single aggregate identity. The credit limit is never enforced (`:74`), and `test_credit_limit_flag` expects it to be breached.

**V5.9: is it Leontief?** **Yes, numerically.**
- `gross_requirements` solves x = f + Ax by Jacobi fixed-point iteration (`v59/model.py:29-36`). This is the Neumann series for (I − A)⁻¹f; no explicit inverse is formed. The A orientation is correct, since `INPUTS[j][s]` is the input of s per unit of j (`:33`).
- `verify_v59_leontief.py` computes the exact inverse by Gauss–Jordan elimination on Fractions and agrees to a **1.2e-14** relative difference. The maximum column sum of A is 0.21, so the system is productive.
- Investment only replaces depreciation, with no expansion investment (`:55-60`). Every demand-growth scenario therefore must end in shortage by construction.
- Rationing is a single uniform ratio across all sectors (`:48-53`). There is no monetary side despite the "investment budget U" label.

---

## Key discrepancies (ranked)

1. **3 of 14 source_tree versions (v49, v50, v53), the "exact optimisation" line, cannot run in the target stdlib environment.** Their requirements are unpinned (v53 has no requirements file). The archived numbers are nevertheless correct: an independent brute-force re-solve matches them exactly.
2. **V5.6 handover misstatement:** the 300,000 U public shortfall is present in the baseline. The "public_fund_shortage" scenario is a duplicate of the baseline because its parameter equals the default.
3. **V6.1 output contradicts a handover caveat:** the archived CSV publishes "additional workers" by scaling all 30.5m workers with the full-time 1,656h ratio, giving 6.1m. The handover explicitly says not to do this.
4. **"Every transaction balances" (V5.6/V5.7) holds only by construction.** V5.7's A = L + E audit is tautological, issuance has no counter-entry in V5.6, and V5.7 creates inventory and capital value without counterparties. This is not SFC.
5. **V5.0 and V5.3 lexicographic / stock-first and carbon-price scenarios produce identical results to cost-min** on the shipped data, so they demonstrate the mechanism, not a trade-off.
6. **Provenance gaps:**
   - V2 and V2.2 code exists only in ZIPs.
   - V3.7 and V4.2 have no package at all.
   - V6.0 "results" are index arithmetic, and its TWh anchors are unused constants.
   - `v51/build.py` hard-codes `/mnt/data` and generates its own tests.
   - The manifest does not hash the handover documents.

**What holds:** the archive is intact. Every output that can be regenerated is byte-identical. All numeric claims checked in 02 for V4.9, V5.3–V5.5, V5.7–V5.9 and V6.1 match the archived outputs. V5.9's input-output solve is a correct Leontief solution.
