# UNIRA V2.1 — Evidence baseline and model audit
**Date:** 2026-11-03  
**Status:** Exploratory research / not peer reviewed.

## Research question
Can a democratically governed global economy provide adequate material living standards for all with a 30-hour working week while respecting resource and ecological constraints?

## Evidence ledger
| Indicator | Value | Reference period | Classification | Source |
|---|---|---|---|---|
| Global employment | 3,544.8 million | 2025 | ILO projection published in WESO Trends 2024, not an observed headcount | [ILO report](https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@dgreports/@inst/documents/publication/wcms_908142.pdf), Appendix C Table C1 |
| Global food supply | >3,000 kcal/person/day | 2023 | FAO reported food availability, not consumption | [FAO 2025 release](https://www.fao.org/statistics/highlights-archive/highlights-detail/food-balance-sheets-2010-2023/) |
| Global electricity generation growth | >1,200 TWh | 2024 | IEA reported year-over-year increase, **not total generation** | [IEA 2025 review](https://www.iea.org/reports/global-energy-review-2025/electricity) |
| UNIRA working adults | 4.35 billion | scenario | Unverified planning assumption | UNIRA V2 |
| UNIRA workweek | 30 hours | scenario | Proposed policy | UNIRA constitution |
| Existing average weekly hours | 43 hours | scenario | Placeholder; **not verified as a global mean** | Prior UNIRA assumption |
| Illustrative food target | 2,500 kcal/person/day | scenario | Model assumption only; actual needs vary with age, activity and health | UNIRA planning assumption |

## Audited results
Using 3.5448 billion employed (ILO 2025 projection) and **assuming** 43 hours per week gives 152.4264 billion hours/week. With 4.35 billion UNIRA workers at 30 hours, UNIRA supplies 130.5 billion hours/week. This is 14.38% fewer hours, and would require a 16.80% average output-per-hour increase to preserve equal aggregate output *if* hours were perfectly substitutable and output mix unchanged. These are conditional arithmetic results, not feasibility findings.

Earlier UNIRA versions compared 130.5 with 154.8 billion hours and estimated an 18.6% required productivity increase. That result depended on a different, rounded employment baseline and must not be treated as an empirical estimate.

FAO's >3,000 kcal/person/day in 2023 does not imply that all individuals have enough to eat. The 3,000 kcal figure is a conservative lower bound for reported average availability; distribution, diet quality, loss, waste and local shortages are unresolved. In a stylized 20% uniform supply shock, the floor would become 2,400 kcal/person/day, below an illustrative 2,500 target. This is not a realistic forecast of a particular crisis.

## Essential limitations
1. Labour: age, disability, unpaid care, education, retirement, training, migration, sector-specific skills and actual hours require regional datasets.
2. Food: model edible availability by commodity, nutrition, climate, land, trade and regional access; do not equate average calories with food security.
3. Electricity: the cited 1,200 TWh is **growth**, not annual production. A credible supply-demand simulation requires verified generation, end-use consumption, losses, grids and dispatchability.
4. Housing: separate new household formation, existing deficit, maintenance, materials, land, infrastructure and skilled labour.
5. Finance: salary totals in U are accounting identities, not evidence of purchasing power or affordability. Household child-allowance eligibility needs a synthetic household population or microdata.
6. Governance: regional autonomy, individual rights, allocation mechanisms, corruption risks and failure recovery remain open design questions.
7. Ecological constraints: emissions, land use, biodiversity, water stress and material throughput need independently sourced limits.

## Next development stage (V2.2)
- Build a country-year indicator registry with source, unit, observed/projection status, uncertainty and download date.
- Build a multi-regional input-output material and energy balance model.
- Include reserve capacity and disruption scenarios, not just global totals.
- Calibrate workforce and households with age distributions and sectoral employment.
- Publish reproducible notebooks, uncertainty intervals and counterfactual comparisons.

## Reproducibility
Run `python unira_v21.py`. It generates `UNIRA_V21_scenarios.csv` and `UNIRA_V21_results.json` using Python's standard library. No live data are fetched; all external figures are documented above.
