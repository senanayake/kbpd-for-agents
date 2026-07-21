---
name: identify-knowledge-gap
description: Identify material unknowns and assumptions before an agent makes a durable engineering decision, narrows a design space, adds a standard, or creates a K-Brief. Use when uncertainty could affect architecture, validation, portability, operations, contribution guidance, or future agent behavior. Do not use for routine implementation details.
---

# Identify Knowledge Gap

Use this skill to decide what must be learned before committing.

## Workflow

1. Search existing K-Briefs first using `.agents/skills/search-kbriefs/SKILL.md`
   or equivalent `rg` searches.
2. State the proposed decision or action.
3. Classify current knowledge:

- Fact: directly verified source, file, command output, or test result.
- Observation: what happened in a specific context.
- Inference: conclusion drawn from facts and observations.
- Assumption: unverified belief that may be wrong.
- Decision: chosen direction.
- Policy: rule the repository requires agents or humans to follow.

4. Ask whether the unknown is material using `AGENTS.md`.
5. If material, write a gap statement:

```text
We need to learn whether <unknown> under <conditions> so that <decision or risk>.
```

6. Choose the likely K-Brief type if the learning becomes reusable:

- trade-off: competing variables;
- limit: boundary or constraint;
- standard: preferred pattern;
- design-space: multiple viable options;
- failure-mode: recurring or consequential failure.

## Output

Produce a short gap summary:

- material decision affected;
- facts already known;
- assumptions still open;
- smallest useful learning target;
- brief type likely to capture the result.

Do not create a K-Brief only because a gap exists. Create or update one when the
learning produces reusable knowledge.
