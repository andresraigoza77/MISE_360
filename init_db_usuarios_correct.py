
import sqlite3
from passlib.context import CryptContext

DB_FILE = "mise_digital.db"
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def init_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Drop incorrect 'users' table
    c.execute("DROP TABLE IF EXISTS users")
    print("Dropped table 'users'.")

    # Ensure 'Usuarios' exists (it should, based on inspect)
    # But let's check content length
    c.execute("SELECT count(*) FROM Usuarios")
    count = c.fetchone()[0]
    print(f"Current rows in Usuarios: {count}")
    
    # Clear existing users to be safe or upsert? 
    # Since there is no UNIQUE constraint on email (maybe?), better to delete specific ones or just clear all for demo.
    # Let's clear all for clean state.
    c.execute("DELETE FROM Usuarios")
    print("Cleared 'Usuarios' table.")
    
    users = [
        # nombre, email, password_hash, rol, id_dependencia
        ("César Decisor", "decisor@misedigital.com", get_password_hash("mipasswordseguro"), "Decisor", None),
        ("Carlos Capturista", "capturista@misedigital.com", get_password_hash("mipasswordseguro"), "Capturista", 1),
        ("Viviana Validadora", "validador@misedigital.com", get_password_hash("mipasswordseguro"), "Validador", None),
        ("Admin", "admin@misedigital.com", get_password_hash("secret"), "Admin", None)
    ]
    
    print("Recreating users in Usuarios...")
    for u in users:
        try:
            c.execute("INSERT INTO Usuarios (nombre, email, password_hash, rol, id_dependencia) VALUES (?, ?, ?, ?, ?)", u)
            print(f"User {u[1]} inserted.")
        except Exception as e:
            print(f"Error inserting {u[1]}: {e}")
            
    conn.commit()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    init_users()
