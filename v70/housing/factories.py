"""UNIRA V7.0 — where should the factories for walls and homes be? (author's direction, 2026-11-08)

The author asked which regions could build factories to produce walls and homes as fast as possible for all regions.
Article 10a.5 says One Earth decides where goods are produced so as to use the fewest hours, resources and transport,
while giving every region productive work. This module applies that rule to industrialised home building with the
project's regional data (179 regions: floor area, population, World Bank manufacturing share, GDP, coordinates):
  1. how much factory output each region needs at the peak of the housing programme (pro rata to its 30-year need);
  2. how many plants that is, at the output of verified module factories (1,000-1,200 homes a year);
  3. whether homes or panels could be imported from a surplus industrial region within the economical transport
     distance (modules: about 200 miles / 320 km, UW CERC 2013; panels: up to 1,000 km, assumption), or must be made
     in the region of need;
  4. the cement and steel the programme needs against world production (reported figures, not verified in source);
  5. the workforce at the industrialised benchmark (Finnish precast value chain: 13 h/m2, verified).
Run after run.py:  python3 factories.py  ->  ../outputs/housing_factories.json
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
U = ROOT.parents[1]
sys.path[:0] = [str(U / "v68" / "counterfactual"), str(U / "v67"), str(U / "v66" / "model")]
import compare  # noqa: E402

TARGET_M2 = 27.0
BASE_CASE = "ramp_10pct_stock_first_low_carbon"
PARAMS = {
    "module_radius_km": {"value": 320, "basis": "200 miles 'probably the most cost-efficient option' for trucking modules "
                         "(UW Construction Management, CERC report 2013, Skanska grant, VERIFIED text)"},
    "panel_radius_km": {"value": 1000, "basis": "flat wall and floor panels are shipped much farther than room modules "
                        "(industry commentary, REPORTED); 1,000 km is a generous SYNTHETIC bound"},
    "plant_homes_per_year": {"low": 1000, "central": 1200, "high": 2000,
                             "basis": "Sekisui Heim plant 80 km north of Bangkok, 1,000 houses/yr (VERIFIED); BoKlok (Skanska/IKEA) "
                                      "about 1,200 homes/yr (VERIFIED); Urban Splash/Sekisui House UK target 2,000/yr (REPORTED). "
                                      "Module plants; panel plants can be larger, so plant counts are upper bounds"},
    "m2_per_home": {"value": 80, "basis": "SYNTHETIC: about three people at the 27 m2 comfortable standard"},
    "material_kg_per_m2": {"cement": 54.3, "steel": 26.7, "concrete": 613.0, "wood": 41.6,
                           "basis": "residential medians, Heeren & Fishman 2019 material-intensity database (v66/construction/evidence.csv, VERIFIED computation)"},
    "world_production_mt": {"cement": 4000, "steel": 1882.6,
                            "basis": "cement: USGS Mineral Commodity Summaries, about 3.8-4.1 bn t in 2023-2025 (REPORTED, PDF refused "
                                     "automated fetch); steel: worldsteel 2024 total 1,882.6 Mt, China 1,005.1, India 149.6 (REPORTED, "
                                     "pages render without text). Both REPORTED_NEEDS_RECHECK"},
    "labour_h_per_m2": {"factory_value_chain": 13.0, "site_central": 48.0,
                        "basis": "13 h/m2 (10-20) for 11 Finnish precast apartment projects, whole value chain excluding material "
                                 "manufacture (RT 2024, VERIFIED); 48 = v70 central site-built value"},
    "hours_per_worker_year": 1290,
}


def km(a, b):
    (la1, lo1), (la2, lo2) = [(math.radians(x), math.radians(y)) for x, y in (a, b)]
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def coords():
    meta = json.loads((U / "v65" / "data" / "raw" / "wb_country_meta.json").read_text())[1]
    return {m["id"]: (float(m["latitude"]), float(m["longitude"])) for m in meta if m["latitude"]}


def latest(code):
    out = {}
    for r in json.loads((U / "v85" / "realdata" / "data" / "raw" / f"wb_{code}.json").read_text())[1]:
        if r["value"] is None or not r["countryiso3code"]:
            continue
        if r["countryiso3code"] not in out or r["date"] > out[r["countryiso3code"]][0]:
            out[r["countryiso3code"]] = (r["date"], float(r["value"]))
    return {k: v for k, (d, v) in out.items()}


def need_m2(v, target=TARGET_M2):
    return max(0.0, target - v["floor_m2"]) * v["pop0"] + target * max(0.0, v["pop50"] - v["pop0"])


def main(write=True):
    regions = compare.rt.load_regions()
    xy = coords()
    manuf, gdp = latest("NV.IND.MANF.ZS"), latest("NY.GDP.PCAP.PP.KD")
    peak = json.loads((ROOT.parent / "outputs" / "housing.json").read_text())["cases"][BASE_CASE]["peak_bn_m2_per_yr"] * 1e9
    needs = {k: need_m2(v) for k, v in regions.items()}
    total = sum(needs.values())
    # manufacturing value added per person (PPP) as the proxy for industrial capacity to make machines and components
    mva_pc = {k: manuf[k] / 100 * gdp[k] for k in regions if k in manuf and k in gdp}
    med = sorted(mva_pc.values())[len(mva_pc) // 2]
    suppliers = [k for k, v in regions.items() if v["floor_m2"] >= TARGET_M2 and mva_pc.get(k, 0) >= med and k in xy]
    industrial = [k for k in regions if mva_pc.get(k, 0) >= med and k in xy]
    deficit = {k: v for k, v in regions.items() if v["floor_m2"] < TARGET_M2}
    P = PARAMS
    plants = {lvl: peak / (P["plant_homes_per_year"][lvl] * P["m2_per_home"]["value"]) for lvl in ("low", "central", "high")}
    rows, cls = [], {"surplus_industrial": {}, "any_industrial": {}}
    for key, pool in (("surplus_industrial", suppliers), ("any_industrial", industrial)):
        shares = {"within_module_radius": 0.0, "within_panel_radius": 0.0, "beyond": 0.0, "no_coordinates": 0.0}
        for k, v in deficit.items():
            if k not in xy:
                shares["no_coordinates"] += v["pop0"]
                continue
            d = min((km(xy[k], xy[s]) for s in pool if s != k), default=float("inf"))
            if d <= P["module_radius_km"]["value"]:
                shares["within_module_radius"] += v["pop0"]
            elif d <= P["panel_radius_km"]["value"]:
                shares["within_panel_radius"] += v["pop0"]
            else:
                shares["beyond"] += v["pop0"]
            if key == "surplus_industrial":
                rows.append({"region": k, "pop_m": round(v["pop0"] / 1e6, 1), "floor_m2": v["floor_m2"],
                             "need_share": round(needs[k] / total, 4), "peak_demand_m2_per_yr": round(needs[k] / total * peak),
                             "plants_central": round(needs[k] / total * plants["central"]),
                             "nearest_surplus_industrial_km": round(d)})
        pop = sum(v["pop0"] for v in deficit.values())
        cls[key] = {s: round(x / pop, 4) for s, x in shares.items()}
    deficit_pop = sum(v["pop0"] for v in deficit.values())
    mat = {m: peak * P["material_kg_per_m2"][m] / 1e9 for m in ("cement", "steel", "concrete", "wood")}  # Mt/yr
    top_suppliers = sorted(suppliers, key=lambda k: -mva_pc[k] * regions[k]["pop0"])[:12]
    rows.sort(key=lambda r: -r["need_share"])
    out = {"question": "author, 2026-11-08: which regions can build factories to make walls and homes as fast as possible for all regions",
           "rule": "Article 10a.5: produce where it takes the fewest hours, resources and transport, giving every region productive work",
           "peak_world_demand_bn_m2_per_yr": round(peak / 1e9, 2), "deficit_regions": len(deficit),
           "deficit_population_bn": round(deficit_pop / 1e9, 2),
           "plants_needed_world": {lvl: round(n) for lvl, n in plants.items()},
           "plants_per_million_people_in_deficit_regions": {lvl: round(n / (deficit_pop / 1e6), 1) for lvl, n in plants.items()},
           "people_per_plant_central": round(deficit_pop / plants["central"]),
           "share_of_deficit_population_by_distance_to_nearest_supplier": cls,
           "surplus_industrial_regions": len(suppliers), "largest_surplus_industrial_regions_by_manufacturing": top_suppliers,
           "materials_at_peak_mt_per_yr": {m: round(x, 1) for m, x in mat.items()},
           "materials_share_of_world_production": {m: round(mat[m] / P["world_production_mt"][m], 3) for m in ("cement", "steel")},
           "workforce_at_peak_m": {"site_built_48_h_per_m2": round(peak * P["labour_h_per_m2"]["site_central"] / P["hours_per_worker_year"] / 1e6),
                                   "factory_value_chain_13_h_per_m2": round(peak * P["labour_h_per_m2"]["factory_value_chain"] / P["hours_per_worker_year"] / 1e6)},
           "regions": rows[:40], "parameters": PARAMS,
           "reading": "the homes must be made where they are needed: almost all people in deficit regions live beyond the distance "
                      "over which room modules travel economically, and most beyond the generous bound for panels, when distance is "
                      "measured between capitals (so even this overstates reach). The programme is a distributed local industry of "
                      "tens of thousands of plants, about one per 80,000-150,000 people, not a few exporting regions. What the "
                      "industrial regions supply is the machines, the training, and the cement and steel where local production is "
                      "short: the programme needs about a tenth of world cement and steel output at its peak. At the industrialised "
                      "benchmark the peak workforce falls from about 265 million to about 70 million.",
           "limits": ["capital-to-capital distances understate distances inside large regions (India, Nigeria, Brazil), so the "
                      "'within radius' shares are upper bounds on what imports could serve",
                      "plant output figures are from module factories in Thailand, Estonia and the UK; panel plants are larger, so "
                      "the plant counts are upper bounds and the people-per-plant figures lower bounds",
                      "cement and steel world production are reported, not verified in source; the shares are ratios, robust to "
                      "about 10% error",
                      "no data on cement production by region in the project; where Sub-Saharan Africa's cement would come from is "
                      "the open question for the next step",
                      "the Finnish 13 h/m2 benchmark excludes material manufacture and earthworks and reflects a high-skill, "
                      "capital-intensive industry; reaching it everywhere is an assumption"]}
    if write:
        (ROOT.parent / "outputs" / "housing_factories.json").write_text(json.dumps(out, indent=2))
        print(f"peak demand {out['peak_world_demand_bn_m2_per_yr']} bn m2/yr in {len(deficit)} deficit regions ({out['deficit_population_bn']} bn people)")
        print("plants needed:", out["plants_needed_world"], "| per million people:", out["plants_per_million_people_in_deficit_regions"])
        print("deficit population by distance to nearest surplus industrial region:", cls["surplus_industrial"])
        print("                             to nearest industrial region of any kind:", cls["any_industrial"])
        print("materials Mt/yr:", out["materials_at_peak_mt_per_yr"], "| share of world:", out["materials_share_of_world_production"])
        print("workforce at peak (m):", out["workforce_at_peak_m"])
        print("largest surplus industrial regions:", top_suppliers)
        print("largest deficit regions:", [(r["region"], r["plants_central"], r["nearest_surplus_industrial_km"]) for r in rows[:10]])
    return out


if __name__ == "__main__":
    main()
