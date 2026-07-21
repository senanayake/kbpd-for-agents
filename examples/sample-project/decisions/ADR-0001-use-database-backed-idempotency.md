# ADR-0001: Use Database-Backed Idempotency For Job Enqueue

## Status

Accepted for the sample project.

## Context

The sample API enqueues background jobs and clients may retry after timeouts.
Duplicate jobs are not acceptable for the example contract.

## Decision

Use a database-backed idempotency record keyed by a client-provided idempotency
key. Return or replay the original result when a duplicate key is received.

## Consequences

- The API needs a table with a uniqueness constraint on the idempotency key.
- The service needs a retention and cleanup policy for old keys.
- In-memory caching may be used only as an optimization in front of durable
  storage.

## Knowledge Used

- [KB-EX-001](../../../.kbriefs/examples/KB-EX-001-retry-idempotency-design-space.md)
- [KB-EX-002](../../../.kbriefs/examples/KB-EX-002-in-memory-idempotency-restart-boundary.md)
