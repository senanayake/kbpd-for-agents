# kbpd-for-agents

A practical, open implementation of Knowledge-Based Product Development for
coding agents.

This repository is a starter kit for applying established KBPD ideas to
AI-assisted software development. It is not a new methodology. It adapts
Knowledge-Based Product Development practices, especially K-Briefs and
set-based learning, to repositories where humans and coding agents collaborate.

The central value proposition is:

> Help coding agents accumulate reusable engineering knowledge instead of
> repeatedly completing isolated tasks.

## Why This Exists

Coding agents make implementation cheaper. They do not make reliable engineering
knowledge free.

Without an explicit knowledge system, agents can:

- repeat the same investigation across tasks;
- generalize beyond the evidence they actually collected;
- lose rationale in chat history, commits, or closed issues;
- converge on the first plausible implementation;
- forget boundaries, failed approaches, and assumptions that should constrain
  future work.

KBPD treats product development as a knowledge-generation system. The point is
not to write more documents. The point is to learn what matters, preserve it in
a reusable form, and let evidence narrow choices over time.

## What The Starter Provides

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Always-on operating rules for agents working in the repository. |
| `.kbriefs/` | Canonical KBPD knowledge system for reusable learning. |
| `.kbriefs/templates/` | Concise templates for the supported K-Brief types. |
| `.agents/skills/` | Portable agent workflows that operate on `.kbriefs/`. |
| `tools/validate_kbriefs.py` | Standard-library validation for K-Briefs and skills. |
| `.kbriefs/examples/` | Example briefs showing evidence, limitations, and decisions. |
| `examples/sample-project/` | A small scenario showing the learning flow end to end. |

The starter intentionally does not include a database, vector store, web app,
agent orchestration framework, or vendor-specific runtime.

## K-Briefs In One Paragraph

A K-Brief is a small, structured record of reusable engineering knowledge: what
was learned, why it matters, what evidence supports it, where it applies, where
it does not apply, and what remains uncertain. K-Briefs are most useful for
trade-offs, limits, standards, design spaces, and failure modes that future
humans or agents would otherwise need to rediscover.

K-Briefs are not task notes, status reports, full design documents, or a place
to justify unsupported certainty.

## How The Pieces Work Together

1. `AGENTS.md` tells agents to search existing K-Briefs before material
   decisions, identify assumptions, preserve alternatives, and capture reusable
   learning.
2. `.agents/skills/` gives portable workflows for searching briefs,
   identifying knowledge gaps, planning learning cycles, creating briefs, and
   reviewing briefs.
3. `.kbriefs/README.md` defines the knowledge system: lifecycle, types,
   evidence expectations, naming, relationships, and overload controls.
4. `tools/validate_kbriefs.py` checks structure and links. It does not prove
   that the evidence is true.

## Adopt This In An Existing Repository

1. Copy `AGENTS.md` into the repository root, then add any project-specific
   build, test, security, or release rules.
2. Copy `.kbriefs/` into the repository root. Keep it named `.kbriefs`.
3. Copy `.agents/skills/` if your coding-agent environment can read portable
   skills or skill-like instructions.
4. Copy `tools/validate_kbriefs.py` and optionally the tests if you want
   structural validation in CI.
5. Point any vendor-specific agent adapters at `AGENTS.md` and `.kbriefs/`
   instead of duplicating the KBPD rules.
6. Run:

```bash
python tools/validate_kbriefs.py
```

Use `python3` instead of `python` on systems where `python` is not installed.

## First Use Walkthrough

Use this flow when a task has material uncertainty:

1. State the decision or unknown that matters.
2. Search existing knowledge:

```bash
rg -n "idempotency|retry|queue" .kbriefs AGENTS.md
```

3. If no brief answers the question, identify the knowledge gap and the smallest
   useful learning cycle.
4. Run the investigation, experiment, comparison, or source review.
5. Capture reusable findings in the closest K-Brief template.
6. Link the brief from the decision, implementation note, ADR, test, or docs
   that changed because of it.
7. Validate:

```bash
python tools/validate_kbriefs.py
python -m unittest discover -s tests -p 'test_*.py'
```

See `examples/sample-project/` for a complete scenario.

## K-Briefs And Other Artifacts

| Artifact | Use it for | Do not use it for |
| --- | --- | --- |
| K-Brief | Reusable learning, evidence, limits, trade-offs, standards, failure modes. | Tracking tasks or recording every implementation detail. |
| ADR | A durable architecture decision and its consequences. | The full investigation behind the decision. Link the K-Briefs instead. |
| Issue | Work tracking, ownership, discussion, acceptance criteria. | Long-lived knowledge that future tasks should reuse. |
| Documentation | How the system works or how to use it. | Preserving uncertain evidence or alternatives that may change. |
| Policy | Rules that must be followed. | Exploratory learning or design-space mapping. |
| Runbook | Operational procedure and recovery steps. | Generalizing one incident into reusable engineering knowledge. |

## Project Status

This is an initial public starter. It is intentionally small and repository
native.

Current limitations:

- The validator checks structure, references, and required sections only.
- The skills are Markdown workflows; each agent product decides how much it can
  automate or enforce.
- The starter does not replace product judgment, tests, design review, or
  security review.
- The included examples are small by design and should be adapted to your
  project domain.

## Attribution

This project applies established KBPD principles. See `ATTRIBUTION.md` for
intellectual lineage, source inspiration, and licensing notes.
