"""Tests for the V6.3 input-output hours model."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT.parents[1] / "v62" / "src"))
from unira_io import analysis, fetch, model  # noqa: E402


class Toy:
    """Two-product economy with a known Leontief inverse."""

    def __init__(self):
        self.products = ["X", "Y"]
        self.A = [[0.2, 0.3], [0.1, 0.4]]
        self.l = [2.0, 1.0]
        self.m = model.multipliers(self.A, self.l)
        self.F = {"hh": [10.0, 20.0]}
        # output x = (I-A)^-1 f
        self.x = model.solve(self.A, [10.0, 20.0])
        self.hours = [l * x for l, x in zip(self.l, self.x)]

    embodied = model.IOSystem.embodied
    hypothetical_extraction = model.IOSystem.hypothetical_extraction
    embodied_by_use_and_product = model.IOSystem.embodied_by_use_and_product


class TestLeontief(unittest.TestCase):
    def test_solve_known_answer(self):
        # (I-A) = [[0.8,-0.3],[-0.1,0.6]], det=0.45; inverse = [[0.6,0.3],[0.1,0.8]]/0.45
        x = model.solve([[0.2, 0.3], [0.1, 0.4]], [10.0, 20.0])
        self.assertAlmostEqual(x[0], (0.6 * 10 + 0.3 * 20) / 0.45)
        self.assertAlmostEqual(x[1], (0.1 * 10 + 0.8 * 20) / 0.45)

    def test_multipliers_known_answer(self):
        m = model.multipliers([[0.2, 0.3], [0.1, 0.4]], [2.0, 1.0])
        self.assertAlmostEqual(m[0], (2 * 0.6 + 1 * 0.1) / 0.45)
        self.assertAlmostEqual(m[1], (2 * 0.3 + 1 * 0.8) / 0.45)

    def test_embodied_equals_total_hours(self):
        t = Toy()
        self.assertAlmostEqual(t.embodied(t.F["hh"]), sum(t.hours))

    def test_singular_raises(self):
        with self.assertRaises(ValueError):
            model.solve([[1.0, 0.0], [0.0, 0.5]], [1.0, 1.0])


class TestCounterfactuals(unittest.TestCase):
    def test_extraction_saves_at_least_direct_hours(self):
        t = Toy()
        saved = t.hypothetical_extraction("Y")
        self.assertGreaterEqual(saved, t.hours[1] - 1e-9)
        self.assertLessEqual(saved, sum(t.hours) + 1e-9)

    def test_extract_everything_saves_everything(self):
        t = Toy()
        t.A = [[0.0, 0.0], [0.0, 0.0]]
        t.m = model.multipliers(t.A, t.l)
        t.x = t.F["hh"]
        t.hours = [l * x for l, x in zip(t.l, t.x)]
        self.assertAlmostEqual(t.hypothetical_extraction("X"), t.hours[0])

    def test_partial_reduction_zero_and_full(self):
        t = Toy()
        self.assertAlmostEqual(analysis.partial_reduction(t, {"X": 0.0}), 0.0)
        self.assertAlmostEqual(analysis.partial_reduction(t, {"Y": 1.0}), t.hypothetical_extraction("Y"))


class TestHoursAllocation(unittest.TestCase):
    def test_residual_allocated_by_persons(self):
        y = "2022"
        h = {(y, n, "THS_HW", "EMP_DC"): v for n, v in [("G", 100.0)]}
        h.update({(y, n, "THS_PER", "EMP_DC"): v for n, v in [("G45", 1.0), ("G46", 1.0), ("G47", 2.0)]})
        # only fill the G subtree; stub every other published code
        for n in {v for v in model.PRODUCTS.values() if v} - {"G45", "G46", "G47"}:
            h[(y, n, "THS_HW", "EMP_DC")] = 1.0
        for parent in model.HOURS_TREE:
            h.setdefault((y, parent, "THS_HW", "EMP_DC"), 1.0)
        out = model.resolve_hours(h, y)
        self.assertAlmostEqual(out["G47"][0], 50.0)
        self.assertAlmostEqual(out["G45"][0] + out["G46"][0] + out["G47"][0], 100.0)
        self.assertTrue(out["G47"][1].startswith("allocated_from_G"))


class TestRealData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(ROOT))
        import run
        cls.cells, cls.hours = run.load()
        cls.io = model.IOSystem(cls.cells, cls.hours, 2022)

    def test_hashes(self):
        self.assertEqual(fetch.verify_manifest(ROOT / "data" / "raw"), [])

    def test_closure_identity(self):
        self.assertAlmostEqual(sum(self.io.embodied_by_use().values()) / sum(self.io.hours), 1, places=5)

    def test_all_hours_mapped(self):
        self.assertAlmostEqual(sum(self.io.hours) / self.io.hours_total_na, 1, places=6)

    def test_imputed_rent_has_no_hours(self):
        self.assertEqual(self.io.hours[self.io.products.index("CPA_L68A")], 0.0)

    def test_inverse_accuracy(self):
        # (I-A)' m = l  =>  m - A' m = l
        A, m, l = self.io.A, self.io.m, self.io.l
        n = len(A)
        res = max(abs(m[j] - sum(A[i][j] * m[i] for i in range(n)) - l[j]) for j in range(n))
        self.assertLess(res, 1e-9)


if __name__ == "__main__":
    unittest.main()
