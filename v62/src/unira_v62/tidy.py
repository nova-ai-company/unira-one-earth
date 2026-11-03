"""Convert frozen Eurostat snapshots into (a) evidence-schema observations and
(b) in-memory lookup tables used by the model.

Evidence classes follow handover/03: a value machine-retrieved from the named
official table (hash-recorded) is VERIFIED_OFFICIAL as a *value*; provisional
('p') values are REPORTED_NEEDS_RECHECK because they will be revised. Whether a
value fits a UNIRA concept is a separate question documented in the note.
"""
import csv
from pathlib import Path

from . import jsonstat

SCHEMA = ["indicator_id", "value", "unit", "year", "observation_date", "publication_date",
          "geography_id", "geography_definition", "population_definition", "method",
          "source_url", "source_table", "source_version", "retrieved_at", "uncertainty",
          "evidence_class", "license", "nace_r2", "status_flag"]

POPULATION = {
    "nama_10_a64_e": "National accounts, domestic concept (persons/hours in resident production units)",
    "nama_10_a64": "National accounts, resident industries",
    "lfsa_ewhun2": "LFS persons aged 15+, main job, usual weekly hours",
    "lfsa_ewhan2": "LFS persons aged 15+ who worked in reference week, main job, actual weekly hours",
    "lfsa_epgan2": "LFS employed persons 15+ (self-declared full-time/part-time)",
    "lfsi_sla_a": "LFS persons aged 15-74",
}


def read_manifest(raw_dir):
    with (Path(raw_dir) / "raw_manifest.csv").open() as f:
        return {r["file"]: r for r in csv.DictReader(f)}


def load_raw(raw_dir):
    """Return {file_stem: (doc, manifest_row)}."""
    manifest = read_manifest(raw_dir)
    return {Path(name).stem: (jsonstat.load(Path(raw_dir) / name), row)
            for name, row in manifest.items()}


def observations(raw):
    """Flatten every snapshot into rows of the UNIRA evidence schema."""
    out = []
    for stem, (doc, man) in raw.items():
        meta = jsonstat.dataset_meta(doc)
        ds = man["dataset"]
        for coords, value, flag in jsonstat.iter_cells(doc):
            key = [stem] + [f"{k}={v}" for k, v in coords.items()
                            if k not in ("freq", "geo", "time")]
            out.append({
                "indicator_id": "|".join(key), "value": value,
                "unit": coords.get("unit", "HR" if "ewh" in ds else ""),
                "year": coords["time"], "observation_date": f"{coords['time']} (annual)",
                "publication_date": meta["updated"], "geography_id": coords["geo"],
                "geography_definition": "France (Eurostat country code FR, incl. overseas departments per Eurostat metadata; check per dataset)",
                "population_definition": POPULATION.get(ds, ""),
                "method": "Eurostat dissemination API JSON-stat, no transformation",
                "source_url": man["url"], "source_table": ds,
                "source_version": f"datastructure {meta['datastructure_version']}; updated {meta['updated']}",
                "retrieved_at": man["retrieved_at_utc"],
                "uncertainty": "; ".join(x for x in (
                    "provisional (p), subject to revision" if "p" in flag else "",
                    "low reliability (u)" if "u" in flag else "",
                    "break in time series (b)" if "b" in flag else "",
                    "LFS sample estimate" if ds.startswith("lfs") else "national accounts estimate; revisions possible",
                ) if x),
                "evidence_class": "REPORTED_NEEDS_RECHECK" if ("p" in flag or "u" in flag) else "VERIFIED_OFFICIAL",
                "license": man["license"], "nace_r2": coords.get("nace_r2", ""),
                "status_flag": flag,
            })
    return out


def write_observations(rows, path):
    with Path(path).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        w.writerows(rows)


class Tables:
    """Typed lookups over the frozen snapshots. Missing cells return None."""

    def __init__(self, raw):
        self.na_emp = {}    # (year, nace, na_item, unit) -> value
        self.na_out = {}    # (year, nace, na_item, unit) -> value
        self.lfs_u = {}     # (year, nace, wstatus, worktime) -> usual weekly hours
        self.lfs_a = {}     # actual weekly hours
        self.lfs_pt = {}    # (year, nace, worktime) -> thousand persons
        self.slack = {}     # (year, wstatus) -> thousand persons
        self.flags = {}     # (table, key) -> status flag
        for coords, v, flag in jsonstat.iter_cells(raw["na_employment_hours"][0]):
            k = (int(coords["time"]), coords["nace_r2"], coords["na_item"], coords["unit"])
            self.na_emp[k] = v
            self.flags[("na_emp", k)] = flag
        for coords, v, flag in jsonstat.iter_cells(raw["na_output"][0]):
            k = (int(coords["time"]), coords["nace_r2"], coords["na_item"], coords["unit"])
            self.na_out[k] = v
            self.flags[("na_out", k)] = flag
        for name, target in (("lfs_usual_hours", self.lfs_u), ("lfs_actual_hours", self.lfs_a)):
            for coords, v, flag in jsonstat.iter_cells(raw[name][0]):
                target[(int(coords["time"]), coords["nace_r2"], coords["wstatus"], coords["worktime"])] = v
        for coords, v, _ in jsonstat.iter_cells(raw["lfs_parttime_persons"][0]):
            self.lfs_pt[(int(coords["time"]), coords["nace_r2"], coords["worktime"])] = v
        for coords, v, _ in jsonstat.iter_cells(raw["lfs_slack"][0]):
            self.slack[(int(coords["time"]), coords["wstatus"])] = v

    def is_provisional(self, year):
        return any(f == "p" for (t, k), f in self.flags.items() if t == "na_emp" and k[0] == year)
