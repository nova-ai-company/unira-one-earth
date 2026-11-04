# UNIRA V8.3 — the D + C transition, the equality credit and the stress test

**Author's framework (2026-11-04):**
- **D, the real economy:** equal rights and essentials from day one. Take inventory, redistribute, repair, renovate, then produce what is missing.
- **C, the money:** regional salary scales rise with sustainable, accessible supply.
- Success is measured by **real living standards**, not money in accounts.

**Four safeguards:**
1. Equal rights are not immediate equal availability.
2. Salaries follow the supply of needed goods, not total production.
3. Regional differences are temporary and independently reviewed.
4. Reserves and emergency capacity.

**Compensation:**
- free non-scarce goods;
- priority on scarce goods;
- an **equality credit** of a provisional **25%** of the salary gap, as a guaranteed obligation.

## Equality credit (`equality_credit/model.py`)

164 regions; full scale = France's consumption per person. A reserve margin of 3% builds a stock of goods. Payouts are at most 5% of usable supply during the transition, then 15% after convergence. Salaries are never cut.

| credit share | equal salaries (strong / very strong catch-up) | credits fully repaid | peak outstanding (years of world consumption) |
|---|---|---|---|
| 0% | year 42 / 33 | – | – |
| **25%** | **year 45 / 37** | **year 55 / 44** | 2.0 / 1.5 |
| 50% | year 45 / 37 | year 75 / 61 | 5.1 / 3.8 |
| 100% | year 45 / 37 | never | 11.5 / 8.7 |

## Stress test (`equality_credit/stress.py`, 25% credit, strong catch-up)

| stress | equal salaries | credits repaid | shortages after reserves |
|---|---|---|---|
| baseline | year 45 | year 55 | none |
| population +30% / −30% | year 46 / 44 | year 56 / 54 | none |
| supply shocks (−5% in five years, −10% once) | year 45 | year 55 | **none: reserves absorb them** |
| Africa and South Asia at half catch-up speed | year 54 | year 66 | none |
| slow productivity (historical +2%) | not within 80 years | not within 80 years | none |
| all combined | not within 80 years | not within 80 years | none |
| slow productivity, with a liability ceiling of 2 years | not within 80 years | – (outstanding held at 2.1 years) | none |

## Findings

1. **25% is payable** under strong or very strong catch-up, repaid about 10 years after salaries become equal. 50% is repaid too late for many workers, and 100% never.
2. **The design never produces shortages** in any stress tested. The capacity rule and the 3% reserves absorb population change and repeated supply shocks.
3. **Regional lag and slow growth are the real risks.** If Africa and South Asia catch up at half speed, convergence takes 54 years. At the historical pace of growth, it does not happen within 80 years.
4. **A liability ceiling keeps promises payable.** Accrual pauses while outstanding credits reach 2 years of world consumption. It is now in T-8.6.
5. **Open question.** Convergence to today's French consumption level may be neither reachable at historical growth nor ecologically possible for everyone (V6.6). Defining the full scale's real basket as the **sustainable comfortable level for all** would make the target reachable sooner.

The 33–45-year range is a simulated range under strong catch-up, not a deadline. All growth rates are scenarios, and consumption in money terms (PPP) stands in for physical supply. The world-data test of D (production capacity by sector, stocks, transport, natural resources) is the next step.

## Amendments by the author (after the stress test)

- **Credits already earned remain valid** when the two-year ceiling pauses new accrual. The model already keeps them; only new accrual pauses.
- **The 25% rate is conditional** on the ceiling and on an annual independent sustainability assessment.
- **"Salaries never cut" protects nominal income, not purchasing power.** In a declared emergency, temporary limits on non-essential purchases are allowed, with essentials always protected (T-8.8).
- **Reserves come in three forms:**
  - inventories (food, medicines, fuel, repair materials);
  - emergency production capacity (standby power, flexible medicine production, mobile care);
  - resilient infrastructure.

  The 3% reserve margin of the model is an aggregate. Modelling each form separately is future work.
- **The target is the UNIRA living standard** (Article 10c), not today's French consumption. The 80-year result shows the French level is impossible *under current assumptions*, not that it is fundamentally impossible. It is recorded as an unresolved research question. The next step is to cost the living-standard basket in hours and resources for every region, and rerun convergence toward it.
