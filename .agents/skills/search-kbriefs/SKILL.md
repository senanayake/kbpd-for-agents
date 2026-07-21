---
name: search-kbriefs
description: Search the repository K-Brief knowledge base before material engineering decisions, investigations, design changes, standards, failures, limits, or trade-off analysis. Use when existing reusable knowledge may affect the task. Do not use for trivial edits with no durable decision or uncertainty.
---

# Search K-Briefs

Use `.kbriefs/` as the canonical knowledge system.

## Workflow

1. Read `.kbriefs/README.md` if the repository's K-Brief rules are unfamiliar.
2. Identify the decision, unknown, failure, limit, standard, or design space in
   the current task.
3. Search with direct terms and synonyms:

```bash
rg -n "<term>|<synonym>|<constraint>" .kbriefs AGENTS.md
```

4. Search metadata when useful:

```bash
rg -n "type: tradeoff|type: design-space|type: limit|type: failure-mode|type: standard" .kbriefs
rg -n "tags:.*<tag>|related:.*KB-" .kbriefs
```

5. Read the most relevant briefs and their `related` links.
6. Separate what is established from what is assumed or still unknown.
7. Use the existing knowledge to narrow the task, update a related brief, or
   identify a new material gap.

## Output

When the search affects the work, report:

- briefs read;
- knowledge that applies;
- knowledge that does not apply;
- remaining gap, if any.

If no relevant brief exists, say that explicitly before investigating.
