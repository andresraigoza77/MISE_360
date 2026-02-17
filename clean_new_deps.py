
import sqlite3

def clean_deps():
    conn = sqlite3.connect('mise_digital.db')
    c = conn.cursor()
    
    updates = {
        725: "Secretaría de Participación Ciudadana",
        761: "Departamento Administrativo de Planeación (DAP)",
        723: "Secretaría de las Mujeres",
        706: "Secretaría de Gestión Humana y SC",
        954: "Gerencia Étnica",
        711: "Secretaría de Educación",
        713: "Secretaría de Cultura",
        722: "Secretaría de Inclusión Social, Familia y DDHH",
        724: "Secretaría de la Juventud",
        712: "Secretaría de Salud" # Just in case
    }
    
    print("Updating dependency names...")
    for code, name in updates.items():
        c.execute("UPDATE Dependencias SET nombre_dependencia = ? WHERE id_dependencia = ?", (name, code))
        if c.rowcount > 0:
            print(f"  Updated {code} -> {name}")
            
    conn.commit()
    
    # Check remaining
    remaining = c.execute("SELECT * FROM Dependencias WHERE nombre_dependencia LIKE 'Dependencia %'").fetchall()
    if remaining:
        print(f"\nRemaining generic dependencies: {len(remaining)}")
        for r in remaining:
            print(f"  {r}")
    else:
        print("\nAll dependencies have clean names.")
        
    conn.close()

if __name__ == "__main__":
    clean_deps()
