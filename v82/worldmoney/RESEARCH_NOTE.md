# UNIRA V8.2 — point 4: the world money model (author's choice C, 20 years)

**The finding that led to the choice:**
- World household consumption is about **$11,500 per person** (World Bank 2023, purchasing power). The lowest UNIRA salary buys about **$21,900**, from France's level.
- Equal salaries everywhere from day one would therefore ask for about twice what the world produces. 93% of people live in countries whose average is below the base basket.
- With fixed prices, that gap becomes empty shelves.

**The author chose option C (2026-11-04):**
- needs (food, health, education, a home, the energy allowance) are guaranteed **in kind everywhere from year 1**;
- each region's salary scale in U starts at its real production level and rises to the **full scale within 20 years**;
- prices are the same everywhere.

**Model** (`model.py`):
- 164 regions (World Bank). The full level is France's consumption per person. The starting salary factor is the region's consumption ÷ full level; the population-weighted average is 0.40.
- Goods per person grow at 1% a year in regions at the full level, faster in poorer ones (three catch-up scenarios).
- Population follows UN/World Bank projections.
- The One Earth Fund moves goods from surplus regions to regions whose salaries buy more than they produce.

| catch-up (extra yearly growth for poorer regions) | strict 20-year schedule: world shortage in year 20 | Fund transfers needed | with the capacity rule: average salary factor in year 20 | full scale reached |
|---|---|---|---|---|
| historical (+2%) | **39%** | 77% of world supply | 0.61 | after year 50 |
| strong (+4%) | 28% | 52% | 0.72 | year 39 |
| very strong (+6%) | 19% | 35% | 0.81 | **year 31** |

(Capacity rule: salaries rise as fast as goods allow, and never faster.)

## Findings

1. **A strict 20-year schedule is not physically possible at any realistic growth rate.** Salaries would buy 20–40% more than exists.
2. **The capacity rule removes shortages entirely.** Every region's salary factor rises each year by as much as the world's goods allow. One Earth transfers 15–20% of world goods to poorer regions. The full scale arrives in **31–39 years** with strong or very strong catch-up.
3. **20 years remains the target.** Reaching it needs growth in poorer regions faster than any large region has sustained, apart from China's best decades. That means maximum investment, training and technology transfer (Articles 10a, 16a, 3d).
4. **Ecological caution:** the full level is France's consumption per person. For 9–10 billion people that is about 2.5 times today's world consumption in money terms. V6.6 found today's European consumption is not possible for everyone within Earth's limits, unless consumption shifts strongly to services, repair and low-material goods (energy allowance, surcharges, Article 11). The full scale must therefore be met with a lighter basket than France's today.

## Rule supported (Transitional provision T-8)

1. Needs are guaranteed in kind everywhere from year 1.
2. Each region's salary scale rises every year toward the full scale, with **20 years as the target**.
3. Salaries never rise faster than the goods available to the region, meaning its own production plus One Earth Fund transfers. Shelves are never emptied by money.
4. Progress is published every year. A region behind schedule receives priority investment and training.

## Limitations

- Consumption in money terms (PPP) stands in for physical production capacity.
- Catch-up rates are scenarios, not forecasts.
- One world ratio is applied to all regions (a fairer rule could favour the poorest first).
- Trade outside UNIRA is not included (point 5).
