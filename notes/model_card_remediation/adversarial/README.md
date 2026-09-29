# Adversarial review of the two-card remediation

Reviewed PR #36 at commit `2736553bf76293d6b14caaa5c3dcfee363235b34` on September 28, 2026,
covering the fixes for issues #30–#32 and their parent badge-rendering change in PR #29.
Independent source checks found no additional reproducible factual defect in either YAML.
The checkpoint-run records, prediction-level evaluation and SubCell split reconciliation
remain external evidence requests tracked by #33–#35.

## Confirmed findings and prepared fixes

| Finding | Evidence | Fix |
|---|---|---|
| [P2: portfolio rebuild restores archived scores](issues/01-portfolio-freshness.md) | The normal Make target excluded the new after-evaluations and overwrote all four current hybrid SVGs. Their hashes then failed the card renderer's check. | Select current YAML hashes, include revised evaluations, reject missing current hybrid results and ambiguous collisions, and keep current dashboards separate from archives. |
| [P2: HTML loses metadata and overflows narrow screens](issues/02-html-metadata.md) | SubCell lost its dataset unit and schema version; DenseNet lost schema version, license name and model category. Both pages exceeded a 390-pixel viewport by over 500 pixels. | Render the omitted metadata and license terms, add responsive grids and a viewport declaration, and regenerate both pages. |
| [P2: read-only detection requires an absent PAT](issues/03-mention-token.md) | PR #29 run 36223938067 failed before executing detection with `Input required and not supplied: github-token`. PR #36 used the same configuration and its detection check also failed. | Use the built-in GitHub token with explicit read-only permissions for detection. The privileged response job is unchanged. |

All issue texts above are local publication drafts at preparation. This document does not
track later GitHub state. The three new fixes are prepared locally pending exact outbound
approval; existing issues #30–#32 should close only after the reviewed changes reach main.

## Verification

- `make test` passed schema generation, unit tests and schema examples using the compatible
  local Python 3.11 environment: 34 unit tests ran, 33 passed and one existing optional-package
  test was skipped. The previously published PR also passed its Python 3.12 test and rubric gate.
- The actual repository `make compare-portfolio` command, with temporary output directories,
  produced DenseNet 47/50 and 67/84, SubCell 45/50 and 62/84. Every badge matched its current
  YAML SHA-256. Hash snapshots confirmed all 115 existing evaluation artifacts were unchanged.
- Regression checks cover stale inputs, input-order-independent newest selection, conflicting
  same-timestamp scores, filename collisions, missing-current failure and the actual Make target.
- Headless Chromium loaded two embedded badges per page and measured zero document overflow
  at both 390- and 1360-pixel viewports; see [browser measurements](browser-checks.json).
- Mention detection was exercised offline for ordinary, unauthorized and authorized PR events
  and manual issue/PR lookups. Mocks provide read endpoints only; no bot was invoked.
- The DenseNet inference example was checked structurally against timm's revision-aware loader.
  The SubCell decoder was executed with notebook-shaped output covering all ten labels. The
  pinned dataset hash and split intersections were independently recomputed. Neither model
  was run, and no accuracy measurement or fresh semantic evaluation is claimed.
- Both YAMLs, the base schema, saved remediation evaluations and existing badge scores remain
  byte-for-byte unchanged by this follow-up. No original-run evidence was fabricated.

## Scope of the portfolio repair

`make compare-portfolio` is still a render-only command. It reads archived and revised reports,
accepts only hashes matching current YAML bytes, and writes current dashboards under
`data/evaluation/current/portfolio/`. Optional newly evaluated reports can be staged under
`data/evaluation/current/<cohort>/{rubric10,rubric20}/`. Explicit archived-report rendering
without `--current-only` remains available. A missing current hybrid score stops rendering;
it does not silently reuse an old judgment or delete an archived SVG.

An initial broader proposal also changed the scheduled audit's evaluation destinations and
existing automatic PR description. Automatic approval review rejected that proposal because
it altered persistent outbound automation beyond the approved content. The accepted narrower
repair resolves the reproduced overwrite without editing the scheduled workflow. That workflow
and its publishing behavior remain unchanged; no further scheduling change is needed for these
three fixes.

The merge proposal retargets PR #36 to main because its current base is the unmerged PR #29
branch. A merge commit preserves the parent commits, allowing GitHub to recognize PR #29 as
indirectly merged. Branch cleanup must follow verification that both reviewed tips are contained
in main and the PRs are merged. See [GitHub's merge documentation](https://docs.github.com/en/pull-requests/reference/pull-request-merges).
