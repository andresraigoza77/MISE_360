
import sqlite3

DB_FILE = "mise_digital.db"

def update_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 1. Ensure 'estado' exists in Reportes_Trimestrales
    try:
        c.execute("SELECT estado FROM Reportes_Trimestrales LIMIT 1")
    except sqlite3.OperationalError:
        print("Adding 'estado' column to Reportes_Trimestrales...")
        c.execute("ALTER TABLE Reportes_Trimestrales ADD COLUMN estado TEXT DEFAULT 'Borrador'")
    
    # 2. Create Comentarios_Revision table
    c.execute("""
        CREATE TABLE IF NOT EXISTS Comentarios_Revision (
            id_comentario INTEGER PRIMARY KEY AUTOINCREMENT,
            id_indicador INTEGER,
            trimestre INTEGER,
            anio INTEGER,
            comentario TEXT,
            fecha_comentario DATETIME DEFAULT CURRENT_TIMESTAMP,
            autor_email TEXT
        )
    """)
    print("Table Comentarios_Revision checked/created.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_db()
