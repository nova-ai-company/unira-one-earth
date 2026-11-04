"""UNIRA V8.3 — the D + C transition with an equality credit (author's decisions, 2026-11-04).

D (real economy): rights and essentials guaranteed in kind from day one; redistribute and repair first.
C (money): regional salary scales rise with sustainable, accessible supply; aggregate purchasing power never
persistently exceeds supply. Safeguard 4: part of supply is kept as reserves (RESERVE_MARGIN).
Compensation (accepted): while a region's salary factor f < 1, each worker accrues an EQUALITY CREDIT equal to a share
s of the gap (1 - f) x full scale, in a protected account. Credits are paid out gradually: at most RELEASE_CAP of
usable world supply per year goes to credit payouts; salaries share the rest under the capacity rule (v82 T-8).
Shares tested: 0%, 25%, 50%, 100%. Catch-up scenarios as in v82/worldmoney.
Measured: year the full salary scale is reached, credit stock at its peak (years of full consumption per person in
the regions concerned), year all credits are paid, and real equality of lifetime purchasing power.
python3 model.py  ->  ../outputs/equality_credit.json"""
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
spec = importlib.util.spec_from_file_location("wm", U / "v82" / "worldmoney" / "model.py")
wm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wm)

RESERVE_MARGIN = 0.03   # SYNTHETIC: 3% of supply each year kept for reserves and emergency capacity (safeguard 4)
RELEASE_CAP = 0.05      # SYNTHETIC: at most 5% of usable world supply per year pays out equality credits
RELEASE_CAP_AFTER = 0.15  # SYNTHETIC: once salaries are equal everywhere, up to 15% a year (variant "faster release")
HORIZON = 80
SHARES = (0.0, 0.25, 0.5, 1.0)


def run(reg, extra, share, cap_after=RELEASE_CAP, rich_growth=None, pop_scale=1.0, shocks=None, lag_regions=None,
        liability_ceiling=None):
    """Stress options: rich_growth (yearly growth at full level), pop_scale (multiplies projected population change),
    shocks {year: share of world supply lost that year}, lag_regions {iso: factor on catch-up speed},
    liability_ceiling: while outstanding credits are at or above this many years of world consumption, new accrual
    pauses (automatic review: promises stay payable)."""
    rich_growth = wm.RICH_GROWTH if rich_growth is None else rich_growth
    shocks, lag_regions = shocks or {}, lag_regions or {}
    full = reg["FRA"]["cons_pc"]
    st = {k: {"supply_pc": r["cons_pc"], "f0": min(1.0, r["cons_pc"] / full), "f": min(1.0, r["cons_pc"] / full),
              "credit": 0.0} for k, r in reg.items()}
    rows = []
    reserve = 0.0          # stock of goods built from the reserve margin (safeguard 4)
    shortage_years = 0
    worst_shortage = 0.0
    for t in range(HORIZON + 1):
        pop = {k: r["pop"] + pop_scale * (r["pop2050"] - r["pop"]) * min(1.0, t / 27) for k, r in reg.items()}
        produced = sum(st[k]["supply_pc"] * pop[k] for k in st) * (1 - shocks.get(t, 0.0))
        reserve += RESERVE_MARGIN * produced
        usable = produced * (1 - RESERVE_MARGIN)
        stock = sum(s["credit"] for s in st.values())
        converged = rows and rows[-1]["mean_salary_factor"] >= 0.99
        release = min(stock, (cap_after if converged else RELEASE_CAP) * usable)
        for s in st.values():  # payouts in proportion to each region's credit stock
            s["credit"] -= release * s["credit"] / stock if stock > 0 else 0.0
        for_salaries = usable - release
        sched = {k: st[k]["f0"] + (1 - st[k]["f0"]) * min(1.0, t / 20) for k in st}
        lo, hi = 0.0, 1.0
        for _ in range(50):
            mid = (lo + hi) / 2
            need = sum(max(st[k]["f0"], min(1.0, sched[k] * mid)) * full * pop[k] for k in st)
            lo, hi = (mid, hi) if need <= for_salaries else (lo, mid)
        eff_share = share
        if liability_ceiling:
            years_out = sum(s["credit"] for s in st.values()) / (full * sum(pop.values()))
            eff_share = share if years_out < liability_ceiling else 0.0  # hard ceiling: accrual pauses at the limit
        for k in st:
            st[k]["f"] = max(st[k]["f"], st[k]["f0"], min(1.0, sched[k] * lo))  # salaries are never cut
            st[k]["credit"] += eff_share * (1 - st[k]["f"]) * full * pop[k]  # accrues this year
        demand = sum(st[k]["f"] * full * pop[k] for k in st)
        short = max(0.0, demand - for_salaries)
        draw = min(reserve, short)            # reserves cover a shock first
        reserve -= draw
        if short - draw > 1e-9 * demand:
            shortage_years += 1
            worst_shortage = max(worst_shortage, (short - draw) / demand)
        world_pop = sum(pop.values())
        behind = [k for k in st if st[k]["f"] < 0.999]
        rows.append({"year": t, "mean_salary_factor": sum(st[k]["f"] * pop[k] for k in st) / world_pop,
                     "credit_stock_years_of_full_consumption_world": sum(s["credit"] for s in st.values()) / (full * world_pop),
                     "credit_release_share_of_supply": release / usable if usable else 0.0,
                     "people_behind_share": sum(pop[k] for k in behind) / world_pop})
        for k, s in st.items():
            gap = max(0.0, math.log(full / s["supply_pc"])) if s["supply_pc"] < full else 0.0
            s["supply_pc"] *= 1 + rich_growth + extra * lag_regions.get(k, 1.0) * min(1.0, gap)
    full_year = next((r["year"] for r in rows if r["mean_salary_factor"] >= 0.99), None)
    paid_year = next((r["year"] for r in rows if full_year is not None and r["year"] > full_year
                      and r["credit_stock_years_of_full_consumption_world"] < 0.01), None) if share else full_year
    peak = max(rows, key=lambda r: r["credit_stock_years_of_full_consumption_world"])
    slowest = None
    return {"year_full_salary_scale": full_year, "year_credits_paid": paid_year,
            "shortage_years_after_reserves": shortage_years, "worst_shortage_share": round(worst_shortage, 4),
            "peak_credit_stock_years_of_world_consumption": round(peak["credit_stock_years_of_full_consumption_world"], 3),
            "peak_year": peak["year"], "mean_salary_factor_year_20": round(rows[20]["mean_salary_factor"], 3),
            "path": [{k: round(v, 4) if isinstance(v, float) else v for k, v in r.items()} for r in rows[:61]]}


def main():
    reg = wm.regions()
    out = {"reserve_margin": RESERVE_MARGIN, "release_cap": RELEASE_CAP, "results": {}}
    for name, extra in (("strong_catch_up", 0.04), ("very_strong_catch_up", 0.06)):
        for s, cap_after in [(x, RELEASE_CAP) for x in SHARES] + [(x, RELEASE_CAP_AFTER) for x in SHARES[1:]]:
            r = run(reg, extra, s, cap_after)
            tag = "" if cap_after == RELEASE_CAP else "/faster_release_after_equal_salaries"
            out["results"][f"{name}/credit_{int(100 * s)}pct{tag}"] = r
            print(f"{name:22s} credit {int(100 * s):3d}%{'+fast' if tag else '     '} | full scale year {r['year_full_salary_scale']} | credits paid by year {r['year_credits_paid']} "
                  f"| peak credit stock {r['peak_credit_stock_years_of_world_consumption']} yrs of world consumption (yr {r['peak_year']}) "
                  f"| mean salary factor yr 20 {r['mean_salary_factor_year_20']}")
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "equality_credit.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
