# UNIRA V7.9 — The missing designs, and safeguards against concentrated power

**Why:** the honest assessment after V7.8 listed what could make UNIRA fail. Two items are addressed here:
- **Five mechanisms were not yet designed:** the allocation formula, prices for new products, desirable homes, the yearly money cap, and motivation and innovation without profit.
- **Concentrated power** (arms, money and allocation in one entity) is the most dangerous risk.

The author approved six design proposals on 2026-11-03. Each is tested here, and each becomes constitution text.

| # | Design | Test | Folder |
|---|---|---|---|
| 1 | Published allocation formula and production location | 30-year world transition; food shipment optimisation | `allocation/` |
| 2 | Price rule for new products | France input–output table (hours embodied per product) | `prices/` |
| 3 | Desirable homes: points plus lottery | City simulation plus evidence (Singapore, Vienna, Stockholm, Netherlands) | `housing/` |
| 4 | Money-cap thermostat | v64 lifecycle model under shocks | `money/` |
| 5 | Motivation and innovation without profit | Evidence review and indicators | `innovation/` |
| 6 | Preventing concentrated power | Evidence review and constitutional stress test | `power/` |

## 1. Allocation formula (`allocation/formula.py`, `location.py`)

**Formula:**
1. Each region's gap is (target − level) × population.
2. Health need is adjusted for age: people aged 65 and over count 3×. This is an assumption to calibrate. *Superseded by rule 37: health need is now weighted by age and disease burden together (`health_need/`).*
3. New capacity first closes every region's gap to the **decent** level (15.3 GJ, 44.5 health workers per 10,000, 15 m²). It then goes to the **comfortable** gaps (40 GJ, 131, 27 m²).
4. Both passes use needs-first water-filling.

**Results** (central case, same resources):

| | single pass (v67) | two passes (decent first) | two passes + age-adjusted health |
|---|---|---|---|
| year every region has decent energy | 8 | **4** | 4 |
| year every region has decent health care | 12 | **7** | 6 |
| year every region has decent housing | 20 | **9** | 9 |
| person-years below decent, energy | 12.7 bn | **8.4 bn** (−33%) | 8.4 bn |
| person-years below decent, health | 30.7 bn | 27.1 bn (−12%) | **25.9 bn** |
| person-years below decent, housing | 37.1 bn | **29.6 bn** (−20%) | 29.6 bn |
| comfortable gap closed by year 30 (energy / health / housing) | 100 / 100 / 50% | 100 / 100 / 50% | not comparable* |

*With age adjustment, the comfortable health target differs by region, so the closure figure is measured against a different target.

**Verdict:** "decent for everyone first" halves the time until every region has decent energy, health care and housing, and costs nothing on the comfortable goal. It should be the constitutional rule. Age adjustment moves health workers toward older populations. It is fairer in need terms, but its weight (3×) must be calibrated with health-spending-by-age data before use.

**Production location (food):**
- Every region keeps a decent diet (2,593 kcal supplied per person at today's 19% waste), and the deficits of 39 regions are covered from the surpluses of 140.
- Only **1.4% of world food supply** needs to move.
- Spreading shipments evenly (each surplus region sends to every deficit region in proportion) means 8,420 km per kcal on average. An optimised plan (min-cost flow over capital-to-capital distances) needs **2,573 km: 69% less transport**. It uses 56 supplier regions and 81 routes, the longest 6,273 km.
- *Limitation:* FAO food balance gives supply, not production, so some "surplus" regions are importers. A production-based plan needs crop-level production data and real transport networks.

## 2. Price rule (`prices/price_rule.py`)

**Rule:**
- price = hours of work embodied in the product, including all inputs, × the fixed hour price of **146.4 U**;
- the price is set once, when the product is introduced;
- later productivity gains shorten working hours instead of lowering prices;
- scarce natural resources carry a physical surcharge.

**Test:** France's 2022 household basket was priced by embodied hours only and compared with today's market prices, with both normalised to the same total.

| cheaper under pure hours pricing | hours price ÷ market | | dearer under pure hours pricing | hours price ÷ market |
|---|---|---|---|---|
| coke and refined petroleum | **0.21** | | other personal services | 2.40 |
| electricity, gas, steam | **0.35** | | residential care, social work | 2.04 |
| real estate (rents) | 0.50 | | retail trade | 1.73 |
| motor vehicles | 0.58 | | accommodation and food | 1.72 |
| telecommunications | 0.62 | | agriculture products | 1.69 |
| air transport | 0.66 | | sport and recreation | 1.50 |

- 38% of household spending would become more than 30% cheaper in relative terms, and 40% more than 30% dearer. The hours rule is a large change in relative prices.
- **Fuels, electricity, flights and cars would become much cheaper relative to everything else.** Their market prices pay mainly for natural resources, land and capital, not work. Pure hours pricing would encourage exactly the uses UNIRA must limit (V7.1 found rebound for energy, travel and data).
- **The resource surcharge is therefore essential, not optional.** It should at least keep fossil fuels, electricity and air travel at today's relative price, rising with ecological limits. The surcharge revenue (in U) goes to the One Earth Fund.
- Care, food and personal services become relatively dearer, because they are work. Under UNIRA, health and care are free (rule 9), so households do not pay them.
- Rare things that cannot be produced again are allocated by turn, lottery or rotation, never by bidding.

## 4. Money-cap thermostat (`money/thermostat.py`)

**Rule:**
- each year, cap ← cap × (target ÷ actual deposits)^0.5;
- the change is limited to **±10% a year**;
- the cap is never below 1 year of base salary in this test (the chosen design uses 1.5 years; see 4b);
- the target is total deposits of 12 months of consumption.

**Test:** 6,000 people over 60 years (v64 lifecycle model), 3 seeds. Shocks hit at year 40, after the cap has phased in from its initial 10 years of salary.

| scenario | deposits, months of consumption (yr 30–60) | largest yearly cap change | cap at year 60 | first homes blocked by the cap |
|---|---|---|---|---|
| calm | 11.8–12.2 | 10% (88% without the limit) | 1.39 yrs of base salary | 0 |
| disaster (30% of savings spent on rebuilding) | 10.0–12.4 | 10% | 1.46 | 0 |
| fear (+15 points of saving for 3 years) | 10.5–14.2 | 10% | 1.41 | 0 |
| baby boom (+15% young adults) | 10.7–12.3 | 10% | 1.49 | 0 |
| automation (+2% a year) | 11.8–12.2 | 10% | 1.39 | 0 |

- The thermostat keeps money stable through every shock, back within 2 months of target in about a year.
- The **±10% limit costs no stability**. Without it, the cap can fall by up to 88% in one year, a shock to every saver. With it, nobody's ceiling moves more than 10% a year.
- Zero-interest credit means **no salaried person is ever blocked from a first home by the cap.**
- **Honest finding: about half of adults reach the cap** (47–51%). The cap binds widely, not only for the rich. The author's options:
  - let money above the cap buy shorter working hours instead of going to the One Earth Fund (option C of V6.4);
  - set the target higher than 12 months.

  This is a choice of values to be decided democratically.

### 4b. Choosing a moderate cap, with protected accounts (`money/cap_level.py`)

The author chose a moderate cap with protected accounts for a home and for retirement:
- money above the cap fills a **home account** (up to 150,000 U, until the person owns a home);
- then a **retirement account** (up to 120,000 U, paid out from 65 to 85 on top of the needs-based pension);
- only then does it go to the One Earth Fund.

Both account limits are assumptions to confirm.

Rush test: a quarter of all free (unprotected) money is spent within one year. Results are at year 60, mean of 3 seeds:

| cap (years of base salary) | adults at the cap | free money (months of consumption) | protected accounts (months) | extra demand in a rush (% of a year's goods) | to One Earth Fund (% of consumption) |
|---|---|---|---|---|---|
| 1.4 (low, thermostat) | 61% | 12.0 | 12.5 | +25% | 22% |
| **1.5 (chosen)** | **40%** | 12.7 | 12.4 | **+26%** | 22% |
| 2 | 38% | 16.5 | 11.9 | +34% | 22% |
| 3 | 36% | 23.8 | 10.9 | +50% | 22% |
| 5 | 29% | 37.4 | 8.3 | +78% | 18% |
| no cap (v64) | 0% | 152 | 0 | +316% | 0% |

- **A floor of 1.5 years of base salary (90,000 U) is the best moderate cap.** It lowers the share of adults at the cap from 61% to 40% with almost no added shortage risk.
- Higher caps barely lower that share, but raise the extra demand a spending rush could create, which fixed prices turn into empty shelves unless reserves cover it.
- With the accounts, an ordinary person can hold up to **360,000 U**.
- No salaried person was blocked from a first home in any case.
- **Cost of the accounts:** the richest tenth's share of money rises from 13% to 23%, because older, higher-paid people fill their retirement accounts. That is still far below 40% without any cap.

## 3. Desirable homes (`housing/`, agent-built, checked)

Simulated city: centre and seaside oversubscribed 2.5 to 1, 30 years, several seeds. The evidence file has 39 rows covering Singapore, Vienna, Stockholm, the Netherlands, Vancouver, and lottery-versus-queue studies.

| method | mean wait if housed | high-need households housed within 5 years | income gradient (top vs bottom tenth) |
|---|---|---|---|
| queue (first come) | 9.7 yrs | 0% | 1.03 |
| points | 5.2 yrs | 27% | 0.86 |
| **points + lottery in bands** | 5.2 yrs | **28%** | **0.86** |
| points + lottery + 30% open | 4.8 yrs | 25% (low-need 7%) | 0.88 |
| pure lottery | 4.2 yrs | 20% | 1.00 |
| highest bidder (market) | short, for the rich only | 27% | ≥99 (the poorer half gets almost nothing) |

- **Points plus a public lottery** is the fairest method.
- Checks on points claims are essential. If 20% of applicants falsely claim care duties, they take 29% of the homes; checking 75% of successful claims undoes this.
- The must-live-in rule cuts empty desirable homes from 6–32% to under 0.5%.
- Building 25% more raises high-need access to 39%.
- The queue's 9.7-year wait is close to Stockholm (9 years) and Amsterdam (10.7 years), but the model was not calibrated to them.
- Constitution Article 18.7–18.11. **Author's decision (rule 36):** 10% of desirable homes go to an open lottery, at most 20% by regional choice. In `housing/open_share.py`, each extra 10% open costs high-need households about 1.2 points (28.3% → 27.1% housed within 5 years at 10%) and gives low-need households about 2.5 points (0.1% → 2.6%).

## 5. Motivation and innovation without profit (`innovation/`, agent-built, checked)

67 evidence rows, 61 read in fetched pages. Verdicts on the six mechanisms:

| mechanism | verdict |
|---|---|
| salary multipliers | partly supported. Pay differences raise effort only when people can see why they were earned (Breza et al. 2018: unexplained differences cut output by 0.45 SD) |
| competition for quality, not profit | partly supported. Plausible, but never tested at the scale of a whole economy |
| fixed research budget, open results, no patents | supported for research (NIH-funded research lies behind all 210 new US drugs of 2010–16; restricting gene data cut follow-on research by 20–30%), weak for development |
| prizes | supported, only for clearly defined problems |
| expert-approved projects and co-ops | partly supported. A single expert gate is biased against novel ideas, so funding should come from several bodies and partly by lottery |
| 30-hour week for creativity | weak. No causal evidence found |

- **New design problem found:** with a fixed price per hour, a team that halves the hours a product needs also halves its revenue. That penalises innovators, as Soviet economists complained in 1962. Article 3d.5 fixes this: the team keeps part of the hours saved for a limited time, and targets are never raised after good results.
- Article 3d adds:
  - research and development of at least 3% of working hours;
  - eight published innovation indicators;
  - automatic review after 2 years of weak results, and compulsory reform after 5.

## 6. Preventing concentrated power (`power/`, agent-built, checked)

48 evidence rows, 45 read in fetched pages:
- 74% of humanity lives in autocracies, and 44 countries are autocratizing (V-Dem 2026);
- at least a third of presidents who reached their term limit tried to stay, two-thirds of them through amendment (Versteeg et al. 2020);
- democracies are 75% more likely to erode during a state of emergency (Lührmann & Rooney);
- established independent courts prevent slides to autocracy, but new courts are fragile.

**Stress test, 13 attack scenarios.** The draft was strong on size bias, the mixed Peace Force and transparency. It was weak exactly where modern backsliding happens: through law, amendment, emergencies, courts, money and information. Five serious gaps were found:
1. no emergency article;
2. accounts could be frozen and payment data read without a court order;
3. the amendment rule, elections and term limits were not entrenched;
4. the Court could be packed;
5. leaving had no procedure.

**Fix:** 17 new articles plus amendments to Article 5a:
- weapons under three keys from different regions;
- a Command Board with no single commander;
- a duty to refuse unlawful orders;
- emergencies limited to 30 days;
- no account freeze or data access without a judge;
- anonymous everyday payments;
- a rule-bound Monetary Authority;
- nine separate powers chosen by different methods;
- term limits and asset declarations;
- a 21-judge Court renewed by thirds;
- citizens' assemblies by lot;
- a democracy health check with automatic brakes;
- a procedure for leaving;
- a protected core that cannot be amended.

After the fixes, every scenario meets at least two independent barriers. 34 of the 111 clauses are directly evidence-supported, and the exact thresholds are judgement. **What no text can guarantee:** resistance by ordinary people stops would-be autocrats more often than courts do, so the design relies on dispersing power and on the right to leave.

## Overall verdict

The five missing mechanisms now have tested, published designs, and the constitution closes the main legal routes to capture. Three findings changed the design:
1. decent-for-all first should be the allocation rule;
2. pure hours pricing would make energy too cheap, so the resource surcharge is essential;
3. a fixed price per hour would penalise innovators, so they keep part of the hours they save.

The constitution now has 66 articles. All results remain model-based. A real pilot is the next test.

## Health-need weighting (`health_need/weights.py`, rule 37)

Healthy life expectancy comes from WHO (WHOSIS_000002, latest year). Gap = 88 − HALE. All-cause DALYs by country are not available as open, redistributable data.

| weighting | new health workers to Sub-Saharan Africa | per 10,000 by year 30: Africa / Europe | every region decent by |
|---|---|---|---|
| equal | 33% | 131 / 141 | year 7 |
| age only (65+ count 3×) | 30% | 116 / 151 | year 6 |
| healthy-life gap | 39% | 164 / 136 | year 7 |
| **age + disease burden (chosen)** | **35%** | **142 / 141** | year 7 |

- Age alone would move care away from young regions with the most disease.
- The combined weighting brings Africa and Europe to the same density.
- Person-years below each region's (weighted) decent level rise from 27.1 to 30.6 billion, because high-burden regions get higher targets. The measure is not comparable across weightings.

## Time account (`money/time_account.py`, rule 35)

| limit | working time lost | equivalent weekly hours | One Earth Fund income |
|---|---|---|---|
| none | 0% | 30.0 | 22.0% of consumption |
| 1 week/yr | 0.9% | 29.7 | 20.9% |
| **2 weeks/yr (chosen)** | **1.8%** | **29.5** | **19.8%** |
| 4 weeks/yr | 3.5% | 28.9 | 17.6% |
