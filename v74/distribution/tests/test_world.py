import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import world  # noqa: E402

EQUAL = {"SI.DST.FRST.10": 10, "SI.DST.FRST.20": 20, "SI.DST.02ND.20": 20, "SI.DST.03RD.20": 20,
         "SI.DST.04TH.20": 20, "SI.DST.05TH.20": 20, "SI.DST.10TH.10": 10}


class TestWorld(unittest.TestCase):
    def test_equal_distribution_all_at_mean(self):
        levels, tot = world.group_levels(EQUAL)
        self.assertAlmostEqual(tot, 100)
        for _, r in levels:
            self.assertAlmostEqual(r, 1.0)

    def test_levels_average_to_mean(self):
        sh = {"SI.DST.FRST.10": 2, "SI.DST.FRST.20": 6, "SI.DST.02ND.20": 11, "SI.DST.03RD.20": 16,
              "SI.DST.04TH.20": 23, "SI.DST.05TH.20": 44, "SI.DST.10TH.10": 29}
        levels, _ = world.group_levels(sh)
        widths = [b - a for a, b, _ in world.GROUPS]
        self.assertAlmostEqual(sum(w * r for w, (_, r) in zip(widths, levels)), 1.0)
        self.assertEqual([r for _, r in levels], sorted(r for _, r in levels))

    def test_share_below_monotone(self):
        sh = {"SI.DST.FRST.10": 2, "SI.DST.FRST.20": 6, "SI.DST.02ND.20": 11, "SI.DST.03RD.20": 16,
              "SI.DST.04TH.20": 23, "SI.DST.05TH.20": 44, "SI.DST.10TH.10": 29}
        levels, _ = world.group_levels(sh)
        shares = [world.share_below(levels, b) for b in (0.1, 0.4, 0.8, 1.2, 3.5)]
        self.assertEqual(shares, sorted(shares))
        self.assertEqual(world.share_below(levels, 10), 1.0)

    def test_france_matches_eurostat(self):
        # World Bank shares and Eurostat deciles must tell the same story for France
        wb = json.loads((HERE.parent / "outputs" / "distribution_world.json").read_text())["regions"]["FRA"]
        es = json.loads((HERE.parent / "outputs" / "distribution.json").read_text())["regions"]["FR"]
        self.assertAlmostEqual(wb["share_of_people_better_off_at_base"], es["share_of_people_who_gain_at_base_level"], delta=0.05)
        self.assertAlmostEqual(wb["poorest_tenth_level_vs_mean"], es["decile_relative_standard"]["1"], delta=0.03)

    def test_all_rich_regions_covered_or_listed(self):
        s = json.loads((HERE.parent / "outputs" / "distribution_world.json").read_text())["rich_regions_summary"]
        self.assertEqual(s["n_with_data"] + len(s["without_income_data"]), s["n_rich_regions"])

    def test_people_based_count(self):
        pb = json.loads((HERE.parent / "outputs" / "distribution_world.json").read_text())["people_based"]
        self.assertGreater(pb["share_of_humanity_better_off"], pb["share_in_gaining_regions"])
        self.assertLess(pb["better_off_in_rich_regions_millions"], pb["people_in_rich_regions_millions"])


if __name__ == "__main__":
    unittest.main()
