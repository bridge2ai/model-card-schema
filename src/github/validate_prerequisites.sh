#!/usr/bin/env bash
# Validate Prerequisites for @mcassistant Model Card Generation
#
# Called by the GitHub Action workflow (see .github/workflows/mc_assistant_create.md
# step 0) before attempting to generate a Model Card. Fails fast if any required
# resource is missing — saving Anthropic API costs and surfacing the issue back to
# the user in the GitHub issue.
#
# Usage:
#   ./src/github/validate_prerequisites.sh --model <model-name> --mode file
#   ./src/github/validate_prerequisites.sh --model <model-name> --mode url --urls "url1 url2 url3"
#
# Exit codes:
#   0  all prerequisites OK
#   1  one or more prerequisites missing
#   2  bad arguments

set -euo pipefail

MODEL=""
MODE=""
URLS=""

usage() {
  cat <<EOF
Usage: $0 --model <model-name> --mode <file|url> [--urls "url1 url2 url3"]

Options:
  --model NAME    Short model name (used to locate input files)
  --mode MODE     'file' or 'url'
  --urls URLS     Space-separated URLs (required when --mode url)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model) MODEL="$2"; shift 2 ;;
    --mode)  MODE="$2"; shift 2 ;;
    --urls)  URLS="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ -z "$MODEL" || -z "$MODE" ]]; then
  usage
  exit 2
fi

if [[ "$MODE" != "file" && "$MODE" != "url" ]]; then
  echo "Invalid mode: $MODE (must be 'file' or 'url')" >&2
  exit 2
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCHEMA="$REPO_ROOT/src/model_card_schema/schema/model_card_schema.yaml"

ERRORS=()
WARNINGS=()

ok()    { printf '  ✅ %s\n' "$1"; }
fail()  { printf '  ❌ %s\n' "$1"; ERRORS+=("$1"); }
warn()  { printf '  ⚠️  %s\n' "$1"; WARNINGS+=("$1"); }

printf '🔍 Prerequisites check for @mcassistant (model=%s, mode=%s)\n' "$MODEL" "$MODE"
printf '═══════════════════════════════════════════════════════════\n'

# --- 1. Schema file ---
printf '\nSchema file:\n'
if [[ -f "$SCHEMA" ]]; then
  ok "Schema exists: $SCHEMA"
else
  fail "Schema file missing: $SCHEMA"
fi

# --- 2. Prompt / workflow files ---
printf '\nPrompt files:\n'
for f in \
  ".github/workflows/mc_assistant_create.md" \
  ".github/workflows/mc_assistant_edit.md" \
  ".goosehints"
do
  if [[ -f "$REPO_ROOT/$f" ]]; then
    ok "Present: $f"
  else
    fail "Missing: $f"
  fi
done

# --- 3. Input sources ---
printf '\nInput sources:\n'
if [[ "$MODE" == "file" ]]; then
  INPUT_DIR="$REPO_ROOT/data/model_cards_assistant/inputs/$MODEL"
  if [[ -d "$INPUT_DIR" ]]; then
    N=$(find "$INPUT_DIR" -type f | wc -l | tr -d ' ')
    if [[ "$N" -gt 0 ]]; then
      ok "Input dir has $N file(s): $INPUT_DIR"
    else
      fail "Input dir is empty: $INPUT_DIR"
    fi
  else
    fail "Input dir not found: $INPUT_DIR"
  fi
else
  if [[ -z "$URLS" ]]; then
    fail "URL mode requires --urls"
  else
    for u in $URLS; do
      if [[ "$u" =~ ^https?:// ]]; then
        ok "URL well-formed: $u"
      else
        fail "URL doesn't start with http(s): $u"
      fi
    done
  fi
fi

# --- 4. Python deps ---
printf '\nPython dependencies:\n'
for pkg in yaml linkml linkml_runtime; do
  if python3 -c "import $pkg" >/dev/null 2>&1; then
    ok "import $pkg"
  else
    fail "import $pkg (try: poetry install)"
  fi
done

# --- 5. Anthropic API key (only for non-Claude-Code env) ---
printf '\nAPI credentials:\n'
if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
  ok "ANTHROPIC_API_KEY is set"
else
  warn "ANTHROPIC_API_KEY not set (OK if running inside Claude Code, required for external API calls)"
fi

# --- 6. Output directory ---
printf '\nOutput directory:\n'
OUT_DIR="$REPO_ROOT/data/model_cards_assistant"
if [[ -d "$OUT_DIR" ]]; then
  ok "Output dir exists: $OUT_DIR"
else
  mkdir -p "$OUT_DIR"
  ok "Output dir created: $OUT_DIR"
fi

# --- Summary ---
printf '\n═══════════════════════════════════════════════════════════\n'
if [[ ${#ERRORS[@]} -eq 0 ]]; then
  printf '✅ All prerequisites satisfied'
  if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    printf ' (%d warning(s))' "${#WARNINGS[@]}"
  fi
  printf '\n'
  exit 0
else
  printf '❌ %d prerequisite(s) failed:\n' "${#ERRORS[@]}"
  for e in "${ERRORS[@]}"; do printf '   • %s\n' "$e"; done
  exit 1
fi
