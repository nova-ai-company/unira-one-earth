# UNIRA V8.2 — does a restaurant (and a supermarket) work with UNIRA's prices and salaries?

**Question from the author:** simulate the sales, costs (rent of premises, raw materials, energy, equipment) and result of a restaurant and of a supermarket, to check that UNIRA's prices and salaries are consistent.

**Method** (`simulate.py`):
- **Real cost structure** per euro of output, France 2022 (Eurostat input–output table): every input bought from the 64 product groups. These add up exactly to the official input total.
- **Sales** = embodied hours × 146.4 U.
- **Inputs:** each at its own UNIRA price. Energy for food businesses has no surcharge (rule 41). Rent of premises is at the hours cost of real-estate services.
- **Wear of equipment and premises:** France's depreciation share of value added, applied to the sector.
- **Salaries:** UNIRA salaries for the real hours worked (30 h a week), including hardship steps (Article 14a).
- **Community share:** what remains, which goes to the region and the One Earth Fund.
- The job mixes are illustrative.

## Restaurant, 10 people (owner-chef 3×, 2 cooks 1.8×, 7 staff 1.2×, plus hardship steps)

About 62,000 meals a year (about 200 a day).

| | U per year | share of sales | today in France (share of output) |
|---|---|---|---|
| sales | 3,202,600 | 100% | |
| food, supplies, services | 1,116,400 | 35% | 57% |
| … rent of premises | 52,200 (4,350 a month) | 1.6% | 5.6% |
| … energy | 17,500 | 0.5% | 2.7% |
| wear of equipment and premises | 150,000 | 5% | (in operating surplus) |
| salaries (average 1.93×) | 1,155,000 | 36% | 32% (staff pay) |
| **community share** | **781,200** | **24%** | 11% operating surplus, plus taxes |

**One meal at 51.3 U:** 17.9 U food and supplies, 2.4 U equipment, 18.5 U staff, 12.5 U community share.

## Supermarket, 40 people (its own retail work; the goods pass through at their fixed prices)

| | U per year | share |
|---|---|---|
| sales of retail work | 11,181,800 | 100% |
| supplies and services | 2,449,500 | 22% |
| … rent of premises | 188,000 | 1.7% |
| wear of equipment and premises | 738,100 | 7% |
| salaries (average 1.64×) | 3,930,000 | 35% |
| **community share** | **4,064,300** | **36%** |

## Quiet periods (fixed prices and salaries)

| demand (share of normal) | 50% | 60% | 70% | 80% | 100% | 120% |
|---|---|---|---|---|---|---|
| restaurant community share (U) | −261,900 | −53,300 | +155,300 | +364,000 | +781,200 | +1,198,400 |
| supermarket community share (U) | −301,900 | +571,300 | +1,444,600 | +2,317,800 | +4,064,300 | +5,810,700 |

**Break-even:** the restaurant covers all costs and salaries down to **63%** of normal demand, the supermarket down to **54%**.

## Findings

1. **The prices and salaries are consistent.** At normal activity both businesses pay all their inputs, rent, energy, equipment wear and UNIRA salaries, including the owner-manager at 3× and hardship steps, and still return a surplus.
2. **The surplus is not profit.** It is the community share, about a quarter to a third of sales. It pays for free health care, education, public services, investment and the One Earth Fund, the role that taxes, social contributions and profits play today. In France today, compulsory levies are of the same order (above 40% of GDP).
3. **Rent and energy weigh much less.** Business rent costs only the work to build and maintain premises (land is not sold for profit), and food businesses pay energy at the hours price.
4. **Quiet periods are the risk.** Below about 60% of normal demand a business runs at a loss, because salaries are fixed. UNIRA needs a rule:
   - the region covers short losses from the pooled community shares;
   - after six months, staff and capacity move to where demand is (Article 10b), with no one losing income;
   - persistent losses lead to review, not bankruptcy of people.

## Limitations

- Sector averages for France; one illustrative job mix per firm.
- Imported inputs are priced like domestic ones.
- The depreciation share is applied economy-wide.
- Hours per unit of output are today's: the productivity gain of a 30-hour week is not included, and would raise the surplus.
