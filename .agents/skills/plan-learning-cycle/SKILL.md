---
name: plan-learning-cycle
description: Plan the smallest useful KBPD learning cycle for a material knowledge gap, including evidence to collect, alternatives to preserve, success signals, and stop conditions. Use before experiments, source reviews, prototypes, benchmarks, or comparisons whose findings may become K-Briefs. Do not use when the answer is already established in existing K-Briefs or ordinary documentation.
---

# Plan Learning Cycle

A learning cycle should reduce uncertainty without building more process than
the question deserves.

## Workflow

1. Start from a material gap identified in `AGENTS.md` terms.
2. Search `.kbriefs/` for prior learning.
3. List plausible alternatives that should remain open.
4. Choose the smallest learning method that can change the decision:

- source review;
- focused experiment;
- reproduction;
- benchmark;
- prototype;
- comparative implementation slice;
- expert or upstream documentation review.

5. Define evidence before running the cycle:

- commands or files to inspect;
- observations to record;
- success signal;
- failure signal;
- stop condition;
- applicability boundary.

6. Avoid learning cycles whose output cannot affect a decision.

## Output

Use this shape:

```text
Gap:
Alternatives still open:
Learning method:
Evidence to collect:
Success or narrowing signal:
Stop condition:
Likely K-Brief type if reusable:
```

After running the cycle, update or create a K-Brief only if the result is
material and reusable. Use `.kbriefs/templates/` for the final artifact.
