"""UNIRA V5.0 reproducible research prototype. All action parameters SYNTHETIC."""
import csv
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
HERE=Path(__file__).resolve().parent
DEMAND={'small':45,'family':35,'accessible':20}

def load():
    with (HERE/'actions.csv').open(newline='') as f:return list(csv.DictReader(f))

def optimize(actions,demand=DEMAND,carbon_price=0,stock_first=False,budget=None,carbon_scale=1,operational_share=.6):
    a=[r for r in actions if all(r[k]=='yes' for k in ('consent','safe','suitable'))]
    n=len(a)
    if not n:return {'status':'infeasible'}
    cost=np.array([float(r['cost_eur']) for r in a]); cap=np.array([int(r['capacity']) for r in a]);
    base=np.array([float(r['carbon_30y_t']) for r in a]); carbon=base*((1-operational_share)+operational_share*carbon_scale)
    new=np.array([int(r['kind']=='new_build') for r in a]); rows=[];lo=[];hi=[]
    for cohort,required in demand.items():
        rows.append([int(r['cohort']==cohort) for r in a]);lo.append(required);hi.append(required)
    if budget is not None:rows.append(cost);lo.append(-np.inf);hi.append(budget)
    bounds=Bounds(np.zeros(n),cap)
    def run(objective,extra=None):
        rr=list(rows);ll=list(lo);hh=list(hi)
        if extra is not None:rr.append(new);ll.append(extra);hh.append(extra)
        res=milp(c=objective,integrality=np.ones(n),bounds=bounds,constraints=LinearConstraint(np.array(rr),np.array(ll),np.array(hh)),options={'time_limit':30,'mip_rel_gap':0})
        return res
    if stock_first:
        first=run(new.astype(float))
        if first.status!=0:return {'status':'infeasible','message':first.message}
        min_new=int(round(first.fun))
    else:min_new=None
    result=run(cost+carbon_price*carbon,min_new)
    if result.status!=0:return {'status':'infeasible','message':result.message}
    counts=np.rint(result.x).astype(int)
    return {'status':'optimal','cost_eur':round(float(counts@cost),2),'carbon_30y_t':round(float(counts@carbon),2),'new_build':int(counts@new),'units':int(sum(counts)),'allocation':{r['id']:int(q) for r,q in zip(a,counts) if q}}

def main():
    actions=load(); scenarios=[]
    for name,price,stock,scale in [('cost',0,False,1),('stock_first',0,True,1),('carbon_weighted',1000,False,1),('stock_first_carbon',1000,True,1),('high_operational_emissions',1000,False,1.5),('low_operational_emissions',1000,False,.5)]:
        result=optimize(actions,carbon_price=price,stock_first=stock,carbon_scale=scale)
        scenarios.append({'scenario':name,**{k:v for k,v in result.items() if k!='allocation'}})
    with (HERE/'results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['scenario','status','cost_eur','carbon_30y_t','new_build','units']);w.writeheader();w.writerows(scenarios)
    for row in scenarios:print(row)
if __name__=='__main__':main()
