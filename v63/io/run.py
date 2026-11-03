"""UNIRA V6.3 (IO): hours embodied in final uses and avoidable-output levers, France.

    python3 run.py          # offline from data/raw
    python3 run.py --fetch  # re-download Eurostat snapshots
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT.parents[1] / "v62" / "src"))

from unira_io import analysis, fetch, model  # noqa: E402
from unira_v62 import jsonstat  # noqa: E402

RAW, OUT = ROOT / "data" / "raw", ROOT / "outputs"


def load():
    cells, hours = {}, {}
    for k, v, _ in jsonstat.iter_cells(jsonstat.load(RAW / "io_symmetric_fr.json")):
        cells[(k["time"], k["stk_flow"], k["prd_ava"], k["prd_use"])] = v
    for k, v, _ in jsonstat.iter_cells(jsonstat.load(RAW / "hours_a64_fr.json")):
        hours[(k["time"], k["nace_r2"], k["unit"], k["na_item"])] = v
    return cells, hours


def write(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()} for r in rows)


def main():
    if "--fetch" in sys.argv:
        fetch.fetch_all(RAW)
    if fetch.verify_manifest(RAW):
        raise SystemExit("raw snapshot hash mismatch")
    cfg = json.loads((ROOT / "config" / "v63_config.json").read_text())
    cells, hours = load()
    OUT.mkdir(exist_ok=True)
    summary, checks = {}, []
    by_use_rows, product_rows = [], []
    for year in (cfg["base_year"], cfg["robustness_year"]):
        io = model.IOSystem(cells, hours, year)
        T = sum(io.hours)
        emb = io.embodied_by_use()
        checks += [
            {"check": "products_partition_total_output", "year": year,
             "passed": abs(sum(io.x) / io.total_output - 1) < 1e-6},
            {"check": "hours_mapped_equal_na_total", "year": year,
             "passed": abs(T / io.hours_total_na - 1) < 1e-6},
            {"check": "row_balance_domestic_output", "year": year,
             "passed": max(abs(r) / max(x, 1) for r, x in zip(io.row_balance_residuals(), io.x)) < 1e-4},
            {"check": "embodied_hours_sum_to_total", "year": year,
             "passed": abs(sum(emb.values()) / T - 1) < 1e-5},
            {"check": "A_columns_productive", "year": year,
             "passed": max(sum(io.A[i][j] for i in range(len(io.A))) for j in range(len(io.A))) < 1},
        ]
        for k, v in emb.items():
            by_use_rows.append({"year": year, "final_use": k, "hours_ths": v, "share": v / T})
        by_up = io.embodied_by_use_and_product()
        ext = {r["product"]: r for r in analysis.extraction_table(io)}
        for i, p in enumerate(io.products):
            row = {"year": year, "product": p, "nace_hours_code": model.PRODUCTS[p] or "",
                   "hours_source": io.hours_source[i], "direct_hours_ths": io.hours[i],
                   "hours_per_meur_output": io.l[i], "total_hours_multiplier": io.m[i]}
            row.update({f"embodied_{k}_ths": by_up[k][i] for k in by_up})
            row["hem_hours_saved_ths"] = ext[p]["hours_saved_full_extraction_ths"]
            row["hem_share_total_hours"] = ext[p]["share_of_total_hours"]
            row["hem_valid"] = "no_labour_pass_through" if p in cfg["market_specific_candidates"]["excluded"] else "yes"
            product_rows.append(row)
        cand = cfg["market_specific_candidates"]["items"]
        levels = {}
        for li, name in enumerate(cfg["market_specific_candidates"]["levels"]):
            saved = analysis.partial_reduction(io, {p: v["reductions"][li] for p, v in cand.items()})
            levels[name] = {"hours_saved_ths": saved, "share_of_total_hours": saved / T}
        durables = analysis.durables_lever(io, cfg["durables"])
        food_idx = [io.products.index(p) for p in cfg["food_products"]]
        summary[str(year)] = {
            "total_hours_ths": T,
            "allocated_hours_share": sum(h for h, s in zip(io.hours, io.hours_source) if s.startswith("alloc")) / T,
            "embodied_by_use": {k: {"hours_ths": v, "share": v / T} for k, v in emb.items()},
            "import_hours_equivalent_ths": io.import_hours_equivalent(),
            "market_candidates": levels,
            "durables": durables,
            "imported_durables_hours_equivalent_ths": analysis.imported_durables_hours_equivalent(io, cfg["durables"]["products"]),
            "household_food_hours_share": sum(by_up["household_consumption"][i] for i in food_idx) / T,
        }
    gap = analysis.uncovered_hours_from_v62(ROOT / cfg["gap_source"], cfg["gap_weekly_cap"])
    base = summary[str(cfg["base_year"])]
    summary["gap_comparison"] = {
        case: {"uncovered_share_after_v62_pathway": g,
               **{f"after_{lvl}_candidates": g - v["share_of_total_hours"] for lvl, v in base["market_candidates"].items()}}
        for case, g in gap.items()}
    write(OUT / "embodied_hours_by_use.csv", by_use_rows)
    write(OUT / "hours_by_product.csv", product_rows)
    write(OUT / "checks.csv", checks)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    for c in checks:
        print(("PASS " if c["passed"] else "FAIL ") + c["check"], c["year"])
    print(json.dumps({"base": {k: base[k] for k in ("embodied_by_use", "market_candidates", "import_hours_equivalent_ths",
                                                     "imported_durables_hours_equivalent_ths", "household_food_hours_share",
                                                     "allocated_hours_share")},
                      "gap_comparison": summary["gap_comparison"]}, indent=1))
    if not all(c["passed"] for c in checks):
        raise SystemExit("checks failed")


if __name__ == "__main__":
    main()
