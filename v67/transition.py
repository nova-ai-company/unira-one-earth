"""UNIRA V6.7 — 30-year world transition plan, region by region (217 countries = regions).

The One Earth entity allocates each year's NEW physical capacity needs-first:
  energy   new clean final energy (EJ/yr, from solar+wind build rate) -> regions below the target,
           in proportion to their shortfall; regions above the target converge down by `excess_decline`
  health   net new health workers (world training plan, v66) -> regions below the target, trained in-region
  housing  new residential floor area (m2/yr, world construction capacity) -> regions below the target
  food     today's surplus redistributed at once (decent); waste falls linearly to the UNIRA level over
           `waste_years`, which raises usable supply toward the comfortable level
Population per region: linear 2024 -> 2050 (UN WPP medium), flat after.
Nothing is moved that cannot be moved: energy, health workers and homes are BUILT or TRAINED where people live.
"""


def lerp(a, b, f):
    return a + (b - a) * max(0.0, min(1.0, f))


def allocate(pool, deficits):
    """Split `pool` across regions in proportion to deficit, never above any region's deficit (water-filling)."""
    give = {k: 0.0 for k in deficits}
    left = pool
    active = {k: d for k, d in deficits.items() if d > 0}
    while left > 1e-9 and active:
        tot = sum(active.values())
        done = []
        for k, d in active.items():
            share = left * d / tot
            g = min(share, d - give[k])
            give[k] += g
        left = pool - sum(give.values())
        done = [k for k, d in active.items() if give[k] >= d - 1e-9]
        if not done:
            break
        for k in done:
            del active[k]
    return give


def allocate_perceived(pool, true_def, p, domain, t):
    """Allocate by the allocator's PERCEIVED deficits (p['perceive'] hook: errors, lags,
    misreporting); a region receives nothing beyond its TRUE deficit, and anything sent to a
    region that turns out not to need it is wasted (not re-allocated within the year)."""
    if "perceive" not in p:
        return allocate(pool, true_def)
    seen = p["perceive"](domain, t, true_def)
    planned = allocate(pool, seen)
    return {k: min(planned[k], true_def[k]) for k in true_def}


def run(regions, p, years=30):
    """regions: {iso: {pop0, pop50, energy_gj, health_10k, floor_m2, kcal}}; p: parameters."""
    st = {k: dict(v) for k, v in regions.items()}
    rows, reached = [], {k: {} for k in regions}
    targets = {"energy": ("energy_gj", p["energy_target"]), "health": ("health_10k", p["health_target"]),
               "housing": ("floor_m2", p["floor_target"])}
    initial = {}
    for t in range(years + 1):
        f = t / 26.0
        for k, r in st.items():
            r["pop"] = lerp(r["pop0"], r["pop50"], f)
        waste = lerp(p["waste_now"], p["waste_unira"], t / p["waste_years"])
        usable_kcal_needed = {lvl: eaten / (1 - waste) for lvl, eaten in p["kcal_eaten"].items()}
        world_kcal = sum(r["kcal"] * r["pop"] for r in st.values()) / sum(r["pop"] for r in st.values())
        # --- record status
        totpop = sum(r["pop"] for r in st.values())
        row = {"year": t}
        for dom, key, tgt in (("energy", "energy_gj", p["energy_target"]), ("health", "health_10k", p["health_target"]),
                              ("housing", "floor_m2", p["floor_target"])):
            ok = sum(r["pop"] for r in st.values() if r[key] >= tgt - 1e-9)
            row[f"{dom}_share_pop_at_target"] = ok / totpop
            for kk, r in st.items():
                if r[key] >= tgt - 1e-9 and dom not in reached[kk]:
                    reached[kk][dom] = t
        for dom, (key, tgt) in targets.items():
            short = sum(max(0.0, tgt - r[key]) * r["pop"] for r in st.values())
            initial.setdefault(dom, short)
            row[f"{dom}_shortfall_closed"] = 1 - short / initial[dom] if initial[dom] else 1.0
        food_ok = world_kcal >= usable_kcal_needed["comfortable"]
        row["food_comfortable_for_all_feasible"] = food_ok
        row["world_energy_ej"] = sum(r["energy_gj"] * r["pop"] for r in st.values()) / 1e9
        row["world_health_workers_m"] = sum(r["health_10k"] * r["pop"] for r in st.values()) / 1e4 / 1e6
        row["world_floor_bn_m2"] = sum(r["floor_m2"] * r["pop"] for r in st.values()) / 1e9
        rows.append(row)
        if food_ok:
            for kk in reached:
                reached[kk].setdefault("food", t)
        # --- this year's allocations (needs-first)
        # no wars (rule 19): military energy use in regions above target is freed over `military_years`
        if t < p.get("military_years", 0):
            above = {k: r for k, r in st.items() if r["energy_gj"] > p["energy_target"]}
            tot_above = sum(r["energy_gj"] * r["pop"] for r in above.values())
            world_e = sum(r["energy_gj"] * r["pop"] for r in st.values())
            cut = p["military_energy_share"] * world_e / p["military_years"]
            for r in above.values():
                r["energy_gj"] = max(p["energy_target"], r["energy_gj"] - cut * r["energy_gj"] / tot_above)
        # energy: new GJ to regions below target; regions above converge down
        e_def = {k: max(0.0, (p["energy_target"] - r["energy_gj"]) * r["pop"]) for k, r in st.items()}
        pool = p["energy_new_ej_per_yr"] * 1e9 * p.get("energy_share_to_deficit", 1.0) * (1 - p.get("leakage", 0.0))
        give = allocate_perceived(pool, e_def, p, "energy", t)
        for k, r in st.items():
            r["energy_gj"] += give[k] / r["pop"]
            if r["energy_gj"] > p["energy_target"]:
                r["energy_gj"] = max(p["energy_target"], r["energy_gj"] * (1 - p["excess_decline"]))
        # health: net new workers this year from the training plan
        h_def = {k: max(0.0, (p["health_target"] - r["health_10k"]) / 1e4 * r["pop"]) for k, r in st.items()}
        new_workers = p["health_net_new"](t) * p.get("health_share_to_deficit", 1.0) * (1 - p.get("leakage", 0.0))
        give = allocate_perceived(new_workers, h_def, p, "health", t)
        for k, r in st.items():
            r["health_10k"] = (r["health_10k"] / 1e4 * r["pop"] + give[k]) / r["pop"] * 1e4
        # housing: new m2
        f_def = {k: max(0.0, (p["floor_target"] - r["floor_m2"]) * r["pop"]) for k, r in st.items()}
        floor_pool = p["floor_new_m2_per_yr"](t, f_def) if callable(p["floor_new_m2_per_yr"]) else p["floor_new_m2_per_yr"]
        give = allocate_perceived(floor_pool * (1 - p.get("leakage", 0.0)), f_def, p, "housing", t)
        row_extra = rows[-1]
        row_extra["floor_built_m2"] = sum(give.values())
        for k, r in st.items():
            r["floor_m2"] = (r["floor_m2"] * r["pop"] + give[k]) / r["pop"]
        # population growth dilutes per-capita stocks next year
        for k, r in st.items():
            nxt = lerp(r["pop0"], r["pop50"], (t + 1) / 26.0)
            scale = r["pop"] / nxt
            r["health_10k"] *= scale
            r["floor_m2"] *= scale
            r["energy_gj"] *= scale  # supply is built capacity: per-person falls as population grows
    p["_final_state"] = st
    return rows, reached
