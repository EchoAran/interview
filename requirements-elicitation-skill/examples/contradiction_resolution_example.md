# contradiction resolution example

## Input

### current_framework
```json
{
  "phase": "runtime",
  "current_topic_id": "constraints_boundaries",
  "topics": [
    {
      "id": "constraints_boundaries",
      "label": "constraints and boundaries",
      "priority": "high",
      "status": "partially_filled",
      "slots": [
        {
          "name": "payment assumptions",
          "value": "No in app payment for first release",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_5",
              "excerpt": "No in app payment for first release",
              "timestamp": "2026-04-15T00:00:00Z",
              "confidence_note": "explicit user statement"
            }
          ],
          "last_updated": "turn_5"
        }
      ]
    }
  ],
  "open_questions": [],
  "schema_version": "2.0.0",
  "session": {
    "session_id": "20260415_000000_ABC123",
    "conversation_id": "conv_example",
    "state_version": "2.0.0",
    "schema_version": "2.0.0",
    "status": "active",
    "closed_at": null,
    "cleanup_pending": false,
    "cleanup_pending_reason": null
  }
}
```

### new_user_input
We must include in app payment in the first release.

## Output

```json
{
  "updated_slot": {
    "name": "payment assumptions",
    "status": "conflicted",
    "contradiction_severity": "high",
    "evidence": [
      {
        "turn_id": "turn_5",
        "excerpt": "No in app payment for first release",
        "timestamp": "2026-04-15T00:00:00Z",
        "confidence_note": "explicit user statement"
      },
      {
        "turn_id": "turn_8",
        "excerpt": "We must include in app payment in the first release.",
        "timestamp": "2026-04-15T00:00:00Z",
        "confidence_note": "explicit user correction"
      }
    ]
  },
  "contradictions": [
    {
      "id": "ctr_payment_v1_001",
      "slot_ref": "constraints_boundaries.payment assumptions",
      "claim_a": "No in app payment for first release",
      "claim_b": "Must include in app payment in first release",
      "severity": "high",
      "status": "open",
      "resolution_note": null,
      "resolved_at": null
    }
  ],
  "open_questions": [
    {
      "id": "oq_0001",
      "text": "[CONTRADICTION] No in app payment for first release vs must include in app payment in first release. Which one is authoritative?",
      "kind": "contradiction",
      "related_slot_ref": "constraints_boundaries.payment assumptions",
      "severity": "high",
      "status": "open"
    }
  ],
  "next_turn_priority": "clarify_contradiction"
}
```
