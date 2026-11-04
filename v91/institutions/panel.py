"""UNIRA V9.1 — what does history say about institutions, living standards and armed conflict? (country-years 2000-2024)

Data (frozen, data/raw): UCDP/PRIO Armed Conflict Dataset v25.1 (intrastate and internationalised intrastate conflicts,
at least 25 battle deaths a year, by location); World Bank Worldwide Governance Indicators; access to basic water,
sanitation, clean cooking and electricity (v87 raw data); GDP per capita PPP.
  Q   institutional quality: mean of Voice and Accountability, Rule of Law, Control of Corruption and Government
      Effectiveness, rescaled from -2.5..+2.5 to 0..1. Political Stability / Absence of Violence is left out on
      purpose: it measures violence itself, so using it would be circular.
  LS  living standards: mean access to the four basic services (0..1), the same index as V9.0.
Logistic regressions (fitted by Newton's method, standard errors from the information matrix):
  onset   P(conflict in t+1 | no conflict in t) ~ LS_t + Q_t + relapse_t   (relapse: a conflict in the past 10 years)
  ending  P(no conflict in t+1 | conflict in t) ~ LS_t + Q_t
  reform  onset ~ ... + rise in Q over the previous 5 years (do rapid institutional changes precede conflict?)
These are ASSOCIATIONS across and within countries. Conflict lowers both indicators (reverse causation), WGI are
perception-based, and the two predictors are correlated; the results bound, but do not identify, causal effects.
python3 panel.py  ->  ../outputs/panel.json"""
import csv
import io
import json
import math
import statistics
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
RAW = HERE / "data" / "raw"
RAW87 = U / "v87" / "livingstandard" / "data" / "raw"
WGI = ("GOV_WGI_VA.EST", "GOV_WGI_RL.EST", "GOV_WGI_CC.EST", "GOV_WGI_GE.EST")
ACCESS = ("SH.H2O.BASW.ZS", "SH.STA.BASS.ZS", "EG.CFT.ACCS.ZS", "EG.ELC.ACCS.ZS")
Y0, Y1 = 2000, 2024
# Gleditsch-Ward country codes of conflict locations since 1946 -> ISO3 (only states that exist in the World Bank data)
GW = {2: "USA", 20: "CAN", 40: "CUB", 41: "HTI", 42: "DOM", 51: "JAM", 52: "TTO", 70: "MEX", 90: "GTM", 91: "HND", 92: "SLV",
      93: "NIC", 94: "CRI", 95: "PAN", 100: "COL", 101: "VEN", 110: "GUY", 115: "SUR", 130: "ECU", 135: "PER", 140: "BRA",
      145: "BOL", 150: "PRY", 155: "CHL", 160: "ARG", 165: "URY", 200: "GBR", 205: "IRL", 210: "NLD", 211: "BEL", 220: "FRA",
      225: "CHE", 230: "ESP", 235: "PRT", 255: "DEU", 260: "DEU", 290: "POL", 310: "HUN", 315: "CZE", 316: "CZE", 317: "SVK",
      339: "ALB", 341: "MNE", 343: "MKD", 344: "HRV", 345: "SRB", 346: "BIH", 349: "SVN", 350: "GRC", 352: "CYP", 355: "BGR",
      359: "MDA", 360: "ROU", 365: "RUS", 366: "EST", 367: "LVA", 368: "LTU", 369: "UKR", 370: "BLR", 371: "ARM", 372: "GEO",
      373: "AZE", 402: "CPV", 404: "GNB", 411: "GNQ", 420: "GMB", 432: "MLI", 433: "SEN", 434: "BEN", 435: "MRT", 436: "NER",
      437: "CIV", 438: "GIN", 439: "BFA", 450: "LBR", 451: "SLE", 452: "GHA", 461: "TGO", 471: "CMR", 475: "NGA", 481: "GAB",
      482: "CAF", 483: "TCD", 484: "COG", 490: "COD", 500: "UGA", 501: "KEN", 510: "TZA", 516: "BDI", 517: "RWA", 520: "SOM",
      522: "DJI", 530: "ETH", 531: "ERI", 540: "AGO", 541: "MOZ", 551: "ZMB", 552: "ZWE", 553: "MWI", 560: "ZAF", 565: "NAM",
      570: "LSO", 571: "BWA", 572: "SWZ", 580: "MDG", 581: "COM", 590: "MUS", 600: "MAR", 615: "DZA", 616: "TUN", 620: "LBY",
      625: "SDN", 626: "SSD", 630: "IRN", 640: "TUR", 645: "IRQ", 651: "EGY", 652: "SYR", 660: "LBN", 663: "JOR", 666: "ISR",
      670: "SAU", 678: "YEM", 680: "YEM", 690: "KWT", 692: "BHR", 694: "QAT", 696: "ARE", 698: "OMN", 700: "AFG", 701: "TKM",
      702: "TJK", 703: "KGZ", 704: "UZB", 705: "KAZ", 710: "CHN", 712: "MNG", 713: "TWN", 731: "PRK", 732: "KOR", 740: "JPN",
      750: "IND", 760: "BTN", 770: "PAK", 771: "BGD", 775: "MMR", 780: "LKA", 781: "MDV", 790: "NPL", 800: "THA", 811: "KHM",
      812: "LAO", 816: "VNM", 817: "VNM", 820: "MYS", 830: "SGP", 835: "BRN", 840: "PHL", 850: "IDN", 860: "TLS", 900: "AUS",
      910: "PNG", 920: "NZL", 940: "SLB", 950: "FJI"}


def ucdp_csv(name):
    with zipfile.ZipFile(RAW / name) as z:
        member = [m for m in z.namelist() if m.endswith(".csv")][0]
        return list(csv.DictReader(io.TextIOWrapper(z.open(member), encoding="utf-8")))


def conflict_years():
    """{iso: set(years)} with an intrastate or internationalised intrastate conflict located in the country."""
    out = {}
    for r in ucdp_csv("ucdp-prio-acd-251-csv.zip"):
        if r["type_of_conflict"] not in ("3", "4"):
            continue
        for g in r["gwno_loc"].split(","):
            iso = GW.get(int(g))
            if iso:
                out.setdefault(iso, set()).add(int(r["year"]))
    return out


def wb(path):
    out = {}
    for x in json.loads(path.read_text())[1]:
        if x["value"] is not None and x["countryiso3code"]:
            out.setdefault(x["countryiso3code"], {})[int(x["date"])] = x["value"]
    return out


def filled(series, years):
    """Values for every year, interpolated linearly inside the observed range (WGI skip 1997, 1999 and 2001)."""
    ys = sorted(series)
    out = {}
    for y in years:
        if y in series:
            out[y] = series[y]
            continue
        lo = [a for a in ys if a < y]
        hi = [a for a in ys if a > y]
        if lo and hi:
            a, b = lo[-1], hi[0]
            out[y] = series[a] + (series[b] - series[a]) * (y - a) / (b - a)
    return out


def indices():
    years = range(1996, Y1 + 1)
    wgi = {c: wb(RAW / f"wb_{c}.json") for c in WGI}
    acc = {c: wb(RAW87 / f"wb_{c}.json") for c in ACCESS}
    gdp = wb(RAW / "wb_NY.GDP.PCAP.PP.KD.json")
    meta = {m["id"]: m for m in json.loads((U / "v65" / "data" / "raw" / "wb_country_meta.json").read_text())[1]}
    keys = sorted(k for k, m in meta.items() if m["region"]["value"].strip() != "Aggregates")
    Q, LS, G = {}, {}, {}
    for k in keys:
        f = [filled(wgi[c].get(k, {}), years) for c in WGI]
        Q[k] = {y: (statistics.fmean(v[y] for v in f) + 2.5) / 5 for y in years if all(y in v for v in f)}
        a = [filled(acc[c].get(k, {}), years) for c in ACCESS]
        LS[k] = {y: min(1.0, statistics.fmean(v[y] for v in a) / 100) for y in years if all(y in v for v in a)}
        G[k] = {y: math.log(v) for y, v in filled(gdp.get(k, {}), years).items()}
    return keys, Q, LS, G


def logit(X, y, iters=50):
    """Maximum-likelihood logistic regression; returns coefficients, standard errors and log-likelihood."""
    n, p = len(X), len(X[0])
    b = [0.0] * p
    for _ in range(iters):
        g = [0.0] * p
        H = [[0.0] * p for _ in range(p)]
        for xi, yi in zip(X, y):
            z = sum(bj * xj for bj, xj in zip(b, xi))
            m = 1 / (1 + math.exp(-max(-35.0, min(35.0, z))))
            for j in range(p):
                g[j] += (yi - m) * xi[j]
                for k in range(p):
                    H[j][k] += m * (1 - m) * xi[j] * xi[k]
        step = solve(H, g)
        b = [bj + sj for bj, sj in zip(b, step)]
        if max(abs(s) for s in step) < 1e-10:
            break
    inv = invert(H)
    ll = 0.0
    for xi, yi in zip(X, y):
        z = sum(bj * xj for bj, xj in zip(b, xi))
        m = min(1 - 1e-12, max(1e-12, 1 / (1 + math.exp(-max(-35.0, min(35.0, z))))))
        ll += yi * math.log(m) + (1 - yi) * math.log(1 - m)
    return b, [math.sqrt(max(0.0, inv[j][j])) for j in range(p)], ll


def solve(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[c][c]:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * yv for x, yv in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def invert(A):
    n = len(A)
    cols = []
    for j in range(n):
        e = [0.0] * n
        e[j] = 1.0
        cols.append(solve(A, e))
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def report(names, b, se, ll, n, events):
    return {"n": n, "events": events, "log_likelihood": round(ll, 2),
            "coefficients": {k: {"estimate": round(v, 3), "se": round(s, 3), "ci95": [round(v - 1.96 * s, 3), round(v + 1.96 * s, 3)],
                                 "odds_ratio_per_0.1": round(math.exp(0.1 * v), 3) if k != "const" else None}
                             for k, v, s in zip(names, b, se)}}


def datasets(keys, Q, LS, G, cy, econ="LS"):
    """Rows for the onset and ending models; econ is LS (access) or G (log GDP per capita)."""
    E = LS if econ == "LS" else G
    on, end = [], []
    for k in keys:
        years = cy.get(k, set())
        for t in range(Y0, Y1):
            if t not in Q[k] or t not in E[k]:
                continue
            recent = any(t - 10 <= y <= t for y in years if y < t) if t not in years else False
            dq = Q[k][t] - Q[k][t - 5] if (t - 5) in Q[k] else None
            row = {"k": k, "t": t, "q": Q[k][t], "e": E[k][t], "recent": float(recent), "dq": dq}
            if t in years:
                end.append(row | {"y": float((t + 1) not in years)})
            else:
                on.append(row | {"y": float((t + 1) in years)})
    return on, end


def fit(rows, cols):
    X = [[1.0] + [r[c] for c in cols] for r in rows]
    y = [r["y"] for r in rows]
    b, se, ll = logit(X, y)
    return report(["const"] + cols, b, se, ll, len(rows), int(sum(y)))


def corr(a, b):
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))


def pace(Q):
    """Historical speed of institutional change: 10-year changes of Q (2004->2014 and 2014->2024), and how often a decade
    of gain was followed by a decade of loss."""
    ch, rev, gains = [], 0, 0
    for k, s in Q.items():
        if all(y in s for y in (2004, 2014, 2024)):
            a, b = s[2014] - s[2004], s[2024] - s[2014]
            ch += [a, b]
            if a > 0.02:
                gains += 1
                rev += b < -0.02
    ch.sort()
    q = lambda f: round(ch[int(f * (len(ch) - 1))], 4)
    return {"ten_year_change_percentiles": {"p10": q(0.1), "p25": q(0.25), "median": q(0.5), "p75": q(0.75), "p90": q(0.9), "p95": q(0.95)},
            "decades_observed": len(ch), "gains_2004_2014_over_0.02": gains,
            "share_of_gains_reversed_next_decade": round(rev / gains, 3) if gains else None}


def main():
    keys, Q, LS, G = indices()
    cy = conflict_years()
    on, end = datasets(keys, Q, LS, G, cy)
    on_dq = [r for r in on if r["dq"] is not None]
    for r in on_dq:
        r["dq_up"] = max(0.0, r["dq"])
    out = {"sample": {"onset_rows": len(on), "onset_events": int(sum(r["y"] for r in on)),
                      "ending_rows": len(end), "endings": int(sum(r["y"] for r in end)),
                      "correlation_Q_LS": round(corr([r["q"] for r in on], [r["e"] for r in on]), 3)},
           "onset": {"LS_only": fit(on, ["e", "recent"]), "Q_only": fit(on, ["q", "recent"]), "LS_and_Q": fit(on, ["e", "q", "recent"]),
                     "with_rapid_institutional_rise": fit(on_dq, ["e", "q", "recent", "dq_up"])},
           "ending": {"LS_and_Q": fit(end, ["e", "q"])},
           "pace_of_institutional_change": pace(Q)}
    ong, endg = datasets(keys, Q, LS, G, cy, econ="G")
    out["robustness_log_gdp_instead_of_access"] = {"onset": fit(ong, ["e", "q", "recent"]), "ending": fit(endg, ["e", "q"])}
    base = sum(r["y"] for r in on) / len(on)
    out["sample"]["onset_rate_per_country_year"] = round(base, 4)
    out["sample"]["ending_rate_per_conflict_year"] = round(sum(r["y"] for r in end) / len(end), 4)
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "panel.json").write_text(json.dumps(out, indent=1))
    s = out["sample"]
    print(f"onset rows {s['onset_rows']} ({s['onset_events']} onsets, {100 * s['onset_rate_per_country_year']:.2f}%/yr); ending rows {s['ending_rows']} "
          f"({s['endings']} endings, {100 * s['ending_rate_per_conflict_year']:.0f}%/yr); corr(Q, LS) = {s['correlation_Q_LS']}")
    for grp in ("onset", "ending"):
        for name, r in out[grp].items():
            print(f"{grp:6s} {name:30s}", "; ".join(f"{k} {v['estimate']:+.2f} [{v['ci95'][0]:+.2f},{v['ci95'][1]:+.2f}]" for k, v in r["coefficients"].items()))
    for grp, r in out["robustness_log_gdp_instead_of_access"].items():
        print(f"robust {grp:30s}", "; ".join(f"{k} {v['estimate']:+.2f} [{v['ci95'][0]:+.2f},{v['ci95'][1]:+.2f}]" for k, v in r["coefficients"].items()))
    print("pace:", out["pace_of_institutional_change"])
    return out


if __name__ == "__main__":
    main()
