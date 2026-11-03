# UNIRA V6.3 — Can France work 30 hours from year 1? A ledger in hours

**Status:** empirically anchored accounting of physical labour time. It is not a forecast and not a model of UNIRA's currency. France is a **regional pilot**. Europe (EU27) is also tested as **one pooled entity**, per the design clarifications (`DESIGN_CLARIFICATIONS_2026-11-03.md`): the world is one entity, there is no commercial competition, and allocation follows needs × population. Everything regenerates with `python3 run_all.py` (71 tests).

| component | question | note |
|---|---|---|
| `io/` | Where do France's 45 bn working hours go, and how many are tied to market-specific activity? | `io/RESEARCH_NOTE.md` |
| `flows/` | What share of each labour-reserve pool actually enters work within a year? | `flows/README.md` |
| `health/` | Can health and care staff be found in year 1? | `health/outputs/` |
| `ledger/` | Putting it together: is the 30 h gap covered in year 1? | `ledger/outputs/year1_ledger.csv` |

## 1. Where the hours go (France 2022, 45.0 bn hours)
| final use | share of hours |
|---|---|
| household consumption | 32% |
| public services | 26% |
| investment | 17% |
| exports (to other regions) | 21.5% |

Imports embody 10.9 bn hours-equivalent at French technology, so France receives more labour than it sends. Market-specific activities (advertising, speculative finance, real-estate intermediation, part of insurance and legal/consulting) free **1.7% / 3.9% / 6.6%** of all hours under modest, moderate and deep reductions. The levels are normative choices. Longer-lasting durables save few *French* hours (≤0.35%) because most durables are imported: stock-first mainly saves labour and materials abroad.

## 2. Empirical take-up of the labour reserve (`flows/`)
Observed year-on-year job-finding rates (France 2023):
- unemployed: 41%;
- extended labour force: 25%;
- part-timers moving to full time (proxy): 23%.

Best three European countries: 61% and 36%.

**These gross rates are mostly normal churn, offset by job losses.** The net year-1 effect of an active mobilisation policy is better measured as the **gap to best practice**: +20 points for the unemployed and +11 for the extended labour force. That adds about **0.53 m people** in France in year 1, far below V6.2's synthetic central assumption (1.8 m). This is the most important correction in V6.3.

## 3. Health and care (`health/`)
30 h with θ≈0 in care requires 16.9% more people in section Q:

| occupation | practising | extra needed | training lead time* | years to close if training intake doubles |
|---|---|---|---|---|
| nurses | 607,644 | ~103,000 | 3 yrs | 8 |
| physicians (upper bound) | 266,380 | ~45,000 | 9+ yrs | 15 |
| caring personnel | 859,956 (2021) | ~145,000 | ~1 yr | graduate data MISSING |

\*Lead times are REPORTED_NEEDS_RECHECK.

- Nurse graduates average about 24,800 per year, against implied exits of about 20,300 per year.
- **No training system can respond within year 1.** Health is the binding year-1 constraint whatever happens to total labour.
- France reports no "licensed but not practising" count, so the qualified reserve is MISSING; national sources (DREES) are a follow-up task.
- The job-vacancy rate in health and social work is already 2.9–3.8% (2022–25).

## 4. Year-1 ledger (`ledger/`)
| case | θ (market/care) | mobilisation | avoidable output | France: uncovered share of hours | France: productivity gain still needed | Europe pooled: gain still needed |
|---|---|---|---|---|---|---|
| low | 0.10 / 0 | best-practice gap | modest | 12.6% | 14.7% | 15.7% |
| **central** | 0.20 / 0.05 | best-practice gap | moderate | **8.9%** | **10.2%** | **11.1%** |
| optimistic | 0.35 / 0.15 | full best-practice rates | deep | 0.4% | 0.5% | 1.8% |
| maximal | 0.35 / 0.15 | job guarantee (100% of slack) | deep | 0% | 0% | 0% |

**Rule 14, "everyone able to work, works"** (user, 2026-11-03). The employment rate (ages 20–64) is raised to a target. Entrants have 75% productivity in year 1; θ is central and market-specific activity is reduced moderately.

| target employment rate 20–64 | France: people entering work | France: gain still needed | Europe pooled: gain still needed |
|---|---|---|---|
| 84% (best observed in Europe: IS 85.3%, NL 83.5%) | ~3.6 m | **2.6%** | 4.4% |
| 88% (beyond any observed country) | ~5.1 m | **0%: gap closed** | 1.3% |
| 92% | ~6.6 m | 0% | 0% |

With universal work at around 88%, France's 30 h week holds in year 1 at today's output under central assumptions, and so does Europe at 92%. The conditions:
- workplaces, equipment and supervision for 4–5 m new workers in year 1 (capital lead times not yet modelled);
- childcare and eldercare so parents and carers can work. Those care hours are themselves part of the demand;
- entrant productivity reaching 75% in year 1 (SYNTHETIC);
- health and care staffing remains the binding constraint because of training lead times (§3).

In the central case the 7.6 bn-hour gap is covered as follows:
- **18%** by the productivity response to shorter hours (θ);
- **6%** by mobilisation;
- **23%** by reducing market-specific activity;
- **the remaining ~53%, about 8.9% of all hours, is uncovered.**

## 5. Findings
1. **On central evidence, 30 h from year 1 leaves France about 9% short of today's output**, unless hourly productivity rises about 10% at once, which is a decade or more of trend growth. Europe pooled as one entity is in the same position (about 11%): every European region faces the gap at the same time.
2. **The gap closes only under the optimistic or maximal cases.** These require a job guarantee (or job-finding rates beyond the best observed) plus deep reduction of market-specific activity plus the upper range of θ. That is a coherent UNIRA programme, but it has not been observed anywhere, and its feasibility is the claim to test.
3. **UNIRA's distinctive institutions contribute a measurable share.** Removing commercial competition and speculation covers about a quarter of the gap in the central case (up to ~40% in deep scenarios). This is the first quantified UNIRA-specific contribution, not an assumed efficiency bonus. A reformed-market baseline (B) could capture part of it, which still needs testing.
4. **Health and care cannot be staffed for 30 h in year 1** (about 100 k nurses, about 145 k care workers) because of training lead times. If the 30 h rule applies from day one, essential-care rights are at risk unless explicit measures are designed, for example:
   - care-assistant training for mobilised entrants;
   - voluntary return of qualified staff;
   - inter-regional support under the One Earth framework;
   - task redesign.

   Choosing among these is a governance decision for the user, not a modelling choice.
5. **What remains to be measured, in priority order:**
   - the take-up a *job guarantee* actually achieves (no evaluated example at this scale);
   - physical output that is genuinely unneeded (food waste and overproduction, in physical units);
   - **world-level sufficiency** under needs × population allocation (global MRIO).

## 6. Limitations
- Euro coefficients are only a technical proxy.
- 51% of IO hours are allocated by persons within parent groups.
- IO year 2022 is combined with the 2023 hours gap.
- Take-up rates are status-quo flows; the best-practice gap is an interpretation, not a policy evaluation.
- France's sector mix is used for θ and avoidable output in the Europe-pooled case.
- Health requirements use the section-Q ratio for every occupation.
- Lead times need verification.
- UNIRA's own institutional work (UGTN, allocation bodies, democratic governance) is not yet counted as new demand for hours.
