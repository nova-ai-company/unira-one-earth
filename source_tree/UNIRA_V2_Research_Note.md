# UNIRA V2 — Preliminary Global Resource Stress Test
**Date:** 3 November 2026  
**Status:** Exploratory working paper; not peer-reviewed; not a demonstrated feasibility assessment.

## Executive finding
A 30-hour working week and universal material security cannot yet be certified as feasible. Under illustrative inputs, weekly labour supply is 130.5 billion hours versus a 154.8-billion-hour comparator; **18.6% greater output per hour** would be required to match the comparator's aggregate output, assuming skills and sector allocation were interchangeable (they are not). A hypothetical 20% productivity improvement crosses this *aggregate* parity threshold but does not resolve sector shortages.

The initial food and electricity assumptions deliberately produce shortfalls, showing why global averages and financial balances cannot establish feasibility. This is a diagnostic exercise, not evidence that UNIRA would produce these shortages.

## Model boundaries
- Population 8.2bn; adults 5.8bn; children 2.4bn; 75% of adults working: **planning assumptions**, not a verified age or ability-to-work census.
- 30h/week, 5,000 U monthly base salary, 25,000 U individual maximum, 5,000 U medical inability guarantee, 1,000 U per child subject to the 15,000 U adult-income-plus-child-allowance threshold: **UNIRA policy proposals**.
- Food benchmark 3,000 kcal/person/day, 20% assumed losses, target 2,500 kcal/person/day: **illustrative physical proxy**, not a complete nutrition, production or access model.
- Electricity 30,000 TWh/year, 4,000 kWh/person/year service target: **rounded assumptions**, not a measured requirement. Supply, generation, consumption and transmission losses are different quantities.
- Housing initial shortfall 288m units and programme of 20m/year for 15 years: **unvalidated planning proxy**; excludes demolitions, new households, location and affordability. Housing output minus the initial deficit is *not* a true housing surplus.
- Labour comparator 3.6bn workers × 43 hours: **prior UNIRA modelling baseline**, not newly verified from an ILO dataset.

## Scenario outputs
| Scenario | Labour output index vs comparator | Usable food kcal / target | Electricity balance (TWh/y) | Construction minus initial housing gap (m units) |
|---|---:|---:|---:|---:|
| Base assumptions | 0.843 | 0.960 | -2,800 | +12 |
| 20% reduction in food supply | 0.843 | 0.768 | -2,800 | +12 |
| 15% electricity supply disruption | 0.843 | 0.960 | -7,300 | +12 |
| 20% labour productivity gain | 1.012 | 0.960 | -2,800 | +12 |
| 10% population growth (supply per capita held constant for food) | 0.927 | 0.960 | -6,080 | +12 |

**Important caveat:** In the population-growth scenario, the food supply assumption is specified *per person*, so food supply grows automatically with population; this is a sensitivity convention, not a realistic fixed-capacity stress test. Future versions must use absolute regional production capacities. The housing result is unchanged because housing supply and initial deficit are held fixed, which is also not a realistic population-growth treatment.

## Preliminary observations
1. **Labour:** aggregate working time falls 15.7%. Achieving unchanged total output requires a productivity multiplier of 1.186; sector-specific constraints are still unmodelled.
2. **Food:** 3,000 × (1−0.20) = 2,400 usable kcal/person/day, below the hypothetical 2,500 target. Nutrition depends on diet composition, distribution, accessibility, waste and local conditions—not calories alone.
3. **Electricity:** the hypothetical 30,000 TWh supply falls short of a 32,800 TWh target. This does not demonstrate actual electricity scarcity because neither value is a calibrated UNIRA demand/supply estimate.
4. **Housing:** 300m units built over 15 years exceeds a static 288m-unit shortfall by 12m, **but this is not a housing feasibility result** because replacement, infrastructure, labour, location, household growth and materials are missing.
5. **Money:** wage and benefit totals are nominal UNIRA accounting entries. No exchange rate, monetary purchasing power or public-fund solvency can be inferred without physical supply, fiscal accounts and household distribution.

## Empirical anchors identified for calibration
- FAO, *The State of Food Security and Nutrition in the World 2026*: 645 million people estimated undernourished in 2025; 2.1 billion moderately or severely food insecure. https://www.fao.org/hunger/en
- IEA, *Global Energy Review 2025 — Electricity*: global electricity generation increased by over 1,200 TWh in 2024; renewables and nuclear contributed over 80% of growth. https://www.iea.org/reports/global-energy-review-2025/electricity

These two sources are **contextual reference points only**; they do not validate the numerical proxies in the V2 engine.

## Essential next work (V2.1)
1. Assemble an auditable data dictionary with year, geography, units, source and uncertainty for UN population, ILO labour, FAOSTAT production and nutrition, IEA energy, UN-Habitat housing, WHO health and UNESCO education.
2. Replace per-capita global supply assumptions with **absolute regional production**, trade/logistics constraints and inventories.
3. Build a multi-sector input–output model with skills, materials, energy and transport constraints.
4. Estimate household composition to calculate *actual* child allowances, and distinguish medical benefits from worker payroll.
5. Design a democratic decision and incentive mechanism; explicitly test rationing, corruption, institutional capture and rights protections.
6. Publish baseline-versus-UNIRA comparisons with uncertainty bands, not point estimates alone.

## Research integrity
UNIRA is a normative proposal under investigation. No result in this report proves it is economically, politically or environmentally feasible. Negative and inconclusive findings must be published alongside positive findings.
