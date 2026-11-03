# UNIRA V8.2 — point 3: investment, machines and infrastructure

**The problem:** the model counted hours of work, but not how factories, machines, networks and buildings are maintained, replaced and expanded, or who decides.

**France, measured (Eurostat 2024):**

| item | value |
|---|---|
| investment (GFCF) | 22.2% of GDP |
| depreciation (GDP − NDP) | 18.4% of GDP, so **83% of investment only replaces what wears out** |
| net fixed assets | 3.4 years of GDP (59% dwellings) |
| investment goods, in hours (input–output 2022) | **17.2% of all hours worked**, of which about 14.2 points are maintenance and 3.0 points are net new capacity |

**Model** (`model.py`): the working week over 30 years, if the hours budget is spent in three priorities:
1. maintenance first;
2. needs for a transition period;
3. hours-saving machines, which save hours over their life of 20 years.

Payback is the number of years for a machine to return the hours spent building it. Consumption needs are held constant (no growth beyond needs).

| hours-saving investment (share of hours) | payback | week after 10 yrs | after 20 yrs |
|---|---|---|---|
| none | – | 29.1 h | 29.1 h |
| 3% (today's net investment) | 15 yrs | 29.4 | 28.8 |
| 3% | 10 yrs | 29.1 | **28.2** |
| 3% | 6 yrs | 28.5 | **27.0** |
| 5% | 6 yrs | 28.1 | **25.6** |
| 3%, plus transition needs of 3% for 15 years | 10 yrs | 30.0 (31 h at the start) | 28.2 |

## Findings

1. **Maintenance is most of investment.** About 14% of all working hours go to keeping existing buildings and machines in shape. UNIRA must protect this first. Planned economies that ran down their capital stock to show output paid for it later.
2. **Hours-saving machines shorten the week** (rule 16). Today's net investment, directed at machines that repay their hours in 6–10 years, brings the week from 30 to about 27–28 hours within 20 years.
3. **The gain levels off after one equipment lifetime.** Further shortening needs technology that keeps improving, which is the reason for the research budget (Article 3d).
4. **The transition costs hours.** Building for unmet needs (energy, renovation, care) at 3–5% of hours for 15 years would push the week to 31–31.5 hours at first. To keep 30 hours from year 1, those hours must come from the extra workers of full employment and from market work UNIRA no longer needs (V6.3).

## Rule supported (proposed Article 16a)

1. Maintenance first: never invest less than measured wear.
2. Then needs (Article 10a).
3. Then hours-saving projects ranked by published hours payback, within ecological limits.
4. Savings go to shorter hours.
5. The investment plan is published in the Register, with a regional share for local priorities.

## Limitations

- France only. Value shares are used as hours shares for depreciation.
- Synthetic payback and equipment life.
- Investment needs of the energy transition are not quantified for France here (the world plan is in v67).
- Constant consumption: no growth of wants beyond needs.
