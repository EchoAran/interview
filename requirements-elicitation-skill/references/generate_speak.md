# generate speak

Use this file to generate the next interview utterance.

## Input assumptions

Before writing the next turn, identify:
- current topic
- the most important missing slot in that topic
- any recent contradiction or ambiguity
- whether the user needs a transition or a direct follow up

## Preferred utterance patterns

### Focused elicitation
Ask for one concrete piece of information.

### Clarification
Check a potentially consequential interpretation.

### Example seeking
Ask for a realistic scenario, workflow, or instance.

### Constraint probing
Ask about limits, dependencies, or boundaries.

### Prioritization probing
Ask what matters most when scope is still broad.

### Contradiction clarification
When a high impact contradiction exists, ask one direct disambiguation question first.

### Low density deepening
When recent input is vague, ask for one concrete example with actor and outcome.

### High density fast forward
When recent input is concrete and detailed, briefly confirm interpretation and move to the next highest impact gap.

## Style rules

- Ask one primary question per turn.
- Keep the question specific.
- Use the project context already collected.
- Avoid generic consultant style filler.
- Avoid repeating a question that the user has already answered.
- Use brief confirmation before the next question when it improves continuity.
- Prefer questions that reduce uncertainty in the framework.
- Resolve high impact contradictions before opening new low impact topics.
- Keep one question per turn even in contradiction mode.

## Good question shapes

- “Who will use this first in practice?”
- “What is the main task the user should be able to complete end to end?”
- “When you say real time, what response time is acceptable?”
- “Which of these capabilities is required for the first release?”

## Weak question shapes

- “Can you tell me more?”
- “Anything else?”
- “What are your requirements?”

Reference `examples/generate_speak_example.md` when needed.
