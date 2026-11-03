# Hours-productivity offset (θ): evidence review for V6.2

Status: bounded evidence review, prepared 2026-11-03. Companion table: `hours_productivity_evidence.csv`.
Scope: (a) the elasticity of hourly productivity/output with respect to cuts in working hours; (b) the employment effects of mandated hours reductions; (c) a proposed parameter range for θ.

**Definition used.** θ is the share of lost hours per worker that higher output per hour makes up, with employment held fixed:
`Δln(Y/H) = −θ · Δln(h)`, so output per worker changes by `(1−θ)·Δln(h)`. θ=0 means output is proportional to hours; θ=1 means output is unchanged.
Where a source reports an output-hours elasticity ε, θ ≈ 1−ε. All θ values below that I derived myself are marked **derived**. The sources do not report them.

**Verification convention.** "Verified" means I read the number in text fetched during this review: the full PDF text, or the abstract on the publisher or repository page. "UNVERIFIED" means I give the citation only, or the figure comes from a search-engine summary or secondary press that I did not open. DOIs I did not see on a fetched page are marked "(DOI unverified)".

---

## 1. What the V6.2 scenario actually asks

Going from about 38.9 h to 30 h is a cut of Δln h ≈ −0.26 (−23%). This is 2–6 times larger than any mandated reduction with a credible evaluation. The largest evaluated cases are France 39→35 (−10.3% nominal, about −6% effective economy-wide), Portugal 44→40 (−6% realised at firm level), Korea 44→40 and Japan 48→40 (phased).

The scenario also ends at 30 h. That is below the range where the micro-evidence finds hourly productivity responding to hours. Evidence near and below 35 h points to near-proportional output (θ close to 0).

Both facts mean the evaluated reforms give an **upper bound** for the offset on the 35→30 segment.

## 2. Evidence on (a): output and hourly productivity

### 2.1 Direct production-function and fatigue evidence (θ low at moderate hours)

**Pencavel, J. (2014/2015). *The Productivity of Working Hours*.** IZA DP 8129, published in *Economic Journal* 125 (2015), 2052–2076. https://docs.iza.org/dp8129.pdf (DOI unverified).
- **Data:** First World War British munition workers, mostly women, from Health of Munition Workers Committee records.
- **Finding (verified in text):** "below 49 weekly hours, variations in output are proportional to variations in hours; for those observations corresponding to 49 or more hours, output rises with hours at a decreasing rate and a maximum of output occurs at about 63 hours."
- In a log-linear fit for the shorter-hours regime, "the estimate of δ1 is, indeed, unity."
- Removing Sunday work raised output slightly: "merely 1.4 percent of the 70 hour output."
- **Implication:** derived θ ≈ 0 for weekly hours below about 48–49.
- **Quality:** Historical observational data with group fixed effects. Hours vary within regimes, not through a policy experiment. The work is manual and piece-rate-like, so external validity to a modern service economy is limited. However, the result is the main reason to expect a *small* offset when cutting from 39 to 30 h.

**Collewet, M. & Sauermann, J. (2017). Working hours and productivity.** *Labour Economics* 47, 96–106, doi:10.1016/j.labeco.2017.03.006. IZA DP 10722: https://docs.iza.org/dp10722.pdf
- **Design:** Call-centre agents, mostly part-time with a modal week of about 24 h. Uses within-worker variation in hours from central scheduling, with individual and time fixed effects.
- **Finding (verified in text):** "an increase in working hours by 1 percent leads to an increase in output by only 0.9 percent, measured as the number of calls answered."
- **Implication:** derived θ ≈ 0.1 in the 20–35 h range.
- **Quality:** Strong internal identification (scheduling is plausibly exogenous). It covers a single firm and a single task, and captures short-run fatigue only, not reorganisation. It is the most directly relevant estimate for the 30–39 h range, and it gives a small θ.

### 2.2 Firm and sector evidence from mandated reforms (θ moderate, noisy, with confounds)

**DARES ex post evaluation: Gubian, A., Jugnot, S., Lerais, F. & Passeron, V. (2004). Les effets de la RTT sur l'emploi : des simulations ex ante aux évaluations ex post.** *Économie et Statistique* 376-377, 25–54. https://www.insee.fr/fr/statistiques/fichier/1376464/es376377b.pdf (verified in text)
- **Aided firms (Aubry I and Robien):** "la baisse d'un peu plus de 10 % de la durée effective du travail s'est accompagnée de créations nettes d'emplois de l'ordre de 6 à 7 %. Les gains de productivité horaire induits seraient donc d'environ 4 à 5 %". This is above the ex ante assumption of one third of the cut (3.4%).
- **Aubry II only:** about 7% effective cut, 2–3% employment effect, and comparable hourly productivity gains of 4–5%.
- **Summary statement:** "les gains de productivité apparente du travail ont été de l'ordre de 40 à 50 % de la baisse de la durée du travail, au lieu d'un tiers dans les travaux ex ante."
- **Economy-wide effective hours cut:** a little under 5% on DARES's synthetic indicator, and a little over 6% in the national accounts, against 10.3% nominal. Some firms met the 35 h target by excluding breaks and holidays from the count.
- **Employment:** about 350,000 jobs over 1998–2002.
- **Implication:** derived θ ≈ 0.4–0.5 for a ~10% cut, and possibly higher for Aubry II firms relative to their smaller real cut.
- **Quality:** These gains are inferred *under an assumption of output neutrality* ("Sous l'hypothèse de neutralité de la production"). Output was not tracked directly. Firms chose their scheme and received large payroll-tax subsidies. The authors are an interested agency. Treat θ≈0.4–0.5 as an upper-end, firm-selected estimate for the first ~10% of a cut from 39 h.

**Crépon, B., Leclair, M. & Roux, S. (2004). RTT, productivité et emploi : nouvelles estimations sur données d'entreprises.** *Économie et Statistique* 376-377, 55–89. https://www.insee.fr/fr/statistiques/fichier/1376466/es376377c.pdf (verified in text)
- **Design:** Firm-level comparison, 1997–2000, controlling for observables.
- **Aided Aubry I firms vs firms still at 39 h:** total factor productivity measured with headcount (not hours) fell "d'environ 3,7 %", whereas hours "aurait dû diminuer … de 4 heures, soit 10,2 %". Employment rose 9.9%.
- **Table 2:** TFP −3.68 (s.e. 0.31); VA/L −4.89 (0.32); VA +5.02 (0.39); K +4.20.
- **Implication:** derived θ ≈ 1−3.7/10.2 ≈ 0.64 on TFP per head, or ≈ 0.52 on value added per head.
- **Quality:** Selection on observables only. Treated firms were already growing faster before the reform, and the authors acknowledge pre-trends. The paper itself says the hours measure is inadequate and that production-function estimates of hours effects are "très difficile". These are volunteer, subsidised firms. Upper-end estimate.

**Asai, K., Lopes, M.C. & Tondini, A. (2024). Firm-Level Effects of Reductions in Working Hours.** Working paper, January 2024. https://www.parisschoolofeconomics.eu/app/uploads/2024/11/asai-kentaro-firm-level-effects-of-reductions-in-working-hours.pdf (verified in text)
- **Design:** Portugal's 1996 law (44→40 h). Difference-in-differences using matched employer-employee data.
- **Hours:** treated firms cut hours by "around 2.5 hours, corresponding to a 6% decrease".
- **Scale effects:** "a 6% increase in the hourly wage rate led to roughly a 2% decrease in employment, 9% decline in total hours, and a 4% reduction in sales" (mainly through fewer hires).
- **Productivity:** "This increase in hourly labor productivity amounts to 4.4%". Productivity gains were larger in capital-intensive sectors, which is consistent with capital substitution, but productivity also rose in labour-intensive sectors.
- **Implication:** derived θ ≈ 4.4/6 ≈ 0.7. Part of this is capital deepening, not free efficiency.
- **Quality:** Credible DiD design and an unexpected reform, but it is a working paper. The starting point is long hours (44 h), and sales per hour mixes in capital, price and composition effects.

**Batut, C., Garnero, A. & Tondini, A. (2023). The Employment Effects of Working Time Reductions: Sector-Level Evidence from European Reforms.** *Industrial Relations* 62(3), 217–232. IZA DP 15566: https://docs.iza.org/dp15566.pdf (verified in text)
- **Design:** Five reforms over 1995–2007 (Portugal, Italy, France, Belgium, Slovenia), using EU KLEMS data for 23 countries × 32 industries. Health, education and agriculture are excluded.
- **Table 2, Panel A with controls (log):** hours per employee −0.013***; total hours −0.036**; employment −0.023 (s.e. 0.027); VA −0.025 (0.022); VA per hour +0.012 (0.022); compensation per hour +0.018 (0.011).
- **Panel B, continuous exposure:** hours per employee −0.059***; VA per hour +0.169 (0.119).
- **Authors' summary:** the effect on VA per hour "appears to be positive but non-significant". The paper "can reject" full work-sharing.
- **Implication:** derived point θ ≈ 0.9 in both panels, but the 95% confidence interval runs roughly from −2 to +4, so the data are uninformative about θ.
- **Quality:** The best multi-country design available, but it identifies only relative sector effects and has low power for productivity.

**Park, W. & Park, Y. (2019). When Less is More: The Impact of the Regulation on Standard Workweek on Labor Productivity in South Korea.** *Journal of Policy Analysis and Management* 38(3), 681–705, doi:10.1002/pam.22136. KDI Policy Forum 267 (2017): https://econpapers.repec.org/RePEc:zbw:kdifor:267
- **Design:** Korea's phased move from 44 to 40 h (2004–11), DiD on manufacturing plants.
- **Finding (verified, abstract):** "the policy reduced per-worker hours but increased per-worker output". The KDI summary gives "an increase of 1.5%" in annual output per worker at plants with 10 or more employees, likely mediated by TFP and capital.
- **Implication:** derived θ > 1.
- **Quality:** Starting hours were very long, well above Pencavel's threshold, and the setting is manufacturing. This does not transfer to a 39→30 h cut.

**Hunt, J. (1999). Has Work-Sharing Worked in Germany?** *Quarterly Journal of Economics* 114(1), 117–148. NBER WP 5724: https://www.nber.org/papers/w5724
- **Working-paper finding (verified in text):** a one-hour cut in standard hours was associated with "a 2-3% fall in worker-hours for hourly-paid workers". Estimates are conditional on sales, so implied hourly-productivity gains are partly mechanical.
- Not used for θ.

### 2.3 Trials and pilots (direction informative, magnitudes not usable)

**Autonomy & Alda (2021). Going Public: Iceland's journey to a shorter working week.** https://en.alda.is/wp-content/uploads/2021/07/ICELAND_4DW.pdf (verified in text)
- **Setting:** Reykjavík City and national government trials, 2015–2019. About 2,500 workers moved from 40 to 35–36 h with no pay cut. Workplaces included offices, playschools, social services and hospitals.
- **Finding:** "Productivity and service provision remained the same or improved across the majority of trial workplaces"; indicators "either stayed within expected levels of variation, or rose".
- **Cost of the national rollout:** "there were a number of workplaces where this was impossible and more staff had to be hired. Increased costs for the Icelandic Government are estimated to be 4.2 billion ISK yearly … due to increased staffing in healthcare — indeed, two-thirds of the total costs are estimated to be in healthcare alone". The report cites a press source for this figure.
- **Quality:** An advocacy-organisation report with no common productivity metric, small and selected trial units, and a cut of only about 10%. The healthcare hiring cost is the most policy-relevant fact in the report.

**Autonomy et al. (2023). The results are in: The UK's four-day week pilot.** https://autonomy.work/wp-content/uploads/2023/02/The-results-are-in-The-UKs-four-day-week-pilot.pdf (verified in text)
- **Setting:** 61 volunteer firms (they paid a small donation to take part), about 2,900 staff, June–December 2022. Pre/post design with **no control group**.
- **Hours:** fell "from 38 hours per week on average to 34" (self-reported).
- **Revenue:** "+1.4% on average, weighted by company size, across those 23 organisations"; +34.5% against an earlier comparison period (24 firms).
- **Other metrics:** headcount −1.3% (34 firms). Sick and personal days fell from 2.0 to 0.7 per employee per month. Resignations fell from 2 to 0.8 per 100. The report itself says the authors are "unable to say that these three trends are statistically significant."
- **Implication:** naive derived θ ≈ 1.
- **Quality:** Severe selection (firms that expected to manage opted in). Revenue is nominal and not output volume. Fewer than half the firms reported revenue. Produced by advocates. Not usable as an economy-wide parameter; it supports only "θ can be high in self-selected knowledge-work firms."

## 3. Evidence on (b): employment effects of mandated reductions

Consensus: mandated cuts with monthly pay held constant **do not create work-sharing jobs economy-wide**. The best-identified studies find employment effects that are null or negative for affected workers and firms.

| Study | Reform | Employment result (as stated) | Verified |
|---|---|---|---|
| Crépon & Kramarz (2002) *JPE* 110(6) 1355–89 | France 1982, 40→39 | Job losses for directly affected workers "between 2% and 4%"; minimum-wage workers hit hardest | yes (IZA abstract) |
| Chemin & Wasmer (2009) *JOLE* 27(4) 487–524 | France 35 h, Alsace-Moselle DiD/DDD | Weaker implementation in Alsace-Moselle but no significant employment difference | yes (abstract) |
| Estevão & Sá (2008) *Economic Policy* 23(55) | France 35 h, large vs small firms | "aggregate employment was unaffected but labour turnover increased" | yes (abstract) |
| Gubian et al. (2004) DARES | France 35 h | About 350,000 jobs 1998–2002 (with payroll-tax cuts and wage moderation) | yes |
| Crépon, Leclair & Roux (2004) | France Aubry I firms | +9.9% employment vs 39 h firms; "mécanismes de partage du travail ne semblent pas prépondérants" (cost reduction channel) | yes |
| Raposo & van Ours (2010) *Econ. Letters* 106(1) 61–63 | Portugal 1996, 44→40 | Lower job separation for affected workers; higher job loss for those already below 40 h | yes (abstract) |
| Asai, Lopes & Tondini (2024) WP | Portugal 1996 | About −2% employment, through reduced hiring | yes |
| Hunt (1996 WP / 1999 QJE) | Germany 1984–94, union agreements | WP: +0.3–0.7% employment per hour cut (1984–89), "at most 1.1%" in total. QJE abstract: "may have reduced employment in the period 1984–1994" | yes |
| Kawaguchi, Naito & Yokoyama (2017) *JJIE* 43 59–76 | Japan 48→40 | "did not contribute to job creation"; ESRI WP: 1 h legal cut → 0.14 h actual cut; graduate hiring suppressed | yes (abstracts) |
| Sánchez (2013) *Labour Econ.* 20 24–37 | Chile 2005, 48→45 | "no significant effects … on employment transitions"; hourly wage compensation | yes (WP abstract) |
| Batut, Garnero & Tondini (2023) | 5 EU reforms 1995–2007 | Employment −0.023 (n.s.); full work-sharing rejected | yes |

The French positive estimates come from comparing firms that **chose** subsidised early adoption with firms that did not. The quasi-experimental designs (Chemin–Wasmer, Estevão–Sá) find no aggregate effect. **For an induced-hiring offset parameter, evidence supports about 0 for a mandate without new subsidies. A positive value, at most about 0.3–0.4 of lost hours, applies only if accompanied by large payroll-tax cuts and wage moderation, as in France 1998–2002.**

## 4. Health and care services

The evidence on long shifts concerns cutting very long hours (≥12 h shifts, >40 h weeks), not cutting from 39 to 30 h. All of it is cross-sectional or observational.
- **Rogers et al. (2004)** *Health Affairs* 23(4):202–212, doi:10.1377/hlthaff.23.4.202 (abstract verified). Error risk was "significantly increased when work shifts were longer than twelve hours, when nurses worked overtime, or when they worked more than forty hours per week" (n=393 nurses, 5,317 shifts).
- **Dall'Ora et al. (2015)** *BMJ Open* 5:e008331 (abstract verified via Europe PMC). In 31,627 nurses across 12 countries, shifts of ≥12 h vs ≤8 h were associated with emotional exhaustion (aOR 1.26), job dissatisfaction (aOR 1.40) and intention to leave (aOR 1.29).
- **Griffiths et al. (2014)** *Medical Care*, doi:10.1097/MLR.0000000000000233 (abstract verified). Shifts of ≥12 h were associated with poor or failing safety (OR 1.41) and care left undone (RR 1.13).
- **Aiken et al. (2014)** *Lancet*, RN4CAST (verified in author manuscript). "Increase in nurses' workloads of one patient increases the odds on inpatient hospital mortality by 7%" (422,730 patients, 300 hospitals, 9 countries).

**Why θ_health is lower.** Much care output is *time-bound presence*: staffed bed-hours, 24/7 rota coverage, mandated nurse-to-patient ratios, opening hours, child-to-staff ratios in childcare and eldercare. If each worker's hours fall 23%, coverage falls 23% unless more people are hired. Working faster cannot substitute for presence, and the Aiken result says thinner coverage raises mortality.

The plausible offsets are indirect: lower sickness absence and turnover, which raise *effective* hours per contracted hour, and some gains in the administrative and documentation share of the work. The direct evidence for these in a 39→30 h setting is thin.

Iceland's rollout is the clearest real-world signal: healthcare was where productivity could not absorb the cut and staff had to be hired (two-thirds of a 4.2 bn ISK per year cost).

The Gothenburg Svartedalen six-hour nursing-home trial is reported in the press to have needed about 14–17 extra staff. **UNVERIFIED**: news coverage only; I did not find the official evaluation.

## 5. Proposed parameter ranges

The evidence base is thin for a cut of this size and endpoint. Every credible estimate comes from cuts of ≤10% starting from ≥39 h, and the offset should shrink as hours fall (Pencavel, Collewet–Sauermann). I therefore build θ piecewise: the first segment (38.9→35 h) draws on the French and Portuguese reform evidence, discounted for selection and subsidy; the second segment (35→30 h) draws on the fatigue and production-function evidence near 25–35 h.

| Sector / horizon | 38.9→35 h segment | 35→30 h segment | Hours-weighted θ for 38.9→30 | Central |
|---|---|---|---|---|
| Market sector, short run (≤3 y) | 0.2–0.5 | 0.0–0.2 | **0.10–0.35** | **0.20** |
| Market sector, medium run (5–10 y, reorganisation) | 0.3–0.6 | 0.05–0.3 | **0.15–0.45** | **0.30** |
| Health / care / education (presence-bound) | 0.0–0.2 | 0.0–0.1 | **0.0–0.15** | **0.05** |
| Office / knowledge work, self-selected (pilot evidence) | up to ~1 (UK, Iceland) | no evidence | not for economy-wide use | — |

**How the weights work.** The weighted value combines the segments by hours: 3.9 h in the first segment and 5 h in the second. Example: 0.45·3.9/8.9 + 0.15·5/8.9 ≈ 0.28. This roughly matches the official ex ante assumption of "un tiers de la RTT", applied to a cut only half as deep.

**Medium-run caveat.** Much of the medium-run gain in the French and Portuguese firms came with capital deepening (Asai et al.; K +4.2% in Crépon et al.). In a model that keeps physical feasibility separate, it should be counted as **capital substitution with its own resource cost**, not as free labour efficiency. If the model tracks capital separately, cut the medium-run θ by about 0.1.

**Implication for V6.2.** Under a central θ of 0.20 short run and 0.30 medium run, the required 16–29% rise in output per hour falls by roughly 3–8 percentage points. Most of the gap remains and must come from additional workers, trend productivity, or lower output. Health and care should be modelled as needing roughly proportional extra staffing (θ≈0–0.15).

**Confidence.**
- **Low–moderate** for the market-sector range. The direction (θ>0, θ<1) is well supported; the magnitude for the 35→30 segment rests on extrapolation from only two studies (Pencavel, Collewet–Sauermann).
- **Moderate** that health and care θ is near zero for coverage-bound tasks.
- **High** that mandated cuts without subsidy do not generate work-sharing hiring economy-wide.

**What the evidence does not support:**
- any θ above 0.5 for an economy-wide mandatory 30 h week;
- using the UK or Iceland pilot figures (θ≈1) as model parameters;
- treating the 350,000 French jobs as a transferable hiring elasticity without the accompanying payroll-tax subsidy.

## 6. Unverified / not opened

- **Svartedalen (Gothenburg) trial:** press only.
- **Studies cited only through Batut et al.'s literature review:** Gonzaga et al. (2003, Brazil), Varejão (2005, Portugal) and Skuterud (2007, Québec). I did not open them; Batut et al. describe their results as null.
- **Unconfirmed DOIs and page numbers:** the DOIs for Crépon & Kramarz (2002), Estevão & Sá (2008), Raposo & van Ours (2010), Pencavel (2015 EJ), and the volume and pages for Aiken et al. (2014). The citations themselves are confirmed by repository pages.
- **Paywalled journal versions:** I did not read the published versions of Chemin & Wasmer, Estevão & Sá or Kawaguchi et al. beyond their abstracts, so I report no effect sizes for them.
