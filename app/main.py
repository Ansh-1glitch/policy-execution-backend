import uuid
from datetime import datetime
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas import PolicyIngestRequest, TaskSchema, AuditLogSchema, TaskStatus, TaskUpdateStatusRequest, TaskEscalateRequest

app = FastAPI()

from app.db import get_db

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/policies/ingest", response_model=list[TaskSchema])
async def ingest_policy(request: PolicyIngestRequest):
    db = get_db()
    # 1. Save Policy
    policy_doc = request.model_dump()
    policy_doc["status"] = "ACTIVE"
    await db.policies.insert_one(policy_doc)

    created_tasks = []
    audit_logs = []

    # 2. Process Rules -> Tasks
    for rule in request.rules:
        task_id = str(uuid.uuid4())
        
        # Normalize deadline
        deadline = rule.deadline if rule.deadline else "Not specified"

        task = TaskSchema(
            task_id=task_id,
            policy_id=request.policy_id,
            rule_id=rule.rule_id,
            task_name=f"Execute rule {rule.rule_id}",
            assigned_role=rule.responsible_role,
            status=TaskStatus.CREATED,
            deadline=deadline
        )
        created_tasks.append(task)

        # 3. Create Audit Log
        log = AuditLogSchema(
            task_id=task_id,
            action="TASK_CREATED",
            performed_by_role="SYSTEM",
            timestamp=datetime.utcnow()
        )
        audit_logs.append(log)

    # Bulk Insert
    if created_tasks:
        await db.tasks.insert_many([t.model_dump() for t in created_tasks])
    
    if audit_logs:
        await db.audit_logs.insert_many([l.model_dump() for l in audit_logs])

    return created_tasks

@app.get("/tasks", response_model=list[TaskSchema])
async def get_tasks(role: str):
    db = get_db()
    query = {}
    # Case-insensitive check for Admin
    if role.lower() != "admin":
        # Case-insensitive regex for assigned_role
        query["assigned_role"] = {"$regex": f"^{role}$", "$options": "i"}

    tasks = []
    cursor = db.tasks.find(query)
    async for document in cursor:
        document["_id"] = str(document["_id"])
        tasks.append(document)
    
    return tasks

@app.post("/tasks/{task_id}/update-status", response_model=TaskSchema)
async def update_task_status(task_id: str, request: TaskUpdateStatusRequest):
    from fastapi import HTTPException
    db = get_db()

    task = await db.tasks.find_one({"task_id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    current_status = task["status"]
    new_status = request.new_status

    valid_transitions = {
        "CREATED": ["ASSIGNED"],
        "ASSIGNED": ["IN_PROGRESS"],
        "IN_PROGRESS": ["COMPLETED", "ESCALATED"],
        "COMPLETED": [],
        "ESCALATED": []
    }

    if new_status not in valid_transitions.get(current_status, []):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid transition from {current_status} to {new_status}"
        )

    await db.tasks.update_one(
        {"task_id": task_id},
        {"$set": {"status": new_status}}
    )
    
    log = AuditLogSchema(
        task_id=task_id,
        action=f"STATUS_UPDATE: {current_status} -> {new_status}",
        performed_by_role=request.role,
        timestamp=datetime.utcnow()
    )
    await db.audit_logs.insert_one(log.model_dump())

    updated_task = await db.tasks.find_one({"task_id": task_id})
    updated_task["_id"] = str(updated_task["_id"])
    return updated_task

@app.post("/tasks/{task_id}/escalate", response_model=TaskSchema)
async def escalate_task(task_id: str, request: TaskEscalateRequest):
    from fastapi import HTTPException
    db = get_db()

    task = await db.tasks.find_one({"task_id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    current_role = task["assigned_role"]
    
    escalation_path = {
        "Clerk": "Officer",
        "Officer": "Admin"
    }
    
    next_role = None
    for role_key, role_val in escalation_path.items():
        if role_key.lower() == current_role.lower():
            next_role = role_val
            break
    
    if not next_role:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot escalate from {current_role}. Already at highest level or invalid role."
        )

    await db.tasks.update_one(
        {"task_id": task_id},
        {"$set": {
            "assigned_role": next_role,
            "status": "ESCALATED"
        }}
    )
    
    log = AuditLogSchema(
        task_id=task_id,
        action=f"ESCALATION: {current_role} -> {next_role}",
        performed_by_role=request.role,
        timestamp=datetime.utcnow()
    )
    await db.audit_logs.insert_one(log.model_dump())

    updated_task = await db.tasks.find_one({"task_id": task_id})
    updated_task["_id"] = str(updated_task["_id"])
    return updated_task
