# UNIRA — One Humanity, One Future

**Open research on a proposed world without war, poverty or waste, tested against real data.**

UNIRA is a proposal for one world federation of equal regions. It has a 30-hour working week, a stable money (the U) with fixed prices, allocation of resources by need and population, and no armies except a small common Peace Force. This repository holds everything behind it: data, models, tests, the papers, the concept, the draft constitution and the book draft. It is published free so that anyone can check it, criticise it and improve it.

**Status (8 November 2026): preliminary, not peer reviewed.** The research tests *physical feasibility under stated assumptions*. It does not show that UNIRA is politically achievable or that people would behave as assumed. A self-audit and the responses to it are in `v77/review/SELF_AUDIT_2026-11-04.md`.

**Website and simulator:** https://nova-ai-company.github.io/unira-one-earth/

| | |
|---|---|
| [Paper V1](https://nova-ai-company.github.io/unira-one-earth/paper_v1.html) | **The consolidated paper:** physical feasibility, validation and joint uncertainty (`paper/`) |
| [The concept](https://nova-ai-company.github.io/unira-one-earth/concept.html) | The normative design in one document, with the research status of each part and the open gaps (`concept/`) |
| [Draft Constitution of One Earth](https://nova-ai-company.github.io/unira-one-earth/constitution.html) | The legal text of the author's decisions |
| [Working Paper 02](https://nova-ai-company.github.io/unira-one-earth/paper.html) | The full research log, V6.2–V9.1 (superseded as the paper by Paper V1; kept for traceability) |
| [Simulator](https://nova-ai-company.github.io/unira-one-earth/simulator.html) | Change the assumptions and see the results |
| [Book draft](https://nova-ai-company.github.io/unira-one-earth/book.html) | *UNIRA: One Humanity, One Future* (second draft, English) |
| [For reviewers](https://nova-ai-company.github.io/unira-one-earth/review.html) | Review brief, questions by field, self-audit, feedback form |
| [Prices](https://nova-ai-company.github.io/unira-one-earth/prices.html) | Price calculator: what things cost in U and in hours of work |
| [Pilot proposal](https://nova-ai-company.github.io/unira-one-earth/pilot.html) | A 30-hour, full-employment town inside today's law, with pre-registered predictions and failure criteria |

## How this research was made (authorship disclosure)

- **The author** set the purpose, the design rules, every decision recorded in `v63/DESIGN_CLARIFICATIONS_2026-11-03.md`, the research questions, and the constitutional text; they reviewed and corrected results throughout.
- **An AI assistant** (Anthropic Claude; models Opus and Fable) drafted the models, code, tests, evidence files, papers, constitution drafts and book chapters under the author's direction, on 3–4 November 2026.
- **No independent human expert has yet reviewed the work.** The evidence files record, row by row, whether a figure was read in its source or taken from a search summary; the reference list records which entries were verified. The models are reproducible, which proves that the code does what it says, not that its assumptions are right.
- **What the pace implies.** Hundreds of modelling judgements were made in hours. Readers should expect errors of judgement, and are asked to report them (issue templates in `.github/`).

## Main results (with their conditions)

- **The working week (France, Europe).** Cutting to 30 h at once would need about 20% more output per hour, or about 88% of adults aged 20–64 at work against 75.4% in 2025 (Eurostat). The constitution instead starts each region at the shortest week its existing labour reserve can cover with no productivity gain (35 h in France, 33–40 h in Europe, never above 40 h), pays the full base salary from day one and shortens the week as measured productivity grows until 30 h (T-10). Shorter hours raise productivity, and less work goes on selling and speculation. (V6.2–V6.3, V9.2)
- **Enough for everyone.** Today's world output already covers decent food and energy for all. A comfortable level (40 GJ of final energy per person) fits a 1.5 °C-class pathway at 6–13% less energy than the world uses today, if waste is halved, materials fall about 2.7× and clean energy is built fast. (V6.5–V6.6)
- **30-year plan.** In the central case every region reaches 40 GJ per person by year 27 and EU-level health staffing by year 30. Comfortable housing for all needs home building to grow 5–10% a year. At 1.2 TW a year of clean energy, the build closes the poorer regions' gap but leaves final energy only about 75% clean by year 30. Bringing fossil use near zero as well needs about 1.8 TW a year. (V6.7, V7.0)
- **Needs-first versus market.** With the same resources, needs-first allocation closes the gaps. A reformed market does not, unless about 90% of its new capacity is directed to need. Strong safeguards against error and corruption keep about 80–89% of this advantage. (V6.8–V6.9)
- **Joining.** Compared with a reformed market world after 30 years, 146 regions with 86% of humanity gain materially by joining. Inside the 33 rich regions whose average falls, 44% of the people (495 million, mostly the poor and lower middle) are better off even at the lowest UNIRA salary, so **about 92% of humanity is better off**. Nobody falls below the comfortable level. (V7.2, V7.4)

- **AI planning.** Machine learning forecasts needs well (population ±0.1% a year ahead) and beats simple rules for population, food and health workers, but not for short-term energy. Over 30 years information errors cost ≤1%, while diversion costs 12–19%, so AI's main value is integrity checks. Forecasts are least accurate in the poorest regions, so their statistics come first. (V7.8)

- **Missing designs and power (V7.9).** Decent-for-all first halves the time until every region has decent energy, health care and housing. A moderate money cap (1.5 years of salary) with protected home and retirement accounts keeps money stable. 17 new constitutional articles close five legal routes to the capture of power found by a 13-scenario stress test.

- **Completing the economy (V8.2).** Ordinary goods follow orders and waiting lists (96% served within 3 months, nobody priced out). Hard jobs get hardship pay, shorter hours and better conditions. Investment puts maintenance first. A restaurant and a supermarket balance their accounts with UNIRA prices and salaries. Salaries converge across regions with needs guaranteed in kind from year 1 (target 20 years).

These are tests of **physical feasibility under stated assumptions**, not forecasts, and not a demonstration that the system would work. The defensible claim is that no physical constraint was identified under the stated conditions. Every limitation is listed in Paper V1 (§7), the concept (§11) and the research notes. A backtest of the delivery model and a joint propagation of all uncertain assumptions are in `validation/`.

## Repository layout

| Folder | Content |
|---|---|
| `paper/` | **Paper V1**: the consolidated modelling paper (physical feasibility, validation, uncertainty) |
| `concept/` | **The concept**: the normative design, research status of each part, open gaps |
| `validation/` | Backtest of the delivery pace rule (2000–2024) and joint uncertainty propagation for v67, v89 and v91 |
| `handover/` | Project specification and history up to V6.1 |
| `v62/` | France: labour hours by sector, 30-hour week, labour reserve (Eurostat) |
| `v63/` | Input–output model in hours, take-up flows, health staffing, year-1 ledger; **`run_all.py` rebuilds everything** |
| `v64/` | Money circuit (stock-flow consistent) and lifecycle model with the money cap |
| `v65/` | World sufficiency: food, energy, health workers (FAO, World Bank, WHO, ILO, OWID) |
| `v66/` | Ecology limits, health training plan and its levers, training capacity with theory online and facilities in rotation, housing need, construction capacity |
| `v67/` | 30-year transition model, dashboard, **Working Paper 02** |
| `v68/` | UNIRA versus reformed market (matched resources) and verification |
| `v69/` | Allocation failures (error, lag, misreporting, leakage) and safeguards |
| `v70/` | Housing acceleration, low-carbon building, housing levers (factory building, decent core first, household-built extensions), where home and wall factories go, materials by region against world resources, safeguard articles |
| `v71/`–`v72/` | Security and consumption; transition, joining, property and debts |
| `v73/book/` | Book draft |
| `v74/` | Income distribution inside rich regions |
| `v75/constitution/` | Draft Constitution of One Earth and voting tests |
| `v76/` | Peace Force and migration evidence |
| `v77/` | Website, simulator and outside-review package |
| `v78/` | AI / machine-learning planning of needed production: backtests, fairness, 30-year information test |
| `v81/prices/` | Price calculator (Article 13): embodied hours × 146.4 U + resource surcharge, 62 product groups, examples |
| `v82/` | Completing the economy: production signals, hard jobs, investment, restaurant and supermarket accounts, world money (option C), trade, resale, sizes, behaviour register |
| `v80/pilot/` | Pilot plan: precedents (TZCLD, Marienthal, shorter-week trials), predictions, failure criteria, budget |
| `v92/` | The working week during the transition: measured starting week (France 35 h, Europe 33–40 h) falling to 30 h as productivity rises, pay unchanged; adopted as T-10 on 8 November 2026, with the consistency check of that day's constitution changes |
| `concept/UNIRA_TRANSITION_PLAN.md` | The transition plan: phases, objectives and measured triggers from joining to a stable UNIRA economy, with model dates and their uncertainty |
| `v87/`–`v89/` | Living-standard levels: real cost, essential infrastructure, integrated dates |
| `v90/` | Fair distribution and armed conflict: evidence, country conflict model coupled with V8.9, scenarios A–D, proposed (not applied) constitution changes |
| `v91/` | Fair institutions and armed conflict: historical panel (UCDP/PRIO, World Bank governance indicators), institutional scenarios A–D, proposed (not applied) constitution changes |
| `v79/` | The missing designs (allocation formula, prices, desirable homes, money cap, innovation) and safeguards against concentrated power |
| `docs/` | The published website (generated) |

## Reproduce everything

Python 3.10+ and nothing else (standard library only). All data are frozen snapshots with SHA-256 hashes in each `raw_manifest.csv`.

```
python3 v63/run_all.py
```

This regenerates every output, the dashboard, book, constitution and website, then runs all tests (about 270).

## Take part

- Report an error or propose better data: open an **Issue**.
- Debate the ideas: use **Discussions**.
- Formal review: see `v77/review/` and the [reviewer page](https://nova-ai-company.github.io/unira-one-earth/review.html).

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licences

- Code: MIT ([LICENSE](LICENSE)).
- Text (paper, book, constitution, notes): CC BY 4.0 ([LICENSE-TEXT.md](LICENSE-TEXT.md)).
- Data: each source keeps its own licence ([DATA_LICENSES.md](DATA_LICENSES.md)). WHO data are non-commercial.

## How to cite

See [CITATION.cff](CITATION.cff).
