"""UNIRA v0.1: reproducible illustrative aggregate scenario, NOT a feasibility proof."""
from dataclasses import dataclass
@dataclass
class Scenario:
    population_billion: float = 8.2
    adults_billion: float = 5.8
    children_billion: float = 2.4
    working_share: float = .75
    hours_week: float = 30
    comparator_workers_billion: float = 3.6
    comparator_hours_week: float = 43
    basic_salary: float = 5000
    child_allowance: float = 1000

def child_benefit(adult_income: float, children: int) -> float:
    if adult_income < 0 or children < 0: raise ValueError('Invalid household input')
    return min(1000 * children, max(0, 15000 - adult_income))

def calculate(s: Scenario) -> dict:
    if abs(s.adults_billion+s.children_billion-s.population_billion)>1e-6:
        raise ValueError('Adult and child counts must sum to population')
    if not 0 <= s.working_share <= 1 or s.hours_week <= 0: raise ValueError('Invalid work inputs')
    workers = s.adults_billion*s.working_share
    hours = workers*s.hours_week
    baseline = s.comparator_workers_billion*s.comparator_hours_week
    return {'workers_billion':workers,'hours_billion_per_week':hours,
            'comparator_hours_billion_per_week':baseline,
            'hours_change_percent':100*(hours/baseline-1),
            'productivity_multiplier_for_equal_output':baseline/hours,
            'base_payroll_trillion_U_year':workers*s.basic_salary*12/1000,
            'maximum_child_allowance_trillion_U_year':s.children_billion*s.child_allowance*12/1000}
if __name__=='__main__':
    for key,value in calculate(Scenario()).items(): print(f'{key}: {value:.3f}')
    assert child_benefit(10000,2)==2000
    assert child_benefit(10000,7)==5000
    assert child_benefit(16000,2)==0
