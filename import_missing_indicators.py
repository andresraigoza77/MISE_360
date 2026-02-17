
import pandas as pd
import sqlite3
import os

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

def import_indicators():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    total_inserted = 0
    seen_ids = set()
    
    for f, default_dep in FILE_MAP.items():
        if not os.path.exists(f): continue
        print(f"Scanning {f}...")
        
        try:
            xl = pd.ExcelFile(f)
            target_sheet = None
            header_row = 0
            
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
                
                print(f"  Processing Sheet: {s}")
                df = df_raw # Already parsed
                headers = [str(x).lower().strip() for x in df.iloc[header_row].values]
            
                
                col_id = next((i for i, x in enumerate(headers) if "código indicador" in x or "codigo indicador" in x), None)
                col_name = next((i for i, x in enumerate(headers) if "nombre indicador" in x or "nombre del indicador" in x or "indicador" in x and "código" not in x), None)
                col_meta = next((i for i, x in enumerate(headers) if "meta del plan" in x or "meta 2024" in x or "meta cuatrienio" in x), None)
                col_dep = next((i for i, x in enumerate(headers) if "dependencia" in x), None)

                if col_id is None or col_name is None:
                    # print(f"Skipping {s}: ID={col_id}, Name={col_name}")
                    continue

                # print(f"  Processing {s} Cols: ID={col_id}")

                for i in range(header_row + 1, len(df)):
                    row = df.iloc[i]
                    try:
                        val_id = row[col_id]
                        if pd.isna(val_id) or not str(val_id).replace('.','').isdigit(): continue
                        id_ind = int(float(str(val_id)))
                        seen_ids.add(id_ind)
                        
                        name = str(row[col_name]).strip()
                        meta = 0.0
                        if col_meta is not None:
                            try: meta = float(row[col_meta])
                            except: pass
                        
                        dep_id = default_dep
                        if dep_id is None: dep_id = 110 
                        
                        try:
                            c.execute("""
                                INSERT INTO Indicadores (id_indicador, nombre_indicador, meta_total, id_dependencia_responsable)
                                VALUES (?, ?, ?, ?)
                            """, (id_ind, name, meta, dep_id))
                            total_inserted += 1
                        except sqlite3.IntegrityError:
                            pass
                            
                    except Exception as ex: 
                        pass
                    
        except Exception as e:
            print(f"File error: {e}")

    conn.commit()
    print(f"✅ Imported {total_inserted} new indicators.")
    print(f"📊 Total Unique Source IDs found: {len(seen_ids)}")
    
if __name__ == "__main__":
    import_indicators()
