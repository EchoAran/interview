# intent routing example

## Input

### user_input
Maybe we should support online payment later, but for first release we need iOS only.  
Also, posting must finish within one minute, except in poor network conditions.

## Output

```json
{
  "intent_classification": [
    {
      "segment": "Maybe we should support online payment later",
      "intent": "exploratory idea",
      "action": "store as supported inference and ask confirmation"
    },
    {
      "segment": "for first release we need iOS only",
      "intent": "constraint declaration",
      "action": "fill platform constraint slot as confirmed"
    },
    {
      "segment": "posting must finish within one minute",
      "intent": "priority expression",
      "action": "fill first release performance expectation and route next turn to success criteria"
    },
    {
      "segment": "except in poor network conditions",
      "intent": "exception or edge-case supplement",
      "action": "record edge condition and ask one follow-up about degraded behavior"
    }
  ]
}
```
