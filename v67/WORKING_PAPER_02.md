# UNIRA Working Paper 02 — One Earth, 30 Hours: Physical Feasibility Evidence (V6.2–V6.7)

3 November 2026

**Abstract.** We test whether UNIRA, a proposed one-world cooperative economy, is physically possible with today's people, energy, food, land and materials. It has a 30-hour week, fixed prices, needs × population allocation and no commercial competition. Using official data for France, 30 European countries and about 180 world regions, the answer is yes, over about one generation and under six conditions:

- universal work at about 88% employment;
- halved food waste;
- clean energy built at 1.2–1.8 TW a year (1.2 TW closes the energy gap of poorer regions; about 1.8 TW is needed to also bring fossil use near zero);
- a 2.7× cut in material use;
- a 20–30-year health-worker training programme;
- home building growing to about 4.7 bn m² a year for the backlog, and to a peak of 6–7 bn m² a year once population growth and upgrading are included.

In the central 30-year plan, every region reaches 40 GJ of final energy per person by year 27 and EU-level health care by year 30, with world energy at or below today's level. Comfortable housing is half done. Everyone's diet is covered from year 1. Giving everyone today's EU energy use is not possible.

With the same resources, a reformed market economy does not converge within 30 years; it would need to direct about 90% of new capacity by need to match UNIRA on energy. The advantage survives realistic allocation errors and leakage, and strong safeguards preserve about 85% of it. UNIRA's money rules are internally consistent once personal money is capped. All results are reproducible from frozen official data and stated assumptions.

## 1. Introduction

UNIRA proposes one democratic world federation in which today's countries become regions. Resources go to regions by needs and population, with a 30-hour week, fixed prices and no commercial competition for profit. This paper tests whether that is **physically possible** with the people, energy, food, land and materials the world has. It does not test whether it is politically achievable.

The design rules below were set by the author and are treated as **normative targets**. Every other number is classed as official, model-derived or a stated assumption.

| # | Design rule (normative) | What the research tests |
| --- | --- | --- |
| 1 | 30-hour week (6 h × 5 days) from the start | Hours lost and how they are replaced, year 1 |
| 2 | Currency U and the economy are not the market model | Results in hours and physical units, never euros |
| 3 | One world entity; countries become regions | Pooling labour and production across regions |
| 4 | No commercial competition for profit; ideas still compared | Hours freed from market-specific activity |
| 5 | Resources allocated by needs × population | World sufficiency and redistribution volumes |
| 6 | Base salary 5,000 U/month; multipliers 1×–5× by experience, knowledge and job complexity | Money circuit, price stability |
| 7 | Surplus goes to region, then to the One Earth entity | Regional balances and One Earth flows |
| 8 | Fixed prices for essentials, permanently | Shortage risk at fixed prices |
| 9 | One Earth decides which region produces what | Allocation of production and transfers |
| 10 | Owner pay is a capped salary; essentials bought with salary | Enterprise surplus, regional fund |
| 11 | Homes 100,000–500,000 U; at most 2 per adult and per family | Affordability, construction capacity |
| 12 | Multipliers set by experience, study and job complexity | Experience creep at fixed prices |
| 13 | Savings kept; studied catastrophe reserves; no waste or overproduction | Deposits, reserves, hours |
| 14 | Everyone able to work, works; 30 h keeps families together | Employment rate and the hours gap |
| 15 | Retirees: needs-based income; health care and education free | Regional fund outflows |
| 16 | Up to 50% saving; zero-interest home credit | Housing finance, money balance |
| 17 | Saving is personal, at most 50% | Lifecycle simulation |
| 18 | Personal money capped yearly; excess and large inheritances to One Earth; automation shortens hours | Money stability, work incentive |
| 19 | No wars; far less disease from better lives | Freed personnel; preventable health demand |

Three proposals from this research were provisionally accepted (P1–P3, section 4). The full wording of every rule is in `v63/DESIGN_CLARIFICATIONS_2026-11-03.md`.

## 2. Data and methods

All results are reproducible offline from frozen official data: 194 tests pass, and outputs regenerate byte for byte from a clean copy.

- **Sources:**
    - Eurostat national accounts and Labour Force Survey;
    - INSEE;
    - World Bank;
    - FAO food balance sheets;
    - WHO health workforce;
    - ILO;
    - UN World Population Prospects 2024;
    - Our World in Data energy (republished, marked for recheck);
    - peer-reviewed literature on decent living, ecology and health.
- **Evidence classes:** every number is tagged as one of:
    - VERIFIED_OFFICIAL, retrieved from the named table with a SHA-256 hash;
    - REPORTED_NEEDS_RECHECK;
    - MODEL_DERIVED;
    - SYNTHETIC_ASSUMPTION;
    - NORMATIVE_TARGET (the author's rules).
- **Units:** UNIRA results are in hours of work, kcal, GJ, persons and m². Euro-denominated input-output tables serve only as a technical proxy for physical interdependence. U is never converted to euros.
- **Independent audit:** four separate reviews were run.
    - Reproducibility of V0.1–V6.1: 125/125 files intact; 90/90 runnable tests pass.
    - Primary-source verification: 23 recorded figures, 0 contradicted.
    - Adversarial code review: 5 major findings, all fixed or documented.
    - Hours-productivity literature review.
- **Corrections to earlier versions** found by the audit:
    - V5.6/V5.7 were not stock-flow consistent.
    - The V5.6 "stress case" was the baseline.
    - V6.1's 46-week convention was not a 30-hour rule.

Code and data: `UNIRA_V62_V67` package, `python3 v63/run_all.py`.

<!-- refs:begin sources §2 -->

*Sources for this section:* Food & Nations n.d.a; Our World in Data n.d.b; United Nations & Social Affairs WPP2024_Demographic_Indicators_Medium.csv.gz, 2024.

<!-- refs:end -->

## 3. Labour: a 30-hour week from year 1

With universal work at an 88% employment rate (ages 20–64), France keeps today's output under a 30-hour week from year 1, on central assumptions. Without new workers, it would need 20% more output per hour.

- **Baseline (France 2023, national accounts, all employed):** 45.6 bn hours, 1,501 h per person. Capping employees' usual week at 30 h removes 16.7% of hours, so output per hour must rise 20.1% at constant output (29.1% if the self-employed are also capped). That is 32 years of 2015–19 trend growth.
- **Sector averages mislead.** In health, education and public administration, average annual hours are already below 1,380 because of part-time work. Full-time and part-time workers must be separated.
- **Labour reserve (30 European countries):** the unemployed, people available but not seeking, and underemployed part-timers could cover up to 51–59% of France's gap (43–50% EU-wide). Observed job-finding flows imply only about 0.53 m additional people in year 1 under today's institutions.
- **Evidence on shorter hours:** hourly productivity recovers 10–35% of lost hours in market sectors and 0–15% in care. Hours cuts alone create no net jobs without subsidies.
- **Market-specific activity** (advertising, speculative finance, real-estate intermediation) could free 1.7–6.6% of all hours. This is a UNIRA-specific contribution.

| France, year 1, 30 h for employees | Output-per-hour gain still needed |
| --- | --- |
| Today's job-finding flows (central) | 10.2% |
| Employment rate 20–64 raised to 84% | 2.6% |
| Employment rate 20–64 raised to 88% (rule 14) | 0% (gap closed) |
| Europe pooled, 88% | 1.3% |

Conditions for the 88% case:

- workplaces for about 5 m new workers;
- childcare and eldercare;
- an employment rate above any country today (Iceland 85.8% in 2025).

Health and care staffing remains short in year 1 (about 100,000 nurses and 145,000 care workers), because training takes years.

<!-- refs:begin sources §3 -->

*Sources for this section:* Aiken et al. 2014; Asai et al. 2024; Batut et al. 2023; Chemin & Wasmer 2009; Collewet & Sauermann 2017; Crépon & Kramarz 2002; Crépon et al. 2004; Estevão & Sá 2008; Eurostat hlth_rs_prs2, 2026; Eurostat lfsi_emp_a, 2026; Eurostat lfsi_long_a, 2026; Eurostat lfsi_sla_a, 2026; Eurostat nama_10_a64, 2026; Eurostat nama_10_a64_e, 2026; Gubian et al. 2004; Hunt 1999; Pencavel 2015.

<!-- refs:end -->

## 4. Money under UNIRA's own rules

UNIRA's money rules are internally consistent once personal money is capped. Without the cap, fixed prices and high saving produce an ever-growing pile of unspent money.

- **Model:** a stock-flow-consistent circuit for the France region, with households, enterprises, the regional fund and the One Earth entity. Every U has a sender and a receiver (11 accounting checks).
- **Fixed price:** one price per hour of embodied work, set once so that household spending buys exactly the goods available. A base worker (2,500 U/month after saving) buys 86% of an average French person's consumption today.
- **Housing:** one base earner saving 50% buys a 100,000 U home in 3.3 years; two average earners buy a 300,000 U home in 2.6 years. A home costing about €200,000 to build today embodies about 3,600 hours of work, roughly 525,000 U at the fixed price, which is at the top of the 100,000–500,000 U range.
- **Experience creep:** if average pay drifts up 0.5% a year without matching productivity, demand exceeds supply by 13% after 30 years. Pay growth must track productivity.

| 60-year simulation, 6,000 adults | No cap | Cap ≈ 1.4 years of base salary + zero-interest home credit |
| --- | --- | --- |
| Unspent money (months of consumption) | 152, still rising | 12, stable |
| Flow to One Earth (share of regional consumption) | ~0% | ~20–23% a year |
| Adults at the cap | — | 57% |
| Work week with +1%/yr productivity | 30 h → 23 h after 30 years | 30 h → 23 h after 30 years |

Proposals provisionally accepted:

- **P1:** an inherited home beyond the heir's first returns to the regional pool. In simulation, second homes came mainly from inheritance.
- **P2:** a low money cap combined with zero-interest home credit.
- **P3:** guaranteed public housing for adults without a salary.

Behavioural parameters are assumptions; no UNIRA economy has been observed.

## 5. Is there enough for everyone on Earth?

On today's production, a decent life for all is possible for food and energy. A comfortable life for all is possible with half the food waste, but not at EU energy use or with today's health workforce.

*(Chart: world supply divided by world need, see the dashboard charts.)*

- **Method:** needs × population against current world supply, in physical units. Thresholds come from the decent-living literature (food 2,100 / 2,470 kcal eaten; energy 15.3 / 40 GJ final per person per year) and from WHO and the EU (44.5 / 131 health workers per 10,000).
- **Distribution:** moving about 7% of world food supply covers everyone. Energy, health workers and homes cannot be shipped; they must be built or trained where people live.
- **Health:** the WHO-level ratio above 1.0 is misleading. 4.2 bn people live in regions below that level today, because workers cannot be redistributed.
- **Labour:** universal work at 30 h (80% of ages 15–64) gives 0.88× today's world working hours.
- **Equal shares:** France's final energy would fall about 43% (90 → 51 GJ per person), still above the comfortable level. Nigeria's would rise 9×.

<!-- refs:begin sources §5 -->

*Sources for this section:* Eurostat n.d.c; Food & Nations n.d.a; International Labour Organization HOW_TEMP_SEX_NB_A, 2026; Millward-Hopkins et al. 2020; Our World in Data n.d.b; United Nations Environment Programme 2024; World Health Organization 2016; World Health Organization 2026d.

<!-- refs:end -->

## 6. Within Earth's limits: ecology, health care, housing

A comfortable life for 9.7 bn people in 2050 fits a 1.5 °C pathway (with temporary overshoot) and 2 °C comfortably. The binding limits are materials, health-worker training and home building.

**Ecology (2050, per person per year)**

|  | Sustainable range (low / central / high) | Today |
| --- | --- | --- |
| Final energy, 1.5 °C-class | 25 / 35 / 42 GJ | ~55 GJ |
| CO₂ | net 0 / 0.35 gross / 1.7 t (2 °C) | 5.2 t |
| Cropland | 1,346 / 1,636 / 1,816 m² | ~2,000 m² |
| Material footprint | 3 / 5.2 / 8 t | 14.2 t |

40 GJ for everyone totals 386 EJ in 2050, 6–13% less than the world uses today (409 EJ in the UNIRA model, 442 EJ per the IEA), and inside the IPCC 1.5 °C range. The conditions:

- about half of final energy as electricity;
- fossil CO₂ near zero by 2050;
- solar and wind built 1.7–1.9× faster than the 2025 record of 669 GW.

Material use per person must fall 2.7×, which UNIRA's stock-first, repair and no-overproduction rules target directly.

**Health workers.** The world has 47.4 m (58 per 10,000) and needs about 107 m at the EU level. Years until everyone has EU-level care, by training capacity (low / central / high):

| Scenario | Years |
| --- | --- |
| Training as today | never |
| Training +7%/yr for 15 years | never / 37 / 27 |
| + 25% of 27.4 m soldiers volunteer (no wars) | never / 36 / 25 |
| + healthier lives, central (−3% need) | never / 34 / 24 |
| Ambitious: +10%/yr, 50% of soldiers, strong prevention (−14%) | 42 / 23 / 18 |

Schools and teachers are the bottleneck. Disarmament helps most early: 71 vs 64 per 10,000 by year 10. On the evidence, better lives cut health-worker need only 3–14% after 30 years. About 41–48% of disease is linked to modifiable risks, but longer lives add later care.

**Housing.** World residential floor area averages about 26 m² per person: 7 in Ethiopia, 10.5 in India, 45 in France, 55 in the USA. Decent space for all (15 m²) needs about 13 bn m² of new homes; comfortable space (27 m²) about 65 bn m², mostly in South Asia and Africa. Floor-area values are regional model estimates (IMAGE); no official country data exists.

<!-- refs:begin sources §6 -->

*Sources for this section:* Brauer et al. 2024; Deetman & others n.d.; Food & Nations 2023; Forster et al. 2025; International Energy Agency 2023b; International Renewable Energy Agency 2026; International Resource Panel 2024; IPCC 2022; Millward-Hopkins et al. 2020; Murray et al. 2020; O’Neill et al. 2018; Rockström et al. 2025; United Nations & Social Affairs WPP2024_Demographic_Indicators_Medium.csv.gz, 2024; World Bank 2026b; World Health Organization 2026c; World Health Organization 2026d.

<!-- refs:end -->

## 7. A 30-year world transition plan

In the central case, every region reaches comfortable energy (40 GJ) by year 27 and EU-level health care by year 30. Comfortable housing is only half done by year 30, because population growth adds about 40 bn m² of need.

*(Chart: share of the world shortfall closed over 30 years, see the dashboard charts.)*

Each year the One Earth entity gives new capacity to the regions furthest below the target (needs first):

- clean energy from solar and wind;
- health workers from the training plan, trained in-region;
- new homes from world construction capacity (3.3–4.7 bn m² a year in the model; for comparison, the world's residential floor area grew by a net 3.4 bn m² in 2024).

Food is redistributed at once, and waste is halved over 10 years. Regions above the target reduce energy use. Population follows the UN 2024 projection.

| Case | All regions at 40 GJ | All at 131 health workers per 10,000 | All at 27 m² | World final energy, year 30 |
| --- | --- | --- | --- | --- |
| Low: record solar+wind pace, today's training | not in 30 yrs | not in 30 yrs | not in 30 yrs | 380 EJ |
| Central: 1.2 TW/yr, ambitious training | year 27 | year 30 | not in 30 yrs (50% closed) | 390 EJ |
| Central + no wars (military energy freed) | year 27 | year 30 | not in 30 yrs | 400 EJ |
| High: 1.8 TW/yr, 4.7 bn m²/yr homes | year 27 | year 27 | year 27 | 383 EJ |

- **Climate:** to keep world energy at or below today's 409 EJ while poorer regions converge, regions above 40 GJ per person must cut energy use about **4% a year**. Without weapons production and military fuel (5.5% of global emissions, confirmed: SGR/CEOBS 2022), **3% a year** is enough.
- **Housing is the slowest domain:** at today's world building rate it takes more than 30 years. Closing the 65 bn m² backlog in 27 years needs about 4.7 bn m² a year, mostly in Africa and South Asia. Including population growth and upgrading (Section 10) raises the peak to 6–7 bn m² a year. Its labour need is 33–64 hours per m², against a world construction workforce of 294 m.
- **Convergence and decarbonisation compete for the same build.** The model sends all new clean energy to regions below 40 GJ. Measured afterwards (`v67/energy_budget_check.py`), convergence absorbs 178 of the 217 EJ a year built by year 30 in the central case. Only 39 EJ is left to replace fossil supply elsewhere, so final energy is about 75% clean by year 30 (assuming 19% clean today). Doing both, with fossil use near zero, needs the high build rate of about 1.8 TW a year, which leaves 147 EJ for replacement against 132 EJ needed. The central case therefore delivers convergence, not full decarbonisation.
- **Food** is feasible for everyone from year 1 by redistribution; comfortable diets follow as waste falls.

<!-- refs:begin sources §7 -->

*Sources for this section:* Eurostat n.d.c; International Labour Organization 2025; Millward-Hopkins et al. 2020; National Bureau of Statistics of China 2011; Parkinson & Cottrell 2022; Press Information Bureau, Government of India 2025; United Nations & Social Affairs WPP2024_Demographic_Indicators_Medium.csv.gz, 2024; United Nations Environment Programme et al. 2026.

<!-- refs:end -->

## 8. UNIRA versus a reformed market economy

With the same people, technology, capacities and targets, UNIRA's institutions close the world's gaps far faster than a reformed market economy. A market world would have to direct about 90% of new capacity by need to match UNIRA on energy and housing, and it would still lag on health.

The comparison reruns the labour ledger and the 30-year transition with only the institutions changed:

- **B (reformed market):** best-observed employment (84%), today's pattern of clean-energy investment (20% to developing economies excluding China, verified), modest cuts to market-specific activity, militaries kept.
- **B2 (ambitious cooperative market):** half of new capacity to regions in need, faster rich-region energy cuts.
- **C (UNIRA):** universal work (88%), needs-first allocation, no commercial competition, disarmament, and the ambitious health programme.

| Outcome | B | B2 | C (UNIRA) |
| --- | --- | --- | --- |
| France, year 1: extra output per hour needed | 5.0% | 5.0% | 0% |
| Everyone at 40 GJ by | not within 30 yrs | not within 30 yrs | year 27 |
| Everyone at EU-level care by | not within 30 yrs | not within 30 yrs | year 30 |
| Energy shortfall closed, year 15 | −14% (gap grows) | 14% | 60% |
| Health shortfall closed, year 15 | −4% | 4% | 38% |
| Housing shortfall closed, year 30 | −21% | 10% | 50% |

- **Allocation by need** is the most decisive single institution. On its own it brings every region to 40 GJ by year 27. It must come with restraint in rich regions, or world energy peaks at 453 EJ.
- **Universal work** and **removing commercial competition** each roughly halve France's year-1 gap; together they close it.
- **Health:** UNIRA's advantage comes from the scale of training, disarmament volunteers and prevention, not from allocation alone.
- **Boundary:** a market world directing 90% of new capacity by need reaches 40 GJ for all by year 29 but closes only 8% of the health gap by year 15. That level of direction would in practice be needs-first allocation.

The advantage is entirely institutional; no efficiency bonus is assumed. It holds only if UNIRA's institutions work as designed, which is the claim still to be tested.

<!-- refs:begin sources §8 -->

*Sources for this section:* International Energy Agency 2026; Millward-Hopkins et al. 2020.

<!-- refs:end -->

## 9. Can the One Earth entity allocate well enough?

UNIRA's advantage survives realistic governance failures. With typical errors and no safeguards it still beats the most ambitious market world. With strong safeguards it keeps about 85% of its ideal performance.

The allocator decides on *perceived* needs. Each failure is calibrated on 44 sourced observations:

- **measurement error:** 5–30% (census undercounts, poverty revisions);
- **data delays:** 1–5 years;
- **exaggeration:** 10–45% of regions inflate needs by 2–20% (China, Brazil);
- **leakage:** 3–15% with strong safeguards, 10–45% without (Uganda, India, Brazil, EU).

| Scenario (median of 30 runs) | Energy gap closed, yr 15 | Health, yr 15 | Housing, yr 30 |
| --- | --- | --- | --- |
| UNIRA, perfect allocation | 60% | 38% | 50% |
| UNIRA, strong safeguards | 52% | 34% | 40% |
| UNIRA, no safeguards | 36% | 24% | 19% |
| UNIRA, worst governance observed | 15% | 12% | −9% |
| Ambitious cooperative market (B2) | 14% | 4% | 10% |

- **Leakage is the decisive failure.** Measurement errors and exaggeration matter much less: errors average out across 179 regions, and audits catch exaggerators.
- **Safeguards with evidence behind them:**
    - independent audits (−8 pp leakage);
    - open publication of every allocation (Uganda: capture of school grants fell from about 80% to under 20%);
    - direct digital delivery (−19 to −24% in India), which UNIRA's digital U and invoice system provide by design;
    - community monitoring;
    - data less than a year old.
- **Sharpened falsification test:** if leakage cannot be kept well below about 45% and data delays under about 5 years, needs-first allocation is no better than a cooperative market.

**AI-assisted planning (V7.8).** The author's rule 32 proposes that an AI model helps decide the production needed. We backtested five forecasting methods out of sample on real history from 2010 to 2024 (UN population, FAO food, OWID energy, WHO health workers). The method was chosen on 2005–2009 data only.
- **Needs are highly predictable.** Population one year ahead has a median error of 0.10% (nearest-neighbour ML, against 0.20% for the best simple trend). Food supply per person has an error of about 1%.
- **ML helps for population, food and health workers, but not for short-term energy use**, where "same as last year" is best.
- **Rerunning the 30-year transition** with AI-forecast information costs at most 1% of progress against perfect information, while misreporting and 8% leakage cost 12–19%. Each point of leakage costs about one point of progress.
- **AI's main value is therefore integrity checking rather than prediction.** Health-worker forecasts are 3–6× less accurate in low-income regions, so fair AI planning requires better statistics there first.
- Article 3b of the draft constitution sets the conditions: AI advises and people decide; models are open and must beat simple benchmarks each year; fairness is tested per region; AI has no role in rights, sanctions or force.

**The missing designs and power safeguards (V7.9).** Five mechanisms had no tested design, and concentrated power was the largest political risk. Each was modelled or reviewed (`v79/`):
- **Allocation formula.** Closing every region's gap to the *decent* level before allocating toward comfortable levels brings every region to decent energy in 4 years instead of 8, decent health care in 7 instead of 12, and decent housing in 9 instead of 20. There is no loss on the comfortable goal. Planning where food comes from cuts transport by 69%.
- **Prices.** Pricing France's household basket by embodied hours alone would make fuels 79% and electricity 65% cheaper relative to other goods, so a physical resource surcharge is essential.
- **Desirable homes.** Points plus a public lottery houses 28% of high-need households within 5 years, against 0% under a queue, with no income gradient. The must-live-in rule cuts empty desirable homes to under 0.5%.
- **Money cap.** A thermostat limited to ±10% a year keeps unspent money within 10–14 months of consumption through shocks. The author chose a moderate cap of 1.5 years of base salary, with protected home (150,000 U) and retirement (120,000 U) accounts. This lowers the share of adults at the cap from 61% to 40% with little added shortage risk; a 5-year cap would raise the demand from a spending rush to +78% of a year's goods.
- **Innovation.** A review of 67 evidence rows supports open public research and prizes, and supports salary differences only when they are visibly earned. A fixed hour price would penalise teams that save hours, so they keep part of the saving for a limited time.
- **Power.** A stress test of 13 attack scenarios, backed by 48 evidence rows, found five legal routes to capture: emergencies, account freezes without a judge, unprotected amendment, a packable Court, and no exit procedure. 17 new articles close them.

The draft constitution now has 66 articles.

<!-- refs:begin sources §9 -->

*Sources for this section:* Avis et al. 2018; Banerjee et al. 2020; Chen et al. 2019; Drèze & Khera 2015; European Court of Auditors n.d.; Monasterio n.d.; Olken 2007; Reinikka & Svensson 2004a; Reinikka & Svensson 2004b; Revista Brasileira de Economia n.d.; Statistics South Africa 2012.

<!-- refs:end -->

## 10. Accelerating housing, and safeguards in the constitution

Comfortable homes for everyone (27 m² per person) are possible within about 27 years if building capacity in regions of need grows 5–10% a year. This requires low-carbon construction and a workforce of about 250 m builders at the peak.

| Housing plan | Everyone at 27 m² by | Gap closed, yr 15 | Embodied CO₂, 30 yrs | Peak builders |
| --- | --- | --- | --- | --- |
| Today's capacity | not within 30 yrs | 15% | 29 Gt | 87 m |
| +10%/yr, conventional concrete | year 27 | 70% | 43 Gt | 253 m |
| +10%/yr, stock-first, low-carbon | year 27 | 83% | 16 Gt | 265 m |
| +5%/yr, stock-first, low-carbon | year 27 | 54% | 15 Gt | 236 m |

- **Scale:** about 109 bn m² must be built or upgraded (65 bn backlog plus about 40 bn for population growth). The peak is about 6–7 bn m² a year, China's past rate per person.
- **Climate:** conventional concrete homes (about 400 kg CO₂e per m²) would take about a third of the remaining 1.5 °C budget. Low-carbon frames of bamboo, timber, vaults or low-cement concrete (about 150) cut that to about 12%.
- **Stock-first** (upgrading and extending existing homes, about 40% of the need, at about 40% of the materials) speeds the early years. Most of the need is missing space, so it cannot replace building. Empty homes in regions of need cover only about 0.5%.
- **Workforce:** the world has 294 m construction workers, about 116 m of them in South Asia and Africa. Universal work and training must roughly double the builders in those regions.

**Safeguards.** The governance results of section 9 are turned into draft constitutional Articles 13–20, each with its evidence and a measurable trigger:

- 13: a public register of every allocation;
- 14: an independent audit authority;
- 15: direct digital delivery and physical verification;
- 16: needs data less than a year old;
- 17: community monitoring and whistleblower protection;
- 18: anti-capture rules (asset declarations, the money cap for officials, rotation);
- 19: correction without cutting people's guaranteed rights;
- 20: a built-in falsification clause. Leakage above 25% or data older than 2 years forces a review; leakage above 45% for 3 years requires a democratic change of the allocation system.

The full article texts follow the paper (Appendix).

**Security and consumption (rule 20).** The author's hypothesis is that secure access reduces over-consumption. The evidence supports it for goods with natural satiation. In France, mobile calls levelled off at about 7 minutes a day after unlimited plans. Panic buying (toilet roll +181% in March 2020) is driven by scarcity. Cash transfers do not raise alcohol or tobacco spending. The evidence contradicts it for energy, travel and data: data use rose from 0.5 to 14 GB a month, and free transit raised trips 14–70%. In the model, a 20–30% energy rebound would raise peak world energy to 424–436 EJ, beyond the climate envelope. Energy, travel and data must therefore stay metered and priced per unit, never flat-rate.

<!-- refs:begin sources §10 -->

*Sources for this section:* Adworld.ie 2020; ARCEP 2015; ARCEP n.d.; Cats et al. 2017; Evans & Popova 2017; Forster et al. 2025; International Labour Organization 2025; Le Den et al. 2022; National Bureau of Statistics of China 2012; Social & (CSEP) n.d.; Sorrell et al. 2009; The Connexion n.d.; World Business Council for Sustainable Development & Arup 2021.

<!-- refs:end -->

## 11. The transition: voluntary joining, property, savings and debts

UNIRA can start with willing regions and grow. Compared with a reformed market world after 30 years, 86% of humanity lives in regions that gain materially by joining. Counting people rather than whole regions, and adding the 495 million people inside rich regions who are better off even at the lowest UNIRA salary, **about 92% of humanity is better off**. In rich regions, *average* energy use per person is 6–12% lower. That is a regional average, not a loss for everyone: no one in UNIRA falls below the comfortable level, and the reduction falls on the heaviest energy users. Inside rich regions, 44% of people are better off even at the lowest UNIRA salary, and the poorest tenth gains +74% to +446% (World Bank income shares, 31 of 33 regions).

- **Who gains:**
    - 146 regions with 86% of the world's people gain materially (Ethiopia +170%, Nigeria +136%, India +72%, Brazil +11%; China about neutral);
    - in 33 rich regions, average energy use per person is 6–12% lower (France −6%, USA and Japan −12%). Health care and housing are unchanged, and no resident falls below the comfortable level. Inside these regions 44% of people are better off even at the lowest UNIRA salary (see below).
- **A union of gainers alone** closes 20% of the energy gap by year 15, against 52% with the whole world. That is still more than the best market world (14%).
- **Lessons from history** (61 sourced findings):
    - Germany's 1990 conversion of all wages at a political 1:1 rate halved East German output within months, and more than 3 million jobs were lost;
    - giving property back to former owners slowed investment;
    - staged EU accession with transfers of 2–4% of recipient output worked (Poland: from 44% of the EU average income per person in 1995 to 81% in 2025, Eurostat);
    - small savings were protected at par;
    - capped debt relief freed poor countries' budgets (7.3% vs 1.9% of output).
- **Draft transition rules:**
    - staged, voluntary joining by referendum;
    - wages move directly onto the UNIRA scale, and essential prices are set from embodied work (no single exchange rate);
    - savings convert at local "basket parity"; amounts above the money cap go directly to the One Earth entity, with the cap phased in over 10 years and an anti-flight rule (author decision); homes are never transferred;
    - homes are never seized, and mortgages become zero-interest U credit;
    - enterprise owners receive their share in U under the same cap (compensation, not restitution);
    - all public debts of member regions are cancelled (author decision), with bonds held by savers and pension funds treated as protected savings; outside creditors are paid on a schedule until they join;
    - a democratic right to leave (author decision); energy, travel and data always metered per unit (Article 21).

**Completing the economy and the transition framework (V8.2–V8.3).**
- **Ordinary goods** follow orders and waiting lists: 96% of wishes are served within 3 months, against a market that prices out 19% of wishes, almost all among the poorer half.
- **Hard jobs** get hardship steps, shorter hours and better conditions: unwilling workers fall from 87% to 46%.
- **Investment** puts maintenance first.
- **A restaurant and a supermarket** balance their accounts with UNIRA prices and salaries.
- **Equal salaries on day one would demand twice what the world produces.** About three-quarters of household spending is local services that cannot be shipped.
- **The author adopted the D + Q + C framework:**
  - D: rights and essentials guaranteed in kind, independently of salaries;
  - Q: needs-based quotas only for genuinely scarce goods, relaxing automatically as supply grows;
  - C: salaries for local services converge with local capacity.
- **Results:** in the same simulated world, the hybrid gives the poorer half of humanity about a quarter more real consumption at first than converging salaries alone. It reaches 90% of today's French level 4–9 years sooner across sensitivity tests (goods shares 24–45%, diversion 8–15%, shipping limits). Equal salaries without the hybrid's design left most money unspendable.
- **Equality credits** did not improve real living standards and are kept for research only.
- **Constitution vs parameters:** the constitution holds the rights and principles (Article 10d, T-8). The salary amounts, reserves, shipping limits and convergence time remain research parameters.

**Essential infrastructure (V8.8).**
- **Who lacks access:** about 624 million people lack basic drinking water, 1.38 billion basic sanitation, and 1.92 billion safe water or clean cooking. The largest gaps are in India, Nigeria, Ethiopia, DR Congo, Pakistan, Indonesia and Bangladesh.
- **Resources are small:** decentralised solutions cost about USD 10–26 billion a year.
- **Delivery capacity is the constraint:** the number of trained people, working institutions, security, maintenance and adoption.
- **Timelines:** reaching 95% of the unserved within 15 years needs 2–4 times the best historical pace with peace; 5 years is not achievable.
- **Constitution:** the Global Essential Infrastructure Priority Rule (Article 10e) puts closing these gaps first, with repair, local solutions, training, local participation and independently verified delivery.

**The integrated living standard (V8.9).**
- **Dates** (every domain together, a person counted only when they have all of it, delivery measured as working services, conflicts not assumed to end):
  - **essential security:** 90% / 95% / 99% of humanity in years 17 / 29 / 53 (accelerated) and 25 / 43 / later (moderate);
  - **comfortable life:** 90% in year 69 (accelerated); 95% and 99% not within 80 years while today's conflicts last;
  - **if conflicts ended** (upper bound): years 14 / 21 / 32 and 44 / 51 / 57.
- **Bottlenecks:** health-worker training first, then clean-cooking supply chains, then conflict. For the comfortable level, local services in the poorest regions.
- **Never binding:** energy, materials and money.

<!-- refs:begin sources §11 -->

*Sources for this section:* Brainard & Perry 1991; Documents & Images n.d.a; Eurostat ilc_di01, 2026; Institut für Arbeitsmarkt- und Berufsforschung (IAB) 1998; International Monetary Fund 2019; Notes from Poland 2026; Polish Economic Institute 2019; Polish Investment \& Trade Agency n.d.; Wikipedia contributors n.d.b.

<!-- refs:end -->

## 12. Limitations and falsification tests

These results show that UNIRA's targets are physically possible under stated conditions. They do not show that people would behave as assumed, or that the institutions could be built.

**Main limitations**

- National and regional averages hide inequality inside countries.
- Floor area per person comes from a regional model; world health-graduate numbers are estimated from OECD ratios.
- Behavioural parameters are assumptions, since no UNIRA economy exists to observe. They include take-up of work, saving choices, response to the money cap, entrant productivity and voluntary military conversion.
- Euro-based input-output coefficients proxy physical structure; physical units (energy, materials, food mass) are still to come.
- Governance failures (section 9) are calibrated on transfer programmes; infrastructure, regional favouritism, correlated errors and political dynamics are not yet modelled.
- UNIRA's own institutions (the U transaction system, allocation bodies, democratic governance) need hours not yet counted.

**What would refute UNIRA's physical claims**

1. **Labour:** under universal work, employment rates cannot be raised above about 85% within a few years, and the output-per-hour response to a 30-hour week stays below 0.1.
2. **Money:** under the cap, people respond by spending rather than saving, and demand exceeds supply at fixed prices by more than reserve stocks can absorb.
3. **Health:** world training capacity cannot grow beyond about 1.5×, which would leave EU-level care for all out of reach for more than 50 years.
4. **Ecology:** clean-energy build rates stay below the 2025 record, or material use cannot be cut by at least 2× while homes and infrastructure are built.
5. **Housing:** world construction capacity is too small to add about 65 bn m² within a generation (section 7).
6. **Comparison:** a reformed market economy with the same resources reaches the same outcomes, so UNIRA adds no advantage beyond its assumptions.

<!-- refs:begin sources §12 -->

*Sources for this section:* Collewet & Sauermann 2017; OECD n.d..

<!-- refs:end -->

## 13. Conclusions and research agenda

On the physical evidence, UNIRA's core aim is achievable over about one generation: a comfortable life for everyone, a 30-hour week, within climate limits. It depends on six conditions, and today's European or US consumption for everyone is not one of them.

**The six conditions**

1. **Universal work:** about 88% employment among adults aged 20–64, which makes the 30-hour week hold at today's output from year 1.
2. **Less waste and a healthier diet,** so comfortable food for all fits within land limits.
3. **Clean-energy building at 1.2–1.8 TW a year,** with regions above 40 GJ per person cutting energy about 3–4% a year (3% once weapons production and military fuel stop).
4. **About 2.7× less material use per person,** through stock-first, repair and no overproduction.
5. **A world health-worker training programme lasting 20–30 years,** helped by disarmament volunteers and healthier lives.
6. **Growing home building 5–10% a year to about 6–7 bn m² a year, with low-carbon materials and about 250 m builders,** mostly in Africa and South Asia, well above today's net growth of the world's residential floor area, about 3.4 bn m² in 2024 (GlobalABC 2026).

**Money:** UNIRA's rules (fixed prices, 1×–5× pay, savings, a yearly money cap with surplus to the One Earth entity) form a consistent system of accounts. The money cap is essential.

**Next research**

- Design and pilot the safeguard institutions (audits, open allocation data, digital delivery, community monitoring) and test leakage in infrastructure, not only transfers.
- Physical-unit accounts for food, energy and materials.
- Construction capacity by region, and its labour and material needs.
- Evidence on take-up of guaranteed work.
- Governance and legitimacy of One Earth allocation.
- External review by economists, demographers, health-workforce and climate scientists.

<!-- refs:begin sources §13 -->

*Sources for this section:* Millward-Hopkins et al. 2020; O’Neill et al. 2018; Rockström et al. 2025; United Nations Environment Programme et al. 2026.

<!-- refs:end -->

## Sources and reproducibility

Every data source is frozen with its retrieval time and SHA-256 hash in a `raw_manifest.csv` beside it. The literature reviews list each value with its citation and whether it was read in fetched text.

| Area | Main sources | Where |
| --- | --- | --- |
| France labour, output | [Eurostat](https://ec.europa.eu/eurostat/web/main/data/database) national accounts (nama_10_a64_e, nama_10_a64), LFS (lfsa_ewhun2, lfsi_sla_a, lfsi_long_a); [INSEE](https://www.insee.fr/fr/statistiques/8733071) | `v62/`, `v63/flows/` |
| Input-output | Eurostat naio_10_cp1700 (France 2022, 2019) | `v63/io/` |
| Health workforce France | Eurostat hlth_rs_prs2, hlth_rs_grd2, hlth_rs_prshp2, jvs_a_rate_r2 | `v63/health/` |
| Population, households | Eurostat demo_pjan, lfst_hhnhtych, ilc_lvho02; [World Bank](https://data.worldbank.org/); UN WPP 2024 | `v64/`, `v65/data/`, `v66/data/` |
| World food, energy, health, labour | FAO food balance sheets; Our World in Data energy; WHO workforce; ILO modelled estimates | `v65/data/` |
| Decent and comfortable thresholds | Millward-Hopkins et al. 2020; Kikstra et al. 2021; Rao & Min 2018; WHO; Eurostat | `v65/thresholds/` |
| Ecology | IPCC AR6; Forster et al. 2025; IEA; EAT-Lancet; UNEP IRP; O'Neill et al. 2018 | `v66/ecology/` |
| Health prevention | GBD 2019/2021; WHO/ILO 2021; lifetime-cost studies | `v66/evidence_health/` |
| Hours and productivity | DARES/INSEE evaluations of the 35-hour week; Pencavel; Collewet & Sauermann; Asai et al. | `v62/audit/` |
| Construction capacity | see section 7 | `v66/construction/` |

To reproduce: unpack the package and run `python3 v63/run_all.py` (Python 3, standard library only). Independent audits are in `v62/audit/`.

## Appendix — UNIRA Constitution — Draft safeguard articles (Articles 13–21)

**Status:** draft proposal for the author's decision (2026-11-03). These articles extend Articles 11 (Responsible Production) and 12 (Universal Digital Transaction Integrity) of the master specification.

**Why they exist:** V6.9 showed that UNIRA's advantage over market economies depends on how well the One Earth entity allocates new capacity by need. With strong safeguards UNIRA keeps about 85% of its ideal performance. Without them it keeps about half. Under the worst governance ever observed it is no better than a cooperative market. Leakage, meaning resources that never reach the people they were meant for, is the decisive failure.

Each article gives the rule, the evidence behind it, and a **measurable trigger** that forces review when it fails.

---

### Article 13 — Public Allocation Register
1. Every allocation by the One Earth entity or a region must be published within 30 days in a free, machine-readable public register. That covers energy capacity, homes, health workers, food, materials and U transfers. Each entry states what was allocated, where, how much, when, and on which needs data and rule.
2. The register publishes amounts and places, never personal data. Article 12 privacy protections apply in full.
3. Anyone may download, analyse and publish the register without permission.

*Evidence:* when Uganda's newspapers published school-grant amounts, schools had received only 13% of the grants in 1991–95; once amounts were published, the share captured before reaching schools fell from about 80% to under 20% (Reinikka & Svensson 2004a, 2004b).
*Trigger:* any allocation missing from the register after 60 days is void until published.

### Article 14 — Independent Audit Authority
1. An Audit Authority, independent of the One Earth executive and of regional governments, audits allocations and delivery in every region every year, with random selection and unannounced inspections.
2. Its budget is fixed by the constitution as a share of allocated value and cannot be reduced by the bodies it audits.
3. All audit reports are published in full in the Public Allocation Register.

*Evidence:* random audits reduced missing expenditure by 8 percentage points (Indonesia, Olken) and corruption by about 8%, and by about 13% after repeated audits (Brazil, Avis, Ferraz & Finan 2018).
*Trigger:* measured leakage above 15% in any region for 2 consecutive years automatically starts an independent review of that region's allocation system.

### Article 15 — Direct Digital Delivery and Physical Verification
1. Payments for allocated work and materials go directly, in digital U through the transaction network of Article 12, to the enterprises and workers who deliver them, with no cash intermediaries.
2. Physical delivery (homes built, energy capacity installed, staff in post) is verified by independent inspection and by remote sensing where possible, before allocation is recorded as complete.

*Evidence:* direct electronic payments reduced leakage by 19–24% in India's public programmes.
*Trigger:* any project whose delivery cannot be verified within 12 months is reported in the register as undelivered.

### Article 16 — Timely and Honest Needs Data
1. An independent statistical office measures needs in every region (population, housing, energy, food, health workforce) and updates them at least once a year, with stated uncertainty.
2. Regions may not change measurement methods alone. Methods are public and comparable across regions.
3. Reported needs are checked against independent sources (censuses, satellite data, sample surveys).

*Evidence:* census undercounts of 10–19% by province (South Africa 2011); poverty data typically published 2 years late; local statistics inflated (China, about +1.7 percentage points of growth a year). In the V6.9 model, data delays and errors cost less than leakage, but delays above about 5 years remove UNIRA's advantage.
*Trigger:* if needs data for a region is more than 2 years old, that region's allocations are flagged for verification.

### Article 17 — Community Monitoring and Whistleblower Protection
1. Every community has the right to form a monitoring committee with access to the register and to delivery sites, and the power to flag irregularities to the Audit Authority.
2. People who report misuse are protected from retaliation. Retaliation is a serious offence.
3. Every person has the right to complain about an allocation and to receive a reasoned answer within 90 days, with appeal to an independent court.

*Evidence:* community monitoring of health services in Uganda reduced under-five deaths by 33% (Björkman & Svensson).

### Article 18 — Anti-Capture Rules for Officials
1. Officials of the One Earth entity, regional bodies and the Audit Authority are subject to the personal money cap (rule 18), like everyone else. Their assets and those of their households are declared publicly every year.
2. Allocation posts have fixed terms and rotation. No person may decide allocations to a region where they or close family hold an interest.
3. Officials found diverting resources lose office and are prosecuted before independent courts.

*Evidence:* elite capture of aid flows reached 7.5% at aid peaks (Andersen, Johannesen & Rijkers).

### Article 19 — Correction Without Punishing People
1. Resources found misallocated are recovered and reallocated by need within the next allocation cycle.
2. A region found misreporting loses priority for discretionary allocations until audits confirm honest reporting. **The guaranteed rights of its people are never reduced:** income guarantees, health care, education, food and housing.
3. The allocation rule itself is reviewed publicly every 5 years by the democratic assembly of the federation.

### Article 20 — Built-in Falsification Clause
The federation commits to measuring whether needs-first allocation is working, and to changing it if it is not:
1. World leakage, data age and delivery rates are published every year.
2. If world leakage exceeds **25%** or average needs data is older than **2 years**, the One Earth assembly must review the allocation system within one year.
3. If leakage exceeds **45%**, or data is older than **5 years**, for 3 consecutive years, needs-first allocation has lost its measured advantage over a cooperative market economy (UNIRA V6.9). The assembly must then adopt a reformed allocation system by democratic vote.

### Article 21 — Metering of Goods Without Natural Limits (author decision, 2026-11-03)
1. Energy, travel and data are always metered and paid per unit at the fixed UNIRA prices. They are never offered at a flat rate or without limit.
2. Food, basic goods and essential services, which people naturally stop wanting once needs are met, may be offered with secure, guaranteed access.

*Evidence (V7.1):* free or flat-rate access raises use of goods without natural satiation. Mobile data rose from 0.5 to 14 GB a month; free transit raised trips 14–70%; flat-rate heating uses about 30% more than metered heating. A 20–30% energy rebound would push world energy beyond the climate envelope.

---
*Evidence sources: `v69/evidence/evidence.md` (44 sourced rows). Model results: `v69/RESEARCH_NOTE.md`. All thresholds are proposals derived from the model and may be set differently by democratic decision.*

## Appendix — UNIRA transition rules — draft for the author's decision (2026-11-03)

**Principles kept:**
- voluntary joining;
- no seizure of homes and no forced relocation;
- the money cap (rule 18);
- needs-based allocation;
- rights are never reduced.

**Evidence:** `evidence/evidence.md` (61 findings on German reunification, EU enlargement, the euro, debt relief, land reforms, wealth taxes and household debt).
**Model:** `joining/run.py`.

### What the models show
- **86% of humanity (146 regions) gains materially by joining**, compared with a reformed market world after 30 years: Ethiopia +170%, Nigeria +136%, India +72%, Indonesia +54%, Brazil +11%. China is about neutral (+2%).
- **In 33 rich regions (14% of humanity), average energy use per person is 6–12% lower** (France −6%, USA and Japan −12%). This is a regional average, not a loss for every resident. Nobody falls below the comfortable level, health care and housing are unchanged, and inside them 44% of people, about 495 million, are better off even at the lowest UNIRA salary, with the poorest tenth gaining +74% to +446% (World Bank income shares, 31 of 33 regions). The reduction falls mainly on the highest consumers. For these regions as a whole, joining is worthwhile if peace, security, the 30-hour week and a stable climate are worth more than that average reduction.
- **A union of only the gaining regions works on its own resources, at about half speed.** By year 15 it closes 20% of the energy gap, 15% of the health gap and 25% of the housing gap by year 30, against 52%, 34% and 40% for the whole world. That still beats the best market world (14%, 4%, 10%). **UNIRA can start with willing regions and grow.**

### Draft rules

**T1. Voluntary, staged joining.**
1. A region joins by referendum.
2. Joining has three stages:
    - **observer:** shares data and builds the safeguard institutions of Articles 13–17;
    - **associate:** receives needs-based transfers and adopts the 30-hour week;
    - **full member:** adopts the U and the full rules.
3. Each stage has published entry criteria.

*Evidence:* the EU grew from 6 to 27 members through staged, rule-based accession. Net transfers of 1.9–4.0% of recipient output cost donors only 0.3–0.4% of theirs.

**T2. Wages and prices: no single "political" exchange rate.**
1. At full membership, wages move directly onto the UNIRA scale (5,000 U base × multiplier).
2. Prices of essentials are set from the work and resources they embody (V6.4), the same everywhere.
3. Living standards are therefore set by physical allocation by need, not by an exchange rate.

*Evidence:* German monetary union converted wages and prices 1:1 at a political rate. Within months East German output fell to about half the 1989 level and more than 3 million jobs were lost. UNIRA avoids converting a whole economy at one invented rate.

**T3. Savings converted at "basket parity", small savings protected, cap phased in over 10 years (author decision 2026-11-03).**
1. Existing savings convert to U so that they buy the same essential basket locally (food, housing, energy) after the change as before.
2. Savings up to the money cap convert in full and stay with their owner.
3. **Savings above the cap are transferred directly to the One Earth entity** (author decision; rule 18).
4. The cap phases in over **10 years**: it starts high and falls each year to its steady level (about 1.4 years of base salary).
5. **Homes are not money and are never transferred** (T4).
6. **Anti-flight rule:** the cap applies to wealth held on the day a region votes to join. Transfers abroad after the vote count as held.

*Risk noted:* direct transfer is legally and politically harder than compensation in bonds. Wealthy holders may try to move wealth out before a vote (France lost 843 wealthy taxpayers in 2006; Norway at least 30 in 2022). The anti-flight rule and the 10-year phase-in reduce this risk but do not remove it.

*Evidence:* Germany protected small savings at 1:1 (up to 2,000–6,000 marks by age) and converted the rest at 2:1. Taiwan compensated landowners with 70% bonds and 30% shares, which worked. Japan paid in money that inflation eroded (under 1,000 yen per unit against a market value of about 20,000), which was unjust.

**T4. Homes are never seized.**
1. Homes people live in are kept.
2. The two-home maximum (rule 11) applies to new purchases.
3. Homes beyond two may be sold to the regional pool at the fixed price within a transition period (e.g. 10 years), paid in U or bonds, or passed on under P1.
4. Mortgages convert to zero-interest U credit at basket parity, repaid from salary.

*Evidence:* Iceland (2014) and Hungary (2014) converted or reduced household mortgages without systemic collapse.

**T5. Enterprises: compensation, not restitution.**
1. Enterprises become cooperative or public enterprises under UNIRA rules: owner pay capped at 5× base, and surplus to the region.
2. Owners receive their share in U, under the same money-cap rules as savings (T3). Any excess goes to the One Earth entity over the 10-year phase-in.
3. Old property claims from past regimes are settled by compensation, never by giving property back.

*Evidence:* Germany's 1990 "restitution before compensation" principle tied up property and slowed investment. The Treuhand privatisation agency closed with a DM 256 bn deficit.

**T6. No public debts (author decision 2026-11-03).**
1. At full membership, **all public debts of member regions are cancelled.** Inside one world entity, debts between regions would be the entity owing money to itself.
2. **Ordinary savers and pensioners are protected.** Government bonds held by households, pension funds and banks on behalf of savers are treated as those people's savings under T3: kept up to the money cap, the rest to the One Earth entity. Pension promises are replaced by UNIRA's needs-based retirement income (rule 15).
3. **Debts owed to creditors outside UNIRA** are paid by the One Earth entity on a negotiated schedule until the creditors' regions join. This avoids asset seizures and trade blockades against new members. When the whole world has joined, no public debt remains anywhere.

*Evidence:* debt relief for heavily indebted poor countries (USD 76 bn + 43 bn) let them spend 7.3% of output on poverty reduction against 1.9% on debt service. UNCTAD reports that about 3.3 billion people live in countries that spend more on interest than on health or education (UNCTAD, *A World of Debt*, 2023). Unilateral defaults on outside creditors have historically triggered litigation and asset seizures, which is why external debts are honoured until creditors join.

**T7. Right to leave, and the money cap.**
1. A region may leave by democratic decision, with a negotiated settlement.
2. Every person has the right to emigrate.
3. A person who emigrates keeps their money up to the cap. Wealth above the cap has already been transferred under T3. (Author decision 2026-11-03: the right to leave is confirmed.)

*Evidence:* wealth taxes leak when the wealthy can move their wealth out: France lost 843 wealthy taxpayers in 2006 (net €2.8 bn), and Norway saw at least 30 leave in 2022. A bond schedule protects the cap without trapping people.

**T8. Protect production during the change.**
1. New members keep their productive capacity running through transitional support from the union.
2. Trade with non-member regions continues at negotiated prices.

*Evidence:* in East Germany only 8% of workers were in firms that could cover their costs after the 1990 conversion. The lesson is to protect production, not let a currency shock destroy it.

### Author decisions (2026-11-03)
1. Money cap phase-in: **10 years**.
2. Savings above the cap: **transferred directly to the One Earth entity**.
3. Regions may leave: **yes**, by democratic vote.
4. Energy, travel and data are **always metered per unit** (Article 21).
5. **No public debts:** all member regions' public debts are cancelled; savers and pensioners are protected; outside creditors are paid on a schedule until they join (T6).

### Distribution inside rich regions (V7.4, `v74/distribution`)
National averages hide who gains. UNIRA's salaries and fixed prices are the same everywhere, so every region is compared with the same absolute basket. The **lowest** UNIRA salary (base worker saving the maximum 50%) buys about 86% of today's average French household consumption, about $21,900 per person a year at 2021 purchasing-power prices (World Bank). Using World Bank income shares (latest year 2019–2024) for 31 of the 33 regions whose average falls, **44% of their people, about 495 million, are already better off at that level**. This ranges from 22–24% in Norway and the USA, where average consumption is highest, to 50% in France, 56% in Japan and 75% in Czechia. **The poorest tenth gains +74% to +446%** (USA +154%, Japan +319%, France +186%, Germany +202%). These are lower bounds. Most workers earn above the lowest salary, and free health care, education and guaranteed housing come on top and are not counted; US households in particular pay much of their health care out of the consumption measured here. Fixed prices also end household price shocks such as the 2022 energy-price crisis. (`v74/distribution/world.py`; the Eurostat decile check for France gives the same 50%.)

**Most people earn more than the lowest salary.** The figures above count only people who are better off even at the *lowest* salary. Under UNIRA, salaries rise with experience, knowledge and job complexity (multipliers 1–5, average 1.9 in the money model, v64). The share of people in the rich regions whose consumption today is below what each UNIRA salary buys (still saving the maximum 50%) is:

| UNIRA salary | USA | Japan | France | Germany | Italy | Canada | Norway | All 31 rich regions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Lowest (1×) | 24% | 56% | 50% | 35% | 48% | 37% | 22% | **44%** |
| 1.5× | 42% | 82% | 77% | 64% | 73% | 67% | 54% | **67%** |
| Average (1.9×) | 54% | 88% | 87% | 79% | 85% | 80% | 73% | **77%** |
| Highest (5×) | 89% | 100% | 100% | 100% | 100% | 100% | 100% | **97%** |

- At the average UNIRA salary, about three in four people in the rich regions consume more than they do today. Free health care, education and guaranteed housing come on top.
- The highest salary covers almost everyone. The exception is the richest group in the most unequal regions: in the USA, about the richest tenth consumes more than even the highest UNIRA salary buys.
- The data come in tenths of the population, so the top 1% cannot be separated. They consume more than this, and they are the ones whose consumption UNIRA limits (at most two homes, the money cap, energy and travel paid per unit), while they still live comfortably.
- Source: `v74/distribution/world.py`, World Bank income shares applied to household consumption per person, PPP.

<!-- refs:begin reference list -->
## References

Author–year list of every source used in this paper (generated from `references/REFERENCES.bib`; the full bibliography of the project, with DOIs and verification notes, is in `references/`).

- Adworld.ie (2020). *Panic Buying Triggers 23% Growth in Retail Sales Says Nielsen*. https://www.adworld.ie/2020/03/27/panic-buying-triggers-23-growth-in-retail-sales-says-nielsen/ (accessed 2026-11-03)
- Aiken, L. H., Sloane, D. M., Bruyneel, L., Van den Heede, K., Griffiths, P., Busse, R., et al. (2014). Nurse staffing and education and hospital mortality in nine European countries: a retrospective observational study. *The Lancet*, *383*(9931), 1824–1830. https://doi.org/10.1016/S0140-6736(13)62631-8
- Andersen, J. J., Johannesen, N., & Rijkers, B. (2022). Elite Capture of Foreign Aid: Evidence from Offshore Bank Accounts. *Journal of Political Economy*, *130*(2), 388–425. https://doi.org/10.1086/717455
- ARCEP (2015). *Observatoire des marchés des communications électroniques, 1er trimestre 2015* [Data set]. https://www.arcep.fr/fileadmin/reprise/observatoire/1-2015/obs-marches-t1_2015.pdf (accessed 2026-11-03) *[not independently verified]*
- ARCEP (n.d.). *Le marché des communications électroniques en France en 2023 (résultats provisoires)* [Data set]. https://www.arcep.fr/cartes-et-donnees/nos-publications-chiffrees/observatoire-des-marches-des-communications-electroniques-en-france/marche-communications-electroniques-france-2023-resultats-provisoires.html (accessed 2026-11-03) *[not independently verified]*
- Asai, K., Lopes, M. C., & Tondini, A. (2024). *Firm-Level Effects of Reductions in Working Hours* (Working paper). Paris School of Economics. https://www.parisschoolofeconomics.eu/app/uploads/2024/11/asai-kentaro-firm-level-effects-of-reductions-in-working-hours.pdf (accessed 2026-11-03) *[not independently verified]*
- Avis, E., Ferraz, C., & Finan, F. (2018). Do Government Audits Reduce Corruption? Estimating the Impacts of Exposing Corrupt Politicians. *Journal of Political Economy*, *126*(5), 1912–1964. https://doi.org/10.1086/699209
- Banerjee, A., Duflo, E., Imbert, C., Mathew, S., & Pande, R. (2020). E-governance, Accountability, and Leakage in Public Programs: Experimental Evidence from a Financial Management Reform in India. *American Economic Journal: Applied Economics*, *12*(4), 39–72. https://doi.org/10.1257/app.20180302
- Batut, C., Garnero, A., & Tondini, A. (2023). The employment effects of working time reductions: Sector‐level evidence from European reforms. *Industrial Relations: A Journal of Economy and Society*, *62*(3), 217–232. https://doi.org/10.1111/irel.12323
- Björkman, M., & Svensson, J. (2009). Power to the People: Evidence from a Randomized Field Experiment on Community-Based Monitoring in Uganda*. *Quarterly Journal of Economics*, *124*(2), 735–769. https://doi.org/10.1162/qjec.2009.124.2.735
- Brainard, W. C., & Perry, G. L. (1991). Editors' Summary. *Brookings Papers on Economic Activity*, *1991*(1), ix. https://doi.org/10.2307/2534637
- Brauer, M., Roth, G. A., Aravkin, A. Y., Zheng, P., Abate, K. H., Abate, Y. H., et al. (2024). Global burden and strength of evidence for 88 risk factors in 204 countries and 811 subnational locations, 1990–2021: a systematic analysis for the Global Burden of Disease Study 2021. *The Lancet*, *403*(10440), 2162–2203. https://doi.org/10.1016/S0140-6736(24)00933-4
- Cats, O., Susilo, Y. O., & Reimal, T. (2017). The prospects of fare-free public transport: evidence from Tallinn. *Transportation*, *44*(5), 1083–1104. https://doi.org/10.1007/s11116-016-9695-5
- Centre for Social & Economic Progress (CSEP)} (n.d.). *India's housing paradox: Empty houses and housing shortages (policy brief)*. https://csep.org/policy-brief/indias-housing-paradox-empty-houses-and-housing-shortages/ (accessed 2026-11-03)
- Chemin, M., & Wasmer, E. (2009). Using Alsace‐Moselle Local Laws to Build a Difference‐in‐Differences Estimation Strategy of the Employment Effects of the 35‐Hour Workweek Regulation in France. *Journal of Labor Economics*, *27*(4), 487–524. https://doi.org/10.1086/605426
- Chen, W., Chen, X., Hsieh, C., & Song, Z. (2019). A Forensic Examination of China's National Accounts. *Brookings Papers on Economic Activity*, *2019*(1), 77–141. https://doi.org/10.1353/eca.2019.0001
- Collewet, M., & Sauermann, J. (2017). Working hours and productivity. *Labour Economics*, *47*, 96–106. https://doi.org/10.1016/j.labeco.2017.03.006
- Crépon, B., & Kramarz, F. (2002). Employed 40 Hours or Not Employed 39: Lessons from the 1982 Mandatory Reduction of the Workweek. *Journal of Political Economy*, *110*(6), 1355–1389. https://doi.org/10.1086/342807
- Crépon, B., Leclair, M., & Roux, S. (2004). RTT, productivité et emploi : nouvelles estimations sur données d'entreprises. *Economie et statistique*, *376*(1), 55–89. https://doi.org/10.3406/estat.2004.7234
- Deetman, S., et al. (n.d.). *BUMA: building material model – model inputs (IMAGE population, residential floor space per capita, rural population share)* [Data set]. https://github.com/SPDeetman/BUMA (accessed 2026-11-03) *[not independently verified]*
- Drèze, J., & Khera, R. (2015). *[Article on PDS leakage estimates]* [Economic and Political Weekly]. *[not independently verified]*
- Estevão, M., & Sá, F. (2008). The 35-hour workweek in France: Straightjacket or welfare improvement?. *Economic Policy*, *23*(55), 417–463. https://doi.org/10.1111/j.1468-0327.2008.00204.x
- European Court of Auditors (n.d.). *2023 EU audit in brief*. https://op.europa.eu/webpub/eca/audit-in-brief-2023/en/ (accessed 2026-11-03)
- Eurostat (2026). *Average usual weekly hours worked in the main job by professional status, full-time/part-time employment and economic activity (NACE Rev. 2) (2008-2026) (lfsa_ewhun2)* [Eurostat database (online data code lfsa_ewhun2)] [Data set]. https://doi.org/10.2908/LFSA_EWHUN2 https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_ewhun2 (accessed 2026-11-03)
- Eurostat (2026). *Distribution of income by quantiles (ilc_di01)* [Eurostat database (online data code ilc_di01)] [Data set]. https://doi.org/10.2908/ILC_DI01 https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_di01 (accessed 2026-11-03)
- Eurostat (2026). *Distribution of population by tenure status, type of household and income group (ilc_lvho02)* [Eurostat database (online data code ilc_lvho02)] [Data set]. https://doi.org/10.2908/ILC_LVHO02 https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_lvho02 (accessed 2026-11-03)
- Eurostat (2026). *Employment and labour force by sex and age - annual data (lfsi_emp_a)* [Eurostat database (online data code lfsi_emp_a)] [Data set]. https://doi.org/10.2908/LFSI_EMP_A https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsi_emp_a (accessed 2026-11-03)
- Eurostat (2026). *Employment by detailed industry (NACE Rev.2) - national accounts (nama_10_a64_e)* [Eurostat database (online data code nama_10_a64_e)] [Data set]. https://doi.org/10.2908/NAMA_10_A64_E https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_a64_e (accessed 2026-11-03)
- Eurostat (2026). *Gross value added and income by detailed industry (NACE Rev.2 ) (nama_10_a64)* [Eurostat database (online data code nama_10_a64)] [Data set]. https://doi.org/10.2908/NAMA_10_A64 https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_a64 (accessed 2026-11-03)
- Eurostat (2026). *Health graduates (hlth_rs_grd2)* [Eurostat database (online data code hlth_rs_grd2)] [Data set]. https://doi.org/10.2908/HLTH_RS_GRD2 https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/hlth_rs_grd2 (accessed 2026-11-03)
- Eurostat (2026). *Health personnel (hlth_rs_prs2)* [Eurostat database (online data code hlth_rs_prs2)] [Data set]. https://doi.org/10.2908/HLTH_RS_PRS2 https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/hlth_rs_prs2 (accessed 2026-11-03)
- Eurostat (2026). *Hospital employment (hlth_rs_prshp2)* [Eurostat database (online data code hlth_rs_prshp2)] [Data set]. https://doi.org/10.2908/HLTH_RS_PRSHP2 https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/hlth_rs_prshp2 (accessed 2026-11-03)
- Eurostat (2026). *Job vacancy rate by NACE Rev. 2 activity - annual data (2008-2025) (jvs_a_rate_r2)* [Eurostat database (online data code jvs_a_rate_r2)] [Data set]. https://doi.org/10.2908/JVS_A_RATE_R2 https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/jvs_a_rate_r2 (accessed 2026-11-03)
- Eurostat (2026). *Labour market slack by sex and age - annual data (lfsi_sla_a)* [Eurostat database (online data code lfsi_sla_a)] [Data set]. https://doi.org/10.2908/LFSI_SLA_A https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsi_sla_a (accessed 2026-11-03)
- Eurostat (2026). *Labour market transitions - annual data (lfsi_long_a)* [Eurostat database (online data code lfsi_long_a)] [Data set]. https://doi.org/10.2908/LFSI_LONG_A https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsi_long_a (accessed 2026-11-03)
- Eurostat (2026). *Population on 1 January by age and sex (demo_pjan)* [Eurostat database (online data code demo_pjan)] [Data set]. https://doi.org/10.2908/DEMO_PJAN https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_pjan (accessed 2026-11-03)
- Eurostat (2026). *Private households by household composition, number of children and age of youngest child (lfst_hhnhtych)* [Eurostat database (online data code lfst_hhnhtych)] [Data set]. https://doi.org/10.2908/LFST_HHNHTYCH https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfst_hhnhtych (accessed 2026-11-03)
- Eurostat (2026). *Symmetric input-output table at basic prices (product by product) (naio_10_cp1700)* [Eurostat database (online data code naio_10_cp1700)] [Data set]. https://doi.org/10.2908/NAIO_10_CP1700 https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/naio_10_cp1700 (accessed 2026-11-03)
- Eurostat (n.d.). *Eurostat database* [Data set]. https://ec.europa.eu/eurostat/web/main/data/database (accessed 2026-11-03) *[not independently verified]*
- Eurostat (n.d.). *Healthcare personnel statistics – physicians* [Statistics Explained] [Data set]. https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Healthcare_personnel_statistics_-_physicians (accessed 2026-11-03)
- Evans, D. K., & Popova, A. (2017). Cash Transfers and Temptation Goods. *Economic Development and Cultural Change*, *65*(2), 189–221. https://doi.org/10.1086/689575
- Food & Agriculture Organization of the United Nations} (2023). *FAOSTAT Analytical Brief 71 [land statistics]* (FAOSTAT Analytical Brief 71). FAO. https://openknowledge.fao.org/server/api/core/bitstreams/5c8b2707-1bcf-4c29-90e2-3487e583f71e/content (accessed 2026-11-03) *[not independently verified]*
- Food & Agriculture Organization of the United Nations} (n.d.). *FAOSTAT Food Balance Sheets (2010–), bulk download* [FAOSTAT] [Data set]. https://bulks-faostat.fao.org/production/FoodBalanceSheets_E_All_Data.zip (accessed 2026-11-03) *[not independently verified]*
- Food & Agriculture Organization of the United Nations} (n.d.). *SDG indicator 12.3.1a: Global food losses (SDG data portal)* [Data set]. https://www.fao.org/sustainable-development-goals-data-portal/data/indicators/1231-global-food-losses/en (accessed 2026-11-03)
- Forster, P. M., Smith, C., Walsh, T., Lamb, W. F., Lamboll, R., Cassou, C., et al. (2025). Indicators of Global Climate Change 2024: annual update of key indicators of the state of the climate system and human influence. *Earth System Science Data*, *17*(6), 2641–2680. https://doi.org/10.5194/essd-17-2641-2025
- German History in Documents & Images} (n.d.). *Closing the Treuhandanstalt [Trusteeship Agency] (December 30, 1994)*. https://germanhistorydocs.org/en/a-new-germany-1990-2023/closing-the-treuhandanstalt-trusteeship-agency-december-30-1994 (accessed 2026-11-03)
- German History in Documents & Images} (n.d.). *Unification and Property Issues (June 15, 1990)*. https://germanhistorydocs.org/en/a-new-germany-1990-2023/unification-and-property-issues-june-15-1990 (accessed 2026-11-03)
- Government of Iceland (2014). *Debt relief will reach 100,000 households (news, 26 March 2014)*. https://www.stjornarradid.is/frettir/grein/2014-03-26-Debt-Relief-Will-Reach-100-000-Households/ (accessed 2026-11-03) *[not independently verified]*
- Government of Iceland (2014). *Improved equity and debt position of 56,000 households (news, 10 November 2014)*. https://www.stjornarradid.is/frettir/grein/2014-11-10-Improved-equity-and-debt-position-of-56-000-households/ (accessed 2026-11-03) *[not independently verified]*
- Gubian, A., Jugnot, S., Lerais, F., & Passeron, V. (2004). Les effets de la RTT sur l'emploi : des estimations ex ante aux évaluations ex post. *Economie et statistique*, *376*(1), 25–54. https://doi.org/10.3406/estat.2004.7233
- HM Government of Gibraltar (2018). *Implementing Article 9(3) of the Energy Efficiency Directive: guidance note*. https://www.gibraltar.gov.gi/new/sites/default/files/HMGoG_Documents/20180501-Implementing_Article_9-3_EED_GuidanceNote.pdf (accessed 2026-11-03) *[not independently verified]*
- Hungarian Ministry for National Economy (2015). *Law on conversion of forex loans and fair banks enters into force (news, 3 February 2015)*. https://2015-2019.kormany.hu/en/ministry-for-national-economy/news/law-on-conversion-of-forex-loans-and-fair-banks-enters-into-force (accessed 2026-11-03)
- Hunt, J. (1999). Has Work-Sharing Worked in Germany?. *The Quarterly Journal of Economics*, *114*(1), 117–148. https://doi.org/10.1162/003355399555963
- INSEE (2026). *Emploi, chômage, revenus du travail – Édition 2026 (Insee Références): fiches « Évolution de l'emploi », « Durée du travail », « Temps partiel »* [Data set]. https://www.insee.fr/fr/statistiques/8733071?sommaire=8733125 (accessed 2026-11-03)
- Institut für Arbeitsmarkt- und Berufsforschung (IAB) (1998). *IAB Topics No. 29* (29). https://doku.iab.de/topics/1998/topics29.pdf (accessed 2026-11-03) *[not independently verified]*
- International Energy Agency (2023). *Net Zero Roadmap: A Global Pathway to Keep the 1.5 °C Goal in Reach – 2023 Update*. IEA. https://iea.blob.core.windows.net/assets/9a698da4-4002-4e53-8ef3-631d8971bf84/NetZeroRoadmap_AGlobalPathwaytoKeepthe1.5CGoalinReach-2023Update.pdf (accessed 2026-11-03) *[not independently verified]*
- International Energy Agency (2026). *World Energy Investment 2026*. IEA. https://www.iea.org/files/64594543-cf6e-4fd9-8238-d3cae35daf48/WorldEnergyInvestment2026.pdf (accessed 2026-11-03) *[not independently verified]*
- International Labour Office (1971). [Article on land reform in Japan]. *International Labour Review*, *103*(4), 393–413. https://webapps.ilo.org/public/libdoc/ilo/P/09602/09602(1971-103-4)393-413.pdf (accessed 2026-11-03) *[not independently verified]*
- International Labour Organization (2025). *Employment by sex and age – ILO modelled estimates, Nov. 2025 (EMP_2EMP_SEX_AGE_NB_A)* [ILOSTAT] [Data set]. https://rplumber.ilo.org/data/indicator/?id=EMP_2EMP_SEX_AGE_NB_A (accessed 2026-11-03)
- International Labour Organization (2025). *Employment by sex and economic activity – ILO modelled estimates, Nov. 2025 (EMP_2EMP_SEX_ECO_NB), construction aggregate* [ILOSTAT SDMX API] [Data set]. https://sdmx.ilo.org/rest/data/ILO,DF_EMP_2EMP_SEX_ECO_NB,1.0/.A..SEX_T.ECO_AGGREGATE_CON (accessed 2026-11-03)
- International Labour Organization (2026). *Average weekly hours actually worked per employed person by sex (HOW_TEMP_SEX_NB_A)* [ILOSTAT] [Data set]. https://rplumber.ilo.org/data/indicator/?id=HOW_TEMP_SEX_NB_A (accessed 2026-11-03)
- International Monetary Fund (2019). *Heavily Indebted Poor Countries (HIPC) Initiative and Multilateral Debt Relief Initiative (MDRI) – Statistical Update*. IMF. https://www.imf.org/-/media/files/publications/pp/2019/ppea2019028.pdf (accessed 2026-11-03) *[not independently verified]*
- International Renewable Energy Agency (2026). *Renewable Capacity Statistics 2026*. IRENA. https://bdd.pseau.org/outils/ouvrages/irena_renewable_capacity_statistics_2026_2026.pdf (accessed 2026-11-03) *[not independently verified]*
- International Resource Panel (2024). *Global Resources Outlook 2024 (press release)*. United Nations Environment Programme. https://resourcepanel.org/news-events/global-resources-outlook-2024-press-release (accessed 2026-11-03)
- IPCC (2022). Mitigation Pathways Compatible with Long-term Goals (Chapter 3). In *Climate Change 2022 -- Mitigation of Climate Change* (pp. 295–408). Cambridge University Press. https://doi.org/10.1017/9781009157926.005
- IPCC (n.d.). *Sixth Assessment Report (AR6) – generic reference; see ipcc2021wg1spm and ipcc2022wg3ch3*. https://www.ipcc.ch/assessment-report/ar6/ (accessed 2026-11-03) *[not independently verified]*
- Kikstra, J. S., Mastrucci, A., Min, J., Riahi, K., & Rao, N. D. (2021). Decent living gaps and energy needs around the world. *Environmental Research Letters*, *16*(9), 095006. https://doi.org/10.1088/1748-9326/ac1c27
- Le Den, X., Steinmann, J., Röck, M., Birgisdottir, H., Horup, L. H., Tozan, B., & Sørensen, A. (2022). *Towards embodied carbon benchmarks for buildings in Europe - Summary report*. Ramboll; Aalborg University (BUILD); KU Leuven. https://doi.org/10.5281/zenodo.6397514 https://vbn.aau.dk/ws/files/518613236/Towards_embodied_carbon_benchmarks_for_buildings_in_Europe.pdf
- Millward-Hopkins, J., Steinberger, J. K., Rao, N. D., & Oswald, Y. (2020). Providing decent living with minimum energy: A global scenario. *Global Environmental Change*, *65*, 102168. https://doi.org/10.1016/j.gloenvcha.2020.102168
- Monasterio, L. (n.d.). *O FPM e a Estranha Distribuição da População dos Pequenos Municípios Brasileiros* (Texto para Discussão 1818). IPEA. https://ideas.repec.org/p/ipe/ipetds/1818.html (accessed 2026-11-03)
- Murray, C. J. L., Aravkin, A. Y., Zheng, P., Abbafati, C., Abbas, K. M., Abbasi-Kangevari, M., et al. (2020). Global burden of 87 risk factors in 204 countries and territories, 1990–2019: a systematic analysis for the Global Burden of Disease Study 2019. *The Lancet*, *396*(10258), 1223–1249. https://doi.org/10.1016/S0140-6736(20)30752-2
- Narain, K. V. (1964). *Prosperity through free economy: a case study of Taiwan* [Republished by Indian Liberals]. https://indianliberals.in/primary-works/prosperity-through-free-enterprise-a-case-study-of-taiwan-by-kv-narain-november-9-1964/ (accessed 2026-11-03)
- National Bureau of Statistics of China (2011). *China Statistical Yearbook 2011, Table 15-2* [Data set]. https://www.stats.gov.cn/sj/ndsj/2011/html/O1502e.htm (accessed 2026-11-03) *[not independently verified]*
- National Bureau of Statistics of China (2012). *China Statistical Yearbook 2012, Table 10-35* [Data set]. https://www.stats.gov.cn/sj/ndsj/2012/html/J1035e.htm (accessed 2026-11-03) *[not independently verified]*
- Notes from Poland (2026). *Poland's wealth gap to EU average narrows to record low level*. https://notesfrompoland.com/2026/03/26/polands-wealth-gap-to-eu-average-narrows-to-record-low-level/ (accessed 2026-11-03) *[secondary source, to be replaced by a primary one]*
- OECD (n.d.). *OECD Health Statistics: health graduates (dataflow DSD_HEALTH_REAC_EMP@DF_GRAD)* [Data set]. https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_HEALTH_REAC_EMP@DF_GRAD,/all (accessed 2026-11-03) *[not independently verified]*
- Olken, B. A. (2007). Monitoring Corruption: Evidence from a Field Experiment in Indonesia. *Journal of Political Economy*, *115*(2), 200–249. https://doi.org/10.1086/517935
- Our World in Data (n.d.). *Energy dataset (owid-energy-data.csv; compiled from Energy Institute, Ember and EIA data)* [Data set]. https://github.com/owid/energy-data (accessed 2026-11-03) *[not independently verified]*
- O’Neill, D. W., Fanning, A. L., Lamb, W. F., & Steinberger, J. K. (2018). A good life for all within planetary boundaries. *Nature Sustainability*, *1*(2), 88–95. https://doi.org/10.1038/s41893-018-0021-4
- Parkinson, S., & Cottrell, L. (2022). *Estimating the Military's Global Greenhouse Gas Emissions*. Scientists for Global Responsibility (SGR) and Conflict and Environment Observatory (CEOBS). https://ceobs.org/wp-content/uploads/2022/11/SGRCEOBS-Estimating_Global_MIlitary_GHG_Emissions_Nov22_rev.pdf (accessed 2026-11-03) *[not independently verified]*
- Pega, F., Náfrádi, B., Momen, N. C., Ujita, Y., Streicher, K. N., Prüss-Üstün, A. M., et al. (2021). Global, regional, and national burdens of ischemic heart disease and stroke attributable to exposure to long working hours for 194 countries, 2000–2016: A systematic analysis from the WHO/ILO Joint Estimates of the Work-related Burden of Disease and Injury. *Environment International*, *154*, 106595. https://doi.org/10.1016/j.envint.2021.106595
- Pencavel, J. (2015). The Productivity of Working Hours. *The Economic Journal*, *125*(589), 2052–2076. https://doi.org/10.1111/ecoj.12166
- Polish Economic Institute (2019). *Cohesion report (Raport Spójność / Cohesion)*. https://pie.net.pl/wp-content/uploads/2019/09/PIE-Raport_Cohesion-Spojnosc-EN-red..pdf (accessed 2026-11-03) *[not independently verified]*
- Polish Investment \& Trade Agency (n.d.). *Poland's GDP is already 80% of the EU average*. https://www.trade.gov.pl/en/news/polands-gdp-is-already-80-of-the-eu-average (accessed 2026-11-03)
- Press Information Bureau, Government of India (2025). *Sapno Ka Ghar (factsheet on Pradhan Mantri Awas Yojana – Gramin)* [Data set]. https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/sep/doc2025924644801.pdf (accessed 2026-11-03) *[not independently verified]*
- Rao, N. D., & Min, J. (2018). Decent Living Standards: Material Prerequisites for Human Wellbeing. *Social Indicators Research*, *138*(1), 225–244. https://doi.org/10.1007/s11205-017-1650-0
- Reinikka, R., & Svensson, J. (2004). *The Power of Information: Evidence from a Newspaper Campaign to Reduce Capture*. World Bank. https://gsdrc.org/document-library/the-power-of-information-evidence-from-a-newspaper-campaign-to-reduce-capture/ (accessed 2026-11-03)
- Reinikka, R., & Svensson, J. (2004). Local Capture: Evidence from a Central Government Transfer Program in Uganda. *The Quarterly Journal of Economics*, *119*(2), 679–705. https://doi.org/10.1162/0033553041382120
- Revista Brasileira de Economia (n.d.). *Elasticity of population (mis)reporting in Brazilian municipalities: A census tale* [Revista Brasileira de Economia]. https://www.scielo.br/j/rbe/a/Js8zBWXCLTtxcYH5z7CPQkn/?lang=en (accessed 2026-11-03)
- Rockström, J., Thilsted, S. H., Willett, W. C., Gordon, L. J., Herrero, M., Hicks, C. C., et al. (2025). The EAT–Lancet Commission on healthy, sustainable, and just food systems. *The Lancet*, *406*(10512), 1625–1700. https://doi.org/10.1016/S0140-6736(25)01201-2
- Serajuddin, U., Uematsu, H., Wieser, C., Yoshida, N., & Dabalen, A. (2015). *Data Deprivation: Another Deprivation to End* (Policy Research Working Paper 7252). World Bank. http://documents1.worldbank.org/curated/en/700611468172787967/txt/WPS7252.txt (accessed 2026-11-03)
- Sorrell, S., Dimitropoulos, J., & Sommerville, M. (2009). Empirical estimates of the direct rebound effect: A review. *Energy Policy*, *37*(4), 1356–1371. https://doi.org/10.1016/j.enpol.2008.11.026
- Statistics South Africa (2012). *Census 2011 evaluation (presentation at the UNSD workshop, Kampala, 2012)*. https://unstats.un.org/unsd/demographic/meetings/wshops/Uganda/2012/docs/South%20Africa.pdf (accessed 2026-11-03) *[not independently verified]*
- SWI swissinfo.ch (n.d.). *Rich Norwegians flee to low-tax Switzerland as wealth levy bites*. https://www.swissinfo.ch/eng/business/rich-norwegians-flee-to-low-tax-switzerland-as-wealth-levy-bites/48140438 (accessed 2026-11-03) *[secondary source, to be replaced by a primary one]*
- The Connexion (n.d.). *Free buses prove successful in French town of Dunkirk*. https://connexionfrance.com/news/free-buses-prove-successful-in-french-town-of-dunkirk/426645 (accessed 2026-11-03) *[secondary source, to be replaced by a primary one]*
- UNCTAD (2023). *A World of Debt*. United Nations Conference on Trade and Development. https://www.un.org/sustainabledevelopment/blog/2023/07/press-release-un-warns-of-soaring-global-public-debt-a-record-92-trillion-in-2022-3-3-billion-people-now-live-in-countries-where-debt-interest-payments-are-greater-than-expenditure-on-health-or-edu (accessed 2026-11-03).
- United Nations Environment Programme (2024). *Food Waste Index Report 2024*. UNEP. https://www.unep.org/resources/publication/food-waste-index-report-2024 (accessed 2026-11-03) *[not independently verified]*
- United Nations Environment Programme, Global Alliance for Buildings, & Construction} (2026). *Building fast. Falling short. As climate risks rise and cities grow, we must rethink how we build to create better lives for all – Global Status Report for Buildings and Construction 2025/26*. https://doi.org/10.59117/20.500.11822/49531 https://build-up.ec.europa.eu/system/files/2026-06/mUPr9hKVkn_15_06_2026_152610.pdf
- United Nations, Department of Economic, & Social Affairs, P. D. (2024). *World Population Prospects 2024: Demographic indicators, medium variant (WPP2024_Demographic_Indicators_Medium.csv.gz)* [Data set]. https://population.un.org/wpp/ (accessed 2026-11-03) *[not independently verified]*
- Wikipedia contributors (n.d.). *East German mark* [Wikipedia, The Free Encyclopedia]. https://en.wikipedia.org/wiki/East_German_mark (accessed 2026-11-03) *[secondary source, to be replaced by a primary one]*
- Wikipedia contributors (n.d.). *Enlargement of the European Union* [Wikipedia, The Free Encyclopedia]. https://en.wikipedia.org/wiki/Enlargement_of_the_European_Union (accessed 2026-11-03) *[secondary source, to be replaced by a primary one]*
- Wikipedia contributors (n.d.). *Solidarity tax on wealth* [Wikipedia, The Free Encyclopedia]. https://en.wikipedia.org/wiki/Solidarity_tax_on_wealth (accessed 2026-11-03) *[secondary source, to be replaced by a primary one]*
- World Bank (2026). *Armed forces personnel, total (MS.MIL.TOTL.P1)* [World Development Indicators (indicator MS.MIL.TOTL.P1)] [Data set]. https://api.worldbank.org/v2/country/all/indicator/MS.MIL.TOTL.P1 (accessed 2026-11-03)
- World Bank (n.d.). *World Bank Open Data* [Data set]. https://data.worldbank.org/ (accessed 2026-11-03) *[not independently verified]*
- World Business Council for Sustainable Development & Arup (2021). *Net-zero buildings: Where do we stand?*. WBCSD. https://archive.wbcsd.org/contentwbc/download/12446/185553/1 (accessed 2026-11-03) *[not independently verified]*
- World Health Organization (2016). *Global strategy on human resources for health: Workforce 2030*. https://www.who.int/publications/i/item/9789241511131 (accessed 2026-11-03)
- World Health Organization (2026). *Medical doctors (number) [indicator HWF_0002]* [Global Health Observatory, National Health Workforce Accounts data (xMart public OData API)] [Data set]. https://xmart-api-public.who.int/GHO/FACT?$filter=INDICATOR_CODE eq 'HWF_0002' (accessed 2026-11-03)
- World Health Organization (2026). *Nursing and midwifery personnel (per 10 000 population) [indicator HWF_0006]* [Global Health Observatory, National Health Workforce Accounts data (xMart public OData API)] [Data set]. https://xmart-api-public.who.int/GHO/FACT?$filter=INDICATOR_CODE eq 'HWF_0006' (accessed 2026-11-03)

<!-- refs:end -->
