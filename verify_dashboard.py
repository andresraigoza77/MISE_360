
import requests
import sys

API_URL = "http://localhost:8000"

def verify_dashboard():
    # 1. Login Decisor
    s = requests.Session()
    resp = s.post(f"{API_URL}/token", data={"username": "decisor@misedigital.com", "password": "medellin2026"})
    if resp.status_code != 200:
        print("❌ Decisor Login Failed")
        return
    token = resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Decisor Login OK")

    # 2. Get KPIs
    resp = s.get(f"{API_URL}/dashboard/kpis", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ KPIs Received: Global={data.get('global_compliance')}%")
        print(f"   Dependencies Count: {len(data.get('dependencies', []))}")
        print(f"   Alerts Count: {len(data.get('alerts', []))}")
    else:
        print(f"❌ KPIs Failed: {resp.status_code} - {resp.text}")

    # 3. Export Report
    print("Testing Export...")
    resp = s.get(f"{API_URL}/reports/export", headers=headers)
    if resp.status_code == 200:
        if resp.headers.get('content-type') == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            print(f"✅ Export Success: Received Excel ({len(resp.content)} bytes)")
            with open("test_export.xlsx", "wb") as f:
                f.write(resp.content)
        else:
            print(f"❌ Export Failed: Wrong Content-Type ({resp.headers.get('content-type')})")
    else:
        print(f"❌ Export Failed: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    verify_dashboard()
