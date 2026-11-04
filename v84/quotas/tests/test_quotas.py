import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compare  # noqa: E402


class TestQuotas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reg = compare.wm.regions()
        cls.r = {s: compare.simulate(reg, s) for s in ("s1_DC", "s2_DCQ", "s3_hybrid")}

    def test_hybrid_has_no_unspendable_money(self):
        for y in ("year_0", "year_20", "year_40"):
            self.assertAlmostEqual(self.r["s3_hybrid"][y]["unspendable_money_share_of_income"], 0.0, places=6)

    def test_equal_salaries_leave_money_unspendable(self):
        self.assertGreater(self.r["s2_DCQ"]["year_0"]["unspendable_money_share_of_income"], 0.3)

    def test_quotas_reduce_inequality(self):
        self.assertLess(self.r["s3_hybrid"]["year_0"]["gini_real_between_regions"], self.r["s1_DC"]["year_0"]["gini_real_between_regions"])

    def test_same_real_outcome_q_and_hybrid(self):
        a, b = self.r["s2_DCQ"]["year_20"], self.r["s3_hybrid"]["year_20"]
        self.assertAlmostEqual(a["real_poorer_half_vs_full"], b["real_poorer_half_vs_full"], places=6)

    def test_unspendable_money_hurts_equal_salaries_not_hybrid(self):
        reg = compare.wm.regions()
        q = compare.simulate(reg, "s2_DCQ", effort=0.5)["year_20"]["real_poorer_half_vs_full"]
        h = compare.simulate(reg, "s3_hybrid", effort=0.5)["year_20"]["real_poorer_half_vs_full"]
        self.assertLess(q, h)

    def test_hybrid_beats_dc_across_goods_shares(self):
        reg = compare.wm.regions()
        for g in (0.24, 0.35, 0.45):
            h = compare.simulate(reg, "s3_hybrid", goods=g)["year_0"]["real_poorer_half_vs_full"]
            d = compare.simulate(reg, "s1_DC", goods=g, credit_share=0.0)["year_0"]["real_poorer_half_vs_full"]
            self.assertGreater(h, d)


if __name__ == "__main__":
    unittest.main()
