# UNIRA V4.8 — First evidence-linked housing calibration audit
Date: 2026-11-03

## Status
This release adds sourced observations to a transparent prototype. It is **not** a city-calibrated optimisation or evidence of UNIRA's superiority. The model's intervention capacity, per-unit cost, and lifecycle emissions are **entirely synthetic** and deliberately not derived from the observed housing indicators.

## Empirical observations
See `calibration.csv` for units, dates, geography and primary sources. England 2024: mean £7,480 per eligible home to reach EPC C; 56% of stock already EPC A–C; 42% potentially upgradeable to C. These are national English Housing Survey figures, **not London estimates**. ONS London EPC median score 70 (certificate sample, not full stock). NYC 2023 rental vacancy 1.41%, 33,210 available rental units; **not** an estimate of recoverable homes.

## Model methodology
`model.py` is a deterministic greedy allocation screen. It orders interventions by (illustrative cost + carbon price × illustrative tCO2e) and fills hypothetical capacities until demand is met. It excludes unsafe or nonconsensual interventions. This is NOT globally optimal when unit costs differ, capacities are indivisible, spatial matching matters, or options interact. Its output is a pedagogical sensitivity analysis, not city outcomes. Costs use unspecified synthetic currency units; carbon values are synthetic tonnes CO2e per dwelling over an unspecified horizon, so they must not be interpreted as real lifecycle assessment.

## Key finding
The sourced England mean upgrade cost (£7,480) cannot legitimately replace a comprehensive renovation or conversion cost (£35,000/£85,000 synthetic) because the scopes differ. Nor can a London EPC median be extrapolated into numbers of suitable vacant homes. Cross-city comparison requires harmonised boundaries, definitions, stock quality, household needs, consent and tenure, cost distributions and consistent 30–60-year life-cycle inventories.

## Next empirical tasks
1. Retrieve London-specific dwelling/retrofit cost distributions and sample weights.
2. Obtain NYC building-condition and household crowding survey cross-tabs.
3. Obtain Paris local housing DPE distributions with coverage bias checks.
4. Verify Tokyo and Cairo metropolitan housing-stock sources and definitions.
5. Source embodied and operational carbon factors by building typology, climate, grid, and retrofit depth.
6. Implement exact mixed-integer allocation with spatial matching, accessibility and household preferences, and compare against current-policy baseline.

## Reproduce
`python model.py` then `python -m unittest test_model.py` from this directory. Standard library only.
