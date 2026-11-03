# UNIRA V6.1 — France labour accounting and 30-hour transition

## Scope and provenance

INSEE reports **30.5 million employed people at end-2025**, including employees and self-employed people. INSEE reports **1,656 effective annual hours for full-time employees in 2025** and **38.9 usual weekly hours**. These describe DIFFERENT populations and measurement concepts. See `sources.csv`.

## Why this version matters

Earlier UNIRA exercises compared hours across populations too casually. This release explicitly avoids using 1,656 hours as the observed mean for all 30.5 million workers. No empirical national labour-hour total is claimed.

The program uses assumed average hours of 1,400, 1,500 and 1,600 hours **only as sensitivity values**, plus a labelled full-time-only reference. The UNIRA target is 30 hours/week times an assumed 46 effective working weeks = 1,380 annual hours. This is not a prediction of actual leave or sickness patterns.

Under constant worker numbers and unchanged total output, required productivity/hour growth is `(current_hours / target_hours) - 1`. This is an **arithmetic requirement**, not a prediction of feasible productivity growth. It excludes sector mix, part-time status, self-employment, capital, input-output constraints, household unpaid work, unemployment transitions, output reduction from eliminating waste, and international supply chains.

## Three policy comparisons

A: Current economy with measured sector-specific work hours and output.
B: Reformed economy with 30-hour target, productivity investment and stock-first reuse.
C: UNIRA with the same starting assets, workforce and demand, plus income guarantees and allocation rules.

These scenarios must not be granted different initial resources or unexplained productivity bonuses. All future work must preserve the distinction between physical feasibility and monetary viability.

## Parallel research workstreams

1. Labour: employment status, full-time/part-time, sector hours, skills and staffing.
2. Physical production: sector outputs, material inputs, energy and supply chains.
3. Needs: households, food, housing, health and service standards.
4. Money: full stock-flow consistency, public financing and U purchasing power.
5. Validation: independent replication, source audit, sensitivity and adversarial scenarios.

This package implements workstream 1's preliminary sensitivity model. The other workstreams are planned, not completed.

## Next data priorities

Obtain hours worked for ALL employed people by industry, preferably annual national accounts total hours worked, plus value added and sector output. Match years, definitions, units, and territorial coverage. Use measured sector production and input-output tables to calculate the real effect of a 30-hour transition, including shortages and productivity requirements.

## Status

Empirically anchored **sensitivity study**, not a calibrated national economy, not proof of UNIRA feasibility, and not an estimate of its expected economic impact.
