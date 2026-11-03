"""UNIRA V8.1 — price calculator (Constitution Article 13.4–13.7).

    price (U) = hours of work embodied in the product, all inputs included (Leontief, v63/io, France 2022)
                x the fixed price of one hour, 146.4 U (v64)
                x (1 + resource surcharge)
Energy prices rise in steps (author's rules 40-41): (1) within the allowance, hours price only; (2) up to 1.5 times
the allowance, half the surcharge; (3) beyond that, the full surcharge. Energy used to produce and transport food is
never surcharged: the surcharge applies only to final purchases, so embodied energy in food stays at the hours price.
Energy for needs is cheap (author's rule 40): each person's ESSENTIAL ENERGY ALLOWANCE (home electricity, heating,
cooking, essential travel) is priced at the hours price only, with no surcharge. Above the allowance, the resource
surcharge applies: the smallest surcharge that keeps the good at least as dear, relative to the average household
good, as today (Article 13.6), because cheap energy beyond needs is used more (V7.1 rebound). Mining products and
air transport always carry the surcharge. Revenue goes to the One Earth Fund. Homes are priced separately
(Article 18) and are not converted here.

Product groups are France's 64 input-output products, so a single product is priced through its group:
U price = today's euro price x (U per euro of its group). Example items use illustrative euro prices (marked).
Time cost = U price / base pay per working hour (5,000 U a month for 30 h a week = 38.5 U an hour).
python3 calculator.py  ->  ../outputs/prices.json, prices.csv"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
HOUR_PRICE = json.loads((U / "v64" / "outputs" / "summary.json").read_text())["fixed_price"]["pi_u_per_hour_equivalent"]
BASE_SALARY_MONTH = 5000
HOURS_PER_MONTH = 30 * 52 / 12
BASE_PAY_PER_HOUR = BASE_SALARY_MONTH / HOURS_PER_MONTH
ENERGY_GROUPS = ("CPA_C19", "CPA_D")  # fuels, electricity and gas: allowance at the hours price (rule 40)
RESOURCE_GROUPS = {"CPA_B": "mining and quarrying products", "CPA_C19": "fuels (coke and refined petroleum)",
                   "CPA_D": "electricity and gas", "CPA_H51": "air transport"}
EXCLUDED = {"CPA_L68A": "imputed rents (homes are priced by Article 18)", "CPA_L68B": "rents (Article 18)",
            "CPA_L68": "real estate (Article 18)"}
# Illustrative everyday items: (name, unit, today's euro price, product group). Euro prices are ILLUSTRATIVE
# round figures for France around 2024, not official statistics; the U price scales linearly with them.
EXAMPLES = [("tomatoes", "1 kg", 3.00, "CPA_A01"), ("bread (baguette)", "1 loaf", 1.00, "CPA_C10-12"),
            ("restaurant meal", "1 meal", 15.00, "CPA_I"), ("electricity", "1 kWh", 0.25, "CPA_D"),
            ("petrol", "1 litre", 1.80, "CPA_C19"), ("a pair of jeans", "1 pair", 40.00, "CPA_C13-15"),
            ("smartphone", "1 phone", 300.00, "CPA_C26"), ("new small car", "1 car", 20000.00, "CPA_C29"),
            ("flight Paris–Rome", "1 return ticket", 200.00, "CPA_H51"), ("haircut", "1 cut", 25.00, "CPA_S96")]


def work_time(u):
    """Readable time of work at the base salary needed to pay `u` U (30-hour week, 4.33 weeks a month)."""
    h = u / BASE_PAY_PER_HOUR
    if h < 1 / 60:
        return f"{round(3600 * h)} s"
    if h < 1:
        return f"{round(60 * h)} min"
    if h < 30:
        return f"{h:.1f} h"
    if h < HOURS_PER_MONTH:
        return f"{h / 30:.1f} weeks"
    return f"{h / HOURS_PER_MONTH:.1f} months"


def load():
    rows = list(csv.DictReader((U / "v63" / "io" / "outputs" / "hours_by_product.csv").open()))
    year = max(r["year"] for r in rows)
    lab = json.loads((U / "v63" / "io" / "data" / "raw" / "io_symmetric_fr.json").read_text())["dimension"]["prd_ava"]["category"]["label"]
    out = {}
    for r in rows:
        if r["year"] != year:
            continue
        m = float(r["total_hours_multiplier"]) / 1000  # hours per euro of final output
        hh = float(r["embodied_household_consumption_ths"]) * 1000 / m / 1e6 if m > 0 else 0.0  # household spending, MEUR
        out[r["product"]] = {"label": lab.get(r["product"], r["product"]), "hours_per_euro": m, "household_meur": hh}
    return int(year), out


def calculate():
    year, prod = load()
    base = {k: v for k, v in prod.items() if v["hours_per_euro"] > 0 and v["household_meur"] > 0 and k not in EXCLUDED}
    spend = sum(v["household_meur"] for v in base.values())
    avg_h = sum(v["hours_per_euro"] * v["household_meur"] for v in base.values()) / spend
    table = {}
    for k, v in prod.items():
        if v["hours_per_euro"] <= 0 or k in EXCLUDED:
            continue
        rel = v["hours_per_euro"] / avg_h  # relative price under pure hours pricing vs today
        sur = max(0.0, 1 / rel - 1) if k in RESOURCE_GROUPS else 0.0
        u_per_eur = v["hours_per_euro"] * HOUR_PRICE * (1 + sur)
        table[k] = {"label": v["label"], "hours_per_1000_eur": round(1000 * v["hours_per_euro"], 2),
                    "u_per_euro_work": round(v["hours_per_euro"] * HOUR_PRICE, 3), "resource_surcharge_pct": round(100 * sur, 1),
                    "u_per_euro": round(u_per_eur, 3), "relative_to_today": round(rel * (1 + sur), 3),
                    "u_per_euro_within_allowance": round(v["hours_per_euro"] * HOUR_PRICE, 3) if k in ENERGY_GROUPS else None,
                    "u_per_euro_step2": round(v["hours_per_euro"] * HOUR_PRICE * (1 + sur / 2), 3) if k in ENERGY_GROUPS else None,
                    "household_spending_share": round(v["household_meur"] / spend, 4) if k in base else 0.0}
    # effect of the surcharge on the household basket (at today's quantities)
    basket_work = sum(t["u_per_euro_work"] * prod[k]["household_meur"] for k, t in table.items() if k in base)
    basket_all = sum(t["u_per_euro"] * prod[k]["household_meur"] for k, t in table.items() if k in base)
    # with the allowance: households' energy within the allowance pays no surcharge (share of household energy covered)
    def basket_with_allowance(covered):
        tot = 0.0
        for k, t in table.items():
            if k not in base:
                continue
            u = t["u_per_euro"]
            if k in ENERGY_GROUPS:
                u = covered * t["u_per_euro_within_allowance"] + (1 - covered) * t["u_per_euro"]
            tot += u * prod[k]["household_meur"]
        return tot
    examples = []
    for name, unit, eur, g in EXAMPLES:
        t = table[g]
        u = eur * t["u_per_euro"]
        ua = eur * t["u_per_euro_within_allowance"] if t["u_per_euro_within_allowance"] is not None else None
        examples.append({"item": name, "unit": unit, "illustrative_eur_today": eur, "group": g, "group_label": t["label"],
                         "u_price": round(u, 2), "surcharge_pct": t["resource_surcharge_pct"],
                         "u_price_within_allowance": round(ua, 3) if ua is not None else None,
                         "u_price_step2": round(eur * t["u_per_euro_step2"], 3) if t["u_per_euro_step2"] is not None else None,
                         "work_time_within_allowance": work_time(ua) if ua is not None else None,
                         "minutes_of_work_at_base_salary": round(60 * u / BASE_PAY_PER_HOUR, 1),
                         "work_time": work_time(u)})
    return {"year": year, "hour_price_u": round(HOUR_PRICE, 2), "base_pay_u_per_hour": round(BASE_PAY_PER_HOUR, 2),
            "average_u_per_euro_household_basket": round(avg_h * HOUR_PRICE, 3),
            "surcharge_raises_household_basket_pct": round(100 * (basket_all / basket_work - 1), 2),
            "basket_increase_pct_if_allowance_covers": {f"{int(c * 100)}%": round(100 * (basket_with_allowance(c) / basket_work - 1), 2)
                                                        for c in (0.0, 0.5, 0.8, 1.0)},
            "energy_groups_with_allowance": list(ENERGY_GROUPS),
            "resource_groups": RESOURCE_GROUPS, "excluded_groups": EXCLUDED, "products": table, "examples": examples}


def main():
    res = calculate()
    out = HERE.parent / "outputs"
    out.mkdir(exist_ok=True)
    (out / "prices.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    with (out / "prices.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["product"] + list(next(iter(res["products"].values()))))
        w.writeheader()
        for k, v in sorted(res["products"].items()):
            w.writerow({"product": k, **v})
    print(f"hour price {res['hour_price_u']} U | base pay {res['base_pay_u_per_hour']} U/h | average {res['average_u_per_euro_household_basket']} U per euro "
          f"| surcharge raises the household basket by {res['surcharge_raises_household_basket_pct']}%")
    for k in RESOURCE_GROUPS:
        t = res["products"][k]
        print(f"  {t['label'][:45]:45s} surcharge +{t['resource_surcharge_pct']:.0f}% -> {t['u_per_euro']} U/EUR")
    print("household basket increase if the allowance covers 0/50/80/100% of household energy:", res["basket_increase_pct_if_allowance_covers"])
    for e in res["examples"]:
        print(f"  {e['item']:20s} {e['unit']:16s} EUR {e['illustrative_eur_today']:8.2f} -> {e['u_price']:9.1f} U  ({e['work_time']} of work at the base salary)" + (f" | within the allowance {e['u_price_within_allowance']} U ({e['work_time_within_allowance']})" if e['u_price_within_allowance'] is not None else ""))


if __name__ == "__main__":
    main()
