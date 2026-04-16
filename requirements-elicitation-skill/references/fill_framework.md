# fill framework

Use this file to write grounded information into the current interview framework.

## Input intent routing before filling

Classify the newest user input into one of these intent types before writing slots:
- explicit requirement
- exploratory idea
- constraint declaration
- priority expression
- exception or edge-case supplement
- scope change or correction
- meta process comment

Routing rules:
- explicit requirement: fill target slots directly with `confirmed` when wording is explicit
- exploratory idea: store as tentative or `supported_inference`, then ask confirmation
- constraint declaration: prioritize constraints slots and run contradiction checks
- priority expression: update release scope or priority slots and adjust next topic routing
- exception or edge-case supplement: store conditional branch evidence and ask one trigger clarification
- scope change or correction: update or replace prior slot values and review structural fit
- meta process comment: do not fill product slots, adjust interview strategy

## Evidence rules

Record information using these confidence levels:
- `confirmed`: explicitly stated by the user
- `supported_inference`: strong inference from the user’s statement, marked as inference
- `open`: unresolved or explicitly unknown

Prefer `confirmed`.
Use `supported_inference` sparingly.

### Evidence payload rule

Use only structured evidence arrays (legacy string evidence is not allowed).
Each `evidence` item must include:
- `turn_id`
- `excerpt`
- `timestamp`
- `confidence_note`

Evidence limits:
- maximum 50 evidence items per slot
- truncate oldest low-value evidence first when limit is exceeded
- record truncation in `metadata.truncated_fields`

## Filling rules

- Map each new user statement to the smallest appropriate slot.
- If a statement affects multiple slots, update all relevant slots.
- Preserve wording fidelity for high impact facts.
- Normalize wording only when it improves clarity without changing meaning.
- If the user corrects prior information, replace the old content and mark the latest content as authoritative.
- If evidence is weak, store it as an open question instead of a filled slot.
- Record contradictions by setting affected slot status to `conflicted`.
- When a contradiction is detected, set slot `contradiction_severity` to `low|medium|high`.

## Status-confidence validity matrix

Apply these constraints when writing slots:
- `empty` -> confidence must be `open`
- `filled` -> confidence must be `confirmed` or `supported_inference` (never `open`)
- `open_question` -> confidence should be `open` or `supported_inference`
- `conflicted` -> confidence must be `confirmed` or `supported_inference`, and `contradiction_severity` must be non-null

If incoming information would violate the matrix:
- downgrade to `open_question` when certainty is insufficient
- keep prior stable value and append an open question instead of forcing invalid state

## Information density and follow up depth

Estimate information density of the latest user answer:
- high when concrete actors, constraints, metrics, or workflow details are present
- medium when intent is clear but details are partial
- low when wording is abstract, vague, or purely directional

Follow up strategy:
- low density: ask for one concrete scenario or example
- medium density: fill what is grounded and ask one clarifying detail
- high density: confirm high impact interpretation and move forward

## Do not do these

- Do not invent requirements.
- Do not silently upgrade assumptions into facts.
- Do not collapse nuanced user statements into vague summaries.
- Do not discard contradictions. Record them and trigger clarification.
- Do not treat meta process feedback as product requirement evidence.

## Recommended slot payload pattern

Each filled slot should ideally preserve:
- value
- confidence
- evidence list with at least one `turn_id` and one direct excerpt
- last updated turn summary
- optional convergence score and information density when available

Reference `examples/fill_framework_example.md` when needed.
