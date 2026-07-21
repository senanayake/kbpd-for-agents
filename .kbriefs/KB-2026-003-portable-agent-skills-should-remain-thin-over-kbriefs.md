---
id: KB-2026-003
type: limit
status: candidate
created: 2026-07-21
updated: 2026-07-21
tags: [agents, skills, portability, codex, copilot, kbpd]
related: [KB-2026-001, KB-2026-004]
---

# Portable Agent Skills Should Remain Thin Over K-Briefs

## Context

The starter must support portable Agent Skills under `.agents/skills/` while
remaining independent of any specific coding-agent product. It also needs to be
usable by projects that only copy Markdown instructions.

## Question

How much behavior can the starter safely place in portable skills without making
the KBPD system vendor-specific or duplicating the source of truth?

## Boundary

Portable skills can describe workflows over `.kbriefs/`, but they cannot
guarantee activation, enforcement, UI behavior, tool availability, or memory
semantics across Codex, GitHub Copilot, and other agent products.

The portable source of truth must remain:

- `AGENTS.md` for always-on rules;
- `.kbriefs/README.md` for the knowledge system;
- `.kbriefs/templates/` for artifact shape.

## Conditions

The boundary appears when an instruction depends on:

- product-specific skill discovery;
- vendor-specific custom instruction files;
- tool availability such as `rg`, test runners, or hosted connectors;
- automatic enforcement rather than agent compliance and repository validation.

## Evidence

- Source implementation did not contain portable `.agents/skills/` for K-Briefs;
  it relied on `AGENTS.md`, `.kbriefs/`, and repository task conventions.
- The `skill-creator` guidance for `SKILL.md` emphasizes concise frontmatter and
  progressive disclosure, which supports thin workflow skills rather than
  duplicated templates.
- The user required vendor-specific Codex or GitHub Copilot definitions, if
  included, to be thin adapters rather than duplicated sources of truth.
- This starter can validate skill frontmatter and template references, but it
  cannot validate how an external agent product activates those skills.
- A first GitHub Copilot adapter was added at `.github/copilot-instructions.md`
  as a thin pointer to `AGENTS.md`, `.kbriefs/`, and `.agents/skills/`, not as a
  duplicate KBPD rule set.

## Implications

Skills should tell agents how to search, identify gaps, plan learning cycles,
create briefs, and review briefs. They should not embed complete template
content, claim universal activation, or replace `AGENTS.md`.

Vendor-specific adapters should point back to the portable core. They may name
the available skills, but should not copy complete skill bodies or templates.

## Recommendations

Keep `.agents/skills/` as thin Markdown workflows. Validate their metadata,
paths, and references. Keep `.github/copilot-instructions.md` as a thin adapter
for Copilot users. Add other product-specific adapters only when they point back
to the portable core and document a real adoption need.

## Applicability

- Applies to: `.agents/skills/`, README adoption guidance, validator skill
  checks, and future vendor adapter decisions.
- Does not apply to: private environments where a single agent product and
  custom skill runtime are guaranteed.

## Assumptions And Unknowns

- Assumption: portable Markdown skills are useful even when an agent product
  treats them as ordinary instructions.
- Unresolved question: which agent products will converge on compatible skill
  discovery and metadata conventions.

## Related Knowledge

- K-Briefs: KB-2026-001, KB-2026-004.
- Source paths: `.agents/skills/`, `AGENTS.md`, `.kbriefs/README.md`.
