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

### 2b. Which levers shorten it? (author's question, 2026-11-06; `model/run_health_levers.py`, `outputs/health_levers.json`)

Parameter changes on the ambitious scenario; low / central / high training capacity. None is a new mechanism and none is evidence that the change can be achieved.

| Lever | Years until everyone has EU-level care |
|---|---|
| Ambitious plan as published (exits 3%/yr, 4-year courses, capacity cap 3×, +10%/yr) | 42 / 23 / 18 |
| Keep more workers: exits 3% → 2% a year | 30 / 20 / 16 |
| Exits 3% → 1.5% a year | 27 / 18 / 15 |
| Shorter courses, 4 → 3 years | 41 / 22 / 17 |
| Shorter courses, 4 → 2 years | 40 / 21 / 16 |
| Training capacity cap 3× → 4× today's intake | 30 / 21 / 18 |
| Capacity cap 5× and +15%/yr (faculties and trainers first) | 23 / 17 / 15 |
| Retention 2% + courses 3 years + capacity 4× | 24 / 18 / 15 |
| **All levers** (retention 2%, courses 3 years, capacity 5×, +15%/yr) | **19 / 15 / 13** |
| Target 131 → 100 per 10,000 | 24 / 15 / 12 |
| Target 131 → 80 per 10,000 | 14 / 8 / 7 |
| Target 44.5 (WHO threshold, world total) | 0 / 0 / 0 (the world total is already above it; the problem is regional, see V7.9) |

- **The capacity cap binds, not the course length.** Two years off the courses saves 1–2 years; faculties and trainers built first save 6 years in the central case. "Training and health capacity first" (T-8.5) should read *faculties first*.
- **Retention is worth as much as capacity.** A one-point fall in yearly exits saves 3 years (12 in the low case). Whether a 30-hour week and better conditions achieve it is untested; people trained in health who no longer practise are a reserve the model does not count (research item).
- **The target decides the date more than any lever.** 131 per 10,000 is the EU's staff density (medium confidence in `v65/thresholds`), not an outcome. An outcome-based Level 2 threshold, and the share of need that community health workers and care workers (not counted in the 131) can meet, are open research questions (concept §11.13); sources must be verified before either enters the paper. The 100 and 80 rows are illustrative, not proposals.
- **Essential care for everyone is a distribution problem, not a world-total problem:** with "decent for everyone first" allocation every region reaches 44.5 per 10,000 by year 6–7 (V7.9), provided workers are trained where people live.
- **Disarmament (rule 19):** it matters most early. Volunteers lift the world to 71 per 10,000 by year 10, against 64 without them, but the training-capacity cap limits the total effect. 27.4 m armed-forces personnel (0.79% of the labour force) also become available for all other work.
- **Healthier lives (rule 19), evidence-based:**
  - 41–48% of the world's disease burden is attributable to modifiable risks.
  - UNIRA's specific levers are a fraction of that; long working hours alone cause 745,000 deaths a year.
  - Longer lives add care needs later.
  - Net effect on health-worker need: about −3% (central) to −14% (high) after 30 years. **It helps, but it does not replace training.** Confidence: low.

### 2c. Training "out of the box": theory online, facilities in rotation, every hospital teaches (author, 2026-11-08)

The author's direction: teach theory online; use schools, universities, laboratories and hospitals for practice only, in rotation (one cohort today, another tomorrow, at full capacity); send trainees to different hospitals to learn with expert practitioners. `model/training_capacity.py` (+6 tests) splits the synthetic 3× capacity cap into four components and asks what each becomes.

| Component | What the evidence says | Cap under the rotation design (× today's intake, low / central / high) |
|---|---|---|
| Lecture space | blended learning as effective as or better than traditional for knowledge in health professions (SMD 0.81, 0.26 after publication-bias adjustment; 1.07 in medical education; both verified abstracts) | stops binding |
| Practice facilities (skills laboratories, simulation centres) | university teaching space occupied about 20% of the time (30+ UK universities, reported); rotation to 50–70% (synthetic) | 5 / 7.5 / 10.5 |
| Clinical placements | half of clinical hours can be simulation with no difference in competency, knowledge or licensing results (NCSBN randomised study, 10 programmes, 666 students, verified); rotation across under-used hospitals (synthetic) | 4 / 6 / 9 |
| Educators | online theory frees 10–50% of educator time per student (synthetic); US schools refuse qualified applicants for lack of clinical sites, faculty, preceptors and classrooms (65,766 applications in 2023, AACN, verified) | **3.3 / 3.9 / 4.5 (binding)** |

| Design (ambitious plan otherwise unchanged) | Years to 131 per 10,000 for all, low / central / high |
|---|---|
| Published (cap 3×, +10%/yr for 15 years) | 42 / 23 / 18 |
| Theory online, facilities in rotation, simulation for half of clinical hours; same educators (cap 3.9×) | 36 / 21 / 18 |
| As above, and every hospital teaches: placements and preceptors grow with the workforce | 29 / 21 / 18 |
| As above, +15%/yr expansion (faculties and trainers first) | 23 / 17 / 15 |
| As above, exits 3% → 2% | **20 / 16 / 14** |

- **Buildings stop being the limit; people who teach are.** With the same educators the cap rises only to about 3.9×. The large gain in the low case (42 → 29 years) comes from treating every hospital as a teaching hospital, so that placement and preceptor capacity grows with the workforce itself (`capacity_scales_with_stock` in `health_plan.py`; off by default, published results unchanged). In the central case the pace of expansion binds, not the cap.
- **It is cheaper in buildings:** the same intake needs about a fifth more laboratory space instead of three times the campuses (not costed; no faculty cost model exists in the project).
- **Boundary:** this is for adult and professional education. School closures cost children 0.14–0.19 standard deviations of learning (two meta-analyses, verified abstracts); children's schooling stays in person.
- **Limits:** the simulation evidence is for pre-licensure nursing and is applied to all cadres; supervising trainees costs clinicians' time that the model does not subtract; trainees rotating across regions need housing, travel and language support. Constitution text proposed in `concept/PROPOSED_CONSTITUTION_CHANGES_2026-11-08.md` (not yet approved).

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
