---
name: review-kbrief
description: Review K-Briefs for evidence quality, scope control, applicability, unsupported certainty, lifecycle status, metadata, links, and fit with repository KBPD rules. Use before accepting new or changed briefs, templates, skills, or KBPD guidance. Do not use as a substitute for validating the implementation the brief references.
---

# Review K-Brief

Review the brief as reusable engineering knowledge, not as prose polish.

## Workflow

1. Read `.kbriefs/README.md` and the relevant template under
   `.kbriefs/templates/`.
2. Confirm the brief has the right type:

- trade-off for competing variables;
- limit for boundaries;
- standard for preferred patterns;
- design-space for preserving and narrowing options;
- failure-mode for recurring or consequential failures.

3. Check evidence:

- Is evidence specific and verifiable?
- Are commands, source paths, examples, or observations named?
- Are weak or missing evidence areas acknowledged?

4. Check scope:

- Are applicability and limitations explicit?
- Are local observations generalized only as far as evidence supports?
- Are assumptions and unresolved questions separate from facts?

5. Check relationship to other artifacts:

- ADRs record decisions; K-Briefs record learning.
- Issues track work; K-Briefs preserve reusable knowledge.
- Runbooks give procedures; K-Briefs explain failure knowledge.
- Policies state rules; K-Briefs can justify them.

6. Run structural validation:

```bash
python tools/validate_kbriefs.py
```

## Review Findings

Lead with material issues:

- unsupported claim;
- missing or weak evidence;
- applicability too broad;
- wrong K-Brief type;
- duplicate of existing knowledge;
- missing relationship to a decision or artifact;
- invalid metadata or broken reference.

If no material issues are found, state any residual risk, such as evidence that
is plausible but not yet independently reproduced.
