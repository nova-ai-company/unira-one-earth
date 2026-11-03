# UNIRA V6.2 — Source verification audit

Retrieved 2026-11-03 (about 11:43–11:47 UTC) with curl and a browser User-Agent. Raw copies of every fetched page, PDF, xlsx and ods are in `source_cache/`. The row-level results, with exact quotes and table IDs, are in `source_verification.csv`.

## Result
**No recorded value is contradicted.** Every indicator in the scope was found at its source with exact digits. Of the 23 rows, 16 are CONFIRMED and 7 are CONFIRMED_WITH_CAVEAT. Nothing was UNREACHABLE. One URL used only in v53 (`nyc.gov/content/tenantprotection/.../fast-facts-about-housing-in-nyc`) returns only the JavaScript page shell, so no figures could be seen there. The NYC values are confirmed from the HPD PDF instead.

## France labour (V6.2 inputs): all CONFIRMED
| Item | Source value | Population / scope |
|---|---|---|
| Employed persons, end-2025 | 30,5 M in the text; Figure 1 total **30 483 k** (26 965 k employees + 3 518 k self-employed) | France excluding Mayotte. Estimations d'emploi, **provisional** 2025 figure |
| Annual effective hours, full-time employees 2025 | **1 656 h** | Full-time employees aged 15+, France excluding Mayotte, Enquête Emploi 2025 |
| Usual weekly hours, full-time employees 2025 | **38,9 h** | same |
| Annual effective hours, part-time employees 2025 | **966 h** (23,2 h usual weekly; 168 days) | ECRT 2026, "Durée du travail" fiche, Figure 2 |
| Annual effective hours, self-employed ("indépendants") 2025 | **1 903 h** (41,3 h weekly; 241 days) | Figure 2 |
| Annual hours, all employees or all workers | **Not published** on the page or in ECRT2026_F17.xlsx | — |
| Part-time share 2025 | **17,6 %** of employees excluding apprentices (4,3 M); **17,7 %** of all employed (ILO definition) | "Temps partiel" fiche (8733075), Figure 1 |

Source pages: insee.fr/fr/statistiques/8733039, 8733071 and 8733075 (Insee Références *Emploi, chômage, revenus du travail*, 2026 edition, published 02/07/2026).

Model caveats:
- The employment count (an administrative year-end stock) and the hours figures (from the household survey) cover different populations.
- Any weighted all-worker hours figure built from 1 656 / 966 / 1 903 and the part-time share is MODEL_DERIVED. INSEE does not publish it.

## Caveats that matter
- **GDP €2 822,5 bn** comes from the first estimate (Insee Première 1997, May 2024). Later vintages of the annual accounts probably revise it. This audit did not check them.
- **Paris vacant dwellings, 136 957** is correct for the 2022 census. The 2023 census gives **139 075** (Dossier complet, published 27/08/2026).
- **London 2024 count, 93 602** does not appear on the GLA page or in the press release. It appears only in MHCLG Live Table 615 (All_vacants, London, 2024). Cite that table.
- **London 2025 count, 105 138** is a council-tax measure taken on 6 Oct 2025. It includes 23 326 homes exempt from council tax. The same GLA page gives two long-term-empty figures: 47 287 (Table 615) and 47 864 (Council Taxbase).
- **London overcrowding, 6,7 %** is a three-year rolling average to 2023-24, using the bedroom standard. The GLA says it is probably an underestimate.
- **Tokyo**: all three components UNIRA records are exact, but a fourth category is missing: second homes ("二次的住宅"), **9 600**. The four categories sum to 896 600, against a total of 896 500 (rounding).
- **England £7 480** is a modelled cost to reach energy band C. It covers only the 42 % of homes that can be improved to C. It is not a renovation cost. The median (£8 648) is higher than the mean.
- **RTE**: the generation figure is described as "en France". RTE states the metropolitan scope only for the consumption figure.
- The INSEE "Dossier complet" pages (Paris overcrowding 28,2 / 2,6; Vallauris) are updated in place. The URLs will show different years after the next census release, so archive the cached copies.

Not audited because they were outside the requested list: the MaPrimeRénov' works-cost figure and England overcrowding (3,0 %).
