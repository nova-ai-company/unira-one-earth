# UNIRA V2.2 — Multi-region, multi-sector input-output prototype

**Status:** Methodological prototype; **not** a calibrated global economic forecast. Prepared 3 November 2026.

## Research question
Can a globally coordinated allocation system satisfy final needs when production itself consumes other industries' outputs, and what happens under regional supply or labour disruptions?

## Model
Three synthetic regions (A/B/C), four sectors (food, energy, materials, housing). `unira_v22.py` contains every assumption and implements the static Leontief input-output relation `x = (I-A)^(-1)y`, where `y` is final demand, `A` is the input coefficient matrix and `x` is required gross output. It compares gross output to aggregate sector capacity and allocates output proportionally to regional capacities, then checks synthetic regional labour budgets. This is a feasibility **screen**, not an optimal allocation solver. All numerical units are arbitrary annual units.

## Findings from synthetic scenarios

- Baseline final demand: food 90, energy 65, materials 45, housing 40.
- Required gross output, including intermediate inputs: food **106.377**, energy **113.640**, materials **88.773**, housing **45.336**. Gross production exceeds final demand because industries use one another's products.
- A **70% loss of energy capacity in region A** produces an aggregate energy capacity shortfall of **14.140** synthetic output units, despite possible cross-region redistribution.
- **25% greater final housing demand** increases gross materials requirement to **93.283** (from 88.773) and energy to **116.602** (from 113.640).
- **40% less regional labour availability** causes labour budget overruns in all three regions under proportional allocation. A different regional allocation might improve results; no optimisation has been performed.
- **20% improvement in energy-sector labour efficiency** reduces energy labour inputs, but does not change physical energy demand or gross output in this simplified setup.

## Critical limitations

1. **Every coefficient, demand, regional capacity and labour budget is synthetic**. These results must not be presented as estimates of real-world shortages or proof of UNIRA feasibility.
2. Regional trade and transport capacity, costs, distance, storage and losses are absent.
3. No country-level data, skills, capital investment, land, water, greenhouse gas or biodiversity limits.
4. Fixed input coefficients ignore substitution, learning, technical innovation and price responses.
5. The proportional regional assignment is not an optimisation; it can miss feasible reallocations.
6. No dynamic inventories, recovery, adaptation, governance, incentives or monetary accounting.
7. The model's labour budgets are unrelated to UNIRA's proposed 30-hour workweek until demographic and occupational data are connected.

## Next stage — V2.3

- Build a documented data dictionary and source register using FAOSTAT, IEA, ILOSTAT, UN population projections, UN-Habitat and multi-regional input-output tables (OECD ICIO, EXIOBASE or Eora subject to availability/licensing).
- Normalize units, years, sector definitions and regional coverage; explicitly track missing data and uncertainty.
- Replace synthetic coefficients and capacities with observed input-output tables; separate food calories/nutrition, TWh, tonnes, homes and worker-hours.
- Solve a constrained allocation problem with transport, labour and environmental ceilings; compare UNIRA against a non-UNIRA baseline.
- Publish scenario ranges, not a single deterministic success claim.

## How to reproduce

Run `python unira_v22.py` using Python 3. It generates `UNIRA_V22_results.json` and `UNIRA_V22_scenarios.csv` alongside the script.
