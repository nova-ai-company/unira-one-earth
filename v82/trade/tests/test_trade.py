import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import analysis  # noqa: E402


class TestTrade(unittest.TestCase):
    def test_outputs(self):
        analysis.main()
        r = json.loads((HERE / "outputs" / "trade.json").read_text())
        self.assertLess(r["essential_imports_meur"], r["imports_meur"])
        self.assertGreater(r["exports_cover_essential_imports_times"], 1.0)
        self.assertAlmostEqual(r["reserve_meur"], r["essential_imports_meur"] * r["reserve_months"] / 12, delta=2)


if __name__ == "__main__":
    unittest.main()
