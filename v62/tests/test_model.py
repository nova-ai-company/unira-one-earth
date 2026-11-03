"""Unit tests for the V6.2 labour-hours arithmetic (synthetic inputs, known answers)."""
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from unira_v62 import model  # noqa: E402


class FakeTables:
    """Minimal stand-in for tidy.Tables with one sector 'X'."""

    def __init__(self, lfs, na_emp, na_out=None):
        self.lfs_u, self.na_emp, self.na_out = lfs, na_emp, na_out or {}
        self.slack, self.lfs_pt = {}, {}


def one_sector(u=(36.0, 40.0, 20.0), H=4000.0, N=100.0, selfH=0.0, selfN=0.0, self_u=None):
    lfs = {(2023, "X", "SAL", t): v for t, v in zip(("TOTAL", "FT", "PT"), u)}
    if self_u:
        lfs.update({(2023, "X", "NSAL", t): v for t, v in zip(("TOTAL", "FT", "PT"), self_u)})
    na = {(2023, "X", "SAL_DC", "THS_HW"): H, (2023, "X", "SAL_DC", "THS_PER"): N,
          (2023, "X", "SELF_DC", "THS_HW"): selfH, (2023, "X", "SELF_DC", "THS_PER"): selfN}
    cfg = {"sectors": ["X"], "trend_windows": [],
           "nonmarket_output_sectors": {"sectors": []}, "imputed_output_sectors": {"sectors": []}}
    return FakeTables(lfs, na), cfg


SCEN = {"id": "t", "cap": 30, "apply_to": ["SAL", "SELF"], "annual_method": "constant_absence"}


class TestPartTimeSplit(unittest.TestCase):
    def test_recovers_known_share(self):
        # 20% part-time at 20h, 80% full-time at 40h -> mean 36h
        self.assertAlmostEqual(model.split_parttime(36, 40, 20), 0.2)

    def test_clipped(self):
        self.assertEqual(model.split_parttime(41, 40, 20), 0.0)
        self.assertEqual(model.split_parttime(19, 40, 20), 1.0)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            model.split_parttime(30, 20, 25)
        with self.assertRaises(ValueError):
            model.split_parttime(None, 40, 20)


class TestCap(unittest.TestCase):
    def test_retained_weekly(self):
        # 0.2*20 + 0.8*30 = 28
        self.assertAlmostEqual(model.retained_weekly(36, 40, 20, 30), 28)

    def test_cap_above_all_hours_is_neutral(self):
        self.assertAlmostEqual(model.retained_weekly(36, 40, 20, 45), 36)

    def test_group_mean_is_upper_bound_on_retained_hours(self):
        # Explicit micro-distribution: mean(min(x,c)) <= group-mean formula
        ft, pt = [32, 35, 50, 43], [10, 20, 31, 27]
        x = ft + pt
        exact = sum(min(v, 30) for v in x) / len(x)
        approx = model.retained_weekly(sum(x) / len(x), sum(ft) / 4, sum(pt) / 4, 30)
        self.assertLessEqual(exact, approx + 1e-12)

    def test_tail_reduces_hours(self):
        base = model.retained_weekly(36, 40, 20, 30)
        tail = model.retained_weekly(36, 40, 20, 30, tail_share=0.25, tail_hours=34)
        self.assertAlmostEqual(base - tail, 0.2 * 0.25 * 4)

    def test_inconsistent_tail_rejected(self):
        with self.assertRaises(ValueError):
            model.retained_weekly(36, 40, 20, 30, tail_share=0.9, tail_hours=34)


class TestScenarioArithmetic(unittest.TestCase):
    def test_constant_absence_known_answer(self):
        t, cfg = one_sector()
        row = model.sector_rows(t, 2023, SCEN, cfg)[0]
        self.assertAlmostEqual(row["hours_after_ths"], 4000 * 28 / 36)
        self.assertAlmostEqual(row["required_hourly_productivity_gain"], 36 / 28 - 1)
        self.assertAlmostEqual(row["additional_persons_same_profile_ths"], 100 * (36 / 28 - 1))
        self.assertAlmostEqual(row["breakeven_avoidable_output_share"], 1 - 28 / 36)

    def test_constant_absence_is_level_invariant(self):
        t1, cfg = one_sector(H=4000)
        t2, _ = one_sector(H=3000)
        g1 = model.sector_rows(t1, 2023, SCEN, cfg)[0]["required_hourly_productivity_gain"]
        g2 = model.sector_rows(t2, 2023, SCEN, cfg)[0]["required_hourly_productivity_gain"]
        self.assertAlmostEqual(g1, g2)

    def test_normative_weeks_known_answer(self):
        # H/N = 40 h/week-units -> weeks = 40/36; use H to get 40 weeks: H/N = 1440 -> weeks 40
        t, cfg = one_sector(H=144000, N=100)
        scen = dict(SCEN, annual_method="normative_weeks", weeks=46)
        row = model.sector_rows(t, 2023, scen, cfg)[0]
        # FT annual = 40*40 = 1600 -> capped 1380; PT annual = 800 unchanged
        expected = 100 * (0.8 * 1380 + 0.2 * 800)
        self.assertAlmostEqual(row["hours_after_ths"], expected)

    def test_extra_weeks_ft(self):
        t, cfg = one_sector(H=144000, N=100)
        scen = dict(SCEN, extra_weeks_ft=2)
        row = model.sector_rows(t, 2023, scen, cfg)[0]
        self.assertAlmostEqual(row["hours_after_ths"], 144000 * 28 / 36 + 100 * 0.8 * 2 * 30)

    def test_observed_is_identity(self):
        t, cfg = one_sector()
        row = model.sector_rows(t, 2023, {"id": "A", "cap": None}, cfg)[0]
        self.assertEqual(row["hours_after_ths"], row["hours_before_ths"])
        self.assertEqual(row["required_hourly_productivity_gain"], 0)

    def test_apply_to_excludes_self_employed(self):
        t, cfg = one_sector(selfH=1000, selfN=20, self_u=(45, 50, 20))
        scen = dict(SCEN, apply_to=["SAL"])
        row = model.sector_rows(t, 2023, scen, cfg)[0]
        self.assertEqual(row["SELF_hours_after_ths"], 1000)
        # extra persons only for the capped group
        self.assertAlmostEqual(row["additional_persons_same_profile_ths"], 100 * (36 / 28 - 1))

    def test_missing_persons_cell_raises_instead_of_dropping_hours(self):
        t, cfg = one_sector()
        del t.na_emp[(2023, "X", "SAL_DC", "THS_PER")]
        with self.assertRaises(ValueError):
            model.sector_rows(t, 2023, {"id": "A", "cap": None}, cfg)

    def test_extra_weeks_not_applied_to_self_employed(self):
        t, cfg = one_sector(H=144000, N=100, selfH=1000, selfN=20, self_u=(45, 50, 20))
        row = model.sector_rows(t, 2023, dict(SCEN, extra_weeks_ft=2), cfg)[0]
        q = model.split_parttime(45, 50, 20)
        self.assertAlmostEqual(row["SELF_hours_after_ths"],
                               1000 * model.retained_weekly(45, 50, 20, 30) / 45)
        self.assertGreater(q, 0)

    def test_normative_weeks_is_not_a_30h_cap(self):
        # 38.7 effective weeks: 30*46 annual cap permits > 35 h/week actually worked
        self.assertGreater(30 * 46 / 38.7, 35)

    def test_missing_lfs_raises(self):
        t, cfg = one_sector()
        t.lfs_u = {}
        with self.assertRaises(ValueError):
            model.sector_rows(t, 2023, SCEN, cfg)


class TestOffset(unittest.TestCase):
    def test_offset_bounds(self):
        self.assertAlmostEqual(model.residual_gain_with_offset(120, 100, 0), 0.2)
        self.assertAlmostEqual(model.residual_gain_with_offset(120, 100, 1), 0.0)
        self.assertAlmostEqual(model.residual_gain_with_offset(120, 100, 0.5), 120 / 110 - 1)
        with self.assertRaises(ValueError):
            model.residual_gain_with_offset(120, 100, 1.5)


class TestLabourReserve(unittest.TestCase):
    def _cd(self, une=10.0, navl=0.0, emp_rate=70.0):
        from unira_v62 import labour_reserve as lr
        cd = lr.CountryData.__new__(lr.CountryData)
        cd.na = {("XX", 2023, "SAL_DC", "THS_HW"): 144000.0, ("XX", 2023, "SAL_DC", "THS_PER"): 100.0,
                 ("XX", 2023, "SELF_DC", "THS_HW"): 0.0, ("XX", 2023, "SELF_DC", "THS_PER"): 0.0}
        cd.lfs_u = {("XX", 2023, "SAL", t): v for t, v in (("TOTAL", 36.0), ("FT", 40.0), ("PT", 20.0))}
        cd.slack = {("XX", 2023, "Y20-64", "UNE"): une, ("XX", 2023, "Y20-64", "SEEK_NAVL"): navl,
                    ("XX", 2023, "Y20-64", "NSEEK_AVL"): 0.0, ("XX", 2023, "Y20-64", "UEMP_PT"): 0.0}
        cd.emp = {("XX", 2023, "Y20-64", "THS_PER"): emp_rate * 2, ("XX", 2023, "Y20-64", "PC_POP"): emp_rate,
                  ("YY", 2023, "Y20-64", "PC_POP"): 80.0}
        cd.pt_reason, cd.inact = {}, {}
        return lr, cd

    def params(self, rho=1.0):
        return {"apply_to": ["SAL"], "age_band": "Y20-64", "entrant_weekly_hours": 30,
                "entrant_relative_productivity": rho, "benchmarks": {"top1": "top1_mean"}}

    def test_known_answer_and_level_invariance(self):
        lr, cd = self._cd(une=10.0)
        r = lr.evaluate(cd, "XX", 2023, self.params())
        # gap = 100*(1-28/36) person-units of weekly hours; supply = 10*30 -> share = 300/(100*8)
        self.assertAlmostEqual(r["slack_gap_closed_share"], 10 * 30 / (100 * 8))
        cd.na[("XX", 2023, "SAL_DC", "THS_HW")] = 100000.0   # change effective weeks
        r2 = lr.evaluate(cd, "XX", 2023, self.params())
        self.assertAlmostEqual(r["slack_gap_closed_share"], r2["slack_gap_closed_share"])

    def test_benchmark_is_alternative_not_additive(self):
        lr, cd = self._cd(une=10.0, emp_rate=70.0)   # pop 200k; 10pp gap -> 20k persons
        r = lr.evaluate(cd, "XX", 2023, self.params())
        self.assertAlmostEqual(r["bench_top1_employment_gap_persons_ths"], 20.0)
        self.assertAlmostEqual(r["bench_top1_persons_ths"], 20.0)       # not 30
        lr, cd = self._cd(une=50.0, emp_rate=70.0)
        r = lr.evaluate(cd, "XX", 2023, self.params())
        self.assertAlmostEqual(r["bench_top1_persons_ths"], 50.0)       # slack exceeds gap

    def test_higher_cap_smaller_gap_and_longer_entrant_week(self):
        lr, cd = self._cd(une=10.0)
        p30 = self.params()
        p35 = dict(p30, entrant_weekly_hours=35)
        r30, r35 = lr.evaluate(cd, "XX", 2023, p30), lr.evaluate(cd, "XX", 2023, p35)
        self.assertLess(r35["hours_gap_ths"], r30["hours_gap_ths"])
        self.assertEqual(r35["weekly_cap"], 35)
        # 35h cap: retained = 0.2*20 + 0.8*35 = 32 -> gap per person-week 4; supply 10*35
        self.assertAlmostEqual(r35["slack_gap_closed_share"], 10 * 35 / (100 * 4))

    def test_entrant_productivity_scales_supply(self):
        lr, cd = self._cd()
        a = lr.evaluate(cd, "XX", 2023, self.params(1.0))["slack_hours_supplied_ths"]
        b = lr.evaluate(cd, "XX", 2023, self.params(0.75))["slack_hours_supplied_ths"]
        self.assertAlmostEqual(b / a, 0.75)


class TestPathway(unittest.TestCase):
    def test_pathway_arithmetic(self):
        rows = [{"nace_r2": "C", "hours_before_ths": 100.0, "hours_after_ths": 80.0},
                {"nace_r2": "Q", "hours_before_ths": 100.0, "hours_after_ths": 80.0}]
        reserve = {"bench_top3_persons_ths": 10.0, "entrant_annual_hours": 1.0, "t3_extra_hours_ths": 2.0}
        case = {"theta_market": 0.5, "theta_care": 0.0, "take_up": 0.5, "entrant_relative_productivity": 1.0}
        r = model.evidence_pathway(rows, reserve, case, ["Q"])
        # offset 10, supply (5*1 + 1)*1 = 6 -> effective 176
        self.assertAlmostEqual(r["residual_required_gain"], 200 / 176 - 1)
        self.assertAlmostEqual(r["share_closed_by_theta"], 0.25)

    def test_pathway_never_negative(self):
        rows = [{"nace_r2": "C", "hours_before_ths": 100.0, "hours_after_ths": 80.0}]
        reserve = {"bench_top3_persons_ths": 1000.0, "entrant_annual_hours": 1.0, "t3_extra_hours_ths": 0.0}
        case = {"theta_market": 0.0, "theta_care": 0.0, "take_up": 1.0, "entrant_relative_productivity": 1.0}
        self.assertEqual(model.evidence_pathway(rows, reserve, case, [])["residual_required_gain"], 0)


class TestTrend(unittest.TestCase):
    def test_cagr(self):
        self.assertAlmostEqual(model.cagr(100, 121, 2), 0.1)
        self.assertIsNone(model.cagr(None, 1, 1))

    def test_years_to_cover(self):
        self.assertAlmostEqual(model.years_to_cover(0.21, 0.1), 2.0)
        self.assertEqual(model.years_to_cover(0.2, -0.01), math.inf)
        self.assertEqual(model.years_to_cover(-0.1, 0.01), 0.0)

    def test_weeks_flag(self):
        self.assertEqual(model.weeks_flag(40), "")
        self.assertEqual(model.weeks_flag(60), "NA_LFS_inconsistent")


if __name__ == "__main__":
    unittest.main()
