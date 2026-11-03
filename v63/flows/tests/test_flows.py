"""Offline tests: Markov known answers, snapshot hashes, sanity bounds, reproducibility."""
import csv
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from takeup import api, compute, markov  # noqa: E402

RAW, OUT = ROOT / "data" / "raw", ROOT / "outputs"


class TestMarkov(unittest.TestCase):
    def test_absorbing_known_answer(self):
        # U leaves to E with p=0.5 per quarter, E and I absorbing: 1 - 0.5**4 = 0.9375
        p = [[0.5, 0.5, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        self.assertAlmostEqual(markov.prob(markov.compound([p] * 4), "U", "E"), 0.9375)

    def test_two_step_hand_computed(self):
        # rows U,E,I. P^2[U][E] = .2*.7 + .7*.9 + .1*.1 = 0.78
        p = [[0.2, 0.7, 0.1], [0.05, 0.9, 0.05], [0.1, 0.1, 0.8]]
        self.assertAlmostEqual(markov.prob(markov.compound([p, p]), "U", "E"), 0.78)

    def test_order_matters_and_rows_stay_stochastic(self):
        a = [[0.6, 0.3, 0.1], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        b = [[1.0, 0.0, 0.0], [0.5, 0.5, 0.0], [0.0, 0.0, 1.0]]
        ab, ba = markov.compound([a, b]), markov.compound([b, a])
        self.assertNotAlmostEqual(ab[0][1], ba[0][1])
        for row in ab + ba:
            self.assertAlmostEqual(sum(row), 1.0)

    def test_from_levels(self):
        lv = {(s, t): 1.0 for s in "UEI" for t in "UEI"}
        self.assertAlmostEqual(markov.from_levels(lv)[0][1], 1 / 3)
        del lv[("U", "E")]
        self.assertIsNone(markov.from_levels(lv))


class TestSnapshotsAndOutputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fl, cls.rows = compute.compute(RAW)

    def test_hashes_match_manifest(self):
        self.assertEqual(compute.verify_snapshots(RAW), [])

    def test_manifest_columns(self):
        with (RAW / "raw_manifest.csv").open() as f:
            self.assertEqual(csv.DictReader(f).fieldnames,
                             ["file", "dataset", "url", "retrieved_at_utc", "sha256", "bytes", "license"])

    def test_rates_in_unit_interval(self):
        for r in self.rows:
            if r["takeup_rate"] is not None:
                self.assertGreaterEqual(r["takeup_rate"], 0.0, r)
                self.assertLessEqual(r["takeup_rate"], 1.0, r)
            else:
                self.assertEqual(r["evidence_class"], "MISSING")

    def test_known_published_cells(self):
        # Read off the API on 2026-11-03: lfsi_long_a FR 2023 UNE_EMP PC_UNE = 41.0,
        # EU27 = 36.2, FR INAC_EMP PC_INAC = 8.2; ilc_lvhl30 FR 2023 EMP_PT->EMP_FT = 23.1
        self.assertAlmostEqual(self.fl.direct_annual("FR", 2023, "UNE_EMP", "PC_UNE"), 0.41)
        self.assertAlmostEqual(self.fl.direct_annual("EU27_2020", 2023, "UNE_EMP", "PC_UNE"), 0.362)
        self.assertAlmostEqual(self.fl.direct_annual("FR", 2023, "INAC_EMP", "PC_INAC"), 0.082)
        self.assertEqual(self.fl.silc[("FR", 2023, "EMP_PT", "EMP_FT")], 23.1)

    def test_fr_eu_proposed_present(self):
        for geo in ("FR", "EU27_2020"):
            for pool in ("T1", "T2", "T3"):
                self.assertIsNotNone(api.get_takeup(geo, 2023, pool, rows=self.rows), (geo, pool))

    def test_markov_overstates_direct_for_most_countries(self):
        # duration dependence => Markov > direct year-on-year for (nearly) all countries
        s = compute.summary(self.fl, self.rows)["years"]["2023"]["markov_minus_direct_T1"]
        self.assertGreater(s["mean"], 0)
        self.assertGreaterEqual(s["n_positive"], 0.8 * s["n"])

    def test_t2_lower_bound_below_proposed(self):
        for geo in ("FR", "EU27_2020"):
            self.assertLess(api.get_takeup(geo, 2023, "T2", "lower_bound", rows=self.rows),
                            api.get_takeup(geo, 2023, "T2", rows=self.rows))

    def test_outputs_reproducible(self):
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=compute.COLUMNS, lineterminator="\n")
        w.writeheader()
        for r in self.rows:
            w.writerow({k: ("" if r[k] is None else r[k]) for k in compute.COLUMNS})
        self.assertEqual(buf.getvalue(), (OUT / "takeup_rates.csv").read_text())


if __name__ == "__main__":
    unittest.main()
