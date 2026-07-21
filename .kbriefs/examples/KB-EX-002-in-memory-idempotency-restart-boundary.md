---
id: KB-EX-002
type: limit
status: validated
created: 2026-07-21
updated: 2026-07-21
tags: [example, idempotency, retries, restart, failure-boundary]
related: [KB-EX-001]
---

# In-Memory Idempotency Restart Boundary

## Context

In-memory idempotency caches are tempting for small services because they are
fast and simple. The sample project needed to know whether that simplicity still
preserves retry safety after a process restart.

## Question

Does an in-memory idempotency cache prevent duplicate job creation after the
application process restarts?

## Boundary

An in-memory idempotency cache only protects requests handled by the same live
process that recorded the original key. It does not protect retries after
restart or retries routed to another application instance.

## Conditions

The boundary applies when:

- idempotency keys are stored only in process memory;
- the process restarts, crashes, deploys, or scales horizontally;
- clients retry after an uncertain request outcome.

## Evidence

- Command:
  `python examples/sample-project/evidence/idempotency_restart_demo.py`.
- Observed behavior: a new in-memory store does not know about the prior key.
- Observed contrast: a SQLite-backed idempotency record remains visible after a
  new connection is opened.
- Confidence level: high for the restart boundary; not a performance benchmark.

## Implications

The sample API must not rely on memory-only idempotency if it promises retry
safety across deploys, crashes, or multiple instances.

## Recommendations

Use persistent idempotency storage for externally visible retry contracts. Use
in-memory caching only as an optimization in front of durable storage or when
duplicates after restart are explicitly acceptable.

## Applicability

- Applies to: HTTP APIs, job enqueue endpoints, and command handlers that use
  idempotency keys.
- Does not apply to: best-effort internal tasks where duplicate execution is
  harmless, or systems whose queue layer has already proven durable dedupe.

## Assumptions And Unknowns

- Assumption: duplicate job creation has user-visible or operational cost.
- Unresolved question: cleanup and retention policy for persistent keys.

## Related Knowledge

- K-Briefs: KB-EX-001.
- Decision: `examples/sample-project/decisions/ADR-0001-use-database-backed-idempotency.md`.
- Evidence: `examples/sample-project/evidence/idempotency_restart_demo.py`.
