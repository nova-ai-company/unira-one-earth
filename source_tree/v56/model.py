"""UNIRA V5.6 synthetic stock-flow transaction ledger, standard library only.
Each transfer conserves deposits; issuance/redemption explicitly changes deposits and
monetary-authority equity. Sector accounts are aggregated, not individual agents.
"""
from dataclasses import dataclass, field
import json, csv
from pathlib import Path

SECTORS=('households','firms','public_fund','investment_fund','monetary_authority')
@dataclass
class Economy:
    deposits: dict=field(default_factory=lambda:{s:0 for s in SECTORS})
    events: list=field(default_factory=list)
    issued: int=0
    def transfer(self, source, target, amount, reason):
        assert source in SECTORS and target in SECTORS and source!=target
        assert isinstance(amount,int) and amount>=0
        if self.deposits[source]<amount: raise ValueError(f'insufficient funds: {source}: {reason}')
        self.deposits[source]-=amount; self.deposits[target]+=amount
        self.events.append(dict(source=source,target=target,amount=amount,reason=reason))
        self.check()
    def issue(self, target, amount, reason):
        assert target!='monetary_authority' and isinstance(amount,int) and amount>=0
        self.deposits[target]+=amount; self.issued+=amount
        self.events.append(dict(source='ISSUANCE',target=target,amount=amount,reason=reason))
        self.check()
    def check(self):
        assert all(v>=0 for v in self.deposits.values())
        assert sum(self.deposits.values())==self.issued
        return True
    def flow_balance(self):
        return {s:sum(e['amount'] for e in self.events if e['target']==s)-sum(e['amount'] for e in self.events if e['source']==s) for s in SECTORS}

def simulate(food_supply=110, food_demand=100, public_cost=500_000, initial_issue=1_000_000, work_hours=1500, shortage_rule='report'):
    e=Economy(); e.issue('firms',initial_issue,'initial working capital (explicit monetary creation)')
    e.transfer('firms','households',600_000,'annual wages: 10 workers x 5,000 U x 12 months')
    e.transfer('firms','public_fund',140_000,'distributable operating surplus')
    e.transfer('firms','investment_fund',80_000,'investment reserve contribution')
    e.transfer('households','firms',350_000,'household purchases of goods')
    e.transfer('households','public_fund',60_000,'illustrative household contribution')
    e.transfer('investment_fund','firms',40_000,'capital purchases')
    # public services purchases limited to available cash: report unpaid obligations
    due=public_cost
    paid=min(e.deposits['public_fund'],due)
    e.transfer('public_fund','firms',paid,'public service procurement')
    # Physical resources are independently assessed; no automatic creation via U.
    actual_food=min(food_supply,food_demand)
    unmet_food=food_demand-actual_food
    labour_available=10*work_hours
    labour_required=12_000
    r={'parameters':dict(food_supply=food_supply,food_demand=food_demand,public_cost=public_cost,initial_issue=initial_issue,work_hours=work_hours,shortage_rule=shortage_rule),
       'closing_deposits_U':e.deposits,'total_issued_U':e.issued,'sector_net_flows_U':e.flow_balance(),
       'public_unpaid_U':due-paid,'food_unmet_units':unmet_food,'food_delivered_units':actual_food,
       'labour_shortfall_hours':max(0,labour_required-labour_available),
       'ledger_balances':e.check(),'transactions':e.events,
       'model_status':'synthetic accounting demonstrator; not full SFC macro model'}
    return r

def main():
    scenarios={'baseline':{},'food_shortage':{'food_supply':70},'public_fund_shortage':{'public_cost':500_000},
               'public_cost_low':{'public_cost':150_000},'labour_shock':{'work_hours':1000},'money_creation':{'initial_issue':1_500_000}}
    results={name:simulate(**args) for name,args in scenarios.items()}
    folder=Path(__file__).resolve().parent
    (folder/'results.json').write_text(json.dumps(results,indent=2))
    with (folder/'results.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['scenario','issued_U','public_unpaid_U','food_unmet_units','labour_shortfall_hours','deposits_sum_U'])
        for name,r in results.items(): writer.writerow([name,r['total_issued_U'],r['public_unpaid_U'],r['food_unmet_units'],r['labour_shortfall_hours'],sum(r['closing_deposits_U'].values())])
    print(json.dumps({n:{k:r[k] for k in ('public_unpaid_U','food_unmet_units','labour_shortfall_hours','ledger_balances')} for n,r in results.items()},indent=2))
if __name__=='__main__':main()
