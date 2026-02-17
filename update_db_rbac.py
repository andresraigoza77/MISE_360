
import sqlite3
from passlib.context import CryptContext

DB_NAME = "mise_digital.db"
# Use a valid scheme configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def migrate_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    print("1. Creating Usuarios table...")
    c.execute("""
    CREATE TABLE IF NOT EXISTS Usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        rol TEXT NOT NULL CHECK(rol IN ('Capturista', 'Validador', 'Consolidador', 'Analista', 'Decisor')),
        id_dependencia INTEGER,
        FOREIGN KEY (id_dependencia) REFERENCES Dependencias (id_dependencia)
    );
    """)

    print("2. Adding 'estado' column to Reportes_Trimestrales...")
    try:
        # Check if column exists
        c.execute("SELECT estado FROM Reportes_Trimestrales LIMIT 1")
    except sqlite3.OperationalError:
        # Column doesn't exist, add it
        c.execute("ALTER TABLE Reportes_Trimestrales ADD COLUMN estado TEXT DEFAULT 'Borrador'")
        print("   Column 'estado' added.")
    else:
        print("   Column 'estado' already exists.")

    print("3. Seeding Test Users...")
    try:
        c.execute("DELETE FROM Usuarios WHERE email LIKE '%@misedigital.com'")
    except: pass

    test_users = [
        ("Juan Captura", "capturista@misedigital.com", "123456", "Capturista", 711), # Educación
        ("Maria Valida", "validador@misedigital.com", "123456", "Validador", 711),
        ("Pedro Consolida", "consolidador@misedigital.com", "123456", "Consolidador", None),
        ("Ana Analista", "analista@misedigital.com", "123456", "Analista", None),
        ("Carlos Decisor", "decisor@misedigital.com", "123456", "Decisor", None)
    ]

    for name, email, pwd, role, dep_id in test_users:
        try:
            hashed = get_password_hash(pwd)
            c.execute("INSERT INTO Usuarios (nombre, email, password_hash, rol, id_dependencia) VALUES (?, ?, ?, ?, ?)",
                      (name, email, hashed, role, dep_id))
            print(f"   Created user: {role} ({email})")
        except sqlite3.IntegrityError:
            print(f"   User {email} already exists.")
        except Exception as e:
            print(f"   Error creating user {email}: {e}")

    conn.commit()
    conn.close()
    print("Migration and Seeding Complete.")

if __name__ == "__main__":
    migrate_db()
