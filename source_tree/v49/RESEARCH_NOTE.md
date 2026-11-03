# UNIRA V4.9 — Exact allocation and lifecycle sensitivity
**Date:** 2026-11-03 | **Status:** computational prototype; NOT city-calibrated.

## What changed
V4.8 used a greedy ranking. V4.9 uses SciPy's mixed-integer linear optimiser (HiGHS via `scipy.optimize.milp`) with integer dwelling counts, separate household cohorts (small, family, accessible), intervention capacities, consent/safety/suitability exclusions, optional budget, and a 30-year cost/carbon objective. A stock-first mode lexicographically minimises new construction before cost/carbon. Unlike a greedy method, it finds a globally optimal allocation **within this deliberately simplified linear model**, subject to solver termination status.

## Illustrative case
100 additional households (45 small, 35 family, 20 requiring accessible homes). Input interventions, capacities, costs and 30-year carbon numbers in `actions.csv` are **invented teaching inputs**, not observations for any of the five cities. Carbon values are not verified lifecycle assessments. Monetary values are hypothetical EUR per dwelling; carbon price €10,000/tCO2e is deliberately extreme to expose trade-offs, NOT a policy recommendation or market price. Reported carbon totals are 30-year illustrative tonnes CO2e, not annual rates. The model treats interventions as mutually independent and prescreened; it does not yet capture spatial matching, construction lead times, tenure, building-level interactions, embodied vs operational carbon, financing or displacement.

## Results
See `results.csv`. Differences between high-carbon-price and stock-first demonstrate that hard stock-first priority can conflict with the lowest modelled lifecycle emissions. The synthetic case also requires new accessible homes because its consented, safe existing accessible capacity is 15 for 20 households. This is an input assumption, not a finding about real accessibility shortages.

## Real-world evidence and limits
- England's 2024 English Housing Survey estimated a mean **£7,480** to improve an eligible dwelling to EPC C, which is **not** the cost of comprehensive renovation or structural repair. Official source: https://www.gov.uk/government/statistics/chapters-for-english-housing-survey-2024-to-2025-headline-findings-on-housing-quality-and-energy-efficiency
- NYC's 2023 rental vacancy rate was **1.41%**, which is **not** the fraction of housing UNIRA could recover. Official source: https://www.nyc.gov/assets/hpd/downloads/pdfs/about/2023-nychvs-selected-initial-findings.pdf
- France's RE2020 uses lifecycle approaches for new buildings. Regulatory guidance: https://www.ecologie.gouv.fr/politiques-publiques/reglementation-environnementale-re2020

These observations are background only and **do not parameterise** `actions.csv`. No comparative claim about UNIRA's actual cost, climate performance, or feasibility follows from the illustrative outputs.

## Technical cautions
- Solver status `optimal` means optimal under the supplied model, not real-world optimal.
- `stock_first` uses a bounded big-M penalty to prioritise minimising new builds; very large numerical coefficients can cause scaling problems on real datasets. A production version should use a two-pass lexicographic solve.
- The model currently meets cohort demand with integer housing units but does not assign individual households to addresses or enforce geographic proximity and preference ranking.
- High carbon price is a sensitivity experiment; no discounting or temporal carbon accounting is included.

## Research roadmap V5.0
1. Gather and archive verified Paris/London/NYC/Tokyo/Cairo metropolitan cost distributions, stock conditions, vacancy definitions and overcrowding by household size.
2. Obtain traceable LCA coefficients for retrofit, conversion and construction under a consistent 30–60 year horizon; separate embodied and operational emissions.
3. Replace prescreened cohort actions with building-to-household assignment including spatial access, affordability, consent and displacement.
4. Benchmark against **existing-policy renovation-and-construction mixes**, not a fictitious all-new-build baseline.
5. Run uncertainty distributions and publish reproducible data provenance, missingness and external validation checks.

## Run
`python -m pip install scipy numpy` then `python model.py` and `python -m unittest -v test_model.py` from this folder. Tested with SciPy 1.17.0.
