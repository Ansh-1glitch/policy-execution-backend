import asyncio
import httpx

BASE_URL = "http://localhost:8000"

async def test_analytics():
    async with httpx.AsyncClient() as client:
        # 1. Test Performance
        print("\n1. Testing /analytics/performance...")
        resp = await client.get(f"{BASE_URL}/analytics/performance")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✅ Success. Range: {data.get('range')}, Data Points: {len(data.get('data', []))}")
        else:
            print(f"   ❌ Failed: {resp.status_code}")

        # 2. Test Storage
        print("\n2. Testing /system/storage...")
        resp = await client.get(f"{BASE_URL}/system/storage")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✅ Success. Total: {data.get('total_storage_gb')}GB, Used: {data.get('used_storage_gb')}GB")
        else:
            print(f"   ❌ Failed: {resp.status_code}")

        # 3. Test Health
        print("\n3. Testing /system/health...")
        resp = await client.get(f"{BASE_URL}/system/health")
        if resp.status_code == 200:
            data = resp.json()
            metrics = data.get('metrics', [])
            print(f"   ✅ Success. Metrics: {[m['name'] for m in metrics]}")
        else:
            print(f"   ❌ Failed: {resp.status_code}")

if __name__ == "__main__":
    asyncio.run(test_analytics())
