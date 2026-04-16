# intent routing

Use this file to classify newest user input before structural maintenance and slot filling.

## Intent classes

- explicit requirement
- exploratory idea
- constraint declaration
- priority expression
- exception or edge-case supplement
- scope change or correction
- meta process comment

## Classification signals

### explicit requirement
Common signals:
- should
- must
- need
- required

Action:
- fill corresponding slot with `confirmed` when mapping is clear
- if mapping is broad, split into one confirmed item and one follow up question

### exploratory idea
Common signals:
- maybe
- perhaps
- we might
- should we

Action:
- store as tentative using `supported_inference` or open question
- ask one confirmation question before treating as committed scope

### constraint declaration
Common signals:
- cannot
- limited to
- only
- must comply with
- no budget for
- not allowed

Action:
- route to constraints related slots first (`platform`, `technical`, `policy`, `operational`)
- mark as `confirmed` if explicit, otherwise `supported_inference`
- trigger contradiction check against existing functional and scope commitments

### priority expression
Common signals:
- first release
- must have first
- highest priority
- nice to have
- later phase
- phase two

Action:
- route to prioritization and release scope slots
- convert implicit sequencing into explicit `first release` vs `later` open questions when needed
- use for topic routing to focus next turn on high impact gaps

### exception or edge-case supplement
Common signals:
- except when
- unless
- in rare cases
- if failure happens
- edge case

Action:
- attach to workflow, risk, or open question slots as scenario evidence
- ask one concrete follow up on trigger condition and expected behavior
- avoid overwriting base flow; record as conditional branch

### scope change or correction
Common signals:
- not anymore
- actually we do not
- replace previous decision
- correction

Action:
- treat newest statement as authoritative candidate
- replace old slot value when correction is explicit
- trigger framework maintenance review when scope direction changes

### meta process comment
Common signals:
- this interview is too long
- summarize what we have
- switch strategy

Action:
- do not fill product requirement slots from this line alone
- adjust question strategy or move to interim summary

## Product type routing at start

When phase is `start`, detect product type from initial idea:
- commerce marketplace
- internal enterprise tool
- social content product
- workflow utility product
- b2b saas product
- ai copilot or agent product
- education product
- platform or infrastructure tool
- data analytics product
- iot or embedded product
- unknown

Routing rule:
- if product type is clear, initialize with the corresponding minimum viable topic emphasis
- if unclear, use default topic set and ask one compact disambiguation question

## Product type emphasis guidance

When product type is clear, bias the initial 5 to 8 topics as follows:

- commerce marketplace: listing lifecycle, trust moderation, transaction workflow
- internal enterprise tool: roles permissions, process handoff, integrations
- social content product: identity graph, content lifecycle, moderation policy
- workflow utility product: task loop, automation boundaries, reliability
- b2b saas product: tenant model, admin controls, billing packaging, integration surface
- ai copilot or agent product: task delegation boundaries, human-in-loop checkpoints, model risk and evaluation
- education product: learner roles, curriculum flow, assessment and feedback loops
- platform or infrastructure tool: developer workflows, operability, reliability and incident response
- data analytics product: data sources, metric definitions, governance, freshness and latency constraints
- iot or embedded product: device lifecycle, connectivity conditions, offline behavior and firmware updates
