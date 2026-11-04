# UNIRA V8.7 — the real cost and timing of the UNIRA living standard

**Question (author):** how quickly can humanity guarantee the UNIRA living standard to every person, using existing resources, redistribution, repair, automation, and only the additional production genuinely required?

**Benchmark:** no longer France's consumption. The basket is a physical standard (`basket.json`) with two levels, following the author's definition:
- **Level 1, essential security:** water, sanitation, electricity, clean cooking, food, essential energy, decent housing, health workers, schooling and basic mobility;
- **Level 2, comfortable life:** the comfortable levels of each, plus a car (owned or shared), an annual holiday, leisure, savings and discretionary goods.

Allocations are adjusted for climate (energy) and for age and disease burden (health). Household composition adjusts housing in practice. Every value is labelled with its source or as an assumption. The definition was not changed to improve results.

## 1. Global resources already available (inventory, latest data)

| domain | people covered today | countries below the essential level |
|---|---|---|
| basic drinking water | 91.5% | 131 |
| basic sanitation | 82.0% | 158 |
| electricity | 91.9% | 79 |
| clean cooking | 75.4% | 130 |
| Internet use | 71.3% | 76 |
| secondary school (gross enrolment ≥ 90%) | 80.9% | 89 |

Other domains, from earlier research:
- **food:** world supply is 1.16× the essential need, and the comfortable diet is possible with halved waste;
- **energy:** world final energy is above the comfortable level for all, but unevenly shared;
- **health workers:** 47.4 m, against about 107 m needed for the comfortable level;
- **housing:** about 65 bn m² backlog at 27 m²;
- **goods:** world goods capacity is about 66% of France's goods level per person after reserves, above the 60% the comfortable basket needs, if shared by quotas (v85).

## 2. Dates (99% of humanity covered)

Three scenarios:
- **conservative:** median historical pace of lagging countries; 0.67 TW clean energy a year; low training; no growth in building;
- **moderate:** top quarter of real historical gains; 1.2 TW; central training; building +5% a year;
- **accelerated:** top tenth of real gains; 1.8 TW; high training; building +10% a year.

| domain | essential (cons. / mod. / acc.) | comfortable (cons. / mod. / acc.) |
|---|---|---|
| food | year 1 / 1 / 1 | 1 / 1 / 1 (world supply sufficient; delivery by redistribution) |
| goods and discretionary | year 0 (by quotas) | year 0 (by quotas) |
| energy (climate-adjusted) | 6 / 3 / 2 | 43 / 27 / 27 |
| housing | 6 / 5 / 5 | 32 / 27 / 27 |
| health workers (age and burden weighted) | 9 / 7 / 6 | 60 / 30 / 27 |
| teachers (40 → 20 pupils per teacher) | 11 / 7 / 5 | 35 / 21 / 14 |
| Internet | 20 / 16 / 14 | 29 / 24 / 20 |
| electricity access | 81 / 44 / 35 | 81 / 44 / 35 |
| secondary school | 105 / 57 / 37 | 124 / 72 / 44 |
| clean cooking | 170 / 72 / 46 | 170 / 72 / 46 |
| sanitation | 149 / 83 / 55 | 149 / 83 / 55 |
| drinking water (basic / safely managed) | 165 / 88 / 54 | 296 / 129 / 82 |
| **everyone: Level 1** | **year 170 / 88 / 55** | |
| **everyone: Level 2** | | **year 296 / 129 / 82** |

**Reading the dates honestly:**
- What UNIRA's own plan builds (energy, housing, health workers, teachers, food, goods) reaches the essential level within about **5–11 years**, and the comfortable level within about **27–35 years** (moderate or accelerated).
- The slow domains are **water, sanitation, clean cooking, electricity access and schooling** in a small number of countries, mostly fragile or conflict-affected states (for example DR Congo, where basic water access has *fallen*; Ethiopia, with 10% basic sanitation). Their dates are extrapolated from the *historical* pace of those countries, which reflects war, finance and governance more than physical limits. The physical resources for universal water and sanitation are small relative to world capacity (cost studies put the investment at roughly a tenth of one per cent of world output). In UNIRA (no war, investment first where needs are greatest), these could be far faster. That is not proven by historical evidence, so the historical dates are kept as the honest upper bound.

## 3. Human labour required (comfortable basket, worldwide, at France's productivity)

| | year 0 | year 30 | year 60 |
|---|---|---|---|
| conservative | 13.6 h per worker per week | 12.2 h | 11.5 h |
| moderate | 13.6 h | 11.3 h | 9.6 h |
| accelerated | 13.6 h | 10.1 h | 8.1 h |

**By domain (moderate, year 0, hours per worker per week):**

| domain | hours |
|---|---|
| health | 2.2 |
| leisure, restaurants and culture | 2.1 |
| public administration | 2.0 |
| trade, finance and business services (halved: no advertising or speculation) | 1.6 |
| education | 1.4 |
| care | 1.2 |
| food | 0.9 |
| mobility | 0.5 |
| housing | 0.5 |
| communication | 0.3 |
| energy | 0.1 |
| goods | 0.1 |

**Automation contribution** (accelerated, year 30), hours saved per worker per week:

| domain | hours saved |
|---|---|
| administration | 0.6 |
| trade and finance | 0.6 |
| leisure services | 0.4 |
| health | 0.3 |
| food | 0.3 |
| mobility | 0.2 |
| education | 0.2 |

**Caution.** France's input–output hours exclude work done abroad on imported goods, and productivity is lower in most of the world. So these hours are a lower bound. Even doubled, they fit within the 30-hour week, which leaves time to build what is missing.

## 4. Level 2: cars and holidays (`level2.py`; approximate world figures, labelled to verify)

| option | fleet needed | new cars a year | energy per person | time to build the fleet |
|---|---|---|---|---|
| one car owned per household | 3.9 bn (2.6× today) | 258 m (2.9× today) | 2.4 GJ (6% of 40 GJ) | 29–48 years (production +6% / +3% a year) |
| one car per two households | 1.9 bn (1.3×) | 129 m (1.4×) | 2.4 GJ | 15–23 years |
| shared, one car per three households | 1.3 bn (0.9× today) | 86 m (about today) | 2.4 GJ | today's fleet already suffices, if redistributed |

| holiday option, every person, every year | energy per person | share of 40 GJ |
|---|---|---|
| abroad far, by air (3,000 km return) | 5.4 GJ | 14% |
| abroad near, by rail or coach (1,500 km) | 0.4 GJ | 1% |
| air every second year, rail otherwise | 2.9 GJ | 7% |

Every option means about 9.7 bn international trips a year, about 7× today's international tourism.

**Findings:**
- **Car access** for every family is physically achievable. A shared fleet (car-sharing, one car per three households) needs no more cars than exist today, and an electric car uses about 6% of the comfortable energy level.
- **One owned car per household** needs 2.6 times today's fleet and decades of factory growth, with heavy materials (steel, batteries).
- **An annual holiday abroad for every person is affordable in energy if travel is mostly by rail or coach,** at about 1% of the comfortable level.
- **Long-distance air travel for everyone every year** would take 14% of the comfortable energy budget and multiply international tourism by seven. Without carbon-free fuels at very large scale, that is not compatible with the 1.5 °C path.
- **Suggested Level 2 rule:** a holiday abroad every year, mostly by rail or coach; long-distance air travel within the travel allowance (for example every few years), paid at the surcharged energy price (Article 13.7).

## 5. Environmental check

- **Energy:** the comfortable level for 9.66 bn people in 2050 (climate-adjusted) is **378 EJ**, below today's 409 EJ and within IPCC 1.5 °C-class pathways if about half of final energy is electricity and fossil CO₂ is near zero by 2050 (v66). **Pass**, with the condition that clean energy is built at about 1.8 TW a year for full decarbonisation (v67 check).
- **Housing:** about 15–16 Gt CO₂ if low-carbon, and about 41–43 Gt if conventional (v70). **Conditional pass:** low-carbon building is necessary.
- **Food and land:** fits only with planetary-health diets and halved waste (v66). **Conditional pass.**
- **Level 2 travel:** **pass** with rail and coach holidays and shared or modest car fleets; **fail** with universal yearly long-haul flights.

## 6. Remaining shortages and why

- **Water, sanitation, clean cooking and school access in fragile states:** limited by institutions and conflict, not by physical resources.
- **Comfortable health care:** limited by training capacity (about 27–60 years).
- **The comfortable energy level:** about 27–43 years, limited by the clean-energy build rate.
- **Household car ownership:** limited by factory capacity and materials; car-sharing removes this limit.

## Limitations

- Coverage dates for access are linear extrapolations of measured gains.
- The 99% threshold is used for "universal".
- Labour uses France's domestic input–output hours.
- Car, aviation and tourism figures are rounded orders of magnitude to verify against primary sources.
- The climate adjustment of energy is an assumption.
- Household composition is not modelled explicitly.
