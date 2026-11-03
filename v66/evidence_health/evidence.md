# V6.6 evidence: how much health-workforce need could UNIRA prevent?

**Hypothesis (rule 19):** no war, a 30 h week, guaranteed income, housing and healthcare, and less fear and stress would prevent much disease. That would cut health-care demand and so ease the binding constraint from v65 (+58.7 m health workers for an EU-like 131 per 10,000).

**Answer in one line:** the evidence supports **less disease**, but only a **small net cut in health-workforce need**: central ~2% at 5 y and ~3% at 15–30 y, high ~14% at 30 y, and low ~0 (possibly slightly negative). That is about 3 m workers in the central case, against a 59 m gap.

All figures are in `evidence.csv` (50 rows). The `verified_in_fetched_text` column is `yes` only where the exact figure appeared in text fetched in this session. Most of these came from abstracts via Europe PMC.

## 1. Disease burden attributable to modifiable risks (upper bound)
- **41.4%** of global DALYs in 2021 were attributable to 88 risk factors (44.7% excluding COVID-19) [GBD 2021, Lancet 2024]. GBD 2019 gives **47.8%** for 87 risks.
- By category in 2021: behavioural **763 m** DALYs, metabolic **476 m**, environmental/occupational **416 m**. These overlap.
- Leading single risks in 2021: particulate matter **8.0%** of DALYs, high SBP **7.8%**, smoking **5.7%**, low birthweight **5.6%**, high FPG **5.4%**.
- In 2019: high SBP caused 10.8 m deaths (19.2%), tobacco 8.71 m (15.4%). Child and maternal malnutrition caused 11.6% of DALYs. Diet, inactivity and BMI together caused 11.9%.
- **Caveats:** these fractions assume exposure falls to the *theoretical minimum*, not to a level UNIRA could plausibly reach. More than half of DALYs are attributed to no risk at all. Disability-heavy, care-intensive conditions are weakly attributable: musculoskeletal disorders are 5.6% of DALYs, of which only 20.5% is risk-attributable.
- Poverty-linked risks are already falling without UNIRA: attributable DALYs fell 66% for unsafe water and 72% for child growth failure (2000–21). Metabolic-attributable DALYs rose 49%.
- Not retrieved: burden for low physical activity and for unsafe WASH. Marked unverified.

## 2. Work, stress and insecurity (UNIRA's specific levers)
- **Long hours (≥55 h/week):** 488 m people exposed (8.9%). This caused **745,194 deaths and 23.3 m DALYs** from IHD and stroke in 2016 [Pega 2021, WHO/ILO]. That is roughly 0.8–0.9% of global DALYs. Relative risks: stroke 1.33, CHD 1.13 [Kivimäki 2015]. A 30 h week removes this exposure.
- **Job strain:** CHD HR 1.23. Population attributable risk is only **3.4%** [Kivimäki 2012].
- **Job insecurity:** CHD RR 1.32, or 1.19 fully adjusted [Virtanen 2013]. *Unverified: search snippet only.*
- **Unemployment:** all-cause mortality HR **1.63**. It is 24% lower when health behaviours are controlled for [Roelfs 2011]. This evidence is observational.
- **Debt:** mental disorder OR 3.24, depression 2.77, suicide 7.9 [Richardson 2013]. The authors say causality is unclear.

## 3. Income, housing
- **Mincome:** hospitalisation **−8.5%** versus controls [Forget 2011]. This is **contested**: Green (2022) argues the data do not support health-cost savings, and Forget replied in 2022.
- **Unconditional cash transfers (LMICs, Cochrane 2022):** any illness **RR 0.79** (moderate certainty) at 1–2 years. However, any health-service use was **RR 1.04**, so income can *raise* care use where need is unmet.
- **Housing First:** ED visits IRR 0.63 and hospitalisations IRR 0.76 [Baxter 2019]. This comes from 4 RCTs, all at high risk of bias, and covers only the homeless population.

## 4. Conflict
- Direct deaths in state-based conflicts were **138,917–284,981 a year** in 2021–2025 (UCDP via OWID, downloaded). Counting all conflict types, 2022 had ~317,000. That is ~0.3–0.5% of the 67.9 m global deaths. Indirect deaths are not included.
- In conflict-affected populations, **22.1%** have a mental disorder at any time (5.1% severe) [Charlson 2019].
- GBD "conflict and terrorism" DALYs could not be retrieved (the data is non-redistributable): unverified.

## 5. Countervailing evidence
- **Longevity offset:** van Baal 2008 found lifetime health spending is *highest* for healthy-living people, then obese people, then smokers. Prevention "is not a cure for increasing health expenditures". Barendregt 1997 found that if all smokers quit, costs fall at first and then exceed the baseline **after 15 years**.
- **Expansion of morbidity:** in England, 4+ disease multimorbidity among people 65+ is projected to rise from 9.8% to 17.0% (2015→2035). Most life-expectancy gains would be spent with 4+ diseases [Kingston 2018]. In Scotland, 23% of people are multimorbid, including most people 65+ [Barnett 2012].
- End-of-life care is only 8.5–11.2% of spending in the last year of life (up to 24.5% over 3 years) [French 2017, *unverified*]. Most care is long-running chronic care, which longevity increases.
- **Prevention paradox** [Rose 1981]: most cases come from the many people at moderate risk. Population-wide gains are real but small per person, and prevention programmes themselves need staff.
- The WHO projects a **11.1 m** shortfall by 2030 and attributes it to supply problems: training, distribution and migration.
- **Workforce need ≠ DALYs.** Need is set by a service standard (here an EU-like 131 per 10k), not by disease rates. Maternity, child, routine, elderly and rehabilitation care stay the same. Premature deaths, which dominate attributable DALYs, consume little care.

## 6. Timing
- **CVD responds fast.** Within 5 years of quitting, heavy smokers have HR 0.61 versus those who continue. The excess risk versus never-smokers disappears only after 10–15 years [Duncan 2019].
- **Cash transfers** reduce illness within 1–2 years. **Mincome** effects appeared within its 4-year run.
- **Population CVD declines are slow:** Finland's coronary mortality fell 80% over 35 years, with 60 percentage points explained by risk-factor change [Vartiainen 2010].
- **Cancer takes decades.** Stopping smoking at 30 reduces lung-cancer risk to age 75 to 2%, versus 10% stopping at 60 [Peto 2000]. Changes in youth smoking show up in mortality only after decades.

## Proposed parameter: net preventable share of health-workforce need

`share(t) = A × r × e × ramp(t) × (1 − offset × offramp(t)) + c_conflict`

| input | low | central | high | basis |
|---|---|---|---|---|
| A, attributable DALY share | 0.414 | 0.45 | 0.478 | GBD 2021/2019 (verified) |
| r, share of that burden UNIRA removes | 0.10 | 0.25 | 0.45 | judgement: UNIRA hits a subset of risks |
| e, DALY → workforce elasticity | 0.4 | 0.5 | 0.7 | judgement: YLL-heavy, chronic care unaffected |
| offset, longevity at 30 y | 1.3 | 0.6 | 0.2 | Barendregt, van Baal, Kingston |
| ramp (benefit / offset) 5, 15, 30 y | 0.3/0.2, 0.65/0.6, 1/1 | | | timing evidence above |
| c, conflict | 0.001 | 0.005 | 0.015 | UCDP, Charlson; judgement |

| horizon | low | central | high | central in workers (of ~107 m EU-like need) |
|---|---|---|---|---|
| 5 y | 0.00 | 0.02 | 0.06 | ~2 m |
| 15 y | 0.00 | 0.03 | 0.10 | ~3 m |
| 30 y | −0.005 | 0.03 | 0.14 | ~3 m (high ~15 m) |

**Confidence: low.** The direction of the gross effect is well supported. The net effect is small, and its sign is uncertain in the low case. Prevention could ease, but **cannot replace**, the training programme for ~59 m health workers. The gross disease reduction would show up more clearly in **health outcomes** (healthy life-years) than in workforce need. Those outcomes are UNIRA's real benefit and should be reported separately.
