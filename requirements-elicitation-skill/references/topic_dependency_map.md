# topic dependency map

Use this file to enforce dependency aware topic routing during runtime.

## Default dependencies

- target users and stakeholders -> user workflow and scenarios
- user workflow and scenarios -> functional capabilities
- functional capabilities -> constraints and boundaries
- constraints and boundaries -> priorities and success criteria

## Optional dependencies

- roles and permissions -> functional capabilities
- integrations -> constraints and boundaries
- compliance and audit -> constraints and boundaries
- deployment environment -> constraints and boundaries

## Routing rules

1. If topic B depends on topic A, do not deeply explore B while A remains `unstarted`, unless user steering is explicit and urgent.
2. If user steering conflicts with dependency order, ask one prerequisite mini question, then follow user steering.
3. Use dependency checks to reduce rework. Prefer clarifying upstream assumptions first.

## Dependency readiness threshold

Treat a prerequisite topic as ready when:
- topic status is at least `partially_filled`, or
- at least one high impact slot in that topic is `filled` with `confirmed`

## Conflict with momentum

If current topic momentum is strong but dependency gap is critical:
- ask one short dependency bridge question
- return to current topic immediately after bridge answer
