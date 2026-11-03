# UNIRA — One Humanity, One Future

**Open research on a world without war, poverty or waste, tested against real data.**

UNIRA is a proposal for one world federation of equal regions. It has a 30-hour working week, a stable money (the U) with fixed prices, allocation of resources by need and population, and no armies except a small common Peace Force. This repository holds everything behind it: data, models, tests, the working paper, the draft constitution and the book draft. It is published free so that anyone can check it, criticise it and improve it.

**Website and simulator:** https://nova-ai-company.github.io/unira-one-earth/

| | |
|---|---|
| [Simulator](https://nova-ai-company.github.io/unira-one-earth/simulator.html) | Change the assumptions and see the results |
| [Working Paper 02](https://nova-ai-company.github.io/unira-one-earth/paper.html) | The scientific paper (also as Word in `docs/downloads/`) |
| [Draft Constitution of One Earth](https://nova-ai-company.github.io/unira-one-earth/constitution.html) | 48 articles |
| [Book draft](https://nova-ai-company.github.io/unira-one-earth/book.html) | *UNIRA: One Humanity, One Future* (second draft, English) |
| [For reviewers](https://nova-ai-company.github.io/unira-one-earth/review.html) | Review brief, 70 questions, feedback form |

## Main results (with their conditions)

- **The 30-hour week (France).** Cutting from today's hours to 30 h needs about 20% more output per hour. That gap closes from year 1 if about 88% of adults aged 20–64 work, against 75.4% in 2025 (Eurostat). Shorter hours raise productivity, and less work goes on selling and speculation. (V6.2–V6.3)
- **Enough for everyone.** Today's world output already covers decent food and energy for all. A comfortable level (40 GJ of final energy per person) fits a 1.5 °C-class pathway at 6–13% less energy than the world uses today, if waste is halved, materials fall about 2.7× and clean energy is built fast. (V6.5–V6.6)
- **30-year plan.** In the central case every region reaches 40 GJ per person by year 27 and EU-level health staffing by year 30. Comfortable housing for all needs home building to grow 5–10% a year. At 1.2 TW a year of clean energy, the build closes the poorer regions' gap but leaves final energy only about 75% clean by year 30. Bringing fossil use near zero as well needs about 1.8 TW a year. (V6.7, V7.0)
- **Needs-first versus market.** With the same resources, needs-first allocation closes the gaps. A reformed market does not, unless about 90% of its new capacity is directed to need. Strong safeguards against error and corruption keep about 80–89% of this advantage. (V6.8–V6.9)
- **Joining.** Compared with a reformed market world after 30 years, 146 regions with 86% of humanity gain materially by joining. (V7.2)

- **AI planning.** Machine learning forecasts needs well (population ±0.1% a year ahead) and beats simple rules for population, food and health workers, but not for short-term energy. Over 30 years information errors cost ≤1%, while diversion costs 12–19%, so AI's main value is integrity checks. Forecasts are least accurate in the poorest regions, so their statistics come first. (V7.8)

These are tests of **physical feasibility under stated assumptions**, not forecasts. Every limitation is listed in the working paper and the research notes.

## Repository layout

| Folder | Content |
|---|---|
| `handover/` | Project specification and history up to V6.1 |
| `v62/` | France: labour hours by sector, 30-hour week, labour reserve (Eurostat) |
| `v63/` | Input–output model in hours, take-up flows, health staffing, year-1 ledger; **`run_all.py` rebuilds everything** |
| `v64/` | Money circuit (stock-flow consistent) and lifecycle model with the money cap |
| `v65/` | World sufficiency: food, energy, health workers (FAO, World Bank, WHO, ILO, OWID) |
| `v66/` | Ecology limits, health training plan, housing need, construction capacity |
| `v67/` | 30-year transition model, dashboard, **Working Paper 02** |
| `v68/` | UNIRA versus reformed market (matched resources) and verification |
| `v69/` | Allocation failures (error, lag, misreporting, leakage) and safeguards |
| `v70/` | Housing acceleration, low-carbon building, safeguard articles |
| `v71/`–`v72/` | Security and consumption; transition, joining, property and debts |
| `v73/book/` | Book draft |
| `v74/` | Income distribution inside rich regions |
| `v75/constitution/` | Draft Constitution of One Earth and voting tests |
| `v76/` | Peace Force and migration evidence |
| `v77/` | Website, simulator and outside-review package |
| `v78/` | AI / machine-learning planning of needed production: backtests, fairness, 30-year information test |
| `docs/` | The published website (generated) |

## Reproduce everything

Python 3.10+ and nothing else (standard library only). All data are frozen snapshots with SHA-256 hashes in each `raw_manifest.csv`.

```
python3 v63/run_all.py
```

This regenerates every output, the dashboard, book, constitution and website, then runs all 157 tests.

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
