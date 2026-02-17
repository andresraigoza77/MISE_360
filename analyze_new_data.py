
import pandas as pd
import os
import sqlite3

def check_files():
    db_file = "mise_digital.db"
    new_files = [
        "020226_SPC_301225.xlsx", "030226_GerenciaÉtnica.xlsx", "090226_SISF_301225.xlsx",
        "230126_Mujeres__MISE.xlsx", "230126_SGHSC_300925.xlsx", "260126_DAP.xlsx", "270126_Sec_Educación.xlsx"
    ]
    
    conn = sqlite3.connect(db_file)
    existing_ids = set([r[0] for r in conn.execute("SELECT id_indicador FROM Indicadores").fetchall()])
    conn.close()
    
    print(f"Existing Indicators in DB: {len(existing_ids)}")
    print("-" * 60)
    print(f"{'File':<30} | {'Sheet':<20} | {'Total':<5} | {'New':<5} | {'Exist'}")
    print("-" * 60)
    
    for f in new_files:
        if not os.path.exists(f):
            print(f"{f:<30} | Not Found")
            continue
            
        try:
            xl = pd.ExcelFile(f)
            # Find relevant sheet
            target_sheet = None
            for s in xl.sheet_names:
                df = xl.parse(s, header=None)
                # Check for "Código Indicador" in first 15 rows
                for r in range(min(15, len(df))):
                    row_vals = [str(x).lower() for x in df.iloc[r].values]
                    if any("código indicador" in v for v in row_vals):
                        target_sheet = s
                        # Count valid IDs
                        col_idx = -1
                        for idx, val in enumerate(row_vals):
                            if "código indicador" in val:
                                col_idx = idx
                                break
                        
                        count = 0
                        new_count = 0
                        exist_count = 0
                        
                        for i in range(r + 1, len(df)):
                            val = df.iloc[i, col_idx]
                            if pd.notna(val) and str(val).replace('.','').isdigit():
                                count += 1
                                if int(float(str(val))) in existing_ids:
                                    exist_count += 1
                                else:
                                    new_count += 1
                        
                        print(f"{f:<30} | {s[:20]:<20} | {count:<5} | {new_count:<5} | {exist_count}")
                        break
                if target_sheet: break
            
            if not target_sheet:
                print(f"{f:<30} | No Valid Sheet Found")
                
        except Exception as e:
            print(f"{f:<30} | Error: {str(e)[:20]}")

if __name__ == "__main__":
    check_files()
