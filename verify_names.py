
import requests

API_URL = "http://localhost:8000"

def verify_names():
    try:
        # Login
        r = requests.post(f"{API_URL}/token", data={"username": "capturista@misedigital.com", "password": "medellin2026"})
        token = r.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get Data
        r_kpi = requests.get(f"{API_URL}/dashboard/kpis", headers=headers)
        data = r_kpi.json()
        
        deps = data.get('dependencies', [])
        print(f"Top 3 Dependencies:")
        for d in deps[:3]:
            print(f"- {d['nombre_dependencia']} ({d['cumplimiento']:.1f}%)")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_names()
