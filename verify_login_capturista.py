
import requests

API_URL = "http://localhost:8000"
USER = "capturista@misedigital.com"
PASS = "medellin2026"

def test_login():
    print(f"Testing login for {USER}...")
    try:
        resp = requests.post(f"{API_URL}/token", data={"username": USER, "password": PASS})
        if resp.status_code == 200:
            token = resp.json()['access_token']
            print("Login Successful!")
            print(f"Token received: {token[:20]}...")
            
            # Verify Role
            headers = {"Authorization": f"Bearer {token}"}
            me = requests.get(f"{API_URL}/users/me", headers=headers)
            if me.status_code == 200:
                user_data = me.json()
                print(f"User Data: {user_data}")
                if user_data['rol'] == 'Capturista':
                    print("✅ Role Verified: Capturista")
                    
                    # Verify Access to Indicators
                    dep_id = user_data['id_dependencia']
                    print(f"Fetching indicators for Dep ID: {dep_id}...")
                    inds = requests.get(f"{API_URL}/indicadores/{dep_id}", headers=headers)
                    if inds.status_code == 200:
                        print(f"✅ Access to Indicators Confirmed. Count: {len(inds.json())}")
                    else:
                        print(f"❌ Failed to fetch indicators: {inds.status_code} - {inds.text}")
                else:
                    print(f"❌ Incorrect Role: {user_data['rol']}")
            else:
                print(f"❌ Failed to get user details: {me.status_code}")
        else:
            print(f"❌ Login Failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_login()
