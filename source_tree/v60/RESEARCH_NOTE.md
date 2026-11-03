# UNIRA V6.0 — First empirical anchor: France electricity (2023)

## Status and scope
This is a deliberately narrow, source-linked **empirical anchor** and reproducible **stress-test scaffold**, **not** an empirical six-sector calibration, an energy dispatch model, or evidence of UNIRA viability. It replaces fictional baseline electricity numbers with a published reference. Its simulated percentage shocks are assumptions, not predictions.

## Verified observations
- RTE reported about **494.7 TWh** of electricity generated in metropolitan France in 2023.
- RTE's **445.7 TWh** demand figure is adjusted for weather and calendar. **It is not the corresponding unadjusted physical demand. Never subtract it from 494.7 TWh to claim a surplus.** Accounting for imports/exports, pumping, network losses and actual load is required.
- RTE reported approximately **32.6 TWh** of fossil-fired electricity generation.
- INSEE reported **€2,822.5 billion** nominal GDP in 2023, as published in the cited 2023 national-accounts release; it is **not** UNIRA output in U.

## Model
Both generation and weather-adjusted consumption are **independently normalised to index 100** in their own baseline. They are *not* set equal in TWh. The model shows index-level stress to each distinct series under assumed percentage changes. `index_gap` is only the difference between two normalised indices, **not** an electricity shortfall or surplus.

## Comparison design for later empirical testing
A. Current economy; B. reformed current economy; C. UNIRA. All must share initial housing, workforce, capital stock, material supply and energy resources. Do not assume productivity or efficiency advantages for C. Explicitly model implementation cost and governance capacity.

## Data still required for V6.1
- France 2023 employment by sector and actual annual hours, with source and scope alignment.
- Harmonised 2023 energy balance: actual load, generation, imports, exports, losses and storage.
- Material flows and industry production volumes (tonnes, not euro sales).
- Agriculture food output, edible availability, losses and nutritional requirements.
- Housing quality/overcrowding and health service capacity, with definitions.
- Input-output technical coefficients, capital depreciation and investment-to-capacity relationships.
- Public accounts, firm accounts and explicit money issuance to test purchasing power and 30-hour workweek.

## Falsification criteria
UNIRA fails a scenario if required essential goods/services cannot be delivered within material, labour, capital, energy, ecological and rights constraints, or if its monetary closure cannot fund obligations without destabilising purchasing power. Report shortages and uncertainties rather than suppressing them.

## Sources
1. RTE 2023 summary: https://analysesetdonnees.rte-france.com/bilan-electrique-2023/synthese
2. RTE 2023 consumption: https://analysesetdonnees.rte-france.com/bilan-electrique-2023/consommation
3. RTE 2023 generation: https://analysesetdonnees.rte-france.com/bilan-electrique-2023/production
4. INSEE 2023 national accounts: https://www.insee.fr/fr/statistiques/8193933?sommaire=8068749
