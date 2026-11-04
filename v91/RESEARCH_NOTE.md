# UNIRA V9.1 — conflict prevention through fair institutions

> **Status (4 November 2026): preliminary.** The five evidence rows that rested on search summaries were verified in source on 4 November 2026 (`evidence.csv`): Fearon (2011) confirmed, with the caveat that the effect is barely present for the CPIA aggregate; Cederman, Wimmer & Min (2010) confirmed from the abstract; Beardsley (2011) confirmed; Powell & Thyne (2011) totals confirmed from a secondary source; Pathways for Peace confirmed verbatim. No model parameter changed. Under joint sampling of the model's assumptions (`validation/uncertainty.py`), scenario C avoids 38% of conflict-years (5–95% range 24–49%); the main drivers are the relapse reduction, the causal fraction and the ending boost, all assumptions.


**Question (author):** can UNIRA reduce the risk of conflict by making institutions fairer (representation, transparent resource allocation, independent justice, peaceful dispute resolution, protection against concentrated power), independently of better living standards?

The rules set for the study:
- use real historical evidence;
- do not assume reforms succeed or that disagreement disappears;
- keep the effects of economic development separate from those of institutions;
- report uncertainty, and keep correlation apart from causation.

The constitution is unchanged. Proposals, where the evidence supports them, are in `PROPOSED_CONSTITUTION_CHANGES.md`.

## Short answer

- **Yes, plausibly, and more than better living standards alone.**
  - **Observed:** in 25 years of real data, institutional quality goes with fewer new conflicts even after living standards are accounted for. Once institutions are accounted for, living standards add little.
- **Simulated (80 years):** compared with today's institutions continuing (A), the share of conflict-years avoided is:
  - B, moderate reform: about **15%**;
  - C, strong reform: about **40%** (range 34–50% depending on how much of the historical association is causal);
  - D, comprehensive reform: about **61%**, an upper bound.
- **But most of that comes from assumed mechanisms, not measured ones.**
  - **The measured part is about a quarter of C's effect.** Institutions improving at the historical pace of the best-reforming tenth of countries avoid only about **11%** of conflict-years on their own.
  - **The rest comes from mediation and from lower relapse after conflicts.** For these, studies show the direction, but the size at national scale is an assumption.
- **What the model cannot resolve:** whether such mechanisms work at scale. That has to be learned during implementation (Article 10e.6).
- **Effect on Level 1 and Level 2:**
  - Level 1 for 90% of humanity: 1–2 years sooner.
  - Level 1 for 99%: not reached within 80 years in A; reached in years 48–58 in C–D.
  - Level 2 for 95%: not reached within 80 years in A; reached in years 64–72 in C–D.
- **Reforms carry risks.** Where institutions are weak, rapid change can raise tensions. If that risk is high (onset risk doubled), the last 1% of people get essential security about 10 years later.

## Data and method

**Historical panel** (`institutions/panel.py`, frozen raw data with SHA-256 in `data/raw/raw_manifest.csv`):

- **Conflict:** UCDP/PRIO Armed Conflict Dataset v25.1 (CC BY 4.0). These are intrastate and internationalised intrastate conflicts with at least 25 battle deaths a year, located in the country.
- **Institutional quality Q (0–1):** the mean of four World Bank Worldwide Governance Indicators (WGI, CC BY 4.0): voice and accountability, rule of law, control of corruption, and government effectiveness.
  - The indicator of political stability and absence of violence is **left out on purpose**: it measures perceived violence, so using it would be circular.
  - The WGI are perception-based estimates with margins of error.
- **Living standards LS:** mean access to basic water, sanitation, clean cooking and electricity, as in V9.0. As a check, log GDP per capita was used instead.
- **Logistic regressions on country-years 2000–2024:**
  - onset of conflict (3,663 country-years at peace, 98 onsets);
  - ending of conflict (694 conflict-years, 94 endings).

| Result (95% interval) | Value | Reading |
|---|---|---|
| Institutions → onset, living standards held constant | −4.10 (−6.01 to −2.19) | 0.1 higher Q goes with about 34% lower odds of a new conflict |
| Living standards → onset, institutions held constant | −0.51 (−1.32 to +0.29) | not distinguishable from zero |
| Same with log GDP per capita | Q −4.31 (−6.35 to −2.26); GDP −0.10 (−0.36 to +0.15) | robust |
| Conflict in the past 10 years → onset | +2.07 | about 8 times the odds: the conflict trap |
| Institutions or living standards → conflict ending | both intervals include zero | the ending rate is about 14% a year whatever the conditions |
| Rapid institutional improvement → onset | +0.46 (−6.6 to +7.5) | inconclusive |
| Historical pace of change in Q (10 years) | median ~0; top quarter +0.032; top tenth +0.062; top twentieth +0.084 | slow |
| Gains reversed in the next decade | 1 in 3 (87 decades of gain) | reforms often fail |

The two predictors are correlated (0.58). These are associations, not causes:
- conflict itself lowers both indicators (reverse causation);
- the WGI measure perceptions;
- unobserved factors may drive both.

The results agree with Fearon (2011), who found that governance predicts onset beyond income, and with Fearon & Laitin's reading that income stands for state capacity. The pace agrees with the World Development Report 2011, which found that even the fastest-reforming countries took 15–30 years to go from fragile to functioning institutions.

**Simulation** (`institutions/model.py`). 179 countries over 80 years, coupled with V8.9 delivery as in V9.0:

- **Start:** the 33 countries with an intrastate conflict in 2024 (UCDP). That is broader than V9.0's 21 on the World Bank list, so the dates are not directly comparable with V9.0. Wars between states (for example Russia–Ukraine) are not included.
- **Onset risk** uses the panel coefficients:
  - only a fraction of each association is treated as causal: cQ = 0.5 for institutions (tested at 0.25 and 1) and cE = 0.5 for living standards, the same in every scenario;
  - the intercept is calibrated so that A keeps today's 33 conflicts on average (A stays at 33–34).
- **Ending:** 13.5% a year, as observed. **Relapse:** as observed.
- **Conflict effects on delivery** are proportional to the people affected: at most 25% of a country's population and at most 30 million people per country. A local insurgency in India is therefore not treated like a national war.
- **Effects of reform on delivery:**
  - in fragile countries, delivery improves from 0.75 toward 1 as Q approaches the median of non-fragile countries;
  - corruption losses fall from 26% (Q ≤ 0.3) to 10% (Q = 0.5) and 5% (Q ≥ 0.7). This mapping is an assumption anchored on the Water Integrity Network's figures.
- **Civilian harm:** UCDP battle deaths and one-sided killings of civilians per conflict-country-year, 2015–2024. The mean is 2,745 battle deaths and 253 civilians killed; the median is 274 and 139. The distribution is heavy-tailed, so both are reported.
- **Implementation:** the number of judges, court staff, mediators and auditors needed, in workers rather than money.
- **Uncertainty:** 30 random runs per scenario; the causal-fraction band; 12 sensitivity tests and a decomposition (10 runs each); and a factorial run with the economic channel switched off.

**Scenarios** (only institutions differ):

| | Pace of Q (historical) | Reversal per decade | Mediation (onset / ending / relapse) | Relapse reduction | Other |
|---|---|---|---|---|---|
| A — baseline | none (today's institutions) | — | — | — | — |
| B — moderate (transparency, representation, grievance) | top quarter | 1 in 3 (historical) | — | 15% | reform tension |
| C — strong (independent justice, anti-corruption, civilian mediation) | top tenth | 1 in 4 | −10% / +30% / +15% | 30% | reform tension |
| D — comprehensive (C plus cooperation and effective prevention) | top twentieth (the fastest reformers in history) | 1 in 6.7 | −15% / +50% / +15% | 50% (incl. peace operations) | cooperation −5%; HYPOTHETICAL at this scale |

The evidence behind each mechanism:

- **Mediation:**
  - *Local dispute-resolution training* (Blattman, Hartman & Blair 2014, an experiment in Liberia): violent land disputes fell by 41%. But the gains faded within 3 years, and extrajudicial punishment rose.
  - *Mediation in crises* (Beardsley 2011): mediated agreements relapse more often later. That is the +15% relapse penalty.
- **Lower relapse:** power sharing (Hartzell & Hoddie 2003), institutions that constrain elites (Walter 2015) and peacekeeping (Fortna 2004: more than 55% lower relapse risk). All of these are associations.
- **Cooperation between communities** (Mousa 2020, an experiment in Iraq): behaviour toward known members of the other group improved, but it did not generalise to strangers.
- **Reform tension** (Hegre et al. 2001; Cederman, Hug & Krebs 2010): onset risk is raised by 30% (tested from 0 to 100%) where institutions are weak (Q < 0.35) and change faster than the top-quarter pace.
- **Reform progress** stops during conflict years.

## Results (30 runs; median, 10–90% range in brackets)

| | Conflicts, yr 0 / 20 / 40 / 80 | Conflict-years over 80 yrs | Avoided vs A | Battle deaths over 80 yrs (mean-based / median-based) | Civilians killed one-sidedly (mean-based) | People in conflict zones, yr 80 | Corruption losses, yr 80 |
|---|---|---|---|---|---|---|---|
| A | 33 / 32.7 / 34.4 / 33.8 | 2,719 (2,529–2,938) | — | 7.5 m / 0.75 m | 0.69 m | 3.0% | 15% |
| B | 33 / 29.3 / 28.9 / 25.9 | 2,302 (2,111–2,491) | 15% | 6.3 m / 0.63 m | 0.58 m | 2.4% | 10% |
| C | 33 / 22.9 / 20.0 / 13.8 | 1,622 (1,448–1,779) | 40% | 4.5 m / 0.44 m | 0.41 m | 1.2% | 8% |
| D | 33 / 15.2 / 11.2 / 7.5 | 1,061 (942–1,193) | 61% | 2.9 m / 0.29 m | 0.27 m | 0.6% | 7% |

Conflicts prevented (onsets fewer than in A over 80 years) are 61 in B, 108 in C and 185 in D, out of 365 in A. People in conflict zones were 5.7% of humanity in year 0 in every scenario. Civilian harm is the conflict-years multiplied by UCDP's death rates per conflict-year. The rates are heavy-tailed, so the true figure lies anywhere between the median-based and the mean-based estimate. Institutional quality, weighted by population, rises from 0.45 to 0.56 (B), 0.62 (C) or 0.64 (D) by year 80.

**Level 1 (essential security), year reached:**

| | 90% | 95% | 99% | 100% |
|---|---|---|---|---|
| A | 20 (20–22) | 35 (33–40) | not within 80 years | — |
| B | 20 (19–21) | 33 (30–37) | 67, 7% of runs | — |
| C | 19 (18–20) | 29 (27–31) | 58 (52–68), 77% of runs | — |
| D | 18 (16–19) | 27 (26–28) | 48 (42–52) | 78, 3% of runs |

**Level 2 (comfortable life), year reached:**

| | 90% | 95% | 99% |
|---|---|---|---|
| A | 70 (63–74) | not within 80 years | — |
| B | 63 (60–68) | 79, 27% of runs | — |
| C | 56 (53–58) | 72 (69–76) | — |
| D | 52 (52–55) | 64 (61–71) | 78, 67% of runs |

## Separating economic development from institutional reform

- **Factorial test.** With the living-standard channel switched off (cE = 0), the reforms avoid almost exactly the same share of conflict-years: 16% / 41% / 62% for B / C / D, against 15% / 40% / 61% with it. The institutional effect does not borrow from economic improvement.
- **The economic channel on its own** (scenario A with cE = 0.5 against cE = 0) avoids only about **3%** of conflict-years once institutions are accounted for.
- **This revises V9.0.** V9.0 found 13–26%, from a pattern estimated with living standards alone. The V9.1 panel suggests much of that pattern belonged to institutions: poor countries tend to have weak institutions, and weak institutions predict conflict. **V9.0's economic effect was probably overstated.** Better living standards still matter for delivery and for people's lives; their direct effect on conflict looks small.

## Which mechanisms matter (around scenario C, 10 runs each)

| Change from C | Conflict-years | Level 1, 99% | Level 2, 95% |
|---|---|---|---|
| C as specified | 1,626 | 57 | 72 |
| **Only institutional quality rising** (panel channel, no mechanisms) | 2,414 (11% avoided vs A) | not within 80 years | 77 |
| **Only the mechanisms** (no rise in institutional quality) | 1,921 (29% avoided) | 71 | 79 |
| Without mediation | 2,015 | 73 | 77 |
| Without lower relapse | 1,995 | 69 | 75 |
| Slower pace (top quarter) | 1,740 | 64 | 75 |
| Reform tension 0% / 100% | 1,582 / 1,721 | 58 / 68 | 71 / 74 |
| Reversal 1 in 3 / 1 in 2 | 1,654 / 1,686 | 58 / 59 | 72 / 74 |
| Causal fraction 0.25 / 1 | 1,798 / 1,357 | 62 / 53 | 74 / 70 |
| No economic channel | 1,675 | 58 | 74 |

**The five mechanisms the author asked about:**

1. **Fair representation.**
   - *In the model:* part of institutional quality (voice and accountability) and of lower relapse (power sharing).
   - *History:* exclusion of groups from power is linked to rebellion (Cederman, Wimmer & Min 2010), and accommodation of groups to the decline of ethnic war (Cederman, Gleditsch & Wucherpfennig 2017).
   - *Limit:* the WGI components move together, so representation cannot be separated from the other components.
2. **Transparent allocation and anti-corruption.**
   - *In the model:* part of institutional quality. Corruption losses fall from 15% to 7–10%.
   - *Caution:* corruption can also buy short-term peace through patronage (Fjelde 2009), so anti-corruption reform can disturb existing bargains. This is part of the reform-tension assumption.
3. **Independent justice and grievance procedures.**
   - *In the model:* rule of law in institutional quality, and lower relapse (Walter 2015; Hegre & Nygård 2015).
   - *Evidence:* the local experiment works only with caveats: gains faded within 3 years and favoured the politically connected.
4. **Mediation and early intervention.** This is **the largest single lever in the model**: without it, conflict-years rise by about a quarter. It is also the least certain at scale, and mediated agreements are less durable.
5. **Protection against concentrated power.**
   - *In the model:* fewer reform reversals. Reversals change results little, because a reversal undoes only a decade's gains.
   - *Not modelled:* concentrated power can also cause conflict directly, through coups and personalist rule (Powell & Thyne 2011; Geddes, Wright & Frantz 2018). The constitution's existing safeguards (Articles 5a–5c, 22a, 39a, 42a) address it, but their effect cannot be quantified from the data available.

## Institutional trust, implementation cost, and risks

- **Trust cannot be measured with open global data.** The WGI index reflects expert and survey *perceptions* of institutions. It is not a measure of people's trust, so the model does not report trust. Regional surveys such as Afrobarometer could test it in a pilot.
- **Implementation cost in workers.** Courts, legal aid, mediators, early warning, auditors and grievance officers for the 6.95 billion people living below the reform ceiling need about **2.5–7.8 million workers**, or 0.07–0.22% of the world's labour force:
  - judges: 10–22 per 100,000 people (CEPEJ, Europe);
  - court staff: 2–3 per judge;
  - mediators: 1.2–10 per 100,000 (Ghana's National Peace Council when fully staffed).
- **Risks of reform:**
  - Rapid change in weak institutions can raise tension. If that risk is high, the last 1% reach essential security 10 years later.
  - One in three historical gains was reversed.
  - Local programmes can have side effects: extrajudicial punishment in Liberia, and gains captured by the politically connected.
  - Community programmes often fail to change institutions at all (Casey, Glennerster & Miguel 2012).
  - Reforms imposed from outside are least likely to last. That is one more reason to keep them local and consented (Article 4).

## Which conflicts remain

The most persistent conflicts are in the states with the weakest institutions today: Somalia, Sudan, Afghanistan, Myanmar, DR Congo, Yemen, Syria and Haiti. Even in D, Afghanistan and Somalia remain in conflict a quarter of the years from year 40 on. Disputes over territory and identity, and wars between states, are outside what institutional reform within countries can be shown to prevent.

## Evidence classes (`evidence.csv`, 29 sources)

| Class | Here |
|---|---|
| **Observed** | the panel associations; the pace and reversal of reforms; UCDP death rates; staffing benchmarks |
| **Causal evidence** | local dispute resolution (Liberia); development programmes and institutions (Sierra Leone, Liberia); intergroup contact (Iraq). All are small-scale experiments |
| **Model assumption** | the causal fractions cQ and cE; mediation, relapse, tension and cooperation effects at national scale; the corruption mapping; 30 million people per conflict zone; staffing ratios |
| **Hypothetical intervention** | scenario D's comprehensive prevention and cooperation at world scale |
| **Simulated outcome** | all results tables |

## Limitations

- **Country level only.** Exclusion of particular groups (EPR data) is not used.
- **Perception-based indicators.** The WGI do not separate the five mechanisms.
- **Wars between states are excluded.**
- **The data cannot identify causal effects:** the panel has no experiment or instrument.
- **The scale of mediation and relapse effects** comes from studies of individual programmes and peace operations, not from world-scale reforms.
- **Coups and personalist rule** are not modelled as direct causes of conflict.

## Reproduce

Run `python3 institutions/fetch.py` once to download the data, then:
- `python3 institutions/panel.py` writes `outputs/panel.json`;
- `python3 institutions/model.py` writes `outputs/institutions.json` (about 6 minutes).

Tests (`institutions/tests/`) check:
- reproducibility;
- that the violence indicator is not used as a predictor;
- the direction of the panel association;
- scenario ordering;
- the calibration of A;
- the separation of economics from institutions;
- that reform never lowers delivery or withholds services;
- reversal and tension rules.

The study is part of `v63/run_all.py`.
