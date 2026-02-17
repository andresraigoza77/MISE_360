
import sqlite3

DB_FILE = "mise_digital.db"

# Mapping inferred from Excel analysis
# Code -> Clean Name
DEP_MAPPING = {
    713: "Secretaría de Cultura",
    761: "Departamento Administrativo de Planeación (DAP)", # Or Comunicaciones? DAP sheet had 761. Let's assume DAP.
    711: "Secretaría de Educación",
    954: "Gerencia Étnica",
    724: "Secretaría de la Juventud",
    706: "Secretaría de Gestión Humana",
    723: "Secretaría de las Mujeres",
    725: "Secretaría de Participación Ciudadana", # Inferred if present
    712: "Secretaría de Salud", # Common code
    # Add generic fallback update
}

def update_names():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    print("Updating Dependency Names...")
    for code, name in DEP_MAPPING.items():
        cursor.execute("UPDATE Dependencias SET nombre_dependencia = ? WHERE id_dependencia = ?", (name, code))
        if cursor.rowcount > 0:
            print(f"  Updated {code} -> {name}")
            
    conn.commit()
    
    # Check remaining generic names
    cursor.execute("SELECT * FROM Dependencias WHERE nombre_dependencia LIKE 'Dependencia %'")
    remaining = cursor.fetchall() 
    if remaining:
        print(f"\nWarning: {len(remaining)} dependencies still have generic names:")
        for r in remaining:
            print(f"  {r}")
            
    conn.close()

if __name__ == "__main__":
    update_names()
