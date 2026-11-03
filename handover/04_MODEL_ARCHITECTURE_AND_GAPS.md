# MODEL ARCHITECTURE — WHAT EXISTS AND WHAT MUST BE BUILT

## Available prototypes
- Housing: stock/reuse, intervention capacity, matching, lexicographic construction minimisation, budget and simplified carbon objectives (V4.7–V5.3). Inspect exact solvers: do not assume full integer optimisation or globally optimal matching until implementation is audited.
- Physical inputs: labour hours, cement, steel, electricity and illustrative emissions per intervention (V5.4).
- Physical/monetary split: goods vs cash availability, sector funding (V5.5).
- Ledger: households, enterprises, government/public fund, investment fund, banking/monetary authority, deposits, loans, inventories and capital/depreciation (V5.6–V5.7). Verify all stock-flow identities and transaction-flow matrix closure.
- Dynamic economy: 20-year capital maintenance, demand growth, shocks and financing diagnostics (V5.8).
- Six-sector physical Leontief-like input-output model with capacity/labour constraints, simplified investment (V5.9).
- Empirical anchors: France electricity and labour sensitivity (V6.0–V6.1).

## Desired integrated model (not yet implemented)
Indices: `r` region, `s` sector, `k` commodity, `h` household type, `t` year, `j` intervention/project.
- `N[r,h,t]` household counts and minimum/comfort needs, adjusted for accessibility, age and climate.
- `S[r,k,t]` usable physical inventories; stocks by quality/condition and spoilage; housing by size, location, occupancy and consent.
- `X[r,s,t]` gross production; `A[k,s]` intermediate input coefficients with consistent units; labour skills matrix `L[skill,s]`.
- `K[r,s,t]` capital stock, investment vintages, lead times, depreciation, productivity and maintenance; energy/material/land constraints.
- Logistics/trade `T[r1,r2,k,t]`, embodied environmental impact, transport capacities, political and rights constraints.
- Household matching and rationing priority: emergency essentials first, protect vulnerable groups, guarantee rights and preference constraints.
- Monetary SFC: transaction-flow matrix `F[sector_from, sector_to, category,t]`, balance sheets, deposits, liabilities, U price vector, government/investment funding, taxes/transfers if applicable, corporate reserves/surplus, credit defaults and money issuance. Every financial asset has matching liability; each flow has counterparty.
- Price stability: derive nominal income vs available baskets, supply bottlenecks, savings, distribution, velocity and monetary-policy responses; no assumed automatic zero inflation.
- Objective: multi-criteria welfare/rights adequacy, physical feasibility, environmental ceilings, distribution fairness, resilience, cost and democratic legitimacy. Report Pareto frontiers and trade-offs; do not reduce rights to cheap scalar penalties.

## Formal checks to implement
1. Physical conservation per commodity and region: opening inventory + production + imports − intermediate use − final consumption − exports − losses = closing inventory.
2. Labour allocation by skill and sector ≤ available effective hours (30h policy plus leave/absences, essential staffing and training).
3. Capital evolution with investment lead times, depreciation and damage; maintenance cannot be counted as new capacity unless justified.
4. Monetary sectoral balances sum to zero for each transaction and all periods; financial stocks reconcile to prior stocks plus flows and revaluations.
5. Goods delivered and services actually provided, not just invoiced or budgeted.
6. No double counting between intermediate and final goods, housing stock vs annual construction flow, gross and net firm surplus, and nominal and real values.
7. Tests for infeasible conditions, missing data, sector bottlenecks, climate shocks, cyber/payment outages, governance capture and rights breaches.

## Numerical methodology
Start with transparent static accounting (supply-use, hours, physical needs), then constrained optimisation, then dynamic simulation, then stochastic sensitivity. Use Python standard libraries where possible; if scientific solvers needed, pin versions and publish environments. Provide data provenance, calibration notebooks, test suite, seed control, error bounds and independent replication. Do not claim 'exact' if model relaxes integrality or omits constraints.
