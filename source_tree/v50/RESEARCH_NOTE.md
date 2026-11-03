# UNIRA V5.0 — Reproducible allocation and calibration-readiness audit
Date: 2026-11-03. Status: **NOT empirically calibrated**.

## Scope and methodological advance
This release replaces V4.9's large-M stock-first objective with a **two-pass exact lexicographic mixed-integer optimisation**: first minimise new construction, then minimise financial cost plus an optional carbon penalty, subject to the minimum achievable new-build count. This avoids numerical instability from arbitrary huge penalties. It also requires *exact* cohort demand, rather than permitting surplus dwellings to be allocated without demand. Seven unit tests cover consent, infeasibility, demand, budget, lexicographic consistency and carbon sensitivity.

## Baseline synthetic results
See `results.csv`: 100 households, including 20 requiring accessible housing. Cost-minimum and stock-first both choose 5 new dwellings at €8.565 million and 4,416 synthetic 30-year tonnes CO2e. The carbon price of €1,000/t does not change that allocation. Higher assumed operational emissions change the optimal mix and calculated emissions. These outputs are NOT findings about any real city.

## Important new limitation made explicit
`actions.csv` comes from the synthetic V4.9 case. Neither monetary amounts nor lifecycle carbon coefficients are derived from actual housing interventions in Paris, London, New York, Tokyo or Cairo. The 60% operational-carbon share and the 0.5–1.5 scaling scenarios are **invented sensitivities**. Do not interpret the resulting 30-year carbon as a genuine LCA; changing operational carbon uniformly across all intervention types is a crude stress test, not a grid-decarbonisation projection.

## Official evidence registry (background; not calibration)
- INSEE Paris housing census: https://www.insee.fr/fr/statistiques/2011101?geo=DEP-75 (administrative Paris, not metropolitan area; verify census year and table before extraction).
- London Assembly, empty homes: https://www.london.gov.uk/who-we-are/what-london-assembly-does/london-assembly-research-unit-publications/empty-homes-london (administrative and tax definitions, not directly comparable with census vacancy).
- NYC 2023 Housing and Vacancy Survey: https://www.nyc.gov/assets/hpd/downloads/pdfs/about/2023-nychvs-selected-initial-findings.pdf (rental vacancy, not recoverable housing stock).
- English Housing Survey 2024–25: https://www.gov.uk/government/statistics/chapters-for-english-housing-survey-2024-to-2025-headline-findings-on-housing-quality-and-energy-efficiency (England national retrofit cost proxy, NOT a London building renovation cost).
- Japan Statistics Bureau housing survey: https://www.stat.go.jp/english/info/news/20241030.html (national stock figures, NOT Tokyo-specific).
- French RE2020: https://www.ecologie.gouv.fr/politiques-publiques/reglementation-environnementale-re2020 (LCA methodology, NOT intervention-specific carbon factors).

## Evidence gaps that block claims of real-world superiority
1. Harmonised metropolitan boundaries and household cohorts for all five cities; Cairo and Tokyo city-level inputs remain absent.
2. Building-level condition, structural safety, tenure, consent, size, accessibility, vacancy duration and spatial match.
3. Real distributions of repair/retrofit/conversion/new-build costs (same currency-year and scope) with sources and sample sizes.
4. Comparable embodied and operational carbon estimates with functional unit, service life, energy grid and uncertainty.
5. Existing-policy counterfactual (current reuse/retrofit/new-build programmes), displacement and equity assessment.
6. Financing, implementation lead time, workforce and supply-chain capacity.

## Research integrity
This version is a **computational-method milestone**, not an empirical calibration milestone. No city-level savings, construction avoidance or emission reductions have been established. Future work must archive raw official datasets with licensing, retrieval dates, geographic definitions and transformation scripts; verify source coverage before publishing a comparative paper.

## Reproduce
Install `numpy` and `scipy` (tested with SciPy 1.17.0), then `python model.py` and `python -m unittest -v test_model.py`.
