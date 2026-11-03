"""UNIRA V7.5: test representation rules on real 2024 populations (World Bank, v65 data).
python3 voting.py
Assembly of the Peoples: S seats; each region gets seats proportional to sqrt(population)
(Penrose square-root rule: equal voting power per citizen in a two-tier union), at least 1,
at most `cap_share` of all seats. Council of Regions: one vote each; a law needs >= q_regions
of regions AND >= q_pop of world population (double majority)."""
import csv
import json
import math
from pathlib import Path

U = Path(__file__).resolve().parents[2]


def populations():
    pop = {}
    for r in csv.DictReader((U / "v65" / "data" / "world_indicators.csv").open()):
        if r["indicator_id"] == "pop_total" and r["iso3"] != "WLD":
            pop[r["iso3"]] = float(r["value"])
    return pop


def seats(pop, S=1000, cap_share=0.10, rule="sqrt"):
    w = {k: (math.sqrt(v) if rule == "sqrt" else v) for k, v in pop.items()}
    cap = cap_share * S
    alloc, free_w, left = {}, dict(w), S
    # iterative cap: regions hitting the cap get it, the rest share the remainder
    while True:
        tot = sum(free_w.values())
        over = {k for k, x in free_w.items() if left * x / tot > cap}
        if not over:
            break
        for k in over:
            alloc[k] = cap
            left -= cap
            del free_w[k]
    tot = sum(free_w.values())
    for k, x in free_w.items():
        alloc[k] = max(1.0, left * x / tot)
    return alloc


def min_coalition_to_pass(pop, q_regions, q_pop):
    """Smallest number of regions that can pass a law alone (largest-first greedy for population,
    then the count condition)."""
    n = len(pop)
    need_n = math.ceil(q_regions * n)
    tot = sum(pop.values())
    order = sorted(pop.values(), reverse=True)
    acc, k = 0.0, 0
    while acc < q_pop * tot:
        acc += order[k]
        k += 1
    return max(k, need_n), k


def min_blocking(pop, q_regions, q_pop):
    """Smallest group able to block: either > (1 - q_pop) of population or > (1 - q_regions) of regions."""
    tot = sum(pop.values())
    order = sorted(pop.values(), reverse=True)
    acc, k = 0.0, 0
    while acc <= (1 - q_pop) * tot:
        acc += order[k]
        k += 1
    by_count = math.floor((1 - q_regions) * len(pop)) + 1
    return min(k, by_count), k, by_count


def main():
    pop = populations()
    tot = sum(pop.values())
    out = {"regions": len(pop), "world_pop": tot}
    top = sorted(pop, key=pop.get, reverse=True)[:5]
    for rule, cap in (("proportional", 1.0), ("sqrt", 1.0), ("sqrt", 0.10), ("sqrt", 0.05)):
        s = seats(pop, cap_share=cap, rule=rule)
        S = sum(s.values())
        out[f"{rule}_cap{cap}"] = {k: round(100 * s[k] / S, 2) for k in top}
        largest_two = sum(sorted(s.values(), reverse=True)[:2]) / S
        out[f"{rule}_cap{cap}"]["largest_two_share"] = round(100 * largest_two, 1)
        out[f"{rule}_cap{cap}"]["smallest_region_seats"] = round(min(s.values()), 2)
    for q_r, q_p in ((0.55, 0.65), (0.55, 0.60), (0.60, 0.65)):
        n_pass, by_pop = min_coalition_to_pass(pop, q_r, q_p)
        n_block, block_pop, block_cnt = min_blocking(pop, q_r, q_p)
        out[f"double_majority_{int(q_r*100)}_{int(q_p*100)}"] = {
            "min_regions_to_pass": n_pass, "regions_needed_for_population_alone": by_pop,
            "min_regions_to_block": n_block, "blocking_by_population_needs": block_pop, "blocking_by_count_needs": block_cnt}
    # Article 25 as agreed: the population leg is counted with square-root seats (cap 5%)
    w = seats(pop, cap_share=0.05, rule="sqrt")
    n_pass, by_pop = min_coalition_to_pass(w, 0.55, 0.65)
    n_block, block_pop, block_cnt = min_blocking(w, 0.55, 0.65)
    out["double_majority_55_65_sqrt"] = {
        "min_regions_to_pass": n_pass, "regions_needed_for_population_alone": by_pop,
        "min_regions_to_block": n_block, "blocking_by_population_needs": block_pop, "blocking_by_count_needs": block_cnt}
    (U / "v75" / "outputs").mkdir(exist_ok=True)
    (U / "v75" / "outputs" / "voting.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
