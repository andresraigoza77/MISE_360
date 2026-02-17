
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    if sh not in xl.sheet_names:
        for s in xl.sheet_names:
            if "seguimiento" in s.lower() and "2025" in s.lower(): sh = s
    
    df = xl.parse(sh, header=None)
    print(f"Sheet: {sh}")
    print("--- Inspecting Col 4 (Rows 8-20) ---")
    for r in range(8, 20):
        if r < len(df):
            val = df.iloc[r, 4]
            print(f"Row {r}: {val} (Type: {type(val)})")
            
except Exception as e:
    print(e)
