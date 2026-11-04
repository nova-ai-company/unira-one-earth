# UNIRA V9.0 — can fair distribution of resources reduce armed conflict?

**Question (author):** can UNIRA's fair distribution of resources reduce armed conflict, and would fewer conflicts let humanity reach Level 1 (essential security) and Level 2 (comfortable life, Article 10c) sooner? The question is to be studied with evidence, separating correlation from causation, with no invented percentages. Scenario D is a conditional upper bound, not a forecast. The constitution is unchanged; proposals are in `PROPOSED_CONSTITUTION_CHANGES.md`.

## Short answers

1. **How much of today's conflict burden is plausibly linked to deprivation?**
   - **Observed:** today, 31% of the poorest quarter of countries are in armed conflict, against 2–4% in each of the other three quarters (World Bank FY26 list; living standards from water, sanitation, clean cooking and electricity access).
   - **If that whole pattern were causal:** about 24–67% of today's conflict risk would be linked to deprivation (central 40%).
   - **But not all of it is causal.** Conflict destroys services (reverse causation), and income largely stands for state capacity (Fearon & Laitin 2003).
   - **Plausibly causal share:** anywhere from **about 5% to about two thirds**, central about **a fifth** (40% × a causal fraction of one half). No more precise figure is justified.
2. **How much could UNIRA realistically reduce it?** Over 80 years, the share of conflict-years avoided compared with no reduction (A) is:
   - **B, moderate:** about 13%;
   - **C, strong:** about 26%;
   - **D, conditional upper bound:** about 68%, but D adds hypothetical diplomacy and reconciliation, so its gain is not UNIRA's alone.
   - **Little changes in the first 20 years** of any scenario except D.
3. **Is a positive feedback loop plausible?** Yes, but it is slow, and it starts by working against UNIRA:
   - conflict halves delivery exactly where conflict risk is highest, so living standards rise slowly there (a "conflict trap");
   - the virtuous loop becomes visible only after year 20–40.
   - Backlash against programmes (Crost et al. 2014) matters locally but changes the world totals by about 1%.
4. **Which conflicts would remain?** In B and C:
   - **Where:** the poorest and weakest states. The Central African Republic, DR Congo, Chad, Niger, Madagascar, Ethiopia, Mozambique and Malawi top the list in every run.
   - **Why:** about two thirds of the remaining risk is **not linked to living standards**. It comes from territory, identity, exclusion from power and state weakness.
   - **Also outside the model:** wars between states and great-power wars.
5. **How much faster are Level 1 and Level 2?**
   - **Level 1 for 90%:** almost no change (year 16 in every scenario).
   - **The last 5–10% of people:** this is where conflict matters. Compared with A:
     - Level 1 for 99%: about 3–8 years sooner in B–C, 21 years sooner in D;
     - Level 2 for 95%: about 4–6 years sooner in B–C, 14 years sooner in D.
   - **Universal Level 1 (100%)** is reached within 80 years only in D (year 57).

## Method (`conflict/model.py`)

**Conflict model.** Each of 179 countries is in conflict or at peace each year (a two-state chain over 80 years):

- **Starting state:** the 19 countries on the World Bank FY26 conflict list that the model covers. South Sudan and Palestine lack data.
- **Onset risk** combines two parts:
  - a **frozen part** (share `s_ne`) that stays at today's level whatever happens to living standards: territory, identity, exclusion, state weakness;
  - a **responsive part** that follows each country's living standards, through a fraction `c` of the observed pattern between poverty and conflict that is assumed causal.
- **The pattern itself** (slope β = 4.75) is estimated by maximum likelihood from which countries are in conflict today. It is an **association**, not a cause.
- **Ending risk:** a conflict ends with a 10% chance a year, giving a median duration of about 7 years. Better living standards raise that chance (`tau`).
- **Relapse:** in the 10 years after a conflict ends, onset risk is 4 times higher, so about 40% relapse within 10 years (the literature finds 20–57%).
- **Backlash:** in conflict and fragile countries, onset risk rises by half (B) or a quarter (C, D, with safeguards) in programme years 1–3.
- **Calibration:** the base risk H is set so that A keeps today's number of conflicts on average. A then stays at 17–19 countries in conflict, with 13–24 in 80% of runs at year 40.

**Coupling with V8.9** (`v89/integrated/simulate.py`, accelerated delivery):

- **Conflict slows UNIRA:**
  - delivery is halved during conflict, as in V8.9;
  - fragility cuts delivery by a quarter;
  - the quarter of the population living inside conflict zones gets no service but food.
- **UNIRA lowers conflict:** each country's living-standard index (today's observed access; later the higher of that and 0.7 × Level 1 + 0.3 × Level 2 coverage) lowers onset risk and raises the chance of ending.
- **Solving the loop:** conflict and living standards are iterated three times with the same random draws.
- **Uncertainty:** 30 random runs per scenario (median and 10–90% range) and 14 one-at-a-time sensitivity tests (10 runs each).

**Scenarios** (only conflict differs; delivery as V8.9 accelerated):

| | causal fraction c | frozen share s_ne | backlash | other |
|---|---|---|---|---|
| A — no conflict reduction | 0 | (all risk frozen) | none | conflicts still end and start at today's rates |
| B — moderate | 0.5 | 0.5 | +50% | |
| C — strong | 1.0 | 0.3 | +25% | |
| D — conditional long-term peace | 1.0 | 0.3 | +25% | HYPOTHETICAL diplomacy and reconciliation: frozen risk falls to a tenth over 50 years; chance of ending tripled |

## Results (30 runs; median year, 10–90% range in brackets)

| | Countries in conflict, yr 0 / 20 / 40 / 80 | Conflict-years avoided vs A | Onsets prevented vs A | Conflicts ended | People in conflict zones, yr 80 |
|---|---|---|---|---|---|
| A | 19 / 19.1 / 19.1 / 19.3 | — | — | 152 | 2.0% |
| B | 19 / 19.1 / 16.7 / 13.5 | 13% (192) | 17 | 140 | 1.5% |
| C | 19 / 19.1 / 14.1 / 8.4 | 26% (391) | 43 | 120 | 0.9% |
| D | 19 / 10.9 / 3.0 / 1.1 | 68% (1,023) | 64 | 106 | 0.3% |

"Conflicts ended" is lower in C and D because fewer conflicts start.

**Level 1 (essential security), year reached:**

| | 90% | 95% | 99% | 100% |
|---|---|---|---|---|
| V8.9 — today's conflicts never end | 17 | 29 | 53 | — |
| A | 16 (16–18) | 27 (25–30) | 60 (51–74), reached in 40% of runs | not within 80 years |
| B | 16 (16–18) | 27 (26–30) | 57 (49–73), 83% of runs | not within 80 years |
| C | 16 (16–18) | 27 (26–30) | 52 (45–65) | 73, 3% of runs |
| D | 16 (15–16) | 25 (24–25) | 39 (38–42) | 57 (53–66) |
| V8.9 — all conflicts end now | 14 | 21 | 32 | — |

**Level 2 (comfortable life), year reached:**

| | 90% | 95% | 99% | 100% |
|---|---|---|---|---|
| V8.9 — today's conflicts never end | 72 | — | — | — |
| A | 55 (51–60) | 75 (67–79), 80% of runs | not within 80 years | — |
| B | 54 (51–58) | 71 (66–76), 97% of runs | not within 80 years | — |
| C | 52 (51–60) | 69 (63–74) | 79 (77–80), 20% of runs | — |
| D | 50 (48–52) | 61 (58–63) | 70 (67–72) | not within 80 years |
| V8.9 — all conflicts end now | 47 | 54 | 59 | — |

**Reading the comparison with V8.9.**
- **Level 2 for 90% is earlier in A (year 55) than in V8.9 (year 72), even with no conflict reduction.** V8.9 assumed the same 21 conflicts last 80 years. In A, conflicts end after about 7 years and new ones start elsewhere, as in history. That gives every country periods of peace in which to build.
- **For the last 1% of Level 1, A is later than V8.9** (year 60 against 53). A also takes services away from the people inside conflict zones, and new conflicts hit countries that V8.9 treated as peaceful.
- **What these differences mean:** they come from modelling conflict realistically, not from UNIRA.
- **The gain attributable to UNIRA's effect on conflict** is the gap between A and B or C.

**Yearly bottleneck (first run).** The bottleneck is the limiting factor, for Level 2:
- years 1–10: training health workers (about 7 bn people short, i.e. everyone not yet at Level 2);
- years 20–40: local services in the poorest regions;
- from year 60 in A and B: **conflict** (people in conflict countries);
- in C, conflict becomes the bottleneck only around year 80; in D, it never does.

**Sensitivity** (one change at a time from B, 10 runs):
- **Conflict-years** depend most on:
  - the causal fraction `c` (1,471 at c = 0.25 against 1,275 at c = 1);
  - the slope β (1,445 at half the fitted slope);
  - the frozen share (1,295–1,444).
- **Backlash** from 0 to +185% changes conflict-years by under 1%. Relapse and duration assumptions change them by about 3%.
- **Level 1 for 90% and 95%** stays at years 16–18 and 27–29 in every test.
- **Level 2 for 95%** ranges from year 65 to 77. The largest delays come from a bigger conflict-zone share (40%) and a weak causal effect.

## Evidence classes (`evidence.csv`)

| Class | What | Examples |
|---|---|---|
| **Observed relationship** | measured facts and associations | UCDP: 61 state-based conflicts in 2024, a record; PRIO: 473 m children live in conflict zones; FY26 list; the poorest quarter has a 31% conflict rate; income predicts onset (Fearon & Laitin 2003); unequal groups fight more (Cederman et al. 2011); unemployment is not linked to insurgency (Berman et al. 2011); median duration 6–7 years; relapse 20–57% |
| **Causal evidence** | designs that identify causes | income shocks raise conflict risk (Miguel, Satyanath & Sergenti 2004, instrumental variables; contested by Ciccone 2011); aid projects provoke attacks at their start (Crost, Felter & Johnston 2014, regression discontinuity) |
| **Model assumption** | values chosen and tested in ranges | causal fraction c (0–1); frozen share (0.3–0.7); backlash size nationally; relapse ×4; tau; 25% of people in conflict countries inside zones |
| **Hypothetical intervention** | not shown to work at this scale | scenario D's diplomacy and reconciliation |
| **Simulated outcome** | everything in the results tables | dates, conflict counts, conflicts avoided |

## Limitations

- **The conflict list is narrow:** the World Bank list holds 21 conflict situations; UCDP counts 61 state-based conflicts, many of them small or in larger states (for example India and Pakistan). The model is about conflicts severe enough to affect a whole country.
- **Not modelled:** wars between states and great-power wars. Russia–Ukraine shows these can dominate battle deaths.
- **Countries are treated as wholes.** Conflict is local, and inequality between groups is not represented.
- **The living-standard index measures access to basic services,** not income or political inclusion.
- **No duration dependence:** the model does not let long wars become harder to end.
- **The main unknown, the causal fraction c,** cannot be estimated from data available today. Proposal 2 would let monitoring measure it during implementation.

## Reproduce

`python3 conflict/model.py` writes `outputs/conflict.json` (about 10 minutes). The tests in `conflict/tests/` cover:
- reproducibility;
- the observed gradient;
- scenario ordering;
- the calibration of A;
- that diplomacy appears only in D;
- the risk rules;
- that no date is earlier than if all conflicts ended now.

The model is part of `v63/run_all.py`.
