# EVIDENCE REGISTER — PRIMARY SOURCES AND VERIFICATION TASKS

The source URLs below are starting points recorded in previous research, **not a fresh audit**. Validate exact table, publication date, denominator, geographic scope, and archive copies before publication. Each historical version's `sources.csv`, `evidence.csv` or `RESEARCH_NOTE.md` may contain more detail.

| Topic | Recorded indicator | Primary source entry point | Major caveat |
|---|---|---|---|
| France employment/hours | 30.5m employed end-2025; 1,656 annual full-time hours 2025 | https://www.insee.fr/fr/statistiques/8733039?sommaire=8733125 | Different populations; no aggregate all-worker hours |
| France electricity 2023 | 494.7 TWh generation; 445.7 TWh weather-adjusted consumption | https://analysesetdonnees.rte-france.com/bilan-electrique-2023/synthese | Different definitions; no inferred spare supply |
| France GDP 2023 | €2,822.5bn | https://www.insee.fr/fr/statistiques/8193933?sommaire=8068749 | Nominal market accounts not physical output |
| Paris housing | 2022 vacant 136,957 | https://www.insee.fr/fr/statistiques/8581193?geo=DEP-75 | Municipality/departement vs metro boundaries |
| Paris overcrowding | 2023 municipality moderate 28.2%, severe 2.6% (previously reported) | https://www.insee.fr/fr/statistiques/2011101?geo=COM-75056 | Verify exact table and denominator |
| London empty homes | 2025 count 105,138 | https://www.london.gov.uk/who-we-are/what-london-assembly-does/london-assembly-research-unit-publications/empty-homes-london | Council-tax based; not NYC vacancy equivalent |
| London overcrowding | 2023–24 ~6.7% households | https://www.london.gov.uk/sites/default/files/2026-01/Housing%20in%20London%202025%20report%20%28002%29.pdf | Definition differs from INSEE |
| NYC rental vacancy | 2023 1.41%, 33,210 units available | https://www.nyc.gov/assets/hpd/downloads/pdfs/about/2023-nychvs-selected-initial-findings.pdf | Available rentals, not all vacant homes |
| Tokyo vacancy | 2023 ~896,500 | https://www.juutakuseisaku.metro.tokyo.lg.jp/documents/d/juutakuseisaku/jyuuseishinkikakubukai_tokyonojutakujijo_260424 | Verify Tokyo boundary and component counts |
| England retrofit | 2024–25 EHS energy ratings, £7,480 upgrade reference | https://www.gov.uk/government/statistics/chapters-for-english-housing-survey-2024-to-2025-headline-findings-on-housing-quality-and-energy-efficiency | England-wide; energy measure ≠ full renovation |
| France residential renovations | average supported works figures | https://www.statistiques.developpement-durable.gouv.fr/tableau-de-suivi-de-la-renovation-energetique-dans-le-secteur-residentiel | Support-program sample selection |
| Vallauris housing | 2023 20,728 dwellings; 1,244 vacant | https://www.insee.fr/fr/statistiques/2011101?geo=COM-06155 | Pilot only; not main megacity case |
| Japan national housing | 2023 ~9m vacant, 13.8% | https://www.stat.go.jp/english/info/news/20241030.html | National, NOT Tokyo-specific |

## Data rules
- Dataset schema: `indicator_id, value, unit, year, observation_date, publication_date, geography_id, geography_definition, population_definition, method, source_url, source_table, source_version, retrieved_at, uncertainty, evidence_class, license`.
- Evidence classes: **VERIFIED_OFFICIAL**, **REPORTED_NEEDS_RECHECK**, **MODEL_DERIVED**, **SYNTHETIC_ASSUMPTION**, **NORMATIVE_TARGET**, **MISSING**. Do not use VERIFIED_OFFICIAL without a source-table audit.
- Never compare vacant dwellings to available rentals, all employed people to full-time annual hours, or production to adjusted consumption without reconciliation.
- Do not convert U to euros arbitrarily. If financial conversion is necessary, estimate price vectors/endogenous purchasing power and identify numeraire.
- Cairo is an explicit missing-data task; use CAPMAS/Greater Cairo definitions and explain any boundary mismatch.
- Environmental coefficients require lifecycle system boundaries, electricity mixes, year, material composition, transport, maintenance, replacement and uncertainty.
