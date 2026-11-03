# v68 source verification for WORKING_PAPER_02 (v67)

Retrieved 2026-11-03. Machine-readable table: `verification.csv`. Parameters for items 7–11: `parameters.json`.
Source copies (text extracts used as data only) are in `source_cache/`.

## A. Figures used in the paper

| # | Claim | Status | Verified value |
|---|---|---|---|
| 1a | Military 5.5% of global GHG incl. supply chains | CONFIRMED | 2,750 MtCO2e = 5.5%. Range 3.3–7.0%. Operational emissions alone: 1.0%. Source: SGR/CEOBS 2022, p.4, p.10, p.12 |
| 1b | Military energy use (EJ/yr) | NOT_FOUND | No primary global estimate exists. The "military energy freed" scenario is a model assumption |
| 2a | 19% of food available to consumers wasted | CONFIRMED | 19%, 1.05 bn t in 2022. Source: UNEP FWI 2024, read through UN News because the UNEP PDF is behind Cloudflare |
| 2b | ~13% supply-chain loss | CONFIRMED | 13.3% in 2023 (13.0% in 2015). Source: FAO SDG 12.3.1a portal. Cite this rather than SOFA 2019 |
| 3a | IFSI nursing 3 years | CONFIRMED_WITH_CAVEAT | Still 6 semesters / 180 ECTS. The new arrêté of 20 Feb 2026 (from Sept 2026) sets 4,620 h, up from 4,200 h |
| 3b | GP minimum 10 years | CONFIRMED_WITH_CAVEAT | DES MG went from 3 to 4 years for interns entering in 2023 (AN question 108). The first 4th-year placements start in Nov 2026. 6 + 4 = 10 |
| 3c | Aide-soignant duration | CONFIRMED_WITH_CAVEAT | 1,540 h (770 theory + 770 placement), about 44 weeks / 11 months. Source: arrêté 10 Jun 2021, via an IFAS programme |
| 4a | World nursing graduates | CONFIRMED_WITH_CAVEAT | WHO SOWN 2025 (Table 6.1, p.72): 25.3 graduates per 100k population. No absolute total is published. ~2.0 M/yr is our own arithmetic only |
| 4b | World medical graduates | NOT_FOUND | No WHO global total. Keep the OECD-ratio estimate labelled as an estimate |
| 5 | 669 GW = 510 solar + 159 wind (2025) | CONFIRMED | IRENA RCS 2026, p.3. All renewables added 692 GW |
| 6 | ~3.4 bn m² residential per year | CONFIRMED_WITH_CAVEAT | +3.4 bn m² is the **net** residential stock increase in 2024, from the GSR **2025–2026** edition (p.15, p.31). It is not gross construction |

## B. Counterfactual evidence

| # | Indicator | Status | Value |
|---|---|---|---|
| 7 | Clean-energy investment to EMDE excl. China | CONFIRMED_WITH_CAVEAT | About 20% (2026e), derived as EMDE 50% minus China 30% (IEA WEI 2026, p.202–203). These countries hold about two-thirds of world population. Africa: 2% (WEI 2025 p.9, WEI 2026 pie) |
| 8 | ODA ~0.33% of GNI; 0.7% target | CONTRADICTED (outdated) | 2025 preliminary: USD 174.3 bn = **0.26%** of DAC GNI, down from 0.34% in 2024 (−23.1% real). Only NO, LU, SE and DK exceed 0.7%. The OECD page is blocked, so this was read through the Greek MFA (Hellenic Aid) |
| 9 | World military expenditure | CONFIRMED | USD 2,887 bn in 2025 = **2.5%** of world GDP. Source: SIPRI Fact Sheet Apr 2026 |
| 10 | Top 20–64 employment rates | CONFIRMED_WITH_CAVEAT | 2025: IS 85.8, **MT 83.6**, NL 83.4, CZ 82.9, CH 82.4 (EU27 76.1, FR 75.4). Malta belongs in the list. Source: Eurostat lfsi_emp_a |
| 11 | New residential construction by income group | NOT_FOUND | The GSR 2025–2026 (p.31) says such estimates "are lacking". Only fragments exist: China 7.3 bn m² of new construction in 2024 (gross, all buildings), SE Asia ~1.6 bn m² in 2025 |

## Required paper edits
- Section 3 / climate: keep "5.5% of global emissions (range 3.3–7.0%)". This share is **emissions incl. supply chains**, not energy. Do not convert it to EJ without stating that as an assumption.
- Update ODA from 0.33% to 0.26% (2025 preliminary).
- The 3.4 bn m² is a net stock increase from the GSR 2025–2026 edition. Cite it that way.
- Add Malta to the list of top employment rates.
- The nursing hours changed with the 2026 reform (4,620 h). The duration is still 3 years.

## Access limitations
The following could not be opened directly by curl or WebFetch: OECD.org (403), UNEP.org and wedocs (Cloudflare), and Légifrance (JS shell). For each one, the value was read from an official copy or an official reproduction, as named in the csv.
