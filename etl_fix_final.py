
import pandas as pd
import sqlite3
import os
import re

# Specific Fix for Education File
FILE = "270126_Sec_Educación.xlsx"
DB_FILE = "mise_digital.db"

# Confirmed Configuration
ID_COL = 3       # "Código Indicador" at Row 7 (Index 3 based on inspection)
DATA_START = 8   # Data starts at Row 8
Q_COLS = {
    1: 24, # Trimestre I -> Resultado
    2: 27, # Trimestre II -> Resultado
    3: 30, # Trimestre III -> Resultado
    4: 33  # Trimestre IV -> Resultado
}

def clean_numeric(val):
    if pd.isna(val) or val == 'No aplica' or str(val).strip() == '' or str(val).lower() == 'nan':
        return None
    if isinstance(val, (int, float)):
        return val
    s = str(val).strip().replace(',', '.')
    s = re.sub(r'[^\d\.-]', '', s)
    try:
        return float(s)
    except:
        return None

def run_fix():
    if not os.path.exists(FILE):
        print(f"File {FILE} not found.")
        return

    print(f"Applying final fix for {FILE}...")
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025" 
    # Fallback
    if sh not in xl.sheet_names:
        for s in xl.sheet_names:
            if "seguimiento" in s.lower() and "2025" in s.lower():
                sh = s
                break
    
    print(f"Sheet: {sh}")
    df = xl.parse(sh, header=None)
    
    reportes_list = []
    
    for r in range(DATA_START, len(df)):
        try:
            row = df.iloc[r]
            id_eff = row[ID_COL]
            if pd.isna(id_eff) or not str(id_eff).replace('.','').isdigit(): continue
            id_ind = int(float(str(id_eff)))
            
            for q, col_idx in Q_COLS.items():
                if col_idx < len(row):
                    val = clean_numeric(row[col_idx])
                    if val is not None:
                         # Upsert
                         reportes_list.append((id_ind, 2025, q, None, val, None, None, None))
        except: continue
        
    print(f"Found {len(reportes_list)} report values to update for Education.")
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.executemany("""
        INSERT OR REPLACE INTO Reportes_Trimestrales
        (id_indicador, anio, trimestre, valor_programado, valor_ejecutado, avance_fisico, avance_financiero, observaciones)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, reportes_list)
    
    conn.commit()
    conn.close()
    print("Update Complete.")

if __name__ == "__main__":
    run_fix()
