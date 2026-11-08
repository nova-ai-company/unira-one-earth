# UNIRA — register of behavioural assumptions (point 8)

The physical results of UNIRA rest on data. Several results also rest on **how people will behave** in an economy that has never existed. This register lists each assumption, the value used, its evidence class, and how the pilot (v80) or later evidence will test it. Any assumption refuted by the pilot must be replaced, and the affected results rerun.

| # | Assumption | Value used | Where | Evidence class | How it will be tested |
|---|---|---|---|---|---|
| 1 | People take a guaranteed job when offered | take-up rates from Eurostat flows (e.g. 61% of unemployed within a year) | v63/flows | measured (today's flows) | pilot: share of unemployed in work within a year (≥61% success, ≤41% failure) |
| 2 | Shorter hours raise output per hour | θ = 0.2–0.4 of lost hours recovered | v62, v63 | literature range | pilot: output per hour in volunteer employers (θ ≥ 0.20 success, < 0.10 failure) |
| 3 | Saving behaviour | saving rates spread evenly from 0 to 50% | v64, v79/money | synthetic | pilot local voucher with a holding cap; household survey |
| 4 | Effort does not fall when the money cap is reached | no effort response | v64, v79 | synthetic (lottery-winner evidence suggests small effects) | pilot: hours and productivity of people near the voucher cap |
| 5 | Security reduces over-consumption of satiable goods, but not energy, travel or data | rebound for energy, travel, data | v71 | literature | metered use in the pilot; energy-allowance trials |
| 6 | Misreporting and leakage | 25% of regions misreport; 8% leakage with safeguards | v69, v78 | observed programmes | pilot: open register, unaccounted funds (≤8% success, >15% failure) |
| 7 | How much people dislike hard work, and vocation | three levels | v82/jobs | synthetic | pilot: vacancies and job choices in care and hospitality with hardship steps |
| 8 | Orders and waiting lists reveal demand honestly | orders kept 3 months, no fake orders | v82/production | synthetic | pilot: order platform data; share of lapsed and cancelled orders |
| 9 | Demand response to market prices (comparison only) | elasticity 1 | v82/production | synthetic | literature review |
| 10 | Housing applicants' preferences and claim honesty | synthetic preferences; false claims tested at 20% | v79/housing | synthetic | pilot: points + lottery allocation of social homes |
| 11 | Catch-up growth of poorer regions | +2%, +4%, +6% a year | v82/worldmoney | scenarios | first member regions; published yearly progress (T-8) |
| 12 | Innovation without profit | indicators of Article 3d | v79/innovation | literature, partly | pilot: proposals, projects started, user satisfaction |

## Evidence that already exists: trials and experiments in related settings (added 8 November 2026)

None of these proves UNIRA. Each moves an assumption from "untested" to "observed in a related setting, with this effect". Verified = read in the source text on 8 November 2026; reported = seen in summaries only. Sources with their rows are in `v80/pilot/evidence.csv` (topic `existing_trials`).

| Assumption | Trial or experiment | What was observed | Status |
|---|---|---|---|
| 2 (shorter hours, output per hour) | Iceland 2015–19: two public-sector trials, 35–36 h with no pay cut, 2,500 workers | productivity and service provision the same or improved in most workplaces; revenue-neutral for the city and the state; wellbeing up; since then 86% of the workforce works shorter hours or has the right to | verified (Autonomy and Alda 2021) |
| 2, 7 | UK four-day-week pilot, June–December 2022: 61 companies, about 2,900 workers | 56 of 61 companies continued, 18 made it permanent; revenue +1.4% over the trial; staff leaving −57%; 39% less stressed, 71% less burnout; no productivity figure published on the results page | verified (Autonomy 2023) |
| 1, 4 (take-up of work, effort under guaranteed income) | Finland 2017–18: 2,000 unemployed, €560 a month unconditional | employment effect small: +6 days of work in Nov 2017–Oct 2018 (78 days on average), none in year one; confounded by the 2018 activation model; recipients more satisfied, less mental strain, depression and loneliness | verified (VATT, 6 May 2020) |
| 4, 12 | Kenya, GiveDirectly long-term UBI: villages of about 118 eligible adults, 12-year commitment, with short-term and lump-sum arms | labour supply did not change overall but shifted from wage work to self-employment; more enterprises and higher net revenues, concentrated outside agriculture; lump sums had similar or larger effects, short-term transfers smaller | verified (Banerjee, Faye, Krueger, Niehaus and Suri, September 2023, abstract) |
| 1, 4 | Stockton, California 2019–21: 125 residents, $500 a month for 24 months | recipients found full-time employment, income volatility fell, less depression and anxiety (the programme's own summary; the published percentages were not readable) | reported (SEED) |
| 4, health | Dauphin, Manitoba 1974–79 (Mincome) | hospitalisations about 8.5% lower; more high-school completion (figures from secondary sources; the paper could not be read) | reported (Forget 2011) |
| 6 (honest needs, leakage), institutions | Participatory budgeting, Brazil's largest cities over 20 years | strongly associated with higher health-care spending, more civil-society organisations and lower infant mortality, stronger the longer it lasts | verified (Touchton and Wampler 2014, abstract) |
| institutions (lot-chosen assemblies) | Irish Citizens' Assembly 2016–18: 99 members selected at random to be representative | worked through five constitutional topics in two years for about €1.5 million; recommendations submitted to parliament (the 2018 referendum that followed is not on the page read) | verified (citizensassembly.ie) |
| 4 (effort under capped pay) | Mondragon, Basque Country: 81 cooperatives, about 70,000 people, "wage solidarity" as a founding principle | a large industrial group has run for decades on capped internal pay ratios (the ratio itself, often cited as 1:6 to 1:9, is not on the pages read) | verified for scale and principle; ratio reported |

What they say together: shorter weeks at the same pay have held output in two national trials; unconditional income has not reduced work in the three experiments with employment data, and it shifted work toward self-employment in Kenya; lot-chosen assemblies and participatory budgets have produced usable decisions at national and city scale. What they do not say: none ran a fixed-price economy, a money cap or needs-based allocation of goods, which only the pilot of `v80/pilot/` would test.

**Rule:** every year, the Scientific Council publishes this register with the newest evidence (Article 3a). Results that depend on a refuted assumption are marked until they are rerun.
