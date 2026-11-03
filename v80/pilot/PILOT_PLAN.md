# UNIRA V8.0 — A real pilot inside today's law

**Status:** proposal, 2026-11-03. Not yet agreed with any council or funder.
**Evidence:** `evidence.csv` (49 rows). Each row says whether the number was read in fetched text (`yes`), only partly (`partly`), or comes from a search snippet or UNIRA's own models (`no`).
**One-page version:** `PILOT_SUMMARY.md`.

---

## 1. Why a pilot

UNIRA cannot be adopted all at once. Its models show what is physically possible. They cannot show how people and institutions behave. Only a real test can do that.

The pilot asks one question:

> **When a town offers everyone a job, works 30 hours a week, publishes every allocation, allocates homes by points and lottery, and lets residents check the rules, do the results match what UNIRA predicts?**

Every prediction is written down **before** the pilot starts. Every failure is published.

## 2. What the pilot can and cannot test

| Can test (inside today's law) | Cannot test |
|---|---|
| 30-hour week at full pay, in volunteer employers | World allocation by needs × population |
| Job guarantee for everyone who wants to work | Fixed prices for all goods "for 1,000 years" |
| Open allocation register for all pilot spending | The U currency and the 1×–5× salary scale |
| Points + lottery for social homes | A real money cap with transfer to One Earth |
| A local voucher with a holding cap (opt-in) | Compulsory work for all ("everyone able to work, works") |
| A citizens' assembly with a formal right of reply | Disarmament, debt cancellation, the Peace Force |
| Safeguards: audits, community monitoring, whistleblowers | Effects of a whole economy changing at once |

Two honest limits:
- **Work cannot be compulsory.** French law and ILO Conventions C029/C105 rule it out. The pilot tests a voluntary guarantee. If voluntary take-up is too low to approach 88%, that is itself evidence against UNIRA's labour claim.
- **A town is open.** People commute, shop and move. Effects leak in and out. The design measures this (section 5.4).

## 3. What precedents show

| Precedent | What was done | Measured result | Source (evidence.csv) |
|---|---|---|---|
| **TZCLD, France** | Law 2016-231: 10 territories. Law of 14 Dec 2020: up to 60. Long-term unemployed hired on permanent contracts (CDI) at ≥ SMIC in *entreprises à but d'emploi* (EBE) | 83 territories, 4,051 employees in 92 EBE (mid-2025). Employment probability **+74 points** over two years. Gross cost **€26,600 per FTE**; net public cost **€11,300–13,700** plus a €6,200 start-up grant. "Few exits" to ordinary jobs | tzcld_* rows |
| **Marienthal (MAGMA), Austria** | Job guarantee for every resident unemployed ≥ 12 months, Oct 2020–2024. Voluntary; no one offered a job declined | Randomised in two waves (4 months apart) plus pre-registered synthetic control. Long-term unemployment **nearly eliminated**; no negative spillovers; better income, security, status, social contact; no effect on physical health. Cost **€29,841 per participant per year** | marienthal_* |
| **Iceland** | 35–36 h week without pay cut, 2015–2019, ~2,500 public workers | Productivity and service "same or improved" in most workplaces. 86% of workforce now has shorter hours or the right to them. Not randomised | iceland_* |
| **UK 4-day week** | 61 volunteer firms, ~2,900 workers, June–Dec 2022 | 56 continued (92%). Revenue +1.4% (23 firms). Sick days −65%, quits −57%, **not statistically significant** (report's own words) | uk_4day_* |
| **Portugal** | 41 firms, >1,000 workers, from June 2023 | Hours 41.6 → 36.5. Only 4 firms went back. Work–life difficulty 50% → 16% (with a control group) | portugal_4day |
| **Valencia** | 4 weeks of Monday holidays, 2023 | 34.9% less stressed; commerce reported lower sales. Weak design | valencia_2023 |
| **Paris participatory budget** | 5% of investment budget, ~€100 m a year | 231,822 voters and 196 projects in 2019 | paris_pb |
| **ProZorro, Ukraine** | All public tenders online and open | Up to 30% savings with >5 bidders; 5,000+ suspicious cases flagged by civil society in six months. Independent study: "some evidence" of more bidders and lower costs | prozorro_* |
| **Singapore, Vienna, Amsterdam** | Quotas + ballot; bonus points; lotteries | Lottery cuts waits for those who win (Utrecht 3.2 vs 10.2 years) | housing_reuse_v79 |
| **Local currencies** | Wörgl 1932; Bristol Pound 2012; Chiemgauer 2003; Sardex | Wörgl stopped by the central bank after 13 months. Bristol closed after use fell and subsidy stopped. Chiemgauer survives at ~€1 m in circulation, with fewer businesses. Sardex: 3,200 firms, 0% interest | worgl, bristol, chiemgauer, sardex |
| **Convention citoyenne pour le climat** | 150 citizens by lot, 149 proposals | Only **24 of 149** truly applied after five years (WWF count) | ccc_outcome |

**Three lessons.**
1. A job guarantee works at small scale and is not budget-neutral. Its net cost is roughly half its gross cost.
2. Shorter weeks keep output in volunteer firms, but the evidence is weak: no randomised firm-level trial and no cut as deep as 35 → 30 h.
3. Local currencies die when they depend on subsidy or on cash. Assemblies disappoint when nobody must answer them.

**The scale gap.** TZCLD averages about **49 jobs per territory**. Raising a town of 20,000 people from 68% to 88% employment needs about **2,200 more people in work**. A UNIRA pilot must be at least 6–15 times more intense than TZCLD, or it does not test UNIRA.

## 4. Site selection

### 4.1 Criteria

| Criterion | Target | Why |
|---|---|---|
| Population | 10,000–100,000 (core components best at 10,000–30,000) | Large enough to measure, small enough to saturate with jobs |
| Employment rate, ages 20–64 | at least 10 points below 88% | So the move toward 88% is measurable |
| Council | Vote by the council **and** support from the main opposition | Must survive the 2032 municipal elections |
| Existing capacity | TZCLD territory or strong social-economy sector | EBEs, staff and know-how already exist |
| Social housing | ≥ 15% of homes; cotation grid already in force | Needed for the housing component |
| Comparison areas | ≥ 50 similar communes not in the pilot | For synthetic control and placebo tests |
| Data | Linked data via INSEE, France Travail, DARES, CAF; social-housing demand register | Outcomes measured from records, not only surveys |
| Contamination | No other large employment programme starting in pilot or control areas | Clean comparison |
| Evaluator | A university team with no stake in the result | Independence |

### 4.2 Example candidate types (no town is named or committed)

| Type | Profile | Strong for | Weak for |
|---|---|---|---|
| A. Former industrial town | 10,000–20,000 people, high long-term unemployment, existing TZCLD | Job guarantee, 30 h, register | Housing (low pressure) |
| B. Priority urban district (QPV) | 15,000–40,000 residents inside a larger city, >40% social homes | Housing points + lottery, assembly | Commuting leaks, harder control |
| C. Rural intercommunality | 15,000–40,000 people, few childcare places, many inactive carers | Mobilising inactive adults, care constraint | Spread-out services |
| D. Mid-size town, two speeds | 50,000–100,000 people; register, housing and assembly town-wide; guarantee and 30 h in one district | Governance at scale | Thin dose of the labour component |

Best plan: **two or three sites of different types**, each with its own synthetic control. One site alone cannot separate the pilot from local luck.

## 5. Components and design

### 5.1 The seven components

| # | Component | What exactly is done | Legal basis today | Who runs it |
|---|---|---|---|---|
| 1 | **Job guarantee** | Every resident aged 18–64 who wants work gets an offer within 3 months: a permanent contract, 30 h at full-time SMIC pay or better, useful local work (care, renovation, repair, food, energy saving). Never a condition for benefits | TZCLD laws (2016, 2020) if renewed; otherwise SIAE/association contracts co-funded by council and foundation | EBE or social enterprise; France Travail; council |
| 2 | **30-hour week** | Employers that volunteer move from 35 h (or more) to 30 h at the same monthly pay, by collective agreement. All guaranteed jobs are 30 h | 35 h is the legal overtime threshold, not a minimum; agreements may set fewer hours (Service-Public F1911). Council staff stay at 1,607 h/year unless a law allows an experiment | Employers, unions; pilot fund pays a declining wage top-up |
| 3 | **Open allocation register** | Every pilot euro, job, home and grant is published within 30 days: what, where, how much, why, on which rule. Machine-readable, open licence. No personal data | Council's own spending powers; open-data duties; Open Contracting Data Standard | Council data office; checked by the audit body |
| 4 | **Homes by points + lottery** | Social homes in the pilot pool: the existing cotation grid sets points; a public lottery among applicants in the same points band; up to 10% by open lottery; must-live-in rule; audit of 75% of successful need claims | Cotation is mandatory (loi ELAN, CCH L.441-2-8). **Whether a lottery is lawful inside French social-housing allocation is not yet verified — legal opinion needed first** | EPCI, social landlords, allocation commission |
| 5 | **Local voucher with a cap** | Opt-in local currency at €1 = 1 unit, digital only. Half of accounts (chosen by lottery) have a holding cap; above it, money moves automatically into the holder's own locked home or retirement savings. No demurrage | Local complementary currency law (CMF L.311-5): issuer must be a social-economy body whose only purpose is this | ESS association; council accepts it for local fees |
| 6 | **Citizens' assembly** | 40–60 residents drawn by lot, stratified, paid for their time. Meets 4 times a year. Sets priorities for a participatory budget (target 5% of investment, as in Paris). Reviews the register. Council must answer every recommendation in writing within 3 months | Council deliberation; advisory status | Independent facilitator; council |
| 7 | **Safeguards** | Random and unannounced audits; community monitoring committee; protected reporting channel; asset declarations for pilot managers; automatic review triggers (section 6) | Council powers; whistleblower law; CNIL rules | Independent audit body named by the scientific committee |

### 5.2 Order of roll-out

| Month | Component starts |
|---|---|
| 0 | Register, safeguards, assembly (cheap, and they watch everything else) |
| 0 and 6 | Job guarantee in two randomised waves |
| 6–18 | 30 h in volunteer employers, in randomised start groups |
| 12 | Housing points + lottery (after legal opinion) |
| 12 | Voucher with randomised cap |

## 6. Measurement

### 6.1 Pre-registered hypotheses

All predictions are filed on a public registry (AEA RCT Registry or OSF) before month 0. The numbers come from UNIRA's own results unless marked *pilot threshold* (set by design, not by a UNIRA model).

| # | Hypothesis | UNIRA prediction | Source of prediction | Counts **against UNIRA** if |
|---|---|---|---|---|
| H1 | Employment rate (20–64) rises toward 88% | Pilot minus control **≥ +10 points** by year 4 (France needs +12.6: 75.4% → 88%) | v63 ledger; README | Effect **< +5 points**, or the rate stalls below 85% when nobody else is left who is able and willing (WP02 test 1) |
| H2 | Take-up within 12 months of an offer | **≥ 61%** of unemployed and **≥ 36%** of attached inactive in work (best three European countries) | v63/flows | No better than France's status quo: **≤ 41%** unemployed, **≤ 25%** attached inactive |
| H3 | Productivity response to 35 → 30 h (θ = share of lost hours recovered) | **θ ≥ 0.20** in market work (output per hour +3.3%); θ ≈ 0.05 in care | v62/v63 central case | **θ < 0.10** in market work (WP02 test 1) |
| H4 | Care staffing at 30 h | Gap (+16.9% staff) closed in ≤ 3 years by training guaranteed workers as care assistants | v63/health | Care vacancies in pilot exceed control by **≥ 2 points for 2 years**, or care hours to residents fall |
| H5 | Leakage of pilot resources | **≤ 8%** of spending not matched to verified delivery (strong safeguards, central) | v69 | **> 15%** in two consecutive years (Article 14 trigger); > 25% at any time (Article 39 review level) |
| H6 | Register timeliness | ≥ 95% of allocations published within 30 days | Article 13/33 | < 80% after year 1 (*pilot threshold*) |
| H7 | Homes: fairness | Income gradient of offers (top vs bottom tenth) **≤ 1.0** (model: 0.86). High-need share of offers falls by **≤ 2 points** vs cotation-only areas; low-need share rises 2–3 points | v79/housing | Gradient > 1.1, or high-need share falls > 5 points |
| H8 | Homes: gaming and vacancy | Audits keep false need claims from changing outcomes; empty pool homes < 0.5% | v79/housing | False-claim winners > 10% of offers after year 1, or vacancy > 2% (*pilot threshold*) |
| H9 | Money cap behaviour | Capped accounts do **not** rush to spend: monthly spending within 10% of uncapped accounts | Money test 2 (WP02) | Capped spending > 25% above uncapped near the cap (*pilot threshold*) |
| H10 | Family time (the purpose of 30 h) | More hours with family; work–life difficulty falls at least as much as Portugal (50% → 16%) | Design clarification 14 | No gain in family time for 30 h workers vs controls |
| H11 | Assembly influence | ≥ 50% of recommendations implemented within 2 years | Article 32b (assemblies by lot) | < 25% (Convention climat: 16%) |
| H12 | No one worse off | Every guaranteed worker earns more than their prior benefits | Design rule | Any group's disposable income falls vs counterfactual |

**What counts against which claim.** H1–H4 test UNIRA's labour claim (the 30 h week holds if ~88% work). H5–H6 test the safeguards claim. H7–H8 test the housing design. H9 tests one part of the money design. H10 tests the social purpose. H11–H12 test governance and fairness.

**Implementation failure is not the same as refutation.** If fewer than 60% of pilot jobs exist by month 18, or funding is cut, the pilot is declared *not delivered*, not *passed* or *failed*. This rule is also pre-registered, so no one can use it as an excuse after the fact.

### 6.2 Outcomes and data

| Outcome | Measure | Data source |
|---|---|---|
| Employment | Employment rate 20–64; long-term unemployment | INSEE census and Filosofi; France Travail registers; DSN payroll |
| Take-up | Share of offered people in work at 3, 6, 12 months | Pilot records linked to France Travail |
| Productivity | Output per hour (sales, service units, cases) in 30 h workplaces | Firm accounts, 2 years before and during |
| Care | Vacancies, hours of care delivered | Employers; ARS/DREES data |
| Leakage | Spending without verified delivery (random audit sample) | Register + audit body |
| Housing | Offers by need band and income tenth; waits; vacancy | Social-housing demand register (SNE), landlords |
| Money behaviour | Spending and balances, capped vs uncapped | Voucher platform (pseudonymised) |
| Wellbeing and time | Life satisfaction, stress, family time, status | Survey every 6 months (same questions as Marienthal and Portugal where possible) |
| Spillovers | Short-term unemployment; local firm sales and jobs | France Travail; URSSAF; INSEE SIRENE |

Linked person-level data are accessed only in a secure centre (e.g. CASD), pseudonymised, under CNIL rules.

### 6.3 Comparison design

| Level | Design | Borrowed from |
|---|---|---|
| Person (job guarantee) | Pairwise matched randomisation into two waves 6 months apart. Everyone gets an offer; only the date is random | Marienthal |
| Workplace (30 h) | Stepped wedge: volunteer workplaces randomised into three start dates 6 months apart | Improves on UK/Portugal (no randomisation) |
| Housing | The lottery is itself random: compare lottery winners and losers in the same points band | Housing lottery studies |
| Voucher | Cap on/off randomised by account | — |
| Town | Synthetic control from ≥ 50 similar communes, plus difference-in-differences | Marienthal (pre-registered) |

### 6.4 Is the pilot big enough? (plain terms)

- **People.** Marienthal had only 62 people in its first group. Its standard errors were 0.02–0.03 on 0–1 outcomes, and its effects were 0.1–0.65. Large effects are easy to see. With 400 eligible people split into two waves of 200, a 14-point difference is detectable without covariates; matching makes it smaller. TZCLD's +74 points is far above that.
- **Workplaces.** This is the weak spot. The UK trial could not show significance with about 23 firms reporting revenue. The pilot needs **at least 40 workplaces** with two years of output data before the start. Below 40, H3 is reported as *underpowered*, not as passed.
- **Town.** One town against a synthetic control is noisy. The effect counts only if it is larger than in at least 95% of placebo runs on the comparison communes. That needs ≥ 20 donor communes; we plan ≥ 50. Two or three sites make this much stronger.

## 7. Safeguards and ethics

| Principle | Rule in the pilot |
|---|---|
| Consent | Every component is opt-in. No sanction for refusing a job. Benefits never depend on taking part |
| No one worse off | Guaranteed pay ≥ prior benefits. 30 h workers keep their monthly pay. Voucher money can always be converted back (5% fee max, as in Chiemgauer) |
| Data protection | Data impact assessment (RGPD) before start. Register never publishes personal data. Pseudonymised research data only |
| Independent evaluation | Scientific committee chosen with the funder, not the council. Right to publish everything, whatever the result |
| Pre-registration | All hypotheses, thresholds and analysis code filed before month 0 |
| Exit | Guaranteed contracts are permanent. If funding ends, a 12-month transition with placement support. The 2016 law already lets the fund cover dismissal compensation if an experiment is not renewed |
| Fair randomisation | Only timing is random for jobs (max 6-month delay). Housing lottery only among equal-points applicants |
| Whistleblowers | Protected reporting channel outside the council |

## 8. Budget and funding

### 8.1 Planning case: one site of 20,000 people

Assumptions (marked): 55% of residents are 20–64 (*assumption*), baseline employment 68% (*assumption*). Jobs cost as in TZCLD.

| Item | Core (300 guaranteed jobs) | Full (800 guaranteed jobs) | Basis |
|---|---|---|---|
| Job guarantee, gross per year | €8.0 m | €21.3 m | €26,600 per FTE (TZCLD 2025) |
| Job guarantee, net public cost per year | €3.4–4.1 m | €9.0–11.0 m | €11,300–13,700 per FTE |
| Start-up grants (once) | €1.9 m | €5.0 m | €6,200 per new job |
| 30 h pay top-up for volunteer employers | €4.3 m over 2 years | same | *Assumption:* 1,000 workers, €40,000 labour cost, 14.3% of pay; 50% in year 1, 25% in year 2, then 0 |
| Evaluation and data | €0.6–1.0 m per year | same | *Assumption* |
| Register, housing lottery, voucher, assembly | €0.3–0.6 m per year | same | *Assumption* |
| **Total, 5.5 years (gross)** | **≈ €45 m** | **≈ €100 m** | |
| **Total, net of avoided benefits and taxes** | **≈ €26–29 m** | **≈ €54–61 m** | |

Cross-check: Marienthal cost €29,841 per participant per year, close to TZCLD's gross cost.

**Reading.** The core case is about 6× TZCLD's average per territory. The full case is the minimum that could move a town of 20,000 most of the way to 88%. Even the full case leaves ~1,400 of the ~2,200 extra workers to ordinary jobs.

### 8.2 Funding options

| Source | Fits |
|---|---|
| State fund for TZCLD (if the experiment is renewed) | Job guarantee wages |
| Département (RSA savings) and France Travail | Part of wages; placement |
| Council and intercommunality | Register, assembly, housing administration |
| European Social Fund+ | Job guarantee, evaluation |
| Private foundations | Evaluation, 30 h top-up, voucher platform |
| Research councils (e.g. ANR, ERC) | Scientific committee |

### 8.3 Timeline

| Phase | Dates | Main tasks |
|---|---|---|
| Preparation | 2027 (12–18 months, after the 2026 municipal elections) | Choose sites; legal opinions (housing lottery, voucher payouts, TZCLD status); council votes; pre-registration; two years of baseline data; build register |
| Running | Jan 2028 – Dec 2031 (4 years) | Components roll out as in 5.2 |
| Interim report | mid-2030 | Published, including any failure |
| Final evaluation | 2032 | Published whatever the result; jobs continue or transition |

## 9. Risks and mitigation

| Risk | Likelihood | Mitigation |
|---|---|---|
| TZCLD experiment not renewed after 2026 | Medium | Second route: SIAE/association contracts co-funded by council and foundations |
| Funding cut midway (as in the 2023 decree) | Medium | Multi-year agreements signed before start; foundation reserve for 12 months |
| Change of council majority | Medium | Cross-party vote; run ends before March 2032 elections |
| Housing lottery unlawful | Medium | Legal opinion first; fall back to points + tie-break lottery only |
| Voucher fades (Bristol) | High | Digital only; no dependence on cash; council accepts it; judged as secondary component |
| Displacement of local firms | Medium | Guaranteed jobs in unmet needs only; spillovers measured (H12, URSSAF data) |
| Too few volunteer employers for 30 h | High | Start recruiting in preparation; report H3 as underpowered below 40 |
| Care staff shortage | High | Care-assistant training inside the guarantee from month 0 (H4) |
| Hawthorne and selection effects | High | Randomised timing; administrative outcomes; synthetic control |
| Cherry-picking results | Medium | Pre-registration; independent committee; publish all |
| Data breach | Low | Secure access centre; no personal data in register |
| "Pilot proves UNIRA" overclaiming | High | Section 2 limits printed on every report |

## 10. What is not yet verified

- How the TZCLD cap rose from 60 to 83 territories, and whether the experiment was renewed after 2026.
- Whether a lottery is lawful in French social-housing allocation.
- Whether a council may pay out (not only accept) a local currency.
- The original TZCLD scientific-committee report and the 2019 IGAS-IGF report were not read directly; their figures come from official summaries.
- Porto Alegre outcomes and ProZorro national savings totals are search snippets only.
- All cost lines marked *assumption* need real quotes.
