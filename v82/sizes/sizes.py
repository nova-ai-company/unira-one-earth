"""UNIRA V8.2 (point 7) — sizes still missing: the essential energy allowance, crisis reserves, the pension formula.
python3 sizes.py  ->  outputs/sizes.json"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
sys.path.insert(0, str(U / "v62" / "src"))
from unira_v62 import jsonstat  # noqa: E402

ALLOWANCE_SHARE = 0.8      # proposal: the allowance covers 80% of today's average home energy per person (rule 40)
HOME_ENERGY_TARGET_KWH = 3000  # proposal: per person after renovation and heat pumps (SYNTHETIC; Scientific Council)
BASE = 5000


def wb_pop(iso, year):
    for x in json.loads((U / "v74" / "distribution" / "data" / "raw" / "wb_SP.POP.TOTL.json").read_text())[1]:
        if x["countryiso3code"] == iso and int(x["date"]) == year and x["value"]:
            return x["value"]


def main():
    d = jsonstat.load(HERE / "data" / "raw" / "nrg_bal_c_households.json")
    cells = {(c["geo"], c["siec"]): v for c, v, _ in jsonstat.iter_cells(d) if v is not None and c["time"] == "2024"}
    pop_fr, pop_eu = wb_pop("FRA", 2024) or wb_pop("FRA", 2023), None
    home_kwh = cells[("FR", "TOTAL")] * 1e6 / pop_fr
    elec_kwh = cells[("FR", "E7000")] * 1e6 / pop_fr
    gas_kwh = cells[("FR", "G3000")] * 1e6 / pop_fr
    allowance = ALLOWANCE_SHARE * home_kwh
    prices = json.loads((U / "v81" / "outputs" / "prices.json").read_text())
    elec_u_per_kwh = 0.25 * prices["products"]["CPA_D"]["u_per_euro_within_allowance"]  # 0.25 EUR/kWh illustrative
    cap = json.loads((U / "v79" / "outputs" / "cap_level.json").read_text())["results"]["cap_1.5y/accounts_time"]
    rush_months = 12 * cap["rush_extra_demand_pct_of_year"] / 100
    trade = json.loads((U / "v82" / "trade" / "outputs" / "trade.json").read_text())
    pension = {"base_u_month": BASE // 2, "per_year_worked_beyond_20_u": round(0.02 * BASE // 2), "max_u_month": round(BASE * 0.75),
               "note": "2,500 U (the needs-based retiree basket of v64) + 50 U per year worked beyond 20 years, up to 3,750 U; "
                       "plus the retirement account (up to 120,000 U paid out from retirement); housing guaranteed; "
                       "health and care free; case-by-case top-ups for disability or high care needs (rule 15)."}
    out = {"energy_allowance": {"france_home_energy_kwh_per_person_2024": round(home_kwh), "electricity_kwh": round(elec_kwh),
                                "gas_kwh": round(gas_kwh), "allowance_kwh_per_person_year_start": round(allowance, -1),
                                "allowance_kwh_per_person_month_start": round(allowance / 12),
                                "target_kwh_after_renovation": HOME_ENERGY_TARGET_KWH,
                                "cost_u_per_month_within_allowance_if_all_electric": round(allowance / 12 * elec_u_per_kwh, 1),
                                "note": "Home energy only (heating, hot water, cooking, appliances). Essential travel is covered by "
                                        "free public transport for needs and a mobility allowance set by the Scientific Council."},
           "reserves": {"spending_rush_extra_demand_months": round(rush_months, 1),
                        "essential_goods_stock_months": 3,
                        "foreign_currency_months_of_essential_imports": trade["reserve_months"],
                        "france_foreign_currency_reserve_meur": trade["reserve_meur"]},
           "pension": pension}
    (HERE / "outputs").mkdir(exist_ok=True)
    (HERE / "outputs" / "sizes.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
