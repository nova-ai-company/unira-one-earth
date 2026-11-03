# Rule 20 evidence review: does security reduce over-consumption?

Hypothesis (v63 rule 20): when people are sure they can always afford and access food and essentials at fixed prices, they over-buy, hoard, waste and over-eat less. The analogy offered is unlimited mobile calls.

Rows and URLs are in `evidence.csv`. Model values are in `parameters.json`. The `verified_in_fetched_text` column is "yes" only when the number appeared in a page or PDF that was actually fetched. Search-only figures are labelled as such and are not used as central values.

## Verdict by good type

| Good | Verdict | Key numbers |
|---|---|---|
| Mobile voice | **Analogy holds, with a step up first.** Unlimited plans raised use, then use plateaued. | France, minutes per customer per month: 2h15 in Q1 2011, 2h51 in Q1 2013 (+15.5% y/y, attributed by ARCEP to unlimited plans), 3h03 in Q1 2015 (+1.6% y/y), 3h28 in 2023 (about 7 min/day) |
| Flat-rate tariffs | **Supports.** People buy flat rates for insurance, not to max out. | Up to 46.4% of consumers chose a flat rate that cost more than pay-per-use for their usage (Lambrecht & Skiera 2006) |
| Mobile data | **Against. No satiation.** | 529 MB/month (2015) to 14 GB (2023), +2 GB/yr. Unlimited users use +20% more than large-cap users in high-GDP countries (Ericsson) |
| Food calories | **Supports (calorie satiation).** | India: calories fell as real incomes rose (Deaton & Dreze 2009). Insecurity is linked to obesity only in adult women in high-income countries (Nettle et al. 2017, 125 studies) |
| Over-eating under abundance | **Mixed.** Food form matters more than security. | Ultra-processed food eaten freely: +508 kcal/day (Hall 2019 RCT) |
| Stockpiling / panic buying | **Supports.** Scarcity drives hoarding. | Ireland, week to 15 Mar 2020: grocery +23% y/y, toilet roll +181%, pasta +199%, rice +123% |
| Household food waste | **Weak or ambiguous.** Security alone does not reduce it. | Waste is similar across country income groups (about a 7 kg/cap/yr spread; 74 kg in the 2021 index). It rises at middle incomes through overbuying "to avoid running out" (inverted U). UK self-reported waste fell 34% during the 2020 lockdown, i.e. under insecurity |
| Temptation goods | **Supports (no rise with income security).** | 44 estimates from 19 studies are almost all null or negative (Evans & Popova) |
| Household energy | **Against when unmetered. Bounded when priced.** | Direct rebound under 30% (Sorrell 2009). Metering vs flat-rate heat billing saves "often" up to 30% |
| Travel | **Against when free.** | Fare-free transit: Tallinn PT use +14%; Dunkirk weekday +70%, weekend +140%. Luxembourg car commuting share only went from 72.3% to 69.3% (2011 to 2021) |

## Reading the analogy correctly

The phone case does not show that security lowers use. Voice use **rose** about 36% within three years of unlimited plans, then stopped rising because time and social need cap it. The same pattern is expected wherever a natural ceiling exists, such as stomach size or storage space. Where no ceiling exists (data, travel, heated space, status), flat or zero pricing raises use without limit. This review supports rule 20's own refinement: **fixed per-unit prices, not flat rates, for energy and travel.**

## Parameters (see parameters.json)

- (a) Reduction in household food waste: 0 / **5%** / 15%. Weak evidence, sign uncertain.
- (b) Avoided share of shock-driven stockpiling spikes: 25 / **50%** / 75%. Needs a credible guarantee, the rule 13 reserves and purchase limits during shocks. Steady-state effect is negligible.
- (c) Direct rebound with fixed prices: 10 / **20%** / 30%. If use is unmetered or flat-rate, add +10–30% for heat. Fare-free transit adds +14–70% trips.
- (d) Satiation table in `parameters.json`.

## Gaps and cautions

- **Unverified figures:** Evans & Popova −0.18 SD, Deaton & Dreze kcal values, GiveDirectly +23%, the OECD transport rebound, Tallinn car figures and Dunkirk car-switch shares. They are flagged "no" in the CSV.
- **Not found:** Finland basic income and Mincome report no consumption-volume or stockpiling outcomes in the sources checked.
- **Wansink:** the buffet studies were deliberately not used because of retractions.
- **ARCEP basis change:** the 2023 voice figure counts mobile-device holders, while 2011–2015 counts customers.
