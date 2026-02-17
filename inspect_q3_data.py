
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    
    print("--- Checking Data in Col 30 (Q3) ---")
    for r in range(8, 20):
        if r < len(df):
            val = df.iloc[r, 30]
            print(f"Row {r}: {val} (Type: {type(val)})")

except Exception as e:
    print(e)
