"""
Deep debug of Habu API to understand why cleanrooms aren't showing
"""
import asyncio
import httpx
import json
from config.habu_config import habu_config

async def deep_debug():
    """Try various approaches to find cleanrooms"""
    print("🔍 Deep Debug: Finding Missing Cleanrooms")
    print("=" * 60)
    
    headers = await habu_config.get_auth_headers()
    base_url = habu_config.base_url
    
    async with httpx.AsyncClient() as client:
        
        # 1. Try different cleanroom endpoints with various filters
        cleanroom_variants = [
            "/cleanrooms",
            "/cleanrooms?status=active", 
            "/cleanrooms?status=inactive",
            "/cleanrooms?status=draft",
            "/cleanrooms?includeInactive=true",
            "/cleanrooms?include=inactive",
            "/cleanrooms?all=true",
            "/cleanrooms?filter=all",
            "/cleanrooms?scope=all",
            "/cleanrooms?view=all",
        ]
        
        print("1. Testing cleanroom endpoint variations:")
        print("-" * 40)
        
        for endpoint in cleanroom_variants:
            try:
                response = await client.get(f"{base_url}{endpoint}", headers=headers, timeout=10.0)
                data = response.json() if response.status_code == 200 else None
                count = len(data) if isinstance(data, list) else "N/A"
                print(f"  {endpoint:<40} -> {response.status_code} (count: {count})")
                
                if response.status_code == 200 and data and isinstance(data, list) and len(data) > 0:
                    print(f"    ✅ FOUND DATA: {data[0]}")
                    
            except Exception as e:
                print(f"  {endpoint:<40} -> ERROR: {e}")
        
        # 2. Try to access resources that might give us clues
        print(f"\n2. Testing related endpoints:")
        print("-" * 40)
        
        related_endpoints = [
            "/questions",  # Global questions
            "/templates",  # Global templates  
            "/organizations",
            "/users",
            "/roles",
            "/permissions",
            "/data-connections",
            "/credentials",
        ]
        
        for endpoint in related_endpoints:
            try:
                response = await client.get(f"{base_url}{endpoint}", headers=headers, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    count = len(data) if isinstance(data, list) else len(data.keys()) if isinstance(data, dict) else "unknown"
                    print(f"  {endpoint:<20} -> 200 (items: {count})")
                    
                    # If we find data, show a sample
                    if isinstance(data, list) and data:
                        print(f"    Sample: {list(data[0].keys()) if isinstance(data[0], dict) else data[0]}")
                    elif isinstance(data, dict) and data:
                        print(f"    Keys: {list(data.keys())}")
                        
                elif response.status_code == 404:
                    print(f"  {endpoint:<20} -> 404")
                else:
                    print(f"  {endpoint:<20} -> {response.status_code}")
                    
            except Exception as e:
                print(f"  {endpoint:<20} -> ERROR: {e}")
        
        # 3. Try HTTP methods other than GET
        print(f"\n3. Testing different HTTP methods on /cleanrooms:")
        print("-" * 40)
        
        methods = ["POST", "PUT", "PATCH"]
        for method in methods:
            try:
                response = await client.request(method, f"{base_url}/cleanrooms", headers=headers, timeout=10.0)
                print(f"  {method:<10} -> {response.status_code}")
                if response.status_code not in [404, 405]:  # Method not allowed is expected
                    print(f"    Response: {response.text[:100]}")
            except Exception as e:
                print(f"  {method:<10} -> ERROR: {e}")
        
        # 4. Check if there are headers or query params we're missing
        print(f"\n4. Testing with different headers:")
        print("-" * 40)
        
        header_variants = [
            {**headers, "X-Organization-ID": "15106e2b-7205-4caf-a2b0-01ca64befe20"},
            {**headers, "X-Tenant-ID": "15106e2b-7205-4caf-a2b0-01ca64befe20"},
            {**headers, "Organization": "ICDC_Demo"},
            {**headers, "Tenant": "ICDC_Demo"},
            {**headers, "Accept": "application/json, */*"},
        ]
        
        for i, test_headers in enumerate(header_variants):
            try:
                response = await client.get(f"{base_url}/cleanrooms", headers=test_headers, timeout=10.0)
                data = response.json() if response.status_code == 200 else None
                count = len(data) if isinstance(data, list) else "N/A"
                extra_header = list(set(test_headers.keys()) - set(headers.keys()))[0] if len(test_headers) > len(headers) else "modified Accept"
                print(f"  With {extra_header:<20} -> {response.status_code} (count: {count})")
                
                if response.status_code == 200 and data and isinstance(data, list) and len(data) > 0:
                    print(f"    ✅ FOUND DATA WITH HEADERS: {data[0]}")
                    
            except Exception as e:
                print(f"  Header variant {i+1:<15} -> ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(deep_debug())