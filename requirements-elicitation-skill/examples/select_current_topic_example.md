# select current topic example

## Input

### current_framework
```json
{
  "phase": "runtime",
  "current_topic_id": "functional_capabilities",
  "topics": [
    {
      "id": "functional_capabilities",
      "label": "functional capabilities",
      "priority": "high",
      "status": "active",
      "notes": [],
      "slots": [
        {
          "name": "must have features",
          "value": [
            "item listing",
            "search",
            "chat"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_5",
              "excerpt": "previous interview turns",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_5"
        },
        {
          "name": "permissions model",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "turn_5"
        }
      ]
    },
    {
      "id": "target_users_stakeholders",
      "label": "target users and stakeholders",
      "priority": "high",
      "status": "partially_filled",
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
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "turn_2"
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

Actually the bigger issue is that parents may also want visibility, but students should remain the main users.

## Output

```json
{
  "selected_topic_id": "target_users_stakeholders",
  "selected_topic_label": "target users and stakeholders",
  "selection_reason": "The user explicitly shifted to stakeholder discussion, and this affects permission and feature decisions.",
  "next_focus_slot": "secondary stakeholders"
}
```