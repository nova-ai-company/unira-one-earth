"""UNIRA V8.4 — equal salaries with quotas (Q) versus converging salaries with an equality credit (D + C).

Same world in every scenario: 164 regions (World Bank), France's consumption per person as the full level F, strong
catch-up (+4%/yr extra growth below the full level, +1%/yr at it), UN population projections, 3% of goods kept as
reserves, supply shocks of -5% (years 5, 13, 21, 29, 37) and -10% (year 15), 80 years.
Consumption is split (France 2022, homes excluded, v81): GOODS 24% (food, energy, manufactured: can be shipped
between regions, can be stored) and LOCAL SERVICES 76% (shops, restaurants, transport, care, repairs, leisure:
produced only by each region's own workers).
    s1_DC        salaries converge (target 20 years) under the capacity rule, now limited by both world goods and
                 the region's own service capacity; 25% equality credit with a 2-year liability ceiling
    s2_DCQ       5,000 U for everyone from day one; goods shared by equal per-person quotas (needs-based in reality;
                 equal here); local services limited by local capacity; money that cannot be spent accumulates
    s3_hybrid    equal goods quotas from day one; the part of salaries meant for local services converges as local
                 service capacity grows (no equality credit needed for goods)
Measured: real consumption per person (goods + services) for the poorer and richer halves of humanity, the
population-weighted Gini of real consumption between regions, unspendable money (black-market pressure), the
richest regions' real consumption change, and the year the poorer half reaches 90% of the full level.
python3 compare.py  ->  ../outputs/quotas.json"""
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
spec = importlib.util.spec_from_file_location("wm", U / "v82" / "worldmoney" / "model.py")
wm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wm)

GOODS = 0.24
YEARS = 80
RESERVE = 0.03
EXTRA, RICH = 0.04, 0.01
SHOCKS = {5: 0.05, 13: 0.05, 15: 0.10, 21: 0.05, 29: 0.05, 37: 0.05}
CREDIT, CEILING, REL_T, REL_A = 0.25, 2.0, 0.05, 0.15


def gini(values, weights):
    pairs = sorted(zip(values, weights))
    tot_w = sum(weights)
    mean = sum(v * w for v, w in pairs) / tot_w
    cum_w = cum_vw = 0.0
    area = 0.0
    for v, w in pairs:
        prev = cum_vw
        cum_w += w
        cum_vw += v * w
        area += w * (prev + cum_vw) / 2
    return 1 - 2 * area / (tot_w * mean * tot_w) if mean else 0.0


def simulate(reg, scenario):
    F = reg["FRA"]["cons_pc"]
    keys = sorted(reg)
    cap = {k: reg[k]["cons_pc"] for k in keys}      # production capacity per person (goods + services), PPP
    f = {k: min(1.0, cap[k] / F) for k in keys}
    f0 = dict(f)
    credit = {k: 0.0 for k in keys}
    reserve = 0.0
    rows = []
    for t in range(YEARS + 1):
        pop = {k: reg[k]["pop"] + (reg[k]["pop2050"] - reg[k]["pop"]) * min(1.0, t / 27) for k in keys}
        shock = 1 - SHOCKS.get(t, 0.0)
        goods_made = sum(GOODS * cap[k] * pop[k] for k in keys) * shock
        reserve += RESERVE * goods_made
        goods_usable = goods_made * (1 - RESERVE)
        svc_cap = {k: (1 - GOODS) * cap[k] * pop[k] * shock for k in keys}  # local only
        W = sum(pop.values())
        if scenario == "s1_DC":
            stock = sum(credit.values())
            converged = rows and rows[-1]["mean_salary_factor"] >= 0.99
            release = min(stock, (REL_A if converged else REL_T) * goods_usable)
            for k in keys:
                credit[k] -= release * credit[k] / stock if stock else 0.0
            sched = {k: f0[k] + (1 - f0[k]) * min(1.0, t / 20) for k in keys}
            lo, hi = 0.0, 1.0
            for _ in range(40):  # world goods constraint
                mid = (lo + hi) / 2
                tf = {k: max(f[k], min(1.0, sched[k] * mid, svc_cap[k] / ((1 - GOODS) * F * pop[k]))) for k in keys}
                need = sum(tf[k] * GOODS * F * pop[k] for k in keys)
                lo, hi = (mid, hi) if need <= goods_usable - release else (lo, mid)
            for k in keys:
                f[k] = max(f[k], min(1.0, sched[k] * lo, svc_cap[k] / ((1 - GOODS) * F * pop[k])))
            years_out = sum(credit.values()) / (F * W)
            share = CREDIT if years_out < CEILING else 0.0
            for k in keys:
                credit[k] += share * (1 - f[k]) * F * pop[k]
            goods_pc = {k: f[k] * GOODS * F for k in keys}
            svc_pc = {k: min(f[k] * (1 - GOODS) * F, svc_cap[k] / pop[k]) for k in keys}
            income = {k: f[k] * F for k in keys}
            extra_goods_for_credits = release
        else:
            # equal goods quota for everyone (capped at the full level's goods)
            q = min(GOODS * F, goods_usable / W)
            goods_pc = {k: q for k in keys}
            if scenario == "s2_DCQ":
                income = {k: F for k in keys}                         # 5,000 U scale everywhere
                svc_pc = {k: min((1 - GOODS) * F, svc_cap[k] / pop[k]) for k in keys}
            else:  # hybrid: service part of income converges with local service capacity
                sf = {k: min(1.0, svc_cap[k] / ((1 - GOODS) * F * pop[k])) for k in keys}
                income = {k: q + sf[k] * (1 - GOODS) * F for k in keys}
                svc_pc = {k: sf[k] * (1 - GOODS) * F for k in keys}
            for k in keys:
                f[k] = income[k] / F
            extra_goods_for_credits = 0.0
        real = {k: goods_pc[k] + svc_pc[k] for k in keys}
        unspent = {k: max(0.0, income[k] - real[k]) for k in keys}
        order = sorted(keys, key=lambda k: cap[k])
        half, acc, poor = W / 2, 0.0, []
        for k in order:
            if acc < half:
                poor.append(k)
            acc += pop[k]
        rich = [k for k in keys if k not in poor]
        avg = lambda ks: sum(real[k] * pop[k] for k in ks) / sum(pop[k] for k in ks)
        top = sorted(keys, key=lambda k: -reg[k]["cons_pc"])[:20]
        rows.append({"year": t, "real_poorer_half_vs_full": avg(poor) / F, "real_richer_half_vs_full": avg(rich) / F,
                     "real_world_vs_full": sum(real[k] * pop[k] for k in keys) / (W * F),
                     "gini_real_between_regions": gini([real[k] for k in keys], [pop[k] for k in keys]),
                     "unspendable_money_share_of_income": sum(unspent[k] * pop[k] for k in keys) / sum(income[k] * pop[k] for k in keys),
                     "richest20_real_vs_today": sum(real[k] * pop[k] for k in top) / sum(min(reg[k]["cons_pc"], 10 * F) * pop[k] for k in top),
                     "mean_salary_factor": sum(f[k] * pop[k] for k in keys) / W,
                     "credit_outstanding_years": sum(credit.values()) / (F * W),
                     "reserve_years_of_goods": reserve / max(goods_made, 1e-9)})
        for k in keys:  # capacity growth
            gap = max(0.0, math.log(F / cap[k])) if cap[k] < F else 0.0
            cap[k] *= 1 + RICH + EXTRA * min(1.0, gap)
    reach = next((r["year"] for r in rows if r["real_poorer_half_vs_full"] >= 0.9), None)
    pick = lambda y: {k: round(v, 3) for k, v in rows[y].items()}
    return {"year_poorer_half_reaches_90pct": reach, "year_0": pick(0), "year_10": pick(10), "year_20": pick(20),
            "year_40": pick(40), "year_80": pick(80)}


def main():
    reg = wm.regions()
    out = {"goods_share": GOODS, "assumptions": {"catch_up": EXTRA, "rich_growth": RICH, "reserve": RESERVE, "shocks": SHOCKS},
           "scenarios": {}}
    for s in ("s1_DC", "s2_DCQ", "s3_hybrid"):
        r = simulate(reg, s)
        out["scenarios"][s] = r
        print(f"\n{s}: poorer half reaches 90% of full level in year {r['year_poorer_half_reaches_90pct']}")
        for y in ("year_0", "year_10", "year_20", "year_40"):
            x = r[y]
            print(f"  {y:7s} poorer half {100 * x['real_poorer_half_vs_full']:.0f}% | richer half {100 * x['real_richer_half_vs_full']:.0f}% | "
                  f"Gini {x['gini_real_between_regions']:.2f} | unspendable money {100 * x['unspendable_money_share_of_income']:.0f}% | "
                  f"richest 20 vs today {100 * x['richest20_real_vs_today']:.0f}% | credits {x['credit_outstanding_years']:.2f}")
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "quotas.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
