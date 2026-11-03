import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestJoining(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "run.py"], cwd=ROOT, check=True, capture_output=True)
        cls.r = json.loads((ROOT.parent / "outputs" / "joining.json").read_text())

    def test_shares_sum_to_one(self):
        self.assertAlmostEqual(self.r["gainers_share_of_world_pop"] + self.r["losers_share_of_world_pop"], 1.0, places=6)

    def test_poor_regions_gain_rich_regions_lose_little(self):
        reg = self.r["regions"]
        for k in ("IND", "NGA", "ETH"):
            self.assertGreater(reg[k]["material_change_pct"], 0)
        for k in ("FRA", "USA", "DEU"):
            self.assertLess(reg[k]["material_change_pct"], 0)
            self.assertGreater(reg[k]["material_change_pct"], -25)   # losses modest
            self.assertAlmostEqual(reg[k]["health_ratio"], 1.0, delta=0.05)

    def test_union_of_gainers_slower_than_whole_world_but_positive(self):
        u = self.r["union_of_gainers"]["outcomes"]
        w = self.r["whole_world_unira_outcomes"]
        for k in u:
            self.assertGreater(u[k], 0)
            self.assertLessEqual(u[k], w[k] + 1e-9)


if __name__ == "__main__":
    unittest.main()
