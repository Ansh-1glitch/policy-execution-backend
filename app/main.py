import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas import (
    PolicyIngestRequest, TaskSchema, AuditLogSchema, TaskStatus, 
    TaskUpdateStatusRequest, TaskEscalateRequest,
    SaveNLPResultRequest, NLPResultSchema
)
from app.pdf_generator import generate_policy_pdf

app = FastAPI()

# CORS Configuration - Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]  # Required for PDF downloads
)

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
async def get_tasks(role: str = None):
    """
    Get tasks, optionally filtered by role.
    
    Args:
        role: Optional role filter (Admin, Officer, Clerk)
              If not provided, returns all tasks
    
    Returns:
        List of tasks (all tasks or filtered by role)
    """
    db = get_db()
    query = {}
    
    # Only filter by role if role parameter is provided
    if role:
        # Case-insensitive check for Admin
        if role.lower() != "admin":
            # Case-insensitive regex for assigned_role
            query["assigned_role"] = {"$regex": f"^{role}$", "$options": "i"}
        # If role is Admin, query remains empty (returns all tasks)

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

@app.get("/audit-logs")
async def get_audit_logs(limit: int = 50):
    """
    Get audit trail of all task actions
    Returns logs in reverse chronological order (newest first)
    """
    db = get_db()
    
    logs = []
    cursor = db.audit_logs.find().sort("timestamp", -1).limit(limit)
    
    async for document in cursor:
        document["_id"] = str(document["_id"])
        # Format timestamp to HH:MM
        if isinstance(document.get("timestamp"), datetime):
            document["timestamp"] = document["timestamp"].strftime("%H:%M")
        logs.append(document)
    
    return logs

@app.get("/activity/recent")
async def get_recent_activity(limit: int = 20):
    """
    Get recent system activity for timeline display
    """
    from datetime import datetime, timedelta
    db = get_db()
    
    activities = []
    
    # Get recent audit logs and convert to activities
    cursor = db.audit_logs.find().sort("timestamp", -1).limit(limit)
    
    async for log in cursor:
        # Determine activity type and description based on action
        action = log.get("action", "")
        activity_type = "processing"
        title = "Task Action"
        description = action
        
        if "CREATED" in action:
            activity_type = "upload"
            title = "Task Created"
            description = f"New task created for {log.get('performed_by_role', 'System')}"
        elif "STATUS_UPDATE" in action:
            activity_type = "processing"
            title = "Task Status Updated"
            description = action
        elif "ESCALATION" in action:
            activity_type = "approval"
            title = "Task Escalated"
            description = action
        
        # Calculate relative time
        timestamp = log.get("timestamp")
        if isinstance(timestamp, datetime):
            time_diff = datetime.utcnow() - timestamp
            if time_diff.seconds < 3600:
                time_ago = f"{time_diff.seconds // 60} minutes ago"
            elif time_diff.seconds < 86400:
                time_ago = f"{time_diff.seconds // 3600} hours ago"
            else:
                time_ago = f"{time_diff.days} days ago"
        else:
            time_ago = "recently"
        
        activity = {
            "id": str(log.get("_id", "")),
            "type": activity_type,
            "title": title,
            "description": description,
            "timestamp": time_ago,
            "user": log.get("performed_by_role", "System"),
            "status": "completed"
        }
        activities.append(activity)
    
    return activities

@app.get("/policies/stats")
async def get_policy_stats():
    """
    Get policy and task statistics for dashboard metrics
    """
    db = get_db()
    
    # Count policies
    total_policies = await db.policies.count_documents({})
    active_policies = await db.policies.count_documents({"status": "ACTIVE"})
    
    # Count tasks by status
    total_tasks = await db.tasks.count_documents({})
    created_tasks = await db.tasks.count_documents({"status": "CREATED"})
    assigned_tasks = await db.tasks.count_documents({"status": "ASSIGNED"})
    in_progress_tasks = await db.tasks.count_documents({"status": "IN_PROGRESS"})
    completed_tasks = await db.tasks.count_documents({"status": "COMPLETED"})
    escalated_tasks = await db.tasks.count_documents({"status": "ESCALATED"})
    
    return {
        "total_policies": total_policies,
        "active_policies": active_policies,
        "completed_policies": 0,  # Can be calculated based on all tasks completed
        "pending_policies": total_policies - active_policies,
        "total_tasks": total_tasks,
        "created_tasks": created_tasks,
        "assigned_tasks": assigned_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completed_tasks": completed_tasks,
        "escalated_tasks": escalated_tasks
    }

# NLP Results Endpoints

@app.post("/nlp-results/save")
async def save_nlp_result(request: SaveNLPResultRequest):
    """
    Save NLP processing results to database
    
    This endpoint stores the complete NLP output including all extracted rules
    and metadata for later retrieval and PDF generation.
    """
    db = get_db()
    
    result_id = str(uuid.uuid4())
    
    nlp_result = {
        "result_id": result_id,
        "policy_id": request.policy_id,
        "file_name": request.file_name,
        "upload_timestamp": datetime.utcnow(),
        "nlp_data": request.nlp_data,
        "status": "completed"
    }
    
    await db.nlp_results.insert_one(nlp_result)
    
    return {
        "result_id": result_id,
        "message": "NLP results saved successfully"
    }

@app.get("/nlp-results")
async def get_nlp_results():
    """
    Get list of all NLP processing results
    
    Returns metadata for all stored NLP results without the full data payload.
    """
    db = get_db()
    
    results = []
    cursor = db.nlp_results.find().sort("upload_timestamp", -1)
    
    async for document in cursor:
        document["_id"] = str(document["_id"])
        # Don't include full nlp_data in list view
        result_summary = {
            "result_id": document["result_id"],
            "policy_id": document["policy_id"],
            "file_name": document["file_name"],
            "upload_timestamp": document["upload_timestamp"].isoformat(),
            "status": document["status"]
        }
        results.append(result_summary)
    
    return results

@app.get("/nlp-results/{result_id}")
async def get_nlp_result(result_id: str):
    """
    Get specific NLP result by ID
    
    Returns the complete NLP data including all rules and metadata.
    """
    db = get_db()
    
    result = await db.nlp_results.find_one({"result_id": result_id})
    
    if not result:
        raise HTTPException(status_code=404, detail="NLP result not found")
    
    result["_id"] = str(result["_id"])
    result["upload_timestamp"] = result["upload_timestamp"].isoformat()
    
    return result

@app.get("/nlp-results/{result_id}/download-pdf")
async def download_pdf(result_id: str):
    """
    Download PDF of NLP results
    
    Generates and returns a formatted PDF document containing the policy rules
    and metadata extracted by the NLP system.
    """
    db = get_db()
    
    # Fetch NLP result from database
    result = await db.nlp_results.find_one({"result_id": result_id})
    
    if not result:
        raise HTTPException(status_code=404, detail="NLP result not found")
    
    # Generate PDF
    try:
        pdf_buffer = generate_policy_pdf(
            nlp_data=result["nlp_data"],
            file_name=result["file_name"]
        )
        
        # Create filename
        safe_policy_id = result["policy_id"].replace("/", "_").replace("\\", "_")
        filename = f"policy_{safe_policy_id}.pdf"
        
        # Return PDF as streaming response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating PDF: {str(e)}"
        )
