# Sample Project Scenario

This sample shows the complete KBPD flow for a realistic software-engineering
decision.

Scenario: an HTTP API enqueues background jobs. Clients retry on timeouts, so
the service needs an idempotency strategy that prevents duplicate job creation.

## Flow

1. Material uncertainty: in-memory idempotency is simpler, but may fail after
   restart or horizontal scaling.
2. Search existing knowledge:

```bash
rg -n "idempotency|retry|restart|queue" .kbriefs
```

3. Identify the gap:

```text
We need to learn whether memory-only idempotency protects retry safety across
process restart so that the API can choose a storage strategy.
```

4. Run a lightweight learning cycle:

```bash
python examples/sample-project/evidence/idempotency_restart_demo.py
```

5. Capture evidence:

- `.kbriefs/examples/KB-EX-001-retry-idempotency-design-space.md`
- `.kbriefs/examples/KB-EX-002-in-memory-idempotency-restart-boundary.md`

6. Make the decision:

- `examples/sample-project/decisions/ADR-0001-use-database-backed-idempotency.md`

## Why This Example Exists

The example is intentionally small. It demonstrates how a K-Brief differs from
an ADR:

- the K-Briefs record reusable learning, evidence, limits, and applicability;
- the ADR records the selected implementation consequence for the sample API.
