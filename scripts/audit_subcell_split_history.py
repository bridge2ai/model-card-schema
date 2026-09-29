#!/usr/bin/env python3
"""Audit pinned SubCell dataset history without inference or training.

Read cache files by default. --download permits downloading missing public
Hugging Face artifacts listed in the manifest; existing corrupt files fail.
LMDB values are decoded as JSON only, never as pickle.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import itertools
import json
import math
import platform
import tempfile
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

STAGES = ("train", "valid", "test")


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_file(path, artifact):
    if path.stat().st_size != artifact["size"]:
        raise ValueError(f"Size mismatch: {path.name}")
    digest = sha256_file(path)
    if digest != artifact["sha256"]:
        raise ValueError(f"SHA-256 mismatch: {path.name}")
    return digest


def cached_artifact(artifact, cache_dir, download):
    filename = artifact["cache_filename"]
    if not isinstance(filename, str) or Path(filename).name != filename or filename in ("", ".", ".."):
        raise ValueError("cache_filename must be a plain filename")
    path = cache_dir / filename
    if not path.exists():
        if not download:
            raise FileNotFoundError(f"Missing cached artifact: {path}; use --download explicitly")
        url = artifact["download_url"]
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != "https" or parsed.hostname != "huggingface.co" or parsed.username or parsed.password:
            raise ValueError("Downloads must use public HTTPS huggingface.co URLs")
        cache_dir.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=cache_dir, delete=False) as stream:
                temporary = Path(stream.name)
                with urllib.request.urlopen(url, timeout=120) as response:
                    for block in iter(lambda: response.read(1024 * 1024), b""):
                        stream.write(block)
            verify_file(temporary, artifact)
            temporary.replace(path)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
    verify_file(path, artifact)
    return path


def checked_row(name, sequence, label, stage, plddt=None):
    if stage not in STAGES:
        raise ValueError(f"Unknown split: {stage!r}")
    if name is not None and (not isinstance(name, str) or not name.strip()):
        raise ValueError("Protein identifier must be a nonempty string")
    if isinstance(label, str) and label in {str(i) for i in range(10)}:
        label = int(label)
    if type(label) is not int or not 0 <= label <= 9:
        raise ValueError(f"Expected an integer classification label in 0..9: {label!r}")
    if (
        not isinstance(sequence, str) or not sequence or len(sequence) % 2
        or not all("A" <= c <= "Z" for c in sequence[::2])
        or not all("a" <= c <= "z" or c == "#" for c in sequence[1::2])
    ):
        raise ValueError("Expected an even-length alternating amino-acid/structural string")
    row = {"name": name, "seq": sequence, "label": label, "stage": stage}
    if plddt is not None:
        if not isinstance(plddt, list) or len(plddt) != len(sequence) // 2:
            raise ValueError("pLDDT length does not match the residue count")
        if any(type(v) not in (int, float) or not math.isfinite(v) or not 0 <= v <= 100 for v in plddt):
            raise ValueError("pLDDT values must be finite numbers in 0..100")
        row["plddt"] = plddt
    return row


def read_lmdb(path, stage):
    import lmdb

    rows = []
    with lmdb.open(str(path), readonly=True, lock=False, subdir=False) as env:
        with env.begin() as transaction:
            length = transaction.get(b"length")
            if length is None or not length.isdigit():
                raise ValueError(f"Missing/invalid LMDB length in {path.name}")
            length = int(length)
            keys = {key for key, _ in transaction.cursor()}
            expected = {str(i).encode("ascii") for i in range(length)}
            if keys - {b"length", b"info"} != expected:
                raise ValueError(f"Unexpected or missing LMDB record keys in {path.name}")
            for index in range(length):
                record = json.loads(transaction.get(str(index).encode("ascii")))
                if not isinstance(record, dict) or set(record) not in (
                    {"name", "seq", "label"}, {"name", "seq", "label", "plddt"},
                ):
                    raise ValueError(f"Unexpected LMDB record shape at {path.name}:{index}")
                rows.append(checked_row(record["name"], record["seq"], record["label"], stage, record.get("plddt")))
    if not rows:
        raise ValueError(f"Empty LMDB artifact: {path.name}")
    if len({"plddt" in row for row in rows}) != 1:
        raise ValueError("Inconsistent pLDDT fields within one artifact")
    return rows, {"format": "lmdb_json", "rows": len(rows), "metadata_keys": sorted(k.decode() for k in keys - expected)}


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        records = list(reader)
    if not records or any(None in row or any(value is None for value in row.values()) for row in records):
        raise ValueError(f"Empty or malformed CSV: {path.name}")
    if fields == ["Sequence", "label", "stage"]:
        labels = [float(row["label"]) for row in records]
        if any(not math.isfinite(value) for value in labels) or not any(not value.is_integer() for value in labels):
            raise ValueError("Unexpected labels in the temporary uppercase-Sequence CSV")
        return None, {
            "format": "csv", "excluded": True, "fields": fields, "rows": len(records),
            "reason": "Temporary artifact uses Sequence and fractional labels; it does not satisfy the audited 10-class SA record format. Task identity is not inferred.",
            "stage_counts": dict(sorted(Counter(row["stage"] for row in records).items())),
            "fractional_label_rows": sum(not value.is_integer() for value in labels),
            "label_examples": [row["label"] for row in records[:3]],
        }
    formats = {
        ("name", "seq", "label", "stage"): "seq",
        ("sequence", "label", "stage"): "sequence",
        ("protein", "label", "stage"): "protein",
    }
    sequence_field = formats.get(tuple(fields or []))
    if sequence_field is None:
        raise ValueError(f"Unexpected CSV fields: {fields}")
    rows = [checked_row(row.get("name"), row[sequence_field], row["label"], row["stage"]) for row in records]
    return rows, {"format": "csv", "fields": fields, "rows": len(rows)}


KEYS = {"SA": lambda row: row["seq"], "AA": lambda row: row["seq"][::2], "ID": lambda row: row["name"]}


def summarize_snapshot(by_stage):
    summary = {"splits": {}, "overlaps": {}}
    for stage in STAGES:
        rows = by_stage[stage]
        if not rows:
            raise ValueError(f"Snapshot is missing split: {stage}")
        present_ids = {row["name"] is not None for row in rows}
        if len(present_ids) != 1:
            raise ValueError("A split mixes missing and present identifiers")
        counts = {key: len({fn(row) for row in rows}) if key != "ID" or True in present_ids else None for key, fn in KEYS.items()}
        summary["splits"][stage] = {
            "rows": len(rows), "unique": counts,
            "excess_repeated_records": {key: len(rows) - count if count is not None else None for key, count in counts.items()},
            "class_counts": dict(sorted(Counter(row["label"] for row in rows).items())),
        }
    for left, right in itertools.combinations(STAGES, 2):
        pair = {}
        for key, fn in KEYS.items():
            if key == "ID" and any(row["name"] is None for stage in (left, right) for row in by_stage[stage]):
                pair[key] = None
                continue
            shared = {fn(row) for row in by_stage[left]} & {fn(row) for row in by_stage[right]}
            pair[key] = {
                "shared_unique": len(shared),
                "affected_rows": {stage: sum(fn(row) in shared for row in by_stage[stage]) for stage in (left, right)},
            }
        summary["overlaps"][f"{left}/{right}"] = pair
    return summary


def compare_snapshots(before, after):
    result = {}
    for stage in STAGES:
        left, right = before[stage], after[stage]
        fields = ["seq", "label", "stage"]
        if all(row["name"] is not None for row in left + right):
            fields.insert(0, "name")
        a = [tuple(row[field] for field in fields) for row in left]
        b = [tuple(row[field] for field in fields) for row in right]
        ca, cb = Counter(a), Counter(b)
        result[stage] = {
            "normalized_fields": fields, "ordered_rows_equal": a == b, "multiset_equal": ca == cb,
            "removed_records": sum((ca - cb).values()), "added_records": sum((cb - ca).values()),
        }
    return result


def masking_proof(before, after, threshold=70):
    result = {"threshold": threshold, "rule": "Replace only the structural character with # when pLDDT < threshold", "splits": {}}
    for stage in STAGES:
        old, new = before[stage], after[stage]
        if len(old) != len(new) or any("plddt" not in row for row in old):
            raise ValueError("Masking comparison requires equally sized rows with original pLDDT")
        alignment = all(a["name"] == b["name"] and a["label"] == b["label"] and a["seq"][::2] == b["seq"][::2] for a, b in zip(old, new))
        matches = changes = changed_rows = 0
        changed_confidences = []
        for a, b in zip(old, new):
            reconstructed = "".join(aa + (st if confidence >= threshold else "#") for aa, st, confidence in zip(a["seq"][::2], a["seq"][1::2], a["plddt"]))
            matches += reconstructed == b["seq"]
            changed_rows += a["seq"] != b["seq"]
            for old_token, new_token, confidence in zip(a["seq"][1::2], b["seq"][1::2], a["plddt"]):
                if old_token != new_token:
                    changes += 1
                    changed_confidences.append(confidence)
        result["splits"][stage] = {
            "rows": len(old), "same_order_ID_AA_label": alignment,
            "reconstructed_rows_matching": matches, "all_rows_reconstructed": alignment and matches == len(old),
            "changed_SA_rows": changed_rows, "changed_structural_positions": changes,
            "changed_plddt_range": [min(changed_confidences), max(changed_confidences)] if changed_confidences else None,
        }
    return result


def write_shared_ids(path, snapshot_id, by_stage):
    """Write IDs and sequence hashes from the latest snapshot retaining names."""
    records = []
    for left, right in itertools.combinations(STAGES, 2):
        maps = {}
        for stage in (left, right):
            mapping = defaultdict(list)
            for row in by_stage[stage]:
                mapping[row["name"]].append(row)
            maps[stage] = mapping
        for identifier in sorted(maps[left].keys() & maps[right].keys()):
            item = {"snapshot": snapshot_id, "left_split": left, "right_split": right, "protein_id": identifier}
            for side, stage in (("left", left), ("right", right)):
                rows = maps[stage][identifier]
                item[side + "_labels"] = ";".join(str(label) for label in sorted({row["label"] for row in rows}))
                for key in ("SA", "AA"):
                    item[side + "_" + key + "_sha256"] = ";".join(sorted({hashlib.sha256(KEYS[key](row).encode()).hexdigest() for row in rows}))
            records.append(item)
    fields = ["snapshot", "left_split", "right_split", "protein_id", "left_labels", "left_SA_sha256", "left_AA_sha256", "right_labels", "right_SA_sha256", "right_AA_sha256"]
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    return len(records)


def run_audit(manifest_path, cache_dir, output_dir, download=False):
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if not isinstance(manifest.get("artifacts"), dict) or not manifest.get("snapshots"):
        raise ValueError("Manifest requires artifacts mapping and snapshots list")
    parsed, artifact_results = {}, {}
    for key, artifact in manifest["artifacts"].items():
        path = cached_artifact(artifact, cache_dir, download)
        if path.suffix == ".mdb":
            rows, details = read_lmdb(path, artifact["path"].split("/")[0])
        elif path.suffix == ".csv":
            rows, details = read_csv(path)
        else:
            raise ValueError(f"Unsupported artifact suffix: {path.suffix}")
        parsed[key] = rows
        artifact_results[key] = {"sha256": artifact["sha256"], "size": artifact["size"], "path": artifact["path"], "first_revision": artifact["first_revision"], "first_date": artifact["first_date"], **details}
    snapshots = sorted(manifest["snapshots"], key=lambda item: item["date"])
    if len({item["id"] for item in snapshots}) != len(snapshots):
        raise ValueError("Duplicate snapshot IDs")
    groups, summaries, used = {}, {}, set()
    for snapshot in snapshots:
        group = {stage: [] for stage in STAGES}
        for split, key in snapshot["artifact_keys"].items():
            if split not in (*STAGES, "all") or key not in parsed or parsed[key] is None:
                raise ValueError(f"Invalid snapshot artifact: {snapshot['id']} {split} {key}")
            used.add(key)
            for row in parsed[key]:
                if split != "all" and row["stage"] != split:
                    raise ValueError("Artifact split does not match snapshot declaration")
                group[row["stage"]].append(row)
        groups[snapshot["id"]] = group
        summaries[snapshot["id"]] = {"date": snapshot["date"], "revision": snapshot["revision"], "format": snapshot["format"], "artifact_keys": snapshot["artifact_keys"], **summarize_snapshot(group)}
    if used != {key for key, rows in parsed.items() if rows is not None}:
        raise ValueError("Some classification artifacts are not assigned to snapshots")
    transitions = []
    masks = []
    for first, second in zip(snapshots, snapshots[1:]):
        before, after = groups[first["id"]], groups[second["id"]]
        transitions.append({"from": first["id"], "to": second["id"], "splits": compare_snapshots(before, after)})
        if all("plddt" in row for rows in before.values() for row in rows) and all("plddt" not in row for rows in after.values() for row in rows):
            masks.append({"from": first["id"], "to": second["id"], **masking_proof(before, after)})
    import lmdb

    result = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(), "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "script_sha256": sha256_file(Path(__file__)), "python_version": platform.python_version(),
            "python_lmdb_version": importlib.metadata.version("lmdb"), "lmdb_library_version": list(lmdb.version()),
            "dataset_repository": manifest["dataset_repository"], "audited_head": manifest["audited_head"],
        },
        "method": "Exact full SA, AA characters at seq[::2], and protein identifier comparisons; no truncation, clustering, inference, or score attribution.",
        "artifacts": artifact_results, "snapshots": summaries, "transitions": transitions, "masking_proofs": masks,
        "timeline": [{key: snapshot[key] for key in ("id", "date", "revision", "format")} for snapshot in snapshots],
        "earliest_observed_snapshot": snapshots[0]["id"], "latest_observed_snapshot": snapshots[-1]["id"],
        "limitations": ["Observed historical dataset overlap does not bind these splits to the checkpoint's reported accuracy.", "Missing identifier fields are unknown, not evidence of zero identifier overlap.", "Fractional-label temporary CSV is excluded by observed format; its task identity is not inferred."],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    named = [snapshot for snapshot in snapshots if all(row["name"] is not None for rows in groups[snapshot["id"]].values() for row in rows)]
    if named:
        latest = named[-1]["id"]
        result["shared_ids_export"] = {"snapshot": latest, "file": "shared_ids.csv", "rows": write_shared_ids(output_dir / "shared_ids.csv", latest, groups[latest])}
    (output_dir / "audit.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--download", action="store_true", help="Download missing manifest-listed public artifacts; verify bytes before use")
    args = parser.parse_args()
    result = run_audit(args.manifest, args.cache_dir, args.output_dir, args.download)
    print(f"Verified {len(result['artifacts'])} artifacts; audited {len(result['snapshots'])} snapshots. Results: {args.output_dir / 'audit.json'}")


if __name__ == "__main__":
    main()
