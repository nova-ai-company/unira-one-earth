"""UNIRA V5.9: transparent hypothetical multi-sector 20-year physical feasibility prototype.
All values synthetic, sector units incomparable. No empirical calibration.
"""
from dataclasses import dataclass, asdict
import json, csv, argparse

SECTORS = ('food','housing','energy','healthcare','manufacturing','infrastructure')
@dataclass(frozen=True)
class Sector:
    demand: float
    capacity: float
    hours_per_unit: float
    maintenance_units: float
    capex_per_capacity: float

BASE = {
 'food': Sector(100,115,12,1.5,1000),
 'housing': Sector(100,108,15,1.2,1300),
 'energy': Sector(100,170,8,1.8,900),
 'healthcare': Sector(100,110,22,1.4,1600),
 'manufacturing': Sector(100,165,18,1.7,1400),
 'infrastructure': Sector(100,108,20,1.5,1800),
}
# Simplified intermediate input coefficients: units of input sector per output unit.
INPUTS = {'food':{'energy':.08,'manufacturing':.04}, 'housing':{'manufacturing':.12,'energy':.06},
          'energy':{'manufacturing':.08}, 'healthcare':{'energy':.07,'manufacturing':.08},
          'manufacturing':{'energy':.15}, 'infrastructure':{'manufacturing':.13,'energy':.08}}

def gross_requirements(final):
    """Solve gross output x = final + A*x by fixed-point iteration."""
    x = dict(final)
    for _ in range(1000):
        new = {s: final[s] + sum(INPUTS[j].get(s,0)*x[j] for j in SECTORS) for s in SECTORS}
        if max(abs(new[s]-x[s]) for s in SECTORS) < 1e-10: return new
        x = new
    raise RuntimeError('Input-output system failed to converge')

def simulate(years=20, growth=0.0, shock_year=None, shock_sector='energy', shock_fraction=0.0,
             annual_investment_budget=120000, annual_labor_hours=16000, replacement=True):
    capacity = {s: BASE[s].capacity for s in SECTORS}
    rows=[]
    for year in range(1,years+1):
        demand = {s:BASE[s].demand*(1+growth)**(year-1) for s in SECTORS}
        gross = gross_requirements(demand)
        actual_cap = dict(capacity)
        if year == shock_year: actual_cap[shock_sector] *= (1-shock_fraction)
        # Production scaled proportionately so neither physical sector nor labour capacity is exceeded.
        sector_ratio = min(1.0, *(actual_cap[s]/gross[s] for s in SECTORS))
        hours_needed = sum(gross[s]*BASE[s].hours_per_unit for s in SECTORS)
        labor_ratio = min(1.0,annual_labor_hours/hours_needed)
        ratio = min(sector_ratio,labor_ratio)
        delivered = {s:demand[s]*ratio for s in SECTORS}
        produced = {s:gross[s]*ratio for s in SECTORS}
        # Depreciation of productive capacity; investment must fit actual monetary budget.
        required_spend = sum(BASE[s].maintenance_units*BASE[s].capex_per_capacity for s in SECTORS)
        investment_spend = min(annual_investment_budget,required_spend) if replacement else 0
        for s in SECTORS:
            depreciation = BASE[s].maintenance_units
            replacement_units = BASE[s].maintenance_units * (investment_spend/required_spend) if required_spend else 0
            capacity[s] = max(0,capacity[s]-depreciation+replacement_units)
        rows.append({'year':year,'demand_total_index':round(sum(demand.values()),4),
                     'served_fraction':round(ratio,6),'unmet_total_index':round(sum(demand[s]-delivered[s] for s in SECTORS),4),
                     'hours_required':round(hours_needed,2),'hours_used':round(hours_needed*ratio,2),
                     'investment_budget_U':annual_investment_budget,'investment_spent_U':round(investment_spend,2),
                     'investment_unfunded_U':round(max(0,required_spend-investment_spend),2),
                     **{f'unmet_{s}':round(demand[s]-delivered[s],4) for s in SECTORS},
                     **{f'capacity_{s}':round(capacity[s],4) for s in SECTORS}})
    return rows

def run_all():
    cases={'baseline':{},'energy_shock':{'shock_year':5,'shock_sector':'energy','shock_fraction':.35},
           'population_growth':{'growth':.025},'no_replacement':{'replacement':False},
           'tight_investment':{'annual_investment_budget':4000},
           'labor_constraint':{'annual_labor_hours':9000}}
    return {name:simulate(**args) for name,args in cases.items()}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='.'); args=p.parse_args()
    from pathlib import Path
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    cases=run_all()
    with open(out/'results.json','w') as f:json.dump(cases,f,indent=2)
    with open(out/'annual_results.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['scenario']+list(next(iter(cases.values()))[0]));w.writeheader()
        for name,rows in cases.items():
            for row in rows:w.writerow({'scenario':name,**row})
    for name,rows in cases.items():
        print(f'{name}: shortage years={sum(r["unmet_total_index"]>0 for r in rows)}, cumulative unmet index={sum(r["unmet_total_index"] for r in rows):.2f}, unfunded investment={sum(r["investment_unfunded_U"] for r in rows):.0f} U')
