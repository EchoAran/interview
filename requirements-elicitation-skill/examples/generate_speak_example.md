# generate speak example

## Input

### current_framework
```json
{
  "phase": "runtime",
  "current_topic_id": "target_users_stakeholders",
  "topics": [
    {
      "id": "target_users_stakeholders",
      "label": "target users and stakeholders",
      "priority": "high",
      "status": "active",
      "notes": [],
      "slots": [
        {
          "name": "primary users",
          "value": "Students",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_2",
              "excerpt": "previous interview turns",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_2"
        },
        {
          "name": "secondary stakeholders",
          "value": "Parents may want visibility",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_6",
              "excerpt": "parents may also want visibility",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_6"
        },
        {
          "name": "decision making stakeholder",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "turn_6"
        }
      ]
    }
  ],
  "open_questions": [
    {
      "id": "oq_0001",
      "text": "Who decides which stakeholder needs drive first release priorities?",
      "kind": "general",
      "related_slot_ref": null,
      "severity": null,
      "status": "open"
    }
  ],
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

### selected_topic

```json
{
  "selected_topic_id": "target_users_stakeholders",
  "selected_topic_label": "target users and stakeholders",
  "selection_reason": "Stakeholder power affects scope and permissions.",
  "next_focus_slot": "decision making stakeholder"
}
```

## Output

Understood. For the first release, who should decide what gets built and prioritized: students, parents, or the school?