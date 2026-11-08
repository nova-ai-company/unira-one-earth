import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import one_member as om  # noqa: E402


class TestOneMember(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = om.main(write=False)
        cls.C = cls.out["candidates"]

    def test_reproducible(self):
        again = om.main(write=False)
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.out, sort_keys=True))

    def test_candidates_match_first_region_screen(self):
        fr = json.loads((ROOT.parents[1] / "v72" / "outputs" / "first_region.json").read_text())
        self.assertEqual(set(self.C), {r["region"] for r in fr["candidates"]})
        self.assertIn("IND", self.C)

    def test_accounting_identities(self):
        for k, r in self.C.items():
            self.assertAlmostEqual(r["trade_balance_pct_gdp"], r["exports_pct_gdp"] - r["imports_pct_gdp"], delta=0.11, msg=k)
            if r["essential_import_share_floor"] is not None:
                self.assertGreater(r["essential_import_share_floor"], 0)
                self.assertLessEqual(r["essential_import_share_floor"], 1)
                self.assertAlmostEqual(r["reserves_months_of_essential_imports"],
                                       r["reserves_months_of_imports"] / r["essential_import_share_floor"], delta=0.2)

    def test_bigger_shocks_breach_sooner_and_leave_less(self):
        for k, r in self.C.items():
            s = r["scenarios"]
            for su in (0, 10):
                prev_res, prev_breach = None, None
                for sh in (0, 10, 25, 40):
                    v = s[f"export_shock_{sh}|needs_surge_{su}"]
                    if prev_res is not None:
                        self.assertLessEqual(v["reserves_year5_months_of_imports"], prev_res, (k, sh, su))
                        if prev_breach is not None:
                            self.assertIsNotNone(v["first_year_below_six_months_of_essential_imports"])
                            self.assertLessEqual(v["first_year_below_six_months_of_essential_imports"], prev_breach)
                    prev_res, prev_breach = v["reserves_year5_months_of_imports"], v["first_year_below_six_months_of_essential_imports"]

    def test_export_growth_needed_rises_with_needs_surge(self):
        for k, r in self.C.items():
            g = r["export_growth_needed_for_5y_balance"]
            self.assertGreaterEqual(g["needs_surge_10"], g["needs_surge_0"], k)

    def test_pareto_tail_behaves(self):
        share, alpha = om.pareto_share_above(30.0, 47.0, 19.0)
        self.assertIsNotNone(share)
        self.assertGreater(alpha, 1)
        self.assertLess(share, 0.01)
        share2, _ = om.pareto_share_above(30.0, 47.0, 10.0)
        self.assertGreater(share2, share)  # a lower ceiling catches more people
        for k, r in self.C.items():
            t = r["top_of_scale"]
            if t.get("share_of_people_above_ceiling") is not None:
                self.assertLess(t["share_of_people_above_ceiling"], 0.05, k)

    def test_price_level_below_world_for_candidates(self):
        for k, r in self.C.items():
            if r["price_level_vs_world"] is not None:
                self.assertLess(r["price_level_vs_world"], 1.0, k)
                self.assertGreater(r["price_level_vs_world"], 0.1, k)


if __name__ == "__main__":
    unittest.main()
