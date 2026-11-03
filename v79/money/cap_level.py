"""UNIRA V7.9 — choosing a moderate money cap, with protected home and retirement accounts (author's decision 2026-11-03).

The cap is a floor of L years of base salary (L = 1.5, 2, 3, 5); the thermostat may raise it but never below L.
Money above the cap goes first to a protected HOME account (people without a home, up to HOME_MAX), then to a
protected RETIREMENT account (up to RET_MAX, drawn down evenly from 65 to 85 as extra income), then to the
One Earth Fund. Compared with the low cap (thermostat, about 1.4 years) and with no protected accounts.
Rush test: if a quarter of free (unprotected) money is spent within one year, how large is the extra demand
for goods, as a share of a normal year's consumption? At fixed prices that extra demand becomes shortages,
unless reserves cover it. Protected accounts cannot be spent in a rush.
python3 cap_level.py  ->  ../outputs/cap_level.json"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
spec = importlib.util.spec_from_file_location("run_lifecycle", U / "v64" / "run_lifecycle.py")
rl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rl)

HOME_MAX = 150_000      # SYNTHETIC_ASSUMPTION: half the price of an average home (300,000 U)
RET_MAX = 120_000       # SYNTHETIC_ASSUMPTION: 2 years of base salary; about +20% on the retiree basket for 20 years
RUSH_SHARE = 0.25
SEEDS = (1, 2, 3)


def run(cfg, floor, accounts, seed, time_weeks=0):
    c = rl.sim_config(cfg, 0.0, True, "cap_low_credit")
    c["cap_floor_years"] = floor
    c["cap_max_change"] = 0.10
    if accounts:
        c["home_account_max"], c["retirement_account_max"] = HOME_MAX, RET_MAX
    if time_weeks:
        c["time_account_weeks_per_year"], c["time_account_max_weeks"] = time_weeks, 13
    rows, people = rl.lifecycle.simulate(c, seed, return_people=True)
    last = rows[-1]
    wealth = sorted((p.dep + p.home_acc + p.ret_acc for p in people), reverse=True)
    tail = rows[-10:]
    return {"free_money_months": last["deposits_months_of_consumption"],
            "protected_months": last["protected_accounts_months_of_consumption"],
            "share_at_cap": sum(r["share_at_cap"] for r in tail) / len(tail),
            "share_losing_money_to_fund": sum(r["share_losing_money_to_fund"] for r in tail) / len(tail),
            "one_earth_inflow_share_of_consumption": sum(r["to_one_earth_cap"] + r["to_one_earth_inheritance"] for r in tail)
            / sum(r["consumption"] for r in tail),
            "top10_share_of_money": sum(wealth[:len(wealth) // 10]) / sum(wealth),
            "rush_extra_demand_pct_of_year": 100 * RUSH_SHARE * last["deposits_months_of_consumption"] / 12,
            "cap_years": last["cap_years_of_base_salary"],
            "first_homes_blocked_by_cap": sum(r["first_homes_blocked_by_cap"] for r in rows),
            "ownership_rate": last["ownership_rate"], "mean_wait_renters_years": last["mean_wait_renters_years"]}


def main():
    cfg = json.loads((U / "v64" / "config" / "circuit_config.json").read_text())
    res = {"home_account_max_u": HOME_MAX, "retirement_account_max_u": RET_MAX, "rush_share": RUSH_SHARE, "results": {}}
    for floor in (1.0, 1.5, 2.0, 3.0, 5.0):
        for accounts, weeks, label in ((False, 0, "no_accounts"), (True, 0, "accounts"), (True, 2, "accounts_time")):
            runs = [run(cfg, floor, accounts, s, weeks) for s in SEEDS]
            avg = {k: sum(r[k] for r in runs) / len(runs) for k in runs[0]}
            key = f"cap_{floor:g}y/{label}"
            res["results"][key] = avg
            print(f"{key:24s} free {avg['free_money_months']:5.1f} m | protected {avg['protected_months']:4.1f} m | "
                  f"at cap {100 * avg['share_at_cap']:3.0f}% | losing {100 * avg['share_losing_money_to_fund']:3.0f}% | to One Earth {100 * avg['one_earth_inflow_share_of_consumption']:4.1f}% | "
                  f"top10 {100 * avg['top10_share_of_money']:3.0f}% | rush +{avg['rush_extra_demand_pct_of_year']:4.1f}% | "
                  f"cap {avg['cap_years']:.2f}y | blocked {avg['first_homes_blocked_by_cap']:.0f}")
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "cap_level.json").write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
