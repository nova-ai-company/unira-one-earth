"""UNIRA V5.3 illustrative integer housing intervention optimizer. Requires scipy >=1.9."""
import csv, json
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

BASE=Path(__file__).parent

def solve(demand=100, budget=18_000_000, carbon_price=0, stock_first=False):
    # All capacities, costs, emissions and household need are synthetic; NOT calibrated city data.
    actions=[
      dict(name='repair_adapt',capacity=20,cost=45000,carbon=14,new=0),
      dict(name='deep_renovation',capacity=35,cost=110000,carbon=20,new=0),
      dict(name='conversion',capacity=25,cost=170000,carbon=32,new=0),
      dict(name='new_construction',capacity=90,cost=280000,carbon=75,new=1),
      dict(name='unmet',capacity=demand,cost=0,carbon=0,new=0),
    ]
    n=len(actions); c=np.array([a['cost']+carbon_price*a['carbon'] for a in actions],float)
    # A large transparent unmet-need penalty makes satisfying needs the primary objective.
    c[-1]=1e9
    if stock_first:
        # First find the least new construction compatible with zero unmet demand and budget.
        constraints=[LinearConstraint(np.ones((1,n)),[demand],[demand]),LinearConstraint(np.array([[a['cost'] for a in actions]]),[-np.inf],[budget]),LinearConstraint(np.eye(n)[-1:],[0],[0])]
        r=milp(np.array([a['new'] for a in actions],float),integrality=np.ones(n),bounds=Bounds(np.zeros(n),[a['capacity'] for a in actions]),constraints=constraints)
        if r.success:
            min_new=round(r.fun)
            constraints.append(LinearConstraint(np.array([[a['new'] for a in actions]]),[-np.inf],[min_new]))
        else: constraints=[]
    else: constraints=[]
    constraints += [LinearConstraint(np.ones((1,n)),[demand],[demand]),LinearConstraint(np.array([[a['cost'] for a in actions]]),[-np.inf],[budget])]
    r=milp(c,integrality=np.ones(n),bounds=Bounds(np.zeros(n),[a['capacity'] for a in actions]),constraints=constraints)
    if not r.success: raise RuntimeError(r.message)
    x=np.rint(r.x).astype(int)
    return {'demand':demand,'budget_eur':budget,'carbon_price_eur_per_t':carbon_price,'stock_first':stock_first,'allocation':{a['name']:int(v) for a,v in zip(actions,x)},'cost_eur':int(sum(a['cost']*v for a,v in zip(actions,x))),'carbon_t_co2e':int(sum(a['carbon']*v for a,v in zip(actions,x))),'unmet':int(x[-1]),'new_homes':int(x[3]),'input_status':'SYNTHETIC — not a city forecast'}

if __name__=='__main__':
    scenarios=[('minimum_cost',dict()),('carbon_price_200',dict(carbon_price=200)),('stock_first',dict(stock_first=True)),('tight_budget',dict(budget=8_000_000)),('higher_need',dict(demand=140,budget=30_000_000))]
    results=[dict(scenario=name,**solve(**kwargs)) for name,kwargs in scenarios]
    (BASE/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    with (BASE/'results.csv').open('w',newline='') as f:
      w=csv.writer(f);w.writerow(['scenario','demand','repair_adapt','deep_renovation','conversion','new_construction','unmet','cost_eur','carbon_t_co2e'])
      for row in results:
       a=row['allocation'];w.writerow([row['scenario'],row['demand'],a['repair_adapt'],a['deep_renovation'],a['conversion'],a['new_construction'],row['unmet'],row['cost_eur'],row['carbon_t_co2e']])
    for r in results: print(r['scenario'],r['allocation'],r['cost_eur'])
