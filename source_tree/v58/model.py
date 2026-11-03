"""UNIRA V5.8: synthetic multi-period physical/monetary stress model.
Not a calibrated forecast or complete stock-flow-consistent model.
Run: python model.py
"""
from dataclasses import dataclass, asdict
import csv, json
from pathlib import Path

@dataclass(frozen=True)
class Params:
    years:int=20
    workers:int=100
    households:int=100
    hours_per_worker:int=1500
    hours_per_unit:float=100
    capital_initial:float=100
    capital_productivity:float=1.0
    depreciation:float=.04
    investment_units:float=4
    investment_hours_per_unit:float=150
    initial_inventory:float=0
    need_per_household:float=1.0
    initial_price:float=60000
    base_monthly_U:float=5000
    public_cost_U:float=1_000_000
    firm_surplus_rate:float=.20
    tax_rate:float=.10
    annual_price_adjustment:float=.20
    shortage_price_sensitivity:float=.35
    population_growth:float=0
    labor_shock_year:int=-1
    labor_shock_fraction:float=0
    supply_shock_year:int=-1
    supply_shock_fraction:float=0
    borrowing_limit_U:float=20_000_000

def run(p:Params):
    if p.years<1 or p.workers<0 or p.households<0 or p.hours_per_unit<=0 or p.initial_price<=0: raise ValueError('invalid parameters')
    if not (0<=p.depreciation<=1 and 0<=p.firm_surplus_rate<=1 and 0<=p.tax_rate<=1): raise ValueError('invalid rates')
    if not (0<=p.labor_shock_fraction<=1 and 0<=p.supply_shock_fraction<=1): raise ValueError('invalid shock')
    capital=p.capital_initial; inventory=p.initial_inventory; price=float(p.initial_price)
    household_cash=0.; firm_cash=0.; gov_cash=0.; debt=0.; records=[]
    for year in range(1,p.years+1):
        hh=p.households*(1+p.population_growth)**(year-1)
        workers=p.workers
        available_hours=workers*p.hours_per_worker*(1-p.labor_shock_fraction if year==p.labor_shock_year else 1)
        invest=min(p.investment_units,available_hours/p.investment_hours_per_unit)
        investment_hours=invest*p.investment_hours_per_unit
        max_output=min(capital*p.capital_productivity,(available_hours-investment_hours)/p.hours_per_unit)
        output=max_output*(1-p.supply_shock_fraction if year==p.supply_shock_year else 1)
        opening_stock=inventory
        inventory+=output
        demand=hh*p.need_per_household
        delivered=min(demand,inventory)
        inventory-=delivered
        shortage=demand-delivered
        wages=workers*p.base_monthly_U*12
        # Simplified: wages financed by firm credit when sales receipts are insufficient.
        firm_cash+=wages*-1
        household_cash+=wages
        sales=min(household_cash,delivered*price)
        household_cash-=sales; firm_cash+=sales
        # Cash taxes, not hypothetical profit taxes; public surplus after a protected firm reserve.
        tax=max(0,firm_cash)*p.tax_rate
        firm_cash-=tax; gov_cash+=tax
        surplus=max(0,firm_cash)*p.firm_surplus_rate
        firm_cash-=surplus; gov_cash+=surplus
        gov_cash-=p.public_cost_U; household_cash+=p.public_cost_U  # public-service providers represented within household sector
        # Credit injection finances negative firm/public balances, not real resources.
        new_credit=max(0,-firm_cash)+max(0,-gov_cash)
        firm_credit=max(0,-firm_cash); gov_credit=max(0,-gov_cash)
        firm_cash+=firm_credit; gov_cash+=gov_credit
        debt+=new_credit
        credit_limit_breached=debt>p.borrowing_limit_U
        capital=max(0,capital*(1-p.depreciation)+invest)
        target_price_change=p.shortage_price_sensitivity*(shortage/demand if demand else 0)
        price*=1+p.annual_price_adjustment*target_price_change
        # Deposits = household + firm + government; credit is explicit counterpart.
        deposits=household_cash+firm_cash+gov_cash
        records.append(dict(year=year,households=round(hh,4),opening_inventory=round(opening_stock,4),output=round(output,4),delivered=round(delivered,4),shortage=round(shortage,4),closing_inventory=round(inventory,4),capital=round(capital,4),hours_available=round(available_hours,2),hours_used=round(investment_hours+max_output*p.hours_per_unit,2),wages_U=round(wages,2),sales_U=round(sales,2),public_cost_U=p.public_cost_U,new_credit_U=round(new_credit,2),total_debt_U=round(debt,2),deposits_U=round(deposits,2),household_cash_U=round(household_cash,2),price_U=round(price,2),credit_limit_breached=credit_limit_breached))
        assert inventory>=-1e-8 and delivered<=demand+1e-8 and delivered<=opening_stock+output+1e-8
        assert investment_hours+max_output*p.hours_per_unit<=available_hours+1e-7
        assert abs(deposits-debt)<1e-6, 'deposit/loan identity violated'
    return records

SCENARIOS={
 'baseline':Params(),
 'food_supply_shock':Params(supply_shock_year=5,supply_shock_fraction=.70),
 'labor_shock':Params(labor_shock_year=5,labor_shock_fraction=.70),
 'population_growth':Params(population_growth=.025),
 'restricted_credit':Params(borrowing_limit_U=5_000_000),
 'lower_investment':Params(investment_units=0),
}

def main():
    dest=Path(__file__).resolve().parent
    allrows=[]; summary=[]
    for name,p in SCENARIOS.items():
        rows=run(p)
        allrows.extend(dict(scenario=name,**r) for r in rows)
        summary.append(dict(scenario=name,shortage_years=sum(r['shortage']>0 for r in rows),total_shortage=round(sum(r['shortage'] for r in rows),3),final_debt_U=rows[-1]['total_debt_U'],final_capital=rows[-1]['capital'],max_price_U=max(r['price_U'] for r in rows),credit_limit_breached=any(r['credit_limit_breached'] for r in rows)))
    with (dest/'annual_results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=allrows[0].keys());w.writeheader();w.writerows(allrows)
    (dest/'summary.json').write_text(json.dumps(summary,indent=2))
    (dest/'assumptions.json').write_text(json.dumps({k:asdict(v) for k,v in SCENARIOS.items()},indent=2))
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
