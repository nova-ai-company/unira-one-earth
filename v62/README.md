# UNIRA V6.2 — France: sector labour hours, output and a 30-hour week

Reproducible, stdlib-only Python (tested on CPython 3.14). No third-party packages.

```bash
python3 run_all.py                          # offline: frozen snapshots -> outputs/
python3 -m unittest discover -s tests -v    # unit + integration tests
python3 run_all.py --fetch                  # optional: re-download Eurostat (new hashes, possibly revised data)
```

| path | content |
|---|---|
| `RESEARCH_NOTE.md` | Method, results, limitations, falsification status — **read this first** |
| `outputs/REPORT_TABLES.md` | All result tables, generated (no hand-typed numbers) |
| `outputs/labour_sector_year.csv` | Workstream A contract dataset (year × scenario × NACE section) |
| `outputs/summary.json`, `outputs/checks.csv`, `outputs/run_log.txt` | Totals, sensitivity grids, checks, console log |
| `data/raw/` + `raw_manifest.csv` | Frozen Eurostat API responses with SHA-256 and retrieval time |
| `data/tidy/observations.csv` | All raw cells in the UNIRA evidence schema |
| `config/v62_config.json` | Scenarios and every non-data parameter, with evidence class |
| `src/unira_v62/` | `jsonstat` reader, `fetch`, `tidy`, `model`, `report` |
| `docs/DATA_DICTIONARY.md` | Column definitions, units, evidence classes |
| `audit/` | Independent audits: archive reproducibility, primary-source verification, code review of V6.2, hours–productivity evidence review, consolidated `AUDIT_FINDINGS.md` |

Data: Eurostat (national accounts transmitted by INSEE; EU-LFS), reuse under Commission Decision 2011/833/EU (CC BY 4.0).
