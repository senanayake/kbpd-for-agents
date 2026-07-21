---
id: KB-EX-001
type: design-space
status: validated
created: 2026-07-21
updated: 2026-07-21
tags: [example, idempotency, retries, api, queue]
related: [KB-EX-002]
---

# Retry Idempotency Design Space For Job-Enqueue API

## Context

The sample project exposes an HTTP endpoint that enqueues background jobs.
Clients retry on network timeouts. Without idempotency, a retry can enqueue the
same job twice.

## Problem Statement

How should the API prevent duplicate job creation when clients retry a request
after an uncertain outcome?

## Dimensions

- Correctness across process restarts.
- Implementation complexity.
- Operational visibility.
- Latency added to the request path.
- Fit for a small service with an existing relational database.

## Options In The Space

### Client-Generated Idempotency Key With Database Record

- Position in the space: persistent, explicit, moderate implementation cost.
- Strengths: survives process restarts, supports auditability, and can return
  the original response for duplicate requests.
- Weaknesses: needs schema, uniqueness constraint, and cleanup policy.
- Evidence needed next: production load behavior and retention policy.

### In-Memory Key Cache

- Position in the space: very simple but process-local.
- Strengths: low latency and no schema.
- Weaknesses: loses state on restart and fails across multiple application
  instances.
- Evidence needed next: none for restart boundary; see KB-EX-002.

### Queue-Level Deduplication Only

- Position in the space: pushes responsibility to infrastructure.
- Strengths: can be strong when the queue supports durable dedupe windows.
- Weaknesses: not portable across queues and may not preserve the HTTP response
  contract.
- Evidence needed next: queue-specific capability review.

## Evidence

- Lightweight reproduction:
  `python examples/sample-project/evidence/idempotency_restart_demo.py`.
- The reproduction shows an in-memory cache loses the key after restart while a
  SQLite-backed record persists across connection lifecycles.
- KB-EX-002 captures the restart boundary in more detail.

## Current Learning

For this sample, database-backed idempotency remains the strongest default.
In-memory caching is dominated because it is simpler but fails the retry safety
property after restart. Queue-level deduplication remains viable only for a
queue-specific design with a documented response contract.

## Narrowing Guidance

Use a database-backed idempotency table for the sample ADR. Do not generalize
this to all systems: high-throughput event pipelines or queues with native
durable dedupe may justify another option.

## Applicability

- Applies to: small HTTP services that already have a relational database and
  need retry-safe job enqueue behavior.
- Does not apply to: single-process scripts, purely internal jobs with no retry
  contract, or queue platforms with proven durable dedupe and response replay.

## Assumptions And Unknowns

- Assumption: the service already has a relational database in the request path.
- Unresolved question: exact retention period for idempotency records.

## Related Knowledge

- K-Briefs: KB-EX-002.
- Decision: `examples/sample-project/decisions/ADR-0001-use-database-backed-idempotency.md`.
- Evidence: `examples/sample-project/evidence/idempotency_restart_demo.py`.
