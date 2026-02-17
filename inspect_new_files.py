
import pandas as pd
import os

NEW_FILES = [
    "020226_SPC_301225.xlsx",
    "030226_GerenciaÉtnica.xlsx",
    "090226_SISF_301225.xlsx",
    "230126_Mujeres__MISE.xlsx",
    "230126_SGHSC_300925.xlsx",
    "260126_DAP.xlsx",
    "270126_Sec_Educación.xlsx"
]

def check_structure(file_path):
    print(f"\nAnalyzing: {file_path}")
    try:
        xl = pd.ExcelFile(file_path)
        sheet_names = xl.sheet_names
        print(f"  Sheets: {sheet_names}")
        
        valid_sheets = []
        for s in sheet_names:
            # Heuristic: usually sheets starting with 'Matriz' or just the first big sheet
            # Let's inspect the sheet with most data or specific name
            df = xl.parse(s, header=None)
            
            # 1. Look for Dependency Name
            dep_name = "Unknown"
            # Scan first 10 rows for "Dependencia" or similar? 
            # Or reliance on file name?
            # User asked to IDENTIFY dependency.
            
            # 2. Look for "Código Indicador" column
            has_id = False
            has_q1 = False
            has_q4 = False
            
            # Scan for headers
            for r in range(min(15, len(df))):
                row_str = df.iloc[r].astype(str).str.lower().values
                if any('código indicador' in x for x in row_str):
                    has_id = True
                if any('trimestre i ' in x for x in row_str) and any('2025' in x for x in row_str):
                    has_q1 = True
                if any('trimestre iv' in x for x in row_str):
                    has_q4 = True
                    
            if has_id:
                valid_sheets.append(s)
                print(f"  [OK] Sheet '{s}' has 'Código Indicador'. Quarters found: Q1={has_q1}, Q4={has_q4}")
            else:
                print(f"  [WARN] Sheet '{s}' missing 'Código Indicador'")
                
        if not valid_sheets:
            print("  [FAIL] No valid sheets found with indicator structure.")
            
    except Exception as e:
        print(f"  Error reading file: {e}")

if __name__ == "__main__":
    for f in NEW_FILES:
        if os.path.exists(f):
            check_structure(f)
        else:
            print(f"File not found: {f}")
