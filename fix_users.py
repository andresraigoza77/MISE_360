
import sqlite3
# import hashlib # Removed
from auth import get_password_hash # Import from auth.py

DB_FILE = "mise_digital.db"
DEFAULT_PASS = "medellin2026"

def get_spc_id(cursor):
    cursor.execute("SELECT id_dependencia FROM Dependencias WHERE nombre_dependencia LIKE '%Planeaci%'")
    res = cursor.fetchone()
    if res: return res[0]
    return 110 # Fallback

def fix_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    spc_id = get_spc_id(c)
    print(f"Using Dependency ID: {spc_id}")

    users = [
        (1, "Capturista SPC", "capturista@misedigital.com", "Capturista", spc_id),
        (2, "Validador SPC", "validador@misedigital.com", "Validador", spc_id),
        (3, "Decisor SPC", "decisor@misedigital.com", "Decisor", spc_id)
    ]

    # Generate bcrypt hash
    # We use get_password_hash from auth.py which uses passlib
    pass_hash = get_password_hash(DEFAULT_PASS)
    print(f"Generated hash: {pass_hash[:10]}...")

    for uid, name, email, rol, dep_id in users:
        c.execute("SELECT email FROM Usuarios WHERE email=?", (email,))
        if not c.fetchone():
            c.execute("INSERT INTO Usuarios (id_usuario, nombre, email, password_hash, rol, id_dependencia) VALUES (?, ?, ?, ?, ?, ?)",
                      (uid, name, email, pass_hash, rol, dep_id))
            print(f"Inserted {email}")
        else:
            # Update password to ensure it matches bcrypt format
            c.execute("UPDATE Usuarios SET password_hash=?, rol=?, id_dependencia=? WHERE email=?",
                      (pass_hash, rol, dep_id, email))
            print(f"Updated {email} with new hash.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_users()
