
import pandas as pd
import sqlite3
import os
import re

# Configuration
# Map filename -> Dependency ID
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

def find_header_row_and_cols(df):
    found_cols = {
        'id_ind': None,
        'nombre_ind': None, 'subdim': None, 'dep_cod': None,
        'proj_cod': None, 'meta': None, 'linea_base': None,
        'trim_1': None, 'trim_2': None, 'trim_3': None, 'trim_4': None
    }
    header_row_idx = -1

    for r in range(min(15, len(df))):
        row_vals = [str(x).lower() for x in df.iloc[r].values]
        for c, val in enumerate(row_vals):
            if 'código indicador' in val:
                found_cols['id_ind'] = c
                header_row_idx = r 
            elif 'subdimensión' in val:
                found_cols['subdim'] = c
            elif ('código dependencia' in val) or ('responsables' in val and 'dependencia' in val):
                found_cols['dep_cod'] = c
            elif 'código' in val and 'proyecto' in val:
                found_cols['proj_cod'] = c
            elif 'meta' in val and 'indicador' in val:
                found_cols['meta'] = c
            elif 'línea base' in val:
                found_cols['linea_base'] = c
            
            # Quarters - RELAXED MATCHING
            # Ideally Q1 should have 2025, but Q2-Q4 might not.
            # We enforce "2025" for Q1 to avoid confusing with other years if present,
            # but for Q2-Q4 we just look for "trimestre ii", etc.
            
            if 'trimestre i ' in val and '2025' in val: 
                found_cols['trim_1'] = c
            elif 'trimestre ii' in val: 
                found_cols['trim_2'] = c
            elif 'trimestre iii' in val: 
                found_cols['trim_3'] = c
            elif 'trimestre iv' in val: 
                found_cols['trim_4'] = c
            
    return found_cols, header_row_idx + 1

def run_etl():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    total_reps = 0
    
    for file_path, forced_dep_id in FILE_MAP.items():
        if not os.path.exists(file_path): continue
            
        print(f"Processing {file_path}...")
        try:
            xl = pd.ExcelFile(file_path)
            # Find valid sheet
            target_sheet = None
            cols = None
            start_row = 0
            
            for s in xl.sheet_names:
                df_raw = xl.parse(s, header=None)
                c, sr = find_header_row_and_cols(df_raw)
                if c['id_ind'] is not None:
                    target_sheet = s
                    cols = c
                    start_row = sr
                    break
            
            if not target_sheet: continue
            
            df = xl.parse(target_sheet, header=None)
            reportes_list = []
            
            for i in range(start_row, len(df)):
                row = df.iloc[i]
                try:
                    # ID
                    id_eff = row[cols['id_ind']]
                    if pd.isna(id_eff) or not str(id_eff).replace('.','').isdigit(): continue
                    id_indicador = int(float(str(id_eff)))
                    
                    # Quarters
                    q_map = {1: cols['trim_1'], 2: cols['trim_2'], 3: cols['trim_3'], 4: cols['trim_4']}
                    for q, col_idx in q_map.items():
                        if col_idx is not None:
                            val = clean_numeric(row[col_idx])
                            # If val is None, we might still want to insert a record with NULL if we want to show it in the dashboard as "missing"
                            # But dashboard shows "Reportados" if val > 0 usually?
                            # The dashboard uses LEFT JOIN Reportes on id_indicador. If no row, it gets NULL.
                            # If we want to capture "Obs" or just update values:
                            if val is not None:
                                reportes_list.append((id_indicador, 2025, q, None, val, None, None, None))
                except: continue

            # Update Reports
            # We use INSERT OR REPLACE. If row existed, it updates.
            cursor.executemany("""
                INSERT OR REPLACE INTO Reportes_Trimestrales
                (id_indicador, anio, trimestre, valor_programado, valor_ejecutado, avance_fisico, avance_financiero, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, reportes_list)
            
            print(f"  Updated {len(reportes_list)} reports.")
            total_reps += len(reportes_list)
            conn.commit()

        except Exception as e:
            print(f"  Error: {e}")

    print(f"\nTotal Reports Updated: {total_reps}")
    c = cursor.execute("SELECT count(*) FROM Reportes_Trimestrales").fetchone()[0]
    print(f"Total Reports in DB: {c}")
    conn.close()

if __name__ == "__main__":
    run_etl()
