"""UNIRA V4.8: auditable screening model, not a calibrated city forecast.
Run: python model.py
"""
import csv
from pathlib import Path
ROOT=Path(__file__).parent
# All numerical intervention assumptions below are explicitly illustrative.
OPTIONS=[
 {'name':'repair','capacity':150,'cost':12000,'carbon':9,'quality':True,'consent':True},
 {'name':'deep_retrofit','capacity':250,'cost':35000,'carbon':6,'quality':True,'consent':True},
 {'name':'conversion','capacity':100,'cost':85000,'carbon':14,'quality':True,'consent':True},
 {'name':'new_build','capacity':1000,'cost':230000,'carbon':35,'quality':True,'consent':True},
]
def allocate(demand, carbon_price=0, options=OPTIONS):
    if demand < 0 or carbon_price < 0: raise ValueError('nonnegative inputs required')
    eligible=[o for o in options if o['quality'] and o['consent'] and o['capacity']>0]
    eligible.sort(key=lambda o:(o['cost']+carbon_price*o['carbon'],o['name']))
    remaining=demand; rows=[]
    for o in eligible:
        n=min(remaining,o['capacity'])
        if n: rows.append({'intervention':o['name'],'units':n,'total_cost':n*o['cost'],'total_tco2e':n*o['carbon']})
        remaining-=n
        if not remaining: break
    return rows,remaining

def main():
    with (ROOT/'scenario_results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['scenario','intervention','units','total_cost','total_tco2e','unmet_units'])
        w.writeheader()
        for label,demand,carbon_price in [('cost_priority',400,0),('carbon_weighted',400,10000),('high_demand',1600,0)]:
            rows,unmet=allocate(demand,carbon_price)
            for r in rows:w.writerow({'scenario':label,**r,'unmet_units':unmet})
            if not rows:w.writerow({'scenario':label,'intervention':'none','units':0,'total_cost':0,'total_tco2e':0,'unmet_units':unmet})
            print(label,'allocated',sum(r['units'] for r in rows),'unmet',unmet,'cost',sum(r['total_cost'] for r in rows))
if __name__=='__main__':main()
