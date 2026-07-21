---
id: KB-2026-005
type: standard
status: candidate
created: 2026-07-21
updated: 2026-07-21
tags: [kbpd, self-validation, release-quality, validation]
related: [KB-2026-001, KB-2026-002, KB-2026-003, KB-2026-004]
---

# Initial Starter Self-Validation Standard

## Context

The starter should demonstrate KBPD rather than merely describe it. Before the
initial release can be credible, the repository needs a repeatable quality pass
that checks whether the knowledge system, skills, examples, and validation work
together.

## Standard

Before releasing changes to the KBPD starter, perform a KBPD quality review that
checks:

- whether the repository teaches learning rather than documentation volume;
- whether agents have clear behavior before, during, and after investigation;
- whether existing K-Briefs are searched before new decisions;
- whether set-based exploration, evidence, applicability, and assumptions are
  explicit;
- whether K-Briefs remain distinct from ADRs, issues, docs, policies, and
  runbooks;
- whether the portable core is independent of Codex, GitHub Copilot, and other
  agent products;
- whether validation commands are executable in the local environment.

Fix material weaknesses before declaring the work complete.

## Rationale

A starter kit for KBPD loses credibility if its own release process skips
learning, evidence, and validation. The review should be lightweight but real:
it should be capable of finding issues that change files.

## Evidence

- The initial review on 2026-07-21 found the documented `python` command could
  not run in this environment because only `python3` is installed. README and
  `.kbriefs/README.md` now mention `python3` as the fallback.
- The review found `python3 -m unittest` discovered zero tests. Documentation
  now uses `python -m unittest discover -s tests -p 'test_*.py'`.
- Test execution created `__pycache__` files. `.gitignore` now excludes Python
  cache artifacts.
- `python3 tools/validate_kbriefs.py` passed after the fixes.
- `python3 -m unittest discover -s tests -p 'test_*.py'` ran 5 tests and
  passed after the fixes.
- `python3 examples/sample-project/evidence/idempotency_restart_demo.py`
  demonstrated the intended sample evidence.
- Human review of the first tutorial found that it under-taught knowledge gaps,
  set-based learning, and design loopbacks, and that it used a low-level `sed`
  command where higher-level explanation was more appropriate. The tutorial now
  teaches the KBPD thinking loop explicitly and removes the `sed` step.

## Applicability

- Use when: changing this starter's KBPD structure, templates, skills,
  validation, examples, README, `AGENTS.md`, or contribution guidance.
- Do not use when: making a minor typo fix that does not affect behavior,
  knowledge flow, commands, or public adoption guidance.

## Verification

Run:

```bash
python tools/validate_kbriefs.py
python -m unittest discover -s tests -p 'test_*.py'
```

Use `python3` instead of `python` where needed.

Also run `git diff --check` before committing.

## Exceptions

If the local environment lacks a required command, run the nearest equivalent
and document the difference in the completion report. Do not claim that an
unrun command passed.

## Assumptions And Unknowns

- Assumption: this lightweight review is enough for the initial public starter.
- Unresolved question: whether future releases need CI workflow examples or a
  broader Markdown link checker.

## Related Knowledge

- K-Briefs: KB-2026-001, KB-2026-002, KB-2026-003, KB-2026-004.
- Files: `README.md`, `.kbriefs/README.md`, `.gitignore`,
  `tools/validate_kbriefs.py`, `tests/test_validate_kbriefs.py`.
