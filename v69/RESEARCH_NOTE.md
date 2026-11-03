# UNIRA V6.9 — Can the One Earth entity allocate well enough?

**Question:** V6.8 showed that UNIRA's advantage over a reformed market comes from directing new capacity (energy, health workers, homes) by need. A real world institution sees needs with errors and delays, some regions exaggerate, and some resources leak. Does the advantage survive realistic governance failures, and what safeguards are needed?

**Model:** `coordination/model.py` + `run.py` (7 tests). The One Earth allocator decides on *perceived* needs:
- measurement error σ: mean-preserving lognormal noise, per region, each year;
- data lag in years;
- a share of regions that inflate their reported need; audits catch each one with a yearly probability;
- leakage: a share of new capacity that reaches no one.

Anything sent to a region beyond its true need is wasted. 30 random runs per scenario on the 30-year world transition (v67), with all other UNIRA levers as in V6.8.

**Evidence** (`evidence/`, 44 sourced rows, 2026-11-03): calibration values, low / central / high.

| failure | low / central / high | basis |
|---|---|---|
| measurement error σ | 0.05 / 0.15 / 0.30 | census undercount 10–19% by province (South Africa 2011); global poverty-count revisions of +400 m / −46 m |
| data lag | 1 / 2 / 5 years | poverty data published about 2 years late; 57 of 155 countries had at most one estimate in 2002–11 |
| leakage, no safeguards | 0.10 / 0.25 / 0.45 | Uganda school grants (87%); India food rations (54% → 9–28%); Brazil audited municipalities 30%; elite aid capture 7.5%; EU cohesion funds 9.3% |
| leakage, strong safeguards | 0.03 / 0.08 / 0.15 | Uganda after the newspaper campaign (< 20%); audits −8 pp (Indonesia); e-payments −19 to −24% (India) |
| regions misreporting | 0.10 / 0.25 / 0.45 | China local GDP +1.7 pp/yr (Liaoning ~20%); Brazil population-threshold bunching |
| misreport inflation | 0.02 / 0.07 / 0.20 | as above |

## Results (median of 30 runs; the 10–90% range is within ±1 point, because errors average out across 179 regions)
| scenario | energy gap closed, yr 15 | health, yr 15 | housing, yr 30 | everyone at 40 GJ |
|---|---|---|---|---|
| UNIRA, perfect allocation | 60% | 38% | 50% | year 27 |
| UNIRA, best observed governance | 57% | 36% | 46% | year 29 |
| **UNIRA, strong safeguards** | **52%** | **34%** | **40%** | **year 29** |
| **UNIRA, no safeguards** | **36%** | **24%** | **19%** | not within 30 yrs |
| UNIRA, worst observed | 15% | 12% | −9% | not within 30 yrs |
| ambitious cooperative market (B2) | 14% | 4% | 10% | not within 30 yrs |
| reformed market (B) | −14% | −4% | −21% | not within 30 yrs |

## Findings
1. **UNIRA's advantage survives realistic governance failures.** Even with typical errors and no safeguards (25% leakage, 2-year-old data, 15% measurement error), needs-first allocation beats the most ambitious market world on energy (36% vs 14%), health (24% vs 4%) and housing (19% vs 10%).
2. **Safeguards are worth about as much as the allocation rule itself.** Strong safeguards recover most of the ideal performance: 52% vs 60% for energy, with everyone reaching 40 GJ by year 29 instead of never. Leakage is the decisive failure. Measurement error and exaggeration matter much less, because errors average out across many regions and audits catch exaggerators.
3. **Under the worst governance ever observed, UNIRA loses its advantage on energy and housing.** It still leads on health, thanks to the training programme and disarmament volunteers. Falsification test 5 is therefore sharpened: **if the One Earth entity cannot keep leakage well below ~45% and data lags under ~5 years, needs-first allocation is not better than a cooperative market.**
4. **Safeguards to build into UNIRA's constitution**, each backed by evidence:
    - independent audits (−8 pp leakage in Indonesia; −8 to −13% corruption in Brazil);
    - public, open data on every allocation, so citizens and media can check (Uganda: 87% → under 20% leakage after newspapers published the grant amounts);
    - direct digital payments and deliveries (−19 to −24% leakage in India). UNIRA's digital U and UGTN invoice system (Article 12) provide this by design;
    - community monitoring (−33% under-five deaths in Uganda);
    - fast data: 1-year lags instead of 2–5.

## Limitations
- Leakage evidence comes mostly from cash and food transfer programmes, not from building energy systems, homes or training. Infrastructure may behave differently (construction-sector corruption is often higher).
- The audit detection rate (50% per year) is an assumption.
- Capture that redirects resources to favoured regions, rather than losing them, is modelled only as loss.
- Political dynamics are not modelled: legitimacy, resistance from regions that receive less, and institutional decay over time.
- Errors are independent across regions; correlated errors (e.g. a whole continent undercounted) would hurt more.
