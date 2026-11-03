# UNIRA V5.9 — Multi-sector, 20-year feasibility prototype

**Status:** synthetic computational experiment; not an empirical assessment of UNIRA or of any country.

## Scope
Six sectors: food, housing, energy, healthcare, manufacturing and infrastructure. Every sector has a final-demand index, capacity, labour-hours coefficient, annual depreciation and investment replacement cost. A simple input-output coefficient matrix makes production of one sector require outputs from others. Gross output is solved as x = final + A x. A common fulfillment fraction respects all capacity and labour constraints. Unmet final demand is explicitly reported.

The model simulates 20 annual periods with a finite annual investment budget. If budget cannot fund replacement, productive capacity depreciates. The energy shock is a one-year capacity reduction, not a permanent loss. A 2.5% population-growth scenario increases all final-demand indices equally.

## Selected reproducible outcomes

| Scenario | Years with shortages | Cumulative unmet index | Unfunded investment (U) |
|---|---:|---:|---:|
| Baseline | 0 | 0 | 0 |
| Energy shock (year 5, -35%) | 1 | 161.99 | 0 |
| Demand growth 2.5% annually | 16 | 2467.29 | 0 |
| No replacement investment | 14 | 903.00 | 240000 |
| Investment budget 4000 U/year | 11 | 396.00 | 160000 |
| Labour available 9000 hours/year | 20 | 1995.27 | 0 |

**Important:** Cumulative unmet index sums different abstract sector indices and years. It is an illustrative diagnostic, **not** a physically meaningful total of goods, people, emissions or welfare losses. Sector-specific shortage columns are in the CSV.

## Limits and audit

- No empirical calibration, no market price assumptions, no environmental coefficients, no regional trade, no demographic household matching.
- Fixed proportions, uniform rationing, and fixed coefficients are strong simplifications. Uniform rationing is **not** an endorsed UNIRA policy: in real deployment essentials and vulnerable populations must receive priority.
- Monetary U investment budget is an **exogenous illustrative financing constraint**, not a fully reconciled stock-flow-consistent system. Funding origin and liabilities are not modeled here.
- Depreciation and replacement investment are represented, but investment does not expand capacity above its initial value when maintenance is fully funded. No endogenous productivity growth or construction lead times.
- Labour hours are sectoral technical coefficients, not derived from the 30-hour workweek or a real population. The 5,000 U salary and child allowances are not simulated. This prototype **cannot** establish their affordability.
- The input-output matrix excludes resource depletion and emissions. A production index of 100 has no comparable physical units across sectors.
- There is no calibrated comparison to an existing or reformed economy. No claim of UNIRA superiority follows.

## Next milestone: V6.0

1. Calibrate a single region with real input-output tables (OECD ICIO, Eurostat or national supply-use tables), labour hours and energy balances.
2. Replace sector indices with unit-consistent commodity vectors and quality-adjusted service outcomes.
3. Model priority allocation of food, healthcare, energy and safe housing, not uniform rationing.
4. Introduce investment lead times, maintenance, material supply constraints, climate and energy transition pathways.
5. Reconnect the physical system to complete financial balance sheets and a binding 30-hour labour constraint.
6. Compare baseline, reformed economy and UNIRA **under matched real resource endowments**, not by presuming different efficiency.

## Reproduce

`python model.py --out .`

`python -m unittest -v test_model.py`

Only Python standard library is required.
