"""UNIRA V5.7 synthetic double-entry sector balance sheets and physical feasibility.
Amounts U; quantities physical units. No empirical calibration or price stability model.
"""
from dataclasses import dataclass, field
import json
from pathlib import Path

@dataclass
class Model:
    deposits: dict = field(default_factory=lambda:{x:0 for x in ('households','firms','government','investment')})
    loans: dict = field(default_factory=lambda:{x:0 for x in ('firms','government')})
    bank_reserves: int = 0
    bank_advance: int = 0
    inventory_units: int = 0
    capital_units: int = 0
    inventory_cost_U: int = 0
    capital_cost_U: int = 0
    physical_output_units: int = 0
    transactions: list = field(default_factory=list)

    def transfer(self, src, dst, amount, why):
        if amount < 0 or self.deposits[src] < amount: raise ValueError('insufficient funds or negative transfer')
        self.deposits[src]-=amount; self.deposits[dst]+=amount
        self.transactions.append({'kind':'transfer','from':src,'to':dst,'U':amount,'reason':why})
        self.audit()

    def lend(self, borrower, amount):
        if borrower not in self.loans or amount<0: raise ValueError('invalid loan')
        self.loans[borrower]+=amount; self.deposits[borrower]+=amount
        self.transactions.append({'kind':'bank_loan','to':borrower,'U':amount})
        self.audit()

    def repay(self, borrower, amount):
        if amount<0 or self.loans[borrower]<amount or self.deposits[borrower]<amount: raise ValueError('invalid repayment')
        self.loans[borrower]-=amount; self.deposits[borrower]-=amount
        self.transactions.append({'kind':'loan_repayment','from':borrower,'U':amount})
        self.audit()

    def reserve_advance(self, amount):
        if amount<0: raise ValueError('negative advance')
        self.bank_reserves+=amount; self.bank_advance+=amount
        self.transactions.append({'kind':'authority_advance','U':amount})
        self.audit()

    def produce(self, units, hours, hours_available, cost_U):
        if units<0 or hours<0 or hours>hours_available or cost_U<0: raise ValueError('production infeasible')
        # Wages and input costs are already funded as deposits; inventory records capitalized cost.
        self.inventory_units+=units; self.inventory_cost_U+=cost_U; self.physical_output_units+=units
        self.transactions.append({'kind':'production','units':units,'hours':hours,'inventory_cost_U':cost_U})
        self.audit()

    def sell(self, buyer, units, price_per_unit):
        if units<0 or units>self.inventory_units or price_per_unit<0: raise ValueError('inventory unavailable')
        amount=units*price_per_unit
        if self.deposits[buyer]<amount: raise ValueError('buyer liquidity insufficient')
        old_units=self.inventory_units
        consumed_cost=self.inventory_cost_U*units//old_units if old_units else 0
        self.transfer(buyer,'firms',amount,'goods purchase')
        self.inventory_units-=units; self.inventory_cost_U-=consumed_cost
        self.transactions.append({'kind':'inventory_delivery','units':units,'cost_U':consumed_cost})
        self.audit()

    def invest(self, amount, capital_units):
        if amount<0 or capital_units<0 or self.deposits['investment']<amount: raise ValueError('investment infeasible')
        self.transfer('investment','firms',amount,'capital investment funding')
        self.capital_units+=capital_units; self.capital_cost_U+=amount
        self.audit()

    def depreciate(self, amount):
        if amount<0 or amount>self.capital_cost_U: raise ValueError('invalid depreciation')
        self.capital_cost_U-=amount
        self.transactions.append({'kind':'depreciation','U':amount})
        self.audit()

    def sheets(self):
        deposits=sum(self.deposits.values())
        bank_assets=self.bank_reserves+sum(self.loans.values())
        bank_liabilities=deposits+self.bank_advance
        bank_equity=bank_assets-bank_liabilities
        authority_assets=self.bank_advance
        authority_liabilities=self.bank_reserves
        firm_equity=self.deposits['firms']+self.inventory_cost_U+self.capital_cost_U-self.loans['firms']
        gov_equity=self.deposits['government']-self.loans['government']
        return {'bank':{'assets_U':bank_assets,'liabilities_U':bank_liabilities,'equity_U':bank_equity},
                'monetary_authority':{'assets_U':authority_assets,'liabilities_U':authority_liabilities,'equity_U':authority_assets-authority_liabilities},
                'households':{'assets_U':self.deposits['households'],'liabilities_U':0,'equity_U':self.deposits['households']},
                'firms':{'assets_U':self.deposits['firms']+self.inventory_cost_U+self.capital_cost_U,'liabilities_U':self.loans['firms'],'equity_U':firm_equity},
                'government':{'assets_U':self.deposits['government'],'liabilities_U':self.loans['government'],'equity_U':gov_equity},
                'investment':{'assets_U':self.deposits['investment'],'liabilities_U':0,'equity_U':self.deposits['investment']}}

    def audit(self):
        s=self.sheets()
        assert all(v>=0 for v in self.deposits.values())
        assert all(x['assets_U']==x['liabilities_U']+x['equity_U'] for x in s.values())
        assert s['bank']['equity_U']==0 and s['monetary_authority']['equity_U']==0
        assert self.inventory_units>=0 and self.capital_cost_U>=0
        return True

def simulate(food_supply=110, food_demand=100, hours_available=15000, public_services_U=160000, government_credit_U=200000, base_wages_U=600000, capital_spend_U=50000):
    e=Model(); e.reserve_advance(100000); e.lend('firms',900000); e.lend('government',government_credit_U)
    e.transfer('firms','households',base_wages_U,'10 employees x 5000 U x 12 months')
    e.transfer('firms','investment',80000,'earmarked investment reserve')
    e.transfer('firms','government',140000,'hypothetical distributable surplus')
    labour_needed=12000
    feasible_hours=min(labour_needed,hours_available)
    production=min(food_supply, int(food_supply*feasible_hours/labour_needed))
    e.produce(production,feasible_hours,hours_available,200000)
    e.sell('households',min(food_demand,production),2000)
    e.invest(capital_spend_U,5)
    e.depreciate(5000)
    paid=min(public_services_U,e.deposits['government'])
    e.transfer('government','firms',paid,'essential services procurement')
    sheets=e.sheets()
    return {'parameters':{'food_supply':food_supply,'food_demand':food_demand,'hours_available':hours_available,'public_services_U':public_services_U,'government_credit_U':government_credit_U},
      'physical':{'food_produced':production,'food_delivered':min(food_demand,production),'food_unmet':max(0,food_demand-production),'labour_shortfall_hours':max(0,labour_needed-hours_available),'inventory_left_units':e.inventory_units,'capital_units':e.capital_units},
      'finance':{'government_unpaid_U':public_services_U-paid,'bank_loans_U':sum(e.loans.values()),'deposits_U':sum(e.deposits.values()),'capital_book_value_U':e.capital_cost_U,'inventory_book_value_U':e.inventory_cost_U,'balance_sheets':sheets},
      'audited':e.audit(),'events':e.transactions,'status':'synthetic accounting demonstration; incomplete macroeconomic model'}

if __name__=='__main__':
    cases={'baseline':{},'food_shock':{'food_supply':70},'labour_shock':{'hours_available':9000},'public_shortfall':{'public_services_U':450000,'government_credit_U':0},'higher_credit':{'government_credit_U':500000}}
    results={k:simulate(**v) for k,v in cases.items()}
    Path(__file__).with_name('results.json').write_text(json.dumps(results,indent=2))
    for k,v in results.items(): print(k,v['physical'], 'government_unpaid_U=',v['finance']['government_unpaid_U'])
