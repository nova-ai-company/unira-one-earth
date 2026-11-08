# UNIRA V7.0 — Housing acceleration and constitutional safeguards

## Part A. Housing: comfortable homes (27 m² per person) for everyone
**Question:** at today's building capacity, comfortable housing for all is only 40–50% done after 30 years (v67). How fast can it be done, and at what cost in workers and CO₂?

**Model:** `housing/run.py` (4 tests). It uses the v67 world transition with UNIRA levers and strong-safeguard leakage (8%, v69):
- building capacity in regions in need grows g% a year, capped at the highest sustained rate ever observed (China 2011: 1.468 m² per person per year);
- stock-first (Article 11) meets part of the shortfall by upgrading and extending existing buildings at a fraction of the materials;
- only floor area actually delivered is counted.

**Evidence** (`evidence/`, 36 sourced rows), central values:
- **Upfront embodied carbon:** 400 kg CO₂e per m² for conventional reinforced-concrete homes (WBCSD/Arup 500–600; EU about 400; Malaysia 406), against 150 for low-carbon homes (bamboo, timber, vaults, low-cement; 30–265). The saving comes from replacing the frame, floors and roof; earth-block walls alone save little.
- **Labour:** 33–64 hours per m² (China 2010; India's rural housing programme PMAY-G).
- **Upgrading:** about 40% of the need could be met by upgrading or extending existing homes (India 2012: 80% of the urban shortage is overcrowding, 17% obsolete houses), using about 40% of the materials of new building (UNEP: 50–75% fewer emissions).
- **Empty homes in regions of need:** about 0.5% of the need (India's 11.1 m vacant urban units). Most empty homes are in China, Japan and the EU, and cannot be moved.

| plan (30 years) | everyone at 27 m² by | gap closed, yr 15 | gap closed, yr 30 | floor built (new + upgraded) | embodied CO₂ | peak construction workers |
|---|---|---|---|---|---|---|
| today's capacity | not within 30 yrs | 15% | 40% | 73 bn m² | 29 Gt | 87 m |
| +5%/yr | year 27 | 39% | 100% | 109 bn m² | 43 Gt | 253 m |
| +10%/yr | year 27 | 70% | 100% | 109 bn m² | 43 Gt | 253 m |
| +10%/yr, stock-first | year 27 | 83% | 100% | 100 + 9 bn m² | 41 Gt | 265 m |
| **+10%/yr, stock-first, low-carbon** | **year 27** | **83%** | **100%** | 100 + 9 bn m² | **16 Gt** | 265 m |
| +5%/yr, stock-first, low-carbon | year 27 | 54% | 100% | 98 + 11 bn m² | 15 Gt | 236 m |

The remaining 1.5 °C carbon budget is 130 Gt from 2025 (50% chance); 2 °C is 1,050 Gt.

**Findings**
1. **Comfortable homes for everyone within about 27 years are possible** if building capacity in regions of need grows 5–10% a year. That peaks at about 6–7 bn m² a year, at China's past rate per person. About 109 bn m² must be built or upgraded in total (65 bn backlog plus about 40 bn for population growth).
2. **Low-carbon construction is essential.** Conventional concrete homes would use about a third of the remaining 1.5 °C budget (43 Gt). Low-carbon frames cut this to about 16 Gt, roughly 12%.
3. **Stock-first speeds the early years:** 83% vs 70% of the gap closed by year 15. It cannot replace building, because most of the need is missing space.
4. **The binding limit is people.** The peak needs 240–265 m construction workers at 48 h per m². The world has 294 m, of whom only about 116 m are in South Asia and Africa. Universal work (rule 14) and training make this feasible, but it is a large workforce programme.

**Limitations:**
- Labour per m² for self-built housing was not found.
- There are no whole-house carbon assessments for African or Indian concrete homes.
- Upgradable share and material ratio are partly judgement.
- Construction capacity is treated globally, not region by region.

**Levers "out of the box" (author, 2026-11-08; `housing/run_levers.py`, +8 tests, `outputs/housing_levers.json`).** The author asked for ways to build homes at low cost and fast. On the published +10%/yr, stock-first, low-carbon case:

| Lever | Gap closed, yr 15 | Peak build, bn m²/yr | Peak workers (professional), m |
|---|---|---|---|
| Published case | 83% | 7.1 | 265 |
| Factory building, 20% / 35% fewer hours per m² (McKinsey: 20–50% faster, up to 20% cheaper; secondary source verified; mapping to labour synthetic) | 83% | 7.1 | 212 / 172 |
| Households build half / 65% of the extension above 15 m² (mutual self-help practice, reported) | 83% | 7.1 | 179 / 152 (+1,700 / 2,200 bn household hours over 30 years, about 11–14 h per person per year in the regions concerned) |
| Decent core (15 m²) for everyone first, designed for extension | 94% of the decent gap | 3.5 | 130 |
| Capacity +15%/yr | 96% | 7.2 | 269 |
| +15%/yr and build rate 1.5× the China 2011 record (synthetic) | 97% | 10.4 | 388 |
| All: factory 20%, half of the extension self-built, +15%/yr, 1.5× record | 97% | 10.4 | 311 (209) |

- **Cost does not set the date; capacity growth and the record build rate do.** The year in which the last region reaches 27 m² stays at 27 in every case because it is driven by population growth in the fastest-growing regions, which the model follows to 2050; the share of the gap closed by year 15 is the sensitive measure.
- **The levers act on the binding limit, people:** factory building and household-built extensions cut the professional workforce at the peak from 265 m toward 150–210 m, against 116 m construction workers in South Asia and Africa today. A decent core first halves the early build rate and workforce.
- **Planned cores do grow:** sites-and-services neighbourhoods in seven Tanzanian cities developed better housing than control areas over 30–40 years (more storeys, water, electricity, sanitation; verified abstract), while upgrading areas did not. The known failure is a core that is never extended, hence a deadline in the proposed text.
- **Empty and under-occupied homes are in the wrong places:** Japan 9.0 m vacant (13.8%, 2023, reported), 33.3% of EU residents in under-occupied homes (2023, verified), India 11.1 m urban vacant units (about 0.5% of the need). They matter for Article 18.9 and T-2 in rich regions, not for the world gap.
- **3D printing:** no independently audited whole-project cost or schedule figures; not used.
- **Limits:** labour hours per m² of self-built extensions unknown (set equal to professional hours); self-build needs tenure, supervision and materials logistics; one world capacity, no regional trade or cement bottlenecks; the 1.5× record case has no observational support. Constitution text proposed in `concept/PROPOSED_CONSTITUTION_CHANGES_2026-11-08.md` (not yet approved).

## Part B. Constitutional safeguards
`constitution/SAFEGUARD_ARTICLES.md` turns the V6.9 results into draft Articles 13–20:
- 13 Public Allocation Register;
- 14 Independent Audit Authority;
- 15 Direct Digital Delivery and Physical Verification;
- 16 Timely and Honest Needs Data;
- 17 Community Monitoring and Whistleblower Protection;
- 18 Anti-Capture Rules for Officials;
- 19 Correction Without Punishing People;
- 20 Built-in Falsification Clause.

Each article has its evidence and a measurable trigger. For example, leakage above 25%, or data older than 2 years, forces a review; leakage above 45% for 3 years requires a democratic change of the allocation system. They are drafts for the author's decision.
