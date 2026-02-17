
import sqlite3

def fix_remaining():
    conn = sqlite3.connect('mise_digital.db')
    cursor = conn.cursor()
    
    # 722 -> Inclusión Social (SISF)
    cursor.execute("UPDATE Dependencias SET nombre_dependencia='Secretaría de Inclusión Social, Familia y DDHH' WHERE id_dependencia=722")
    if cursor.rowcount > 0:
        print("Updated 722 -> Secretaría de Inclusión Social, Familia y DDHH")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_remaining()
