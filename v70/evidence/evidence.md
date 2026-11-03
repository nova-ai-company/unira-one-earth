# Stock-first housing (Article 11): evidence review

Built 2026-11-03. Files in this folder:

- `evidence.csv` has 36 rows. Each row records whether its value was found in the fetched source text.
- `parameters.json` holds low, central and high values for each parameter, with its basis.

Rows marked "via v66" reuse values from `v66/construction/evidence.csv`, which were verified in that run. A row marked **no** was seen only in a search snippet and should not carry weight. Global CO2 budgets are not covered here; they stay in `v66/ecology/constraints.json`.

## 1. Embodied carbon, upfront (kgCO2e per m² of floor area)

| Typology | Value | Source | Verified |
|---|---|---|---|
| Conventional, WBCSD/Arup case studies (A1–A5 average) | 500–600 | WBCSD/Arup 2021 | yes |
| EU residential, life-cycle mean (about 2/3 upfront, so about 400 upfront) | 600 (range 400–800) | Ramboll/AAU/KU Leuven 2022 | yes (v66) |
| Malaysia, RC frame with fired brick (A1–A3) | 406 | Asman 2020 | yes |
| Malaysia, interlocking compressed earth bricks, same building | 265 (−35%) | Asman 2020 | yes |
| Bamboo buildings vs concrete or brick buildings | 30 vs 240 | Escamilla 2018, cited in Tello-Ayala 2023 | yes (secondary) |
| Ecuador/Colombia two-storey social house: bahareque (Guadua bamboo) structure vs RC frame | 27% of the RC frame's emissions; 36% cheaper | Tello-Ayala 2023 | yes |
| Colombia: bamboo house vs brick house | about 107 vs about 298 | MDPI 2023 | no |
| South Africa sandbag house | 174–189 | Saint 2023 | no |

**Walls alone barely move the total.** Results per m² of wall (not of floor area):

| Wall type | kgCO2e per m² of wall | Boundary | Source |
|---|---|---|---|
| Kenya, compressed earth blocks, 5% cement | 18–27 | A1–A5 | TNO 2025 |
| Kenya, compressed earth blocks, 10% cement | 33–40 | A1–A5 | TNO 2025 |
| Kenya, machine-cut stone | 40 | A1–A5 | TNO 2025 |
| Nepal, compressed stabilised earth blocks | about 20–29 (derived) | cradle to site | Max Fordham 2021 |

By weight, the Nepal blocks emit 75–78% less than fired brick. In Kenya, cement accounts for 83–91% of the blocks' footprint, and at 10% cement the blocks are no better than stone.

**Implication:** large savings come from replacing the RC frame, slab and roof with bamboo, timber or low-cement alternatives, not from changing the blocks. I found no verified whole-house LCA of an Indian or sub-Saharan African RC-frame house.

**Parameters:**
- Conventional: 250 / 400 / 600 kgCO2e/m².
- Low-carbon: 30 / 150 / 265 kgCO2e/m². The central value of 150 is a judgment.

## 2. Labour (hours per m²)

- No verified per-m² labour figure for owner-built or Habitat-style housing was found. This is a gap.
- PMAY-G rural houses in India take 201 person-days per house, with a minimum size of 25 m². At an assumed 8-hour day, that is 64 h/m² or less.
- A top-down estimate for China in 2010 gives 33 h/m² (derived, using an assumed 2,200 working hours a year).
- For comparison, industrialised precast housing in Finland takes 13 h/m².
- Earth and other alternative materials are reported to be more labour-intensive than conventional ones.
- **Parameters:** 33 / 48 / 64 h/m². The central value is the midpoint.

## 3. Vacant stock

| Region | Vacant | Source | Verified |
|---|---|---|---|
| India, urban (2011) | 11.09 m units, about 12% of urban stock (19% in Gujarat) | CSEP, from Census 2011 | yes |
| China, urban (2017) | 21.4%, about 65 m units | Gan Li, NBER 26585 | yes |
| Japan (2023) | 9.00 m dwellings, 13.8% | Statistics Bureau of Japan | yes |
| EU27 (2021) | 46.6 m of 236.0 m conventional dwellings unoccupied (19.7%, including second homes) | Eurostat API | yes |
| Africa | not found | — | gap |

India's vacant urban units equal 59% of its 2012 urban shortage when counted in units. At an assumed 30 m² each, they hold only about 0.33 bn m², about 0.5% of the 65 bn m² need.

The large vacant stocks are in China, Japan and the EU, and homes cannot be moved between regions. **Parameter:** 0 / 0.005 / 0.02 of the need.

## 4. Upgrading and renovation vs new build

- **Emissions:** UNEP (2023) says repurposing an existing building emits 50–75% less than new construction, a ratio of 0.25–0.5 (verified through a secondary summary).
- **Cost:** in Chile, upgrading a slum in place costs about 2/3 as much per household as relocating its residents, and only upgrading in place produced lasting gains in housing quality (NBER 34560, verified).
- **India's 2012 urban shortage of 18.78 m units** (TG-12, verified) breaks down as:
  - congestion: 14.99 m (79.8%), which calls for added floor area that could partly be built as extensions in place;
  - obsolescent or non-serviceable katcha houses: 3.26 m (17.4%), which could be upgraded or replaced;
  - homeless: 0.53 m.
- I found no global UN-Habitat figure for the share of slums that can be upgraded in place.
- **Parameters:**
  - Share of need met by upgrading: 0.17 / 0.4 / 0.8. The central value is a judgment.
  - Material ratio of upgrading vs new build: 0.25 / 0.4 / 0.67.

## 5. Maximum sustained build-out

- **China, 2011:** 1,468 m² per 1,000 people per year (v66), the highest verified rate.
- **Korea, 1990:** 750,378 dwellings were built, against a population of 42.87 m. That is 17.5 dwellings per 1,000 people, or about 1,050–1,490 m² per 1,000 if each dwelling is 60–85 m² (unit size assumed). After 1990 the rate settled at about 600,000 units a year.
- **Post-war Europe:** not sourced.
- **Parameters:** 720 / 1,468 / 1,500 m² per 1,000 people per year.
- **Workforce:** ILO counts 294 m construction workers in 2024, including 91.6 m in Southern Asia and 24.8 m in Africa (v66).

## What this means for Article 11

Reusing vacant homes and renovating existing ones are worthwhile within a region, and renovation cuts emissions by 50–75% per m² dealt with. But almost all of the floor-area deficit in South Asia and Africa is a shortage of space (congestion and population growth), not homes standing empty. Most of the 65 bn m² therefore has to be built, and the main lever on its carbon is the choice of structure: bamboo, timber or low-cement in place of an RC frame. That choice cuts upfront carbon by about 3–8 times.
