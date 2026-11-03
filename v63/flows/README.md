# UNIRA V6.3 · flows: empirical year-1 take-up of the labour reserve

V6.2 (`../../v62/src/unira_v62/labour_reserve.py`, RESEARCH_NOTE §4b–4d) sized three reserve
pools for a 30 h week: T1 = unemployed, T2 = extended labour force (seeking-not-available +
available-not-seeking), T3 = underemployed part-timers. Take-up was a SYNTHETIC parameter
(25/50/100 %). This module replaces it with the **observed share of each pool that is
employed one year later**, from Eurostat labour-market flow statistics.

Stdlib only. The V6.2 `fetch.py`/`jsonstat.py` helpers are imported via `sys.path`
(`takeup/_v62.py`) and are not copied or modified.

```
python3 run.py                          # offline: verify hashes, regenerate outputs/
python3 run.py --fetch                  # re-download snapshots (network; new hashes)
python3 -m unittest discover -s tests   # 12 tests
```

## Data (queried 2026-11-03; hashes in `data/raw/raw_manifest.csv`)

| snapshot | table | what it is | dims / units used |
|---|---|---|---|
| flows_annual | `lfsi_long_a` | **Year-on-year** ILO flows. Same quarter of two consecutive years, averaged over the 4 quarters, ages 15–74 (ESMS `lfsi_long_esms` §18) | `wstatus` UNE_EMP, INAC_EMP…; `unit` PC_UNE, PC_INAC, PC_EMP, THS_PER; `sex`=T |
| flows_quarterly | `lfsi_long_q` | Quarter-on-quarter flows, published under the final quarter | `s_adj`=NSA, `unit`=THS_PER, 9 `wstatus` cells |
| flows_inactive_attachment | `lfsi_long_e06` | Out of labour force → employment by attachment. *Experimental*: regression-based annual average of **quarterly** probabilities, integer % | `wstatus` TOTAL/SEEK_NAVL/NSEEK_AVL/OTH; `age` Y15-74, Y25-54; `unit` PC_INAC |
| flows_unemp_duration | `lfsi_long_e01` | U → E by unemployment duration (experimental, quarterly probabilities) | `duration` TOTAL/Y_LT1/Y_GE1/Y_GE2; `unit` PC_UNE |
| flows_pt_to_ft | `lfsi_long_e08` | Part-time → full-time (experimental, quarterly probabilities) | `age` Y25-64; `unit` PC |
| silc_labour_transitions | `ilc_lvhl30` | EU-SILC longitudinal: year t-1 → t. `wstatusp` = previous status, `wstatus` = current status; self-defined status | `unit` PC (row % of previous status) |
| lfs_slack_stocks | `lfsi_sla_a` | Stocks of SEEK_NAVL and NSEEK_AVL, used to weight T2 | `age` Y15-74, `unit` THS_PER |

Geography is the same as V6.2: EU27, IS, NO, CH and EU27_2020. Years: 2023 and 2024.

**Time label.** `lfsi_long_a` year *y* covers the flows (y−1) → y. ESMS says quarterly flows are
published under the final quarter. Annual 2025 values were already published in Aug-2026,
when quarterly data ended at 2026-Q2, so *y* must be the target year.

**Gaps.** `lfsi_long_a` has no data for NO and no UNE_EMP value for LU. `lfsi_long_e06`, `e01`
and `e08` have no data for LU and MT. `ilc_lvhl30` has no data for IS, and no RO 2024
PT→FT value. Some cells of `lfsi_long_q` are suppressed for HR, IS, LV, SK and MT; the
pipeline then falls back as described below. MISSING rows have an empty `takeup_rate`.

## Method, per pool (`takeup/compute.py`)

**T1 (proposed) = `lfsi_long_a` UNE_EMP / PC_UNE.** This is the published share of the
ILO-unemployed who are employed one year later. VERIFIED_OFFICIAL.

The pipeline also compounds the four NSA quarterly U/E/I matrices of `lfsi_long_q`
(built from THS_PER levels, `takeup/markov.py`) as a cross-check (MODEL_DERIVED). This
Markov chain assumes no duration dependence and homogeneous states. Real exits fall
sharply with duration: in FR 2023 the quarterly U→E rate is 32 % for spells under 1 year
and 11 % for spells of 1 year or more (`e01`). The chain therefore applies the average exit
rate to survivors who are in fact slower, and it **overstates** the annual rate. Measured
2023 bias: Markov exceeds the direct rate in 23 of 24 countries, by +0.10 on average (FR
0.499 vs 0.410). This is why the direct year-on-year table is used as the proposed value.

The SILC U→E rate is shown as a second cross-check. It is lower (FR 0.307) because it uses
self-defined status, a different concept from ILO.

**T2.** No official *annual* flow exists for the attached inactive. `e06` gives only
quarterly probabilities.
- **lower_bound** = `lfsi_long_a` INAC_EMP / PC_INAC for *all* inactive people aged 15–74
  (VERIFIED_OFFICIAL). This group includes students, retirees and people with long-term
  illness. It is a **floor** for T2, whose members want work or are available for it.
- **proposed** = q_T2 × f_U (MODEL_DERIVED).
  - q_T2 is the quarterly I→E probability of SEEK_NAVL and NSEEK_AVL (`e06`, ages 15–74),
    weighted by the `lfsi_sla_a` stocks.
  - f_U = direct annual U→E ÷ mean quarterly U→E, for the same country and year. The
    quarterly rate comes from `lfsi_long_q` levels, or from `e01` TOTAL where quarterly
    cells are suppressed.
  - Assumption: the attached inactive follow the same quarter-to-year profile as the
    unemployed, so f_U carries the observed duration-dependence damping.
  - In BG, EL and SK the result exceeds T1. The `notes` column flags these cases.
- **alternative** = annual all-inactive I→E × (q_T2 / q_TOTAL from `e06`). This assumes
  proportional scaling. It runs high, because the all-inactive annual-to-quarterly ratio
  is inflated by heterogeneity, and `e06` TOTAL is rounded to whole % (1–3 %). Use it only
  as a sensitivity check.

**T3 (proposed, PROXY) = `ilc_lvhl30` EMP_PT → EMP_FT**, year t-1 → t (VERIFIED_OFFICIAL as a
published number). No official flow exists for *underemployed* part-timers. This rate
covers all part-timers, voluntary ones included, and FT/PT is self-defined rather than
"≥ 30 h". It is probably a **lower bound** for T3: NL has 0.054 because its part-time work
is mostly voluntary. `e08` (LFS, quarterly) is reported in `summary.json` for context
only. No T3 benchmark is computed, because the proxy is dominated by composition (RO 2023
= 0.935).

**Benchmark (`geo=TOP3_MEAN`, role `benchmark`)** = the mean of the three highest country
values, excluding aggregates. It serves as an upper bound for an active mobilisation
policy.

## Results (2023; 2024 in the CSV)

| | T1 proposed | T2 proposed [lower bound · alt] | T3 proxy |
|---|---|---|---|
| FR | 0.410 | 0.253 [0.082 · 0.452] | 0.231 |
| EU27 | 0.362 | 0.231 [0.084 · 0.319] | 0.198 |
| Top-3 benchmark | 0.612 (IS, NL, DK) | 0.361 (IS, HU, DK) | not computed |

2024: FR 0.413 / 0.243 / 0.222; EU27 0.368 / 0.219 / 0.180; benchmark T1 0.605, T2 0.398.

## Caveats (read before using in V6.2)

1. **These are status-quo baselines, not policy effects.** The flows include normal churn:
   people who would have found a job anyway, without UNIRA. A take-up of 41 % does not
   mean a mobilisation policy adds 41 % of T1 to employment. The policy effect is the
   increment above this baseline, and it is not estimated here. The flows also run both
   ways: E→U and E→I outflows refill the pools every year.
2. Ages are 15–74 for all LFS flows, while the V6.2 pools cover ages 20–64. `e06` Y25-54 is
   in the snapshot for sensitivity work.
3. The tables measure status at one point, one year later, so intermediate spells are
   missed. They also say nothing about hours, sector or location of the job, or whether
   it is 30 h.
4. The `e0x` tables are experimental, regression-based and rounded to whole %.
5. The benchmark countries reflect their own composition and institutions, for example
   high turnover. Their rates are not evidence that a policy can be transplanted.

## Integration interface

`outputs/takeup_rates.csv` columns:
- `geo`, `year`
- `pool` (T1/T2/T3)
- `takeup_rate` (0..1, empty = MISSING)
- `method`, `source_dataset`
- `evidence_class` (VERIFIED_OFFICIAL / MODEL_DERIVED / MISSING)
- `notes`
- `role` (proposed / lower_bound / alternative / cross_check / benchmark). This is a
  trailing extra column. Filter on `role == "proposed"` for one value per geo, year and
  pool.

```python
sys.path.insert(0, "<UNIRA>/v63/flows")
from takeup.api import get_takeup, load_takeup
get_takeup("FR", 2023, "T1")                         # 0.41
get_takeup("FR", 2023, "T2", role="lower_bound")     # 0.082
get_takeup("TOP3_MEAN", 2023, "T1", role="benchmark")  # 0.612
```

In V6.2, persons mobilised = Σ_pool takeup_pool × pool size. Do not apply a T1/T2 rate to
the BENCH employment-gap framing: that gap is not a flow pool.
