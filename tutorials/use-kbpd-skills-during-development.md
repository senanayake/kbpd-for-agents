# Use KBPD Skills During Development

This tutorial walks through a small development decision using the KBPD skills
in this repository. You will learn the visible decision reasoning behind the
files: name the knowledge gap, keep multiple options alive, run a small
learning cycle, avoid costly loopbacks, and capture reusable knowledge.

The goal is to learn the workflow, not to produce a perfect architecture.

## What You Need

- A checkout of this repository.
- A terminal in the repository root.
- `rg` for search.
- `python` or `python3`.
- A coding agent that can read repository files. GitHub Copilot users should
  keep `.github/copilot-instructions.md`, `AGENTS.md`, `.kbriefs/`, and
  `.agents/skills/` in the repository.

## 1. Understand The KBPD Thinking Loop

KBPD starts from the assumption that development is a learning system. The
important question is not only "what should we build?" It is also "what must we
learn before this decision is reliable?"

Use this loop during development:

```text
material uncertainty
-> knowledge gap
-> set of plausible options
-> learning cycle
-> evidence
-> narrowed design space
-> decision
-> reusable K-Brief
```

Loopbacks matter because they are expensive. In KBPD, a design loopback occurs
when a knowledge gap creates a quality issue after the design process has moved
forward, forcing the team to return to an earlier design point because of
something it did not know.

KBPD tries to reduce loopbacks by front-loading learning, preserving sets of
options, and understanding design trade-offs before convergence. When an early
learning cycle exposes a knowledge gap before commitment, that is not a costly
loopback. That is cheap knowledge doing its job.

## 2. Start With A Material Uncertainty

Use the sample project scenario:

```text
An HTTP API enqueues background jobs. Clients retry on timeouts. We need to
choose an idempotency strategy that avoids duplicate jobs.
```

The uncertainty is material because the wrong choice can create duplicate
background work and because more than one plausible approach exists.

If you are using Copilot, prompt it like this:

```text
Use the /search-kbriefs skill. For this sample API idempotency decision, search
existing K-Briefs before recommending an implementation.
```

If your Copilot surface does not show project skills as slash commands, ask for
the skill by name instead:

```text
Use the search-kbriefs skill from `.agents/skills/search-kbriefs/SKILL.md`.
```

## 3. Search Existing Knowledge

Run:

```bash
rg -n "idempotency|retry|restart|queue|dedupe" .kbriefs examples AGENTS.md
```

You should find the example K-Briefs:

- `.kbriefs/examples/KB-EX-001-retry-idempotency-design-space.md`
- `.kbriefs/examples/KB-EX-002-in-memory-idempotency-restart-boundary.md`

Use the `/search-kbriefs` skill when working with an agent. Ask for a short
report:

- briefs read;
- knowledge that applies;
- knowledge that does not apply;
- remaining gap.

## 4. Name The Knowledge Gap

A knowledge gap is not a vague area of ignorance. It is a specific thing the
team must learn because a design decision or quality outcome depends on it.

For this scenario:

```text
We need to learn whether memory-only idempotency protects retry safety after
process restart so that we can decide whether the sample API needs durable
idempotency storage.
```

This is narrower than "research idempotency". It names the uncertainty, the
condition, and the decision it affects.

Ask Copilot:

```text
Use the /identify-knowledge-gap skill. Separate facts, observations,
inferences, assumptions, decisions, and policies for this idempotency scenario.
```

## 5. Separate Facts, Observations, And Assumptions

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

Use the `/identify-knowledge-gap` skill if the gap is not clear yet.

## 6. Keep A Set Of Options Alive

Set-based learning means you do not collapse to the first plausible answer too
early. Hold several options long enough for evidence to eliminate or narrow
them.

For this scenario, keep at least these options open:

| Option | Why It Is Plausible | What Could Eliminate It |
| --- | --- | --- |
| Memory cache | Smallest implementation, low latency. | Fails restart or multi-instance safety. |
| Database record | Durable and explicit. | Too much latency or operational cost for the use case. |
| Queue-level dedupe | Moves duplicate prevention to infrastructure. | Queue cannot replay HTTP results or has too short a dedupe window. |

The point is not to analyze every possible system. It is to avoid premature
convergence while the important uncertainty is still open.

## 7. Map The Design Trade-Offs

Set-based design is not just listing options. It requires understanding the
trade-offs that make each option better or worse under different conditions.

For this scenario:

| Trade-Off | What To Learn |
| --- | --- |
| Durability vs simplicity | Does the simpler memory cache preserve retry safety after restart? |
| Portability vs infrastructure leverage | Is queue-level dedupe available in the environments the starter should teach? |
| Request latency vs correctness | Does durable idempotency add enough cost to change the default? |
| Example clarity vs production completeness | How much policy, cleanup, and scaling detail belongs in a starter example? |

Ask Copilot:

```text
Use the /search-kbriefs and /identify-knowledge-gap skills. Turn the option set
into design trade-offs, then identify which trade-off needs evidence first.
```

The first trade-off to test is durability vs simplicity, because a restart
failure would create a quality issue: duplicate jobs after client retries.

## 8. Plan The Learning Cycle

Use the smallest learning cycle that can change the decision. For this sample,
the cycle is a focused reproduction:

```text
Gap: Does memory-only idempotency protect retry safety after restart?
Alternatives still open: memory cache, database record, queue-level dedupe.
Learning method: run the restart demo.
Evidence to collect: whether the key survives memory restart and SQLite reopen.
Success or narrowing signal: memory loses the key while SQLite retains it.
Stop condition: one clear reproduction of the restart boundary.
Likely K-Brief type if reusable: limit.
```

Ask Copilot:

```text
Use the /plan-learning-cycle skill. Plan the smallest learning cycle that can
narrow the idempotency design space without committing to an implementation.
```

## 9. Run The Evidence

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

## 10. Avoid Costly Design Loopbacks

After the evidence, narrow the option set:

```text
Evidence: memory-only state does not survive restart.
Set-based narrowing: remove memory-only cache as the default for retry safety.
Quality issue avoided: duplicate jobs after retry across restart.
Still viable: database record and queue-level dedupe.
Next narrowing question: does the sample already have a database, and does the
queue support durable dedupe plus response replay?
```

This is the desired KBPD behavior: learn cheaply before committing. The sample
project narrows toward database-backed idempotency because it needs a portable,
durable example. A real product might run another learning cycle on queue
capabilities before deciding.

If the team had already implemented memory-only idempotency as the committed
design, then discovering duplicate jobs after restart would reveal the missed
knowledge gap as a quality issue. That quality issue would force a loopback:
return to the earlier design question, reopen the option set, change the
implementation, and record what the team did not know soon enough.

## 11. Connect Knowledge To A Decision

Open `examples/sample-project/decisions/ADR-0001-use-database-backed-idempotency.md`
and notice the artifact boundary:

- K-Briefs record reusable learning and evidence.
- The ADR records the selected consequence for the sample project.

If this were new learning, use the `/create-kbrief` skill to update an existing
brief or create a new one from `.kbriefs/templates/`.

## 12. Capture Or Update Reusable Knowledge

Use a K-Brief when the learning should guide future work. In this scenario:

- the design-space brief preserves the option set and narrowing logic;
- a trade-off brief would be appropriate if this comparison became reusable
  beyond the sample;
- the limit brief records the restart boundary;
- the ADR records the chosen sample-project consequence.

Ask Copilot:

```text
Use the /create-kbrief skill if this investigation produced new reusable
knowledge. If an existing K-Brief already covers it, update that brief instead.
```

Do not create a K-Brief just because a task happened. Create one when the
learning is material, evidence-backed, and likely to be reused.

## 13. Review The K-Brief Quality

Use the `/review-kbrief` skill on one example brief:

```text
Use the /review-kbrief skill to review
`.kbriefs/examples/KB-EX-002-in-memory-idempotency-restart-boundary.md`. Check
evidence, scope, applicability, and unsupported certainty.
```

A good review should confirm that the brief states a narrow restart boundary and
does not claim to solve all idempotency design.

## 14. Validate The Repository

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
-> preserve a set of plausible options
-> map the design trade-offs
-> plan a small learning cycle
-> run evidence
-> avoid late loopbacks by narrowing before commitment
-> capture or reuse K-Briefs
-> make a decision informed by knowledge
```

The important habit is not creating more Markdown. The habit is making reusable
learning visible before an agent or human commits to a solution, so expensive
loopbacks become less likely.
