# UNIRA v79 — Who gets the flat by the sea? Allocating desirable homes at fixed prices

Files: `evidence.csv` (39 rows, 34 verified in fetched text), `config.json`, `simulate.py`,
`tests/test_housing_alloc.py` (11 tests), `outputs/results.json`, `outputs/results.csv`.
Run `python3 simulate.py` (about 27 s, deterministic, standard library only) and
`python3 -m unittest discover -s tests` (about 5 s).

## 1. Question

Article 18 fixes home prices (100,000–500,000 U), so price can no longer ration the
places everybody wants: the city centre and the seaside. **What rule should decide who gets a
desirable home, if income must not matter?** The author's design to test:

1. published priority points for household size and children, distance to work, disability or care duties, time already waiting, and local roots;
2. a public lottery among applicants with similar points, and no way to buy in;
3. more building where demand is high, with jobs and amenities spread out;
4. a must-live-in rule in high-demand spots, so no home is held empty or for speculation.

## 2. Evidence (see `evidence.csv`)

| Topic | What the sources show | Verified |
|---|---|---|
| Singapore HDB | 77.2% of resident households live in HDB dwellings (SingStat 2025). Desirable projects are oversubscribed: in Feb 2025, 3-room-and-bigger flats drew 8,402 applicants for 3,621 units (2.3×), and 4-room flats at central Tanjong Rhu drew 3.5×. **Quotas, not absolute priority**: families with children get up to 40% of BTO supply, people living within 4 km of parents or children up to 30%, third-child families up to 10%; the rest is balloted. **Plus and Prime (high-demand) flats** have a 10-year minimum occupation period (5 years for Standard), no rental of the whole flat, and subsidy recovery on resale. | yes |
| Vienna | 220,000 municipal flats with about 500,000 tenants; around 50% of residents live in subsidised housing (the city's figure; press reports say over 60%). Applicants need 2–3 years of main residence. Income ceilings are high (€59,320 for one person), and long-standing residents get a bonus of 3 months per 5 years of residence. From 2026, a single Wohn-Ticket with **bonus points** replaces fixed need categories. | yes |
| Stockholm queue | Average time in the queue for those who get a flat is 9 years (2023), with most housed between 4.8 and 12.7 years. A housing-company survey puts Stockholm county at 28 years (different definition). Central Stockholm was about 18 years in 2022 (search snippet only). | yes / partly |
| Netherlands | In the Amsterdam region, the average registration time of people housed in 2024 was 10.7 years, and only 4.4% of active seekers found a home that year. The region uses points: waiting points, search points and situation points. Amsterdam allocated **3.3%** of lets by lottery (276 of 8,473). Nationally the wait averages over 7 years, with 27% of lets going to urgent cases. | yes |
| Lottery vs queue (theory) | Arnosti & Shi (2020): a lottery per item and a waitlist that removes priority after a refusal give the same results; a single **common lottery** improves match quality; and when many low-need people apply, matching and targeting cannot both be maximised. Thakral (2019): when supply arrives at random, no mechanism can guarantee ex-post efficiency or fairness. Waldinger (2021): removing applicant choice improves targeting but cuts tenant welfare by more than 30%. | yes |
| Empty homes | Vancouver's Empty Homes Tax: vacant properties fell 36% (2017→2021); vacancy among taxed homes fell to 0.71%; 49% of homes vacant in 2020 were occupied in 2021. France's TLV cut vacancy rates by 13%, mostly long-term vacancy, and most units became main residences (Segú 2020). In Paris, about 19% of dwellings are not a main residence (Apur 2020). Vancouver's −67% by 2024 and the Paris 8.5% vacancy rate were seen in search snippets only. | yes / partly |

**What the evidence says.** No real system ranks applicants by income, but none fully avoids long queues
either. Where only waiting time counts (Stockholm, the Amsterdam region), waits run to 9–11 years,
and young or newly arrived households are shut out. Singapore and Vienna mix need criteria with
ballots or bonus points. Singapore already ties its high-demand locations to a longer occupancy
duty. Occupancy rules or taxes clearly reduce vacancy, though how much varies by place.

## 3. Method

The model is a stylised city with six zones (coordinates in km). Two zones are desirable and rationed:
the centre (3,000 homes) and the seaside (1,800). The four other zones always have spare
fixed-price homes, so each applicant has a fallback home. Each year 1,000 households look at the
city; about 600 prefer a desirable zone to their fallback and apply. Their preference is zone appeal,
plus a personal taste, minus commute cost. On top of these come speculators: owners of one home
seeking a desirable second home that they mostly leave empty, which Article 18.2 allows. They make
up 8% of applicants and come from income deciles 7–10. Each year, 5% of occupied desirable homes
turn over, about 2.5 applicants compete for each vacancy, and 10% of those waiting give up. The run
covers 30 years, and outcomes are measured for applicants arriving in years 5–24.

Households have a size, a number of children, disability (more common in low deciles), care duties,
local roots, a workplace zone, and an income decile. **The income decile never enters UNIRA
priorities.** A test shuffles incomes and confirms that allocations stay identical. Vacancies are
matched by applicant-proposing deferred acceptance, which is stable. Applicants rank the zones they
prefer to their fallback; zones rank applicants using one of six methods:

| Method | Priority |
|---|---|
| queue | registration date |
| points | points (children 3 each up to 3, extra adult 1, disability 6, care 4, roots 2, 1 per year waited up to 10, +4 if work is in the zone or +2 if within 5 km); ties by registration date |
| points_lottery | points grouped in bands of 3, with one common public lottery each year inside a band (following Arnosti & Shi) |
| points_lottery_open | as points_lottery for 70% of vacancies; the other 30% go to an open lottery among all applicants (HDB-style quota) |
| lottery | one common public lottery each year |
| market | highest bid: income × noise, with speculators bidding 1.5× (benchmark only) |

Sensitivity runs cover the following:
- **Gaming:** 10% or 20% of applicants falsely claim a care duty, and better-off households cheat more. A successful claim is audited with probability 0, 25% or 75%; a caught cheater loses the offer and is barred for 5 years.
- **Must-live-in rule off vs on:** 10% of homes start empty, inside the Paris 8.5–19% range. Under the rule, 80% of speculators are deterred, and an empty home is detected and returned with 50% probability each year, anchored on Vancouver's 49%.
- **Building more:** +10% or +25% desirable homes over 30 years.
- **Spreading jobs:** 30% of centre jobs move out.
- **The full UNIRA package:** rule, +25% homes, spread jobs, and 10% gaming with a 25% audit.

Main results use 5 seeds and sensitivity runs use 3; values below are means (standard deviations
across seeds are in `results.json`). Every parameter that does not come from the evidence is marked
`SYNTHETIC_ASSUMPTION` in `config.json`.

## 4. Results

### 4.1 Baseline (must-live-in rule on, honest reporting)

| Method | Mean wait if housed (y) | P90 wait (y) | Housed ≤5 y: all | **Housed ≤5 y: high-need** | Housed ≤5 y: low-need | Commute at 5 y (km) | Commute of winners (km) | **D10/D1 allocation** | Speculators' share of allocations |
|---|---|---|---|---|---|---|---|---|---|
| queue | 9.7 | 11.0 | 0.0% | 0.0% | 0.0% | 3.94 | 4.46 | 1.03 | 1.8% |
| points | 5.2 | 9.8 | 14.8% | 27.2% | 0.0% | 3.46 | 2.60 | 0.86 | 0.4% |
| **points_lottery** | 5.2 | 10.0 | 15.3% | **27.9%** | 0.1% | **3.45** | 2.64 | 0.86 | 0.4% |
| points_lottery_open | 4.8 | 9.2 | 16.7% | 24.8% | 7.0% | 3.61 | 3.17 | 0.88 | 0.8% |
| lottery | 4.2 | 10.0 | 20.0% | 19.9% | 20.0% | 4.02 | 4.40 | 1.00 | 1.8% |
| market | 0.9* | 3.0* | 28.0% | 27.1% | 29.3% | 4.07 | 4.43 | **≥99** (D1 gets 0%) | 5.5% |

\* Under the market, only rich applicants are ever housed, so their waits are short. Deciles 1–5
receive 0.02% of desirable homes, while deciles 8–10 receive about 90%.

Some observations:
- **The queue reproduces real queues.** It gives a 9.7-year mean wait, close to Stockholm's 9 years and the Amsterdam region's 10.7 years, although the model was not fitted to those numbers. Under the queue nobody is housed within 5 years, whatever their need.
- **Points roughly halve the wait and target need.** High-need households (with children, a disability or a care duty) are 28% likely to be housed within 5 years. Winners also live about 1.8 km closer to work. The allocation is mildly progressive (D10/D1 = 0.86), but only because need is slightly more common in low deciles. Income itself plays no role.
- **Strict points and points + lottery bands are indistinguishable** on every outcome, with differences within 1–2 standard deviations. The lottery's value is therefore procedural. It breaks ties among people with similar points openly instead of by registration date or by an official's discretion, and it makes small point disputes less decisive. It does not change who gets housed.
- **The pure lottery is perfectly income-neutral** (D10/D1 = 1.00) but ignores need: high-need and low-need households are housed at the same rate, and commutes are 0.6 km longer.
- **Both need-based methods almost completely exclude low-need applicants** (0–0.1% housed within 5 years). The open-lottery share brings this to 7%, at a cost of 3 points of high-need access (27.9% → 24.8%). This is the matching versus targeting trade-off predicted by Arnosti & Shi.

### 4.2 Must-live-in rule (3 seeds)

| Method | Empty share of desirable stock, year 30 (no rule → rule) | High-need housed ≤5 y (no rule → rule) | Speculators' share of allocations (no rule → rule) |
|---|---|---|---|
| queue | 11.3% → 0.2% | 0% → 0% | 8.1% → 1.8% |
| points_lottery | 6.3% → 0.1% | 24.7% → 27.9% | 1.7% → 0.4% |
| lottery | 11.6% → 0.2% | 17.0% → 19.9% | 8.0% → 1.8% |
| market | **32.3%** → 0.5% | 16.4% → 27.1% | 30.8% → 5.5% |

Without the rule, the two-homes allowance lets 6–12% of the best homes sit empty under the UNIRA
methods, and nearly a third under bidding. The rule brings this below 0.5%, in line with
Vancouver's 0.5–0.7%, and adds about 3 points of high-need access.

### 4.3 Gaming and audits (points_lottery; points shows the same pattern)

| False claimants | Audit probability | Share of allocations to false claimants | High-need housed ≤5 y | D10 − D1 allocation ratio |
|---|---|---|---|---|
| 0% | — | 0% | 27.9% | −0.15 |
| 10% | 0% | 14.9% | 28.3% | −0.10 |
| 10% | 25% | 11.3% | 27.8% | −0.10 |
| 10% | 75% | 3.9% | 27.9% | −0.14 |
| 20% | 0% | **28.9%** | 28.2% | **+0.01** |
| 20% | 25% | 22.2% | 27.9% | −0.03 |
| 20% | 75% | 8.0% | 27.6% | −0.14 |

Without audits, a fifth of applicants lying about care duties capture nearly 29% of the homes.
Because better-off households cheat more in this model, the progressive tilt disappears; points
then stop being fair even though income never enters them. Most cheaters are already high-need
families topping up their points, which is why aggregate high-need access hardly moves.
Checking 75% of successful claims before the keys are handed over restores the honest outcome
almost fully. A 25% check rate is not enough.

### 4.4 Building more, spreading jobs, and the full package (3 seeds)

| Scenario | queue: mean wait (y) | points_lottery: high-need ≤5 y | points_lottery: commute at 5 y (km) | lottery: all ≤5 y | market: D10/D1 |
|---|---|---|---|---|---|
| baseline | 9.7 | 27.9% | 3.45 | 20.0% | ≥99 |
| +10% homes | 8.8 | 32.7% | 3.38 | 22.8% | ≥99 |
| +25% homes | 7.7 | 39.3% | 3.31 | 27.3% | ≥99 |
| jobs spread (30% of centre jobs out) | 9.3 | 30.4% | **2.96** | 21.2% | ≥99 |
| package (+25%, jobs spread, rule, 10% gaming with 25% audit) | 7.4 | **42.1%** | 2.93 | 29.0% | ≥99 |

Supply is the strongest single lever: +25% desirable homes raises high-need access by 11 points.
Spreading jobs mainly cuts commuting (by 0.5 km) and modestly reduces demand. No allocation rule
alone makes the queue short. Under the full package the queue still averages 7.4 years.

## 5. Verdict

Judged by UNIRA's fairness-first rule (allocation by need, no income gradient, no buying in):

1. **Market: rejected.** It has a total income gradient: deciles 1–5 get essentially nothing. It also invites empty speculative holdings, reaching 32% of desirable stock without a rule.
2. **Pure queue: rejected.** It is income-neutral, but it gives a 10-year wait for everyone, never reaches high-need households within 5 years, and rewards registering early rather than need. Stockholm and Amsterdam show the same pattern.
3. **Pure lottery: fair but blind.** It is perfectly income-neutral and fast on average, but it ignores need and commuting.
4. **Points + public lottery within bands: recommended core.** It reaches the most high-need households, gives the shortest commutes, and has no income gradient. Its fairness depends on two things the simulation shows are essential:
   - **audits** of a high share of successful claims (≥75% in the model); without them, cheating recreates an income gradient;
   - the **must-live-in rule**.

   The lottery inside bands does not change outcomes compared with strict points. It is kept because it makes ties public and random instead of discretionary.
5. **Optional open-lottery share.** The author's design (points + lottery) shuts low-need households out almost entirely when demand is 2.5× supply. If UNIRA also values "everyone has some chance", reserve a small share of vacancies for an open lottery. A 30% share gives low-need households a 7% chance within 5 years and costs about 3 points of high-need access. This is a value choice, not a technical one, so the draft below leaves it as a bounded regional option.
6. **Supply and jobs matter more than the rule.** The allocation rule decides who waits; only building more and spreading jobs reduce how long everyone waits.

## 6. Draft amendment to Article 18 (Homes)

Add after Article 18.6:

> **7. Allocation where demand exceeds supply.** When more households apply for homes in a zone than there are homes free, the homes are allocated by published priority points. Points are given for:
> - household size and children;
> - nearness of the home to the household's place of work or study;
> - disability and care duties;
> - time already waiting;
> - local roots.
>
> Income, wealth and any offer to pay more are never taken into account.
>
> **8. Public lottery.** Applicants whose points fall in the same published band are ranked by a public lottery, drawn once a year for all zones together. A region may reserve up to three-tenths of these homes for an open lottery among all applicants. No one may buy, sell or transfer a place in the ranking.
>
> **9. Must live in.** In a zone declared high-demand, a home must be the main residence of the household that holds it. It may not be left empty, used as a second home, or let out whole. A home left empty for more than six months without a recognised reason (care, study, work posting, repair) returns to the regional pool. The second home allowed by Article 18.2 may not be in a high-demand zone.
>
> **10. Checks.** Points claims are checked before a home is handed over. A household that made a false claim loses the offer and may not apply for five years.
>
> **11. Building to need.** Each region publishes waiting times and points thresholds for every zone each year. Where the average wait in a zone exceeds five years, the region builds more homes there and moves jobs and services towards other zones until waits fall.

*Evidence: in a 30-year simulation of a city with 2.5 applicants per desirable home (`v79/housing`):*
- *points with a lottery in bands housed 28% of high-need households within 5 years, against 0% for a queue and 20% for a pure lottery, with no income gradient;*
- *bidding gave deciles 1–5 almost nothing;*
- *the must-live-in rule cut empty desirable homes from 6–32% to under 0.5%;*
- *+25% homes raised high-need access to 39%.*

*Precedents: Singapore requires 10 years' occupation of Prime and Plus flats; Vienna is introducing points; Vancouver's empty-homes tax cut vacancy 36% (2017–2021).*

## 7. Limitations

- **Stylised city.** Zone sizes, demand (2.5 applicants per vacancy), the 5% turnover rate, the 10% dropout rate, tastes, point weights and band width are all `SYNTHETIC_ASSUMPTION`. The queue result (9.7 years) is close to Stockholm and Amsterdam, but this is a plausibility check, not a calibration.
- **Fixed behaviour.** Households do not change their behaviour in response to the rule, for example by registering earlier, refusing offers strategically, or moving jobs to gain commute points. Speculator deterrence (80%) and detection (50% per year) are assumed; detection is anchored on a single Vancouver number from a tax, not a rule.
- **Gaming is limited to one false claim** (care duty), with an assumed income gradient. Other forms are not modelled: fake addresses for roots or commute points, splitting households, or corruption of the auditors.
- **Truncated waits.** Waits are measured only for housed households and are truncated by the 30-year window (P90 ≤ 11 years). The market's short "wait" reflects who is housed, not a better process.
- **Narrow welfare measure.** Only who gets housed, wait and commute are measured. Waldinger (2021) shows that applicant choice has large welfare value. Here applicants rank zones but not individual homes, and refusals are not modelled.
- **Synthetic income, need and income tilt.** The income gradient results depend on the assumed slight concentration of disability in low deciles. With need uncorrelated with income, points would give a flat gradient, as the lottery does.
- **Evidence gaps.** Some figures were seen only in search snippets and are marked `verified_in_fetched_text = no`: Vancouver −67% (2017–2024), Paris 8.5% vacancy, central Stockholm 18 years, and the Utrecht lottery-vs-offer waits. The City of Vancouver and HDB annual-report PDFs could not be fetched or read here. Thakral's paper "The Public-Housing Allocation Problem" was not located by that title; his AEA P&P 2019 paper is cited instead.
