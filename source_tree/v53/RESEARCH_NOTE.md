# UNIRA V5.3 — Housing Needs, Intervention Costs and Feasibility
Date: 2026-11-03
Status: **Computational prototype; not an empirically calibrated urban forecast**.

## Objective
Determine whether a needs-based housing planner can explicitly satisfy household demand, prioritize existing stock, stay within a budget and expose unmet need. Compare the outcomes of cost-minimization, a carbon price and stock-first policy. This is **not** yet a test of whether UNIRA beats real housing policies.

## Official evidence and limits

1. **England, English Housing Survey 2024 (published 2026):** Mean modelled energy-efficiency upgrade cost to band C among eligible dwellings: **£7,480**; median **£8,648**. Among F/G-rated homes the mean was **£17,354**. These estimates exclude comprehensive rehabilitation, structural repair and conversion. England is **not Greater London**.
   Source: https://www.gov.uk/government/statistics/chapters-for-english-housing-survey-2024-to-2025-headline-findings-on-housing-quality-and-energy-efficiency/chapter-2-energy-efficiency
2. **France, government residential-renovation monitoring:** Average works cost for MaPrimeRénov' single-measure aided renovations in 2023 approximately **€12,000**; programme participants are not representative of whole-building deep renovations, and this figure must not be extrapolated to Paris conversions.
   Source: https://www.statistiques.developpement-durable.gouv.fr/tableau-de-suivi-de-la-renovation-energetique-dans-le-secteur-residentiel
3. **New York City, 2023 Housing and Vacancy Survey:** **1.41% net rental vacancy**; **33,210 units available for rent**. Market vacancy is not the same as legally recoverable unused housing. NYC official city geography, not the metropolitan statistical area.
   Source: https://www.nyc.gov/content/tenantprotection/pages/fast-facts-about-housing-in-nyc
4. **France, ADEME Perf in Mind 2:** Measured renovation performance data and lifecycle assessment are available; programme-specific findings must not be generalized to all urban buildings.
   Source: https://data.ademe.fr/datasets/pim2

## Model formulation
Integer decision variable x_i for number of households accommodated by intervention i, plus unmet demand u. Constraints: sum(x_i)+u = demand; 0<=x_i<=capacity_i; sum(cost_i*x_i)<=budget. Objective: minimize cost + carbon_price*carbon + large explicit penalty for unmet needs. The stock-first scenario solves a first-stage integer program to minimize new construction subject to zero unmet need and budget, if feasible, then optimizes cost within that new-build cap. When zero unmet need is infeasible it falls back to a model that reports unmet need.

All costs and carbon factors in model.py are **invented illustrative coefficients** in EUR and tCO2e per intervention over an assumed 30-year comparison period. They are not estimates for Paris, London, New York, Tokyo or Cairo. The emissions inputs are not derived from an ISO-compliant LCA. Carbon prices are scenario levers, not market observations. The 1e9 EUR unmet penalty is a modelling priority, not a real social cost.

## Main scenarios
See `results.csv` and `results.json`. For 100 households and EUR18m budget, 20 repair/adapt + 35 deep renovation + 25 conversion + 20 new-build = 100 households, EUR14.6m, 3280 illustrative tCO2e. Under EUR8m, 26 households remain unserved. The EUR200/t carbon-price case has the same allocation because, in this dataset, existing interventions are both cheaper and lower-carbon. This agreement is a consequence of **assumptions**, not proof of a general law.

## Model limitations / research audit
- No household-to-unit matching by bedrooms, neighborhood, transit, accessibility, tenure, safety, consent or preference. Intervention eligibility is assumed pre-screened, **not actually checked**.
- No empirical city-level intervention capacity, housing-need counts, cost distributions or lifecycle factors.
- No financing cost, displacement during renovation, construction workforce capacity, material constraints, operational energy modelling, climate adaptation or uncertainty intervals.
- The same hypothetical household is counted once; real households are not represented individually.
- Comparison with current policy is not valid until the same budgets, constraints and measured input distributions are used.
- Cairo remains a data gap; do not fabricate metropolitan figures.

## Next milestone (V5.4)
Acquire geographically matched city datasets, source building condition and renovation unit costs, construct household-by-building suitability constraints, incorporate carbon uncertainty ranges, and define realistic policy comparator scenarios. Independent reproducibility review should follow.

## Reproduction
`pip install scipy numpy` then `python model.py` and `python -m unittest -v test_model.py`.
