# UNIRA review questions, by field

Each question names the file or section to check. "WP02 Lnn" means line nn of `v67/WORKING_PAPER_02.md`, and "Const. Art. n" refers to `v75/constitution/UNIRA_CONSTITUTION_DRAFT.md`. Please answer the questions in your own field. Answer others only if you have something useful to say. Record answers in `FEEDBACK_FORM.md`.

---

## 1. Labour economics

1. **Method.** Is the constant-absence ratio method (H′ = H·R/uT, applying LFS weekly-hour ratios to national-accounts hours) a sound way to estimate the hours lost under a 30 h cap? The research says the net direction of bias is unknown. Do you agree? (`v62/RESEARCH_NOTE.md` §3, §5.3; `v62/src/unira_v62/model.py`)
2. **Self-employed.** National-accounts hours per self-employed person are about 21% above INSEE's LFS figure. Is leaving the self-employed uncapped in the primary scenario defensible? (`v62` §5.2)
3. **θ range.** All evaluated reforms cut hours by 10% or less, starting from 39 h or more, yet θ = 0.10–0.35 (market) and 0–0.15 (care) is applied to a cut of about 17% down to 30 h. Can it be extrapolated that far? Is there evidence that output is roughly proportional to hours below 35 h (Pencavel; Collewet & Sauermann)? (`v62/audit/hours_productivity_evidence.md`, `.csv`)
4. **Job-finding flows as mobilisation.** Is the "gap to best-practice job-finding rates" (+20 points for the unemployed, +11 for the extended labour force, about 0.53 m people) a reasonable estimate of what an active mobilisation policy adds in year 1? (`v63/RESEARCH_NOTE.md` §2; `v63/flows/`)
5. **88% employment.** Ages 20–64 at 88% is above any observed country (IS 85.8% in 2025). Is it plausible within one year, or within five? What do job-guarantee evaluations (e.g. MGNREGA, Argentina's Jefes, the French *Territoires zéro chômeur*) say about take-up and output? (`v63` §4, rule 14; WP02 L94–102)
6. **Entrant productivity.** Is 75% productivity for new entrants in year 1 (SYNTHETIC) consistent with evidence on returners and the long-term unemployed? (`v62` §4b)
7. **Capital and care.** The ledger does not count the hours of childcare and eldercare needed to free carers, or the workplaces and equipment for about 5 m entrants. How large are these hours, and would they reopen the gap? (`v63` §4 conditions)
8. **Market-specific activity.** Are the candidate activities (advertising, real-estate services, financial services, insurance, legal and consulting work) and the 5–75% reduction levels defensible? Would a reformed market (B) capture a similar share? (`v63/io/RESEARCH_NOTE.md` §4.1)

## 2. Macroeconomics and money (stock-flow consistency, fixed prices, money cap)

1. **Stock-flow consistency.** An earlier audit found V5.6/V5.7 "SFC by construction only": money issuance had no matching liability and equity was a residual. Does the V6.4 circuit fix this? Does every issuance of U by One Earth have a counterpart liability, and could any of the 11 checks actually fail? (`v62/audit/AUDIT_FINDINGS.md` A.3; `v64/src/`, `v64/tests/test_circuit.py`)
2. **Fixed price.** π (U per hour of embodied work) is set once so that household spending equals household goods supply in the base year. Is a single price per embodied hour coherent when goods differ in non-labour inputs (energy, land, imported materials)? (`v64/RESEARCH_NOTE.md` §1–2)
3. **Shortage risk.** With fixed prices, what stops excess demand in individual goods even when the aggregate balances (the Kornai shortage mechanism)? Is "production planned to needs plus buffer stocks" specified well enough to test? (`v63/DESIGN_CLARIFICATIONS_2026-11-03.md`, "Specific risks of rules 8–9")
4. **Money cap.** A cap of about 1.4 years of base salary binds for 57% of adults. Is the 60-year lifecycle simulation (6,000 agents, 3 seeds) enough to support "stable at 12 months"? What happens if capped people spend instead of saving (F2)? (`v64/run_lifecycle.py`; WP02 L115–120)
5. **Flow to One Earth.** Is a transfer of about 20–23% of regional consumption value to One Earth each year compatible with the region's own balance? Is it double-counted with enterprise surplus (rule 7)? (`v64` §4b)
6. **Wage drift.** Is "average pay may rise only as fast as productivity" (Const. Art. 14.4) enforceable when multipliers are set by experience and complexity? (`v64` §3.4)
7. **Housing price check.** A €200,000 home embodies about 3,600 h, which is about 525,000 U at π and above the 500,000 U ceiling. Is the 100,000–500,000 U range consistent with labour content? (`v64` §2; Const. Art. 18)
8. **Conversion.** Is "basket parity" for savings and the absence of any single exchange rate workable in practice? Is the lesson drawn from German monetary union (1990) appropriate? (`v72/TRANSITION_RULES.md` T2–T3; `v72/evidence/`)

## 3. Energy and climate

1. **Double use of the build rate.** The 30-year model sends all new clean energy (7 EJ/yr at 1.2 TW/yr) to regions *below* 40 GJ. The 1.1–1.3 TW/yr figure comes from 1.5 °C pathways that use it to replace fossil supply everywhere. Is the same build rate being counted twice, once for convergence and once for decarbonisation? (`v67/transition.py` L97–104; `v67/config.json`; `v66/ecology/`)
2. **Final energy as a climate test.** The climate test compares world *final* energy (≤ 409 EJ) with IPCC ranges, but the model does not track emissions or the fossil share. Is final energy an adequate proxy? (WP02 L155–161, L198)
3. **Rich-region decline.** Is a 3–4%/yr cut in final energy per person in rich regions, for decades, plausible alongside 50% electrification? (`v67/config.json` `excess_decline`)
4. **Conversion factors.** Is the EU primary→final ratio (0.66) applied to the world, and a blended capacity factor of 0.186, acceptable? (`v65/RESEARCH_NOTE.md` limitations; `v67/config.json`)
5. **Military energy.** The model frees military *energy* using military *emissions* share (5.5%, SGR/CEOBS) as a proxy. Is that justified? (`v68/verification/verification.md`)
6. **Decent-living thresholds.** Are 15.3 GJ (decent) and 40 GJ (comfortable) final energy per person faithful to Millward-Hopkins et al. 2020, Kikstra et al. 2021 and Rao & Min 2018? Should they vary with climate? (`v65/thresholds/thresholds.csv`)
7. **Materials.** Is the 2.7× cut in material footprint, from 14.2 t to about 5.2 t per person, consistent with building about 109 bn m² of housing and the energy system at the same time? (`v66/ecology/ecology.md`; `v70`)
8. **Rebound.** Is a 20–30% rebound under flat-rate energy well supported, and is per-unit metering (Const. Art. 19) the right response? (`v71/RESEARCH_NOTE.md`)

## 4. Food and land

1. Are FAO food balance sheet supply (kcal) and the 19% consumer waste figure used consistently? Is halving waste within 10 years realistic? (`v65/RESEARCH_NOTE.md`; `v67/config.json` `waste_*`)
2. Is "redistribute 7% of world food supply at once" physically and logistically credible (storage, transport, local production effects, farmer incomes in importing regions)? (WP02 L137, L200)
3. Does a comfortable diet of 2,470 kcal eaten for 9.7 bn people fit within the cropland range of 1,346–1,816 m² per person only under an EAT-Lancet diet? Is that dietary shift assumed or modelled? (`v66/ecology/`)
4. Is the year-1 sufficiency test (world average kcal ≥ need) too coarse, given seasonality, protein and micronutrients? (`v67/transition.py` food block)

## 5. Health workforce

1. Is 131 health workers per 10,000 (EU level) a sensible "comfortable" target, compared with the WHO 44.5 threshold? (`v65/thresholds/`)
2. Are training capacity limits of 3/4.5/6% of the workforce per year and growth of +7–10%/yr plausible for medical, nursing and midwifery schools, given the shortage of teachers? (`v66/evidence_health/parameters.json`; WP02 L163–173)
3. The world plan allocates training output to regions in need as if "trained in-region". Can training capacity be relocated or expanded where it is lacking? (`v67/transition.py` L105–110)
4. Is it credible that 25–50% of 27.4 m soldiers would volunteer for health training? (`v66` §2)
5. Is prevention lowering need by 3–14% after 30 years consistent with the GBD and lifetime-cost literature (van Baal, Barendregt)? (`v66/evidence_health/evidence.md`)
6. France year 1: are the gaps of about 103 k nurses, about 45 k physicians and about 145 k care workers, and their lead times, correct? Is the absence of a "licensed but not practising" count a serious gap? (`v63` §3; `v63/health/`)
7. Does the 30 h week from year 1 put the constitutional right to care (Const. Art. 6, 9) at risk? (`v63` finding 4)

## 6. Housing and construction

1. Floor area per person comes from the IMAGE model and is not official data. How reliable is the 65 bn m² backlog? (`v66` §3; `v66/data/`)
2. Is 33–64 h of labour per m² (48 h central) right for the building types needed in South Asia and Africa, including self-build? (`v70/evidence/`; inconsistency with WP02 L199, "13–64")
3. Is a sustained 5–10%/yr growth in building capacity, peaking at China's past per-capita rate, plausible across many regions at once? (`v70/RESEARCH_NOTE.md`)
4. Are the embodied-carbon values (400 kg CO₂e/m² conventional, 150 low-carbon) and the stock-first share (40% of need at 40% of the materials) supported? (`v70/evidence/evidence.csv`)
5. Is the gross-vs-net treatment of world construction (3.4 bn m² as a net increase) handled consistently in `v66/construction/capacity.json` and in the model?
6. The paper now gives 4.7 bn m²/yr for the backlog alone and a 6–7 bn m²/yr peak including population growth and upgrading. Is that reconciliation right?

## 7. Governance and political science (allocation errors, safeguards, voting rules)

1. **Leakage evidence transfer.** Leakage parameters come from cash and food transfers (Reinikka & Svensson; Olken; Ferraz & Finan; Muralidharan et al.). Do they apply to infrastructure, construction and training, where corruption is often higher? (`v69/evidence/evidence.csv`, `parameters.json`)
2. **Error structure.** Errors are independent across 179–217 regions, so they average out. How would correlated errors, systematic undercounting of a whole continent, or strategic coalitions of regions change the results? (`v69/coordination/model.py`)
3. **Capture.** Capture is modelled as loss, not as redirection to favoured regions. Would redirection change the ranking against B2? (`v69` limitations)
4. **Comparator design.** Are B and B2 fair comparators? Is B's 30% share of new homes to regions in need (no source) too low? Would a stronger B2 (80–90%) remove most of the advantage, as the boundary test suggests? (`v68/RESEARCH_NOTE.md`)
5. **Square-root rule.** Penrose's square-root rule gives equal voting power to citizens when it sets the *weights of delegates* in a two-tier council. Does it justify square-root *seat apportionment* in a directly elected Assembly (Const. Art. 23)? (`v75/constitution/voting.py`)
6. **Double majority.** Is 55% of regions plus 65% of square-root-weighted population appropriate? The blocking-minority figure (21 regions, now saved) is not saved in `v75/outputs/voting.json`, which shows raw-population blocking (2). Please check. (Const. Art. 25)
7. **Safeguard triggers.** Are the Art. 39 triggers (25% leakage or data older than 2 years leads to review; 45% for 3 years forces reform) measurable in practice? Who measures leakage independently of the bodies being measured? (Const. Art. 33–39)
8. **Concentration of power.** One Earth would control the currency, allocation, the only armed force and the money cap. Are the separation of powers (Art. 22), the Peace Force limits (Art. 5a) and the Court (Art. 32) sufficient against capture? What does the coup literature (Powell & Thyne; De Bruin) imply for the transition? (`v76/peace_force/evidence.md`)
9. **Legitimacy.** Which political-science evidence is missing from the research (legitimacy, compliance, institutional decay)?

## 8. Law (property, transition, constitution, human rights)

1. **Expropriation.** Transferring savings and enterprise shares above the money cap to One Earth (T3, T5; Const. T-1, T-3) is a taking. Is it compatible with property-protection norms (e.g. ECHR Protocol 1 Art. 1, national constitutions) when approved by referendum? What compensation standard would courts apply? (`v72/TRANSITION_RULES.md`)
2. **Anti-flight rule.** The cap applies to wealth held on the day of the joining vote. Is that retroactive, and is it enforceable across non-member jurisdictions? (T3.6; Const. T-1.3)
3. **Debt cancellation.** Cancelling all public debts of members while protecting savers' bonds and paying outside creditors on a schedule (T6; Const. Art. 20, T-4) raises questions of sovereign-debt law, pari passu and litigation risk. How serious are they? (`v72/evidence/`: Cruces & Trebesch)
4. **Duty to work.** Is the duty to work in Art. 7, with exemptions and free choice of occupation, compatible with ILO Conventions 29 and 105 and with ICESCR Art. 6?
5. **Rights guarantees.** Art. 6 guarantees housing, care and a 30 h week, and Art. 9 says these can never be reduced. Can they be enforced when supply is physically short (e.g. care in year 1)? Is Art. 9 justiciable?
6. **Freedom of movement.** Is regional border control (Art. 4b) compatible with the right to leave and return and with non-refoulement? Does it cover disaster and climate relocation? (`v76/migration/evidence.md`)
7. **Amendment and entrenchment.** Are the amendment rules (Art. 42), together with unamendable Art. 6 and Art. 9, coherent with democratic self-government?
8. **Digital currency.** Do the guarantees of Art. 12 (no cash, every commercial transaction invoiced) meet privacy and data-protection standards (e.g. GDPR, ICCPR Art. 17)?

## 9. Demography and migration

1. Is linear interpolation of UN WPP 2024 population from 2024 to 2050, held flat afterwards, adequate for a 30-year plan? Does it affect regional needs, especially in Africa? (`v67/transition.py` L58–61)
2. Is universal work at "80% of ages 15–64" (world) consistent with 88% of ages 20–64 (France)? Does it account for ageing and enrolment in education? (`v65`; WP02 L139)
3. Are the refugee return share of 50–85% and steady-state international migration of 2–4% reasonable (Clemens' migration hump)? (`v76/migration/evidence.md`, `parameters.json`)
4. During convergence, emigration is expected to rise before it falls. How should this interact with regional visa control and with the labour pooling assumed in V6.3?
5. Does the research handle household-size change (needed for housing per person) and dependency ratios (needed for the money circuit)? (`v64` limitations)

## 10. Statistics and reproducibility

1. **Reproduce.** Do outputs regenerate byte for byte from frozen data? Steps: `python3 v63/run_all.py`, then `run.py` in v65–v76; compare against `outputs/`. Check the hashes in each `raw_manifest.csv`.
2. **Tests.** Do the tests check substantive properties, or do any of them restate the model? An earlier self-audit found one tautological check. (`v62/audit/AUDIT_FINDINGS.md` D; `*/tests/`)
3. **Uncertainty.** Only V6.9 propagates uncertainty, through 30 Monte Carlo runs. Is 30 runs enough? Should other results (θ, take-up, capacities) carry joint uncertainty intervals?
4. **Evidence classes.** Is the VERIFIED_OFFICIAL / REPORTED_NEEDS_RECHECK / MODEL_DERIVED / SYNTHETIC / NORMATIVE tagging applied consistently? Pick 10 random rows across the `evidence.csv` files and check them against their sources.
5. **Snippet-only sources.** Several registers include rows marked "no" or "snippet only". Do any headline numbers depend on them? (e.g. `v69/evidence/evidence.csv` 10 of 44; `v72/evidence/evidence.csv` 10 of 61)
6. **Inconsistencies to confirm.**
   - WP02 now reports 151 tests (`python3 v63/run_all.py`). Do they all pass on your machine?
   - Abstract vs conclusions on housing m²/yr.
   - WP02 L199 vs `v70` on h/m².
   - "≈85% preserved" vs 80–89% by domain.
7. **Sensitivity.** Is one-at-a-time lever attribution (V6.8) adequate, given the interactions it notes (energy allocation × restraint)? Would a Shapley-type decomposition change the conclusions? (`v68/counterfactual/compare.py`)
8. **Audit independence.** The four earlier audits were run as separate agents within the project, not by external human experts. Which of their conclusions need independent human confirmation first? (`v62/audit/`)

## 11. New in V7.8–V7.9: AI planning, missing designs and power

1. **Forecast backtests** (`v78/planning/forecast.py`). Is the split (fit before 2005, choose on 2005–09, test from 2010) free of look-ahead? Are naive, drift and trend fair benchmarks? Is median absolute percentage error the right metric for planning?
2. **Information vs integrity** (`v78/planning/information.py`). Errors are applied to levels and population, not to gaps. Is this the right way to represent statistics and forecasts? Is leakage of 8% (from v69) reasonable?
3. **Decent-first allocation** (`v79/allocation/formula.py`). Should decent thresholds (15.3 GJ, 44.5 per 10,000, 15 m²) be uniform across climates and ages?
4. **Food location** (`v79/allocation/location.py`). FAO food balance supply, not production, is used, so importers appear as suppliers. How should a production-based version be built?
5. **Price rule** (`v79/prices/price_rule.py`). Embodied hours come from the domestic France IO table, so imports are not traced. How would a multi-regional IO table change the relative prices?
6. **Money cap** (`v79/money/`). Are the behavioural assumptions (uniform saving rates 0–50%, no response of effort to the cap) acceptable? What evidence exists on labour supply under wealth ceilings?
7. **Housing simulation** (`v79/housing/`). Are the synthetic household and preference parameters plausible? Does the lottery-in-bands design survive strategic behaviour beyond false claims?
8. **Health-need weights** (`v79/health_need/`). Healthy life expectancy is used as a proxy for disease burden. What open, redistributable DALY data could replace it?
9. **Power articles** (`v79/power/POWER_ARTICLES.md`, `STRESS_TEST.md`). Which attack scenarios are missing? Are the thresholds (30-day emergencies, 21 judges, three-key weapons) defensible?
10. **Innovation** (`v79/innovation/evidence.md`). Is the "innovation dividend" of Article 3d.5 compatible with fixed prices? What indicators would detect stagnation earliest?


## 12. New in V8.2–V9.1 and the consolidation of 4 November 2026

*Status: these components are the least verified part of the research. Their evidence rows were sent for verification in source on 4 November 2026; the research notes carry a status banner with the result. Reviewers are asked to treat them as preliminary.*

1. **D + Q + C framework** (`v84/quotas`, Const. Art. 10d, T-8). Is the shortage-economy critique (Kornai) answered by quotas that expire, incomes tied to available goods and buffer stocks? What historical case would test the "no permanent rationing" claim?
2. **Living-standard levels** (`v87`, Art. 10c). Are the physical values (27 m², 2,470 kcal, 131 health workers per 10,000, 40 GJ) defensible as "comfortable" across cultures and climates? Which should vary regionally?
3. **Delivery pace** (`v89/integrated`, `validation/backtest.py`). The pace rule extrapolates each country's own gain with a percentile floor and governance factors. The backtest finds the floors optimistic in conflict and fragile states unless the factors are applied, and saturation in enrolment and Internet use. Is a logistic (saturating) rule warranted? Are the governance factors (0.5 conflict, 0.75 fragility) supported by delivery evidence you know?
4. **Essential infrastructure costs** (`v88/essential`). Are the per-person cost benchmarks (borehole, piped scheme, latrine, stove) current? Is 15% of the water gap reachable by repair plausible?
5. **Distribution and conflict** (`v90`). The conflict gradient is fitted to a cross-section of today's conflicts. Is the causal-fraction device (0–1) a reasonable way to express ignorance, or does it smuggle in a point estimate? What identification strategy would you recommend with open data?
6. **Institutions and conflict** (`v91`). The panel uses four WGI components and excludes Political Stability on circularity grounds. Are perception-based indicators acceptable here? Should ethnic-power-relations data (EPR) replace the country-level index? Are the mediation and relapse effects at national scale (10–15% onset reduction, 30–50% ending boost, 15–50% relapse cut) defensible readings of Blattman et al. 2014, Beardsley 2011, Hartzell & Hoddie 2003, Walter 2015 and Fortna 2004?
7. **Joint uncertainty** (`validation/uncertainty.py`). Are the sampled ranges wide enough? Which assumption that we hold fixed should have been sampled?
8. **Conflict-prevention articles** (Const. Art. 5.6, 10e.6, 10f; proposals 4c, 10f.6, T-9 in `v91/PROPOSED_CONSTITUTION_CHANGES.md`). Do the safeguards against surveillance and withholding of services hold under an adversarial reading? Is an unarmed Mediation Service separate from the Peace Force workable?
10. **The working week during the transition** (`v92/`, T-10, adopted 8 November 2026). The starting week is the shortest week a region's existing labour reserve can cover with no productivity gain (France 35 h, Europe 33–40 h), falling to 30 h with measured productivity, pay unchanged. Is the "slack" reserve framing the right one? Is a cap-by-cap residual of zero a sound definition of "no gap"? What would you require before calling 30 h reachable?
11. **The health target** (`v66/outputs/health_levers.json`, concept §11.13). 131 doctors, nurses and midwives per 10,000 is the EU's density, and it decides the date of comfortable care more than any training lever. What outcome-based threshold would you use, and what share of need can community health workers and care workers meet?
12. **The transition plan** (`concept/UNIRA_TRANSITION_PLAN.md`). Phases are defined by measured triggers, with model dates and their 5–95% ranges. Which triggers are unmeasurable in practice, and which phase boundary is most likely to be crossed on paper only?
13. **Conditional disarmament** (Const. T-5, amended 8 November 2026; `v92/CONSTITUTION_CONSISTENCY_CHECK.md`). A member keeps its existing forces for defence only until the Court finds that its security no longer depends on them: the federation has reached a size and the Peace Force a strength set by law, or every neighbour is a member or bound by a verified agreement. What evidence would you use to set those thresholds? Does a federation in which some members are armed and others are not hold together, and what would make the "defence only" limits enforceable?
14. **Training capacity** (`v66/outputs/training_capacity.json`). Theory online, physical facilities used in rotation for practice, simulation for up to half of clinical hours, every hospital a teaching hospital. Is the NCSBN 50% finding transferable to medicine and midwifery? What share of a clinician's time does supervising trainees cost, and should the model subtract it from care delivered? Is a cap on intake that grows with the workforce the right representation of placement capacity?
15. **Housing levers** (`v70/outputs/housing_levers.json`). Factory building, a decent core first with household-built extensions, and a build rate above the China 2011 record. What are the labour hours per m2 of self-built extensions in practice? Which materials and trades would bottleneck at 7-10 billion m2 a year? Is there audited evidence on 3D-printed housing that we missed?
9. **Authorship and process** (`v77/review/SELF_AUDIT_2026-11-04.md`). The research was produced in two days with an AI assistant. Which results would you expect to change most under slower, human-led modelling, and why?
