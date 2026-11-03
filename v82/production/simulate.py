"""UNIRA V8.2 (point 1) — producing what people want without price signals.

Stylised economy of ordinary (non-essential) products, monthly for 20 years. Latent demand per product moves with
a trend, seasons, fashions (temporary booms) and random shocks; products die out and new ones arrive. Capacity can
move between products only slowly (lag and a maximum monthly change). Every regime has the SAME total labour hours.

    market       flexible prices clear demand; output follows price/cost; people below the price drop out
                 (poorer first); measured: who is priced out, price volatility
    plan         Soviet-style: fixed prices; annual plan = last plan x growth target (ratchet), revised once a
                 year and only halfway toward observed sales
    unira        fixed prices; monthly production follows revealed demand = sales + new entries on waiting
                 lists (orders kept up to 3 months), forecast by exponential smoothing, plus a stock target sized
                 from measured forecast error; new products start with a pilot run
    unira_sales  as unira, but without waiting lists: only sales are seen, so demand hidden by stockouts is missed
Unmet orders wait at most 3 months, then lapse. Units of a product that dies out are written off (waste).
python3 simulate.py  ->  outputs/results.json"""
import json
import math
import random
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGIMES = ("market", "plan", "unira", "unira_sales")


def load_config():
    cfg = json.loads((HERE / "config.json").read_text())
    return {k: (v["value"] if isinstance(v, dict) and "value" in v else v) for k, v in cfg.items() if not k.startswith("_")}


class Product:
    __slots__ = ("base", "trend", "season", "phase", "fad_t", "fad_size", "born", "dies", "hours")

    def __init__(self, rng, t, cfg):
        self.base = rng.lognormvariate(math.log(cfg["mean_demand"]), 0.8)
        self.trend = rng.gauss(0, cfg["trend_sd"])
        self.season = rng.uniform(0, cfg["season_amp"])
        self.phase = rng.uniform(0, 2 * math.pi)
        self.fad_t, self.fad_size = -999, 0.0
        self.born = t
        self.dies = t + int(rng.expovariate(1 / cfg["mean_life_months"])) + 12
        self.hours = rng.uniform(0.5, 3.0)

    def demand(self, t, rng, cfg):
        age = t - self.born
        ramp = min(1.0, (age + 1) / cfg["launch_months"])
        fade = max(0.0, min(1.0, (self.dies - t) / cfg["fade_months"]))
        fad = 1 + self.fad_size * math.exp(-max(0, t - self.fad_t) / 4.0) if t >= self.fad_t else 1.0
        level = self.base * math.exp(self.trend * age / 12) * (1 + self.season * math.sin(2 * math.pi * t / 12 + self.phase))
        return max(0.0, level * ramp * fade * fad * rng.lognormvariate(-cfg["noise_sd"] ** 2 / 2, cfg["noise_sd"]))


def run(cfg, regime, seed):
    rng_d = random.Random(seed)          # demand world: identical across regimes
    rng_x = random.Random(seed + 10_000)  # regime-specific randomness (none used, kept for clarity)
    T, n = cfg["months"], cfg["products"]
    prods = [Product(rng_d, 0, cfg) for _ in range(n)]
    hours_total = sum(p.base * p.hours for p in prods) * cfg["hours_slack"]
    cap = [p.base for p in prods]                 # units/month currently producible
    target = list(cap)
    stock = [p.base * 1.0 for p in prods]
    backlog = [[] for _ in prods]                 # list of (month ordered, units)
    fc = [p.base for p in prods]                  # forecast of revealed demand
    err = [0.25 * p.base for p in prods]           # running abs forecast error
    price = [1.0] * n                             # relative to the fixed price
    plan = list(cap)
    m = {"desired": 0.0, "served_1m": 0.0, "served_3m": 0.0, "lost": 0.0, "produced": 0.0, "waste": 0.0,
         "stock_months": [], "priced_out": 0.0, "wait_units": 0.0, "priced_out_poor_half": 0.0, "price_changes": [], "hours_used": 0.0}
    shocks = []
    for t in range(T):
        # --- world changes: fads, deaths and births (same in every regime)
        if rng_d.random() < cfg["fad_rate"] * n:
            k = rng_d.randrange(n)
            prods[k].fad_t, prods[k].fad_size = t, rng_d.uniform(1.0, 3.0)
            shocks.append((t, k))
        for k, p in enumerate(prods):
            if t >= p.dies:
                m["waste"] += stock[k]
                for _, u in backlog[k]:
                    m["lost"] += u
                prods[k] = Product(rng_d, t, cfg)
                stock[k] = 0.0
                backlog[k] = []
                pilot = prods[k].base * cfg["pilot_share"]
                cap[k] = target[k] = plan[k] = pilot
                fc[k], err[k], price[k] = pilot, 0.5 * pilot, 1.0
        # --- production this month (capacity limited by total labour hours)
        need_h = sum(cap[k] * prods[k].hours for k in range(n))
        scale = min(1.0, hours_total / need_h) if need_h else 1.0
        out = [cap[k] * scale for k in range(n)]
        m["produced"] += sum(out)
        m["hours_used"] += sum(out[k] * prods[k].hours for k in range(n))
        for k in range(n):
            stock[k] += out[k]
        # --- demand and sales
        sales_seen, revealed = [0.0] * n, [0.0] * n
        for k, p in enumerate(prods):
            d0 = p.demand(t, rng_d, cfg)
            m["desired"] += d0
            if regime == "market":
                d = d0 * price[k] ** (-cfg["elasticity"])
                out_of_market = max(0.0, d0 - d)  # people a high price pushes out (poorer first)
                m["priced_out"] += out_of_market
                m["priced_out_poor_half"] += min(out_of_market, 0.5 * d0)
                sold = min(d, stock[k])
                stock[k] -= sold
                m["served_1m"] += min(sold, d0)    # extra buying in a glut does not count as served desire
                m["served_3m"] += min(sold, d0)
                m["lost"] += max(0.0, min(d, d0) - sold)
                # price moves toward clearing
                gap = (d - sold) / max(sold, 1e-9) if sold < d else -(stock[k] / max(d, 1e-9)) * 0.1
                new = min(cfg["price_cap"], max(0.3, price[k] * (1 + cfg["price_speed"] * max(-0.5, min(1.0, gap)))))
                m["price_changes"].append(abs(new / price[k] - 1))
                price[k] = new
                sales_seen[k] = sold
                continue
            # fixed-price regimes: old orders first, then new demand
            served_old = 0.0
            keep = []
            for (t0, u) in backlog[k]:
                take = min(u, stock[k])
                stock[k] -= take
                served_old += take
                if take > 0 and t - t0 <= 3:
                    m["served_3m"] += take
                    m["wait_units"] += take * (t - t0)
                if u - take > 0:
                    if t - t0 >= 3:
                        m["lost"] += u - take
                    else:
                        keep.append((t0, u - take))
            backlog[k] = keep
            sold = min(d0, stock[k])
            stock[k] -= sold
            m["served_1m"] += sold
            m["served_3m"] += sold
            unmet = d0 - sold
            if regime == "unira" or regime == "plan":
                backlog[k].append((t, unmet)) if unmet > 0 else None
                revealed[k] = sold + unmet       # orders reveal demand even when out of stock
            else:  # unira_sales: unmet demand walks away unseen
                m["lost"] += unmet
                revealed[k] = sold
            sales_seen[k] = sold + served_old
        # --- planning for next month
        for k, p in enumerate(prods):
            if regime == "market":
                margin = price[k] - 1.0
                target[k] = max(0.0, cap[k] * (1 + cfg["market_response"] * margin))
            elif regime == "plan":
                if t % 12 == 11:
                    observed = sales_seen[k] * 1.0
                    plan[k] = max(0.0, plan[k] * (1 + cfg["plan_growth"]) + 0.5 * (observed - plan[k]))
                target[k] = plan[k]
            else:
                a = cfg["smoothing"]
                e = revealed[k] - fc[k]
                err[k] = 0.8 * err[k] + 0.2 * abs(e)
                fc[k] = fc[k] + a * e
                stock_target = cfg["stock_z"] * err[k]
                pending = sum(u for _, u in backlog[k])
                target[k] = max(0.0, fc[k] + (stock_target - stock[k] + pending) / cfg["stock_close_months"])
            # capacity moves toward target within limits (lag)
            lim = cfg["max_cap_change"] * max(cap[k], 0.1 * p.base)
            cap[k] = max(0.0, cap[k] + max(-lim, min(lim, target[k] - cap[k])))
        tot_d = sum(p.base for p in prods)
        m["stock_months"].append(sum(stock) / max(tot_d, 1e-9))
    # end: remaining stock counts as unsold
    m["waste_end_stock"] = sum(stock)
    D = m["desired"]
    res = {"served_within_1_month": m["served_1m"] / D, "served_within_3_months": m["served_3m"] / D,
           "lost_or_lapsed": m["lost"] / D, "waste_share_of_production": (m["waste"]) / max(m["produced"], 1e-9),
           "mean_stock_months": statistics.fmean(m["stock_months"][12:]), "hours_used_share": m["hours_used"] / (hours_total * T),
           "mean_wait_months_of_served": m["wait_units"] / max(m["served_3m"], 1e-9)}
    if regime == "market":
        res["priced_out_share_of_desire"] = m["priced_out"] / D
        res["priced_out_share_in_poorer_half"] = m["priced_out_poor_half"] / m["priced_out"] if m["priced_out"] > 0 else 0.0
        res["mean_monthly_price_change"] = statistics.fmean(m["price_changes"])
    return res


def summary(cfg, regime):
    runs = [run(cfg, regime, s) for s in cfg["seeds"]]
    return {k: round(statistics.fmean(x[k] for x in runs), 4) for k in runs[0]}


def main():
    cfg = load_config()
    out = {"regimes": {}, "unira_stock_target_sensitivity": {}}
    for r in REGIMES:
        out["regimes"][r] = summary(cfg, r)
        print(r, out["regimes"][r])
    for z in (1.5, 3.0, 5.0, 8.0):  # bigger stock targets: shorter waits, more waste
        c = dict(cfg, stock_z=z)
        out["unira_stock_target_sensitivity"][str(z)] = summary(c, "unira")
        print("unira stock_z", z, out["unira_stock_target_sensitivity"][str(z)])
    (HERE / "outputs").mkdir(exist_ok=True)
    (HERE / "outputs" / "results.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
