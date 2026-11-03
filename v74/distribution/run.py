"""UNIRA V7.4: who gains inside rich regions? Income deciles vs UNIRA's guaranteed standard.
python3 run.py
Current relative standard of decile d = 10 x its share of national equivalised income (1.0 = mean).
UNIRA levels relative to today's mean consumption per person (v64): base worker after saving 50% = 0.86;
average worker (multiplier 1.9) = 1.6. Free health care/education and guaranteed housing come on top
(not counted here, so gains for the poorest are understated)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "v62" / "src"))
from unira_v62 import fetch, jsonstat  # noqa: E402

BASE_REL = json.loads((ROOT.parents[1] / "v64" / "outputs" / "summary.json").read_text())["fixed_price"]["base_basket_vs_today_average_person"]


def main():
    if fetch.verify_manifest(ROOT / "data" / "raw"):
        raise SystemExit("hash mismatch")
    shares = {}
    for c, v, _ in jsonstat.iter_cells(jsonstat.load(ROOT / "data" / "raw" / "income_deciles_eu.json")):
        if c["quant_inc"].startswith("D") and c["quant_inc"][1:].isdigit():
            shares.setdefault(c["geo"], {})[int(c["quant_inc"][1:])] = v / 100
    out = {"unira_base_worker_level_vs_today_mean": BASE_REL, "regions": {}}
    for geo, sh in shares.items():
        rel = {d: 10 * s for d, s in sorted(sh.items())}
        gain = [d for d, r in rel.items() if r < BASE_REL]
        out["regions"][geo] = {"decile_relative_standard": rel, "deciles_below_unira_base": gain,
                               "share_of_people_who_gain_at_base_level": len(gain) / 10,
                               "bottom_decile_gain_pct_at_base": 100 * (BASE_REL / rel[1] - 1)}
        print(f"{geo:10s} deciles vs mean: " + " ".join(f"{r:.2f}" for r in rel.values())
              + f" | below UNIRA base ({BASE_REL:.2f}): {len(gain)*10}% of people | poorest tenth +{out['regions'][geo]['bottom_decile_gain_pct_at_base']:.0f}%")
    (ROOT.parent / "outputs").mkdir(exist_ok=True)
    (ROOT.parent / "outputs" / "distribution.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
