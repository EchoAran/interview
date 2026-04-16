# modify framework example

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
              "turn_id": "turn_6",
              "excerpt": "previous interview turns",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_6"
        },
        {
          "name": "optional features",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "turn_6"
        },
        {
          "name": "release scope",
          "value": "student user features only",
          "confidence": "supported_inference",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_6",
              "excerpt": "previous interview turns",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_6"
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

Teachers also need a separate backend to review reports and take down suspicious listings.

## Output

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
              "turn_id": "turn_6",
              "excerpt": "previous interview turns",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_6"
        },
        {
          "name": "optional features",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "turn_6"
        },
        {
          "name": "release scope",
          "value": "student user features only",
          "confidence": "supported_inference",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_6",
              "excerpt": "previous interview turns",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_6"
        }
      ]
    },
    {
      "id": "roles_moderation_operations",
      "label": "roles and moderation operations",
      "priority": "high",
      "status": "partially_filled",
      "notes": [
        "Added during runtime because a distinct actor group and moderation workflow emerged."
      ],
      "slots": [
        {
          "name": "admin actors",
          "value": "Teachers",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "Teachers also need a separate backend",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        },
        {
          "name": "moderation actions",
          "value": [
            "review reports",
            "take down suspicious listings"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "review reports and take down suspicious listings",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        },
        {
          "name": "review triggers",
          "value": "Suspicious listings and user reports",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "review reports and take down suspicious listings",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        },
        {
          "name": "audit trace needs",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "turn_7"
        }
      ]
    }
  ],
  "open_questions": [
    {
      "id": "oq_0001",
      "text": "What actions should teachers be allowed to take in the moderation backend?",
      "kind": "general",
      "related_slot_ref": null,
      "severity": null,
      "status": "open"
    },
    {
      "id": "oq_0002",
      "text": "Does the moderation workflow require audit logs or action history?",
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