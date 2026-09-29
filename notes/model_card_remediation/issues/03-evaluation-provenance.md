# Bind card badges to evaluated inputs and render the added documentation

Editing a model card leaves its old badges in place, and the renderer previously displayed every matching filename. The supplied analysis also reports two unverifiable archived semantic input hashes. Added usage, benchmark, evaluation and reproducibility fields were partly omitted from HTML.

Fix prepared locally: bind new SVG badges to the evaluated YAML SHA-256, show only matching badges, explain omitted archived/unverified scores, and render the missing structured sections. Preserve the supplied figure and archived semantic evaluations. Produce paired deterministic evaluations and a separate field-presence comparison for the revised cards.

Acceptance: regression checks reject stale, missing and placeholder hashes; portable HTML displays supported documentation; current deterministic scores are never presented as fresh semantic judgments. Close only after the reviewed fix is merged.
