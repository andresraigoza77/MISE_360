
import pandas as pd
import os
import sqlite3

def check_files():
    db_file = "mise_digital.db"
    report_file = "compact_report.txt"
    new_files = [
        "020226_SPC_301225.xlsx", "030226_GerenciaÉtnica.xlsx", "090226_SISF_301225.xlsx",
        "230126_Mujeres__MISE.xlsx", "230126_SGHSC_300925.xlsx", "260126_DAP.xlsx", "270126_Sec_Educación.xlsx"
    ]
    
    conn = sqlite3.connect(db_file)
    existing_ids = set([r[0] for r in conn.execute("SELECT id_indicador FROM Indicadores").fetchall()])
    conn.close()
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("-" * 80 + "\n")
        f.write(f"{'File':<30} | {'Sheet':<20} | {'Total':<5} | {'New':<5}\n")
        f.write("-" * 80 + "\n")
        
        for file_path in new_files:
            if not os.path.exists(file_path):
                f.write(f"{file_path[:20]}.. | Not Found\n")
                continue
            try:
                xl = pd.ExcelFile(file_path)
                found = False
                for s in xl.sheet_names:
                    df = xl.parse(s, header=None)
                    for r in range(min(15, len(df))):
                        # Safe string conversion
                        row_vals = [str(x).lower() for x in df.iloc[r].values]
                        if any("código indicador" in v for v in row_vals):
                            total = 0
                            new_cnt = 0
                            col_idx = [i for i,x in enumerate(row_vals) if "código indicador" in x][0]
                            
                            for i in range(r+1, len(df)):
                                v = df.iloc[i, col_idx]
                                if pd.notna(v) and str(v).replace('.','').isdigit():
                                    total += 1
                                    if int(float(str(v))) not in existing_ids:
                                        new_cnt += 1
                                        
                            f.write(f"{file_path:<30} | {s[:20]:<20} | {total:<5} | {new_cnt:<5}\n")
                            found = True
                            break
                    if found: break
                if not found: f.write(f"{file_path:<30} | No Valid Sheet\n")
            except Exception as e:
                f.write(f"{file_path:<30} | Error: {str(e)[:10]}\n")
        f.write("-" * 80 + "\n")

if __name__ == "__main__":
    check_files()
