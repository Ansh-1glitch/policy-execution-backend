import asyncio
import httpx
import uuid

BASE_URL = "http://localhost:8000"

async def test_reset_db():
    # 1. Create Initial Data (Policy A)
    print("\n1. Creating Initial Data (Policy A)...")
    policy_id_a = f"TEST-POL-A-{uuid.uuid4().hex[:8]}"
    payload_a = {
        "policy_id": policy_id_a,
        "rules": [{"rule_id": "R1", "action": "Action A", "responsible_role": "Admin"}]
    }
    
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/policies/ingest", json=payload_a)
        
        # Verify Policy A exists
        tasks = (await client.get(f"{BASE_URL}/tasks")).json()
        count_a = len([t for t in tasks if t['policy_id'] == policy_id_a])
        print(f"   Tasks for Policy A: {count_a}")
        assert count_a > 0

    # 2. Ingest Policy B with reset_db=True
    print("\n2. Ingesting Policy B with reset_db=True...")
    policy_id_b = f"TEST-POL-B-{uuid.uuid4().hex[:8]}"
    payload_b = {
        "policy_id": policy_id_b,
        "reset_db": True,
        "rules": [{"rule_id": "R2", "action": "Action B", "responsible_role": "Clerk"}]
    }
    
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/policies/ingest", json=payload_b)
        
        # 3. Verify Data
        print("\n3. Verifying Data...")
        tasks = (await client.get(f"{BASE_URL}/tasks")).json()
        
        # Check Policy A is gone
        count_a = len([t for t in tasks if t['policy_id'] == policy_id_a])
        print(f"   Tasks for Policy A: {count_a} (Expected: 0)")
        
        # Check Policy B exists
        count_b = len([t for t in tasks if t['policy_id'] == policy_id_b])
        print(f"   Tasks for Policy B: {count_b} (Expected: 1)")
        
        if count_a == 0 and count_b == 1:
            print("✅ SUCCESS: Database reset worked correctly")
        else:
            print("❌ FAILURE: Database reset failed")

if __name__ == "__main__":
    asyncio.run(test_reset_db())
