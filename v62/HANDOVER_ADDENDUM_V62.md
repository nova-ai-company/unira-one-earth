# Handover addendum — V6.2 (2026-11-03)

Read after `handover/00_START_HERE.md`. This addendum does not modify the original handover; it supersedes specific statements as noted.

## What V6.2 delivered
- `v62/`: reproducible stdlib-only package covering France sector hours by NACE section (Eurostat national accounts, all employed persons) and a full-time/part-time decomposition from the LFS. It models a 30 h cap, productivity requirements against historical trends, a labour reserve for 30 European countries, and an evidence-graded pathway.
- **Data:** 12 frozen Eurostat snapshots with SHA-256 hashes.
- **Tests and checks:** 37 tests; 34 machine checks.
- **Audits:** 4 independent audits, consolidated in `v62/audit/AUDIT_FINDINGS.md`.

## Headline results (France 2023; details in `v62/RESEARCH_NOTE.md`)
- All-worker hours: 45.6 bn, 1,501 h/person. This replaces V6.1's 1,400/1,500/1,600 sensitivity values.
- **30 h cap, employees, constant output:**
  - +20.1% output per hour (+29.1% if the self-employed are also capped);
  - about 32 years of the 2015–19 trend, or about 300 years of the 2015–23 trend.
- **Labour reserve (unemployed, extended labour force, underemployed part-timers, employment-rate convergence):** up to 51–59% of the gap. That is an upper bound.
- **Evidence-graded pathway** (literature θ + partial mobilisation): residual about 11% (range 1.6–15.6%).

- **Enforced 35 h alternative (France):** +7.8% without offsets. The reserve covers 142–161% of the gap, and the evidence-graded residual is 0–3.9%. **User decision 2026-11-03: 30 h from the start; staged path rejected.** 35 h is kept only as a comparator.

## Statements in the original handover now superseded
- **02, V6.1 "required productivity 1.45–20%":** superseded. The 46-week convention is not a 30 h rule, and V6.1's output extrapolates a full-time benchmark to all workers.
- **02, V5.6 "public shortfall 300,000 U in independent stress cases":** incorrect. It is in the baseline.
- **04, "Ledger … verify stock-flow identities":** V5.6/V5.7 are not SFC. Treat the monetary block as unbuilt.

## User direction recorded this session
- "Think big" on labour supply. The 30 h week may let unemployed and excluded adults work, and countries have large reserves of such adults. Implemented as `labour_reserve.py`.
- The evidence supports the size of the reserve. It does **not** support automatic job creation from shorter hours. Mobilisation needs deliberate institutions.

## Open decisions surfaced (add to handover/07)
1. How the 30 h rule applies to the self-employed. The headline result moves 9 points on this choice.
2. Whether RTT-type compensatory days survive under a 30 h week (±4 points).
3. Institutions for labour mobilisation: training, care services, regional matching, a job guarantee?
4. Cross-border labour and production coordination, given very uneven reserves (Spain, Italy, Greece high; Germany, Czechia, Iceland low).

## Next
Next steps are V6.2.1 (health and education staffing pipelines; Q86 vs Q87–88), take-up estimation for the reserve, and ILOSTAT global extension. Then V6.3: supply-use tables for avoidable output. See `RESEARCH_NOTE.md §7`.

## Continued in V6.3 (same day)
See `v63/RESEARCH_NOTE.md` and `v63/DESIGN_CLARIFICATIONS_2026-11-03.md`. The design clarifications are:
- 30 h from the start;
- the economy is not the market model;
- the world is one entity with regions;
- no commercial competition;
- allocation by needs × population;
- the salary range is intended;
- surplus goes to the One Earth entity.

The year-1 ledger (central case) leaves France about 9% of hours short (about 10% productivity gain needed). Health and care staffing is the binding year-1 constraint. Empirical mobilisation is much lower than V6.2's synthetic assumption.
