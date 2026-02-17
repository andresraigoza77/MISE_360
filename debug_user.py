
import sqlite3
from passlib.context import CryptContext

DB_NAME = "mise_digital.db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    email = "capturista@misedigital.com"
    pwd = "123" # Check 123
    pwd2 = "123456" # Check 123456
    
    print(f"Checking user {email}...")
    user = c.execute("SELECT password_hash FROM Usuarios WHERE email=?", (email,)).fetchone()
    
    if user:
        stored_hash = user[0]
        print(f"Stored Hash: {stored_hash[:10]}...") 
        
        if pwd_context.verify(pwd, stored_hash):
            print(f"MATCHES password '{pwd}'")
        elif pwd_context.verify(pwd2, stored_hash):
            print(f"MATCHES password '{pwd2}'")
        else:
            print("DOES NOT MATCH '123' OR '123456'")
            
            # Create new hash to compare
            new_hash = pwd_context.hash(pwd2)
            print(f"Expected hash for '{pwd2}': {new_hash[:10]}...")
            
    else:
        print("User not found.")
        
    conn.close()

if __name__ == "__main__":
    verify()
