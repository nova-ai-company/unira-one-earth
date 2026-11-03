# UNIRA V5.8 — Twenty-year economic stress prototype

## Scope and scientific status
This is an **illustrative**, single-sector, annual, 20-period computational experiment, not a real-world forecast, complete stock-flow-consistent macro model, or validation of UNIRA. Every numerical coefficient is invented for testing. No empirical cost or carbon calibration is asserted.

## Core design
- 100 households and 100 workers initially; 1,500 hours per worker/year (30 hours/week × 50 weeks).
- Household needs: 1 abstract consumption unit per year; base wage 5,000 U/month/worker. Units are NOT real food quantities or housing.
- Production capacity constrained by productive capital and working hours; investment consumes labour and adds capital; 4% annual capital depreciation.
- Physical stock accounting: opening inventory + output = delivered + closing inventory.
- Wage transfers, household purchases, taxes, distributable business surplus and public payments are recorded as sector cash transfers.
- Government public-service spending is represented as a transfer to the household sector, a deliberately crude proxy that does NOT represent physical public-service output or separate provider balance sheets.
- Any firm or government cash deficit is automatically funded by new bank credit. Total deposits = cumulative loans because the model starts with zero deposits and loans. The borrowing limit is an **alert**, not a binding rationing mechanism.
- A shortage-responsive price rule is included only as a toy feedback mechanism. It is not an estimated inflation equation, equilibrium price model, or purchasing-power guarantee.

## Scenarios and interpretation
The baseline is engineered to deliver exactly 100 consumption units per year while replacing depreciated capital. It is **not** evidence that UNIRA can do so. The supply shock removes 70% of year-5 production; population growth increases needs without adding workers or capital; zero investment allows productive capital to erode; the credit ceiling test flags financial exposure without physically restricting production.

A one-year 70% labour shock is absorbed in this particular example because production is **capital-constrained** and substantial unused labour capacity exists. This does not mean labour shortages are harmless. Results change when hours become binding.

## Major limitations
1. One abstract good; no food/housing/health/energy input-output linkages, supply chains, transport, or ecological ceilings.
2. No demographic age structure, skills, regional distribution, unemployment, migration, or accessibility.
3. No interest, loan repayments, default, central bank, reserves, net worth, bank capital, external sector, or reconciled national accounts.
4. Public-service output is not measured. Child allowances and disability guarantee are not yet simulated.
5. Corporate surplus is a cash-flow fraction rather than distributable profit after full costs and investment reserves; this is NOT UNIRA's final institutional rule.
6. Credit limit is diagnostic only; not an actual funding constraint. No monetary-policy credibility or empirically grounded inflation mechanism.
7. The baseline wage is nominal; 5,000 U purchasing power is unproven.
8. Rounded output in CSV may introduce tiny arithmetic differences; full-precision identities are checked before rounding.

## Next research steps
Build a true multi-sector transaction-flow matrix with bank and monetary authority balance sheets, enforce credit limits, include explicit public-service capacity, physical input-output coefficients, heterogeneous household needs, regional constraints, and benchmark reformed-market versus UNIRA scenarios with identical initial physical endowments. Empirical calibration requires independently sourced data, uncertainty bounds, and falsifiable performance metrics.

## Reproduce
`python -m unittest -v` and `python model.py` from this folder (Python standard library only). Outputs: annual_results.csv, summary.json, assumptions.json.
