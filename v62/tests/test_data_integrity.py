"""Integration tests against the frozen Eurostat snapshots (offline)."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from unira_v62 import fetch, jsonstat, model, tidy  # noqa: E402

RAW = ROOT / "data" / "raw"


class TestSnapshots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = tidy.load_raw(RAW)
        cls.t = tidy.Tables(cls.raw)
        cls.cfg = json.loads((ROOT / "config" / "v62_config.json").read_text())

    def test_hashes_match_manifest(self):
        self.assertEqual(fetch.verify_manifest(RAW), [])

    def test_known_cell_decoded(self):
        # Independently located in nama_10_a64_e: FR 2023 TOTAL EMP_DC THS_HW
        self.assertEqual(self.t.na_emp[(2023, "TOTAL", "EMP_DC", "THS_HW")], 45599310)
        self.assertAlmostEqual(self.t.na_emp[(2023, "TOTAL", "EMP_DC", "THS_PER")], 30375.5)
        self.assertEqual(self.t.lfs_u[(2023, "TOTAL", "SAL", "FT")], 38.9)

    def test_lfs_ft_employee_hours_matches_insee_weekly(self):
        # INSEE reports 38.9 usual weekly hours for full-time employees (2025 edition);
        # Eurostat LFS 2025 gives 38.8 - documented, not identical concept/rounding.
        self.assertAlmostEqual(self.t.lfs_u[(2025, "TOTAL", "SAL", "FT")], 38.9, delta=0.15)

    def test_every_cell_has_time_and_geo(self):
        for stem, (doc, _) in self.raw.items():
            allowed = set(fetch.GEOS) if stem.startswith("eu_") else {"FR"}
            for coords, value, _ in jsonstat.iter_cells(doc):
                self.assertIn(coords["geo"], allowed)
                self.assertTrue(coords["time"].isdigit())

    def test_provisional_years(self):
        self.assertFalse(self.t.is_provisional(2023))
        self.assertTrue(self.t.is_provisional(2024))

    def test_sections_sum_to_total(self):
        y = self.cfg["base_year"]
        tot = self.t.na_emp[(y, "TOTAL", "EMP_DC", "THS_HW")]
        s = sum(self.t.na_emp.get((y, x, "EMP_DC", "THS_HW")) or 0 for x in self.cfg["sectors"] + ["U"])
        self.assertAlmostEqual(s / tot, 1, places=4)

    def test_inferred_part_time_share_matches_direct_count(self):
        y = self.cfg["base_year"]
        for s in ["TOTAL", "C", "G", "P", "Q"]:
            m = model.lfs_means(self.t, y, s, "EMP")
            direct = self.t.lfs_pt[(y, s, "PT")] / self.t.lfs_pt[(y, s, "TOTAL")]
            self.assertAlmostEqual(model.split_parttime(*m[:3]), direct, delta=0.02, msg=s)

    def test_primary_scenario_bounded_by_upper(self):
        y = self.cfg["base_year"]
        sc = {s["id"]: s for s in self.cfg["scenarios"]}
        p = model.run_scenario(self.t, y, sc[self.cfg["primary_scenario"]], self.cfg)[-1]
        u = model.run_scenario(self.t, y, sc[self.cfg["upper_scenario"]], self.cfg)[-1]
        self.assertLess(p["required_hourly_productivity_gain"], u["required_hourly_productivity_gain"])
        self.assertGreater(p["required_hourly_productivity_gain"], 0)

    def test_cap_monotone(self):
        y = self.cfg["base_year"]
        gains = []
        for cap in (30, 32, 35, 40):
            sc = {"id": f"c{cap}", "cap": cap, "apply_to": ["SAL", "SELF"], "annual_method": "constant_absence"}
            gains.append(model.run_scenario(self.t, y, sc, self.cfg)[-1]["required_hourly_productivity_gain"])
        self.assertEqual(gains, sorted(gains, reverse=True))


if __name__ == "__main__":
    unittest.main()
