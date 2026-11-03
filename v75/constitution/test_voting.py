import unittest

import voting


class TestVoting(unittest.TestCase):
    def setUp(self):
        self.pop = voting.populations()

    def test_no_region_majority_and_cap(self):
        s = voting.seats(self.pop, cap_share=0.05)
        S = sum(s.values())
        self.assertLessEqual(max(s.values()) / S, 0.05 + 1e-9)
        self.assertGreaterEqual(min(s.values()), 1.0)

    def test_passing_needs_many_regions(self):
        n_pass, _ = voting.min_coalition_to_pass(self.pop, 0.55, 0.65)
        self.assertGreaterEqual(n_pass, 100)

    def test_raw_population_lets_two_regions_block(self):
        n_block, _, _ = voting.min_blocking(self.pop, 0.55, 0.65)
        self.assertLessEqual(n_block, 2)   # the reason Article 25 uses square-root weights

    def test_sqrt_weights_need_many_regions_to_block(self):
        w = voting.seats(self.pop, cap_share=0.05, rule="sqrt")
        n_block, _, _ = voting.min_blocking(w, 0.55, 0.65)
        self.assertGreaterEqual(n_block, 20)


if __name__ == "__main__":
    unittest.main()
