# Use KBPD Skills During Development

This tutorial walks through a small development decision using the KBPD skills
in this repository. You will search existing knowledge, name the knowledge gap,
plan a learning cycle, run evidence, connect the evidence to a decision, and
validate the result.

The goal is to learn the workflow, not to produce a perfect architecture.

## What You Need

- A checkout of this repository.
- A terminal in the repository root.
- `rg` for search.
- `python` or `python3`.
- A coding agent that can read repository files. GitHub Copilot users should
  keep `.github/copilot-instructions.md`, `AGENTS.md`, `.kbriefs/`, and
  `.agents/skills/` in the repository.

## 1. Start With A Material Uncertainty

Use the sample project scenario:

```text
An HTTP API enqueues background jobs. Clients retry on timeouts. We need to
choose an idempotency strategy that avoids duplicate jobs.
```

The uncertainty is material because the wrong choice can create duplicate
background work and because more than one plausible approach exists.

If you are using Copilot, prompt it like this:

```text
Use the KBPD skills in `.agents/skills/`. For this sample API idempotency
decision, search existing K-Briefs before recommending an implementation.
```

## 2. Search Existing Knowledge

Run:

```bash
rg -n "idempotency|retry|restart|queue|dedupe" .kbriefs examples AGENTS.md
```

You should find the example K-Briefs:

- `.kbriefs/examples/KB-EX-001-retry-idempotency-design-space.md`
- `.kbriefs/examples/KB-EX-002-in-memory-idempotency-restart-boundary.md`

Use the `search-kbriefs` skill when working with an agent. Ask for a short
report of:

- briefs read;
- knowledge that applies;
- knowledge that does not apply;
- remaining gap.

## 3. Separate Facts, Observations, And Assumptions

Write a short working note before deciding:

```text
Fact: the sample project includes two example K-Briefs about idempotency.
Observation: KB-EX-002 says memory-only idempotency fails after restart.
Inference: memory-only storage is not enough for retry safety across deploys.
Assumption: duplicate jobs are unacceptable for the sample API.
Decision not yet made: which idempotency strategy should be the default.
```

This is the visible reasoning you want from an agent. It should not claim more
than the evidence supports.

Use the `identify-knowledge-gap` skill if the gap is not clear yet.

## 4. Plan The Learning Cycle

Use the smallest learning cycle that can change the decision.

For this sample, the cycle is a focused reproduction:

```text
Gap: Does memory-only idempotency protect retry safety after restart?
Alternatives still open: memory cache, database record, queue-level dedupe.
Learning method: run the restart demo.
Evidence to collect: whether the key survives memory restart and SQLite reopen.
Success or narrowing signal: memory loses the key while SQLite retains it.
Stop condition: one clear reproduction of the restart boundary.
Likely K-Brief type if reusable: limit.
```

Use the `plan-learning-cycle` skill for this step when working with an agent.

## 5. Run The Evidence

Run:

```bash
python examples/sample-project/evidence/idempotency_restart_demo.py
```

If `python` is not installed, run:

```bash
python3 examples/sample-project/evidence/idempotency_restart_demo.py
```

Expected result:

```text
memory_cache_has_key_after_restart=False
sqlite_store_has_key_after_restart=True
result=in-memory idempotency is restart-local; sqlite persists
```

The evidence is intentionally small. It proves a restart boundary; it does not
prove production performance, retention policy, or queue-specific behavior.

## 6. Connect Knowledge To A Decision

Read:

```bash
sed -n '1,180p' examples/sample-project/decisions/ADR-0001-use-database-backed-idempotency.md
```

Notice the artifact boundary:

- K-Briefs record reusable learning and evidence.
- The ADR records the selected consequence for the sample project.

If this were new learning, use the `create-kbrief` skill to update an existing
brief or create a new one from `.kbriefs/templates/`.

## 7. Review The K-Brief Quality

Use the `review-kbrief` skill on one example brief:

```text
Use the `review-kbrief` skill to review
`.kbriefs/examples/KB-EX-002-in-memory-idempotency-restart-boundary.md`.
Check evidence, scope, applicability, and unsupported certainty.
```

A good review should confirm that the brief states a narrow restart boundary and
does not claim to solve all idempotency design.

## 8. Validate The Repository

Run:

```bash
python tools/validate_kbriefs.py
python -m unittest discover -s tests -p 'test_*.py'
```

Use `python3` instead of `python` where needed.

The validator checks structure and references. It does not prove that the
engineering conclusion is true.

## What You Learned

You used the KBPD loop:

```text
material uncertainty
-> search existing knowledge
-> identify the knowledge gap
-> plan a small learning cycle
-> run evidence
-> capture or reuse K-Briefs
-> make a decision informed by knowledge
```

The important habit is not creating more Markdown. The habit is making reusable
learning visible before an agent or human commits to a solution.
