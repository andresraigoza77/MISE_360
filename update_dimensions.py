
import pandas as pd
import sqlite3
import os

# Copy FILE_MAP from etl_process_v7.py
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

def update_dimensions():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    updated_count = 0
    
    for f in FILE_MAP:
        if not os.path.exists(f): continue
        print(f"Processing {f}...")
        
        try:
            xl = pd.ExcelFile(f)
            target_sheet = None
            header_row = 0
            
            # Iterate Sheets
            for s in xl.sheet_names:
                df_raw = xl.parse(s, header=None)
                target_sheet = False
                header_row = 0
                
                for r in range(min(20, len(df_raw))):
                    row = [str(x).lower() for x in df_raw.iloc[r].values]
                    if any("código indicador" in v for v in row):
                        target_sheet = True
                        header_row = r
                        break
                
                if not target_sheet: continue
                
                df = df_raw
                headers = [str(x).lower().strip() for x in df.iloc[header_row].values]
            
                
                col_id = None
                col_pob = None
                col_terr = None
                
                for idx, val in enumerate(headers):
                    if "código indicador" in val: col_id = idx
                    if "población objetivo" in val: col_pob = idx
                    if "comunas" in val and "corregimientos" in val: col_terr = idx
                
                if col_id is None: 
                    # print(f"  ❌ ID Column not found in {s}")
                    continue
                    
                # print(f"  Sheet {s} Columns: ID={col_id}, Pob={col_pob}, Terr={col_terr}")
                
                # Update DB
                for i in range(header_row + 1, len(df)):
                    row = df.iloc[i]
                    try:
                        val_id = row[col_id]
                        if pd.isna(val_id) or not str(val_id).replace('.','').isdigit(): continue
                        id_ind = int(float(str(val_id)))
                        
                        pob = str(row[col_pob]).strip() if col_pob is not None and pd.notna(row[col_pob]) else None
                        terr = str(row[col_terr]).strip() if col_terr is not None and pd.notna(row[col_terr]) else None
                        
                        if pob or terr:
                            c.execute("UPDATE Indicadores SET poblacion = ?, territorial = ? WHERE id_indicador = ?", (pob, terr, id_ind))
                            updated_count += 1
                    except: continue
                
        except Exception as e:
            print(f"  Error {f}: {e}")

    conn.commit()
    conn.close()
    print(f"✅ Dimensions updated for {updated_count} indicators.")

if __name__ == "__main__":
    update_dimensions()
