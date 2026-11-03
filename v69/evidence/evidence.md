# V6.9 evidence: errors, lags, leakage and capture in needs-based allocation

**Purpose.** In V6.8, UNIRA's advantage comes from a world entity that allocates new capacity (energy, homes, health workers) to regions by need. This file collects verified numbers on how real allocators fail, and turns them into parameter ranges for a stress test. See `evidence.csv` (44 rows) and `parameters.json`.

**Verification rule.** A row has `verified_in_fetched_text = yes` only when the number appeared in text fetched on 2026-11-03: an abstract, a landing page or a PDF text. Commonly cited figures that could not be seen in fetched text are marked `no` and are not used as anchors. These include Olken's ~24% missing expenditures, the Smartcards ~12.7 pp effect, the TI "10–25%" figure and China's provincial-sum gap.

## 1. Measurement error in needs data
- **Census coverage.** South Africa's 2011 census missed **14.6%** of persons nationally. By province the omission ranged from **10.0% to 18.6%** (Stats SA PES). The level is corrected after the fact. The **regional spread of about ±4 pp** is what would mis-steer a needs allocator.
- **Price and poverty revisions.** The 2005 PPPs added about **400 million** poor. Revised 2011 PPPs added **+20 m (+0.3 pp)**, and 2017 PPPs removed **−46 m (−0.6 pp, about 6%)**. The changes were concentrated in a few countries (India, Nigeria).
- **Data deprivation.** **57 of 155** countries had zero or one poverty estimate in 2002–11 (WB PRWP 7252).
- **Household targeting** errors are much larger than regional errors. Proxy means tests in 9 African countries classify **80%** of poor households as non-poor and **40%** of non-poor as poor. Bolsa Família 2004 had **59%** exclusion and **49%** inclusion error, yet it ranks among the most progressive programmes.
- **Gaps.** No verified figures were found for WHO NHWA completeness or SPI scores by income group.

## 2. Lags
- Poverty data reach users **about 2 years** after collection, on top of multi-year survey intervals (WB).
- Build lead times (IEA): **transmission takes 5–15 years**, **renewables 1–5 years**. These come on top of the data lag.
- The budget-cycle lag of about 1 year is an unsourced assumption.

## 3. Leakage and capture
| setting | leakage | source |
|---|---|---|
| Uganda school grants, 1991–95 | 87% (13% received) | Reinikka & Svensson 2004 |
| Uganda, mid-1990s → 2001 | about 80% → under 20% captured | WB / GSDRC |
| India PDS grain | 54% (2004-05) → 41.7% (2011-12) → 8.8–28% (2022-24) | Drèze & Khera; Ideas for India |
| Brazil audited municipalities | 30% of funds diverted | J-PAL / Avis, Ferraz & Finan |
| Aid to aid-dependent countries (offshore, elites only) | 7.5% | Andersen, Johannesen & Rijkers 2022 |
| EU budget / cohesion irregularity (not fraud) | 5.6% / 9.3% (2023) | European Court of Auditors |

## 4. Strategic misreporting by subnational units
- **China.** Local statistics inflated growth by **1.7 pp/yr** in 2008–16. NBS corrections average **5% of GDP** (Chen et al., BPEA 2019). Liaoning admitted fiscal revenue was exaggerated by **about 20%** in 2011–14, and its GDP was revised down **by more than 20%**.
- **Brazil FPM grants by population bracket.** In 2010, **192 of 3,565** municipalities (5.4%) were misclassified, a misallocation of over US$100 m/yr. Of municipalities near the first threshold, **17–42%** bunch just above it. The over-report is **62–241 persons**, about 0.5–2.4% of population. The pattern has worsened across censuses.
- **Soviet ratchet effect.** Only qualitative evidence was found; no number was verified.

## 5. Safeguards: effect sizes
- **Top-down audits.** Raising the audit probability from 4% to 100% cut missing expenditures by **8 pp** (Olken 2007). Grassroots monitoring had little effect because of free-riding.
- **Random public audits (Brazil).** Corruption fell **7.9%**, or **12.7%** with repeat audits. There were media spillovers of 7.5–10.4%.
- **E-payments / e-invoicing (Bihar).** Spending fell **24%** with no loss of employment, and **19%** after national scale-up. Payment delays rose, so a safeguard can add lag.
- **Information and transparency.** Uganda's newspaper campaign cut capture from about 80% to under 20%. Part of that drop coincided with wider reforms (Hubbard, CGD).
- **Community monitoring (Uganda health).** Under-five mortality fell **33%**.
- **Biometric smartcards, AP.** Leakage fell "significantly"; no magnitude was verified. **E-procurement** improved quality but not price; this comes from a search summary only.

## 6. Large allocators
COVAX promised **2 bn doses in 2021** and had delivered **about 596 m by end-November** (about 30%). The shortfall was in supply, not targeting. That points to a different failure mode: the allocator is only as good as the resources it controls. India's PDS shows that a large allocator can cut leakage by 30–45 pp in about a decade. EU cohesion shows that even high-capacity systems stay above 5% irregularity.

## Proposed parameters (`parameters.json`)
| parameter | low | central | high |
|---|---|---|---|
| needs-measurement error σ (relative, per region) | 0.05 | 0.15 | 0.30 |
| data lag (years) | 1 | 2 | 5 |
| leakage, no safeguards | 0.10 | 0.25 | 0.45 |
| leakage, strong safeguards | 0.03 | 0.08 | 0.15 |
| share of regions misreporting | 0.10 | 0.25 | 0.45 |
| misreport inflation of need | 0.02 | 0.07 | 0.20 |
Supplementary: build lead time is 1–5 years for renewables and 5–15 years for transmission.

**Confidence.** Medium for leakage and lag. Low to medium for σ and misreporting, which are judgement calls anchored on proxies. Most leakage evidence comes from cash and in-kind transfers in low- and middle-income countries, not from building physical capacity. Model the safeguard cost too: about +0.5–1 year of lag (Bihar) and audit spending.

**Suggested tests.** (a) Rerun V6.8 C with the central values. Does C still beat B2 on the year-15 energy and health shortfall closed? (b) Find the break-even leakage at which C equals B2. (c) Check whether a σ of 0.30 combined with misreporting that is correlated with region (the rich-region data advantage) reverses the needs-first gains.
