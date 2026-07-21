# GitHub Copilot Instructions

Follow `AGENTS.md` for this repository.

Use `.kbriefs/` as the canonical KBPD knowledge base. Before material
engineering decisions, search existing K-Briefs and apply relevant findings.

Use the portable skills under `.agents/skills/` when the task calls for them.
When explicit invocation is supported, the user may name them as slash skills:

- `/search-kbriefs` before material decisions or investigations;
- `/identify-knowledge-gap` when important assumptions or unknowns affect the
  work;
- `/plan-learning-cycle` before experiments, comparisons, prototypes, or source
  reviews;
- `/create-kbrief` when reusable knowledge with evidence should be captured;
- `/review-kbrief` before accepting new or changed K-Briefs.

Do not duplicate the full KBPD system here. Treat this file as a thin Copilot
adapter pointing back to `AGENTS.md`, `.kbriefs/README.md`, `.kbriefs/templates/`,
and `.agents/skills/`.
