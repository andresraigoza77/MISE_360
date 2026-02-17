
import pandas as pd
import os
import sqlite3

def check_files():
    db_file = "mise_digital.db"
    report_file = "analysis_report_v2.txt"
    new_files = [
        "020226_SPC_301225.xlsx", 
        "030226_GerenciaÉtnica.xlsx", 
        "090226_SISF_301225.xlsx",
        "230126_Mujeres__MISE.xlsx", 
        "230126_SGHSC_300925.xlsx", 
        "260126_DAP.xlsx", 
        "270126_Sec_Educación.xlsx"
    ]
    
    conn = sqlite3.connect(db_file)
    existing_ids = set([r[0] for r in conn.execute("SELECT id_indicador FROM Indicadores").fetchall()])
    conn.close()
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"Existing Indicators in DB: {len(existing_ids)}\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'File':<30} | {'Sheet':<20} | {'Total':<5} | {'New':<5} | {'Exist'}\n")
        f.write("-" * 80 + "\n")
        
        for file_path in new_files:
            if not os.path.exists(file_path):
                f.write(f"{file_path:<30} | {'Not Found':<20} | {'-':<5} | {'-':<5} | {'-'}\n")
                continue
                
            try:
                xl = pd.ExcelFile(file_path)
                target_sheet = None
                
                # Sheet search
                for s in xl.sheet_names:
                    df = xl.parse(s, header=None)
                    for r in range(min(15, len(df))):
                        # Safe string conversion
                        row_vals = [str(x).lower() for x in df.iloc[r].values]
                        if any("código indicador" in v for v in row_vals):
                            target_sheet = s
                            
                            # Find ID column
                            col_idx = -1
                            for idx, val in enumerate(row_vals):
                                if "código indicador" in val:
                                    col_idx = idx
                                    break
                            
                            # Count
                            count = 0
                            new_count = 0
                            exist_count = 0
                            
                            for i in range(r + 1, len(df)):
                                val = df.iloc[i, col_idx]
                                if pd.notna(val) and str(val).replace('.','').isdigit():
                                    count += 1
                                    indic_id = int(float(str(val)))
                                    if indic_id in existing_ids:
                                        exist_count += 1
                                    else:
                                        new_count += 1
                            
                            f.write(f"{file_path:<30} | {s[:20]:<20} | {count:<5} | {new_count:<5} | {exist_count}\n")
                            break
                    if target_sheet: break
                
                if not target_sheet:
                    f.write(f"{file_path:<30} | {'No Valid Sheet':<20} | {'-':<5} | {'-':<5} | {'-'}\n")
                    
            except Exception as e:
                f.write(f"{file_path:<30} | Error: {str(e)[:20]}...\n")

if __name__ == "__main__":
    check_files()
