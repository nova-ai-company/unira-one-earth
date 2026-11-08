# V7.2 — The one-member economy: Ghana and India as first members

**Status (8 November 2026): preliminary, not peer reviewed.** The author asked for the model that the first-region screen (`FIRST_REGION.md`) said was missing: trade balance, reserves, the price wedge at the border and emigration at the top of the pay scale, for the two regions that pass every screen. `joining/one_member.py` (+7 tests), output `outputs/one_member.json`. Data: World Bank series frozen in `joining/data/raw` with hashes (trade, GDP, reserves, remittances, import composition, PPP factor, exchange rate) and the income shares of V7.4. It is a stock-flow exposure test with fixed shocks, not a forecast, and nothing in it says a region would vote to join.

## Today's position

| | Ghana | India | Median of the 36 passing or near-miss regions |
|---|---|---|---|
| Exports / imports, % of GDP | 35 / 34 | 22 / 24 | 24 / 26 |
| Trade balance, % of GDP | +1.1 | −1.8 | +0.8 |
| Remittances received, % of GDP | 3.6 | 3.7 | 1.8 |
| Reserves, months of imports | 3.0 | 8.6 | 5.4 |
| Food, fuel, ores and metals, share of merchandise imports (a floor for "essential imports") | 41% | 43% | – |
| Reserves, months of essential imports (Article 12b.4 asks for 6) | 7.3 | 19.8 | – |
| Price level relative to world prices (PPP factor / exchange rate) | 0.30 | 0.24 | 0.34 |
| People above the UNIRA pay ceiling (5 × base), Pareto tail on the top decile | 0.025% (about 8,600) | 0.001% (about 8,700) | – |

## The five-year balance (Article 12b.2) and the six-month reserve (12b.4)

Reserves follow R(t+1) = R(t) + exports × (1 − shock) − imports × (1 + needs) + remittances. The export shock stands for the market world's reaction and for competitiveness lost while internal prices move to the world hour price; the needs surge for the import of medicines and equipment that needs-first allocation brings forward.

| Scenario | Ghana: reserves at year 5 (months of imports), first year below six months of essential imports | India |
|---|---|---|
| No shock | 11.5, never | 13.3, never |
| Needs imports +10% | 5.5, never | 7.3, never |
| Exports −10% | 5.3, never | 7.8, never |
| Exports −10% and needs +10% | −0.7, **year 1** | 1.8, year 5 |
| Exports −25% | −4.0, year 1 | −0.6, year 4 |
| Exports −40% | −13.3, year 1 | −8.9, year 2 |

Export growth needed to balance over five years: none for either region (today's exports plus remittances already cover imports); +0.8% a year for India if needs imports rise 10%.

## Reading

1. **A one-member UNIRA balances its foreign currency today**, in both regions, because exports and remittances cover imports. The design's rule of five-year balance without debt (12b.2) is met at the start.
2. **It survives a 10% fall in exports; it does not survive 25%.** India's eight months of reserves buy four years; Ghana's three months buy one. The decisive variable is therefore not the region's economy but the market world's reaction, which the project cannot model, and the Trade Office's export earnings, which it must manage from day one. A first member with thin reserves should build them before the vote, or join with a partner that has them.
3. **The border wedge is large.** Both regions' goods sell today at a quarter to a third of world prices. Inside UNIRA, with savings converted at basket parity (T-1.2), a tradeable good bought at the fixed internal price and sold abroad fetches three to four times more: the smuggling incentive the Trade Office monopoly (12b.1) and customs must hold, strongest for the most open economy (arbitrage index = wedge × openness: Ghana 0.24, India 0.18). The wedge is an economy-wide average; the real incentive is good by good.
4. **Emigration at the top of the pay scale is a small pool**: about 8,000–9,000 people in each region earn more than the 5× ceiling today; even the top decile's average income is below the UNIRA base basket in both. The risk is in specific professions (doctors, engineers, researchers) whose world wages exceed the ceiling, not in the income distribution as a whole; the register of behavioural assumptions does not cover it, and the pilot cannot test it.
5. **Remittances are a hidden pillar** (3.6–3.7% of GDP, twice the group median). They are assumed to continue; if a first member's diaspora sends less because families no longer need it, the balance weakens by that much.

## What this does not settle

The market world's reaction (sanctions, tariffs, loss of market access) is a scenario, not an estimate; there is no capital account and no behavioural response of exporters; the essential-import share is a floor (medicines and equipment are missing from the series); the Pareto tail gives an order of magnitude; and the price wedge is averaged over the whole economy. The political question, whether a region would vote to join, is untouched. Review question 19.
