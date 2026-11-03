"""UNIRA V7.9 — the price rule for new and existing products (design 2), tested on France's input-output table.

Rule (proposed amendment to Article 13): price = hours of work embodied in the product (direct + all inputs,
Leontief, v63/io) x the fixed hour price (146 U, v64), set once when a product is introduced; productivity
gains then shorten working hours instead of lowering prices; scarce natural resources carry a physical surcharge.
Test: how relative prices would move if today's French household basket were priced by embodied hours only,
compared with today's market prices (both normalised so the household basket costs the same in total).
Products far below 1 are those where market prices pay for things other than work: natural resources, land and
capital. They show where a resource surcharge is needed so that metered goods (rule 19) are not under-priced.
python3 price_rule.py  ->  ../outputs/price_rule.json"""
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
HOUR_PRICE = json.loads((U / "v64" / "outputs" / "summary.json").read_text())["fixed_price"]
RESOURCE_CODES = {"CPA_B": "mining and quarrying", "CPA_C19": "coke and refined petroleum",
                  "CPA_D35": "electricity and gas", "CPA_L68B": "rental of homes (imputed and actual)",
                  "CPA_L68A": "imputed rents of owner-occupiers", "CPA_L68": "real estate"}


def labels():
    d = json.loads((U / "v63" / "io" / "data" / "raw" / "io_symmetric_fr.json").read_text())
    return d["dimension"]["prd_ava"]["category"]["label"]


def main():
    rows = [r for r in csv.DictReader((U / "v63" / "io" / "outputs" / "hours_by_product.csv").open())]
    year = max(r["year"] for r in rows)
    rows = [r for r in rows if r["year"] == year]
    lab = labels()
    hh = []
    for r in rows:
        m = float(r["total_hours_multiplier"])  # thousand hours per million EUR of final output
        h = float(r["embodied_household_consumption_ths"])
        if m > 0 and h > 0:
            hh.append((r["product"], m, h / m))  # (code, hours/MEUR, household spending MEUR)
    spend = sum(e for _, _, e in hh)
    avg = sum(m * e for _, m, e in hh) / spend  # household-weighted hours per MEUR
    out = []
    for code, m, e in hh:
        out.append({"product": code, "label": lab.get(code, code), "household_spending_share": round(e / spend, 4),
                    "hours_per_1000_eur": round(m, 2), "hours_price_vs_market": round(m / avg, 3)})
    out.sort(key=lambda x: x["hours_price_vs_market"])
    big = [x for x in out if x["household_spending_share"] >= 0.005]
    res = {"year": int(year), "hour_price_u": round(HOUR_PRICE["pi_u_per_hour_equivalent"], 1),
           "household_weighted_hours_per_1000_eur": round(avg, 2), "products": len(out),
           "cheaper_under_pure_hours_pricing": big[:8], "dearer_under_pure_hours_pricing": big[-8:][::-1],
           "resource_products": [x for x in out if x["product"] in RESOURCE_CODES],
           "share_of_spending_more_than_30pct_cheaper": round(sum(x["household_spending_share"] for x in out if x["hours_price_vs_market"] < 0.7), 3),
           "share_of_spending_more_than_30pct_dearer": round(sum(x["household_spending_share"] for x in out if x["hours_price_vs_market"] > 1.3), 3),
           "all": out}
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "price_rule.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print("hours/1000 EUR household average", round(avg, 2))
    for x in res["cheaper_under_pure_hours_pricing"] + [None] + res["dearer_under_pure_hours_pricing"]:
        print("---" if x is None else f"{x['hours_price_vs_market']:5.2f}  {100 * x['household_spending_share']:4.1f}%  {x['label'][:70]}")
    print("resource products:", [(x["product"], x["hours_price_vs_market"]) for x in res["resource_products"]])
    print("spending >30% cheaper:", res["share_of_spending_more_than_30pct_cheaper"], " >30% dearer:", res["share_of_spending_more_than_30pct_dearer"])


if __name__ == "__main__":
    main()
