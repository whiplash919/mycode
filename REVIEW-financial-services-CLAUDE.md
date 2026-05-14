# Review: `anthropics/financial-services` `CLAUDE.md`

Source: https://raw.githubusercontent.com/anthropics/financial-services/refs/heads/main/CLAUDE.md
Reviewed: 2026-05-12 (46 lines)

## Summary

The doc is concise and the directory tree is the strongest part — a reader can locate any concept within seconds. The main issues are (1) a few contradictions between stated rules, (2) under-documented conventions a newcomer will trip over, and (3) missing scaffolding around testing, validation, and ownership.

## Issues

### 1. Opening line typo — "Cowork plugins"
Line 3: *"Cowork plugins and Claude Managed Agent templates …"* — almost certainly meant **"Claude Code plugins"**. As written, "Cowork" is undefined and the sentence is the first thing a reader sees.

### 2. Contradictory instructions for editing skills
- Development Workflow step 1: *"Edit markdown files directly — changes take effect immediately."*
- Two paragraphs earlier: ***"Edit skills in `vertical-plugins/`**, then run `python3 scripts/sync-agent-skills.py` to propagate into the agent bundles."*

A newcomer following step 1 will edit `agent-plugins/<slug>/skills/…`, then have the change flagged by `check.py` or wiped by the next sync. Reword step 1 to exclude skill files, or restructure the workflow as: *edit source → sync → check → commit*.

### 3. "One source, two wrappers" left implicit
The tree comment on `agents/<slug>.md` says *"canonical system prompt (one source, two wrappers)"*, but the doc never names the two wrappers. From the rest of the tree they are presumably (a) the Claude Code plugin under `agent-plugins/<slug>/` and (b) the Managed Agent cookbook under `managed-agent-cookbooks/<slug>/`. Spell that out — it's the central architectural idea.

### 4. Skills are mirrored, not single-source
Skills live in `vertical-plugins/<vertical>/skills/` and are **copied** into `agent-plugins/<slug>/skills/` by `sync-agent-skills.py`; `check.py` enforces non-drift. That's mirror-with-drift-detection, not a single source of truth. Worth one sentence on the rationale (plugin self-containment for marketplace distribution?) and on why symlinks weren't used — otherwise readers will keep asking.

### 5. Cross-tree relative paths in `agent.yaml`
The tree shows `agent.yaml` referencing `../../plugins/agent-plugins/<slug>/...`. Brittle under any reorg. The doc says `check.py` validates `system.file` / `skills.path` / `callable_agents.manifest` references but never names those keys' parent files — link a minimal example of an `agent.yaml` so readers can see the schema.

### 6. `check.py` vs `validate.py` — what's the difference?
The scripts comment lists both. Their division of labor isn't explained. Either describe it in one sentence or consolidate.

### 7. `*.local.md` location undefined
Listed under Key Files as gitignored user config, but the tree doesn't show where they're allowed. Anywhere? Only in specific dirs? State it.

### 8. `marketplace.json` / `mcp-categories.json` missing from the tree
Both appear in **Key Files** but neither is placed in the directory structure. Add them so the reader knows whether they're top-level or nested.

### 9. `claude-for-msft-365-install/` co-location unexplained
Flagged as *"separate from FSI plugins"* — fine, but why does it live in this repo? One line of rationale (e.g., shared release cadence, same admin audience) prevents the obvious "why is this here" question.

### 10. No mention of testing or CI
*"Test commands with `/plugin:command-name` syntax"* is the only testing guidance. Nothing on:
- How to dry-run a managed agent locally before deploy.
- Whether `check.py` runs in CI (and what blocks merge).
- Where `deploy-managed-agent.sh` is meant to be run from, with what credentials.

### 11. Security tiers referenced but not enumerated
`managed-agent-cookbooks/<slug>/README.md` is said to contain *"security tier + handoff notes"*, but tiers aren't defined here or linked. Add either the enumeration or a pointer to where it lives.

### 12. `partner-built/` governance not documented
LSEG and S&P Global plugins are partner-maintained but live in the same tree. Who reviews their PRs? Are they subject to `check.py`? Same sync rules? State the policy.

### 13. Development Workflow is incomplete
Steps end at "Skills are invoked automatically when their trigger conditions match" — that's about runtime, not workflow. The workflow should end with the two mandatory pre-commit actions already mentioned elsewhere:
1. `python3 scripts/sync-agent-skills.py`
2. `python3 scripts/check.py`

## Suggested rewrite — Development Workflow section

```markdown
## Development Workflow

1. **Edit at the source**
   - Skills: `plugins/vertical-plugins/<vertical>/skills/<skill>/SKILL.md`
   - System prompts: `plugins/agent-plugins/<slug>/agents/<slug>.md`
   - Commands / MCP config: under the owning `vertical-plugins/<vertical>/`
2. **Sync** bundled copies: `python3 scripts/sync-agent-skills.py`
3. **Validate**: `python3 scripts/check.py` (lints manifests, resolves references,
   fails on drift between agent-plugins/ and vertical-plugins/)
4. **Test** the plugin locally: `/plugin:<command-name>`
5. **Commit** — CI re-runs `check.py`.
```

## Nice-to-have additions

- A small ASCII diagram showing the source → sync → two-wrapper flow.
- A `CONTRIBUTING.md` link covering partner-plugin policy and security review.
- An example managed-agent `agent.yaml` snippet inline so the path keys (`system.file`, `skills.path`, `callable_agents.manifest`) are concrete.

## What's already good

- The tree is annotated where it counts (the `agents/<slug>.md` and `skills/` comments earn their keep).
- The `check.py` description is specific about what it lints, which is rare.
- Clear separation between named agents, verticals, and partner-built.
