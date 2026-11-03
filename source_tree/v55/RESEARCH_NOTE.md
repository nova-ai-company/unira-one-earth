# UNIRA V5.5 — Physical–monetary consistency prototype
**Date:** 2026-11-03  
**Research status:** synthetic stress-test, not empirical calibration, inflation forecast, general-equilibrium model, or proof of viability.

## Purpose
Separate three distinct questions: (1) do enough *physical* goods and services exist? (2) do households have sufficient purchasing power at a defined illustrative price schedule? (3) can a public fund meet its obligations? A positive answer to one does not guarantee the others.

## Core rules implemented
- 30-hour workweek, 50 weeks/year in baseline (1,500 hours/worker-year); test 44-week sensitivity.
- 5,000 U/month base-pay reference and no adult household income cap; maximum individual salary of 25,000 U is a policy rule but **the toy model does not simulate the full salary distribution or enforce this cap on arbitrary inputs**.
- Child benefit: `min(1000 × children, max(0, 15000 − adult household income))`. Adult income includes a disability guarantee where applicable; adult income itself is never capped at 15,000 U.
- Essential services are modelled as distinct labour and financial requirements, not charged to household shopping baskets.
- Separate production, public services and maintenance hours; separate public-fund cash-flow check.

## Toy baseline and stress tests
100 households, 120 workers, fixed toy capacities for food, housing services and other goods. All quantities, prices, labour coefficients, spending propensity and public-fund values are **invented demonstration inputs**. Household income is derived from illustrative household incomes, **not reconciled to payroll of the 120-worker production economy**. The worker payroll number is an independent diagnostic; do not add it to household income or claim monetary stock-flow consistency.

| Case | Physical basket + labour feasible? | Public fund sufficient? | Key issue |
|---|---|---|---|
| Baseline | Yes | Yes | Only under deliberately chosen toy capacities |
| Food supply shock | No | Yes | Food units below desired physical quantity |
| Shorter work year | Yes | Yes | Reduced labour buffer, but still sufficient in this toy case |
| Housing supply shock | No | Yes | Housing services insufficient |
| Public fund gap | Yes | No | 1.3m U funding shortfall |

Baseline annual household income: **10.2m U**; 75% nominal spending envelope **7.65m U**; cost of desired annual basket at fixed toy prices **5.484m U**. This is a **budget arithmetic comparison**, not measured purchasing power or an inflation prediction. Goods are not allocated by household and individual affordability is not tested; no transaction ledger, endogenous price mechanism, savings accounting, taxation, firm balance sheets, investment supply chain, trade, monetary issuance rule, or public-fund revenue source is implemented.

## Interpretation and research safeguards
1. **No arbitrary euro/U conversion.** U prices are placeholders, not prices derived from labour, scarcity or real-world data.
2. **No inflation forecast.** A supply gap could manifest as queues, rationing, higher prices, imports, or deferred consumption, depending on institutions. The model predicts none of these mechanisms.
3. **Do not conflate nominal and real wages.** 5,000 U/month cannot establish a comfortable standard of living until the accessible goods basket and allocation rules are specified.
4. **Avoid double counting.** The 120-worker payroll and household income belong to different illustrative ledgers; they are not a closed circular flow.
5. **Resource opportunity costs persist.** Producing more food may divert land, water, energy or skilled labour from other sectors; those interdependencies are not modelled.
6. **Public-fund balance is partial.** The model checks a stipulated revenue against stipulated obligations, but does not explain where revenue comes from or whether it is sustainable.
7. **Baseline deliberately passes.** This is software validation, not evidence that a real UNIRA economy works.

## Next research milestone — V5.6
Build a *closed stock-flow-consistent* institutional accounting model: workers and households, firms, public fund, investment and monetary authority, with transaction identities and sectoral balances. Add labour skills and resource input-output links, income distributions, household-specific minimum consumption, scarcity allocation rules, fiscal/monetary controls and a shock-response policy. Only then start calibrating physical coefficients to real statistical sources (ILO, OECD input-output, FAO, IEA, housing-sector LCA) with transparent uncertainty ranges. Compare current, reformed and UNIRA institutions against the **same** resource endowments and wellbeing requirements.

## Reproducibility
Run `python model.py` to generate `results.json` and `results.csv`; run `python -m unittest -v` for eleven tests. No external packages or internet needed. Source files are in this archive.
