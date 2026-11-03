"""UNIRA V8.2 — does a restaurant (and a supermarket) work with UNIRA's prices and salaries?

Real cost structure per euro of output, France 2022 (Eurostat symmetric input-output table, v63/io):
every input the sector buys (food, wholesale, rent of premises, energy, accounting, transport...) and its value added.
Under UNIRA:
    sales        = hours of work embodied in the output x 146.4 U (fixed price, Article 13)
    inputs       = each input at its own UNIRA price (embodied hours x 146.4 U); energy for food businesses at the
                   hours price with no surcharge (rule 41); premises rent at the hours cost of real-estate services
    equipment    = wear of equipment and premises: 20.5% of gross value added (France's depreciation share of value
                   added, 2024, applied to the sector: SYNTHETIC_ASSUMPTION) priced at the UNIRA price of
                   investment goods
    salaries     = UNIRA salaries for the sector's real hours of work: base 5,000 U a month for 30 h a week,
                   multipliers by job (Article 14) plus hardship steps (Article 14a)
    community    = what remains: it goes to the region and the One Earth Fund (Article 17a), and pays for free health
    share          care, education, public services and investment. The owner is a salaried manager (max 5x).
Illustrative firms: a restaurant of 10 people and a supermarket of 40 people (job mixes are SYNTHETIC_ASSUMPTION).
For the supermarket, the accounts show its own retail work (the margin); the goods it resells pass through at their
fixed price, which already includes the shop's work.
python3 simulate.py  ->  outputs/enterprise.json"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
sys.path.insert(0, str(U / "v62" / "src"))
from unira_v62 import jsonstat  # noqa: E402

PI = json.loads((U / "v64" / "outputs" / "summary.json").read_text())["fixed_price"]["pi_u_per_hour_equivalent"]
BASE = 5000.0
HOURS_YEAR = 30 * 52            # hours per worker per year (30-hour week)
DEP_SHARE_OF_GVA = None          # computed from Eurostat (depreciation / GDP) below
FIRMS = {
    "restaurant": {"sector": "CPA_I", "meal_eur": 15.0,
                   "staff": [("owner-manager and head cook", 1, 3.0), ("cooks", 2, 1.8), ("kitchen helpers and waiters", 6, 1.2),
                             ("dishwasher and cleaning", 1, 1.2)], "hardship": 0.85},
    "supermarket": {"sector": "CPA_G47", "meal_eur": None,
                    "staff": [("store manager", 1, 3.0), ("department heads", 4, 2.0), ("cashiers and shelf staff", 30, 1.3),
                              ("logistics and night staff", 5, 1.3)], "hardship": 0.45},
}


def io_data():
    d = jsonstat.load(U / "v63" / "io" / "data" / "raw" / "io_symmetric_fr.json")
    lab = d["dimension"]["prd_ava"]["category"]["label"]
    col = {}
    for c, v, _ in jsonstat.iter_cells(d):
        if c["time"] == "2022" and c["stk_flow"] == "TOTAL" and v and c["prd_use"] in ("CPA_I", "CPA_G47"):
            col.setdefault(c["prd_use"], {})[c["prd_ava"]] = v
    hrs = {r["product"]: r for r in csv.DictReader((U / "v63" / "io" / "outputs" / "hours_by_product.csv").open()) if r["year"] == "2022"}
    return col, hrs, lab


def facts():
    cap = json.loads((U / "v82" / "capital" / "outputs" / "capital.json").read_text())["facts"]
    gfcf_h = [r for r in (U / "v63" / "io" / "outputs" / "embodied_hours_by_use.csv").read_text().splitlines()
              if r.startswith("2022,gross_fixed_capital_formation")][0].split(",")
    gfcf_eur_2022 = 623311.7  # Eurostat nama_10_gdp P51G France 2022, MEUR (v82/capital/data/raw)
    return {"dep_share_of_gva": cap["depreciation_share_gdp"] / 0.898,  # GVA is about 89.8% of GDP (net taxes on products)
            "u_per_eur_investment_goods": float(gfcf_h[2]) / gfcf_eur_2022 * PI / 1000}


def per_euro(sector, col, hrs, f):
    c = col[sector]
    out = c["P1"]
    m = lambda p: float(hrs[p]["total_hours_multiplier"]) / 1000 if p in hrs else None  # hours per euro
    inputs = {}
    for p, v in c.items():
        if p in hrs:  # only the 64 standard product groups; sub-items (e.g. CPA_C10 inside CPA_C10-12) would double count
            inputs[p] = (v / out, v / out * m(p) * PI)
    missing = c["CPA_TOTAL"] - sum(v * out for v, _ in inputs.values())  # inputs not covered by the 64 groups
    return {"today": {"inputs": c["P2_ADJ"] / out, "staff_pay": c["D1"] / out, "operating_surplus": c["B2A3G"] / out,
                      "taxes_on_production": c.get("D29X39", 0) / out},
            "inputs_u": sum(u for _, u in inputs.values()), "inputs_detail": inputs,
            "equipment_u": f["dep_share_of_gva"] * c["B1G"] / out * f["u_per_eur_investment_goods"],
            "sales_u": m(sector) * PI, "direct_hours": float(hrs[sector]["hours_per_meur_output"]) / 1000,  # thousand hours per MEUR -> hours per euro
            "unpriced_input_share": missing / out}


def firm_accounts(name, spec, col, hrs, lab, f):
    pe = per_euro(spec["sector"], col, hrs, f)
    staff = sum(n for _, n, _ in spec["staff"])
    hours = staff * HOURS_YEAR
    output_eur = hours / pe["direct_hours"]           # today's euro value of what these hours produce
    hard_step = 0.5 * spec["hardship"]                # Article 14a
    salaries = sum(n * min(5.0, mult + hard_step) * BASE * 12 for _, n, mult in spec["staff"])
    sales = output_eur * pe["sales_u"]
    inputs = output_eur * pe["inputs_u"]
    equipment = output_eur * pe["equipment_u"]
    community = sales - inputs - equipment - salaries
    top = sorted(pe["inputs_detail"].items(), key=lambda x: -x[1][1])[:8]
    acc = {"staff": staff, "hours_per_year": hours, "output_today_eur": round(output_eur),
           "sales_u": round(sales), "inputs_u": round(inputs), "equipment_and_premises_wear_u": round(equipment),
           "salaries_u": round(salaries), "community_share_u": round(community),
           "shares_of_sales": {"inputs": round(inputs / sales, 3), "equipment": round(equipment / sales, 3),
                               "salaries": round(salaries / sales, 3), "community_share": round(community / sales, 3)},
           "today_shares_of_output": {k: round(v, 3) for k, v in pe["today"].items()},
           "largest_inputs_u": [[lab.get(p, p), round(output_eur * u)] for p, (_, u) in top],
           "rent_of_premises_u": round(output_eur * pe["inputs_detail"].get("CPA_L68B", (0, 0))[1]),
           "energy_u": round(output_eur * pe["inputs_detail"].get("CPA_D", (0, 0))[1]),
           "average_multiplier": round(salaries / (staff * BASE * 12), 2),
           "unpriced_input_share": round(pe["unpriced_input_share"], 4)}
    # demand below normal: sales and inputs fall, salaries and wear stay (fixed prices, fixed salaries)
    acc["break_even_share_of_normal_demand"] = round((salaries + equipment) / (sales - inputs), 3)
    acc["community_share_by_demand"] = {f"{int(100 * x)}%": round(x * (sales - inputs) - salaries - equipment)
                                        for x in (0.5, 0.6, 0.7, 0.8, 1.0, 1.2)}
    if spec["meal_eur"]:
        u_per_eur = pe["sales_u"]
        meal = spec["meal_eur"] * u_per_eur
        k = meal / sales
        acc["meals_per_year"] = round(output_eur / spec["meal_eur"])
        acc["one_meal"] = {"price_u": round(meal, 1), "inputs_u": round(inputs * k, 1), "equipment_u": round(equipment * k, 1),
                           "salaries_u": round(salaries * k, 1), "community_share_u": round(community * k, 1)}
    return acc


def main():
    col, hrs, lab = io_data()
    f = facts()
    out = {"hour_price_u": round(PI, 2), "facts": {k: round(v, 4) for k, v in f.items()}, "firms": {}}
    for name, spec in FIRMS.items():
        a = firm_accounts(name, spec, col, hrs, lab, f)
        out["firms"][name] = a
        print(f"\n{name}: {a['staff']} people, sales {a['sales_u']:,} U/yr")
        for k in ("inputs_u", "equipment_and_premises_wear_u", "salaries_u", "community_share_u"):
            print(f"  {k:32s} {a[k]:>12,} U  ({100 * a[k] / a['sales_u']:.0f}%)")
        print(f"  of which rent of premises {a['rent_of_premises_u']:,} U, energy {a['energy_u']:,} U; average multiplier {a['average_multiplier']}")
        print("  today's shares of output:", a["today_shares_of_output"])
        print(f"  break-even at {100 * a['break_even_share_of_normal_demand']:.0f}% of normal demand; community share by demand:", a["community_share_by_demand"])
        if "one_meal" in a:
            print("  one meal:", a["one_meal"], "| meals/yr", a["meals_per_year"])
    (HERE / "outputs").mkdir(exist_ok=True)
    (HERE / "outputs" / "enterprise.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
