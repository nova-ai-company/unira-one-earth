# UNIRA V8.8 — a targeted programme for water, sanitation and clean cooking

> **Status (4 November 2026): preliminary.** Every evidence row that rested on a search summary was verified in source on 4 November 2026 (`essential/evidence.csv`). Confirmed: the basic-WASH capital cost (USD 28.4 bn a year, range 13.8–46.7), handpump non-functionality (about one in four), the IEG outcome ratings (74% against 85%) and the 26% integrity-loss figure. Corrected: the safely-managed WASH range is USD 74–166 bn a year, not 74–116; and the sanitation unit costs had been misread, with recurrent costs per year taken for capital costs — the IRC capital benchmarks are 7–26 USD per person for a pit latrine with slab and 36–358 for a VIP latrine. The model's 40 USD assumption lies between them. Raising it to 100 USD lifts the programme's total capital from about USD 13–20 bn to 17–28 bn a year (scale 2, 15 to 5 years); the timelines, which depend on delivery capacity rather than money, are unchanged.


**Question (author):** if global resources are sufficient, why do people still lack clean water, sanitation and clean cooking, and can UNIRA close these gaps in 5, 10 or 15 years? Delivery counts, not spending. Conflict and governance are modelled, not assumed away. The constitution stays unchanged until the evidence is evaluated.

## 1. Who is without access (latest World Bank / JMP / WHO data; "universal" = 99%)

| service | people without access | largest gaps (people; World Bank FY26 status) |
|---|---|---|
| basic drinking water | **624 m** | DR Congo 69 m (conflict), Ethiopia 57 m (conflict), India 48 m, China 40 m, Nigeria 39 m (conflict), Indonesia 28 m, Tanzania 24 m |
| safely managed drinking water | **1.92 bn** | India 327 m, Indonesia 194 m, Nigeria 161 m, Pakistan 136 m, Ethiopia 113 m, DR Congo 95 m, Mexico 73 m |
| basic sanitation | **1.38 bn** | India 227 m, Nigeria 119 m, Ethiopia 117 m, DR Congo 90 m, Pakistan 68 m, Bangladesh 54 m, Tanzania 42 m |
| clean cooking | **1.92 bn** | India 261 m, Nigeria 165 m, China 127 m, Ethiopia 122 m, Bangladesh 122 m, Pakistan 121 m, DR Congo 103 m |

The fragile and conflict-affected list comes from the official World Bank FY26 document: 21 countries in conflict, 17 with institutional and social fragility.

## 2. Resources needed (`evidence.csv`, `model.py`)

**Per person** (2011 USD capital, ranges from IRC/WASHCost; IEA for cooking):

| service | decentralised | centralised |
|---|---|---|
| basic water | borehole and handpump, about 40 | small piped scheme, about 80 |
| safe water | protected source with household or community treatment, about 70 | piped on premises with treatment, about 150 |
| sanitation | improved pit or pour-flush latrine, about 40 | sewer with treatment, about 500 (assumption: no benchmark found) |
| clean cooking | stove and start-up, about 25 | – |

- **Repair first:** about a quarter of rural water points in sub-Saharan Africa are out of order at any time (Foster et al. 2019). Restoring them costs a fraction of new ones; 15% of the unserved in water are assumed reachable this way.
- **Corruption** adds 26% in fragile and conflict states and 10% elsewhere (Water Integrity Network 2024 and 2016).
- **Totals:**
  - decentralised: **about USD 10–26 bn a year** of capital (0.01–0.03% of world output, about 1% of world military spending);
  - centralised: **USD 52–95 bn a year** (0.05–0.09% of world output).
- Upkeep is a few USD per person a year.
- Workforce needs are in the low millions of mostly local workers, a third skilled.
- These figures agree in order of magnitude with Hutton & Varughese (2016): about USD 28 bn a year for universal basic water, sanitation and hygiene, and about USD 114 bn a year for safely managed services.

## 3. What can be delivered (people durably served)

Delivery capacity per country is based on the best yearly coverage gain achieved by lagging countries (top tenth, measured), times the programme scale, times a governance factor (conflict 0.5, fragility 0.75). Durability: with community operation and funded maintenance, 10% of new points fail; without, 25%.

| plan (decentralised, local participation) | basic water | safe water | sanitation | clean cooking |
|---|---|---|---|---|
| 5 years at 2× best pace | 43% | 22% | 43% | 40% |
| 10 years at 2× | 58% | 42% | 57% | 57% |
| 10 years at 3× | 70% | 53% | 68% | 69% |
| 15 years at 3× | 77% | 66% | 79% | 81% |
| 10 years at 2×, **without local participation** | 48% | – | 53% | – |
| 10 years at 2×, **centralised** | 46% | 26% | 46% | 44% |

**Pace needed to reach 95% of the unserved durably** (multiple of the best historical pace, decentralised):

| target | with today's conflicts | if conflict and fragility were overcome |
|---|---|---|
| 5 years | 11–22× | 6.5–12.5× |
| 10 years | 5–11× | **3.3–6×** |
| 15 years | 3.6–7.5× | **2.2–4×** |

## 4. Answers to the author's questions

**Physically feasible?** Yes. Materials, energy and workers are small relative to world capacity. The capital needed is about 0.01–0.09% of world output a year.

**Economically sustainable?** Yes. Capital is about 1–3% of world military spending, and upkeep is a few dollars per person a year.

**Institutionally achievable?**
- **In 15 years:** yes, if delivery runs at about 2–4× the best historical pace and conflicts are resolved; with today's conflicts, 4–7.5× is needed.
- **In 10 years:** only with an unprecedented, sustained effort (3–6× the best pace) and peace in the conflict states.
- **In 5 years:** not achievable. It needs 6.5–12.5× the best pace even in peace, and 11–22× with today's conflicts.

**What prevents a five-year solution:**
1. **Delivery capacity:** the number of trained local technicians, masons, plumbers and managers, and of working utilities, cannot be multiplied ten-fold in a few years.
2. **Conflict and access:** in DR Congo, Ethiopia, Nigeria, Sudan, Yemen and others, insecurity halves the possible pace (World Bank projects in fragile and conflict states are rated satisfactory less often: 74% against about 85%). In DR Congo, basic water coverage has fallen in recent years.
3. **Durability:** without local operation, maintenance and spare parts, a quarter of new water points stop working, and gains are lost.
4. **Adoption:** sanitation and clean cooking need behaviour change and fuel or electricity supply chains, not only hardware.
5. **Safe water quality:** safely managed water needs treatment, testing and continuous operation, which are the slowest to scale.

**Centralised or decentralised?**
- **Decentralised first:** wells and handpumps, community treatment, safe latrines, clean stoves. They are 3–10× cheaper and faster to deploy, and work in insecure areas.
- **Centralised networks** where density justifies them (cities), as a second step.
- **Repair before building** everywhere.

**The proposed Global Essential Infrastructure Priority Rule** costs very little: the whole programme is about 1–3% of world military spending. So putting it ahead of non-essential consumption elsewhere would not noticeably reduce anyone's living standard. The evidence supports the rule. The binding constraints are capacity, peace and participation, which the rule should address explicitly (training, local operation, safe access), not only money.

## Limitations

- Delivery capacity is extrapolated from historical coverage gains.
- Governance factors, the repair share, sewer costs, labour shares and wages are assumptions.
- Cost figures come from search summaries of benchmark studies (2011 USD), not full reports.
- Very fast national campaigns (for example India's recent tap-water and toilet programmes) suggest higher paces are possible in stable states, but their functionality and safety need independent verification before being used as evidence.
