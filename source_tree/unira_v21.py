"""UNIRA V2.1: transparent exploratory calculations. Python 3 standard library only."""
import csv, json
from pathlib import Path
OUT=Path(__file__).parent
EMPLOYED_2025=3_544_800_000  # ILO WESO 2024 projection for 2025; not an observed census
UNIRA_WORKERS=4_350_000_000  # proposed, unvalidated
HOURS_UNIRA=30
HOURS_BASELINE=43  # illustrative assumption, not ILO measured global hours
FOOD_SUPPLY_LOWER_BOUND=3000 # FAO 2023 strictly above this
FOOD_TARGET=2500 # illustrative dietary-energy planning target, not clinical recommendation

def labor(hours_baseline=HOURS_BASELINE, workers=UNIRA_WORKERS):
    baseline=EMPLOYED_2025*hours_baseline
    unira=workers*HOURS_UNIRA
    return {'baseline_weekly_hours':baseline,'unira_weekly_hours':unira,'hours_change_pct':round((unira/baseline-1)*100,2),'productivity_multiplier_for_equal_aggregate_output':round(baseline/unira,4)}

def food(supply=FOOD_SUPPLY_LOWER_BOUND,target=FOOD_TARGET,shock=0):
    available=supply*(1-shock)
    return {'daily_kcal_supply_floor':available,'illustrative_target':target,'supply_target_ratio_floor':round(available/target,3),'caveat':'FAO >3000 kcal 2023: 3000 is a conservative floor, not exact observed supply; food balances are not consumed calories.'}

rows=[]
for name,workers,hours,shock in [('base',4.35e9,43,0),('participation_low',3.8e9,43,0),('participation_high',4.7e9,43,0),('shorter_current_hours',4.35e9,38,0),('food_shock_20pct',4.35e9,43,.2)]:
    l=labor(hours,workers); f=food(shock=shock)
    rows.append({'scenario':name,'unira_workers_billion':workers/1e9,'baseline_hours_assumed':hours,'food_supply_shock':shock,**l,'food_supply_target_ratio_floor':f['supply_target_ratio_floor']})
with (OUT/'UNIRA_V21_scenarios.csv').open('w',newline='') as fp:
    w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'UNIRA_V21_results.json').write_text(json.dumps({'labor_scenarios':rows,'food':food(),'sources':{'ilo':'https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@dgreports/@inst/documents/publication/wcms_908142.pdf','fao':'https://www.fao.org/statistics/highlights-archive/highlights-detail/food-balance-sheets-2010-2023/','iea':'https://www.iea.org/reports/global-energy-review-2025/electricity'}},indent=2))
if __name__=='__main__':
 for row in rows: print(row['scenario'],row['hours_change_pct'],row['productivity_multiplier_for_equal_aggregate_output'])
