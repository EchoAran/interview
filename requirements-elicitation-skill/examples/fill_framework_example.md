# fill framework example

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
      "status": "active",
      "notes": [],
      "slots": [
        {
          "name": "platform",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "turn_3"
        },
        {
          "name": "moderation",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "turn_3"
        }
      ]
    },
    {
      "id": "priorities_success_criteria",
      "label": "priorities and success criteria",
      "priority": "medium",
      "status": "partially_filled",
      "notes": [],
      "slots": [
        {
          "name": "workflow efficiency target",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "turn_3"
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

The first version only needs iOS, and students should be able to post an item in under one minute.

## Output

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
      "notes": [],
      "slots": [
        {
          "name": "platform",
          "value": "iOS only for first version",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_4",
              "excerpt": "The first version only needs iOS",
              "timestamp": "2026-04-15T00:00:00Z",
              "confidence_note": "explicit user statement"
            }
          ],
          "last_updated": "turn_4"
        },
        {
          "name": "moderation",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "turn_3"
        }
      ]
    },
    {
      "id": "priorities_success_criteria",
      "label": "priorities and success criteria",
      "priority": "medium",
      "status": "partially_filled",
      "notes": [],
      "slots": [
        {
          "name": "workflow efficiency target",
          "value": "Posting an item should take under one minute",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_4",
              "excerpt": "students should be able to post an item in under one minute",
              "timestamp": "2026-04-15T00:00:00Z",
              "confidence_note": "explicit user statement"
            }
          ],
          "last_updated": "turn_4"
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
