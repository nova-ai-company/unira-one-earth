"""How large should the open lottery for desirable homes be? (author's question, Article 18.8)
Points + lottery in bands, with 0%, 10%, 20% and 30% of each year's desirable vacancies given by open lottery
among all applicants. Baseline settings and seeds of simulate.py.
python3 open_share.py  ->  outputs/open_share.json"""
import copy
import json
import os

import simulate

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = ("high_need_housed_within_5y", "low_need_housed_within_5y", "wait_mean_housed", "wait_p90_housed",
        "share_housed_within_5y", "d10_over_d1", "commute_km_all_at_5y")


def main():
    cfg = simulate.load_config()
    seeds = simulate._v(cfg["seeds_main"])
    out = {}
    for share in (0.0, 0.1, 0.2, 0.3):
        c = copy.deepcopy(cfg)
        c["open_lottery_share"]["value"] = share
        r = simulate.scenario(c, f"open_{share}", ["points_lottery_open"], seeds)["methods"]["points_lottery_open"]
        out[f"{int(share * 100)}%"] = {k: r[k]["mean"] for k in KEYS}
        print(f"open {int(share * 100):2d}%: " + " | ".join(f"{k} {r[k]['mean']}" for k in KEYS))
    os.makedirs(os.path.join(HERE, "outputs"), exist_ok=True)
    with open(os.path.join(HERE, "outputs", "open_share.json"), "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
