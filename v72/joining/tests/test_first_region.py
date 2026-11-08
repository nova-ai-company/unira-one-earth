import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import first_region as fr  # noqa: E402


class TestFirstRegion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = fr.main(write=False)

    def test_reproducible(self):
        again = fr.main(write=False)
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.out, sort_keys=True))

    def test_candidates_pass_every_screen(self):
        self.assertGreaterEqual(len(self.out["candidates"]), 1)
        med = self.out["median_import_share_of_gainers_pct_gdp"]
        for r in self.out["candidates"]:
            self.assertTrue(all(r["passes"].values()), r["region"])
            self.assertTrue(r["material_gainer"] and not r["in_conflict"])
            self.assertGreaterEqual(r["wgi_mean"], 0)
            self.assertLessEqual(r["imports_pct_gdp"], med)
            self.assertGreaterEqual(r["pop_m"], 5)
            self.assertGreaterEqual(r["share_better_off_at_base"], 0.9)

    def test_losers_and_conflict_regions_never_pass(self):
        losers = set(json.loads((ROOT.parents[1] / "v72" / "outputs" / "joining.json").read_text())["losers_all"])
        names = {r["region"] for r in self.out["candidates"]}
        self.assertFalse(names & losers)
        self.assertFalse(names & {"USA", "LUX", "ISL", "FRA"})

    def test_counts_are_consistent(self):
        c = self.out["counts"]
        self.assertEqual(c["gainers"], 146)
        self.assertLess(c["passing_all_screens"], c["gainers"])
        self.assertGreater(c["gainers_in_conflict"], 0)
        self.assertLess(self.out["passing_population_share_of_world"], 0.5)

    def test_one_screen_short_list_is_sorted_by_missing_one(self):
        for r in self.out["one_screen_short"]:
            self.assertEqual(len(r["missing"]), 1, r)


if __name__ == "__main__":
    unittest.main()
