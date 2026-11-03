"""UNIRA V4.9: exact integer allocation using scipy.optimize.milp.
All case inputs are SYNTHETIC. Emissions are illustrative 30-year tCO2e.
"""
import csv
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

HERE=Path(__file__).resolve().parent

def load():
    with (HERE/'actions.csv').open(newline='') as f:
        return list(csv.DictReader(f))

def solve(actions, demand, carbon_price=0., budget=None, stock_first=False):
    """Minimise cost + carbon_price * 30y tCO2e; integer unit counts.
    Each action is a location/household-compatible intervention, pre-screened
    for consent, safety and accessible accommodation. Demand by cohort.
    """
    cohorts=sorted(demand)
    valid=[a for a in actions if a['consent']=='yes' and a['safe']=='yes' and a['suitable']=='yes']
    if not valid: return {'status':'infeasible'}
    n=len(valid)
    costs=np.array([float(a['cost_eur']) for a in valid])
    carbon=np.array([float(a['carbon_30y_t']) for a in valid])
    capacity=np.array([int(a['capacity']) for a in valid])
    if stock_first:
        # Lexicographic priority: minimise new build, then monetised cost.
        # A mathematically safe large-M bound for this bounded dataset.
        max_objective=float(np.sum(capacity * (costs + carbon_price*carbon)))+1
        penalty=np.array([max_objective if a['kind']=='new_build' else 0 for a in valid])
    else: penalty=np.zeros(n)
    rows=[]; low=[]; high=[]
    for cohort in cohorts:
        rows.append([1. if a['cohort']==cohort else 0. for a in valid]); low.append(demand[cohort]); high.append(np.inf)
    if budget is not None:
        rows.append(costs.tolist());low.append(-np.inf);high.append(budget)
    res=milp(c=costs+carbon_price*carbon+penalty, integrality=np.ones(n),bounds=Bounds(np.zeros(n),capacity),constraints=LinearConstraint(np.array(rows),np.array(low),np.array(high)),options={'time_limit':30})
    if not res.success: return {'status':'infeasible','solver_message':res.message}
    counts=np.rint(res.x).astype(int)
    allocation=[{'id':a['id'],'cohort':a['cohort'],'kind':a['kind'],'units':int(q)} for a,q in zip(valid,counts) if q]
    return {'status':'optimal','allocation':allocation,'units':int(counts.sum()),'cost_eur':round(float(counts@costs),2),'carbon_30y_t':round(float(counts@carbon),2),'new_build':sum(int(q) for a,q in zip(valid,counts) if a['kind']=='new_build')}

def run():
    actions=load()
    demand={'small':45,'family':35,'accessible':20}
    scenarios=[('cost_min',0,False),('carbon_10000',10000,False),('stock_first',0,True),('stock_first_carbon_10000',10000,True)]
    rows=[]
    for name,price,stock in scenarios:
        r=solve(actions,demand,price,stock_first=stock)
        rows.append({'scenario':name,**{k:v for k,v in r.items() if k!='allocation'}})
        print(name, r)
    with (HERE/'results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['scenario','status','units','cost_eur','carbon_30y_t','new_build']);w.writeheader();w.writerows(rows)
if __name__=='__main__':run()
