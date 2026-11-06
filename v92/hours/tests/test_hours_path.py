import csv
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import hours_path as hp  # noqa: E402


class TestHoursPath(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res = hp.main(write=False)
        cls.fr = cls.res["france"]["2023"]

    def test_reproducible(self):
        again = hp.main(write=False)
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.res, sort_keys=True))

    def test_france_matches_v62_research_note(self):
        # v62 §4d: at 35 h the existing reserve covers 142% of the gap (rho 1.0) and the residual is 0
        sw = self.res["starting_week"]["FR"]["2023"]
        self.assertEqual(sw["1.0"], 34)
        self.assertEqual(sw["0.75"], 35)
        r35 = self.fr["1.0"][5]
        self.assertEqual(r35["cap"], 35)
        self.assertAlmostEqual(r35["reserve_closes_share"], 1.42, places=2)
        self.assertEqual(r35["residual_gain"], 0.0)

    def test_cap30_row_equals_v62_output(self):
        rows = [r for r in csv.DictReader((hp.V62 / "outputs" / "labour_reserve_country_year.csv").open())
                if r["geo"] == "FR" and r["year"] == "2023" and r["weekly_cap"] == "30" and r["apply_to"] == "SAL"
                and r["entrant_relative_productivity"] == "1.0"]
        self.assertEqual(len(rows), 1)
        # v62 writes its CSV rounded to 6 decimals
        self.assertAlmostEqual(self.fr["1.0"][0]["gain_no_mobilisation"], float(rows[0]["required_gain_no_mobilisation"]), places=5)
        self.assertAlmostEqual(self.fr["1.0"][0]["residual_gain"], float(rows[0]["slack_residual_gain"]), places=5)

    def test_monotone_in_cap(self):
        for rho, rows in self.fr.items():
            for a, b in zip(rows, rows[1:]):
                self.assertLessEqual(b["hours_lost_share"], a["hours_lost_share"] + 1e-12)
                self.assertLessEqual(b["residual_gain"], a["residual_gain"] + 1e-12)
            self.assertEqual(rows[-1]["residual_gain"], 0.0)  # at 40 h nothing is lost in France

    def test_starting_week_is_the_first_cap_with_no_residual(self):
        for geo, years in self.res["starting_week"].items():
            for year, by_rho in years.items():
                for rho, sw in by_rho.items():
                    if sw is None:
                        continue
                    self.assertIn(sw, hp.CAPS)
                    if geo == "FR" and year == "2023":
                        rows = self.fr[rho]
                        self.assertEqual(rows[sw - 30]["residual_gain"], 0.0)
                        if sw > 30:
                            self.assertGreater(rows[sw - 31]["residual_gain"], 0.0)

    def test_lower_entrant_productivity_never_shortens_the_start(self):
        for geo, years in self.res["starting_week"].items():
            for by_rho in years.values():
                if by_rho.get("1.0") is not None and by_rho.get("0.75") is not None:
                    self.assertGreaterEqual(by_rho["0.75"], by_rho["1.0"])

    def test_years_to_target(self):
        self.assertEqual(hp.years_to_target(30, 0.01), 0)
        self.assertIsNone(hp.years_to_target(35, 0.0))
        self.assertEqual(hp.years_to_target(35, 0.01), 16)  # 35/1.01^16 = 29.85 < 30 < 35/1.01^15
        self.assertEqual(hp.years_to_target(40, 0.03), 10)
        y = self.res["years_to_30h_by_start"]["35"]
        self.assertGreater(y["FR_trend_2015_2023"], y["FR_trend_2015_2019"])  # slower trend, later arrival

    def test_distribution_covers_all_countries(self):
        d = self.res["distribution_2023_countries"]
        for rho in ("1.0", "0.75"):
            self.assertEqual(sum(d[rho].values()), d["n"])
        self.assertGreaterEqual(d["n"], 25)
        self.assertIn("EU27_2020", self.res["starting_week"])  # the aggregate is reported but not counted

    def test_no_country_needs_more_than_40h_at_central_assumption(self):
        for geo, years in self.res["starting_week"].items():
            if "2023" in years and geo not in hp.AGGREGATES:
                self.assertIsNotNone(years["2023"]["0.75"], geo)


if __name__ == "__main__":
    unittest.main()
