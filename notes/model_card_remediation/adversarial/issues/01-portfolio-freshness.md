# Prevent portfolio rebuilds from replacing current badges with archived scores

Adversarial review of PR #36 at commit `2736553` found that `make compare-portfolio` reads the older cohort evaluations but excludes the revised two-card evaluations. Rebuilding therefore overwrites all four current DenseNet/SubCell hybrid SVGs with scores bound to the old YAMLs. README badges show the old scores, and regenerated card HTML omits them because their input hashes no longer match.

The prepared fix selects reports whose recorded SHA-256 matches the current YAML, includes the remediation's after-evaluations, and writes current dashboards separately from archived dashboards. Missing current hybrid evaluations fail the rebuild before badges are written. Existing evaluation JSONs remain unchanged by this render-only command.

Acceptance: exercise the actual Make target with archived and revised inputs; verify all four current badge hashes and scores, deterministic selection, stale-input failure, and unchanged archive bytes. Close after the reviewed fix is merged into main.
