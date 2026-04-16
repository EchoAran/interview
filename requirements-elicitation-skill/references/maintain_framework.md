# maintain framework

Use this file to maintain the interview framework structure.

Framework maintenance changes the interview skeleton. It does not fill slot values.

## At `start`

Create a new framework using `assets/interview_framework_schema.json`.
Reference `examples/new_framework_example.md`.

Before initializing topics, classify product type from user input using `references/intent_routing.md`.
Use the smallest viable topic template for the detected product type.

Initialize a compact topic set that is sufficient to start elicitation. Prefer 5 to 8 topics.
A good default set is:
- product objective
- target users and stakeholders
- user workflow and scenarios
- functional capabilities
- constraints and boundaries
- priorities and success criteria

Add domain specific topics only when suggested by the user input.
Examples:
- compliance and audit
- integrations
- data and content
- deployment environment
- business model
- roles and permissions

Type oriented minimum topic emphasis:
- commerce marketplace: transaction workflow, listing lifecycle, trust and moderation
- internal enterprise tool: roles permissions, integrations, process handoff
- social content product: identity and relationship graph, content creation and moderation
- workflow utility product: user task loop, automation boundaries, reliability constraints
- b2b saas product: tenant model, admin controls, billing packaging, integrations
- ai copilot or agent product: delegation boundaries, human review checkpoints, evaluation and safety constraints
- education product: learner and instructor roles, learning path, assessment and feedback
- platform or infrastructure tool: developer workflow, operability, reliability and incident handling
- data analytics product: data source lineage, metrics semantics, freshness latency, governance
- iot or embedded product: device lifecycle, connectivity variability, offline behavior, firmware updates

## At `runtime`

Reference `examples/modify_framework_example.md`.

Make a structural edit only when at least one of the following applies:
- the user introduces a genuinely new requirement area
- an existing topic is too broad and blocks precise questioning
- two topics are overlapping and causing duplicate questions
- a slot is repeatedly needed but does not exist
- a topic or slot is clearly irrelevant to this project
- product direction changed and the current structure no longer fits

## Structural edit rules

### Add a topic when:
- the new area materially affects requirements quality
- the area cannot be cleanly represented as a slot under an existing topic

Signal driven topic suggestions:
- mentions integrating with external system -> `integrations`
- mentions permission differences by role -> `roles and permissions`
- mentions legal or policy obligations -> `compliance and audit`
- mentions runtime platform or hosting constraints -> `deployment environment`
- mentions backup, retention, restore, disaster handling -> `data backup and recovery`

### Add a slot when:
- the information is repeatedly needed within the same topic
- the slot improves traceability or later summarization

### Remove a topic or slot when:
- it is irrelevant to the product being discussed
- it duplicates another element
- it adds questioning overhead without improving requirements clarity

### Split a topic when:
- the topic contains multiple independently evolving concern areas
- one topic would otherwise produce confusing, multi part questioning

### Merge topics when:
- the distinction is artificial for the current project
- the same user evidence fills both repeatedly

## Guardrails

- Prefer small, conservative edits.
- Do not restructure every turn.
- Do not create ontology like complexity.
- Keep names operational and interview friendly.
- Every topic should justify at least one likely future question.
