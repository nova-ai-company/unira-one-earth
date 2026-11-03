"""UNIRA V6.4b — lifecycle simulation of people under the money cap (rules 11-18).

A sample of adults (ages from Eurostat 2024) lives through T years:
  * works 20-64 (employment rate from config) at 5,000 U x multiplier; 3% unable
    to work receive the 5,000 U guarantee; retirees (65+) receive needs-based income
  * each person saves a personal share of income, 0-50% (rule 17)
  * renters pay rent and queue for a home; a home is bought when savings plus
    zero-interest credit (repaid from salary, capped share of salary) cover the
    price; homes available each year = freed homes (deaths) + new construction
    capacity; first homes before second homes; max 2 homes per person (rule 11)
  * death follows a Gompertz hazard (SYNTHETIC until replaced by a life table);
    the estate goes to a random younger heir; inheritance above the cap and
    homes beyond the heir's 2-home limit go to One Earth / the regional pool
  * money cap (rule 18): every year cap = coefficient x annual base salary;
    deposits above the cap go to One Earth. The coefficient is adjusted each
    year so that total deposits stay at a target number of months of consumption
    (what reserves and capacity can back), but never below the price of the
    most expensive home, so home ownership stays reachable.
  * fixed price: household consumption at year 0 defines the goods supply at
    30 h/week; productivity growth g raises supply, and weekly hours fall so
    that output never exceeds demand (no overproduction, rule 13).

Everything is per sampled person in U; aggregate ratios are scale-free.
"""
import math
import random


class Person:
    __slots__ = ("age", "mult", "save", "dep", "homes", "credit", "repay", "unable", "wait", "home_acc", "ret_acc")

    def __init__(self, age, mult, save, unable):
        self.age, self.mult, self.save, self.unable = age, mult, save, unable
        self.dep, self.homes, self.credit, self.repay, self.wait = 0.0, 0, 0.0, 0.0, 0
        self.home_acc = self.ret_acc = 0.0  # protected accounts outside the cap (V7.9)


def gompertz_death_prob(age, a, b):
    return 1 - math.exp(-a * math.exp(b * age))


def draw_ages(rng, age_weights, n):
    ages, w = zip(*age_weights)
    return rng.choices(ages, weights=w, k=n)


def monthly_income(p, cfg):
    base = cfg["base_salary"]
    if p.age >= 65:
        rent = 0 if p.homes else cfg["rent_month"]
        return cfg["retiree_basket_month"] + rent
    if p.unable:
        return cfg["disability_month"]
    return base * p.mult if p.mult else 0.0


def simulate(cfg, seed=1, return_people=False):
    rng = random.Random(seed)
    n = cfg["sample_size"]
    people = []
    for a in draw_ages(rng, cfg["age_weights"], n):
        unable = rng.random() < cfg["unable_share"]
        employed = (not unable) and rng.random() < cfg["employment_rate"]
        mult = rng.choices(cfg["mult_values"], weights=cfg["mult_weights"])[0] if employed else 0.0
        save = rng.uniform(*cfg["saving_range"])
        p = Person(a, mult, save, unable)
        if rng.random() < cfg["initial_owner_share"] * min(1.0, max(0.0, (a - 20) / 30)):
            p.homes = 1
        people.append(p)
    coef, base_year_cons = cfg["cap_coef_initial"], None
    pool_homes, out = 0.0, []
    supply_index, hours = 1.0, cfg["weekly_hours"]
    shocks = {sh["year"]: sh for sh in cfg.get("shocks", [])}
    fear = (0, 0.0)  # (until year, extra saving share)
    for t in range(cfg["years"] + 1):
        cons = to_one_earth = inherit_to_one = 0.0
        sh = shocks.get(t)
        if sh and sh["type"] == "disaster":  # households spend part of their savings on rebuilding
            for p in people:
                p.dep *= 1 - sh["size"]
        if sh and sh["type"] == "fear":  # precautionary saving for some years
            fear = (t + sh.get("years", 3), sh["size"])
        if sh and sh["type"] == "baby_boom":  # an extra cohort of young adults
            for _ in range(int(sh["size"] * n)):
                unable = rng.random() < cfg["unable_share"]
                employed = (not unable) and rng.random() < cfg["employment_rate"]
                mult = rng.choices(cfg["mult_values"], weights=cfg["mult_weights"])[0] if employed else 0.0
                people.append(Person(20, mult, rng.uniform(*cfg["saving_range"]), unable))
        extra_save = fear[1] if t < fear[0] else 0.0
        # --- income, consumption, saving, credit repayment
        for p in people:
            y = monthly_income(p, cfg) * 12
            if p.age >= 65:
                c = y  # retirees spend their needs-based income (rule 15)
                if p.ret_acc > 0:  # plus an even draw-down of the protected retirement account to age 85
                    w = p.ret_acc / max(1, 85 - p.age)
                    p.ret_acc -= w
                    c += w
                s = 0.0
            else:
                rent = 0.0 if p.homes else cfg["rent_month"] * 12
                s = min(0.5, p.save + extra_save) * y  # never above the 50% maximum (rule 17)
                c = y - s  # rent is part of consumption
            if p.credit > 0:
                pay = min(p.credit, p.repay, max(0.0, s))
                p.credit -= pay
                s -= pay
            p.dep += s
            cons += c
        if base_year_cons is None:
            base_year_cons = cons
        # --- automation: supply grows; hours fall so output = demand (no overproduction)
        supply = base_year_cons * supply_index
        excess = cons / supply - 1
        if excess < 0:
            hours = cfg["weekly_hours"] * max(cons / supply, 0.0)
        else:
            hours = cfg["weekly_hours"]
        # --- housing market: freed + new homes, first homes before second homes
        avail = pool_homes + cfg["new_homes_per_person_year"] * n
        queue1 = sorted((p for p in people if p.homes == 0 and p.age >= 20), key=lambda p: -p.wait)
        queue2 = [p for p in people if p.homes == 1 and 20 <= p.age < 65 and p.dep > cfg["home_price"]]
        if cfg.get("second_home_only_if_no_queue") and any(p.homes == 0 for p in queue1):
            queue2 = []
        bought = blocked_by_cap = 0
        cap_now = coef * cfg["base_salary"] * 12
        for p in queue1 + queue2:
            if avail < 1:
                break
            price = cfg["home_price"]
            credit_cap = 0.0 if p.age >= 65 else min(price, p.repay_cap if hasattr(p, "repay_cap") else
                                                    monthly_income(p, cfg) * 12 * cfg["credit_repay_share"]
                                                    * cfg["credit_max_years"])
            need_cash = max(0.0, price - credit_cap)
            if need_cash > cap_now and p.homes == 0 and p.mult and p.age < 65:  # salaried first-home buyers only
                blocked_by_cap += 1  # the cap itself would stop this first home (should never happen)
            if p.dep + p.home_acc >= need_cash:
                from_acc = min(p.home_acc, need_cash)
                p.home_acc -= from_acc
                p.dep -= need_cash - from_acc
                p.credit += price - need_cash
                p.repay = monthly_income(p, cfg) * 12 * cfg["credit_repay_share"]
                p.homes += 1
                avail -= 1
                bought += 1
        for p in queue1:
            if p.homes == 0:
                p.wait += 1
        pool_homes = max(0.0, avail)  # unsold freed homes stay in the regional pool
        # --- money cap (rule 18)
        cap = coef * cfg["base_salary"] * 12
        n_at_cap = 0
        for p in people:
            if p.dep > cap:
                over = p.dep - cap
                p.dep = cap
                n_at_cap += 1
                if p.homes == 0 and p.age < 65:
                    put = min(over, max(0.0, cfg.get("home_account_max", 0.0) - p.home_acc))
                    p.home_acc += put
                    over -= put
                if p.age < 65:
                    put = min(over, max(0.0, cfg.get("retirement_account_max", 0.0) - p.ret_acc))
                    p.ret_acc += put
                    over -= put
                to_one_earth += over
        deposits = sum(p.dep for p in people)
        target = cfg["deposit_target_months"] / 12 * cons
        step = (target / deposits) ** cfg["cap_adjust_speed"] if deposits > 0 else 1.0
        if cfg.get("cap_max_change"):  # thermostat: at most +/- this share per year
            step = min(1 + cfg["cap_max_change"], max(1 - cfg["cap_max_change"], step))
        coef = max(cfg.get("cap_floor_years", cfg["home_price"] / (cfg["base_salary"] * 12)), coef * step)
        # --- ageing, death, inheritance, newcomers at 20 keep the sample stationary
        survivors, deaths = [], 0
        for p in people:
            p.age += 1
            if rng.random() < gompertz_death_prob(p.age, cfg["gompertz_a"], cfg["gompertz_b"]):
                deaths += 1
                heirs = [q for q in people if q.age < p.age - 15]
                heir = rng.choice(heirs) if heirs else None
                estate = p.dep + p.home_acc + p.ret_acc
                if heir:
                    room = max(0.0, cap - heir.dep)
                    heir.dep += min(estate, room)
                    inherit_to_one += max(0.0, estate - room)
                    for _ in range(p.homes):
                        if heir.homes < 2:
                            heir.homes += 1
                        else:
                            pool_homes += 1
                else:
                    inherit_to_one += estate
                    pool_homes += p.homes
            else:
                survivors.append(p)
        for _ in range(deaths):
            unable = rng.random() < cfg["unable_share"]
            employed = (not unable) and rng.random() < cfg["employment_rate"]
            mult = rng.choices(cfg["mult_values"], weights=cfg["mult_weights"])[0] if employed else 0.0
            survivors.append(Person(20, mult, rng.uniform(*cfg["saving_range"]), unable))
        people = survivors
        adults = [p for p in people if p.age >= 20]
        out.append({
            "year": t, "consumption": cons, "deposits": deposits,
            "deposits_months_of_consumption": 12 * deposits / cons,
            "cap_u": cap, "cap_years_of_base_salary": cap / (cfg["base_salary"] * 12),
            "share_at_cap": n_at_cap / len(people), "to_one_earth_cap": to_one_earth,
            "to_one_earth_inheritance": inherit_to_one, "homes_bought": bought,
            "ownership_rate": sum(1 for p in adults if p.homes > 0) / len(adults),
            "second_home_rate": sum(1 for p in adults if p.homes > 1) / len(adults),
            "mean_wait_renters_years": (sum(p.wait for p in adults if p.homes == 0) /
                                        max(1, sum(1 for p in adults if p.homes == 0))),
            "excess_demand_share": excess, "weekly_hours": hours,
            "first_homes_blocked_by_cap": blocked_by_cap, "population": len(people),
            "protected_accounts_months_of_consumption": 12 * sum(p.home_acc + p.ret_acc for p in people) / cons})
        supply_index *= 1 + cfg["productivity_growth"]
    return (out, people) if return_people else out
