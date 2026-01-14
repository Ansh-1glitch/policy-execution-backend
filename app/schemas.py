from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ESCALATED = "ESCALATED"

class PolicySchema(BaseModel):
    policy_id: str
    status: str = "ACTIVE"

class TaskSchema(BaseModel):
    task_id: str
    policy_id: str
    rule_id: str
    task_name: str
    assigned_role: str
    status: TaskStatus
    deadline: str

class AuditLogSchema(BaseModel):
    task_id: str
    action: str
    performed_by_role: str
    timestamp: datetime

class IngestRule(BaseModel):
    rule_id: str
    action: str
    responsible_role: str
    deadline: Optional[str] = None

class PolicyIngestRequest(BaseModel):
    policy_id: str
    rules: list[IngestRule]

class TaskUpdateStatusRequest(BaseModel):
    new_status: TaskStatus
    role: str

class TaskEscalateRequest(BaseModel):
    role: str

# NLP Results Schemas
class NLPResultSchema(BaseModel):
    result_id: str
    policy_id: str
    file_name: str
    upload_timestamp: datetime
    nlp_data: dict
    status: str = "completed"

class SaveNLPResultRequest(BaseModel):
    policy_id: str
    file_name: str
    nlp_data: dict
