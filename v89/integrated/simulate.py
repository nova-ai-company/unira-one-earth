"""UNIRA V8.9 — how quickly can every person on Earth have a genuinely comfortable life (Article 10c), using existing
resources first, delivering essential infrastructure first (Article 10e) and minimising unnecessary labour?

Per country and per year, coverage in every domain, with ONE set of scenario assumptions for all sectors:
    energy, health workers, housing   world plan with decent-first allocation (v67 engine via v87), automation boosts
                                      housing capacity and training
    water, sanitation, clean cooking, electricity, Internet, secondary school
                                      per-country delivery (v88): pace = max(own measured pace, scenario percentile of
                                      real gains) x governance (conflict 0.5, fragility 0.75) x automation boost;
                                      repair first (water); durability: only functioning services count
    teachers                          pupils per teacher falls with teacher growth (v87)
    food                              redistribution (Level 1, year 1); comfortable diet when waste is halved (v67)
    goods, savings, leisure, holidays Level 2: needs-based goods quotas (v85/v87) and local services: each region's
                                      service capacity (v85, World Bank) grows with catch-up; Level 2 needs 0.6 of
                                      France's services per person (ASSUMPTION, consistent with the v87 basket scaling)
    mobility (Level 2)                shared car access, one car per three households, built where cars are lacking
                                      (ASSUMPTION: 60% of people live where cars are lacking; production share to them)
Level 1 / Level 2 coverage of a country = the smallest coverage among its domains (a person has the level only if
they have every part of it). Dates for 90%, 95% and 99% of humanity. Each year the critical bottleneck is the domain
leaving the most people short, with its type (materials, labour, energy, logistics, institutions, conflict).
Labour: v87 basket hours plus construction of new essential infrastructure (v88; operation already counted in v87).
python3 simulate.py  ->  ../outputs/integrated.json"""
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


L87 = load("ls87", U / "v87" / "livingstandard" / "simulate.py")
E88 = load("ess88", U / "v88" / "essential" / "model.py")
YEARS = 80
SCEN = {  # one consistent set per scenario across all sectors
    "conservative": {"v87": "conservative", "access_pctl": 0.5, "scale": 1.0, "auto30": 0.15, "service_catch_up": 0.02, "car_growth": 0.0, "car_share": 0.3},
    "moderate": {"v87": "moderate", "access_pctl": 0.75, "scale": 2.0, "auto30": 0.35, "service_catch_up": 0.04, "car_growth": 0.03, "car_share": 0.5},
    "accelerated": {"v87": "accelerated", "access_pctl": 0.9, "scale": 3.0, "auto30": 0.6, "service_catch_up": 0.06, "car_growth": 0.06, "car_share": 0.7},
    # comparison only (upper bound, not a forecast): as accelerated, but conflict and fragility no longer slow delivery
    "accelerated_if_conflicts_end": {"v87": "accelerated", "access_pctl": 0.9, "scale": 3.0, "auto30": 0.6, "service_catch_up": 0.06,
                                     "car_growth": 0.06, "car_share": 0.7, "no_conflict": True}}
ACCESS = {"water": ("SH.H2O.BASW.ZS", "SH.H2O.SMDW.ZS", "institutions"), "sanitation": ("SH.STA.BASS.ZS", "SH.STA.BASS.ZS", "institutions"),
          "clean_cooking": ("EG.CFT.ACCS.ZS", "EG.CFT.ACCS.ZS", "logistics"), "electricity": ("EG.ELC.ACCS.ZS", "EG.ELC.ACCS.ZS", "institutions"),
          "internet": ("IT.NET.USER.ZS", "IT.NET.USER.ZS", "logistics"), "secondary_school": ("SE.SEC.ENRR", "SE.SEC.ENRR", "labour")}
TYPE = {"energy": "energy", "health": "labour (training)", "housing": "materials and labour (construction)", "teachers": "labour (training)",
        "food": "logistics", "services": "labour (local services)", "mobility": "materials (vehicles)", "goods": "logistics"}
SERVICES_L2 = 0.6     # ASSUMPTION: Level 2 local services per person, share of France's
CAR_LACKING = 0.6     # ASSUMPTION: share of humanity living where shared cars are lacking
DURABLE = {"water": 0.9, "sanitation": 0.95, "clean_cooking": 0.95}  # functioning share of NEW services at first (v88)
MATURE = 0.99      # ASSUMPTION: with maintenance funded for the whole life (Article 10e), functioning reaches 99%
MATURE_YEARS = 15  # ASSUMPTION: years for maintenance systems to mature
TOL = 0.98         # measurement tolerance for physical thresholds (population growth dilutes levels slightly)
REPAIR_SHARE = 0.15


def automation(t, sc):
    return 1 + sc["auto30"] * min(1.0, t / 30)  # delivery speed-up in construction and services (never energy or materials)


def access_cov(cty, level, sc, gov):
    """{domain: {iso: [coverage share per year]}} for per-country delivery domains."""
    out = {}
    for dom, (ess, com, _) in ACCESS.items():
        code = ess if level == "essential" else com
        s = L87.series(code)
        target = 99.0
        if dom == "secondary_school":
            target = L87.B["domains"]["education"][f"{level}_secondary_enrolment"]
        if dom == "internet":
            target = L87.B["domains"]["internet"][level]
        gains = sorted((L87.latest(s, k)[1] - s[k][2010]) / (L87.latest(s, k)[0] - 2010) for k in s
                       if 2010 in s[k] and L87.latest(s, k)[0] and L87.latest(s, k)[0] > 2010 and s[k][2010] < target
                       and L87.latest(s, k)[1] > s[k][2010])
        pct = gains[min(len(gains) - 1, int(sc["access_pctl"] * len(gains)))] if gains else 1.0
        res = {}
        for k in cty:
            y, v = L87.latest(s, k)
            if v is None:
                continue
            own = ((v - s[k][2010]) / (y - 2010)) if 2010 in s[k] and y > 2010 else 0.0
            rate = max(own, pct) * gov.get(k, 1.0)
            path, val = [], v
            if dom == "water" and v < target:  # repair first: restoring broken points serves part of the gap quickly
                val = min(target, v + REPAIR_SHARE * (target - v) * 0.5)
            for t in range(YEARS + 1):
                if t > 0:
                    val = min(target, val + rate * automation(t, sc))
                d0 = DURABLE.get(dom, 1.0)
                f = d0 + (MATURE - d0) * min(1.0, t / MATURE_YEARS) if dom in DURABLE else 1.0
                reliable = min(v, target) + max(0.0, val - v) * f  # only newly built services can fail
                path.append(min(1.0, reliable / (target * TOL)) if target else 1.0)
            res[k] = path
        out[dom] = res
    return out


def main():
    cty = L87.countries()
    regions = L87.rt.load_regions()
    fcs = json.loads((U / "v88" / "essential" / "data" / "raw" / "fcs_fy26.json").read_text())
    gov = {k: 0.5 for k in fcs["conflict"]} | {k: 0.75 for k in fcs["institutional_social_fragility"]}
    status = {k: "conflict" for k in fcs["conflict"]} | {k: "fragile" for k in fcs["institutional_social_fragility"]}
    capf = json.loads((U / "v85" / "realdata" / "outputs" / "capacity.json").read_text())["regions"]
    tch = L87.series("SE.PRM.ENRL.TC.ZS", U / "v85" / "realdata" / "data" / "raw")
    out = {"years": YEARS, "scenarios": {}}
    for name, sc in SCEN.items():
        base = L87.B["scenarios"][sc["v87"]]
        gov_s = {} if sc.get("no_conflict") else gov
        rec = []
        phys, rows, built, ew = L87.physical_dates(regions, cty, base, record=rec, years=YEARS, boost=lambda t: automation(t, sc))
        food_com = next((r["year"] for r in rows if r["food_comfortable_for_all_feasible"]), 0)
        acc = {lvl: access_cov(cty, lvl, sc, gov_s) for lvl in ("essential", "comfortable")}
        keys = [k for k in cty if k in regions]
        W0 = sum(cty[k]["pop"] for k in keys)
        cov = {"L1": [], "L2": []}
        bottleneck = []
        car_fleet_needed = 1.29e9 * CAR_LACKING
        cars_built, prod = 0.0, 90e6
        for t in range(YEARS + 1):
            snap = rec[min(t, len(rec) - 1)]
            per_dom = {"L1": {}, "L2": {}}
            # teachers
            for k in keys:
                r = L87.latest(tch, k)[1]
                for lvl, L in (("essential", "L1"), ("comfortable", "L2")):
                    tgt = L87.B["domains"]["education"][f"{lvl}_pupils_per_teacher"]
                    if r is None or r <= tgt:
                        c = 1.0
                    else:
                        g = base["teacher_growth"] * automation(t, sc) ** 0.5 * gov_s.get(k, 1.0)
                        c = 1.0 if r / (1 + g) ** t <= tgt else 0.0
                    per_dom[L].setdefault("teachers", {})[k] = c
            # physical
            for k in keys:
                e_c, h_c, fl, e_e, h_e = snap[k]
                per_dom["L1"].setdefault("energy", {})[k] = 1.0 if e_e >= TOL else 0.0
                per_dom["L1"].setdefault("health", {})[k] = 1.0 if h_e >= TOL else 0.0
                per_dom["L1"].setdefault("housing", {})[k] = 1.0 if fl >= 15 * TOL else 0.0
                per_dom["L2"].setdefault("energy", {})[k] = 1.0 if e_c >= TOL else 0.0
                per_dom["L2"].setdefault("health", {})[k] = 1.0 if h_c >= TOL else 0.0
                per_dom["L2"].setdefault("housing", {})[k] = 1.0 if fl >= 27 * TOL else 0.0
                per_dom["L1"].setdefault("food", {})[k] = 1.0 if t >= 1 else 0.0
                per_dom["L2"].setdefault("food", {})[k] = 1.0 if t >= max(1, food_com) else 0.0
                per_dom["L2"].setdefault("goods", {})[k] = 1.0 if t >= 1 else 0.0
                # local services for Level 2 (savings, leisure, holidays, restaurants, culture)
                sv = capf.get(k, {}).get("services_vs_france")
                if sv is None:
                    sv = 0.3
                gap = max(0.0, math.log(SERVICES_L2 / sv)) if sv < SERVICES_L2 else 0.0
                level = sv
                for _ in range(t):
                    g = max(0.0, math.log(SERVICES_L2 / level)) if level < SERVICES_L2 else 0.0
                    level *= 1 + (0.01 + sc["service_catch_up"] * min(1.0, g)) * automation(t, sc) ** 0.5 * gov_s.get(k, 1.0)
                per_dom["L2"].setdefault("services", {})[k] = 1.0 if level >= SERVICES_L2 else level / SERVICES_L2 * 0  # binary
            for lvl, L in (("essential", "L1"), ("comfortable", "L2")):
                for dom, d in acc[lvl].items():
                    per_dom[L][dom] = {k: d[k][t] if k in d else 1.0 for k in keys}
            # mobility (Level 2): shared cars built for regions lacking them
            share_cars = min(1.0, cars_built / car_fleet_needed)
            # countries ordered by need (lowest services first get cars first)
            order = sorted(keys, key=lambda k: capf.get(k, {}).get("services_vs_france", 0.3))
            lacking_pop = CAR_LACKING * sum(cty[k]["pop"] for k in keys)
            served_pop = lacking_pop * share_cars   # people in car-lacking regions already given shared car access
            acc_pop, mob = 0.0, {}
            for k in order:  # regions with the greatest need are served first
                if acc_pop >= lacking_pop:
                    mob[k] = 1.0  # regions that already have cars
                else:  # share of this region's people already given shared car access (proportional at the boundary)
                    lacking_here = min(cty[k]["pop"], lacking_pop - acc_pop)
                    got = min(lacking_here, max(0.0, served_pop - acc_pop))
                    mob[k] = 1.0 - (lacking_here - got) / cty[k]["pop"]
                acc_pop += cty[k]["pop"]
            per_dom["L2"]["mobility"] = mob
            cars_built += prod * sc["car_share"]
            prod *= 1 + sc["car_growth"]
            # levels and bottleneck
            for L in ("L1", "L2"):
                doms = per_dom[L]
                covered = sum(cty[k]["pop"] * min(doms[d].get(k, 1.0) for d in doms) for k in keys) / W0
                cov[L].append(covered)
            entry = {"year": t}
            for L in ("L1", "L2"):
                short = {}
                for d, m in per_dom[L].items():
                    if t == 0 and d == "food":
                        continue  # delivery starts in year 1
                    short[d] = sum(cty[k]["pop"] * (1 - m.get(k, 1.0)) for k in keys)
                worst = max(short, key=short.get)
                people = short[worst]
                in_conflict = 0.0 if sc.get("no_conflict") else sum(cty[k]["pop"] * (1 - per_dom[L][worst].get(k, 1.0)) for k in keys if status.get(k) == "conflict")
                kind = ACCESS[worst][2] if worst in ACCESS else TYPE.get(worst, "other")
                if people and in_conflict / people > 0.5:
                    kind = "conflict"
                entry[L] = {"domain": worst, "type": kind, "people_short_m": round(people / 1e6),
                            "share_in_conflict_states": round(in_conflict / people, 2) if people else 0.0,
                            "all_domains_short_m": {d: round(v / 1e6) for d, v in sorted(short.items(), key=lambda x: -x[1])}}
            bottleneck.append(entry)
        dates = {L: {f"{int(100 * q)}pct": next((t for t, v in enumerate(cov[L]) if v >= q), None) for q in (0.9, 0.95, 0.99)} for L in cov}
        lab = L87.labour(base, regions, built, years=(0, 30, 60))
        res88 = E88.plan(E88.inventory(), 15, sc["scale"], "decentralised")
        infra_workers = sum(v["all_workers_needed_m"] for v in res88["services"].values())
        out["scenarios"][name] = {
            "dates": dates, "coverage_L1": [round(x, 4) for x in cov["L1"]], "coverage_L2": [round(x, 4) for x in cov["L2"]],
            "bottlenecks": bottleneck,
            "labour_hours_per_worker_week": {y: lab[y]["hours_per_worker_week"] for y in lab},
            "essential_infrastructure_construction": {"capital_usd_bn_per_year": res88["total_capital_usd_bn_per_year"],
                                                      "workers_m": round(infra_workers, 2),
                                                      "note": "construction only; operation and maintenance are already in the basket labour (v87 energy and water domain)"},
            "environment": {"world_final_energy_2050_ej": round(sum(40 * ew[k] * r["pop50"] for k, r in regions.items()) / 1e9),
                            "clean_cooking_energy_ej": round(1.92e9 * 0.5 / 1e9, 1),
                            "check": "energy within today's 409 EJ; housing needs low-carbon building; travel mostly rail (v87)"}}
        s = out["scenarios"][name]
        print(f"\n== {name}: Level 1 for 90/95/99% of humanity in year {dates['L1']['90pct']}/{dates['L1']['95pct']}/{dates['L1']['99pct']}; "
              f"Level 2 in year {dates['L2']['90pct']}/{dates['L2']['95pct']}/{dates['L2']['99pct']}")
        for t in (1, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80):
            b = bottleneck[t]
            print(f"   yr {t:2d}: L1 {100 * cov['L1'][t]:5.1f}% [{b['L1']['domain']}: {b['L1']['type']}, {b['L1']['people_short_m']} m] | "
                  f"L2 {100 * cov['L2'][t]:5.1f}% [{b['L2']['domain']}: {b['L2']['type']}, {b['L2']['people_short_m']} m, "
                  f"{100 * b['L2']['share_in_conflict_states']:.0f}% in conflict states]")
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "integrated.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
