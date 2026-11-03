# UNIRA V8.2 — point 2: who does the hard and unwanted jobs?

**The problem:** without wage competition, what brings people into night, weekend, heavy or unpleasant jobs? Article 14 rewarded knowledge and complexity only. In France, the jobs hardest to fill in 2025 were:

| sector | vacancy rate (Eurostat jvs_a_rate_r2, 2025) |
|---|---|
| hotels and restaurants | 4.5% |
| personal services | 3.2% |
| arts and leisure | 3.0% |
| health and social care | 2.9% |
| construction | 2.8% |

In the EU as a whole: support services such as cleaning and security (3.3%), construction (2.8%), hotels and restaurants (2.7%).

**Model:** `simulate.py`.
- 20,000 people choose jobs, weighing pay, hours, how hard the job is, and their own vocation.
- Sector sizes are France's 2022 hours by sector (v63).
- Everyone able to work works (Article 7), so every job is filled. The measure is the share of people placed **unwillingly**, outside their top three choices: low motivation, turnover and poorer care follow.
- Hardness and base multipliers by sector are synthetic.
- How much people dislike hard work is unknown, so it is tested at three levels; 3 seeds.

Share of workers in hard jobs who are there unwillingly (central dislike):

| rule | hard jobs | other jobs | average multiplier | hours covered |
|---|---|---|---|---|
| knowledge and complexity only | **87%** | 48% | 1.60 | 100% |
| + hardship step (up to +0.5, within 5×) | 69% | 38% | 1.85 | 100% |
| + shorter hours (hard jobs: 25 h paid as 30) | 80% | 44% | 1.60 | 92% |
| + both | 58% | 34% | 1.85 | 92% |
| **+ both + jobs made 30% less hard** | **46%** | 29% | 1.85 | 92% |

Low and high dislike give the same ranking (hard jobs, from knowledge-only to all three levers: low 76% → 37%, high 94% → 77% with both, without better conditions).

## Findings

1. **Paying only for knowledge leaves hard jobs to the unwilling.** Almost nine in ten people in hard jobs would rather be elsewhere. That is the Soviet experience of forced assignment, and today's shortages in care and hospitality.
2. **Pay for hardship is the strongest single lever.** It stays within the 5× ceiling.
3. **Shorter hours help less on their own,** but they reward the job directly and protect health. They also cost hours: hard sectors need about 9% more people. UNIRA's universal employment and training provide them.
4. **Making the work itself less hard matters most.** With all three levers, hard jobs become about as wanted as ordinary jobs were before. Better staffing ratios, ergonomics, machines for heavy tasks and no split shifts belong in the design, not only higher pay.
5. **Cost:** the average multiplier rises from 1.60 to 1.85. Average pay may rise only with productivity (Article 14.4), so the hardship steps are financed within the scale, and the base salary is unchanged.
6. **Plausibility is weak:** the sectors the model finds hardest to fill match France's measured vacancy ranking only loosely (rank correlation 0.31), because hardness per sector is a synthetic score. Real calibration needs occupational survey data, for example on night work and physical strain.

## Rule supported (proposed Article 14a)

1. **Hardship steps:** a published score for night, weekend, physical, dangerous or unpleasant work adds up to half a multiplier step, within 5×.
2. **Shorter hours** for the hardest jobs, of up to 5 hours a week at the same pay.
3. **A duty to improve:** each hard job has a yearly plan to reduce hardness, through staffing, equipment and organisation, published and audited.
4. **Training paid in full** for anyone moving into a shortage job.
5. If a sector stays short for two years, the hardship step and conditions are reviewed automatically.

## Limitations

- Synthetic preferences and hardness scores.
- No model of turnover over time.
- Rotation and short civic service in care were not tested; they could spread the hardest tasks.
