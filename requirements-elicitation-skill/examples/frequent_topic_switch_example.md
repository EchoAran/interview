# frequent topic switch example

## Input

### conversation snippet
- user turn 1: "Let's discuss features first. I want chat and recommendations."
- user turn 2: "Pause features for now, budget is more important."
- user turn 3: "Actually, postpone budget and discuss compliance first."

## Expected handling

1. Respect explicit user steering each turn.
2. Ask one dependency bridge mini-question when prerequisite is missing.
3. Keep one primary question only, do not ask mixed-topic bundles.
4. Update `current_topic_id` with each explicit shift, but preserve unresolved high-impact open questions.

## Good next utterance pattern

```text
Understood. You want to confirm compliance boundaries first. To avoid rework later, let me confirm one prerequisite: will this product process any regulated sensitive personal data?
```
