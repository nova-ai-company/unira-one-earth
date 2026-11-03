# UNIRA V6.5 — Is there enough for everyone on Earth?

**Question (the user's central aim):** if the world is one entity and resources go to regions by needs × population, can *every* human have a decent, or a comfortable, standard of living with what the world produces **today**?

**Data:** `data/` covers 217 countries and 99%+ of world population: World Bank population, FAO food balance sheets, primary energy (Our World in Data), WHO health workforce, ILO employment and hours. Hours cover only 71% of employment (China missing). 17 frozen sources.
**Thresholds:** `thresholds/` has 34 sourced values from the Decent Living Standards literature, WHO and Eurostat.
**Model:** `model/` (`python3 run.py`, 6 tests).
**Units:** physical only (kcal, GJ, workers, hours). No money.

## Results (latest year, 8.14 bn people)
| domain | level | world supply ÷ world need | people in regions below today | redistribution needed (share of world supply moved) |
|---|---|---|---|---|
| food | decent (2,100 kcal eaten), today's waste | **1.16** | 1.57 bn | 7% |
| food | decent, UNIRA half waste | **1.30** | 0.48 bn | 7% |
| food | comfortable (2,470 kcal eaten), today's waste | 0.99 | 4.45 bn | 7% |
| food | comfortable, UNIRA half waste | **1.11** | 3.36 bn | 7% |
| energy (final) | decent 15.3 GJ/yr | **3.33** | 2.07 bn | 40% |
| energy (final) | comfortable 40 GJ/yr | **1.27** | 4.45 bn | 40% |
| energy (final) | EU-today 82 GJ/yr for everyone | **0.62** | 5.49 bn | — |
| health workers | decent 44.5 per 10k (WHO) | 1.32 (but people cannot be shipped) | 4.21 bn | shortfall 7.7 m workers where needed |
| health workers | comfortable 131 per 10k (EU) | **0.45** | 7.27 bn | **+58.7 m workers** needed (world has 47.4 m) |

**Labour:** world employment is 3.53 bn at about 40.7 h/week. Universal work under UNIRA (80% of ages 15–64 = 4.23 bn people) at 30 h gives **0.88×** today's world working hours, a 12% gap. That is smaller than France's 17%, because the world has a larger labour reserve.

## Findings
1. **Food: enough for everyone, comfortably, if waste is cut.** Today's supply already covers a decent diet for all (1.16×). Halving consumer waste (rule 13) makes a *comfortable* diet for all possible (1.11×). Moving about 7% of world food supply between regions is enough. **The binding problem is distribution and waste, not production.**
2. **Energy: comfortable for all is possible; European consumption for all is not.** The world already has 3.3× the energy needed for decent living and 1.27× a comfortable level (40 GJ final per person). Giving everyone the EU's current final energy use would need 1.6× today's supply. Under equal shares, final energy per person falls about 43% in France (90 → 51 GJ), still above "comfortable", and 72% in the USA. It rises 2.7× in India and 9× in Nigeria. Energy "moves" mainly by **building energy systems where people live**, not by shipping, so this is a decades-long investment programme.
3. **Health workers are the binding constraint on Earth, as in France.** Even the WHO minimum leaves 4.2 bn people in regions below it today (7.7 m missing workers there). Bringing everyone to an EU-like level needs **about 59 m more health workers, more than doubling the world total**. People cannot be redistributed by decision (no forced relocation), so this means **training in every region**: the longest lead time in the whole system.
4. **Rich regions receive less under strict equal shares, but stay comfortable.** France under equal shares: food 3,490 → 3,017 kcal (still above comfortable); energy −43% (still above comfortable). Health workers 134 → 59 per 10k is above the WHO minimum but far below today. For health, "equal share" must mean *build up* the South, not take from the North.
5. **Overall:** on today's physical evidence, **a decent life for everyone on Earth is already possible for food and energy. A comfortable life is possible with less waste and large redistribution, but not at today's European consumption levels.** Health care capacity is the decisive bottleneck and needs a global training programme.

## Limitations
- National averages hide inequality within countries (people below thresholds are counted by region).
- Primary→final energy uses the EU ratio 0.66 for the world.
- Food waste figures are not verified.
- Hours are missing for China and others.
- Floor area per person has no world dataset (MISSING): housing sufficiency is not yet tested.
- Thresholds are not adjusted for climate, age or region.
- Ecological limits (emissions, land, water) are not yet applied. A comfortable 40 GJ for all still needs a low-carbon energy system.
