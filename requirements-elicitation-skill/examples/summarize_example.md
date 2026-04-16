# summarize example

## Input

### final_framework
```json
{
  "phase": "complete",
  "current_topic_id": null,
  "topics": [
    {
      "id": "product_objective",
      "label": "product objective",
      "priority": "high",
      "status": "sufficient",
      "notes": [],
      "slots": [
        {
          "name": "core problem",
          "value": "Students need a convenient way to buy and sell second hand items within the same campus community.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_3",
              "excerpt": "interview turns 1 to 3",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_3"
        },
        {
          "name": "expected outcome",
          "value": "A campus focused marketplace app that reduces friction in student to student trading.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_3",
              "excerpt": "interview turns 1 to 3",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_3"
        },
        {
          "name": "non goals",
          "value": "No support for off campus public marketplace usage in the first release.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_8",
              "excerpt": "turn_8",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_8"
        }
      ]
    },
    {
      "id": "target_users_stakeholders",
      "label": "target users and stakeholders",
      "priority": "high",
      "status": "sufficient",
      "notes": [],
      "slots": [
        {
          "name": "primary users",
          "value": "Students",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_1",
              "excerpt": "turn_1",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_1"
        },
        {
          "name": "secondary stakeholders",
          "value": [
            "Parents with view access",
            "Teachers as moderators"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "turn_6 and turn_7",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        },
        {
          "name": "role distinctions",
          "value": "Students buy and sell items. Parents may view. Teachers handle moderation actions.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "turn_6 and turn_7",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        }
      ]
    },
    {
      "id": "user_workflow_scenarios",
      "label": "user workflow and scenarios",
      "priority": "high",
      "status": "sufficient",
      "notes": [],
      "slots": [
        {
          "name": "main usage path",
          "value": "A student posts an item, another student browses or searches, they chat, and complete an offline trade on campus.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_5",
              "excerpt": "turn_4 and turn_5",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_5"
        },
        {
          "name": "important supporting scenarios",
          "value": [
            "report suspicious listing",
            "teacher reviews report"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "turn_7",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        },
        {
          "name": "edge cases already identified",
          "value": [
            "fraudulent listings",
            "unsafe off campus transaction attempts"
          ],
          "confidence": "supported_inference",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_8",
              "excerpt": "turn_7 and turn_8",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_8"
        }
      ]
    },
    {
      "id": "functional_capabilities",
      "label": "functional capabilities",
      "priority": "high",
      "status": "sufficient",
      "notes": [],
      "slots": [
        {
          "name": "core required capabilities",
          "value": [
            "item listing",
            "search and browse",
            "in app chat",
            "report listing"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "turn_4 to turn_7",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        },
        {
          "name": "secondary or optional capabilities",
          "value": [
            "parent visibility"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_6",
              "excerpt": "turn_6",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_6"
        },
        {
          "name": "first release scope",
          "value": "Student trading workflow, basic moderation, and campus only usage.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_8",
              "excerpt": "turn_4 to turn_8",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_8"
        }
      ]
    },
    {
      "id": "constraints_boundaries",
      "label": "constraints and boundaries",
      "priority": "high",
      "status": "sufficient",
      "notes": [],
      "slots": [
        {
          "name": "platform or environment constraints",
          "value": "iOS only for the first release",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_4",
              "excerpt": "turn_4",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_4"
        },
        {
          "name": "technical constraints",
          "value": "No integrated online payment in the first release",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_5",
              "excerpt": "turn_5",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_5"
        },
        {
          "name": "operational constraints",
          "value": "Trades are expected to happen within campus",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_8",
              "excerpt": "turn_8",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_8"
        },
        {
          "name": "policy or compliance constraints",
          "value": "Moderation is required for suspicious listings",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "turn_7",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        }
      ]
    },
    {
      "id": "priorities_success_criteria",
      "label": "priorities and success criteria",
      "priority": "medium",
      "status": "sufficient",
      "notes": [],
      "slots": [
        {
          "name": "highest priority needs",
          "value": [
            "fast posting flow",
            "safe campus specific trading"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_8",
              "excerpt": "turn_4 and turn_8",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_8"
        },
        {
          "name": "tradeoffs already stated",
          "value": [
            "iOS first before broader platform support",
            "offline transaction instead of integrated payment"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_5",
              "excerpt": "turn_4 and turn_5",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_5"
        },
        {
          "name": "success signals or metrics",
          "value": [
            "posting an item takes under one minute",
            "students can complete a basic trade workflow end to end"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_9",
              "excerpt": "turn_4 and turn_9",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_9"
        }
      ]
    }
  ],
  "open_questions": [
    {
      "id": "oq_0001",
      "text": "Should parent visibility be part of the first release or a later phase?",
      "kind": "general",
      "related_slot_ref": null,
      "severity": null,
      "status": "open"
    },
    {
      "id": "oq_0002",
      "text": "What level of moderation audit history is required?",
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

## Output

### Artifact 1. final_interview_framework

```json
{
  "phase": "complete",
  "current_topic_id": null,
  "topics": [
    {
      "id": "product_objective",
      "label": "product objective",
      "priority": "high",
      "status": "sufficient",
      "notes": [],
      "slots": [
        {
          "name": "core problem",
          "value": "Students need a convenient way to buy and sell second hand items within the same campus community.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_3",
              "excerpt": "interview turns 1 to 3",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_3"
        },
        {
          "name": "expected outcome",
          "value": "A campus focused marketplace app that reduces friction in student to student trading.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_3",
              "excerpt": "interview turns 1 to 3",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_3"
        },
        {
          "name": "non goals",
          "value": "No support for off campus public marketplace usage in the first release.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_8",
              "excerpt": "turn_8",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_8"
        }
      ]
    },
    {
      "id": "target_users_stakeholders",
      "label": "target users and stakeholders",
      "priority": "high",
      "status": "sufficient",
      "notes": [],
      "slots": [
        {
          "name": "primary users",
          "value": "Students",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_1",
              "excerpt": "turn_1",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_1"
        },
        {
          "name": "secondary stakeholders",
          "value": [
            "Parents with view access",
            "Teachers as moderators"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "turn_6 and turn_7",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        },
        {
          "name": "role distinctions",
          "value": "Students buy and sell items. Parents may view. Teachers handle moderation actions.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "turn_6 and turn_7",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        }
      ]
    },
    {
      "id": "user_workflow_scenarios",
      "label": "user workflow and scenarios",
      "priority": "high",
      "status": "sufficient",
      "notes": [],
      "slots": [
        {
          "name": "main usage path",
          "value": "A student posts an item, another student browses or searches, they chat, and complete an offline trade on campus.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_5",
              "excerpt": "turn_4 and turn_5",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_5"
        },
        {
          "name": "important supporting scenarios",
          "value": [
            "report suspicious listing",
            "teacher reviews report"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "turn_7",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        },
        {
          "name": "edge cases already identified",
          "value": [
            "fraudulent listings",
            "unsafe off campus transaction attempts"
          ],
          "confidence": "supported_inference",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_8",
              "excerpt": "turn_7 and turn_8",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_8"
        }
      ]
    },
    {
      "id": "functional_capabilities",
      "label": "functional capabilities",
      "priority": "high",
      "status": "sufficient",
      "notes": [],
      "slots": [
        {
          "name": "core required capabilities",
          "value": [
            "item listing",
            "search and browse",
            "in app chat",
            "report listing"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "turn_4 to turn_7",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        },
        {
          "name": "secondary or optional capabilities",
          "value": [
            "parent visibility"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_6",
              "excerpt": "turn_6",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_6"
        },
        {
          "name": "first release scope",
          "value": "Student trading workflow, basic moderation, and campus only usage.",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_8",
              "excerpt": "turn_4 to turn_8",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_8"
        }
      ]
    },
    {
      "id": "constraints_boundaries",
      "label": "constraints and boundaries",
      "priority": "high",
      "status": "sufficient",
      "notes": [],
      "slots": [
        {
          "name": "platform or environment constraints",
          "value": "iOS only for the first release",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_4",
              "excerpt": "turn_4",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_4"
        },
        {
          "name": "technical constraints",
          "value": "No integrated online payment in the first release",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_5",
              "excerpt": "turn_5",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_5"
        },
        {
          "name": "operational constraints",
          "value": "Trades are expected to happen within campus",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_8",
              "excerpt": "turn_8",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_8"
        },
        {
          "name": "policy or compliance constraints",
          "value": "Moderation is required for suspicious listings",
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_7",
              "excerpt": "turn_7",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_7"
        }
      ]
    },
    {
      "id": "priorities_success_criteria",
      "label": "priorities and success criteria",
      "priority": "medium",
      "status": "sufficient",
      "notes": [],
      "slots": [
        {
          "name": "highest priority needs",
          "value": [
            "fast posting flow",
            "safe campus specific trading"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_8",
              "excerpt": "turn_4 and turn_8",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_8"
        },
        {
          "name": "tradeoffs already stated",
          "value": [
            "iOS first before broader platform support",
            "offline transaction instead of integrated payment"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_5",
              "excerpt": "turn_4 and turn_5",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_5"
        },
        {
          "name": "success signals or metrics",
          "value": [
            "posting an item takes under one minute",
            "students can complete a basic trade workflow end to end"
          ],
          "confidence": "confirmed",
          "status": "filled",
          "evidence": [
            {
              "turn_id": "turn_9",
              "excerpt": "turn_4 and turn_9",
              "timestamp": "1970-01-01T00:00:00Z",
              "confidence_note": "example placeholder"
            }
          ],
          "last_updated": "turn_9"
        }
      ]
    }
  ],
  "open_questions": [
    {
      "id": "oq_0001",
      "text": "Should parent visibility be part of the first release or a later phase?",
      "kind": "general",
      "related_slot_ref": null,
      "severity": null,
      "status": "open"
    },
    {
      "id": "oq_0002",
      "text": "What level of moderation audit history is required?",
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

### Artifact 2. requirements_summary_report

```md
# Requirements Summary Report

## 1. Document Metadata
- **Project / Product Name**: Campus second hand trading app
- **Interview Session ID**: `20260415_000000_ABC123`
- **Report Version**: `1.0.0`
- **Schema Version**: `2.0.0`
- **Generated At**: `TBD`
- **Last Updated At**: `TBD`
- **Current Interview Status**: `complete`
- **Overall Confidence**: `medium`

## 2. Executive Summary
### 2.1 One Sentence Summary
> Build a campus-focused second hand trading app that enables students to post, discover, chat, and complete offline trades safely and efficiently.

### 2.2 Problem Statement
- What problem is being addressed: Student-to-student second hand trading is fragmented and inefficient.
- Why this problem matters: Friction in posting/discovery/communication reduces transaction completion.
- What happens if the problem remains unsolved: Students keep using ad-hoc channels with lower trust and poorer moderation.

### 2.3 Proposed Product Direction
- Product category: Campus marketplace app
- Core value proposition: Fast local trading workflow with safety-oriented moderation
- Expected outcome for target users: Lower effort and higher confidence for on-campus trades

### 2.4 Current Requirement Maturity
- Requirement maturity level: medium
- Main unknowns: Parent visibility scope, moderation audit history depth
- Main risks: Moderation scope expansion may impact release complexity
- Whether the current information is sufficient for solution design: `partial`

---

## 3. Product Scope
### 3.1 In Scope
- Student listing and browsing
- In-app chat
- Report suspicious listing
- Basic moderation workflow
- Campus-only usage context

### 3.2 Out of Scope
- Off-campus public marketplace usage
- Integrated online payment in first release
- Non-iOS clients in first release

### 3.3 Scope Boundaries
- Business boundary: Focus on campus second hand transactions
- User boundary: Students as primary users; parents/teachers as secondary roles
- Technical boundary: iOS first; no integrated payment
- Operational boundary: Offline trade completion expected on campus

### 3.4 Scope Notes
- Parent visibility is still open and can shift first-release scope.

---

## 4. Users and Stakeholders
### 4.1 Primary Users
- User group name: Students
- Role / characteristics: Buyers and sellers within campus
- Core goals: Post quickly, discover relevant items, complete safe trades
- Main pain points: Slow listing/discovery and uncertain trust
- Context of use: Daily campus life, mobile-first interactions

### 4.2 Secondary Users
- User group name: Parents
- Role / characteristics: View access only (pending scope decision)
- Why they matter: Visibility and trust support for students

### 4.3 Stakeholders
- Stakeholder name / role: Teachers (moderators)
- Interests: Reduce suspicious/fraudulent listings
- Influence on requirements: Define moderation workflow needs
- Concerns or constraints introduced: Auditability depth is not finalized

### 4.4 Beneficiaries and Decision Makers
- Who benefits directly: Students
- Who approves or funds the product: `TBD`
- Who may block progress: Moderation/policy stakeholders if controls are insufficient

---

## 5. Goals and Success Criteria
### 5.1 Business Goals
- Increase efficiency and trust of campus second hand trading.

### 5.2 User Goals
- Post items quickly and find/buy safely.

### 5.3 Product Goals
- Deliver an end-to-end campus trading loop with basic moderation.

### 5.4 Success Metrics
- Metric name: Posting completion time
- What it measures: Listing creation efficiency
- Target or threshold: Under one minute
- Why it matters: Indicates core workflow usability

### 5.5 Failure Signals
- Users fail to complete end-to-end trade flow reliably.

---

## 6. Core Workflows and Use Scenarios
### 6.1 Key Use Scenarios
- Scenario name: Student trade flow
- Trigger: User wants to sell an item
- Primary actor: Student
- Preconditions: User has item details/photos
- Expected outcome: Item posted, discovered, chatted, and traded offline

### 6.2 Main User Journey
- Post item -> browse/search -> chat -> meet on campus -> complete offline trade.

### 6.3 Alternative Flows
- User reports suspicious listing; moderator reviews and acts.

### 6.4 Exception Flows
- Fraudulent listing detection and moderation intervention.

### 6.5 Frequency and Criticality
- Frequency of use: High for posting/browsing/chat
- Business criticality: High
- User criticality: High

---

## 7. Functional Requirements
- **Requirement ID**: FR-001
- **Title**: Item listing
- **Description**: Users can create campus-targeted listings.
- **Primary user / actor**: Student
- **Related workflow / scenario**: Student trade flow
- **Inputs**: Item title/description/category/media
- **System behavior**: Persist listing and make it discoverable
- **Outputs / results**: Published listing
- **Priority**: `must`
- **Confidence**: `high`
- **Evidence**: turns 4-8
- **Notes**: iOS-first boundary

- **Requirement ID**: FR-002
- **Title**: Search and browse
- **Description**: Users can discover listings efficiently.
- **Primary user / actor**: Student
- **Related workflow / scenario**: Student trade flow
- **Inputs**: Query and filters
- **System behavior**: Return relevant listings
- **Outputs / results**: Search results list
- **Priority**: `must`
- **Confidence**: `high`
- **Evidence**: turns 4-7
- **Notes**: Campus context emphasized

- **Requirement ID**: FR-003
- **Title**: In-app chat
- **Description**: Buyer and seller can communicate in app.
- **Primary user / actor**: Student
- **Related workflow / scenario**: Student trade flow
- **Inputs**: Chat messages
- **System behavior**: Deliver/store conversation
- **Outputs / results**: Message thread
- **Priority**: `must`
- **Confidence**: `high`
- **Evidence**: turns 4-7
- **Notes**: Supports offline trade coordination

- **Requirement ID**: FR-004
- **Title**: Listing report and moderation
- **Description**: Users report suspicious listings; moderators review.
- **Primary user / actor**: Student / Teacher moderator
- **Related workflow / scenario**: Moderation flow
- **Inputs**: Report submission
- **System behavior**: Queue and process moderation actions
- **Outputs / results**: Moderation decision
- **Priority**: `must`
- **Confidence**: `high`
- **Evidence**: turn 7
- **Notes**: Audit history depth is open

---

## 8. Data and Information Requirements
### 8.1 Core Data Objects
- Name: Listing
- Description: Sell item record
- Key attributes: Title, description, media, price, seller
- Source: Student input
- Owner: Product system
- Sensitivity level: medium

- Name: Chat message
- Description: Buyer-seller communication
- Key attributes: Sender, receiver, content, timestamp
- Source: Student input
- Owner: Product system
- Sensitivity level: medium

### 8.2 Data Inputs
- Listing details, search queries, chat content, report reasons

### 8.3 Data Outputs
- Listing feeds, search results, chat threads, moderation outcomes

### 8.4 Data Quality Expectations
- Accuracy expectations: Listing info should be user-verified
- Timeliness expectations: Near-real-time chat and listing visibility
- Completeness expectations: Core listing fields required
- Consistency expectations: Unified campus-scoped listing behavior

### 8.5 Data Retention and Privacy Notes
- Privacy/compliance detail is partially defined and needs follow-up.

---

## 9. Non Functional Requirements
### 9.1 Performance
- Response time expectations: Posting should complete quickly
- Throughput expectations: `TBD`
- Scale expectations: `TBD`

### 9.2 Reliability
- Availability expectations: `TBD`
- Error tolerance expectations: Basic resilience for listing/chat/report paths
- Recovery expectations: `TBD`

### 9.3 Security
- Authentication needs: `TBD`
- Authorization needs: Role distinction for moderators
- Sensitive data handling: `TBD`
- Auditability expectations: Moderation history depth unresolved

### 9.4 Usability
- Ease of use expectations: Minimal-friction posting flow
- Accessibility expectations: `TBD`
- Learning curve expectations: Low

### 9.5 Maintainability
- Configuration expectations: `TBD`
- Extensibility expectations: Parent visibility can be added in later phase
- Operational maintenance expectations: Moderator operations support needed

### 9.6 Compatibility and Integration
- Required platforms: iOS (first release)
- Browsers / devices: iOS devices
- Systems to integrate with: `TBD`
- External dependencies: `TBD`

---

## 10. Constraints
### 10.1 Business Constraints
- Budget: `TBD`
- Timeline: First release scope constrained
- Staffing: `TBD`
- Policy constraints: Suspicious listing moderation required

### 10.2 Technical Constraints
- Required technologies: iOS-first implementation
- Existing systems: `TBD`
- Infrastructure limitations: `TBD`
- Deployment limitations: Platform scope restricted in v1

### 10.3 Legal / Compliance Constraints
- Regulatory requirements: `TBD`
- Privacy requirements: `TBD`
- Industry specific constraints: `TBD`

### 10.4 Organizational Constraints
- Process constraints: Moderator workflow required
- Approval constraints: `TBD`
- Cross team dependencies: `TBD`

---

## 11. Prioritization
### 11.1 High Priority Requirements
- Listing
- Search and browse
- In-app chat
- Report/moderation

### 11.2 Medium Priority Requirements
- Parent visibility (pending scope decision)

### 11.3 Low Priority Requirements
- Integrated online payment (deferred)

### 11.4 Priority Rationale
- Prioritize minimal complete trade loop and safety before expansion.

---

## 12. Assumptions
- Assumption: Basic moderation without deep audit trail may be acceptable initially
- Why it is assumed: Scope and complexity control
- Risk if false: Rework and compliance risk
- Validation needed: `yes`

---

## 13. Open Questions
- Question: Should parent visibility be in first release?
- Related topic: functional capabilities
- Why it matters: Direct scope and implementation impact
- Blocking level: `high`
- Recommended next action: Confirm with business owner

- Question: What moderation audit history depth is required?
- Related topic: constraints and moderation operations
- Why it matters: Affects data model and compliance posture
- Blocking level: `medium`
- Recommended next action: Run focused follow-up with moderation stakeholders

---

## 14. Conflicts and Inconsistencies
- Conflict ID: none
- Topic / slot: n/a
- Conflicting statements: n/a
- Source / evidence: n/a
- Impact: n/a
- Resolution status: `resolved`
- Recommended follow up: continue monitoring in follow-up interviews

---

## 15. Risk Assessment
### 15.1 Requirement Risks
- Parent visibility ambiguity may destabilize v1 scope.

### 15.2 Delivery Risks
- Moderation requirement expansion can increase implementation effort.

### 15.3 Adoption Risks
- If trust/safety signals are weak, users may avoid in-app trading flow.

### 15.4 Highest Priority Risks
- Scope shift from unresolved parent visibility
- Under-specified moderation audit requirements

---

## 16. Requirement Coverage Assessment
### 16.1 Covered Areas
- Product objective, users, workflows, core functions, constraints

### 16.2 Partially Covered Areas
- Success metrics breadth, moderation operations detail

### 16.3 Weakly Covered or Missing Areas
- Compliance specifics, integration requirements, budget/timeline precision

### 16.4 Coverage Summary
- Breadth of coverage: medium-high
- Depth of coverage: medium
- Confidence in completeness: medium

---

## 17. Recommended Next Steps
### 17.1 Immediate Next Steps
- Resolve parent visibility scope
- Define moderation audit depth

### 17.2 Follow Up Interviews or Workshops
- Business owner for release boundary decisions
- Moderation/operations stakeholders for policy and tooling requirements

### 17.3 Artifacts to Produce Next
- PRD
- user stories
- workflow diagrams
- moderation flow design notes

### 17.4 Readiness Assessment
- solution design: partial
- prototyping: yes
- backlog creation: partial
- stakeholder review: yes
- further elicitation only: required for unresolved items

---

## 18. Structured Summary Snapshot
### 18.1 Product Snapshot
- Product name: Campus second hand trading app
- Product type: Marketplace
- Core problem: Inefficient campus second hand trade process
- Primary users: Students
- Core value proposition: Fast and safer campus-local trading workflow

### 18.2 Requirement Snapshot
- Number of major topics covered: 6
- Number of high priority requirements: 4
- Number of open questions: 2
- Number of unresolved conflicts: 0
- Overall convergence level: medium-high

### 18.3 Final Assessment
The requirement set is structurally usable for next-step solution design, but two scope-critical uncertainties should be resolved before finalizing first-release commitments.

---

## Appendix A. Evidence Trace
- **Item**: Parent visibility scope
- **Type**: `requirement`
- **Supporting evidence**: turns 6-8
- **Confidence**: medium
- **Notes**: still open, impacts release boundary

- **Item**: Moderation capability requirement
- **Type**: `constraint`
- **Supporting evidence**: turn 7
- **Confidence**: high
- **Notes**: baseline confirmed; audit depth pending

## Appendix B. Raw Notes
- Placeholder for additional observations captured during interview and synthesis.
```

## Post-Summary Lifecycle Transition (Required)

After this summarize flow finishes, do not hard-delete the session immediately.
Follow the current two-phase lifecycle model:

1. Confirm final summary has been generated successfully.
2. Mark the session as closed:
   - `metadata.status = "closed"`
   - `metadata.closed_at = <timestamp>`
   - `framework.session.status = "closed"`
   - `framework.session.closed_at = <timestamp>`
3. Persist the closure as a new immutable revision under:
   - `state/sessions/{session_id}/revisions/r{n}/`
   - then atomically switch `state/sessions/{session_id}/CURRENT` to that revision.
4. Keep checkpoints and revision history for delayed cleanup; do not remove the session directory in this step.
5. Cleanup job behavior:
   - archive only sessions already marked `closed`
   - delete only after retention threshold from `state/archive/`
6. Conversation mapping behavior:
   - remove `conversation_index.json` mapping during archive/delete transition
   - archived sessions are not restored through the old `conversation_id` mapping.
