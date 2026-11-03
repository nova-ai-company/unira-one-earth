"""Minimal JSON-stat 2.0 reader for Eurostat dissemination API responses (stdlib only)."""
import json
from itertools import product


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def iter_cells(doc):
    """Yield (coords: dict, value, status) for every non-missing cell.

    JSON-stat stores a flattened row-major array; the position of a cell is
    sum(index_k * stride_k) with strides computed from `size`.
    """
    ids, sizes = doc["id"], doc["size"]
    labels = []
    for dim in ids:
        index = doc["dimension"][dim]["category"]["index"]
        ordered = sorted(index.items(), key=lambda kv: kv[1])
        labels.append([code for code, _ in ordered])
    values, status = doc.get("value", {}), doc.get("status", {})
    if isinstance(values, list):  # dense form
        values = {str(i): v for i, v in enumerate(values) if v is not None}
    strides = [1] * len(sizes)
    for i in range(len(sizes) - 2, -1, -1):
        strides[i] = strides[i + 1] * sizes[i + 1]
    for combo in product(*[range(s) for s in sizes]):
        pos = str(sum(c * st for c, st in zip(combo, strides)))
        if pos in values:
            coords = {dim: labels[k][combo[k]] for k, dim in enumerate(ids)}
            yield coords, values[pos], status.get(pos, "")


def dataset_meta(doc):
    ext = doc.get("extension", {})
    return {"label": doc.get("label", ""), "updated": doc.get("updated", ""),
            "dataset_id": ext.get("id", ""),
            "datastructure_version": ext.get("datastructure", {}).get("version", "")}
