
import requests

URL = "http://127.0.0.1:8000/token"

def test_login():
    # Test valid user (from seed)
    payload = {
        "username": "capturista@misedigital.com",
        "password": "123456" # Correct seed password
                          # Wait, the migration script CAUGHT the exception for Decisor but others might have worked if < 72 bytes.
                          # "123456" is < 72 bytes. 
                          # Re-check migration output: "Created user: Capturista..."
                          # So password should be "123456"
    }
    
    try:
        print(f"Attempting login with {payload['username']}...")
        response = requests.post(URL, data=payload)
        
        if response.status_code == 200:
            print("Login Successful!")
            print(response.json())
        else:
            print(f"Login Failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()
