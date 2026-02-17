
import sqlite3

def verify():
    conn = sqlite3.connect('mise_digital.db')
    c = conn.cursor()
    
    id_ind = 428
    print(f"--- Checking Indicator {id_ind} ---")
    
    # 1. Check Indicator Table
    row = c.execute("SELECT * FROM Indicadores WHERE id_indicador = ?", (id_ind,)).fetchone()
    print(f"Indicator Data: {row}")
    if row:
        print(f"Dependency ID: {row[-1]}") # Assuming last column is dep
    
    # 2. Check Reports
    rows = c.execute("SELECT trimestre, valor_ejecutado, observaciones FROM Reportes_Trimestrales WHERE id_indicador = ? AND anio = 2025 ORDER BY trimestre", (id_ind,)).fetchall()
    print(f"Reports (Found {len(rows)}):")
    for r in rows:
        print(f"  Q{r[0]}: Val={r[1]}, Obs={r[2]}")
        
    conn.close()

if __name__ == "__main__":
    verify()
