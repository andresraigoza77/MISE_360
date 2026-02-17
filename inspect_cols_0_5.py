
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
    print("--- Inspecting Cols 0-5 (Rows 8-15) ---")
    for r in range(8, 15):
        if r < len(df):
            row = df.iloc[r, 0:6].values
            print(f"Row {r}: {[str(x)[:20] for x in row]}")
            
except Exception as e:
    print(e)
