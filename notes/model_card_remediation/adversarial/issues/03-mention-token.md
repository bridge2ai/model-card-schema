# Run read-only mention detection without a personal access token

The check-mention job supplies `secrets.PAT_FOR_PR` to github-script even though detection only reads repository data. When that secret is absent, the empty value overrides the action's default token and fails before detection starts. PR #29's run 36223938067 records `Input required and not supplied: github-token`; PR #36 contains the same configuration.

The prepared fix uses the built-in `github.token` for detection and explicitly grants only read access to contents, issues and pull requests. The privileged response job remains unchanged.

Acceptance: verify detection has no repository-secret dependency and only read permissions; exercise ordinary, unauthorized and authorized PR events plus manual issue/PR reads with offline JavaScript mocks. The ordinary PR check should pass without starting the response job. Close after the reviewed fix is merged into main.
