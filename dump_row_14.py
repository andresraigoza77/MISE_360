
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    if sh not in xl.sheet_names:
        for s in xl.sheet_names:
            if "seguimiento" in s.lower() and "2025" in s.lower(): sh = s
    
    df = xl.parse(s, header=None)
    
    r = 14
    if r < len(df):
        row = df.iloc[r].values
        print(f"--- Row {r} Content ---")
        for i, val in enumerate(row):
            s = str(val).strip()
            if s and s.lower() != 'nan':
                 print(f"Col {i}: {s}")
            
except Exception as e:
    print(e)
