
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    
    # Scan first 20 rows
    for r in range(min(20, len(df))):
        row = df.iloc[r].values
        for c, val in enumerate(row):
            s_val = str(val).lower()
            if "trimestre" in s_val:
                print(f"Found 'trimestre' at Row {r}, Col {c}: {val}")
            
except Exception as e:
    print(e)
