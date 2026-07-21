---
id: KB-2026-002
type: tradeoff
status: candidate
created: 2026-07-21
updated: 2026-07-21
tags: [kbpd, templates, adoption, validation, documentation-overload]
related: [KB-2026-001, KB-2026-004]
---

# Lightweight K-Brief Templates Vs Comprehensive Templates

## Context

The source repository contains detailed K-Brief templates and a smaller starter
scaffold version. The public starter needs templates that agents will complete
meaningfully while still preserving evidence, applicability, assumptions, and
retrieval structure.

## Variables

- Completeness: how much guidance the template gives.
- Completion quality: whether agents fill sections with meaningful evidence.
- Adoption friction: how much process the template adds to ordinary tasks.
- Validation: whether structure can be checked with lightweight tooling.
- Resistance to unsupported certainty: whether the template forces scope and
  evidence boundaries.

## Options Considered

### Option A: Copy The Source Root Templates

- Description: preserve the long templates from source `.kbriefs/templates/`.
- Strengths: many prompts for analysis, rich detail for mature briefs.
- Costs or risks: invites boilerplate, makes small learning cycles feel heavy,
  and increases the chance agents fill sections speculatively.

### Option B: Use Very Minimal Templates

- Description: only frontmatter plus `Evidence` and `Applicability`.
- Strengths: low friction and easy adoption.
- Costs or risks: too little shape for retrieval, review, and type-specific
  learning.

### Option C: Required Core With Concise Type-Specific Sections

- Description: keep five templates, each with a small required core and
  optional detail inside sections.
- Strengths: validates consistently, keeps evidence and limitations explicit,
  and avoids forcing large boilerplate.
- Costs or risks: less exhaustive guidance than the source root templates.

## Evidence

- Source root templates inspected at `cc01cce87143` include many sections such
  as trade-off curves, migration, monitoring, chaos engineering, and status
  checklists. These are useful in mature contexts but heavy for starter use.
- Source `assets/starter-scaffold/.kbriefs/templates/` contains much shorter
  versions, suggesting the source implementation already recognized an adoption
  difference between an internal repository and a reusable scaffold.
- The prompt explicitly required templates to be concise enough that agents
  complete them meaningfully and free of sections that invite boilerplate or
  hallucinated content.
- The validator in this starter can check a small required section set without
  requiring a complex parser or external dependency.

## Analysis

Option C dominates the first release. It keeps the source's five reusable
knowledge types while dropping sections that are only sometimes useful. The
templates still require evidence, applicability, assumptions, unresolved
questions, and related knowledge, which are the sections most likely to prevent
unsupported generalization by agents.

Option A is appropriate for a mature repository with many K-Briefs and strong
review discipline. Option B is attractive for adoption but too weak to teach the
method or support validation.

## Recommendations

Use concise required-core templates for the starter. Allow teams to add optional
sections inside a brief when evidence requires them. Do not add a new template
or mandatory section until real use shows the current core loses important
knowledge.

## Applicability

- Applies to: this starter's public templates, validator section checks, and
  contribution guidance.
- Does not apply to: teams that already have KBPD practice maturity and need
  richer internal templates.

## Assumptions And Unknowns

- Assumption: agents are more likely to produce high-signal briefs when the
  required structure is short.
- Unresolved question: which optional sections practitioners will repeatedly
  add after real adoption.

## Related Knowledge

- K-Briefs: KB-2026-001, KB-2026-004.
- Source paths:
  `https://github.com/senanayake/polyglot-devcontainers/tree/cc01cce87143bc15d7bc26b24361283092639400/.kbriefs/templates`,
  `https://github.com/senanayake/polyglot-devcontainers/tree/cc01cce87143bc15d7bc26b24361283092639400/assets/starter-scaffold/.kbriefs/templates`.
