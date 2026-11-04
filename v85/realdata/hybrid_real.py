"""UNIRA V8.5 — the hybrid D + Q + C (and D + C) rerun with each country's REAL goods and services capacity.

Instead of one goods/services split for every region (v84: 24/76 from France), each region starts with its measured
capacity relative to France (capacity.py, World Bank): goods (agriculture + industry) and local services, per person.
Demand at the full level keeps France's consumption composition (24% goods, 76% services). Capacities in consumption
units: goods = 0.24 F x goods_vs_france, services = 0.76 F x services_vs_france. Each grows with catch-up toward the
full level (+1%/yr at it, plus EXTRA x gap below it), separately for goods and services. 3% of goods kept as reserves;
supply shocks as in v84; UN population projections (v82 regions); 80 years.
    hybrid  equal needs-based goods quotas from day one (shipped between regions) + local services by local capacity
    DC      no quotas: each region's goods and services follow its own converging salary (capacity rule)
python3 hybrid_real.py  ->  outputs/hybrid_real.json"""
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
spec = importlib.util.spec_from_file_location("wm", U / "v82" / "worldmoney" / "model.py")
wm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wm)
GOODS, RESERVE, RICH, YEARS = 0.24, 0.03, 0.01, 80
SHOCKS = {5: 0.05, 13: 0.05, 15: 0.10, 21: 0.05, 29: 0.05, 37: 0.05}


def gini(values, weights):
    pairs = sorted(zip(values, weights))
    tw = sum(weights)
    mean = sum(v * w for v, w in pairs) / tw
    cw = cvw = area = 0.0
    for v, w in pairs:
        prev = cvw
        cvw += v * w
        area += w * (prev + cvw) / 2
    return 1 - 2 * area / (tw * mean * tw)


def simulate(reg, capf, scenario, extra=0.04, services_extra=None):
    """capf: {iso: (goods_vs_france, services_vs_france)}. services_extra: catch-up for services if different."""
    services_extra = extra if services_extra is None else services_extra
    F = reg["FRA"]["cons_pc"]
    keys = sorted(k for k in reg if k in capf)
    g = {k: GOODS * F * capf[k][0] for k in keys}
    s = {k: (1 - GOODS) * F * capf[k][1] for k in keys}
    rows = []
    for t in range(YEARS + 1):
        pop = {k: reg[k]["pop"] + (reg[k]["pop2050"] - reg[k]["pop"]) * min(1.0, t / 27) for k in keys}
        W = sum(pop.values())
        shock = 1 - SHOCKS.get(t, 0.0)
        goods_usable = sum(g[k] * pop[k] for k in keys) * shock * (1 - RESERVE)
        if scenario == "hybrid":
            q = min(GOODS * F, goods_usable / W)
            goods_pc = {k: q for k in keys}
        else:  # each region consumes its own goods capacity up to the full level (no sharing)
            local = {k: min(GOODS * F, g[k] * shock * (1 - RESERVE)) for k in keys}
            goods_pc = local
        svc_pc = {k: min((1 - GOODS) * F, s[k] * shock) for k in keys}
        real = {k: goods_pc[k] + svc_pc[k] for k in keys}
        order = sorted(keys, key=lambda k: real[k])
        acc, poor = 0.0, []
        for k in order:
            if acc < W / 2:
                poor.append(k)
            acc += pop[k]
        avg = lambda ks: sum(real[k] * pop[k] for k in ks) / sum(pop[k] for k in ks)
        rows.append({"year": t, "poorer_half_vs_full": avg(poor) / F, "world_vs_full": avg(keys) / F,
                     "goods_quota_vs_full_goods": (goods_usable / W) / (GOODS * F),
                     "poorer_half_services_vs_full": sum(svc_pc[k] * pop[k] for k in poor) / (sum(pop[k] for k in poor) * (1 - GOODS) * F),
                     "gini": gini([real[k] for k in keys], [pop[k] for k in keys])})
        for k in keys:
            for d, full_lvl, ex in ((g, GOODS * F, extra), (s, (1 - GOODS) * F, services_extra)):
                gap = max(0.0, math.log(full_lvl / d[k])) if d[k] < full_lvl else 0.0
                d[k] *= 1 + RICH + ex * min(1.0, gap)
    reach = next((r["year"] for r in rows if r["poorer_half_vs_full"] >= 0.9), None)
    pick = lambda y: {k: round(v, 3) for k, v in rows[y].items()}
    return {"year_poorer_half_90pct": reach, "year_0": pick(0), "year_20": pick(20), "year_40": pick(40)}


def main():
    reg = wm.regions()
    cap = json.loads((HERE / "outputs" / "capacity.json").read_text())["regions"]
    capf = {k: (v["goods_vs_france"], v["services_vs_france"]) for k, v in cap.items() if k in reg}
    out = {"regions": len(capf), "results": {}}
    for scen in ("hybrid", "DC"):
        for label, kw in (("strong", {"extra": 0.04}), ("very_strong", {"extra": 0.06}),
                          ("services_slower", {"extra": 0.04, "services_extra": 0.02})):
            r = simulate(reg, capf, scen, **kw)
            out["results"][f"{scen}/{label}"] = r
            y0, y20, y40 = r["year_0"], r["year_20"], r["year_40"]
            print(f"{scen:6s} {label:16s} poorer half yr0/20/40 {100 * y0['poorer_half_vs_full']:.0f}/{100 * y20['poorer_half_vs_full']:.0f}/"
                  f"{100 * y40['poorer_half_vs_full']:.0f}% | services of poorer half yr0 {100 * y0['poorer_half_services_vs_full']:.0f}% | "
                  f"goods quota yr0 {100 * y0['goods_quota_vs_full_goods']:.0f}% of full | Gini yr0 {y0['gini']:.2f} | 90% in yr {r['year_poorer_half_90pct']}")
    (HERE / "outputs" / "hybrid_real.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
