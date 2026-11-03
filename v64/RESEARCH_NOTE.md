# UNIRA V6.4 — The UNIRA money circuit under its own rules (France region pilot)

**Status (updated with §4b lifecycle simulation):** the first stock-flow-consistent model of UNIRA's *own* monetary rules: fixed prices, a 5,000 U base salary with 1–5× multipliers, needs-based retiree income, the disability guarantee, the child-allowance formula, 50% saving, and surplus to the region and the One Earth entity. It is built **from the design rules** (`../v63/DESIGN_CLARIFICATIONS_2026-11-03.md`, rules 1–16), not from today's market institutions. Physical inputs come from V6.2–V6.3 (France 2022–2024). Every U has a source and a destination (11 checks, 9 tests). `python3 run.py`.

## 1. How the circuit works
- **Sectors:**
  - households;
  - enterprises (owners paid as capped salaries);
  - regional fund, which receives enterprise surplus and pays public-service wages, retiree incomes, disability guarantees and child allowances;
  - One Earth, which issues U, holds deposits, and finances or receives regional balances.
- **Fixed price (rule 8):** one price per hour-equivalent of goods, π (U per hour of embodied work, from V6.3), set **once** so that household spending buys exactly the household goods supply (no shortage, no overproduction). It never changes afterwards.
- **Population (Eurostat 2024):** 14.2 m children, 38.1 m adults 20–64, 14.8 m aged 65+.
- **Workers:** 88% of adults (rule 14) = 33.5 m. Unable to work (5,000 U guarantee): 3%, 1.14 m (SYNTHETIC; national data MISSING).
- **Salary multipliers (rule 12):** illustrative values by occupation, as a proxy for knowledge and job complexity. The average multiplier is **1.90** (illustrative; to be set democratically).

## 2. Base-year results (U per year)
| flow | bn U/yr |
|---|---|
| salaries (all workers) | 3,822 |
| disability guarantees | 69 |
| retiree incomes (needs-based; 2,500 U single, ×1.5 couple, +500 U rent if tenant) | 387 |
| child allowances (spec formula, means test) | 64 |
| **household income** | **4,342** |
| saving (50% of adult income) | 1,945 |
| consumption | 2,396 |
| new and renovated homes (limited by construction capacity) | 335 |
| **saving left unspent** | **1,610** |

**Fixed price:** π ≈ 146 U per hour of embodied work. A base worker's spending (2,500 U/month) buys **86%** of an average French person's consumption today. At the average multiplier it is about 1.6×.

**Housing:**

| earners and multiplier | years to buy 100k U | 300k U | 500k U |
|---|---|---|---|
| 1 earner, base 1.0× | 3.3 | 10.0 | 16.7 |
| 2 earners, base | 1.7 | 5.0 | 8.3 |
| 2 earners, average 1.9× | 0.9 | 2.6 | 4.4 |

At π, a 300,000 U home pays for about **2,050 hours** of work. Construction capacity, assuming half of construction investment is housing (SYNTHETIC), is about 1.1 m new or renovated homes per year. **To check:** does a comfortable home really need ≤2,050–3,400 hours of work (100–500k U)? If it needs more, homes are sold below their labour content. Physical construction data (hours per m²) is the next evidence task. A first signal from V6.3: construction embodies about **17.9 hours of work per €1,000 of output**, supply chain included. So a home whose construction costs about €200,000 today embodies about 3,600 hours, which is about **525,000 U at π**. That is at or above the 500,000 U ceiling. Either comfortable homes must be built with fewer hours, or the price range must be checked against labour content. (The euro figure is only a technical proxy; the conclusion is in hours.)

## 3. Findings
1. **The rules are accounting-consistent in a single year.** Every flow balances, and a fixed price exists that clears the market for goods. UNIRA's monetary design is coherent as a system of accounts.
2. **50% saving is not consistent with fixed prices over time.** Only about 335 bn U of the 1,945 bn U saved each year can become new homes, because construction is physically limited. The remaining **~1,610 bn U per year accumulates as deposits**, financed by One Earth. That is 7 years of total consumption after 10 years and **21 years after 30 years**. At fixed prices, those savings are claims on goods that do not exist. If people try to spend them, the result is the shortage economy that fixed prices are meant to prevent. Regional surplus to One Earth never appears: France would *receive* about 1,610 bn U per year.
3. **The balancing saving rate is about 14%.** At that rate the region finances itself (enterprise surplus = public wages + transfers), with no money overhang. But a single base earner then needs **36 years** for a 300k U home.
4. **Experience creep breaks fixed prices slowly.** If the average multiplier drifts up 0.5%/yr, demand exceeds supply at fixed prices by 13% after 30 years (28% at 1%/yr). Productivity growth of 0.5%/yr offsets a 0.5% drift. **Rule needed:** average pay may rise only as fast as productivity, or the multiplier distribution is kept fixed.
5. **Productivity gains under fixed prices and fixed wages create unsold goods** (−14% demand vs supply after 30 years at +0.5%/yr). Under "no overproduction", the gain must become **shorter hours**: more family time, which fits the purpose of the 30 h week.

## 4. Options to reconcile 50% saving with fixed prices (user decision)
- **A. Save 50% only until the first home is paid,** then a low rate (about 10–15%). Zero-interest credit brings the purchase forward and is repaid from salary. Saving then matches homes over a lifetime. *Recommended.*
- **B. Savings ceiling:** deposits above a ceiling (e.g. 2–3 years of income) flow to the One Earth fund (consistent with rule 7).
- **C. Savings into time:** unspent saving reduces required output, so the work week falls below 30 h.

The options combine (A + B). Whatever is chosen, **home purchases are limited by how many homes can physically be built or renovated each year**. The allocation order must stay need-first: first homes before second homes.

## 4b. Lifecycle simulation with the money cap (rules 17–18, `run_lifecycle.py`)
The user clarified two points:
- saving is personal, up to a 50% maximum, for a modest but comfortable life;
- personal money is capped. The excess, including large inheritances, goes to the One Earth entity. A coefficient recalculated every year keeps people working. If technology or AI replaces work, hours are cut.

A sample of 6,000 adults (Eurostat 2024 ages, 3 seeds) works, saves 0–50%, buys homes with savings and zero-interest credit within the construction capacity, retires, dies and passes on a capped inheritance, over 60 years.

| 60-year result (average of 3 seeds) | no cap | cap ≥ home price (300k U) | **low cap + credit** (floor 60k U) |
|---|---|---|---|
| unspent deposits, months of consumption (yr 10 / 30 / 60) | 33 / 83 / **152** | 25 / 35 / 38 | 23 / **12 / 12** |
| cap (years of base salary) | — | 5.0 | ≈1.4 |
| adults at the cap (yr 60) | — | 28% | **57%** |
| flow to One Earth (% of the region's consumption) | ~0% | 20% | 23% |
| home ownership (yr 30) | 92% | 92% | 91% |
| second-home rate (yr 60) | 60% | 60% | 38% |

**Automation (rule 18):** productivity +1%/yr brings the week from 30 h to **23 h after 30 years** and 17 h after 60; +2%/yr gives 17 h, then 9 h. No overproduction, and fixed prices are preserved.

**Findings**
1. **Without a cap, money piles up without limit:** 12.7 years of consumption by year 60. **The user's cap solves this.** With a low cap and zero-interest credit for homes, deposits settle at the 12-month target, and the region sends about a fifth of its consumption value to One Earth each year. This is the mechanism by which "extra goes to the One Earth entity".
2. **Trade-off:** a cap low enough to stabilise money (about 1.4 years of base salary) is reached by more than half of adults. Saving beyond that point brings no personal benefit. That can weaken the motive to save, but not the motive to work, because salaries are still spent. If capped people respond by **spending** rather than saving, demand at fixed prices rises, so the yearly coefficient must account for it. Behavioural evidence: none (SYNTHETIC).
3. **Second homes come mainly from inheritance, not purchase.** Blocking second-home purchases while anyone waits ("need first") changes nothing. Heirs who already own a home inherit another while renters wait 15–19 years. **Rule proposal:** an inherited home beyond the heir's first home returns to the regional pool (or the heir chooses one), while the 2-home maximum is kept.
4. **The people still renting after 30 years are mostly adults without a salary** (not employed, unable to work). Credit can't serve them. They need **guaranteed public housing**, as the spec requires.

## 5. Limitations
- Single region, annual, representative groups (no household microdata).
- Multipliers and the share unable to work are illustrative.
- The retiree basket is a proposal.
- Existing-home sales between households, inheritance, and inter-regional money flows are not modelled.
- Investment and public-service inputs are consolidated inside the enterprise and regional sectors.
- The housing share of construction is SYNTHETIC.
- Demographic ageing is not yet projected.
