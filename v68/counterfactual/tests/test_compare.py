import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compare  # noqa: E402


class TestComparison(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res = compare.run_all()

    def test_matched_resources(self):
        # same shared capacities and targets for both economies (only levers differ)
        cfg = compare.load_config()
        self.assertEqual(set(cfg["levers"]), set(cfg["lever_order"]))
        for k, v in cfg["levers"].items():
            self.assertIn("B", v)
            self.assertIn("C", v)

    def test_c_at_least_as_good_as_b(self):
        b, c = self.res["B_reformed_market"], self.res["C_unira"]
        self.assertLessEqual(c["france_year1_gain_needed"], b["france_year1_gain_needed"])
        for k in ("energy_closed_y15", "health_closed_y15", "housing_closed_y30"):
            self.assertGreaterEqual(c[k], b[k], k)

    def test_b2_between_b_and_c(self):
        b, b2, c = self.res["B_reformed_market"], self.res["B2_ambitious_cooperative_market"], self.res["C_unira"]
        for k in ("energy_closed_y15", "health_closed_y15", "housing_closed_y30"):
            self.assertGreaterEqual(b2[k], b[k], k)
            self.assertLessEqual(b2[k], c[k], k)

    def test_each_lever_never_hurts_its_own_domain(self):
        b = self.res["B_reformed_market"]
        one = self.res["one_lever_from_B"]
        self.assertLessEqual(one["employment_rate_20_64"]["france_year1_gain_needed"], b["france_year1_gain_needed"])
        self.assertGreaterEqual(one["energy_share_to_regions_in_need"]["energy_closed_y15"], b["energy_closed_y15"])
        self.assertGreaterEqual(one["housing_share_to_regions_in_need"]["housing_closed_y30"], b["housing_closed_y30"])
        self.assertGreaterEqual(one["health_plan"]["health_closed_y15"], b["health_closed_y15"])

    def test_climate_envelope_respected_by_c(self):
        self.assertLessEqual(self.res["C_unira"]["peak_world_energy_ej"], 410)


if __name__ == "__main__":
    unittest.main()
