"""UNIRA V5.5: synthetic monetary/physical consistency stress tests. No empirical calibration."""
from dataclasses import dataclass, replace
import csv, json
from pathlib import Path

@dataclass(frozen=True)
class Household:
    adults: tuple[int,...] # monthly adult U incomes, incl guaranteed disability payments
    children: int

def child_allowance(h: Household) -> int:
    if h.children < 0 or any(x < 0 for x in h.adults): raise ValueError('negative income or children')
    return min(1000*h.children, max(0,15000-sum(h.adults)))

def income(h: Household) -> int:
    return sum(h.adults)+child_allowance(h)

# All capacities, needs, unit U prices and worker counts are hypothetical.
BASE={
 'name':'baseline', 'workers':120, 'hours_per_week':30, 'weeks_per_year':50,
 'public_service_workers':25, 'capital_maintenance_workers':10,
 'households':[{'adults':[5000,5000],'children':2,'count':30},
               {'adults':[5000],'children':1,'count':40},
               {'adults':[9000,5000],'children':3,'count':10},
               {'adults':[5000],'children':0,'count':20}],
 'goods':{
   'food':{'annual_units':200000,'labour_hours_per_unit':0.12,'price_u':12,'desired_units_per_household_month':110},
   'housing_services':{'annual_units':1200,'labour_hours_per_unit':4,'price_u':1600,'desired_units_per_household_month':1},
   'other_goods':{'annual_units':20000,'labour_hours_per_unit':1.5,'price_u':110,'desired_units_per_household_month':15}},
 'public_services_annual_hours_required':33000,
 'maintenance_annual_hours_required':13000,
 'household_spending_share':0.75,
 'public_fund_annual_u':4000000,
 'public_services_financial_cost_u':2500000,
 'maintenance_financial_cost_u':800000,
 'investment_financial_cost_u':500000,
 'worker_payroll_monthly_u':5000,
}

def evaluate(s):
    households=[]
    for group in s['households']:
        h=Household(tuple(group['adults']),group['children'])
        households += [h]*group['count']
    n=len(households)
    annual_income=sum(income(h) for h in households)*12
    annual_allowance=sum(child_allowance(h) for h in households)*12
    consumer_budget=annual_income*s['household_spending_share']
    annual_hours=s['hours_per_week']*s['weeks_per_year']
    total_hours=s['workers']*annual_hours
    public_hours=s['public_service_workers']*annual_hours
    maintenance_hours=s['capital_maintenance_workers']*annual_hours
    production_hours=sum(g['annual_units']*g['labour_hours_per_unit'] for g in s['goods'].values())
    required_hours=production_hours+s['public_services_annual_hours_required']+s['maintenance_annual_hours_required']
    # At fixed illustrative prices, how many units are desired and affordable?
    goods={}
    basket_cost=0
    for k,g in s['goods'].items():
        desired=n*12*g['desired_units_per_household_month']
        basket_cost += n*12*g['desired_units_per_household_month']*g['price_u']
        goods[k]={'desired_units':desired,'available_units':g['annual_units'],
                  'physical_gap_units':max(0,desired-g['annual_units']),
                  'supply_coverage':round(g['annual_units']/desired,4) if desired else None,
                  'notional_sales_u':g['annual_units']*g['price_u']}
    # Demand cannot be inferred from money alone; this is a budget diagnostic.
    annual_fund_need=sum(s[k] for k in ('public_services_financial_cost_u','maintenance_financial_cost_u','investment_financial_cost_u'))
    return {'scenario':s['name'],'households':n,'annual_income_u':annual_income,
       'annual_child_allowance_u':annual_allowance,'consumer_spending_budget_u':round(consumer_budget,2),
       'annual_desired_basket_u':basket_cost,'basket_affordability_ratio':round(consumer_budget/basket_cost,4),
       'total_labour_hours':total_hours,'required_labour_hours':round(required_hours,2),
       'labour_gap_hours':max(0,round(required_hours-total_hours,2)),
       'public_service_hours_shortfall':max(0,s['public_services_annual_hours_required']-public_hours),
       'maintenance_hours_shortfall':max(0,s['maintenance_annual_hours_required']-maintenance_hours),
       'public_fund_u':s['public_fund_annual_u'],'public_fund_need_u':annual_fund_need,
       'public_fund_shortfall_u':max(0,annual_fund_need-s['public_fund_annual_u']),
       'worker_base_payroll_u':s['workers']*s['worker_payroll_monthly_u']*12,
       'goods':goods,
       'physical_feasible':required_hours<=total_hours and all(v['physical_gap_units']==0 for v in goods.values()) and s['public_services_annual_hours_required']<=public_hours and s['maintenance_annual_hours_required']<=maintenance_hours,
       'financially_balanced_public_fund':s['public_fund_annual_u']>=annual_fund_need,
       'note':'Fixed-price stress test; affordability and gaps do not predict inflation or market clearing.'}

def scenarios():
    import copy
    a=copy.deepcopy(BASE)
    b=copy.deepcopy(BASE);b['name']='food_supply_shock';b['goods']['food']['annual_units']=95000
    c=copy.deepcopy(BASE);c['name']='shorter_work_year';c['weeks_per_year']=44
    d=copy.deepcopy(BASE);d['name']='housing_shortage';d['goods']['housing_services']['annual_units']=900
    e=copy.deepcopy(BASE);e['name']='public_fund_gap';e['public_fund_annual_u']=2500000
    return [a,b,c,d,e]

def main():
    root=Path(__file__).parent
    results=[evaluate(s) for s in scenarios()]
    (root/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    with (root/'results.csv').open('w',newline='') as f:
        fields=['scenario','households','annual_income_u','annual_child_allowance_u','consumer_spending_budget_u','annual_desired_basket_u','basket_affordability_ratio','total_labour_hours','required_labour_hours','labour_gap_hours','public_service_hours_shortfall','maintenance_hours_shortfall','public_fund_shortfall_u','physical_feasible','financially_balanced_public_fund']
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows([{k:r[k] for k in fields} for r in results])
    for r in results:print(r['scenario'], 'physical_feasible=',r['physical_feasible'],'fund_balanced=',r['financially_balanced_public_fund'])
if __name__=='__main__':main()
