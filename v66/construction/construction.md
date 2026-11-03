# Residential construction capacity: evidence for years-to-house (v66 §3)

Built 2026-11-03. Files: `evidence.csv` (74 rows, one per value, with a URL and a verification flag) and `capacity.json` (low, central and high values with derivations). A row marked **derived** is arithmetic on cited values, and any assumption it uses is named. A row marked **no** was seen only in a search snippet and should not carry weight.

## 1. How much residential floor area the world builds now

| Scope | Value | Year | Source | Verified |
|---|---|---|---|---|
| World residential stock, **net** increase | **3.4 bn m²/yr** | 2024 | UNEP/GlobalABC GSR 2025-26 (quoted by Gleaner) | yes, secondary press. The primary PDF returns 403 |
| World non-residential, net increase | 1.3 bn m²/yr | 2024 | same | yes, secondary |
| World new floor space, all buildings | 12.7 mn m²/day (4.6 bn/yr) | 2024 | AA summary of GSR | yes, secondary |
| World stock | 273 bn m² (+1.7%) | 2024 | GSR | yes |
| China, developer residential completions | 809 (2014, derived peak), 730 (2021), 724 (2023), **537 (2024)**, **428 (2025)** mn m² | | NBS releases | yes |
| China, all new residential (urban + rural self-build) | **1.975 bn m²** (0.949 urban + 1.026 rural) | 2011 | China Statistical Yearbook 2012, T10-35 | yes |
| USA, completions | about 245 mn m² (1.005 m single-family × 2,142 ft², 0.484 m multifamily × 1,000 ft², medians) | 2025 | Census | derived |
| EU27, residential **permits** | 163 mn m² of useful floor area (236 in 2021) | 2024 | Eurostat sts_cobp_a | yes (API) |
| India, PMAY-G rural | 17.6 m houses completed FY20/21 to FY24/25, minimum 25 m² each, so **at least 88 to 110 mn m²/yr** | 2025 | PIB factsheet | yes, rate derived |

The GSR describes growth as "robust in India and Southeast Asia", while Europe and China have slowed. I found no fetchable regional floor-area split for Africa or South Asia.

## 2. Maximum build rate per capita (m² per 1,000 people per year)

- **China 2011: 1,468.** This is the highest verified rate found. It is computed as 1.975 bn m² divided by 1.345 bn people (World Bank).
- Other current rates: USA 2025 is 720, world 2024 is 418, China developers only 2024 is 381, and EU27 permits 2024 is 362.
- Singapore HDB built 189,299 dwellings in 1981-85, about 14 dwellings per 1,000 people per year. This came from a search snippet only, and the flat size is not verified, so it has no m² conversion.
- Post-war Europe and South Korea were not sourced.

capacity.json uses low 720, central 1,468 and high 1,468. High equals central because no verified observation exceeds China's 2011 rate.

## 3. Labour, materials and carbon per m²

- **Labour:**
  - Finland 2023 precast apartments: 13 h per gross m², range 10 to 20 (RT 2024). Singapore sites produce 0.4 m² per worker-day and Finland 0.8.
  - China 2010 top-down: 15 workers per 1,000 m²/yr, which gives about 33 h/m² if a worker puts in 2,200 h/yr (assumed).
  - India PMAY-G: 201 person-days per house of at least 25 m², which gives 64 h/m² or less if a workday is 8 h (assumed).
  - Values used: **13 / 33 / 64**.
- **Steel:** median 27 kg/m², interquartile range 11 to 59. This is computed from the Heeren & Fishman 2019 open material-intensity database, residential rows (n=431).
- **Concrete:** median 613 kg/m², interquartile range 303 to 974 (n=455).
- **Cement:** 38 / 92 / 166 kg/m². These are derived as concrete multiplied by an assumed cement mass fraction of 12.5%, 15% or 17%. That fraction is not verified.
- **Caveat on materials:** the database sample is mostly European and concrete-framed. Brick and adobe housing in South Asia and Africa is likely lighter in steel and concrete.
- **Embodied carbon:** EU residential life-cycle values range from 400 to 800 kgCO2e/m², with a mean of 600 (Ramboll/AAU/KU Leuven 2022). About two thirds of that is upfront. A cross-check: the GSR's 2.1 GtCO2/yr from cement, steel and aluminium divided by 4.7 bn m² added gives about 450 kgCO2/m².
- **Workforce:** ILO modelled estimates give **294.4 m construction workers in 2024** (8.3% of employment). That includes 91.6 m in Southern Asia, 24.8 m in Africa (15.3 m in Sub-Saharan Africa), 73.1 m in India and 66.0 m in China. These cover all construction, including civil engineering.

## 4. Illustrative years-to-house (global, before any regional split)

| Need | At the current 3.4 bn m²/yr, all of it redirected | At the China-2011 rate applied worldwide (1,468 × 8.14 bn people = 11.9 bn m²/yr) |
|---|---|---|
| Comfortable, 65 bn m² | about 19 yr | about 5.4 yr |
| Decent, 13 bn m² | about 3.8 yr | about 1.1 yr |

These are upper bounds on speed. The need sits in South Asia and Africa, so the binding figure is the regional rate × the regional population, which the v66 model should compute with its own population data. For a 65 bn m² build-out, the central values above imply:

- about 2.1 trillion labour-hours, which is about 3.6 years of the entire world construction workforce at an assumed 2,000 h/yr;
- about 6 Gt of cement;
- about 1.8 Gt of steel;
- about 39 GtCO2e life-cycle emissions, of which about 26 Gt is upfront.

## Gaps and cautions

- The 3.4 bn figure is **net** of demolitions, so gross construction is higher by an amount I could not find.
- The primary GSR PDF and the Deetman/Marinova regional intensities were not fetchable (403 errors and paywalls). Regional material intensities for South Asia and Africa remain unsourced.
- The EU figure counts permits, not completions. The US figure uses median sizes, not means.
- The labour-hours values rest on assumed hours per day and per year, which are labelled where they are used.
