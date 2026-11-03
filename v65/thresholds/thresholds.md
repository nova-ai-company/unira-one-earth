# UNIRA v65: per-person needs thresholds (decent vs comfortable)

Date: 2026-11-03. Machine-readable version with full citations: `thresholds.csv` (same folder).
Verification rule: "yes" means the exact number was read in fetched source text (PDF, HTML or data CSV). "partial" means the inputs were verified and the per-capita value was derived here. "no" means only a search snippet or a secondary citation was seen. No values were invented. Unverified items are listed in their own section.

## Summary table

| Domain | Decent (minimum dignified) | Comfortable (reference) | Confidence |
|---|---|---|---|
| Food intake | 2,000–2,150 kcal/cap/day (Millward-Hopkins et al. 2020, Table 2); FAO world MDER floor 1,836 kcal (2024) | about 2,300–2,470 kcal (MH2020 Higher Demand +15%, derived) | High (decent); medium (comfortable) |
| Food supply incl. waste | about 2,590 kcal/cap/day at food-balance level for 2,100 kcal eaten, if 19% consumer waste (derived) | current world supply 3,006 kcal (2023) | Medium: the waste share was not fetched |
| Protein | 0.83 g/kg/day safe level (WHO TRS 935), about 50–55 g/day for an adult (derived) | world supply 92 g/cap/day (2023) | High |
| Energy (FINAL) | 15.3 GJ/cap/yr (MH2020; country range 13–18.4); about 17 (Kikstra 2021; range 9–36) | 24 (HD) to about 40 (HD+LAT) GJ/cap/yr (MH2020); 73 UK "good life" footprint (McElroy & O'Neill 2025) | High |
| Energy, EU today | — | about 81.7 GJ/cap final (derived); 124 GJ/cap gross available (Eurostat 2024) | High |
| Housing | 30 m² per household + 10 m² per person above 3, i.e. about 10 m²/cap (Rao & Min 2018); 15 m²/cap incl. shared space (MH2020) | about 27 m²/cap (MH HD, derived); Germany 49.5 m²/cap (2025); EU states range 19–64 | High |
| Health workforce | 44.5 doctors+nurses+midwives per 10,000 (WHO 2016); 1.5–1.7 physicians per 1,000 (Rao & Min) | about 131 per 10,000 (EU, derived from Eurostat counts); OECD 3.9 doctors + 9.2 nurses per 1,000 (not fetched) | High (decent); medium (comfortable) |
| Education | 9 years of schooling (Rao & Min) | 12 years; 14.3 pupils per teacher in primary (high-income countries 2024) vs 25.7 world | High (ratios); medium (12 years) |
| Mobility | 5,000–15,000 pkm/cap/yr (MH2020); 23.4 pkm/day, about 8,540 per year (Kikstra 2021) | EU car-only 6,200–13,000 km/cap/yr (ODYSSEE 2022); total EU pkm not verified | Medium |
| Water (domestic) | 20 L/day basic floor (WHO 2020); 50 L/day DLS (Rao & Min; MH2020) | about 100 L (MH HD +100%, derived); 155 L observed with piped water inside the home (WHO 2020) | High (decent); low–medium (comfortable) |

## Caveats

1. **Decent is not comfortable.** The DLS literature defines a material floor. Rao & Min call their values thresholds that "should be decided at a local level". UNIRA's "comfortable, not castles" target sits between the DLS values and current high-income averages. The "comfortable" figures above are references (the HD scenario, the EU or Germany, the OECD), not normative findings. Choosing a value is a design decision UNIRA must make explicitly. A defensible band is MH2020 HD/HD-LAT (24–40 GJ final; about 27 m²/cap; 3-person households).
2. **The WHO 44.5 is a low bar.** It matches the *median* (25%) attainment of 12 SDG tracer indicators (WHO 2016, Annex 1). It is a shortage threshold, not a comfortable level. EU and OECD densities are about 3 times higher.
3. **Climate and age adjustments.** Food needs vary with age, sex, body size and activity (MDER is a sedentary-level cut-off). Energy for thermal comfort and water heating depends on heating and cooling degree-days. In MH2020, climate and demographics drive the 13–18.4 GJ country spread, and Kikstra finds about 9 GJ (South Asia) to about 36 GJ (North America). Water needs rise in hot climates and for strenuous work. School and health floor space scale with the age structure.
4. **Final vs primary energy.** All DLE values (MH2020, Kikstra, Rao 2019, Grubler LED) are *final* energy. Comparing them with world *primary* supply requires a conversion. The EU in 2024 had final energy / gross available energy = 36,755 / 55,790 PJ, about 0.66 (derived), so primary is about 1.5 times final. A highly electrified renewable system has a much smaller gap, because renewables are counted at their direct output. Never compare 15 GJ final with about 80 GJ/cap of world primary energy without stating the conversion.
5. **Footprints vs bottom-up values.** McElroy & O'Neill's 35 and 73 GJ are consumption-based MRIO footprints that include supply chains under current technology. MH2020 is a bottom-up model with best available technology. These numbers are not interchangeable.
6. **Food losses.** UNEP's 19% (consumer stages) and FAO's 13% (post-harvest to retail) apply at different stages. FAO food-balance supply already sits after most supply-chain losses, so apply only consumer-stage waste when you compare with dietary energy supply. Both percentages were seen only in search-result quotes, not in fetched text.
7. **Construction labour.** No per-m² labour coefficient was found in the fetched sources. The material and energy intensities found were 2–4 GJ/m² embodied energy for housing, 14–23 GJ/m² for hospitals and 4.5–7.5 GJ/m² for schools (MH2020 Table 2). For labour, McElroy & O'Neill (MRIO) give total labour footprints: a 17.5–18 h working week for decent living and 45.5–46 h for the "good life" (UK).

## Unverified / to check

- FAO world *average* dietary energy requirement (ADER, often quoted as 2,100–2,400 kcal): no fetched value.
- OECD Health at a Glance 2025 averages (3.9 doctors, 9.2 nurses per 1,000): OECD returned HTTP 403, so these come from search snippets only.
- UNEP Food Waste Index 2024 (19%, 1.05 Gt) and FAO 13% loss: search-snippet quotes only.
- Rao, Min & Mastrucci 2019 (Nature Energy) range: not fetched. Secondary sources disagree (12–24 vs 11–24 GJ/cap).
- Grubler et al. 2018 LED (245 EJ final in 2050): only quoted in MH2020; the per-capita value was not stated.
- Total EU passenger-km per capita (all modes): not found. Only car km was verified.
- SDG 4.1 wording (12 years): not fetched.
