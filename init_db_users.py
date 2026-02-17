
import sqlite3
from passlib.context import CryptContext

DB_FILE = "mise_digital.db"
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def init_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Create table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT,
            full_name TEXT,
            rol TEXT,
            id_dependencia INTEGER,
            hashed_password TEXT,
            disabled INTEGER DEFAULT 0
        )
    ''')
    
    users = [
        ("decisor@misedigital.com", None, "César Decisor", "Decisor", None, get_password_hash("mipasswordseguro")),
        ("capturista@misedigital.com", None, "Carlos Capturista", "Capturista", 1, get_password_hash("mipasswordseguro")),
        ("validador@misedigital.com", None, "Viviana Validadora", "Validador", None, get_password_hash("mipasswordseguro")),
        ("admin@misedigital.com", None, "Admin", "Admin", None, get_password_hash("secret"))
    ]
    
    print("Recreating users...")
    for u in users:
        try:
            c.execute("INSERT OR REPLACE INTO users (username, email, full_name, rol, id_dependencia, hashed_password) VALUES (?, ?, ?, ?, ?, ?)", u)
            print(f"User {u[0]} upserted.")
        except Exception as e:
            print(f"Error inserting {u[0]}: {e}")
            
    conn.commit()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    init_users()
