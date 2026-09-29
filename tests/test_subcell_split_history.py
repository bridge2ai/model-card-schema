"""Check audit boundaries: verified bytes, identifier absence and exact split comparisons."""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("history_audit", ROOT / "scripts/audit_subcell_split_history.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def row(stage, sequence="AaBb", name="P1", label=0):
    return audit.checked_row(name, sequence, label, stage)


class AuditTests(unittest.TestCase):
    def test_existing_corrupt_cache_fails_without_downloading(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.csv"
            path.write_bytes(b"bad!")
            artifact = {"cache_filename": path.name, "size": 4, "sha256": hashlib.sha256(b"good").hexdigest()}
            with patch.object(audit.urllib.request, "urlopen") as download:
                with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                    audit.cached_artifact(artifact, path.parent, download=True)
                download.assert_not_called()

    def test_missing_cache_requires_explicit_download_and_rejects_wrong_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            artifact = {
                "cache_filename": "artifact.csv", "size": 4,
                "sha256": hashlib.sha256(b"good").hexdigest(),
                "download_url": "https://huggingface.co/datasets/example/data/resolve/revision/data.csv",
            }
            with patch.object(audit.urllib.request, "urlopen") as download:
                with self.assertRaises(FileNotFoundError):
                    audit.cached_artifact(artifact, cache, download=False)
                download.assert_not_called()
            with patch.object(audit.urllib.request, "urlopen", return_value=io.BytesIO(b"bad!")):
                with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                    audit.cached_artifact(artifact, cache, download=True)
            self.assertEqual(list(cache.iterdir()), [])

    def test_missing_ids_are_unknown_and_aa_overlap_is_distinct_from_sa(self):
        splits = {"train": [row("train", "CaDb", None)], "valid": [row("valid", "AaBb", None)], "test": [row("test", "AcBd", None)]}
        result = audit.summarize_snapshot(splits)
        self.assertIsNone(result["splits"]["train"]["unique"]["ID"])
        self.assertIsNone(result["overlaps"]["valid/test"]["ID"])
        self.assertEqual(result["overlaps"]["valid/test"]["AA"]["shared_unique"], 1)
        self.assertEqual(result["overlaps"]["valid/test"]["SA"]["shared_unique"], 0)

    def test_multiset_comparison_preserves_duplicate_multiplicity(self):
        before = {stage: [row(stage), row(stage)] for stage in audit.STAGES}
        after = {stage: [row(stage, name=None)] for stage in audit.STAGES}
        result = audit.compare_snapshots(before, after)
        for stage in audit.STAGES:
            self.assertEqual(result[stage]["normalized_fields"], ["seq", "label", "stage"])
            self.assertFalse(result[stage]["multiset_equal"])
            self.assertEqual(result[stage]["removed_records"], 1)

    def test_masking_uses_strict_less_than_threshold_and_preserves_amino_acids(self):
        before = {stage: [audit.checked_row("P1", "AaBbCc", 0, stage, [69.99, 70, 70.01])] for stage in audit.STAGES}
        after = {stage: [row(stage, "A#BbCc")] for stage in audit.STAGES}
        result = audit.masking_proof(before, after)
        for stage in audit.STAGES:
            self.assertTrue(result["splits"][stage]["all_rows_reconstructed"])
            self.assertEqual(result["splits"][stage]["changed_structural_positions"], 1)
        after["test"][0]["seq"] = "A#B#Cc"
        self.assertFalse(audit.masking_proof(before, after)["splits"]["test"]["all_rows_reconstructed"])

    def test_fractional_label_csv_is_excluded_without_inventing_task_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "temporary.csv"
            path.write_text("Sequence,label,stage\nABCD,10.15988,train\n")
            rows, details = audit.read_csv(path)
            self.assertIsNone(rows)
            self.assertTrue(details["excluded"])
            self.assertEqual(details["fields"], ["Sequence", "label", "stage"])
            self.assertEqual(details["fractional_label_rows"], 1)
            self.assertIn("Task identity is not inferred", details["reason"])
            path.write_text("protein,label,stage\nAaBb,0.5,train\n")
            with self.assertRaisesRegex(ValueError, "integer classification label"):
                audit.read_csv(path)

    @unittest.skipUnless(importlib.util.find_spec("lmdb"), "optional python-lmdb package not installed")
    def test_lmdb_reader_accepts_json_and_rejects_non_json_values(self):
        import lmdb

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.mdb"
            with lmdb.open(str(path), subdir=False, map_size=1024 * 1024) as env:
                with env.begin(write=True) as transaction:
                    transaction.put(b"length", b"1")
                    transaction.put(b"0", json.dumps({"name": "P1", "seq": "AaBb", "label": 0}).encode())
            rows, _ = audit.read_lmdb(path, "train")
            self.assertEqual(rows, [row("train")])
            with lmdb.open(str(path), subdir=False, map_size=1024 * 1024) as env:
                with env.begin(write=True) as transaction:
                    transaction.put(b"0", b"\x80\x04untrusted non-JSON payload")
            with self.assertRaises((ValueError, UnicodeError)):
                audit.read_lmdb(path, "train")


if __name__ == "__main__":
    unittest.main()
