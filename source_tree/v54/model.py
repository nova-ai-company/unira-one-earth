"""UNIRA V5.4: transparent physical feasibility and monetary consistency model.
Run: python model.py. All scenario inputs are illustrative, not observed city data.
"""
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SCENARIOS=json.loads((ROOT/'scenarios.json').read_text())

def evaluate(s):
    interventions=s['interventions']; demand=s['housing_need']; workforce=s['available_workers']; hours_per_worker=s['hours_per_worker_year']
    result={'scenario':s['name'],'housing_need':demand}
    for metric in ('labour_hours','cement_t','steel_t','electricity_mwh','water_m3','embodied_tco2e'):
        result[metric]=round(sum(i['homes']*i[metric+'_per_home'] for i in interventions),2)
    result['homes_delivered']=sum(i['homes'] for i in interventions)
    result['unmet_homes']=max(0,demand-result['homes_delivered'])
    result['excess_homes']=max(0,result['homes_delivered']-demand)
    result['worker_years_required']=round(result['labour_hours']/hours_per_worker,2)
    result['labour_capacity_hours']=workforce*hours_per_worker
    limits=s['resource_limits']; result['shortages']={k:round(max(0,result[k]-v),2) for k,v in limits.items()}
    result['feasible']=result['unmet_homes']==0 and result['excess_homes']==0 and result['labour_hours']<=result['labour_capacity_hours'] and all(x==0 for x in result['shortages'].values())
    # Nominal salary U is not a physical input or purchasing power estimate.
    result['annual_base_payroll_u']=workforce*s['monthly_base_salary_u']*12
    result['physical_cost_index']=round(sum(result[k]/v for k,v in limits.items() if v>0)/sum(v>0 for v in limits.values()),4) if any(v>0 for v in limits.values()) else None
    return result

def main():
    rows=[evaluate(s) for s in SCENARIOS]
    (ROOT/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
    with (ROOT/'results.csv').open('w',newline='') as f:
        fields=['scenario','housing_need','homes_delivered','unmet_homes','excess_homes','labour_hours','worker_years_required','cement_t','steel_t','electricity_mwh','water_m3','embodied_tco2e','physical_cost_index','annual_base_payroll_u','feasible']
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows([{k:r[k] for k in fields} for r in rows])
    for r in rows:print(r['scenario'], 'feasible=',r['feasible'],'unmet=',r['unmet_homes'],'shortages=',r['shortages'])
if __name__=='__main__':main()
