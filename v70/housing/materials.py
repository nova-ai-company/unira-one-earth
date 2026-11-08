"""UNIRA V7.0 — can other materials do better than cement and steel? (author's question, 2026-11-08)

Six building systems are described per m2 of floor area (cement, steel, wood, bamboo, earth, embodied CO2, labour),
and mixes of them are tested against the housing programme's peak (7.1 bn m2 a year, v70) and 30-year total
(about 109 bn m2) for: cement and steel against world output; wood against industrial roundwood and plantation
forest area; bamboo against yield and area; embodied CO2 against the remaining 1.5 C budget; labour against the
workforce. Where a figure could be read in its source it is marked VERIFIED; others are REPORTED or ASSUMPTION.
The answer is a map, not a material: bamboo where it grows, earth where it is dry, timber where forests are managed,
low-clinker (LC3) cement everywhere concrete is still needed, and clinker and steel kept for height and bad ground.
Run after run.py:  python3 materials.py  ->  ../outputs/housing_materials.json
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
U = ROOT.parents[1]
sys.path[:0] = [str(U / "v68" / "counterfactual"), str(U / "v67"), str(U / "v66" / "model")]
import compare  # noqa: E402

BASE_CASE = "ramp_10pct_stock_first_low_carbon"
TARGET_M2 = 27.0
CEMENT_IN_CONCRETE = 0.125  # ASSUMPTION: about 300 kg cement per m3 of 2,400 kg concrete
CONV_CEMENT = 54.3 + CEMENT_IN_CONCRETE * 613.0  # kg/m2: Heeren & Fishman residential medians (VERIFIED computation) + cement in concrete

SYSTEMS = {  # per m2 of floor area; "where" is the climate / density the system suits
    "rc_conventional": {
        "label": "Reinforced concrete frame, fired brick or block infill (today's standard)",
        "cement_kg": CONV_CEMENT, "steel_kg": 26.7, "wood_m3": 41.6 / 500, "bamboo_kg": 0.0, "earth_t": 0.0,
        "co2_kg": 400, "labour_h": 48, "storeys": "any", "where": "everywhere today",
        "basis": "materials: Heeren & Fishman 2019 medians (VERIFIED); CO2 400 and labour 48: v70 central values"},
    "rc_lc3": {
        "label": "Same building with LC3 limestone calcined clay cement",
        "cement_kg": CONV_CEMENT, "steel_kg": 26.7, "wood_m3": 41.6 / 500, "bamboo_kg": 0.0, "earth_t": 0.0,
        "co2_kg": 400 - 0.40 * CONV_CEMENT * 0.6, "labour_h": 48, "storeys": "any", "where": "everywhere concrete is still needed",
        "basis": "LC3 cuts cement CO2 by up to 40% using abundant low-grade clays in existing plants (lc3.ch, VERIFIED); "
                 "0.6 kg CO2 per kg of ordinary cement (REPORTED); only the cement share of the building's CO2 changes"},
    "timber_frame": {
        "label": "Light timber frame, 1-3 storeys",
        "cement_kg": 30.0, "steel_kg": 5.0, "wood_m3": 0.18, "bamboo_kg": 0.0, "earth_t": 0.0,
        "co2_kg": 150, "labour_h": 35, "storeys": "1-3", "where": "temperate and boreal forest regions; tropical where forests are managed",
        "basis": "wood 0.16-0.22 m3/m2 for timber-frame homes incl. insulation and cladding (REPORTED); cement for foundations and "
                 "steel for fasteners ASSUMPTION; CO2 150 = v70 low-carbon central; labour between the Finnish precast benchmark "
                 "(13) and site-built (48), ASSUMPTION"},
    "clt_midrise": {
        "label": "Cross-laminated timber, 4-8 storeys",
        "cement_kg": 45.0, "steel_kg": 8.0, "wood_m3": 0.30, "bamboo_kg": 0.0, "earth_t": 0.0,
        "co2_kg": 200, "labour_h": 25, "storeys": "4-8", "where": "dense cities in or near forest regions",
        "basis": "CLT use factors 0.149-0.457 m3 per m2 of footprint per storey, most above 0.305 (Dolan et al. 2019 citing Crespell "
                 "& Gagnon 2010, VERIFIED); cement for foundations and cores, steel connectors, CO2 and labour ASSUMPTION"},
    "bamboo_frame": {
        "label": "Engineered bamboo or bahareque frame, 1-3 storeys",
        "cement_kg": 30.0, "steel_kg": 4.0, "wood_m3": 0.02, "bamboo_kg": 45.0, "earth_t": 0.0,
        "co2_kg": 60, "labour_h": 45, "storeys": "1-3", "where": "humid tropics (South and South-East Asia, Central Africa, Latin America)",
        "basis": "bamboo buildings about 30 kg CO2e/m2 (Escamilla 2018, cited in v70) and a Colombian bamboo house about 107 (unverified): "
                 "60 is judgement; bamboo mass per m2 (30-60 kg) ASSUMPTION, the inventory paper could not be read (publisher refuses "
                 "automated access); cement for foundations and render ASSUMPTION; needs treatment against borers and fungi"},
    "earth_vault": {
        "label": "Compressed or raw earth walls with earth vault roofs, 1-2 storeys",
        "cement_kg": 8.0, "steel_kg": 1.0, "wood_m3": 0.0, "bamboo_kg": 0.0, "earth_t": 1.2,
        "co2_kg": 40, "labour_h": 70, "storeys": "1-2", "where": "dry and semi-arid regions (Sahel, Horn of Africa, South Asia's dry zones, Middle East, Andes)",
        "basis": "Nubian Vault programme: 8,500+ buildings, 4,900+ trained masons, 7 Sahel countries, 'based exclusively on local raw "
                 "earth' (lavoutenubienne.org, VERIFIED); cement 0-15 kg for optional stabilised blocks, earth mass, CO2 and labour "
                 "(PMAY-G upper value 64 h/m2) ASSUMPTION; limited to low rise and to climates with little driving rain"},
}

MIXES = {  # shares of the floor area built each year
    "all_rc_conventional": {"rc_conventional": 1.0},
    "all_rc_lc3": {"rc_lc3": 1.0},
    "regional_mix": {"bamboo_frame": 0.25, "earth_vault": 0.20, "timber_frame": 0.20, "clt_midrise": 0.10, "rc_lc3": 0.25},
    "max_bio": {"bamboo_frame": 0.40, "timber_frame": 0.20, "clt_midrise": 0.20, "earth_vault": 0.15, "rc_lc3": 0.05},
    "all_timber_frame": {"timber_frame": 1.0},
    "all_bamboo": {"bamboo_frame": 1.0},
}

WORLD = {
    "cement_mt_per_yr": {"value": 4000, "class": "REPORTED", "basis": "USGS MCS 2025/2026, 3.8-4.1 bn t (PDF refuses automated fetch)"},
    "steel_mt_per_yr": {"value": 1882.6, "class": "REPORTED", "basis": "worldsteel 2024 (page renders without text)"},
    "industrial_roundwood_mm3_per_yr": {"value": 1984, "class": "VERIFIED", "basis": "FAO forest products statistics, 2020 table: roundwood 3,912, "
                                                                                   "wood fuel 1,928, industrial roundwood 1,984 million m3"},
    "forest_area_bn_ha": {"value": 4.06, "class": "VERIFIED", "basis": "FAO FRA 2020 key findings: 4.06 billion ha, nearly a third of land"},
    "plantation_forest_mha": {"value": 131, "class": "VERIFIED", "basis": "FAO FRA 2020: plantation forests about 131 million ha, 3% of forest area"},
    "bamboo_area_mha": {"value": 35, "class": "REPORTED", "basis": "FAO FRA 2020 bamboo area about 35 million ha; not read in source this session"},
    "bamboo_yield_t_ha_yr": {"low": 10, "central": 20, "high": 30, "class": "REPORTED",
                             "basis": "Dendrocalamus giganteus 20-30 t/ha/yr dry (commercial nursery claim); 10 as a conservative value"},
    "plantation_wood_yield_m3_ha_yr": {"low": 5, "central": 10, "high": 15, "class": "ASSUMPTION",
                                       "basis": "managed temperate forests about 3-5 m3/ha/yr, tropical plantations 10-20"},
    "co2_budget_1p5_gt": {"value": 130, "class": "VERIFIED", "basis": "v66/ecology (Forster et al. 2025), 50% chance, from 2025"},
    "hours_per_worker_year": 1290,
}


def mix_inventory(shares):
    inv = {k: 0.0 for k in ("cement_kg", "steel_kg", "wood_m3", "bamboo_kg", "earth_t", "co2_kg", "labour_h")}
    for sysname, sh in shares.items():
        for k in inv:
            inv[k] += sh * SYSTEMS[sysname][k]
    return inv


def tropical_share(regions):
    """Share of the population of deficit regions whose capital lies within the tropics / within 30 degrees (crude)."""
    meta = json.loads((U / "v65" / "data" / "raw" / "wb_country_meta.json").read_text())[1]
    lat = {m["id"]: abs(float(m["latitude"])) for m in meta if m["latitude"]}
    deficit = {k: v for k, v in regions.items() if v["floor_m2"] < TARGET_M2 and k in lat}
    pop = sum(v["pop0"] for v in deficit.values())
    return {"within_tropics_23_5": round(sum(v["pop0"] for k, v in deficit.items() if lat[k] <= 23.5) / pop, 3),
            "within_30_degrees": round(sum(v["pop0"] for k, v in deficit.items() if lat[k] <= 30.0) / pop, 3)}


def main(write=True):
    pub = json.loads((ROOT.parent / "outputs" / "housing.json").read_text())["cases"][BASE_CASE]
    peak = pub["peak_bn_m2_per_yr"] * 1e9
    total30 = (pub["new_bn_m2_30y"] + pub["upgraded_bn_m2_30y"]) * 1e9
    W = WORLD
    res = {}
    for name, shares in MIXES.items():
        assert abs(sum(shares.values()) - 1.0) < 1e-9, name
        inv = mix_inventory(shares)
        cement_mt = peak * inv["cement_kg"] / 1e9
        steel_mt = peak * inv["steel_kg"] / 1e9
        wood_mm3 = peak * inv["wood_m3"] / 1e6
        bamboo_mt = peak * inv["bamboo_kg"] / 1e9
        res[name] = {
            "shares": shares, "per_m2": {k: round(v, 3) for k, v in inv.items()},
            "cement_mt_per_yr": round(cement_mt, 1), "cement_share_of_world": round(cement_mt / W["cement_mt_per_yr"]["value"], 3),
            "steel_mt_per_yr": round(steel_mt, 1), "steel_share_of_world": round(steel_mt / W["steel_mt_per_yr"]["value"], 3),
            "wood_mm3_per_yr": round(wood_mm3, 1), "wood_share_of_industrial_roundwood": round(wood_mm3 / W["industrial_roundwood_mm3_per_yr"]["value"], 3),
            "plantation_mha_needed": {lvl: round(wood_mm3 / W["plantation_wood_yield_m3_ha_yr"][lvl], 1) for lvl in ("low", "central", "high")},
            "plantation_mha_needed_vs_existing_plantations": round(wood_mm3 / W["plantation_wood_yield_m3_ha_yr"]["central"] / W["plantation_forest_mha"]["value"], 2),
            "bamboo_mt_per_yr": round(bamboo_mt, 1),
            "bamboo_mha_needed": {lvl: round(bamboo_mt / W["bamboo_yield_t_ha_yr"][lvl], 1) for lvl in ("low", "central", "high")},
            "bamboo_mha_needed_vs_existing_area": round(bamboo_mt / W["bamboo_yield_t_ha_yr"]["central"] / W["bamboo_area_mha"]["value"], 2),
            "earth_gt_per_yr": round(peak * inv["earth_t"] / 1e9, 2),
            "co2_gt_per_yr_at_peak": round(peak * inv["co2_kg"] / 1e12, 2),
            "co2_gt_30y": round(total30 * inv["co2_kg"] / 1e12, 1),
            "co2_30y_share_of_1p5_budget": round(total30 * inv["co2_kg"] / 1e12 / W["co2_budget_1p5_gt"]["value"], 2),
            "peak_workers_m": round(peak * inv["labour_h"] / W["hours_per_worker_year"] / 1e6),
        }
    regions = compare.rt.load_regions()
    out = {"question": "author, 2026-11-08: can any material be used better than cement and steel?",
           "peak_bn_m2_per_yr": round(peak / 1e9, 2), "total_30y_bn_m2": round(total30 / 1e9), "systems": SYSTEMS, "mixes": res,
           "world_resources": W, "deficit_population_by_latitude": tropical_share(regions),
           "reading": "no single material replaces cement and steel for 7 billion m2 a year: all-timber would take about two-thirds "
                      "of the world's industrial roundwood, and all-bamboo half to all of today's bamboo area at reported yields, in a "
                      "climate that holds 44-81% of the people in need. A regional mix does the job: bamboo in the humid tropics, earth with "
                      "vault roofs in dry regions, timber where forests are managed, cross-laminated timber in dense cities, and LC3 cement "
                      "where concrete is still needed. It cuts cement to about 40% of the conventional programme, steel to 40%, and embodied "
                      "CO2 by about 60%, with about the same hours of work, more of them local and low-skill. Its weak point is wood: about "
                      "a third of today's industrial roundwood, like the conventional programme itself. LC3 alone saves only about 8% of a "
                      "building's embodied CO2, because cement is a fifth of it: the frame, floors and roof are where the carbon is.",
           "limits": ["bamboo mass per m2 and bamboo area are not verified; yields are commercial claims",
                      "earth and bamboo systems are limited to 1-3 storeys and to their climates; durability depends on treatment, "
                      "detailing and maintenance (driving rain, termites, earthquakes)",
                      "labour per m2 for timber, bamboo and earth systems are assumptions; earth is deliberately labour-intensive",
                      "the mix shares are a design proposal, not an optimisation; the latitude test uses capitals only",
                      "the conventional system's wood (41.6 kg/m2) is the median of a Europe-heavy sample with many timber homes and probably "
                      "overstates wood in concrete-frame homes of the regions in need",
                      "wood: harvesting 0.6-0.8 bn m3 a year for housing competes with paper, fuel and furniture; plantation "
                      "expansion has land and biodiversity costs not modelled"]}
    if write:
        (ROOT.parent / "outputs" / "housing_materials.json").write_text(json.dumps(out, indent=2))
        print(f"peak {out['peak_bn_m2_per_yr']} bn m2/yr; 30-year total {out['total_30y_bn_m2']} bn m2; deficit population by latitude {out['deficit_population_by_latitude']}")
        print(f"{'mix':22s}{'cement%':>9s}{'steel%':>8s}{'wood% rw':>10s}{'plant Mha':>10s}{'bamboo Mha':>11s}{'CO2 Gt/30y':>11s}{'budget%':>9s}{'workers m':>10s}")
        for n, r in res.items():
            print(f"{n:22s}{r['cement_share_of_world']*100:8.0f}%{r['steel_share_of_world']*100:7.0f}%{r['wood_share_of_industrial_roundwood']*100:9.0f}%"
                  f"{r['plantation_mha_needed']['central']:10.0f}{r['bamboo_mha_needed']['central']:11.0f}{r['co2_gt_30y']:11.0f}{r['co2_30y_share_of_1p5_budget']*100:8.0f}%{r['peak_workers_m']:10.0f}")
    return out


if __name__ == "__main__":
    main()
