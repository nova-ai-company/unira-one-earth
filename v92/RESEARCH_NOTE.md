# UNIRA V9.2 — The working week during the transition

**Status (2026-11-08): preliminary, not peer reviewed. The proposal in `PROPOSED_CONSTITUTION_CHANGES.md` was approved by the author on 8 November 2026 and is in the constitution (Article 6 "time", T-10, Article 40.2); see `CONSTITUTION_CONSISTENCY_CHECK.md`.** Produced with an AI assistant from the V6.2 labour model and its frozen Eurostat data. Research basis only, not independent evidence.

## 1. The question (author, 2026-11-06)

> "In the beginning we can increase the number of hours to ensure we don't have any gap in productivity until AI replaces some stuff, and we can decrease the hours but guarantee the same salaries."

Restated as a rule that can be tested:

1. On joining, a region's standard week starts at the **shortest week its existing labour reserve can cover without any productivity gain**, never above 40 hours (8 hours × 5 days).
2. The **full base salary** (Article 14) is paid from the first day, whatever the length of the week.
3. Each year the week is **shortened by the region's measured productivity growth**, pay unchanged (this is already Article 13.3), until it reaches the 30-hour standard of Article 6. It never rises again.

The trigger is *measured* productivity, from whatever source (automation, AI, organisation). Nothing is assumed about AI: if productivity does not grow, hours simply stay where they are, and that is reported, not hidden.

## 2. Why it matters

The paper's condition 1 (`paper/UNIRA_PAPER_V1.md` §3) is the one that rests on the weakest evidence: a 30-hour week from year 1 needs either a 20% rise in output per hour or an employment rate of 88%, above any country's record, and the hours–productivity elasticities are extrapolated beyond any evaluated reform (V6.2 §4c). The 35-hour comparator of V6.2 §4d was "within reach on current evidence" but was rejected as a design on 2026-11-03. The author's new direction makes the starting week a *measured* value and 30 hours the destination.

## 3. Method

`hours/hours_path.py` reuses the V6.2 labour-reserve model (`v62/src/unira_v62/labour_reserve.py`) and its manifest-verified Eurostat data for 30 European countries, employees, 2023 (2024 as a robustness year):

- For every whole-hour cap from 30 to 40, the hours removed by the cap and the output-per-hour gain needed with no mobilisation (`required_gain_no_mobilisation`).
- The existing reserve: the unemployed plus people available but not seeking (the V6.2 "slack" framing, the smaller of its two framings). Entrants work the capped week at productivity ρ relative to incumbents: 1.0 (upper bound) and **0.75 (central, conservative)**; both are V6.2 assumptions, not estimates.
- **Starting week** = the shortest cap at which the reserve maintains the region's hours (residual gain 0).
- **Years to 30 hours** when the week falls as 1/(1+g) per year with output and pay unchanged, for France's measured value-added-per-hour trends (2015–19: 0.57% a year; 2015–23: 0.06% a year, from `v62/outputs/summary.json`) and for illustrative rates of 1, 1.5, 2 and 3% a year (not forecasts).

Nothing is random. `hours/tests/` (9 tests) checks reproducibility, agreement with the V6.2 outputs and research note, monotonicity in the cap, and the definition of the starting week.

## 4. Results

**France 2023, employees capped, central assumption (ρ = 0.75).**

| Week | Hours removed | Gain needed, no mobilisation | Existing reserve covers | Gain still needed |
|---|---|---|---|---|
| 30 h | 16.8% | 20.2% | 39% | 11.5% |
| 32 h | 13.0% | 15.0% | 54% | 6.4% |
| 33 h | 11.1% | 12.5% | 65% | 4.0% |
| 34 h | 9.3% | 10.2% | 82% | 1.7% |
| **35 h** | 7.4% | 8.0% | **106%** | **0** |
| 36 h | 5.5% | 5.8% | 148% | 0 |
| 38 h | 1.7% | 1.7% | 509% | 0 |
| 39–40 h | 0 | 0 | — | 0 |

With entrants as productive as incumbents (ρ = 1.0) the starting week is 34 h (reserve covers 109%). France's reserve is about 3.1 million people; at 35 h about 2.5 million of them are needed. The 2024 data give the same starting week.

**Starting week across 30 European countries, 2023 (ρ = 0.75):** 33 h in 2 countries (Spain, Italy), 35 h in 3 (France, Finland, Netherlands), 36 h in 4, 37 h in 4, 38 h in 8 (Germany among them), 39 h in 7 (Poland, Slovenia among them), 40 h in 2 (Iceland, Malta). The EU27 aggregate starts at 36 h (35 h with ρ = 1.0). Countries with high employment and long usual hours start longest: they have less reserve and more to remove. No country needs more than 40 h.

**Years from the starting week to 30 h, pay unchanged.**

| Start | at 0.06%/yr (France 2015–23) | at 0.57%/yr (France 2015–19) | 1%/yr | 1.5%/yr | 2%/yr | 3%/yr |
|---|---|---|---|---|---|---|
| 34 h | 206 | 23 | 13 | 9 | 7 | 5 |
| 35 h | 254 | 28 | 16 | 11 | 8 | 6 |
| 36 h | 300 | 33 | 19 | 13 | 10 | 7 |
| 38 h | 389 | 42 | 24 | 16 | 12 | 8 |
| 40 h | 473 | 51 | 29 | 20 | 15 | 10 |

**Reading.** At the productivity France actually recorded in 2015–19, a region starting at 35 h reaches 30 h in about 28 years; at the 2015–23 trend it effectively never does. The 30-hour week within a working life requires productivity growth of 1–2% a year or more, which Europe has not had since the 2000s. Whether automation and AI deliver it is unknown; the rule does not need to know, because it follows the measurement.

## 5. What this changes

- **The paper's condition 1 becomes weaker and better supported.** "Universal work at about 88% employment" is replaced by "a starting week the region's existing reserve can cover (33–40 h in Europe, 35 h in France, measured), falling to 30 h as productivity rises". The evaluated reforms (cuts of ≤10% from ≥39 h) now cover the size of cut involved, instead of being extrapolated.
- **The falsification test on employment** ("employment cannot exceed about 85%") no longer decides the design: at the starting week, the employment rate needed is today's best observed or lower.
- **The money circuit is unchanged by construction.** The hour price is calibrated once, at the starting week, so that incomes buy what is produced (`v64`, `pi = consumption / supply`). Prices are set from embodied hours once (Article 13.4–13.5); when hours fall with output constant, prices and salaries stay where they are. This is reasoning on the existing rules, not a new simulation; if the proposal is adopted, V6.4 should be rerun with the starting week as a check.

## 6. What this does not change (honest limits)

1. **Mobilising the reserve still needs institutions.** No evaluated hours cut created net jobs by itself (V6.2 §4c); take-up is a synthetic parameter. The starting week makes the task 2.5 times smaller than at 30 h, not automatic. Training, childcare, eldercare, accessible jobs and matching remain conditions.
2. **Health and care stay short** at any week, because training takes years (V6.2 §4d: about 0.27 million extra people in France at 35 h, with hours–productivity elasticity near zero).
3. **The reserve is European data.** The rule applies everywhere; the numbers exist only for 30 European countries. Regions with low employment and large informal sectors would start short of 40 h but their reserve and hours are not measured here.
4. **ρ is assumed.** Entrants at 0.75 of incumbent productivity is illustrative; the starting week moves by about one hour between ρ = 1.0 and 0.75.
5. **Self-employed are not capped** in these runs (the V6.2 primary scenario); capping them too raises the gap by about half.
6. **The arrival date at 30 h is not a promise.** It depends entirely on productivity growth, which the project does not forecast. Automation effects are not assumed anywhere in this note.
7. **Fewer hours for the same pay is an increase in hourly pay.** Article 14.4 ("average pay may rise only as fast as productivity") is respected: total pay is constant while productivity rises; the gain is taken as time, as Article 13.3 requires.

## 7. Recommendation to the author

Adopt the rule as a transitional provision (T-10) and amend the "time" right of Article 6 so that 30 hours is the standard reached through T-10, with a 40-hour ceiling and no one working more than before joining. Keep the base salary at 5,000 U from day one at any week. Set no starting hour in the constitution: it is a measured value set by law for each region (as T-8.9 does for other parameters). Do not write any AI expectation into the text.

## 8. Reproduction

```
cd v92/hours && python3 hours_path.py && python3 -m unittest discover -s tests
```

Inputs: `v62/data/raw` (Eurostat, hashes in `v62/data/raw/raw_manifest.csv`), `v62/config/v62_config.json`, `v62/outputs/summary.json`. Outputs: `v92/outputs/hours_path.json`, `v92/outputs/starting_week.csv`. The full pipeline (`v63/run_all.py`) runs this step after V6.2.
