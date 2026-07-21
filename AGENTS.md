# AGENTS.md

This file defines operating rules for coding agents working in this repository.

The repository exists to make Knowledge-Based Product Development practical for
AI-assisted and agentic software development. Use KBPD when changing this
starter kit itself.

## Development Philosophy

Treat development as a knowledge-generation system, not only a task-execution
system.

Agents must:

- search existing K-Briefs before material decisions;
- identify important unknowns and assumptions before narrowing;
- preserve multiple plausible options until evidence supports eliminating them;
- distinguish facts, observations, inferences, assumptions, decisions, and
  policies;
- update or create K-Briefs when reusable knowledge is produced;
- avoid creating K-Briefs for trivial implementation details;
- validate repository changes before declaring the work complete.

## Canonical Knowledge System

`.kbriefs/` is the canonical KBPD knowledge system for this repository.

Before making a material design, tooling, documentation, validation, or workflow
choice, search:

```bash
rg -n "<topic>|<synonym>|<constraint>" .kbriefs AGENTS.md
```

Then read the most relevant briefs and their `related` links before deciding.

Use `.agents/skills/` for portable workflows that operate on `.kbriefs/`.
Skills may guide the work, but they do not replace the templates or
`.kbriefs/README.md`.

## Materiality Test For K-Briefs

Create or update a K-Brief when the learning is likely to be reused and at least
one of these is true:

- two or more plausible approaches have meaningful trade-offs;
- an assumption was tested and the result should constrain future work;
- a limit, compatibility boundary, or failure mode was discovered;
- evidence was collected that would be expensive or easy to misremember;
- the finding changes agent instructions, repository structure, validation,
  public guidance, or contribution expectations;
- an ADR, policy, runbook, or major documentation change needs reusable
  evidence behind it.

Do not create a K-Brief for:

- routine edits with no durable lesson;
- formatting, naming, or dependency bumps without a new boundary or trade-off;
- one-off task status;
- speculative ideas that have no evidence yet;
- implementation details already clear from the code or ordinary docs.

When in doubt, write a short assumption or TODO in the local change first. Add a
K-Brief only when the learning becomes reusable.

## Working Rules

Before investigation:

- state the material knowledge gap or confirm none exists;
- record facts separately from assumptions;
- search `.kbriefs/` using likely terms and synonyms;
- keep alternatives open when the cost of doing so is reasonable.

During investigation:

- prefer small learning cycles with explicit success signals;
- capture evidence as commands, test results, source paths, benchmarks, logs, or
  comparative notes;
- avoid upgrading assumptions into facts;
- note where evidence does not apply.

After investigation:

- narrow alternatives using evidence;
- update an existing K-Brief before creating a new overlapping one;
- use the closest template under `.kbriefs/templates/`;
- link K-Briefs from ADRs, docs, tests, or code comments when the knowledge
  materially shaped the outcome;
- run validation.

## Repository Validation

For documentation, K-Brief, skill, or validator changes, run:

```bash
python tools/validate_kbriefs.py
python -m unittest discover -s tests -p 'test_*.py'
```

If a command cannot be run, report why and what risk remains.

## Evolving This Starter

When changing the KBPD system itself:

- use the current K-Briefs as prior knowledge;
- compare alternatives rather than adopting the first plausible structure;
- keep the first release small unless evidence supports expansion;
- avoid adding new artifact types, frameworks, or automation layers without a
  K-Brief documenting the need and trade-off;
- ensure changes still work for ordinary small and medium repositories.
