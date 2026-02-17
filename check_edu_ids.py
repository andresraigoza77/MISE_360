
import pandas as pd
import sqlite3

FILE = "270126_Sec_Educación.xlsx"
DB = "mise_digital.db"

try:
    # 1. Get IDs from Excel
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    if sh not in xl.sheet_names:
        for s in xl.sheet_names:
            if "seguimiento" in s.lower() and "2025" in s.lower(): sh = s
    
    df = xl.parse(sh, header=None)
    ids_excel = []
    # ID is Col 4, Row 8
    for r in range(8, len(df)):
        val = df.iloc[r, 4]
        if pd.notna(val) and str(val).replace('.','').isdigit():
            ids_excel.append(int(float(str(val))))
            
    ids_excel = list(set(ids_excel))
    print(f"Found {len(ids_excel)} IDs in Excel: {ids_excel}")
    
    # 2. Check DB
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    print("\n--- DB Status for these IDs ---")
    rows = c.execute(f"SELECT id_indicador, id_dependencia_responsable FROM Indicadores WHERE id_indicador IN ({','.join(map(str, ids_excel))})").fetchall()
    
    found_map = {r[0]: r[1] for r in rows}
    
    missing_in_db = [i for i in ids_excel if i not in found_map]
    wrong_dep = [i for i, d in found_map.items() if d != 711]
    
    print(f"Total found in DB: {len(found_map)}")
    print(f"Missing in DB: {missing_in_db}")
    print(f"Wrong Dependency (Not 711): {wrong_dep}")
    
    if wrong_dep:
        print("Sample Wrong Deps:", [(i, found_map[i]) for i in wrong_dep[:5]])
        
    conn.close()

except Exception as e:
    print(e)
