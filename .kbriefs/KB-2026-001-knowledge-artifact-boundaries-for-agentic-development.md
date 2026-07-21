---
id: KB-2026-001
type: design-space
status: candidate
created: 2026-07-21
updated: 2026-07-21
tags: [kbpd, artifacts, adr, documentation, agents]
related: [KB-2026-002, KB-2026-003, KB-2026-004]
---

# Knowledge Artifact Boundaries For Agentic Development

## Context

The starter needs to teach agents when to create reusable knowledge without
turning every task into documentation work. The prompt required a clear boundary
between K-Briefs, ADRs, issues, runbooks, policies, and ordinary documentation.

## Problem Statement

What repository artifacts should exist in the portable starter, and what should
each artifact own, so that agents preserve learning without duplicating work
tracking, architecture records, or procedural docs?

## Dimensions

- Reuse: whether future tasks should search and apply the artifact.
- Decision ownership: whether the artifact records learning or the chosen
  commitment.
- Process cost: how likely the artifact is to create low-value paperwork.
- Portability: whether the artifact works in ordinary Git repositories without
  specialized infrastructure.

## Options In The Space

### K-Briefs As The Only Durable Artifact

- Position in the space: simple surface area, but too much responsibility.
- Strengths: one searchable knowledge base.
- Weaknesses: blurs decisions, procedures, policies, and reference docs.
- Evidence needed next: adoption feedback from teams using only K-Briefs.

### Separate Artifacts With Linked Responsibilities

- Position in the space: modest structure with clear boundaries.
- Strengths: K-Briefs capture learning; ADRs capture decisions; docs explain
  behavior; runbooks describe operations; issues track work.
- Weaknesses: contributors must understand which artifact to update.
- Evidence needed next: real contribution review experience.

### Add Knowledge-Gap And Learning-Cycle Artifacts

- Position in the space: more explicit KBPD workflow.
- Strengths: makes uncertainty visible before learning is complete.
- Weaknesses: adds artifact types before the starter has evidence that they are
  needed; may encourage process for small tasks.
- Evidence needed next: repeated cases where K-Briefs cannot represent learning
  gaps cleanly.

## Evidence

- Source implementation inspected: `polyglot-devcontainers` at commit
  `cc01cce87143`.
- Source `.kbriefs/README.md` defines K-Briefs as reusable learning and compares
  them with ADRs, issues, documentation, and roadmaps.
- Source `docs/explanation/decisions/README.md` states the useful split: ADRs
  record choices while K-Briefs record learning and evidence behind choices.
- Source `KB-2026-031-starter-generator-knowledge-gaps-and-learning-cycles.md`
  shows that knowledge gaps and learning cycles can be represented inside a
  design-space brief without requiring a separate artifact type.
- This starter has no existing user evidence showing that additional artifact
  types improve adoption.

## Current Learning

The linked-artifact model is the best first-release fit. K-Briefs should own
reusable learning, evidence, applicability, and assumptions. ADRs should own
durable decisions. Issues should own task coordination. Documentation should own
current behavior and user guidance. Policies and runbooks should own rules and
procedures.

Separate knowledge-gap and learning-cycle artifacts remain viable but
unsupported for the portable core. They are dominated for the initial release by
using sections inside K-Briefs and workflows inside skills.

## Narrowing Guidance

Keep the starter to K-Briefs plus ordinary repository artifacts. Reconsider a
new artifact type only after repeated real contributions show that important
learning is being lost or distorted by the five K-Brief types.

Do not add a new artifact type for conceptual completeness alone.

## Applicability

- Applies to: small and medium software repositories adopting KBPD for coding
  agents; this starter's README, `AGENTS.md`, contribution guidance, templates,
  and validator.
- Does not apply to: regulated environments that already require additional
  records; organizations with established KBPD databases; project management
  systems outside Git.

## Assumptions And Unknowns

- Assumption: ordinary repositories benefit more from fewer artifact types than
  from complete conceptual separation.
- Unresolved question: whether larger teams need a dedicated learning backlog
  once many K-Briefs accumulate.

## Related Knowledge

- K-Briefs: KB-2026-002, KB-2026-003, KB-2026-004.
- Source paths:
  `https://github.com/senanayake/polyglot-devcontainers/blob/cc01cce87143bc15d7bc26b24361283092639400/.kbriefs/README.md`,
  `https://github.com/senanayake/polyglot-devcontainers/blob/cc01cce87143bc15d7bc26b24361283092639400/docs/explanation/decisions/README.md`.
