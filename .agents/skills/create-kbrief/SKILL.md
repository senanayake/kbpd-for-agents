---
name: create-kbrief
description: Create or update a K-Brief when a task produces reusable engineering knowledge with evidence, such as a trade-off, limit, standard, design space, or failure mode. Use after searching existing briefs and completing enough investigation to support the claim. Do not use for one-off task notes, speculative ideas, or trivial implementation details.
---

# Create K-Brief

`.kbriefs/` is the canonical knowledge system. Prefer updating an existing brief
when the new learning fits the same question.

## Workflow

1. Read `.kbriefs/README.md`.
2. Search existing briefs for overlap.
3. Pick the closest template:

- `.kbriefs/templates/tradeoff.md`
- `.kbriefs/templates/limit.md`
- `.kbriefs/templates/standard.md`
- `.kbriefs/templates/design-space.md`
- `.kbriefs/templates/failure-mode.md`

4. Assign the next ID:

- repository knowledge: `KB-YYYY-NNN-short-title.md`;
- examples only: `KB-EX-NNN-short-title.md`.

5. Fill the required core with concise, evidence-backed content.
6. Separate observations, inferences, assumptions, and decisions.
7. State applicability and limitations explicitly.
8. Link related K-Briefs, ADRs, docs, tests, source paths, commands, or evidence
   artifacts.
9. Run:

```bash
python tools/validate_kbriefs.py
```

## Quality Bar

A useful K-Brief lets a future human or agent answer:

- What was learned?
- What evidence supports it?
- Where does it apply?
- Where does it not apply?
- What assumptions remain?
- How should this change future work?

If those answers are not available yet, keep investigating or record an
assumption in the local task instead of creating a weak brief.
