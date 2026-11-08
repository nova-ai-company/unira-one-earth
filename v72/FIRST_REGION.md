# V7.2 — Which region could be first? A screen for the political-path gap

**Status (8 November 2026): preliminary, not peer reviewed.** Written in answer to the author's question "how can we solve the gaps". The concept's gap 5 says that no region has a reason to be first until a one-member UNIRA is shown to be workable. This note does the first half: a transparent screen of the 179 regions for the conditions under which a first member is least exposed. `joining/first_region.py` (+5 tests), output `outputs/first_region.json`. It is a screen, not a prediction that any region would vote to join.

## Screens (all must hold)

| Screen | Source |
|---|---|
| Gains materially from joining at year 30 | V7.2 (146 gainers, 33 losers) |
| Not on the World Bank list of countries in conflict (FCS FY26) | v88 raw data |
| Institutions at or above the world average: mean of four Worldwide Governance Indicators (voice, rule of law, control of corruption, government effectiveness) ≥ 0 | v91 raw data |
| Imports of goods and services at or below the median of gaining regions (39.3% of GDP) | World Bank NE.IMP.GNFS.ZS, frozen in `joining/data/raw` with its hash |
| Population at least 5 million | v67 regions |
| At least 90% of people better off at the lowest UNIRA salary | V7.4 (150 regions with income distributions) |

## Result

- Of 146 gaining regions, 19 are in conflict, 14 more are fragile, and only 47 have institutions at or above the world average. The gainers' median import share is 39% of GDP (quartiles 27–58%).
- **Two regions pass every screen: Ghana (34 m) and India (1.45 bn), 18% of humanity.** Both gain, are at peace, have institutions just above the world average (WGI mean 0.07 and 0.04), import a quarter to a third of GDP, and everyone is better off at the base salary.
- **34 regions fail by one screen only.** Most fail on institutions (Bangladesh, Indonesia, China, Kenya, Côte d'Ivoire, Benin, Sri Lanka, Ecuador, Bolivia, Algeria...); the stable higher-income gainers fail because a large share of their people would lose at the base salary (Chile 82% better off, Costa Rica 79%, Argentina 76%, Israel 63%, the United Kingdom 41%).

## Reading

A first member exists on the data, and it is neither a poor region nor a rich one: a stable middle-income region whose people gain and whose borders are manageable. The screen also shows the shape of the coalition problem: the regions that gain most have the weakest institutions, and the regions with the strongest institutions gain least. The design's answer to the first (T-9, paced reform; Article 10f) and to the second (multipliers to 5×, convergence, time and security valued beyond material goods, V7.2 break-even) are both untested.

## What a first member is exposed to (the channels, with what can and cannot be measured)

1. **Import dependence.** The Trade Office (12b) must earn in exports the foreign currency for imports at world prices; the import share of GDP measures the exposure (India 24%, Ghana 34%). What matters more is the essential-import share, known only for France (36%, V8.2).
2. **Capital flight before the vote.** Money moved abroad is not converted into U (T-1.3 applies to wealth held on the voting day). It does not remove workers, land or plants, so the internal economy in hours is unaffected; the foreign-currency reserve is. A look-back rule is an open question (review brief E6).
3. **Skilled emigration.** The people who lose at the base salary are the pool that may leave: none in Ghana or India at the base, more at the top of the scale. Multipliers to 5× and salaries never cut are the design's answer.
4. **Smuggling.** Incentive = price wedge between fixed internal prices and world prices × openness. The wedge is not measurable here.

## What is still missing for gap 5

The model of the one-member economy for the two passing regions is in `ONE_MEMBER.md` (built the same day on the author's "Go"): both balance their foreign currency today, survive a 10% export shock and not a 25% one, face a border wedge of three to four times, and have about 8,000–9,000 people above the pay ceiling. Nothing in either note shows that a region would choose to join.
