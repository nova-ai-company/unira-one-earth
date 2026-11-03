# UNIRA V6.6 — Comfortable for all, within Earth's limits? Health, disarmament, ecology, housing

**Question:** V6.5 found that today's world production can give everyone decent food and energy, and comfortable levels with less waste. V6.6 asks four things:
- **(a)** Does a comfortable life for ~9.7 bn people (2050) fit within ecological limits?
- **(b)** How long until everyone has comfortable health care?
- **(c)** What do disarmament and healthier lives contribute (rule 19)?
- **(d)** Is there enough housing?

**Inputs:**
- `ecology/`: 45 sourced rows (IPCC AR6, Forster 2025, IEA, EAT-Lancet, UNEP IRP, O'Neill 2018).
- `evidence_health/`: 50 rows (GBD, WHO/ILO, lifetime-cost studies).
- `data/`: World Bank armed forces, OECD graduates, regional floor-area model, UN WPP 2050.

**Models:** `model/` (`run_health.py`, `run_housing.py`). Units are physical only.

## 1. Ecology (2050, 9.66 bn people)
| per person per year | sustainable range (low / central / high) | today |
|---|---|---|
| final energy, 1.5 °C-class | 25 / 35 / 42 GJ | ~55 GJ |
| CO₂ | net 0 / 0.35 gross / 1.7 (2 °C) t | 5.2 t |
| cropland | 1,346 / 1,636 / 1,816 m² | ~2,000 m² |
| material footprint | 3 / 5.2 / 8 t | 14.2 t |

**Verdict:**
- **UNIRA's comfortable energy level (40 GJ final per person) fits a 1.5 °C pathway.** It totals 386 EJ in 2050, *6–13% less than the world uses today*, within the IPCC 1.5 °C range. It requires:
  - about half of final energy as electricity;
  - fossil CO₂ near zero by 2050;
  - solar and wind built about 1.7–1.9× faster than the 2025 record (669 GW).
- The 1.5 °C budget is now about 3 years of emissions, so a temporary overshoot with some CO₂ removal is unavoidable for any system. 2 °C is comfortably reachable.
- **Food:** a 2,470 kcal comfortable diet for 9.7 bn fits only with a planetary-health diet and halved waste.
- **The tightest limit is materials:** a 2.7× cut per person. This supports UNIRA's stock-first, repair, no-waste and no-overproduction rules.

## 2. Health workers: years until everyone has EU-like care (131 per 10,000)
The world has 47.4 m doctors, nurses and midwives (58 per 10,000). Population reaches 9.66 bn by 2050.

| scenario | training capacity low / central / high (3 / 4.5 / 6% of workforce per year) |
|---|---|
| training as today | never / never / never |
| training +7%/yr for 15 yrs (max 3× today) | never / 37 yrs / 27 yrs |
| + disarmament: 25% of 27.4 m soldiers volunteer for health training | never / 36 / 25 |
| + healthier lives (central prevention, −3%) | never / 34 / 24 |
| **ambitious:** training +10%/yr, 50% of soldiers volunteer, strong prevention (−14% at 30 yrs) | **42 / 23 / 18** |

- **Training capacity (schools, teachers) is the bottleneck.** Without expanding it, the world never reaches comfortable care. With an ambitious UNIRA programme it takes about 18–42 years (central 23).
- **Disarmament (rule 19):** it matters most early. Volunteers lift the world to 71 per 10,000 by year 10, against 64 without them, but the training-capacity cap limits the total effect. 27.4 m armed-forces personnel (0.79% of the labour force) also become available for all other work.
- **Healthier lives (rule 19), evidence-based:**
  - 41–48% of the world's disease burden is attributable to modifiable risks.
  - UNIRA's specific levers are a fraction of that; long working hours alone cause 745,000 deaths a year.
  - Longer lives add care needs later.
  - Net effect on health-worker need: about −3% (central) to −14% (high) after 30 years. **It helps, but it does not replace training.** Confidence: low.

## 3. Housing (floor area, regional model values)
| standard | world supply ÷ need | people in regions below | new floor area to build |
|---|---|---|---|
| decent 15 m²/person | 1.70 | 3.5 bn | ~13 bn m² |
| comfortable 27 m²/person | 0.94 | 5.0 bn | **~65 bn m²** |

Current floor area per person ranges from 7 m² (Ethiopia) and 10.5 m² (India) to 44.7 m² (France) and 55.1 m² (USA). Homes cannot be moved, and there is no forced relocation, so comfortable housing for all means a **building programme of about 65 bn m², mostly in South Asia and Africa**. At 2–4 GJ per m² of embodied energy, that is about 6.5 EJ a year over 30 years: affordable in energy, heavy in materials. Rich regions are above "comfortable" already. The 2-homes rule, stock-first and P1 keep them from growing further.

## 4. Overall verdict on UNIRA's core claim (so far)
**A comfortable life for everyone on Earth is physically possible within a 2 °C limit (and 1.5 °C with temporary overshoot), *if*:**
1. food waste is halved and diets shift toward planetary-health composition;
2. energy is decarbonised about twice as fast as the current record;
3. material use per person falls about 2.7× (stock-first, repair, durability: UNIRA rules 11 and 13);
4. health-worker training is expanded worldwide for 20–40 years, using disarmament volunteers;
5. about 65 bn m² of homes are built where people live now;
6. rich regions accept lower energy and material use per person (still above the comfortable level).

**Not possible:** today's European or US consumption levels for everyone.

## 5. Limitations
- Regional and world averages hide inequality inside countries.
- The floor-area data are model values, not statistics.
- World graduate counts are MISSING (estimated from OECD ratios).
- Training capacity cap, volunteer shares, prevention parameters and lead times are assumptions or judgements.
- Population after 2050 is held flat (the UN projects a peak in the 2080s).
- Global construction capacity (m² per year) is not yet quantified, so years-to-house is unknown.
- Ecology constraints are global per-capita budgets. Regional distribution of emissions and land is not modelled.
