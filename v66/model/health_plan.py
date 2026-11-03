"""UNIRA V6.6 — global health-workforce plan (years until everyone has care at a threshold).

Annual stock-flow, world as one entity (rule 3), physical persons:
  need[t]   = tau_per_10k/1e4 * population[t] * (1 - preventable_share(t))      (rule 19 hypothesis)
  stock[t+1]= stock[t]*(1-exit_rate) + graduates[t]
  graduates[t] = intake[t - lead_time]            (training pipeline)
  intake[t] = base_intake * (1 + expansion)^min(t, ramp_years) + converted_military[t]
              capped by training capacity (teachers/schools) = intake_capacity_multiple * base_intake
Converted military: disarmament (rule 19) frees armed-forces personnel; a voluntary share joins
health training over `conversion_years` (no coercion). Health need is not proportional to disease
burden: ageing raises need; preventable_share is the evidence-based net effect.
"""


def interp(points, t):
    """Piecewise-linear interpolation over {year: value} (flat outside)."""
    ys = sorted(points)
    if t <= ys[0]:
        return points[ys[0]]
    if t >= ys[-1]:
        return points[ys[-1]]
    for a, b in zip(ys, ys[1:]):
        if a <= t <= b:
            return points[a] + (points[b] - points[a]) * (t - a) / (b - a)


def simulate(p, years=60):
    """p: dict of parameters (see config). Returns yearly rows and the first year gap <= 0."""
    stock = p["stock0"]
    pipeline = [p["base_intake"]] * p["lead_time"]  # students already in training graduate at base rate
    mil_left = p["military_pool"] * p["military_volunteer_share"]
    rows, closed = [], None
    for t in range(years + 1):
        pop = interp(p["population"], t)
        prevent = interp(p["preventable_share"], t)
        need = p["tau_per_10k"] / 1e4 * pop * (1 - prevent)
        gap = need - stock
        if closed is None and gap <= 0:
            closed = t
        rows.append({"year": t, "need": need, "stock": stock, "gap": gap, "preventable_share": prevent,
                     "per_10k": stock / pop * 1e4})
        conv = 0.0
        if mil_left > 0 and t < p["conversion_years"]:
            conv = min(mil_left, p["military_pool"] * p["military_volunteer_share"] / p["conversion_years"])
            mil_left -= conv
        intake = p["base_intake"] * (1 + p["expansion"]) ** min(t, p["ramp_years"]) + conv
        intake = min(intake, p["base_intake"] * p["intake_capacity_multiple"])
        pipeline.append(intake)
        graduates = pipeline.pop(0)
        stock = stock * (1 - p["exit_rate"]) + graduates
    return rows, closed
