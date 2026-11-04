"""UNIRA V8.7 — how fast can humanity guarantee the UNIRA living standard (Constitution Article 10c) to every person?

Order of means (UNIRA): use and redistribute what exists, repair and renovate, then build and train only what is
missing. Two dates per scenario: when everyone has the ESSENTIAL standard, and when everyone has the COMFORTABLE one
(basket.json). Domains:
    access (water, sanitation, electricity, clean cooking, internet, secondary school): each country's coverage rises by
        max(its own measured 2010-latest yearly gain, the median gain of lagging countries) x scenario speed
    energy, health workers, housing: the 30-year world plan (v67 transition) with decent-first allocation (v79),
        region-specific targets (energy adjusted for climate, health for age and disease burden), scenario capacities
    food: redistribution of today's supply (v65/v79) and halving waste (v67)
    teachers: pupils per teacher falls as teacher numbers grow in deficit countries
    goods and discretionary: needs-based quotas from world goods capacity (v85)
Labour: hours per person needed for the comfortable basket, from France's input-output hours by domain (v63) scaled to
the UNIRA standard, plus building the housing gap; automation by sector reduces them over time.
Environment: world final energy at the comfortable level for 2050's population against today's level and the 1.5 C range
(v66). Dates use two coverage tests: 99% of humanity, and every country with data ("last country").
python3 simulate.py  ->  ../outputs/livingstandard.json"""
import importlib.util
import json
import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
B = json.loads((HERE / "basket.json").read_text())
sys.path[:0] = [str(U / "v67"), str(U / "v68" / "counterfactual"), str(U / "v66" / "model"), str(U / "v79" / "allocation")]
import run_transition as rt  # noqa: E402
import transition as tr  # noqa: E402
spec = importlib.util.spec_from_file_location("hw", U / "v79" / "health_need" / "weights.py")
hw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hw)
HORIZON = 80
ACCESS = {"water": ("SH.H2O.BASW.ZS", "SH.H2O.SMDW.ZS"), "sanitation": ("SH.STA.BASS.ZS", "SH.STA.BASS.ZS"),
          "electricity": ("EG.ELC.ACCS.ZS", "EG.ELC.ACCS.ZS"), "clean_cooking": ("EG.CFT.ACCS.ZS", "EG.CFT.ACCS.ZS"),
          "internet": ("IT.NET.USER.ZS", "IT.NET.USER.ZS"), "secondary_school": ("SE.SEC.ENRR", "SE.SEC.ENRR")}


def series(code, folder=HERE / "data" / "raw"):
    out = {}
    for x in json.loads((folder / f"wb_{code}.json").read_text())[1]:
        if x["value"] is not None and x["countryiso3code"]:
            out.setdefault(x["countryiso3code"], {})[int(x["date"])] = x["value"]
    return out


def latest(s, k):
    ys = sorted(s.get(k, {}))
    return (ys[-1], s[k][ys[-1]]) if ys else (None, None)


def countries():
    meta = {m["id"]: m for m in json.loads((U / "v65" / "data" / "raw" / "wb_country_meta.json").read_text())[1]}
    pop = series("SP.POP.TOTL", U / "v74" / "distribution" / "data" / "raw")
    return {k: {"pop": latest(pop, k)[1], "lat": float(meta[k]["latitude"]), "region": meta[k]["region"]["value"].strip(),
                "income": meta[k]["incomeLevel"]["value"]}
            for k in meta if meta[k]["region"]["value"].strip() != "Aggregates" and meta[k]["latitude"] and latest(pop, k)[1]}


UNIVERSAL = 99.0  # ASSUMPTION: 99% coverage counts as universal (the last fraction needs targeted, not average, effort)


def access_dates(cty, speed):
    """Year each access domain reaches its essential and comfortable target (99% of humanity, last country)."""
    out, inventory = {}, {}
    for dom, (ess_code, com_code) in ACCESS.items():
        res = {}
        for level, code in (("essential", ess_code), ("comfortable", com_code)):
            s = series(code)
            if dom == "secondary_school":
                target = B["domains"]["education"][f"{level}_secondary_enrolment"]
            else:
                target = min(UNIVERSAL, B["domains"][dom][level])
            gains = []
            for k in s:
                y1, v1 = latest(s, k)
                if y1 and 2010 in s[k] and s[k][2010] < target and y1 > 2010:
                    gains.append((v1 - s[k][2010]) / (y1 - 2010))
            pos = sorted(g for g in gains if g > 0)
            q = {1.0: 0.5, 1.5: 0.75, 2.5: 0.9}.get(speed, 0.5)  # scenario = median / top quarter / top tenth of real gains
            med = pos[min(len(pos) - 1, int(q * len(pos)))] if pos else 1.0
            pts = []
            covered_now = 0.0
            known_pop = 0.0
            for k, c in cty.items():
                y1, v = latest(s, k)
                if v is None:
                    continue
                known_pop += c["pop"]
                own = ((v - s[k][2010]) / (y1 - 2010)) if 2010 in s[k] and y1 > 2010 else 0.0
                rate = max(own, med)
                years = 0 if v >= target else math.ceil((target - v) / rate) if rate > 0 else 999
                pts.append((years, c["pop"], k))
                covered_now += c["pop"] * min(v, 100) / 100
            pts.sort()
            acc, y99 = 0.0, None
            for years, p, _ in pts:
                acc += p
                if y99 is None and acc >= 0.99 * known_pop:
                    y99 = years
            res[level] = {"target": target, "yearly_gain_points_used": round(med, 2), "gain_percentile": q, "year_99pct_of_people": y99,
                          "year_last_country": pts[-1][0] if pts else None, "last_country": pts[-1][2] if pts else None}
            if level == "essential":
                inventory[dom] = {"people_covered_share_now": round(covered_now / known_pop, 3),
                                  "countries_below_essential_now": sum(1 for y, _, _ in pts if y > 0)}
        out[dom] = res
    return out, inventory


def climate_weights(regions, cty):
    raw = {k: min(1.25, max(0.85, 1 + 0.25 * (abs(cty[k]["lat"]) - 25) / 40)) if k in cty else 1.0 for k in regions}
    mean = sum(raw[k] * regions[k]["pop0"] for k in regions) / sum(r["pop0"] for r in regions.values())
    return {k: v / mean for k, v in raw.items()}


def physical_dates(regions, cty, sc):
    """Energy, health and housing: decent-first allocation with region-specific targets; per-year coverage."""
    cap = json.loads((U / "v66" / "construction" / "capacity.json").read_text())
    ew = climate_weights(regions, cty)
    a3, gw = hw.age_weights(regions, 3.0), hw.gap_weights(regions)
    hwt = hw.normalise({k: 0.5 * (a3[k] + gw[k]) for k in regions}, regions)
    d = B["domains"]
    spec_ = {"energy": ("energy_gj", d["energy"]["essential"], d["energy"]["comfortable"], 1.0, ew),
             "health": ("health_10k", d["health"]["essential"], d["health"]["comfortable"], 1e-4, hwt),
             "housing": ("floor_m2", d["housing"]["essential"], d["housing"]["comfortable"], 1.0, {k: 1.0 for k in regions})}
    base = cap["world_res_floor_added_m2_per_yr"]["central"]

    def floor(t, f_def):
        need_pop = sum(regions[k]["pop0"] for k, v in f_def.items() if v > 0)
        return min(base * (1 + sc["housing_growth"]) ** t, 1.468 * need_pop)
    p = {"energy_target": 40, "health_target": 131, "floor_target": 27, "excess_decline": 0.04,
         "energy_new_ej_per_yr": sc["energy_new_ej_per_yr"], "health_net_new": rt.health_flow(sc["health_plan"]),
         "floor_new_m2_per_yr": floor, "kcal_eaten": {"decent": 2100, "comfortable": 2470},
         "waste_now": 0.19, "waste_unira": 0.095, "waste_years": 10, "military_energy_share": 0.0, "military_years": 0,
         "energy_target_by_region": {k: d["energy"]["comfortable"] * ew[k] for k in regions}}
    cover = {dom: {"essential": [], "comfortable": []} for dom in spec_}
    built = []
    real = tr.allocate_perceived

    def alloc(pool, true_def, p_, domain, t):
        st = p_["_state"]
        key, ess, com, unit, w = spec_[domain]
        W = sum(r["pop"] for r in st.values())
        for lvl, tgt in (("essential", ess), ("comfortable", com)):
            if len(cover[domain][lvl]) == t:
                cover[domain][lvl].append(sum(r["pop"] for k, r in st.items() if r[key] >= tgt * w[k] - 1e-9) / W)
        dec = {k: max(0.0, (ess * w[k] - st[k][key]) * unit * st[k]["pop"]) for k in st}
        com_def = {k: max(0.0, (com * w[k] - st[k][key]) * unit * st[k]["pop"]) for k in st}
        g1 = tr.allocate(pool, dec)
        g2 = tr.allocate(pool - sum(g1.values()), {k: com_def[k] - g1[k] for k in st})
        g = {k: g1[k] + g2[k] for k in st}
        if domain == "housing":
            built.append(sum(g.values()))
        return g
    tr.allocate_perceived = alloc
    try:
        rows, _ = tr.run(regions, p, HORIZON)
    finally:
        tr.allocate_perceived = real
    out = {}
    for dom, c in cover.items():
        out[dom] = {lvl: {"year_99pct_of_people": next((t for t, v in enumerate(c[lvl]) if v >= 0.99), None),
                          "year_everyone": next((t for t, v in enumerate(c[lvl]) if v >= 0.9999), None),
                          "share_covered_year_0": round(c[lvl][0], 3)} for lvl in c}
    food_ok = next((r["year"] for r in rows if r["food_comfortable_for_all_feasible"]), None)
    out["food"] = {"essential": {"year_99pct_of_people": 1, "year_everyone": 1, "how": "redistribution of today's supply (1.16x decent need; 1.4% of supply moved, v79)"},
                   "comfortable": {"year_99pct_of_people": food_ok, "year_everyone": food_ok, "how": "halving waste (v67)"}}
    return out, rows, built, ew


def teacher_dates(cty, sc):
    s = series("SE.PRM.ENRL.TC.ZS", U / "v85" / "realdata" / "data" / "raw")
    res = {}
    for lvl in ("essential", "comfortable"):
        tgt = B["domains"]["education"][f"{lvl}_pupils_per_teacher"]
        pts = []
        for k, c in cty.items():
            y, r = latest(s, k)
            if r is None:
                continue
            yrs = 0 if r <= tgt else math.ceil(math.log(r / tgt) / math.log(1 + sc["teacher_growth"]))
            pts.append((yrs, c["pop"], k))
        pts.sort()
        tot, acc, y99 = sum(p for _, p, _ in pts), 0.0, None
        for yrs, p, _ in pts:
            acc += p
            if y99 is None and acc >= 0.99 * tot:
                y99 = yrs
        res[lvl] = {"year_99pct_of_people": y99, "year_last_country": pts[-1][0], "last_country": pts[-1][2]}
    return res


def labour(sc, regions, built, years=(0, 30, 60)):
    lab = B["labour"]
    hrs = {r["product"]: r for r in __import__("csv").DictReader((U / "v63" / "io" / "outputs" / "hours_by_product.csv").open()) if r["year"] == "2022"}
    fr_pop = latest(series("SP.POP.TOTL", U / "v74" / "distribution" / "data" / "raw"), "FRA")[1]
    scale = dict(lab["scale_to_unira"])
    scale["energy"] = B["domains"]["energy"]["comfortable"] / regions["FRA"]["energy_gj"]
    scale["housing"] = B["domains"]["housing"]["comfortable"] / regions["FRA"]["floor_m2"]
    per = {}
    for dom, prods in lab["domain_products"].items():
        h = sum((float(hrs[p]["embodied_household_consumption_ths"]) + float(hrs[p]["embodied_government_consumption_ths"])) * 1000
                for p in prods if p in hrs)
        per[dom] = h / fr_pop / 52 * float(scale[dom])  # hours per person per week, at the UNIRA standard
    build_h = (statistics.fmean(built[:30]) * 48.0 / sum(r["pop0"] for r in regions.values()) / 52) if built else 0.0  # v70: 48 h/m2
    worker_share = 0.45  # ASSUMPTION: workers per person (France 2022 about 0.45; universal work under UNIRA)
    out = {}
    for y in years:
        prog = min(1.0, sc["automation_by_year_30"] * y / 30)
        dom_h = {d: per[d] * (1 - lab["automation_potential"][d] * prog) for d in per}
        b = build_h if y < 30 else build_h * 0.3  # building the gap, then maintenance
        tot = sum(dom_h.values()) + b
        out[f"year_{y}"] = {"hours_per_person_week": round(tot, 2), "hours_per_worker_week": round(tot / worker_share, 1),
                            "building_gap_hours_per_worker_week": round(b / worker_share, 2),
                            "by_domain_hours_per_worker_week": {d: round(v / worker_share, 2) for d, v in dom_h.items()},
                            "automation_saving_by_domain_hours_per_worker_week": {d: round(per[d] * lab["automation_potential"][d] * prog / worker_share, 2) for d in per}}
    return out


def main():
    cty = countries()
    regions = rt.load_regions()
    out = {"basket": B["domains"], "scenarios": {}}
    access0, inventory = access_dates(cty, 1.0)
    out["inventory_now"] = inventory
    for name, sc in B["scenarios"].items():
        if name.startswith("_"):
            continue
        acc, _ = access_dates(cty, sc["access_speed"])
        phys, rows, built, ew = physical_dates(regions, cty, sc)
        teach = teacher_dates(cty, sc)
        goods = {"essential": {"year_99pct_of_people": 0, "year_everyone": 0},
                 "comfortable": {"year_99pct_of_people": 0, "year_everyone": 0},
                 "how": "world goods capacity covers about 66% of France's goods level per person after reserves (v85); the basket needs 30% (essential) and 60% (comfortable), delivered by needs-based quotas"}
        allx = {**{k: v for k, v in acc.items()}, **phys, "teachers": teach, "goods": goods}
        def date(level, key):
            ys = []
            for dom, v in allx.items():
                x = v[level] if level in v else None
                if x is None:
                    continue
                y = x.get(key, x.get("year_99pct_of_people"))
                ys.append((999 if y is None else y, dom))
            return max(ys)
        lab = labour(sc, regions, built)
        world_e_2050 = sum(B["domains"]["energy"]["comfortable"] * ew[k] * r["pop50"] for k, r in regions.items()) / 1e9
        out["scenarios"][name] = {
            "essential_99pct": date("essential", "year_99pct_of_people"), "comfortable_99pct": date("comfortable", "year_99pct_of_people"),
            "essential_everyone": date("essential", "year_everyone"), "comfortable_everyone": date("comfortable", "year_everyone"),
            "domains": allx, "labour": lab,
            "environment": {"world_final_energy_comfortable_2050_ej": round(world_e_2050), "today_model_ej": 409,
                            "ipcc_1p5_range_note": "v66: 386 EJ for 9.66 bn at 40 GJ lies within IPCC 1.5 C-class pathways if about half of final energy is electricity and fossil CO2 is near zero by 2050",
                            "energy_check": "pass" if world_e_2050 <= 409 else "fail",
                            "housing_co2": "v70: about 15-16 Gt with low-carbon building (about 12% of the remaining 1.5 C budget); about 41-43 Gt if conventional",
                            "food_land": "v66: fits within cropland limits only with planetary-health diets and halved waste"}}
        s = out["scenarios"][name]
        print(f"\n== {name}: essential for 99% of people in year {s['essential_99pct'][0]} (last: {s['essential_99pct'][1]}); "
              f"comfortable for 99% in year {s['comfortable_99pct'][0]} (last: {s['comfortable_99pct'][1]})")
        for dom, v in allx.items():
            e, c = v["essential"], v["comfortable"]
            print(f"   {dom:16s} essential 99%: {e.get('year_99pct_of_people')} | comfortable 99%: {c.get('year_99pct_of_people')}")
        print(f"   labour hours per worker-week: yr0 {lab['year_0']['hours_per_worker_week']} | yr30 {lab['year_30']['hours_per_worker_week']} | yr60 {lab['year_60']['hours_per_worker_week']}"
              f" | energy 2050 at comfortable: {world_e_2050:.0f} EJ ({s['environment']['energy_check']})")
    print("\ninventory now:", inventory)
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "livingstandard.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
