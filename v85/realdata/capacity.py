"""UNIRA V8.5 — real production capacity by country: goods versus local services (replacing the uniform 24/76 split).

From World Bank data (latest year 2015-2024 per country): GDP per person (PPP), value added of agriculture, industry
and services (% of GDP), employment by sector, hospital beds and primary pupils per teacher.
    goods capacity per person    = GDP per person x (agriculture + industry share)
    services capacity per person = GDP per person x services share
each relative to France. Value added includes investment and exports, so these are capacities to PRODUCE, not
consumption; they replace the uniform split in the hybrid model (v84) by each region's real structure.
python3 capacity.py  ->  outputs/capacity.json, capacity.csv"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
CODES = ["NY.GDP.PCAP.PP.KD", "NV.AGR.TOTL.ZS", "NV.IND.TOTL.ZS", "NV.SRV.TOTL.ZS", "SL.AGR.EMPL.ZS", "SL.IND.EMPL.ZS",
         "SL.SRV.EMPL.ZS", "SH.MED.BEDS.ZS", "SE.PRM.ENRL.TC.ZS"]


def latest(code, since=2015):
    out = {}
    for x in json.loads((HERE / "data" / "raw" / f"wb_{code}.json").read_text())[1]:
        y = int(x["date"])
        if x["value"] is not None and x["countryiso3code"] and y >= since and y > out.get(x["countryiso3code"], (0, 0))[0]:
            out[x["countryiso3code"]] = (y, x["value"])
    return {k: v for k, (_, v) in out.items()}


def main():
    data = {c: latest(c) for c in CODES}
    meta = {m["id"]: m for m in json.loads((U / "v65" / "data" / "raw" / "wb_country_meta.json").read_text())[1]}
    pop = {}
    for x in json.loads((U / "v74" / "distribution" / "data" / "raw" / "wb_SP.POP.TOTL.json").read_text())[1]:
        if x["value"] and x["countryiso3code"] and int(x["date"]) == 2023:
            pop[x["countryiso3code"]] = x["value"]
    rows = {}
    for k in data["NY.GDP.PCAP.PP.KD"]:
        if k not in meta or meta[k]["region"]["value"].strip() == "Aggregates" or k not in pop:
            continue
        g = data["NY.GDP.PCAP.PP.KD"][k]
        a, i, s = (data[c].get(k) for c in ("NV.AGR.TOTL.ZS", "NV.IND.TOTL.ZS", "NV.SRV.TOTL.ZS"))
        if None in (a, i, s):
            continue
        tot = a + i + s  # shares exclude net taxes; renormalise
        rows[k] = {"region": meta[k]["region"]["value"].strip(), "income": meta[k]["incomeLevel"]["value"], "pop": pop[k],
                   "gdp_pc_ppp": g, "goods_pc": g * (a + i) / tot, "services_pc": g * s / tot,
                   "goods_share_of_production": (a + i) / tot,
                   "employment_agri_pct": data["SL.AGR.EMPL.ZS"].get(k), "employment_services_pct": data["SL.SRV.EMPL.ZS"].get(k),
                   "hospital_beds_per_1000": data["SH.MED.BEDS.ZS"].get(k), "pupils_per_teacher_primary": data["SE.PRM.ENRL.TC.ZS"].get(k)}
    fr = rows["FRA"]
    for r in rows.values():
        r["goods_vs_france"] = r["goods_pc"] / fr["goods_pc"]
        r["services_vs_france"] = r["services_pc"] / fr["services_pc"]
    W = sum(r["pop"] for r in rows.values())
    wavg = lambda key, sel=lambda r: True: sum(r[key] * r["pop"] for r in rows.values() if sel(r)) / sum(r["pop"] for r in rows.values() if sel(r))
    groups = sorted({r["income"] for r in rows.values()})
    out = {"countries": len(rows), "population_covered": W,
           "france": {k: fr[k] for k in ("gdp_pc_ppp", "goods_share_of_production", "employment_services_pct")},
           "world": {"goods_vs_france": wavg("goods_vs_france"), "services_vs_france": wavg("services_vs_france"),
                     "goods_share_of_production": wavg("goods_share_of_production")},
           "by_income_group": {g: {"goods_vs_france": wavg("goods_vs_france", lambda r, g=g: r["income"] == g),
                                   "services_vs_france": wavg("services_vs_france", lambda r, g=g: r["income"] == g),
                                   "goods_share_of_production": wavg("goods_share_of_production", lambda r, g=g: r["income"] == g),
                                   "population_share": sum(r["pop"] for r in rows.values() if r["income"] == g) / W} for g in groups},
           "regions": rows}
    (HERE / "outputs").mkdir(exist_ok=True)
    (HERE / "outputs" / "capacity.json").write_text(json.dumps(out, indent=2))
    with (HERE / "outputs" / "capacity.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["iso3"] + list(next(iter(rows.values()))))
        w.writeheader()
        for k, r in sorted(rows.items()):
            w.writerow({"iso3": k, **r})
    print(f"{len(rows)} countries, {W / 1e9:.2f} bn people")
    print("world (pop-weighted) vs France: goods %.2f, services %.2f; goods share of production %.2f (France %.2f)" % (
        out["world"]["goods_vs_france"], out["world"]["services_vs_france"], out["world"]["goods_share_of_production"], fr["goods_share_of_production"]))
    for g, v in out["by_income_group"].items():
        print(f"  {g:20s} pop {100 * v['population_share']:4.1f}% | goods {v['goods_vs_france']:.2f} | services {v['services_vs_france']:.2f} | goods share {v['goods_share_of_production']:.2f}")
    for k in ("USA", "CHN", "IND", "NGA", "ETH", "BRA", "EGY"):
        r = rows.get(k)
        if r:
            print(f"  {k}: goods {r['goods_vs_france']:.2f} services {r['services_vs_france']:.2f} beds {r['hospital_beds_per_1000']} pupils/teacher {r['pupils_per_teacher_primary']}")


if __name__ == "__main__":
    main()
