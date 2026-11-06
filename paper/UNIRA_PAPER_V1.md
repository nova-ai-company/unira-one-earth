# Is a one-world cooperative economy physically feasible? Evidence, validation and uncertainty for the UNIRA proposal

**Paper V1 — 4 November 2026. Preliminary; not peer reviewed.** This paper consolidates the physical-feasibility results of the UNIRA research (Working Paper 02, V6.2–V9.1) into one document, adds a historical backtest of its delivery model and a joint propagation of its uncertain assumptions, and states its claims at the strength the evidence supports. The normative design it tests is described separately (`concept/UNIRA_CONCEPT.md`); the legal text is the Draft Constitution of One Earth. An authorship disclosure is in section 12.

## Abstract

UNIRA proposes one democratic world federation in which today's countries become regions, resources go to regions by measured needs and population, every adult able to work works 30 hours a week, essentials have fixed prices and personal money is capped. We ask one question: is that world *physically* possible with the people, energy, food, land, materials, health workers and homes the Earth has? We do not ask whether it is politically achievable or whether people would behave as assumed.

Using frozen official data (Eurostat, INSEE, World Bank, FAO, WHO, ILO, UN population projections) and reproducible models, we find **no physical constraint that rules UNIRA out under stated conditions**, and six conditions that would have to hold: employment of about 88% of adults aged 20–64, food waste halved, clean energy built at 1.2–1.8 TW a year, material use per person cut about 2.7-fold, a 20–30-year health-worker training programme, and home building growing to 6–7 billion m² a year. In the central 30-year plan every region reaches 40 GJ of final energy per person by year 27 and EU-level health staffing by year 30, with world energy at or below today's level; comfortable housing is half done.

Two additions change how those results should be read. **Joint uncertainty:** when all uncertain assumptions of the 30-year plan are sampled together, energy for all within 30 years holds in 68% of cases, health in 66% and housing in 11%; when the assumptions of the later living-standard model are sampled together, essential security for 90% of humanity comes in year 26 (5–95% range 17–36), and a comfortable life for 95% of humanity is not reached within 80 years in any sampled case while today's conflicts persist. **Validation:** the delivery-pace rule used to project access to services reproduces 2012–2024 history to within 1–3 percentage points for water, sanitation and electricity when each country's own pace is extrapolated, but the faster "programme" paces it assumes over-predict by 10–25 points in conflict and fragile states unless delivery is discounted there.

The results are therefore a feasibility envelope, not a forecast. The design's central economic claims (fixed prices, planned production, a money cap) are shown to be internally consistent but rest on behavioural assumptions that no data can test before a pilot. All code, data and tests are open.

## 1. Introduction and scope

The UNIRA proposal is a design, set by its author, whose rules are treated here as normative premises (Table 1). The research question is narrow: **given today's physical resources and plausible rates of building, training and reorganisation, could the world described by these rules exist, and over what time?** The question is worth asking because objections to proposals of this kind are usually physical ("there is not enough energy", "you cannot train that many doctors", "housing cannot be built that fast") before they are political. We test the physical objections with official data and state the political and behavioural ones as untested.

| # | Premise (normative) | What this paper tests |
|---|---|---|
| 1 | A 30-hour week (6 h × 5 days) from year 1 | Hours lost and how they could be replaced (§3) |
| 2 | Results in hours and physical units, never in today's prices | All results are in hours, kcal, GJ, persons and m² |
| 3 | One world entity; countries become regions | Pooling of labour and production across regions |
| 4 | No commercial competition for profit; ideas still compete | Hours freed from market-specific activity (§3) |
| 5 | Resources allocated by needs × population | World sufficiency and the transition plan (§4–6) |
| 6 | Fixed prices for essentials; a base salary with multipliers up to 5×; a personal money cap | Internal consistency of the money circuit (§7.3) |
| 7 | Everyone able to work works; disarmament; health care and education free | Employment, freed labour and energy, training (§3, §5) |

What this paper does **not** show: that people would take up work at 88%, save and spend as assumed under a cap, report their needs honestly, or accept the premises; that the institutions could be built; or that the political path exists. Those limits are stated in §10 and in the concept document.

## 2. Data, methods and reproducibility

- **Sources.** Eurostat national accounts and Labour Force Survey; INSEE; World Bank World Development Indicators and governance indicators; FAO food balances; WHO health-workforce accounts; ILO; UN World Population Prospects 2024; Our World in Data energy (a republished series, marked for recheck); UCDP/PRIO conflict data; peer-reviewed literature on decent living, ecology and health.
- **Evidence classes.** Every figure is tagged as *verified official* (retrieved from the named table, SHA-256 hashed), *reported, needs recheck*, *model-derived*, *synthetic assumption* or *normative target*. Evidence files (`*/evidence.csv`) record, row by row, whether a figure was read in its source or taken from a search summary; a second verification pass on 4 November 2026 opened every source that had not been opened before and recorded every correction (`references/VERIFICATION_2026-11-04.csv`, §12).
- **Units.** Hours of work, kcal, GJ, persons and m². Euro-denominated input–output tables serve only as a technical proxy for physical interdependence; the U is never converted to euros.
- **Reproducibility.** Standard-library Python; frozen raw data; byte-identical reruns; about 270 automated tests; `python3 v63/run_all.py` regenerates every result, including those of this paper.
- **Earlier audits.** Four internal audits corrected the pre-V6.2 versions (stock-flow inconsistency in V5.6–5.7; a stress case that was the baseline; a 46-week convention that was not a 30-hour rule). A self-audit of 4 November 2026 (`v77/review/SELF_AUDIT_2026-11-04.md`) led to this consolidated paper, the validation of §9 and the uncertainty analysis of §6.4 and §8.

<!-- refs:begin sources §2 -->

*Sources for this section:* Food & Nations n.d.a; Our World in Data n.d.b; United Nations & Social Affairs WPP2024_Demographic_Indicators_Medium.csv.gz, 2024.

<!-- refs:end -->

## 3. Labour: a 30-hour week from year 1

**Baseline (France 2023, national accounts, all employed):** 45.6 billion hours, 1,501 hours per person employed. Capping employees' usual week at 30 hours removes 16.7% of hours, so output per hour would have to rise 20.1% to keep output constant (29.1% if the self-employed are also capped) — about 32 years of the 2015–19 productivity trend. Sector averages mislead: in health, education and public administration, annual hours are already below 1,380 because of part-time work, so full-time and part-time workers must be separated.

**Where the hours could come from.**

- *The labour reserve* (30 European countries): the unemployed, people available but not seeking, and underemployed part-timers could cover 51–59% of France's gap (43–50% EU-wide). But observed job-finding flows imply only about 0.53 million additional people in year 1 under today's institutions.
- *Hours and productivity*: evaluated reductions in working time (all cuts of 10% or less, from 39 hours or more) recover 10–35% of lost hours as higher hourly productivity in market sectors and 0–15% in care. Hours cuts alone create no net jobs without subsidies.
- *Market-specific activity* (advertising, speculative finance, real-estate intermediation) could free 1.7–6.6% of all hours. This is specific to UNIRA's premise 4.

| France, year 1, 30 h for employees | Output-per-hour gain still needed |
|---|---|
| Today's job-finding flows (central) | 10.2% |
| Employment rate 20–64 raised to 84% (best observed, Iceland 85.8% in 2025) | 2.6% |
| Employment rate raised to 88% (premise 7) | 0% |
| Europe pooled, 88% | 1.3% |

The 88% case needs workplaces for about 5 million new workers, childcare and eldercare, and an employment rate above any country's today. Health and care staffing stays short in year 1 (about 100,000 nurses and 145,000 care workers) because training takes years. The hours–productivity elasticities are extrapolated far beyond any evaluated reform; this is the first item reviewers should test.

<!-- refs:begin sources §3 -->

*Sources for this section:* Aiken et al. 2014; Asai et al. 2024; Batut et al. 2023; Chemin & Wasmer 2009; Collewet & Sauermann 2017; Crépon & Kramarz 2002; Crépon et al. 2004; Estevão & Sá 2008; Eurostat hlth_rs_prs2, 2026; Eurostat lfsi_emp_a, 2026; Eurostat lfsi_long_a, 2026; Eurostat lfsi_sla_a, 2026; Eurostat nama_10_a64, 2026; Eurostat nama_10_a64_e, 2026; Gubian et al. 2004; Hunt 1999; Pencavel 2015.

<!-- refs:end -->

## 4. Is there enough for everyone?

**Method.** Needs × population against current world supply, in physical units. Thresholds come from the decent-living literature and from WHO and EU staffing: food 2,100 (decent) / 2,470 (comfortable) kcal eaten per day; final energy 15.3 / 40 GJ per person per year; health workers 44.5 / 131 per 10,000 people.

**Results.**

- **Food.** Today's production covers a decent diet for all; a comfortable diet for all fits within land limits only with food waste halved. Moving about 7% of world food supply between regions covers everyone from year 1.
- **Energy.** A decent level for all is covered by today's supply. A comfortable level (40 GJ) for 9.7 billion people in 2050 totals about 386 EJ, 6–13% less than the world uses today (409 EJ in the model's data, 442 EJ per the IEA). Today's EU energy use for everyone is not possible within climate limits. Under equal shares, France's final energy would fall about 43% (90 to 51 GJ per person, still above the comfortable level) and Nigeria's would rise about 9-fold.
- **Health workers.** The world has 47.4 million (58 per 10,000) and would need about 107 million at the EU level. The world ratio above the WHO threshold is misleading: 4.2 billion people live in regions below it, and workers cannot be redistributed; they must be trained where people live.
- **Labour.** Universal work at 30 hours (80% of ages 15–64) gives 0.88 times today's world working hours.

Energy, health workers and homes cannot be shipped; they must be built or trained where people live. That is why the transition (§6) is about build rates, not totals.

<!-- refs:begin sources §4 -->

*Sources for this section:* Eurostat n.d.c; Food & Nations n.d.a; International Labour Organization HOW_TEMP_SEX_NB_A, 2026; Millward-Hopkins et al. 2020; Our World in Data n.d.b; United Nations Environment Programme 2024; World Health Organization 2016; World Health Organization 2026d.

<!-- refs:end -->

## 5. Earth's limits and the slow stocks

**Ecology (2050, per person per year).**

| | Sustainable range (low / central / high) | Today |
|---|---|---|
| Final energy, 1.5 °C-class | 25 / 35 / 42 GJ | about 55 GJ |
| CO₂ | net 0 / 0.35 gross / 1.7 t (2 °C) | 5.2 t |
| Cropland | 1,346 / 1,636 / 1,816 m² | about 2,000 m² |
| Material footprint | 3 / 5.2 / 8 t | 14.2 t |

40 GJ for everyone lies inside the IPCC 1.5 °C range if about half of final energy is electricity, fossil CO₂ is near zero by 2050, and solar and wind are built 1.7–1.9 times faster than the 2025 record (669 GW of solar and wind). Material use per person must fall about 2.7-fold, which the design's stock-first, repair and no-overproduction rules target but do not guarantee.

**Health workers.** Years until everyone has EU-level care, by world training capacity (low / central / high):

| Training scenario | Years |
|---|---|
| Training as today | never |
| Training +7% a year for 15 years | never / 37 / 27 |
| + 25% of 27.4 million soldiers volunteer (no wars) | never / 36 / 25 |
| + healthier lives, central (−3% need) | never / 34 / 24 |
| Ambitious: +10% a year, 50% of soldiers, strong prevention (−14%) | 42 / 23 / 18 |

Schools and teachers are the bottleneck. Disarmament helps most early (71 against 64 per 10,000 by year 10). On the evidence, healthier lives cut health-worker need only 3–14% after 30 years, because longer lives add later care.

*Levers (sensitivity on the ambitious case, central capacity; `v66/outputs/health_levers.json`):* lower yearly exits from 3% to 2% save 3 years (23 → 20); a training-capacity cap of 5× today's intake with +15% a year expansion saves 6 (→ 17); shorter courses save 1–2, because the intake cap binds, not the pipeline; all three together give 15 years (19 / 15 / 13 for low / central / high capacity). The target itself matters more than any lever: at 100 per 10,000 the central date is year 15, at 80 year 8. The 131 figure is the EU's staff density, not an outcome-based threshold; defining Level 2 health by outcomes, and the share of need that community health workers and care workers can meet, are open questions (§11). Essential care for everyone is a regional distribution problem: the world total already exceeds 44.5 per 10,000, and needs-first allocation of training brings every region to that level by year 6–7 (`v79/health_need`).

**Housing.** World residential floor area averages about 26 m² per person (7 in Ethiopia, 10.5 in India, 45 in France, 55 in the USA; regional model estimates, no official country data). Decent space for all (15 m²) needs about 13 billion m² of new homes; comfortable space (27 m²) about 65 billion m², mostly in South Asia and Africa. With population growth and upgrading, about 109 billion m² must be built or upgraded over a generation, a peak of 6–7 billion m² a year — China's past rate per person — against a net growth of the world's residential floor area of 3.4 billion m² in 2024. Conventional concrete homes would take about a third of the remaining 1.5 °C budget; low-carbon frames cut that to about 12%. The low-carbon value used (about 150 kg CO₂e per m²) comes from material studies of bamboo, compressed earth and timber construction; it is below the whole-building targets of UK guidance (LETI 300 and RIBA 625 kg CO₂e per m² for 2030), and an earlier citation of 144–201 as UK targets was a structures-only figure, corrected on 4 November 2026. The world has 294 million construction workers, 116 million of them in South Asia and Africa; the builders in those regions would roughly have to double.

<!-- refs:begin sources §5 -->

*Sources for this section:* Brauer et al. 2024; Deetman & others n.d.; Food & Nations 2023; Forster et al. 2025; International Energy Agency 2023b; International Renewable Energy Agency 2026; International Resource Panel 2024; IPCC 2022; Millward-Hopkins et al. 2020; Murray et al. 2020; O’Neill et al. 2018; Rockström et al. 2025; United Nations & Social Affairs WPP2024_Demographic_Indicators_Medium.csv.gz, 2024; World Bank 2026b; World Health Organization 2026c; World Health Organization 2026d.

<!-- refs:end -->

## 6. A 30-year world transition plan

Each year the One Earth entity gives new capacity to the regions furthest below the target (needs first): clean energy from solar and wind; health workers from the training plan, trained in-region; new homes from world construction capacity. Food is redistributed at once and waste halved over 10 years; regions above the energy target reduce their use; population follows the UN 2024 medium projection.

### 6.1 Scenario results

| Case | All regions at 40 GJ | All at 131 health workers per 10,000 | All at 27 m² | World final energy, year 30 |
|---|---|---|---|---|
| Low: record solar+wind pace (0.67 TW/yr), today's training | not in 30 yrs | not in 30 yrs | not in 30 yrs | 380 EJ |
| Central: 1.2 TW/yr, ambitious training | year 27 | year 30 | not in 30 yrs (50% closed) | 390 EJ |
| Central + no wars (military energy freed) | year 27 | year 30 | not in 30 yrs | 400 EJ |
| High: 1.8 TW/yr, 4.7 bn m²/yr homes | year 27 | year 27 | year 27 | 383 EJ |

### 6.2 What the plan requires

- **Restraint in rich regions.** To keep world energy at or below today's 409 EJ while poorer regions converge, regions above 40 GJ per person must cut energy use about 4% a year; 3% a year if weapons production and military fuel (5.5% of global emissions) stop.
- **Convergence and decarbonisation compete for the same build.** Convergence absorbs 178 of the 217 EJ a year built by year 30 in the central case, leaving 39 EJ to replace fossil supply elsewhere, so final energy is only about 75% clean by year 30. Doing both needs the high build rate of about 1.8 TW a year.
- **Housing is the slowest domain.** Closing the 65 billion m² backlog in 27 years needs about 4.7 billion m² a year; with population growth and upgrading, 6–7 billion m² a year, at 33–64 hours of labour per m².

### 6.3 One-at-a-time sensitivity

The results above are three hand-picked cases. The energy date depends almost entirely on the clean-energy build rate; the health date on training growth; the housing date on the share of world building sent to regions in deficit.

### 6.4 Joint uncertainty

To see what the plan looks like when nothing is hand-picked, 2,000 samples drew all uncertain assumptions together (`validation/uncertainty.py`): clean-energy build uniformly between the record pace and 1.8 TW a year (3.9–10.5 EJ/yr), the health training plan (low/central/high), home building capacity (low/central/high) and the share sent to regions in deficit (0.5–0.9), rich-region energy decline (2–5% a year), food waste after the transition (9.5–19%) and whether military energy is freed.

| Outcome | Median | 5–95% range | Share of samples reached within 30 years | Main driver (rank correlation) |
|---|---|---|---|---|
| Every region at 40 GJ | year 27 | 27–not reached | **68%** | clean-energy build (−0.88) |
| Every region at EU-level health staffing | year 30 | 27–not reached | **66%** | training plan (+0.51) |
| Every region at 27 m² | not reached | 28–not reached | **11%** | share of building to deficit regions (−0.41) |
| Peak world energy at or below today's 409 EJ | 409 EJ | 409–446 EJ | 70% | rich-region decline (−0.66), build rate (+0.47) |
| Energy shortfall closed by year 15 | 61% | 23–98% | — | build rate (+1.00) |
| Health shortfall closed by year 15 | 38% | 14–61% | — | training plan (−0.51) |
| Housing shortfall closed by year 30 | 52% | 14–100% | — | share to deficit regions (+0.73) |

The central case is therefore a median, not a safe bet: roughly one sample in three fails to bring every region to comfortable energy or health within 30 years, and nine in ten fail on housing. The model has no feedback between domains (a housing shortfall does not slow training), which is a simplification that probably makes these ranges too narrow.

<!-- refs:begin sources §6 -->

*Sources for this section:* Eurostat n.d.c; International Labour Organization 2025; Millward-Hopkins et al. 2020; National Bureau of Statistics of China 2011; Parkinson & Cottrell 2022; Press Information Bureau, Government of India 2025; United Nations & Social Affairs WPP2024_Demographic_Indicators_Medium.csv.gz, 2024; United Nations Environment Programme et al. 2026.

<!-- refs:end -->

## 7. Institutions: needs-first allocation, its failures, and money

### 7.1 Needs-first allocation against a reformed market economy

The labour ledger and the 30-year transition were rerun with only the institutions changed: **B** (reformed market: best-observed employment of 84%, today's pattern of clean-energy investment with 20% to developing economies excluding China, modest cuts to market-specific activity, militaries kept); **B2** (ambitious cooperative market: half of new capacity to regions in need, faster rich-region energy cuts); **C** (UNIRA: universal work at 88%, needs-first allocation, no commercial competition, disarmament, the ambitious health programme).

| Outcome | B | B2 | C (UNIRA) |
|---|---|---|---|
| France, year 1: extra output per hour needed | 5.0% | 5.0% | 0% |
| Everyone at 40 GJ by | not within 30 yrs | not within 30 yrs | year 27 |
| Everyone at EU-level care by | not within 30 yrs | not within 30 yrs | year 30 |
| Energy shortfall closed, year 15 | −14% (gap grows) | 14% | 60% |
| Health shortfall closed, year 15 | −4% | 4% | 38% |
| Housing shortfall closed, year 30 | −21% | 10% | 50% |

Allocation by need is the most decisive single institution: on its own it brings every region to 40 GJ by year 27, provided rich regions restrain their use (otherwise world energy peaks at 453 EJ). A market world would have to direct about 90% of its new capacity by need to match UNIRA on energy, and would still lag on health. The advantage is entirely institutional; no efficiency bonus is assumed. It holds only if the institutions work as designed, which is the claim still to be tested.

### 7.2 Governance failures

The allocator decides on *perceived* needs. Each failure is calibrated on 44 sourced observations of transfer programmes: measurement error 5–30%; data delays 1–5 years; exaggeration of needs by 10–45% of regions, by 2–20%; leakage of 3–15% with strong safeguards and 10–45% without (Uganda, India, Brazil, EU).

| Scenario (median of 30 runs) | Energy gap closed, yr 15 | Health, yr 15 | Housing, yr 30 |
|---|---|---|---|
| UNIRA, perfect allocation | 60% | 38% | 50% |
| UNIRA, strong safeguards | 52% | 34% | 40% |
| UNIRA, no safeguards | 36% | 24% | 19% |
| UNIRA, worst governance observed | 15% | 12% | −9% |
| Ambitious cooperative market (B2) | 14% | 4% | 10% |

Leakage is the decisive failure; measurement errors average out across 179 regions and audits catch exaggerators. Safeguards with evidence behind them: independent audits (about −8 percentage points of leakage in Brazil and Indonesia), open publication of every allocation (in Uganda, capture of school grants fell from about 80% to under 20%), direct digital delivery (−19 to −24% in India), community monitoring, and data less than a year old. A sharpened falsification test follows: if leakage cannot be kept well below about 45% and data delays under about 5 years, needs-first allocation is no better than a cooperative market.

**Planning information.** Five forecasting methods were backtested out of sample on 2010–2024 history (UN population, FAO food, OWID energy, WHO health workers), with the method chosen on 2005–2009 data only. Population one year ahead has a median error of 0.10% (nearest-neighbour method, against 0.20% for the best simple trend); food supply per person about 1%. Rerunning the 30-year transition with forecast rather than perfect information costs at most 1% of progress, while misreporting and 8% leakage cost 12–19%. Integrity, not prediction, is the binding information problem. Forecasts are 3–6 times less accurate in low-income regions.

### 7.3 Money: internal consistency only

A stock-flow-consistent circuit for the France region (households, enterprises, the regional fund, the One Earth entity; 11 accounting checks) shows that the money rules can be made consistent: one price per hour of embodied work, set once so that household spending buys exactly the goods available; a base worker (2,500 U a month after saving) buys 86% of an average French person's consumption today. Without a cap, fixed prices and high saving produce an ever-growing pile of unspent money (152 months of consumption after 60 years, still rising); with a cap of about 1.4 years of base salary and zero-interest home credit, unspent money stabilises at 12 months, and 20–23% of regional consumption flows each year to the One Earth entity. If pay drifts up 0.5% a year faster than productivity, demand exceeds supply by 13% after 30 years, so pay growth must track productivity.

These are consistency results. Every behavioural parameter in them — saving under a cap, work effort under 1–5× pay, the response to fixed prices — is an assumption, because no UNIRA economy has been observed.

<!-- refs:begin sources §7 -->

*Sources for this section:* Avis et al. 2018; Banerjee et al. 2020; Chen et al. 2019; Drèze & Khera 2015; European Court of Auditors n.d.; International Energy Agency 2026; Millward-Hopkins et al. 2020; Monasterio n.d.; Olken 2007; Reinikka & Svensson 2004a; Reinikka & Svensson 2004b; Revista Brasileira de Economia n.d.; Statistics South Africa 2012.

<!-- refs:end -->

## 8. Later extensions (preliminary)

Versions V8.2–V9.1 extended the research to the living-standard levels of the constitution, essential infrastructure, and conflict. Their evidence base was the weakest part of the project until the verification pass of 4 November 2026 (§12); they are reported here briefly, as preliminary.

**Living-standard dates.** Counting a person as served only when every domain is covered (water, sanitation, clean cooking, electricity, Internet, schooling, teachers, health workers, housing, energy, food, goods, local services, car access), with delivery measured as working services and today's conflicts not assumed to end, the "accelerated" scenario reaches essential security (Level 1) for 90 / 95 / 99% of humanity in years 17 / 29 / 53, and a comfortable life (Level 2) for 90% in year 72; 95% and 99% are not reached within 80 years. If all conflicts ended now (an upper bound), the dates are 14 / 21 / 32 and 47 / 54 / 59.

Sampling all 14 uncertain assumptions of that model together (400 samples: delivery pace percentile, automation, local-services catch-up, car production and sharing, first-year and mature functioning of new services, the share of people lacking shared cars, and the delivery factors in conflict and fragile countries):

| Outcome | Median year | 5–95% | Share reached within 80 years | Main drivers |
|---|---|---|---|---|
| Level 1 for 90% | 26 | 17–36 | 100% | delivery pace (−0.94), conflict factor (−0.25) |
| Level 1 for 95% | 47 | 28–not reached | 95% | delivery pace (−0.91), conflict factor (−0.32) |
| Level 1 for 99% | not reached | 50–not reached | 33% | delivery pace (−0.68), conflict factor (−0.42) |
| Level 2 for 90% | not reached | 68–not reached | 16% | conflict factor (−0.47), local-services catch-up (−0.43) |
| Level 2 for 95% | not reached | — | **0%** | — |

The accelerated scenario sits near the optimistic edge of that distribution. Under joint uncertainty, a comfortable life for 95% of humanity within 80 years requires conditions outside the sampled ranges, in practice the end of today's conflicts and faster growth of local services than any sampled value.

**Essential infrastructure.** About 624 million people lack basic drinking water, 1.38 billion basic sanitation, and 1.92 billion safe water or clean cooking. The resources are small (decentralised solutions about USD 10–26 billion a year at the model's unit costs; the verification pass found the model's sanitation unit cost at the low end of the IRC benchmarks, and raising it from 40 to 100 USD per person raises the total to about USD 17–28 billion a year); the binding limits are trained people, institutions, security and maintenance. Reaching 95% of the unserved within 15 years needs 2–4 times the best historical pace, with peace.

**Conflict.** Two historical panels (country-years 2000–2024, UCDP/PRIO) find that armed conflict is concentrated in the poorest quarter of countries (31% in conflict against 2–4%), and that institutional quality (World Bank governance indicators, excluding the violence indicator) predicts fewer onsets once living standards are controlled, while living standards add little once institutions are included. These are associations, not causes. In simulation, institutional reform at historical paces avoids about 15–40% of conflict-years over 80 years (strong reform: 38%, 5–95% range 24–49% under joint uncertainty), of which only about a quarter comes from the measured association and the rest from assumed mediation and relapse mechanisms. A first version of the conflict study attributed 13–26% of conflict-years to fair distribution; the second found that most of that pattern belonged to institutions, and the first estimate was withdrawn. Wars between states are outside these models.

## 9. Validation

**What was validated against history.**

- **The planning-information model** (§7.2): forecasting methods chosen on 2005–2009 data and tested on 2010–2024.
- **The delivery-pace rule** used by the living-standard models (`validation/backtest.py`). The rule projects each country's access to a service at the higher of its own measured pace and a percentile of all countries' gains, times delivery factors. Fitting on 2000–2012 and predicting 2024 for six services (water, sanitation, clean cooking, electricity, Internet, secondary enrolment):

| Variant | Mean absolute error (points) | Mean bias | World-coverage error (points) |
|---|---|---|---|
| Own pace only | 4.3 | −1.8 | −3.9 |
| Own pace or median gain (conservative) | 3.9 | +0.1 | −1.7 |
| Own pace or top-quarter gain (moderate) | 4.1 | +2.5 | +1.5 |
| Own pace or top-tenth gain (accelerated) | 5.6 | +5.1 | +4.6 |
| Moderate, with delivery factors (conflict 0.5, fragility 0.75) | 3.8 | +1.4 | +0.2 |

For water, sanitation and electricity, countries kept their pace (rank correlations 0.94, 0.96, 0.82 between 2000–12 and 2012–24 gains) and own-pace extrapolation is nearly unbiased (errors of 1–3 points). The percentile floors over-predict in conflict and fragile states by 10–25 points in some services unless the delivery factors are applied, which supports the factors. Internet use and secondary enrolment saturate (pace correlation −0.3 and 0.0; enrolment gains halved between the periods), so a linear rule is wrong for them. The floors describe programme effort beyond history, as the models say; the backtest shows that such effort was not sustained historically. A saturating (logistic) rule and empirically estimated delivery factors are the obvious improvements.

**What was not validated.** The 30-year transition model (§6), the market comparison (§7.1), the governance-failure model (§7.2) and the money circuit (§7.3) are calibrated on observed rates and literature ranges but cannot be tested against history, because no needs-first world allocation, universal work programme or capped money system has existed. Their results are conditional projections. The conflict models (§8) are calibrated to reproduce today's number of conflicts and are therefore not independent forecasts of it.

<!-- refs:begin sources §9 -->

*Sources for this section:* Food & Nations n.d.a; Our World in Data n.d.b; United Nations & Social Affairs WPP2024_Demographic_Indicators_Medium.csv.gz, 2024.

<!-- refs:end -->

## 10. Limitations and falsification tests

**Limitations of the evidence and methods.**

- National and regional averages hide inequality inside countries.
- Floor area per person comes from a regional model; world health-graduate numbers are estimated from OECD ratios; input–output coefficients are euro-based proxies for physical structure.
- Behavioural parameters are assumptions: take-up of work, saving under the cap, effort under 1–5× pay, entrant productivity, voluntary military conversion, honesty in reporting needs.
- Governance failures are calibrated on transfer programmes; infrastructure, regional favouritism, correlated errors and political dynamics are not modelled.
- The hours needed by UNIRA's own institutions (the payment system, allocation bodies, courts, audits) are only partly counted.
- The models have no feedback between domains, so joint uncertainty ranges are probably too narrow.
- **Verification corrections.** The 4 November 2026 pass changed no model parameter, but it corrected several evidence figures (sanitation unit costs, the safely-managed WASH range, the LETI/RIBA embodied-carbon figures, civil-war duration), found two figures that could not be located (an UN-Habitat slum share; a UK police-ratio "UN recommendation" that fact-checkers call a ghost statistic), and left a few corroborative figures unconfirmed (OECD 2025 staffing averages, WHO nursing-graduate rate, TNO earth-block emissions). None of these enters a headline result; all are listed in `references/PROBLEMS.md`.
- **Process.** The models and documents were produced in two days with an AI assistant (§12). Hundreds of modelling judgements were made quickly. The verification pass of 4 November 2026 found corrections in about a third of the previously unchecked references and in several evidence figures; more should be expected.

**What would refute the physical claims.**

1. **Labour:** under universal work, employment cannot be raised above about 85% within a few years, and the productivity response to a 30-hour week stays below 0.1.
2. **Money:** under the cap, people respond by spending rather than saving, and demand exceeds supply at fixed prices by more than reserve stocks can absorb.
3. **Health:** world training capacity cannot grow beyond about 1.5-fold, leaving EU-level care for all out of reach for more than 50 years.
4. **Ecology:** clean-energy build rates stay below the 2025 record, or material use cannot be cut at least 2-fold while homes and infrastructure are built.
5. **Housing:** world construction cannot add about 65 billion m² within a generation.
6. **Comparison:** a reformed market economy with the same resources reaches the same outcomes.
7. **Governance:** leakage cannot be kept below about 45% with data under five years old.
8. **Delivery:** the paces assumed for services in fragile states cannot be sustained even with the delivery factors applied (the backtest of §9 gives the first evidence on this).

<!-- refs:begin sources §10 -->

*Sources for this section:* Collewet & Sauermann 2017; OECD n.d..

<!-- refs:end -->

## 11. Conclusions

On the physical evidence, no constraint rules out a comfortable life for everyone, a 30-hour week and a world within climate limits over about one generation, **under six conditions**: universal work at about 88% employment; less waste and a healthier diet; clean energy built at 1.2–1.8 TW a year with rich regions cutting energy use 3–4% a year; about 2.7-fold less material use per person; a 20–30-year health-worker training programme; and home building growing to 6–7 billion m² a year with low-carbon materials. Today's European or US consumption for everyone is not one of the conditions: it is not possible.

Under joint uncertainty the central 30-year plan succeeds on energy and health in about two cases in three and on housing in one in nine; the last 10% of humanity, who live mostly in fragile and conflict-affected states, are the slowest to reach even essential security, and a comfortable life for 95% of humanity within 80 years requires conditions outside the sampled ranges. Needs-first allocation is the institution that matters most, and leakage is the failure that matters most.

What remains untested is everything behavioural and political: whether people would work, save and report as assumed; whether the institutions could be built and would hold; whether regions would join. Those questions need a pilot and independent review, not more modelling.

**Next steps.** Independent expert review (`v77/review/`); replacement of euro-based coefficients and regional estimates with physical-unit data (EXIOBASE, building stocks); a saturating delivery rule with estimated delivery factors; feedback between domains in the transition model; and the pilot design of `v80/pilot/`.

<!-- refs:begin sources §11 -->

*Sources for this section:* Millward-Hopkins et al. 2020; O’Neill et al. 2018; Rockström et al. 2025; United Nations Environment Programme et al. 2026.

<!-- refs:end -->

## 12. Author contributions, AI disclosure and data availability

**Author contributions.** The author of UNIRA set the purpose, the normative premises, every design decision recorded in `v63/DESIGN_CLARIFICATIONS_2026-11-03.md`, the research questions and the constitutional text, and reviewed and corrected results throughout. An AI assistant (Anthropic Claude; models Opus and Fable) drafted the models, code, tests, evidence files and documents, including this paper, under the author's direction, on 3–4 November 2026. No independent human expert has yet reviewed the work; the self-audit that led to this version is published with it.

**Verification status of the sources.** The project bibliography (`references/`) records for each of its 365 entries whether its bibliographic details were verified. On 4 November 2026 the 120 entries that had been taken from project files without checking were opened one by one: most were confirmed, about a quarter needed corrected titles, years or URLs, and a handful could not be located (`references/VERIFICATION_2026-11-04.csv`, `references/PROBLEMS.md`). Every evidence row of the newest work (V8.8, V9.0, V9.1) that rested on a search summary was read in its source; the corrections are recorded in the evidence files and summarised in the research notes.

**Data and code.** Everything is at `https://github.com/nova-ai-company/unira-one-earth` (MIT licence for code, CC BY 4.0 for text; data licences in `DATA_LICENSES.md`). `python3 v63/run_all.py` regenerates every result in this paper.

**Competing interests.** None declared. The author is the proponent of the design being tested; the research was structured to make its own refutation possible (evidence classes, falsification tests, open code), and readers should weigh the results accordingly.

<!-- refs:begin reference list -->
## References

Author–year list of the 57 sources cited in sections 2–11 (generated from `references/REFERENCES.bib`). 57 were verified against DOI metadata, a publisher or catalogue record or the landing page; 0 are marked *not independently verified*. A second verification pass on 4 November 2026 is recorded in `references/VERIFICATION_2026-11-04.csv`. Sources of the preliminary section 8 are listed row by row, with their verification status, in `v87/livingstandard/basket.json` and the `evidence.csv` files of `v88/`, `v90/` and `v91/`.

- Aiken, L. H., Sloane, D. M., Bruyneel, L., Van den Heede, K., Griffiths, P., Busse, R., et al. (2014). Nurse staffing and education and hospital mortality in nine European countries: a retrospective observational study. *The Lancet*, *383*(9931), 1824–1830. https://doi.org/10.1016/S0140-6736(13)62631-8
- Asai, K., Lopes, M. C., & Tondini, A. (2024). *Firm-Level Effects of Reductions in Working Hours* (Working paper). Paris School of Economics. https://www.parisschoolofeconomics.eu/app/uploads/2024/11/asai-kentaro-firm-level-effects-of-reductions-in-working-hours.pdf (accessed 2026-11-03)
- Avis, E., Ferraz, C., & Finan, F. (2018). Do Government Audits Reduce Corruption? Estimating the Impacts of Exposing Corrupt Politicians. *Journal of Political Economy*, *126*(5), 1912–1964. https://doi.org/10.1086/699209
- Banerjee, A., Duflo, E., Imbert, C., Mathew, S., & Pande, R. (2020). E-governance, Accountability, and Leakage in Public Programs: Experimental Evidence from a Financial Management Reform in India. *American Economic Journal: Applied Economics*, *12*(4), 39–72. https://doi.org/10.1257/app.20180302
- Batut, C., Garnero, A., & Tondini, A. (2023). The employment effects of working time reductions: Sector‐level evidence from European reforms. *Industrial Relations: A Journal of Economy and Society*, *62*(3), 217–232. https://doi.org/10.1111/irel.12323
- Brauer, M., Roth, G. A., Aravkin, A. Y., Zheng, P., Abate, K. H., Abate, Y. H., et al. (2024). Global burden and strength of evidence for 88 risk factors in 204 countries and 811 subnational locations, 1990–2021: a systematic analysis for the Global Burden of Disease Study 2021. *The Lancet*, *403*(10440), 2162–2203. https://doi.org/10.1016/S0140-6736(24)00933-4
- Chemin, M., & Wasmer, E. (2009). Using Alsace‐Moselle Local Laws to Build a Difference‐in‐Differences Estimation Strategy of the Employment Effects of the 35‐Hour Workweek Regulation in France. *Journal of Labor Economics*, *27*(4), 487–524. https://doi.org/10.1086/605426
- Chen, W., Chen, X., Hsieh, C., & Song, Z. (2019). A Forensic Examination of China's National Accounts. *Brookings Papers on Economic Activity*, *2019*(1), 77–141. https://doi.org/10.1353/eca.2019.0001
- Collewet, M., & Sauermann, J. (2017). Working hours and productivity. *Labour Economics*, *47*, 96–106. https://doi.org/10.1016/j.labeco.2017.03.006
- Crépon, B., & Kramarz, F. (2002). Employed 40 Hours or Not Employed 39: Lessons from the 1982 Mandatory Reduction of the Workweek. *Journal of Political Economy*, *110*(6), 1355–1389. https://doi.org/10.1086/342807
- Crépon, B., Leclair, M., & Roux, S. (2004). RTT, productivité et emploi : nouvelles estimations sur données d'entreprises. *Economie et statistique*, *376*(1), 55–89. https://doi.org/10.3406/estat.2004.7234
- Deetman, S., et al. (n.d.). *BUMA: building material model – model inputs (IMAGE population, residential floor space per capita, rural population share)* [Data set]. https://github.com/SPDeetman/BUMA (accessed 2026-11-03)
- Drèze, J., & Khera, R. (2015). *[Article on PDS leakage estimates]* [Economic and Political Weekly]. — *corrected 2026-11-04: Understanding Leakages in the Public Distribution System; 2015; https://web.iitd.ac.in/~suban/COP290/stuff/pds/Understanding_Leakages_in_the_Public_Distribution_System.pdf*
- Estevão, M., & Sá, F. (2008). The 35-hour workweek in France: Straightjacket or welfare improvement?. *Economic Policy*, *23*(55), 417–463. https://doi.org/10.1111/j.1468-0327.2008.00204.x
- European Court of Auditors (n.d.). *2023 EU audit in brief*. https://op.europa.eu/webpub/eca/audit-in-brief-2023/en/ (accessed 2026-11-03)
- Eurostat (2026). *Employment and labour force by sex and age - annual data (lfsi_emp_a)* [Eurostat database (online data code lfsi_emp_a)] [Data set]. https://doi.org/10.2908/LFSI_EMP_A https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsi_emp_a (accessed 2026-11-03)
- Eurostat (2026). *Employment by detailed industry (NACE Rev.2) - national accounts (nama_10_a64_e)* [Eurostat database (online data code nama_10_a64_e)] [Data set]. https://doi.org/10.2908/NAMA_10_A64_E https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_a64_e (accessed 2026-11-03)
- Eurostat (2026). *Gross value added and income by detailed industry (NACE Rev.2 ) (nama_10_a64)* [Eurostat database (online data code nama_10_a64)] [Data set]. https://doi.org/10.2908/NAMA_10_A64 https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_a64 (accessed 2026-11-03)
- Eurostat (2026). *Health personnel (hlth_rs_prs2)* [Eurostat database (online data code hlth_rs_prs2)] [Data set]. https://doi.org/10.2908/HLTH_RS_PRS2 https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/hlth_rs_prs2 (accessed 2026-11-03)
- Eurostat (2026). *Labour market slack by sex and age - annual data (lfsi_sla_a)* [Eurostat database (online data code lfsi_sla_a)] [Data set]. https://doi.org/10.2908/LFSI_SLA_A https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsi_sla_a (accessed 2026-11-03)
- Eurostat (2026). *Labour market transitions - annual data (lfsi_long_a)* [Eurostat database (online data code lfsi_long_a)] [Data set]. https://doi.org/10.2908/LFSI_LONG_A https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsi_long_a (accessed 2026-11-03)
- Eurostat (n.d.). *Healthcare personnel statistics – physicians* [Statistics Explained] [Data set]. https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Healthcare_personnel_statistics_-_physicians (accessed 2026-11-03)
- Food & Agriculture Organization of the United Nations} (2023). *FAOSTAT Analytical Brief 71 [land statistics]* (FAOSTAT Analytical Brief 71). FAO. https://openknowledge.fao.org/server/api/core/bitstreams/5c8b2707-1bcf-4c29-90e2-3487e583f71e/content (accessed 2026-11-03) — *corrected 2026-11-04: Land statistics and indicators 2000-2021: Global regional and country trends; 2023; https://openknowledge.fao.org/handle/20.500.14283/cc6907en*
- Food & Agriculture Organization of the United Nations} (n.d.). *FAOSTAT Food Balance Sheets (2010–), bulk download* [FAOSTAT] [Data set]. https://bulks-faostat.fao.org/production/FoodBalanceSheets_E_All_Data.zip (accessed 2026-11-03)
- Forster, P. M., Smith, C., Walsh, T., Lamb, W. F., Lamboll, R., Cassou, C., et al. (2025). Indicators of Global Climate Change 2024: annual update of key indicators of the state of the climate system and human influence. *Earth System Science Data*, *17*(6), 2641–2680. https://doi.org/10.5194/essd-17-2641-2025
- Gubian, A., Jugnot, S., Lerais, F., & Passeron, V. (2004). Les effets de la RTT sur l'emploi : des estimations ex ante aux évaluations ex post. *Economie et statistique*, *376*(1), 25–54. https://doi.org/10.3406/estat.2004.7233
- Hunt, J. (1999). Has Work-Sharing Worked in Germany?. *The Quarterly Journal of Economics*, *114*(1), 117–148. https://doi.org/10.1162/003355399555963
- International Energy Agency (2023). *Net Zero Roadmap: A Global Pathway to Keep the 1.5 °C Goal in Reach – 2023 Update*. IEA. https://iea.blob.core.windows.net/assets/9a698da4-4002-4e53-8ef3-631d8971bf84/NetZeroRoadmap_AGlobalPathwaytoKeepthe1.5CGoalinReach-2023Update.pdf (accessed 2026-11-03)
- International Energy Agency (2026). *World Energy Investment 2026*. IEA. https://www.iea.org/files/64594543-cf6e-4fd9-8238-d3cae35daf48/WorldEnergyInvestment2026.pdf (accessed 2026-11-03)
- International Labour Organization (2025). *Employment by sex and economic activity – ILO modelled estimates, Nov. 2025 (EMP_2EMP_SEX_ECO_NB), construction aggregate* [ILOSTAT SDMX API] [Data set]. https://sdmx.ilo.org/rest/data/ILO,DF_EMP_2EMP_SEX_ECO_NB,1.0/.A..SEX_T.ECO_AGGREGATE_CON (accessed 2026-11-03)
- International Labour Organization (2026). *Average weekly hours actually worked per employed person by sex (HOW_TEMP_SEX_NB_A)* [ILOSTAT] [Data set]. https://rplumber.ilo.org/data/indicator/?id=HOW_TEMP_SEX_NB_A (accessed 2026-11-03)
- International Renewable Energy Agency (2026). *Renewable Capacity Statistics 2026*. IRENA. https://bdd.pseau.org/outils/ouvrages/irena_renewable_capacity_statistics_2026_2026.pdf (accessed 2026-11-03)
- International Resource Panel (2024). *Global Resources Outlook 2024 (press release)*. United Nations Environment Programme. https://resourcepanel.org/news-events/global-resources-outlook-2024-press-release (accessed 2026-11-03)
- IPCC (2022). Mitigation Pathways Compatible with Long-term Goals (Chapter 3). In *Climate Change 2022 -- Mitigation of Climate Change* (pp. 295–408). Cambridge University Press. https://doi.org/10.1017/9781009157926.005
- Millward-Hopkins, J., Steinberger, J. K., Rao, N. D., & Oswald, Y. (2020). Providing decent living with minimum energy: A global scenario. *Global Environmental Change*, *65*, 102168. https://doi.org/10.1016/j.gloenvcha.2020.102168
- Monasterio, L. (n.d.). *O FPM e a Estranha Distribuição da População dos Pequenos Municípios Brasileiros* (Texto para Discussão 1818). IPEA. https://ideas.repec.org/p/ipe/ipetds/1818.html (accessed 2026-11-03)
- Murray, C. J. L., Aravkin, A. Y., Zheng, P., Abbafati, C., Abbas, K. M., Abbasi-Kangevari, M., et al. (2020). Global burden of 87 risk factors in 204 countries and territories, 1990–2019: a systematic analysis for the Global Burden of Disease Study 2019. *The Lancet*, *396*(10258), 1223–1249. https://doi.org/10.1016/S0140-6736(20)30752-2
- National Bureau of Statistics of China (2011). *China Statistical Yearbook 2011, Table 15-2* [Data set]. https://www.stats.gov.cn/sj/ndsj/2011/html/O1502e.htm (accessed 2026-11-03)
- OECD (n.d.). *OECD Health Statistics: health graduates (dataflow DSD_HEALTH_REAC_EMP@DF_GRAD)* [Data set]. https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_HEALTH_REAC_EMP@DF_GRAD,/all (accessed 2026-11-03)
- Olken, B. A. (2007). Monitoring Corruption: Evidence from a Field Experiment in Indonesia. *Journal of Political Economy*, *115*(2), 200–249. https://doi.org/10.1086/517935
- Our World in Data (n.d.). *Energy dataset (owid-energy-data.csv; compiled from Energy Institute, Ember and EIA data)* [Data set]. https://github.com/owid/energy-data (accessed 2026-11-03)
- O’Neill, D. W., Fanning, A. L., Lamb, W. F., & Steinberger, J. K. (2018). A good life for all within planetary boundaries. *Nature Sustainability*, *1*(2), 88–95. https://doi.org/10.1038/s41893-018-0021-4
- Parkinson, S., & Cottrell, L. (2022). *Estimating the Military's Global Greenhouse Gas Emissions*. Scientists for Global Responsibility (SGR) and Conflict and Environment Observatory (CEOBS). https://ceobs.org/wp-content/uploads/2022/11/SGRCEOBS-Estimating_Global_MIlitary_GHG_Emissions_Nov22_rev.pdf (accessed 2026-11-03)
- Pencavel, J. (2015). The Productivity of Working Hours. *The Economic Journal*, *125*(589), 2052–2076. https://doi.org/10.1111/ecoj.12166
- Press Information Bureau, Government of India (2025). *Sapno Ka Ghar (factsheet on Pradhan Mantri Awas Yojana – Gramin)* [Data set]. https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/sep/doc2025924644801.pdf (accessed 2026-11-03)
- Reinikka, R., & Svensson, J. (2004). *The Power of Information: Evidence from a Newspaper Campaign to Reduce Capture*. World Bank. https://gsdrc.org/document-library/the-power-of-information-evidence-from-a-newspaper-campaign-to-reduce-capture/ (accessed 2026-11-03)
- Reinikka, R., & Svensson, J. (2004). Local Capture: Evidence from a Central Government Transfer Program in Uganda. *The Quarterly Journal of Economics*, *119*(2), 679–705. https://doi.org/10.1162/0033553041382120
- Revista Brasileira de Economia (n.d.). *Elasticity of population (mis)reporting in Brazilian municipalities: A census tale* [Revista Brasileira de Economia]. https://www.scielo.br/j/rbe/a/Js8zBWXCLTtxcYH5z7CPQkn/?lang=en (accessed 2026-11-03)
- Rockström, J., Thilsted, S. H., Willett, W. C., Gordon, L. J., Herrero, M., Hicks, C. C., et al. (2025). The EAT–Lancet Commission on healthy, sustainable, and just food systems. *The Lancet*, *406*(10512), 1625–1700. https://doi.org/10.1016/S0140-6736(25)01201-2
- Statistics South Africa (2012). *Census 2011 evaluation (presentation at the UNSD workshop, Kampala, 2012)*. https://unstats.un.org/unsd/demographic/meetings/wshops/Uganda/2012/docs/South%20Africa.pdf (accessed 2026-11-03) — *corrected 2026-11-04: Evaluation of the South African population census 2011: a presentation for the UN Workshop on Census Evaluation, 12–16 November 2012, Kampala, Uganda; 2012; https://unstats.un.org/unsd/demographic/meetings/wshops/Uganda/2012/docs/South%20Africa.pdf*
- United Nations Environment Programme (2024). *Food Waste Index Report 2024*. UNEP. https://www.unep.org/resources/publication/food-waste-index-report-2024 (accessed 2026-11-03) — *corrected 2026-11-04: Food Waste Index Report 2024. Think Eat Save: Tracking Progress to Halve Global Food Waste; 2024 (March 2024); https://wedocs.unep.org/handle/20.500.11822/45230 ; https://www.unep.org/resources/publication/food-waste-index-report-2024 (both 403 to direct automated fetch; read via a text-reader proxy)*
- United Nations Environment Programme, Global Alliance for Buildings, & Construction} (2026). *Building fast. Falling short. As climate risks rise and cities grow, we must rethink how we build to create better lives for all – Global Status Report for Buildings and Construction 2025/26*. https://doi.org/10.59117/20.500.11822/49531 https://build-up.ec.europa.eu/system/files/2026-06/mUPr9hKVkn_15_06_2026_152610.pdf
- United Nations, Department of Economic, & Social Affairs, P. D. (2024). *World Population Prospects 2024: Demographic indicators, medium variant (WPP2024_Demographic_Indicators_Medium.csv.gz)* [Data set]. https://population.un.org/wpp/ (accessed 2026-11-03)
- World Bank (2026). *Armed forces personnel, total (MS.MIL.TOTL.P1)* [World Development Indicators (indicator MS.MIL.TOTL.P1)] [Data set]. https://api.worldbank.org/v2/country/all/indicator/MS.MIL.TOTL.P1 (accessed 2026-11-03)
- World Health Organization (2016). *Global strategy on human resources for health: Workforce 2030*. https://www.who.int/publications/i/item/9789241511131 (accessed 2026-11-03)
- World Health Organization (2026). *Medical doctors (number) [indicator HWF_0002]* [Global Health Observatory, National Health Workforce Accounts data (xMart public OData API)] [Data set]. https://xmart-api-public.who.int/GHO/FACT?$filter=INDICATOR_CODE eq 'HWF_0002' (accessed 2026-11-03)
- World Health Organization (2026). *Nursing and midwifery personnel (per 10 000 population) [indicator HWF_0006]* [Global Health Observatory, National Health Workforce Accounts data (xMart public OData API)] [Data set]. https://xmart-api-public.who.int/GHO/FACT?$filter=INDICATOR_CODE eq 'HWF_0006' (accessed 2026-11-03)

<!-- refs:end -->
