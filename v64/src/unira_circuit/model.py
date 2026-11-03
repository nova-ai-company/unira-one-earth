"""UNIRA V6.4 — the money circuit under UNIRA's own rules (France region pilot).

Money unit: U (never converted to euros). Physical unit: hour-equivalents (h) of
goods, i.e. hours of human work embodied in them (v63/io multipliers).

Sectors: HH households, ENT enterprises, REG regional fund (pays public-service
wages, retiree incomes, disability guarantees, child allowances, receives
enterprise surplus), ONE One Earth (issues U, holds deposits, finances regions).

Fixed price rule (rule 8): one price per hour-equivalent, pi (U/h), set ONCE so
that household consumption spending buys exactly the household goods supply
(no shortage, no overproduction) in the base year; then never changed.

Accounting identity (checked): REG balance = consumption + new-home purchases
- total household income = -(household saving not spent on new homes).
So unspent saving is mirrored, U for U, by deposits that are liabilities of ONE.
"""


def population_groups(pop):
    """pop: {'Y<age>': n, 'Y_LT1': n, 'Y_OPEN': n} -> children, adults 20-64, 65+, 18-19."""
    def age(k):
        if k == "Y_LT1":
            return 0
        if k == "Y_OPEN":
            return 100
        return int(k[1:]) if k[1:].isdigit() else None
    g = {"children_0_17": 0.0, "young_18_19": 0.0, "adults_20_64": 0.0, "retired_65_plus": 0.0}
    for k, v in pop.items():
        a = age(k)
        if a is None:
            continue
        key = ("children_0_17" if a <= 17 else "young_18_19" if a <= 19 else
               "adults_20_64" if a <= 64 else "retired_65_plus")
        g[key] += v
    return g


def wage_distribution(isco_counts, multipliers, cap):
    """Shares of workers by multiplier level (from occupation mix)."""
    total = sum(v for k, v in isco_counts.items() if k in multipliers)
    return {k: (isco_counts[k] / total, min(multipliers[k], cap)) for k in multipliers if k in isco_counts}


def mean_multiplier(dist):
    return sum(share * m for share, m in dist.values())


def child_benefit(n_children, adult_income, per_child=1000, threshold=15000):
    """Spec formula: min(1000*n, max(0, 15000 - adult household income)), per month."""
    return min(per_child * n_children, max(0.0, threshold - adult_income))


def expected_child_benefit(n_children, n_adults, dist, emp_rate, base, per_child, threshold):
    """Expected monthly benefit for a household, enumerating each adult's status
    (employed with a multiplier drawn from the occupation mix, or not employed)."""
    outcomes = [(1 - emp_rate, 0.0)] + [(emp_rate * s, base * m) for s, m in dist.values()]
    if n_adults == 1:
        return sum(p * child_benefit(n_children, y, per_child, threshold) for p, y in outcomes)
    return sum(p1 * p2 * child_benefit(n_children, y1 + y2, per_child, threshold)
               for p1, y1 in outcomes for p2, y2 in outcomes)


def annual_circuit(inp, cfg, multiplier_scale=1.0, supply_scale=1.0, pi=None):
    """One year of flows (U/year) and the physical check. Returns dict."""
    base = cfg["base_salary_u_month"]["value"]
    g = inp["groups"]
    workers = cfg["employment_rate_20_64"]["value"] * g["adults_20_64"]
    unable = cfg["unable_to_work_share_20_64"]["value"] * g["adults_20_64"]
    dist = inp["wage_dist"]
    mbar = mean_multiplier(dist) * multiplier_scale
    wages = workers * base * mbar * 12
    pub_share = cfg["public_service_employment_share"]["value"]
    wages_pub, wages_ent = wages * pub_share, wages * (1 - pub_share)
    disability = unable * cfg["disability_guarantee_u_month"]["value"] * 12
    rn = cfg["retiree_needs"]
    r = inp["retirees"]
    retiree_income = 12 * (r["single_units"] * rn["single_basket_u_month"]
                           + r["couple_units"] * rn["single_basket_u_month"] * rn["couple_factor"]
                           + (r["single_units"] + r["couple_units"]) * r["renter_share"] * rn["rent_u_month"])
    child = inp["child_benefit_month"] * 12
    income_adults = wages + disability
    income = income_adults + retiree_income + child
    s_ad = cfg["saving_rate_adults_20_64"]["value"]
    s_ret = cfg["saving_rate_retirees"]["value"]
    saving = s_ad * income_adults + s_ret * retiree_income
    consumption = income - saving
    supply_h = inp["household_supply_h"] * supply_scale
    if pi is None:
        pi = consumption / supply_h  # base-year calibration, then fixed forever
    demand_h = consumption / pi
    homes_value_capacity = inp["residential_construction_h"] * supply_scale * pi
    home_spending = min(saving, homes_value_capacity)
    reg_balance = consumption + home_spending - income
    return {"workers": workers, "unable_to_work": unable, "mean_multiplier": mbar,
            "wages": wages, "wages_public": wages_pub, "wages_enterprise": wages_ent,
            "disability_guarantees": disability, "retiree_income": retiree_income,
            "child_allowances": child, "household_income": income, "saving": saving,
            "consumption": consumption, "pi_u_per_hour": pi, "supply_h": supply_h, "demand_h": demand_h,
            "excess_demand_share": demand_h / supply_h - 1,
            "new_home_capacity_u": homes_value_capacity, "new_home_spending": home_spending,
            "unspent_saving": saving - home_spending,
            "enterprise_surplus": consumption + home_spending - wages_ent,
            "reg_outflows": wages_pub + disability + retiree_income + child,
            "reg_balance": reg_balance}


def transaction_matrix(c):
    """Flow-of-funds for one year: rows = transactions, columns = sectors (+ source, - use).
    Every row must sum to zero; every column sums to the sector's net lending."""
    rows = {
        "wages_enterprise": {"HH": c["wages_enterprise"], "ENT": -c["wages_enterprise"]},
        "wages_public": {"HH": c["wages_public"], "REG": -c["wages_public"]},
        "transfers_reg": {"HH": c["disability_guarantees"] + c["retiree_income"] + c["child_allowances"],
                          "REG": -(c["disability_guarantees"] + c["retiree_income"] + c["child_allowances"])},
        "consumption": {"HH": -c["consumption"], "ENT": c["consumption"]},
        "new_homes": {"HH": -c["new_home_spending"], "ENT": c["new_home_spending"]},
        "enterprise_surplus_to_reg": {"ENT": -c["enterprise_surplus"], "REG": c["enterprise_surplus"]},
        "one_earth_financing": {"REG": -c["reg_balance"], "ONE": c["reg_balance"]},
        "change_in_deposits": {"HH": -c["unspent_saving"], "ONE": c["unspent_saving"]},
    }
    cols = {"HH": 0.0, "ENT": 0.0, "REG": 0.0, "ONE": 0.0}
    for r in rows.values():
        for k, v in r.items():
            cols[k] += v
    return rows, cols


def years_to_buy(price, monthly_salary, saving_rate, earners=1):
    return price / (monthly_salary * saving_rate * earners * 12)


def dynamics(inp, cfg, creep, productivity):
    """Fixed pi from year 0; multipliers drift by `creep`/yr, supply grows by `productivity`/yr.
    Tracks deposits (= ONE liabilities) and the excess-demand share at fixed prices."""
    pi = annual_circuit(inp, cfg)["pi_u_per_hour"]
    deposits, out = 0.0, []
    for t in range(cfg["dynamics"]["years"] + 1):
        c = annual_circuit(inp, cfg, (1 + creep) ** t, (1 + productivity) ** t, pi=pi)
        deposits += c["unspent_saving"]
        out.append({"year": t, "creep": creep, "productivity": productivity,
                    "excess_demand_share": c["excess_demand_share"], "deposits_u": deposits,
                    "deposits_in_years_of_consumption": deposits / c["consumption"]})
    return out
