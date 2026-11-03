import json
import math
import random
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import forecast  # noqa: E402
import information as info  # noqa: E402


def synthetic(n_regions=40, years=range(1980, 2024), seed=0):
    rng = random.Random(seed)
    out = {}
    for i in range(n_regions):
        g, y = rng.uniform(-0.01, 0.03), rng.uniform(10, 100)
        out[f"R{i:02d}"] = {}
        for t in years:
            y *= math.exp(g + rng.gauss(0, 0.002))
            out[f"R{i:02d}"][t] = y
    return out


class TestForecast(unittest.TestCase):
    def test_no_look_ahead(self):
        s = synthetic()
        for h in (1, 5):
            rows = forecast.samples(s, h)
            fit = [r for r in rows if r[1] + h < forecast.VAL_START]
            self.assertTrue(fit)
            self.assertTrue(all(r[1] + h < forecast.VAL_START for r in fit))
            # features only use data at or before the origin
            r = rows[0]
            self.assertAlmostEqual(r[2][0], math.log(s[r[0]][r[1]] / s[r[0]][r[1] - 1]))

    def test_naive_exact_on_constant_series(self):
        s = {"A": {t: 5.0 for t in range(1990, 2024)}}
        r = forecast.backtest(s, 2)
        self.assertAlmostEqual(r["test"]["naive"]["median_ape"], 0.0)

    def test_ridge_learns_steady_growth(self):
        # regions growing at a steady rate: the pooled ML model must beat 'no change'
        r = forecast.backtest(synthetic(), 2)
        self.assertLess(r["test"]["ridge"]["median_ape"], r["test"]["naive"]["median_ape"] / 3)

    def test_choice_made_on_validation_not_test(self):
        r = forecast.backtest(synthetic(), 1)
        chosen = r["chosen_on_validation"]
        self.assertEqual(chosen, min(r["validation_median_ape"], key=r["validation_median_ape"].get))

    def test_backtest_outputs_real_data(self):
        out = json.loads((HERE.parent / "outputs" / "backtest.json").read_text())
        pop = out["results"]["population"]["h1"]
        self.assertLess(pop["test"][pop["chosen_on_validation"]]["median_ape"], 0.01)
        for series in out["results"].values():
            for r in series.values():
                self.assertGreater(r["test"]["naive"]["n"], 50)


class TestInformation(unittest.TestCase):
    def test_zero_error_equals_perfect(self):
        cfg = info.compare.load_config()
        regions = info.compare.rt.load_regions()
        cap = json.loads((info.U / "v66" / "construction" / "capacity.json").read_text())
        s = info.compare.settings(cfg, {k: "C" for k in cfg["lever_order"]})
        perfect = info.world(s, regions, cfg, cap, {"leakage": 0.0}, 0)
        zero = {"misreport_share": 0.0, "inflation": 0.0, "audit_detect": 0.0, "leakage": 0.0,
                "sigma_level": {d: 0.0 for d in info.DOMAINS}, "sigma_pop": 0.0}
        same = info.world(s, regions, cfg, cap, zero, 0)
        for k in ("energy_closed_y15", "health_closed_y15", "housing_closed_y30"):
            self.assertAlmostEqual(perfect[k], same[k], places=9)


if __name__ == "__main__":
    unittest.main()
