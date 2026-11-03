"""Rebuild world_indicators.csv and coverage_report.md OFFLINE from frozen raw/ files.

    python3 -I build.py

Inputs : raw/*  (hash-checked against raw/raw_manifest.csv; build aborts on mismatch)
Outputs: world_indicators.csv  (long tidy; see INTERFACE below)
         coverage_report.md

INTERFACE (world_indicators.csv, UTF-8, comma, header row, sorted by indicator_id, iso3):
    iso3, country, indicator_id, value, unit, year, source, source_url, evidence_class
  - iso3: ISO 3166-1 alpha-3; "WLD" = world row as published by the source (never computed here).
  - year: the reference year of that value (string; WHO world rows are a period, e.g. "2016-2024").
  - evidence_class: VERIFIED_OFFICIAL (World Bank, WHO, FAO, ILO APIs/bulk) or
    REPORTED_NEEDS_RECHECK (Our World in Data republication).
  - One row per (iso3, indicator_id). Latest available year per country within each
    indicator's window (INDICATORS[...]["window"]). Missing values are absent rows, never imputed.
Stdlib only. Raw downloads are parsed as data only.
"""
import csv
import io
import json
import sys
import zipfile
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OUT_CSV = HERE / "world_indicators.csv"
OUT_MD = HERE / "coverage_report.md"
COLS = ["iso3", "country", "indicator_id", "value", "unit", "year", "source", "source_url",
        "evidence_class"]
VO, RR = "VERIFIED_OFFICIAL", "REPORTED_NEEDS_RECHECK"

# indicator_id -> metadata. window = (min_year, max_year) for "current" values.
INDICATORS = {
    "pop_total": dict(unit="persons", file="wb_SP.POP.TOTL.json", window=(2022, 2024),
                      label="Population, total (WB SP.POP.TOTL)"),
    "pop_share_15_64": dict(unit="% of total population", file="wb_SP.POP.1564.TO.ZS.json",
                            window=(2022, 2024), label="Population aged 15-64 share"),
    "pop_share_65plus": dict(unit="% of total population", file="wb_SP.POP.65UP.TO.ZS.json",
                             window=(2022, 2024), label="Population aged 65+ share"),
    "food_kcal_per_cap_day": dict(unit="kcal/capita/day", file="fao_FoodBalanceSheets_E_All_Data.zip",
                                  window=(2015, 2025),
                                  label="FAO FBS Grand Total food supply (element 664; supply, not intake)"),
    "food_protein_g_per_cap_day": dict(unit="g protein/capita/day",
                                       file="fao_FoodBalanceSheets_E_All_Data.zip",
                                       window=(2015, 2025),
                                       label="FAO FBS Grand Total protein supply (element 674)"),
    "energy_primary_kwh_per_cap": dict(unit="kWh/capita/year (primary energy, substitution method)",
                                       file="owid_energy_data.csv", window=(2015, 2025),
                                       label="Primary energy consumption per capita (OWID energy_per_capita)"),
    "energy_primary_twh": dict(unit="TWh/year (primary energy, substitution method)",
                               file="owid_energy_data.csv", window=(2015, 2025),
                               label="Primary energy consumption total (OWID primary_energy_consumption)"),
    "elec_generation_kwh_per_cap": dict(unit="kWh/capita/year (electricity generation)",
                                        file="owid_energy_data.csv", window=(2015, 2025),
                                        label="Electricity generation per capita (OWID per_capita_electricity)"),
    "elec_generation_twh": dict(unit="TWh/year (electricity generation)", file="owid_energy_data.csv",
                                window=(2015, 2025),
                                label="Electricity generation total (OWID electricity_generation)"),
    "doctors_per_10k": dict(unit="medical doctors per 10 000 population", file="who_HWF_0001.json",
                            window=(2015, 2025), label="WHO HWF_0001 medical doctors per 10 000"),
    "nurses_midwives_per_10k": dict(unit="nursing and midwifery personnel per 10 000 population",
                                    file="who_HWF_0006.json", window=(2015, 2025),
                                    label="WHO HWF_0006 nursing & midwifery personnel per 10 000"),
    "employment_15plus_thousands": dict(unit="thousand persons employed, age 15+",
                                        file="ilo_EMP_2EMP_SEX_AGE_NB_A.csv", window=(2022, 2024),
                                        label="ILO modelled estimates EMP_2EMP (employment 15+)"),
    "labour_force_15plus_thousands": dict(unit="thousand persons in labour force, age 15+",
                                          file="ilo_EAP_2EAP_SEX_AGE_NB_A.csv", window=(2022, 2024),
                                          label="ILO modelled estimates EAP_2EAP (labour force 15+)"),
    "emp_to_pop_ratio_15plus_pct": dict(unit="% of population 15+ (ILO modelled, via WB)",
                                        file="wb_SL.EMP.TOTL.SP.ZS.json", window=(2022, 2024),
                                        label="Employment-to-population ratio 15+ (WB SL.EMP.TOTL.SP.ZS)"),
    "hours_actual_weekly_per_employed": dict(unit="hours/week actually worked per employed person (all jobs)",
                                             file="ilo_HOW_TEMP_SEX_NB_A.csv", window=(2015, 2025),
                                             label="ILO HOW_TEMP_SEX_NB mean weekly hours actually worked (survey-based)"),
}

# Plausibility bounds (inclusive). Source values outside them are REJECTED (listed in the
# coverage report) and the latest *plausible* year is used instead; nothing is corrected.
PLAUSIBLE = {
    "pop_total": (1e3, 2e9),
    "pop_share_15_64": (40, 90),
    "pop_share_65plus": (0, 40),
    "food_kcal_per_cap_day": (1500, 4500),
    "food_protein_g_per_cap_day": (20, 200),
    "energy_primary_kwh_per_cap": (0, 400_000),
    "elec_generation_kwh_per_cap": (0, 100_000),
    "doctors_per_10k": (0, 120),
    "nurses_midwives_per_10k": (0, 300),
    "emp_to_pop_ratio_15plus_pct": (10, 95),
    "hours_actual_weekly_per_employed": (15, 65),
}
REJECTED = []  # (indicator_id, iso3, year, value) filled by build()

M49_OVERRIDES = {"158": ("TWN", "Taiwan (China, Taiwan Province of)")}  # ISO 3166-1 numeric 158; absent from UNSD M49 page


# ---------------------------------------------------------------- helpers
def manifest():
    with (RAW / "raw_manifest.csv").open(newline="") as f:
        return {r["file"]: r for r in csv.DictReader(f)}


def verify(raw_dir=RAW):
    sys.path.insert(0, str(HERE))
    from fetch_world import verify_manifest
    return verify_manifest(raw_dir)


def num(s):
    if s is None:
        return None
    s = str(s).strip()
    if s == "":
        return None
    return float(s)


def fmt(v):
    if isinstance(v, int):
        return str(v)
    r = round(v, 6)
    return str(int(r)) if r == int(r) and abs(r) >= 1e6 else repr(r)


class M49Parser(HTMLParser):
    """Collect <td> text of rows in <table id="downloadTableEN">."""

    def __init__(self):
        super().__init__()
        self.in_table = self.in_cell = False
        self.depth = 0
        self.rows, self.row, self.cell, self.header = [], [], [], []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            if dict(attrs).get("id") == "downloadTableEN":
                self.in_table, self.depth = True, 1
            elif self.in_table:
                self.depth += 1
        if not self.in_table:
            return
        if tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.in_cell, self.cell = True, []

    def handle_endtag(self, tag):
        if not self.in_table:
            return
        if tag in ("td", "th"):
            self.in_cell = False
            self.row.append(" ".join("".join(self.cell).split()))
        elif tag == "tr" and self.row:
            self.rows.append(self.row)
        elif tag == "table":
            self.depth -= 1
            if self.depth == 0:
                self.in_table = False

    def handle_data(self, data):
        if self.in_table and self.in_cell:
            self.cell.append(data)


def load_m49():
    p = M49Parser()
    p.feed((RAW / "un_m49_overview.html").read_text(encoding="utf-8"))
    head = p.rows[0]
    i_name, i_m49, i_iso = head.index("Country or Area"), head.index("M49 Code"), head.index("ISO-alpha3 Code")
    out = {}
    for r in p.rows[1:]:
        if len(r) > i_iso and len(r[i_iso]) == 3 and r[i_m49].isdigit():
            out[r[i_m49].zfill(3)] = (r[i_iso], r[i_name])
    for k, v in M49_OVERRIDES.items():
        out.setdefault(k, v)
    return out


def latest(series, window):
    """series: {year:int -> value}. Latest year within window with a value."""
    ys = [y for y, v in series.items() if v is not None and window[0] <= y <= window[1]]
    if not ys:
        return None
    y = max(ys)
    return y, series[y]


# ---------------------------------------------------------------- readers
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


def read_fao(element):
    out, src = defaultdict(dict), {}
    with zipfile.ZipFile(RAW / "fao_FoodBalanceSheets_E_All_Data.zip") as z:
        with z.open("FoodBalanceSheets_E_All_Data_NOFLAG.csv") as fb:
            rd = csv.DictReader(io.TextIOWrapper(fb, encoding="utf-8-sig", errors="strict"))
            for r in rd:
                if r["Item Code"] != "2901" or r["Element Code"] != element:
                    continue
                m49 = r["Area Code (M49)"].lstrip("'").zfill(3)
                for k, v in r.items():
                    if k.startswith("Y") and k[1:].isdigit() and num(v) is not None:
                        y = int(k[1:])
                        prev = out[m49].get(y)
                        if prev is not None and abs(prev - num(v)) > 1e-9:
                            raise ValueError(f"FAO conflicting duplicate {m49} {y} {element}")
                        out[m49][y] = num(v)
                src[m49] = r["Area"]
    return out, src


def read_who(fname):
    d = json.loads((RAW / fname).read_text(encoding="utf-8"))
    if d.get("@odata.nextLink"):
        raise ValueError(f"{fname}: paginated response not fully frozen")
    out, world = defaultdict(dict), None
    for r in d["value"]:
        if r["DIMENSION_1"] is not None:
            continue
        if r["LOCATION_TYPE"] == "COUNTRY" and r["PERIOD_CODE"].isdigit():
            out[r["LOCATION_CODE"]][int(r["PERIOD_CODE"])] = r["VALUE_NUMERIC"]
        elif r["LOCATION_TYPE"] == "GLOBAL":
            world = (r["PERIOD_CODE"], r["VALUE_NUMERIC"])
    return out, world


def read_ilo(fname, classif=None):
    out, srcs = defaultdict(dict), defaultdict(dict)
    with (RAW / fname).open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if r.get("sex") != "SEX_T" or (classif and r.get("classif1") != classif):
                continue
            v, y = num(r["obs_value"]), int(r["time"])
            if v is None:
                continue
            if y in out[r["ref_area"]] and out[r["ref_area"]][y] != v:
                raise ValueError(f"ILO duplicate {fname} {r['ref_area']} {y}")
            out[r["ref_area"]][y] = v
            srcs[r["ref_area"]][y] = r["source"]
    return out, srcs


def ilo_world_code():
    with (RAW / "ilo_dic_ref_area.csv").open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if r["ref_area.label"].strip() == "World":
                return r["ref_area"]
    return None


FOOD_GAPFILL = {"food_kcal_per_cap_day": "owid_daily_per_capita_caloric_supply.csv",
                "food_protein_g_per_cap_day": "owid_daily_per_capita_protein_supply.csv"}


def read_owid_grapher(fname):
    """OWID grapher CSV: entity,code,year,<one value column>. Real ISO3 codes only."""
    out = defaultdict(dict)
    with (RAW / fname).open(encoding="utf-8", newline="") as f:
        rd = csv.reader(f)
        head = next(rd)
        if head[:3] != ["entity", "code", "year"] or len(head) != 4:
            raise ValueError(f"{fname}: unexpected columns {head}")
        for ent, code, year, val in rd:
            if len(code) == 3 and code.isalpha() and num(val) is not None:
                out[code][int(year)] = num(val)
    return out


def read_owid(col):
    out, names = defaultdict(dict), {}
    with (RAW / "owid_energy_data.csv").open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            iso = r["iso_code"].strip()
            if r["country"] == "World" and not iso:
                iso = "WLD"
            if not iso or iso.startswith("OWID"):
                continue
            v = num(r[col])
            if v is not None:
                out[iso][int(r["year"])] = v
                names[iso] = r["country"]
    return out, names


# ---------------------------------------------------------------- build
def build(out_csv=OUT_CSV, out_md=OUT_MD, check_hashes=True):
    if check_hashes:
        bad = verify()
        if bad:
            raise SystemExit(f"raw files changed vs manifest: {bad}")
    man = manifest()
    REJECTED.clear()
    wb_meta = json.loads((RAW / "wb_country_meta.json").read_text(encoding="utf-8"))[1]
    wb_econ = {r["id"]: r["name"] for r in wb_meta if r["region"]["id"] != "NA"}
    m49 = load_m49()
    m49_iso = {iso: name for iso, name in m49.values()}
    valid = set(wb_econ) | set(m49_iso)
    names = {**m49_iso, **wb_econ, "WLD": "World"}

    rows = []

    def emit(ind, series_by_iso, source, fname, evidence, world=None):
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
                                 source=source, source_url=man[fname]["url"], evidence_class=evidence))
        if world is not None:
            rows.append(dict(iso3="WLD", country="World", indicator_id=ind, value=fmt(world[1]),
                             unit=md["unit"], year=str(world[0]), source=source,
                             source_url=man[fname]["url"], evidence_class=evidence))

    # 1. World Bank population & employment ratio
    for ind, code in [("pop_total", "SP.POP.TOTL"), ("pop_share_15_64", "SP.POP.1564.TO.ZS"),
                      ("pop_share_65plus", "SP.POP.65UP.TO.ZS"),
                      ("emp_to_pop_ratio_15plus_pct", "SL.EMP.TOTL.SP.ZS")]:
        fname = INDICATORS[ind]["file"]
        d = read_wb(fname)
        w = latest(d.get("WLD", {}), INDICATORS[ind]["window"])
        emit(ind, {k: v for k, v in d.items() if k != "WLD"}, f"World Bank WDI {code}", fname, VO, w)

    # 2. FAO food balance sheets
    for ind, el in [("food_kcal_per_cap_day", "664"), ("food_protein_g_per_cap_day", "674")]:
        d, _ = read_fao(el)
        by_iso = {}
        for code, series in d.items():
            if code in m49:
                by_iso[m49[code][0]] = series
        w = latest(d.get("001", {}), INDICATORS[ind]["window"])
        emit(ind, by_iso, f"FAOSTAT Food Balance Sheets element {el} item 2901 Grand Total",
             INDICATORS[ind]["file"], VO, w)
        # Gap-fill from OWID's republication of FAO for economies absent from the FAO bulk release.
        have = {r["iso3"] for r in rows if r["indicator_id"] == ind}
        gfile = FOOD_GAPFILL[ind]
        g = {k: v for k, v in read_owid_grapher(gfile).items()
             if k not in have and latest(v, INDICATORS[ind]["window"])}
        emit(ind, g, "Our World in Data grapher (republishes FAO FBS), gap-fill", gfile, RR)

    # 3. OWID energy
    for ind, col in [("energy_primary_kwh_per_cap", "energy_per_capita"),
                     ("energy_primary_twh", "primary_energy_consumption"),
                     ("elec_generation_kwh_per_cap", "per_capita_electricity"),
                     ("elec_generation_twh", "electricity_generation")]:
        d, _ = read_owid(col)
        w = latest(d.pop("WLD", {}), INDICATORS[ind]["window"])
        emit(ind, d, f"Our World in Data energy dataset column {col}", INDICATORS[ind]["file"], RR, w)

    # 4. WHO health workforce
    for ind, code in [("doctors_per_10k", "HWF_0001"), ("nurses_midwives_per_10k", "HWF_0006")]:
        d, w = read_who(INDICATORS[ind]["file"])
        emit(ind, d, f"WHO GHO {code} (NHWA)", INDICATORS[ind]["file"], VO, w)

    # 5. ILO labour
    wcode = ilo_world_code()
    for ind, classif in [("employment_15plus_thousands", "AGE_YTHADULT_YGE15"),
                         ("labour_force_15plus_thousands", "AGE_YTHADULT_YGE15"),
                         ("hours_actual_weekly_per_employed", None)]:
        fname = INDICATORS[ind]["file"]
        d, _ = read_ilo(fname, classif)
        w = latest(d.pop(wcode, {}), INDICATORS[ind]["window"]) if wcode else None
        emit(ind, d, "ILOSTAT " + fname[4:-4], fname, VO, w)

    rows.sort(key=lambda r: (r["indicator_id"], r["iso3"] != "WLD", r["iso3"]))
    with Path(out_csv).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    if out_md:
        Path(out_md).write_text(coverage_report(rows), encoding="utf-8")
    return rows


# ---------------------------------------------------------------- coverage report
def summarize(rows):
    by = defaultdict(dict)
    for r in rows:
        by[r["indicator_id"]][r["iso3"]] = r
    pop = {k: float(r["value"]) for k, r in by["pop_total"].items() if k != "WLD"}
    world_pop = float(by["pop_total"]["WLD"]["value"])

    def wmean(ind, weights):
        num_, den = 0.0, 0.0
        for k, r in by[ind].items():
            if k != "WLD" and k in weights:
                num_ += float(r["value"]) * weights[k]
                den += weights[k]
        return num_ / den if den else None

    emp = {k: float(r["value"]) for k, r in by["employment_15plus_thousands"].items() if k != "WLD"}
    s = {"by": by, "pop": pop, "world_pop": world_pop, "sum_country_pop": sum(pop.values())}
    s["kcal_pw"] = wmean("food_kcal_per_cap_day", pop)
    s["protein_pw"] = wmean("food_protein_g_per_cap_day", pop)
    s["energy_pw"] = wmean("energy_primary_kwh_per_cap", pop)
    s["elec_pw"] = wmean("elec_generation_kwh_per_cap", pop)
    s["doc_pw"] = wmean("doctors_per_10k", pop)
    s["nurse_pw"] = wmean("nurses_midwives_per_10k", pop)
    s["hours_ew"] = wmean("hours_actual_weekly_per_employed", emp)
    s["emp_sum"] = sum(emp.values())
    return s


def coverage_report(rows):
    s = summarize(rows)
    by, pop, wp = s["by"], s["pop"], s["world_pop"]
    L = ["# V6.5 world indicators: coverage report", "",
         "Generated by `build.py` from frozen files in `raw/` (see `raw/raw_manifest.csv`). "
         "Do not edit by hand.", "",
         f"Population denominator: World Bank SP.POP.TOTL world (WLD) = {wp:,.0f} "
         f"({by['pop_total']['WLD']['year']}). Sum of the {len(pop)} country/economy rows = "
         f"{s['sum_country_pop']:,.0f} ({100 * s['sum_country_pop'] / wp:.2f}% of WLD).", "",
         "Coverage share = sum of WB population (latest year) of economies that have a value, "
         "divided by WB world population. Territories without a WB population (e.g. Taiwan) count as 0.", "",
         "| indicator_id | unit | source | evidence | countries | % world pop | years (min-max) | source WORLD row |",
         "|---|---|---|---|---|---|---|---|"]
    for ind, md in INDICATORS.items():
        d = {k: r for k, r in by.get(ind, {}).items() if k != "WLD"}
        if not d:
            L.append(f"| {ind} | {md['unit']} | | | 0 | 0 | MISSING | |")
            continue
        cov = sum(pop.get(k, 0.0) for k in d) / wp
        yrs = sorted(int(r["year"]) for r in d.values())
        wr = by[ind].get("WLD")
        wtxt = f"{float(wr['value']):,.4g} ({wr['year']})" if wr else "none"
        evc = defaultdict(int)
        for r in d.values():
            evc[r["evidence_class"]] += 1
        ev = "; ".join(f"{k} {n}" for k, n in sorted(evc.items()))
        L.append(f"| {ind} | {md['unit']} | {md['label']} | {ev} | {len(d)} | {100 * cov:.1f}% | "
                 f"{yrs[0]}-{yrs[-1]} | {wtxt} |")
    L += ["", "## Computed world aggregates (population-weighted over covered countries; WB pop latest year)", "",
          "These are computed here, not published values; weights use WB population of the latest year "
          "even where the indicator year is older.", "",
          f"- Population (WB WLD): {wp:,.0f}",
          f"- Food supply: {s['kcal_pw']:,.0f} kcal/cap/day; protein {s['protein_pw']:.1f} g/cap/day "
          "(FAO FBS supply at retail level, includes household waste; not intake)",
          f"- Primary energy: {s['energy_pw']:,.0f} kWh/cap/yr (= {s['energy_pw'] * 0.0036:.1f} GJ/cap/yr; "
          "OWID substitution method, primary not final energy)",
          f"- Electricity generation: {s['elec_pw']:,.0f} kWh/cap/yr",
          f"- Medical doctors: {s['doc_pw']:.1f} per 10k; nursing & midwifery: {s['nurse_pw']:.1f} per 10k "
          "(latest year per country, 2015+)",
          f"- Employment 15+ (ILO modelled, sum of countries): {s['emp_sum'] / 1e6:,.3f} billion persons",
          f"- Mean weekly hours actually worked (employment-weighted over countries with survey data): "
          f"{s['hours_ew']:.1f} h/week", "",
          "## Largest gaps (most populous economies with no value)", ""]
    for ind in INDICATORS:
        d = by.get(ind, {})
        miss = sorted((k for k in pop if k not in d), key=lambda k: -pop[k])
        if miss:
            top = ", ".join(f"{k} ({pop[k] / 1e6:,.1f}M)" for k in miss[:8])
            L.append(f"- **{ind}**: {len(miss)} WB economies missing; largest: {top}")
    L += ["", "## Source values rejected as implausible (not corrected; previous plausible year used)", ""]
    L += [f"- {ind} {iso} {y}: {v} (bounds {PLAUSIBLE[ind]})" for ind, iso, y, v in sorted(REJECTED)] or ["- none"]
    L += ["", "## Known caveats", "",
          "- Food (FAO FBS): 11 economies (incl. Japan, Sudan, Mali, Chad, Somalia) are absent from the current "
          "FAOSTAT FBS bulk release (2010-2023); their values come from OWID's republication of an earlier "
          "FAO release (year 2022) and are flagged REPORTED_NEEDS_RECHECK. Values are dietary "
          "energy *supply* (availability), not consumption; Taiwan mapped "
          "via ISO numeric 158 (absent from the UNSD M49 page); FAO 'China' (M49 159) aggregate is "
          "excluded, 'China, mainland' maps to CHN, Hong Kong/Macao separately.",
          "- Energy (OWID): REPORTED_NEEDS_RECHECK. Primary energy uses OWID's substitution method "
          "(non-fossil electricity grossed up to fossil-equivalent input); it is *primary*, not final, "
          "energy. Small economies come from EIA with older years. Recheck against Energy Institute "
          "Statistical Review / IEA before use in final results.",
          "- Health workforce (WHO NHWA): reporting years vary widely; WORLD row is WHO's period "
          "estimate (2016-2024). Values older than 2015 are excluded.",
          "- Labour (ILO modelled estimates): employment and labour force are model-based for "
          "countries without recent surveys. Hours actually worked are survey-based only and patchy; "
          "missing countries (incl. China) are left MISSING, not imputed. The hours WORLD row is ILO's "
          "published world aggregate (ref_area X01), which is model-based.",
          "- The GHO OData endpoint ghoapi.azureedge.net returned HTTP 500 on 2026-11-03; WHO data were "
          "taken from WHO's public xMart OData (GHO mart, FACT view), the backend of the same GHO data.",
          "- No monetary indicators are included (UNIRA works in hours and physical units).", ""]
    return "\n".join(L)


if __name__ == "__main__":
    rs = build()
    print(f"wrote {OUT_CSV.name}: {len(rs)} rows; {OUT_MD.name}")
