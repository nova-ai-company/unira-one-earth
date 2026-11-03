"""UNIRA V6.0: anchored France 2023 electricity stress test (not full economy)."""
import csv
from pathlib import Path

# Source: RTE 2023 production 494.7 TWh; weather-adjusted demand 445.7 TWh.
# These series are NOT a matched physical electricity balance: deliberately
# never subtract them to infer surplus or available electricity.
BASE_PRODUCTION_TWH = 494.7
BASE_WEATHER_ADJUSTED_CONSUMPTION_TWH = 445.7
BASE_FOSSIL_GENERATION_TWH = 32.6


def scenario(demand_growth=0, generation_loss=0, demand_reduction=0):
    """Independent *index* comparison, NOT grid adequacy or supply balance."""
    assert demand_growth > -1 and 0 <= generation_loss <= 1 and 0 <= demand_reduction <= 1
    production_index = (1-generation_loss)*100
    demand_index = (1+demand_growth)*(1-demand_reduction)*100
    return {"production_index": round(production_index, 3),
            "demand_index": round(demand_index, 3),
            "index_gap": round(production_index-demand_index, 3)}


def run(path=None):
    scenarios = {
        'reference': (0,0,0),
        '10pct_demand_growth': (.1,0,0),
        '10pct_generation_loss': (0,.1,0),
        'demand_growth_and_efficiency': (.1,0,.1),
        'combined_shock': (.1,.1,0),
    }
    rows = []
    for name, args in scenarios.items():
        rows.append({'scenario':name, **scenario(*args)})
    if path:
        with open(path,'w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    return rows

if __name__ == '__main__':
    for row in run(Path(__file__).with_name('scenario_results.csv')): print(row)
