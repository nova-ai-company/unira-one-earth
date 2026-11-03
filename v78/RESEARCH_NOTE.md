# UNIRA V7.8 — An AI model to plan the production One Earth needs

**Author's rule 32:** an AI / machine-learning model helps One Earth decide the production needed, based on data and science by default.

**Questions:**
1. Can machine learning forecast regional needs better than simple rules, on data it has not seen?
2. How large must reserves be to cover forecast errors?
3. Is the AI equally accurate for rich and poor regions (fairness)?
4. Over 30 years, how much does better information change what people actually receive?

**Code:** `planning/data.py`, `forecast.py` (backtest), `information.py` (30-year test), `tests/` (6 tests). Python standard library only. Run with `python3 planning/forecast.py && python3 planning/information.py`.

## 1. Method

**Data:** real history already frozen in the repository. Countries only, no projections.
- Population: UN WPP 2024, 1950–2023, 237 regions.
- Primary energy per person: Our World in Data, 1965–2024, 215 regions.
- Food supply per person: FAO via Our World in Data, 1961–2022, 192 regions.
- Doctors and nurses per 10,000: WHO GHO, 1990–2024, 194 regions.

**Models:** each predicts the log change from the last observed year to 1, 2 or 5 years ahead.
- Simple rules: *naive* (no change), *drift* (5-year average growth) and *trend* (6-year regression).
- Machine learning: *ridge*, a pooled linear model across all regions, with its penalty chosen on validation data. *knn* averages the 30 most similar past growth paths of any region. *ensemble* is the mean of drift and ridge.

**No look-ahead:**
- Models are fitted on outcomes before 2005.
- The model is chosen on outcomes from 2005 to 2009.
- Accuracy is reported only for forecasts made from 2010 onward, refitted on all data before 2010.

**The rule tested ("science by default"):** an ML model is adopted only if it beats the simple rules on the validation period.

## 2. Results: needs are highly predictable

Median absolute error of the model chosen on validation, out of sample 2010–2024 (`outputs/backtest.json`):

| need | 1 year ahead | 2 years | 5 years | model chosen (1 / 2 / 5 yr) | reserve for 95% cover, 2 yr |
|---|---|---|---|---|---|
| population | **0.10%** | 0.31% | 1.07% | knn / knn / knn | 1.4% |
| food supply per person | 0.99% | 1.40% | 2.53% | ensemble / knn / ridge | 4.0% |
| doctors per 10,000 | 1.56% | 2.56% | 6.81% | ensemble / ensemble / trend | 17% |
| nurses per 10,000 | 1.81% | 3.55% | 7.96% | drift / trend / naive | 20% |
| energy per person (today's markets) | 3.96% | 6.02% | 12.9% | naive / naive / ridge | 24% |

- **ML helps where needs follow structure.** For population, kNN cuts the 1-year error from 0.20% (best simple trend) to 0.10% and the 5-year error from 1.33% to 1.07%. For world population the errors partly cancel: 0.03% at 1 year and 0.48% at 5 years. For food and health workers, ML models are best or near best.
- **ML does not help for short-term energy use.** "Same as last year" stays best at 1–2 years. Today's energy use moves with prices, crises and weather (2020, 2022). Under UNIRA, energy is supplied and metered by plan (rule 23), so this market noise is not a need.
- **The validation choice is not always the best on test.** For nurses at 5 years, naive was chosen but the ensemble did better. That is the honest cost of choosing without looking at the future. The published yearly re-test of Article 3b(2) corrects such choices over time.
- **Reserves.** To cover the true need in 95% of cases two years ahead, about 1.4% above forecast is enough for population and 4% for food. For health workers it is 17–20%, but staff are trained over years, so that error is absorbed by the training plan, not by stocks.

## 3. Fairness: forecasts are least accurate where needs are greatest

Median error 1 year ahead, by World Bank income group:

| | low income | lower-middle | upper-middle | high income |
|---|---|---|---|---|
| population | 0.1% | 0.1% | 0.1% | 0.1% |
| food per person | 1.5% | 1.1% | 1.0% | 0.8% |
| doctors per 10,000 | **6.9%** | 2.5% | 1.9% | 1.1% |
| nurses per 10,000 | **5.8%** (bias −6.1%) | 5.0% | 2.1% | 1.6% |

- Population forecasts are equally good everywhere. Health-worker forecasts are 3–6× worse in low-income regions, because their statistics are sparse and irregular.
- For nurses in low-income regions, the forecast is also biased downwards by 6%. A planner trusting it would under-supply the poorest regions.
- **So fairness needs better statistics in the poorest regions before, or alongside, AI planning.** Article 3b(4) requires this and requires per-region accuracy tests.

## 4. Thirty years: information is not the bottleneck, integrity is

The 30-year world transition (v67) was rerun with the allocator seeing each region's levels and population through different information systems. There were 30 random seeds per case, and median results are shown as a share of what perfect information achieves (`outputs/information.json`):

| information system | energy gap closed, yr 15 | health, yr 15 | housing, yr 30 |
|---|---|---|---|
| perfect information | 100% | 100% | 100% |
| statistics only (1-year delay, 5% noise), no misreporting or leakage | 100% | 100% | 100% |
| AI nowcast with measured errors, no misreporting or leakage | 98.9% | 99.9% | 99.2% |
| misreporting (25% of regions) and leakage (8%) only, perfect data | 87.5% | 88.1% | 80.9% |
| statistics today, with misreporting and leakage (= v69 strong safeguards) | 87.5% | 88.1% | 80.9% |
| AI nowcast, with misreporting and leakage | 86.7% | 88.0% | 80.3% |
| AI nowcast, metered energy and better audit (0.8), with misreporting and leakage | 87.5% | 88.0% | 80.3% |

**Leakage is what matters.** With AI information and the same misreporting:

| leakage | 0% | 2% | 4% | 8% | 15% |
|---|---|---|---|---|---|
| energy gap closed, yr 15 | 59.2% | 57.4% | 55.6% | 51.9% | 45.5% |
| housing gap closed, yr 30 | 49.6% | 47.2% | 44.8% | 40.1% | 31.8% |

- Information errors, from statistics or from AI forecasts, cost at most about 1%. Needs-first water-filling is robust to small, unbiased errors.
- **All of the loss comes from diversion.** Each point of leakage costs about one point of energy progress and 1.2 points of housing progress.
- **The AI's main value for One Earth is integrity, not prediction:**
  - cross-checking deliveries against needs and metered use;
  - flagging anomalies for audit (Articles 33–37);
  - sizing reserves from measured errors.
  If such checks halve leakage from 8% to 4%, the energy gap closed by year 15 rises from 51.9% to 55.6% (assuming they can). That is far more than any forecasting improvement.

## 5. Verdict on rule 32

- **Supported, with conditions.** Planning production from measured needs is feasible: the main driver of needs, population, is predictable to about 0.1% a year ahead and about 1% five years ahead. Machine learning adds real but modest accuracy over simple rules for population, food and health workers. It must be held to beat those rules, and in short-term energy it does not.
- AI does **not** replace honest data and audits. Its largest benefit is detecting misreporting and leakage. That part is an assumption here (audit 0.5 → 0.8 had little effect alone; leakage is the lever).
- **Fairness first:** the weakest data are in the poorest regions, so the AI is least accurate there. Investing in their statistics is the precondition.
- Constitution **Article 3b** sets these conditions:
  - AI advises and people decide;
  - models are open and tested against simple rules every year;
  - accuracy and fairness are tested per region;
  - AI has no role in rights, sanctions or force;
  - a manual fallback always exists;
  - reserves are sized from measured errors.

## 6. Limitations

- Backtests use the history of today's economies. Under UNIRA, needs follow normative targets (40 GJ, 2,100–2,470 kcal, 131 health workers per 10,000) and population, so they should be easier to forecast than market demand. That is not proven.
- No time series exists for floor area, so the housing level error is assumed equal to energy's.
- Forecasting production *location* (which region produces what) is not modelled here. Allocation is needs-first water-filling (v67), and choosing locations by capacity, transport and climate is future work.
- The models are deliberately simple (linear and nearest-neighbour). Larger models might gain a little on population and food, but the 30-year test shows that information quality is not the bottleneck.
- Misreporting and leakage parameters come from v69 (observed programmes). The effect of AI anomaly detection on leakage is not measured. It is a hypothesis to test in pilots.
