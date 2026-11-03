"""Historical country series used to backtest needs forecasting (all frozen snapshots already in the repo).

    population     UN WPP 2024, total population 1 July, 1950-2023 (estimates only, no projections)
    energy_pc      Our World in Data energy dataset, primary energy per person (kWh), 1965-2024
    kcal_pc        FAO food balance via Our World in Data, daily supply per person, 1961-2022
    doctors_10k    WHO GHO HWF_0001, medical doctors per 10,000, 1990-2024
    nurses_10k     WHO GHO HWF_0006, nursing and midwifery personnel per 10,000, 1990-2024
Returns {series: {iso3: {year: value}}}, countries only (aggregates removed), positive values only."""
import csv
import gzip
import json
from pathlib import Path

U = Path(__file__).resolve().parents[2]
R65 = U / "v65" / "data" / "raw"
R66 = U / "v66" / "data" / "raw"
LAST_ESTIMATE_YEAR = 2023  # WPP 2024: later years are projections, not observations


def _put(out, iso, year, val):
    if iso and len(iso) == 3 and not iso.startswith("OWID") and val is not None and val > 0:
        out.setdefault(iso, {})[int(year)] = float(val)


def population():
    out = {}
    with gzip.open(R66 / "un_WPP2024_Demographic_Indicators_Medium.csv.gz", "rt", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["LocTypeName"] == "Country/Area" and r["Variant"] == "Medium" and int(r["Time"]) <= LAST_ESTIMATE_YEAR \
                    and r["TPopulation1July"]:
                _put(out, r["ISO3_code"], r["Time"], float(r["TPopulation1July"]) * 1000)
    return out


def energy_pc():
    out = {}
    with open(R65 / "owid_energy_data.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["energy_per_capita"]:
                _put(out, r["iso_code"], r["year"], float(r["energy_per_capita"]))
    return out


def kcal_pc():
    out = {}
    with open(R65 / "owid_daily_per_capita_caloric_supply.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["daily_calories"] and int(r["year"]) >= 1961:  # FAO statistics start in 1961
                _put(out, r["code"], r["year"], float(r["daily_calories"]))
    return out


def _who(code):
    out = {}
    for x in json.loads((R65 / f"who_{code}.json").read_text())["value"]:
        if x["LOCATION_TYPE"] == "COUNTRY" and x["PERIOD_CODE"].isdigit():
            _put(out, x["LOCATION_CODE"], x["PERIOD_CODE"], x["VALUE_NUMERIC"])
    return out


def income_groups():
    meta = json.loads((R65 / "wb_country_meta.json").read_text())[1]
    return {c["id"]: c["incomeLevel"]["id"] for c in meta if c["incomeLevel"]["id"] in ("LIC", "LMC", "UMC", "HIC")}


def load_all():
    return {"population": population(), "energy_pc": energy_pc(), "kcal_pc": kcal_pc(),
            "doctors_10k": _who("HWF_0001"), "nurses_10k": _who("HWF_0006")}
