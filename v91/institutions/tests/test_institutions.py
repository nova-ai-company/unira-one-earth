import json
import random
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import model  # noqa: E402
import panel  # noqa: E402


class TestInstitutions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w = model.World()
        cls.out = model.main(runs=2, write=False, sens=False, world=cls.w)
        cls.s = cls.out["scenarios"]

    def test_reproducible(self):
        again = model.main(runs=2, write=False, sens=False, world=model.World())
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.out, sort_keys=True))

    def test_panel_uses_no_violence_indicator(self):
        self.assertNotIn("GOV_WGI_PV.EST", panel.WGI)  # political stability measures violence: circular

    def test_panel_institutions_associated_with_fewer_onsets(self):
        c = self.w.panel["onset"]["LS_and_Q"]["coefficients"]
        self.assertLess(c["q"]["ci95"][1], 0)
        self.assertGreater(c["recent"]["estimate"], 0)

    def test_scenarios_ordered(self):
        cy = [self.s[n]["conflict_country_years_80y"] for n in model.SCEN]
        self.assertEqual(cy, sorted(cy, reverse=True))

    def test_baseline_keeps_todays_conflicts(self):
        c = self.s["A_baseline"]["countries_in_conflict"]
        mean = sum(c[f"year_{t}"] for t in (20, 40, 60, 80)) / 4
        self.assertLess(abs(mean - self.out["countries_in_conflict_2024_ucdp"]), 0.4 * self.out["countries_in_conflict_2024_ucdp"])

    def test_economics_separated(self):
        self.assertEqual(set(self.out["factorial_economics_off"]), set(model.SCEN))
        for p in model.SCEN.values():
            self.assertEqual(p["cE"], model.COMMON["cE"])  # same economic channel in every institutional scenario

    def test_reform_never_reduces_delivery_or_withholds_services(self):
        """Delivery factors: conflict at worst halves delivery and never removes it; reform only raises fragile
        countries' factor; institutional quality never enters the entitlement (capfn depends on conflict only)."""
        w = self.w
        for k in w.keys:
            self.assertGreaterEqual(1 - 0.5 * w.aff[k] / model.AFFECTED, 0.5 - 1e-12)
            self.assertGreaterEqual(1 - w.aff[k], 0.75 - 1e-12)
        p = model.SCEN["D_comprehensive_reform"]
        qp = model.q_paths(w, p, random.Random(1))
        for k in w.keys:
            self.assertTrue(all(q >= w.q0[k] - 1e-12 for q in qp[k]))

    def test_reversal_undoes_a_decade(self):
        p = model.SCEN["C_strong_reform"] | {"reversal": 1.0}
        qp = model.q_paths(self.w, p, random.Random(3))
        k = min(self.w.keys, key=lambda x: self.w.q0[x])
        self.assertAlmostEqual(qp[k][10], self.w.q0[k])
        self.assertGreater(qp[k][9], self.w.q0[k])

    def test_only_D_is_comprehensive_upper_bound(self):
        self.assertEqual([n for n, p in model.SCEN.items() if p["cooperation"]], ["D_comprehensive_reform"])

    def test_tension_only_where_institutions_weak(self):
        w, p = self.w, model.SCEN["C_strong_reform"]
        ls = w.ls0
        k = min(w.keys, key=lambda x: w.q0[x])
        qp = {x: [w.q0[x]] * (model.YEARS + 1) for x in w.keys}
        self.assertGreater(model.onset_p(w, p, k, ls, qp, 5, False, True), model.onset_p(w, p, k, ls, qp, 5, False, False))


if __name__ == "__main__":
    unittest.main()
