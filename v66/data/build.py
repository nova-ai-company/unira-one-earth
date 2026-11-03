"""Rebuild indicators_v66.csv and coverage_report.md OFFLINE from frozen raw/ files.

    python3 -I build.py

Inputs : raw/*  (hash-checked against raw/raw_manifest.csv; build aborts on mismatch)
Outputs: indicators_v66.csv  (long tidy; see INTERFACE below)
         coverage_report.md

INTERFACE (indicators_v66.csv, UTF-8, comma, header row, sorted by indicator_id, WLD first, iso3):
    iso3, country, indicator_id, value, unit, year, source, source_url, evidence_class
  - iso3: ISO 3166-1 alpha-3 (World Bank codes, e.g. XKX Kosovo). "WLD" = world row; it is
    either published by the source, or (floor area only) computed here from the source's
    regional values and flagged as such in `source`.
  - year: reference year of the value (string).
  - evidence_class:
      VERIFIED_OFFICIAL     value as published by WB / WHO / OECD / Eurostat / UN DESA APIs or bulk files
      DERIVED_FROM_OFFICIAL arithmetic here on official values only (ratio of two published series)
      MODELLED_REGIONAL     model output for a world region (IMAGE 26 regions, Deetman et al. 2020)
                            repeated on every country of that region; NOT a country observation
  - One row per (iso3, indicator_id). Latest available year per country within each
    indicator's window. Missing values are absent rows (reported as MISSING in
    coverage_report.md), never imputed.
Stdlib only. Raw downloads are parsed as data only.
"""
import csv
import gzip
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True  # never write into ../../v65 when importing its helpers

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OUT_CSV = HERE / "indicators_v66.csv"
OUT_MD = HERE / "coverage_report.md"
V65 = HERE.parents[1] / "v65" / "data"
COLS = ["iso3", "country", "indicator_id", "value", "unit", "year", "source", "source_url",
        "evidence_class"]
VO, DER, MOD = "VERIFIED_OFFICIAL", "DERIVED_FROM_OFFICIAL", "MODELLED_REGIONAL"
EVIDENCE = (VO, DER, MOD)


def _v65(name, fname):
    spec = importlib.util.spec_from_file_location(name, V65 / fname)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_fw = _v65("v65_fetch_world", "fetch_world.py")
_b65 = _v65("v65_build", "build.py")
verify_manifest, M49Parser, num, fmt, latest = (_fw.verify_manifest, _b65.M49Parser, _b65.num,
                                                _b65.fmt, _b65.latest)

INDICATORS = {
    # 0. denominator
    "pop_total": dict(unit="persons", file="wb_SP.POP.TOTL.json", window=(2022, 2024),
                      label="Population, total (WB SP.POP.TOTL)"),
    # 1. armed forces
    "armed_forces_personnel": dict(unit="persons (active + paramilitary)", file="wb_MS.MIL.TOTL.P1.json",
                                   window=(2015, 2025), label="Armed forces personnel, total (WB MS.MIL.TOTL.P1)"),
    "armed_forces_pct_labour_force": dict(unit="% of total labour force", file="wb_MS.MIL.TOTL.TF.ZS.json",
                                          window=(2015, 2025),
                                          label="Armed forces personnel % of labour force (WB MS.MIL.TOTL.TF.ZS)"),
    # 2. health-worker training output (OECD primary, Eurostat cross-check) and stocks (WHO)
    "grad_medical_number": dict(unit="graduates/year (persons)", file="oecd_health_graduates.csv",
                                window=(2015, 2025), label="Medical graduates (OECD HSG, PHYS)"),
    "grad_nursing_number": dict(unit="graduates/year (persons)", file="oecd_health_graduates.csv",
                                window=(2015, 2025),
                                label="Nursing graduates, professional + associate (OECD HSG, MINU)"),
    "grad_midwifery_number": dict(unit="graduates/year (persons)", file="oecd_health_graduates.csv",
                                  window=(2015, 2025), label="Midwifery graduates (OECD HSG, MIDW)"),
    "grad_medical_number_eurostat": dict(unit="graduates/year (persons)", file="estat_hlth_rs_grd2.json",
                                         window=(2015, 2025),
                                         label="Physician graduates (Eurostat hlth_rs_grd2 PHYS; cross-check)"),
    "grad_nursing_number_eurostat": dict(unit="graduates/year (persons, EU-recognised qualification)",
                                         file="estat_hlth_rs_grd2.json", window=(2015, 2025),
                                         label="Nurse graduates (Eurostat hlth_rs_grd2 NRS; cross-check)"),
    "grad_midwifery_number_eurostat": dict(unit="graduates/year (persons, EU-recognised qualification)",
                                           file="estat_hlth_rs_grd2.json", window=(2015, 2025),
                                           label="Midwife graduates (Eurostat hlth_rs_grd2 MWS; cross-check)"),
    "doctors_stock_number": dict(unit="medical doctors (persons)", file="who_HWF_0002.json",
                                 window=(2015, 2025), label="WHO HWF_0002 medical doctors (number), latest"),
    "nurses_midwives_stock_number": dict(unit="nursing and midwifery personnel (persons)",
                                         file="who_HWF_0007.json", window=(2015, 2025),
                                         label="WHO HWF_0007 nursing & midwifery personnel (number), latest"),
    "doctors_stock_number_at_grad_year": dict(
        unit="medical doctors (persons)", file="who_HWF_0002.json", window=(2015, 2025),
        label="WHO HWF_0002 in the same year as grad_medical_number (only where WHO has that year)"),
    "nurses_midwives_stock_number_at_grad_year": dict(
        unit="nursing and midwifery personnel (persons)", file="who_HWF_0007.json", window=(2015, 2025),
        label="WHO HWF_0007 in the same year as grad_nursing_number (only where WHO has that year)"),
    # 3. housing floor area
    "floor_area_res_m2_per_cap_image_region": dict(
        unit="m2 residential floor area per capita (regional model value)", file="buma_res_Floorspace.csv",
        window=(2020, 2020),
        label="IMAGE/SSP2 residential floor space per capita of the country's IMAGE region (Deetman et al. 2020)"),
    "dwelling_avg_size_m2": dict(unit="m2 per dwelling (average useful floor area)", file="estat_ilc_hcmh02.json",
                                 window=(2012, 2012), label="Eurostat ilc_hcmh02 average size of dwelling, 2012"),
    "household_avg_size_persons": dict(unit="persons per household", file="estat_ilc_lvph01.json",
                                       window=(2012, 2012), label="Eurostat ilc_lvph01 average household size, 2012"),
    "floor_area_m2_per_cap_eu_derived": dict(
        unit="m2 per person (= dwelling m2 / persons per household)", file="estat_ilc_hcmh02.json",
        window=(2012, 2012), label="Eurostat dwelling size / household size, 2012 (computed here)"),
    # 4. ageing and projections
    "old_age_dependency_ratio": dict(unit="persons 65+ per 100 persons 15-64", file="wb_SP.POP.DPND.OL.json",
                                     window=(2022, 2024), label="Old-age dependency ratio (WB SP.POP.DPND.OL)"),
    "old_age_dependency_ratio_2050": dict(unit="persons 65+ per 100 persons 15-64 (projection)",
                                          file="wb40_SP.POP.DPND.OL_2050.json", window=(2050, 2050),
                                          label="Old-age dependency ratio 2050 (WB Population Projections, source 40)"),
    "pop_share_65plus_2050": dict(unit="% of total population (projection)", file="wb40_SP.POP.65UP.TO.ZS_2050.json",
                                  window=(2050, 2050), label="Population 65+ share 2050 (WB source 40)"),
    "pop_total_2050_wb": dict(unit="persons (projection)", file="wb40_SP.POP.TOTL_2050.json", window=(2050, 2050),
                              label="Population 2050 (WB Population Projections, source 40)"),
    "pop_total_2050_wpp2024_medium": dict(unit="thousand persons, 1 July (projection, medium variant)",
                                          file="un_WPP2024_Demographic_Indicators_Medium.csv.gz",
                                          window=(2050, 2050), label="Population 2050, UN WPP 2024 medium variant"),
}

PLAUSIBLE = {
    "pop_total": (1e3, 2e9),
    "armed_forces_personnel": (0, 5e6),
    "armed_forces_pct_labour_force": (0, 25),
    "grad_medical_number": (0, 2e5),
    "grad_nursing_number": (0, 1e6),
    "grad_midwifery_number": (0, 1e5),
    "floor_area_res_m2_per_cap_image_region": (3, 120),
    "dwelling_avg_size_m2": (30, 250),
    "household_avg_size_persons": (1, 6),
    "floor_area_m2_per_cap_eu_derived": (10, 120),
    "old_age_dependency_ratio": (0, 100),
    "old_age_dependency_ratio_2050": (0, 120),
    "pop_share_65plus_2050": (0, 60),
    "pop_total_2050_wb": (1e2, 2e9),
    "pop_total_2050_wpp2024_medium": (0.1, 2e6),
}
REJECTED = []

# IMAGE 26-region numbering used in BUMA's files_IMAGE/*.csv (1..26; 27 is an empty slot).
# Order from the IMAGE 3 documentation; verified in tests against BUMA 1970/2020 populations.
IMAGE_REGIONS = {1: "Canada", 2: "United States", 3: "Mexico", 4: "Central America", 5: "Brazil",
                 6: "Rest of South America", 7: "Northern Africa", 8: "Western Africa", 9: "Eastern Africa",
                 10: "South Africa", 11: "Western Europe", 12: "Central Europe", 13: "Turkey",
                 14: "Ukraine Region", 15: "Central Asia", 16: "Russia Region", 17: "Middle East", 18: "India",
                 19: "Korea Region", 20: "China Region", 21: "Southeastern Asia", 22: "Indonesia Region",
                 23: "Japan", 24: "Oceania", 25: "Rest of South Asia", 26: "Rest of Southern Africa"}
# Country names in the IAMC IMAGE yaml that do not literally match a UNSD M49 / WB name.
NAME_ALIASES = {"Turkey": "TUR", "South Korea": "KOR", "North Korea": "PRK", "Iran": "IRN", "Syria": "SYR",
                "Palestine": "PSE", "Laos": "LAO", "Moldova": "MDA", "Bolivia": "BOL", "Venezuela": "VEN",
                "Tanzania": "TZA", "Micronesia": "FSM", "Taiwan": "TWN", "Hong Kong": "HKG", "Macao": "MAC",
                "Vatican": "VAT", "United Kingdom": "GBR", "United States": "USA", "Netherlands": "NLD",
                "Saint Helena, Ascension and Tristan da Cunha": "SHN", "Nauru": "NRU",
                "Wallis and Futuna": "WLF", "Côte d'Ivoire": "CIV"}
ESTAT_GEO = {"EL": "GRC", "UK": "GBR", "XK": "XKX"}
IMAGE_YEAR = 2020


# ---------------------------------------------------------------- helpers
def manifest():
    with (RAW / "raw_manifest.csv").open(newline="") as f:
        return {r["file"]: r for r in csv.DictReader(f)}


def load_m49():
    p = M49Parser()
    p.feed((RAW / "un_m49_overview.html").read_text(encoding="utf-8"))
    head = p.rows[0]
    i_name, i_iso2, i_iso = head.index("Country or Area"), head.index("ISO-alpha2 Code"), head.index("ISO-alpha3 Code")
    names, iso2 = {}, {}
    for r in p.rows[1:]:
        if len(r) > max(i_iso, i_iso2) and len(r[i_iso]) == 3:
            names[r[i_iso]] = r[i_name]
            if len(r[i_iso2]) == 2:
                iso2[r[i_iso2]] = r[i_iso]
    return names, iso2


def read_wb(fname):
    meta, data = json.loads((RAW / fname).read_text(encoding="utf-8"))
    if int(meta["pages"]) != 1:
        raise ValueError(f"{fname}: paginated response not fully frozen")
    out = defaultdict(dict)
    for r in data:
        iso = r["countryiso3code"]
        if iso and r["value"] is not None:
            out[iso][int(r["date"])] = r["value"]
    return out


def read_who(fname):
    d = json.loads((RAW / fname).read_text(encoding="utf-8"))
    if d.get("@odata.nextLink"):
        raise ValueError(f"{fname}: paginated response not fully frozen")
    out = defaultdict(dict)
    for r in d["value"]:
        if r["DIMENSION_1"] is None and r["LOCATION_TYPE"] == "COUNTRY" and r["PERIOD_CODE"].isdigit():
            if r["VALUE_NUMERIC"] is not None:
                out[r["LOCATION_CODE"]][int(r["PERIOD_CODE"])] = r["VALUE_NUMERIC"]
    return out


def read_oecd(prof):
    out = defaultdict(dict)
    with (RAW / "oecd_health_graduates.csv").open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if r["MEASURE"] != "HSG" or r["UNIT_MEASURE"] != "PS" or r["HEALTH_PROF"] != prof:
                continue
            v = num(r["OBS_VALUE"])
            if v is None:
                continue
            y = int(r["TIME_PERIOD"])
            if y in out[r["REF_AREA"]] and out[r["REF_AREA"]][y] != v:
                raise ValueError(f"OECD duplicate {prof} {r['REF_AREA']} {y}")
            out[r["REF_AREA"]][y] = v
    return out


def jsonstat(fname, fixed):
    """Eurostat JSON-stat 2.0 -> {geo: {year: value}} for one combination of the other dimensions."""
    d = json.loads((RAW / fname).read_text(encoding="utf-8"))
    ids, sizes = d["id"], d["size"]
    idx = {k: d["dimension"][k]["category"]["index"] for k in ids}
    out = defaultdict(dict)
    strides = [1] * len(ids)
    for i in range(len(ids) - 2, -1, -1):
        strides[i] = strides[i + 1] * sizes[i + 1]
    for geo, gi in idx["geo"].items():
        for t, ti in idx["time"].items():
            pos = 0
            for k, s in zip(ids, strides):
                code_i = gi if k == "geo" else ti if k == "time" else idx[k][fixed[k]]
                pos += code_i * s
            v = d["value"].get(str(pos))
            if v is not None:
                out[geo][int(t)] = float(v)
    return out


def read_wpp_2050():
    out, world = {}, None
    with gzip.open(RAW / "un_WPP2024_Demographic_Indicators_Medium.csv.gz", "rt", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["Time"] != "2050" or r["Variant"] != "Medium":
                continue
            v = num(r["TPopulation1July"])
            if r["LocTypeName"] == "World" and r["Location"] == "World":
                world = (2050, v)
            elif r["LocTypeName"] == "Country/Area" and len(r["ISO3_code"]) == 3:
                out[r["ISO3_code"]] = {2050: v}
    return out, world


def read_image_yaml():
    """IAMC native-region yaml -> {region name: [country names]} (tiny purpose-built parser)."""
    regions, cur, buf, inlist = {}, None, "", False
    for line in (RAW / "iamc_IMAGE_v3.2_regions.yaml").read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("- IMAGE 3.2|") and s.endswith(":"):
            cur = s[len("- IMAGE 3.2|"):-1]
        elif s.startswith("countries: ["):
            inlist, buf = True, s[len("countries: ["):]
        elif inlist:
            buf += " " + s
        if inlist and buf.rstrip().endswith("]"):
            inlist = False
            body = buf.rstrip()[:-1]
            regions[cur] = [c.strip() for c in next(csv.reader([body], skipinitialspace=True)) if c.strip()]
    return regions


def read_buma(fname):
    with (RAW / fname).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def image_region_values(year=IMAGE_YEAR):
    """Per IMAGE region: total m2/cap = urban m2/cap*(1-rural share) + rural m2/cap*rural share; plus pop."""
    fs = {(int(r["t"]), int(r["Region"])): (float(r["Urban"]), float(r["Rural"]))
          for r in read_buma("buma_res_Floorspace.csv")}
    rur = {int(r["t"]): r for r in read_buma("buma_rurpop.csv")}[year]
    pop = {int(r["t"]): r for r in read_buma("buma_pop.csv")}[year]
    out = {}
    for n, name in IMAGE_REGIONS.items():
        u, ru = fs[(year, n)]
        sh = float(rur[str(n)])
        out[name] = dict(urban=u, rural=ru, rural_share=sh, total=u * (1 - sh) + ru * sh,
                         pop_million=float(pop[str(n)]))
    return out


def image_country_map(names_to_iso):
    mapping, unresolved = {}, []
    for region, countries in read_image_yaml().items():
        for c in countries:
            iso = NAME_ALIASES.get(c) or names_to_iso.get(c)
            if iso:
                mapping[iso] = region
            else:
                unresolved.append((region, c))
    return mapping, unresolved


# ---------------------------------------------------------------- build
def build(out_csv=OUT_CSV, out_md=OUT_MD, check_hashes=True):
    if check_hashes:
        bad = verify_manifest(RAW)
        if bad:
            raise SystemExit(f"raw files changed vs manifest: {bad}")
    man = manifest()
    REJECTED.clear()
    wb_meta = json.loads((RAW / "wb_country_meta.json").read_text(encoding="utf-8"))[1]
    wb_econ = {r["id"]: r["name"] for r in wb_meta if r["region"]["id"] != "NA"}
    m49_names, iso2 = load_m49()
    valid = set(wb_econ) | set(m49_names)
    names = {**m49_names, **wb_econ, "WLD": "World"}
    rows = []

    def emit(ind, series_by_iso, source, fname, evidence, world=None, source_by_iso=None):
        md = INDICATORS[ind]
        lo, hi = PLAUSIBLE.get(ind, (float("-inf"), float("inf")))
        for iso, series in series_by_iso.items():
            if iso not in valid:
                continue
            ok = {}
            for y, v in series.items():
                if v is not None and md["window"][0] <= y <= md["window"][1] and not lo <= v <= hi:
                    REJECTED.append((ind, iso, y, v))
                else:
                    ok[y] = v
            got = latest(ok, md["window"])
            if got:
                rows.append(dict(iso3=iso, country=names.get(iso, iso), indicator_id=ind,
                                 value=fmt(got[1]), unit=md["unit"], year=str(got[0]),
                                 source=(source_by_iso or {}).get(iso, source),
                                 source_url=man[fname]["url"], evidence_class=evidence))
        if world is not None:
            rows.append(dict(iso3="WLD", country="World", indicator_id=ind, value=fmt(world[1]),
                             unit=md["unit"], year=str(world[0]), source=world[2] if len(world) > 2 else source,
                             source_url=man[fname]["url"], evidence_class=evidence))

    # 0/1/4. World Bank series (WDI and source 40 projections)
    for ind, code in [("pop_total", "WDI SP.POP.TOTL"), ("armed_forces_personnel", "WDI MS.MIL.TOTL.P1"),
                      ("armed_forces_pct_labour_force", "WDI MS.MIL.TOTL.TF.ZS"),
                      ("old_age_dependency_ratio", "WDI SP.POP.DPND.OL"),
                      ("old_age_dependency_ratio_2050", "Population Estimates and Projections SP.POP.DPND.OL"),
                      ("pop_share_65plus_2050", "Population Estimates and Projections SP.POP.65UP.TO.ZS"),
                      ("pop_total_2050_wb", "Population Estimates and Projections SP.POP.TOTL")]:
        fname = INDICATORS[ind]["file"]
        d = read_wb(fname)
        w = latest(d.get("WLD", {}), INDICATORS[ind]["window"])
        emit(ind, {k: v for k, v in d.items() if k != "WLD"}, f"World Bank {code}", fname, VO, w)

    d, w = read_wpp_2050()
    emit("pop_total_2050_wpp2024_medium", d, "UN DESA World Population Prospects 2024, medium variant",
         INDICATORS["pop_total_2050_wpp2024_medium"]["file"], VO, w)

    # 2. graduates (OECD primary; Eurostat cross-check) and WHO stocks
    grads = {}
    for ind, prof in [("grad_medical_number", "PHYS"), ("grad_nursing_number", "MINU"),
                      ("grad_midwifery_number", "MIDW")]:
        grads[ind] = read_oecd(prof)
        emit(ind, grads[ind], f"OECD Health Statistics, health graduates (HSG), HEALTH_PROF={prof}",
             INDICATORS[ind]["file"], VO)
    for ind, spec in [("grad_medical_number_eurostat", "PHYS"), ("grad_nursing_number_eurostat", "NRS"),
                      ("grad_midwifery_number_eurostat", "MWS")]:
        es = jsonstat("estat_hlth_rs_grd2.json", {"freq": "A", "unit": "NR", "med_spec": spec})
        emit(ind, {iso2.get(g) or ESTAT_GEO.get(g, g): v for g, v in es.items()},
             f"Eurostat hlth_rs_grd2 med_spec={spec}", INDICATORS[ind]["file"], VO)
    for ind, at_ind, grad_ind, code in [
            ("doctors_stock_number", "doctors_stock_number_at_grad_year", "grad_medical_number", "HWF_0002"),
            ("nurses_midwives_stock_number", "nurses_midwives_stock_number_at_grad_year", "grad_nursing_number",
             "HWF_0007")]:
        who = read_who(INDICATORS[ind]["file"])
        emit(ind, who, f"WHO GHO {code} (NHWA)", INDICATORS[ind]["file"], VO)
        gy = {r["iso3"]: int(r["year"]) for r in rows if r["indicator_id"] == grad_ind}
        same = {iso: {y: who[iso][y]} for iso, y in gy.items() if y in who.get(iso, {})}
        emit(at_ind, same, f"WHO GHO {code} (NHWA), year matched to OECD graduates year",
             INDICATORS[at_ind]["file"], VO)

    # 3. housing floor area
    regvals = image_region_values()
    names_to_iso = {v: k for k, v in m49_names.items()}
    names_to_iso.update({v: k for k, v in wb_econ.items()})
    cmap, unresolved = image_country_map(names_to_iso)
    if unresolved:
        raise ValueError(f"IMAGE country names not resolved to ISO3: {unresolved}")
    ind = "floor_area_res_m2_per_cap_image_region"
    series = {iso: {IMAGE_YEAR: regvals[reg]["total"]} for iso, reg in cmap.items()}
    srcs = {iso: f"Deetman et al. 2020 BUMA/IMAGE SSP2, value of IMAGE region '{reg}' (not country-specific)"
            for iso, reg in cmap.items()}
    wsum = sum(v["total"] * v["pop_million"] for v in regvals.values())
    wpop = sum(v["pop_million"] for v in regvals.values())
    emit(ind, series, "", "buma_res_Floorspace.csv", MOD,
         (IMAGE_YEAR, wsum / wpop, "Deetman et al. 2020 BUMA/IMAGE SSP2, world = IMAGE-population-weighted mean "
                                   "of 26 regions (computed here)"), source_by_iso=srcs)
    dw = jsonstat("estat_ilc_hcmh02.json", {"freq": "A", "unit": "AVG", "deg_urb": "TOTAL", "hhcomp": "TOTAL"})
    hh = jsonstat("estat_ilc_lvph01.json", {"freq": "A", "unit": "AVG"})
    dw = {iso2.get(g) or ESTAT_GEO.get(g, g): v for g, v in dw.items()}
    hh = {iso2.get(g) or ESTAT_GEO.get(g, g): v for g, v in hh.items()}
    emit("dwelling_avg_size_m2", dw, "Eurostat ilc_hcmh02 (EU-SILC 2012 housing module), total",
         "estat_ilc_hcmh02.json", VO)
    emit("household_avg_size_persons", hh, "Eurostat ilc_lvph01 (EU-SILC)", "estat_ilc_lvph01.json", VO)
    ratio = {iso: {2012: dw[iso][2012] / hh[iso][2012]} for iso in dw
             if 2012 in dw[iso] and 2012 in hh.get(iso, {})}
    emit("floor_area_m2_per_cap_eu_derived", ratio,
         "Computed here: Eurostat ilc_hcmh02 / ilc_lvph01, 2012 (dwelling-weighted, approx. m2 per person)",
         "estat_ilc_hcmh02.json", DER)

    rows.sort(key=lambda r: (r["indicator_id"], r["iso3"] != "WLD", r["iso3"]))
    with Path(out_csv).open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    if out_md:
        Path(out_md).write_text(coverage_report(rows, regvals, cmap, wb_econ), encoding="utf-8")
    return rows


# ---------------------------------------------------------------- coverage report
def coverage_report(rows, regvals, cmap, wb_econ):
    by = defaultdict(dict)
    for r in rows:
        by[r["indicator_id"]][r["iso3"]] = r
    pop = {k: float(r["value"]) for k, r in by["pop_total"].items() if k != "WLD"}
    wp = float(by["pop_total"]["WLD"]["value"])

    def total(ind):
        return sum(float(r["value"]) for k, r in by[ind].items() if k != "WLD")

    def cov(ind):
        return sum(pop.get(k, 0.0) for k in by[ind] if k != "WLD") / wp

    L = ["# V6.6 indicators: coverage report", "",
         "Generated by `build.py` from frozen files in `raw/` (see `raw/raw_manifest.csv`). Do not edit by hand.", "",
         f"Population denominator: World Bank SP.POP.TOTL world (WLD) = {wp:,.0f} ({by['pop_total']['WLD']['year']}). "
         "Coverage share = sum of WB population of economies with a value / WB world population "
         "(territories without a WB population count as 0). MISSING = no row in the CSV.", "",
         "| indicator_id | unit | source | evidence | countries | % world pop | years (min-max) | WORLD row |",
         "|---|---|---|---|---|---|---|---|"]
    for ind, md in INDICATORS.items():
        d = {k: r for k, r in by.get(ind, {}).items() if k != "WLD"}
        if not d:
            L.append(f"| {ind} | {md['unit']} | {md['label']} | | 0 | 0 | MISSING | MISSING |")
            continue
        yrs = sorted(int(r["year"]) for r in d.values())
        wr = by[ind].get("WLD")
        wtxt = f"{float(wr['value']):,.4g} ({wr['year']})" if wr else "MISSING"
        evc = defaultdict(int)
        for r in d.values():
            evc[r["evidence_class"]] += 1
        ev = "; ".join(f"{k} {n}" for k, n in sorted(evc.items()))
        L.append(f"| {ind} | {md['unit']} | {md['label']} | {ev} | {len(d)} | {100 * cov(ind):.1f}% | "
                 f"{yrs[0]}-{yrs[-1]} | {wtxt} |")

    af = by["armed_forces_personnel"]
    L += ["", "## Key totals", "",
          "Sums over countries are computed here and cover only the countries listed; they are not world values.", "",
          f"- Armed forces personnel, WB WORLD row: {float(af['WLD']['value']):,.0f} ({af['WLD']['year']}); "
          f"sum of {len(af) - 1} countries (latest year 2015+) = {total('armed_forces_personnel'):,.0f}; "
          f"world share of labour force (WB WLD): {float(by['armed_forces_pct_labour_force']['WLD']['value']):.2f}%."]
    for ind, lab in [("grad_medical_number", "Medical graduates/yr"), ("grad_nursing_number", "Nursing graduates/yr"),
                     ("grad_midwifery_number", "Midwifery graduates/yr")]:
        L.append(f"- {lab} (OECD, {len(by[ind])} countries, {100 * cov(ind):.1f}% of world pop): "
                 f"{total(ind):,.0f}. WORLD total: MISSING (WHO NHWA graduate data are not on any public API).")
    # graduates per 1000 stock where years match
    for g, s, lab in [("grad_medical_number", "doctors_stock_number_at_grad_year", "medical graduates per 100 doctors"),
                      ("grad_nursing_number", "nurses_midwives_stock_number_at_grad_year",
                       "nursing graduates per 100 nursing & midwifery personnel")]:
        ks = [k for k in by[s] if k in by[g]]
        if ks:
            gsum = sum(float(by[g][k]["value"]) for k in ks)
            ssum = sum(float(by[s][k]["value"]) for k in ks)
            L.append(f"- Replacement-rate check, {lab} (same year, {len(ks)} countries): "
                     f"{100 * gsum / ssum:.2f} (= {gsum:,.0f} / {ssum:,.0f}).")
    L.append(f"- WHO stocks (latest 2015+, sum of countries): doctors {total('doctors_stock_number'):,.0f} "
             f"({100 * cov('doctors_stock_number'):.1f}% pop); nursing & midwifery "
             f"{total('nurses_midwives_stock_number'):,.0f} ({100 * cov('nurses_midwives_stock_number'):.1f}% pop).")
    p50 = by["pop_total_2050_wpp2024_medium"]["WLD"]
    L += [f"- Population 2050: UN WPP 2024 medium {float(p50['value']) * 1e3:,.0f}; World Bank projection "
          f"{float(by['pop_total_2050_wb']['WLD']['value']):,.0f}. Old-age dependency (65+/15-64 x100): "
          f"{float(by['old_age_dependency_ratio']['WLD']['value']):.1f} ({by['old_age_dependency_ratio']['WLD']['year']}) "
          f"-> {float(by['old_age_dependency_ratio_2050']['WLD']['value']):.1f} (2050, WB). 65+ share 2050: "
          f"{float(by['pop_share_65plus_2050']['WLD']['value']):.1f}%."]

    # Eurostat vs OECD cross-check
    L += ["", "## Graduates cross-check: OECD vs Eurostat (same year only)", "",
          "| indicator | country | year | OECD | Eurostat | Eurostat/OECD |", "|---|---|---|---|---|---|"]
    for o, e in [("grad_medical_number", "grad_medical_number_eurostat"),
                 ("grad_nursing_number", "grad_nursing_number_eurostat")]:
        for k in sorted(set(by[o]) & set(by[e])):
            ro, re_ = by[o][k], by[e][k]
            if ro["year"] == re_["year"] and float(ro["value"]) > 0:
                L.append(f"| {o} | {k} | {ro['year']} | {float(ro['value']):,.0f} | {float(re_['value']):,.0f} | "
                         f"{float(re_['value']) / float(ro['value']):.2f} |")

    # floor area regions
    L += ["", f"## Residential floor area per capita by IMAGE region ({IMAGE_YEAR}, Deetman et al. 2020 / IMAGE SSP2)",
          "", "Total = urban m2/cap x (1 - rural share) + rural m2/cap x rural share (computed here from BUMA "
          "input files). Country rows in the CSV repeat their region's total (evidence MODELLED_REGIONAL).", "",
          "| IMAGE region | urban m2/cap | rural m2/cap | rural share | total m2/cap | pop (M, IMAGE) | WB countries mapped |",
          "|---|---|---|---|---|---|---|"]
    cnt = defaultdict(int)
    for iso, reg in cmap.items():
        if iso in wb_econ:
            cnt[reg] += 1
    for n, name in IMAGE_REGIONS.items():
        v = regvals[name]
        L.append(f"| {n} {name} | {v['urban']:.1f} | {v['rural']:.1f} | {v['rural_share']:.2f} | {v['total']:.1f} | "
                 f"{v['pop_million']:,.0f} | {cnt[name]} |")
    fw = by["floor_area_res_m2_per_cap_image_region"]["WLD"]
    L += ["", f"- World (IMAGE-population-weighted): {float(fw['value']):.1f} m2/cap ({fw['year']}).",
          f"- Eurostat 2012 derived m2/person (dwelling m2 / household size): {len(by['floor_area_m2_per_cap_eu_derived'])} "
          "countries; EU aggregate rows are excluded from the CSV (not ISO3).", "",
          "Unmapped WB economies (absent from the IAMC IMAGE 3.2 list; floor area MISSING): " +
          ", ".join(sorted(k for k in wb_econ if k not in cmap)) + ".", ""]

    L += ["## Largest gaps (most populous WB economies with no value)", ""]
    for ind in INDICATORS:
        d = by.get(ind, {})
        miss = sorted((k for k in pop if k not in d), key=lambda k: -pop[k])
        if miss:
            top = ", ".join(f"{k} ({pop[k] / 1e6:,.1f}M)" for k in miss[:8])
            L.append(f"- **{ind}**: {len(miss)} WB economies MISSING; largest: {top}")
    L += ["", "## Source values rejected as implausible (not corrected; previous plausible year used)", ""]
    L += [f"- {i} {iso} {y}: {v} (bounds {PLAUSIBLE[i]})" for i, iso, y, v in sorted(REJECTED)] or ["- none"]
    L += ["", "## Known caveats", "",
          "- Armed forces (WB MS.MIL.TOTL.P1, from IISS Military Balance): active + paramilitary forces; "
          "reservists excluded. Latest WB year is often 2020; a few countries have no data.",
          "- Graduates: WHO NHWA module 2 (education) graduate counts are only exposed through the NHWA "
          "portal's embedded Power BI dashboard (apps.who.int/nhwaportal); they are absent from the GHO / "
          "xMart public OData registry (searched 2026-11-03: no 'graduat' HWF indicator). Graduate numbers "
          "therefore come from OECD Health Statistics (OECD + partner countries incl. IDN, THA, ARG, COL, UKR...); "
          "large populations (CHN, IND, NGA, PAK, BRA...) are MISSING. Eurostat hlth_rs_grd2 counts EU-recognised "
          "qualifications (Directive 2005/36/EC) and can differ from OECD (e.g. associate nurses excluded).",
          "- OECD MINU = professional + associate professional nurses; midwives (MIDW) are separate. Values with "
          "OECD status flags (break, estimate, provisional) are kept as published.",
          "- Stocks at graduate year: only where WHO HWF has exactly that year; otherwise absent.",
          "- Floor area: no consolidated official country dataset exists (checked OECD AHD HC2.1 = rooms per person "
          "only; OWID has no series; Odyssee-Mure needs a login). The global series is MODELLED: IMAGE (SSP2) regional "
          "residential floor space per capita as used in Deetman et al. 2020 (J. Clean. Prod., "
          "doi:10.1016/j.jclepro.2019.118658), urban/rural combined with IMAGE rural population share. "
          "2020 is a model year (IMAGE calibrated on historical data to ~2010). Region numbering 1-26 follows the "
          "IMAGE convention (PBL region page was down on 2026-11-03); it is verified in tests by matching BUMA "
          "region populations against World Bank country populations. Country->region list from IAMC "
          "common-definitions IMAGE 3.2 (some territories, e.g. South Sudan, Rep. Congo, Kosovo, are not listed there).",
          "- Eurostat floor area per person is derived (average dwelling size / average household size, 2012); "
          "it approximates m2 per person but weights by dwelling, not person.",
          "- Projections: population 2050 from UN WPP 2024 medium (thousands, as published) and from the World Bank "
          "Population Estimates and Projections database (source 40, its own projection; differs slightly from WPP). "
          "Old-age dependency 2050 and 65+ share 2050 come from WB source 40 (the WPP demographic-indicator file has "
          "no dependency ratio).",
          "- The UN DESA Data Portal API requires a bearer token; the WPP 2024 bulk CSV was used instead.",
          "- No monetary indicators are included (UNIRA works in hours and physical units).", ""]
    return "\n".join(L)


if __name__ == "__main__":
    rs = build()
    print(f"wrote {OUT_CSV.name}: {len(rs)} rows; {OUT_MD.name}")
