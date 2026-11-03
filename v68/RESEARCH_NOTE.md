# UNIRA V6.8 — UNIRA versus a reformed market economy, with matched resources

**Question:** the master specification requires matched-resource counterfactuals. If a reformed market economy (B) has the same population, technology, capacities, productivity response and targets (a 30 h week and a comfortable life for all), how much better does UNIRA (C) do, and *which institutions* make the difference?

**Method:** `counterfactual/compare.py` reruns the existing models: the year-1 labour ledger (v63) and the 30-year world transition (v67) with the health plan (v66). Only institutional levers change between runs. Each lever is then switched from B to C on its own, to attribute the difference. 5 tests.

## Levers
| lever | B: reformed market | B2: ambitious cooperative market | C: UNIRA |
|---|---|---|---|
| employment, ages 20–64 | 84% (best observed) | 84% | 88% (universal work) |
| market-specific activity | modest cut | modest cut | moderate cut |
| new clean energy to regions in need | 20% (verified: today's clean-energy investment in developing economies excl. China; Africa 2%) | 50% | 100% (needs first) |
| energy cut in rich regions | 2%/yr | 3%/yr | 3%/yr + military energy freed |
| health training | +7%/yr | +7%/yr | ambitious + soldiers volunteer + prevention |
| new health workers to regions in need | 50% | 75% | 100% |
| new homes to regions in need | 30% (assumption: no source splits construction by income group) | 50% | 75% |

Verified values come from `verification/` (11 items checked against primary sources, 2026-11-03).

## Results (central capacities; outputs in `outputs/comparison.json`)
| outcome | B | B2 | C |
|---|---|---|---|
| France year 1: extra output per hour still needed | 5.0% | 5.0% | **0%** |
| Europe pooled, year 1 | 6.8% | 6.8% | 1.3% |
| everyone at 40 GJ energy by | not within 30 yrs | not within 30 yrs | **year 27** |
| everyone at EU-level care (131/10k) by | not within 30 yrs | not within 30 yrs | **year 30** |
| energy shortfall closed by year 15 | −14% (gap grows) | 14% | **60%** |
| health shortfall closed by year 15 | −4% | 4% | **38%** |
| housing shortfall closed by year 30 | −21% | 10% | **50%** |
| peak world final energy | 409 EJ | 409 EJ | 409 EJ |

## Attribution: which institution matters (one lever switched from B to C)
- **Needs-first allocation of new energy** alone brings every region to 40 GJ by year 27. Without the rich-region cut and freed military energy, though, world energy peaks at 453 EJ, outside the climate envelope. **Allocation and restraint must go together.**
- **Needs-first allocation of new homes** alone moves housing from −21% to +50% by year 30.
- **The health programme plus in-region training** are both needed. Either one alone gives only about 10% by year 15.
- **Universal work (88% vs 84%)** alone cuts France's year-1 need from 5.0% to 1.9%. **Removing commercial competition** alone cuts it to 2.6%. Together they close the gap.
- Military energy freed and the faster rich-region cut matter mainly for the climate, not for convergence speed.

## Boundary test: how cooperative would a market world need to be?
B2 is given ever larger shares of new energy, health workers and homes for regions in need. Everything else stays market (militaries kept, today's training expansion, 84% employment).

| share of new capacity to regions in need | everyone at 40 GJ by | energy closed by year 15 | health closed by year 15 | housing closed by year 30 |
|---|---|---|---|---|
| 50% | not within 30 yrs | 14% | −4% | 10% |
| 65% | not within 30 yrs | 28% | 1% | 34% |
| 80% | not within 30 yrs | 41% | 5% | 50% |
| 90% | year 29 | 51% | 8% | 50% |
| 100% | year 27 | 60% | 11% | 50% |
| **C, UNIRA** | **year 27** | **60%** | **38%** | **50%** |

**Reading:**
- A market world that directs about 90% of new capacity by need nearly matches UNIRA on energy and housing. That is far beyond today's 20%, and it would effectively *be* needs-first allocation.
- It still lags far behind on health (8% vs 38% by year 15). UNIRA's health advantage comes from the scale of the training programme, disarmament volunteers and prevention, not from allocation alone.

## Interpretation
1. **Under matched resources, UNIRA's institutions, if they work as designed, deliver convergence that a reformed market does not.** That holds even with ambitious international cooperation (B2). Under today's allocation patterns (B), the gaps *widen* as population grows.
2. **The advantage is entirely institutional.** It comes from directing new capacity by need rather than by purchasing power, from universal work, and from removing market-specific activity. None of it comes from an assumed efficiency bonus: technology, productivity response and capacities are identical.
3. **That is also where UNIRA must prove itself.** The model shows what needs-first allocation and universal work would achieve. It cannot show that a world institution can allocate 100% of new capacity by need without error, delay or capture (falsification test 5), or that 88% employment is reachable. A reviewer can fairly say that B2 with stronger transfers (say 80% of new capacity to regions in need) would close much of the gap without the rest of UNIRA. Testing that boundary is the next step.

## Limitations
- B and B2 lever values are policy scenarios (SYNTHETIC) except where verified.
- One-at-a-time attribution ignores interactions (the energy + restraint interaction is noted above).
- Behaviour, governance and transition costs of building UNIRA's institutions are not modelled.

## Verification of earlier figures (`verification/verification.md`)
- **Confirmed:**
  - military 5.5% of global emissions (SGR/CEOBS 2022, range 3.3–7.0%). No global military *energy* statistic exists, so the energy share is a proxy;
  - consumer food waste 19% (UNEP 2024);
  - supply-chain loss 13.3% (FAO 2023);
  - 669 GW of solar and wind added in 2025 (IRENA);
  - military spending USD 2,887 bn, 2.5% of world GDP (SIPRI 2025).
- **Corrected:**
  - GP training in France is 6 + 4 = 10 years (the V6.3 health model is updated: doubling intake closes the physician gap in 16 years);
  - nursing is 3 years (4,620 h from Sept 2026);
  - development aid is 0.26% of donor income in 2025 (0.34% in 2024; target 0.7%);
  - the 3.4 bn m² of world homes is a *net* stock increase (gross construction is higher);
  - the top 20–64 employment rates in 2025 are IS 85.8, MT 83.6, NL 83.4.
- **Not found:** a world total of medical graduates; construction by income group.
