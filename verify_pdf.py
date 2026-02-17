
import requests
import os

# Login to get token
API_URL = "http://localhost:8000"
TOKEN_URL = f"{API_URL}/token"
REPORT_URL = f"{API_URL}/reports/hallazgos"

def verify_pdf():
    # 1. Login
    creds = [
        ("decisor@misedigital.com", "mipasswordseguro"),
        ("capturista@misedigital.com", "mipasswordseguro"),
        ("validador@misedigital.com", "mipasswordseguro")
    ]
    
    token = None
    for u, p in creds:
        print(f"Trying login for {u}...")
        r = requests.post(TOKEN_URL, data={"username": u, "password": p})
        if r.status_code == 200:
            token = r.json()["access_token"]
            print(f"✅ Login successful for {u}")
            break
        else:
            print(f"❌ Login failed for {u}: {r.status_code}")
    
    if not token:
        print("All logins failed.")
        return
    
    # 2. Request PDF
    print("Requesting PDF...")
    headers = {"Authorization": f"Bearer {token}"}
    r_pdf = requests.get(REPORT_URL, headers=headers)
    
    if r_pdf.status_code == 200:
        with open("test_report.pdf", "wb") as f:
            f.write(r_pdf.content)
        size = os.path.getsize("test_report.pdf")
        print(f"✅ PDF Generated. Size: {size} bytes")
        if size > 1000:
            print("✅ PDF seems valid (size > 1KB).")
        else:
            print("⚠️ PDF is suspiciously small.")
    else:
        print(f"❌ Failed to get PDF: {r_pdf.status_code} - {r_pdf.text}")

if __name__ == "__main__":
    verify_pdf()
