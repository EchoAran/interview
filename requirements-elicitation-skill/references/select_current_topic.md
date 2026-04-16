# select current topic

Use this file to select the topic that should drive the next interview turn.

## At `start`

Choose the first high priority topic from the initialized framework.
Default preference order:
1. product objective
2. target users and stakeholders
3. user workflow and scenarios
4. functional capabilities
5. constraints and boundaries
6. priorities and success criteria

## At `runtime`

Select the next topic using the following priority order.

### Priority 1. Explicit user steering
If the user clearly wants to discuss a specific topic, follow that topic unless doing so would block the interview because a prerequisite is missing.

### Priority 2. Contradictions or ambiguities with high scope impact
Resolve ambiguities that would materially change later questioning.

### Priority 3. Current topic momentum
Stay on the current topic when the user is still providing useful detail and there are important unfilled slots nearby.

### Priority 4. Dependency driven progression
Ask upstream questions before downstream detail.
Examples:
- clarify users before advanced feature prioritization
- clarify deployment context before infrastructure constraints

Use `references/topic_dependency_map.md` to check whether a candidate topic has unmet prerequisites.
If topic B depends on topic A, prefer A until A is at least `partially_filled`, unless user steering is explicit and high urgency.

### Priority 5. Coverage balancing
Move to high priority topics that remain weakly filled.

### Priority 6. Convergence window routing
Prefer topics that are not too empty and not almost finished.
Use convergence guidance:
- low convergence (<0.4): only enter when dependency critical or user explicitly steers there
- medium convergence (0.4 to 0.7): best zone for next focused question
- high convergence (>0.7): close with confirmation or move on

## Recommended runtime scoring

When multiple candidates are valid, rank with:
- dependency readiness
- contradiction impact
- explicit user steering strength
- convergence window fit
- topic priority and coverage gap

## Avoid

- switching topics every turn without reason
- ignoring a direct user topic shift
- staying too long on a topic with diminishing returns
- selecting topics solely by original order when the conversation has moved elsewhere

Reference `examples/select_current_topic_example.md` when needed.
