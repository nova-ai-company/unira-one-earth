import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import capacity  # noqa: E402
import hybrid_real  # noqa: E402


class TestRealData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        capacity.main()
        cls.cap = json.loads((HERE / "outputs" / "capacity.json").read_text())

    def test_france_is_reference(self):
        fr = self.cap["regions"]["FRA"]
        self.assertAlmostEqual(fr["goods_vs_france"], 1.0)
        self.assertAlmostEqual(fr["services_vs_france"], 1.0)
        self.assertGreater(self.cap["countries"], 150)

    def test_services_gap_larger_than_goods_gap(self):
        w = self.cap["world"]
        self.assertLess(w["services_vs_france"], w["goods_vs_france"])

    def test_hybrid_better_start_than_dc(self):
        reg = hybrid_real.wm.regions()
        capf = {k: (v["goods_vs_france"], v["services_vs_france"]) for k, v in self.cap["regions"].items() if k in reg}
        h = hybrid_real.simulate(reg, capf, "hybrid")["year_0"]
        d = hybrid_real.simulate(reg, capf, "DC")["year_0"]
        self.assertGreater(h["poorer_half_vs_full"], d["poorer_half_vs_full"])
        self.assertLess(h["gini"], d["gini"])


if __name__ == "__main__":
    unittest.main()
