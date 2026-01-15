import asyncio
import httpx
import uuid

BASE_URL = "http://localhost:8000"

async def test_filename_ingest():
    # Test Case 1: Ingest with file_name
    policy_id_1 = f"TEST-FILE-{uuid.uuid4().hex[:8]}"
    file_name_1 = "Employee_Handbook_2026.pdf"
    
    print(f"\n1. Testing Ingest WITH file_name ({file_name_1})...")
    
    payload_1 = {
        "policy_id": policy_id_1,
        "file_name": file_name_1,
        "rules": [
            {
                "rule_id": "R1",
                "action": "Verify handbook distribution",
                "responsible_role": "HR",
                "deadline": "5 days"
            }
        ]
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/policies/ingest", json=payload_1)
        if response.status_code != 200:
            print(f"❌ Ingest failed: {response.text}")
            return
            
        tasks = response.json()
        task = tasks[0]
        
        print(f"   Task created: {task['task_id']}")
        print(f"   File Name in Task: {task.get('file_name')}")
        
        if task.get('file_name') == file_name_1:
            print("✅ SUCCESS: file_name correctly saved in task")
        else:
            print(f"❌ FAILURE: Expected {file_name_1}, got {task.get('file_name')}")

    # Test Case 2: Ingest WITHOUT file_name (Backward Compatibility)
    policy_id_2 = f"TEST-NOFILE-{uuid.uuid4().hex[:8]}"
    print(f"\n2. Testing Ingest WITHOUT file_name...")
    
    payload_2 = {
        "policy_id": policy_id_2,
        # file_name omitted
        "rules": [
            {
                "rule_id": "R1",
                "action": "Legacy action",
                "responsible_role": "Admin"
            }
        ]
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/policies/ingest", json=payload_2)
        if response.status_code != 200:
            print(f"❌ Ingest failed: {response.text}")
            return
            
        tasks = response.json()
        task = tasks[0]
        
        print(f"   Task created: {task['task_id']}")
        print(f"   File Name in Task: {task.get('file_name')}")
        
        if task.get('file_name') is None:
            print("✅ SUCCESS: file_name is None as expected")
        else:
            print(f"❌ FAILURE: Expected None, got {task.get('file_name')}")

if __name__ == "__main__":
    asyncio.run(test_filename_ingest())
