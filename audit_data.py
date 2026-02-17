
import pandas as pd
import sqlite3
import os

# Map from etl_process_v7.py
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

def audit_data():
    print("--- 🔍 Starting Data Audit ---")
    
    # 1. Count Source Rows
    total_source = 0
    details = {}
    
    for f, dep_id in FILE_MAP.items():
        if not os.path.exists(f): 
            print(f"⚠️ File missing: {f}")
            continue
            
        try:
            xl = pd.ExcelFile(f)
            # Find Data Sheet logic from ETL (searching for "Código Indicador")
            target_sheet = None
            start_row = 0
            
            for s in xl.sheet_names:
                df_raw = xl.parse(s, header=None)
                # Quick search for header in first 15 rows
                for r in range(min(20, len(df_raw))):
                    row_vals = [str(x).lower() for x in df_raw.iloc[r].values]
                    if any("código indicador" in v for v in row_vals):
                        target_sheet = s
                        start_row = r + 1
                        break
                if target_sheet: break
            
            if target_sheet:
                df = xl.parse(target_sheet, header=None)
                # Count valid rows (assuming col 0 or 1 is ID)
                # ETL uses dynamic column search, but let's assume if we found header, we count rows below
                # that have a numeric-like ID in the ID column.
                # We'll just count total rows minus header for a rough estimate, or try to be precise?
                # Let's count non-empty IDs.
                
                # Check column index again?
                # Re-finding id col
                df_head = xl.parse(target_sheet, header=None)
                id_col = None
                row_head = df_head.iloc[start_row-1]
                for c, val in enumerate(row_head):
                    if "código indicador" in str(val).lower():
                        id_col = c
                        break
                
                if id_col is not None:
                    count = 0
                    for i in range(start_row, len(df)):
                        val = df.iloc[i, id_col]
                        if pd.notna(val) and str(val).replace('.','').isdigit():
                            count += 1
                    total_source += count
                    details[f] = count
                    print(f"  📄 {f}: {count} indicators found.")
                else:
                    print(f"  ❌ Could not identify ID column in {f}")

        except Exception as e:
            print(f"  ❌ Error reading {f}: {e}")

    print(f"\n📊 Total Source Indicators: {total_source}")

    # 2. Count DB Rows
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    db_count = c.execute("SELECT count(*) FROM Indicadores").fetchone()[0]
    conn.close()
    
    print(f"🗄️ Total DB Indicators: {db_count}")
    
    diff = total_source - db_count
    if diff == 0:
        print("✅ MATCH: Data load is consistent.")
    else:
        print(f"⚠️ MISMATCH: Discrepancy of {diff} indicators.")

if __name__ == "__main__":
    audit_data()
