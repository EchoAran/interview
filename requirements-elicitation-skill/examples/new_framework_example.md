# new framework example

## Input

### user_request
We want to build a campus second hand trading app for students.

## Output

```json
{
  "phase": "runtime",
  "current_topic_id": "product_objective",
  "topics": [
    {
      "id": "product_objective",
      "label": "product objective",
      "priority": "high",
      "status": "active",
      "notes": [],
      "slots": [
        {
          "name": "core problem",
          "value": "Students need a convenient way to trade second hand items within campus.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "initialization",
              "excerpt": "We want to build a campus second hand trading app for students.",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "initialization"
        },
        {
          "name": "expected outcome",
          "value": "A campus focused marketplace app for student to student second hand trading.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "initialization",
              "excerpt": "We want to build a campus second hand trading app for students.",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "initialization"
        },
        {
          "name": "non goals",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        }
      ]
    },
    {
      "id": "target_users_stakeholders",
      "label": "target users and stakeholders",
      "priority": "high",
      "status": "unstarted",
      "notes": [],
      "slots": [
        {
          "name": "primary users",
          "value": "Students",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "initialization",
              "excerpt": "for students",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "initialization"
        },
        {
          "name": "secondary stakeholders",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        },
        {
          "name": "user segments",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        }
      ]
    },
    {
      "id": "user_workflow_scenarios",
      "label": "user workflow and scenarios",
      "priority": "high",
      "status": "unstarted",
      "notes": [],
      "slots": [
        {
          "name": "main scenario",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        },
        {
          "name": "posting flow",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        },
        {
          "name": "browsing flow",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        },
        {
          "name": "transaction flow",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        }
      ]
    },
    {
      "id": "functional_capabilities",
      "label": "functional capabilities",
      "priority": "high",
      "status": "unstarted",
      "notes": [],
      "slots": [
        {
          "name": "must have features",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        },
        {
          "name": "optional features",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        },
        {
          "name": "release scope",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        }
      ]
    },
    {
      "id": "constraints_boundaries",
      "label": "constraints and boundaries",
      "priority": "high",
      "status": "unstarted",
      "notes": [],
      "slots": [
        {
          "name": "platform",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        },
        {
          "name": "moderation",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        },
        {
          "name": "payment assumptions",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        },
        {
          "name": "campus scope",
          "value": "Campus focused usage scope is implied.",
          "confidence": "supported_inference",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "initialization",
              "excerpt": "campus second hand trading app",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "initialization"
        }
      ]
    },
    {
      "id": "priorities_success_criteria",
      "label": "priorities and success criteria",
      "priority": "medium",
      "status": "unstarted",
      "notes": [],
      "slots": [
        {
          "name": "first release priority",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        },
        {
          "name": "adoption signal",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        },
        {
          "name": "success metrics",
          "value": null,
          "confidence": "open",
          "status": "open_question",
          "evidence": [],
          "last_updated": "initialization"
        }
      ]
    }
  ],
  "open_questions": [
    {
      "id": "oq_0001",
      "text": "What items and transaction types should the first release support?",
      "kind": "general",
      "related_slot_ref": null,
      "severity": null,
      "status": "open"
    },
    {
      "id": "oq_0002",
      "text": "What are the main user flows for posting, browsing, and completing a trade?",
      "kind": "general",
      "related_slot_ref": null,
      "severity": null,
      "status": "open"
    },
    {
      "id": "oq_0003",
      "text": "Are payments handled inside the app or outside the app?",
      "kind": "general",
      "related_slot_ref": null,
      "severity": null,
      "status": "open"
    },
    {
      "id": "oq_0004",
      "text": "What counts as success for the first release?",
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