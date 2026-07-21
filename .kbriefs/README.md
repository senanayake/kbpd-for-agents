# Knowledge Briefs

`.kbriefs/` is the repository's KBPD knowledge system.

It stores reusable engineering knowledge that should survive beyond a chat, pull
request, issue, or single implementation pass. The directory is intentionally
plain Markdown with parseable frontmatter so humans can read it and agents can
search, validate, and link it.

## Purpose

Use K-Briefs to capture:

- important trade-offs and the evidence behind them;
- limits, boundaries, and compatibility constraints;
- standards that should guide future work;
- design spaces that should not be prematurely narrowed;
- failure modes and how to detect, prevent, or recover from them.

Do not use K-Briefs as general notes, work logs, status reports, or mandatory
paperwork for every task.

## Lifecycle

The normal lifecycle is:

```text
knowledge gap -> learning cycle -> evidence -> K-Brief -> reuse -> update
```

1. Identify a material unknown or assumption.
2. Search existing K-Briefs for prior learning.
3. Run the smallest useful learning cycle: source review, experiment,
   reproduction, benchmark, comparison, or implementation slice.
4. Capture the evidence and its limits.
5. Create or update the closest K-Brief.
6. Link the brief from the decision, docs, tests, ADR, runbook, or policy that
   changed because of it.
7. Revisit the brief when new evidence changes the conclusion.

Knowledge-gap and learning-cycle records usually belong inside a K-Brief rather
than in separate artifact types. Add a new artifact type only when repeated use
shows the current types cannot represent important learning.

## Supported Types

| Type | Template | Use when |
| --- | --- | --- |
| `tradeoff` | `templates/tradeoff.md` | Competing variables make multiple approaches viable. |
| `limit` | `templates/limit.md` | A boundary, constraint, scale limit, or applicability edge is discovered. |
| `standard` | `templates/standard.md` | Evidence supports a preferred pattern or practice. |
| `design-space` | `templates/design-space.md` | The team needs to preserve options and narrow by evidence. |
| `failure-mode` | `templates/failure-mode.md` | A system can fail in a recurring or consequential way. |

The first public release intentionally keeps these five types. Source-profile,
knowledge-gap, learning-record, or decision templates can be useful in specific
repositories, but they are not part of the portable core until evidence shows
they reduce more confusion than they add process.

## Creation And Update Triggers

Create or update a K-Brief when learning is reusable and material. A brief is
usually warranted when at least one of these is true:

- a future agent should search for this before deciding;
- evidence changed which option is preferred;
- a limit or failure mode was discovered by testing, review, or operation;
- the result explains an ADR, policy, runbook, validator rule, or public guide;
- the same question is likely to recur across tasks or projects.

Prefer updating an existing brief when the new learning refines the same
question. Create a new brief when the question, scope, type, or applicability is
meaningfully different.

## Maturity States

Use the `status` field to describe maturity:

- `draft`: early capture; evidence may be incomplete.
- `candidate`: useful and reviewed enough to guide near-term work, but not yet
  broadly proven.
- `validated`: supported by enough evidence to guide default behavior.
- `superseded`: replaced by newer knowledge; keep for history and link to the
  replacement.
- `deprecated`: no longer recommended or no longer applicable.

Validation tooling checks that the status value is allowed. It does not prove
that the maturity claim is correct.

## Evidence Expectations

Every K-Brief must explain what evidence supports it and where that evidence
does not apply.

Useful evidence includes:

- commands and test results;
- source paths, commit IDs, or examples inspected;
- benchmark data or small reproduction scripts;
- incidents, logs, or failure traces;
- comparative notes across alternatives;
- source references with enough context to verify them.

Avoid unsupported claims such as "best", "always", or "proven" unless the
evidence and applicability section justify that scope.

## Applicability And Limitations

Every brief must state:

- where the knowledge applies;
- where it does not apply;
- assumptions still being made;
- unresolved questions worth revisiting.

This prevents agents from treating local evidence as universal truth.

## Naming And IDs

Repository K-Briefs use:

```text
.kbriefs/KB-YYYY-NNN-short-title.md
```

Examples:

```text
.kbriefs/KB-2026-001-template-weight-tradeoff.md
.kbriefs/KB-2026-002-agent-skill-portability-boundary.md
```

Use the current year and the next available sequence number for that year. Keep
the slug lowercase, hyphenated, and descriptive.

Example briefs under `.kbriefs/examples/` use:

```text
.kbriefs/examples/KB-EX-NNN-short-title.md
```

Example IDs are for demonstration and should not be used for project knowledge.

## Relationships

Use `related` for K-Briefs that should be read together.

Use body links for ADRs, docs, tests, runbooks, issues, source files, or external
references. If one K-Brief replaces another, mark the older brief
`superseded` and link both directions in the body.

## Searching

Agents and humans should search before material decisions:

```bash
rg -n "cache|idempotency|retry" .kbriefs
rg -n "type: tradeoff|type: design-space" .kbriefs/*.md
rg -n "related:.*KB-2026-001" .kbriefs
```

Search titles, tags, evidence, limitations, and related briefs. Use synonyms;
older briefs may use different words than the current task.

## Relationship To Other Artifacts

| Artifact | Role |
| --- | --- |
| K-Brief | Reusable knowledge and evidence. |
| ADR | The choice made and its consequences. |
| Issue | Work tracking, discussion, ownership, and acceptance criteria. |
| Documentation | Current system behavior and user-facing explanation. |
| Policy | Rules the project requires people or agents to follow. |
| Runbook | Operational procedure for detection, response, and recovery. |

ADRs often link to K-Briefs. K-Briefs should not replace ADRs when a durable
architecture decision needs an explicit record.

## Avoiding Documentation Overload

Keep K-Briefs short and specific. Prefer a focused one-page brief with strong
evidence over a long template filled with generic prose.

Do not create a brief when:

- the learning is obvious from the code;
- the result affects only one small implementation detail;
- there were no meaningful alternatives or assumptions;
- the note would be a task update rather than reusable knowledge.

## Deprecation And Supersession

Do not delete obsolete K-Briefs unless they were created in error.

When knowledge changes:

1. update `status` to `superseded` or `deprecated`;
2. add a short note explaining why;
3. link to the replacing brief or current documentation;
4. update any ADRs, docs, skills, or agent instructions that still point to the
   old guidance.

## Validation

Run:

```bash
python tools/validate_kbriefs.py
```

Use `python3` instead of `python` on systems where `python` is not installed.

The validator checks frontmatter shape, required fields, allowed types and
statuses, unique IDs, filenames, related links, required sections, skill
metadata, and template references. It does not validate the truth of evidence or
the quality of judgment.
