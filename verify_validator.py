
import requests
import time

API_URL = "http://localhost:8000"

def verify():
    # 1. Login Capturista
    s = requests.Session()
    resp = s.post(f"{API_URL}/token", data={"username": "capturista@misedigital.com", "password": "medellin2026"})
    if resp.status_code != 200:
        print("❌ Capturista Login Failed")
        return
    cap_token = resp.json()['access_token']
    print("✅ Capturista Login OK")

    # Get User Dep ID
    headers_cap = {"Authorization": f"Bearer {cap_token}"}
    me = s.get(f"{API_URL}/users/me", headers=headers_cap).json()
    dep_id = me['id_dependencia']
    print(f"Capturista Dep ID: {dep_id}")

    # 2. Capturista submits report
    inds = s.get(f"{API_URL}/indicadores/{dep_id}", headers=headers_cap).json()
    if not inds or not isinstance(inds, list):
        print(f"❌ No indicators for Capturista (Resp: {inds})")
        return
    
    ind_id = inds[0]['id_indicador']
    print(f"Using Indicator {ind_id} for test")

    payload = {
        "id_indicador": ind_id,
        "trimestre": 3,
        "valor_ejecutado": 50,
        "observaciones": "Test Report for Validation"
    }
    resp = s.post(f"{API_URL}/reportes/update", json=payload, headers=headers_cap)
    if resp.status_code == 200 and resp.json()['estado'] == 'Enviado':
        print(f"✅ Report Submitted (Enviado) for Ind {ind_id}")
    else:
        print(f"❌ Report Submission Failed: {resp.text}")
        return

    # 3. Login Validator
    resp = s.post(f"{API_URL}/token", data={"username": "validador@misedigital.com", "password": "medellin2026"})
    if resp.status_code != 200:
        print("❌ Validator Login Failed")
        return
    val_token = resp.json()['access_token']
    print("✅ Validator Login OK")

    # 4. Check visibility
    headers_val = {"Authorization": f"Bearer {val_token}"}
    inds_val = s.get(f"{API_URL}/indicadores/{dep_id}", headers=headers_val).json() # Use dynamic dep_id
    
    if isinstance(inds_val, dict):
        print(f"❌ Validator Get Indicators Failed (Dict Returned): {inds_val}")
        return
        
    print(f"Validator Indicators Count: {len(inds_val)}")
    
    found = False
    for i in inds_val:
        if i['id_indicador'] == ind_id:
            rep = i['reportes'].get('3')
            if rep and rep['estado'] == 'Enviado':
                print(f"✅ Validator sees report for Ind {ind_id}")
                found = True
                break
    if not found:
        print("❌ Validator CANNOT see the report")
        return

    # 5. Approve
    review_payload = {
        "id_indicador": ind_id,
        "trimestre": 3,
        "accion": "Aprobar"
    }
    resp = s.post(f"{API_URL}/reportes/review", json=review_payload, headers=headers_val)
    if resp.status_code == 200 and resp.json()['estado'] == 'Validado':
        print("✅ Report Approved Successfully")
    else:
        print(f"❌ Approval Failed: {resp.text}")

if __name__ == "__main__":
    verify()
