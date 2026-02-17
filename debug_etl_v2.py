
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    
    print("--- Searching for Quarters ---")
    for r in range(min(15, len(df))):
        row = [str(x).lower() for x in df.iloc[r].values]
        has_q = False
        for val in row:
            if "trimestre" in val:
                has_q = True
                break
        
        if has_q:
            print(f"Row {r} has 'trimestre'")
            for i, val in enumerate(row):
                if "trimestre" in val or "trim" in val or "iv" in val or "iii" in val:
                    print(f"  Col {i}: {val}")
                        
except Exception as e:
    print(e)
