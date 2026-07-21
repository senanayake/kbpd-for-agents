# Contributing

Use KBPD when proposing changes to this starter kit.

## Before Changing The System

Search existing K-Briefs:

```bash
rg -n "<topic>|<alternative>|<constraint>" .kbriefs
```

If the change affects repository structure, templates, skills, validation, or
public guidance, identify the material knowledge gap before implementing.

## When A Contribution Needs A K-Brief

Include a K-Brief when the contribution produces reusable knowledge, such as:

- a trade-off between starter-kit designs;
- a boundary in portability across agent products;
- evidence that a template or skill is too heavy or too weak;
- a failure mode in validation or adoption;
- a standard that future contributors should follow.

Do not add a K-Brief for routine edits, typo fixes, local refactors, or task
status.

## Evidence Expectations

Good evidence can be small. Use commands, tests, source paths, comparison notes,
reproduction steps, or operational observations.

Separate:

- facts: directly verified source or command output;
- observations: what happened in a specific context;
- inferences: conclusions drawn from facts and observations;
- assumptions: beliefs still awaiting proof.

## Avoid Framework Expansion

This repository should remain a small starter kit. Do not add orchestration
frameworks, databases, hosted services, package ecosystems, vector stores, or
large CLIs without a K-Brief showing why repository-native Markdown and a small
validator are insufficient.

## Adding A Template

Add a new K-Brief template only when an existing type repeatedly fails to
represent important knowledge without distortion.

A template proposal should include:

- the knowledge gap it closes;
- why existing templates are insufficient;
- example briefs using the new type;
- validator updates and tests;
- migration or compatibility notes for adopters.

## Adding A Skill

Skills under `.agents/skills/<skill-name>/SKILL.md` must:

- use lowercase hyphenated names;
- include `name` and `description` frontmatter;
- operate on `.kbriefs/` as the canonical knowledge system;
- reference templates instead of duplicating their full content;
- state when the skill should and should not be used.

## Compatibility

Keep the public starter structure stable:

- `.kbriefs/` remains the top-level knowledge system;
- `.agents/skills/` remains the portable skills location;
- `AGENTS.md` remains the always-on agent rule file;
- vendor-specific files, if added, should be thin adapters to these sources of
  truth.

Run before opening a pull request:

```bash
python tools/validate_kbriefs.py
python -m unittest discover -s tests -p 'test_*.py'
```
