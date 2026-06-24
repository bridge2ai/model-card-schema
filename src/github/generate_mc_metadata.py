#!/usr/bin/env python3
"""
Generate provenance metadata for a Model Card produced by @mcassistant.

For every Model Card YAML the assistant writes, emit a sibling
`{stem}_metadata.yaml` with:
  - SHA-256 hashes of the Model Card, input sources, schema, and prompts
  - Generation settings (model id, temperature, max tokens)
  - Git commit + dirty flag
  - Processing environment (Python version, platform)
  - GitHub issue / PR numbers

Used by `.github/workflows/mc_assistant_create.md` step 6 and the edit workflow's
step 5 (when sources change).

Usage:
    python src/github/generate_mc_metadata.py \\
        --mc-file data/model_cards_assistant/mymodel_model_card.yaml \\
        --model-name mymodel \\
        --input-dir data/model_cards_assistant/inputs/mymodel \\
        --issue-number 42

    # URL-based mode
    python src/github/generate_mc_metadata.py \\
        --mc-file data/model_cards_assistant/mymodel_model_card.yaml \\
        --model-name mymodel \\
        --input-sources https://huggingface.co/x/y https://github.com/x/y \\
        --issue-number 42
"""
from __future__ import annotations

import argparse
import hashlib
import os
import platform
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA = REPO_ROOT / "src/model_card_schema/schema/model_card_schema.yaml"
DEFAULT_PROMPTS = [
    REPO_ROOT / ".github/workflows/mc_assistant_create.md",
    REPO_ROOT / ".github/workflows/mc_assistant_edit.md",
    REPO_ROOT / ".goosehints",
]

# Default model / temperature settings — should match what the workflow doc declares.
DEFAULT_MODEL_NAME = "claude-sonnet-4-5-20250929"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_MAX_TOKENS = 16000


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_of_string(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def hash_directory(path: Path) -> dict[str, str]:
    """Hash every regular file under `path` (relative to it)."""
    hashes: dict[str, str] = {}
    if not path.exists() or not path.is_dir():
        return hashes
    for p in sorted(path.rglob("*")):
        if p.is_file():
            hashes[str(p.relative_to(path))] = sha256_of(p)
    return hashes


def git_commit() -> dict[str, str | bool]:
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
        dirty = bool(subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=REPO_ROOT, text=True
        ).strip())
        return {"sha": sha, "dirty": dirty}
    except Exception:
        return {"sha": "unknown", "dirty": False}


def build_metadata(
    mc_file: Path,
    model_name: str,
    input_dir: Path | None,
    input_sources: list[str] | None,
    issue_number: int | None,
    pr_number: int | None,
    schema_path: Path,
    prompt_paths: list[Path],
    llm_model: str,
    temperature: float,
    max_tokens: int,
) -> dict:
    now = datetime.now(timezone.utc).isoformat()

    inputs: dict = {}
    if input_dir is not None:
        inputs["mode"] = "file"
        inputs["input_dir"] = str(input_dir)
        inputs["file_hashes"] = hash_directory(input_dir)
    elif input_sources:
        inputs["mode"] = "url"
        inputs["urls"] = list(input_sources)
        inputs["url_hashes"] = {u: sha256_of_string(u) for u in input_sources}
    else:
        inputs["mode"] = "unknown"

    prompt_hashes = {}
    for pp in prompt_paths:
        if pp.exists():
            prompt_hashes[str(pp.relative_to(REPO_ROOT))] = sha256_of(pp)

    metadata = {
        "extraction": {
            "extraction_type": "github_assistant_claude_code",
            "performed_by": "mcassistant",
            "wrapper_script": "src/github/generate_mc_metadata.py",
            "version": "1.0.0",
            "extraction_id": str(uuid.uuid4()),
            "timestamp": now,
        },
        "model_card": {
            "name": model_name,
            "file": str(mc_file),
            "file_hash": sha256_of(mc_file),
        },
        "inputs": inputs,
        "schema": {
            "path": str(schema_path.relative_to(REPO_ROOT)) if schema_path.is_absolute() else str(schema_path),
            "hash": sha256_of(schema_path) if schema_path.exists() else None,
        },
        "prompts": prompt_hashes,
        "model": {
            "provider": "anthropic",
            "name": llm_model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        },
        "git": git_commit(),
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "machine": platform.machine(),
            "node": os.uname().nodename if hasattr(os, "uname") else platform.node(),
        },
        "github": {
            "issue_number": issue_number,
            "pr_number": pr_number,
        },
    }
    return metadata


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mc-file", type=Path, required=True, help="The generated Model Card YAML")
    p.add_argument("--model-name", required=True, help="Short model name (used in metadata.model_card.name)")

    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--input-dir", type=Path, help="Directory containing input source files (file mode)")
    src.add_argument("--input-sources", nargs="+", help="URLs used as source documentation (URL mode)")

    p.add_argument("--issue-number", type=int, default=None)
    p.add_argument("--pr-number", type=int, default=None)
    p.add_argument("--schema-path", type=Path, default=DEFAULT_SCHEMA)
    p.add_argument("--prompt-path", action="append", type=Path,
                   help="Prompt file to hash. Repeat for multiple. Defaults to the workflow + goosehints.")
    p.add_argument("--llm-model", default=DEFAULT_MODEL_NAME)
    p.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    p.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    p.add_argument("--output", type=Path, default=None,
                   help="Output path. Defaults to <stem>_metadata.yaml alongside --mc-file.")

    args = p.parse_args(argv)

    if not args.mc_file.exists():
        print(f"Model Card file not found: {args.mc_file}", file=sys.stderr)
        return 2

    prompt_paths = args.prompt_path or DEFAULT_PROMPTS

    metadata = build_metadata(
        mc_file=args.mc_file,
        model_name=args.model_name,
        input_dir=args.input_dir,
        input_sources=args.input_sources,
        issue_number=args.issue_number,
        pr_number=args.pr_number,
        schema_path=args.schema_path,
        prompt_paths=prompt_paths,
        llm_model=args.llm_model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )

    output = args.output or args.mc_file.with_name(args.mc_file.stem + "_metadata.yaml")
    output.write_text(yaml.safe_dump(metadata, sort_keys=False, default_flow_style=False))
    print(f"Wrote metadata to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
