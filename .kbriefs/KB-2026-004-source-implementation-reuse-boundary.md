---
id: KB-2026-004
type: limit
status: candidate
created: 2026-07-21
updated: 2026-07-21
tags: [source-implementation, polyglot-devcontainers, starter-scope, kbpd]
related: [KB-2026-001, KB-2026-002, KB-2026-003]
---

# Source Implementation Reuse Boundary

## Context

The public starter is based on the practical KBPD implementation in
`polyglot-devcontainers`, but that repository is a devcontainer product with
many project-specific constraints. Copying it mechanically would make this
starter too specialized.

## Question

Which parts of `polyglot-devcontainers` can be reused for a general KBPD starter
kit, and where does the source implementation stop applying?

## Boundary

Reusable for the starter:

- the `.kbriefs/` top-level knowledge system;
- YAML-frontmatter Markdown briefs;
- the five core K-Brief types: trade-off, limit, standard, design space, and
  failure mode;
- the agent habit of searching briefs before durable decisions;
- the split between K-Briefs and ADRs;
- the smaller starter-scaffold templates as evidence for concise adoption.

Not reusable as a portable default:

- devcontainer-specific task contracts;
- maintainer-container validation requirements;
- source-profile as a sixth core brief type;
- broad triggers that imply a brief for every decision, experiment, or failure;
- task automation tied to the source repository's scaffold and release system.

## Conditions

The boundary appears whenever source guidance depends on:

- the source repository's container-first workflow;
- specific task runners, image publication, or security scans;
- project-specific examples such as starter images and DevPod behavior;
- an internal corpus with dozens of K-Briefs that a new adopter will not have.

## Evidence

- Source inspected: `polyglot-devcontainers` at commit `cc01cce87143`.
- Source Section 0 of `AGENTS.md` establishes KBPD but includes broad brief
  creation triggers.
- Source `.kbriefs/README.md` documents five core types and a reusable
  lifecycle.
- Source `.kbriefs/templates/` includes long templates plus `source-profile.md`;
  the desired public starter named only five starting templates.
- Source `assets/starter-scaffold/AGENTS.md.template` and
  `assets/starter-scaffold/.kbriefs/templates/` are more portable and concise
  than the source repository root.
- Source automation copies starter scaffold assets but does not provide a
  portable K-Brief validator independent of its project task system.

## Implications

The starter should adapt the source implementation rather than copy it. The
portable release should keep `.kbriefs/`, five templates, agent rules, and
skill workflows, while replacing devcontainer-specific automation with a small
standard-library validator.

## Recommendations

Use `polyglot-devcontainers` as the source implementation for practice, not as a
file tree to mirror. Preserve ideas that are useful across repositories and
omit or document anything that depends on the source product's devcontainer
domain.

## Applicability

- Applies to: this initial public release and future decisions about pulling
  source concepts into the starter.
- Does not apply to: repositories that intentionally adopt the full
  `polyglot-devcontainers` task contract and devcontainer lifecycle.

## Assumptions And Unknowns

- Assumption: the five core K-Brief types are sufficient for initial adopters.
- Unresolved question: whether source-profile becomes valuable after teams use
  K-Briefs to evaluate external tools and documentation sources.

## Related Knowledge

- K-Briefs: KB-2026-001, KB-2026-002, KB-2026-003.
- Source paths:
  `https://github.com/senanayake/polyglot-devcontainers/blob/cc01cce87143bc15d7bc26b24361283092639400/AGENTS.md`,
  `https://github.com/senanayake/polyglot-devcontainers/blob/cc01cce87143bc15d7bc26b24361283092639400/.kbriefs/README.md`,
  `https://github.com/senanayake/polyglot-devcontainers/tree/cc01cce87143bc15d7bc26b24361283092639400/assets/starter-scaffold`.
