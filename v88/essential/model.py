"""UNIRA V8.8 — a targeted programme: universal safe water, sanitation and clean cooking in 5, 10 or 15 years?

Inventory: people without access, by country (World Bank / JMP / WHO data, latest year; v87 raw data):
basic drinking water, safely managed drinking water, basic sanitation, clean cooking.
Means, in UNIRA's order: repair and restore existing water points first, then build; decentralised and
centralised options compared (evidence.csv). Governance: World Bank FY26 fragile and conflict-affected list.
Delivery is what counts: people durably served (functioning services), not money spent.

Resources per person newly served (2011 USD capital, ASSUMPTION ranges from evidence.csv):
    water, basic:        repair 30% of new cost for the share served by restoring broken points; borehole/handpump
                         40 (decentralised) or small piped scheme 80 (centralised); upkeep 4.5 / 9 a year
    water, safely managed: piped on premises with treatment 150 (centralised) or household/community treatment plus
                         protected source 70 (decentralised); upkeep 12 / 8 a year
    sanitation, basic:   improved pit or pour-flush 40 (decentralised) or sewer connection with treatment 500
                         (centralised, ASSUMPTION: no per-person sewer benchmark found); upkeep 3 / 25 a year
    clean cooking:       stove and start-up about 25 (IEA: about USD 8 bn a year for ~2.3 bn people by 2030); fuel or
                         electricity is metered energy (about 0.5 GJ per person a year, ASSUMPTION)
Labour: half of capital cost is local work at about 5 USD per hour (ASSUMPTION), of which a third skilled.
Delivery capacity per country and year = population x (best yearly coverage gain achieved by lagging countries,
v87) x programme scale (1x, 2x, 3x: resources mobilised by One Earth) x governance factor
(conflict 0.5, institutional fragility 0.75, others 1.0; informed by IEG outcome ratings and access limits).
Corruption: extra resources needed 26% in fragile and conflict states, 10% elsewhere (WIN 2024 / 2016).
Durability: without local participation and maintenance, 25% of new rural water points are out of order at any time
(Foster et al. 2019); with community operation and funded maintenance, 10% (ASSUMPTION).
python3 model.py  ->  ../outputs/essential.json"""
import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
RAW87 = U / "v87" / "livingstandard" / "data" / "raw"
SERVICES = {"basic_water": "SH.H2O.BASW.ZS", "safe_water": "SH.H2O.SMDW.ZS", "basic_sanitation": "SH.STA.BASS.ZS",
            "clean_cooking": "EG.CFT.ACCS.ZS"}
COST = {  # (capital per person, upkeep per person-year) by option
    "basic_water": {"decentralised": (40, 4.5), "centralised": (80, 9.0)},
    "safe_water": {"decentralised": (70, 8.0), "centralised": (150, 12.0)},
    "basic_sanitation": {"decentralised": (40, 3.0), "centralised": (500, 25.0)},
    "clean_cooking": {"decentralised": (25, 0.0), "centralised": (25, 0.0)}}
REPAIR_SHARE, REPAIR_COST = 0.15, 0.30   # ASSUMPTION: 15% of the unserved in water reachable by restoring broken points
GOV = {"conflict": 0.5, "fragile": 0.75, "other": 1.0}
SPEED = {"decentralised": 1.0, "centralised": 0.6}  # ASSUMPTION: networks need longer planning and construction
CORRUPTION = {"conflict": 0.26, "fragile": 0.26, "other": 0.10}
LABOUR_SHARE, WAGE, SKILLED = 0.5, 5.0, 1 / 3
WORLD_GDP_USD_BN = 105_000   # ASSUMPTION: rounded world GDP, nominal, about 2023
MILITARY_USD_BN = 2_887      # SIPRI (2026) world military spending 2025 (project bibliography, sipri2026milex)


def series(code, folder=RAW87):
    out = {}
    for x in json.loads((folder / f"wb_{code}.json").read_text())[1]:
        if x["value"] is not None and x["countryiso3code"]:
            out.setdefault(x["countryiso3code"], {})[int(x["date"])] = x["value"]
    return out


def latest(s, k):
    ys = sorted(s.get(k, {}))
    return (ys[-1], s[k][ys[-1]]) if ys else (None, None)


def inventory():
    meta = {m["id"]: m for m in json.loads((U / "v65" / "data" / "raw" / "wb_country_meta.json").read_text())[1]}
    pop = series("SP.POP.TOTL", U / "v74" / "distribution" / "data" / "raw")
    fcs = json.loads((HERE / "data" / "raw" / "fcs_fy26.json").read_text())
    status = {k: "conflict" for k in fcs["conflict"]} | {k: "fragile" for k in fcs["institutional_social_fragility"]}
    out = {}
    for svc, code in SERVICES.items():
        s = series(code)
        gains = []
        for k in s:
            y1, v1 = latest(s, k)
            if y1 and 2010 in s[k] and s[k][2010] < 99 and y1 > 2010 and v1 > s[k][2010]:
                gains.append((v1 - s[k][2010]) / (y1 - 2010))
        best = sorted(gains)[int(0.9 * (len(gains) - 1))] if gains else 2.0  # top tenth of real gains
        for k, m in meta.items():
            if m["region"]["value"].strip() == "Aggregates":
                continue
            y, v = latest(s, k)
            p = latest(pop, k)[1]
            if v is None or not p or v >= 99:
                continue
            out.setdefault(k, {"name": m["name"], "status": status.get(k, "other"), "pop": p})[svc] = {
                "coverage": v, "unserved_m": p * (99 - v) / 100 / 1e6, "best_gain_points": best}
    return out


def plan(inv, years, scale, option, participation=True, gov=None):
    gov = gov or GOV
    res = {"years": years, "scale": scale, "option": option, "participation": participation, "services": {}}
    for svc in SERVICES:
        served = unserved = capex = upkeep = labour_h = 0.0
        stuck = []
        for k, c in inv.items():
            x = c.get(svc)
            if not x:
                continue
            need = x["unserved_m"]
            cap_per_year = c["pop"] / 1e6 * x["best_gain_points"] / 100 * scale * gov[c["status"]] * SPEED[option]
            reach = min(need, cap_per_year * years)
            decay = 0.10 if participation else 0.25
            durable = reach * (1 - decay) if svc in ("basic_water", "safe_water") else reach * (1 - decay / 2)
            unserved += need
            served += durable
            if durable < 0.95 * need and need > 1:
                stuck.append((round(need - durable, 1), k, c["status"]))
            cost, up = COST[svc][option]
            rep = REPAIR_SHARE if svc in ("basic_water",) else 0.0
            per_person = cost * (rep * REPAIR_COST + (1 - rep)) * (1 + CORRUPTION[c["status"]])
            capex += reach * 1e6 * per_person
            upkeep += reach * 1e6 * up
            labour_h += reach * 1e6 * per_person * LABOUR_SHARE / WAGE
        stuck.sort(reverse=True)
        yrs = years
        res["services"][svc] = {"unserved_m": round(unserved), "durably_served_m": round(served),
                                "share_reached": round(served / unserved, 3) if unserved else 1.0,
                                "capital_usd_bn_per_year": round(capex / 1e9 / yrs, 1), "upkeep_usd_bn_per_year_at_end": round(upkeep / 1e9, 1),
                                "skilled_workers_needed_m": round(labour_h * SKILLED / yrs / 1800 / 1e6, 2),
                                "all_workers_needed_m": round(labour_h / yrs / 1800 / 1e6, 2),
                                "largest_remaining_gaps": [{"country": k, "status": st, "people_m": g} for g, k, st in stuck[:8]]}
    tot = sum(v["capital_usd_bn_per_year"] for v in res["services"].values())
    res["total_capital_usd_bn_per_year"] = round(tot, 1)
    res["share_of_world_gdp"] = round(tot / WORLD_GDP_USD_BN, 5)
    res["share_of_world_military_spending"] = round(tot / MILITARY_USD_BN, 3)
    return res


def main():
    inv = inventory()
    top = {}
    for svc in SERVICES:
        top[svc] = sorted(((round(c[svc]["unserved_m"], 1), k, c["status"]) for k, c in inv.items() if svc in c), reverse=True)[:10]
    out = {"inventory_top_unserved": {s: [{"country": k, "people_m": m, "status": st} for m, k, st in v] for s, v in top.items()},
           "totals_unserved_m": {s: round(sum(c[s]["unserved_m"] for c in inv.values() if s in c)) for s in SERVICES},
           "plans": {}}
    print("people without access (millions):", out["totals_unserved_m"])
    for s, v in top.items():
        print(f"  {s:17s}", ", ".join(f"{k} {m:.0f}m ({st})" for m, k, st in v[:7]))
    for years in (5, 10, 15):
        for scale in (1, 2, 3):
            for option in ("decentralised", "centralised"):
                r = plan(inv, years, scale, option)
                key = f"{years}y/scale{scale}/{option}"
                out["plans"][key] = r
                if option == "decentralised" or scale == 2:
                    sv = r["services"]
                    print(f"{key:28s} reached: water {100 * sv['basic_water']['share_reached']:.0f}% | safe water {100 * sv['safe_water']['share_reached']:.0f}% | "
                          f"sanitation {100 * sv['basic_sanitation']['share_reached']:.0f}% | cooking {100 * sv['clean_cooking']['share_reached']:.0f}% | "
                          f"capital {r['total_capital_usd_bn_per_year']} bn/yr ({100 * r['share_of_world_gdp']:.2f}% of world GDP, "
                          f"{100 * r['share_of_world_military_spending']:.0f}% of military spending)")
    # what programme scale (multiple of the best historical pace) would reach 95% of the unserved?
    out["scale_needed_for_95pct"] = {}
    for years in (5, 10, 15):
        for label, gov in (("with_conflict_limits", GOV), ("if_conflict_and_fragility_lifted", {"conflict": 1.0, "fragile": 1.0, "other": 1.0})):
            need = {}
            for svc in SERVICES:
                lo, hi = 0.5, 60.0
                for _ in range(40):
                    mid = (lo + hi) / 2
                    ok = plan(inv, years, mid, "decentralised", True, gov)["services"][svc]["share_reached"] >= 0.95 * 0.9
                    lo, hi = (lo, mid) if ok else (mid, hi)
                need[svc] = round(hi, 1) if hi < 59 else None
            out["scale_needed_for_95pct"][f"{years}y/{label}"] = need
            print(f"scale needed (x best historical pace) to reach 95% of the unserved durably in {years} yrs, {label}: {need}")
    # without local participation (durability falls)
    r = plan(inv, 10, 2, "decentralised", participation=False)
    out["plans"]["10y/scale2/decentralised/no_participation"] = r
    print("10y scale2 decentralised WITHOUT local participation: water", r["services"]["basic_water"]["share_reached"],
          "sanitation", r["services"]["basic_sanitation"]["share_reached"])
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "essential.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
