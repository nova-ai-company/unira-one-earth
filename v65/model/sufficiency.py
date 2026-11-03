"""UNIRA V6.5 — is there enough for everyone on Earth? (needs x population, physical units)

For one domain (food kcal, energy GJ, health workers, floor area …):
  s_i   current supply per person in region i (physical units)
  P_i   population of region i
  tau   threshold per person (decent or comfortable; from v65/thresholds)

  world supply S = sum s_i P_i ;  world need N = tau * sum P_i ;  sufficiency R = S / N
  people below the threshold today = sum P_i [s_i < tau]
  shortfall volume D = sum max(0, tau - s_i) P_i ;  surplus volume U = sum max(0, s_i - tau) P_i

UNIRA allocation (rules 5 and 9: one entity, by needs x population):
  1. needs first: every region is brought to tau (needs D to be moved; possible iff R >= 1)
  2. what remains, S - N, is shared by population -> everyone gets a = S / sum P
  Volume moved between regions = sum max(0, s_i - a) P_i (= sum max(0, a - s_i) P_i).
For NON-TRADABLE domains (health workers, homes) "moving" means building or training
capacity locally; the model reports the years needed at a given world build rate.
"""


def domain_summary(rows, tau):
    """rows: list of dicts with keys region, population, supply_pc (None = missing)."""
    have = [r for r in rows if r["supply_pc"] is not None and r["population"]]
    pop = sum(r["population"] for r in have)
    S = sum(r["supply_pc"] * r["population"] for r in have)
    N = tau * pop
    below = [r for r in have if r["supply_pc"] < tau]
    D = sum((tau - r["supply_pc"]) * r["population"] for r in below)
    U = sum((r["supply_pc"] - tau) * r["population"] for r in have if r["supply_pc"] > tau)
    a = S / pop if pop else None
    moved = sum(max(0.0, r["supply_pc"] - a) * r["population"] for r in have) if a else None
    return {"population_covered": pop, "world_supply": S, "world_need": N,
            "sufficiency_ratio": S / N if N else None,
            "people_below_threshold": sum(r["population"] for r in below),
            "share_people_below": sum(r["population"] for r in below) / pop if pop else None,
            "shortfall_volume": D, "surplus_volume": U,
            "needs_first_feasible": S >= N,
            "equal_share_per_person": a, "equal_share_vs_threshold": a / tau if tau else None,
            "volume_moved_equal_share": moved, "share_of_supply_moved": moved / S if S else None}


def region_change(rows, region, tau=None):
    """Per-person change for one region if everyone receives the equal share."""
    have = [r for r in rows if r["supply_pc"] is not None and r["population"]]
    pop = sum(r["population"] for r in have)
    a = sum(r["supply_pc"] * r["population"] for r in have) / pop
    r = next((x for x in have if x["region"] == region), None)
    if r is None:
        return None
    out = {"region": region, "today_pc": r["supply_pc"], "equal_share_pc": a,
           "change_pct": 100 * (a / r["supply_pc"] - 1)}
    if tau:
        out["today_vs_threshold"] = r["supply_pc"] / tau
    return out


def years_to_close_nontradable(shortfall_volume, world_annual_addition):
    """E.g. health workers: shortfall / (new workers trained per year beyond replacement)."""
    if shortfall_volume <= 0:
        return 0.0
    if world_annual_addition <= 0:
        return float("inf")
    return shortfall_volume / world_annual_addition
