# checkpoints

Use this file to determine the current interview phase.

## Phase definitions

### `start`
Use `start` when any of the following is true:
- there is no existing interview framework
- the user has only provided an initial idea and no structured elicitation has begun
- the previous turn explicitly asked to start requirements elicitation from scratch

### `runtime`
Use `runtime` when:
- an interview framework already exists
- the interview is ongoing
- there are still unresolved required topics or material ambiguities

### `complete`
Use `complete` only when the framework is sufficiently mature and one of these conditions holds:
- all required high priority topics have enough information for a useful requirements summary
- the remaining unknowns are minor and clearly marked as open questions
- the user explicitly asks to stop and summarize
- the user signals that the current understanding is enough for drafting requirements

## Completion checklist

Before choosing `complete`, verify all of the following:
1. Product goal is captured.
2. Target users or stakeholders are identified.
3. Core workflow or main usage path is described.
4. Main functional expectations are captured.
5. Major constraints, assumptions, or non goals are captured or explicitly unknown.
6. Any major ambiguity that changes scope is either clarified or clearly listed as open.
7. No unresolved high impact contradiction remains in `conflicted` slots.

If two or more items above are still weak or missing, remain in `runtime`.
If item 7 fails, remain in `runtime` even when the user asks for summary.

## Score based completion gate

In addition to the checklist, compute completion readiness using existing framework scores.

### Required score inputs

- topic `coverage_score` (0 to 1)
- slot `convergence_score` (0 to 1) when available
- `efficiency_metrics.estimated_completion` (0 to 1) when available

### Aggregates

Compute:

1. `high_priority_coverage_avg` = average `coverage_score` over all high priority topics with non-null score.
2. `high_priority_convergence_avg` = average `convergence_score` over filled slots in high priority topics with non-null score.
3. `high_priority_sufficient_ratio` = count of high priority topics in `partially_filled|sufficient` divided by high priority topic count.
4. `estimated_completion` = `efficiency_metrics.estimated_completion` if non-null, otherwise null.

### Complexity tiering

Choose complexity tier from topic structure:

- `simple`: <= 6 total topics and <= 4 high priority topics
- `moderate`: 7 to 10 total topics or 5 to 6 high priority topics
- `complex`: >= 11 total topics or >= 7 high priority topics

### Thresholds by complexity

- simple:
  - `high_priority_coverage_avg >= 0.60`
  - `high_priority_convergence_avg >= 0.55`
  - `high_priority_sufficient_ratio >= 0.70`
  - if `estimated_completion` exists, `>= 0.65`
- moderate:
  - `high_priority_coverage_avg >= 0.68`
  - `high_priority_convergence_avg >= 0.62`
  - `high_priority_sufficient_ratio >= 0.75`
  - if `estimated_completion` exists, `>= 0.72`
- complex:
  - `high_priority_coverage_avg >= 0.75`
  - `high_priority_convergence_avg >= 0.70`
  - `high_priority_sufficient_ratio >= 0.80`
  - if `estimated_completion` exists, `>= 0.78`

### Decision rule

Mark `complete` only when:
1. checklist item 1 to 7 all pass, and
2. all available tier thresholds pass.

If one score is missing, continue using available scores and explicitly list missing scoring fields in open questions.
If two or more required score aggregates are unavailable, remain in `runtime` unless the user explicitly asks to stop and summarize; in that case summarize with a quality caveat.

## Runtime subcases

Within `runtime`, detect whether the next action should emphasize:
- structural update
- slot filling
- topic switching
- clarification of contradictions
- summarization before continuation

## Notes

Do not mark `complete` just because the conversation is long.
Do not remain in `runtime` forever if the user wants to stop and the remaining gaps are non critical.
When stopping early by user request, keep unresolved contradictions and major assumptions explicit in open questions and risk section.

## Semantic alignment requirements

This file follows the authoritative state semantics in `SKILL.md` ("State semantics mapping").

Before `complete`, verify these additional consistency rules:
- no `conflicted` slot remains with `contradiction_severity=high`
- no slot uses invalid `status`/`confidence` pair (for example `filled + open`, `empty + confirmed`)
- `open_question` slots are treated as unresolved and must not be counted as fully converged evidence
