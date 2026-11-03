"""UNIRA V5.2: evidence-anchored housing-need indicators and transparent sensitivity.
Run: python model.py; test: python -m unittest discover -s . -p 'test_*.py'
"""
import csv
from pathlib import Path
BASE=Path(__file__).resolve().parent
DATA=[
 {'place':'Paris municipality','year':'2023','measure':'moderate_overcrowding_pct','value':28.2,'geography':'Paris commune','source':'https://www.insee.fr/fr/statistiques/2011101?geo=COM-75056','caveat':'INSEE occupancy index, not UK bedroom standard'},
 {'place':'Paris municipality','year':'2023','measure':'severe_overcrowding_pct','value':2.6,'geography':'Paris commune','source':'https://www.insee.fr/fr/statistiques/2011101?geo=COM-75056','caveat':'INSEE occupancy index, not UK bedroom standard'},
 {'place':'Paris urban unit','year':'2022','measure':'moderate_overcrowding_pct','value':19.8,'geography':'Paris unité urbaine 2020','source':'https://www.insee.fr/fr/statistiques/8581193?geo=UU2020-00851','caveat':'INSEE occupancy index, different geography and year'},
 {'place':'Paris urban unit','year':'2022','measure':'severe_overcrowding_pct','value':2.9,'geography':'Paris unité urbaine 2020','source':'https://www.insee.fr/fr/statistiques/8581193?geo=UU2020-00851','caveat':'INSEE occupancy index, different geography and year'},
 {'place':'Greater London','year':'2023-24','measure':'overcrowding_pct','value':6.7,'geography':'Greater London','source':'https://www.london.gov.uk/sites/default/files/2026-01/Housing%20in%20London%202025%20report%20%28002%29.pdf','caveat':'UK bedroom standard, three-year rolling survey estimate; likely underestimated'},
 {'place':'England','year':'2024-25','measure':'overcrowding_pct','value':3.0,'geography':'England','source':'https://www.gov.uk/government/statistics/chapters-for-english-housing-survey-2024-to-2025-headline-findings-on-housing-quality-and-energy-efficiency/chapter-1-housing-quality','caveat':'National comparator only; three-year rolling estimate'},
]
CITIES=['Paris','London','New York','Tokyo','Cairo']

def hypothetical_screening(affected_households, voluntarily_rehoused, adequately_upgraded, new_suitable_homes):
    assert all(isinstance(x,int) and x>=0 for x in (affected_households,voluntarily_rehoused,adequately_upgraded,new_suitable_homes))
    # Improvements cannot count beyond households in need; avoid double counting.
    reused=min(affected_households,voluntarily_rehoused)
    upgraded=min(affected_households-reused,adequately_upgraded)
    newly=min(affected_households-reused-upgraded,new_suitable_homes)
    return {'need':affected_households,'voluntary_rehousing':reused,'upgraded_in_place':upgraded,'new_suitable_homes':newly,'remaining_need':affected_households-reused-upgraded-newly}

def write():
    with (BASE/'verified_indicators.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=DATA[0].keys());w.writeheader();w.writerows(DATA)
    scenarios=[('low',1000,50,100,100),('middle',1000,150,250,250),('high',1000,250,350,400)]
    with (BASE/'illustrative_scenarios.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['scenario','need','voluntary_rehousing','upgraded_in_place','new_suitable_homes','remaining_need']);w.writeheader()
        for name,*args in scenarios:w.writerow({'scenario':name,**hypothetical_screening(*args)})
if __name__=='__main__':write();print('Wrote verified_indicators.csv and illustrative_scenarios.csv')
