"""UNIRA V8.2 (point 3) — investment, machines and infrastructure, counted in hours of work.

France's measured starting point (Eurostat, 2024): investment (GFCF) 22.2% of GDP; depreciation (GDP minus NDP)
18.4% of GDP, so 83% of investment only replaces what wears out; net fixed assets about 3.5 years of GDP.
In hours (v63 input-output, 2022): investment goods embody 17.2% of all hours worked.

Rule tested (proposed Article 16a), each year:
  1. MAINTENANCE FIRST: replace what wears out (depreciation), so the stock never runs down;
  2. NEEDS: new capacity for unmet needs (Article 10a: energy, homes, care, transport), for a transition period;
  3. HOURS-SAVING: machines and methods that save more hours over their life than they take to build, ranked by
     hours payback; savings shorten the working week (rule 16), never raise output beyond needs.
30-year path of the average working week (starting at 30 h) for different hours-saving investment shares and
paybacks (years to recover the hours spent). Consumption needs are held constant (no growth beyond needs).
python3 model.py  ->  outputs/capital.json"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
sys.path.insert(0, str(U / "v62" / "src"))
from unira_v62 import jsonstat  # noqa: E402

LIFE_YEARS = 20          # SYNTHETIC_ASSUMPTION: average life of hours-saving equipment
NEEDS_YEARS = 15         # SYNTHETIC_ASSUMPTION: transition period of extra needs investment
YEARS = 30


def facts():
    def cells(f):
        return [(c, v) for c, v, _ in jsonstat.iter_cells(jsonstat.load(HERE / "data" / "raw" / f)) if v is not None]
    gdp = cells("nama_10_gdp_fr.json")
    nf = cells("nasa_10_nf_tr_fr.json")
    st = cells("nama_10_nfa_st_fr.json")
    y = "2024"
    b1gq = {c["na_item"]: v for c, v in gdp if c["time"] == y}
    net = {c["na_item"]: v for c, v in nf if c["time"] == y and c["direct"] == "PAID"}
    stock = {c["asset10"]: v for c, v in st if c["time"] == y}
    gfcf_h = [r for r in (U / "v63" / "io" / "outputs" / "embodied_hours_by_use.csv").read_text().splitlines()
              if r.startswith("2022,gross_fixed_capital_formation")][0].split(",")[-1]
    dep = net["B1GQ"] - net["B1NQ"]
    return {"year": int(y), "gdp_meur": b1gq["B1GQ"], "gfcf_share_gdp": b1gq["P51G"] / b1gq["B1GQ"],
            "depreciation_share_gdp": dep / net["B1GQ"], "maintenance_share_of_investment": dep / b1gq["P51G"],
            "net_fixed_assets_years_of_gdp": stock["N11N"] / b1gq["B1GQ"],
            "dwellings_share_of_assets": stock["N111N"] / stock["N11N"],
            "investment_share_of_hours_2022": float(gfcf_h)}


def path(f, needs_share, saving_share, payback):
    """Average weekly hours over 30 years. Hours budget shares: consumption C, maintenance M, needs N, saving S."""
    inv_h = f["investment_share_of_hours_2022"]
    maint = inv_h * f["maintenance_share_of_investment"]
    cons = 1.0 - inv_h                       # consumption + public services, held constant in physical terms
    rate = 1.0 / payback                     # hours saved per year per hour invested
    cohorts = []                             # (year built, hours invested) -> saves rate*h per year for LIFE_YEARS
    week = []
    for t in range(YEARS + 1):
        saved = sum(h * rate for (t0, h) in cohorts if 0 < t - t0 <= LIFE_YEARS)
        needs = needs_share if t < NEEDS_YEARS else 0.0
        # total hours needed, as a share of today's total (today = 1.0 at 30 h)
        total = max(0.2, cons - saved) + maint + needs + saving_share
        week.append(30 * total / (cons + inv_h))  # today's total hours = 30 h a week
        cohorts.append((t, saving_share))
    return week


def main():
    f = facts()
    out = {"facts": f, "life_years": LIFE_YEARS, "needs_years": NEEDS_YEARS, "scenarios": {}}
    net_today = f["investment_share_of_hours_2022"] * (1 - f["maintenance_share_of_investment"])
    print({k: round(v, 3) if isinstance(v, float) else v for k, v in f.items()})
    for payback in (6, 10, 15):
        for s in (0.0, net_today, 0.05):
            w = path(f, needs_share=0.0, saving_share=s, payback=payback)
            key = f"payback_{payback}y/saving_{round(100 * s, 1)}pct"
            out["scenarios"][key] = {"week_year_0": round(w[0], 2), "week_year_10": round(w[10], 2), "week_year_20": round(w[20], 2),
                                     "week_year_30": round(w[30], 2), "path": [round(x, 2) for x in w]}
            print(f"{key:30s} weekly hours: yr0 {w[0]:.1f} | yr10 {w[10]:.1f} | yr20 {w[20]:.1f} | yr30 {w[30]:.1f}")
    for needs in (0.03, 0.05):
        w = path(f, needs_share=needs, saving_share=net_today, payback=10)
        key = f"needs_{int(100 * needs)}pct_15y/payback_10y/saving_{round(100 * net_today, 1)}pct"
        out["scenarios"][key] = {"week_year_0": round(w[0], 2), "week_year_10": round(w[10], 2), "week_year_15": round(w[15], 2),
                                 "week_year_20": round(w[20], 2), "week_year_30": round(w[30], 2), "path": [round(x, 2) for x in w]}
        print(f"{key:44s} weekly hours: yr0 {w[0]:.1f} | yr10 {w[10]:.1f} | yr15 {w[15]:.1f} | yr20 {w[20]:.1f} | yr30 {w[30]:.1f}")
    (HERE / "outputs").mkdir(exist_ok=True)
    (HERE / "outputs" / "capital.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
