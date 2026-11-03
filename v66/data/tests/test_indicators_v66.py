"""Tests for the V6.6 indicators dataset.  Run from v66/data:
    python3 -I -m unittest discover -s tests -v
"""
import csv
import sys
import tempfile
import unittest
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
DATA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DATA))

import build  # noqa: E402

CSV = DATA / "indicators_v66.csv"


def rows():
    with CSV.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestIndicatorsV66(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = rows()
        cls.by = defaultdict(dict)
        for r in cls.rows:
            cls.by[r["indicator_id"]][r["iso3"]] = r

    def test_raw_hashes_match_manifest(self):
        self.assertEqual(build.verify_manifest(DATA / "raw"), [])

    def test_manifest_columns_and_licenses(self):
        with (DATA / "raw" / "raw_manifest.csv").open(newline="") as f:
            rd = csv.DictReader(f)
            self.assertEqual(rd.fieldnames,
                             ["file", "source", "url", "retrieved_at_utc", "sha256", "bytes", "license"])
            for r in rd:
                self.assertTrue(r["license"] and r["url"].startswith("https://"), r["file"])

    def test_columns(self):
        with CSV.open(newline="", encoding="utf-8") as f:
            self.assertEqual(next(csv.reader(f)), build.COLS)

    def test_no_duplicate_iso3_indicator(self):
        c = Counter((r["iso3"], r["indicator_id"]) for r in self.rows)
        self.assertEqual([k for k, n in c.items() if n > 1], [])

    def test_iso3_evidence_numeric(self):
        for r in self.rows:
            self.assertRegex(r["iso3"], r"^[A-Z]{3}$")
            self.assertIn(r["indicator_id"], build.INDICATORS)
            self.assertIn(r["evidence_class"], build.EVIDENCE)
            float(r["value"])
            self.assertRegex(r["year"], r"^\d{4}$")
            if r["indicator_id"] == "floor_area_res_m2_per_cap_image_region":
                self.assertEqual(r["evidence_class"], "MODELLED_REGIONAL")
            elif r["indicator_id"] == "floor_area_m2_per_cap_eu_derived":
                self.assertEqual(r["evidence_class"], "DERIVED_FROM_OFFICIAL")
            else:
                self.assertEqual(r["evidence_class"], "VERIFIED_OFFICIAL")

    def test_no_regional_aggregates(self):
        aggregates = {"AFE", "AFW", "ARB", "EUU", "HIC", "LMC", "OED", "SSF", "EAS", "ECS", "EUR", "EU2"}
        self.assertFalse(aggregates & {r["iso3"] for r in self.rows})

    def test_plausible_bounds(self):
        for r in self.rows:
            b = build.PLAUSIBLE.get(r["indicator_id"])
            if b and r["iso3"] != "WLD":
                v = float(r["value"])
                self.assertTrue(b[0] <= v <= b[1], f"{r['iso3']} {r['indicator_id']} {v}")

    def test_world_rows_present(self):
        for ind in ["pop_total", "armed_forces_personnel", "armed_forces_pct_labour_force",
                    "old_age_dependency_ratio", "old_age_dependency_ratio_2050", "pop_total_2050_wb",
                    "pop_total_2050_wpp2024_medium", "floor_area_res_m2_per_cap_image_region"]:
            self.assertIn("WLD", self.by[ind], ind)
        for ind in ["grad_medical_number", "grad_nursing_number"]:
            self.assertNotIn("WLD", self.by[ind])  # never fabricated

    def test_projection_sums(self):
        for ind, scale in [("pop_total_2050_wpp2024_medium", 1), ("pop_total_2050_wb", 1)]:
            d = self.by[ind]
            tot = sum(float(r["value"]) for k, r in d.items() if k != "WLD")
            self.assertLess(abs(tot - float(d["WLD"]["value"])) / float(d["WLD"]["value"]), 0.02, ind)
        self.assertTrue(9.0e6 < float(self.by["pop_total_2050_wpp2024_medium"]["WLD"]["value"]) < 1.05e7)

    def test_armed_forces_sum_close_to_world(self):
        d = self.by["armed_forces_personnel"]
        tot = sum(float(r["value"]) for k, r in d.items() if k != "WLD")
        self.assertLess(abs(tot - float(d["WLD"]["value"])) / float(d["WLD"]["value"]), 0.05)

    def test_stock_at_grad_year_matches_grad_year(self):
        for s, g in [("doctors_stock_number_at_grad_year", "grad_medical_number"),
                     ("nurses_midwives_stock_number_at_grad_year", "grad_nursing_number")]:
            for k, r in self.by[s].items():
                self.assertEqual(r["year"], self.by[g][k]["year"])

    def test_eu_derived_is_ratio(self):
        for k, r in self.by["floor_area_m2_per_cap_eu_derived"].items():
            q = float(self.by["dwelling_avg_size_m2"][k]["value"]) / float(
                self.by["household_avg_size_persons"][k]["value"])
            self.assertAlmostEqual(float(r["value"]), q, places=4)

    def test_image_region_numbering_matches_population(self):
        """BUMA region n population (2020, million, SSP2) vs WB 2024 population of countries mapped to region
        name. A wrong numbering would give errors of several hundred %; 25% tolerates SSP2-vs-actual drift
        (largest: Central Asia, SSP2 under-projected growth)."""
        regvals = build.image_region_values()
        reg_of = {}
        for r in self.by["floor_area_res_m2_per_cap_image_region"].values():
            if r["iso3"] != "WLD":
                reg_of[r["iso3"]] = r["source"].split("'")[1]
        wbpop = defaultdict(float)
        for k, r in self.by["pop_total"].items():
            if k in reg_of:
                wbpop[reg_of[k]] += float(r["value"]) / 1e6
        for name, v in regvals.items():
            self.assertLess(abs(wbpop[name] - v["pop_million"]) / v["pop_million"], 0.25, name)

    def test_floor_area_regional_values_consistent(self):
        regvals = build.image_region_values()
        for r in self.by["floor_area_res_m2_per_cap_image_region"].values():
            if r["iso3"] != "WLD":
                name = r["source"].split("'")[1]
                self.assertAlmostEqual(float(r["value"]), regvals[name]["total"], places=4)

    def test_rebuild_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "w.csv"
            build.build(out_csv=out, out_md=None)
            self.assertEqual(out.read_bytes(), CSV.read_bytes())


if __name__ == "__main__":
    unittest.main()
