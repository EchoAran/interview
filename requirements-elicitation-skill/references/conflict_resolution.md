# conflict resolution

Use this file to detect, record, and resolve contradictory requirement statements.

## What counts as contradiction

- direct reversal of a prior committed requirement
- user group inclusion in one turn and exclusion in another
- first release scope includes an area that another statement explicitly removes
- technical assumption conflicts with declared constraints

## Detection and recording rules

When contradiction is found:
1. mark affected slot `status` as `conflicted`
2. ensure slot `confidence` is not `open` (use `supported_inference` if explicit confirmation is not yet available)
3. retain both claims in evidence trail
4. classify contradiction severity as `low|medium|high`
5. append one structured open question item (`kind=contradiction`)
6. append one structured item to framework `contradictions`

Open question format:
- `id`: unique question id
- `text`: `[CONTRADICTION] {claim_a} vs {claim_b}. Which one should be authoritative for first release?`
- `kind`: `contradiction`
- `related_slot_ref`: `{topic_id}.{slot_name}`
- `severity`: `low|medium|high`
- `status`: `open`

Severity guidance:
- `high`: reverses scope, architecture, user group boundary, release commitment, or compliance/security requirement
- `medium`: changes workflow variants, role responsibilities, or major feature priority
- `low`: wording differences or minor detail variance with low scope impact

## Clarification priority

- high impact contradictions are first priority in next turn
- do not open new low impact topics until high impact contradiction is clarified

## Resolution rules

When user clarifies:
1. set authoritative value in the slot
2. update confidence based on explicitness
3. move slot from `conflicted` to `filled` or `open_question`
4. clear slot `contradiction_severity` or downgrade it when partial ambiguity remains
5. mark related item in `contradictions` as `resolved` with a resolution note
6. remove or close related contradiction open question

## Completion guard

Do not mark interview `complete` when unresolved high impact contradiction remains.
