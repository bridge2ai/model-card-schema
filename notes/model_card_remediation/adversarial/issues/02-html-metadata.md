# Preserve populated metadata and readable layouts in standalone card HTML

Adversarial review of PR #36 found that the HTML drops schema version, dataset unit, license name and model category despite those values being populated in the two YAMLs. Some top-level metadata is marked consumed without being rendered. Custom license text is also omitted by the same license renderer. At a 390-pixel viewport, the pages overflow horizontally by more than 500 pixels.

The prepared fix renders the omitted metadata and license details, adds a narrow-screen layout and viewport declaration, and regenerates both standalone pages. Model-card YAMLs and evaluation scores are unchanged.

Acceptance: regression checks preserve schema/category/dataset/metric/language fields, dataset units and custom license terms. Both pages must load two current embedded badges and show zero document overflow at 390- and 1360-pixel viewports. Close after the reviewed fix is merged into main.
