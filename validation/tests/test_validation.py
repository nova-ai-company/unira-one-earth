import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import backtest  # noqa: E402
import uncertainty  # noqa: E402


class TestBacktest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = backtest.main(write=False)

    def test_reproducible(self):
        self.assertEqual(json.dumps(backtest.main(write=False), sort_keys=True), json.dumps(self.out, sort_keys=True))

    def test_every_domain_has_enough_countries_and_finite_errors(self):
        self.assertGreaterEqual(len(self.out["domains"]), 5)
        for d in self.out["domains"].values():
            self.assertGreaterEqual(d["countries"], 100)
            for v in d["variants"].values():
                self.assertGreaterEqual(v["mae_points"], 0.0)
                self.assertLessEqual(abs(v["bias_points_pred_minus_actual"]), 40.0)

    def test_higher_floor_predicts_more(self):
        """A higher percentile floor can only raise predicted coverage (monotone in p)."""
        for d in self.out["domains"].values():
            cov = [d["variants"][f"{p}/no_governance_factor"]["predicted_world_coverage_2024"] for p in ("own_only", "p50", "p75", "p90")]
            self.assertEqual(cov, sorted(cov))

    def test_governance_factor_lowers_predictions_in_conflict_states(self):
        for d in self.out["domains"].values():
            a = d["variants"]["p75/no_governance_factor"]["bias_by_status"].get("conflict")
            b = d["variants"]["p75/with_governance_factor"]["bias_by_status"].get("conflict")
            if a is not None and b is not None:
                self.assertLessEqual(b, a)


class TestUncertainty(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = uncertainty.main(write=False, n67=40, n89=6, n91=2)

    def test_reproducible(self):
        again = uncertainty.main(write=False, n67=40, n89=6, n91=2)
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.out, sort_keys=True))

    def test_structure_and_bounds(self):
        for name, r in self.out.items():
            self.assertGreater(r["n"], 0)
            for o, q in r["outcomes"].items():
                self.assertLessEqual(q["p5"], q["median"])
                self.assertLessEqual(q["median"], q["p95"])
                self.assertTrue(all(-1.0 <= v <= 1.0 for _, v in r["drivers"][o]))

    def test_energy_build_drives_energy_date(self):
        d = dict(self.out["v67_transition"]["drivers"]["year_all_energy"])
        self.assertLess(d["energy_new_ej_per_yr"], 0)  # more clean energy built, earlier date


if __name__ == "__main__":
    unittest.main()
