# Contributing

Thanks for improving RecallGuard AI. This repository uses a lightweight Git workflow and Conventional Commits so the project history stays readable for reviewers, collaborators, and portfolio visitors.

## Branch Naming

Use short, lowercase branches with a clear type prefix.

| Type | Use for | Example |
|---|---|---|
| `feat/` | New product or agent capability | `feat/reviewer-packet-export` |
| `fix/` | Bug fixes or behavior corrections | `fix/recall-match-threshold` |
| `docs/` | README, docs, reports, diagrams | `docs/agentathon-readme` |
| `test/` | Test coverage or evaluation harness work | `test/decision-harness-cases` |
| `chore/` | Tooling, repo maintenance, generated asset cleanup | `chore/ci-workflow` |
| `refactor/` | Internal cleanup without behavior change | `refactor/checker-rules` |

## Commit Convention

Use Conventional Commit format:

```text
type(scope): short imperative summary
```

Examples:

```text
feat(ui): add trace monitor status cards
fix(checker): prevent certification-only evidence from creating hold
docs(readme): polish Agent-a-Thon project framing
test(checker): add prompt-injection vendor row coverage
chore(ci): run pytest on pull requests
```

Allowed types:

```text
feat, fix, docs, test, chore, refactor, style, build, ci, perf
```

Recommended scopes:

```text
ui, checker, foundry, workflow, docs, readme, tests, data, ci, final
```

## Local Workflow

Start from an updated `main`:

```bash
git checkout main
git pull --ff-only origin main
git checkout -b feat/short-description
```

Before committing:

```bash
python -m py_compile src/recallguard/server.py scripts/run_local_server.py
pytest -q
git status --short
```

Commit only intentional files:

```bash
git add README.md docs/assets/recallguard-console.png
git commit -m "docs(readme): polish portfolio presentation"
```

Push and open a pull request:

```bash
git push -u origin HEAD
gh pr create --fill
```

## Pull Request Checklist

Every PR should answer:

- What changed?
- How was it tested?
- Does this affect Microsoft Foundry agent setup, workflow behavior, or governance evidence?
- Does this affect generated final submission assets?
- If UI changed, is there a screenshot or Playwright verification note?

## Testing Standard

Run this before opening a PR:

```bash
pytest -q
```

For UI changes, also run the local console:

```bash
python scripts/run_local_server.py
```

Then open `http://127.0.0.1:8765` and verify:

- no console errors
- no mobile horizontal scroll
- sample cases still produce expected `APPROVE`, `REVIEW`, and `HOLD` outcomes

## Repository Hygiene

- Do not commit secrets, API keys, local `.venv/`, cache folders, or generated intermediate render folders.
- Keep `final/` only for deliberate submission artifacts.
- Keep public-facing documentation in English.
- Keep Korean notes in separate personal docs only when needed.
- Prefer small commits with clear intent over large mixed commits.
