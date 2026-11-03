"""UNIRA V6.3 health & care staffing under 30 h from year 1 (France).

Headcount requirement: the 30 h cap removes a share of hours in NACE Q (V6.2,
primary scenario, employees). With theta about 0 in care (evidence review), each
occupation needs N_extra = N * (gain_Q) more people. Occupation-specific hours
are not available, so the section-Q ratio is applied to every occupation
(documented assumption). Self-employed physicians are partly outside the
primary cap; using the Q ratio for all physicians is therefore an upper bound.

Training pipeline:
  graduates[t]                observed (hlth_rs_grd2)
  exits ~= graduates - net stock change   (MODEL_DERIVED; includes migration)
  lead_time                   years from training expansion to new graduates
                              (REPORTED_NEEDS_RECHECK, see config)
Additional graduates from an expansion of e (share of current intake) arrive
from year lead_time+1 onward; years to close = lead_time + ceil(N_extra / (e*G)).
"""
import math


def mean_annual_change(series, start, end):
    return (series[end] - series[start]) / (end - start)


def implied_exits(graduates, stock, start, end):
    """Average annual exits (incl. net emigration) = graduates - net stock growth."""
    g = sum(graduates[y] for y in range(start + 1, end + 1)) / (end - start)
    return g - mean_annual_change(stock, start, end)


def extra_needed(stock, gain):
    return stock * gain


def years_to_close(extra, graduates_per_year, expansion, lead_time):
    """Years until an expansion of training intake (share e of current graduates)
    has produced `extra` additional practitioners; inf if no expansion."""
    if extra <= 0:
        return 0
    added = graduates_per_year * expansion
    if added <= 0:
        return math.inf
    return lead_time + math.ceil(extra / added)


def year1_shortfall(extra, year1_additional_supply):
    """Persons still missing in year 1 (training cannot respond within a year)."""
    return max(0.0, extra - year1_additional_supply)
