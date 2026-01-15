import asyncio
import httpx
import uuid
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_policy_stats():
    policy_id = f"TEST-POL-{uuid.uuid4().hex[:8]}"
    print(f"Testing with Policy ID: {policy_id}")

    # 1. Ingest Policy
    ingest_payload = {
        "policy_id": policy_id,
        "rules": [
            {
                "rule_id": "R1",
                "action": "Test Action 1",
                "responsible_role": "Clerk",
                "deadline": "2 days"
            },
            {
                "rule_id": "R2",
                "action": "Test Action 2",
                "responsible_role": "Officer",
                "deadline": "5 days"
            },
            {
                "rule_id": "R3",
                "action": "Test Action 3",
                "responsible_role": "Admin",
                "deadline": "1 day"
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        print("\n1. Ingesting Policy...")
        response = await client.post(f"{BASE_URL}/policies/ingest", json=ingest_payload)
        if response.status_code != 200:
            print(f"❌ Ingest failed: {response.text}")
            return
        tasks = response.json()
        print(f"✅ Created {len(tasks)} tasks")

        # 2. Update some task statuses
        print("\n2. Updating Task Statuses...")
        # Task 1: Clerk -> COMPLETED
        task1_id = tasks[0]["task_id"]
        await client.post(f"{BASE_URL}/tasks/{task1_id}/update-status", json={"new_status": "ASSIGNED", "role": "Clerk"})
        await client.post(f"{BASE_URL}/tasks/{task1_id}/update-status", json={"new_status": "IN_PROGRESS", "role": "Clerk"})
        await client.post(f"{BASE_URL}/tasks/{task1_id}/update-status", json={"new_status": "COMPLETED", "role": "Clerk"})
        
        # Task 2: Officer -> IN_PROGRESS
        task2_id = tasks[1]["task_id"]
        await client.post(f"{BASE_URL}/tasks/{task2_id}/update-status", json={"new_status": "ASSIGNED", "role": "Officer"})
        await client.post(f"{BASE_URL}/tasks/{task2_id}/update-status", json={"new_status": "IN_PROGRESS", "role": "Officer"})

        # Task 3: Admin -> CREATED (No change)

        # 3. Get Policy Stats
        print(f"\n3. Fetching Stats for {policy_id}...")
        response = await client.get(f"{BASE_URL}/policies/stats/{policy_id}")
        if response.status_code != 200:
            print(f"❌ Get stats failed: {response.text}")
            return
        
        stats = response.json()
        print("\n📊 Policy Statistics:")
        print(f"Total Tasks: {stats['total_tasks']} (Expected: 3)")
        print(f"Completion Rate: {stats['completion_rate_percent']}% (Expected: 33%)")
        print("\nTasks by Status:")
        print(f"  CREATED: {stats['tasks_by_status']['CREATED']} (Expected: 1)")
        print(f"  IN_PROGRESS: {stats['tasks_by_status']['IN_PROGRESS']} (Expected: 1)")
        print(f"  COMPLETED: {stats['tasks_by_status']['COMPLETED']} (Expected: 1)")
        
        print("\nTasks by Role:")
        print(f"  Clerk: {stats['tasks_by_role'].get('Clerk', 0)} (Expected: 1)")
        print(f"  Officer: {stats['tasks_by_role'].get('Officer', 0)} (Expected: 1)")
        print(f"  Admin: {stats['tasks_by_role'].get('Admin', 0)} (Expected: 1)")

        # Verification
        assert stats['total_tasks'] == 3
        assert stats['completion_rate_percent'] == 33
        assert stats['tasks_by_status']['COMPLETED'] == 1
        assert stats['tasks_by_status']['IN_PROGRESS'] == 1
        assert stats['tasks_by_status']['CREATED'] == 1
        
        print("\n✅ VERIFICATION SUCCESSFUL!")

if __name__ == "__main__":
    asyncio.run(test_policy_stats())
