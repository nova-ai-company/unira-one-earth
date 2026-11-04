# UNIRA V8.5 — real data, step 1: production capacity in goods and in local services by country

**Why:** the hybrid D + Q + C (adopted provisionally in V8.4) depends most on how much each region can produce in goods (which can be shared) and in local services (which cannot). V8.4 assumed France's split (24% goods, 76% services) everywhere.

**Data** (World Bank, latest year 2015–2024, 193 countries, 7.9 bn people):
- GDP per person (PPP);
- value added of agriculture, industry and services;
- employment by sector;
- hospital beds;
- pupils per teacher.

Goods capacity is GDP × (agriculture + industry share); services capacity is GDP × services share; both are relative to France. These are capacities to *produce* (they include investment and exports), not consumption.

| countries | share of humanity | goods per person (France = 1) | services per person (France = 1) | goods share of production |
|---|---|---|---|---|
| high income | 17.5% | 1.37 | 0.98 | 28% |
| upper middle income | 38.6% | 0.78 | **0.28** | 43% |
| lower middle income | 36.0% | 0.35 | **0.10** | 47% |
| low income | 8.0% | 0.11 | **0.02** | 55% |
| world (population-weighted) | | **0.68** | **0.32** | 43% (France 21%) |

Examples (goods / services, France = 1):
- USA 1.30 / 1.40;
- China 0.91 / 0.31 (5.6 hospital beds per 1,000);
- India 0.39 / 0.11 (33 pupils per teacher);
- Ethiopia 0.16 / 0.03 (0.3 hospital beds per 1,000).

**Finding 1: the gap between rich and poor regions is mostly a services gap.** The world can produce two-thirds of France's goods per person, but only a third of its services. For the poorer half of humanity, local services are at about 10% of France's level.

## The hybrid rerun with real capacities (`hybrid_real.py`)

Full level = France's consumption; 80 years; 3% reserves; supply shocks; UN population.

| scenario | poorer half: yr 0 / 20 / 40 | inequality (Gini) yr 0 | poorer half reaches 90% |
|---|---|---|---|
| **hybrid**, strong catch-up (+4%) | **24% / 39% / 61%** | **0.28** | year 69 |
| D + C, strong | 16% / 33% / 57% | 0.40 | year 69 |
| **hybrid**, very strong catch-up (+6%) | **24% / 48% / 77%** | 0.28 | year 50 |
| D + C, very strong | 16% / 43% / 76% | 0.40 | year 51 |
| hybrid, services grow only +2% | 24% / 34% / 44% | 0.28 | not within 80 years |

**Finding 2: with real data, sharing goods helps even more at the start.** World goods capacity covers 67% of France's goods level for everyone from day one. Equal goods quotas raise the poorer half from 16% to 24% of the full level immediately (+8 points, against +6 with the synthetic split), and cut inequality from 0.40 to 0.28.

**Finding 3: the long run is decided by local services.** Both designs reach 90% at about the same time (year 50–69 depending on growth), because services, which cannot be shipped, are what is missing. If services in poorer regions grow only at +2% a year, convergence does not happen within 80 years.

**What this means for UNIRA:**
- Goods quotas (Q) are justified by real data: large immediate gains in fairness.
- The real bottleneck is **building local services**: care, teaching, transport, shops, repair. That means training people and building facilities in the regions furthest behind. T-8.5 (investment first where needs are greatest) should give services capacity explicit priority.
- Measured against the UNIRA living standard (Article 10c) rather than French consumption, the dates would come earlier. Costing that standard remains the open research item.

**Limitations:**
- Value added measures production, including exports and investment, not consumption.
- Services include public administration and finance, not only household services.
- Informal production is undercounted.
- Catch-up rates are scenarios.
- Hospital beds and teachers are reported but not yet used in the model.
