import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import model  # noqa: E402
import run  # noqa: E402


class TestPerceiver(unittest.TestCase):
    def test_perfect_information_is_identity(self):
        regs = {"A": {}, "B": {}}
        gov = {"sigma": 0.0, "lag": 0, "misreport_share": 0.0, "inflation": 0.0, "audit_detect": 0.0, "leakage": 0.0}
        f = model.make_perceiver(regs, gov, 1)
        self.assertEqual(f("energy", 0, {"A": 5.0, "B": 0.0}), {"A": 5.0, "B": 0.0})

    def test_lag_uses_old_needs(self):
        regs = {"A": {}}
        gov = {"sigma": 0.0, "lag": 2, "misreport_share": 0.0, "inflation": 0.0, "audit_detect": 0.0, "leakage": 0.0}
        f = model.make_perceiver(regs, gov, 1)
        f("energy", 0, {"A": 10.0})
        f("energy", 1, {"A": 8.0})
        self.assertEqual(f("energy", 2, {"A": 6.0}), {"A": 10.0})

    def test_noise_mean_preserving(self):
        regs = {f"R{i}": {} for i in range(2000)}
        gov = {"sigma": 0.3, "lag": 0, "misreport_share": 0.0, "inflation": 0.0, "audit_detect": 0.0, "leakage": 0.0}
        seen = model.make_perceiver(regs, gov, 3)("energy", 0, {k: 1.0 for k in regs})
        self.assertAlmostEqual(sum(seen.values()) / len(seen), 1.0, delta=0.03)

    def test_quantiles(self):
        self.assertEqual(model.quantiles([1, 2, 3, 4, 5]), [1.4, 3, 4.6])


class TestWorld(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = run.compare.load_config()
        cls.regions = run.compare.rt.load_regions()
        cls.cap = json.loads((ROOT.parents[1] / "v66" / "construction" / "capacity.json").read_text())
        cls.s = run.compare.settings(cls.cfg, {k: "C" for k in cls.cfg["lever_order"]})

    def gov(self, **kw):
        g = {"sigma": 0.0, "lag": 0, "misreport_share": 0.0, "inflation": 0.0, "audit_detect": 0.0, "leakage": 0.0}
        g.update(kw)
        return g

    def test_perfect_matches_v68_unira(self):
        r = run.world_with_gov(self.s, self.regions, self.cfg, self.cap, self.gov(), 0)
        comp = json.loads((ROOT.parents[1] / "v68" / "outputs" / "comparison.json").read_text())["C_unira"]
        self.assertAlmostEqual(r["energy_closed_y15"], comp["energy_closed_y15"], places=6)

    def test_leakage_hurts(self):
        a = run.world_with_gov(self.s, self.regions, self.cfg, self.cap, self.gov(), 0)
        b = run.world_with_gov(self.s, self.regions, self.cfg, self.cap, self.gov(leakage=0.3), 0)
        self.assertLess(b["energy_closed_y15"], a["energy_closed_y15"])

    def test_audits_help_against_misreporting(self):
        g = dict(misreport_share=0.3, inflation=1.0)
        no = run.world_with_gov(self.s, self.regions, self.cfg, self.cap, self.gov(**g), 5)
        yes = run.world_with_gov(self.s, self.regions, self.cfg, self.cap, self.gov(audit_detect=0.5, **g), 5)
        self.assertGreaterEqual(yes["housing_closed_y30"], no["housing_closed_y30"])


if __name__ == "__main__":
    unittest.main()
