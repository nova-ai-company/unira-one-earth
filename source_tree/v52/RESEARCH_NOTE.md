# UNIRA V5.2 — Housing Need, Quality, and Recoverability
Date: 2026-11-03. Research stage: evidence registry plus transparent *illustrative* scenarios, NOT city-level calibration.

## Major result
Vacancy counts alone cannot identify housing need. Overcrowding provides a complementary metric, but occupancy definitions and geographic boundaries differ. This release adds official overcrowding measures to the five-city research agenda and tests a non-double-counting intervention accounting framework.

## Official observations
- **Paris municipality (INSEE, 2023):** 28.2% moderately overcrowded and 2.6% severely overcrowded according to the INSEE population-of-dwellings index. The published categories are mutually exclusive. This is *not* a count of households in need of a new home; renovation or in-place adaptation may resolve some problems.
- **Paris urban unit (INSEE, 2022):** 19.8% moderately overcrowded, 2.9% severely overcrowded. This is a different geography and year, not a time series with the municipality.
- **Greater London (GLA Housing in London 2025 report):** 6.7% of households overcrowded in 2023–24 according to the UK bedroom standard; a three-year rolling estimate, possibly understated because of pandemic survey disruption.
- **England (EHS 2024–25):** 3% overcrowded; this is a national comparator, not a London figure.
- **New York, Tokyo, Cairo:** comparable, definition-checked overcrowding indicators not verified in this release. No invented values.

## Model
The screening algorithm assigns each hypothetical household in need to at most one outcome: voluntary rehousing, suitable in-place upgrade, suitable new dwelling, or unresolved need. It is a transparent *accounting identity*, not an optimisation algorithm. Inputs are fictional counts of households; scenario outputs must NOT be extrapolated to any of the five cities.

## Why comparisons are restricted
INSEE's occupation index and the UK's bedroom standard do not measure exactly the same condition. Administrative vacancy, rental availability, overcrowding, homelessness, structural fitness and energy performance require separate denominators. City boundaries must be explicit. A vacant dwelling cannot be considered recoverable without tenure, condition, size, location, consent, costs and legal availability.

## Missing empirical inputs and next tests
1. New York: source and extract 2023 NYCHVS overcrowding by tenure and household type; document precise definition.
2. Tokyo: official metropolitan household crowding / minimum housing-area standards; obtain municipality or metropolitan tables and translations.
3. Cairo: obtain CAPMAS governorate-level 2017/2027 housing/occupancy tables and document formal/informal housing coverage. Do not substitute nationwide figures.
4. Each city: estimate *unique households* needing interventions, excluding double counting across overcrowding, homelessness and unsafe housing.
5. Link dwelling inventories to physical inspections, willingness/consent, renovation/energy costs, lifecycle embodied and operational carbon, and location-specific household needs.
6. Test baseline real-world policy against UNIRA under identical constraints; preregister welfare and environmental outcome metrics and uncertainty intervals.

## Governance and rights
No compulsory displacement or appropriation inferred from under-occupation or vacancy. Preferences, legal rights, accessibility, thermal comfort and safe living space are hard constraints. Unmet need must remain visible, not hidden by forced or inadequate allocation.

## Source URLs
- INSEE Paris 2023: https://www.insee.fr/fr/statistiques/2011101?geo=COM-75056
- INSEE Paris urban unit 2022: https://www.insee.fr/fr/statistiques/8581193?geo=UU2020-00851
- Greater London Authority Housing in London 2025: https://www.london.gov.uk/sites/default/files/2026-01/Housing%20in%20London%202025%20report%20%28002%29.pdf
- English Housing Survey: https://www.gov.uk/government/statistics/chapters-for-english-housing-survey-2024-to-2025-headline-findings-on-housing-quality-and-energy-efficiency/chapter-1-housing-quality
