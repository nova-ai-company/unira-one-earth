"""V6.3 analyses on top of IOSystem. Every quantity is in thousand hours."""
import json
from pathlib import Path


def uncovered_hours_from_v62(summary_path, cap="30"):
    """Hours still uncovered after V6.2's evidence pathway, as a SHARE of total hours
    (applied to the IO base year; the V6.2 base year is 2023)."""
    s = json.loads(Path(summary_path).read_text())
    out = {}
    for case, r in s["evidence_pathway_FR"][cap].items():
        g = r["residual_required_gain"]
        out[case] = g / (1 + g)  # share of hours: H0 - H0/(1+g)
    return out


def household_basket(io, top=15):
    by = io.embodied_by_use_and_product()["household_consumption"]
    rows = sorted(zip(io.products, by), key=lambda t: -t[1])
    return rows[:top]


def extraction_table(io):
    total = sum(io.hours)
    rows = []
    for p in io.products:
        saved = io.hypothetical_extraction(p)
        rows.append({"product": p, "direct_hours_ths": io.hours[io.products.index(p)],
                     "hours_saved_full_extraction_ths": saved, "share_of_total_hours": saved / total})
    return rows


def partial_reduction(io, reductions):
    """Hours saved when the product's activity shrinks by r both as final and as
    intermediate good: A row and final demand scaled by (1-r). Upper bound (no substitutes)."""
    A2 = [[a * (1 - reductions[io.products[i]]) if io.products[i] in reductions else a
           for a in row] for i, row in enumerate(io.A)]
    from . import model
    m2 = model.multipliers(A2, io.l)
    f = [sum(io.F[c][i] for c in io.F) * (1 - reductions.get(p, 0.0)) for i, p in enumerate(io.products)]
    return sum(io.hours) - sum(a * b for a, b in zip(m2, f))


def durables_lever(io, cfg):
    """Household + investment purchases of durables scaled by 1/(1+e); repair hours added."""
    hh = io.embodied_by_use_and_product()
    idx = [io.products.index(p) for p in cfg["products"]]
    base = sum(hh["household_consumption"][i] + hh["gross_fixed_capital_formation"][i] for i in idx)
    rr = cfg["repair_hours_per_saved_hour"]["value"]
    out = []
    for e in cfg["lifetime_extensions"]:
        saved = base * (1 - 1 / (1 + e))
        out.append({"lifetime_extension": e, "durables_hours_ths": base, "gross_saved_ths": saved,
                    "net_saved_ths": saved * (1 - rr), "share_of_total_hours": saved * (1 - rr) / sum(io.hours)})
    return out


def imported_durables_hours_equivalent(io, products):
    """Hours France would need to make its imported durables itself (domestic technology
    assumption): an indicator of labour embodied ABROAD that stock-first could save."""
    imp = [0.0] * len(io.products)
    for p in products:
        i = io.products.index(p)
        imp[i] = io.F_imp["household_consumption"][i] + io.F_imp["gross_fixed_capital_formation"][i]
    return io.embodied(imp)
