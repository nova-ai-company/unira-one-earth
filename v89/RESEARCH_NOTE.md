# UNIRA V8.9 — how quickly can every person have a genuinely comfortable life?

**Question (author):** how quickly can UNIRA provide every person on Earth with a genuinely comfortable life (Article 10c), using existing resources first (Article 10e), delivering essential infrastructure first, and minimising unnecessary human labour? The constitutional standards are unchanged. Where a target looks unreachable, the limitation is reported rather than the definition weakened.

## Method (`integrated/simulate.py`)

- **Coverage per country and per year,** for 80 years, in every domain:
  - water, sanitation, clean cooking, electricity, Internet, secondary school;
  - teachers, health workers, housing, energy, food, goods;
  - local services (savings, leisure, holidays, restaurants, culture);
  - shared car access.
- **One consistent set of assumptions per scenario** across all sectors:
  - delivery pace as a percentile of countries' real historical gains (median / top quarter / top tenth);
  - programme scale 1× / 2× / 3×;
  - clean-energy build 0.67 / 1.2 / 1.8 TW-equivalent;
  - training plans low / central / high;
  - building growth 0 / 5 / 10% a year;
  - automation reaching 15 / 35 / 60% of each sector's potential by year 30, speeding construction, training and services, but never energy or materials.
- **Existing assets first:**
  - broken water points restored before building;
  - goods shared by quotas from what exists;
  - redistribution of food in year 1;
  - stock-first housing (v70).
- **Delivery, not construction:** newly built water, sanitation and cooking services count only while they work. At first 90–95% work; with maintenance funded for the whole life (Article 10e) this rises to 99% over 15 years (assumption).
- **Regional constraints:**
  - conflict halves delivery and fragility cuts it by a quarter, for all 80 years (World Bank FY26 list). Conflict is not assumed to end;
  - training lead times (v66);
  - building capacity (v70);
  - local services grow with catch-up (v85 real capacities).
- **Counting people:** a person has a level only if they have every domain in it (each country's smallest coverage).
- **No double counting:** the labour to operate water, sewer and energy systems is already in the basket hours (v87). Only the construction of new essential infrastructure is added (v88).
- **Reproducibility:** two complete runs give byte-identical results (tested).

## Results: share of humanity with each level

| scenario | Level 1: 90% / 95% / 99% | Level 2: 90% / 95% / 99% | Level 1 at yr 20 / 40 / 80 | Level 2 at yr 20 / 40 / 60 / 80 |
|---|---|---|---|---|
| conservative | year 39 / – / – | – / – / – | 86% / 90% / 94% | 12% / 14% / 49% / 76% |
| moderate | year 25 / 43 / – | – / – / – | 88% / 94% / 99% | 14% / 49% / 84% / 89% |
| **accelerated** | **year 17 / 29 / 53** | **year 69 / – / –** | 92% / 98% / 100% | 20% / 83% / 89% / 93% |
| *comparison only: accelerated if conflicts end* | *year 14 / 21 / 32* | *year 44 / 51 / 57* | *95% / 100% / 100%* | *20% / 88% / 100% / 100%* |

"–" means not reached within 80 years.

## The critical bottleneck, year by year

| scenario | years 1–5/8 | then | later | Level 2 |
|---|---|---|---|---|
| conservative | health workers: **labour (training)** | clean cooking: **logistics** (fuel and stove supply chains), from year 8 | clean cooking in conflict states: **conflict**, from year 14 | local services |
| moderate | health workers: **labour (training)** | clean cooking: **logistics**, from year 6 | clean cooking, then sanitation, in conflict states: **conflict**, from year 11 | local services in conflict states |
| accelerated | health workers: **labour (training)** | clean cooking: **logistics**, from year 5 | clean cooking, then sanitation: **conflict**, from year 8 | local services in conflict states: **conflict**, from year 53 |
| if conflicts end | health workers: **labour (training)** | clean cooking: **logistics**, from year 5 | sanitation: **institutions**, from year 28 | local services: **labour**, from year 32; then teachers: **labour (training)** |

**Never the binding constraint:** energy, materials and money. Energy for the comfortable level in 2050 is 378 EJ, below today's 409 EJ. Essential infrastructure construction costs USD 9–16 bn a year (decentralised) and needs about 0.5–0.9 m workers.

## Remaining shortages after 80 years (people short, millions)

| scenario | Level 1 | Level 2 |
|---|---|---|
| conservative | clean cooking 419, sanitation 240, secondary school 156, water 57, electricity 52 | local services 1,747, safe water 601 |
| moderate | sanitation 86, clean cooking 85, water 26, secondary school 9 | local services 903, safe water 207 |
| accelerated | none | local services 584 (98% of them in conflict states), safe water 37 |
| if conflicts end | none | none |

## Resources and working hours

**Working hours for the comfortable basket**, per worker per week, at France's productivity (a lower bound; see v87):

| scenario | year 0 | year 30 | year 60 |
|---|---|---|---|
| conservative | 13.6 | 12.3 | 11.5 |
| moderate | 13.6 | 11.3 | 9.6 |
| accelerated | 13.6 | 10.1 | 8.1 |

**Building new essential infrastructure** (water, sanitation, clean cooking): USD 8.6 / 12.8 / 15.5 bn a year and 0.47 / 0.86 m workers (conservative / accelerated), less than 0.02% of world output.

**Environment:**
- energy is within today's use (378 EJ in 2050);
- clean cooking adds about 1 EJ;
- housing must be low-carbon (v70);
- holidays mainly by rail (v87);
- energy, materials and land are never the binding limit in any scenario.

## Findings

1. **Essential security for 90% of humanity in about 17–25 years, and for 95% in about 29–43 years** (accelerated / moderate). The plan-built domains (energy, housing, health, food, goods) arrive early. The slow part is household services (clean cooking, sanitation, water) where delivery capacity and security are weakest.
2. **A comfortable life for 90% of humanity is reached only in the accelerated scenario, in year 69.** 95% and 99% are not reached within 80 years while today's conflicts continue. **If conflicts end, the dates fall sharply:** Level 1 for 99% in year 32, and Level 2 for 90/95/99% in years 44/51/57.
3. **Conflict is the single largest barrier.** From about year 10, most of the people still short live in states affected by conflict. In the end almost all of them do. Resources are not the limit: energy, materials and money never bind.
4. **Early on, the bottleneck is people, not things:** training health workers in the first years, then the supply chains for clean cooking. UNIRA should allocate first to health training and to clean-cooking supply (stoves, LPG or electricity, distribution), then to safe access and local institutions in conflict regions.
5. **For Level 2, the long-run limit is building local services:** the trained people and facilities for care, transport, shops, culture and leisure in the poorest regions.
6. **Automation helps but does not remove these limits.** It shortens hours (13.6 → 8–10 h per worker per week by year 60) and speeds construction and services, but it cannot train enough nurses overnight or make a war zone safe.

## Limitations

- Coverage per country is extrapolated from measured paces, and governance factors are constant assumptions.
- The functioning rates of new services and the Level 2 services threshold (0.6 of France's services per person) are assumptions.
- Shared car access is approximated (60% of people live where cars are lacking).
- A country counts as covered only when every domain is covered, a strict, conservative rule.
- Within-country inequality is not modelled.
- Labour uses France's productivity.
- The "conflicts end" variant is an upper bound, not a forecast.
