# UNIRA V5.7 — Institutional balance sheets and physical stocks

**Status:** synthetic, exploratory research prototype. 3 November 2026.

## Purpose
This model moves beyond the V5.6 transfer-only ledger by recording deposit liabilities, bank loans, monetary-authority reserve advances, sector financial positions, physical inventories, fixed-capital book value and depreciation. All amounts are illustrative UNIRA U, not converted euros. No observed metropolitan or global economic quantities are used.

## Accounting mechanics
- Commercial-bank loans create both a borrower deposit (bank liability) and a loan receivable (bank asset). Loan repayment destroys both.
- The monetary authority lends reserves to the commercial bank: the bank records reserves as an asset and an advance payable as a liability; the authority records the corresponding advance asset and reserve liability.
- Payments move deposits between sectors; no transfer creates money.
- Household, firm, government and investment balances are reported alongside bank and monetary authority accounts.
- Goods production adds physical inventory; sale requires available units and deposits; remaining inventory is explicit. Investment increases capital stock and a depreciable book value.
- Equity is calculated as residual assets minus liabilities, and therefore balance-sheet identity tests check internal arithmetic, **not** the correctness of valuation or economic realism.

## Scenario results
| Case | Unmet food units | Labour shortfall hours | Public services unpaid U |
|---|---:|---:|---:|
| Baseline | 0 | 0 | 0 |
| Food supply shock | 30 | 0 | 0 |
| Labour shock | 18 | 3,000 | 0 |
| Public shortfall | 0 | 0 | 310,000 |
| Higher public credit | 0 | 0 | 0 |

The model uses ten workers receiving 5,000 U/month for twelve months, 12,000 required hours, illustrative food production and a single representative consumption good. It does not model the 25,000 U salary cap, household child allowances, household heterogeneity, or the disability guarantee yet. The 30-hour week is compatible with 15,000 available hours in the baseline (10 workers x 1,500 hours/year), but is not an empirically established capacity assumption.

## Critical limitations and accounting caveats
1. **Not a fully stock-flow-consistent macroeconomic model.** Equity is residual, but sector transaction-flow matrices, production accounts, comprehensive expense recognition, and reconciled opening/closing net worth changes are not implemented. The inventory valuation and capital spending are simplified and should not be interpreted as audited accounting statements.
2. Bank capital requirements, defaults, credit risk, interest, debt service and government repayment rules are absent. Unlimited public credit cannot be assumed.
3. The monetary authority reserve advance is not an allocation mechanism for household welfare or production. No monetary-policy rule, inflation model or price discovery mechanism is provided.
4. Physical inventories represent a single good. There is no intermediate-input network, sectoral production technology, energy constraint, maintenance requirement, transport, skill mix, resource depletion or emissions.
5. Investment capital units are illustrative and do not yet affect future productivity; depreciation is accounting-only.
6. No international trade, migration, geographic matching, rights constraints or environmental life-cycle modelling is included.
7. Financial feasibility is not established merely because payments can clear: future obligations, asset quality, real purchasing power and distributional welfare must be analysed.

## Next methodological milestone: V5.8
Build a **transaction-flow matrix and sectoral production accounts** with double-entry validation for wages, intermediate inputs, taxes/transfers, business surplus, investment and depreciation. Add multi-period inventory carryover and investment-to-capacity relationships. Introduce explicit public-finance rules and debt-service constraints; evaluate inflationary pressure as demand relative to feasible output rather than a direct inference from the quantity of money.

## Reproduction
Run `python model.py` to regenerate `results.json`, and `python -m unittest -v` to execute 13 tests. Python standard library only.
