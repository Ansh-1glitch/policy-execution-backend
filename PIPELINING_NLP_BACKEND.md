# NLP -> Backend Pipelining Guide

## 1. Overview
**Purpose**: This pipeline bridges the gap between the AI/NLP Policy Parser and the Execution Engine.
**Function**: The backend accepts structured policy rules extracted by the NLP system, persists the policy, and automatically generates executable **Tasks** and **Audit Logs** for each rule. These tasks are then available for human agents (Clerks, Officers) to execute.

## 2. Backend URLs

### Execution Backend (This Backend)
`https://policy-execution-backend.onrender.com`

### NLP Backend (AI Model)
`https://eighty-clubs-stop.loca.lt`

**Note:** NLP backend uses localtunnel - URL may change on server restart.

## 3. Required Endpoint for NLP
- **Method**: `POST`
- **Path**: `/policies/ingest`
- **Purpose**: Ingest a parsed policy and generate execution tasks.

## 4. Request Payload Contract
The backend expects a strict JSON structure. Extra fields (e.g., `confidence_score`, `metadata`) are **ignored** and will not cause errors.

### Structure
```json
{
  "policy_id": "string (Required)",
  "rules": [
    {
      "rule_id": "string (Required)",
      "action": "string (Required)",
      "responsible_role": "string (Required)",
      "deadline": "string (Optional)"
    }
  ]
}
```

### Field Details
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `policy_id` | `str` | **Yes** | Unique identifier for the policy document. |
| `rules` | `list` | **Yes** | List of extracted rules. |
| `rule_id` | `str` | **Yes** | Unique ID for the rule (e.g., "RULE-001"). |
| `action` | `str` | **Yes** | The action to be performed (e.g., "Verify age"). |
| `responsible_role` | `str` | **Yes** | The role assigned to this task (e.g., "Clerk"). |
| `deadline` | `str` | No | Natural language string (e.g., "30 days"). Defaults to "Not specified" if missing/empty. |

## 5. Rules Processing Logic
1.  **Iteration**: The backend iterates through every item in the `rules` list.
2.  **Task Generation**: For **each** rule, exactly one **Task** is created in the database.
3.  **Mapping**:
    - `rule.rule_id` → `task.rule_id`
    - `rule.responsible_role` → `task.assigned_role`
    - `rule.deadline` → `task.deadline`
    - `task.task_name` is auto-generated as: `"Execute rule {rule_id}"`
    - `task.status` is set to `"CREATED"`

## 6. Role Handling
- **Usage**: The `responsible_role` field directly determines who sees the task in their dashboard.
- **Normalization**: The backend stores the role **exactly as received** (case-sensitive storage).
- **Recommendation**: Use standard capitalized roles: `"Clerk"`, `"Officer"`, `"Admin"`.
- **Note**: Retrieval logic is case-insensitive, so `"clerk"` and `"Clerk"` are treated effectively the same by the dashboard API, but consistency is preferred.

## 7. Deadline Handling
- **Format**: Treated as a **String**. No date parsing is performed.
- **Values**: Accepts any string: `"30 days"`, `"Immediately"`, `"2025-12-31"`.
- **Missing/Empty**: If `deadline` is `null`, missing, or `""` (empty string), the backend automatically sets it to `"Not specified"`.

## 8. Backend Response
Returns a JSON list of the created tasks. The NLP system can use this to confirm successful creation.

```json
[
  {
    "task_id": "uuid-string",
    "policy_id": "POL-001",
    "rule_id": "RULE-A",
    "task_name": "Execute rule RULE-A",
    "assigned_role": "Clerk",
    "status": "CREATED",
    "deadline": "30 days"
  }
]
```

## 9. Error Scenarios
| Scenario | HTTP Status | Description |
| :--- | :--- | :--- |
| **Success** | `200 OK` | Tasks created successfully. |
| **Validation Error** | `422 Unprocessable Entity` | Missing required fields (`policy_id`, `rules`, `rule_id`, etc.) or wrong data types. |
| **Server Error** | `500 Internal Server Error` | Database connection failure or unexpected bug. |

**Note**: Extra fields in the JSON do **NOT** cause errors; they are silently stripped.

## 10. Minimal Example
**Valid JSON Payload:**
```json
{
  "policy_id": "POL-2024-001",
  "rules": [
    {
      "rule_id": "1.1",
      "action": "Verify applicant residency",
      "responsible_role": "Clerk",
      "deadline": "5 business days"
    },
    {
      "rule_id": "1.2",
      "action": "Approve final grant",
      "responsible_role": "Officer",
      "deadline": "" 
    }
  ]
}
```
*(In this example, the second rule's deadline will become "Not specified")*

## 11. Integration Checklist for NLP Engineer
- [ ] **Sanitize Output**: Ensure `rules` is a list of objects.
- [ ] **Verify Required Fields**: Ensure `rule_id`, `action`, and `responsible_role` are never null.
- [ ] **Handle Deadlines**: Pass whatever text is extracted; if none, pass `""` or omit the field.
- [ ] **Ignore Extras**: Don't worry about stripping `confidence_score` or `metadata`; the backend handles it.
- [ ] **Test**: Send the Minimal Example to `https://policy-execution-backend.onrender.com/policies/ingest` to verify connectivity.

## 12. Using Integration Utilities (Recommended)

We provide Python utilities to simplify integration:

### Validation
```python
from app.nlp_integration import validate_nlp_payload

is_valid, error = validate_nlp_payload(your_payload)
if not is_valid:
    print(f"Error: {error}")
```

### Transformation (Strip Extra Fields)
```python
from app.nlp_integration import transform_to_ingest_format

# Your NLP output can have extra fields
nlp_output = {
    "policy_id": "POL-001",
    "confidence_score": 0.95,  # Extra field - will be stripped
    "rules": [...]
}

# Clean payload ready for API
clean_payload = transform_to_ingest_format(nlp_output)
```

### Sample Payload Generation
```python
from app.nlp_integration import create_sample_payload

# Generate test payload with 3 rules
sample = create_sample_payload(num_rules=3)
```

### Testing
```bash
# Run comprehensive integration tests
python test_integration.py
```

**See [NLP_INTEGRATION_GUIDE.md](file:///c:/Users/kambo/Desktop/Hackathon/NLP_INTEGRATION_GUIDE.md) for detailed examples and troubleshooting.**
