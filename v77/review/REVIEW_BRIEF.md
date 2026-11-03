# UNIRA research V6.2–V7.6: brief for external reviewers

*Prepared 3 November 2026 for independent expert review. Paths are relative to the UNIRA research folder. "WP02 L120" means line 120 of `v67/WORKING_PAPER_02.md`; "Const. Art. 25" means `v75/constitution/UNIRA_CONSTITUTION_DRAFT.md`.*

## 1. What UNIRA is: design and claims kept apart

UNIRA is a proposal by one author for a single democratic world federation, "One Earth", in which today's countries become regions. The research has two layers, and reviewers are asked to judge them separately.

**A. Normative design (not tested; set by the author).** WP02 L24–44 lists 19 design rules, and the full wording is in `v63/DESIGN_CLARIFICATIONS_2026-11-03.md`. The main ones are:

- a 30-hour week (6 h × 5 days) from year 1;
- allocation of resources by needs × population;
- no commercial competition for profit;
- one digital currency (U) with permanently fixed prices for essentials;
- a 5,000 U base salary with multipliers of 1×–5×;
- a yearly personal money cap, with money above it going to a One Earth Fund;
- at most two homes per adult;
- abolition of national armed forces.

Three proposals that came out of the research were accepted provisionally (P1–P3, WP02 L122–126). A draft constitution (`v75/constitution/`) and draft transition rules (`v72/TRANSITION_RULES.md`) turn the design into legal text. These are value choices. The research does not argue that they are desirable.

**B. Empirical and model-based claims (what we ask you to test).** The research asks whether those rules are *physically* feasible, given today's people, hours, energy, food, land, materials, health workers and homes. It also asks how the rules perform against a reformed market economy that has the same resources. It does **not** test political achievability, legitimacy or behaviour under the new institutions (WP02 L20, L312).

## 2. Research questions

| Version | Question | Main files |
|---|---|---|
| V6.2 | How many hours does France lose under a 30 h cap, and what productivity gain, extra workforce or output cut would offset it? How large is the labour reserve in 30 European countries? | `v62/RESEARCH_NOTE.md` |
| V6.3 | Where do France's 45 bn hours go (input-output)? What do observed job-finding flows imply for mobilisation in year 1? Can health and care be staffed? | `v63/RESEARCH_NOTE.md`, `v63/io/` |
| V6.4 | Are UNIRA's own monetary rules consistent: fixed prices, 50% saving, the money cap? | `v64/RESEARCH_NOTE.md` |
| V6.5 | Does world supply cover decent or comfortable living for everyone, allocated by needs × population? | `v65/RESEARCH_NOTE.md` |
| V6.6 | Does comfortable living for 9.7 bn people fit within climate, land and material limits? How long does the health-workforce build-up take? | `v66/RESEARCH_NOTE.md` |
| V6.7 | What does a 30-year, region-by-region transition look like (217 regions)? | `v67/transition.py`, WP02 §7 |
| V6.8 | How does UNIRA compare with a reformed market economy (B, B2) when resources are matched? | `v68/RESEARCH_NOTE.md` |
| V6.9 | Does the advantage survive measurement error, data lags, misreporting and leakage? | `v69/RESEARCH_NOTE.md` |
| V7.0 | How fast can housing be built, and with what carbon and labour? What constitutional safeguards follow? | `v70/RESEARCH_NOTE.md` |
| V7.1 | Does secure access reduce over-consumption? | `v71/RESEARCH_NOTE.md` |
| V7.2 / V7.4 | Who gains by joining voluntarily? What are the distributional effects inside rich regions? | `v72/TRANSITION_RULES.md`, `v74/distribution/` |
| V7.3 | Book draft. This is communication, not evidence. | `v73/book/` |
| V7.5 / V7.6 | Constitution draft and voting-rule test; evidence on migration and on sizing a Peace Force. | `v75/constitution/`, `v76/` |

## 3. Methods

- **Data.**
  - Labour and output: Eurostat national accounts and LFS (nama_10_a64_e, lfsa_ewhun2, lfsi_sla_a and others), INSEE.
  - France 2022 input-output: naio_10_cp1700.
  - Health workforce: Eurostat health tables and WHO NHWA.
  - Population, food and labour: World Bank, UN WPP 2024, FAO food balance sheets, ILO modelled estimates.
  - Energy: Our World in Data, which republishes Energy Institute data and is marked for recheck.
  - Literature registers: decent-living thresholds (`v65/thresholds/`), ecology (`v66/ecology/`), health prevention (`v66/evidence_health/`), governance and leakage (`v69/evidence/`), housing (`v70/evidence/`), transition history (`v72/evidence/`), migration and the Peace Force (`v76/`).
- **Evidence classes.** Every number carries one tag: VERIFIED_OFFICIAL, REPORTED_NEEDS_RECHECK, MODEL_DERIVED, SYNTHETIC_ASSUMPTION or NORMATIVE_TARGET (WP02 L62–67). Each row in a literature register states whether the value was found in text that was actually fetched (`verified_in_fetched_text`), and some rows say "no / snippet only".
- **Models.** All are written in pure Python using only the standard library.
  - Sector hours-cap arithmetic with a constant-absence ratio method (`v62/src/unira_v62/model.py`).
  - A Leontief hours-multiplier model with hypothetical extraction (`v63/io`).
  - A year-1 labour ledger (`v63/ledger`).
  - A one-region stock-flow money circuit plus a 6,000-agent, 60-year lifecycle simulation (`v64`).
  - Per-capita sufficiency ratios (`v65/model`).
  - A 30-year water-filling allocation across 217 regions (`v67/transition.py`).
  - Lever-swap counterfactuals (`v68/counterfactual/compare.py`).
  - A Monte Carlo of perceived needs, with 30 runs per scenario (`v69/coordination/model.py`).
  - A Penrose/double-majority voting check (`v75/constitution/voting.py`).
- **Reproducibility.** Raw data are frozen with SHA-256 hashes and retrieval times in `raw_manifest.csv` files. WP02 reports 151 tests and byte-identical regeneration for V6.2–V6.7. The current tree contains about 150 test functions across v62–v75. The entry point is `python3 v63/run_all.py`, and each later version has its own `run.py`.
- **Earlier audits.** Four audits were run as separate agents (`v62/audit/AUDIT_FINDINGS.md`):
  - archive integrity: 125/125 hashes match and 90/90 tests pass;
  - primary-source checks of 23 figures: 0 contradicted, 7 with caveats;
  - an adversarial code review: 5 major findings, fixed or documented;
  - an evidence review on hours and productivity (22 sources).

  The audits produced corrections that matter for this review. V5.6/V5.7 were *not* stock-flow consistent, the V5.6 stress case was the baseline, and V6.1's 46-week convention was not a 30 h cap. **None of these audits was done by an independent human expert.** That is the purpose of this review.

## 4. Headline results and their conditions

Each result holds only under the conditions stated next to it.

1. **Labour, France year 1 (V6.2–V6.3).**
   - A 30 h cap on employees removes 16.7% of hours, so output per hour must rise 20.1% (29.1% if the self-employed are also capped). That is about 32 years of 2015–19 trend growth.
   - Central evidence (θ = 0.20 market / 0.05 care, observed job-finding flows giving +0.53 m people, a moderate cut in market-specific activity) still leaves about 10% to find.
   - Raising the employment rate at ages 20–64 to **88%**, higher than in any observed country, with entrants at 75% productivity, closes the gap.
   - Health and care remain short in year 1 (about 100 k nurses and 145 k care workers).
2. **Money (V6.4).**
   - Fixed prices plus 50% saving make unspent money grow without limit: 152 months of consumption by year 60.
   - A cap of about 1.4 years of base salary, plus zero-interest home credit, stabilises deposits at about 12 months. About 57% of adults are then at the cap, and about 20–23% of regional consumption value flows to One Earth.
   - Pay drift must not exceed productivity growth.
   - All behavioural responses are SYNTHETIC.
3. **World sufficiency (V6.5).** Supply ÷ need, world level:

   | Need | Ratio | Condition |
   |---|---|---|
   | Decent food | 1.16 | — |
   | Comfortable food | 1.11 | Only with consumer waste halved |
   | Energy at 40 GJ final per person | 1.27 | — |
   | Energy at today's EU level | 0.62 | — |
   | Health workers at the EU level | 0.45 | About +59 m workers needed |
4. **Ecology (V6.6).**
   - 40 GJ per person for 9.7 bn people is 386 EJ, inside IPCC 1.5 °C-class ranges. That needs about 50% electrification, fossil CO₂ near zero by 2050, and solar plus wind built 1.7–1.9× faster than the 2025 record.
   - Material footprint per person must fall about 2.7×.
5. **30-year transition (V6.7), central case.**
   - Everyone reaches 40 GJ by year 27 and EU-level health staffing by year 30. Housing is 50% closed.
   - This requires regions above 40 GJ to cut energy use by about 3–4% a year.
   - These figures assume **perfect allocation**. With strong safeguards, 40 GJ for everyone is reached in year 29 (V6.9).
6. **Counterfactual (V6.8).** With matched resources, B (reformed market) widens the gaps and B2 (ambitious cooperative market) closes 14% of the energy gap by year 15, against 60% for UNIRA. The advantage is defined entirely by lever settings (allocation share, employment rate, training plan, disarmament). No efficiency bonus is assumed.
7. **Governance (V6.9).** Share of the energy gap closed by year 15:

   | Scenario | Energy gap closed by year 15 |
   |---|---|
   | UNIRA, perfect allocation | 60% |
   | UNIRA, strong safeguards | 52% |
   | UNIRA, no safeguards | 36% |
   | UNIRA, worst governance observed | 15% |
   | B2 | 14% |

   Leakage dominates the result. It is calibrated mainly on cash and food transfer programmes.
8. **Housing (V7.0).** 27 m² per person for everyone by about year 27 needs building capacity to grow 5–10% a year, to a peak of 6–7 bn m² a year, with about 250 m builders. Low-carbon frames keep embodied CO₂ to about 16 Gt, against 43 Gt for conventional concrete.
9. **Joining (V7.2).** 86% of the world's population "gains materially". **The comparator is the reformed-market world (B) at year 30, not today.** The material index is an equal-weight log mean of energy, health workers and floor area.
10. **Voting (V7.5).** Square-root seat apportionment with a 5% cap gives India and China about 4.4% of seats each. Under the 55%/65% double majority, with population counted by square root, at least 21 regions are needed to block.

## 5. SYNTHETIC or judgement-based assumptions that drive the results

| # | Assumption (value) | Drives | Where |
|---|---|---|---|
| S1 | An employment rate of 88% at ages 20–64 is reachable in year 1 (rule 14 is normative; its feasibility is not) | Closing France's year-1 gap; C vs B | `v63/ledger`, `v68` |
| S2 | Entrant productivity 75% in year 1 | Year-1 ledger | `v62` §4b, `v63/ledger` |
| S3 | θ (share of lost hours recovered as productivity) of 0.10–0.35 in market sectors and 0–0.15 in care, extrapolated beyond any evaluated reform (all evaluated reforms were cuts of 10% or less, from 39 h or more) | Labour gap | `v62/audit/hours_productivity_evidence.md` |
| S4 | Reduction levels for market-specific activity (5–75%) are normative illustrations | 1.7–6.6% of hours freed | `v63/io` §4.1 |
| S5 | Share unable to work 3%; mean pay multiplier 1.90; housing share of construction 50% | Money circuit | `v64` §1–2 |
| S6 | Saving behaviour (0–50%) and the response to the money cap (save vs spend) | Money stability | `v64/run_lifecycle.py` |
| S7 | Rich-region energy decline of 3–4%/yr; military energy proxied by its 5.5% *emissions* share | Climate envelope (409 EJ) | `v67/config.json` |
| S8 | Share of new homes to regions in need (50/75/90% for UNIRA cases; 30% for B, with no source) | Housing results; C vs B | `v67/config.json`, `v68` |
| S9 | Health training capacity of 3/4.5/6% of the workforce per year; growth of +7% or +10%/yr; 25–50% of 27.4 m soldiers volunteer; prevention lowers need by 3–14% | Health timelines | `v66/evidence_health/parameters.json` |
| S10 | Audit detection 50%/yr; errors independent across regions; capture modelled as loss only | Governance robustness | `v69/evidence/parameters.json` |
| S11 | Building growth of 5–10%/yr; 40% of need upgradable at 40% of the materials; 48 h of labour per m² | Housing timeline and workforce | `v70/evidence/parameters.json` |
| S12 | B/B2 lever values other than the verified 20% clean-energy investment share | Size of the UNIRA advantage | `v68` levers table |
| S13 | Equal weights in the material index; the union-of-gainers' capacity proxied by its share of energy use | "86% gain"; union result | `v72/joining/run.py` |
| S14 | World primary→final energy ratio 0.66 (the EU's); population linear 2024→2050, then flat | Energy sufficiency | `v65`, `v67/transition.py` |
| S15 | Energy rebound of 10–30% under flat-rate access | Metering rule | `v71` |
| S16 | Peace Force rotation multiplier 3×; USD 100–150 k per member; refugee return share 50–85%; steady-state migration 2–4% | Constitutional ceilings and Art. 4b | `v76/*/parameters.json` |

## 6. Known limitations (as stated by the research)

- National and regional averages hide inequality within countries.
- Floor area per person comes from a regional model (IMAGE), not from statistics. World health-graduate numbers are estimated from OECD ratios.
- Euro input-output coefficients stand in for physical structure. Physical-unit accounts do not exist yet.
- No UNIRA economy has ever been observed, so all behavioural parameters are assumptions.
- Leakage evidence comes from transfers, not infrastructure. Correlated errors, regional favouritism and political dynamics are not modelled.
- The hours needed to run UNIRA's own institutions (the U transaction network, allocation bodies, democratic bodies) are not counted.
- Capital, workplaces and supervision for about 5 m new workers in France are not modelled, and neither are capital lead times.
- The 30-year transition handles energy, health and housing independently. It does not draw labour, materials or energy for construction out of the other domains.
- Lead times and several thresholds are REPORTED_NEEDS_RECHECK.

**Internal inconsistencies found while preparing this brief, and corrected on 2026-11-03** (reviewers should check the corrections):

- **Annual home-building figure.** The figures are now reconciled. About 4.7 bn m² a year closes the 65 bn m² backlog by year 27 (V6.7). Counting population growth and upgrading (109 bn m², V7.0) raises the peak to 6–7 bn m² a year. WP02 now states both.
- **Labour per m².** WP02 now uses 33–64 h per m² (V7.0, 48 h central) throughout.
- **Safeguard performance.** The "≈85% preserved under strong safeguards" figure ranges from 80% to 89% depending on domain (still open).
- **Voting outputs.** `v75/outputs/voting.json` now records the square-root double majority (`double_majority_55_65_sqrt`), and a test covers it. Blocking needs at least **21** regions (not 20), and passing needs 120 of 217.
- **Double use of the clean-energy build.** This is confirmed and now quantified (`v67/energy_budget_check.py`). At 1.2 TW a year, convergence absorbs 178 of the 217 EJ built by year 30, so final energy is only about 75% clean by year 30. About 1.8 TW a year is needed for convergence plus fossil use near zero. WP02 §7 and the abstract now say so.
- **Test counts.** The test suite now has 151 tests, and WP02 reports this.

## 7. Falsification tests (WP02 L323–330; Const. Art. 39)

| # | Domain | The physical claims are refuted if… |
|---|---|---|
| F1 | Labour | under universal work, the 20–64 employment rate cannot be raised above about 85% within a few years, **and** θ stays below 0.1 |
| F2 | Money | under the cap, people spend rather than save, and demand at fixed prices exceeds supply by more than reserve stocks can absorb |
| F3 | Health | world training capacity cannot grow beyond about 1.5×, which puts EU-level care for all more than 50 years away |
| F4 | Ecology | clean-energy build stays below the 2025 record (669 GW/yr), or material use cannot fall by at least 2× while homes and infrastructure are built |
| F5 | Housing | world construction capacity is too small to add about 65 bn m² within a generation |
| F6 | Comparison | a reformed market economy with the same resources reaches the same outcomes |
| F7 | Governance (V6.9; Art. 39) | leakage cannot be kept well below about 45%, or data lags stay above about 5 years. Needs-first allocation is then no better than a cooperative market. |

Reviewers are asked to judge whether each test is well posed (measurable, not trivially passed, not dependent on SYNTHETIC inputs), and to propose sharper versions. See `FEEDBACK_FORM.md` §5.
