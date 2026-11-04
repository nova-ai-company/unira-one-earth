# UNIRA V8.4 — quotas (Q): equal salaries from day one, or a hybrid?

**Proposal (author, via a discussion with another AI assistant):** add quotas, so that scarce goods are shared by need and population and cannot be bought up by money. That might allow equal salaries from day one without equality credits. The suggested test compared D + C with D + C + Q under the same production, population, reserves and shocks.

**A physical point added before testing:** in France, **76% of household spending is on local services** (shops, restaurants, transport, care, repairs, leisure) and only **24% on goods** (food, energy, manufactured products), homes excluded (v81). Goods can be shipped between regions and stored. Local services are produced only by each region's own workers.

**Model** (`quotas/compare.py`):
- 164 regions, 80 years, strong catch-up;
- 3% of goods kept as reserves; shocks of −5% (five times) and −10% (once);
- full level = France's consumption per person;
- in every scenario, services are limited by local capacity and goods by world supply.

| | poorer half of humanity (real consumption ÷ full level): yr 0 / 10 / 20 / 40 | richer half, yr 0 / 20 | inequality between regions (Gini), yr 0 / 20 / 40 | money that cannot be spent, yr 0 / 20 | richest 20 regions vs today, yr 0 | poorer half reaches 90% |
|---|---|---|---|---|---|---|
| **1. D + C** (converging salaries + 25% credit) | 19% / 30% / 43% / 74% | 60% / 83% | 0.37 / 0.23 / 0.11 | 0% / 0% | 65% | year 55 |
| **2. D + C + Q** (5,000 U for all from day one + equal goods quotas) | 25% / 36% / 49% / 79% | 56% / 80% | 0.28 / 0.17 / 0.08 | **59% / 36%** | 56% | year 50 |
| **3. Hybrid** (equal goods quotas from day one + salaries for local services converge) | 25% / 36% / 49% / 79% | 56% / 80% | 0.28 / 0.17 / 0.08 | **0% / 0%** | 56% | **year 50** |

Credits outstanding under D + C reach 2 years of world consumption, the ceiling, by year 20. Quotas need no credits.

## Findings

1. **Quotas on goods make UNIRA fairer and faster.**
   - The poorer half of humanity gets 6 percentage points more real consumption from the first day.
   - It reaches 90% of the full level 5 years sooner.
   - Inequality between regions is a quarter lower.
   - No equality-credit debt is created.
2. **Equal salaries from day one do not create equal living standards.** Most of what money buys is local services, and local services in poorer regions must be built, not shipped. With 5,000 U for everyone, **59% of money is unspendable at the start** (still 36% after 20 years). That is strong pressure for black markets, and a salary that is partly symbolic.
3. **The hybrid gives the same real outcome as Q without the unspendable money.**
   - Goods are shared equally by quotas from day one.
   - The part of salaries meant for local services rises as each region's services grow.
   - Money then always matches what can be bought.
4. **The price is paid by the richest regions in goods.** Sharing goods equally means the richest 20 regions consume about 56% of today's level at first, against 65% under D + C, recovering as the world grows. Their local services are unaffected.
5. **The full level is still France's consumption.** Measured against the UNIRA living standard of Article 10c, every date would come earlier.

## Recommendation

Adopt the **hybrid (D + C + Q for goods):**
- guaranteed essentials in kind (D);
- equal, needs-based quotas for goods that are scarce;
- money for local services that rises with local capacity (C).

No equality credit is needed for goods. The credit could be kept only for the services gap, or replaced.

## Limitations

- One goods/services split for every region (poorer regions spend more on food).
- Quotas equal per person (in practice adjusted to needs: household size, climate, health).
- No transport losses or delays.
- Black-market pressure is shown as unspendable money, not modelled as behaviour.
- PPP consumption stands in for physical capacity.
