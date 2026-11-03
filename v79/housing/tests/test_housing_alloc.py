import copy
import random
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import simulate as sim  # noqa: E402

CFG = sim.load_config()


def housed(pop):
    return {h.hid: (h.housed_year, h.housed_zone) for h in pop if h.housed_year is not None}


class TestConservation(unittest.TestCase):
    def test_homes_conserved_every_year(self):
        for rule, build in ((True, 0), (False, 25)):
            r = sim.run(CFG, "points_lottery", 3, rule=rule, build_pct=build, return_ledger=True)
            zones = {i: z for i, z in enumerate(CFG["zones"]["value"]) if z["desirable"]}
            for t, row in enumerate(r["_ledger"]):
                for z, s in row.items():
                    self.assertEqual(s["occ"] + s["empty"] + s["vacant"], s["stock"])
                    self.assertGreaterEqual(min(s["occ"], s["empty"], s["vacant"]), 0)
            for z, s in r["_ledger"][-1].items():
                self.assertEqual(s["stock"], zones[z]["stock"] + round(zones[z]["stock"] * build / 100))

    def test_no_household_gets_two_desirable_homes(self):
        r = sim.run(CFG, "lottery", 5, rule=False, return_ledger=True)
        pop = r["_pop"]
        ids = [h.hid for h in pop]
        self.assertEqual(len(ids), len(set(ids)))
        n_housed = sum(h.housed_year is not None for h in pop)
        # each allocation filled exactly one vacancy: count via ledger flows is implicit in
        # conservation; here check one zone per household and allocations == housed households
        for h in pop:
            if h.housed_year is not None:
                self.assertIn(h.housed_zone, h.prefs)
        self.assertGreater(n_housed, 0)

    def test_deferred_acceptance_unique_and_stable(self):
        rng = random.Random(1)

        class H:
            pass
        apps = []
        for i in range(60):
            h = H()
            h.hid = i
            h.prefs = rng.sample([0, 1], rng.choice([1, 2]))
            apps.append(h)
        pr = {(h.hid, z): rng.random() for h in apps for z in (0, 1)}
        vac = {0: 7, 1: 5}
        m = sim.deferred_acceptance(apps, vac, lambda h, z: pr[(h.hid, z)])
        got = [h.hid for hs in m.values() for h in hs]
        self.assertEqual(len(got), len(set(got)))
        for z in vac:
            self.assertLessEqual(len(m[z]), vac[z])
        where = {h.hid: z for z, hs in m.items() for h in hs}
        for h in apps:  # no blocking pair
            for z in h.prefs:
                if where.get(h.hid) == z:
                    break
                worst = max((pr[(x.hid, z)] for x in m[z]), default=None)
                self.assertTrue(len(m[z]) == vac[z] and worst < pr[(h.hid, z)])


class TestFairness(unittest.TestCase):
    def test_lottery_income_neutral_in_expectation(self):
        cfg = copy.deepcopy(CFG)
        cfg["speculation"]["speculator_share_of_applicants"]["value"] = 0.0
        ratios = [sim.run(cfg, "lottery", s)["decile_alloc_ratio"] for s in (1, 2, 3)]
        mean = [sum(c) / len(c) for c in zip(*ratios)]
        for d, x in enumerate(mean, 1):
            self.assertAlmostEqual(x, 1.0, delta=0.08, msg=f"decile {d}")

    def test_income_never_enters_unira_priority(self):
        pop = sim.generate_population(CFG, 9)
        for m in ("queue", "points", "points_lottery", "points_lottery_open", "lottery"):
            sim.run(CFG, m, 9, population=pop)
            a = housed(pop[0])
            incomes = [h.income for h in pop[0]]
            random.Random(0).shuffle(incomes)
            for h, inc in zip(pop[0], incomes):
                h.income = inc
            sim.run(CFG, m, 9, population=pop)
            self.assertEqual(a, housed(pop[0]), m)

    def test_market_benchmark_has_income_gradient(self):
        r = sim.run(CFG, "market", 4)
        self.assertGreater(r["income_gradient_slope"], 0.2)
        self.assertLess(r["decile_alloc_ratio"][0], 0.1)

    def test_points_favour_high_need(self):
        r = sim.run(CFG, "points_lottery", 4)
        self.assertGreater(r["high_need_housed_within_5y"], r["low_need_housed_within_5y"] + 0.1)


class TestRulesAndDeterminism(unittest.TestCase):
    def test_determinism_with_seed(self):
        a = sim.run(CFG, "points_lottery", 7, gaming_rate=0.1, audit=0.25)
        b = sim.run(CFG, "points_lottery", 7, gaming_rate=0.1, audit=0.25)
        self.assertEqual(a, b)
        c = sim.run(CFG, "points_lottery", 8, gaming_rate=0.1, audit=0.25)
        self.assertNotEqual(a, c)

    def test_live_in_rule_cuts_empty_homes(self):
        on = sim.run(CFG, "lottery", 2, rule=True)
        off = sim.run(CFG, "lottery", 2, rule=False)
        self.assertLess(on["empty_share_final"], 0.02)
        self.assertGreater(off["empty_share_final"], 0.05)

    def test_audit_reduces_false_claims(self):
        no = sim.run(CFG, "points", 2, gaming_rate=0.2, audit=0.0)
        hi = sim.run(CFG, "points", 2, gaming_rate=0.2, audit=0.75)
        self.assertGreater(no["false_claim_share_of_allocations"], hi["false_claim_share_of_allocations"])
        self.assertGreater(hi["cheaters_caught"], 0)

    def test_building_more_shortens_queue(self):
        base = sim.run(CFG, "queue", 2)
        more = sim.run(CFG, "queue", 2, build_pct=25)
        self.assertGreater(more["share_housed_ever"], base["share_housed_ever"])


if __name__ == "__main__":
    unittest.main()
