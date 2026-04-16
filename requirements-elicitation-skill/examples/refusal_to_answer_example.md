# refusal to answer example

## Input

### user_input
I do not want to discuss budget now. Please continue with user workflow first.

## Expected handling

1. Do not force the declined topic unless it blocks interview completion.
2. Mark budget-related slot as deferred or open question with reason.
3. Continue with requested topic (`user workflow and scenarios`).

## Good next utterance pattern

```text
Understood, we can defer budget for now. I will focus on user workflow first: what are the exact steps from opening the product to completing one core task for first-wave users?
```
