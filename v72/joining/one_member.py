"""UNIRA V7.2 — the one-member economy: what the first member faces at its border, in its reserves and at the top of
its pay scale (author, 2026-11-08: "Go").

For the regions that pass the first-region screen (and, for comparison, every region with data), from frozen World Bank
series (data/raw, hashes in raw_manifest.csv) and the project's own results:
  1. Trade and reserves today: exports and imports of goods and services, the balance, total reserves in months of
     imports, and the share of merchandise imports that is food, fuel and ores and metals (a floor for the "essential
     imports" of Article 12b.3; medicines and equipment are not in the series).
  2. The five-year balance test of Article 12b.2 and the six-month reserve of 12b.4: a foreign-currency stock-flow,
         R[t+1] = R[t] + X(1 - shock) - M(1 + needs) + remittances,
     with export shocks (market partners' reaction, loss of competitiveness while prices realign) of 0, 10, 25 and 40%
     and a needs-first import surge of 0 or 10%; the year reserves fall below six months of essential imports, and the
     export growth needed to balance over five years.
  3. The price wedge at the border: the ratio of the PPP conversion factor to the market exchange rate (how cheap the
     region's goods are today in world prices). Inside UNIRA prices are set from embodied hours at one world hour price,
     so the region's tradeable goods are re-priced toward world levels; the wedge measures the size of that re-pricing
     and the arbitrage incentive at the border (times openness). The Trade Office sells exports at world prices and
     buys imports at world prices whatever the internal U price (12b), so the wedge is a smuggling incentive, not a
     trade loss.
  4. Emigration at the top of the pay scale: the share of people whose income exceeds the UNIRA ceiling (5 x the base
     salary), from World Bank income shares (top 10% and top 20%) with a Pareto tail fitted to the top decile.
It is a stock-flow exposure test, not a forecast; nothing here says a region would vote to join.
python3 one_member.py  ->  ../outputs/one_member.json
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
U = ROOT.parents[1]
RAW = ROOT / "data" / "raw"
RAW74 = U / "v74" / "distribution" / "data" / "raw"
sys.path[:0] = [str(U / "v68" / "counterfactual"), str(U / "v67"), str(U / "v66" / "model")]
import compare  # noqa: E402

CEILING_MULTIPLE = 5.0  # Article 14: multipliers up to 5x the base salary
ESSENTIAL_RESERVE_MONTHS = 6  # Article 12b.4
BALANCE_YEARS = 5  # Article 12b.2
EXPORT_SHOCKS = (0.0, 0.10, 0.25, 0.40)
NEEDS_SURGES = (0.0, 0.10)
HORIZON = 10


def latest(path, year_min="2015"):
    out = {}
    for r in json.loads(Path(path).read_text())[1]:
        if r["value"] is None or not r["countryiso3code"] or r["date"] < year_min:
            continue
        k = r["countryiso3code"]
        if k not in out or r["date"] > out[k][0]:
            out[k] = (r["date"], float(r["value"]))
    return {k: v for k, (d, v) in out.items()}


def pareto_share_above(top10_share, top20_share, threshold_vs_mean):
    """Share of people with income above `threshold_vs_mean` x the mean, from a Pareto tail fitted to the top decile.
    top10/top20 = shares of total income held by the top 10% and 20%. Returns (share_above, alpha)."""
    s10, s20 = top10_share / 100, top20_share / 100
    if not (0 < s10 < s20 < 1):
        return None, None
    ratio = s10 / s20  # for a Pareto tail, share(top p)/share(top 2p) = 2^(-(1 - 1/alpha))
    expo = -math.log(ratio) / math.log(2)  # = 1 - 1/alpha
    if expo <= 0 or expo >= 1:
        return None, None
    alpha = 1 / (1 - expo)
    mean_top10 = s10 / 0.10  # in units of the overall mean
    x10 = mean_top10 * (alpha - 1) / alpha  # 90th-percentile income (Pareto mean = alpha/(alpha-1) x threshold)
    if threshold_vs_mean <= x10:
        return 0.10, alpha  # the whole top decile is above the threshold (not the case here)
    return 0.10 * (threshold_vs_mean / x10) ** (-alpha), alpha


def reserve_path(X, M, rem, ess_months_bill, shock, surge, years=HORIZON, R0=0.0):
    R, breach = R0, None
    path = []
    for t in range(1, years + 1):
        R = R + X * (1 - shock) - M * (1 + surge) + rem
        path.append(R)
        if breach is None and R < ess_months_bill:
            breach = t
    return path, breach


def main(write=True):
    regions = compare.rt.load_regions()
    fr = json.loads((U / "v72" / "outputs" / "first_region.json").read_text())
    candidates = [r["region"] for r in fr["candidates"]]
    v74 = json.loads((U / "v74" / "outputs" / "distribution_world.json").read_text())["regions"]
    X = latest(RAW / "wb_NE.EXP.GNFS.CD.json"); M = latest(RAW / "wb_NE.IMP.GNFS.CD.json")
    GDP = latest(RAW / "wb_NY.GDP.MKTP.CD.json"); RES = latest(RAW / "wb_FI.RES.TOTL.CD.json")
    REM = latest(RAW / "wb_BX.TRF.PWKR.CD.DT.json")
    FOOD = latest(RAW / "wb_TM.VAL.FOOD.ZS.UN.json"); FUEL = latest(RAW / "wb_TM.VAL.FUEL.ZS.UN.json"); ORES = latest(RAW / "wb_TM.VAL.MMTL.ZS.UN.json")
    PPP = latest(RAW / "wb_PA.NUS.PPP.json"); FX = latest(RAW / "wb_PA.NUS.FCRF.json")
    S10 = latest(RAW74 / "wb_SI.DST.10TH.10.json", "2005"); S20 = latest(RAW74 / "wb_SI.DST.05TH.20.json", "2005")
    rows = {}
    for k in regions:
        if not all(k in d for d in (X, M, GDP)):
            continue
        ess_share = None
        if k in FOOD and k in FUEL and k in ORES:
            ess_share = min(1.0, (FOOD[k] + FUEL[k] + ORES[k]) / 100)
        res_months = 12 * RES[k] / M[k] if k in RES else None
        ess_bill = M[k] * (ess_share if ess_share is not None else 0.35)  # France: essentials 36% of imports (V8.2), fallback
        ess6 = ess_bill * ESSENTIAL_RESERVE_MONTHS / 12
        wedge = (PPP[k] / FX[k]) if (k in PPP and k in FX and FX[k] > 0) else None  # price level vs US (1 = world prices)
        base_vs_mean = v74.get(k, {}).get("unira_base_vs_region_mean")
        top = {}
        if k in S10 and k in S20 and base_vs_mean:
            share_above, alpha = pareto_share_above(S10[k], S20[k], CEILING_MULTIPLE * base_vs_mean)
            top = {"top10_income_share_pct": round(S10[k], 1), "top20_income_share_pct": round(S20[k], 1),
                   "pareto_alpha": None if alpha is None else round(alpha, 2),
                   "ceiling_vs_region_mean": round(CEILING_MULTIPLE * base_vs_mean, 1),
                   "share_of_people_above_ceiling": None if share_above is None else round(share_above, 5),
                   "people_above_ceiling": None if share_above is None else round(share_above * regions[k]["pop0"])}
        scen = {}
        for sh in EXPORT_SHOCKS:
            for su in NEEDS_SURGES:
                path, breach = reserve_path(X[k], M[k], REM.get(k, 0.0), ess6, sh, su, R0=RES.get(k, 0.0))
                scen[f"export_shock_{int(sh*100)}|needs_surge_{int(su*100)}"] = {
                    "reserves_year5_months_of_imports": round(12 * path[BALANCE_YEARS - 1] / M[k], 1),
                    "first_year_below_six_months_of_essential_imports": breach}
        # export growth g needed so that cumulative balance over 5 years is zero with imports up by the surge
        need_g = {}
        for su in NEEDS_SURGES:
            lo, hi = -0.5, 2.0
            for _ in range(60):
                g = (lo + hi) / 2
                bal = sum(X[k] * (1 + g) ** t - M[k] * (1 + su) + REM.get(k, 0.0) for t in range(1, BALANCE_YEARS + 1))
                lo, hi = (lo, g) if bal > 0 else (g, hi)
            need_g[f"needs_surge_{int(su*100)}"] = round(g, 3)
        rows[k] = {"region": k, "candidate": k in candidates, "pop_m": round(regions[k]["pop0"] / 1e6, 1),
                   "exports_pct_gdp": round(100 * X[k] / GDP[k], 1), "imports_pct_gdp": round(100 * M[k] / GDP[k], 1),
                   "trade_balance_pct_gdp": round(100 * (X[k] - M[k]) / GDP[k], 1),
                   "remittances_pct_gdp": round(100 * REM.get(k, 0.0) / GDP[k], 1),
                   "reserves_months_of_imports": None if res_months is None else round(res_months, 1),
                   "essential_import_share_floor": None if ess_share is None else round(ess_share, 2),
                   "reserves_months_of_essential_imports": None if res_months is None or ess_share is None else round(res_months / ess_share, 1),
                   "price_level_vs_world": None if wedge is None else round(wedge, 2),
                   "arbitrage_index": None if wedge is None else round(abs(1 - wedge) * M[k] / GDP[k], 3),
                   "top_of_scale": top, "scenarios": scen, "export_growth_needed_for_5y_balance": need_g}
    cands = {k: rows[k] for k in candidates if k in rows}
    # context: distribution over the 36 regions that pass or miss by one screen
    group = candidates + [r["region"] for r in fr["one_screen_short"]]
    grp = [rows[k] for k in group if k in rows]
    def med(key):
        vals = sorted(r[key] for r in grp if r.get(key) is not None)
        return vals[len(vals) // 2] if vals else None
    out = {"question": "author, 2026-11-08: model the one-member economy for the regions that pass the first-region screen",
           "rules_tested": {"12b.2": "imports paid by exports over five years, no new debt", "12b.4": "reserve of at least six months of essential imports",
                            "14": "salaries up to 5x the base", "T-1.2/T-1.3": "savings convert at basket parity; the cap applies to wealth held on the voting day"},
           "candidates": cands,
           "context_median_over_candidates_and_near_misses": {k: med(k) for k in ("exports_pct_gdp", "imports_pct_gdp", "trade_balance_pct_gdp",
                                                                                   "remittances_pct_gdp", "reserves_months_of_imports", "price_level_vs_world")},
           "all_regions": rows, "parameters": {"ceiling_multiple": CEILING_MULTIPLE, "essential_reserve_months": ESSENTIAL_RESERVE_MONTHS,
                                                "export_shocks": EXPORT_SHOCKS, "needs_surges": NEEDS_SURGES, "horizon_years": HORIZON,
                                                "essential_share_fallback": 0.35},
           "evidence": {"trade, reserves, remittances, GDP": "World Bank WDI, latest year 2015-2024, frozen with hashes (VERIFIED_OFFICIAL)",
                        "essential import share": "food + fuel + ores and metals, % of merchandise imports (WDI); a floor: medicines and needs equipment are not in the series",
                        "price level": "PPP conversion factor / official exchange rate (WDI); 1 = US price level",
                        "top of scale": "WDI income shares of the top 10% and 20%; Pareto tail fitted to the top decile (MODEL_DERIVED); the UNIRA base basket vs the region's mean from V7.4"},
           "limits": ["a stock-flow of foreign currency with fixed shocks; no behavioural response of exporters, no capital account",
                      "the export shock stands for partners' reactions and lost competitiveness while internal prices move to the world hour price; its size is a scenario, not an estimate",
                      "the price wedge is an economy-wide average; the smuggling incentive is good by good",
                      "Pareto tail from two income shares: the share above the ceiling is an order of magnitude, not a count",
                      "remittances are assumed to continue; they would fall if emigrants' families no longer need them, or rise"]}
    if write:
        (U / "v72" / "outputs" / "one_member.json").write_text(json.dumps(out, indent=2))
        for k, r in cands.items():
            print(f"{k}: exports {r['exports_pct_gdp']}% imports {r['imports_pct_gdp']}% balance {r['trade_balance_pct_gdp']}% remittances {r['remittances_pct_gdp']}% of GDP; "
                  f"reserves {r['reserves_months_of_imports']} months of imports ({r['reserves_months_of_essential_imports']} of essential, floor share {r['essential_import_share_floor']}); "
                  f"price level {r['price_level_vs_world']}; above ceiling {r['top_of_scale'].get('share_of_people_above_ceiling')} ({r['top_of_scale'].get('people_above_ceiling')} people)")
            for s, v in r["scenarios"].items():
                print(f"   {s:36s} reserves y5 {v['reserves_year5_months_of_imports']:>6} months; breach year {v['first_year_below_six_months_of_essential_imports']}")
            print("   export growth needed for 5-year balance:", r["export_growth_needed_for_5y_balance"])
        print("context medians:", out["context_median_over_candidates_and_near_misses"])
    return out


if __name__ == "__main__":
    main()
