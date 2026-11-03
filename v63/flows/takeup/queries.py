"""Eurostat dissemination-API queries for the flow snapshots (verified 2026-11-03).

Dataset ids and dimension codes were checked by querying the API (see README.md):
  lfsi_long_a   Labour market transitions - annual data. YEAR-ON-YEAR flows (same quarter
                of two consecutive years, annual average), ILO status, ages 15-74.
                dims: unit{THS_PER,PC_EMP,PC_UNE,PC_INAC} wstatus{UNE_EMP,...} sex geo time
  lfsi_long_q   Labour market transitions - quarterly data. Quarter-on-quarter flows,
                published under the FINAL quarter. dims: unit s_adj{NSA,SA} wstatus sex geo time
  lfsi_long_e06 Outside the labour force -> employment by labour market attachment
                (experimental; annual averages of QUARTERLY transition probabilities, %).
                wstatus{TOTAL,SEEK_NAVL,NSEEK_AVL,OTH} age{Y15-24,Y15-74,Y25-54,Y55-74}
  lfsi_long_e01 Unemployment -> employment by duration of unemployment (experimental,
                quarterly probabilities). duration{TOTAL,Y_LT1,Y_GE1,Y_GE2}
  lfsi_long_e08 Part-time -> full-time (experimental, quarterly probabilities). age{Y25-64,...}
  ilc_lvhl30    EU-SILC longitudinal: labour transitions by employment status (year t-1 ->
                year t, % of status in t-1). wstatusp = previous, wstatus = current status.
  lfsi_sla_a    Labour market slack (stocks used to weight the two T2 sub-pools).
"""
from ._v62 import fetch

GEOS = list(fetch.GEOS)  # EU27 + IS/NO/CH + EU27_2020 aggregate (same set as V6.2)
YEARS = ["2023", "2024"]
QUARTERS = [f"{y}-Q{q}" for y in YEARS for q in (1, 2, 3, 4)]

QUERIES = [
    ("flows_annual", "lfsi_long_a",
     {"geo": GEOS, "time": YEARS, "sex": "T",
      "unit": ["THS_PER", "PC_EMP", "PC_UNE", "PC_INAC"]}),
    ("flows_quarterly", "lfsi_long_q",
     {"geo": GEOS, "time": QUARTERS, "sex": "T", "s_adj": "NSA", "unit": "THS_PER"}),
    ("flows_inactive_attachment", "lfsi_long_e06",
     {"geo": GEOS, "time": YEARS, "sex": "T", "age": ["Y15-74", "Y25-54"]}),
    ("flows_unemp_duration", "lfsi_long_e01",
     {"geo": GEOS, "time": YEARS, "sex": "T", "age": ["Y15-74", "Y25-54"]}),
    ("flows_pt_to_ft", "lfsi_long_e08",
     {"geo": GEOS, "time": YEARS, "sex": "T", "age": "Y25-64"}),
    ("silc_labour_transitions", "ilc_lvhl30",
     {"geo": GEOS, "time": YEARS, "sex": "T"}),
    ("lfs_slack_stocks", "lfsi_sla_a",
     {"geo": GEOS, "time": YEARS, "sex": "T", "age": "Y15-74", "unit": "THS_PER",
      "wstatus": ["UNE", "SEEK_NAVL", "NSEEK_AVL", "UEMP_PT"]}),
]
