import hashlib
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import simulate  # noqa: E402

OUT = HERE.parent / "outputs" / "integrated.json"


class TestIntegrated(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        simulate.main()
        cls.h1 = hashlib.sha256(OUT.read_bytes()).hexdigest()
        cls.d = json.loads(OUT.read_text())["scenarios"]

    def test_reproducible_byte_for_byte(self):
        simulate.main()
        self.assertEqual(hashlib.sha256(OUT.read_bytes()).hexdigest(), self.h1)

    def test_coverage_shares_valid_and_level2_not_above_level1(self):
        for s in self.d.values():
            for a, b in zip(s["coverage_L1"], s["coverage_L2"]):
                self.assertTrue(0.0 <= b <= a + 1e-9 <= 1.0 + 1e-9)

    def test_scenarios_ordered(self):
        y = lambda s: s["dates"]["L1"]["90pct"] or 999
        self.assertGreaterEqual(y(self.d["conservative"]), y(self.d["moderate"]))
        self.assertGreaterEqual(y(self.d["moderate"]), y(self.d["accelerated"]))
        self.assertGreaterEqual(y(self.d["accelerated"]), y(self.d["accelerated_if_conflicts_end"]))

    def test_constitutional_thresholds_unchanged(self):
        b = json.loads((simulate.U / "v87" / "livingstandard" / "basket.json").read_text())["domains"]
        self.assertEqual((b["housing"]["essential"], b["housing"]["comfortable"]), (15, 27))
        self.assertEqual((b["health"]["essential"], b["health"]["comfortable"]), (44.5, 131))
        self.assertEqual((b["energy"]["essential"], b["energy"]["comfortable"]), (15.3, 40))


if __name__ == "__main__":
    unittest.main()
