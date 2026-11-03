"""UNIRA V7.9 — a time account: may money above the cap buy paid free time? (author's question)

Chosen design: cap floor 1.5 years of base salary, thermostat limited to +/-10% a year, protected home (150,000 U)
and retirement (120,000 U) accounts. Money above the cap then fills a TIME account (salaried people under 65),
up to 13 weeks of the person's own pay (a sabbatical); each year a person may take at most W weeks of banked
paid leave. W = 0, 1, 2, 4. Measured: share of working time lost, its equivalent in weekly hours, money going to
the One Earth Fund, free money, and the share of adults at the cap (mean of the last 10 of 60 years, 3 seeds).
python3 time_account.py  ->  ../outputs/time_account.json"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
spec = importlib.util.spec_from_file_location("cap_level", HERE / "cap_level.py")
cl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cl)
SEEDS = (1, 2, 3)


def main():
    cfg = json.loads((U / "v64" / "config" / "circuit_config.json").read_text())
    res = {"design": {"cap_floor_years": 1.5, "home_account_max_u": cl.HOME_MAX, "retirement_account_max_u": cl.RET_MAX,
                      "time_account_max_weeks": 13}, "results": {}}
    for weeks in (0, 1, 2, 4):
        runs = []
        for seed in SEEDS:
            c = cl.rl.sim_config(cfg, 0.0, True, "cap_low_credit")
            c.update({"cap_floor_years": 1.5, "cap_max_change": 0.10, "home_account_max": cl.HOME_MAX,
                      "retirement_account_max": cl.RET_MAX, "time_account_weeks_per_year": weeks, "time_account_max_weeks": 13})
            rows = cl.rl.lifecycle.simulate(c, seed)
            tail = rows[-10:]
            runs.append({"time_off_share_of_work": sum(r["time_off_share_of_work"] for r in tail) / len(tail),
                         "one_earth_inflow_share_of_consumption": sum(r["to_one_earth_cap"] + r["to_one_earth_inheritance"] for r in tail)
                         / sum(r["consumption"] for r in tail),
                         "free_money_months": tail[-1]["deposits_months_of_consumption"],
                         "share_at_cap": sum(r["share_at_cap"] for r in tail) / len(tail)})
        avg = {k: sum(r[k] for r in runs) / len(runs) for k in runs[0]}
        avg["equivalent_weekly_hours"] = 30 * (1 - avg["time_off_share_of_work"])
        res["results"][f"{weeks}_weeks"] = avg
        print(f"{weeks} weeks/yr: time off {100 * avg['time_off_share_of_work']:.2f}% of work (= {avg['equivalent_weekly_hours']:.2f} h/week) | "
              f"to One Earth {100 * avg['one_earth_inflow_share_of_consumption']:.1f}% | free money {avg['free_money_months']:.1f} m | "
              f"at cap {100 * avg['share_at_cap']:.0f}%")
    (HERE.parent / "outputs" / "time_account.json").write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
