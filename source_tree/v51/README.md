# UNIRA V5.1 — Metropolitan Housing Evidence Registry

## Research advancement
Five-city framework: **Paris, Greater London, New York City, Tokyo Metropolis, Cairo**. Four have verified city/region-specific housing indicators; Cairo remains explicitly missing. This is not a harmonized vacancy dataset and is not empirical calibration of intervention costs or carbon.

### Important improvements
* Tokyo now has verified metropolitan data: **896,500** vacant dwellings (2023), including **629,000** rental vacancies, **43,800** sale vacancies, **9,600** second homes, **214,200** other vacancies. Total components sum to 896,600 owing to source rounding. Do not sum as if exact. Tokyo source also gives **105,000** vacancies with damage/deterioration, but this does not establish structural suitability.
* London 2025: **105,138** empty homes; **47,287** long-term empty homes, a subset. Do not add.
* Paris 2022: **136,957** census vacant homes; **136,693** secondary/occasional, separate categories.
* NYC 2023: **33,210** rental units available; vacancy rate **1.41%**. Ordinary market turnover, not an idle-housing recovery pool.
* Cairo: **missing**. A country-level figure would be misleading.

### Comparability and research design
City boundaries differ; indicators measure different concepts, surveys/administrative records differ and years vary. **No cross-city ranking of 'wasted homes' is defensible.** Screening scenarios (5/15/30%) are arbitrary sensitivity calculations only, applied to different proxy stocks; never sum or treat as projections.

### Housing optimisation specification
For each building and household category, gather verified: legal status/consent, dwelling size, accessibility, location/travel time, structural condition, renovation scope, local construction/retrofit costs, embodied carbon and operating-energy baseline, life-cycle horizon, household preferences and actual unmet need. Build feasible matches; solve integer optimisation for quality-constrained minimum lifecycle cost/carbon; compare with realistic existing-policy counterfactual; run uncertainty analysis.

### Next research tasks
1. Obtain CAPMAS Cairo Governorate and Greater Cairo housing census tables, definitions and dates.
2. Obtain comparable subregional building condition, household crowding and energy-performance data for all five.
3. Acquire audited local unit costs and lifecycle carbon factors; do not import England-wide costs into other cities without explicit transfer modelling.
4. Publish dataset version, provenance, transformation scripts and uncertainty intervals.

### Source URLs
See `city_evidence.csv`; all primary governmental/municipal sources. Source years are data reference years, not publication years.
