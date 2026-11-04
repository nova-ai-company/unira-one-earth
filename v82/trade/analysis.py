"""UNIRA V8.2 (point 5) — trade with non-members during the transition (France as the example member region).

From France's 2022 input-output table (Eurostat, v63/io): imports by product, the share of each product's use that is
imported, and exports. Essential imports (needs of Article 10a: energy, medicines, food, equipment for needs) are
separated from others, to size what a member region must earn from non-members and the reserve of foreign currency
One Earth should keep. Exchange: one accounting rate per product group from the price calculator (v81: U per euro).
python3 analysis.py  ->  outputs/trade.json"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
sys.path.insert(0, str(U / "v62" / "src"))
from unira_v62 import jsonstat  # noqa: E402

ESSENTIAL = {"CPA_B": "energy and raw materials (mining)", "CPA_C19": "fuels", "CPA_D": "electricity and gas",
             "CPA_C21": "medicines", "CPA_A01": "farm products", "CPA_C10-12": "food products",
             "CPA_C26": "electronics (health, networks)", "CPA_C28": "machinery (needs-first capacity)"}
RESERVE_MONTHS = 6  # SYNTHETIC_ASSUMPTION: foreign-currency reserve to cover essential imports for six months


def main():
    d = jsonstat.load(U / "v63" / "io" / "data" / "raw" / "io_symmetric_fr.json")
    lab = d["dimension"]["prd_ava"]["category"]["label"]
    std = {r.split(",")[1] for r in (U / "v63" / "io" / "outputs" / "hours_by_product.csv").read_text().splitlines()[1:]}
    imp, use, exp = {}, {}, {}
    for c, v, _ in jsonstat.iter_cells(d):
        if c["time"] != "2022" or not v or c["prd_ava"] not in std:
            continue
        if c["prd_use"] == "TOTAL" and c["stk_flow"] == "IMP":
            imp[c["prd_ava"]] = v
        if c["prd_use"] == "TOTAL" and c["stk_flow"] == "TOTAL":
            use[c["prd_ava"]] = v
        if c["prd_use"] == "P6" and c["stk_flow"] == "TOTAL":
            exp[c["prd_ava"]] = v
    prices = json.loads((U / "v81" / "outputs" / "prices.json").read_text())["products"]
    total_imp, total_exp = sum(imp.values()), sum(exp.values())
    ess = {k: imp.get(k, 0.0) for k in ESSENTIAL}
    rows = sorted(({"product": k, "label": lab.get(k, k), "imports_meur": round(v), "imported_share_of_use": round(v / use[k], 3) if use.get(k) else None,
                    "u_per_euro": prices.get(k, {}).get("u_per_euro")} for k, v in imp.items()), key=lambda r: -r["imports_meur"])
    out = {"year": 2022, "imports_meur": round(total_imp), "exports_meur": round(total_exp),
           "essential_imports_meur": round(sum(ess.values())), "essential_share_of_imports": round(sum(ess.values()) / total_imp, 3),
           "essential_imports_detail": {ESSENTIAL[k]: round(v) for k, v in ess.items()},
           "reserve_months": RESERVE_MONTHS, "reserve_meur": round(sum(ess.values()) * RESERVE_MONTHS / 12),
           "exports_cover_essential_imports_times": round(total_exp / sum(ess.values()), 2),
           "largest_imports": rows[:15]}
    (HERE / "outputs").mkdir(exist_ok=True)
    (HERE / "outputs" / "trade.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print({k: v for k, v in out.items() if k not in ("largest_imports",)})
    for r in rows[:10]:
        print(f"  {r['label'][:45]:45s} imports {r['imports_meur']:>8,} MEUR  imported share of use {r['imported_share_of_use']}")


if __name__ == "__main__":
    main()
