"""Download raw snapshots for the V6.6 indicators and record provenance.

Run once (network required):  python3 -I fetch.py   [file ...]
Every later step (build.py) reads ONLY the frozen files in raw/, so results are
reproducible offline and auditable against raw/raw_manifest.csv
(columns: file, source, url, retrieved_at_utc, sha256, bytes, license).

The HTTP downloader, manifest writer and hash verifier are imported unchanged from
../../v65/data/fetch_world.py (same contract as V6.5). Downloads are untrusted data:
they are written as bytes and never executed. Stdlib only (Python 3.14).
"""
import hashlib
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
V65 = HERE.parents[1] / "v65" / "data"
sys.path.insert(0, str(V65))
from fetch_world import download, verify_manifest, write_manifest  # noqa: E402,F401

LIC_WB = "World Bank Open Data, CC BY 4.0"
LIC_WHO = "WHO GHO data, CC BY-NC-SA 3.0 IGO (WHO data policy)"
LIC_UN = "United Nations Statistics Division, UN terms of use"
LIC_WPP = "UN DESA Population Division, World Population Prospects 2024, CC BY 3.0 IGO"
LIC_OECD = "OECD Data, CC BY 4.0 (OECD Terms and Conditions)"
LIC_ESTAT = "Eurostat, CC BY 4.0 (Commission Decision 2011/833/EU)"
LIC_BUMA = "MIT License (SPDeetman/BUMA GitHub repository, Deetman et al. 2020)"
LIC_IAMC = "CC0-1.0 (IAMconsortium/common-definitions GitHub repository)"


def wb(indicator, dates, source=None):
    s = f"&source={source}" if source else ""
    return ("https://api.worldbank.org/v2/country/all/indicator/"
            f"{indicator}?format=json&per_page=20000&date={dates}{s}")


def who(code):
    q = urllib.parse.urlencode({
        "$filter": f"INDICATOR_CODE eq '{code}'",
        "$select": "INDICATOR_CODE,PERIOD_CODE,LOCATION_CODE,LOCATION_TYPE,"
                   "VALUE_NUMERIC,VALUE_STRING,DIMENSION_1,DIMENSION_MEMBER_1"}, safe="$,'")
    return "https://xmart-api-public.who.int/GHO/FACT?" + q


def estat(ds, params):
    return ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
            f"{ds}?" + urllib.parse.urlencode(params, doseq=True))


BUMA = "https://raw.githubusercontent.com/SPDeetman/BUMA/master/"
WPP = ("https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/"
       "CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz")

# (file name, source label, url, license)
QUERIES = [
    ("wb_country_meta.json", "World Bank API v2 country list (aggregate flags)",
     "https://api.worldbank.org/v2/country?format=json&per_page=400", LIC_WB),
    ("un_m49_overview.html", "UNSD M49 standard country codes (names, ISO2/ISO3 map)",
     "https://unstats.un.org/unsd/methodology/m49/overview/", LIC_UN),
    ("wb_SP.POP.TOTL.json", "World Bank WDI SP.POP.TOTL", wb("SP.POP.TOTL", "2022:2024"), LIC_WB),
    # 1. Armed forces
    ("wb_MS.MIL.TOTL.P1.json", "World Bank WDI MS.MIL.TOTL.P1 (IISS Military Balance via WB)",
     wb("MS.MIL.TOTL.P1", "2015:2025"), LIC_WB),
    ("wb_MS.MIL.TOTL.TF.ZS.json", "World Bank WDI MS.MIL.TOTL.TF.ZS (armed forces % labour force)",
     wb("MS.MIL.TOTL.TF.ZS", "2015:2025"), LIC_WB),
    # 2. Health-worker training output and stocks
    ("oecd_health_graduates.csv", "OECD Health Statistics, dataflow DSD_HEALTH_REAC_EMP@DF_GRAD (SDMX CSV)",
     "https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_HEALTH_REAC_EMP@DF_GRAD,/all"
     "?startPeriod=2015&dimensionAtObservation=AllDimensions&format=csvfile", LIC_OECD),
    ("estat_hlth_rs_grd2.json", "Eurostat hlth_rs_grd2 Health graduates (JSON-stat)",
     estat("hlth_rs_grd2", {"format": "JSON", "lang": "EN", "unit": "NR",
                            "sinceTimePeriod": "2015"}), LIC_ESTAT),
    ("who_HWF_0002.json", "WHO GHO (xMart public OData) HWF_0002 medical doctors (number)",
     who("HWF_0002"), LIC_WHO),
    ("who_HWF_0007.json", "WHO GHO (xMart public OData) HWF_0007 nursing & midwifery personnel (number)",
     who("HWF_0007"), LIC_WHO),
    # 3. Housing floor area
    ("buma_res_Floorspace.csv", "Deetman et al. 2020 BUMA model input: IMAGE residential m2/cap by region, urban/rural",
     BUMA + "files_IMAGE/res_Floorspace.csv", LIC_BUMA),
    ("buma_pop.csv", "Deetman et al. 2020 BUMA model input: IMAGE population by region (million)",
     BUMA + "files_IMAGE/pop.csv", LIC_BUMA),
    ("buma_rurpop.csv", "Deetman et al. 2020 BUMA model input: IMAGE rural population share by region",
     BUMA + "files_IMAGE/rurpop.csv", LIC_BUMA),
    ("buma_README.md", "Deetman et al. 2020 BUMA repository README (citation, DOIs)",
     BUMA + "README.md", LIC_BUMA),
    ("iamc_IMAGE_v3.2_regions.yaml", "IAMC common-definitions: IMAGE 3.2 native region -> country list",
     "https://raw.githubusercontent.com/IAMconsortium/common-definitions/main/"
     "definitions/region/native_regions/IMAGE/IMAGE_v3.2.yaml", LIC_IAMC),
    ("estat_ilc_hcmh02.json", "Eurostat ilc_hcmh02 Average size of dwelling (m2), EU-SILC 2012 ad-hoc module",
     estat("ilc_hcmh02", {"format": "JSON", "lang": "EN"}), LIC_ESTAT),
    ("estat_ilc_lvph01.json", "Eurostat ilc_lvph01 Average household size (EU-SILC)",
     estat("ilc_lvph01", {"format": "JSON", "lang": "EN", "time": "2012"}), LIC_ESTAT),
    # 4. Ageing and projections
    ("wb_SP.POP.DPND.OL.json", "World Bank WDI SP.POP.DPND.OL old-age dependency ratio",
     wb("SP.POP.DPND.OL", "2022:2024"), LIC_WB),
    ("wb40_SP.POP.TOTL_2050.json", "World Bank Population Estimates and Projections (source 40) SP.POP.TOTL 2050",
     wb("SP.POP.TOTL", "2050", 40), LIC_WB),
    ("wb40_SP.POP.DPND.OL_2050.json", "World Bank Population Estimates and Projections (source 40) SP.POP.DPND.OL 2050",
     wb("SP.POP.DPND.OL", "2050", 40), LIC_WB),
    ("wb40_SP.POP.65UP.TO.ZS_2050.json",
     "World Bank Population Estimates and Projections (source 40) SP.POP.65UP.TO.ZS 2050",
     wb("SP.POP.65UP.TO.ZS", "2050", 40), LIC_WB),
    ("un_WPP2024_Demographic_Indicators_Medium.csv.gz",
     "UN World Population Prospects 2024, Demographic Indicators, Medium variant (CSV)", WPP, LIC_WPP),
]


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


if __name__ == "__main__":
    fetch_all(only=set(sys.argv[1:]) or None)
