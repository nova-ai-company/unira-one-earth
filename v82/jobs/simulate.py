"""UNIRA V8.2 (point 2) — who does the hard and unwanted jobs, without wage competition?

Each person chooses the job that is best for them, weighing pay (salary multiplier), hours, how hard the job is
(night and weekend work, physical strain, unpleasantness) and their own vocation (a random taste for each sector).
Sector sizes = France's 2022 hours worked by sector (v63/io). Everyone able to work works (Article 7), so every job is filled; the measure is how many people end up UNWILLINGLY in a
job outside their top three choices (low motivation, turnover, poorer care). Rules compared:
    knowledge_only   multipliers by knowledge and complexity only (Article 14 as first written)
    hardship_pay     + up to 0.5 multiplier step for hard jobs, within 5x
    shorter_hours    hard jobs count 25 paid hours as 30 (up to 5 hours less a week at the same pay)
    both             hardship pay + shorter hours
    both_better_conditions  + the jobs themselves are made 30% less hard (staffing, ergonomics, machines)
Hardness and base multipliers per sector are SYNTHETIC_ASSUMPTION (documented below). How much people dislike
hard work is unknown, so three levels are tested. A plausibility check compares the sectors with the most unwilling
workers under the baseline with France's measured 2025 vacancy rates (Eurostat jvs_a_rate_r2).
python3 simulate.py  ->  outputs/results.json"""
import csv
import json
import math
import random
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
# sector: (hardness 0-1, base multiplier by knowledge/complexity) -- SYNTHETIC_ASSUMPTION
SECTORS = {"I": (0.85, 1.2, "hotels and restaurants"), "F": (0.8, 1.4, "construction"),
           "N": (0.7, 1.2, "cleaning, security, support"), "Q": (0.7, 1.7, "health and social care"),
           "S": (0.5, 1.3, "personal services"), "H": (0.6, 1.4, "transport and storage"),
           "A": (0.75, 1.2, "agriculture"), "C": (0.5, 1.6, "manufacturing"), "G": (0.45, 1.3, "trade"),
           "P": (0.35, 1.9, "education"), "R": (0.4, 1.4, "arts and leisure"), "O": (0.2, 1.8, "public administration"),
           "M": (0.1, 2.3, "professional and scientific"), "J": (0.1, 2.3, "information and communication"),
           "K": (0.1, 2.4, "finance")}
RULES = ("knowledge_only", "hardship_pay", "shorter_hours", "both", "both_better_conditions")
CONDITIONS_CUT = 0.3  # SYNTHETIC: better staffing, ergonomics, no split shifts, machines for heavy tasks cut hardness by 30%
DISLIKE = {"low": 0.6, "central": 1.2, "high": 2.0}  # SYNTHETIC: utility cost of a fully hard job, in multiplier steps


def sector_shares():
    hours = {}
    for r in csv.DictReader((U / "v63" / "io" / "outputs" / "hours_by_product.csv").open()):
        if r["year"] != max(x["year"] for x in [r]):
            pass
        k = r["product"].replace("CPA_", "")[0]
        if k in SECTORS:
            hours[k] = hours.get(k, 0.0) + float(r["direct_hours_ths"])
    tot = sum(hours.values())
    return {k: v / tot for k, v in hours.items()}


def vacancy_rates():
    sys_path = str(U / "v62" / "src")
    import sys
    if sys_path not in sys.path:
        sys.path.insert(0, sys_path)
    from unira_v62 import jsonstat
    d = jsonstat.load(HERE / "data" / "raw" / "jvs_a_rate_r2.json")
    rows = [(c, v) for c, v, _ in jsonstat.iter_cells(d) if v is not None and c["geo"] == "FR"]
    y = max(c["time"] for c, _ in rows)
    return {c["nace_r2"]: v for c, v in rows if c["time"] == y and c["nace_r2"] in SECTORS}, y


def run(rule, dislike, seed, n=20000):
    rng = random.Random(seed)
    shares = sector_shares()
    keys = sorted(shares)
    cap = {k: int(round(shares[k] * n * 0.97)) for k in keys}  # 3% fewer jobs than people: some choice
    pay, hours = {}, {}
    for k in keys:
        hard, base = SECTORS[k][0], SECTORS[k][1]
        pay[k] = min(5.0, base + (0.5 * hard if rule in ("hardship_pay", "both", "both_better_conditions") else 0.0))
        hours[k] = 30 - (5 * hard if rule in ("shorter_hours", "both", "both_better_conditions") else 0.0)
    prefs = []
    for i in range(n):
        dis = dislike * rng.lognormvariate(-0.125, 0.5)  # people differ in how much they mind hard work
        u = {}
        for k in keys:
            felt = SECTORS[k][0] * (1 - CONDITIONS_CUT if rule == "both_better_conditions" else 1.0)
            vocation = rng.gauss(0, 0.6)
            free_time = 0.06 * (30 - hours[k])          # one hour less a week ~ 0.06 multiplier steps (SYNTHETIC)
            u[k] = math.log(pay[k]) * 2 + free_time - dis * felt + vocation
        prefs.append(sorted(keys, key=lambda k: -u[k]))
    order = list(range(n))
    rng.shuffle(order)  # people are placed in random order (equal access; no bidding)
    filled = {k: 0 for k in keys}
    unwilling = {k: 0 for k in keys}  # placed in a job outside their top three choices
    for i in order:
        for rank, k in enumerate(prefs[i]):
            if filled[k] < cap[k]:
                filled[k] += 1
                unwilling[k] += rank >= 3
                break
    vac = {k: 1 - filled[k] / cap[k] for k in keys}
    hard = [k for k in keys if SECTORS[k][0] >= 0.7]
    hours_supplied = sum(filled[k] * hours[k] for k in keys)
    hours_needed = sum(cap[k] * 30 for k in keys)
    return {"vacancy_by_sector": vac,
            "unwilling_by_sector": {k: unwilling[k] / max(filled[k], 1) for k in keys},
            "unwilling_hard_jobs": sum(unwilling[k] for k in hard) / sum(filled[k] for k in hard),
            "unwilling_other_jobs": sum(unwilling[k] for k in keys if k not in hard) / sum(filled[k] for k in keys if k not in hard),
            "vacancy_hard_jobs": sum(cap[k] - filled[k] for k in hard) / sum(cap[k] for k in hard),
            "vacancy_other_jobs": sum(cap[k] - filled[k] for k in keys if k not in hard) / sum(cap[k] for k in keys if k not in hard),
            "mean_multiplier": sum(filled[k] * pay[k] for k in keys) / sum(filled.values()),
            "hours_needed_covered": hours_supplied / hours_needed}


def spearman(a, b):
    ks = sorted(a)
    ra = {k: r for r, k in enumerate(sorted(ks, key=lambda k: a[k]))}
    rb = {k: r for r, k in enumerate(sorted(ks, key=lambda k: b[k]))}
    n = len(ks)
    return 1 - 6 * sum((ra[k] - rb[k]) ** 2 for k in ks) / (n * (n * n - 1))


def main():
    vr, year = vacancy_rates()
    out = {"sectors": {k: {"hardness": v[0], "base_multiplier": v[1], "name": v[2]} for k, v in SECTORS.items()},
           "france_vacancy_rate_pct": vr, "vacancy_year": year, "results": {}}
    for lvl, d in DISLIKE.items():
        for rule in RULES:
            runs = [run(rule, d, s) for s in (1, 2, 3)]
            avg = {k: statistics.fmean(r[k] for r in runs) for k in ("unwilling_hard_jobs", "unwilling_other_jobs", "mean_multiplier", "hours_needed_covered")}
            byk = {k: statistics.fmean(r["unwilling_by_sector"][k] for r in runs) for k in runs[0]["unwilling_by_sector"]}
            if rule == "knowledge_only":
                common = [k for k in byk if k in vr]
                avg["rank_correlation_with_france_vacancies"] = spearman({k: byk[k] for k in common}, {k: vr[k] for k in common})
            avg["unwilling_by_sector"] = byk
            out["results"][f"{lvl}/{rule}"] = avg
            print(f"dislike {lvl:7s} {rule:15s} unwilling in hard jobs {100 * avg['unwilling_hard_jobs']:5.1f}% | other {100 * avg['unwilling_other_jobs']:4.1f}% "
                  f"| mean multiplier {avg['mean_multiplier']:.2f} | hours covered {100 * avg['hours_needed_covered']:.1f}%"
                  + (f" | rank corr. with France {avg['rank_correlation_with_france_vacancies']:.2f}" if 'rank_correlation_with_france_vacancies' in avg else ""))
    (HERE / "outputs").mkdir(exist_ok=True)
    (HERE / "outputs" / "results.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
