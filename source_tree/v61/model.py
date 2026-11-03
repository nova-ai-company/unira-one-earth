"""UNIRA V6.1: transparent labour-hours sensitivity, not an economic forecast."""
import csv
from pathlib import Path

ROOT=Path(__file__).parent
# Official INSEE 2025: full-time employee effective annual hours, NOT all-worker mean.
FULL_TIME_HOURS=1656
EMPLOYED_TOTAL=30_500_000 # end 2025, includes part-time and self-employed
WEEKS=46 # hypothetical effective working weeks, not official estimate
TARGET_HOURS=30*WEEKS

def evaluate(current_hours, target_hours=TARGET_HOURS, workers=EMPLOYED_TOTAL):
    if min(current_hours,target_hours,workers)<=0: raise ValueError('Inputs must be positive')
    ratio=target_hours/current_hours
    return {'workers':workers,'assumed_current_annual_hours':current_hours,
            'target_annual_hours':target_hours,'hour_ratio':ratio,
            'hours_change_pct':100*(ratio-1),
            'required_productivity_increase_pct':100*(1/ratio-1),
            'additional_workers_at_unchanged_productivity':workers*(1/ratio-1)}

def main():
    rows=[{'scenario':label,**evaluate(hours)} for label,hours in
          [('all_workers_1400h_assumption',1400),('all_workers_1500h_assumption',1500),
           ('all_workers_1600h_assumption',1600),('full_time_reference_not_population',FULL_TIME_HOURS)]]
    with (ROOT/'scenarios.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    for r in rows: print(f"{r['scenario']}: {r['required_productivity_increase_pct']:.2f}% required hourly productivity gain if output held fixed")
if __name__=='__main__':main()
