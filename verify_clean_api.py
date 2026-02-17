
import requests

try:
    # Login
    r = requests.post("http://localhost:8000/token", data={"username": "decisor@misedigital.com", "password": "medellin2026"})
    if r.status_code != 200:
        print(f"❌ Login failed: {r.text}")
        exit()
    token = r.json()['access_token']
    
    # Get KPIs
    r = requests.get("http://localhost:8000/dashboard/kpis", headers={"Authorization": f"Bearer {token}"})
    if r.status_code != 200:
        print(f"❌ KPI fetch failed: {r.text}")
        exit()
        
    data = r.json()
    print("✅ KPI Data Recalibrated:")
    print(f"  Global Compliance: {data.get('global_compliance')}%")
    print(f"  Total Indicators: {data.get('total_indicators')}")
    print(f"  Dependencies count: {len(data.get('dependencies', []))}")
    if data.get('dependencies'):
        print(f"  Top Dependency: {data['dependencies'][0]}")

    # Check alert count
    print(f"  Alerts count: {len(data.get('alerts', []))}")

except Exception as e:
    print(f"❌ Error: {e}")
