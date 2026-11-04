"""UNIRA V8.6 — automation and model B (author, 2026-11-04): guaranteed income plus rewards for work.

Illustrative 100-year path for a region (population of adults normalised to 1). All parameters are SYNTHETIC.
    automation   share of today's work tasks done by machines, rising along an S-curve to AUTO_MAX (scenarios)
    human-only   a share of work that stays human (care, teaching, research, governance, repair of the machines)
    needs        real consumption per adult grows slowly (ecological limits: no endless growth), +NEED_GROWTH/yr
    hours        work hours needed per adult per week = 30 x (1 - automation) x (needs growth) / (productivity of the
                 remaining human tasks), shared among everyone able to work (rule 16: automation shortens hours)
    money        total income each year = value of what is produced for people (fixed prices: no inflation).
                 Model B: a GUARANTEED income for every adult, funded by the community share of automated production,
                 rises as automation grows; people who work receive pay for their hours on top (multipliers, Art. 14).
                 Rule: the guaranteed income takes the automated share of output; pay for work takes the human share.
    failure      a year in which 20% of automated capacity fails (cyber-attack, breakdown): how many extra human hours
                 are needed, and are there enough people still trained to do them (skills reserve)?
python3 model.py  ->  ../outputs/automation.json"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
HUMAN_ONLY = 0.10      # SYNTHETIC: share of today's tasks that stays human even with advanced machines
NEED_GROWTH = 0.005    # SYNTHETIC: real needs per adult grow 0.5%/yr (better quality, not more material use)
HUMAN_PRODUCTIVITY = 0.01  # SYNTHETIC: tools make the remaining human tasks 1%/yr more productive
SCENARIOS = {"slow": (60, 0.9), "medium": (40, 0.9), "fast": (25, 0.9)}  # (midpoint year, maximum automation)
FAILURE_SHARE = 0.20
SKILLS_RESERVE_HOURS = 2.0  # SYNTHETIC: hours a week everyone keeps practising essential skills (training, rotation)


def automation(t, mid, top):
    return min(top, (1 - HUMAN_ONLY), top / (1 + math.exp(-(t - mid) / 8)))


def run(mid, top, years=100):
    rows = []
    for t in range(years + 1):
        a = automation(t, mid, top)
        need = (1 + NEED_GROWTH) ** t
        hours = 30 * (1 - a) * need / (1 + HUMAN_PRODUCTIVITY) ** t
        hours = max(hours, 0.0)
        human_share = hours / (30 * need) if need else 0.0      # share of output value from human work
        guaranteed = 1 - human_share                            # share of total income paid as guaranteed income
        # failure year: 20% of automated output must be covered by humans for a while
        extra = 30 * a * need * FAILURE_SHARE / (1 + HUMAN_PRODUCTIVITY) ** t
        covered = min(1.0, SKILLS_RESERVE_HOURS * 3 / extra) if extra > 0 else 1.0  # trained people can triple practice hours
        rows.append({"year": t, "automation": a, "weekly_hours": hours, "guaranteed_share_of_income": guaranteed,
                     "work_pay_share_of_income": human_share, "income_vs_today": need,
                     "failure_extra_hours_needed": extra, "failure_share_covered_by_trained_people": covered})
    return rows


def main():
    out = {"assumptions": {"human_only": HUMAN_ONLY, "need_growth": NEED_GROWTH, "human_productivity": HUMAN_PRODUCTIVITY,
                           "failure_share": FAILURE_SHARE, "skills_reserve_hours": SKILLS_RESERVE_HOURS}, "scenarios": {}}
    for name, (mid, top) in SCENARIOS.items():
        rows = run(mid, top)
        out["scenarios"][name] = {f"year_{y}": {k: round(v, 3) for k, v in rows[y].items()} for y in (0, 10, 25, 50, 75, 100)}
        print(f"\n{name} automation (midpoint year {mid}):")
        for y in (0, 10, 25, 50, 75, 100):
            r = rows[y]
            print(f"  year {y:3d}: automation {100 * r['automation']:3.0f}% | week {r['weekly_hours']:4.1f} h | guaranteed income "
                  f"{100 * r['guaranteed_share_of_income']:3.0f}% of income, pay for work {100 * r['work_pay_share_of_income']:3.0f}% | "
                  f"real income x{r['income_vs_today']:.2f} | failure: {r['failure_extra_hours_needed']:4.1f} extra h/wk needed, "
                  f"{100 * r['failure_share_covered_by_trained_people']:3.0f}% coverable")
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "automation.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
