"""Download raw world-indicator snapshots for V6.5 and record provenance.

Run once (network required):  python3 -I fetch_world.py   [stem ...]
Every later step (build.py) reads ONLY the frozen files in raw/, so results are
reproducible offline and auditable against raw/raw_manifest.csv
(columns: file, source, url, retrieved_at_utc, sha256, bytes, license).

Downloads are untrusted data: they are written as bytes and never executed.
Stdlib only (Python 3.14).
"""
import csv
import hashlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 UNIRA-V6.5-research")
FIELDS = ["file", "source", "url", "retrieved_at_utc", "sha256", "bytes", "license"]

LIC_WB = "World Bank Open Data, CC BY 4.0"
LIC_WHO = "WHO GHO data, CC BY-NC-SA 3.0 IGO (WHO data policy)"
LIC_FAO = "FAOSTAT, CC BY 4.0 (FAO Statistical Database Terms of Use)"
LIC_ILO = "ILOSTAT, CC BY 4.0"
LIC_OWID = "Our World in Data, CC BY 4.0 (underlying Energy Institute/Ember/EIA terms apply)"
LIC_UN = "United Nations Statistics Division, UN terms of use"


def wb(indicator, dates):
    return ("https://api.worldbank.org/v2/country/all/indicator/"
            f"{indicator}?format=json&per_page=20000&date={dates}")


def who(code):
    q = urllib.parse.urlencode({
        "$filter": f"INDICATOR_CODE eq '{code}'",
        "$select": "INDICATOR_CODE,PERIOD_CODE,LOCATION_CODE,LOCATION_TYPE,"
                   "VALUE_NUMERIC,VALUE_STRING,DIMENSION_1,DIMENSION_MEMBER_1"}, safe="$,'")
    return "https://xmart-api-public.who.int/GHO/FACT?" + q


def ilo(ind, extra):
    q = urllib.parse.urlencode({"id": ind, **extra, "format": ".csv"})
    return "https://rplumber.ilo.org/data/indicator/?" + q


# (file name, source label, url, license)
QUERIES = [
    ("wb_country_meta.json", "World Bank API v2 country list (aggregate flags)",
     "https://api.worldbank.org/v2/country?format=json&per_page=400", LIC_WB),
    ("wb_SP.POP.TOTL.json", "World Bank WDI SP.POP.TOTL", wb("SP.POP.TOTL", "2022:2024"), LIC_WB),
    ("wb_SP.POP.1564.TO.ZS.json", "World Bank WDI SP.POP.1564.TO.ZS",
     wb("SP.POP.1564.TO.ZS", "2022:2024"), LIC_WB),
    ("wb_SP.POP.65UP.TO.ZS.json", "World Bank WDI SP.POP.65UP.TO.ZS",
     wb("SP.POP.65UP.TO.ZS", "2022:2024"), LIC_WB),
    ("wb_SL.EMP.TOTL.SP.ZS.json", "World Bank WDI SL.EMP.TOTL.SP.ZS (ILO modelled)",
     wb("SL.EMP.TOTL.SP.ZS", "2022:2025"), LIC_WB),
    ("fao_FoodBalanceSheets_E_All_Data.zip", "FAOSTAT Food Balance Sheets (2010-) bulk",
     "https://bulks-faostat.fao.org/production/FoodBalanceSheets_E_All_Data.zip", LIC_FAO),
    ("un_m49_overview.html", "UNSD M49 standard country codes (M49 -> ISO3 map)",
     "https://unstats.un.org/unsd/methodology/m49/overview/", LIC_UN),
    ("who_HWF_0001.json", "WHO GHO (xMart public OData) HWF_0001 medical doctors per 10 000",
     who("HWF_0001"), LIC_WHO),
    ("who_HWF_0006.json", "WHO GHO (xMart public OData) HWF_0006 nursing & midwifery per 10 000",
     who("HWF_0006"), LIC_WHO),
    ("who_REF_INDICATOR_HWF.json", "WHO GHO indicator registry (code verification)",
     "https://xmart-api-public.who.int/GHO/REF_INDICATOR?"
     + urllib.parse.urlencode({"$filter": "startswith(INDICATOR_CODE,'HWF_')"}, safe="$,'"),
     LIC_WHO),
    ("ilo_EMP_2EMP_SEX_AGE_NB_A.csv", "ILOSTAT EMP_2EMP_SEX_AGE_NB_A (ILO modelled employment)",
     ilo("EMP_2EMP_SEX_AGE_NB_A", {"sex": "SEX_T", "classif1": "AGE_YTHADULT_YGE15",
                                    "timefrom": "2022", "timeto": "2024"}), LIC_ILO),
    ("ilo_EAP_2EAP_SEX_AGE_NB_A.csv", "ILOSTAT EAP_2EAP_SEX_AGE_NB_A (ILO modelled labour force)",
     ilo("EAP_2EAP_SEX_AGE_NB_A", {"sex": "SEX_T", "classif1": "AGE_YTHADULT_YGE15",
                                    "timefrom": "2022", "timeto": "2024"}), LIC_ILO),
    ("ilo_HOW_TEMP_SEX_NB_A.csv", "ILOSTAT HOW_TEMP_SEX_NB_A (mean weekly hours actually worked)",
     ilo("HOW_TEMP_SEX_NB_A", {"sex": "SEX_T", "timefrom": "2015"}), LIC_ILO),
    ("ilo_dic_ref_area.csv", "ILOSTAT ref_area dictionary (aggregate labels)",
     "https://rplumber.ilo.org/metadata/dic/?var=ref_area&format=.csv&lang=en", LIC_ILO),
    ("owid_energy_data.csv", "Our World in Data energy dataset (republishes EI/Ember/EIA)",
     "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv", LIC_OWID),
    # Gap-fill only (countries absent from the current FAOSTAT FBS bulk release).
    ("owid_daily_per_capita_caloric_supply.csv", "Our World in Data grapher (republishes FAO FBS)",
     "https://ourworldindata.org/grapher/daily-per-capita-caloric-supply.csv"
     "?v=1&csvType=full&useColumnShortNames=true", LIC_OWID),
    ("owid_daily_per_capita_protein_supply.csv", "Our World in Data grapher (republishes FAO FBS)",
     "https://ourworldindata.org/grapher/daily-per-capita-protein-supply.csv"
     "?v=1&csvType=full&useColumnShortNames=true", LIC_OWID),
]


def download(url, tries=4, timeout=300):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status != 200:
                    raise urllib.error.HTTPError(url, resp.status, "bad status", resp.headers, None)
                return resp.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = e
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"failed after {tries} tries: {url}: {last}")


def write_manifest(raw_dir, rows):
    manifest = raw_dir / "raw_manifest.csv"
    merged = {}
    if manifest.exists():
        with manifest.open(newline="") as f:
            merged = {r["file"]: r for r in csv.DictReader(f)}
    merged.update({r["file"]: r for r in rows})
    with manifest.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for k in sorted(merged):
            w.writerow(merged[k])


def fetch_all(raw_dir=RAW, only=None):
    raw_dir = Path(raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, source, url, lic in QUERIES:
        if only and name not in only:
            continue
        body = download(url)
        (raw_dir / name).write_bytes(body)
        rows.append({"file": name, "source": source, "url": url,
                     "retrieved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                     "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
                     "license": lic})
        print(f"fetched {name} ({len(body)} bytes)")
    if rows:
        write_manifest(raw_dir, rows)
    return rows


def verify_manifest(raw_dir=RAW):
    """Return files whose sha256 no longer matches the manifest (same contract as v62)."""
    raw_dir = Path(raw_dir)
    bad = []
    with (raw_dir / "raw_manifest.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            p = raw_dir / row["file"]
            if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != row["sha256"]:
                bad.append(row["file"])
    return bad


if __name__ == "__main__":
    fetch_all(only=set(sys.argv[1:]) or None)
