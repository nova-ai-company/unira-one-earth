# UNIRA V5.6 — Monetary transaction conservation and physical constraints
Date: 2026-11-03

## Scope
A reproducible **synthetic transaction-ledger prototype**, not an empirically calibrated or complete stock-flow-consistent (SFC) macroeconomic model. It advances V5.5 by reconciling every included monetary transfer and explicitly recording issuance. All input quantities are invented. No U/EUR conversion is implied.

## Institutional accounts
Five aggregate accounts: households, firms, public fund, investment fund and monetary authority. Transfers debit one account and credit another; no overdrafts. Issuance is an explicit external event. Total balances always equal cumulative issuance. Monetary-authority liabilities and counterpart assets are **not** separately represented; therefore this is **not double-entry financial accounting** and cannot establish financial sustainability. In particular, the public fund is not assumed to have unlimited access to monetary creation.

## Baseline assumptions
- 10 paid workers × 5,000 U/month × 12 = 600,000 U annual payroll, **not** a representative sample of global wage distribution.
- Firms begin with 1,000,000 U of explicitly issued working capital.
- Firms pay 600,000 U wages, transfer 140,000 U to public fund and 80,000 U to investment fund.
- Households spend 350,000 U with firms and contribute 60,000 U to public fund.
- Investment fund buys 40,000 U of capital goods from firms.
- Public service procurement obligation 500,000 U; public fund has 200,000 U and pays only that amount. The unpaid 300,000 U is an **unfunded obligation**, not an automatically issued debt.
- Physical food demand 100 units, baseline supply 110; 10 workers × 1,500 hours = 15,000 available hours versus 12,000 hours needed.
- Food units and labour hours are independent screening indicators. **No detailed production functions, pricing, consumption baskets, stocks or trade linkages** have been implemented.

## Results
Baseline food gap 0, labour gap 0, public funding gap 300,000 U. Reduced food supply to 70 creates 30-unit shortfall without altering ledger conservation. Reducing worker hours to 1,000 creates a 2,000-hour labour gap. Increasing issuance to firms does not change food output in this prototype. Lowering public procurement obligation to 150,000 U closes the public-fund gap but does not imply that adequate public services were provided.

## Critical interpretation
A balanced transaction ledger is a **necessary accounting check**, not evidence of price stability, macroeconomic equilibrium, adequate purchasing power or economic feasibility. Initial monetary issuance is an assumed policy choice with no modelled governance, repayment or inflation response. Firms' transfer to the public fund is a stipulated distribution; production costs, retained profits, firm net worth and capital depreciation have not been reconciled. The child allowance formula and disability guarantee from UNIRA policy are not yet represented in this aggregate 10-worker toy economy. Household cash holdings do not measure access to adequate goods.

## Priority for V5.7
1. Introduce full sectoral balance sheets (financial assets, corresponding liabilities, real capital, inventories), transaction-flow matrix, and period-end consistency identities.
2. Implement firm output and sales, input requirements, depreciation, investment, government services, taxation/contributions and household heterogeneity, including child allowances and disability guarantees.
3. Specify a bounded, democratically governed issuance rule and stress test scarcity, queues, inflation pressure and public deficits, without treating monetary creation as real production.
4. Calibrate physical resource coefficients and household needs using official evidence; compare current, reformed and UNIRA institutions under identical resource constraints.
5. Validate model against external macro accounting references and test sensitivity rather than claim proof of feasibility.

## Reproduce
`python model.py` generates `results.json` and `results.csv`. `python -m unittest -v` runs 12 tests. Python standard library only.
