
import pandas as pd
import sqlite3
import os
import re

# Configuration
FILE_MAP = {
    "SegIndic_PPPC_300625.xlsx": None, 
    "020226_SPC_301225.xlsx": 725, 
    "030226_GerenciaÉtnica.xlsx": 954, 
    "090226_SISF_301225.xlsx": 722, 
    "230126_Mujeres__MISE.xlsx": 723, 
    "230126_SGHSC_300925.xlsx": 706, 
    "260126_DAP.xlsx": 761, 
    "270126_Sec_Educación.xlsx": 711 
}

DB_FILE = "mise_digital.db"

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

def find_q_cols(df):
    # Search rows 5 to 10 for Quarter Headers
    q_starts = {1: None, 2: None, 3: None, 4: None}
    
    # helper to find "ejecutado" column near a start column
    def find_val_col(start_c, header_r):
        # Look in columns start_c to start_c + 8
        # And rows header_r to header_r + 2
        for r in range(header_r, min(header_r + 3, len(df))):
            for c in range(start_c, min(start_c + 12, df.shape[1])):
                val = str(df.iloc[r, c]).lower()
                if "ejecutado" in val and "presupuesto" not in val and "físico" not in val:
                    return c
                # Fallback: "valor" but be careful
                if "valor" in val and "ejecutado" in val:
                    return c
        return None

    for r in range(min(15, len(df))):
        row = [str(x).lower() for x in df.iloc[r].values]
        
        # Check for Quarter Headers
        for c, val in enumerate(row):
            # Q1
            if ("trimestre" in val and " i" in val and "ii" not in val) or ("start_q1" in val): # or other markers
                if not q_starts[1]: q_starts[1] = (c, r)
            # Q2
            if ("trimestre" in val and "ii" in val and "iii" not in val):
                if not q_starts[2]: q_starts[2] = (c, r)
            # Q3
            if ("trimestre" in val and "iii" in val):
                if not q_starts[3]: q_starts[3] = (c, r)
            # Q4
            if ("trimestre" in val and "iv" in val):
                if not q_starts[4]: q_starts[4] = (c, r)

    # Now find value columns
    val_cols = {1: None, 2: None, 3: None, 4: None}
    for q in range(1, 5):
        if q_starts[q]:
            c_start, r_start = q_starts[q]
            v_c = find_val_col(c_start, r_start)
            if v_c:
                val_cols[q] = v_c
            else:
                # If distinct "Ejecutado" column not found, maybe it's the SAME column?
                # (unlikely for "Trimestre" header, usually merged)
                # But let's assume if we found the header, the data is nearby.
                # If we fail to find "Ejecutado", we might try just looking for ANY column with data? No.
                # Let's trust the search.
                pass
    
    return val_cols

def run_etl():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    total_reps = 0
    
    for file_path, forced_dep_id in FILE_MAP.items():
        if not os.path.exists(file_path): continue
        print(f"Processing {file_path}...")
        
        try:
            xl = pd.ExcelFile(file_path)
            target_sheet = None
            id_col_idx = None
            header_row_idx = None
            
            # Find Sheet and ID col
            for s in xl.sheet_names:
                df_raw = xl.parse(s, header=None)
                for r in range(min(15, len(df_raw))):
                    row = [str(x).lower() for x in df_raw.iloc[r].values]
                    for c, val in enumerate(row):
                        if "código indicador" in val:
                            target_sheet = s
                            id_col_idx = c
                            header_row_idx = r + 1 # Data starts after
                            break
                    if target_sheet: break
                if target_sheet: break
            
            if not target_sheet: continue
            
            df = xl.parse(target_sheet, header=None)
            
            # Find Quarter Value Columns dynamically
            q_cols = find_q_cols(df)
            print(f"  Quarter Cols: {q_cols}")
            
            reportes_list = []
            for i in range(header_row_idx, len(df)):
                row = df.iloc[i]
                try:
                    # ID
                    id_eff = row[id_col_idx]
                    if pd.isna(id_eff) or not str(id_eff).replace('.','').isdigit(): continue
                    id_indicador = int(float(str(id_eff)))
                    
                    for q, col_idx in q_cols.items():
                        if col_idx is not None:
                            val = clean_numeric(row[col_idx])
                            if val is not None:
                                reportes_list.append((id_indicador, 2025, q, None, val, None, None, None))
                except: continue

            if reportes_list:
                cursor.executemany("""
                    INSERT OR REPLACE INTO Reportes_Trimestrales
                    (id_indicador, anio, trimestre, valor_programado, valor_ejecutado, avance_fisico, avance_financiero, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, reportes_list)
                print(f"  Upserted {len(reportes_list)} reports.")
                total_reps += len(reportes_list)
                conn.commit()

        except Exception as e:
            print(f"  Error: {e}")

    print(f"\nTotal Reports Updated: {total_reps}")
    conn.close()

if __name__ == "__main__":
    run_etl()
