"""UNIRA V6.3 health & care staffing (France): python3 run.py [--fetch]."""
import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT.parents[1] / "v62" / "src"))

from unira_health import fetch, model  # noqa: E402
from unira_v62 import jsonstat  # noqa: E402

RAW, OUT = ROOT / "data" / "raw", ROOT / "outputs"


def series(stem, **match):
    out = {}
    for c, v, _ in jsonstat.iter_cells(jsonstat.load(RAW / f"{stem}.json")):
        if all(c.get(k) == val for k, val in match.items()):
            out[int(c["time"])] = v
    return out


def q_gain(cfg):
    with (ROOT / cfg["v62_sector_csv"]).open() as f:
        for r in csv.DictReader(f):
            if r["scenario"] == cfg["v62_scenario"] and r["year"] == str(cfg["v62_year"]) and r["nace_r2"] == "Q":
                return float(r["required_hourly_productivity_gain"])
    raise SystemExit("section Q row not found in V6.2 outputs")


def main():
    if "--fetch" in sys.argv:
        fetch.fetch_all(RAW)
    if fetch.verify_manifest(RAW):
        raise SystemExit("raw snapshot hash mismatch")
    cfg = json.loads((ROOT / "config" / "health_config.json").read_text())
    OUT.mkdir(exist_ok=True)
    gain = q_gain(cfg)
    rows = []
    for occ, meta in cfg["occupations"].items():
        a, b = meta.get("trend_window", cfg["trend_window"])
        stock = series("health_personnel_fr", med_spec=occ, wstatus="PRACT")
        grads = series("health_graduates_fr", med_spec=occ) if occ != "PER_CARE" else {}
        sy = max(y for y in stock if y <= cfg["stock_year"])
        extra = model.extra_needed(stock[sy], gain)
        row = {"occupation": occ, "label": meta["label"], "stock_year": sy, "practising": stock[sy],
               "trend_window": f"{a}-{b}",
               "q_required_gain": gain, "extra_needed_year1": extra,
               "lead_time_years": meta["lead_time_years"], "lead_time_evidence": meta["lead_time_note"]}
        if grads and a in stock and b in stock and all(y in grads for y in range(a + 1, b + 1)):
            g = sum(grads[y] for y in range(a + 1, b + 1)) / (b - a)
            row.update({"graduates_per_year": g, "net_stock_growth_per_year": model.mean_annual_change(stock, a, b),
                        "implied_exits_per_year": model.implied_exits(grads, stock, a, b),
                        "extra_as_years_of_graduates": extra / g})
            for e in cfg["training_expansions"]:
                row[f"years_to_close_if_intake_plus_{int(e*100)}pct"] = model.years_to_close(
                    extra, g, e, meta["lead_time_years"])
        else:
            row["graduates_per_year"] = "MISSING"
        row["year1_shortfall_no_reserve"] = model.year1_shortfall(extra, 0.0)
        rows.append(row)
    hosp = {k: series("hospital_employment_fr", med_spec="NRS_MWS", unit=k) for k in ("FTE", "HC")}
    vac = series("vacancy_rate_q_fr")
    summary = {"q_required_gain": gain, "occupations": rows,
               "hospital_nurse_fte_per_head_2023": hosp["FTE"][2023] / hosp["HC"][2023],
               "vacancy_rate_q_pct": vac, "missing": cfg["missing"]}
    fields = []
    for r in rows:
        fields += [k for k in r if k not in fields]
    with (OUT / "health_staffing.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows({k: ("inf" if v == math.inf else (round(v, 4) if isinstance(v, float) else v))
                     for k, v in r.items()} for r in rows)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, default=lambda x: "inf"))
    print(json.dumps(summary, indent=1, default=str))


if __name__ == "__main__":
    main()
